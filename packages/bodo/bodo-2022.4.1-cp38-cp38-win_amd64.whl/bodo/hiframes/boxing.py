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
    iqejh__myz = tuple(val.columns.to_list())
    cltu__ejnqy = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        vsq__hbgs = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        vsq__hbgs = numba.typeof(val.index)
    hlypl__cxb = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    yinmt__aqpu = len(cltu__ejnqy) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(cltu__ejnqy, vsq__hbgs, iqejh__myz, hlypl__cxb,
        is_table_format=yinmt__aqpu)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    hlypl__cxb = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        fbg__hofd = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        fbg__hofd = numba.typeof(val.index)
    dtype = _infer_series_dtype(val)
    qngr__oxze = dtype_to_array_type(dtype)
    if _use_dict_str_type and qngr__oxze == string_array_type:
        qngr__oxze = bodo.dict_str_arr_type
    return SeriesType(dtype, data=qngr__oxze, index=fbg__hofd, name_typ=
        numba.typeof(val.name), dist=hlypl__cxb)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    vcz__lwh = c.pyapi.object_getattr_string(val, 'index')
    qnzc__aqhw = c.pyapi.to_native_value(typ.index, vcz__lwh).value
    c.pyapi.decref(vcz__lwh)
    if typ.is_table_format:
        nxlk__bka = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        nxlk__bka.parent = val
        for ajvka__fkc, esfj__swlyy in typ.table_type.type_to_blk.items():
            eocvv__zfb = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[esfj__swlyy]))
            wcxfi__frg, uic__onigq = ListInstance.allocate_ex(c.context, c.
                builder, types.List(ajvka__fkc), eocvv__zfb)
            uic__onigq.size = eocvv__zfb
            setattr(nxlk__bka, f'block_{esfj__swlyy}', uic__onigq.value)
        ahv__pzqt = c.pyapi.call_method(val, '__len__', ())
        uqx__oyeve = c.pyapi.long_as_longlong(ahv__pzqt)
        c.pyapi.decref(ahv__pzqt)
        nxlk__bka.len = uqx__oyeve
        pfph__opkr = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [nxlk__bka._getvalue()])
    else:
        hbx__iveh = [c.context.get_constant_null(ajvka__fkc) for ajvka__fkc in
            typ.data]
        pfph__opkr = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            hbx__iveh)
    rykwc__rwr = construct_dataframe(c.context, c.builder, typ, pfph__opkr,
        qnzc__aqhw, val, None)
    return NativeValue(rykwc__rwr)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        rboqc__lgr = df._bodo_meta['type_metadata'][1]
    else:
        rboqc__lgr = [None] * len(df.columns)
    odt__fei = [dtype_to_array_type(_infer_series_dtype(df.iloc[:, i],
        array_metadata=rboqc__lgr[i])) for i in range(len(df.columns))]
    odt__fei = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        ajvka__fkc == string_array_type else ajvka__fkc) for ajvka__fkc in
        odt__fei]
    return tuple(odt__fei)


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
    wal__dbtbm, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(wal__dbtbm) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {wal__dbtbm}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        klj__uyck, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return klj__uyck, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        klj__uyck, typ = _dtype_from_type_enum_list_recursor(typ_enum_list[1:])
        return klj__uyck, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        raxha__odbq = typ_enum_list[1]
        olx__yhq = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(raxha__odbq, olx__yhq)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        xbj__rnv = typ_enum_list[1]
        botyk__rhh = tuple(typ_enum_list[2:2 + xbj__rnv])
        wvut__cfohf = typ_enum_list[2 + xbj__rnv:]
        obttq__emrd = []
        for i in range(xbj__rnv):
            wvut__cfohf, lxx__jwu = _dtype_from_type_enum_list_recursor(
                wvut__cfohf)
            obttq__emrd.append(lxx__jwu)
        return wvut__cfohf, StructType(tuple(obttq__emrd), botyk__rhh)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        hvmu__ypjr = typ_enum_list[1]
        wvut__cfohf = typ_enum_list[2:]
        return wvut__cfohf, hvmu__ypjr
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        hvmu__ypjr = typ_enum_list[1]
        wvut__cfohf = typ_enum_list[2:]
        return wvut__cfohf, numba.types.literal(hvmu__ypjr)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        wvut__cfohf, jyihu__iom = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        wvut__cfohf, hje__zgfcd = _dtype_from_type_enum_list_recursor(
            wvut__cfohf)
        wvut__cfohf, cigmp__atdxc = _dtype_from_type_enum_list_recursor(
            wvut__cfohf)
        wvut__cfohf, smhy__diew = _dtype_from_type_enum_list_recursor(
            wvut__cfohf)
        wvut__cfohf, xvb__uex = _dtype_from_type_enum_list_recursor(wvut__cfohf
            )
        return wvut__cfohf, PDCategoricalDtype(jyihu__iom, hje__zgfcd,
            cigmp__atdxc, smhy__diew, xvb__uex)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        wvut__cfohf, szdu__zopsu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return wvut__cfohf, DatetimeIndexType(szdu__zopsu)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        wvut__cfohf, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        wvut__cfohf, szdu__zopsu = _dtype_from_type_enum_list_recursor(
            wvut__cfohf)
        wvut__cfohf, smhy__diew = _dtype_from_type_enum_list_recursor(
            wvut__cfohf)
        return wvut__cfohf, NumericIndexType(dtype, szdu__zopsu, smhy__diew)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        wvut__cfohf, sju__pleos = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        wvut__cfohf, szdu__zopsu = _dtype_from_type_enum_list_recursor(
            wvut__cfohf)
        return wvut__cfohf, PeriodIndexType(sju__pleos, szdu__zopsu)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        wvut__cfohf, smhy__diew = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        wvut__cfohf, szdu__zopsu = _dtype_from_type_enum_list_recursor(
            wvut__cfohf)
        return wvut__cfohf, CategoricalIndexType(smhy__diew, szdu__zopsu)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        wvut__cfohf, szdu__zopsu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return wvut__cfohf, RangeIndexType(szdu__zopsu)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        wvut__cfohf, szdu__zopsu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return wvut__cfohf, StringIndexType(szdu__zopsu)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        wvut__cfohf, szdu__zopsu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return wvut__cfohf, BinaryIndexType(szdu__zopsu)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        wvut__cfohf, szdu__zopsu = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return wvut__cfohf, TimedeltaIndexType(szdu__zopsu)
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
        ohn__tjpt = get_overload_const_int(typ)
        if numba.types.maybe_literal(ohn__tjpt) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ohn__tjpt]
    elif is_overload_constant_str(typ):
        ohn__tjpt = get_overload_const_str(typ)
        if numba.types.maybe_literal(ohn__tjpt) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ohn__tjpt]
    elif is_overload_constant_bool(typ):
        ohn__tjpt = get_overload_const_bool(typ)
        if numba.types.maybe_literal(ohn__tjpt) == typ:
            return [SeriesDtypeEnum.LiteralType.value, ohn__tjpt]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        uwbmc__zdq = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for dmey__zqyc in typ.names:
            uwbmc__zdq.append(dmey__zqyc)
        for dmzt__nwzns in typ.data:
            uwbmc__zdq += _dtype_to_type_enum_list_recursor(dmzt__nwzns)
        return uwbmc__zdq
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        lpd__tvvn = _dtype_to_type_enum_list_recursor(typ.categories)
        ducg__mylfb = _dtype_to_type_enum_list_recursor(typ.elem_type)
        xynm__din = _dtype_to_type_enum_list_recursor(typ.ordered)
        raj__osul = _dtype_to_type_enum_list_recursor(typ.data)
        zstxc__lep = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + lpd__tvvn + ducg__mylfb + xynm__din + raj__osul + zstxc__lep
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                fcn__fuzqk = types.float64
                hthdr__zpk = types.Array(fcn__fuzqk, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                fcn__fuzqk = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    hthdr__zpk = IntegerArrayType(fcn__fuzqk)
                else:
                    hthdr__zpk = types.Array(fcn__fuzqk, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                fcn__fuzqk = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    hthdr__zpk = IntegerArrayType(fcn__fuzqk)
                else:
                    hthdr__zpk = types.Array(fcn__fuzqk, 1, 'C')
            elif typ.dtype == types.bool_:
                fcn__fuzqk = typ.dtype
                hthdr__zpk = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(fcn__fuzqk
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(hthdr__zpk)
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
                vdveh__vif = S._bodo_meta['type_metadata'][1]
                return _dtype_from_type_enum_list(vdveh__vif)
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
        lcl__slwfz = S.dtype.unit
        if lcl__slwfz != 'ns':
            raise BodoError("Timezone-aware datetime data requires 'ns' units")
        elwoz__oelbu = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(S.
            dtype.tz)
        return PandasDatetimeTZDtype(elwoz__oelbu)
    try:
        return numpy_support.from_dtype(S.dtype)
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    nbzsj__cbbwy = cgutils.is_not_null(builder, parent_obj)
    vzlai__fqcf = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(nbzsj__cbbwy):
        ymj__fgt = pyapi.object_getattr_string(parent_obj, 'columns')
        ahv__pzqt = pyapi.call_method(ymj__fgt, '__len__', ())
        builder.store(pyapi.long_as_longlong(ahv__pzqt), vzlai__fqcf)
        pyapi.decref(ahv__pzqt)
        pyapi.decref(ymj__fgt)
    use_parent_obj = builder.and_(nbzsj__cbbwy, builder.icmp_unsigned('==',
        builder.load(vzlai__fqcf), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        wiwo__tbewe = df_typ.runtime_colname_typ
        context.nrt.incref(builder, wiwo__tbewe, dataframe_payload.columns)
        return pyapi.from_native_value(wiwo__tbewe, dataframe_payload.
            columns, c.env_manager)
    if all(isinstance(c, int) for c in df_typ.columns):
        varpq__dtoib = np.array(df_typ.columns, 'int64')
    elif all(isinstance(c, str) for c in df_typ.columns):
        varpq__dtoib = pd.array(df_typ.columns, 'string')
    else:
        varpq__dtoib = df_typ.columns
    fqcv__urnt = numba.typeof(varpq__dtoib)
    fxxc__ivoxm = context.get_constant_generic(builder, fqcv__urnt,
        varpq__dtoib)
    lzh__lrh = pyapi.from_native_value(fqcv__urnt, fxxc__ivoxm, c.env_manager)
    return lzh__lrh


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (wnsvp__hug, vcu__exg):
        with wnsvp__hug:
            pyapi.incref(obj)
            kvjm__iiqk = context.insert_const_string(c.builder.module, 'numpy')
            ivr__murv = pyapi.import_module_noblock(kvjm__iiqk)
            if df_typ.has_runtime_cols:
                tqqs__hxgrk = 0
            else:
                tqqs__hxgrk = len(df_typ.columns)
            hcsg__xuhze = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), tqqs__hxgrk))
            dvfll__ods = pyapi.call_method(ivr__murv, 'arange', (hcsg__xuhze,))
            pyapi.object_setattr_string(obj, 'columns', dvfll__ods)
            pyapi.decref(ivr__murv)
            pyapi.decref(dvfll__ods)
            pyapi.decref(hcsg__xuhze)
        with vcu__exg:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            vddgk__nqk = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            kvjm__iiqk = context.insert_const_string(c.builder.module, 'pandas'
                )
            ivr__murv = pyapi.import_module_noblock(kvjm__iiqk)
            df_obj = pyapi.call_method(ivr__murv, 'DataFrame', (pyapi.
                borrow_none(), vddgk__nqk))
            pyapi.decref(ivr__murv)
            pyapi.decref(vddgk__nqk)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    neyie__hbg = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = neyie__hbg.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        zuuzf__crb = typ.table_type
        nxlk__bka = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, zuuzf__crb, nxlk__bka)
        rew__kznsk = box_table(zuuzf__crb, nxlk__bka, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (jiqjy__rnjb, cbw__iwtdw):
            with jiqjy__rnjb:
                wcanr__bzkm = pyapi.object_getattr_string(rew__kznsk, 'arrays')
                jgqh__istc = c.pyapi.make_none()
                if n_cols is None:
                    ahv__pzqt = pyapi.call_method(wcanr__bzkm, '__len__', ())
                    eocvv__zfb = pyapi.long_as_longlong(ahv__pzqt)
                    pyapi.decref(ahv__pzqt)
                else:
                    eocvv__zfb = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, eocvv__zfb) as iusn__zdj:
                    i = iusn__zdj.index
                    sox__qzqlq = pyapi.list_getitem(wcanr__bzkm, i)
                    fbaym__czuz = c.builder.icmp_unsigned('!=', sox__qzqlq,
                        jgqh__istc)
                    with builder.if_then(fbaym__czuz):
                        otoc__xpx = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, otoc__xpx, sox__qzqlq)
                        pyapi.decref(otoc__xpx)
                pyapi.decref(wcanr__bzkm)
                pyapi.decref(jgqh__istc)
            with cbw__iwtdw:
                df_obj = builder.load(res)
                vddgk__nqk = pyapi.object_getattr_string(df_obj, 'index')
                dtxd__wri = c.pyapi.call_method(rew__kznsk, 'to_pandas', (
                    vddgk__nqk,))
                builder.store(dtxd__wri, res)
                pyapi.decref(df_obj)
                pyapi.decref(vddgk__nqk)
        pyapi.decref(rew__kznsk)
    else:
        caf__gpdt = [builder.extract_value(dataframe_payload.data, i) for i in
            range(n_cols)]
        ogcut__kwirm = typ.data
        for i, dta__ukn, qngr__oxze in zip(range(n_cols), caf__gpdt,
            ogcut__kwirm):
            zmn__bzq = cgutils.alloca_once_value(builder, dta__ukn)
            gzk__fxe = cgutils.alloca_once_value(builder, context.
                get_constant_null(qngr__oxze))
            fbaym__czuz = builder.not_(is_ll_eq(builder, zmn__bzq, gzk__fxe))
            uzpg__znj = builder.or_(builder.not_(use_parent_obj), builder.
                and_(use_parent_obj, fbaym__czuz))
            with builder.if_then(uzpg__znj):
                otoc__xpx = pyapi.long_from_longlong(context.get_constant(
                    types.int64, i))
                context.nrt.incref(builder, qngr__oxze, dta__ukn)
                arr_obj = pyapi.from_native_value(qngr__oxze, dta__ukn, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, otoc__xpx, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(otoc__xpx)
    df_obj = builder.load(res)
    lzh__lrh = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', lzh__lrh)
    pyapi.decref(lzh__lrh)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    jgqh__istc = pyapi.borrow_none()
    rhvrc__ygt = pyapi.unserialize(pyapi.serialize_object(slice))
    wav__lphxc = pyapi.call_function_objargs(rhvrc__ygt, [jgqh__istc])
    tyhe__yqj = pyapi.long_from_longlong(col_ind)
    yhsb__fgf = pyapi.tuple_pack([wav__lphxc, tyhe__yqj])
    pzz__xly = pyapi.object_getattr_string(df_obj, 'iloc')
    vmdu__oxxv = pyapi.object_getitem(pzz__xly, yhsb__fgf)
    if isinstance(data_typ, bodo.DatetimeArrayType):
        qaap__sdb = pyapi.object_getattr_string(vmdu__oxxv, 'array')
    else:
        qaap__sdb = pyapi.object_getattr_string(vmdu__oxxv, 'values')
    if isinstance(data_typ, types.Array):
        sozmy__jcf = context.insert_const_string(builder.module, 'numpy')
        cpe__leb = pyapi.import_module_noblock(sozmy__jcf)
        arr_obj = pyapi.call_method(cpe__leb, 'ascontiguousarray', (qaap__sdb,)
            )
        pyapi.decref(qaap__sdb)
        pyapi.decref(cpe__leb)
    else:
        arr_obj = qaap__sdb
    pyapi.decref(rhvrc__ygt)
    pyapi.decref(wav__lphxc)
    pyapi.decref(tyhe__yqj)
    pyapi.decref(yhsb__fgf)
    pyapi.decref(pzz__xly)
    pyapi.decref(vmdu__oxxv)
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
        neyie__hbg = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            neyie__hbg.parent, args[1], data_typ)
        sofp__gnsmi = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            nxlk__bka = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            esfj__swlyy = df_typ.table_type.type_to_blk[data_typ]
            sguw__yfnrh = getattr(nxlk__bka, f'block_{esfj__swlyy}')
            vqtkk__ikkr = ListInstance(c.context, c.builder, types.List(
                data_typ), sguw__yfnrh)
            aypg__ayb = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[col_ind])
            vqtkk__ikkr.inititem(aypg__ayb, sofp__gnsmi.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, sofp__gnsmi.value, col_ind)
        aib__hwdc = DataFramePayloadType(df_typ)
        ynh__ndp = context.nrt.meminfo_data(builder, neyie__hbg.meminfo)
        uhh__aqy = context.get_value_type(aib__hwdc).as_pointer()
        ynh__ndp = builder.bitcast(ynh__ndp, uhh__aqy)
        builder.store(dataframe_payload._getvalue(), ynh__ndp)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    if isinstance(typ.data, DatetimeArrayType):
        qaap__sdb = c.pyapi.object_getattr_string(val, 'array')
    else:
        qaap__sdb = c.pyapi.object_getattr_string(val, 'values')
    if isinstance(typ.data, types.Array):
        sozmy__jcf = c.context.insert_const_string(c.builder.module, 'numpy')
        cpe__leb = c.pyapi.import_module_noblock(sozmy__jcf)
        arr_obj = c.pyapi.call_method(cpe__leb, 'ascontiguousarray', (
            qaap__sdb,))
        c.pyapi.decref(qaap__sdb)
        c.pyapi.decref(cpe__leb)
    else:
        arr_obj = qaap__sdb
    ryrh__jzfyz = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    vddgk__nqk = c.pyapi.object_getattr_string(val, 'index')
    qnzc__aqhw = c.pyapi.to_native_value(typ.index, vddgk__nqk).value
    txa__jsv = c.pyapi.object_getattr_string(val, 'name')
    saiqs__izasr = c.pyapi.to_native_value(typ.name_typ, txa__jsv).value
    nxka__gvn = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, ryrh__jzfyz, qnzc__aqhw, saiqs__izasr)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(vddgk__nqk)
    c.pyapi.decref(txa__jsv)
    return NativeValue(nxka__gvn)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        nzgar__psy = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(nzgar__psy._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    kvjm__iiqk = c.context.insert_const_string(c.builder.module, 'pandas')
    lauh__uzvk = c.pyapi.import_module_noblock(kvjm__iiqk)
    pzd__yigot = bodo.hiframes.pd_series_ext.get_series_payload(c.context,
        c.builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, pzd__yigot.data)
    c.context.nrt.incref(c.builder, typ.index, pzd__yigot.index)
    c.context.nrt.incref(c.builder, typ.name_typ, pzd__yigot.name)
    arr_obj = c.pyapi.from_native_value(typ.data, pzd__yigot.data, c.
        env_manager)
    vddgk__nqk = c.pyapi.from_native_value(typ.index, pzd__yigot.index, c.
        env_manager)
    txa__jsv = c.pyapi.from_native_value(typ.name_typ, pzd__yigot.name, c.
        env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(lauh__uzvk, 'Series', (arr_obj, vddgk__nqk,
        dtype, txa__jsv))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(vddgk__nqk)
    c.pyapi.decref(txa__jsv)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(lauh__uzvk)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    vwg__kvldi = []
    for neuxa__jdsz in typ_list:
        if isinstance(neuxa__jdsz, int) and not isinstance(neuxa__jdsz, bool):
            zju__xdab = pyapi.long_from_longlong(lir.Constant(lir.IntType(
                64), neuxa__jdsz))
        else:
            klpt__lnfnd = numba.typeof(neuxa__jdsz)
            mssm__cumjm = context.get_constant_generic(builder, klpt__lnfnd,
                neuxa__jdsz)
            zju__xdab = pyapi.from_native_value(klpt__lnfnd, mssm__cumjm,
                env_manager)
        vwg__kvldi.append(zju__xdab)
    ckedv__thg = pyapi.list_pack(vwg__kvldi)
    for val in vwg__kvldi:
        pyapi.decref(val)
    return ckedv__thg


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    mvhcl__onx = not typ.has_runtime_cols and (not typ.is_table_format or 
        len(typ.columns) < TABLE_FORMAT_THRESHOLD)
    bszyy__cwht = 2 if mvhcl__onx else 1
    kmkek__npx = pyapi.dict_new(bszyy__cwht)
    kif__orn = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(kmkek__npx, 'dist', kif__orn)
    pyapi.decref(kif__orn)
    if mvhcl__onx:
        wfxel__jucnz = _dtype_to_type_enum_list(typ.index)
        if wfxel__jucnz != None:
            wnsk__vzpbz = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, wfxel__jucnz)
        else:
            wnsk__vzpbz = pyapi.make_none()
        fyzd__yfvi = []
        for dtype in typ.data:
            typ_list = _dtype_to_type_enum_list(dtype)
            if typ_list != None:
                ckedv__thg = type_enum_list_to_py_list_obj(pyapi, context,
                    builder, c.env_manager, typ_list)
            else:
                ckedv__thg = pyapi.make_none()
            fyzd__yfvi.append(ckedv__thg)
        cpxnx__lmdrt = pyapi.list_pack(fyzd__yfvi)
        myvsh__znv = pyapi.list_pack([wnsk__vzpbz, cpxnx__lmdrt])
        for val in fyzd__yfvi:
            pyapi.decref(val)
        pyapi.dict_setitem_string(kmkek__npx, 'type_metadata', myvsh__znv)
    pyapi.object_setattr_string(obj, '_bodo_meta', kmkek__npx)
    pyapi.decref(kmkek__npx)


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
    kmkek__npx = pyapi.dict_new(2)
    kif__orn = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    wfxel__jucnz = _dtype_to_type_enum_list(typ.index)
    if wfxel__jucnz != None:
        wnsk__vzpbz = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, wfxel__jucnz)
    else:
        wnsk__vzpbz = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            kpi__zii = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            kpi__zii = pyapi.make_none()
    else:
        kpi__zii = pyapi.make_none()
    chj__hwfq = pyapi.list_pack([wnsk__vzpbz, kpi__zii])
    pyapi.dict_setitem_string(kmkek__npx, 'type_metadata', chj__hwfq)
    pyapi.decref(chj__hwfq)
    pyapi.dict_setitem_string(kmkek__npx, 'dist', kif__orn)
    pyapi.object_setattr_string(obj, '_bodo_meta', kmkek__npx)
    pyapi.decref(kmkek__npx)
    pyapi.decref(kif__orn)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as ntnl__hcmg:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    izghb__sivw = numba.np.numpy_support.map_layout(val)
    uaofx__urpcc = not val.flags.writeable
    return types.Array(dtype, val.ndim, izghb__sivw, readonly=uaofx__urpcc)


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
    voc__gnvu = val[i]
    if isinstance(voc__gnvu, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(voc__gnvu, bytes):
        return binary_array_type
    elif isinstance(voc__gnvu, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(voc__gnvu, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(voc__gnvu))
    elif isinstance(voc__gnvu, (dict, Dict)) and all(isinstance(ssng__dzxuo,
        str) for ssng__dzxuo in voc__gnvu.keys()):
        botyk__rhh = tuple(voc__gnvu.keys())
        qcaym__fjhf = tuple(_get_struct_value_arr_type(v) for v in
            voc__gnvu.values())
        return StructArrayType(qcaym__fjhf, botyk__rhh)
    elif isinstance(voc__gnvu, (dict, Dict)):
        jrnq__wki = numba.typeof(_value_to_array(list(voc__gnvu.keys())))
        xvas__audpg = numba.typeof(_value_to_array(list(voc__gnvu.values())))
        jrnq__wki = to_str_arr_if_dict_array(jrnq__wki)
        xvas__audpg = to_str_arr_if_dict_array(xvas__audpg)
        return MapArrayType(jrnq__wki, xvas__audpg)
    elif isinstance(voc__gnvu, tuple):
        qcaym__fjhf = tuple(_get_struct_value_arr_type(v) for v in voc__gnvu)
        return TupleArrayType(qcaym__fjhf)
    if isinstance(voc__gnvu, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.StringArray)):
        if isinstance(voc__gnvu, list):
            voc__gnvu = _value_to_array(voc__gnvu)
        xuhi__gbfj = numba.typeof(voc__gnvu)
        xuhi__gbfj = to_str_arr_if_dict_array(xuhi__gbfj)
        return ArrayItemArrayType(xuhi__gbfj)
    if isinstance(voc__gnvu, datetime.date):
        return datetime_date_array_type
    if isinstance(voc__gnvu, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(voc__gnvu, decimal.Decimal):
        return DecimalArrayType(38, 18)
    raise BodoError(f'Unsupported object array with first value: {voc__gnvu}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    slf__gmjq = val.copy()
    slf__gmjq.append(None)
    dta__ukn = np.array(slf__gmjq, np.object_)
    if len(val) and isinstance(val[0], float):
        dta__ukn = np.array(val, np.float64)
    return dta__ukn


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
    qngr__oxze = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        qngr__oxze = to_nullable_type(qngr__oxze)
    return qngr__oxze
