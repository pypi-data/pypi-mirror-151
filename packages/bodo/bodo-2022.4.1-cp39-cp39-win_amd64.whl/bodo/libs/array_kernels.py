"""
Implements array kernels such as median and quantile.
"""
import hashlib
import inspect
import math
import operator
import re
import warnings
from math import sqrt
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types, typing
from numba.core.imputils import lower_builtin
from numba.core.ir_utils import find_const, guard
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload, overload_attribute, register_jitable
from numba.np.arrayobj import make_array
from numba.np.numpy_support import as_dtype
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, init_categorical_array
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs import quantile_alg
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, drop_duplicates_table, info_from_table, info_to_array, sample_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import DictionaryArrayType
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import str_arr_set_na, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, check_unsupported_args, decode_if_dict_array, element_type, find_common_np_dtype, get_overload_const_bool, get_overload_const_list, get_overload_const_str, is_overload_none, is_str_arr_type, raise_bodo_error, to_str_arr_if_dict_array
from bodo.utils.utils import build_set_seen_na, check_and_propagate_cpp_exception, numba_to_c_type, unliteral_all
ll.add_symbol('quantile_sequential', quantile_alg.quantile_sequential)
ll.add_symbol('quantile_parallel', quantile_alg.quantile_parallel)
MPI_ROOT = 0
sum_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value)
max_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Max.value)
min_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Min.value)


def isna(arr, i):
    return False


@overload(isna)
def overload_isna(arr, i):
    i = types.unliteral(i)
    if arr == string_array_type:
        return lambda arr, i: bodo.libs.str_arr_ext.str_arr_is_na(arr, i)
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type,
        datetime_timedelta_array_type, string_array_split_view_type):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._null_bitmap, i)
    if isinstance(arr, ArrayItemArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, StructArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.struct_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, TupleArrayType):
        return lambda arr, i: bodo.libs.array_kernels.isna(arr._data, i)
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return lambda arr, i: arr.codes[i] == -1
    if arr == bodo.binary_array_type:
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, types.List):
        if arr.dtype == types.none:
            return lambda arr, i: True
        elif isinstance(arr.dtype, types.optional):
            return lambda arr, i: arr[i] is None
        else:
            return lambda arr, i: False
    if isinstance(arr, bodo.NullableTupleType):
        return lambda arr, i: arr._null_values[i]
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._indices._null_bitmap, i) or bodo.libs.array_kernels.isna(arr.
            _data, arr._indices[i])
    if isinstance(arr, DatetimeArrayType):
        return lambda arr, i: np.isnat(arr._data[i])
    assert isinstance(arr, types.Array), f'Invalid array type in isna(): {arr}'
    dtype = arr.dtype
    if isinstance(dtype, types.Float):
        return lambda arr, i: np.isnan(arr[i])
    if isinstance(dtype, (types.NPDatetime, types.NPTimedelta)):
        return lambda arr, i: np.isnat(arr[i])
    return lambda arr, i: False


def setna(arr, ind, int_nan_const=0):
    arr[ind] = np.nan


@overload(setna, no_unliteral=True)
def setna_overload(arr, ind, int_nan_const=0):
    if isinstance(arr.dtype, types.Float):
        return setna
    if isinstance(arr.dtype, (types.NPDatetime, types.NPTimedelta)):
        iftti__uyxop = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = iftti__uyxop
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        iftti__uyxop = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = iftti__uyxop
        return _setnan_impl
    if arr == string_array_type:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = ''
            str_arr_set_na(arr, ind)
        return impl
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, ind, int_nan_const=0: bodo.libs.array_kernels.setna(
            arr._indices, ind)
    if arr == boolean_array:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = False
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)):
        return (lambda arr, ind, int_nan_const=0: bodo.libs.int_arr_ext.
            set_bit_to_arr(arr._null_bitmap, ind, 0))
    if arr == bodo.binary_array_type:

        def impl_binary_arr(arr, ind, int_nan_const=0):
            egul__yppmb = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            egul__yppmb[ind + 1] = egul__yppmb[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            egul__yppmb = bodo.libs.array_item_arr_ext.get_offsets(arr)
            egul__yppmb[ind + 1] = egul__yppmb[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.struct_arr_ext.StructArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.struct_arr_ext.
                get_null_bitmap(arr), ind, 0)
            data = bodo.libs.struct_arr_ext.get_data(arr)
            setna_tup(data, ind)
        return impl
    if isinstance(arr, TupleArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._data, ind)
        return impl
    if arr.dtype == types.bool_:

        def b_set(arr, ind, int_nan_const=0):
            arr[ind] = False
        return b_set
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):

        def setna_cat(arr, ind, int_nan_const=0):
            arr.codes[ind] = -1
        return setna_cat
    if isinstance(arr.dtype, types.Integer):

        def setna_int(arr, ind, int_nan_const=0):
            arr[ind] = int_nan_const
        return setna_int
    if arr == datetime_date_array_type:

        def setna_datetime_date(arr, ind, int_nan_const=0):
            arr._data[ind] = (1970 << 32) + (1 << 16) + 1
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_date
    if arr == datetime_timedelta_array_type:

        def setna_datetime_timedelta(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._days_data, ind)
            bodo.libs.array_kernels.setna(arr._seconds_data, ind)
            bodo.libs.array_kernels.setna(arr._microseconds_data, ind)
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_timedelta
    return lambda arr, ind, int_nan_const=0: None


def setna_tup(arr_tup, ind, int_nan_const=0):
    for arr in arr_tup:
        arr[ind] = np.nan


@overload(setna_tup, no_unliteral=True)
def overload_setna_tup(arr_tup, ind, int_nan_const=0):
    pgwd__sdq = arr_tup.count
    lgm__apxaw = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(pgwd__sdq):
        lgm__apxaw += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    lgm__apxaw += '  return\n'
    uvss__fjs = {}
    exec(lgm__apxaw, {'setna': setna}, uvss__fjs)
    impl = uvss__fjs['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        jqg__igl = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(jqg__igl.start, jqg__igl.stop, jqg__igl.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        jsxw__gqot = 'n'
        cuha__rjcae = 'n_pes'
        vhw__hgzk = 'min_op'
    else:
        jsxw__gqot = 'n-1, -1, -1'
        cuha__rjcae = '-1'
        vhw__hgzk = 'max_op'
    lgm__apxaw = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {cuha__rjcae}
    for i in range({jsxw__gqot}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {vhw__hgzk}))
        if possible_valid_rank != {cuha__rjcae}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    uvss__fjs = {}
    exec(lgm__apxaw, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, uvss__fjs)
    impl = uvss__fjs['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    uusol__asrn = array_to_info(arr)
    _median_series_computation(res, uusol__asrn, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(uusol__asrn)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    uusol__asrn = array_to_info(arr)
    _autocorr_series_computation(res, uusol__asrn, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(uusol__asrn)


@numba.njit
def autocorr(arr, lag=1, parallel=False):
    res = np.empty(1, types.float64)
    autocorr_series_computation(res.ctypes, arr, lag, parallel)
    return res[0]


ll.add_symbol('compute_series_monotonicity', quantile_alg.
    compute_series_monotonicity)
_compute_series_monotonicity = types.ExternalFunction(
    'compute_series_monotonicity', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def series_monotonicity_call(res, arr, inc_dec, is_parallel):
    uusol__asrn = array_to_info(arr)
    _compute_series_monotonicity(res, uusol__asrn, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(uusol__asrn)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    wzzh__edzf = res[0] > 0.5
    return wzzh__edzf


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        rip__eng = '-'
        nnbv__vll = 'index_arr[0] > threshhold_date'
        jsxw__gqot = '1, n+1'
        mbq__rada = 'index_arr[-i] <= threshhold_date'
        kicw__gpev = 'i - 1'
    else:
        rip__eng = '+'
        nnbv__vll = 'index_arr[-1] < threshhold_date'
        jsxw__gqot = 'n'
        mbq__rada = 'index_arr[i] >= threshhold_date'
        kicw__gpev = 'i'
    lgm__apxaw = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        lgm__apxaw += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        lgm__apxaw += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            lgm__apxaw += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            lgm__apxaw += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            lgm__apxaw += '    else:\n'
            lgm__apxaw += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            lgm__apxaw += (
                f'    threshhold_date = initial_date {rip__eng} date_offset\n')
    else:
        lgm__apxaw += f'  threshhold_date = initial_date {rip__eng} offset\n'
    lgm__apxaw += '  local_valid = 0\n'
    lgm__apxaw += f'  n = len(index_arr)\n'
    lgm__apxaw += f'  if n:\n'
    lgm__apxaw += f'    if {nnbv__vll}:\n'
    lgm__apxaw += '      loc_valid = n\n'
    lgm__apxaw += '    else:\n'
    lgm__apxaw += f'      for i in range({jsxw__gqot}):\n'
    lgm__apxaw += f'        if {mbq__rada}:\n'
    lgm__apxaw += f'          loc_valid = {kicw__gpev}\n'
    lgm__apxaw += '          break\n'
    lgm__apxaw += '  if is_parallel:\n'
    lgm__apxaw += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    lgm__apxaw += '    return total_valid\n'
    lgm__apxaw += '  else:\n'
    lgm__apxaw += '    return loc_valid\n'
    uvss__fjs = {}
    exec(lgm__apxaw, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, uvss__fjs)
    return uvss__fjs['impl']


def quantile(A, q):
    return 0


def quantile_parallel(A, q):
    return 0


@infer_global(quantile)
@infer_global(quantile_parallel)
class QuantileType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) in [2, 3]
        return signature(types.float64, *unliteral_all(args))


@lower_builtin(quantile, types.Array, types.float64)
@lower_builtin(quantile, IntegerArrayType, types.float64)
@lower_builtin(quantile, BooleanArrayType, types.float64)
def lower_dist_quantile_seq(context, builder, sig, args):
    xjnb__ygc = numba_to_c_type(sig.args[0].dtype)
    rkt__dmyos = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), xjnb__ygc))
    qti__ydgpw = args[0]
    isebb__adzw = sig.args[0]
    if isinstance(isebb__adzw, (IntegerArrayType, BooleanArrayType)):
        qti__ydgpw = cgutils.create_struct_proxy(isebb__adzw)(context,
            builder, qti__ydgpw).data
        isebb__adzw = types.Array(isebb__adzw.dtype, 1, 'C')
    assert isebb__adzw.ndim == 1
    arr = make_array(isebb__adzw)(context, builder, qti__ydgpw)
    phau__rozvu = builder.extract_value(arr.shape, 0)
    kwh__dbn = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        phau__rozvu, args[1], builder.load(rkt__dmyos)]
    kjb__evi = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    cgt__kwft = lir.FunctionType(lir.DoubleType(), kjb__evi)
    qus__syudu = cgutils.get_or_insert_function(builder.module, cgt__kwft,
        name='quantile_sequential')
    rqp__fkf = builder.call(qus__syudu, kwh__dbn)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return rqp__fkf


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    xjnb__ygc = numba_to_c_type(sig.args[0].dtype)
    rkt__dmyos = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), xjnb__ygc))
    qti__ydgpw = args[0]
    isebb__adzw = sig.args[0]
    if isinstance(isebb__adzw, (IntegerArrayType, BooleanArrayType)):
        qti__ydgpw = cgutils.create_struct_proxy(isebb__adzw)(context,
            builder, qti__ydgpw).data
        isebb__adzw = types.Array(isebb__adzw.dtype, 1, 'C')
    assert isebb__adzw.ndim == 1
    arr = make_array(isebb__adzw)(context, builder, qti__ydgpw)
    phau__rozvu = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        ngde__gtzq = args[2]
    else:
        ngde__gtzq = phau__rozvu
    kwh__dbn = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        phau__rozvu, ngde__gtzq, args[1], builder.load(rkt__dmyos)]
    kjb__evi = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType(
        64), lir.DoubleType(), lir.IntType(32)]
    cgt__kwft = lir.FunctionType(lir.DoubleType(), kjb__evi)
    qus__syudu = cgutils.get_or_insert_function(builder.module, cgt__kwft,
        name='quantile_parallel')
    rqp__fkf = builder.call(qus__syudu, kwh__dbn)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return rqp__fkf


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    loytn__lhit = start
    tyhgq__yrzsw = 2 * start + 1
    zemmu__qwqog = 2 * start + 2
    if tyhgq__yrzsw < n and not cmp_f(arr[tyhgq__yrzsw], arr[loytn__lhit]):
        loytn__lhit = tyhgq__yrzsw
    if zemmu__qwqog < n and not cmp_f(arr[zemmu__qwqog], arr[loytn__lhit]):
        loytn__lhit = zemmu__qwqog
    if loytn__lhit != start:
        arr[start], arr[loytn__lhit] = arr[loytn__lhit], arr[start]
        ind_arr[start], ind_arr[loytn__lhit] = ind_arr[loytn__lhit], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, loytn__lhit, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        jcjj__njt = np.empty(k, A.dtype)
        dmoqi__zrs = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                jcjj__njt[ind] = A[i]
                dmoqi__zrs[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            jcjj__njt = jcjj__njt[:ind]
            dmoqi__zrs = dmoqi__zrs[:ind]
        return jcjj__njt, dmoqi__zrs, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        auotr__xrz = np.sort(A)
        nqmd__swu = index_arr[np.argsort(A)]
        wem__cwts = pd.Series(auotr__xrz).notna().values
        auotr__xrz = auotr__xrz[wem__cwts]
        nqmd__swu = nqmd__swu[wem__cwts]
        if is_largest:
            auotr__xrz = auotr__xrz[::-1]
            nqmd__swu = nqmd__swu[::-1]
        return np.ascontiguousarray(auotr__xrz), np.ascontiguousarray(nqmd__swu
            )
    jcjj__njt, dmoqi__zrs, start = select_k_nonan(A, index_arr, m, k)
    dmoqi__zrs = dmoqi__zrs[jcjj__njt.argsort()]
    jcjj__njt.sort()
    if not is_largest:
        jcjj__njt = np.ascontiguousarray(jcjj__njt[::-1])
        dmoqi__zrs = np.ascontiguousarray(dmoqi__zrs[::-1])
    for i in range(start, m):
        if cmp_f(A[i], jcjj__njt[0]):
            jcjj__njt[0] = A[i]
            dmoqi__zrs[0] = index_arr[i]
            min_heapify(jcjj__njt, dmoqi__zrs, k, 0, cmp_f)
    dmoqi__zrs = dmoqi__zrs[jcjj__njt.argsort()]
    jcjj__njt.sort()
    if is_largest:
        jcjj__njt = jcjj__njt[::-1]
        dmoqi__zrs = dmoqi__zrs[::-1]
    return np.ascontiguousarray(jcjj__njt), np.ascontiguousarray(dmoqi__zrs)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    etvv__zvllm = bodo.libs.distributed_api.get_rank()
    mpn__ynzvm, ayggc__yyr = nlargest(A, I, k, is_largest, cmp_f)
    ivzw__lei = bodo.libs.distributed_api.gatherv(mpn__ynzvm)
    kqpzr__myj = bodo.libs.distributed_api.gatherv(ayggc__yyr)
    if etvv__zvllm == MPI_ROOT:
        res, gnhva__vctg = nlargest(ivzw__lei, kqpzr__myj, k, is_largest, cmp_f
            )
    else:
        res = np.empty(k, A.dtype)
        gnhva__vctg = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(gnhva__vctg)
    return res, gnhva__vctg


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    xav__vuo, zrvro__xmn = mat.shape
    loq__shq = np.empty((zrvro__xmn, zrvro__xmn), dtype=np.float64)
    for djesb__mkzx in range(zrvro__xmn):
        for uhtl__dbul in range(djesb__mkzx + 1):
            dxnmq__ncv = 0
            iyrw__qgllm = cyg__bkjn = uyoqk__nnydb = thfo__lflo = 0.0
            for i in range(xav__vuo):
                if np.isfinite(mat[i, djesb__mkzx]) and np.isfinite(mat[i,
                    uhtl__dbul]):
                    vrlkr__qwns = mat[i, djesb__mkzx]
                    iyt__gggs = mat[i, uhtl__dbul]
                    dxnmq__ncv += 1
                    uyoqk__nnydb += vrlkr__qwns
                    thfo__lflo += iyt__gggs
            if parallel:
                dxnmq__ncv = bodo.libs.distributed_api.dist_reduce(dxnmq__ncv,
                    sum_op)
                uyoqk__nnydb = bodo.libs.distributed_api.dist_reduce(
                    uyoqk__nnydb, sum_op)
                thfo__lflo = bodo.libs.distributed_api.dist_reduce(thfo__lflo,
                    sum_op)
            if dxnmq__ncv < minpv:
                loq__shq[djesb__mkzx, uhtl__dbul] = loq__shq[uhtl__dbul,
                    djesb__mkzx] = np.nan
            else:
                chc__srhum = uyoqk__nnydb / dxnmq__ncv
                rdlzb__sdxmb = thfo__lflo / dxnmq__ncv
                uyoqk__nnydb = 0.0
                for i in range(xav__vuo):
                    if np.isfinite(mat[i, djesb__mkzx]) and np.isfinite(mat
                        [i, uhtl__dbul]):
                        vrlkr__qwns = mat[i, djesb__mkzx] - chc__srhum
                        iyt__gggs = mat[i, uhtl__dbul] - rdlzb__sdxmb
                        uyoqk__nnydb += vrlkr__qwns * iyt__gggs
                        iyrw__qgllm += vrlkr__qwns * vrlkr__qwns
                        cyg__bkjn += iyt__gggs * iyt__gggs
                if parallel:
                    uyoqk__nnydb = bodo.libs.distributed_api.dist_reduce(
                        uyoqk__nnydb, sum_op)
                    iyrw__qgllm = bodo.libs.distributed_api.dist_reduce(
                        iyrw__qgllm, sum_op)
                    cyg__bkjn = bodo.libs.distributed_api.dist_reduce(cyg__bkjn
                        , sum_op)
                hto__gph = dxnmq__ncv - 1.0 if cov else sqrt(iyrw__qgllm *
                    cyg__bkjn)
                if hto__gph != 0.0:
                    loq__shq[djesb__mkzx, uhtl__dbul] = loq__shq[uhtl__dbul,
                        djesb__mkzx] = uyoqk__nnydb / hto__gph
                else:
                    loq__shq[djesb__mkzx, uhtl__dbul] = loq__shq[uhtl__dbul,
                        djesb__mkzx] = np.nan
    return loq__shq


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    uzjr__nklmv = n != 1
    lgm__apxaw = 'def impl(data, parallel=False):\n'
    lgm__apxaw += '  if parallel:\n'
    xzwf__bhc = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    lgm__apxaw += f'    cpp_table = arr_info_list_to_table([{xzwf__bhc}])\n'
    lgm__apxaw += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    xqfo__azb = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    lgm__apxaw += f'    data = ({xqfo__azb},)\n'
    lgm__apxaw += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    lgm__apxaw += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    lgm__apxaw += '    bodo.libs.array.delete_table(cpp_table)\n'
    lgm__apxaw += '  n = len(data[0])\n'
    lgm__apxaw += '  out = np.empty(n, np.bool_)\n'
    lgm__apxaw += '  uniqs = dict()\n'
    if uzjr__nklmv:
        lgm__apxaw += '  for i in range(n):\n'
        gqzo__goa = ', '.join(f'data[{i}][i]' for i in range(n))
        lchrw__xuecp = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        lgm__apxaw += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({gqzo__goa},), ({lchrw__xuecp},))
"""
        lgm__apxaw += '    if val in uniqs:\n'
        lgm__apxaw += '      out[i] = True\n'
        lgm__apxaw += '    else:\n'
        lgm__apxaw += '      out[i] = False\n'
        lgm__apxaw += '      uniqs[val] = 0\n'
    else:
        lgm__apxaw += '  data = data[0]\n'
        lgm__apxaw += '  hasna = False\n'
        lgm__apxaw += '  for i in range(n):\n'
        lgm__apxaw += '    if bodo.libs.array_kernels.isna(data, i):\n'
        lgm__apxaw += '      out[i] = hasna\n'
        lgm__apxaw += '      hasna = True\n'
        lgm__apxaw += '    else:\n'
        lgm__apxaw += '      val = data[i]\n'
        lgm__apxaw += '      if val in uniqs:\n'
        lgm__apxaw += '        out[i] = True\n'
        lgm__apxaw += '      else:\n'
        lgm__apxaw += '        out[i] = False\n'
        lgm__apxaw += '        uniqs[val] = 0\n'
    lgm__apxaw += '  if parallel:\n'
    lgm__apxaw += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    lgm__apxaw += '  return out\n'
    uvss__fjs = {}
    exec(lgm__apxaw, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        uvss__fjs)
    impl = uvss__fjs['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    pgwd__sdq = len(data)
    lgm__apxaw = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    lgm__apxaw += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        pgwd__sdq)))
    lgm__apxaw += '  table_total = arr_info_list_to_table(info_list_total)\n'
    lgm__apxaw += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(pgwd__sdq))
    for ywwc__sgtuo in range(pgwd__sdq):
        lgm__apxaw += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(ywwc__sgtuo, ywwc__sgtuo, ywwc__sgtuo))
    lgm__apxaw += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(pgwd__sdq))
    lgm__apxaw += '  delete_table(out_table)\n'
    lgm__apxaw += '  delete_table(table_total)\n'
    lgm__apxaw += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(pgwd__sdq)))
    uvss__fjs = {}
    exec(lgm__apxaw, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, uvss__fjs)
    impl = uvss__fjs['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    pgwd__sdq = len(data)
    lgm__apxaw = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    lgm__apxaw += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        pgwd__sdq)))
    lgm__apxaw += '  table_total = arr_info_list_to_table(info_list_total)\n'
    lgm__apxaw += '  keep_i = 0\n'
    lgm__apxaw += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for ywwc__sgtuo in range(pgwd__sdq):
        lgm__apxaw += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(ywwc__sgtuo, ywwc__sgtuo, ywwc__sgtuo))
    lgm__apxaw += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(pgwd__sdq))
    lgm__apxaw += '  delete_table(out_table)\n'
    lgm__apxaw += '  delete_table(table_total)\n'
    lgm__apxaw += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(pgwd__sdq)))
    uvss__fjs = {}
    exec(lgm__apxaw, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, uvss__fjs)
    impl = uvss__fjs['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        oltj__siv = [array_to_info(data_arr)]
        ptctg__dzj = arr_info_list_to_table(oltj__siv)
        kpk__bxmzw = 0
        zlj__xge = drop_duplicates_table(ptctg__dzj, parallel, 1,
            kpk__bxmzw, False, True)
        pbsz__tvvd = info_to_array(info_from_table(zlj__xge, 0), data_arr)
        delete_table(zlj__xge)
        delete_table(ptctg__dzj)
        return pbsz__tvvd
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    uzcv__xue = len(data.types)
    japg__yoy = [('out' + str(i)) for i in range(uzcv__xue)]
    vqddm__vfhob = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    ncc__moag = ['isna(data[{}], i)'.format(i) for i in vqddm__vfhob]
    axtau__sspm = 'not ({})'.format(' or '.join(ncc__moag))
    if not is_overload_none(thresh):
        axtau__sspm = '(({}) <= ({}) - thresh)'.format(' + '.join(ncc__moag
            ), uzcv__xue - 1)
    elif how == 'all':
        axtau__sspm = 'not ({})'.format(' and '.join(ncc__moag))
    lgm__apxaw = 'def _dropna_imp(data, how, thresh, subset):\n'
    lgm__apxaw += '  old_len = len(data[0])\n'
    lgm__apxaw += '  new_len = 0\n'
    lgm__apxaw += '  for i in range(old_len):\n'
    lgm__apxaw += '    if {}:\n'.format(axtau__sspm)
    lgm__apxaw += '      new_len += 1\n'
    for i, out in enumerate(japg__yoy):
        if isinstance(data[i], bodo.CategoricalArrayType):
            lgm__apxaw += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            lgm__apxaw += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    lgm__apxaw += '  curr_ind = 0\n'
    lgm__apxaw += '  for i in range(old_len):\n'
    lgm__apxaw += '    if {}:\n'.format(axtau__sspm)
    for i in range(uzcv__xue):
        lgm__apxaw += '      if isna(data[{}], i):\n'.format(i)
        lgm__apxaw += '        setna({}, curr_ind)\n'.format(japg__yoy[i])
        lgm__apxaw += '      else:\n'
        lgm__apxaw += '        {}[curr_ind] = data[{}][i]\n'.format(japg__yoy
            [i], i)
    lgm__apxaw += '      curr_ind += 1\n'
    lgm__apxaw += '  return {}\n'.format(', '.join(japg__yoy))
    uvss__fjs = {}
    jve__anibm = {'t{}'.format(i): nxa__kvui for i, nxa__kvui in enumerate(
        data.types)}
    jve__anibm.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(lgm__apxaw, jve__anibm, uvss__fjs)
    aku__seh = uvss__fjs['_dropna_imp']
    return aku__seh


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        isebb__adzw = arr.dtype
        gurpu__wamq = isebb__adzw.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            ufwr__gbupk = init_nested_counts(gurpu__wamq)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                ufwr__gbupk = add_nested_counts(ufwr__gbupk, val[ind])
            pbsz__tvvd = bodo.utils.utils.alloc_type(n, isebb__adzw,
                ufwr__gbupk)
            for ggks__qje in range(n):
                if bodo.libs.array_kernels.isna(arr, ggks__qje):
                    setna(pbsz__tvvd, ggks__qje)
                    continue
                val = arr[ggks__qje]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(pbsz__tvvd, ggks__qje)
                    continue
                pbsz__tvvd[ggks__qje] = val[ind]
            return pbsz__tvvd
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    vyoh__cgdjb = _to_readonly(arr_types.types[0])
    return all(isinstance(nxa__kvui, CategoricalArrayType) and _to_readonly
        (nxa__kvui) == vyoh__cgdjb for nxa__kvui in arr_types.types)


def concat(arr_list):
    return pd.concat(arr_list)


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arr_list.
        dtype, 'bodo.concat()')
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        gmov__amzk = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            spw__yln = 0
            iyoo__tms = []
            for A in arr_list:
                bapbx__tpinu = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                iyoo__tms.append(bodo.libs.array_item_arr_ext.get_data(A))
                spw__yln += bapbx__tpinu
            vsqo__aoba = np.empty(spw__yln + 1, offset_type)
            fttuf__vkg = bodo.libs.array_kernels.concat(iyoo__tms)
            wjhf__ujfck = np.empty(spw__yln + 7 >> 3, np.uint8)
            wxabz__bbod = 0
            qswd__dftr = 0
            for A in arr_list:
                iga__tsgns = bodo.libs.array_item_arr_ext.get_offsets(A)
                exolt__sps = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                bapbx__tpinu = len(A)
                aoyj__mmbob = iga__tsgns[bapbx__tpinu]
                for i in range(bapbx__tpinu):
                    vsqo__aoba[i + wxabz__bbod] = iga__tsgns[i] + qswd__dftr
                    nriqx__eaxd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        exolt__sps, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(wjhf__ujfck, i +
                        wxabz__bbod, nriqx__eaxd)
                wxabz__bbod += bapbx__tpinu
                qswd__dftr += aoyj__mmbob
            vsqo__aoba[wxabz__bbod] = qswd__dftr
            pbsz__tvvd = bodo.libs.array_item_arr_ext.init_array_item_array(
                spw__yln, fttuf__vkg, vsqo__aoba, wjhf__ujfck)
            return pbsz__tvvd
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        npl__obq = arr_list.dtype.names
        lgm__apxaw = 'def struct_array_concat_impl(arr_list):\n'
        lgm__apxaw += f'    n_all = 0\n'
        for i in range(len(npl__obq)):
            lgm__apxaw += f'    concat_list{i} = []\n'
        lgm__apxaw += '    for A in arr_list:\n'
        lgm__apxaw += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(npl__obq)):
            lgm__apxaw += f'        concat_list{i}.append(data_tuple[{i}])\n'
        lgm__apxaw += '        n_all += len(A)\n'
        lgm__apxaw += '    n_bytes = (n_all + 7) >> 3\n'
        lgm__apxaw += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        lgm__apxaw += '    curr_bit = 0\n'
        lgm__apxaw += '    for A in arr_list:\n'
        lgm__apxaw += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        lgm__apxaw += '        for j in range(len(A)):\n'
        lgm__apxaw += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        lgm__apxaw += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        lgm__apxaw += '            curr_bit += 1\n'
        lgm__apxaw += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        snhwx__lbxft = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(npl__obq))])
        lgm__apxaw += f'        ({snhwx__lbxft},),\n'
        lgm__apxaw += '        new_mask,\n'
        lgm__apxaw += f'        {npl__obq},\n'
        lgm__apxaw += '    )\n'
        uvss__fjs = {}
        exec(lgm__apxaw, {'bodo': bodo, 'np': np}, uvss__fjs)
        return uvss__fjs['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            gnmiv__hir = 0
            for A in arr_list:
                gnmiv__hir += len(A)
            wvo__jtdf = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(gnmiv__hir))
            czrk__hsjf = 0
            for A in arr_list:
                for i in range(len(A)):
                    wvo__jtdf._data[i + czrk__hsjf] = A._data[i]
                    nriqx__eaxd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(wvo__jtdf.
                        _null_bitmap, i + czrk__hsjf, nriqx__eaxd)
                czrk__hsjf += len(A)
            return wvo__jtdf
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            gnmiv__hir = 0
            for A in arr_list:
                gnmiv__hir += len(A)
            wvo__jtdf = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(gnmiv__hir))
            czrk__hsjf = 0
            for A in arr_list:
                for i in range(len(A)):
                    wvo__jtdf._days_data[i + czrk__hsjf] = A._days_data[i]
                    wvo__jtdf._seconds_data[i + czrk__hsjf] = A._seconds_data[i
                        ]
                    wvo__jtdf._microseconds_data[i + czrk__hsjf
                        ] = A._microseconds_data[i]
                    nriqx__eaxd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(wvo__jtdf.
                        _null_bitmap, i + czrk__hsjf, nriqx__eaxd)
                czrk__hsjf += len(A)
            return wvo__jtdf
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        yuhdq__uqsj = arr_list.dtype.precision
        rxf__ivzc = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            gnmiv__hir = 0
            for A in arr_list:
                gnmiv__hir += len(A)
            wvo__jtdf = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                gnmiv__hir, yuhdq__uqsj, rxf__ivzc)
            czrk__hsjf = 0
            for A in arr_list:
                for i in range(len(A)):
                    wvo__jtdf._data[i + czrk__hsjf] = A._data[i]
                    nriqx__eaxd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(wvo__jtdf.
                        _null_bitmap, i + czrk__hsjf, nriqx__eaxd)
                czrk__hsjf += len(A)
            return wvo__jtdf
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        nxa__kvui) for nxa__kvui in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            xmj__raar = arr_list.types[0]
        else:
            xmj__raar = arr_list.dtype
        xmj__raar = to_str_arr_if_dict_array(xmj__raar)

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            lkhq__eqgg = 0
            ned__laml = 0
            for A in arr_list:
                arr = A
                lkhq__eqgg += len(arr)
                ned__laml += bodo.libs.str_arr_ext.num_total_chars(arr)
            pbsz__tvvd = bodo.utils.utils.alloc_type(lkhq__eqgg, xmj__raar,
                (ned__laml,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(pbsz__tvvd, -1)
            wqy__aerw = 0
            fyhbq__hshyx = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(pbsz__tvvd,
                    arr, wqy__aerw, fyhbq__hshyx)
                wqy__aerw += len(arr)
                fyhbq__hshyx += bodo.libs.str_arr_ext.num_total_chars(arr)
            return pbsz__tvvd
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(nxa__kvui.dtype, types.Integer) for
        nxa__kvui in arr_list.types) and any(isinstance(nxa__kvui,
        IntegerArrayType) for nxa__kvui in arr_list.types):

        def impl_int_arr_list(arr_list):
            cqsh__rduzz = convert_to_nullable_tup(arr_list)
            dtgpo__fwa = []
            brcu__ila = 0
            for A in cqsh__rduzz:
                dtgpo__fwa.append(A._data)
                brcu__ila += len(A)
            fttuf__vkg = bodo.libs.array_kernels.concat(dtgpo__fwa)
            iebr__fwal = brcu__ila + 7 >> 3
            jln__jdlp = np.empty(iebr__fwal, np.uint8)
            dao__fpb = 0
            for A in cqsh__rduzz:
                wft__vliz = A._null_bitmap
                for ggks__qje in range(len(A)):
                    nriqx__eaxd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        wft__vliz, ggks__qje)
                    bodo.libs.int_arr_ext.set_bit_to_arr(jln__jdlp,
                        dao__fpb, nriqx__eaxd)
                    dao__fpb += 1
            return bodo.libs.int_arr_ext.init_integer_array(fttuf__vkg,
                jln__jdlp)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(nxa__kvui.dtype == types.bool_ for nxa__kvui in
        arr_list.types) and any(nxa__kvui == boolean_array for nxa__kvui in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            cqsh__rduzz = convert_to_nullable_tup(arr_list)
            dtgpo__fwa = []
            brcu__ila = 0
            for A in cqsh__rduzz:
                dtgpo__fwa.append(A._data)
                brcu__ila += len(A)
            fttuf__vkg = bodo.libs.array_kernels.concat(dtgpo__fwa)
            iebr__fwal = brcu__ila + 7 >> 3
            jln__jdlp = np.empty(iebr__fwal, np.uint8)
            dao__fpb = 0
            for A in cqsh__rduzz:
                wft__vliz = A._null_bitmap
                for ggks__qje in range(len(A)):
                    nriqx__eaxd = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        wft__vliz, ggks__qje)
                    bodo.libs.int_arr_ext.set_bit_to_arr(jln__jdlp,
                        dao__fpb, nriqx__eaxd)
                    dao__fpb += 1
            return bodo.libs.bool_arr_ext.init_bool_array(fttuf__vkg, jln__jdlp
                )
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            nrqdb__jfsed = []
            for A in arr_list:
                nrqdb__jfsed.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                nrqdb__jfsed), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        bpvu__ewbrm = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        lgm__apxaw = 'def impl(arr_list):\n'
        lgm__apxaw += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({bpvu__ewbrm},)), arr_list[0].dtype)
"""
        ugdgm__jmc = {}
        exec(lgm__apxaw, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, ugdgm__jmc)
        return ugdgm__jmc['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            brcu__ila = 0
            for A in arr_list:
                brcu__ila += len(A)
            pbsz__tvvd = np.empty(brcu__ila, dtype)
            kur__nuunh = 0
            for A in arr_list:
                n = len(A)
                pbsz__tvvd[kur__nuunh:kur__nuunh + n] = A
                kur__nuunh += n
            return pbsz__tvvd
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(nxa__kvui,
        (types.Array, IntegerArrayType)) and isinstance(nxa__kvui.dtype,
        types.Integer) for nxa__kvui in arr_list.types) and any(isinstance(
        nxa__kvui, types.Array) and isinstance(nxa__kvui.dtype, types.Float
        ) for nxa__kvui in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            pwzq__cgjj = []
            for A in arr_list:
                pwzq__cgjj.append(A._data)
            kykc__mofma = bodo.libs.array_kernels.concat(pwzq__cgjj)
            loq__shq = bodo.libs.map_arr_ext.init_map_arr(kykc__mofma)
            return loq__shq
        return impl_map_arr_list
    for fmqv__gmfj in arr_list:
        if not isinstance(fmqv__gmfj, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(nxa__kvui.astype(np.float64) for nxa__kvui in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    pgwd__sdq = len(arr_tup.types)
    lgm__apxaw = 'def f(arr_tup):\n'
    lgm__apxaw += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(pgwd__sdq
        )), ',' if pgwd__sdq == 1 else '')
    uvss__fjs = {}
    exec(lgm__apxaw, {'np': np}, uvss__fjs)
    lgzdm__qgygz = uvss__fjs['f']
    return lgzdm__qgygz


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    pgwd__sdq = len(arr_tup.types)
    tmo__gxj = find_common_np_dtype(arr_tup.types)
    gurpu__wamq = None
    kov__xxvx = ''
    if isinstance(tmo__gxj, types.Integer):
        gurpu__wamq = bodo.libs.int_arr_ext.IntDtype(tmo__gxj)
        kov__xxvx = '.astype(out_dtype, False)'
    lgm__apxaw = 'def f(arr_tup):\n'
    lgm__apxaw += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, kov__xxvx) for i in range(pgwd__sdq)), ',' if pgwd__sdq ==
        1 else '')
    uvss__fjs = {}
    exec(lgm__apxaw, {'bodo': bodo, 'out_dtype': gurpu__wamq}, uvss__fjs)
    dzdhn__zfc = uvss__fjs['f']
    return dzdhn__zfc


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, ozmvv__zwkr = build_set_seen_na(A)
        return len(s) + int(not dropna and ozmvv__zwkr)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        oiat__nxe = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        ygnh__ktp = len(oiat__nxe)
        return bodo.libs.distributed_api.dist_reduce(ygnh__ktp, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([vkez__yzm for vkez__yzm in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        cptu__yetz = np.finfo(A.dtype(1).dtype).max
    else:
        cptu__yetz = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        pbsz__tvvd = np.empty(n, A.dtype)
        ljsxg__pvpur = cptu__yetz
        for i in range(n):
            ljsxg__pvpur = min(ljsxg__pvpur, A[i])
            pbsz__tvvd[i] = ljsxg__pvpur
        return pbsz__tvvd
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        cptu__yetz = np.finfo(A.dtype(1).dtype).min
    else:
        cptu__yetz = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        pbsz__tvvd = np.empty(n, A.dtype)
        ljsxg__pvpur = cptu__yetz
        for i in range(n):
            ljsxg__pvpur = max(ljsxg__pvpur, A[i])
            pbsz__tvvd[i] = ljsxg__pvpur
        return pbsz__tvvd
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        vqg__wyr = arr_info_list_to_table([array_to_info(A)])
        ojdkd__hmlea = 1
        kpk__bxmzw = 0
        zlj__xge = drop_duplicates_table(vqg__wyr, parallel, ojdkd__hmlea,
            kpk__bxmzw, dropna, True)
        pbsz__tvvd = info_to_array(info_from_table(zlj__xge, 0), A)
        delete_table(vqg__wyr)
        delete_table(zlj__xge)
        return pbsz__tvvd
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    gmov__amzk = bodo.utils.typing.to_nullable_type(arr.dtype)
    tzzon__kbdf = index_arr
    tnvs__hbzla = tzzon__kbdf.dtype

    def impl(arr, index_arr):
        n = len(arr)
        ufwr__gbupk = init_nested_counts(gmov__amzk)
        lpzuu__irmg = init_nested_counts(tnvs__hbzla)
        for i in range(n):
            fowp__ljb = index_arr[i]
            if isna(arr, i):
                ufwr__gbupk = (ufwr__gbupk[0] + 1,) + ufwr__gbupk[1:]
                lpzuu__irmg = add_nested_counts(lpzuu__irmg, fowp__ljb)
                continue
            zfzco__poq = arr[i]
            if len(zfzco__poq) == 0:
                ufwr__gbupk = (ufwr__gbupk[0] + 1,) + ufwr__gbupk[1:]
                lpzuu__irmg = add_nested_counts(lpzuu__irmg, fowp__ljb)
                continue
            ufwr__gbupk = add_nested_counts(ufwr__gbupk, zfzco__poq)
            for clvpa__zmw in range(len(zfzco__poq)):
                lpzuu__irmg = add_nested_counts(lpzuu__irmg, fowp__ljb)
        pbsz__tvvd = bodo.utils.utils.alloc_type(ufwr__gbupk[0], gmov__amzk,
            ufwr__gbupk[1:])
        cmc__nokfg = bodo.utils.utils.alloc_type(ufwr__gbupk[0],
            tzzon__kbdf, lpzuu__irmg)
        qswd__dftr = 0
        for i in range(n):
            if isna(arr, i):
                setna(pbsz__tvvd, qswd__dftr)
                cmc__nokfg[qswd__dftr] = index_arr[i]
                qswd__dftr += 1
                continue
            zfzco__poq = arr[i]
            aoyj__mmbob = len(zfzco__poq)
            if aoyj__mmbob == 0:
                setna(pbsz__tvvd, qswd__dftr)
                cmc__nokfg[qswd__dftr] = index_arr[i]
                qswd__dftr += 1
                continue
            pbsz__tvvd[qswd__dftr:qswd__dftr + aoyj__mmbob] = zfzco__poq
            cmc__nokfg[qswd__dftr:qswd__dftr + aoyj__mmbob] = index_arr[i]
            qswd__dftr += aoyj__mmbob
        return pbsz__tvvd, cmc__nokfg
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    gmov__amzk = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        ufwr__gbupk = init_nested_counts(gmov__amzk)
        for i in range(n):
            if isna(arr, i):
                ufwr__gbupk = (ufwr__gbupk[0] + 1,) + ufwr__gbupk[1:]
                ooeo__qfqte = 1
            else:
                zfzco__poq = arr[i]
                nxro__yujgs = len(zfzco__poq)
                if nxro__yujgs == 0:
                    ufwr__gbupk = (ufwr__gbupk[0] + 1,) + ufwr__gbupk[1:]
                    ooeo__qfqte = 1
                    continue
                else:
                    ufwr__gbupk = add_nested_counts(ufwr__gbupk, zfzco__poq)
                    ooeo__qfqte = nxro__yujgs
            if counts[i] != ooeo__qfqte:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        pbsz__tvvd = bodo.utils.utils.alloc_type(ufwr__gbupk[0], gmov__amzk,
            ufwr__gbupk[1:])
        qswd__dftr = 0
        for i in range(n):
            if isna(arr, i):
                setna(pbsz__tvvd, qswd__dftr)
                qswd__dftr += 1
                continue
            zfzco__poq = arr[i]
            aoyj__mmbob = len(zfzco__poq)
            if aoyj__mmbob == 0:
                setna(pbsz__tvvd, qswd__dftr)
                qswd__dftr += 1
                continue
            pbsz__tvvd[qswd__dftr:qswd__dftr + aoyj__mmbob] = zfzco__poq
            qswd__dftr += aoyj__mmbob
        return pbsz__tvvd
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(cohug__uzx) for cohug__uzx in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        urkn__sfwf = 'np.empty(n, np.int64)'
        hsf__izxxz = 'out_arr[i] = 1'
        ujm__mqf = 'max(len(arr[i]), 1)'
    else:
        urkn__sfwf = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        hsf__izxxz = 'bodo.libs.array_kernels.setna(out_arr, i)'
        ujm__mqf = 'len(arr[i])'
    lgm__apxaw = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {urkn__sfwf}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {hsf__izxxz}
        else:
            out_arr[i] = {ujm__mqf}
    return out_arr
    """
    uvss__fjs = {}
    exec(lgm__apxaw, {'bodo': bodo, 'numba': numba, 'np': np}, uvss__fjs)
    impl = uvss__fjs['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    tzzon__kbdf = index_arr
    tnvs__hbzla = tzzon__kbdf.dtype

    def impl(arr, pat, n, index_arr):
        hocii__pmi = pat is not None and len(pat) > 1
        if hocii__pmi:
            oslu__gyj = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        cjfwy__tcrlx = len(arr)
        lkhq__eqgg = 0
        ned__laml = 0
        lpzuu__irmg = init_nested_counts(tnvs__hbzla)
        for i in range(cjfwy__tcrlx):
            fowp__ljb = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                lkhq__eqgg += 1
                lpzuu__irmg = add_nested_counts(lpzuu__irmg, fowp__ljb)
                continue
            if hocii__pmi:
                hlfam__pafb = oslu__gyj.split(arr[i], maxsplit=n)
            else:
                hlfam__pafb = arr[i].split(pat, n)
            lkhq__eqgg += len(hlfam__pafb)
            for s in hlfam__pafb:
                lpzuu__irmg = add_nested_counts(lpzuu__irmg, fowp__ljb)
                ned__laml += bodo.libs.str_arr_ext.get_utf8_size(s)
        pbsz__tvvd = bodo.libs.str_arr_ext.pre_alloc_string_array(lkhq__eqgg,
            ned__laml)
        cmc__nokfg = bodo.utils.utils.alloc_type(lkhq__eqgg, tzzon__kbdf,
            lpzuu__irmg)
        qogev__fehaj = 0
        for ggks__qje in range(cjfwy__tcrlx):
            if isna(arr, ggks__qje):
                pbsz__tvvd[qogev__fehaj] = ''
                bodo.libs.array_kernels.setna(pbsz__tvvd, qogev__fehaj)
                cmc__nokfg[qogev__fehaj] = index_arr[ggks__qje]
                qogev__fehaj += 1
                continue
            if hocii__pmi:
                hlfam__pafb = oslu__gyj.split(arr[ggks__qje], maxsplit=n)
            else:
                hlfam__pafb = arr[ggks__qje].split(pat, n)
            tecbt__yglsc = len(hlfam__pafb)
            pbsz__tvvd[qogev__fehaj:qogev__fehaj + tecbt__yglsc] = hlfam__pafb
            cmc__nokfg[qogev__fehaj:qogev__fehaj + tecbt__yglsc] = index_arr[
                ggks__qje]
            qogev__fehaj += tecbt__yglsc
        return pbsz__tvvd, cmc__nokfg
    return impl


def gen_na_array(n, arr):
    return np.full(n, np.nan)


@overload(gen_na_array, no_unliteral=True)
def overload_gen_na_array(n, arr):
    if isinstance(arr, types.TypeRef):
        arr = arr.instance_type
    dtype = arr.dtype
    if isinstance(dtype, (types.Integer, types.Float)):
        dtype = dtype if isinstance(dtype, types.Float) else types.float64

        def impl_float(n, arr):
            numba.parfors.parfor.init_prange()
            pbsz__tvvd = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                pbsz__tvvd[i] = np.nan
            return pbsz__tvvd
        return impl_float
    ytzq__llcvd = to_str_arr_if_dict_array(arr)

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        pbsz__tvvd = bodo.utils.utils.alloc_type(n, ytzq__llcvd, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(pbsz__tvvd, i)
        return pbsz__tvvd
    return impl


def gen_na_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_gen_na_array = (
    gen_na_array_equiv)


def resize_and_copy(A, new_len):
    return A


@overload(resize_and_copy, no_unliteral=True)
def overload_resize_and_copy(A, old_size, new_len):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.resize_and_copy()')
    can__rid = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            pbsz__tvvd = bodo.utils.utils.alloc_type(new_len, can__rid)
            bodo.libs.str_arr_ext.str_copy_ptr(pbsz__tvvd.ctypes, 0, A.
                ctypes, old_size)
            return pbsz__tvvd
        return impl_char

    def impl(A, old_size, new_len):
        pbsz__tvvd = bodo.utils.utils.alloc_type(new_len, can__rid, (-1,))
        pbsz__tvvd[:old_size] = A[:old_size]
        return pbsz__tvvd
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    kio__lpz = math.ceil((stop - start) / step)
    return int(max(kio__lpz, 0))


def calc_nitems_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    if guard(find_const, self.func_ir, args[0]) == 0 and guard(find_const,
        self.func_ir, args[2]) == 1:
        return ArrayAnalysis.AnalyzeResult(shape=args[1], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_calc_nitems = (
    calc_nitems_equiv)


def arange_parallel_impl(return_type, *args):
    dtype = as_dtype(return_type.dtype)

    def arange_1(stop):
        return np.arange(0, stop, 1, dtype)

    def arange_2(start, stop):
        return np.arange(start, stop, 1, dtype)

    def arange_3(start, stop, step):
        return np.arange(start, stop, step, dtype)
    if any(isinstance(vkez__yzm, types.Complex) for vkez__yzm in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            jucm__zbe = (stop - start) / step
            kio__lpz = math.ceil(jucm__zbe.real)
            yhyu__qve = math.ceil(jucm__zbe.imag)
            lzucq__fdgq = int(max(min(yhyu__qve, kio__lpz), 0))
            arr = np.empty(lzucq__fdgq, dtype)
            for i in numba.parfors.parfor.internal_prange(lzucq__fdgq):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            lzucq__fdgq = bodo.libs.array_kernels.calc_nitems(start, stop, step
                )
            arr = np.empty(lzucq__fdgq, dtype)
            for i in numba.parfors.parfor.internal_prange(lzucq__fdgq):
                arr[i] = start + i * step
            return arr
    if len(args) == 1:
        return arange_1
    elif len(args) == 2:
        return arange_2
    elif len(args) == 3:
        return arange_3
    elif len(args) == 4:
        return arange_4
    else:
        raise BodoError('parallel arange with types {}'.format(args))


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.arange_parallel_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c72b0390b4f3e52dcc5426bd42c6b55ff96bae5a425381900985d36e7527a4bd':
        warnings.warn('numba.parfors.parfor.arange_parallel_impl has changed')
numba.parfors.parfor.swap_functions_map['arange', 'numpy'
    ] = arange_parallel_impl


def sort(arr, ascending, inplace):
    return np.sort(arr)


@overload(sort, no_unliteral=True)
def overload_sort(arr, ascending, inplace):

    def impl(arr, ascending, inplace):
        n = len(arr)
        data = np.arange(n),
        wktjc__isn = arr,
        if not inplace:
            wktjc__isn = arr.copy(),
        ajt__gab = bodo.libs.str_arr_ext.to_list_if_immutable_arr(wktjc__isn)
        inf__chv = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(ajt__gab, 0, n, inf__chv)
        if not ascending:
            bodo.libs.timsort.reverseRange(ajt__gab, 0, n, inf__chv)
        bodo.libs.str_arr_ext.cp_str_list_to_array(wktjc__isn, ajt__gab)
        return wktjc__isn[0]
    return impl


def overload_array_max(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).max()
        return impl


overload(np.max, inline='always', no_unliteral=True)(overload_array_max)
overload(max, inline='always', no_unliteral=True)(overload_array_max)


def overload_array_min(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).min()
        return impl


overload(np.min, inline='always', no_unliteral=True)(overload_array_min)
overload(min, inline='always', no_unliteral=True)(overload_array_min)


def overload_array_sum(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).sum()
    return impl


overload(np.sum, inline='always', no_unliteral=True)(overload_array_sum)
overload(sum, inline='always', no_unliteral=True)(overload_array_sum)


@overload(np.prod, inline='always', no_unliteral=True)
def overload_array_prod(A):
    if isinstance(A, IntegerArrayType) or A == boolean_array:

        def impl(A):
            return pd.Series(A).prod()
    return impl


def nonzero(arr):
    return arr,


@overload(nonzero, no_unliteral=True)
def nonzero_overload(A, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.nonzero()')
    if not bodo.utils.utils.is_array_typ(A, False):
        return

    def impl(A, parallel=False):
        n = len(A)
        if parallel:
            offset = bodo.libs.distributed_api.dist_exscan(n, Reduce_Type.
                Sum.value)
        else:
            offset = 0
        loq__shq = []
        for i in range(n):
            if A[i]:
                loq__shq.append(i + offset)
        return np.array(loq__shq, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    can__rid = element_type(A)
    if can__rid == types.unicode_type:
        null_value = '""'
    elif can__rid == types.bool_:
        null_value = 'False'
    elif can__rid == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif can__rid == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    qogev__fehaj = 'i'
    bfdt__ldep = False
    vmb__kufy = get_overload_const_str(method)
    if vmb__kufy in ('ffill', 'pad'):
        jeg__ppjmp = 'n'
        send_right = True
    elif vmb__kufy in ('backfill', 'bfill'):
        jeg__ppjmp = 'n-1, -1, -1'
        send_right = False
        if can__rid == types.unicode_type:
            qogev__fehaj = '(n - 1) - i'
            bfdt__ldep = True
    lgm__apxaw = 'def impl(A, method, parallel=False):\n'
    lgm__apxaw += '  A = decode_if_dict_array(A)\n'
    lgm__apxaw += '  has_last_value = False\n'
    lgm__apxaw += f'  last_value = {null_value}\n'
    lgm__apxaw += '  if parallel:\n'
    lgm__apxaw += '    rank = bodo.libs.distributed_api.get_rank()\n'
    lgm__apxaw += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    lgm__apxaw += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    lgm__apxaw += '  n = len(A)\n'
    lgm__apxaw += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    lgm__apxaw += f'  for i in range({jeg__ppjmp}):\n'
    lgm__apxaw += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    lgm__apxaw += (
        f'      bodo.libs.array_kernels.setna(out_arr, {qogev__fehaj})\n')
    lgm__apxaw += '      continue\n'
    lgm__apxaw += '    s = A[i]\n'
    lgm__apxaw += '    if bodo.libs.array_kernels.isna(A, i):\n'
    lgm__apxaw += '      s = last_value\n'
    lgm__apxaw += f'    out_arr[{qogev__fehaj}] = s\n'
    lgm__apxaw += '    last_value = s\n'
    lgm__apxaw += '    has_last_value = True\n'
    if bfdt__ldep:
        lgm__apxaw += '  return out_arr[::-1]\n'
    else:
        lgm__apxaw += '  return out_arr\n'
    vbru__kegn = {}
    exec(lgm__apxaw, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, vbru__kegn)
    impl = vbru__kegn['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        dsb__ikxh = 0
        dirg__pnjal = n_pes - 1
        bhl__dgk = np.int32(rank + 1)
        xcag__nbbl = np.int32(rank - 1)
        tyz__cer = len(in_arr) - 1
        vhgn__yak = -1
        fmgz__ppei = -1
    else:
        dsb__ikxh = n_pes - 1
        dirg__pnjal = 0
        bhl__dgk = np.int32(rank - 1)
        xcag__nbbl = np.int32(rank + 1)
        tyz__cer = 0
        vhgn__yak = len(in_arr)
        fmgz__ppei = 1
    jugyo__xoae = np.int32(bodo.hiframes.rolling.comm_border_tag)
    uvu__ucpjg = np.empty(1, dtype=np.bool_)
    ppbj__iql = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    iti__bri = np.empty(1, dtype=np.bool_)
    ihjd__jqj = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    gqzoe__omfx = False
    pxhr__jri = null_value
    for i in range(tyz__cer, vhgn__yak, fmgz__ppei):
        if not isna(in_arr, i):
            gqzoe__omfx = True
            pxhr__jri = in_arr[i]
            break
    if rank != dsb__ikxh:
        yxf__cyrqc = bodo.libs.distributed_api.irecv(uvu__ucpjg, 1,
            xcag__nbbl, jugyo__xoae, True)
        bodo.libs.distributed_api.wait(yxf__cyrqc, True)
        rsggf__puqcv = bodo.libs.distributed_api.irecv(ppbj__iql, 1,
            xcag__nbbl, jugyo__xoae, True)
        bodo.libs.distributed_api.wait(rsggf__puqcv, True)
        ezw__rge = uvu__ucpjg[0]
        hvx__zxld = ppbj__iql[0]
    else:
        ezw__rge = False
        hvx__zxld = null_value
    if gqzoe__omfx:
        iti__bri[0] = gqzoe__omfx
        ihjd__jqj[0] = pxhr__jri
    else:
        iti__bri[0] = ezw__rge
        ihjd__jqj[0] = hvx__zxld
    if rank != dirg__pnjal:
        gls__cvr = bodo.libs.distributed_api.isend(iti__bri, 1, bhl__dgk,
            jugyo__xoae, True)
        ccg__zzd = bodo.libs.distributed_api.isend(ihjd__jqj, 1, bhl__dgk,
            jugyo__xoae, True)
    return ezw__rge, hvx__zxld


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    drqdd__hdxx = {'axis': axis, 'kind': kind, 'order': order}
    vyrh__fyfd = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', drqdd__hdxx, vyrh__fyfd, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    can__rid = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            A = decode_if_dict_array(A)
            cjfwy__tcrlx = len(A)
            pbsz__tvvd = bodo.utils.utils.alloc_type(cjfwy__tcrlx * repeats,
                can__rid, (-1,))
            for i in range(cjfwy__tcrlx):
                qogev__fehaj = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for ggks__qje in range(repeats):
                        bodo.libs.array_kernels.setna(pbsz__tvvd, 
                            qogev__fehaj + ggks__qje)
                else:
                    pbsz__tvvd[qogev__fehaj:qogev__fehaj + repeats] = A[i]
            return pbsz__tvvd
        return impl_int

    def impl_arr(A, repeats):
        A = decode_if_dict_array(A)
        cjfwy__tcrlx = len(A)
        pbsz__tvvd = bodo.utils.utils.alloc_type(repeats.sum(), can__rid, (-1,)
            )
        qogev__fehaj = 0
        for i in range(cjfwy__tcrlx):
            wamgj__bcy = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for ggks__qje in range(wamgj__bcy):
                    bodo.libs.array_kernels.setna(pbsz__tvvd, qogev__fehaj +
                        ggks__qje)
            else:
                pbsz__tvvd[qogev__fehaj:qogev__fehaj + wamgj__bcy] = A[i]
            qogev__fehaj += wamgj__bcy
        return pbsz__tvvd
    return impl_arr


@overload(np.repeat, inline='always', no_unliteral=True)
def np_repeat(A, repeats):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    if not isinstance(repeats, types.Integer):
        raise BodoError(
            'Only integer type supported for repeats in np.repeat()')

    def impl(A, repeats):
        return bodo.libs.array_kernels.repeat_kernel(A, repeats)
    return impl


@numba.generated_jit
def repeat_like(A, dist_like_arr):
    if not bodo.utils.utils.is_array_typ(A, False
        ) or not bodo.utils.utils.is_array_typ(dist_like_arr, False):
        raise BodoError('Both A and dist_like_arr must be array-like.')

    def impl(A, dist_like_arr):
        return bodo.libs.array_kernels.repeat_kernel(A, len(dist_like_arr))
    return impl


@overload(np.unique, inline='always', no_unliteral=True)
def np_unique(A):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return

    def impl(A):
        cbcdo__qvwzn = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(cbcdo__qvwzn, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        xtev__rcew = bodo.libs.array_kernels.concat([A1, A2])
        hul__rlw = bodo.libs.array_kernels.unique(xtev__rcew)
        return pd.Series(hul__rlw).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    drqdd__hdxx = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    vyrh__fyfd = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', drqdd__hdxx, vyrh__fyfd, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        pvogh__rjhfb = bodo.libs.array_kernels.unique(A1)
        djlt__bbe = bodo.libs.array_kernels.unique(A2)
        xtev__rcew = bodo.libs.array_kernels.concat([pvogh__rjhfb, djlt__bbe])
        kjms__zzz = pd.Series(xtev__rcew).sort_values().values
        return slice_array_intersect1d(kjms__zzz)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    wem__cwts = arr[1:] == arr[:-1]
    return arr[:-1][wem__cwts]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    drqdd__hdxx = {'assume_unique': assume_unique}
    vyrh__fyfd = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', drqdd__hdxx, vyrh__fyfd, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        pvogh__rjhfb = bodo.libs.array_kernels.unique(A1)
        djlt__bbe = bodo.libs.array_kernels.unique(A2)
        wem__cwts = calculate_mask_setdiff1d(pvogh__rjhfb, djlt__bbe)
        return pd.Series(pvogh__rjhfb[wem__cwts]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    wem__cwts = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        wem__cwts &= A1 != A2[i]
    return wem__cwts


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    drqdd__hdxx = {'retstep': retstep, 'axis': axis}
    vyrh__fyfd = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', drqdd__hdxx, vyrh__fyfd, 'numpy')
    xfm__sws = False
    if is_overload_none(dtype):
        can__rid = np.promote_types(np.promote_types(numba.np.numpy_support
            .as_dtype(start), numba.np.numpy_support.as_dtype(stop)), numba
            .np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            xfm__sws = True
        can__rid = numba.np.numpy_support.as_dtype(dtype).type
    if xfm__sws:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            wscb__hwvtw = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            pbsz__tvvd = np.empty(num, can__rid)
            for i in numba.parfors.parfor.internal_prange(num):
                pbsz__tvvd[i] = can__rid(np.floor(start + i * wscb__hwvtw))
            return pbsz__tvvd
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            wscb__hwvtw = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            pbsz__tvvd = np.empty(num, can__rid)
            for i in numba.parfors.parfor.internal_prange(num):
                pbsz__tvvd[i] = can__rid(start + i * wscb__hwvtw)
            return pbsz__tvvd
        return impl


def np_linspace_get_stepsize(start, stop, num, endpoint):
    return 0


@overload(np_linspace_get_stepsize, no_unliteral=True)
def overload_np_linspace_get_stepsize(start, stop, num, endpoint):

    def impl(start, stop, num, endpoint):
        if num < 0:
            raise ValueError('np.linspace() Num must be >= 0')
        if endpoint:
            num -= 1
        if num > 1:
            return (stop - start) / num
        return 0
    return impl


@overload(operator.contains, no_unliteral=True)
def arr_contains(A, val):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'np.contains()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.dtype == types.
        unliteral(val)):
        return

    def impl(A, val):
        numba.parfors.parfor.init_prange()
        pgwd__sdq = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                pgwd__sdq += A[i] == val
        return pgwd__sdq > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    drqdd__hdxx = {'axis': axis, 'out': out, 'keepdims': keepdims}
    vyrh__fyfd = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', drqdd__hdxx, vyrh__fyfd, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        pgwd__sdq = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                pgwd__sdq += int(bool(A[i]))
        return pgwd__sdq > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    drqdd__hdxx = {'axis': axis, 'out': out, 'keepdims': keepdims}
    vyrh__fyfd = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', drqdd__hdxx, vyrh__fyfd, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        pgwd__sdq = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                pgwd__sdq += int(bool(A[i]))
        return pgwd__sdq == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    drqdd__hdxx = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    vyrh__fyfd = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', drqdd__hdxx, vyrh__fyfd, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        dtsjn__hxge = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            pbsz__tvvd = np.empty(n, dtsjn__hxge)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(pbsz__tvvd, i)
                    continue
                pbsz__tvvd[i] = np_cbrt_scalar(A[i], dtsjn__hxge)
            return pbsz__tvvd
        return impl_arr
    dtsjn__hxge = np.promote_types(numba.np.numpy_support.as_dtype(A),
        numba.np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, dtsjn__hxge)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    orny__fwt = x < 0
    if orny__fwt:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if orny__fwt:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    xbx__rqu = isinstance(tup, (types.BaseTuple, types.List))
    mba__dsjqo = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for fmqv__gmfj in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                fmqv__gmfj, 'numpy.hstack()')
            xbx__rqu = xbx__rqu and bodo.utils.utils.is_array_typ(fmqv__gmfj,
                False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        xbx__rqu = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif mba__dsjqo:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        cwuc__uxuy = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for fmqv__gmfj in cwuc__uxuy.types:
            mba__dsjqo = mba__dsjqo and bodo.utils.utils.is_array_typ(
                fmqv__gmfj, False)
    if not (xbx__rqu or mba__dsjqo):
        return
    if mba__dsjqo:

        def impl_series(tup):
            arr_tup = bodo.hiframes.pd_series_ext.get_series_data(tup)
            return bodo.libs.array_kernels.concat(arr_tup)
        return impl_series

    def impl(tup):
        return bodo.libs.array_kernels.concat(tup)
    return impl


@overload(np.random.multivariate_normal, inline='always', no_unliteral=True)
def np_random_multivariate_normal(mean, cov, size=None, check_valid='warn',
    tol=1e-08):
    drqdd__hdxx = {'check_valid': check_valid, 'tol': tol}
    vyrh__fyfd = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', drqdd__hdxx,
        vyrh__fyfd, 'numpy')
    if not isinstance(size, types.Integer):
        raise BodoError(
            'np.random.multivariate_normal() size argument is required and must be an integer'
            )
    if not (bodo.utils.utils.is_array_typ(mean, False) and mean.ndim == 1):
        raise BodoError(
            'np.random.multivariate_normal() mean must be a 1 dimensional numpy array'
            )
    if not (bodo.utils.utils.is_array_typ(cov, False) and cov.ndim == 2):
        raise BodoError(
            'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
            )

    def impl(mean, cov, size=None, check_valid='warn', tol=1e-08):
        _validate_multivar_norm(cov)
        xav__vuo = mean.shape[0]
        ony__cnb = size, xav__vuo
        ijief__kmpw = np.random.standard_normal(ony__cnb)
        cov = cov.astype(np.float64)
        ndmo__vlll, s, rrvwk__bekh = np.linalg.svd(cov)
        res = np.dot(ijief__kmpw, np.sqrt(s).reshape(xav__vuo, 1) * rrvwk__bekh
            )
        qof__xuice = res + mean
        return qof__xuice
    return impl


def _validate_multivar_norm(cov):
    return


@overload(_validate_multivar_norm, no_unliteral=True)
def _overload_validate_multivar_norm(cov):

    def impl(cov):
        if cov.shape[0] != cov.shape[1]:
            raise ValueError(
                'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
                )
    return impl


def _nan_argmin(arr):
    return


@overload(_nan_argmin, no_unliteral=True)
def _overload_nan_argmin(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            numba.parfors.parfor.init_prange()
            cuha__rjcae = bodo.hiframes.series_kernels._get_type_max_value(arr)
            jpk__begp = typing.builtins.IndexValue(-1, cuha__rjcae)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                ocxgl__wkkm = typing.builtins.IndexValue(i, arr[i])
                jpk__begp = min(jpk__begp, ocxgl__wkkm)
            return jpk__begp.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        kznu__acz = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            blui__oilzh = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            cuha__rjcae = kznu__acz(len(arr.dtype.categories) + 1)
            jpk__begp = typing.builtins.IndexValue(-1, cuha__rjcae)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                ocxgl__wkkm = typing.builtins.IndexValue(i, blui__oilzh[i])
                jpk__begp = min(jpk__begp, ocxgl__wkkm)
            return jpk__begp.index
        return impl_cat_arr
    return lambda arr: arr.argmin()


def _nan_argmax(arr):
    return


@overload(_nan_argmax, no_unliteral=True)
def _overload_nan_argmax(arr):
    if isinstance(arr, IntegerArrayType) or arr in [boolean_array,
        datetime_date_array_type] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            n = len(arr)
            numba.parfors.parfor.init_prange()
            cuha__rjcae = bodo.hiframes.series_kernels._get_type_min_value(arr)
            jpk__begp = typing.builtins.IndexValue(-1, cuha__rjcae)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                ocxgl__wkkm = typing.builtins.IndexValue(i, arr[i])
                jpk__begp = max(jpk__begp, ocxgl__wkkm)
            return jpk__begp.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        kznu__acz = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            blui__oilzh = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            cuha__rjcae = kznu__acz(-1)
            jpk__begp = typing.builtins.IndexValue(-1, cuha__rjcae)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                ocxgl__wkkm = typing.builtins.IndexValue(i, blui__oilzh[i])
                jpk__begp = max(jpk__begp, ocxgl__wkkm)
            return jpk__begp.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
