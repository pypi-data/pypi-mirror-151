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
    tzib__hlhrn = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(tzib__hlhrn.ctypes,
        arr, parallel, skipna)
    return tzib__hlhrn[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        osggn__edile = len(arr)
        rvb__juf = np.empty(osggn__edile, np.bool_)
        for evgou__tgyw in numba.parfors.parfor.internal_prange(osggn__edile):
            rvb__juf[evgou__tgyw] = bodo.libs.array_kernels.isna(arr,
                evgou__tgyw)
        return rvb__juf
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        jhqni__jvoiu = 0
        for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
            ykmk__smds = 0
            if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                ykmk__smds = 1
            jhqni__jvoiu += ykmk__smds
        tzib__hlhrn = jhqni__jvoiu
        return tzib__hlhrn
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    dvhi__xamg = array_op_count(arr)
    ingb__zotvl = array_op_min(arr)
    qcpss__tugpk = array_op_max(arr)
    rnu__kvv = array_op_mean(arr)
    fpdec__ypqbo = array_op_std(arr)
    ram__binah = array_op_quantile(arr, 0.25)
    liogk__nva = array_op_quantile(arr, 0.5)
    bcnok__reksz = array_op_quantile(arr, 0.75)
    return (dvhi__xamg, rnu__kvv, fpdec__ypqbo, ingb__zotvl, ram__binah,
        liogk__nva, bcnok__reksz, qcpss__tugpk)


def array_op_describe_dt_impl(arr):
    dvhi__xamg = array_op_count(arr)
    ingb__zotvl = array_op_min(arr)
    qcpss__tugpk = array_op_max(arr)
    rnu__kvv = array_op_mean(arr)
    ram__binah = array_op_quantile(arr, 0.25)
    liogk__nva = array_op_quantile(arr, 0.5)
    bcnok__reksz = array_op_quantile(arr, 0.75)
    return (dvhi__xamg, rnu__kvv, ingb__zotvl, ram__binah, liogk__nva,
        bcnok__reksz, qcpss__tugpk)


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
            knxu__uzjeu = numba.cpython.builtins.get_type_max_value(np.int64)
            jhqni__jvoiu = 0
            for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
                kctc__izn = knxu__uzjeu
                ykmk__smds = 0
                if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                    kctc__izn = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[evgou__tgyw]))
                    ykmk__smds = 1
                knxu__uzjeu = min(knxu__uzjeu, kctc__izn)
                jhqni__jvoiu += ykmk__smds
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(knxu__uzjeu,
                jhqni__jvoiu)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = numba.cpython.builtins.get_type_max_value(np.int64)
            jhqni__jvoiu = 0
            for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
                kctc__izn = knxu__uzjeu
                ykmk__smds = 0
                if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                    kctc__izn = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[evgou__tgyw])
                    ykmk__smds = 1
                knxu__uzjeu = min(knxu__uzjeu, kctc__izn)
                jhqni__jvoiu += ykmk__smds
            return bodo.hiframes.pd_index_ext._dti_val_finalize(knxu__uzjeu,
                jhqni__jvoiu)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            hnyn__cntzx = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = numba.cpython.builtins.get_type_max_value(np.int64)
            jhqni__jvoiu = 0
            for evgou__tgyw in numba.parfors.parfor.internal_prange(len(
                hnyn__cntzx)):
                tan__kwuj = hnyn__cntzx[evgou__tgyw]
                if tan__kwuj == -1:
                    continue
                knxu__uzjeu = min(knxu__uzjeu, tan__kwuj)
                jhqni__jvoiu += 1
            tzib__hlhrn = bodo.hiframes.series_kernels._box_cat_val(knxu__uzjeu
                , arr.dtype, jhqni__jvoiu)
            return tzib__hlhrn
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = bodo.hiframes.series_kernels._get_date_max_value()
            jhqni__jvoiu = 0
            for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
                kctc__izn = knxu__uzjeu
                ykmk__smds = 0
                if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                    kctc__izn = arr[evgou__tgyw]
                    ykmk__smds = 1
                knxu__uzjeu = min(knxu__uzjeu, kctc__izn)
                jhqni__jvoiu += ykmk__smds
            tzib__hlhrn = bodo.hiframes.series_kernels._sum_handle_nan(
                knxu__uzjeu, jhqni__jvoiu)
            return tzib__hlhrn
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        knxu__uzjeu = bodo.hiframes.series_kernels._get_type_max_value(arr.
            dtype)
        jhqni__jvoiu = 0
        for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
            kctc__izn = knxu__uzjeu
            ykmk__smds = 0
            if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                kctc__izn = arr[evgou__tgyw]
                ykmk__smds = 1
            knxu__uzjeu = min(knxu__uzjeu, kctc__izn)
            jhqni__jvoiu += ykmk__smds
        tzib__hlhrn = bodo.hiframes.series_kernels._sum_handle_nan(knxu__uzjeu,
            jhqni__jvoiu)
        return tzib__hlhrn
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = numba.cpython.builtins.get_type_min_value(np.int64)
            jhqni__jvoiu = 0
            for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
                kctc__izn = knxu__uzjeu
                ykmk__smds = 0
                if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                    kctc__izn = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[evgou__tgyw]))
                    ykmk__smds = 1
                knxu__uzjeu = max(knxu__uzjeu, kctc__izn)
                jhqni__jvoiu += ykmk__smds
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(knxu__uzjeu,
                jhqni__jvoiu)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = numba.cpython.builtins.get_type_min_value(np.int64)
            jhqni__jvoiu = 0
            for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
                kctc__izn = knxu__uzjeu
                ykmk__smds = 0
                if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                    kctc__izn = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        arr[evgou__tgyw])
                    ykmk__smds = 1
                knxu__uzjeu = max(knxu__uzjeu, kctc__izn)
                jhqni__jvoiu += ykmk__smds
            return bodo.hiframes.pd_index_ext._dti_val_finalize(knxu__uzjeu,
                jhqni__jvoiu)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            hnyn__cntzx = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = -1
            for evgou__tgyw in numba.parfors.parfor.internal_prange(len(
                hnyn__cntzx)):
                knxu__uzjeu = max(knxu__uzjeu, hnyn__cntzx[evgou__tgyw])
            tzib__hlhrn = bodo.hiframes.series_kernels._box_cat_val(knxu__uzjeu
                , arr.dtype, 1)
            return tzib__hlhrn
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = bodo.hiframes.series_kernels._get_date_min_value()
            jhqni__jvoiu = 0
            for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
                kctc__izn = knxu__uzjeu
                ykmk__smds = 0
                if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                    kctc__izn = arr[evgou__tgyw]
                    ykmk__smds = 1
                knxu__uzjeu = max(knxu__uzjeu, kctc__izn)
                jhqni__jvoiu += ykmk__smds
            tzib__hlhrn = bodo.hiframes.series_kernels._sum_handle_nan(
                knxu__uzjeu, jhqni__jvoiu)
            return tzib__hlhrn
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        knxu__uzjeu = bodo.hiframes.series_kernels._get_type_min_value(arr.
            dtype)
        jhqni__jvoiu = 0
        for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
            kctc__izn = knxu__uzjeu
            ykmk__smds = 0
            if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                kctc__izn = arr[evgou__tgyw]
                ykmk__smds = 1
            knxu__uzjeu = max(knxu__uzjeu, kctc__izn)
            jhqni__jvoiu += ykmk__smds
        tzib__hlhrn = bodo.hiframes.series_kernels._sum_handle_nan(knxu__uzjeu,
            jhqni__jvoiu)
        return tzib__hlhrn
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
    ohtoq__ybiuz = types.float64
    mlfio__mxxsp = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        ohtoq__ybiuz = types.float32
        mlfio__mxxsp = types.float32
    atw__kvpa = ohtoq__ybiuz(0)
    cyk__axq = mlfio__mxxsp(0)
    xnsi__cwv = mlfio__mxxsp(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        knxu__uzjeu = atw__kvpa
        jhqni__jvoiu = cyk__axq
        for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
            kctc__izn = atw__kvpa
            ykmk__smds = cyk__axq
            if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                kctc__izn = arr[evgou__tgyw]
                ykmk__smds = xnsi__cwv
            knxu__uzjeu += kctc__izn
            jhqni__jvoiu += ykmk__smds
        tzib__hlhrn = bodo.hiframes.series_kernels._mean_handle_nan(knxu__uzjeu
            , jhqni__jvoiu)
        return tzib__hlhrn
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        yrf__gjkj = 0.0
        herl__neeqz = 0.0
        jhqni__jvoiu = 0
        for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
            kctc__izn = 0.0
            ykmk__smds = 0
            if not bodo.libs.array_kernels.isna(arr, evgou__tgyw
                ) or not skipna:
                kctc__izn = arr[evgou__tgyw]
                ykmk__smds = 1
            yrf__gjkj += kctc__izn
            herl__neeqz += kctc__izn * kctc__izn
            jhqni__jvoiu += ykmk__smds
        tzib__hlhrn = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            yrf__gjkj, herl__neeqz, jhqni__jvoiu, ddof)
        return tzib__hlhrn
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
                rvb__juf = np.empty(len(q), np.int64)
                for evgou__tgyw in range(len(q)):
                    coozn__xczg = np.float64(q[evgou__tgyw])
                    rvb__juf[evgou__tgyw] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), coozn__xczg)
                return rvb__juf.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            rvb__juf = np.empty(len(q), np.float64)
            for evgou__tgyw in range(len(q)):
                coozn__xczg = np.float64(q[evgou__tgyw])
                rvb__juf[evgou__tgyw] = bodo.libs.array_kernels.quantile(arr,
                    coozn__xczg)
            return rvb__juf
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
        cmkbq__jxhbd = types.intp
    elif arr.dtype == types.bool_:
        cmkbq__jxhbd = np.int64
    else:
        cmkbq__jxhbd = arr.dtype
    wgip__fey = cmkbq__jxhbd(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = wgip__fey
            osggn__edile = len(arr)
            jhqni__jvoiu = 0
            for evgou__tgyw in numba.parfors.parfor.internal_prange(
                osggn__edile):
                kctc__izn = wgip__fey
                ykmk__smds = 0
                if not bodo.libs.array_kernels.isna(arr, evgou__tgyw
                    ) or not skipna:
                    kctc__izn = arr[evgou__tgyw]
                    ykmk__smds = 1
                knxu__uzjeu += kctc__izn
                jhqni__jvoiu += ykmk__smds
            tzib__hlhrn = bodo.hiframes.series_kernels._var_handle_mincount(
                knxu__uzjeu, jhqni__jvoiu, min_count)
            return tzib__hlhrn
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = wgip__fey
            osggn__edile = len(arr)
            for evgou__tgyw in numba.parfors.parfor.internal_prange(
                osggn__edile):
                kctc__izn = wgip__fey
                if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                    kctc__izn = arr[evgou__tgyw]
                knxu__uzjeu += kctc__izn
            return knxu__uzjeu
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    icwc__cbou = arr.dtype(1)
    if arr.dtype == types.bool_:
        icwc__cbou = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = icwc__cbou
            jhqni__jvoiu = 0
            for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
                kctc__izn = icwc__cbou
                ykmk__smds = 0
                if not bodo.libs.array_kernels.isna(arr, evgou__tgyw
                    ) or not skipna:
                    kctc__izn = arr[evgou__tgyw]
                    ykmk__smds = 1
                jhqni__jvoiu += ykmk__smds
                knxu__uzjeu *= kctc__izn
            tzib__hlhrn = bodo.hiframes.series_kernels._var_handle_mincount(
                knxu__uzjeu, jhqni__jvoiu, min_count)
            return tzib__hlhrn
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            knxu__uzjeu = icwc__cbou
            for evgou__tgyw in numba.parfors.parfor.internal_prange(len(arr)):
                kctc__izn = icwc__cbou
                if not bodo.libs.array_kernels.isna(arr, evgou__tgyw):
                    kctc__izn = arr[evgou__tgyw]
                knxu__uzjeu *= kctc__izn
            return knxu__uzjeu
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        evgou__tgyw = bodo.libs.array_kernels._nan_argmax(arr)
        return index[evgou__tgyw]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        evgou__tgyw = bodo.libs.array_kernels._nan_argmin(arr)
        return index[evgou__tgyw]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            jnu__wfbwq = {}
            for jja__arcv in values:
                jnu__wfbwq[bodo.utils.conversion.box_if_dt64(jja__arcv)] = 0
            return jnu__wfbwq
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
        osggn__edile = len(arr)
        rvb__juf = np.empty(osggn__edile, np.bool_)
        for evgou__tgyw in numba.parfors.parfor.internal_prange(osggn__edile):
            rvb__juf[evgou__tgyw] = bodo.utils.conversion.box_if_dt64(arr[
                evgou__tgyw]) in values
        return rvb__juf
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    edxcb__ervfg = len(in_arr_tup) != 1
    wktnm__gvhl = list(in_arr_tup.types)
    mhbk__zebee = 'def impl(in_arr_tup):\n'
    mhbk__zebee += '  n = len(in_arr_tup[0])\n'
    if edxcb__ervfg:
        uzdn__neh = ', '.join([f'in_arr_tup[{evgou__tgyw}][unused]' for
            evgou__tgyw in range(len(in_arr_tup))])
        pyja__tfq = ', '.join(['False' for gkopg__vic in range(len(
            in_arr_tup))])
        mhbk__zebee += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({uzdn__neh},), ({pyja__tfq},)): 0 for unused in range(0)}}
"""
        mhbk__zebee += '  map_vector = np.empty(n, np.int64)\n'
        for evgou__tgyw, lyd__vves in enumerate(wktnm__gvhl):
            mhbk__zebee += f'  in_lst_{evgou__tgyw} = []\n'
            if is_str_arr_type(lyd__vves):
                mhbk__zebee += f'  total_len_{evgou__tgyw} = 0\n'
            mhbk__zebee += f'  null_in_lst_{evgou__tgyw} = []\n'
        mhbk__zebee += '  for i in range(n):\n'
        itu__ppklp = ', '.join([f'in_arr_tup[{evgou__tgyw}][i]' for
            evgou__tgyw in range(len(wktnm__gvhl))])
        gcbm__inx = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{evgou__tgyw}], i)' for
            evgou__tgyw in range(len(wktnm__gvhl))])
        mhbk__zebee += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({itu__ppklp},), ({gcbm__inx},))
"""
        mhbk__zebee += '    if data_val not in arr_map:\n'
        mhbk__zebee += '      set_val = len(arr_map)\n'
        mhbk__zebee += '      values_tup = data_val._data\n'
        mhbk__zebee += '      nulls_tup = data_val._null_values\n'
        for evgou__tgyw, lyd__vves in enumerate(wktnm__gvhl):
            mhbk__zebee += (
                f'      in_lst_{evgou__tgyw}.append(values_tup[{evgou__tgyw}])\n'
                )
            mhbk__zebee += (
                f'      null_in_lst_{evgou__tgyw}.append(nulls_tup[{evgou__tgyw}])\n'
                )
            if is_str_arr_type(lyd__vves):
                mhbk__zebee += f"""      total_len_{evgou__tgyw}  += nulls_tup[{evgou__tgyw}] * len(values_tup[{evgou__tgyw}])
"""
        mhbk__zebee += '      arr_map[data_val] = len(arr_map)\n'
        mhbk__zebee += '    else:\n'
        mhbk__zebee += '      set_val = arr_map[data_val]\n'
        mhbk__zebee += '    map_vector[i] = set_val\n'
        mhbk__zebee += '  n_rows = len(arr_map)\n'
        for evgou__tgyw, lyd__vves in enumerate(wktnm__gvhl):
            if is_str_arr_type(lyd__vves):
                mhbk__zebee += f"""  out_arr_{evgou__tgyw} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{evgou__tgyw})
"""
            else:
                mhbk__zebee += f"""  out_arr_{evgou__tgyw} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{evgou__tgyw}], (-1,))
"""
        mhbk__zebee += '  for j in range(len(arr_map)):\n'
        for evgou__tgyw in range(len(wktnm__gvhl)):
            mhbk__zebee += f'    if null_in_lst_{evgou__tgyw}[j]:\n'
            mhbk__zebee += (
                f'      bodo.libs.array_kernels.setna(out_arr_{evgou__tgyw}, j)\n'
                )
            mhbk__zebee += '    else:\n'
            mhbk__zebee += (
                f'      out_arr_{evgou__tgyw}[j] = in_lst_{evgou__tgyw}[j]\n')
        zppn__nrp = ', '.join([f'out_arr_{evgou__tgyw}' for evgou__tgyw in
            range(len(wktnm__gvhl))])
        mhbk__zebee += f'  return ({zppn__nrp},), map_vector\n'
    else:
        mhbk__zebee += '  in_arr = in_arr_tup[0]\n'
        mhbk__zebee += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        mhbk__zebee += '  map_vector = np.empty(n, np.int64)\n'
        mhbk__zebee += '  is_na = 0\n'
        mhbk__zebee += '  in_lst = []\n'
        if is_str_arr_type(wktnm__gvhl[0]):
            mhbk__zebee += '  total_len = 0\n'
        mhbk__zebee += '  for i in range(n):\n'
        mhbk__zebee += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        mhbk__zebee += '      is_na = 1\n'
        mhbk__zebee += (
            '      # Always put NA in the last location. We can safely use\n')
        mhbk__zebee += (
            '      # -1 because in_arr[-1] == in_arr[len(in_arr) - 1]\n')
        mhbk__zebee += '      set_val = -1\n'
        mhbk__zebee += '    else:\n'
        mhbk__zebee += '      data_val = in_arr[i]\n'
        mhbk__zebee += '      if data_val not in arr_map:\n'
        mhbk__zebee += '        set_val = len(arr_map)\n'
        mhbk__zebee += '        in_lst.append(data_val)\n'
        if is_str_arr_type(wktnm__gvhl[0]):
            mhbk__zebee += '        total_len += len(data_val)\n'
        mhbk__zebee += '        arr_map[data_val] = len(arr_map)\n'
        mhbk__zebee += '      else:\n'
        mhbk__zebee += '        set_val = arr_map[data_val]\n'
        mhbk__zebee += '    map_vector[i] = set_val\n'
        mhbk__zebee += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(wktnm__gvhl[0]):
            mhbk__zebee += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            mhbk__zebee += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        mhbk__zebee += '  for j in range(len(arr_map)):\n'
        mhbk__zebee += '    out_arr[j] = in_lst[j]\n'
        mhbk__zebee += '  if is_na:\n'
        mhbk__zebee += (
            '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n')
        mhbk__zebee += f'  return (out_arr,), map_vector\n'
    dbako__cwn = {}
    exec(mhbk__zebee, {'bodo': bodo, 'np': np}, dbako__cwn)
    impl = dbako__cwn['impl']
    return impl
