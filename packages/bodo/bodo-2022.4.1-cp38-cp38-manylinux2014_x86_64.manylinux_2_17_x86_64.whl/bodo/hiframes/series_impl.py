"""
Implementation of Series attributes and methods using overload.
"""
import operator
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, overload_attribute, overload_method, register_jitable
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, datetime_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_offsets_ext import is_offsets_type
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType, if_series_to_array_type, is_series_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.transform import gen_const_tup, is_var_size_item_array_type
from bodo.utils.typing import BodoError, can_replace, check_unsupported_args, dtype_to_array_type, element_type, get_common_scalar_dtype, get_literal_value, get_overload_const_bytes, get_overload_const_int, get_overload_const_str, is_common_scalar_dtype, is_iterable_type, is_literal_type, is_nullable_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_int, is_overload_constant_nan, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, is_str_arr_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array


@overload_attribute(HeterogeneousSeriesType, 'index', inline='always')
@overload_attribute(SeriesType, 'index', inline='always')
def overload_series_index(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_index(s)


@overload_attribute(HeterogeneousSeriesType, 'values', inline='always')
@overload_attribute(SeriesType, 'values', inline='always')
def overload_series_values(s):
    if isinstance(s.data, bodo.DatetimeArrayType):

        def impl(s):
            ilte__vfc = bodo.hiframes.pd_series_ext.get_series_data(s)
            konz__pbtv = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                ilte__vfc)
            return konz__pbtv
        return impl
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s)


@overload_attribute(SeriesType, 'dtype', inline='always')
def overload_series_dtype(s):
    if s.dtype == bodo.string_type:
        raise BodoError('Series.dtype not supported for string Series yet')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(s, 'Series.dtype'
        )
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s).dtype


@overload_attribute(HeterogeneousSeriesType, 'shape')
@overload_attribute(SeriesType, 'shape')
def overload_series_shape(s):
    return lambda s: (len(bodo.hiframes.pd_series_ext.get_series_data(s)),)


@overload_attribute(HeterogeneousSeriesType, 'ndim', inline='always')
@overload_attribute(SeriesType, 'ndim', inline='always')
def overload_series_ndim(s):
    return lambda s: 1


@overload_attribute(HeterogeneousSeriesType, 'size')
@overload_attribute(SeriesType, 'size')
def overload_series_size(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s))


@overload_attribute(HeterogeneousSeriesType, 'T', inline='always')
@overload_attribute(SeriesType, 'T', inline='always')
def overload_series_T(s):
    return lambda s: s


@overload_attribute(SeriesType, 'hasnans', inline='always')
def overload_series_hasnans(s):
    return lambda s: s.isna().sum() != 0


@overload_attribute(HeterogeneousSeriesType, 'empty')
@overload_attribute(SeriesType, 'empty')
def overload_series_empty(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s)) == 0


@overload_attribute(SeriesType, 'dtypes', inline='always')
def overload_series_dtypes(s):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(s,
        'Series.dtypes')
    return lambda s: s.dtype


@overload_attribute(HeterogeneousSeriesType, 'name', inline='always')
@overload_attribute(SeriesType, 'name', inline='always')
def overload_series_name(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_name(s)


@overload(len, no_unliteral=True)
def overload_series_len(S):
    if isinstance(S, (SeriesType, HeterogeneousSeriesType)):
        return lambda S: len(bodo.hiframes.pd_series_ext.get_series_data(S))


@overload_method(SeriesType, 'copy', inline='always', no_unliteral=True)
def overload_series_copy(S, deep=True):
    if is_overload_true(deep):

        def impl1(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr.copy(),
                index, name)
        return impl1
    if is_overload_false(deep):

        def impl2(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl2

    def impl(S, deep=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        if deep:
            arr = arr.copy()
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'to_list', no_unliteral=True)
@overload_method(SeriesType, 'tolist', no_unliteral=True)
def overload_series_to_list(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.tolist()')
    if isinstance(S.dtype, types.Float):

        def impl_float(S):
            wiqtf__maywo = list()
            for vov__ggess in range(len(S)):
                wiqtf__maywo.append(S.iat[vov__ggess])
            return wiqtf__maywo
        return impl_float

    def impl(S):
        wiqtf__maywo = list()
        for vov__ggess in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, vov__ggess):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            wiqtf__maywo.append(S.iat[vov__ggess])
        return wiqtf__maywo
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    jrezx__dexj = dict(dtype=dtype, copy=copy, na_value=na_value)
    adk__dtahn = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    jrezx__dexj = dict(name=name, inplace=inplace)
    adk__dtahn = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not bodo.hiframes.dataframe_impl._is_all_levels(S, level):
        raise_bodo_error(
            'Series.reset_index(): only dropping all index levels supported')
    if not is_overload_constant_bool(drop):
        raise_bodo_error(
            "Series.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if is_overload_true(drop):

        def impl_drop(S, level=None, drop=False, name=None, inplace=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_index_ext.init_range_index(0, len(arr),
                1, None)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl_drop

    def get_name_literal(name_typ, is_index=False, series_name=None):
        if is_overload_none(name_typ):
            if is_index:
                return 'index' if series_name != 'index' else 'level_0'
            return 0
        if is_literal_type(name_typ):
            return get_literal_value(name_typ)
        else:
            raise BodoError(
                'Series.reset_index() not supported for non-literal series names'
                )
    series_name = get_name_literal(S.name_typ)
    nggh__fpje = get_name_literal(S.index.name_typ, True, series_name)
    columns = [nggh__fpje, series_name]
    wvw__gcjfb = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    wvw__gcjfb += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    wvw__gcjfb += """    index = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S))
"""
    wvw__gcjfb += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    wvw__gcjfb += '    col_var = {}\n'.format(gen_const_tup(columns))
    wvw__gcjfb += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe((index, arr), df_index, col_var)
"""
    huc__cuo = {}
    exec(wvw__gcjfb, {'bodo': bodo}, huc__cuo)
    kyuyx__zjz = huc__cuo['_impl']
    return kyuyx__zjz


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rkrju__svrna = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


@overload_method(SeriesType, 'round', inline='always', no_unliteral=True)
def overload_series_round(S, decimals=0):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.round()')

    def impl(S, decimals=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        rkrju__svrna = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for vov__ggess in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[vov__ggess]):
                bodo.libs.array_kernels.setna(rkrju__svrna, vov__ggess)
            else:
                rkrju__svrna[vov__ggess] = np.round(arr[vov__ggess], decimals)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    jrezx__dexj = dict(level=level, numeric_only=numeric_only)
    adk__dtahn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sum(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sum(): skipna argument must be a boolean')
    if not is_overload_int(min_count):
        raise BodoError('Series.sum(): min_count argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sum()'
        )

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_sum(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'prod', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'product', inline='always', no_unliteral=True)
def overload_series_prod(S, axis=None, skipna=True, level=None,
    numeric_only=None, min_count=0):
    jrezx__dexj = dict(level=level, numeric_only=numeric_only)
    adk__dtahn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.product(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.product(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.product()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_prod(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'any', inline='always', no_unliteral=True)
def overload_series_any(S, axis=0, bool_only=None, skipna=True, level=None):
    jrezx__dexj = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    adk__dtahn = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ljzr__stms = 0
        for vov__ggess in numba.parfors.parfor.internal_prange(len(A)):
            lszr__jejsh = 0
            if not bodo.libs.array_kernels.isna(A, vov__ggess):
                lszr__jejsh = int(A[vov__ggess])
            ljzr__stms += lszr__jejsh
        return ljzr__stms != 0
    return impl


@overload_method(SeriesType, 'equals', inline='always', no_unliteral=True)
def overload_series_equals(S, other):
    if not isinstance(other, SeriesType):
        raise BodoError("Series.equals() 'other' must be a Series")
    if isinstance(S.data, bodo.ArrayItemArrayType):
        raise BodoError(
            'Series.equals() not supported for Series where each element is an array or list'
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.equals()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.equals()')
    if S.data != other.data:
        return lambda S, other: False

    def impl(S, other):
        umc__ybmvj = bodo.hiframes.pd_series_ext.get_series_data(S)
        purzt__rbz = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        ljzr__stms = 0
        for vov__ggess in numba.parfors.parfor.internal_prange(len(umc__ybmvj)
            ):
            lszr__jejsh = 0
            bvtl__bydu = bodo.libs.array_kernels.isna(umc__ybmvj, vov__ggess)
            uxfh__nwmc = bodo.libs.array_kernels.isna(purzt__rbz, vov__ggess)
            if bvtl__bydu and not uxfh__nwmc or not bvtl__bydu and uxfh__nwmc:
                lszr__jejsh = 1
            elif not bvtl__bydu:
                if umc__ybmvj[vov__ggess] != purzt__rbz[vov__ggess]:
                    lszr__jejsh = 1
            ljzr__stms += lszr__jejsh
        return ljzr__stms == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    jrezx__dexj = dict(axis=axis, bool_only=bool_only, skipna=skipna, level
        =level)
    adk__dtahn = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ljzr__stms = 0
        for vov__ggess in numba.parfors.parfor.internal_prange(len(A)):
            lszr__jejsh = 0
            if not bodo.libs.array_kernels.isna(A, vov__ggess):
                lszr__jejsh = int(not A[vov__ggess])
            ljzr__stms += lszr__jejsh
        return ljzr__stms == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    jrezx__dexj = dict(level=level)
    adk__dtahn = dict(level=None)
    check_unsupported_args('Series.mad', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    hqhap__ylol = types.float64
    hozs__rsik = types.float64
    if S.dtype == types.float32:
        hqhap__ylol = types.float32
        hozs__rsik = types.float32
    kcbp__ltiow = hqhap__ylol(0)
    rvrs__fijb = hozs__rsik(0)
    dlcr__qsewg = hozs__rsik(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        fpffz__ypalf = kcbp__ltiow
        ljzr__stms = rvrs__fijb
        for vov__ggess in numba.parfors.parfor.internal_prange(len(A)):
            lszr__jejsh = kcbp__ltiow
            fbo__isw = rvrs__fijb
            if not bodo.libs.array_kernels.isna(A, vov__ggess) or not skipna:
                lszr__jejsh = A[vov__ggess]
                fbo__isw = dlcr__qsewg
            fpffz__ypalf += lszr__jejsh
            ljzr__stms += fbo__isw
        hfn__hqv = bodo.hiframes.series_kernels._mean_handle_nan(fpffz__ypalf,
            ljzr__stms)
        luxyu__dqbd = kcbp__ltiow
        for vov__ggess in numba.parfors.parfor.internal_prange(len(A)):
            lszr__jejsh = kcbp__ltiow
            if not bodo.libs.array_kernels.isna(A, vov__ggess) or not skipna:
                lszr__jejsh = abs(A[vov__ggess] - hfn__hqv)
            luxyu__dqbd += lszr__jejsh
        hmwi__dlczu = bodo.hiframes.series_kernels._mean_handle_nan(luxyu__dqbd
            , ljzr__stms)
        return hmwi__dlczu
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    jrezx__dexj = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    adk__dtahn = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mean(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.mean()')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_mean(arr)
    return impl


@overload_method(SeriesType, 'sem', inline='always', no_unliteral=True)
def overload_series_sem(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    jrezx__dexj = dict(level=level, numeric_only=numeric_only)
    adk__dtahn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sem(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sem(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.sem(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sem()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ggn__xtn = 0
        rvbim__cmw = 0
        ljzr__stms = 0
        for vov__ggess in numba.parfors.parfor.internal_prange(len(A)):
            lszr__jejsh = 0
            fbo__isw = 0
            if not bodo.libs.array_kernels.isna(A, vov__ggess) or not skipna:
                lszr__jejsh = A[vov__ggess]
                fbo__isw = 1
            ggn__xtn += lszr__jejsh
            rvbim__cmw += lszr__jejsh * lszr__jejsh
            ljzr__stms += fbo__isw
        twgpo__ejelw = (bodo.hiframes.series_kernels.
            _compute_var_nan_count_ddof(ggn__xtn, rvbim__cmw, ljzr__stms, ddof)
            )
        cer__lfec = bodo.hiframes.series_kernels._sem_handle_nan(twgpo__ejelw,
            ljzr__stms)
        return cer__lfec
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    jrezx__dexj = dict(level=level, numeric_only=numeric_only)
    adk__dtahn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.kurtosis(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError(
            "Series.kurtosis(): 'skipna' argument must be a boolean")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.kurtosis()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ggn__xtn = 0.0
        rvbim__cmw = 0.0
        fkv__xszmd = 0.0
        cyo__qyjl = 0.0
        ljzr__stms = 0
        for vov__ggess in numba.parfors.parfor.internal_prange(len(A)):
            lszr__jejsh = 0.0
            fbo__isw = 0
            if not bodo.libs.array_kernels.isna(A, vov__ggess) or not skipna:
                lszr__jejsh = np.float64(A[vov__ggess])
                fbo__isw = 1
            ggn__xtn += lszr__jejsh
            rvbim__cmw += lszr__jejsh ** 2
            fkv__xszmd += lszr__jejsh ** 3
            cyo__qyjl += lszr__jejsh ** 4
            ljzr__stms += fbo__isw
        twgpo__ejelw = bodo.hiframes.series_kernels.compute_kurt(ggn__xtn,
            rvbim__cmw, fkv__xszmd, cyo__qyjl, ljzr__stms)
        return twgpo__ejelw
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    jrezx__dexj = dict(level=level, numeric_only=numeric_only)
    adk__dtahn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.skew(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.skew(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.skew()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ggn__xtn = 0.0
        rvbim__cmw = 0.0
        fkv__xszmd = 0.0
        ljzr__stms = 0
        for vov__ggess in numba.parfors.parfor.internal_prange(len(A)):
            lszr__jejsh = 0.0
            fbo__isw = 0
            if not bodo.libs.array_kernels.isna(A, vov__ggess) or not skipna:
                lszr__jejsh = np.float64(A[vov__ggess])
                fbo__isw = 1
            ggn__xtn += lszr__jejsh
            rvbim__cmw += lszr__jejsh ** 2
            fkv__xszmd += lszr__jejsh ** 3
            ljzr__stms += fbo__isw
        twgpo__ejelw = bodo.hiframes.series_kernels.compute_skew(ggn__xtn,
            rvbim__cmw, fkv__xszmd, ljzr__stms)
        return twgpo__ejelw
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    jrezx__dexj = dict(level=level, numeric_only=numeric_only)
    adk__dtahn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.var(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.var(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.var(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.var()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_var(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'std', inline='always', no_unliteral=True)
def overload_series_std(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    jrezx__dexj = dict(level=level, numeric_only=numeric_only)
    adk__dtahn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.std(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.std(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.std(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.std()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_std(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'dot', inline='always', no_unliteral=True)
def overload_series_dot(S, other):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.dot()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.dot()')

    def impl(S, other):
        umc__ybmvj = bodo.hiframes.pd_series_ext.get_series_data(S)
        purzt__rbz = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        nro__fyq = 0
        for vov__ggess in numba.parfors.parfor.internal_prange(len(umc__ybmvj)
            ):
            xrd__sxec = umc__ybmvj[vov__ggess]
            zraf__hwkt = purzt__rbz[vov__ggess]
            nro__fyq += xrd__sxec * zraf__hwkt
        return nro__fyq
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    jrezx__dexj = dict(skipna=skipna)
    adk__dtahn = dict(skipna=True)
    check_unsupported_args('Series.cumsum', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumsum(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumsum()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumsum(), index, name)
    return impl


@overload_method(SeriesType, 'cumprod', inline='always', no_unliteral=True)
def overload_series_cumprod(S, axis=None, skipna=True):
    jrezx__dexj = dict(skipna=skipna)
    adk__dtahn = dict(skipna=True)
    check_unsupported_args('Series.cumprod', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumprod(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumprod()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(A.cumprod(), index, name
            )
    return impl


@overload_method(SeriesType, 'cummin', inline='always', no_unliteral=True)
def overload_series_cummin(S, axis=None, skipna=True):
    jrezx__dexj = dict(skipna=skipna)
    adk__dtahn = dict(skipna=True)
    check_unsupported_args('Series.cummin', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummin(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummin()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummin(arr), index, name)
    return impl


@overload_method(SeriesType, 'cummax', inline='always', no_unliteral=True)
def overload_series_cummax(S, axis=None, skipna=True):
    jrezx__dexj = dict(skipna=skipna)
    adk__dtahn = dict(skipna=True)
    check_unsupported_args('Series.cummax', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummax(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummax()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.cummax(arr), index, name)
    return impl


@overload_method(SeriesType, 'rename', inline='always', no_unliteral=True)
def overload_series_rename(S, index=None, axis=None, copy=True, inplace=
    False, level=None, errors='ignore'):
    if not (index == bodo.string_type or isinstance(index, types.StringLiteral)
        ):
        raise BodoError("Series.rename() 'index' can only be a string")
    jrezx__dexj = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    adk__dtahn = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        pbbsr__mkq = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, pbbsr__mkq, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    jrezx__dexj = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    adk__dtahn = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if is_overload_none(mapper) or not is_scalar_type(mapper):
        raise BodoError(
            "Series.rename_axis(): 'mapper' is required and must be a scalar type."
            )

    def impl(S, mapper=None, index=None, columns=None, axis=None, copy=True,
        inplace=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        index = index.rename(mapper)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'abs', inline='always', no_unliteral=True)
def overload_series_abs(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.abs()'
        )

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(np.abs(A), index, name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    jrezx__dexj = dict(level=level)
    adk__dtahn = dict(level=None)
    check_unsupported_args('Series.count', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    jrezx__dexj = dict(method=method, min_periods=min_periods)
    adk__dtahn = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        kwa__rqdzm = S.sum()
        ymwaq__eihni = other.sum()
        a = n * (S * other).sum() - kwa__rqdzm * ymwaq__eihni
        foje__nwwp = n * (S ** 2).sum() - kwa__rqdzm ** 2
        bihyb__mcbdn = n * (other ** 2).sum() - ymwaq__eihni ** 2
        return a / np.sqrt(foje__nwwp * bihyb__mcbdn)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    jrezx__dexj = dict(min_periods=min_periods)
    adk__dtahn = dict(min_periods=None)
    check_unsupported_args('Series.cov', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        kwa__rqdzm = S.mean()
        ymwaq__eihni = other.mean()
        rnmaq__cvgn = ((S - kwa__rqdzm) * (other - ymwaq__eihni)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(rnmaq__cvgn, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            tzo__fho = np.sign(sum_val)
            return np.inf * tzo__fho
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    jrezx__dexj = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    adk__dtahn = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.min()'
        )

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_min(arr)
    return impl


@overload(max, no_unliteral=True)
def overload_series_builtins_max(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.max()
        return impl


@overload(min, no_unliteral=True)
def overload_series_builtins_min(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.min()
        return impl


@overload(sum, no_unliteral=True)
def overload_series_builtins_sum(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.sum()
        return impl


@overload(np.prod, inline='always', no_unliteral=True)
def overload_series_np_prod(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.prod()
        return impl


@overload_method(SeriesType, 'max', inline='always', no_unliteral=True)
def overload_series_max(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    jrezx__dexj = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    adk__dtahn = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.max()'
        )

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    jrezx__dexj = dict(axis=axis, skipna=skipna)
    adk__dtahn = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmin()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmin() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmin(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmin(arr, index)
    return impl


@overload_method(SeriesType, 'idxmax', inline='always', no_unliteral=True)
def overload_series_idxmax(S, axis=0, skipna=True):
    jrezx__dexj = dict(axis=axis, skipna=skipna)
    adk__dtahn = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmax()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.CategoricalArrayType)) or S.
        data in [bodo.boolean_array, bodo.datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmax() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmax(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmax(arr, index)
    return impl


@overload_method(SeriesType, 'infer_objects', inline='always')
def overload_series_infer_objects(S):
    return lambda S: S.copy()


@overload_attribute(SeriesType, 'is_monotonic', inline='always')
@overload_attribute(SeriesType, 'is_monotonic_increasing', inline='always')
def overload_series_is_monotonic_increasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_increasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 1)


@overload_attribute(SeriesType, 'is_monotonic_decreasing', inline='always')
def overload_series_is_monotonic_decreasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_decreasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 2)


@overload_attribute(SeriesType, 'nbytes', inline='always')
def overload_series_nbytes(S):
    return lambda S: bodo.hiframes.pd_series_ext.get_series_data(S).nbytes


@overload_method(SeriesType, 'autocorr', inline='always', no_unliteral=True)
def overload_series_autocorr(S, lag=1):
    return lambda S, lag=1: bodo.libs.array_kernels.autocorr(bodo.hiframes.
        pd_series_ext.get_series_data(S), lag)


@overload_method(SeriesType, 'median', inline='always', no_unliteral=True)
def overload_series_median(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    jrezx__dexj = dict(level=level, numeric_only=numeric_only)
    adk__dtahn = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.median(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.median(): skipna argument must be a boolean')
    return (lambda S, axis=None, skipna=True, level=None, numeric_only=None:
        bodo.libs.array_ops.array_op_median(bodo.hiframes.pd_series_ext.
        get_series_data(S), skipna))


def overload_series_head(S, n=5):

    def impl(S, n=5):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        lazp__jgax = arr[:n]
        oppbw__tfv = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(lazp__jgax,
            oppbw__tfv, name)
    return impl


@lower_builtin('series.head', SeriesType, types.Integer)
@lower_builtin('series.head', SeriesType, types.Omitted)
def series_head_lower(context, builder, sig, args):
    impl = overload_series_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@numba.extending.register_jitable
def tail_slice(k, n):
    if n == 0:
        return k
    return -n


@overload_method(SeriesType, 'tail', inline='always', no_unliteral=True)
def overload_series_tail(S, n=5):
    if not is_overload_int(n):
        raise BodoError("Series.tail(): 'n' must be an Integer")

    def impl(S, n=5):
        xllm__xqb = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        lazp__jgax = arr[xllm__xqb:]
        oppbw__tfv = index[xllm__xqb:]
        return bodo.hiframes.pd_series_ext.init_series(lazp__jgax,
            oppbw__tfv, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    rftef__iwhy = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in rftef__iwhy:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            zfzfk__wqd = index[0]
            fbkzf__bxeg = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                zfzfk__wqd, False))
        else:
            fbkzf__bxeg = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        lazp__jgax = arr[:fbkzf__bxeg]
        oppbw__tfv = index[:fbkzf__bxeg]
        return bodo.hiframes.pd_series_ext.init_series(lazp__jgax,
            oppbw__tfv, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    rftef__iwhy = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in rftef__iwhy:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            qng__fxv = index[-1]
            fbkzf__bxeg = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset, qng__fxv,
                True))
        else:
            fbkzf__bxeg = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        lazp__jgax = arr[len(arr) - fbkzf__bxeg:]
        oppbw__tfv = index[len(arr) - fbkzf__bxeg:]
        return bodo.hiframes.pd_series_ext.init_series(lazp__jgax,
            oppbw__tfv, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        xjtg__xsxy = bodo.utils.conversion.index_to_array(index)
        ncivz__dvnvv, kpi__pbiex = (bodo.libs.array_kernels.
            first_last_valid_index(arr, xjtg__xsxy))
        return kpi__pbiex if ncivz__dvnvv else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        xjtg__xsxy = bodo.utils.conversion.index_to_array(index)
        ncivz__dvnvv, kpi__pbiex = (bodo.libs.array_kernels.
            first_last_valid_index(arr, xjtg__xsxy, False))
        return kpi__pbiex if ncivz__dvnvv else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    jrezx__dexj = dict(keep=keep)
    adk__dtahn = dict(keep='first')
    check_unsupported_args('Series.nlargest', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        xjtg__xsxy = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rkrju__svrna, atli__muh = bodo.libs.array_kernels.nlargest(arr,
            xjtg__xsxy, n, True, bodo.hiframes.series_kernels.gt_f)
        vnjey__vue = bodo.utils.conversion.convert_to_index(atli__muh)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
            vnjey__vue, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    jrezx__dexj = dict(keep=keep)
    adk__dtahn = dict(keep='first')
    check_unsupported_args('Series.nsmallest', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        xjtg__xsxy = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rkrju__svrna, atli__muh = bodo.libs.array_kernels.nlargest(arr,
            xjtg__xsxy, n, False, bodo.hiframes.series_kernels.lt_f)
        vnjey__vue = bodo.utils.conversion.convert_to_index(atli__muh)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
            vnjey__vue, name)
    return impl


@overload_method(SeriesType, 'notnull', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'notna', inline='always', no_unliteral=True)
def overload_series_notna(S):
    return lambda S: S.isna() == False


@overload_method(SeriesType, 'astype', inline='always', no_unliteral=True)
@overload_method(HeterogeneousSeriesType, 'astype', inline='always',
    no_unliteral=True)
def overload_series_astype(S, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    jrezx__dexj = dict(errors=errors)
    adk__dtahn = dict(errors='raise')
    check_unsupported_args('Series.astype', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "Series.astype(): 'dtype' when passed as string must be a constant value"
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.astype()')

    def impl(S, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rkrju__svrna = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    jrezx__dexj = dict(axis=axis, is_copy=is_copy)
    adk__dtahn = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        qjud__nya = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[qjud__nya],
            index[qjud__nya], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    jrezx__dexj = dict(axis=axis, kind=kind, order=order)
    adk__dtahn = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        lub__rxaw = S.notna().values
        if not lub__rxaw.all():
            rkrju__svrna = np.full(n, -1, np.int64)
            rkrju__svrna[lub__rxaw] = argsort(arr[lub__rxaw])
        else:
            rkrju__svrna = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    jrezx__dexj = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    adk__dtahn = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        tqh__xifdr = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        gsyg__dwnc = tqh__xifdr.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        rkrju__svrna = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            gsyg__dwnc, 0)
        vnjey__vue = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            gsyg__dwnc)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
            vnjey__vue, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    jrezx__dexj = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    adk__dtahn = dict(axis=0, inplace=False, kind='quicksort', ignore_index
        =False, key=None)
    check_unsupported_args('Series.sort_values', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        tqh__xifdr = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        gsyg__dwnc = tqh__xifdr.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        rkrju__svrna = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            gsyg__dwnc, 0)
        vnjey__vue = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            gsyg__dwnc)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
            vnjey__vue, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    yfr__sjtvc = is_overload_true(is_nullable)
    wvw__gcjfb = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    wvw__gcjfb += '  numba.parfors.parfor.init_prange()\n'
    wvw__gcjfb += '  n = len(arr)\n'
    if yfr__sjtvc:
        wvw__gcjfb += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        wvw__gcjfb += '  out_arr = np.empty(n, np.int64)\n'
    wvw__gcjfb += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    wvw__gcjfb += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if yfr__sjtvc:
        wvw__gcjfb += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        wvw__gcjfb += '      out_arr[i] = -1\n'
    wvw__gcjfb += '      continue\n'
    wvw__gcjfb += '    val = arr[i]\n'
    wvw__gcjfb += '    if include_lowest and val == bins[0]:\n'
    wvw__gcjfb += '      ind = 1\n'
    wvw__gcjfb += '    else:\n'
    wvw__gcjfb += '      ind = np.searchsorted(bins, val)\n'
    wvw__gcjfb += '    if ind == 0 or ind == len(bins):\n'
    if yfr__sjtvc:
        wvw__gcjfb += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        wvw__gcjfb += '      out_arr[i] = -1\n'
    wvw__gcjfb += '    else:\n'
    wvw__gcjfb += '      out_arr[i] = ind - 1\n'
    wvw__gcjfb += '  return out_arr\n'
    huc__cuo = {}
    exec(wvw__gcjfb, {'bodo': bodo, 'np': np, 'numba': numba}, huc__cuo)
    impl = huc__cuo['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        adi__rpiu, urlm__spge = np.divmod(x, 1)
        if adi__rpiu == 0:
            ornxf__eksyf = -int(np.floor(np.log10(abs(urlm__spge)))
                ) - 1 + precision
        else:
            ornxf__eksyf = precision
        return np.around(x, ornxf__eksyf)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        bgm__ofzau = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(bgm__ofzau)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        cakuz__gahqw = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            hca__cbzzl = bins.copy()
            if right and include_lowest:
                hca__cbzzl[0] = hca__cbzzl[0] - cakuz__gahqw
            blv__ljps = bodo.libs.interval_arr_ext.init_interval_array(
                hca__cbzzl[:-1], hca__cbzzl[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(blv__ljps,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        hca__cbzzl = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            hca__cbzzl[0] = hca__cbzzl[0] - 10.0 ** -precision
        blv__ljps = bodo.libs.interval_arr_ext.init_interval_array(hca__cbzzl
            [:-1], hca__cbzzl[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(blv__ljps, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        zhz__khzv = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        aehng__asjd = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        rkrju__svrna = np.zeros(nbins, np.int64)
        for vov__ggess in range(len(zhz__khzv)):
            rkrju__svrna[aehng__asjd[vov__ggess]] = zhz__khzv[vov__ggess]
        return rkrju__svrna
    return impl


def compute_bins(nbins, min_val, max_val):
    pass


@overload(compute_bins, no_unliteral=True)
def overload_compute_bins(nbins, min_val, max_val, right=True):

    def impl(nbins, min_val, max_val, right=True):
        if nbins < 1:
            raise ValueError('`bins` should be a positive integer.')
        min_val = min_val + 0.0
        max_val = max_val + 0.0
        if np.isinf(min_val) or np.isinf(max_val):
            raise ValueError(
                'cannot specify integer `bins` when input data contains infinity'
                )
        elif min_val == max_val:
            min_val -= 0.001 * abs(min_val) if min_val != 0 else 0.001
            max_val += 0.001 * abs(max_val) if max_val != 0 else 0.001
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
        else:
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
            dchkf__shy = (max_val - min_val) * 0.001
            if right:
                bins[0] -= dchkf__shy
            else:
                bins[-1] += dchkf__shy
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    jrezx__dexj = dict(dropna=dropna)
    adk__dtahn = dict(dropna=True)
    check_unsupported_args('Series.value_counts', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            'Series.value_counts(): normalize argument must be a constant boolean'
            )
    if not is_overload_constant_bool(sort):
        raise_bodo_error(
            'Series.value_counts(): sort argument must be a constant boolean')
    if not is_overload_bool(ascending):
        raise_bodo_error(
            'Series.value_counts(): ascending argument must be a constant boolean'
            )
    thoe__yeky = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    wvw__gcjfb = 'def impl(\n'
    wvw__gcjfb += '    S,\n'
    wvw__gcjfb += '    normalize=False,\n'
    wvw__gcjfb += '    sort=True,\n'
    wvw__gcjfb += '    ascending=False,\n'
    wvw__gcjfb += '    bins=None,\n'
    wvw__gcjfb += '    dropna=True,\n'
    wvw__gcjfb += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    wvw__gcjfb += '):\n'
    wvw__gcjfb += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    wvw__gcjfb += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    wvw__gcjfb += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    if thoe__yeky:
        wvw__gcjfb += '    right = True\n'
        wvw__gcjfb += _gen_bins_handling(bins, S.dtype)
        wvw__gcjfb += '    arr = get_bin_inds(bins, arr)\n'
    wvw__gcjfb += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    wvw__gcjfb += "        (arr,), index, ('$_bodo_col2_',)\n"
    wvw__gcjfb += '    )\n'
    wvw__gcjfb += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if thoe__yeky:
        wvw__gcjfb += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        wvw__gcjfb += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        wvw__gcjfb += '    index = get_bin_labels(bins)\n'
    else:
        wvw__gcjfb += (
            '    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)\n'
            )
        wvw__gcjfb += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        wvw__gcjfb += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        wvw__gcjfb += '    )\n'
        wvw__gcjfb += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    wvw__gcjfb += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        wvw__gcjfb += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        tlo__rvgw = 'len(S)' if thoe__yeky else 'count_arr.sum()'
        wvw__gcjfb += f'    res = res / float({tlo__rvgw})\n'
    wvw__gcjfb += '    return res\n'
    huc__cuo = {}
    exec(wvw__gcjfb, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, huc__cuo)
    impl = huc__cuo['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    wvw__gcjfb = ''
    if isinstance(bins, types.Integer):
        wvw__gcjfb += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        wvw__gcjfb += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            wvw__gcjfb += '    min_val = min_val.value\n'
            wvw__gcjfb += '    max_val = max_val.value\n'
        wvw__gcjfb += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            wvw__gcjfb += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        wvw__gcjfb += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return wvw__gcjfb


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    jrezx__dexj = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    adk__dtahn = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    wvw__gcjfb = 'def impl(\n'
    wvw__gcjfb += '    x,\n'
    wvw__gcjfb += '    bins,\n'
    wvw__gcjfb += '    right=True,\n'
    wvw__gcjfb += '    labels=None,\n'
    wvw__gcjfb += '    retbins=False,\n'
    wvw__gcjfb += '    precision=3,\n'
    wvw__gcjfb += '    include_lowest=False,\n'
    wvw__gcjfb += "    duplicates='raise',\n"
    wvw__gcjfb += '    ordered=True\n'
    wvw__gcjfb += '):\n'
    if isinstance(x, SeriesType):
        wvw__gcjfb += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        wvw__gcjfb += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        wvw__gcjfb += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        wvw__gcjfb += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    wvw__gcjfb += _gen_bins_handling(bins, x.dtype)
    wvw__gcjfb += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    wvw__gcjfb += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    wvw__gcjfb += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    wvw__gcjfb += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        wvw__gcjfb += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        wvw__gcjfb += '    return res\n'
    else:
        wvw__gcjfb += '    return out_arr\n'
    huc__cuo = {}
    exec(wvw__gcjfb, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, huc__cuo)
    impl = huc__cuo['impl']
    return impl


def _get_q_list(q):
    return q


@overload(_get_q_list, no_unliteral=True)
def get_q_list_overload(q):
    if is_overload_int(q):
        return lambda q: np.linspace(0, 1, q + 1)
    return lambda q: q


@overload(pd.unique, inline='always', no_unliteral=True)
def overload_unique(values):
    if not is_series_type(values) and not (bodo.utils.utils.is_array_typ(
        values, False) and values.ndim == 1):
        raise BodoError(
            "pd.unique(): 'values' must be either a Series or a 1-d array")
    if is_series_type(values):

        def impl(values):
            arr = bodo.hiframes.pd_series_ext.get_series_data(values)
            return bodo.allgatherv(bodo.libs.array_kernels.unique(arr), False)
        return impl
    else:
        return lambda values: bodo.allgatherv(bodo.libs.array_kernels.
            unique(values), False)


@overload(pd.qcut, inline='always', no_unliteral=True)
def overload_qcut(x, q, labels=None, retbins=False, precision=3, duplicates
    ='raise'):
    jrezx__dexj = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    adk__dtahn = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        omjw__jcx = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, omjw__jcx)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    jrezx__dexj = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze
        =squeeze, observed=observed, dropna=dropna)
    adk__dtahn = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='GroupBy')
    if not is_overload_true(as_index):
        raise BodoError('as_index=False only valid with DataFrame')
    if is_overload_none(by) and is_overload_none(level):
        raise BodoError("You have to supply one of 'by' and 'level'")
    if not is_overload_none(by) and not is_overload_none(level):
        raise BodoError(
            "Series.groupby(): 'level' argument should be None if 'by' is not None"
            )
    if not is_overload_none(level):
        if not (is_overload_constant_int(level) and get_overload_const_int(
            level) == 0) or isinstance(S.index, bodo.hiframes.
            pd_multi_index_ext.MultiIndexType):
            raise BodoError(
                "Series.groupby(): MultiIndex case or 'level' other than 0 not supported yet"
                )

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            bkngv__qqzgy = bodo.utils.conversion.coerce_to_array(index)
            tqh__xifdr = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                bkngv__qqzgy, arr), index, (' ', ''))
            return tqh__xifdr.groupby(' ')['']
        return impl_index
    ghrc__umqm = by
    if isinstance(by, SeriesType):
        ghrc__umqm = by.data
    if isinstance(ghrc__umqm, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        bkngv__qqzgy = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        tqh__xifdr = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            bkngv__qqzgy, arr), index, (' ', ''))
        return tqh__xifdr.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    jrezx__dexj = dict(verify_integrity=verify_integrity)
    adk__dtahn = dict(verify_integrity=False)
    check_unsupported_args('Series.append', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_append,
        'Series.append()')
    if isinstance(to_append, SeriesType):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S, to_append), ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    if isinstance(to_append, types.BaseTuple):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S,) + to_append, ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    return (lambda S, to_append, ignore_index=False, verify_integrity=False:
        pd.concat([S] + to_append, ignore_index=ignore_index,
        verify_integrity=verify_integrity))


@overload_method(SeriesType, 'isin', inline='always', no_unliteral=True)
def overload_series_isin(S, values):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.isin()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(values,
        'Series.isin()')
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(S, values):
            zhb__bxlwt = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            rkrju__svrna = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(rkrju__svrna, A, zhb__bxlwt, False)
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rkrju__svrna = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    jrezx__dexj = dict(interpolation=interpolation)
    adk__dtahn = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            rkrju__svrna = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                index, name)
        return impl_list
    elif isinstance(q, (float, types.Number)) or is_overload_constant_int(q):

        def impl(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return bodo.libs.array_ops.array_op_quantile(arr, q)
        return impl
    else:
        raise BodoError(
            f'Series.quantile() q type must be float or iterable of floats only.'
            )


@overload_method(SeriesType, 'nunique', inline='always', no_unliteral=True)
def overload_series_nunique(S, dropna=True):
    if not is_overload_bool(dropna):
        raise BodoError('Series.nunique: dropna must be a boolean value')

    def impl(S, dropna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_kernels.nunique(arr, dropna)
    return impl


@overload_method(SeriesType, 'unique', inline='always', no_unliteral=True)
def overload_series_unique(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        ekex__ubh = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(ekex__ubh, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    jrezx__dexj = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    adk__dtahn = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.describe()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)
        ) and not isinstance(S.data, IntegerArrayType):
        raise BodoError(f'describe() column input type {S.data} not supported.'
            )
    if S.data.dtype == bodo.datetime64ns:

        def impl_dt(S, percentiles=None, include=None, exclude=None,
            datetime_is_numeric=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
                array_ops.array_op_describe(arr), bodo.utils.conversion.
                convert_to_index(['count', 'mean', 'min', '25%', '50%',
                '75%', 'max']), name)
        return impl_dt

    def impl(S, percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.array_ops.
            array_op_describe(arr), bodo.utils.conversion.convert_to_index(
            ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']), name)
    return impl


@overload_method(SeriesType, 'memory_usage', inline='always', no_unliteral=True
    )
def overload_series_memory_usage(S, index=True, deep=False):
    if is_overload_true(index):

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            return arr.nbytes + index.nbytes
        return impl
    else:

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return arr.nbytes
        return impl


def binary_str_fillna_inplace_series_impl(is_binary=False):
    if is_binary:
        jsu__sphrd = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        jsu__sphrd = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    wvw__gcjfb = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {jsu__sphrd}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    hhfl__qzsq = dict()
    exec(wvw__gcjfb, {'bodo': bodo, 'numba': numba}, hhfl__qzsq)
    uiwkz__zjky = hhfl__qzsq['impl']
    return uiwkz__zjky


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        jsu__sphrd = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        jsu__sphrd = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    wvw__gcjfb = 'def impl(S,\n'
    wvw__gcjfb += '     value=None,\n'
    wvw__gcjfb += '    method=None,\n'
    wvw__gcjfb += '    axis=None,\n'
    wvw__gcjfb += '    inplace=False,\n'
    wvw__gcjfb += '    limit=None,\n'
    wvw__gcjfb += '   downcast=None,\n'
    wvw__gcjfb += '):\n'
    wvw__gcjfb += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    wvw__gcjfb += '    n = len(in_arr)\n'
    wvw__gcjfb += f'    out_arr = {jsu__sphrd}(n, -1)\n'
    wvw__gcjfb += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    wvw__gcjfb += '        s = in_arr[j]\n'
    wvw__gcjfb += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    wvw__gcjfb += '            s = value\n'
    wvw__gcjfb += '        out_arr[j] = s\n'
    wvw__gcjfb += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    hhfl__qzsq = dict()
    exec(wvw__gcjfb, {'bodo': bodo, 'numba': numba}, hhfl__qzsq)
    uiwkz__zjky = hhfl__qzsq['impl']
    return uiwkz__zjky


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
    mdzqg__xsr = bodo.hiframes.pd_series_ext.get_series_data(value)
    for vov__ggess in numba.parfors.parfor.internal_prange(len(zso__gglp)):
        s = zso__gglp[vov__ggess]
        if bodo.libs.array_kernels.isna(zso__gglp, vov__ggess
            ) and not bodo.libs.array_kernels.isna(mdzqg__xsr, vov__ggess):
            s = mdzqg__xsr[vov__ggess]
        zso__gglp[vov__ggess] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
    for vov__ggess in numba.parfors.parfor.internal_prange(len(zso__gglp)):
        s = zso__gglp[vov__ggess]
        if bodo.libs.array_kernels.isna(zso__gglp, vov__ggess):
            s = value
        zso__gglp[vov__ggess] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    mdzqg__xsr = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(zso__gglp)
    rkrju__svrna = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for dxom__dkut in numba.parfors.parfor.internal_prange(n):
        s = zso__gglp[dxom__dkut]
        if bodo.libs.array_kernels.isna(zso__gglp, dxom__dkut
            ) and not bodo.libs.array_kernels.isna(mdzqg__xsr, dxom__dkut):
            s = mdzqg__xsr[dxom__dkut]
        rkrju__svrna[dxom__dkut] = s
        if bodo.libs.array_kernels.isna(zso__gglp, dxom__dkut
            ) and bodo.libs.array_kernels.isna(mdzqg__xsr, dxom__dkut):
            bodo.libs.array_kernels.setna(rkrju__svrna, dxom__dkut)
    return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    mdzqg__xsr = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(zso__gglp)
    rkrju__svrna = bodo.utils.utils.alloc_type(n, zso__gglp.dtype, (-1,))
    for vov__ggess in numba.parfors.parfor.internal_prange(n):
        s = zso__gglp[vov__ggess]
        if bodo.libs.array_kernels.isna(zso__gglp, vov__ggess
            ) and not bodo.libs.array_kernels.isna(mdzqg__xsr, vov__ggess):
            s = mdzqg__xsr[vov__ggess]
        rkrju__svrna[vov__ggess] = s
    return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    jrezx__dexj = dict(limit=limit, downcast=downcast)
    adk__dtahn = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    sidmi__xdbtu = not is_overload_none(value)
    rnhob__aoi = not is_overload_none(method)
    if sidmi__xdbtu and rnhob__aoi:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not sidmi__xdbtu and not rnhob__aoi:
        raise BodoError(
            "Series.fillna(): Must specify one of 'value' and 'method'.")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.fillna(): axis argument not supported')
    elif is_iterable_type(value) and not isinstance(value, SeriesType):
        raise BodoError('Series.fillna(): "value" parameter cannot be a list')
    elif is_var_size_item_array_type(S.data
        ) and not S.dtype == bodo.string_type:
        raise BodoError(
            f'Series.fillna() with inplace=True not supported for {S.dtype} values yet.'
            )
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "Series.fillna(): 'inplace' argument must be a constant boolean")
    if rnhob__aoi:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        efnu__lwxwu = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(efnu__lwxwu)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(efnu__lwxwu)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    wqa__zcnd = element_type(S.data)
    jfru__hna = None
    if sidmi__xdbtu:
        jfru__hna = element_type(types.unliteral(value))
    if jfru__hna and not can_replace(wqa__zcnd, jfru__hna):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {jfru__hna} with series type {wqa__zcnd}'
            )
    if is_overload_true(inplace):
        if S.dtype == bodo.string_type:
            if S.data == bodo.dict_str_arr_type:
                raise_bodo_error(
                    "Series.fillna(): 'inplace' not supported for dictionary-encoded string arrays yet."
                    )
            if is_overload_constant_str(value) and get_overload_const_str(value
                ) == '':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=False)
            return binary_str_fillna_inplace_impl(is_binary=False)
        if S.dtype == bodo.bytes_type:
            if is_overload_constant_bytes(value) and get_overload_const_bytes(
                value) == b'':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=True)
            return binary_str_fillna_inplace_impl(is_binary=True)
        else:
            if isinstance(value, SeriesType):
                return fillna_inplace_series_impl
            return fillna_inplace_impl
    else:
        ythg__dmvm = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                mdzqg__xsr = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(zso__gglp)
                rkrju__svrna = bodo.utils.utils.alloc_type(n, ythg__dmvm, (-1,)
                    )
                for vov__ggess in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(zso__gglp, vov__ggess
                        ) and bodo.libs.array_kernels.isna(mdzqg__xsr,
                        vov__ggess):
                        bodo.libs.array_kernels.setna(rkrju__svrna, vov__ggess)
                        continue
                    if bodo.libs.array_kernels.isna(zso__gglp, vov__ggess):
                        rkrju__svrna[vov__ggess
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            mdzqg__xsr[vov__ggess])
                        continue
                    rkrju__svrna[vov__ggess
                        ] = bodo.utils.conversion.unbox_if_timestamp(zso__gglp
                        [vov__ggess])
                return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                    index, name)
            return fillna_series_impl
        if rnhob__aoi:
            hnlw__wiw = (types.unicode_type, types.bool_, bodo.datetime64ns,
                bodo.timedelta64ns)
            if not isinstance(wqa__zcnd, (types.Integer, types.Float)
                ) and wqa__zcnd not in hnlw__wiw:
                raise BodoError(
                    f"Series.fillna(): series of type {wqa__zcnd} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                rkrju__svrna = bodo.libs.array_kernels.ffill_bfill_arr(
                    zso__gglp, method)
                return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(zso__gglp)
            rkrju__svrna = bodo.utils.utils.alloc_type(n, ythg__dmvm, (-1,))
            for vov__ggess in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(zso__gglp[
                    vov__ggess])
                if bodo.libs.array_kernels.isna(zso__gglp, vov__ggess):
                    s = value
                rkrju__svrna[vov__ggess] = s
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        ddlvx__mdz = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        jrezx__dexj = dict(limit=limit, downcast=downcast)
        adk__dtahn = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', jrezx__dexj,
            adk__dtahn, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        wqa__zcnd = element_type(S.data)
        hnlw__wiw = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(wqa__zcnd, (types.Integer, types.Float)
            ) and wqa__zcnd not in hnlw__wiw:
            raise BodoError(
                f'Series.{overload_name}(): series of type {wqa__zcnd} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rkrju__svrna = bodo.libs.array_kernels.ffill_bfill_arr(zso__gglp,
                ddlvx__mdz)
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        gzrap__rqrhm = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            gzrap__rqrhm)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        zttz__kxm = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(zttz__kxm)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        zttz__kxm = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(zttz__kxm)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        zttz__kxm = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(zttz__kxm)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    jrezx__dexj = dict(inplace=inplace, limit=limit, regex=regex, method=method
        )
    sien__vpms = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', jrezx__dexj, sien__vpms,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    wqa__zcnd = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        aug__qgn = element_type(to_replace.key_type)
        jfru__hna = element_type(to_replace.value_type)
    else:
        aug__qgn = element_type(to_replace)
        jfru__hna = element_type(value)
    alxa__coh = None
    if wqa__zcnd != types.unliteral(aug__qgn):
        if bodo.utils.typing.equality_always_false(wqa__zcnd, types.
            unliteral(aug__qgn)
            ) or not bodo.utils.typing.types_equality_exists(wqa__zcnd,
            aug__qgn):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(wqa__zcnd, (types.Float, types.Integer)
            ) or wqa__zcnd == np.bool_:
            alxa__coh = wqa__zcnd
    if not can_replace(wqa__zcnd, types.unliteral(jfru__hna)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    ueu__qya = to_str_arr_if_dict_array(S.data)
    if isinstance(ueu__qya, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(zso__gglp.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(zso__gglp)
        rkrju__svrna = bodo.utils.utils.alloc_type(n, ueu__qya, (-1,))
        dnqd__jljga = build_replace_dict(to_replace, value, alxa__coh)
        for vov__ggess in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(zso__gglp, vov__ggess):
                bodo.libs.array_kernels.setna(rkrju__svrna, vov__ggess)
                continue
            s = zso__gglp[vov__ggess]
            if s in dnqd__jljga:
                s = dnqd__jljga[s]
            rkrju__svrna[vov__ggess] = s
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    logng__ybj = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    nfwm__gupq = is_iterable_type(to_replace)
    fby__qnue = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    qlu__kdx = is_iterable_type(value)
    if logng__ybj and fby__qnue:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                dnqd__jljga = {}
                dnqd__jljga[key_dtype_conv(to_replace)] = value
                return dnqd__jljga
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            dnqd__jljga = {}
            dnqd__jljga[to_replace] = value
            return dnqd__jljga
        return impl
    if nfwm__gupq and fby__qnue:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                dnqd__jljga = {}
                for xgbb__dnp in to_replace:
                    dnqd__jljga[key_dtype_conv(xgbb__dnp)] = value
                return dnqd__jljga
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            dnqd__jljga = {}
            for xgbb__dnp in to_replace:
                dnqd__jljga[xgbb__dnp] = value
            return dnqd__jljga
        return impl
    if nfwm__gupq and qlu__kdx:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                dnqd__jljga = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for vov__ggess in range(len(to_replace)):
                    dnqd__jljga[key_dtype_conv(to_replace[vov__ggess])
                        ] = value[vov__ggess]
                return dnqd__jljga
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            dnqd__jljga = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for vov__ggess in range(len(to_replace)):
                dnqd__jljga[to_replace[vov__ggess]] = value[vov__ggess]
            return dnqd__jljga
        return impl
    if isinstance(to_replace, numba.types.DictType) and is_overload_none(value
        ):
        return lambda to_replace, value, key_dtype_conv: to_replace
    raise BodoError(
        'Series.replace(): Not supported for types to_replace={} and value={}'
        .format(to_replace, value))


@overload_method(SeriesType, 'diff', inline='always', no_unliteral=True)
def overload_series_diff(S, periods=1):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.diff()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)):
        raise BodoError(
            f'Series.diff() column input type {S.data} not supported.')
    if not is_overload_int(periods):
        raise BodoError("Series.diff(): 'periods' input must be an integer.")
    if S.data == types.Array(bodo.datetime64ns, 1, 'C'):

        def impl_datetime(S, periods=1):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            rkrju__svrna = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo
                .hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rkrju__svrna = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    jrezx__dexj = dict(ignore_index=ignore_index)
    ori__bvk = dict(ignore_index=False)
    check_unsupported_args('Series.explode', jrezx__dexj, ori__bvk,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xjtg__xsxy = bodo.utils.conversion.index_to_array(index)
        rkrju__svrna, naq__eexm = bodo.libs.array_kernels.explode(arr,
            xjtg__xsxy)
        vnjey__vue = bodo.utils.conversion.index_from_array(naq__eexm)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
            vnjey__vue, name)
    return impl


@overload(np.digitize, inline='always', no_unliteral=True)
def overload_series_np_digitize(x, bins, right=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.digitize()')
    if isinstance(x, SeriesType):

        def impl(x, bins, right=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(x)
            return np.digitize(arr, bins, right)
        return impl


@overload(np.argmax, inline='always', no_unliteral=True)
def argmax_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            tbss__ytczr = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for vov__ggess in numba.parfors.parfor.internal_prange(n):
                tbss__ytczr[vov__ggess] = np.argmax(a[vov__ggess])
            return tbss__ytczr
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            zoyne__sxsj = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for vov__ggess in numba.parfors.parfor.internal_prange(n):
                zoyne__sxsj[vov__ggess] = np.argmin(a[vov__ggess])
            return zoyne__sxsj
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(a)
            return np.dot(arr, b)
        return impl
    if isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(b)
            return np.dot(a, arr)
        return impl


overload(np.dot, inline='always', no_unliteral=True)(overload_series_np_dot)
overload(operator.matmul, inline='always', no_unliteral=True)(
    overload_series_np_dot)


@overload_method(SeriesType, 'dropna', inline='always', no_unliteral=True)
def overload_series_dropna(S, axis=0, inplace=False, how=None):
    jrezx__dexj = dict(axis=axis, inplace=inplace, how=how)
    qmx__hxxs = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', jrezx__dexj, qmx__hxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            lub__rxaw = S.notna().values
            xjtg__xsxy = bodo.utils.conversion.extract_index_array(S)
            vnjey__vue = bodo.utils.conversion.convert_to_index(xjtg__xsxy[
                lub__rxaw])
            rkrju__svrna = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(zso__gglp))
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                vnjey__vue, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            xjtg__xsxy = bodo.utils.conversion.extract_index_array(S)
            lub__rxaw = S.notna().values
            vnjey__vue = bodo.utils.conversion.convert_to_index(xjtg__xsxy[
                lub__rxaw])
            rkrju__svrna = zso__gglp[lub__rxaw]
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                vnjey__vue, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    jrezx__dexj = dict(freq=freq, axis=axis, fill_value=fill_value)
    adk__dtahn = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.shift()')
    if not is_supported_shift_array_type(S.data):
        raise BodoError(
            f"Series.shift(): Series input type '{S.data.dtype}' not supported yet."
            )
    if not is_overload_int(periods):
        raise BodoError("Series.shift(): 'periods' input must be an integer.")

    def impl(S, periods=1, freq=None, axis=0, fill_value=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rkrju__svrna = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    jrezx__dexj = dict(fill_method=fill_method, limit=limit, freq=freq)
    adk__dtahn = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not is_overload_int(periods):
        raise BodoError(
            'Series.pct_change(): periods argument must be an Integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.pct_change()')

    def impl(S, periods=1, fill_method='pad', limit=None, freq=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rkrju__svrna = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


def create_series_mask_where_overload(func_name):

    def overload_series_mask_where(S, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
            f'Series.{func_name}()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
            f'Series.{func_name}()')
        _validate_arguments_mask_where(f'Series.{func_name}', S, cond,
            other, inplace, axis, level, errors, try_cast)
        if is_overload_constant_nan(other):
            tmnq__eia = 'None'
        else:
            tmnq__eia = 'other'
        wvw__gcjfb = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            wvw__gcjfb += '  cond = ~cond\n'
        wvw__gcjfb += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        wvw__gcjfb += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        wvw__gcjfb += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        wvw__gcjfb += (
            f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {tmnq__eia})\n'
            )
        wvw__gcjfb += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        huc__cuo = {}
        exec(wvw__gcjfb, {'bodo': bodo, 'np': np}, huc__cuo)
        impl = huc__cuo['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        gzrap__rqrhm = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(gzrap__rqrhm)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    jrezx__dexj = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    adk__dtahn = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if isinstance(other, SeriesType):
        _validate_self_other_mask_where(func_name, S.data, other.data)
    else:
        _validate_self_other_mask_where(func_name, S.data, other)
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        cond.ndim == 1 and cond.dtype == types.bool_):
        raise BodoError(
            f"{func_name}() 'cond' argument must be a Series or 1-dim array of booleans"
            )


def _validate_self_other_mask_where(func_name, arr, other, max_ndim=1,
    is_default=False):
    if not (isinstance(arr, types.Array) or isinstance(arr,
        BooleanArrayType) or isinstance(arr, IntegerArrayType) or bodo.
        utils.utils.is_array_typ(arr, False) and arr.dtype in [bodo.
        string_type, bodo.bytes_type] or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type not in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.pd_timestamp_type, bodo.
        pd_timedelta_type]):
        raise BodoError(
            f'{func_name}() Series data with type {arr} not yet supported')
    ovhk__qwkc = is_overload_constant_nan(other)
    if not (is_default or ovhk__qwkc or is_scalar_type(other) or isinstance
        (other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
        isinstance(other, SeriesType) and (isinstance(arr, types.Array) or 
        arr.dtype in [bodo.string_type, bodo.bytes_type]) or 
        is_str_arr_type(other) and (arr.dtype == bodo.string_type or 
        isinstance(arr, bodo.CategoricalArrayType) and arr.dtype.elem_type ==
        bodo.string_type) or isinstance(other, BinaryArrayType) and (arr.
        dtype == bodo.bytes_type or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type == bodo.bytes_type) or
        (not (isinstance(other, (StringArrayType, BinaryArrayType)) or 
        other == bodo.dict_str_arr_type) and (isinstance(arr.dtype, types.
        Integer) and (bodo.utils.utils.is_array_typ(other) and isinstance(
        other.dtype, types.Integer) or is_series_type(other) and isinstance
        (other.dtype, types.Integer))) or (bodo.utils.utils.is_array_typ(
        other) and arr.dtype == other.dtype or is_series_type(other) and 
        arr.dtype == other.dtype)) and (isinstance(arr, BooleanArrayType) or
        isinstance(arr, IntegerArrayType))):
        raise BodoError(
            f"{func_name}() 'other' must be a scalar, non-categorical series, 1-dim numpy array or StringArray with a matching type for Series."
            )
    if not is_default:
        if isinstance(arr.dtype, bodo.PDCategoricalDtype):
            fnio__fomr = arr.dtype.elem_type
        else:
            fnio__fomr = arr.dtype
        if is_iterable_type(other):
            bimn__cfpn = other.dtype
        elif ovhk__qwkc:
            bimn__cfpn = types.float64
        else:
            bimn__cfpn = types.unliteral(other)
        if not ovhk__qwkc and not is_common_scalar_dtype([fnio__fomr,
            bimn__cfpn]):
            raise BodoError(
                f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        jrezx__dexj = dict(level=level, axis=axis)
        adk__dtahn = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), jrezx__dexj,
            adk__dtahn, package_name='pandas', module_name='Series')
        whor__rcfhs = other == string_type or is_overload_constant_str(other)
        tpok__jpo = is_iterable_type(other) and other.dtype == string_type
        jnvmo__edfy = S.dtype == string_type and (op == operator.add and (
            whor__rcfhs or tpok__jpo) or op == operator.mul and isinstance(
            other, types.Integer))
        tgob__hai = S.dtype == bodo.timedelta64ns
        gtkv__qtubh = S.dtype == bodo.datetime64ns
        uvm__obwaj = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        ucl__pnm = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        hsm__kayzf = tgob__hai and (uvm__obwaj or ucl__pnm
            ) or gtkv__qtubh and uvm__obwaj
        hsm__kayzf = hsm__kayzf and op == operator.add
        if not (isinstance(S.dtype, types.Number) or jnvmo__edfy or hsm__kayzf
            ):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        uqg__iqk = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            ueu__qya = uqg__iqk.resolve_function_type(op, args, {}).return_type
            if isinstance(S.data, IntegerArrayType
                ) and ueu__qya == types.Array(types.bool_, 1, 'C'):
                ueu__qya = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                rkrju__svrna = bodo.utils.utils.alloc_type(n, ueu__qya, (-1,))
                for vov__ggess in numba.parfors.parfor.internal_prange(n):
                    dqc__vegld = bodo.libs.array_kernels.isna(arr, vov__ggess)
                    if dqc__vegld:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(rkrju__svrna,
                                vov__ggess)
                        else:
                            rkrju__svrna[vov__ggess] = op(fill_value, other)
                    else:
                        rkrju__svrna[vov__ggess] = op(arr[vov__ggess], other)
                return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        ueu__qya = uqg__iqk.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and ueu__qya == types.Array(
            types.bool_, 1, 'C'):
            ueu__qya = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            kvmq__qyi = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            rkrju__svrna = bodo.utils.utils.alloc_type(n, ueu__qya, (-1,))
            for vov__ggess in numba.parfors.parfor.internal_prange(n):
                dqc__vegld = bodo.libs.array_kernels.isna(arr, vov__ggess)
                emfm__rtms = bodo.libs.array_kernels.isna(kvmq__qyi, vov__ggess
                    )
                if dqc__vegld and emfm__rtms:
                    bodo.libs.array_kernels.setna(rkrju__svrna, vov__ggess)
                elif dqc__vegld:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(rkrju__svrna, vov__ggess)
                    else:
                        rkrju__svrna[vov__ggess] = op(fill_value, kvmq__qyi
                            [vov__ggess])
                elif emfm__rtms:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(rkrju__svrna, vov__ggess)
                    else:
                        rkrju__svrna[vov__ggess] = op(arr[vov__ggess],
                            fill_value)
                else:
                    rkrju__svrna[vov__ggess] = op(arr[vov__ggess],
                        kvmq__qyi[vov__ggess])
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                index, name)
        return impl
    return overload_series_explicit_binary_op


def create_explicit_binary_reverse_op_overload(op):

    def overload_series_explicit_binary_reverse_op(S, other, level=None,
        fill_value=None, axis=0):
        if not is_overload_none(level):
            raise BodoError('level argument not supported')
        if not is_overload_zero(axis):
            raise BodoError('axis argument not supported')
        if not isinstance(S.dtype, types.Number):
            raise BodoError('only numeric values supported')
        uqg__iqk = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            ueu__qya = uqg__iqk.resolve_function_type(op, args, {}).return_type
            if isinstance(S.data, IntegerArrayType
                ) and ueu__qya == types.Array(types.bool_, 1, 'C'):
                ueu__qya = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                rkrju__svrna = bodo.utils.utils.alloc_type(n, ueu__qya, None)
                for vov__ggess in numba.parfors.parfor.internal_prange(n):
                    dqc__vegld = bodo.libs.array_kernels.isna(arr, vov__ggess)
                    if dqc__vegld:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(rkrju__svrna,
                                vov__ggess)
                        else:
                            rkrju__svrna[vov__ggess] = op(other, fill_value)
                    else:
                        rkrju__svrna[vov__ggess] = op(other, arr[vov__ggess])
                return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        ueu__qya = uqg__iqk.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and ueu__qya == types.Array(
            types.bool_, 1, 'C'):
            ueu__qya = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            kvmq__qyi = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            rkrju__svrna = bodo.utils.utils.alloc_type(n, ueu__qya, None)
            for vov__ggess in numba.parfors.parfor.internal_prange(n):
                dqc__vegld = bodo.libs.array_kernels.isna(arr, vov__ggess)
                emfm__rtms = bodo.libs.array_kernels.isna(kvmq__qyi, vov__ggess
                    )
                rkrju__svrna[vov__ggess] = op(kvmq__qyi[vov__ggess], arr[
                    vov__ggess])
                if dqc__vegld and emfm__rtms:
                    bodo.libs.array_kernels.setna(rkrju__svrna, vov__ggess)
                elif dqc__vegld:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(rkrju__svrna, vov__ggess)
                    else:
                        rkrju__svrna[vov__ggess] = op(kvmq__qyi[vov__ggess],
                            fill_value)
                elif emfm__rtms:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(rkrju__svrna, vov__ggess)
                    else:
                        rkrju__svrna[vov__ggess] = op(fill_value, arr[
                            vov__ggess])
                else:
                    rkrju__svrna[vov__ggess] = op(kvmq__qyi[vov__ggess],
                        arr[vov__ggess])
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                index, name)
        return impl
    return overload_series_explicit_binary_reverse_op


explicit_binop_funcs_two_ways = {operator.add: {'add'}, operator.sub: {
    'sub'}, operator.mul: {'mul'}, operator.truediv: {'div', 'truediv'},
    operator.floordiv: {'floordiv'}, operator.mod: {'mod'}, operator.pow: {
    'pow'}}
explicit_binop_funcs_single = {operator.lt: 'lt', operator.gt: 'gt',
    operator.le: 'le', operator.ge: 'ge', operator.ne: 'ne', operator.eq: 'eq'}
explicit_binop_funcs = set()
split_logical_binops_funcs = [operator.or_, operator.and_]


def _install_explicit_binary_ops():
    for op, hep__ovjg in explicit_binop_funcs_two_ways.items():
        for name in hep__ovjg:
            gzrap__rqrhm = create_explicit_binary_op_overload(op)
            aefym__vryao = create_explicit_binary_reverse_op_overload(op)
            wci__xsqbr = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(gzrap__rqrhm)
            overload_method(SeriesType, wci__xsqbr, no_unliteral=True)(
                aefym__vryao)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        gzrap__rqrhm = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(gzrap__rqrhm)
        explicit_binop_funcs.add(name)


_install_explicit_binary_ops()


def create_binary_op_overload(op):

    def overload_series_binary_op(lhs, rhs):
        if (isinstance(lhs, SeriesType) and isinstance(rhs, SeriesType) and
            lhs.dtype == bodo.datetime64ns and rhs.dtype == bodo.
            datetime64ns and op == operator.sub):

            def impl_dt64(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yrw__pkpu = bodo.utils.conversion.get_array_if_series_or_index(
                    rhs)
                rkrju__svrna = dt64_arr_sub(arr, yrw__pkpu)
                return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                    index, name)
            return impl_dt64
        if op in [operator.add, operator.sub] and isinstance(lhs, SeriesType
            ) and lhs.dtype == bodo.datetime64ns and is_offsets_type(rhs):

            def impl_offsets(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                rkrju__svrna = np.empty(n, np.dtype('datetime64[ns]'))
                for vov__ggess in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, vov__ggess):
                        bodo.libs.array_kernels.setna(rkrju__svrna, vov__ggess)
                        continue
                    nmoui__nbcgw = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[vov__ggess]))
                    vbk__lxjeq = op(nmoui__nbcgw, rhs)
                    rkrju__svrna[vov__ggess
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        vbk__lxjeq.value)
                return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                    index, name)
            return impl_offsets
        if op == operator.add and is_offsets_type(lhs) and isinstance(rhs,
            SeriesType) and rhs.dtype == bodo.datetime64ns:

            def impl(lhs, rhs):
                return op(rhs, lhs)
            return impl
        if isinstance(lhs, SeriesType):
            if lhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                    yrw__pkpu = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    rkrju__svrna = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(yrw__pkpu))
                    return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna
                        , index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                yrw__pkpu = bodo.utils.conversion.get_array_if_series_or_index(
                    rhs)
                rkrju__svrna = op(arr, yrw__pkpu)
                return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    hcx__jmj = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    rkrju__svrna = op(bodo.utils.conversion.
                        unbox_if_timestamp(hcx__jmj), arr)
                    return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna
                        , index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                hcx__jmj = bodo.utils.conversion.get_array_if_series_or_index(
                    lhs)
                rkrju__svrna = op(hcx__jmj, arr)
                return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        gzrap__rqrhm = create_binary_op_overload(op)
        overload(op)(gzrap__rqrhm)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    ednkv__tapa = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, ednkv__tapa)
        for vov__ggess in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, vov__ggess
                ) or bodo.libs.array_kernels.isna(arg2, vov__ggess):
                bodo.libs.array_kernels.setna(S, vov__ggess)
                continue
            S[vov__ggess
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                vov__ggess]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[vov__ggess]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                kvmq__qyi = bodo.utils.conversion.get_array_if_series_or_index(
                    other)
                op(arr, kvmq__qyi)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        gzrap__rqrhm = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(gzrap__rqrhm)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                rkrju__svrna = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        gzrap__rqrhm = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(gzrap__rqrhm)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    rkrju__svrna = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna
                        , index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    kvmq__qyi = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    rkrju__svrna = ufunc(arr, kvmq__qyi)
                    return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna
                        , index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    kvmq__qyi = bodo.hiframes.pd_series_ext.get_series_data(S2)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    rkrju__svrna = ufunc(arr, kvmq__qyi)
                    return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna
                        , index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        gzrap__rqrhm = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(gzrap__rqrhm)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        uymph__hkfyc = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.
            copy(),))
        ilte__vfc = np.arange(n),
        bodo.libs.timsort.sort(uymph__hkfyc, 0, n, ilte__vfc)
        return ilte__vfc[0]
    return impl


@overload(pd.to_numeric, inline='always', no_unliteral=True)
def overload_to_numeric(arg_a, errors='raise', downcast=None):
    if not is_overload_none(downcast) and not (is_overload_constant_str(
        downcast) and get_overload_const_str(downcast) in ('integer',
        'signed', 'unsigned', 'float')):
        raise BodoError(
            'pd.to_numeric(): invalid downcasting method provided {}'.
            format(downcast))
    out_dtype = types.float64
    if not is_overload_none(downcast):
        jcch__zut = get_overload_const_str(downcast)
        if jcch__zut in ('integer', 'signed'):
            out_dtype = types.int64
        elif jcch__zut == 'unsigned':
            out_dtype = types.uint64
        else:
            assert jcch__zut == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            zso__gglp = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            rkrju__svrna = pd.to_numeric(zso__gglp, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            sxwqb__ypvt = np.empty(n, np.float64)
            for vov__ggess in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, vov__ggess):
                    bodo.libs.array_kernels.setna(sxwqb__ypvt, vov__ggess)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(sxwqb__ypvt,
                        vov__ggess, arg_a, vov__ggess)
            return sxwqb__ypvt
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            sxwqb__ypvt = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for vov__ggess in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, vov__ggess):
                    bodo.libs.array_kernels.setna(sxwqb__ypvt, vov__ggess)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(sxwqb__ypvt,
                        vov__ggess, arg_a, vov__ggess)
            return sxwqb__ypvt
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        tfwg__lgsut = if_series_to_array_type(args[0])
        if isinstance(tfwg__lgsut, types.Array) and isinstance(tfwg__lgsut.
            dtype, types.Integer):
            tfwg__lgsut = types.Array(types.float64, 1, 'C')
        return tfwg__lgsut(*args)


def where_impl_one_arg(c):
    return np.where(c)


@overload(where_impl_one_arg, no_unliteral=True)
def overload_where_unsupported_one_arg(condition):
    if isinstance(condition, SeriesType) or bodo.utils.utils.is_array_typ(
        condition, False):
        return lambda condition: np.where(condition)


def overload_np_where_one_arg(condition):
    if isinstance(condition, SeriesType):

        def impl_series(condition):
            condition = bodo.hiframes.pd_series_ext.get_series_data(condition)
            return bodo.libs.array_kernels.nonzero(condition)
        return impl_series
    elif bodo.utils.utils.is_array_typ(condition, False):

        def impl(condition):
            return bodo.libs.array_kernels.nonzero(condition)
        return impl


overload(np.where, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)
overload(where_impl_one_arg, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)


def where_impl(c, x, y):
    return np.where(c, x, y)


@overload(where_impl, no_unliteral=True)
def overload_where_unsupported(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return lambda condition, x, y: np.where(condition, x, y)


@overload(where_impl, no_unliteral=True)
@overload(np.where, no_unliteral=True)
def overload_np_where(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return
    assert condition.dtype == types.bool_, 'invalid condition dtype'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.where()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(y,
        'numpy.where()')
    plwwp__uer = bodo.utils.utils.is_array_typ(x, True)
    lkyxh__upnlm = bodo.utils.utils.is_array_typ(y, True)
    wvw__gcjfb = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        wvw__gcjfb += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if plwwp__uer and not bodo.utils.utils.is_array_typ(x, False):
        wvw__gcjfb += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if lkyxh__upnlm and not bodo.utils.utils.is_array_typ(y, False):
        wvw__gcjfb += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    wvw__gcjfb += '  n = len(condition)\n'
    syjzv__ktqe = x.dtype if plwwp__uer else types.unliteral(x)
    nyn__zqbr = y.dtype if lkyxh__upnlm else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        syjzv__ktqe = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        nyn__zqbr = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    ilpe__wqj = get_data(x)
    ekn__qhrk = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(ilte__vfc) for
        ilte__vfc in [ilpe__wqj, ekn__qhrk])
    if ekn__qhrk == types.none:
        if isinstance(syjzv__ktqe, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif ilpe__wqj == ekn__qhrk and not is_nullable:
        out_dtype = dtype_to_array_type(syjzv__ktqe)
    elif syjzv__ktqe == string_type or nyn__zqbr == string_type:
        out_dtype = bodo.string_array_type
    elif ilpe__wqj == bytes_type or (plwwp__uer and syjzv__ktqe == bytes_type
        ) and (ekn__qhrk == bytes_type or lkyxh__upnlm and nyn__zqbr ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(syjzv__ktqe, bodo.PDCategoricalDtype):
        out_dtype = None
    elif syjzv__ktqe in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(syjzv__ktqe, 1, 'C')
    elif nyn__zqbr in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(nyn__zqbr, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(syjzv__ktqe), numba.np.numpy_support.
            as_dtype(nyn__zqbr)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(syjzv__ktqe, bodo.PDCategoricalDtype):
        cdwu__wasry = 'x'
    else:
        cdwu__wasry = 'out_dtype'
    wvw__gcjfb += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {cdwu__wasry}, (-1,))\n')
    if isinstance(syjzv__ktqe, bodo.PDCategoricalDtype):
        wvw__gcjfb += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        wvw__gcjfb += (
            '  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)\n'
            )
    wvw__gcjfb += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    wvw__gcjfb += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if plwwp__uer:
        wvw__gcjfb += '      if bodo.libs.array_kernels.isna(x, j):\n'
        wvw__gcjfb += '        setna(out_arr, j)\n'
        wvw__gcjfb += '        continue\n'
    if isinstance(syjzv__ktqe, bodo.PDCategoricalDtype):
        wvw__gcjfb += '      out_codes[j] = x_codes[j]\n'
    else:
        wvw__gcjfb += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if plwwp__uer else 'x'))
    wvw__gcjfb += '    else:\n'
    if lkyxh__upnlm:
        wvw__gcjfb += '      if bodo.libs.array_kernels.isna(y, j):\n'
        wvw__gcjfb += '        setna(out_arr, j)\n'
        wvw__gcjfb += '        continue\n'
    if ekn__qhrk == types.none:
        if isinstance(syjzv__ktqe, bodo.PDCategoricalDtype):
            wvw__gcjfb += '      out_codes[j] = -1\n'
        else:
            wvw__gcjfb += '      setna(out_arr, j)\n'
    else:
        wvw__gcjfb += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if lkyxh__upnlm else 'y'))
    wvw__gcjfb += '  return out_arr\n'
    huc__cuo = {}
    exec(wvw__gcjfb, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, huc__cuo)
    kyuyx__zjz = huc__cuo['_impl']
    return kyuyx__zjz


def _verify_np_select_arg_typs(condlist, choicelist, default):
    if isinstance(condlist, (types.List, types.UniTuple)):
        if not (bodo.utils.utils.is_np_array_typ(condlist.dtype) and 
            condlist.dtype.dtype == types.bool_):
            raise BodoError(
                "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
                )
    else:
        raise BodoError(
            "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
            )
    if not isinstance(choicelist, (types.List, types.UniTuple, types.BaseTuple)
        ):
        raise BodoError(
            "np.select(): 'choicelist' argument must be list or tuple type")
    if isinstance(choicelist, (types.List, types.UniTuple)):
        ddm__wzk = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(ddm__wzk, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(ddm__wzk):
            gqi__tuwh = ddm__wzk.data.dtype
        else:
            gqi__tuwh = ddm__wzk.dtype
        if isinstance(gqi__tuwh, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        pqmtt__obtx = ddm__wzk
    else:
        jjfl__veow = []
        for ddm__wzk in choicelist:
            if not bodo.utils.utils.is_array_typ(ddm__wzk, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(ddm__wzk):
                gqi__tuwh = ddm__wzk.data.dtype
            else:
                gqi__tuwh = ddm__wzk.dtype
            if isinstance(gqi__tuwh, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            jjfl__veow.append(gqi__tuwh)
        if not is_common_scalar_dtype(jjfl__veow):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        pqmtt__obtx = choicelist[0]
    if is_series_type(pqmtt__obtx):
        pqmtt__obtx = pqmtt__obtx.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, pqmtt__obtx.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(pqmtt__obtx, types.Array) or isinstance(pqmtt__obtx,
        BooleanArrayType) or isinstance(pqmtt__obtx, IntegerArrayType) or 
        bodo.utils.utils.is_array_typ(pqmtt__obtx, False) and pqmtt__obtx.
        dtype in [bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {pqmtt__obtx} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    gkw__qou = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        dvkqf__wbo = choicelist.dtype
    else:
        trd__gxbv = False
        jjfl__veow = []
        for ddm__wzk in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(ddm__wzk,
                'numpy.select()')
            if is_nullable_type(ddm__wzk):
                trd__gxbv = True
            if is_series_type(ddm__wzk):
                gqi__tuwh = ddm__wzk.data.dtype
            else:
                gqi__tuwh = ddm__wzk.dtype
            if isinstance(gqi__tuwh, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            jjfl__veow.append(gqi__tuwh)
        cjick__wco, ogycp__qszq = get_common_scalar_dtype(jjfl__veow)
        if not ogycp__qszq:
            raise BodoError('Internal error in overload_np_select')
        jhtq__kch = dtype_to_array_type(cjick__wco)
        if trd__gxbv:
            jhtq__kch = to_nullable_type(jhtq__kch)
        dvkqf__wbo = jhtq__kch
    if isinstance(dvkqf__wbo, SeriesType):
        dvkqf__wbo = dvkqf__wbo.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pjruo__sfmqf = True
    else:
        pjruo__sfmqf = False
    xwxu__zddz = False
    zuhe__oid = False
    if pjruo__sfmqf:
        if isinstance(dvkqf__wbo.dtype, types.Number):
            pass
        elif dvkqf__wbo.dtype == types.bool_:
            zuhe__oid = True
        else:
            xwxu__zddz = True
            dvkqf__wbo = to_nullable_type(dvkqf__wbo)
    elif default == types.none or is_overload_constant_nan(default):
        xwxu__zddz = True
        dvkqf__wbo = to_nullable_type(dvkqf__wbo)
    wvw__gcjfb = 'def np_select_impl(condlist, choicelist, default=0):\n'
    wvw__gcjfb += '  if len(condlist) != len(choicelist):\n'
    wvw__gcjfb += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    wvw__gcjfb += '  output_len = len(choicelist[0])\n'
    wvw__gcjfb += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    wvw__gcjfb += '  for i in range(output_len):\n'
    if xwxu__zddz:
        wvw__gcjfb += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif zuhe__oid:
        wvw__gcjfb += '    out[i] = False\n'
    else:
        wvw__gcjfb += '    out[i] = default\n'
    if gkw__qou:
        wvw__gcjfb += '  for i in range(len(condlist) - 1, -1, -1):\n'
        wvw__gcjfb += '    cond = condlist[i]\n'
        wvw__gcjfb += '    choice = choicelist[i]\n'
        wvw__gcjfb += '    out = np.where(cond, choice, out)\n'
    else:
        for vov__ggess in range(len(choicelist) - 1, -1, -1):
            wvw__gcjfb += f'  cond = condlist[{vov__ggess}]\n'
            wvw__gcjfb += f'  choice = choicelist[{vov__ggess}]\n'
            wvw__gcjfb += f'  out = np.where(cond, choice, out)\n'
    wvw__gcjfb += '  return out'
    huc__cuo = dict()
    exec(wvw__gcjfb, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': dvkqf__wbo}, huc__cuo)
    impl = huc__cuo['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        rkrju__svrna = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    jrezx__dexj = dict(subset=subset, keep=keep, inplace=inplace)
    adk__dtahn = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', jrezx__dexj,
        adk__dtahn, package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        edsmy__kwv = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (edsmy__kwv,), xjtg__xsxy = bodo.libs.array_kernels.drop_duplicates((
            edsmy__kwv,), index, 1)
        index = bodo.utils.conversion.index_from_array(xjtg__xsxy)
        return bodo.hiframes.pd_series_ext.init_series(edsmy__kwv, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    psn__ulve = element_type(S.data)
    if not is_common_scalar_dtype([psn__ulve, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([psn__ulve, right]):
        raise_bodo_error(
            "Series.between(): 'right' must be compariable with the Series data"
            )
    if not is_overload_constant_str(inclusive) or get_overload_const_str(
        inclusive) not in ('both', 'neither'):
        raise_bodo_error(
            "Series.between(): 'inclusive' must be a constant string and one of ('both', 'neither')"
            )

    def impl(S, left, right, inclusive='both'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        rkrju__svrna = np.empty(n, np.bool_)
        for vov__ggess in numba.parfors.parfor.internal_prange(n):
            lszr__jejsh = bodo.utils.conversion.box_if_dt64(arr[vov__ggess])
            if inclusive == 'both':
                rkrju__svrna[vov__ggess
                    ] = lszr__jejsh <= right and lszr__jejsh >= left
            else:
                rkrju__svrna[vov__ggess
                    ] = lszr__jejsh < right and lszr__jejsh > left
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna, index,
            name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    jrezx__dexj = dict(axis=axis)
    adk__dtahn = dict(axis=None)
    check_unsupported_args('Series.repeat', jrezx__dexj, adk__dtahn,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.repeat()')
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Series.repeat(): 'repeats' should be an integer or array of integers"
            )
    if isinstance(repeats, types.Integer):

        def impl_int(S, repeats, axis=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            xjtg__xsxy = bodo.utils.conversion.index_to_array(index)
            rkrju__svrna = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            naq__eexm = bodo.libs.array_kernels.repeat_kernel(xjtg__xsxy,
                repeats)
            vnjey__vue = bodo.utils.conversion.index_from_array(naq__eexm)
            return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
                vnjey__vue, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xjtg__xsxy = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        rkrju__svrna = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        naq__eexm = bodo.libs.array_kernels.repeat_kernel(xjtg__xsxy, repeats)
        vnjey__vue = bodo.utils.conversion.index_from_array(naq__eexm)
        return bodo.hiframes.pd_series_ext.init_series(rkrju__svrna,
            vnjey__vue, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        ilte__vfc = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(ilte__vfc)
        tkat__hjhc = {}
        for vov__ggess in range(n):
            lszr__jejsh = bodo.utils.conversion.box_if_dt64(ilte__vfc[
                vov__ggess])
            tkat__hjhc[index[vov__ggess]] = lszr__jejsh
        return tkat__hjhc
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    efnu__lwxwu = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            oai__uscwe = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(efnu__lwxwu)
    elif is_literal_type(name):
        oai__uscwe = get_literal_value(name)
    else:
        raise_bodo_error(efnu__lwxwu)
    oai__uscwe = 0 if oai__uscwe is None else oai__uscwe

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (oai__uscwe,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
