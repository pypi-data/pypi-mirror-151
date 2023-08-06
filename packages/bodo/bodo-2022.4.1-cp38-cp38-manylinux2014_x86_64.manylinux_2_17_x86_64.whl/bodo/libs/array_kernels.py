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
        wof__sug = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = wof__sug
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        wof__sug = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = wof__sug
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
            brjtt__bzbj = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            brjtt__bzbj[ind + 1] = brjtt__bzbj[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            brjtt__bzbj = bodo.libs.array_item_arr_ext.get_offsets(arr)
            brjtt__bzbj[ind + 1] = brjtt__bzbj[ind]
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
    aozu__rde = arr_tup.count
    bibxl__rzv = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(aozu__rde):
        bibxl__rzv += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    bibxl__rzv += '  return\n'
    goycq__cwe = {}
    exec(bibxl__rzv, {'setna': setna}, goycq__cwe)
    impl = goycq__cwe['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        gmh__yhwr = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(gmh__yhwr.start, gmh__yhwr.stop, gmh__yhwr.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        cwd__smjwn = 'n'
        qdh__xsiex = 'n_pes'
        qkd__ihgcd = 'min_op'
    else:
        cwd__smjwn = 'n-1, -1, -1'
        qdh__xsiex = '-1'
        qkd__ihgcd = 'max_op'
    bibxl__rzv = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {qdh__xsiex}
    for i in range({cwd__smjwn}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {qkd__ihgcd}))
        if possible_valid_rank != {qdh__xsiex}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    goycq__cwe = {}
    exec(bibxl__rzv, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op':
        max_op, 'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.
        box_if_dt64}, goycq__cwe)
    impl = goycq__cwe['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    sgmqr__fva = array_to_info(arr)
    _median_series_computation(res, sgmqr__fva, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(sgmqr__fva)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    sgmqr__fva = array_to_info(arr)
    _autocorr_series_computation(res, sgmqr__fva, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(sgmqr__fva)


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
    sgmqr__fva = array_to_info(arr)
    _compute_series_monotonicity(res, sgmqr__fva, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(sgmqr__fva)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    wvzbl__fyu = res[0] > 0.5
    return wvzbl__fyu


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        rsfxn__ozcu = '-'
        jfp__yor = 'index_arr[0] > threshhold_date'
        cwd__smjwn = '1, n+1'
        amhs__nct = 'index_arr[-i] <= threshhold_date'
        rro__amuzg = 'i - 1'
    else:
        rsfxn__ozcu = '+'
        jfp__yor = 'index_arr[-1] < threshhold_date'
        cwd__smjwn = 'n'
        amhs__nct = 'index_arr[i] >= threshhold_date'
        rro__amuzg = 'i'
    bibxl__rzv = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        bibxl__rzv += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_type):\n')
        bibxl__rzv += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            bibxl__rzv += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            bibxl__rzv += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            bibxl__rzv += '    else:\n'
            bibxl__rzv += (
                '      threshhold_date = initial_date + date_offset\n')
        else:
            bibxl__rzv += (
                f'    threshhold_date = initial_date {rsfxn__ozcu} date_offset\n'
                )
    else:
        bibxl__rzv += (
            f'  threshhold_date = initial_date {rsfxn__ozcu} offset\n')
    bibxl__rzv += '  local_valid = 0\n'
    bibxl__rzv += f'  n = len(index_arr)\n'
    bibxl__rzv += f'  if n:\n'
    bibxl__rzv += f'    if {jfp__yor}:\n'
    bibxl__rzv += '      loc_valid = n\n'
    bibxl__rzv += '    else:\n'
    bibxl__rzv += f'      for i in range({cwd__smjwn}):\n'
    bibxl__rzv += f'        if {amhs__nct}:\n'
    bibxl__rzv += f'          loc_valid = {rro__amuzg}\n'
    bibxl__rzv += '          break\n'
    bibxl__rzv += '  if is_parallel:\n'
    bibxl__rzv += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    bibxl__rzv += '    return total_valid\n'
    bibxl__rzv += '  else:\n'
    bibxl__rzv += '    return loc_valid\n'
    goycq__cwe = {}
    exec(bibxl__rzv, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, goycq__cwe)
    return goycq__cwe['impl']


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
    rjnw__niqp = numba_to_c_type(sig.args[0].dtype)
    lnhxk__pgwo = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), rjnw__niqp))
    lfhj__qpi = args[0]
    ntg__rji = sig.args[0]
    if isinstance(ntg__rji, (IntegerArrayType, BooleanArrayType)):
        lfhj__qpi = cgutils.create_struct_proxy(ntg__rji)(context, builder,
            lfhj__qpi).data
        ntg__rji = types.Array(ntg__rji.dtype, 1, 'C')
    assert ntg__rji.ndim == 1
    arr = make_array(ntg__rji)(context, builder, lfhj__qpi)
    wep__ntsu = builder.extract_value(arr.shape, 0)
    yxr__eqv = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        wep__ntsu, args[1], builder.load(lnhxk__pgwo)]
    ryf__kjgl = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    dqu__zre = lir.FunctionType(lir.DoubleType(), ryf__kjgl)
    wwj__ofvi = cgutils.get_or_insert_function(builder.module, dqu__zre,
        name='quantile_sequential')
    gmztz__accf = builder.call(wwj__ofvi, yxr__eqv)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return gmztz__accf


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    rjnw__niqp = numba_to_c_type(sig.args[0].dtype)
    lnhxk__pgwo = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), rjnw__niqp))
    lfhj__qpi = args[0]
    ntg__rji = sig.args[0]
    if isinstance(ntg__rji, (IntegerArrayType, BooleanArrayType)):
        lfhj__qpi = cgutils.create_struct_proxy(ntg__rji)(context, builder,
            lfhj__qpi).data
        ntg__rji = types.Array(ntg__rji.dtype, 1, 'C')
    assert ntg__rji.ndim == 1
    arr = make_array(ntg__rji)(context, builder, lfhj__qpi)
    wep__ntsu = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        jhs__qsjo = args[2]
    else:
        jhs__qsjo = wep__ntsu
    yxr__eqv = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        wep__ntsu, jhs__qsjo, args[1], builder.load(lnhxk__pgwo)]
    ryf__kjgl = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.IntType(
        64), lir.DoubleType(), lir.IntType(32)]
    dqu__zre = lir.FunctionType(lir.DoubleType(), ryf__kjgl)
    wwj__ofvi = cgutils.get_or_insert_function(builder.module, dqu__zre,
        name='quantile_parallel')
    gmztz__accf = builder.call(wwj__ofvi, yxr__eqv)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return gmztz__accf


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    hglo__agp = start
    adqa__wvnvf = 2 * start + 1
    mcbvj__gzb = 2 * start + 2
    if adqa__wvnvf < n and not cmp_f(arr[adqa__wvnvf], arr[hglo__agp]):
        hglo__agp = adqa__wvnvf
    if mcbvj__gzb < n and not cmp_f(arr[mcbvj__gzb], arr[hglo__agp]):
        hglo__agp = mcbvj__gzb
    if hglo__agp != start:
        arr[start], arr[hglo__agp] = arr[hglo__agp], arr[start]
        ind_arr[start], ind_arr[hglo__agp] = ind_arr[hglo__agp], ind_arr[start]
        min_heapify(arr, ind_arr, n, hglo__agp, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        uko__zds = np.empty(k, A.dtype)
        vfsig__rxquy = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                uko__zds[ind] = A[i]
                vfsig__rxquy[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            uko__zds = uko__zds[:ind]
            vfsig__rxquy = vfsig__rxquy[:ind]
        return uko__zds, vfsig__rxquy, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        tfobv__eiu = np.sort(A)
        thohb__jjkiw = index_arr[np.argsort(A)]
        qxqev__mxsnd = pd.Series(tfobv__eiu).notna().values
        tfobv__eiu = tfobv__eiu[qxqev__mxsnd]
        thohb__jjkiw = thohb__jjkiw[qxqev__mxsnd]
        if is_largest:
            tfobv__eiu = tfobv__eiu[::-1]
            thohb__jjkiw = thohb__jjkiw[::-1]
        return np.ascontiguousarray(tfobv__eiu), np.ascontiguousarray(
            thohb__jjkiw)
    uko__zds, vfsig__rxquy, start = select_k_nonan(A, index_arr, m, k)
    vfsig__rxquy = vfsig__rxquy[uko__zds.argsort()]
    uko__zds.sort()
    if not is_largest:
        uko__zds = np.ascontiguousarray(uko__zds[::-1])
        vfsig__rxquy = np.ascontiguousarray(vfsig__rxquy[::-1])
    for i in range(start, m):
        if cmp_f(A[i], uko__zds[0]):
            uko__zds[0] = A[i]
            vfsig__rxquy[0] = index_arr[i]
            min_heapify(uko__zds, vfsig__rxquy, k, 0, cmp_f)
    vfsig__rxquy = vfsig__rxquy[uko__zds.argsort()]
    uko__zds.sort()
    if is_largest:
        uko__zds = uko__zds[::-1]
        vfsig__rxquy = vfsig__rxquy[::-1]
    return np.ascontiguousarray(uko__zds), np.ascontiguousarray(vfsig__rxquy)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    cgpzz__agz = bodo.libs.distributed_api.get_rank()
    mgeuf__uff, wds__wejk = nlargest(A, I, k, is_largest, cmp_f)
    gwces__tdl = bodo.libs.distributed_api.gatherv(mgeuf__uff)
    joz__fem = bodo.libs.distributed_api.gatherv(wds__wejk)
    if cgpzz__agz == MPI_ROOT:
        res, lua__liohp = nlargest(gwces__tdl, joz__fem, k, is_largest, cmp_f)
    else:
        res = np.empty(k, A.dtype)
        lua__liohp = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(lua__liohp)
    return res, lua__liohp


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    aju__mrmy, rtb__ezjn = mat.shape
    ovecz__grbh = np.empty((rtb__ezjn, rtb__ezjn), dtype=np.float64)
    for qhec__ojn in range(rtb__ezjn):
        for nnh__fjmm in range(qhec__ojn + 1):
            iwo__jnzjl = 0
            rypg__onf = xokqt__uihv = enoth__ibgzx = zpb__rst = 0.0
            for i in range(aju__mrmy):
                if np.isfinite(mat[i, qhec__ojn]) and np.isfinite(mat[i,
                    nnh__fjmm]):
                    gug__lbc = mat[i, qhec__ojn]
                    hjaxg__wbes = mat[i, nnh__fjmm]
                    iwo__jnzjl += 1
                    enoth__ibgzx += gug__lbc
                    zpb__rst += hjaxg__wbes
            if parallel:
                iwo__jnzjl = bodo.libs.distributed_api.dist_reduce(iwo__jnzjl,
                    sum_op)
                enoth__ibgzx = bodo.libs.distributed_api.dist_reduce(
                    enoth__ibgzx, sum_op)
                zpb__rst = bodo.libs.distributed_api.dist_reduce(zpb__rst,
                    sum_op)
            if iwo__jnzjl < minpv:
                ovecz__grbh[qhec__ojn, nnh__fjmm] = ovecz__grbh[nnh__fjmm,
                    qhec__ojn] = np.nan
            else:
                zbglp__erlbw = enoth__ibgzx / iwo__jnzjl
                nlca__izfgf = zpb__rst / iwo__jnzjl
                enoth__ibgzx = 0.0
                for i in range(aju__mrmy):
                    if np.isfinite(mat[i, qhec__ojn]) and np.isfinite(mat[i,
                        nnh__fjmm]):
                        gug__lbc = mat[i, qhec__ojn] - zbglp__erlbw
                        hjaxg__wbes = mat[i, nnh__fjmm] - nlca__izfgf
                        enoth__ibgzx += gug__lbc * hjaxg__wbes
                        rypg__onf += gug__lbc * gug__lbc
                        xokqt__uihv += hjaxg__wbes * hjaxg__wbes
                if parallel:
                    enoth__ibgzx = bodo.libs.distributed_api.dist_reduce(
                        enoth__ibgzx, sum_op)
                    rypg__onf = bodo.libs.distributed_api.dist_reduce(rypg__onf
                        , sum_op)
                    xokqt__uihv = bodo.libs.distributed_api.dist_reduce(
                        xokqt__uihv, sum_op)
                gcdeq__mpy = iwo__jnzjl - 1.0 if cov else sqrt(rypg__onf *
                    xokqt__uihv)
                if gcdeq__mpy != 0.0:
                    ovecz__grbh[qhec__ojn, nnh__fjmm] = ovecz__grbh[
                        nnh__fjmm, qhec__ojn] = enoth__ibgzx / gcdeq__mpy
                else:
                    ovecz__grbh[qhec__ojn, nnh__fjmm] = ovecz__grbh[
                        nnh__fjmm, qhec__ojn] = np.nan
    return ovecz__grbh


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    vze__arazw = n != 1
    bibxl__rzv = 'def impl(data, parallel=False):\n'
    bibxl__rzv += '  if parallel:\n'
    war__niem = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    bibxl__rzv += f'    cpp_table = arr_info_list_to_table([{war__niem}])\n'
    bibxl__rzv += f"""    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)
"""
    onuw__mazfr = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    bibxl__rzv += f'    data = ({onuw__mazfr},)\n'
    bibxl__rzv += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    bibxl__rzv += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    bibxl__rzv += '    bodo.libs.array.delete_table(cpp_table)\n'
    bibxl__rzv += '  n = len(data[0])\n'
    bibxl__rzv += '  out = np.empty(n, np.bool_)\n'
    bibxl__rzv += '  uniqs = dict()\n'
    if vze__arazw:
        bibxl__rzv += '  for i in range(n):\n'
        skko__kybos = ', '.join(f'data[{i}][i]' for i in range(n))
        jxjp__yacm = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        bibxl__rzv += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({skko__kybos},), ({jxjp__yacm},))
"""
        bibxl__rzv += '    if val in uniqs:\n'
        bibxl__rzv += '      out[i] = True\n'
        bibxl__rzv += '    else:\n'
        bibxl__rzv += '      out[i] = False\n'
        bibxl__rzv += '      uniqs[val] = 0\n'
    else:
        bibxl__rzv += '  data = data[0]\n'
        bibxl__rzv += '  hasna = False\n'
        bibxl__rzv += '  for i in range(n):\n'
        bibxl__rzv += '    if bodo.libs.array_kernels.isna(data, i):\n'
        bibxl__rzv += '      out[i] = hasna\n'
        bibxl__rzv += '      hasna = True\n'
        bibxl__rzv += '    else:\n'
        bibxl__rzv += '      val = data[i]\n'
        bibxl__rzv += '      if val in uniqs:\n'
        bibxl__rzv += '        out[i] = True\n'
        bibxl__rzv += '      else:\n'
        bibxl__rzv += '        out[i] = False\n'
        bibxl__rzv += '        uniqs[val] = 0\n'
    bibxl__rzv += '  if parallel:\n'
    bibxl__rzv += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    bibxl__rzv += '  return out\n'
    goycq__cwe = {}
    exec(bibxl__rzv, {'bodo': bodo, 'np': np, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'info_to_array': info_to_array, 'info_from_table': info_from_table},
        goycq__cwe)
    impl = goycq__cwe['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    return data, ind_arr


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    aozu__rde = len(data)
    bibxl__rzv = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    bibxl__rzv += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        aozu__rde)))
    bibxl__rzv += '  table_total = arr_info_list_to_table(info_list_total)\n'
    bibxl__rzv += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(aozu__rde))
    for pyg__akgz in range(aozu__rde):
        bibxl__rzv += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(pyg__akgz, pyg__akgz, pyg__akgz))
    bibxl__rzv += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(aozu__rde))
    bibxl__rzv += '  delete_table(out_table)\n'
    bibxl__rzv += '  delete_table(table_total)\n'
    bibxl__rzv += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(aozu__rde)))
    goycq__cwe = {}
    exec(bibxl__rzv, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'sample_table': sample_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, goycq__cwe)
    impl = goycq__cwe['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    return data, ind_arr


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    aozu__rde = len(data)
    bibxl__rzv = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    bibxl__rzv += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        aozu__rde)))
    bibxl__rzv += '  table_total = arr_info_list_to_table(info_list_total)\n'
    bibxl__rzv += '  keep_i = 0\n'
    bibxl__rzv += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for pyg__akgz in range(aozu__rde):
        bibxl__rzv += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(pyg__akgz, pyg__akgz, pyg__akgz))
    bibxl__rzv += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(aozu__rde))
    bibxl__rzv += '  delete_table(out_table)\n'
    bibxl__rzv += '  delete_table(table_total)\n'
    bibxl__rzv += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(aozu__rde)))
    goycq__cwe = {}
    exec(bibxl__rzv, {'np': np, 'bodo': bodo, 'array_to_info':
        array_to_info, 'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, goycq__cwe)
    impl = goycq__cwe['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    return data_arr


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        yct__zcznm = [array_to_info(data_arr)]
        kvbx__igwol = arr_info_list_to_table(yct__zcznm)
        xcis__cacg = 0
        ehbr__acd = drop_duplicates_table(kvbx__igwol, parallel, 1,
            xcis__cacg, False, True)
        doqje__fxa = info_to_array(info_from_table(ehbr__acd, 0), data_arr)
        delete_table(ehbr__acd)
        delete_table(kvbx__igwol)
        return doqje__fxa
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    return data


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    ctjl__wwe = len(data.types)
    bqet__xmy = [('out' + str(i)) for i in range(ctjl__wwe)]
    jtdv__nuom = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    flzb__cqi = ['isna(data[{}], i)'.format(i) for i in jtdv__nuom]
    bmf__dqfzh = 'not ({})'.format(' or '.join(flzb__cqi))
    if not is_overload_none(thresh):
        bmf__dqfzh = '(({}) <= ({}) - thresh)'.format(' + '.join(flzb__cqi),
            ctjl__wwe - 1)
    elif how == 'all':
        bmf__dqfzh = 'not ({})'.format(' and '.join(flzb__cqi))
    bibxl__rzv = 'def _dropna_imp(data, how, thresh, subset):\n'
    bibxl__rzv += '  old_len = len(data[0])\n'
    bibxl__rzv += '  new_len = 0\n'
    bibxl__rzv += '  for i in range(old_len):\n'
    bibxl__rzv += '    if {}:\n'.format(bmf__dqfzh)
    bibxl__rzv += '      new_len += 1\n'
    for i, out in enumerate(bqet__xmy):
        if isinstance(data[i], bodo.CategoricalArrayType):
            bibxl__rzv += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            bibxl__rzv += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    bibxl__rzv += '  curr_ind = 0\n'
    bibxl__rzv += '  for i in range(old_len):\n'
    bibxl__rzv += '    if {}:\n'.format(bmf__dqfzh)
    for i in range(ctjl__wwe):
        bibxl__rzv += '      if isna(data[{}], i):\n'.format(i)
        bibxl__rzv += '        setna({}, curr_ind)\n'.format(bqet__xmy[i])
        bibxl__rzv += '      else:\n'
        bibxl__rzv += '        {}[curr_ind] = data[{}][i]\n'.format(bqet__xmy
            [i], i)
    bibxl__rzv += '      curr_ind += 1\n'
    bibxl__rzv += '  return {}\n'.format(', '.join(bqet__xmy))
    goycq__cwe = {}
    nfsn__fgat = {'t{}'.format(i): kgrs__ild for i, kgrs__ild in enumerate(
        data.types)}
    nfsn__fgat.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(bibxl__rzv, nfsn__fgat, goycq__cwe)
    ibwh__fswj = goycq__cwe['_dropna_imp']
    return ibwh__fswj


def get(arr, ind):
    return pd.Series(arr).str.get(ind)


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        ntg__rji = arr.dtype
        xxv__bkn = ntg__rji.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            uzk__pqx = init_nested_counts(xxv__bkn)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                uzk__pqx = add_nested_counts(uzk__pqx, val[ind])
            doqje__fxa = bodo.utils.utils.alloc_type(n, ntg__rji, uzk__pqx)
            for acxyz__geg in range(n):
                if bodo.libs.array_kernels.isna(arr, acxyz__geg):
                    setna(doqje__fxa, acxyz__geg)
                    continue
                val = arr[acxyz__geg]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(doqje__fxa, acxyz__geg)
                    continue
                doqje__fxa[acxyz__geg] = val[ind]
            return doqje__fxa
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    hmn__wisjy = _to_readonly(arr_types.types[0])
    return all(isinstance(kgrs__ild, CategoricalArrayType) and _to_readonly
        (kgrs__ild) == hmn__wisjy for kgrs__ild in arr_types.types)


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
        euu__jfe = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            omwij__hbdv = 0
            emhx__cgmay = []
            for A in arr_list:
                egz__gqgzd = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                emhx__cgmay.append(bodo.libs.array_item_arr_ext.get_data(A))
                omwij__hbdv += egz__gqgzd
            ttbrl__uieka = np.empty(omwij__hbdv + 1, offset_type)
            gxlft__pqugu = bodo.libs.array_kernels.concat(emhx__cgmay)
            vkw__acera = np.empty(omwij__hbdv + 7 >> 3, np.uint8)
            ikb__hoj = 0
            lzde__idv = 0
            for A in arr_list:
                tskvw__uuciz = bodo.libs.array_item_arr_ext.get_offsets(A)
                srw__hadx = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                egz__gqgzd = len(A)
                zga__hljyj = tskvw__uuciz[egz__gqgzd]
                for i in range(egz__gqgzd):
                    ttbrl__uieka[i + ikb__hoj] = tskvw__uuciz[i] + lzde__idv
                    sjhd__ougr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        srw__hadx, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(vkw__acera, i +
                        ikb__hoj, sjhd__ougr)
                ikb__hoj += egz__gqgzd
                lzde__idv += zga__hljyj
            ttbrl__uieka[ikb__hoj] = lzde__idv
            doqje__fxa = bodo.libs.array_item_arr_ext.init_array_item_array(
                omwij__hbdv, gxlft__pqugu, ttbrl__uieka, vkw__acera)
            return doqje__fxa
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        losae__szgl = arr_list.dtype.names
        bibxl__rzv = 'def struct_array_concat_impl(arr_list):\n'
        bibxl__rzv += f'    n_all = 0\n'
        for i in range(len(losae__szgl)):
            bibxl__rzv += f'    concat_list{i} = []\n'
        bibxl__rzv += '    for A in arr_list:\n'
        bibxl__rzv += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(losae__szgl)):
            bibxl__rzv += f'        concat_list{i}.append(data_tuple[{i}])\n'
        bibxl__rzv += '        n_all += len(A)\n'
        bibxl__rzv += '    n_bytes = (n_all + 7) >> 3\n'
        bibxl__rzv += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        bibxl__rzv += '    curr_bit = 0\n'
        bibxl__rzv += '    for A in arr_list:\n'
        bibxl__rzv += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        bibxl__rzv += '        for j in range(len(A)):\n'
        bibxl__rzv += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        bibxl__rzv += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        bibxl__rzv += '            curr_bit += 1\n'
        bibxl__rzv += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        gjo__bwq = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(losae__szgl))])
        bibxl__rzv += f'        ({gjo__bwq},),\n'
        bibxl__rzv += '        new_mask,\n'
        bibxl__rzv += f'        {losae__szgl},\n'
        bibxl__rzv += '    )\n'
        goycq__cwe = {}
        exec(bibxl__rzv, {'bodo': bodo, 'np': np}, goycq__cwe)
        return goycq__cwe['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            haq__kuk = 0
            for A in arr_list:
                haq__kuk += len(A)
            tztt__gtn = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(haq__kuk))
            fpizw__bdgja = 0
            for A in arr_list:
                for i in range(len(A)):
                    tztt__gtn._data[i + fpizw__bdgja] = A._data[i]
                    sjhd__ougr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(tztt__gtn.
                        _null_bitmap, i + fpizw__bdgja, sjhd__ougr)
                fpizw__bdgja += len(A)
            return tztt__gtn
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            haq__kuk = 0
            for A in arr_list:
                haq__kuk += len(A)
            tztt__gtn = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(haq__kuk))
            fpizw__bdgja = 0
            for A in arr_list:
                for i in range(len(A)):
                    tztt__gtn._days_data[i + fpizw__bdgja] = A._days_data[i]
                    tztt__gtn._seconds_data[i + fpizw__bdgja
                        ] = A._seconds_data[i]
                    tztt__gtn._microseconds_data[i + fpizw__bdgja
                        ] = A._microseconds_data[i]
                    sjhd__ougr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(tztt__gtn.
                        _null_bitmap, i + fpizw__bdgja, sjhd__ougr)
                fpizw__bdgja += len(A)
            return tztt__gtn
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        wrsdl__rszf = arr_list.dtype.precision
        rfb__nfdru = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            haq__kuk = 0
            for A in arr_list:
                haq__kuk += len(A)
            tztt__gtn = bodo.libs.decimal_arr_ext.alloc_decimal_array(haq__kuk,
                wrsdl__rszf, rfb__nfdru)
            fpizw__bdgja = 0
            for A in arr_list:
                for i in range(len(A)):
                    tztt__gtn._data[i + fpizw__bdgja] = A._data[i]
                    sjhd__ougr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(tztt__gtn.
                        _null_bitmap, i + fpizw__bdgja, sjhd__ougr)
                fpizw__bdgja += len(A)
            return tztt__gtn
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        kgrs__ild) for kgrs__ild in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            hdq__piga = arr_list.types[0]
        else:
            hdq__piga = arr_list.dtype
        hdq__piga = to_str_arr_if_dict_array(hdq__piga)

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            khdxt__ezb = 0
            qeslf__foyqt = 0
            for A in arr_list:
                arr = A
                khdxt__ezb += len(arr)
                qeslf__foyqt += bodo.libs.str_arr_ext.num_total_chars(arr)
            doqje__fxa = bodo.utils.utils.alloc_type(khdxt__ezb, hdq__piga,
                (qeslf__foyqt,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(doqje__fxa, -1)
            qaf__ktxe = 0
            ncbtu__xvt = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(doqje__fxa,
                    arr, qaf__ktxe, ncbtu__xvt)
                qaf__ktxe += len(arr)
                ncbtu__xvt += bodo.libs.str_arr_ext.num_total_chars(arr)
            return doqje__fxa
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(kgrs__ild.dtype, types.Integer) for
        kgrs__ild in arr_list.types) and any(isinstance(kgrs__ild,
        IntegerArrayType) for kgrs__ild in arr_list.types):

        def impl_int_arr_list(arr_list):
            kzee__lrpy = convert_to_nullable_tup(arr_list)
            ozzq__lat = []
            gzzne__lhius = 0
            for A in kzee__lrpy:
                ozzq__lat.append(A._data)
                gzzne__lhius += len(A)
            gxlft__pqugu = bodo.libs.array_kernels.concat(ozzq__lat)
            zthi__vth = gzzne__lhius + 7 >> 3
            ezm__xyqs = np.empty(zthi__vth, np.uint8)
            vqb__jlpqj = 0
            for A in kzee__lrpy:
                opr__diaih = A._null_bitmap
                for acxyz__geg in range(len(A)):
                    sjhd__ougr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        opr__diaih, acxyz__geg)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ezm__xyqs,
                        vqb__jlpqj, sjhd__ougr)
                    vqb__jlpqj += 1
            return bodo.libs.int_arr_ext.init_integer_array(gxlft__pqugu,
                ezm__xyqs)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(kgrs__ild.dtype == types.bool_ for kgrs__ild in
        arr_list.types) and any(kgrs__ild == boolean_array for kgrs__ild in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            kzee__lrpy = convert_to_nullable_tup(arr_list)
            ozzq__lat = []
            gzzne__lhius = 0
            for A in kzee__lrpy:
                ozzq__lat.append(A._data)
                gzzne__lhius += len(A)
            gxlft__pqugu = bodo.libs.array_kernels.concat(ozzq__lat)
            zthi__vth = gzzne__lhius + 7 >> 3
            ezm__xyqs = np.empty(zthi__vth, np.uint8)
            vqb__jlpqj = 0
            for A in kzee__lrpy:
                opr__diaih = A._null_bitmap
                for acxyz__geg in range(len(A)):
                    sjhd__ougr = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        opr__diaih, acxyz__geg)
                    bodo.libs.int_arr_ext.set_bit_to_arr(ezm__xyqs,
                        vqb__jlpqj, sjhd__ougr)
                    vqb__jlpqj += 1
            return bodo.libs.bool_arr_ext.init_bool_array(gxlft__pqugu,
                ezm__xyqs)
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            ppe__fkoo = []
            for A in arr_list:
                ppe__fkoo.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                ppe__fkoo), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        lbtux__jhyzc = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        bibxl__rzv = 'def impl(arr_list):\n'
        bibxl__rzv += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({lbtux__jhyzc},)), arr_list[0].dtype)
"""
        yqdm__pra = {}
        exec(bibxl__rzv, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, yqdm__pra)
        return yqdm__pra['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            gzzne__lhius = 0
            for A in arr_list:
                gzzne__lhius += len(A)
            doqje__fxa = np.empty(gzzne__lhius, dtype)
            oxu__ysugy = 0
            for A in arr_list:
                n = len(A)
                doqje__fxa[oxu__ysugy:oxu__ysugy + n] = A
                oxu__ysugy += n
            return doqje__fxa
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(kgrs__ild,
        (types.Array, IntegerArrayType)) and isinstance(kgrs__ild.dtype,
        types.Integer) for kgrs__ild in arr_list.types) and any(isinstance(
        kgrs__ild, types.Array) and isinstance(kgrs__ild.dtype, types.Float
        ) for kgrs__ild in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            dms__fdt = []
            for A in arr_list:
                dms__fdt.append(A._data)
            gxh__njq = bodo.libs.array_kernels.concat(dms__fdt)
            ovecz__grbh = bodo.libs.map_arr_ext.init_map_arr(gxh__njq)
            return ovecz__grbh
        return impl_map_arr_list
    for xonh__hjlrt in arr_list:
        if not isinstance(xonh__hjlrt, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(kgrs__ild.astype(np.float64) for kgrs__ild in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    aozu__rde = len(arr_tup.types)
    bibxl__rzv = 'def f(arr_tup):\n'
    bibxl__rzv += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(aozu__rde
        )), ',' if aozu__rde == 1 else '')
    goycq__cwe = {}
    exec(bibxl__rzv, {'np': np}, goycq__cwe)
    nuvs__phfs = goycq__cwe['f']
    return nuvs__phfs


def convert_to_nullable_tup(arr_tup):
    return arr_tup


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple)
    aozu__rde = len(arr_tup.types)
    lbcg__ltcou = find_common_np_dtype(arr_tup.types)
    xxv__bkn = None
    unhu__ojfen = ''
    if isinstance(lbcg__ltcou, types.Integer):
        xxv__bkn = bodo.libs.int_arr_ext.IntDtype(lbcg__ltcou)
        unhu__ojfen = '.astype(out_dtype, False)'
    bibxl__rzv = 'def f(arr_tup):\n'
    bibxl__rzv += '  return ({}{})\n'.format(','.join(
        'bodo.utils.conversion.coerce_to_array(arr_tup[{}], use_nullable_array=True){}'
        .format(i, unhu__ojfen) for i in range(aozu__rde)), ',' if 
        aozu__rde == 1 else '')
    goycq__cwe = {}
    exec(bibxl__rzv, {'bodo': bodo, 'out_dtype': xxv__bkn}, goycq__cwe)
    mnc__agsp = goycq__cwe['f']
    return mnc__agsp


def nunique(A, dropna):
    return len(set(A))


def nunique_parallel(A, dropna):
    return len(set(A))


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, kvnwf__vfikg = build_set_seen_na(A)
        return len(s) + int(not dropna and kvnwf__vfikg)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        feeb__ryr = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        flpj__yscx = len(feeb__ryr)
        return bodo.libs.distributed_api.dist_reduce(flpj__yscx, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    return np.array([ynax__ubf for ynax__ubf in set(A)]).astype(A.dtype)


def cummin(A):
    return A


@overload(cummin, no_unliteral=True)
def cummin_overload(A):
    if isinstance(A.dtype, types.Float):
        vxi__ulyu = np.finfo(A.dtype(1).dtype).max
    else:
        vxi__ulyu = np.iinfo(A.dtype(1).dtype).max

    def impl(A):
        n = len(A)
        doqje__fxa = np.empty(n, A.dtype)
        gxok__pha = vxi__ulyu
        for i in range(n):
            gxok__pha = min(gxok__pha, A[i])
            doqje__fxa[i] = gxok__pha
        return doqje__fxa
    return impl


def cummax(A):
    return A


@overload(cummax, no_unliteral=True)
def cummax_overload(A):
    if isinstance(A.dtype, types.Float):
        vxi__ulyu = np.finfo(A.dtype(1).dtype).min
    else:
        vxi__ulyu = np.iinfo(A.dtype(1).dtype).min

    def impl(A):
        n = len(A)
        doqje__fxa = np.empty(n, A.dtype)
        gxok__pha = vxi__ulyu
        for i in range(n):
            gxok__pha = max(gxok__pha, A[i])
            doqje__fxa[i] = gxok__pha
        return doqje__fxa
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        ayz__zbr = arr_info_list_to_table([array_to_info(A)])
        ijtqg__xeur = 1
        xcis__cacg = 0
        ehbr__acd = drop_duplicates_table(ayz__zbr, parallel, ijtqg__xeur,
            xcis__cacg, dropna, True)
        doqje__fxa = info_to_array(info_from_table(ehbr__acd, 0), A)
        delete_table(ayz__zbr)
        delete_table(ehbr__acd)
        return doqje__fxa
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    euu__jfe = bodo.utils.typing.to_nullable_type(arr.dtype)
    ecdvx__kdqw = index_arr
    vyrq__csil = ecdvx__kdqw.dtype

    def impl(arr, index_arr):
        n = len(arr)
        uzk__pqx = init_nested_counts(euu__jfe)
        aoan__ywnmn = init_nested_counts(vyrq__csil)
        for i in range(n):
            yrv__nefb = index_arr[i]
            if isna(arr, i):
                uzk__pqx = (uzk__pqx[0] + 1,) + uzk__pqx[1:]
                aoan__ywnmn = add_nested_counts(aoan__ywnmn, yrv__nefb)
                continue
            tqvmb__fxir = arr[i]
            if len(tqvmb__fxir) == 0:
                uzk__pqx = (uzk__pqx[0] + 1,) + uzk__pqx[1:]
                aoan__ywnmn = add_nested_counts(aoan__ywnmn, yrv__nefb)
                continue
            uzk__pqx = add_nested_counts(uzk__pqx, tqvmb__fxir)
            for apr__dlbju in range(len(tqvmb__fxir)):
                aoan__ywnmn = add_nested_counts(aoan__ywnmn, yrv__nefb)
        doqje__fxa = bodo.utils.utils.alloc_type(uzk__pqx[0], euu__jfe,
            uzk__pqx[1:])
        dft__jdxlk = bodo.utils.utils.alloc_type(uzk__pqx[0], ecdvx__kdqw,
            aoan__ywnmn)
        lzde__idv = 0
        for i in range(n):
            if isna(arr, i):
                setna(doqje__fxa, lzde__idv)
                dft__jdxlk[lzde__idv] = index_arr[i]
                lzde__idv += 1
                continue
            tqvmb__fxir = arr[i]
            zga__hljyj = len(tqvmb__fxir)
            if zga__hljyj == 0:
                setna(doqje__fxa, lzde__idv)
                dft__jdxlk[lzde__idv] = index_arr[i]
                lzde__idv += 1
                continue
            doqje__fxa[lzde__idv:lzde__idv + zga__hljyj] = tqvmb__fxir
            dft__jdxlk[lzde__idv:lzde__idv + zga__hljyj] = index_arr[i]
            lzde__idv += zga__hljyj
        return doqje__fxa, dft__jdxlk
    return impl


def explode_no_index(arr):
    return pd.Series(arr).explode()


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    euu__jfe = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        uzk__pqx = init_nested_counts(euu__jfe)
        for i in range(n):
            if isna(arr, i):
                uzk__pqx = (uzk__pqx[0] + 1,) + uzk__pqx[1:]
                mkde__yhixs = 1
            else:
                tqvmb__fxir = arr[i]
                cercs__hjuuk = len(tqvmb__fxir)
                if cercs__hjuuk == 0:
                    uzk__pqx = (uzk__pqx[0] + 1,) + uzk__pqx[1:]
                    mkde__yhixs = 1
                    continue
                else:
                    uzk__pqx = add_nested_counts(uzk__pqx, tqvmb__fxir)
                    mkde__yhixs = cercs__hjuuk
            if counts[i] != mkde__yhixs:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        doqje__fxa = bodo.utils.utils.alloc_type(uzk__pqx[0], euu__jfe,
            uzk__pqx[1:])
        lzde__idv = 0
        for i in range(n):
            if isna(arr, i):
                setna(doqje__fxa, lzde__idv)
                lzde__idv += 1
                continue
            tqvmb__fxir = arr[i]
            zga__hljyj = len(tqvmb__fxir)
            if zga__hljyj == 0:
                setna(doqje__fxa, lzde__idv)
                lzde__idv += 1
                continue
            doqje__fxa[lzde__idv:lzde__idv + zga__hljyj] = tqvmb__fxir
            lzde__idv += zga__hljyj
        return doqje__fxa
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    return [len(pprbf__shvk) for pprbf__shvk in arr]


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        qzpf__vfkhd = 'np.empty(n, np.int64)'
        llgqq__zdgix = 'out_arr[i] = 1'
        jvla__zbm = 'max(len(arr[i]), 1)'
    else:
        qzpf__vfkhd = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        llgqq__zdgix = 'bodo.libs.array_kernels.setna(out_arr, i)'
        jvla__zbm = 'len(arr[i])'
    bibxl__rzv = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {qzpf__vfkhd}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {llgqq__zdgix}
        else:
            out_arr[i] = {jvla__zbm}
    return out_arr
    """
    goycq__cwe = {}
    exec(bibxl__rzv, {'bodo': bodo, 'numba': numba, 'np': np}, goycq__cwe)
    impl = goycq__cwe['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    return pd.Series(arr, index_arr).str.split(pat, n).explode()


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    ecdvx__kdqw = index_arr
    vyrq__csil = ecdvx__kdqw.dtype

    def impl(arr, pat, n, index_arr):
        uxb__qdg = pat is not None and len(pat) > 1
        if uxb__qdg:
            ufeo__zmta = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        kjn__soht = len(arr)
        khdxt__ezb = 0
        qeslf__foyqt = 0
        aoan__ywnmn = init_nested_counts(vyrq__csil)
        for i in range(kjn__soht):
            yrv__nefb = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                khdxt__ezb += 1
                aoan__ywnmn = add_nested_counts(aoan__ywnmn, yrv__nefb)
                continue
            if uxb__qdg:
                nwl__tqva = ufeo__zmta.split(arr[i], maxsplit=n)
            else:
                nwl__tqva = arr[i].split(pat, n)
            khdxt__ezb += len(nwl__tqva)
            for s in nwl__tqva:
                aoan__ywnmn = add_nested_counts(aoan__ywnmn, yrv__nefb)
                qeslf__foyqt += bodo.libs.str_arr_ext.get_utf8_size(s)
        doqje__fxa = bodo.libs.str_arr_ext.pre_alloc_string_array(khdxt__ezb,
            qeslf__foyqt)
        dft__jdxlk = bodo.utils.utils.alloc_type(khdxt__ezb, ecdvx__kdqw,
            aoan__ywnmn)
        xilbr__ysigg = 0
        for acxyz__geg in range(kjn__soht):
            if isna(arr, acxyz__geg):
                doqje__fxa[xilbr__ysigg] = ''
                bodo.libs.array_kernels.setna(doqje__fxa, xilbr__ysigg)
                dft__jdxlk[xilbr__ysigg] = index_arr[acxyz__geg]
                xilbr__ysigg += 1
                continue
            if uxb__qdg:
                nwl__tqva = ufeo__zmta.split(arr[acxyz__geg], maxsplit=n)
            else:
                nwl__tqva = arr[acxyz__geg].split(pat, n)
            wehc__efzq = len(nwl__tqva)
            doqje__fxa[xilbr__ysigg:xilbr__ysigg + wehc__efzq] = nwl__tqva
            dft__jdxlk[xilbr__ysigg:xilbr__ysigg + wehc__efzq] = index_arr[
                acxyz__geg]
            xilbr__ysigg += wehc__efzq
        return doqje__fxa, dft__jdxlk
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
            doqje__fxa = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                doqje__fxa[i] = np.nan
            return doqje__fxa
        return impl_float
    fei__jmzc = to_str_arr_if_dict_array(arr)

    def impl(n, arr):
        numba.parfors.parfor.init_prange()
        doqje__fxa = bodo.utils.utils.alloc_type(n, fei__jmzc, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(doqje__fxa, i)
        return doqje__fxa
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
    gtju__qsg = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            doqje__fxa = bodo.utils.utils.alloc_type(new_len, gtju__qsg)
            bodo.libs.str_arr_ext.str_copy_ptr(doqje__fxa.ctypes, 0, A.
                ctypes, old_size)
            return doqje__fxa
        return impl_char

    def impl(A, old_size, new_len):
        doqje__fxa = bodo.utils.utils.alloc_type(new_len, gtju__qsg, (-1,))
        doqje__fxa[:old_size] = A[:old_size]
        return doqje__fxa
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    xtxo__bpxr = math.ceil((stop - start) / step)
    return int(max(xtxo__bpxr, 0))


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
    if any(isinstance(ynax__ubf, types.Complex) for ynax__ubf in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            tswze__cxouo = (stop - start) / step
            xtxo__bpxr = math.ceil(tswze__cxouo.real)
            xphy__joozy = math.ceil(tswze__cxouo.imag)
            emylb__ugfn = int(max(min(xphy__joozy, xtxo__bpxr), 0))
            arr = np.empty(emylb__ugfn, dtype)
            for i in numba.parfors.parfor.internal_prange(emylb__ugfn):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            emylb__ugfn = bodo.libs.array_kernels.calc_nitems(start, stop, step
                )
            arr = np.empty(emylb__ugfn, dtype)
            for i in numba.parfors.parfor.internal_prange(emylb__ugfn):
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
        yusn__tdrfz = arr,
        if not inplace:
            yusn__tdrfz = arr.copy(),
        mjjzt__xbopz = bodo.libs.str_arr_ext.to_list_if_immutable_arr(
            yusn__tdrfz)
        czmgq__fef = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(mjjzt__xbopz, 0, n, czmgq__fef)
        if not ascending:
            bodo.libs.timsort.reverseRange(mjjzt__xbopz, 0, n, czmgq__fef)
        bodo.libs.str_arr_ext.cp_str_list_to_array(yusn__tdrfz, mjjzt__xbopz)
        return yusn__tdrfz[0]
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
        ovecz__grbh = []
        for i in range(n):
            if A[i]:
                ovecz__grbh.append(i + offset)
        return np.array(ovecz__grbh, np.int64),
    return impl


def ffill_bfill_arr(arr):
    return arr


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    gtju__qsg = element_type(A)
    if gtju__qsg == types.unicode_type:
        null_value = '""'
    elif gtju__qsg == types.bool_:
        null_value = 'False'
    elif gtju__qsg == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_datetime(0))')
    elif gtju__qsg == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_timestamp(pd.to_timedelta(0))')
    else:
        null_value = '0'
    xilbr__ysigg = 'i'
    izdo__cyei = False
    dxxaz__pgwo = get_overload_const_str(method)
    if dxxaz__pgwo in ('ffill', 'pad'):
        ubnpc__qnwk = 'n'
        send_right = True
    elif dxxaz__pgwo in ('backfill', 'bfill'):
        ubnpc__qnwk = 'n-1, -1, -1'
        send_right = False
        if gtju__qsg == types.unicode_type:
            xilbr__ysigg = '(n - 1) - i'
            izdo__cyei = True
    bibxl__rzv = 'def impl(A, method, parallel=False):\n'
    bibxl__rzv += '  A = decode_if_dict_array(A)\n'
    bibxl__rzv += '  has_last_value = False\n'
    bibxl__rzv += f'  last_value = {null_value}\n'
    bibxl__rzv += '  if parallel:\n'
    bibxl__rzv += '    rank = bodo.libs.distributed_api.get_rank()\n'
    bibxl__rzv += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    bibxl__rzv += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    bibxl__rzv += '  n = len(A)\n'
    bibxl__rzv += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    bibxl__rzv += f'  for i in range({ubnpc__qnwk}):\n'
    bibxl__rzv += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    bibxl__rzv += (
        f'      bodo.libs.array_kernels.setna(out_arr, {xilbr__ysigg})\n')
    bibxl__rzv += '      continue\n'
    bibxl__rzv += '    s = A[i]\n'
    bibxl__rzv += '    if bodo.libs.array_kernels.isna(A, i):\n'
    bibxl__rzv += '      s = last_value\n'
    bibxl__rzv += f'    out_arr[{xilbr__ysigg}] = s\n'
    bibxl__rzv += '    last_value = s\n'
    bibxl__rzv += '    has_last_value = True\n'
    if izdo__cyei:
        bibxl__rzv += '  return out_arr[::-1]\n'
    else:
        bibxl__rzv += '  return out_arr\n'
    unq__naed = {}
    exec(bibxl__rzv, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, unq__naed)
    impl = unq__naed['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        ryqa__ragg = 0
        tvkwa__rtqxn = n_pes - 1
        gzm__zqpoo = np.int32(rank + 1)
        kbzhr__tnqm = np.int32(rank - 1)
        qzr__onjtx = len(in_arr) - 1
        vyog__mcet = -1
        eiyk__mndr = -1
    else:
        ryqa__ragg = n_pes - 1
        tvkwa__rtqxn = 0
        gzm__zqpoo = np.int32(rank - 1)
        kbzhr__tnqm = np.int32(rank + 1)
        qzr__onjtx = 0
        vyog__mcet = len(in_arr)
        eiyk__mndr = 1
    vgv__mwml = np.int32(bodo.hiframes.rolling.comm_border_tag)
    gpsf__yuqu = np.empty(1, dtype=np.bool_)
    klm__kut = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    ujd__rirc = np.empty(1, dtype=np.bool_)
    ujo__vuiar = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    rcxg__mqkuj = False
    bek__zyte = null_value
    for i in range(qzr__onjtx, vyog__mcet, eiyk__mndr):
        if not isna(in_arr, i):
            rcxg__mqkuj = True
            bek__zyte = in_arr[i]
            break
    if rank != ryqa__ragg:
        uin__odw = bodo.libs.distributed_api.irecv(gpsf__yuqu, 1,
            kbzhr__tnqm, vgv__mwml, True)
        bodo.libs.distributed_api.wait(uin__odw, True)
        apit__atmd = bodo.libs.distributed_api.irecv(klm__kut, 1,
            kbzhr__tnqm, vgv__mwml, True)
        bodo.libs.distributed_api.wait(apit__atmd, True)
        atde__imv = gpsf__yuqu[0]
        zvk__rynhe = klm__kut[0]
    else:
        atde__imv = False
        zvk__rynhe = null_value
    if rcxg__mqkuj:
        ujd__rirc[0] = rcxg__mqkuj
        ujo__vuiar[0] = bek__zyte
    else:
        ujd__rirc[0] = atde__imv
        ujo__vuiar[0] = zvk__rynhe
    if rank != tvkwa__rtqxn:
        djjmc__uyre = bodo.libs.distributed_api.isend(ujd__rirc, 1,
            gzm__zqpoo, vgv__mwml, True)
        jsu__dlt = bodo.libs.distributed_api.isend(ujo__vuiar, 1,
            gzm__zqpoo, vgv__mwml, True)
    return atde__imv, zvk__rynhe


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    cpc__cqr = {'axis': axis, 'kind': kind, 'order': order}
    aeqkw__mphfz = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', cpc__cqr, aeqkw__mphfz, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    return A


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    gtju__qsg = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):

        def impl_int(A, repeats):
            A = decode_if_dict_array(A)
            kjn__soht = len(A)
            doqje__fxa = bodo.utils.utils.alloc_type(kjn__soht * repeats,
                gtju__qsg, (-1,))
            for i in range(kjn__soht):
                xilbr__ysigg = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for acxyz__geg in range(repeats):
                        bodo.libs.array_kernels.setna(doqje__fxa, 
                            xilbr__ysigg + acxyz__geg)
                else:
                    doqje__fxa[xilbr__ysigg:xilbr__ysigg + repeats] = A[i]
            return doqje__fxa
        return impl_int

    def impl_arr(A, repeats):
        A = decode_if_dict_array(A)
        kjn__soht = len(A)
        doqje__fxa = bodo.utils.utils.alloc_type(repeats.sum(), gtju__qsg,
            (-1,))
        xilbr__ysigg = 0
        for i in range(kjn__soht):
            arrnb__pbxkj = repeats[i]
            if bodo.libs.array_kernels.isna(A, i):
                for acxyz__geg in range(arrnb__pbxkj):
                    bodo.libs.array_kernels.setna(doqje__fxa, xilbr__ysigg +
                        acxyz__geg)
            else:
                doqje__fxa[xilbr__ysigg:xilbr__ysigg + arrnb__pbxkj] = A[i]
            xilbr__ysigg += arrnb__pbxkj
        return doqje__fxa
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
        wiel__ddxqy = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(wiel__ddxqy, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        wpug__uug = bodo.libs.array_kernels.concat([A1, A2])
        vsghq__oil = bodo.libs.array_kernels.unique(wpug__uug)
        return pd.Series(vsghq__oil).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    cpc__cqr = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    aeqkw__mphfz = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', cpc__cqr, aeqkw__mphfz, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        cap__eau = bodo.libs.array_kernels.unique(A1)
        qsiiy__pif = bodo.libs.array_kernels.unique(A2)
        wpug__uug = bodo.libs.array_kernels.concat([cap__eau, qsiiy__pif])
        tqcv__tkstt = pd.Series(wpug__uug).sort_values().values
        return slice_array_intersect1d(tqcv__tkstt)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    qxqev__mxsnd = arr[1:] == arr[:-1]
    return arr[:-1][qxqev__mxsnd]


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    cpc__cqr = {'assume_unique': assume_unique}
    aeqkw__mphfz = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', cpc__cqr, aeqkw__mphfz, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        cap__eau = bodo.libs.array_kernels.unique(A1)
        qsiiy__pif = bodo.libs.array_kernels.unique(A2)
        qxqev__mxsnd = calculate_mask_setdiff1d(cap__eau, qsiiy__pif)
        return pd.Series(cap__eau[qxqev__mxsnd]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    qxqev__mxsnd = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        qxqev__mxsnd &= A1 != A2[i]
    return qxqev__mxsnd


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    cpc__cqr = {'retstep': retstep, 'axis': axis}
    aeqkw__mphfz = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', cpc__cqr, aeqkw__mphfz, 'numpy')
    wrly__hml = False
    if is_overload_none(dtype):
        gtju__qsg = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            wrly__hml = True
        gtju__qsg = numba.np.numpy_support.as_dtype(dtype).type
    if wrly__hml:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            mvcwl__dqlqt = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            doqje__fxa = np.empty(num, gtju__qsg)
            for i in numba.parfors.parfor.internal_prange(num):
                doqje__fxa[i] = gtju__qsg(np.floor(start + i * mvcwl__dqlqt))
            return doqje__fxa
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            mvcwl__dqlqt = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            doqje__fxa = np.empty(num, gtju__qsg)
            for i in numba.parfors.parfor.internal_prange(num):
                doqje__fxa[i] = gtju__qsg(start + i * mvcwl__dqlqt)
            return doqje__fxa
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
        aozu__rde = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                aozu__rde += A[i] == val
        return aozu__rde > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    cpc__cqr = {'axis': axis, 'out': out, 'keepdims': keepdims}
    aeqkw__mphfz = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', cpc__cqr, aeqkw__mphfz, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        aozu__rde = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                aozu__rde += int(bool(A[i]))
        return aozu__rde > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    cpc__cqr = {'axis': axis, 'out': out, 'keepdims': keepdims}
    aeqkw__mphfz = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', cpc__cqr, aeqkw__mphfz, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        aozu__rde = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                aozu__rde += int(bool(A[i]))
        return aozu__rde == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    cpc__cqr = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    aeqkw__mphfz = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', cpc__cqr, aeqkw__mphfz, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        edrxn__qbni = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            doqje__fxa = np.empty(n, edrxn__qbni)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(doqje__fxa, i)
                    continue
                doqje__fxa[i] = np_cbrt_scalar(A[i], edrxn__qbni)
            return doqje__fxa
        return impl_arr
    edrxn__qbni = np.promote_types(numba.np.numpy_support.as_dtype(A),
        numba.np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, edrxn__qbni)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    kfco__vrsoo = x < 0
    if kfco__vrsoo:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if kfco__vrsoo:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    viuak__tqcg = isinstance(tup, (types.BaseTuple, types.List))
    ipcsc__cvhma = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for xonh__hjlrt in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                xonh__hjlrt, 'numpy.hstack()')
            viuak__tqcg = viuak__tqcg and bodo.utils.utils.is_array_typ(
                xonh__hjlrt, False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        viuak__tqcg = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif ipcsc__cvhma:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        lghpl__jfucn = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for xonh__hjlrt in lghpl__jfucn.types:
            ipcsc__cvhma = ipcsc__cvhma and bodo.utils.utils.is_array_typ(
                xonh__hjlrt, False)
    if not (viuak__tqcg or ipcsc__cvhma):
        return
    if ipcsc__cvhma:

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
    cpc__cqr = {'check_valid': check_valid, 'tol': tol}
    aeqkw__mphfz = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', cpc__cqr,
        aeqkw__mphfz, 'numpy')
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
        aju__mrmy = mean.shape[0]
        xkx__ckogj = size, aju__mrmy
        eur__wauc = np.random.standard_normal(xkx__ckogj)
        cov = cov.astype(np.float64)
        actx__frl, s, nnoms__pjy = np.linalg.svd(cov)
        res = np.dot(eur__wauc, np.sqrt(s).reshape(aju__mrmy, 1) * nnoms__pjy)
        qsny__xbfm = res + mean
        return qsny__xbfm
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
            qdh__xsiex = bodo.hiframes.series_kernels._get_type_max_value(arr)
            gmni__khn = typing.builtins.IndexValue(-1, qdh__xsiex)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                gvw__jgcvs = typing.builtins.IndexValue(i, arr[i])
                gmni__khn = min(gmni__khn, gvw__jgcvs)
            return gmni__khn.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        scfuh__thiil = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(arr.dtype))

        def impl_cat_arr(arr):
            iwpa__ylx = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            qdh__xsiex = scfuh__thiil(len(arr.dtype.categories) + 1)
            gmni__khn = typing.builtins.IndexValue(-1, qdh__xsiex)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                gvw__jgcvs = typing.builtins.IndexValue(i, iwpa__ylx[i])
                gmni__khn = min(gmni__khn, gvw__jgcvs)
            return gmni__khn.index
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
            qdh__xsiex = bodo.hiframes.series_kernels._get_type_min_value(arr)
            gmni__khn = typing.builtins.IndexValue(-1, qdh__xsiex)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                gvw__jgcvs = typing.builtins.IndexValue(i, arr[i])
                gmni__khn = max(gmni__khn, gvw__jgcvs)
            return gmni__khn.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        scfuh__thiil = (bodo.hiframes.pd_categorical_ext.
            get_categories_int_type(arr.dtype))

        def impl_cat_arr(arr):
            n = len(arr)
            iwpa__ylx = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            qdh__xsiex = scfuh__thiil(-1)
            gmni__khn = typing.builtins.IndexValue(-1, qdh__xsiex)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                gvw__jgcvs = typing.builtins.IndexValue(i, iwpa__ylx[i])
                gmni__khn = max(gmni__khn, gvw__jgcvs)
            return gmni__khn.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
