"""
Boxing and unboxing support for DataFrame, Series, etc.
"""
import datetime
import decimal
import warnings
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.ir_utils import GuardException, guard
from numba.core.typing import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, intrinsic, typeof_impl, unbox
from numba.np import numpy_support
from numba.typed.typeddict import Dict
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFramePayloadType, DataFrameType, check_runtime_cols_unsupported, construct_dataframe
from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType, typeof_pd_int_dtype
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType, PandasDatetimeTZDtype
from bodo.libs.str_arr_ext import string_array_type, string_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import BodoError, BodoWarning, dtype_to_array_type, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
ll.add_symbol('is_np_array', hstr_ext.is_np_array)
ll.add_symbol('array_size', hstr_ext.array_size)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
TABLE_FORMAT_THRESHOLD = 20
_use_dict_str_type = False


def _set_bodo_meta_in_pandas():
    if '_bodo_meta' not in pd.Series._metadata:
        pd.Series._metadata.append('_bodo_meta')
    if '_bodo_meta' not in pd.DataFrame._metadata:
        pd.DataFrame._metadata.append('_bodo_meta')


_set_bodo_meta_in_pandas()


@typeof_impl.register(pd.DataFrame)
def typeof_pd_dataframe(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    qno__okphm = tuple(val.columns.to_list())
    efesa__grlbk = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        cnqrs__iaa = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        cnqrs__iaa = numba.typeof(val.index)
    hfjy__fgj = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    uqee__tndf = len(efesa__grlbk) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(efesa__grlbk, cnqrs__iaa, qno__okphm, hfjy__fgj,
        is_table_format=uqee__tndf)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    hfjy__fgj = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        ofrip__wmg = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        ofrip__wmg = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    gxfgl__oktb = dtype_to_array_type(dtype)
    if _use_dict_str_type and gxfgl__oktb == string_array_type:
        gxfgl__oktb = bodo.dict_str_arr_type
    return SeriesType(dtype, data=gxfgl__oktb, index=ofrip__wmg, name_typ=
        numba.typeof(val.name), dist=hfjy__fgj)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    nopu__ctf = c.pyapi.object_getattr_string(val, 'index')
    llgjd__yxzzq = c.pyapi.to_native_value(typ.index, nopu__ctf).value
    c.pyapi.decref(nopu__ctf)
    if typ.is_table_format:
        aevg__aabmo = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        aevg__aabmo.parent = val
        for zmzl__jck, ckhxu__zcxil in typ.table_type.type_to_blk.items():
            qid__qea = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[ckhxu__zcxil]))
            trcq__ferqy, jczpl__abz = ListInstance.allocate_ex(c.context, c
                .builder, types.List(zmzl__jck), qid__qea)
            jczpl__abz.size = qid__qea
            setattr(aevg__aabmo, f'block_{ckhxu__zcxil}', jczpl__abz.value)
        crtyl__prjvg = c.pyapi.call_method(val, '__len__', ())
        ums__mbew = c.pyapi.long_as_longlong(crtyl__prjvg)
        c.pyapi.decref(crtyl__prjvg)
        aevg__aabmo.len = ums__mbew
        puolh__owlox = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [aevg__aabmo._getvalue()])
    else:
        ofwjx__gic = [c.context.get_constant_null(zmzl__jck) for zmzl__jck in
            typ.data]
        puolh__owlox = c.context.make_tuple(c.builder, types.Tuple(typ.data
            ), ofwjx__gic)
    zqewc__mkk = construct_dataframe(c.context, c.builder, typ,
        puolh__owlox, llgjd__yxzzq, val, None)
    return NativeValue(zqewc__mkk)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        fdc__spmj = df._bodo_meta['type_metadata'][1]
    else:
        fdc__spmj = [None] * len(df.columns)
    ohify__hvikw = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=fdc__spmj[i])) for i in range(len(df.columns))]
    ohify__hvikw = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        zmzl__jck == string_array_type else zmzl__jck) for zmzl__jck in
        ohify__hvikw]
    return tuple(ohify__hvikw)


class SeriesDtypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Datime_Date = 13
    NP_Datetime64ns = 14
    NP_Timedelta64ns = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 21
    ARRAY = 22
    PD_nullable_Int8 = 23
    PD_nullable_UInt8 = 24
    PD_nullable_Int16 = 25
    PD_nullable_UInt16 = 26
    PD_nullable_Int32 = 27
    PD_nullable_UInt32 = 28
    PD_nullable_Int64 = 29
    PD_nullable_UInt64 = 30
    PD_nullable_bool = 31
    CategoricalType = 32
    NoneType = 33
    Literal = 34
    IntegerArray = 35
    RangeIndexType = 36
    DatetimeIndexType = 37
    NumericIndexType = 38
    PeriodIndexType = 39
    IntervalIndexType = 40
    CategoricalIndexType = 41
    StringIndexType = 42
    BinaryIndexType = 43
    TimedeltaIndexType = 44
    LiteralType = 45


_one_to_one_type_to_enum_map = {types.int8: SeriesDtypeEnum.Int8.value,
    types.uint8: SeriesDtypeEnum.UInt8.value, types.int32: SeriesDtypeEnum.
    Int32.value, types.uint32: SeriesDtypeEnum.UInt32.value, types.int64:
    SeriesDtypeEnum.Int64.value, types.uint64: SeriesDtypeEnum.UInt64.value,
    types.float32: SeriesDtypeEnum.Float32.value, types.float64:
    SeriesDtypeEnum.Float64.value, types.NPDatetime('ns'): SeriesDtypeEnum.
    NP_Datetime64ns.value, types.NPTimedelta('ns'): SeriesDtypeEnum.
    NP_Timedelta64ns.value, types.bool_: SeriesDtypeEnum.Bool.value, types.
    int16: SeriesDtypeEnum.Int16.value, types.uint16: SeriesDtypeEnum.
    UInt16.value, types.Integer('int128', 128): SeriesDtypeEnum.Int128.
    value, bodo.hiframes.datetime_date_ext.datetime_date_type:
    SeriesDtypeEnum.Datime_Date.value, IntDtype(types.int8):
    SeriesDtypeEnum.PD_nullable_Int8.value, IntDtype(types.uint8):
    SeriesDtypeEnum.PD_nullable_UInt8.value, IntDtype(types.int16):
    SeriesDtypeEnum.PD_nullable_Int16.value, IntDtype(types.uint16):
    SeriesDtypeEnum.PD_nullable_UInt16.value, IntDtype(types.int32):
    SeriesDtypeEnum.PD_nullable_Int32.value, IntDtype(types.uint32):
    SeriesDtypeEnum.PD_nullable_UInt32.value, IntDtype(types.int64):
    SeriesDtypeEnum.PD_nullable_Int64.value, IntDtype(types.uint64):
    SeriesDtypeEnum.PD_nullable_UInt64.value, bytes_type: SeriesDtypeEnum.
    BINARY.value, string_type: SeriesDtypeEnum.STRING.value, bodo.bool_:
    SeriesDtypeEnum.Bool.value, types.none: SeriesDtypeEnum.NoneType.value}
_one_to_one_enum_to_type_map = {SeriesDtypeEnum.Int8.value: types.int8,
    SeriesDtypeEnum.UInt8.value: types.uint8, SeriesDtypeEnum.Int32.value:
    types.int32, SeriesDtypeEnum.UInt32.value: types.uint32,
    SeriesDtypeEnum.Int64.value: types.int64, SeriesDtypeEnum.UInt64.value:
    types.uint64, SeriesDtypeEnum.Float32.value: types.float32,
    SeriesDtypeEnum.Float64.value: types.float64, SeriesDtypeEnum.
    NP_Datetime64ns.value: types.NPDatetime('ns'), SeriesDtypeEnum.
    NP_Timedelta64ns.value: types.NPTimedelta('ns'), SeriesDtypeEnum.Int16.
    value: types.int16, SeriesDtypeEnum.UInt16.value: types.uint16,
    SeriesDtypeEnum.Int128.value: types.Integer('int128', 128),
    SeriesDtypeEnum.Datime_Date.value: bodo.hiframes.datetime_date_ext.
    datetime_date_type, SeriesDtypeEnum.PD_nullable_Int8.value: IntDtype(
    types.int8), SeriesDtypeEnum.PD_nullable_UInt8.value: IntDtype(types.
    uint8), SeriesDtypeEnum.PD_nullable_Int16.value: IntDtype(types.int16),
    SeriesDtypeEnum.PD_nullable_UInt16.value: IntDtype(types.uint16),
    SeriesDtypeEnum.PD_nullable_Int32.value: IntDtype(types.int32),
    SeriesDtypeEnum.PD_nullable_UInt32.value: IntDtype(types.uint32),
    SeriesDtypeEnum.PD_nullable_Int64.value: IntDtype(types.int64),
    SeriesDtypeEnum.PD_nullable_UInt64.value: IntDtype(types.uint64),
    SeriesDtypeEnum.BINARY.value: bytes_type, SeriesDtypeEnum.STRING.value:
    string_type, SeriesDtypeEnum.Bool.value: bodo.bool_, SeriesDtypeEnum.
    NoneType.value: types.none}


def _dtype_from_type_enum_list(typ_enum_list):
    rsgc__dbbta, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(rsgc__dbbta) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {rsgc__dbbta}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        esn__ylyqe, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return esn__ylyqe, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        esn__ylyqe, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        return esn__ylyqe, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        onf__puywo = typ_enum_list[1]
        twde__widk = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(onf__puywo, twde__widk)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        ecfc__slre = typ_enum_list[1]
        ccall__swh = tuple(typ_enum_list[2:2 + ecfc__slre])
        gjv__rnf = typ_enum_list[2 + ecfc__slre:]
        iies__bcy = []
        for i in range(ecfc__slre):
            gjv__rnf, meu__ldud = _dtype_from_type_enum_list_recursor(gjv__rnf)
            iies__bcy.append(meu__ldud)
        return gjv__rnf, StructType(tuple(iies__bcy), ccall__swh)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        cqyr__zogwa = typ_enum_list[1]
        gjv__rnf = typ_enum_list[2:]
        return gjv__rnf, cqyr__zogwa
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        cqyr__zogwa = typ_enum_list[1]
        gjv__rnf = typ_enum_list[2:]
        return gjv__rnf, numba.types.literal(cqyr__zogwa)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        gjv__rnf, iuh__jeyq = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        gjv__rnf, gok__owa = _dtype_from_type_enum_list_recursor(gjv__rnf)
        gjv__rnf, tbt__hpx = _dtype_from_type_enum_list_recursor(gjv__rnf)
        gjv__rnf, vecdd__fnfbx = _dtype_from_type_enum_list_recursor(gjv__rnf)
        gjv__rnf, jlofp__igvkg = _dtype_from_type_enum_list_recursor(gjv__rnf)
        return gjv__rnf, PDCategoricalDtype(iuh__jeyq, gok__owa, tbt__hpx,
            vecdd__fnfbx, jlofp__igvkg)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        gjv__rnf, ulitn__vrzq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return gjv__rnf, DatetimeIndexType(ulitn__vrzq)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        gjv__rnf, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list[1:]
            )
        gjv__rnf, ulitn__vrzq = _dtype_from_type_enum_list_recursor(gjv__rnf)
        gjv__rnf, vecdd__fnfbx = _dtype_from_type_enum_list_recursor(gjv__rnf)
        return gjv__rnf, NumericIndexType(dtype, ulitn__vrzq, vecdd__fnfbx)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        gjv__rnf, vgyr__ttr = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        gjv__rnf, ulitn__vrzq = _dtype_from_type_enum_list_recursor(gjv__rnf)
        return gjv__rnf, PeriodIndexType(vgyr__ttr, ulitn__vrzq)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        gjv__rnf, vecdd__fnfbx = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        gjv__rnf, ulitn__vrzq = _dtype_from_type_enum_list_recursor(gjv__rnf)
        return gjv__rnf, CategoricalIndexType(vecdd__fnfbx, ulitn__vrzq)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        gjv__rnf, ulitn__vrzq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return gjv__rnf, RangeIndexType(ulitn__vrzq)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        gjv__rnf, ulitn__vrzq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return gjv__rnf, StringIndexType(ulitn__vrzq)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        gjv__rnf, ulitn__vrzq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return gjv__rnf, BinaryIndexType(ulitn__vrzq)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        gjv__rnf, ulitn__vrzq = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return gjv__rnf, TimedeltaIndexType(ulitn__vrzq)
    else:
        raise_bodo_error(
            f'Unexpected Internal Error while converting typing metadata: unable to infer dtype for type enum {typ_enum_list[0]}. Please file the error here: https://github.com/Bodo-inc/Feedback'
            )


def _dtype_to_type_enum_list(typ):
    return guard(_dtype_to_type_enum_list_recursor, typ)


def _dtype_to_type_enum_list_recursor(typ, upcast_numeric_index=True):
    if typ.__hash__ and typ in _one_to_one_type_to_enum_map:
        return [_one_to_one_type_to_enum_map[typ]]
    if isinstance(typ, (dict, int, list, tuple, str, bool, bytes, float)):
        return [SeriesDtypeEnum.Literal.value, typ]
    elif typ is None:
        return [SeriesDtypeEnum.Literal.value, typ]
    elif is_overload_constant_int(typ):
        eohtm__zqlla = get_overload_const_int(typ)
        if numba.types.maybe_literal(eohtm__zqlla) == typ:
            return [SeriesDtypeEnum.LiteralType.value, eohtm__zqlla]
    elif is_overload_constant_str(typ):
        eohtm__zqlla = get_overload_const_str(typ)
        if numba.types.maybe_literal(eohtm__zqlla) == typ:
            return [SeriesDtypeEnum.LiteralType.value, eohtm__zqlla]
    elif is_overload_constant_bool(typ):
        eohtm__zqlla = get_overload_const_bool(typ)
        if numba.types.maybe_literal(eohtm__zqlla) == typ:
            return [SeriesDtypeEnum.LiteralType.value, eohtm__zqlla]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        cez__lgm = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for ltmbd__qpk in typ.names:
            cez__lgm.append(ltmbd__qpk)
        for iiq__mifld in typ.data:
            cez__lgm += _dtype_to_type_enum_list_recursor(iiq__mifld)
        return cez__lgm
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        xbw__sgz = _dtype_to_type_enum_list_recursor(typ.categories)
        bbk__cuolb = _dtype_to_type_enum_list_recursor(typ.elem_type)
        sbj__vlvj = _dtype_to_type_enum_list_recursor(typ.ordered)
        cwzwr__vcbu = _dtype_to_type_enum_list_recursor(typ.data)
        ckm__hyci = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + xbw__sgz + bbk__cuolb + sbj__vlvj + cwzwr__vcbu + ckm__hyci
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                zix__avnd = types.float64
                spkvg__wkmp = types.Array(zix__avnd, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                zix__avnd = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    spkvg__wkmp = IntegerArrayType(zix__avnd)
                else:
                    spkvg__wkmp = types.Array(zix__avnd, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                zix__avnd = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    spkvg__wkmp = IntegerArrayType(zix__avnd)
                else:
                    spkvg__wkmp = types.Array(zix__avnd, 1, 'C')
            elif typ.dtype == types.bool_:
                zix__avnd = typ.dtype
                spkvg__wkmp = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(zix__avnd
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(spkvg__wkmp)
        else:
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(typ.dtype
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(typ.data)
    elif isinstance(typ, PeriodIndexType):
        return [SeriesDtypeEnum.PeriodIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.freq
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, CategoricalIndexType):
        return [SeriesDtypeEnum.CategoricalIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.data
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, RangeIndexType):
        return [SeriesDtypeEnum.RangeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, StringIndexType):
        return [SeriesDtypeEnum.StringIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, BinaryIndexType):
        return [SeriesDtypeEnum.BinaryIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, TimedeltaIndexType):
        return [SeriesDtypeEnum.TimedeltaIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    else:
        raise GuardException('Unable to convert type')


def _infer_series_dtype(S, array_metadata=None):
    if S.dtype == np.dtype('O'):
        if len(S.values) == 0:
            if (hasattr(S, '_bodo_meta') and S._bodo_meta is not None and 
                'type_metadata' in S._bodo_meta and S._bodo_meta[
                'type_metadata'][1] is not None):
                hhzkq__oyzhi = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(hhzkq__oyzhi)
            elif array_metadata != None:
                return _dtype_from_type_enum_list(array_metadata).dtype
        return numba.typeof(S.values).dtype
    if isinstance(S.dtype, pd.core.arrays.integer._IntegerDtype):
        return typeof_pd_int_dtype(S.dtype, None)
    elif isinstance(S.dtype, pd.CategoricalDtype):
        return bodo.typeof(S.dtype)
    elif isinstance(S.dtype, pd.StringDtype):
        return string_type
    elif isinstance(S.dtype, pd.BooleanDtype):
        return types.bool_
    if isinstance(S.dtype, pd.DatetimeTZDtype):
        aevmq__rbfwe = S.dtype.unit
        if aevmq__rbfwe != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        umpmv__lfj = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.
            dtype.tz)
        return PandasDatetimeTZDtype(umpmv__lfj)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    grbn__bbosb = cgutils.is_not_null(builder, parent_obj)
    bwijx__swqm = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(grbn__bbosb):
        dirs__fqwb = pyapi.object_getattr_string(parent_obj, 'columns')
        crtyl__prjvg = pyapi.call_method(dirs__fqwb, '__len__', ())
        builder.store(pyapi.long_as_longlong(crtyl__prjvg), bwijx__swqm)
        pyapi.decref(crtyl__prjvg)
        pyapi.decref(dirs__fqwb)
    use_parent_obj = builder.and_(grbn__bbosb, builder.icmp_unsigned('==',
        builder.load(bwijx__swqm), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        vobap__ppz = df_typ.runtime_colname_typ
        context.nrt.incref(builder, vobap__ppz, dataframe_payload.columns)
        return pyapi.from_native_value(vobap__ppz, dataframe_payload.
            columns, c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        pum__bohad = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        pum__bohad = pd.array(df_typ.columns, 'string')
    else:
        pum__bohad = df_typ.columns
    wwx__rbg = numba.typeof(pum__bohad)
    skut__nov = context.get_constant_generic(builder, wwx__rbg, pum__bohad)
    htj__ncr = pyapi.from_native_value(wwx__rbg, skut__nov, c.env_manager)
    return htj__ncr


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (pvoaz__pqint, tvoip__wowe):
        with pvoaz__pqint:
            pyapi.incref(obj)
            vso__tom = context.insert_const_string(c.builder.module, 'numpy')
            rozwy__nnk = pyapi.import_module_noblock(vso__tom)
            if df_typ.has_runtime_cols:
                ifoig__oiry = 0
            else:
                ifoig__oiry = len(df_typ.columns)
            qlem__dki = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), ifoig__oiry))
            gjm__mir = pyapi.call_method(rozwy__nnk, 'arange', (qlem__dki,))
            pyapi.object_setattr_string(obj, 'columns', gjm__mir)
            pyapi.decref(rozwy__nnk)
            pyapi.decref(gjm__mir)
            pyapi.decref(qlem__dki)
        with tvoip__wowe:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            oqrbm__xmriu = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            vso__tom = context.insert_const_string(c.builder.module, 'pandas')
            rozwy__nnk = pyapi.import_module_noblock(vso__tom)
            df_obj = pyapi.call_method(rozwy__nnk, 'DataFrame', (pyapi.
                borrow_none(), oqrbm__xmriu))
            pyapi.decref(rozwy__nnk)
            pyapi.decref(oqrbm__xmriu)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    irgp__oiedw = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = irgp__oiedw.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        yqy__txqwb = typ.table_type
        aevg__aabmo = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, yqy__txqwb, aevg__aabmo)
        budl__jmjky = box_table(yqy__txqwb, aevg__aabmo, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (azrz__jke, cdsrk__slyan):
            with azrz__jke:
                cnc__mmm = pyapi.object_getattr_string(budl__jmjky, 'arrays')
                xkdru__epkld = c.pyapi.make_none()
                if n_cols is None:
                    crtyl__prjvg = pyapi.call_method(cnc__mmm, '__len__', ())
                    qid__qea = pyapi.long_as_longlong(crtyl__prjvg)
                    pyapi.decref(crtyl__prjvg)
                else:
                    qid__qea = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, qid__qea) as ihaf__kmq:
                    i = ihaf__kmq.index
                    fytcr__wet = pyapi.list_getitem(cnc__mmm, i)
                    djx__mapxu = c.builder.icmp_unsigned('!=', fytcr__wet,
                        xkdru__epkld)
                    with builder.if_then(djx__mapxu):
                        fna__rmqaa = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, fna__rmqaa, fytcr__wet)
                        pyapi.decref(fna__rmqaa)
                pyapi.decref(cnc__mmm)
                pyapi.decref(xkdru__epkld)
            with cdsrk__slyan:
                df_obj = builder.load(res)
                oqrbm__xmriu = pyapi.object_getattr_string(df_obj, 'index')
                rdf__gpgjd = c.pyapi.call_method(budl__jmjky, 'to_pandas',
                    (oqrbm__xmriu,))
                builder.store(rdf__gpgjd, res)
                pyapi.decref(df_obj)
                pyapi.decref(oqrbm__xmriu)
        pyapi.decref(budl__jmjky)
    else:
        kzvkl__izhtf = [builder.extract_value(dataframe_payload.data, i) for
            i in range(n_cols)]
        swlq__nymt = typ.data
        for i, wknz__sqyf, gxfgl__oktb in zip(range(n_cols), kzvkl__izhtf,
            swlq__nymt):
            npo__dhju = cgutils.alloca_once_value(builder, wknz__sqyf)
            doi__dua = cgutils.alloca_once_value(builder, context.
                get_constant_null(gxfgl__oktb))
            djx__mapxu = builder.not_(is_ll_eq(builder, npo__dhju, doi__dua))
            osme__srqd = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, djx__mapxu))
            with builder.if_then(osme__srqd):
                fna__rmqaa = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, gxfgl__oktb, wknz__sqyf)
                arr_obj = pyapi.from_native_value(gxfgl__oktb, wknz__sqyf,
                    c.env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, fna__rmqaa, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(fna__rmqaa)
    df_obj = builder.load(res)
    htj__ncr = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', htj__ncr)
    pyapi.decref(htj__ncr)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    xkdru__epkld = pyapi.borrow_none()
    urgw__txiih = pyapi.unserialize(pyapi.serialize_object(slice))
    ccwl__smkqx = pyapi.call_function_objargs(urgw__txiih, [xkdru__epkld])
    apgh__dcub = pyapi.long_from_longlong(col_ind)
    mzbdv__duvll = pyapi.tuple_pack([ccwl__smkqx, apgh__dcub])
    fpqz__qmuzz = pyapi.object_getattr_string(df_obj, 'iloc')
    uzrce__wmapl = pyapi.object_getitem(fpqz__qmuzz, mzbdv__duvll)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        ywn__kyklb = pyapi.object_getattr_string(uzrce__wmapl, 'array')
    else:
        ywn__kyklb = pyapi.object_getattr_string(uzrce__wmapl, 'values')
    if isinstance(data_typ, types.Array):
        dudx__nkle = context.insert_const_string(builder.module, 'numpy')
        cmn__keyt = pyapi.import_module_noblock(dudx__nkle)
        arr_obj = pyapi.call_method(cmn__keyt, 'ascontiguousarray', (
            ywn__kyklb,))
        pyapi.decref(ywn__kyklb)
        pyapi.decref(cmn__keyt)
    else:
        arr_obj = ywn__kyklb
    pyapi.decref(urgw__txiih)
    pyapi.decref(ccwl__smkqx)
    pyapi.decref(apgh__dcub)
    pyapi.decref(mzbdv__duvll)
    pyapi.decref(fpqz__qmuzz)
    pyapi.decref(uzrce__wmapl)
    return arr_obj


@intrinsic
def unbox_dataframe_column(typingctx, df, i=None):
    assert isinstance(df, DataFrameType) and is_overload_constant_int(i)

    def codegen(context, builder, sig, args):
        pyapi = context.get_python_api(builder)
        c = numba.core.pythonapi._UnboxContext(context, builder, pyapi)
        df_typ = sig.args[0]
        col_ind = get_overload_const_int(sig.args[1])
        data_typ = df_typ.data[col_ind]
        irgp__oiedw = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            irgp__oiedw.parent, args[1], data_typ)
        tlb__vozr = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            aevg__aabmo = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            ckhxu__zcxil = df_typ.table_type.type_to_blk[data_typ]
            yijk__mzair = getattr(aevg__aabmo, f'block_{ckhxu__zcxil}')
            ososp__jap = ListInstance(c.context, c.builder, types.List(
                data_typ), yijk__mzair)
            axlxv__fxq = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[col_ind])
            ososp__jap.inititem(axlxv__fxq, tlb__vozr.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, tlb__vozr.value, col_ind)
        lwqfm__pfus = DataFramePayloadType(df_typ)
        vox__kqia = context.nrt.meminfo_data(builder, irgp__oiedw.meminfo)
        drec__hpata = context.get_value_type(lwqfm__pfus).as_pointer()
        vox__kqia = builder.bitcast(vox__kqia, drec__hpata)
        builder.store(dataframe_payload._getvalue(), vox__kqia)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        ywn__kyklb = c.pyapi.object_getattr_string(val, 'array')
    else:
        ywn__kyklb = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        dudx__nkle = c.context.insert_const_string(c.builder.module, 'numpy')
        cmn__keyt = c.pyapi.import_module_noblock(dudx__nkle)
        arr_obj = c.pyapi.call_method(cmn__keyt, 'ascontiguousarray', (
            ywn__kyklb,))
        c.pyapi.decref(ywn__kyklb)
        c.pyapi.decref(cmn__keyt)
    else:
        arr_obj = ywn__kyklb
    tsihn__lkgyg = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    oqrbm__xmriu = c.pyapi.object_getattr_string(val, 'index')
    llgjd__yxzzq = c.pyapi.to_native_value(typ.index, oqrbm__xmriu).value
    zizq__dnpsq = c.pyapi.object_getattr_string(val, 'name')
    lppnj__lxt = c.pyapi.to_native_value(typ.name_typ, zizq__dnpsq).value
    mxo__qfdjq = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, tsihn__lkgyg, llgjd__yxzzq, lppnj__lxt)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(oqrbm__xmriu)
    c.pyapi.decref(zizq__dnpsq)
    return NativeValue(mxo__qfdjq)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        uqiq__wfjyf = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(uqiq__wfjyf._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    vso__tom = c.context.insert_const_string(c.builder.module, 'pandas')
    gjs__cut = c.pyapi.import_module_noblock(vso__tom)
    qgm__pgur = bodo.hiframes.pd_series_ext.get_series_payload(c.context, c
        .builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, qgm__pgur.data)
    c.context.nrt.incref(c.builder, typ.index, qgm__pgur.index)
    c.context.nrt.incref(c.builder, typ.name_typ, qgm__pgur.name)
    arr_obj = c.pyapi.from_native_value(typ.data, qgm__pgur.data, c.env_manager
        )
    oqrbm__xmriu = c.pyapi.from_native_value(typ.index, qgm__pgur.index, c.
        env_manager)
    zizq__dnpsq = c.pyapi.from_native_value(typ.name_typ, qgm__pgur.name, c
        .env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(gjs__cut, 'Series', (arr_obj, oqrbm__xmriu,
        dtype, zizq__dnpsq))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(oqrbm__xmriu)
    c.pyapi.decref(zizq__dnpsq)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(gjs__cut)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    tqz__ezz = []
    for jgoin__gxvcm in typ_list:
        if isinstance(jgoin__gxvcm, int) and not isinstance(jgoin__gxvcm, bool
            ):
            hgtwn__cfgx = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), jgoin__gxvcm))
        else:
            wfgy__ibwn = numba.typeof(jgoin__gxvcm)
            kigf__trco = context.get_constant_generic(builder, wfgy__ibwn,
                jgoin__gxvcm)
            hgtwn__cfgx = pyapi.from_native_value(wfgy__ibwn, kigf__trco,
                env_manager)
        tqz__ezz.append(hgtwn__cfgx)
    teed__vwop = pyapi.list_pack(tqz__ezz)
    for val in tqz__ezz:
        pyapi.decref(val)
    return teed__vwop


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    amsi__zbwuq = not typ.has_runtime_cols and (not typ.is_table_format or 
        len(typ.columns) < TABLE_FORMAT_THRESHOLD)
    tnht__dnal = 2 if amsi__zbwuq else 1
    udkts__dhokn = pyapi.dict_new(tnht__dnal)
    lqnju__wwtsj = pyapi.long_from_longlong(lir.Constant(lir.IntType(64),
        typ.dist.value))
    pyapi.dict_setitem_string(udkts__dhokn, 'dist', lqnju__wwtsj)
    pyapi.decref(lqnju__wwtsj)
    if amsi__zbwuq:
        jvupb__prbx = _dtype_to_type_enum_list(typ.index)
        if jvupb__prbx != None:
            qhjia__bqb = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, jvupb__prbx)
        else:
            qhjia__bqb = pyapi.make_none()
        jpvmv__jpmf = []
        for dtype in typ.data:
            typ_list = _dtype_to_type_enum_list(dtype)
            if typ_list != None:
                teed__vwop = type_enum_list_to_py_list_obj(pyapi, context,
                    builder, c.env_manager, typ_list)
            else:
                teed__vwop = pyapi.make_none()
            jpvmv__jpmf.append(teed__vwop)
        zbq__mhw = pyapi.list_pack(jpvmv__jpmf)
        zxo__bkvz = pyapi.list_pack([qhjia__bqb, zbq__mhw])
        for val in jpvmv__jpmf:
            pyapi.decref(val)
        pyapi.dict_setitem_string(udkts__dhokn, 'type_metadata', zxo__bkvz)
    pyapi.object_setattr_string(obj, '_bodo_meta', udkts__dhokn)
    pyapi.decref(udkts__dhokn)


def get_series_dtype_handle_null_int_and_hetrogenous(series_typ):
    if isinstance(series_typ, HeterogeneousSeriesType):
        return None
    if isinstance(series_typ.dtype, types.Number) and isinstance(series_typ
        .data, IntegerArrayType):
        return IntDtype(series_typ.dtype)
    return series_typ.dtype


def _set_bodo_meta_series(obj, c, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    udkts__dhokn = pyapi.dict_new(2)
    lqnju__wwtsj = pyapi.long_from_longlong(lir.Constant(lir.IntType(64),
        typ.dist.value))
    jvupb__prbx = _dtype_to_type_enum_list(typ.index)
    if jvupb__prbx != None:
        qhjia__bqb = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, jvupb__prbx)
    else:
        qhjia__bqb = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            yvihq__hnz = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            yvihq__hnz = pyapi.make_none()
    else:
        yvihq__hnz = pyapi.make_none()
    ovrug__qjuyt = pyapi.list_pack([qhjia__bqb, yvihq__hnz])
    pyapi.dict_setitem_string(udkts__dhokn, 'type_metadata', ovrug__qjuyt)
    pyapi.decref(ovrug__qjuyt)
    pyapi.dict_setitem_string(udkts__dhokn, 'dist', lqnju__wwtsj)
    pyapi.object_setattr_string(obj, '_bodo_meta', udkts__dhokn)
    pyapi.decref(udkts__dhokn)
    pyapi.decref(lqnju__wwtsj)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as amwa__swyx:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    wldtu__wmqnn = numba.np.numpy_support.map_layout(val)
    ehcty__pwt = not val.flags.writeable
    return types.Array(dtype, val.ndim, wldtu__wmqnn, readonly=ehcty__pwt)


def _infer_ndarray_obj_dtype(val):
    if not val.dtype == np.dtype('O'):
        raise BodoError('Unsupported array dtype: {}'.format(val.dtype))
    i = 0
    while i < len(val) and (pd.api.types.is_scalar(val[i]) and pd.isna(val[
        i]) or not pd.api.types.is_scalar(val[i]) and len(val[i]) == 0):
        i += 1
    if i == len(val):
        warnings.warn(BodoWarning(
            'Empty object array passed to Bodo, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    nmri__qbj = val[i]
    if isinstance(nmri__qbj, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(nmri__qbj, bytes):
        return binary_array_type
    elif isinstance(nmri__qbj, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(nmri__qbj, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(nmri__qbj))
    elif isinstance(nmri__qbj, (dict, Dict)) and all(isinstance(wys__ojg,
        str) for wys__ojg in nmri__qbj.keys()):
        ccall__swh = tuple(nmri__qbj.keys())
        cvaj__pobil = tuple(_get_struct_value_arr_type(v) for v in
            nmri__qbj.values())
        return StructArrayType(cvaj__pobil, ccall__swh)
    elif isinstance(nmri__qbj, (dict, Dict)):
        gtg__dkq = numba.typeof(_value_to_array(list(nmri__qbj.keys())))
        cjipi__ffe = numba.typeof(_value_to_array(list(nmri__qbj.values())))
        gtg__dkq = to_str_arr_if_dict_array(gtg__dkq)
        cjipi__ffe = to_str_arr_if_dict_array(cjipi__ffe)
        return MapArrayType(gtg__dkq, cjipi__ffe)
    elif isinstance(nmri__qbj, tuple):
        cvaj__pobil = tuple(_get_struct_value_arr_type(v) for v in nmri__qbj)
        return TupleArrayType(cvaj__pobil)
    if isinstance(nmri__qbj, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(nmri__qbj, list):
            nmri__qbj = _value_to_array(nmri__qbj)
        oha__kch = numba.typeof(nmri__qbj)
        oha__kch = to_str_arr_if_dict_array(oha__kch)
        return ArrayItemArrayType(oha__kch)
    if isinstance(nmri__qbj, datetime.date):
        return datetime_date_array_type
    if isinstance(nmri__qbj, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(nmri__qbj, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError(f'Unsupported object array with first value: {nmri__qbj}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    kllz__nxdnt = val.copy()
    kllz__nxdnt.append(None)
    wknz__sqyf = np.array(kllz__nxdnt, np.object_)
    if len(val) and isinstance(val[0], float):
        wknz__sqyf = np.array(val, np.float64)
    return wknz__sqyf


def _get_struct_value_arr_type(v):
    if isinstance(v, (dict, Dict)):
        return numba.typeof(_value_to_array(v))
    if isinstance(v, list):
        return dtype_to_array_type(numba.typeof(_value_to_array(v)))
    if pd.api.types.is_scalar(v) and pd.isna(v):
        warnings.warn(BodoWarning(
            'Field value in struct array is NA, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    gxfgl__oktb = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        gxfgl__oktb = to_nullable_type(gxfgl__oktb)
    return gxfgl__oktb
