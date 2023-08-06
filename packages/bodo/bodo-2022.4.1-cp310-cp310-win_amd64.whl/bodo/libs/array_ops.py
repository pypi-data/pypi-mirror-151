"""
Implements array operations for usage by DataFrames and Series
such as count and max.
"""
import numba
import numpy as np
import pandas as pd
from numba import generated_jit
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.utils.typing import element_type, is_hashable_type, is_iterable_type, is_overload_true, is_overload_zero, is_str_arr_type


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    nhvwa__mldl = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(nhvwa__mldl.ctypes,
        arr, parallel, skipna)
    return nhvwa__mldl[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        ycpt__sua = len(arr)
        zkkyz__yab = np.empty(ycpt__sua, np.bool_)
        for kbftm__vnbsh in numba.parfors.parfor.internal_prange(ycpt__sua):
            zkkyz__yab[kbftm__vnbsh] = bodo.libs.array_kernels.isna(arr,
                kbftm__vnbsh)
        return zkkyz__yab
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        kbfw__uypuc = 0
        for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
            sre__mwodm = 0
            if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                sre__mwodm = 1
            kbfw__uypuc += sre__mwodm
        nhvwa__mldl = kbfw__uypuc
        return nhvwa__mldl
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    eke__tkmmw = array_op_count(arr)
    ajawh__qbilk = array_op_min(arr)
    basfb__mjt = array_op_max(arr)
    bil__cjob = array_op_mean(arr)
    agc__nltf = array_op_std(arr)
    bdc__czz = array_op_quantile(arr, 0.25)
    bdhy__obyh = array_op_quantile(arr, 0.5)
    bvrk__vcjhl = array_op_quantile(arr, 0.75)
    return (eke__tkmmw, bil__cjob, agc__nltf, ajawh__qbilk, bdc__czz,
        bdhy__obyh, bvrk__vcjhl, basfb__mjt)


def array_op_describe_dt_impl(arr):
    eke__tkmmw = array_op_count(arr)
    ajawh__qbilk = array_op_min(arr)
    basfb__mjt = array_op_max(arr)
    bil__cjob = array_op_mean(arr)
    bdc__czz = array_op_quantile(arr, 0.25)
    bdhy__obyh = array_op_quantile(arr, 0.5)
    bvrk__vcjhl = array_op_quantile(arr, 0.75)
    return (eke__tkmmw, bil__cjob, ajawh__qbilk, bdc__czz, bdhy__obyh,
        bvrk__vcjhl, basfb__mjt)


@overload(array_op_describe)
def overload_array_op_describe(arr):
    if arr.dtype == bodo.datetime64ns:
        return array_op_describe_dt_impl
    return array_op_describe_impl


@generated_jit(nopython=True)
def array_op_nbytes(arr):
    return array_op_nbytes_impl


def array_op_nbytes_impl(arr):
    return arr.nbytes


def array_op_min(arr):
    pass


@overload(array_op_min)
def overload_array_op_min(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            kdf__dxghk = numba.cpython.builtins.get_type_max_value(np.int64)
            kbfw__uypuc = 0
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
                rysyr__ezqil = kdf__dxghk
                sre__mwodm = 0
                if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                    rysyr__ezqil = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[kbftm__vnbsh]))
                    sre__mwodm = 1
                kdf__dxghk = min(kdf__dxghk, rysyr__ezqil)
                kbfw__uypuc += sre__mwodm
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(kdf__dxghk,
                kbfw__uypuc)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            kdf__dxghk = numba.cpython.builtins.get_type_max_value(np.int64)
            kbfw__uypuc = 0
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
                rysyr__ezqil = kdf__dxghk
                sre__mwodm = 0
                if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                    rysyr__ezqil = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[kbftm__vnbsh]))
                    sre__mwodm = 1
                kdf__dxghk = min(kdf__dxghk, rysyr__ezqil)
                kbfw__uypuc += sre__mwodm
            return bodo.hiframes.pd_index_ext._dti_val_finalize(kdf__dxghk,
                kbfw__uypuc)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            cdd__oxheo = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            kdf__dxghk = numba.cpython.builtins.get_type_max_value(np.int64)
            kbfw__uypuc = 0
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(
                cdd__oxheo)):
                atz__xgfa = cdd__oxheo[kbftm__vnbsh]
                if atz__xgfa == -1:
                    continue
                kdf__dxghk = min(kdf__dxghk, atz__xgfa)
                kbfw__uypuc += 1
            nhvwa__mldl = bodo.hiframes.series_kernels._box_cat_val(kdf__dxghk,
                arr.dtype, kbfw__uypuc)
            return nhvwa__mldl
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            kdf__dxghk = bodo.hiframes.series_kernels._get_date_max_value()
            kbfw__uypuc = 0
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
                rysyr__ezqil = kdf__dxghk
                sre__mwodm = 0
                if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                    rysyr__ezqil = arr[kbftm__vnbsh]
                    sre__mwodm = 1
                kdf__dxghk = min(kdf__dxghk, rysyr__ezqil)
                kbfw__uypuc += sre__mwodm
            nhvwa__mldl = bodo.hiframes.series_kernels._sum_handle_nan(
                kdf__dxghk, kbfw__uypuc)
            return nhvwa__mldl
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        kdf__dxghk = bodo.hiframes.series_kernels._get_type_max_value(arr.dtype
            )
        kbfw__uypuc = 0
        for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
            rysyr__ezqil = kdf__dxghk
            sre__mwodm = 0
            if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                rysyr__ezqil = arr[kbftm__vnbsh]
                sre__mwodm = 1
            kdf__dxghk = min(kdf__dxghk, rysyr__ezqil)
            kbfw__uypuc += sre__mwodm
        nhvwa__mldl = bodo.hiframes.series_kernels._sum_handle_nan(kdf__dxghk,
            kbfw__uypuc)
        return nhvwa__mldl
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            kdf__dxghk = numba.cpython.builtins.get_type_min_value(np.int64)
            kbfw__uypuc = 0
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
                rysyr__ezqil = kdf__dxghk
                sre__mwodm = 0
                if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                    rysyr__ezqil = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[kbftm__vnbsh]))
                    sre__mwodm = 1
                kdf__dxghk = max(kdf__dxghk, rysyr__ezqil)
                kbfw__uypuc += sre__mwodm
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(kdf__dxghk,
                kbfw__uypuc)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            kdf__dxghk = numba.cpython.builtins.get_type_min_value(np.int64)
            kbfw__uypuc = 0
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
                rysyr__ezqil = kdf__dxghk
                sre__mwodm = 0
                if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                    rysyr__ezqil = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[kbftm__vnbsh]))
                    sre__mwodm = 1
                kdf__dxghk = max(kdf__dxghk, rysyr__ezqil)
                kbfw__uypuc += sre__mwodm
            return bodo.hiframes.pd_index_ext._dti_val_finalize(kdf__dxghk,
                kbfw__uypuc)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            cdd__oxheo = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            kdf__dxghk = -1
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(
                cdd__oxheo)):
                kdf__dxghk = max(kdf__dxghk, cdd__oxheo[kbftm__vnbsh])
            nhvwa__mldl = bodo.hiframes.series_kernels._box_cat_val(kdf__dxghk,
                arr.dtype, 1)
            return nhvwa__mldl
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            kdf__dxghk = bodo.hiframes.series_kernels._get_date_min_value()
            kbfw__uypuc = 0
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
                rysyr__ezqil = kdf__dxghk
                sre__mwodm = 0
                if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                    rysyr__ezqil = arr[kbftm__vnbsh]
                    sre__mwodm = 1
                kdf__dxghk = max(kdf__dxghk, rysyr__ezqil)
                kbfw__uypuc += sre__mwodm
            nhvwa__mldl = bodo.hiframes.series_kernels._sum_handle_nan(
                kdf__dxghk, kbfw__uypuc)
            return nhvwa__mldl
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        kdf__dxghk = bodo.hiframes.series_kernels._get_type_min_value(arr.dtype
            )
        kbfw__uypuc = 0
        for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
            rysyr__ezqil = kdf__dxghk
            sre__mwodm = 0
            if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                rysyr__ezqil = arr[kbftm__vnbsh]
                sre__mwodm = 1
            kdf__dxghk = max(kdf__dxghk, rysyr__ezqil)
            kbfw__uypuc += sre__mwodm
        nhvwa__mldl = bodo.hiframes.series_kernels._sum_handle_nan(kdf__dxghk,
            kbfw__uypuc)
        return nhvwa__mldl
    return impl


def array_op_mean(arr):
    pass


@overload(array_op_mean)
def overload_array_op_mean(arr):
    if arr.dtype == bodo.datetime64ns:

        def impl(arr):
            return pd.Timestamp(types.int64(bodo.libs.array_ops.
                array_op_mean(arr.view(np.int64))))
        return impl
    valan__mvq = types.float64
    nmjy__ucpu = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        valan__mvq = types.float32
        nmjy__ucpu = types.float32
    pub__ucuru = valan__mvq(0)
    mbode__pblft = nmjy__ucpu(0)
    lqha__ydtot = nmjy__ucpu(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        kdf__dxghk = pub__ucuru
        kbfw__uypuc = mbode__pblft
        for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
            rysyr__ezqil = pub__ucuru
            sre__mwodm = mbode__pblft
            if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                rysyr__ezqil = arr[kbftm__vnbsh]
                sre__mwodm = lqha__ydtot
            kdf__dxghk += rysyr__ezqil
            kbfw__uypuc += sre__mwodm
        nhvwa__mldl = bodo.hiframes.series_kernels._mean_handle_nan(kdf__dxghk,
            kbfw__uypuc)
        return nhvwa__mldl
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        kdvrt__kaed = 0.0
        nouvu__fcbrs = 0.0
        kbfw__uypuc = 0
        for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
            rysyr__ezqil = 0.0
            sre__mwodm = 0
            if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh
                ) or not skipna:
                rysyr__ezqil = arr[kbftm__vnbsh]
                sre__mwodm = 1
            kdvrt__kaed += rysyr__ezqil
            nouvu__fcbrs += rysyr__ezqil * rysyr__ezqil
            kbfw__uypuc += sre__mwodm
        nhvwa__mldl = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            kdvrt__kaed, nouvu__fcbrs, kbfw__uypuc, ddof)
        return nhvwa__mldl
    return impl


def array_op_std(arr, skipna=True, ddof=1):
    pass


@overload(array_op_std)
def overload_array_op_std(arr, skipna=True, ddof=1):
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr, skipna=True, ddof=1):
            return pd.Timedelta(types.int64(array_op_var(arr.view(np.int64),
                skipna, ddof) ** 0.5))
        return impl_dt64
    return lambda arr, skipna=True, ddof=1: array_op_var(arr, skipna, ddof
        ) ** 0.5


def array_op_quantile(arr, q):
    pass


@overload(array_op_quantile)
def overload_array_op_quantile(arr, q):
    if is_iterable_type(q):
        if arr.dtype == bodo.datetime64ns:

            def _impl_list_dt(arr, q):
                zkkyz__yab = np.empty(len(q), np.int64)
                for kbftm__vnbsh in range(len(q)):
                    rjt__lvgl = np.float64(q[kbftm__vnbsh])
                    zkkyz__yab[kbftm__vnbsh
                        ] = bodo.libs.array_kernels.quantile(arr.view(np.
                        int64), rjt__lvgl)
                return zkkyz__yab.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            zkkyz__yab = np.empty(len(q), np.float64)
            for kbftm__vnbsh in range(len(q)):
                rjt__lvgl = np.float64(q[kbftm__vnbsh])
                zkkyz__yab[kbftm__vnbsh] = bodo.libs.array_kernels.quantile(arr
                    , rjt__lvgl)
            return zkkyz__yab
        return impl_list
    if arr.dtype == bodo.datetime64ns:

        def _impl_dt(arr, q):
            return pd.Timestamp(bodo.libs.array_kernels.quantile(arr.view(
                np.int64), np.float64(q)))
        return _impl_dt

    def impl(arr, q):
        return bodo.libs.array_kernels.quantile(arr, np.float64(q))
    return impl


def array_op_sum(arr, skipna, min_count):
    pass


@overload(array_op_sum, no_unliteral=True)
def overload_array_op_sum(arr, skipna, min_count):
    if isinstance(arr.dtype, types.Integer):
        tabhb__apd = types.intp
    elif arr.dtype == types.bool_:
        tabhb__apd = np.int64
    else:
        tabhb__apd = arr.dtype
    syplv__wczyp = tabhb__apd(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            kdf__dxghk = syplv__wczyp
            ycpt__sua = len(arr)
            kbfw__uypuc = 0
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(ycpt__sua
                ):
                rysyr__ezqil = syplv__wczyp
                sre__mwodm = 0
                if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh
                    ) or not skipna:
                    rysyr__ezqil = arr[kbftm__vnbsh]
                    sre__mwodm = 1
                kdf__dxghk += rysyr__ezqil
                kbfw__uypuc += sre__mwodm
            nhvwa__mldl = bodo.hiframes.series_kernels._var_handle_mincount(
                kdf__dxghk, kbfw__uypuc, min_count)
            return nhvwa__mldl
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            kdf__dxghk = syplv__wczyp
            ycpt__sua = len(arr)
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(ycpt__sua
                ):
                rysyr__ezqil = syplv__wczyp
                if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                    rysyr__ezqil = arr[kbftm__vnbsh]
                kdf__dxghk += rysyr__ezqil
            return kdf__dxghk
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    jmukg__elplk = arr.dtype(1)
    if arr.dtype == types.bool_:
        jmukg__elplk = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            kdf__dxghk = jmukg__elplk
            kbfw__uypuc = 0
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
                rysyr__ezqil = jmukg__elplk
                sre__mwodm = 0
                if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh
                    ) or not skipna:
                    rysyr__ezqil = arr[kbftm__vnbsh]
                    sre__mwodm = 1
                kbfw__uypuc += sre__mwodm
                kdf__dxghk *= rysyr__ezqil
            nhvwa__mldl = bodo.hiframes.series_kernels._var_handle_mincount(
                kdf__dxghk, kbfw__uypuc, min_count)
            return nhvwa__mldl
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            kdf__dxghk = jmukg__elplk
            for kbftm__vnbsh in numba.parfors.parfor.internal_prange(len(arr)):
                rysyr__ezqil = jmukg__elplk
                if not bodo.libs.array_kernels.isna(arr, kbftm__vnbsh):
                    rysyr__ezqil = arr[kbftm__vnbsh]
                kdf__dxghk *= rysyr__ezqil
            return kdf__dxghk
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        kbftm__vnbsh = bodo.libs.array_kernels._nan_argmax(arr)
        return index[kbftm__vnbsh]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        kbftm__vnbsh = bodo.libs.array_kernels._nan_argmin(arr)
        return index[kbftm__vnbsh]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            xnezc__unil = {}
            for szxs__jfkh in values:
                xnezc__unil[bodo.utils.conversion.box_if_dt64(szxs__jfkh)] = 0
            return xnezc__unil
        return impl
    else:

        def impl(values, use_hash_impl):
            return values
        return impl


def array_op_isin(arr, values):
    pass


@overload(array_op_isin, inline='always')
def overload_array_op_isin(arr, values):
    use_hash_impl = element_type(values) == element_type(arr
        ) and is_hashable_type(element_type(values))

    def impl(arr, values):
        values = bodo.libs.array_ops._convert_isin_values(values, use_hash_impl
            )
        numba.parfors.parfor.init_prange()
        ycpt__sua = len(arr)
        zkkyz__yab = np.empty(ycpt__sua, np.bool_)
        for kbftm__vnbsh in numba.parfors.parfor.internal_prange(ycpt__sua):
            zkkyz__yab[kbftm__vnbsh] = bodo.utils.conversion.box_if_dt64(arr
                [kbftm__vnbsh]) in values
        return zkkyz__yab
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    qxu__djw = len(in_arr_tup) != 1
    tzm__pat = list(in_arr_tup.types)
    kxo__etuxt = 'def impl(in_arr_tup):\n'
    kxo__etuxt += '  n = len(in_arr_tup[0])\n'
    if qxu__djw:
        jmp__eirk = ', '.join([f'in_arr_tup[{kbftm__vnbsh}][unused]' for
            kbftm__vnbsh in range(len(in_arr_tup))])
        awua__vwl = ', '.join(['False' for jna__wubw in range(len(in_arr_tup))]
            )
        kxo__etuxt += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({jmp__eirk},), ({awua__vwl},)): 0 for unused in range(0)}}
"""
        kxo__etuxt += '  map_vector = np.empty(n, np.int64)\n'
        for kbftm__vnbsh, ltxjh__lqs in enumerate(tzm__pat):
            kxo__etuxt += f'  in_lst_{kbftm__vnbsh} = []\n'
            if is_str_arr_type(ltxjh__lqs):
                kxo__etuxt += f'  total_len_{kbftm__vnbsh} = 0\n'
            kxo__etuxt += f'  null_in_lst_{kbftm__vnbsh} = []\n'
        kxo__etuxt += '  for i in range(n):\n'
        rrk__fsf = ', '.join([f'in_arr_tup[{kbftm__vnbsh}][i]' for
            kbftm__vnbsh in range(len(tzm__pat))])
        rjve__ggg = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{kbftm__vnbsh}], i)' for
            kbftm__vnbsh in range(len(tzm__pat))])
        kxo__etuxt += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({rrk__fsf},), ({rjve__ggg},))
"""
        kxo__etuxt += '    if data_val not in arr_map:\n'
        kxo__etuxt += '      set_val = len(arr_map)\n'
        kxo__etuxt += '      values_tup = data_val._data\n'
        kxo__etuxt += '      nulls_tup = data_val._null_values\n'
        for kbftm__vnbsh, ltxjh__lqs in enumerate(tzm__pat):
            kxo__etuxt += (
                f'      in_lst_{kbftm__vnbsh}.append(values_tup[{kbftm__vnbsh}])\n'
                )
            kxo__etuxt += (
                f'      null_in_lst_{kbftm__vnbsh}.append(nulls_tup[{kbftm__vnbsh}])\n'
                )
            if is_str_arr_type(ltxjh__lqs):
                kxo__etuxt += f"""      total_len_{kbftm__vnbsh}  += nulls_tup[{kbftm__vnbsh}] * len(values_tup[{kbftm__vnbsh}])
"""
        kxo__etuxt += '      arr_map[data_val] = len(arr_map)\n'
        kxo__etuxt += '    else:\n'
        kxo__etuxt += '      set_val = arr_map[data_val]\n'
        kxo__etuxt += '    map_vector[i] = set_val\n'
        kxo__etuxt += '  n_rows = len(arr_map)\n'
        for kbftm__vnbsh, ltxjh__lqs in enumerate(tzm__pat):
            if is_str_arr_type(ltxjh__lqs):
                kxo__etuxt += f"""  out_arr_{kbftm__vnbsh} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{kbftm__vnbsh})
"""
            else:
                kxo__etuxt += f"""  out_arr_{kbftm__vnbsh} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{kbftm__vnbsh}], (-1,))
"""
        kxo__etuxt += '  for j in range(len(arr_map)):\n'
        for kbftm__vnbsh in range(len(tzm__pat)):
            kxo__etuxt += f'    if null_in_lst_{kbftm__vnbsh}[j]:\n'
            kxo__etuxt += (
                f'      bodo.libs.array_kernels.setna(out_arr_{kbftm__vnbsh}, j)\n'
                )
            kxo__etuxt += '    else:\n'
            kxo__etuxt += (
                f'      out_arr_{kbftm__vnbsh}[j] = in_lst_{kbftm__vnbsh}[j]\n'
                )
        pxfr__zyhk = ', '.join([f'out_arr_{kbftm__vnbsh}' for kbftm__vnbsh in
            range(len(tzm__pat))])
        kxo__etuxt += f'  return ({pxfr__zyhk},), map_vector\n'
    else:
        kxo__etuxt += '  in_arr = in_arr_tup[0]\n'
        kxo__etuxt += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        kxo__etuxt += '  map_vector = np.empty(n, np.int64)\n'
        kxo__etuxt += '  is_na = 0\n'
        kxo__etuxt += '  in_lst = []\n'
        if is_str_arr_type(tzm__pat[0]):
            kxo__etuxt += '  total_len = 0\n'
        kxo__etuxt += '  for i in range(n):\n'
        kxo__etuxt += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        kxo__etuxt += '      is_na = 1\n'
        kxo__etuxt += (
            '      # Always put NA in the last location. We can safely use\n')
        kxo__etuxt += (
            '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n')
        kxo__etuxt += '      set_val = -1\n'
        kxo__etuxt += '    else:\n'
        kxo__etuxt += '      data_val = in_arr[i]\n'
        kxo__etuxt += '      if data_val not in arr_map:\n'
        kxo__etuxt += '        set_val = len(arr_map)\n'
        kxo__etuxt += '        in_lst.append(data_val)\n'
        if is_str_arr_type(tzm__pat[0]):
            kxo__etuxt += '        total_len += len(data_val)\n'
        kxo__etuxt += '        arr_map[data_val] = len(arr_map)\n'
        kxo__etuxt += '      else:\n'
        kxo__etuxt += '        set_val = arr_map[data_val]\n'
        kxo__etuxt += '    map_vector[i] = set_val\n'
        kxo__etuxt += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(tzm__pat[0]):
            kxo__etuxt += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            kxo__etuxt += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        kxo__etuxt += '  for j in range(len(arr_map)):\n'
        kxo__etuxt += '    out_arr[j] = in_lst[j]\n'
        kxo__etuxt += '  if is_na:\n'
        kxo__etuxt += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        kxo__etuxt += f'  return (out_arr,), map_vector\n'
    ecoa__cvgvd = {}
    exec(kxo__etuxt, {'bodo': bodo, 'np': np}, ecoa__cvgvd)
    impl = ecoa__cvgvd['impl']
    return impl
