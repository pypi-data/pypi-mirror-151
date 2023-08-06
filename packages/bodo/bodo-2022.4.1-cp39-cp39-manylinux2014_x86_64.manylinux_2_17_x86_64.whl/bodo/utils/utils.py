"""
Collection of utility functions. Needs to be refactored in separate files.
"""
import hashlib
import inspect
import keyword
import re
import warnings
from enum import Enum
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.core.ir_utils import find_callname, find_const, get_definition, guard, mk_unique_var, require
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload
from numba.np.arrayobj import get_itemsize, make_array, populate_array
import bodo
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import num_total_chars, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import NOT_CONSTANT, BodoError, BodoWarning, MetaType, is_str_arr_type
int128_type = types.Integer('int128', 128)


class CTypeEnum(Enum):
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
    Date = 13
    Datetime = 14
    Timedelta = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 20


_numba_to_c_type_map = {types.int8: CTypeEnum.Int8.value, types.uint8:
    CTypeEnum.UInt8.value, types.int32: CTypeEnum.Int32.value, types.uint32:
    CTypeEnum.UInt32.value, types.int64: CTypeEnum.Int64.value, types.
    uint64: CTypeEnum.UInt64.value, types.float32: CTypeEnum.Float32.value,
    types.float64: CTypeEnum.Float64.value, types.NPDatetime('ns'):
    CTypeEnum.Datetime.value, types.NPTimedelta('ns'): CTypeEnum.Timedelta.
    value, types.bool_: CTypeEnum.Bool.value, types.int16: CTypeEnum.Int16.
    value, types.uint16: CTypeEnum.UInt16.value, int128_type: CTypeEnum.
    Int128.value}
numba.core.errors.error_extras = {'unsupported_error': '', 'typing': '',
    'reportable': '', 'interpreter': '', 'constant_inference': ''}
np_alloc_callnames = 'empty', 'zeros', 'ones', 'full'
CONST_DICT_SLOW_WARN_THRESHOLD = 100
CONST_LIST_SLOW_WARN_THRESHOLD = 100000


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


def get_constant(func_ir, var, default=NOT_CONSTANT):
    ejig__hroa = guard(get_definition, func_ir, var)
    if ejig__hroa is None:
        return default
    if isinstance(ejig__hroa, ir.Const):
        return ejig__hroa.value
    if isinstance(ejig__hroa, ir.Var):
        return get_constant(func_ir, ejig__hroa, default)
    return default


def numba_to_c_type(t):
    if isinstance(t, bodo.libs.decimal_arr_ext.Decimal128Type):
        return CTypeEnum.Decimal.value
    if t == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return CTypeEnum.Date.value
    return _numba_to_c_type_map[t]


def is_alloc_callname(func_name, mod_name):
    return isinstance(mod_name, str) and (mod_name == 'numpy' and func_name in
        np_alloc_callnames or func_name == 'empty_inferred' and mod_name in
        ('numba.extending', 'numba.np.unsafe.ndarray') or func_name ==
        'pre_alloc_string_array' and mod_name == 'bodo.libs.str_arr_ext' or
        func_name == 'pre_alloc_binary_array' and mod_name ==
        'bodo.libs.binary_arr_ext' or func_name ==
        'alloc_random_access_string_array' and mod_name ==
        'bodo.libs.str_ext' or func_name == 'pre_alloc_array_item_array' and
        mod_name == 'bodo.libs.array_item_arr_ext' or func_name ==
        'pre_alloc_struct_array' and mod_name == 'bodo.libs.struct_arr_ext' or
        func_name == 'pre_alloc_map_array' and mod_name ==
        'bodo.libs.map_arr_ext' or func_name == 'pre_alloc_tuple_array' and
        mod_name == 'bodo.libs.tuple_arr_ext' or func_name ==
        'alloc_bool_array' and mod_name == 'bodo.libs.bool_arr_ext' or 
        func_name == 'alloc_int_array' and mod_name ==
        'bodo.libs.int_arr_ext' or func_name == 'alloc_datetime_date_array' and
        mod_name == 'bodo.hiframes.datetime_date_ext' or func_name ==
        'alloc_datetime_timedelta_array' and mod_name ==
        'bodo.hiframes.datetime_timedelta_ext' or func_name ==
        'alloc_decimal_array' and mod_name == 'bodo.libs.decimal_arr_ext' or
        func_name == 'alloc_categorical_array' and mod_name ==
        'bodo.hiframes.pd_categorical_ext' or func_name == 'gen_na_array' and
        mod_name == 'bodo.libs.array_kernels')


def find_build_tuple(func_ir, var):
    require(isinstance(var, (ir.Var, str)))
    aplev__qhdvb = get_definition(func_ir, var)
    require(isinstance(aplev__qhdvb, ir.Expr))
    require(aplev__qhdvb.op == 'build_tuple')
    return aplev__qhdvb.items


def cprint(*s):
    print(*s)


@infer_global(cprint)
class CprintInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.none, *unliteral_all(args))


typ_to_format = {types.int32: 'd', types.uint32: 'u', types.int64: 'lld',
    types.uint64: 'llu', types.float32: 'f', types.float64: 'lf', types.
    voidptr: 's'}


@lower_builtin(cprint, types.VarArg(types.Any))
def cprint_lower(context, builder, sig, args):
    for jkso__cus, val in enumerate(args):
        typ = sig.args[jkso__cus]
        if isinstance(typ, types.ArrayCTypes):
            cgutils.printf(builder, '%p ', val)
            continue
        wrb__tea = typ_to_format[typ]
        cgutils.printf(builder, '%{} '.format(wrb__tea), val)
    cgutils.printf(builder, '\n')
    return context.get_dummy_value()


def is_whole_slice(typemap, func_ir, var, accept_stride=False):
    require(typemap[var.name] == types.slice2_type or accept_stride and 
        typemap[var.name] == types.slice3_type)
    hcbn__biwuv = get_definition(func_ir, var)
    require(isinstance(hcbn__biwuv, ir.Expr) and hcbn__biwuv.op == 'call')
    assert len(hcbn__biwuv.args) == 2 or accept_stride and len(hcbn__biwuv.args
        ) == 3
    assert find_callname(func_ir, hcbn__biwuv) == ('slice', 'builtins')
    izxw__zmle = get_definition(func_ir, hcbn__biwuv.args[0])
    tue__hag = get_definition(func_ir, hcbn__biwuv.args[1])
    require(isinstance(izxw__zmle, ir.Const) and izxw__zmle.value == None)
    require(isinstance(tue__hag, ir.Const) and tue__hag.value == None)
    return True


def is_slice_equiv_arr(arr_var, index_var, func_ir, equiv_set,
    accept_stride=False):
    gkhr__usez = get_definition(func_ir, index_var)
    require(find_callname(func_ir, gkhr__usez) == ('slice', 'builtins'))
    require(len(gkhr__usez.args) in (2, 3))
    require(find_const(func_ir, gkhr__usez.args[0]) in (0, None))
    require(equiv_set.is_equiv(gkhr__usez.args[1], arr_var.name + '#0'))
    require(accept_stride or len(gkhr__usez.args) == 2 or find_const(
        func_ir, gkhr__usez.args[2]) == 1)
    return True


def get_slice_step(typemap, func_ir, var):
    require(typemap[var.name] == types.slice3_type)
    hcbn__biwuv = get_definition(func_ir, var)
    require(isinstance(hcbn__biwuv, ir.Expr) and hcbn__biwuv.op == 'call')
    assert len(hcbn__biwuv.args) == 3
    return hcbn__biwuv.args[2]


def is_array_typ(var_typ, include_index_series=True):
    return is_np_array_typ(var_typ) or var_typ in (string_array_type, bodo.
        binary_array_type, bodo.dict_str_arr_type, bodo.hiframes.split_impl
        .string_array_split_view_type, bodo.hiframes.datetime_date_ext.
        datetime_date_array_type, bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type, boolean_array, bodo.libs.str_ext.
        random_access_string_array) or isinstance(var_typ, (
        IntegerArrayType, bodo.libs.decimal_arr_ext.DecimalArrayType, bodo.
        hiframes.pd_categorical_ext.CategoricalArrayType, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType, bodo.libs.struct_arr_ext.
        StructArrayType, bodo.libs.interval_arr_ext.IntervalArrayType, bodo
        .libs.tuple_arr_ext.TupleArrayType, bodo.libs.map_arr_ext.
        MapArrayType, bodo.libs.csr_matrix_ext.CSRMatrixType, bodo.
        DatetimeArrayType)) or include_index_series and (isinstance(var_typ,
        (bodo.hiframes.pd_series_ext.SeriesType, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType)) or bodo.hiframes.pd_index_ext.
        is_pd_index_type(var_typ))


def is_np_array_typ(var_typ):
    return isinstance(var_typ, types.Array)


def is_distributable_typ(var_typ):
    return is_array_typ(var_typ) or isinstance(var_typ, bodo.hiframes.table
        .TableType) or isinstance(var_typ, bodo.hiframes.pd_dataframe_ext.
        DataFrameType) or isinstance(var_typ, types.List
        ) and is_distributable_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_typ(var_typ.value_type)


def is_distributable_tuple_typ(var_typ):
    return isinstance(var_typ, types.BaseTuple) and any(
        is_distributable_typ(t) or is_distributable_tuple_typ(t) for t in
        var_typ.types) or isinstance(var_typ, types.List
        ) and is_distributable_tuple_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_tuple_typ(var_typ.value_type
        ) or isinstance(var_typ, types.iterators.EnumerateType) and (
        is_distributable_typ(var_typ.yield_type[1]) or
        is_distributable_tuple_typ(var_typ.yield_type[1]))


@numba.generated_jit(nopython=True, cache=True)
def build_set_seen_na(A):

    def impl(A):
        s = dict()
        tqr__ocj = False
        for jkso__cus in range(len(A)):
            if bodo.libs.array_kernels.isna(A, jkso__cus):
                tqr__ocj = True
                continue
            s[A[jkso__cus]] = 0
        return s, tqr__ocj
    return impl


def empty_like_type(n, arr):
    return np.empty(n, arr.dtype)


@overload(empty_like_type, no_unliteral=True)
def empty_like_type_overload(n, arr):
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda n, arr: bodo.hiframes.pd_categorical_ext.
            alloc_categorical_array(n, arr.dtype))
    if isinstance(arr, types.Array):
        return lambda n, arr: np.empty(n, arr.dtype)
    if isinstance(arr, types.List) and arr.dtype == string_type:

        def empty_like_type_str_list(n, arr):
            return [''] * n
        return empty_like_type_str_list
    if isinstance(arr, types.List) and arr.dtype == bytes_type:

        def empty_like_type_binary_list(n, arr):
            return [b''] * n
        return empty_like_type_binary_list
    if isinstance(arr, IntegerArrayType):
        wqa__kqeoj = arr.dtype

        def empty_like_type_int_arr(n, arr):
            return bodo.libs.int_arr_ext.alloc_int_array(n, wqa__kqeoj)
        return empty_like_type_int_arr
    if arr == boolean_array:

        def empty_like_type_bool_arr(n, arr):
            return bodo.libs.bool_arr_ext.alloc_bool_array(n)
        return empty_like_type_bool_arr
    if arr == bodo.hiframes.datetime_date_ext.datetime_date_array_type:

        def empty_like_type_datetime_date_arr(n, arr):
            return bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(n)
        return empty_like_type_datetime_date_arr
    if (arr == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type):

        def empty_like_type_datetime_timedelta_arr(n, arr):
            return (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(n))
        return empty_like_type_datetime_timedelta_arr
    if isinstance(arr, bodo.libs.decimal_arr_ext.DecimalArrayType):
        precision = arr.precision
        scale = arr.scale

        def empty_like_type_decimal_arr(n, arr):
            return bodo.libs.decimal_arr_ext.alloc_decimal_array(n,
                precision, scale)
        return empty_like_type_decimal_arr
    assert arr == string_array_type

    def empty_like_type_str_arr(n, arr):
        fjh__gaytz = 20
        if len(arr) != 0:
            fjh__gaytz = num_total_chars(arr) // len(arr)
        return pre_alloc_string_array(n, n * fjh__gaytz)
    return empty_like_type_str_arr


def _empty_nd_impl(context, builder, arrtype, shapes):
    detv__dxjkt = make_array(arrtype)
    rysze__hizve = detv__dxjkt(context, builder)
    pta__aghgd = context.get_data_type(arrtype.dtype)
    rti__vxfmq = context.get_constant(types.intp, get_itemsize(context,
        arrtype))
    hfbei__fxuyo = context.get_constant(types.intp, 1)
    twqkj__ckq = lir.Constant(lir.IntType(1), 0)
    for s in shapes:
        hzuvu__tgjs = builder.smul_with_overflow(hfbei__fxuyo, s)
        hfbei__fxuyo = builder.extract_value(hzuvu__tgjs, 0)
        twqkj__ckq = builder.or_(twqkj__ckq, builder.extract_value(
            hzuvu__tgjs, 1))
    if arrtype.ndim == 0:
        hmimj__sxbzi = ()
    elif arrtype.layout == 'C':
        hmimj__sxbzi = [rti__vxfmq]
        for zotb__dzk in reversed(shapes[1:]):
            hmimj__sxbzi.append(builder.mul(hmimj__sxbzi[-1], zotb__dzk))
        hmimj__sxbzi = tuple(reversed(hmimj__sxbzi))
    elif arrtype.layout == 'F':
        hmimj__sxbzi = [rti__vxfmq]
        for zotb__dzk in shapes[:-1]:
            hmimj__sxbzi.append(builder.mul(hmimj__sxbzi[-1], zotb__dzk))
        hmimj__sxbzi = tuple(hmimj__sxbzi)
    else:
        raise NotImplementedError(
            "Don't know how to allocate array with layout '{0}'.".format(
            arrtype.layout))
    ynsfs__gkpp = builder.smul_with_overflow(hfbei__fxuyo, rti__vxfmq)
    enupm__tstvs = builder.extract_value(ynsfs__gkpp, 0)
    twqkj__ckq = builder.or_(twqkj__ckq, builder.extract_value(ynsfs__gkpp, 1))
    with builder.if_then(twqkj__ckq, likely=False):
        cgutils.printf(builder,
            'array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.'
            )
    dtype = arrtype.dtype
    htl__dxm = context.get_preferred_array_alignment(dtype)
    ukv__diz = context.get_constant(types.uint32, htl__dxm)
    bbve__kba = context.nrt.meminfo_alloc_aligned(builder, size=
        enupm__tstvs, align=ukv__diz)
    data = context.nrt.meminfo_data(builder, bbve__kba)
    ecou__ozzm = context.get_value_type(types.intp)
    ldoi__neuv = cgutils.pack_array(builder, shapes, ty=ecou__ozzm)
    dhdp__keblb = cgutils.pack_array(builder, hmimj__sxbzi, ty=ecou__ozzm)
    populate_array(rysze__hizve, data=builder.bitcast(data, pta__aghgd.
        as_pointer()), shape=ldoi__neuv, strides=dhdp__keblb, itemsize=
        rti__vxfmq, meminfo=bbve__kba)
    return rysze__hizve


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.np.arrayobj._empty_nd_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b6a998927680caa35917a553c79704e9d813d8f1873d83a5f8513837c159fa29':
        warnings.warn('numba.np.arrayobj._empty_nd_impl has changed')


def alloc_arr_tup(n, arr_tup, init_vals=()):
    but__vtszu = []
    for tsw__afajv in arr_tup:
        but__vtszu.append(np.empty(n, tsw__afajv.dtype))
    return tuple(but__vtszu)


@overload(alloc_arr_tup, no_unliteral=True)
def alloc_arr_tup_overload(n, data, init_vals=()):
    pvwp__awur = data.count
    hhm__pwvw = ','.join(['empty_like_type(n, data[{}])'.format(jkso__cus) for
        jkso__cus in range(pvwp__awur)])
    if init_vals != ():
        hhm__pwvw = ','.join(['np.full(n, init_vals[{}], data[{}].dtype)'.
            format(jkso__cus, jkso__cus) for jkso__cus in range(pvwp__awur)])
    efqv__czon = 'def f(n, data, init_vals=()):\n'
    efqv__czon += '  return ({}{})\n'.format(hhm__pwvw, ',' if pvwp__awur ==
        1 else '')
    yjtv__zkps = {}
    exec(efqv__czon, {'empty_like_type': empty_like_type, 'np': np}, yjtv__zkps
        )
    itst__urep = yjtv__zkps['f']
    return itst__urep


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_to_scalar(n):
    if isinstance(n, types.BaseTuple) and len(n.types) == 1:
        return lambda n: n[0]
    return lambda n: n


def alloc_type(n, t, s=None):
    return np.empty(n, t.dtype)


@overload(alloc_type)
def overload_alloc_type(n, t, s=None):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(typ,
        'bodo.alloc_type()')
    if is_str_arr_type(typ):
        return (lambda n, t, s=None: bodo.libs.str_arr_ext.
            pre_alloc_string_array(n, s[0]))
    if typ == bodo.binary_array_type:
        return (lambda n, t, s=None: bodo.libs.binary_arr_ext.
            pre_alloc_binary_array(n, s[0]))
    if isinstance(typ, bodo.libs.array_item_arr_ext.ArrayItemArrayType):
        dtype = typ.dtype
        return (lambda n, t, s=None: bodo.libs.array_item_arr_ext.
            pre_alloc_array_item_array(n, s, dtype))
    if isinstance(typ, bodo.libs.struct_arr_ext.StructArrayType):
        dtypes = typ.data
        names = typ.names
        return (lambda n, t, s=None: bodo.libs.struct_arr_ext.
            pre_alloc_struct_array(n, s, dtypes, names))
    if isinstance(typ, bodo.libs.map_arr_ext.MapArrayType):
        struct_typ = bodo.libs.struct_arr_ext.StructArrayType((typ.
            key_arr_type, typ.value_arr_type), ('key', 'value'))
        return lambda n, t, s=None: bodo.libs.map_arr_ext.pre_alloc_map_array(n
            , s, struct_typ)
    if isinstance(typ, bodo.libs.tuple_arr_ext.TupleArrayType):
        dtypes = typ.data
        return (lambda n, t, s=None: bodo.libs.tuple_arr_ext.
            pre_alloc_tuple_array(n, s, dtypes))
    if isinstance(typ, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        if isinstance(t, types.TypeRef):
            if typ.dtype.categories is None:
                raise BodoError(
                    'UDFs or Groupbys that return Categorical values must have categories known at compile time.'
                    )
            is_ordered = typ.dtype.ordered
            int_type = typ.dtype.int_type
            new_cats_arr = pd.CategoricalDtype(typ.dtype.categories, is_ordered
                ).categories.values
            new_cats_tup = MetaType(tuple(new_cats_arr))
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, bodo.hiframes.pd_categorical_ext
                .init_cat_dtype(bodo.utils.conversion.index_from_array(
                new_cats_arr), is_ordered, int_type, new_cats_tup)))
        else:
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, t.dtype))
    if typ.dtype == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return (lambda n, t, s=None: bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(n))
    if (typ.dtype == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_type):
        return (lambda n, t, s=None: bodo.hiframes.datetime_timedelta_ext.
            alloc_datetime_timedelta_array(n))
    if isinstance(typ, DecimalArrayType):
        precision = typ.dtype.precision
        scale = typ.dtype.scale
        return (lambda n, t, s=None: bodo.libs.decimal_arr_ext.
            alloc_decimal_array(n, precision, scale))
    dtype = numba.np.numpy_support.as_dtype(typ.dtype)
    if isinstance(typ, IntegerArrayType):
        return lambda n, t, s=None: bodo.libs.int_arr_ext.alloc_int_array(n,
            dtype)
    if typ == boolean_array:
        return lambda n, t, s=None: bodo.libs.bool_arr_ext.alloc_bool_array(n)
    return lambda n, t, s=None: np.empty(n, dtype)


def astype(A, t):
    return A.astype(t.dtype)


@overload(astype, no_unliteral=True)
def overload_astype(A, t):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    dtype = typ.dtype
    if A == typ:
        return lambda A, t: A
    if isinstance(A, (types.Array, IntegerArrayType)) and isinstance(typ,
        types.Array):
        return lambda A, t: A.astype(dtype)
    if isinstance(typ, IntegerArrayType):
        return lambda A, t: bodo.libs.int_arr_ext.init_integer_array(A.
            astype(dtype), np.full(len(A) + 7 >> 3, 255, np.uint8))
    if (A == bodo.libs.dict_arr_ext.dict_str_arr_type and typ == bodo.
        string_array_type):
        return lambda A, t: bodo.utils.typing.decode_if_dict_array(A)
    raise BodoError(f'cannot convert array type {A} to {typ}')


def full_type(n, val, t):
    return np.full(n, val, t.dtype)


@overload(full_type, no_unliteral=True)
def overload_full_type(n, val, t):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    if isinstance(typ, types.Array):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: np.full(n, val, dtype)
    if isinstance(typ, IntegerArrayType):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: bodo.libs.int_arr_ext.init_integer_array(np
            .full(n, val, dtype), np.full(tuple_to_scalar(n) + 7 >> 3, 255,
            np.uint8))
    if typ == boolean_array:
        return lambda n, val, t: bodo.libs.bool_arr_ext.init_bool_array(np.
            full(n, val, np.bool_), np.full(tuple_to_scalar(n) + 7 >> 3, 
            255, np.uint8))
    if typ == string_array_type:

        def impl_str(n, val, t):
            dfwo__kggv = n * len(val)
            A = pre_alloc_string_array(n, dfwo__kggv)
            for jkso__cus in range(n):
                A[jkso__cus] = val
            return A
        return impl_str

    def impl(n, val, t):
        A = alloc_type(n, typ, (-1,))
        for jkso__cus in range(n):
            A[jkso__cus] = val
        return A
    return impl


@intrinsic
def is_null_pointer(typingctx, ptr_typ=None):

    def codegen(context, builder, signature, args):
        uul__shz, = args
        rwwta__bam = context.get_constant_null(ptr_typ)
        return builder.icmp_unsigned('==', uul__shz, rwwta__bam)
    return types.bool_(ptr_typ), codegen


@intrinsic
def is_null_value(typingctx, val_typ=None):

    def codegen(context, builder, signature, args):
        val, = args
        tky__rnv = cgutils.alloca_once_value(builder, val)
        ayjy__xmao = cgutils.alloca_once_value(builder, context.
            get_constant_null(val_typ))
        return is_ll_eq(builder, tky__rnv, ayjy__xmao)
    return types.bool_(val_typ), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_list_to_array(A, data, elem_type):
    elem_type = elem_type.instance_type if isinstance(elem_type, types.TypeRef
        ) else elem_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'tuple_list_to_array()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(elem_type,
        'tuple_list_to_array()')
    efqv__czon = 'def impl(A, data, elem_type):\n'
    efqv__czon += '  for i, d in enumerate(data):\n'
    if elem_type == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        efqv__czon += (
            '    A[i] = bodo.utils.conversion.unbox_if_timestamp(d)\n')
    else:
        efqv__czon += '    A[i] = d\n'
    yjtv__zkps = {}
    exec(efqv__czon, {'bodo': bodo}, yjtv__zkps)
    impl = yjtv__zkps['impl']
    return impl


def object_length(c, obj):
    bzo__rvcy = c.context.get_argument_type(types.pyobject)
    qwbjn__jioic = lir.FunctionType(lir.IntType(64), [bzo__rvcy])
    ypiyr__yowt = cgutils.get_or_insert_function(c.builder.module,
        qwbjn__jioic, name='PyObject_Length')
    return c.builder.call(ypiyr__yowt, (obj,))


@intrinsic
def incref(typingctx, data=None):

    def codegen(context, builder, signature, args):
        wgxw__hiqsx, = args
        context.nrt.incref(builder, signature.args[0], wgxw__hiqsx)
    return types.void(data), codegen


def gen_getitem(out_var, in_var, ind, calltypes, nodes):
    xqrmq__bmh = out_var.loc
    nftk__ikalc = ir.Expr.static_getitem(in_var, ind, None, xqrmq__bmh)
    calltypes[nftk__ikalc] = None
    nodes.append(ir.Assign(nftk__ikalc, out_var, xqrmq__bmh))


def is_static_getsetitem(node):
    return is_expr(node, 'static_getitem') or isinstance(node, ir.StaticSetItem
        )


def get_getsetitem_index_var(node, typemap, nodes):
    index_var = node.index_var if is_static_getsetitem(node) else node.index
    if index_var is None:
        assert is_static_getsetitem(node)
        try:
            nwc__cxbbl = types.literal(node.index)
        except:
            nwc__cxbbl = numba.typeof(node.index)
        index_var = ir.Var(node.value.scope, ir_utils.mk_unique_var(
            'dummy_index'), node.loc)
        typemap[index_var.name] = nwc__cxbbl
        nodes.append(ir.Assign(ir.Const(node.index, node.loc), index_var,
            node.loc))
    return index_var


import copy
ir.Const.__deepcopy__ = lambda self, memo: ir.Const(self.value, copy.
    deepcopy(self.loc))


def is_call_assign(stmt):
    return isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
        ) and stmt.value.op == 'call'


def is_call(expr):
    return isinstance(expr, ir.Expr) and expr.op == 'call'


def is_var_assign(inst):
    return isinstance(inst, ir.Assign) and isinstance(inst.value, ir.Var)


def is_assign(inst):
    return isinstance(inst, ir.Assign)


def is_expr(val, op):
    return isinstance(val, ir.Expr) and val.op == op


def sanitize_varname(varname):
    if isinstance(varname, (tuple, list)):
        varname = '_'.join(sanitize_varname(v) for v in varname)
    varname = str(varname)
    meh__xmi = re.sub('\\W+', '_', varname)
    if not meh__xmi or not meh__xmi[0].isalpha():
        meh__xmi = '_' + meh__xmi
    if not meh__xmi.isidentifier() or keyword.iskeyword(meh__xmi):
        meh__xmi = mk_unique_var('new_name').replace('.', '_')
    return meh__xmi


def dump_node_list(node_list):
    for n in node_list:
        print('   ', n)


def debug_prints():
    return numba.core.config.DEBUG_ARRAY_OPT == 1


@overload(reversed)
def list_reverse(A):
    if isinstance(A, types.List):

        def impl_reversed(A):
            mvj__qoom = len(A)
            for jkso__cus in range(mvj__qoom):
                yield A[mvj__qoom - 1 - jkso__cus]
        return impl_reversed


@numba.njit
def count_nonnan(a):
    return np.count_nonzero(~np.isnan(a))


@numba.njit
def nanvar_ddof1(a):
    vwdv__qxxm = count_nonnan(a)
    if vwdv__qxxm <= 1:
        return np.nan
    return np.nanvar(a) * (vwdv__qxxm / (vwdv__qxxm - 1))


@numba.njit
def nanstd_ddof1(a):
    return np.sqrt(nanvar_ddof1(a))


def has_supported_h5py():
    try:
        import h5py
        from bodo.io import _hdf5
    except ImportError as uvjo__gluj:
        ogd__lnrl = False
    else:
        ogd__lnrl = h5py.version.hdf5_version_tuple[1] in (10, 12)
    return ogd__lnrl


def check_h5py():
    if not has_supported_h5py():
        raise BodoError("install 'h5py' package to enable hdf5 support")


def has_pyarrow():
    try:
        import pyarrow
    except ImportError as uvjo__gluj:
        xfnjn__wrx = False
    else:
        xfnjn__wrx = True
    return xfnjn__wrx


def has_scipy():
    try:
        import scipy
    except ImportError as uvjo__gluj:
        nrz__lbhuo = False
    else:
        nrz__lbhuo = True
    return nrz__lbhuo


@intrinsic
def check_and_propagate_cpp_exception(typingctx):

    def codegen(context, builder, sig, args):
        yyo__xymv = context.get_python_api(builder)
        axumh__unh = yyo__xymv.err_occurred()
        efig__ljmo = cgutils.is_not_null(builder, axumh__unh)
        with builder.if_then(efig__ljmo):
            builder.ret(numba.core.callconv.RETCODE_EXC)
    return types.void(), codegen


def inlined_check_and_propagate_cpp_exception(context, builder):
    yyo__xymv = context.get_python_api(builder)
    axumh__unh = yyo__xymv.err_occurred()
    efig__ljmo = cgutils.is_not_null(builder, axumh__unh)
    with builder.if_then(efig__ljmo):
        builder.ret(numba.core.callconv.RETCODE_EXC)


@numba.njit
def check_java_installation(fname):
    with numba.objmode():
        check_java_installation_(fname)


def check_java_installation_(fname):
    if not fname.startswith('hdfs://'):
        return
    import shutil
    if not shutil.which('java'):
        rxfp__yovxx = (
            "Java not found. Make sure openjdk is installed for hdfs. openjdk can be installed by calling 'conda install openjdk=8 -c conda-forge'."
            )
        raise BodoError(rxfp__yovxx)


dt_err = """
        If you are trying to set NULL values for timedelta64 in regular Python, 

        consider using np.timedelta64('nat') instead of None
        """


@lower_constant(types.List)
def lower_constant_list(context, builder, typ, pyval):
    if len(pyval) > CONST_LIST_SLOW_WARN_THRESHOLD:
        warnings.warn(BodoWarning(
            'Using large global lists can result in long compilation times. Please pass large lists as arguments to JIT functions or use arrays.'
            ))
    jqedr__uty = []
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in list must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
        jqedr__uty.append(context.get_constant_generic(builder, typ.dtype, a))
    eoq__vvszo = context.get_constant_generic(builder, types.int64, len(pyval))
    xhj__jzgc = context.get_constant_generic(builder, types.bool_, False)
    sdvmz__cci = context.get_constant_null(types.pyobject)
    jmcy__lhnox = lir.Constant.literal_struct([eoq__vvszo, eoq__vvszo,
        xhj__jzgc] + jqedr__uty)
    jmcy__lhnox = cgutils.global_constant(builder, '.const.payload',
        jmcy__lhnox).bitcast(cgutils.voidptr_t)
    iguh__bvb = context.get_constant(types.int64, -1)
    xrsn__ngepo = context.get_constant_null(types.voidptr)
    bbve__kba = lir.Constant.literal_struct([iguh__bvb, xrsn__ngepo,
        xrsn__ngepo, jmcy__lhnox, iguh__bvb])
    bbve__kba = cgutils.global_constant(builder, '.const.meminfo', bbve__kba
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([bbve__kba, sdvmz__cci])


@lower_constant(types.Set)
def lower_constant_set(context, builder, typ, pyval):
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in set must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
    mmziv__didol = types.List(typ.dtype)
    nttq__pgz = context.get_constant_generic(builder, mmziv__didol, list(pyval)
        )
    tkd__mmp = context.compile_internal(builder, lambda l: set(l), types.
        Set(typ.dtype)(mmziv__didol), [nttq__pgz])
    return tkd__mmp


def lower_const_dict_fast_path(context, builder, typ, pyval):
    from bodo.utils.typing import can_replace
    lceh__wiet = pd.Series(pyval.keys()).values
    lwfxq__brv = pd.Series(pyval.values()).values
    cox__szjk = bodo.typeof(lceh__wiet)
    natm__ufvms = bodo.typeof(lwfxq__brv)
    require(cox__szjk.dtype == typ.key_type or can_replace(typ.key_type,
        cox__szjk.dtype))
    require(natm__ufvms.dtype == typ.value_type or can_replace(typ.
        value_type, natm__ufvms.dtype))
    pmu__cdtid = context.get_constant_generic(builder, cox__szjk, lceh__wiet)
    vrf__mhq = context.get_constant_generic(builder, natm__ufvms, lwfxq__brv)

    def create_dict(keys, vals):
        dzb__yyxn = {}
        for k, v in zip(keys, vals):
            dzb__yyxn[k] = v
        return dzb__yyxn
    tuc__sxne = context.compile_internal(builder, create_dict, typ(
        cox__szjk, natm__ufvms), [pmu__cdtid, vrf__mhq])
    return tuc__sxne


@lower_constant(types.DictType)
def lower_constant_dict(context, builder, typ, pyval):
    try:
        return lower_const_dict_fast_path(context, builder, typ, pyval)
    except:
        pass
    if len(pyval) > CONST_DICT_SLOW_WARN_THRESHOLD:
        warnings.warn(BodoWarning(
            'Using large global dictionaries can result in long compilation times. Please pass large dictionaries as arguments to JIT functions.'
            ))
    slwv__udtq = typ.key_type
    pzz__bvmpe = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(slwv__udtq, pzz__bvmpe)
    tuc__sxne = context.compile_internal(builder, make_dict, typ(), [])

    def set_dict_val(d, k, v):
        d[k] = v
    for k, v in pyval.items():
        ufh__tpoct = context.get_constant_generic(builder, slwv__udtq, k)
        qyun__yud = context.get_constant_generic(builder, pzz__bvmpe, v)
        context.compile_internal(builder, set_dict_val, types.none(typ,
            slwv__udtq, pzz__bvmpe), [tuc__sxne, ufh__tpoct, qyun__yud])
    return tuc__sxne
