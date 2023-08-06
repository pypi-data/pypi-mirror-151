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
            esl__nikxw = bodo.hiframes.pd_series_ext.get_series_data(s)
            ibvd__lzsx = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                esl__nikxw)
            return ibvd__lzsx
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
            uqza__mmihz = list()
            for akpf__lmugn in range(len(S)):
                uqza__mmihz.append(S.iat[akpf__lmugn])
            return uqza__mmihz
        return impl_float

    def impl(S):
        uqza__mmihz = list()
        for akpf__lmugn in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, akpf__lmugn):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            uqza__mmihz.append(S.iat[akpf__lmugn])
        return uqza__mmihz
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    nnsql__vhjox = dict(dtype=dtype, copy=copy, na_value=na_value)
    bckl__matd = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    nnsql__vhjox = dict(name=name, inplace=inplace)
    bckl__matd = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', nnsql__vhjox, bckl__matd,
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
    htkau__mpp = get_name_literal(S.index.name_typ, True, series_name)
    columns = [htkau__mpp, series_name]
    fpahm__tbnf = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    fpahm__tbnf += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    fpahm__tbnf += """    index = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S))
"""
    fpahm__tbnf += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    fpahm__tbnf += '    col_var = {}\n'.format(gen_const_tup(columns))
    fpahm__tbnf += """    return bodo.hiframes.pd_dataframe_ext.init_dataframe((index, arr), df_index, col_var)
"""
    nrf__glaf = {}
    exec(fpahm__tbnf, {'bodo': bodo}, nrf__glaf)
    dunig__bsn = nrf__glaf['_impl']
    return dunig__bsn


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mpln__nmiei = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
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
        mpln__nmiei = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[akpf__lmugn]):
                bodo.libs.array_kernels.setna(mpln__nmiei, akpf__lmugn)
            else:
                mpln__nmiei[akpf__lmugn] = np.round(arr[akpf__lmugn], decimals)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    nnsql__vhjox = dict(level=level, numeric_only=numeric_only)
    bckl__matd = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(level=level, numeric_only=numeric_only)
    bckl__matd = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(axis=axis, bool_only=bool_only, skipna=skipna,
        level=level)
    bckl__matd = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        aah__xyif = 0
        for akpf__lmugn in numba.parfors.parfor.internal_prange(len(A)):
            hpqjz__buj = 0
            if not bodo.libs.array_kernels.isna(A, akpf__lmugn):
                hpqjz__buj = int(A[akpf__lmugn])
            aah__xyif += hpqjz__buj
        return aah__xyif != 0
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
        ixbpe__ngxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        okzti__wwow = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        aah__xyif = 0
        for akpf__lmugn in numba.parfors.parfor.internal_prange(len(
            ixbpe__ngxx)):
            hpqjz__buj = 0
            tsvkm__xkn = bodo.libs.array_kernels.isna(ixbpe__ngxx, akpf__lmugn)
            gehgy__tkvh = bodo.libs.array_kernels.isna(okzti__wwow, akpf__lmugn
                )
            if (tsvkm__xkn and not gehgy__tkvh or not tsvkm__xkn and
                gehgy__tkvh):
                hpqjz__buj = 1
            elif not tsvkm__xkn:
                if ixbpe__ngxx[akpf__lmugn] != okzti__wwow[akpf__lmugn]:
                    hpqjz__buj = 1
            aah__xyif += hpqjz__buj
        return aah__xyif == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    nnsql__vhjox = dict(axis=axis, bool_only=bool_only, skipna=skipna,
        level=level)
    bckl__matd = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        aah__xyif = 0
        for akpf__lmugn in numba.parfors.parfor.internal_prange(len(A)):
            hpqjz__buj = 0
            if not bodo.libs.array_kernels.isna(A, akpf__lmugn):
                hpqjz__buj = int(not A[akpf__lmugn])
            aah__xyif += hpqjz__buj
        return aah__xyif == 0
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    nnsql__vhjox = dict(level=level)
    bckl__matd = dict(level=None)
    check_unsupported_args('Series.mad', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    ybku__bus = types.float64
    vnn__lih = types.float64
    if S.dtype == types.float32:
        ybku__bus = types.float32
        vnn__lih = types.float32
    rql__ary = ybku__bus(0)
    ebw__ztnxc = vnn__lih(0)
    fgbfc__zce = vnn__lih(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        hibnf__uqkk = rql__ary
        aah__xyif = ebw__ztnxc
        for akpf__lmugn in numba.parfors.parfor.internal_prange(len(A)):
            hpqjz__buj = rql__ary
            hauk__gtkr = ebw__ztnxc
            if not bodo.libs.array_kernels.isna(A, akpf__lmugn) or not skipna:
                hpqjz__buj = A[akpf__lmugn]
                hauk__gtkr = fgbfc__zce
            hibnf__uqkk += hpqjz__buj
            aah__xyif += hauk__gtkr
        axj__xlwl = bodo.hiframes.series_kernels._mean_handle_nan(hibnf__uqkk,
            aah__xyif)
        qss__tconc = rql__ary
        for akpf__lmugn in numba.parfors.parfor.internal_prange(len(A)):
            hpqjz__buj = rql__ary
            if not bodo.libs.array_kernels.isna(A, akpf__lmugn) or not skipna:
                hpqjz__buj = abs(A[akpf__lmugn] - axj__xlwl)
            qss__tconc += hpqjz__buj
        klyy__dehwu = bodo.hiframes.series_kernels._mean_handle_nan(qss__tconc,
            aah__xyif)
        return klyy__dehwu
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    nnsql__vhjox = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    bckl__matd = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(level=level, numeric_only=numeric_only)
    bckl__matd = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', nnsql__vhjox, bckl__matd,
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
        ukc__tuu = 0
        lwj__shlu = 0
        aah__xyif = 0
        for akpf__lmugn in numba.parfors.parfor.internal_prange(len(A)):
            hpqjz__buj = 0
            hauk__gtkr = 0
            if not bodo.libs.array_kernels.isna(A, akpf__lmugn) or not skipna:
                hpqjz__buj = A[akpf__lmugn]
                hauk__gtkr = 1
            ukc__tuu += hpqjz__buj
            lwj__shlu += hpqjz__buj * hpqjz__buj
            aah__xyif += hauk__gtkr
        bbqf__ziwq = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            ukc__tuu, lwj__shlu, aah__xyif, ddof)
        lyyi__zbk = bodo.hiframes.series_kernels._sem_handle_nan(bbqf__ziwq,
            aah__xyif)
        return lyyi__zbk
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    nnsql__vhjox = dict(level=level, numeric_only=numeric_only)
    bckl__matd = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', nnsql__vhjox, bckl__matd,
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
        ukc__tuu = 0.0
        lwj__shlu = 0.0
        ywar__ilvbr = 0.0
        cehi__ebyxm = 0.0
        aah__xyif = 0
        for akpf__lmugn in numba.parfors.parfor.internal_prange(len(A)):
            hpqjz__buj = 0.0
            hauk__gtkr = 0
            if not bodo.libs.array_kernels.isna(A, akpf__lmugn) or not skipna:
                hpqjz__buj = np.float64(A[akpf__lmugn])
                hauk__gtkr = 1
            ukc__tuu += hpqjz__buj
            lwj__shlu += hpqjz__buj ** 2
            ywar__ilvbr += hpqjz__buj ** 3
            cehi__ebyxm += hpqjz__buj ** 4
            aah__xyif += hauk__gtkr
        bbqf__ziwq = bodo.hiframes.series_kernels.compute_kurt(ukc__tuu,
            lwj__shlu, ywar__ilvbr, cehi__ebyxm, aah__xyif)
        return bbqf__ziwq
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    nnsql__vhjox = dict(level=level, numeric_only=numeric_only)
    bckl__matd = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', nnsql__vhjox, bckl__matd,
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
        ukc__tuu = 0.0
        lwj__shlu = 0.0
        ywar__ilvbr = 0.0
        aah__xyif = 0
        for akpf__lmugn in numba.parfors.parfor.internal_prange(len(A)):
            hpqjz__buj = 0.0
            hauk__gtkr = 0
            if not bodo.libs.array_kernels.isna(A, akpf__lmugn) or not skipna:
                hpqjz__buj = np.float64(A[akpf__lmugn])
                hauk__gtkr = 1
            ukc__tuu += hpqjz__buj
            lwj__shlu += hpqjz__buj ** 2
            ywar__ilvbr += hpqjz__buj ** 3
            aah__xyif += hauk__gtkr
        bbqf__ziwq = bodo.hiframes.series_kernels.compute_skew(ukc__tuu,
            lwj__shlu, ywar__ilvbr, aah__xyif)
        return bbqf__ziwq
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    nnsql__vhjox = dict(level=level, numeric_only=numeric_only)
    bckl__matd = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(level=level, numeric_only=numeric_only)
    bckl__matd = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', nnsql__vhjox, bckl__matd,
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
        ixbpe__ngxx = bodo.hiframes.pd_series_ext.get_series_data(S)
        okzti__wwow = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        lkr__wzk = 0
        for akpf__lmugn in numba.parfors.parfor.internal_prange(len(
            ixbpe__ngxx)):
            sqqw__ljsgr = ixbpe__ngxx[akpf__lmugn]
            onps__kkkme = okzti__wwow[akpf__lmugn]
            lkr__wzk += sqqw__ljsgr * onps__kkkme
        return lkr__wzk
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    nnsql__vhjox = dict(skipna=skipna)
    bckl__matd = dict(skipna=True)
    check_unsupported_args('Series.cumsum', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(skipna=skipna)
    bckl__matd = dict(skipna=True)
    check_unsupported_args('Series.cumprod', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(skipna=skipna)
    bckl__matd = dict(skipna=True)
    check_unsupported_args('Series.cummin', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(skipna=skipna)
    bckl__matd = dict(skipna=True)
    check_unsupported_args('Series.cummax', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    bckl__matd = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        quz__hzgf = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, quz__hzgf, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    nnsql__vhjox = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    bckl__matd = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(level=level)
    bckl__matd = dict(level=None)
    check_unsupported_args('Series.count', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    nnsql__vhjox = dict(method=method, min_periods=min_periods)
    bckl__matd = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        izl__rrva = S.sum()
        susiv__gbbi = other.sum()
        a = n * (S * other).sum() - izl__rrva * susiv__gbbi
        xpo__quob = n * (S ** 2).sum() - izl__rrva ** 2
        wekh__qjah = n * (other ** 2).sum() - susiv__gbbi ** 2
        return a / np.sqrt(xpo__quob * wekh__qjah)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    nnsql__vhjox = dict(min_periods=min_periods)
    bckl__matd = dict(min_periods=None)
    check_unsupported_args('Series.cov', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        izl__rrva = S.mean()
        susiv__gbbi = other.mean()
        hvxmr__zfmv = ((S - izl__rrva) * (other - susiv__gbbi)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(hvxmr__zfmv, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            nmcak__lvh = np.sign(sum_val)
            return np.inf * nmcak__lvh
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    nnsql__vhjox = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    bckl__matd = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    bckl__matd = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(axis=axis, skipna=skipna)
    bckl__matd = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(axis=axis, skipna=skipna)
    bckl__matd = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', nnsql__vhjox, bckl__matd,
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
    nnsql__vhjox = dict(level=level, numeric_only=numeric_only)
    bckl__matd = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', nnsql__vhjox, bckl__matd,
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
        xjida__bdtuh = arr[:n]
        rcqt__kjku = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(xjida__bdtuh,
            rcqt__kjku, name)
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
        nacpf__uad = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xjida__bdtuh = arr[nacpf__uad:]
        rcqt__kjku = index[nacpf__uad:]
        return bodo.hiframes.pd_series_ext.init_series(xjida__bdtuh,
            rcqt__kjku, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    wzg__sip = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in wzg__sip:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            miyp__fgrdw = index[0]
            gso__jwb = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                miyp__fgrdw, False))
        else:
            gso__jwb = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xjida__bdtuh = arr[:gso__jwb]
        rcqt__kjku = index[:gso__jwb]
        return bodo.hiframes.pd_series_ext.init_series(xjida__bdtuh,
            rcqt__kjku, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    wzg__sip = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in wzg__sip:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            yargd__wdsf = index[-1]
            gso__jwb = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                yargd__wdsf, True))
        else:
            gso__jwb = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xjida__bdtuh = arr[len(arr) - gso__jwb:]
        rcqt__kjku = index[len(arr) - gso__jwb:]
        return bodo.hiframes.pd_series_ext.init_series(xjida__bdtuh,
            rcqt__kjku, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        uim__ypxos = bodo.utils.conversion.index_to_array(index)
        ucx__plm, tqbp__ldll = bodo.libs.array_kernels.first_last_valid_index(
            arr, uim__ypxos)
        return tqbp__ldll if ucx__plm else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        uim__ypxos = bodo.utils.conversion.index_to_array(index)
        ucx__plm, tqbp__ldll = bodo.libs.array_kernels.first_last_valid_index(
            arr, uim__ypxos, False)
        return tqbp__ldll if ucx__plm else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    nnsql__vhjox = dict(keep=keep)
    bckl__matd = dict(keep='first')
    check_unsupported_args('Series.nlargest', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        uim__ypxos = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mpln__nmiei, efdl__ejnj = bodo.libs.array_kernels.nlargest(arr,
            uim__ypxos, n, True, bodo.hiframes.series_kernels.gt_f)
        jzw__rary = bodo.utils.conversion.convert_to_index(efdl__ejnj)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
            jzw__rary, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    nnsql__vhjox = dict(keep=keep)
    bckl__matd = dict(keep='first')
    check_unsupported_args('Series.nsmallest', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        uim__ypxos = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mpln__nmiei, efdl__ejnj = bodo.libs.array_kernels.nlargest(arr,
            uim__ypxos, n, False, bodo.hiframes.series_kernels.lt_f)
        jzw__rary = bodo.utils.conversion.convert_to_index(efdl__ejnj)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
            jzw__rary, name)
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
    nnsql__vhjox = dict(errors=errors)
    bckl__matd = dict(errors='raise')
    check_unsupported_args('Series.astype', nnsql__vhjox, bckl__matd,
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
        mpln__nmiei = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    nnsql__vhjox = dict(axis=axis, is_copy=is_copy)
    bckl__matd = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        qwht__pqo = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[qwht__pqo],
            index[qwht__pqo], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    nnsql__vhjox = dict(axis=axis, kind=kind, order=order)
    bckl__matd = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        ady__qsudf = S.notna().values
        if not ady__qsudf.all():
            mpln__nmiei = np.full(n, -1, np.int64)
            mpln__nmiei[ady__qsudf] = argsort(arr[ady__qsudf])
        else:
            mpln__nmiei = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    nnsql__vhjox = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    bckl__matd = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', nnsql__vhjox, bckl__matd,
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
        lyeao__uqs = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col3_',))
        bqsqm__rsyk = lyeao__uqs.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        mpln__nmiei = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            bqsqm__rsyk, 0)
        jzw__rary = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            bqsqm__rsyk)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
            jzw__rary, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    nnsql__vhjox = dict(axis=axis, inplace=inplace, kind=kind, ignore_index
        =ignore_index, key=key)
    bckl__matd = dict(axis=0, inplace=False, kind='quicksort', ignore_index
        =False, key=None)
    check_unsupported_args('Series.sort_values', nnsql__vhjox, bckl__matd,
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
        lyeao__uqs = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, ('$_bodo_col_',))
        bqsqm__rsyk = lyeao__uqs.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        mpln__nmiei = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
            bqsqm__rsyk, 0)
        jzw__rary = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            bqsqm__rsyk)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
            jzw__rary, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    xtgl__hts = is_overload_true(is_nullable)
    fpahm__tbnf = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    fpahm__tbnf += '  numba.parfors.parfor.init_prange()\n'
    fpahm__tbnf += '  n = len(arr)\n'
    if xtgl__hts:
        fpahm__tbnf += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        fpahm__tbnf += '  out_arr = np.empty(n, np.int64)\n'
    fpahm__tbnf += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    fpahm__tbnf += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if xtgl__hts:
        fpahm__tbnf += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        fpahm__tbnf += '      out_arr[i] = -1\n'
    fpahm__tbnf += '      continue\n'
    fpahm__tbnf += '    val = arr[i]\n'
    fpahm__tbnf += '    if include_lowest and val == bins[0]:\n'
    fpahm__tbnf += '      ind = 1\n'
    fpahm__tbnf += '    else:\n'
    fpahm__tbnf += '      ind = np.searchsorted(bins, val)\n'
    fpahm__tbnf += '    if ind == 0 or ind == len(bins):\n'
    if xtgl__hts:
        fpahm__tbnf += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        fpahm__tbnf += '      out_arr[i] = -1\n'
    fpahm__tbnf += '    else:\n'
    fpahm__tbnf += '      out_arr[i] = ind - 1\n'
    fpahm__tbnf += '  return out_arr\n'
    nrf__glaf = {}
    exec(fpahm__tbnf, {'bodo': bodo, 'np': np, 'numba': numba}, nrf__glaf)
    impl = nrf__glaf['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        qdca__xkoz, pjc__gyrz = np.divmod(x, 1)
        if qdca__xkoz == 0:
            tvh__jfypy = -int(np.floor(np.log10(abs(pjc__gyrz)))
                ) - 1 + precision
        else:
            tvh__jfypy = precision
        return np.around(x, tvh__jfypy)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        vnajd__tuda = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(vnajd__tuda)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        zxli__exwa = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            geltc__fbeoi = bins.copy()
            if right and include_lowest:
                geltc__fbeoi[0] = geltc__fbeoi[0] - zxli__exwa
            bud__urgk = bodo.libs.interval_arr_ext.init_interval_array(
                geltc__fbeoi[:-1], geltc__fbeoi[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(bud__urgk,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        geltc__fbeoi = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            geltc__fbeoi[0] = geltc__fbeoi[0] - 10.0 ** -precision
        bud__urgk = bodo.libs.interval_arr_ext.init_interval_array(geltc__fbeoi
            [:-1], geltc__fbeoi[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(bud__urgk, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        qrnzp__etnq = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        ydj__weh = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        mpln__nmiei = np.zeros(nbins, np.int64)
        for akpf__lmugn in range(len(qrnzp__etnq)):
            mpln__nmiei[ydj__weh[akpf__lmugn]] = qrnzp__etnq[akpf__lmugn]
        return mpln__nmiei
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
            gntwi__glzrt = (max_val - min_val) * 0.001
            if right:
                bins[0] -= gntwi__glzrt
            else:
                bins[-1] += gntwi__glzrt
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    nnsql__vhjox = dict(dropna=dropna)
    bckl__matd = dict(dropna=True)
    check_unsupported_args('Series.value_counts', nnsql__vhjox, bckl__matd,
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
    ihl__qfj = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    fpahm__tbnf = 'def impl(\n'
    fpahm__tbnf += '    S,\n'
    fpahm__tbnf += '    normalize=False,\n'
    fpahm__tbnf += '    sort=True,\n'
    fpahm__tbnf += '    ascending=False,\n'
    fpahm__tbnf += '    bins=None,\n'
    fpahm__tbnf += '    dropna=True,\n'
    fpahm__tbnf += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    fpahm__tbnf += '):\n'
    fpahm__tbnf += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    fpahm__tbnf += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    fpahm__tbnf += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if ihl__qfj:
        fpahm__tbnf += '    right = True\n'
        fpahm__tbnf += _gen_bins_handling(bins, S.dtype)
        fpahm__tbnf += '    arr = get_bin_inds(bins, arr)\n'
    fpahm__tbnf += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    fpahm__tbnf += "        (arr,), index, ('$_bodo_col2_',)\n"
    fpahm__tbnf += '    )\n'
    fpahm__tbnf += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if ihl__qfj:
        fpahm__tbnf += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        fpahm__tbnf += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        fpahm__tbnf += '    index = get_bin_labels(bins)\n'
    else:
        fpahm__tbnf += """    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)
"""
        fpahm__tbnf += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        fpahm__tbnf += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        fpahm__tbnf += '    )\n'
        fpahm__tbnf += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    fpahm__tbnf += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        fpahm__tbnf += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        cjrkf__fhzx = 'len(S)' if ihl__qfj else 'count_arr.sum()'
        fpahm__tbnf += f'    res = res / float({cjrkf__fhzx})\n'
    fpahm__tbnf += '    return res\n'
    nrf__glaf = {}
    exec(fpahm__tbnf, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, nrf__glaf)
    impl = nrf__glaf['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    fpahm__tbnf = ''
    if isinstance(bins, types.Integer):
        fpahm__tbnf += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        fpahm__tbnf += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            fpahm__tbnf += '    min_val = min_val.value\n'
            fpahm__tbnf += '    max_val = max_val.value\n'
        fpahm__tbnf += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            fpahm__tbnf += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        fpahm__tbnf += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return fpahm__tbnf


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    nnsql__vhjox = dict(right=right, labels=labels, retbins=retbins,
        precision=precision, duplicates=duplicates, ordered=ordered)
    bckl__matd = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    fpahm__tbnf = 'def impl(\n'
    fpahm__tbnf += '    x,\n'
    fpahm__tbnf += '    bins,\n'
    fpahm__tbnf += '    right=True,\n'
    fpahm__tbnf += '    labels=None,\n'
    fpahm__tbnf += '    retbins=False,\n'
    fpahm__tbnf += '    precision=3,\n'
    fpahm__tbnf += '    include_lowest=False,\n'
    fpahm__tbnf += "    duplicates='raise',\n"
    fpahm__tbnf += '    ordered=True\n'
    fpahm__tbnf += '):\n'
    if isinstance(x, SeriesType):
        fpahm__tbnf += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        fpahm__tbnf += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        fpahm__tbnf += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        fpahm__tbnf += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    fpahm__tbnf += _gen_bins_handling(bins, x.dtype)
    fpahm__tbnf += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    fpahm__tbnf += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    fpahm__tbnf += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    fpahm__tbnf += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        fpahm__tbnf += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        fpahm__tbnf += '    return res\n'
    else:
        fpahm__tbnf += '    return out_arr\n'
    nrf__glaf = {}
    exec(fpahm__tbnf, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, nrf__glaf)
    impl = nrf__glaf['impl']
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
    nnsql__vhjox = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    bckl__matd = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        vvqqp__ubj = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, vvqqp__ubj)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    nnsql__vhjox = dict(axis=axis, sort=sort, group_keys=group_keys,
        squeeze=squeeze, observed=observed, dropna=dropna)
    bckl__matd = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', nnsql__vhjox, bckl__matd,
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
            jvc__knm = bodo.utils.conversion.coerce_to_array(index)
            lyeao__uqs = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                jvc__knm, arr), index, (' ', ''))
            return lyeao__uqs.groupby(' ')['']
        return impl_index
    mjt__zyuq = by
    if isinstance(by, SeriesType):
        mjt__zyuq = by.data
    if isinstance(mjt__zyuq, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        jvc__knm = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        lyeao__uqs = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            jvc__knm, arr), index, (' ', ''))
        return lyeao__uqs.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    nnsql__vhjox = dict(verify_integrity=verify_integrity)
    bckl__matd = dict(verify_integrity=False)
    check_unsupported_args('Series.append', nnsql__vhjox, bckl__matd,
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
            ssx__busq = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            mpln__nmiei = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(mpln__nmiei, A, ssx__busq, False)
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                index, name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mpln__nmiei = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    nnsql__vhjox = dict(interpolation=interpolation)
    bckl__matd = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            mpln__nmiei = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
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
        cgdvy__jjj = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(cgdvy__jjj, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    nnsql__vhjox = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    bckl__matd = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', nnsql__vhjox, bckl__matd,
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
        fahh__rzuh = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        fahh__rzuh = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    fpahm__tbnf = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {fahh__rzuh}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    avkk__mbnk = dict()
    exec(fpahm__tbnf, {'bodo': bodo, 'numba': numba}, avkk__mbnk)
    tltfk__ofaf = avkk__mbnk['impl']
    return tltfk__ofaf


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        fahh__rzuh = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        fahh__rzuh = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    fpahm__tbnf = 'def impl(S,\n'
    fpahm__tbnf += '     value=None,\n'
    fpahm__tbnf += '    method=None,\n'
    fpahm__tbnf += '    axis=None,\n'
    fpahm__tbnf += '    inplace=False,\n'
    fpahm__tbnf += '    limit=None,\n'
    fpahm__tbnf += '   downcast=None,\n'
    fpahm__tbnf += '):\n'
    fpahm__tbnf += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    fpahm__tbnf += '    n = len(in_arr)\n'
    fpahm__tbnf += f'    out_arr = {fahh__rzuh}(n, -1)\n'
    fpahm__tbnf += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    fpahm__tbnf += '        s = in_arr[j]\n'
    fpahm__tbnf += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    fpahm__tbnf += '            s = value\n'
    fpahm__tbnf += '        out_arr[j] = s\n'
    fpahm__tbnf += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    avkk__mbnk = dict()
    exec(fpahm__tbnf, {'bodo': bodo, 'numba': numba}, avkk__mbnk)
    tltfk__ofaf = avkk__mbnk['impl']
    return tltfk__ofaf


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
    jhpq__gbsrc = bodo.hiframes.pd_series_ext.get_series_data(value)
    for akpf__lmugn in numba.parfors.parfor.internal_prange(len(glh__wyg)):
        s = glh__wyg[akpf__lmugn]
        if bodo.libs.array_kernels.isna(glh__wyg, akpf__lmugn
            ) and not bodo.libs.array_kernels.isna(jhpq__gbsrc, akpf__lmugn):
            s = jhpq__gbsrc[akpf__lmugn]
        glh__wyg[akpf__lmugn] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
    for akpf__lmugn in numba.parfors.parfor.internal_prange(len(glh__wyg)):
        s = glh__wyg[akpf__lmugn]
        if bodo.libs.array_kernels.isna(glh__wyg, akpf__lmugn):
            s = value
        glh__wyg[akpf__lmugn] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    jhpq__gbsrc = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(glh__wyg)
    mpln__nmiei = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for fznjz__euuep in numba.parfors.parfor.internal_prange(n):
        s = glh__wyg[fznjz__euuep]
        if bodo.libs.array_kernels.isna(glh__wyg, fznjz__euuep
            ) and not bodo.libs.array_kernels.isna(jhpq__gbsrc, fznjz__euuep):
            s = jhpq__gbsrc[fznjz__euuep]
        mpln__nmiei[fznjz__euuep] = s
        if bodo.libs.array_kernels.isna(glh__wyg, fznjz__euuep
            ) and bodo.libs.array_kernels.isna(jhpq__gbsrc, fznjz__euuep):
            bodo.libs.array_kernels.setna(mpln__nmiei, fznjz__euuep)
    return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    jhpq__gbsrc = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(glh__wyg)
    mpln__nmiei = bodo.utils.utils.alloc_type(n, glh__wyg.dtype, (-1,))
    for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
        s = glh__wyg[akpf__lmugn]
        if bodo.libs.array_kernels.isna(glh__wyg, akpf__lmugn
            ) and not bodo.libs.array_kernels.isna(jhpq__gbsrc, akpf__lmugn):
            s = jhpq__gbsrc[akpf__lmugn]
        mpln__nmiei[akpf__lmugn] = s
    return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    nnsql__vhjox = dict(limit=limit, downcast=downcast)
    bckl__matd = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', nnsql__vhjox, bckl__matd,
        package_name='pandas', module_name='Series')
    kln__ddhn = not is_overload_none(value)
    zhz__cqgay = not is_overload_none(method)
    if kln__ddhn and zhz__cqgay:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not kln__ddhn and not zhz__cqgay:
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
    if zhz__cqgay:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        qph__cjzk = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(qph__cjzk)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(qph__cjzk)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    vlve__ppzsn = element_type(S.data)
    psmqg__nfehi = None
    if kln__ddhn:
        psmqg__nfehi = element_type(types.unliteral(value))
    if psmqg__nfehi and not can_replace(vlve__ppzsn, psmqg__nfehi):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {psmqg__nfehi} with series type {vlve__ppzsn}'
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
        eoge__vzb = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                jhpq__gbsrc = bodo.hiframes.pd_series_ext.get_series_data(value
                    )
                n = len(glh__wyg)
                mpln__nmiei = bodo.utils.utils.alloc_type(n, eoge__vzb, (-1,))
                for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(glh__wyg, akpf__lmugn
                        ) and bodo.libs.array_kernels.isna(jhpq__gbsrc,
                        akpf__lmugn):
                        bodo.libs.array_kernels.setna(mpln__nmiei, akpf__lmugn)
                        continue
                    if bodo.libs.array_kernels.isna(glh__wyg, akpf__lmugn):
                        mpln__nmiei[akpf__lmugn
                            ] = bodo.utils.conversion.unbox_if_timestamp(
                            jhpq__gbsrc[akpf__lmugn])
                        continue
                    mpln__nmiei[akpf__lmugn
                        ] = bodo.utils.conversion.unbox_if_timestamp(glh__wyg
                        [akpf__lmugn])
                return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                    index, name)
            return fillna_series_impl
        if zhz__cqgay:
            aghf__vnrj = (types.unicode_type, types.bool_, bodo.
                datetime64ns, bodo.timedelta64ns)
            if not isinstance(vlve__ppzsn, (types.Integer, types.Float)
                ) and vlve__ppzsn not in aghf__vnrj:
                raise BodoError(
                    f"Series.fillna(): series of type {vlve__ppzsn} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                mpln__nmiei = bodo.libs.array_kernels.ffill_bfill_arr(glh__wyg,
                    method)
                return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_timestamp(value)
            glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(glh__wyg)
            mpln__nmiei = bodo.utils.utils.alloc_type(n, eoge__vzb, (-1,))
            for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_timestamp(glh__wyg[
                    akpf__lmugn])
                if bodo.libs.array_kernels.isna(glh__wyg, akpf__lmugn):
                    s = value
                mpln__nmiei[akpf__lmugn] = s
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                index, name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        wltos__who = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        nnsql__vhjox = dict(limit=limit, downcast=downcast)
        bckl__matd = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', nnsql__vhjox,
            bckl__matd, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        vlve__ppzsn = element_type(S.data)
        aghf__vnrj = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(vlve__ppzsn, (types.Integer, types.Float)
            ) and vlve__ppzsn not in aghf__vnrj:
            raise BodoError(
                f'Series.{overload_name}(): series of type {vlve__ppzsn} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            mpln__nmiei = bodo.libs.array_kernels.ffill_bfill_arr(glh__wyg,
                wltos__who)
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                index, name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        hohzo__ihiv = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            hohzo__ihiv)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        spnyq__rbxev = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(spnyq__rbxev)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        spnyq__rbxev = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(spnyq__rbxev)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        spnyq__rbxev = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(spnyq__rbxev)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    nnsql__vhjox = dict(inplace=inplace, limit=limit, regex=regex, method=
        method)
    kvdsr__tbha = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', nnsql__vhjox, kvdsr__tbha,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    vlve__ppzsn = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        mvg__fvq = element_type(to_replace.key_type)
        psmqg__nfehi = element_type(to_replace.value_type)
    else:
        mvg__fvq = element_type(to_replace)
        psmqg__nfehi = element_type(value)
    qtlin__ktx = None
    if vlve__ppzsn != types.unliteral(mvg__fvq):
        if bodo.utils.typing.equality_always_false(vlve__ppzsn, types.
            unliteral(mvg__fvq)
            ) or not bodo.utils.typing.types_equality_exists(vlve__ppzsn,
            mvg__fvq):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(vlve__ppzsn, (types.Float, types.Integer)
            ) or vlve__ppzsn == np.bool_:
            qtlin__ktx = vlve__ppzsn
    if not can_replace(vlve__ppzsn, types.unliteral(psmqg__nfehi)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    lmhn__zsokd = to_str_arr_if_dict_array(S.data)
    if isinstance(lmhn__zsokd, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(glh__wyg.replace
                (to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(glh__wyg)
        mpln__nmiei = bodo.utils.utils.alloc_type(n, lmhn__zsokd, (-1,))
        baly__hwnnh = build_replace_dict(to_replace, value, qtlin__ktx)
        for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(glh__wyg, akpf__lmugn):
                bodo.libs.array_kernels.setna(mpln__nmiei, akpf__lmugn)
                continue
            s = glh__wyg[akpf__lmugn]
            if s in baly__hwnnh:
                s = baly__hwnnh[s]
            mpln__nmiei[akpf__lmugn] = s
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    fdqnm__ohev = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    axke__pejdu = is_iterable_type(to_replace)
    xcu__zlor = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    hincq__bqfmt = is_iterable_type(value)
    if fdqnm__ohev and xcu__zlor:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                baly__hwnnh = {}
                baly__hwnnh[key_dtype_conv(to_replace)] = value
                return baly__hwnnh
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            baly__hwnnh = {}
            baly__hwnnh[to_replace] = value
            return baly__hwnnh
        return impl
    if axke__pejdu and xcu__zlor:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                baly__hwnnh = {}
                for tygq__ykfh in to_replace:
                    baly__hwnnh[key_dtype_conv(tygq__ykfh)] = value
                return baly__hwnnh
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            baly__hwnnh = {}
            for tygq__ykfh in to_replace:
                baly__hwnnh[tygq__ykfh] = value
            return baly__hwnnh
        return impl
    if axke__pejdu and hincq__bqfmt:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                baly__hwnnh = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for akpf__lmugn in range(len(to_replace)):
                    baly__hwnnh[key_dtype_conv(to_replace[akpf__lmugn])
                        ] = value[akpf__lmugn]
                return baly__hwnnh
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            baly__hwnnh = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for akpf__lmugn in range(len(to_replace)):
                baly__hwnnh[to_replace[akpf__lmugn]] = value[akpf__lmugn]
            return baly__hwnnh
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
            mpln__nmiei = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                index, name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mpln__nmiei = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    nnsql__vhjox = dict(ignore_index=ignore_index)
    liw__bks = dict(ignore_index=False)
    check_unsupported_args('Series.explode', nnsql__vhjox, liw__bks,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        uim__ypxos = bodo.utils.conversion.index_to_array(index)
        mpln__nmiei, ixcca__umb = bodo.libs.array_kernels.explode(arr,
            uim__ypxos)
        jzw__rary = bodo.utils.conversion.index_from_array(ixcca__umb)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
            jzw__rary, name)
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
            rljvg__inpcd = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                rljvg__inpcd[akpf__lmugn] = np.argmax(a[akpf__lmugn])
            return rljvg__inpcd
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            kxo__nfk = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                kxo__nfk[akpf__lmugn] = np.argmin(a[akpf__lmugn])
            return kxo__nfk
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
    nnsql__vhjox = dict(axis=axis, inplace=inplace, how=how)
    srgo__yzqwp = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', nnsql__vhjox, srgo__yzqwp,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            ady__qsudf = S.notna().values
            uim__ypxos = bodo.utils.conversion.extract_index_array(S)
            jzw__rary = bodo.utils.conversion.convert_to_index(uim__ypxos[
                ady__qsudf])
            mpln__nmiei = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(glh__wyg))
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                jzw__rary, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            uim__ypxos = bodo.utils.conversion.extract_index_array(S)
            ady__qsudf = S.notna().values
            jzw__rary = bodo.utils.conversion.convert_to_index(uim__ypxos[
                ady__qsudf])
            mpln__nmiei = glh__wyg[ady__qsudf]
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                jzw__rary, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    nnsql__vhjox = dict(freq=freq, axis=axis, fill_value=fill_value)
    bckl__matd = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('Series.shift', nnsql__vhjox, bckl__matd,
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
        mpln__nmiei = bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    nnsql__vhjox = dict(fill_method=fill_method, limit=limit, freq=freq)
    bckl__matd = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', nnsql__vhjox, bckl__matd,
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
        mpln__nmiei = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
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
            kus__qaf = 'None'
        else:
            kus__qaf = 'other'
        fpahm__tbnf = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            fpahm__tbnf += '  cond = ~cond\n'
        fpahm__tbnf += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        fpahm__tbnf += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        fpahm__tbnf += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        fpahm__tbnf += (
            f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {kus__qaf})\n'
            )
        fpahm__tbnf += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        nrf__glaf = {}
        exec(fpahm__tbnf, {'bodo': bodo, 'np': np}, nrf__glaf)
        impl = nrf__glaf['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        hohzo__ihiv = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(hohzo__ihiv)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, S, cond, other, inplace, axis,
    level, errors, try_cast):
    nnsql__vhjox = dict(inplace=inplace, level=level, errors=errors,
        try_cast=try_cast)
    bckl__matd = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', nnsql__vhjox, bckl__matd,
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
    wnao__gzh = is_overload_constant_nan(other)
    if not (is_default or wnao__gzh or is_scalar_type(other) or isinstance(
        other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
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
            jxac__tfpvv = arr.dtype.elem_type
        else:
            jxac__tfpvv = arr.dtype
        if is_iterable_type(other):
            syx__ire = other.dtype
        elif wnao__gzh:
            syx__ire = types.float64
        else:
            syx__ire = types.unliteral(other)
        if not wnao__gzh and not is_common_scalar_dtype([jxac__tfpvv, syx__ire]
            ):
            raise BodoError(
                f"{func_name}() series and 'other' must share a common type.")


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        nnsql__vhjox = dict(level=level, axis=axis)
        bckl__matd = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__),
            nnsql__vhjox, bckl__matd, package_name='pandas', module_name=
            'Series')
        tum__imri = other == string_type or is_overload_constant_str(other)
        fnr__nvsxt = is_iterable_type(other) and other.dtype == string_type
        fbb__hnevh = S.dtype == string_type and (op == operator.add and (
            tum__imri or fnr__nvsxt) or op == operator.mul and isinstance(
            other, types.Integer))
        yesex__rao = S.dtype == bodo.timedelta64ns
        lygs__uuzq = S.dtype == bodo.datetime64ns
        ffds__tev = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        tdbpe__ugzqv = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype == pd_timestamp_type or 
            other.dtype == bodo.datetime64ns)
        oyzie__nfb = yesex__rao and (ffds__tev or tdbpe__ugzqv
            ) or lygs__uuzq and ffds__tev
        oyzie__nfb = oyzie__nfb and op == operator.add
        if not (isinstance(S.dtype, types.Number) or fbb__hnevh or oyzie__nfb):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        lan__imoa = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            lmhn__zsokd = lan__imoa.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and lmhn__zsokd == types.Array(types.bool_, 1, 'C'):
                lmhn__zsokd = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_timestamp(other)
                n = len(arr)
                mpln__nmiei = bodo.utils.utils.alloc_type(n, lmhn__zsokd, (-1,)
                    )
                for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                    odv__wxup = bodo.libs.array_kernels.isna(arr, akpf__lmugn)
                    if odv__wxup:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(mpln__nmiei,
                                akpf__lmugn)
                        else:
                            mpln__nmiei[akpf__lmugn] = op(fill_value, other)
                    else:
                        mpln__nmiei[akpf__lmugn] = op(arr[akpf__lmugn], other)
                return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        lmhn__zsokd = lan__imoa.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and lmhn__zsokd == types.Array(
            types.bool_, 1, 'C'):
            lmhn__zsokd = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            vrbe__zdws = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            mpln__nmiei = bodo.utils.utils.alloc_type(n, lmhn__zsokd, (-1,))
            for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                odv__wxup = bodo.libs.array_kernels.isna(arr, akpf__lmugn)
                eylc__vbpm = bodo.libs.array_kernels.isna(vrbe__zdws,
                    akpf__lmugn)
                if odv__wxup and eylc__vbpm:
                    bodo.libs.array_kernels.setna(mpln__nmiei, akpf__lmugn)
                elif odv__wxup:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mpln__nmiei, akpf__lmugn)
                    else:
                        mpln__nmiei[akpf__lmugn] = op(fill_value,
                            vrbe__zdws[akpf__lmugn])
                elif eylc__vbpm:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mpln__nmiei, akpf__lmugn)
                    else:
                        mpln__nmiei[akpf__lmugn] = op(arr[akpf__lmugn],
                            fill_value)
                else:
                    mpln__nmiei[akpf__lmugn] = op(arr[akpf__lmugn],
                        vrbe__zdws[akpf__lmugn])
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
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
        lan__imoa = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            lmhn__zsokd = lan__imoa.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, IntegerArrayType
                ) and lmhn__zsokd == types.Array(types.bool_, 1, 'C'):
                lmhn__zsokd = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                mpln__nmiei = bodo.utils.utils.alloc_type(n, lmhn__zsokd, None)
                for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                    odv__wxup = bodo.libs.array_kernels.isna(arr, akpf__lmugn)
                    if odv__wxup:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(mpln__nmiei,
                                akpf__lmugn)
                        else:
                            mpln__nmiei[akpf__lmugn] = op(other, fill_value)
                    else:
                        mpln__nmiei[akpf__lmugn] = op(other, arr[akpf__lmugn])
                return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        lmhn__zsokd = lan__imoa.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, IntegerArrayType) and lmhn__zsokd == types.Array(
            types.bool_, 1, 'C'):
            lmhn__zsokd = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            vrbe__zdws = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            mpln__nmiei = bodo.utils.utils.alloc_type(n, lmhn__zsokd, None)
            for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                odv__wxup = bodo.libs.array_kernels.isna(arr, akpf__lmugn)
                eylc__vbpm = bodo.libs.array_kernels.isna(vrbe__zdws,
                    akpf__lmugn)
                mpln__nmiei[akpf__lmugn] = op(vrbe__zdws[akpf__lmugn], arr[
                    akpf__lmugn])
                if odv__wxup and eylc__vbpm:
                    bodo.libs.array_kernels.setna(mpln__nmiei, akpf__lmugn)
                elif odv__wxup:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mpln__nmiei, akpf__lmugn)
                    else:
                        mpln__nmiei[akpf__lmugn] = op(vrbe__zdws[
                            akpf__lmugn], fill_value)
                elif eylc__vbpm:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(mpln__nmiei, akpf__lmugn)
                    else:
                        mpln__nmiei[akpf__lmugn] = op(fill_value, arr[
                            akpf__lmugn])
                else:
                    mpln__nmiei[akpf__lmugn] = op(vrbe__zdws[akpf__lmugn],
                        arr[akpf__lmugn])
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
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
    for op, xsjbi__qkm in explicit_binop_funcs_two_ways.items():
        for name in xsjbi__qkm:
            hohzo__ihiv = create_explicit_binary_op_overload(op)
            ynnx__oyf = create_explicit_binary_reverse_op_overload(op)
            ofqe__fnmsu = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(hohzo__ihiv)
            overload_method(SeriesType, ofqe__fnmsu, no_unliteral=True)(
                ynnx__oyf)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        hohzo__ihiv = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(hohzo__ihiv)
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
                xqsv__bdusx = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                mpln__nmiei = dt64_arr_sub(arr, xqsv__bdusx)
                return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
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
                mpln__nmiei = np.empty(n, np.dtype('datetime64[ns]'))
                for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, akpf__lmugn):
                        bodo.libs.array_kernels.setna(mpln__nmiei, akpf__lmugn)
                        continue
                    ywbt__eusm = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[akpf__lmugn]))
                    zsp__fsj = op(ywbt__eusm, rhs)
                    mpln__nmiei[akpf__lmugn
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        zsp__fsj.value)
                return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
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
                    xqsv__bdusx = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    mpln__nmiei = op(arr, bodo.utils.conversion.
                        unbox_if_timestamp(xqsv__bdusx))
                    return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                xqsv__bdusx = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                mpln__nmiei = op(arr, xqsv__bdusx)
                return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    qgz__fnclo = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    mpln__nmiei = op(bodo.utils.conversion.
                        unbox_if_timestamp(qgz__fnclo), arr)
                    return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                qgz__fnclo = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                mpln__nmiei = op(qgz__fnclo, arr)
                return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        hohzo__ihiv = create_binary_op_overload(op)
        overload(op)(hohzo__ihiv)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    tfrp__oyodf = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, tfrp__oyodf)
        for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, akpf__lmugn
                ) or bodo.libs.array_kernels.isna(arg2, akpf__lmugn):
                bodo.libs.array_kernels.setna(S, akpf__lmugn)
                continue
            S[akpf__lmugn
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                akpf__lmugn]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[akpf__lmugn]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                vrbe__zdws = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, vrbe__zdws)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        hohzo__ihiv = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(hohzo__ihiv)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                mpln__nmiei = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        hohzo__ihiv = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(hohzo__ihiv)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    mpln__nmiei = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                        index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    vrbe__zdws = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    mpln__nmiei = ufunc(arr, vrbe__zdws)
                    return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    vrbe__zdws = bodo.hiframes.pd_series_ext.get_series_data(S2
                        )
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    mpln__nmiei = ufunc(arr, vrbe__zdws)
                    return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        hohzo__ihiv = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(hohzo__ihiv)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        kcwkr__zxjl = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.
            copy(),))
        esl__nikxw = np.arange(n),
        bodo.libs.timsort.sort(kcwkr__zxjl, 0, n, esl__nikxw)
        return esl__nikxw[0]
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
        whryx__vsna = get_overload_const_str(downcast)
        if whryx__vsna in ('integer', 'signed'):
            out_dtype = types.int64
        elif whryx__vsna == 'unsigned':
            out_dtype = types.uint64
        else:
            assert whryx__vsna == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            glh__wyg = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            mpln__nmiei = pd.to_numeric(glh__wyg, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                index, name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if out_dtype == types.float64:

        def to_numeric_float_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            htarw__ozbs = np.empty(n, np.float64)
            for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, akpf__lmugn):
                    bodo.libs.array_kernels.setna(htarw__ozbs, akpf__lmugn)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(htarw__ozbs,
                        akpf__lmugn, arg_a, akpf__lmugn)
            return htarw__ozbs
        return to_numeric_float_impl
    else:

        def to_numeric_int_impl(arg_a, errors='raise', downcast=None):
            numba.parfors.parfor.init_prange()
            n = len(arg_a)
            htarw__ozbs = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)
            for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arg_a, akpf__lmugn):
                    bodo.libs.array_kernels.setna(htarw__ozbs, akpf__lmugn)
                else:
                    bodo.libs.str_arr_ext.str_arr_item_to_numeric(htarw__ozbs,
                        akpf__lmugn, arg_a, akpf__lmugn)
            return htarw__ozbs
        return to_numeric_int_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        gfvid__hwi = if_series_to_array_type(args[0])
        if isinstance(gfvid__hwi, types.Array) and isinstance(gfvid__hwi.
            dtype, types.Integer):
            gfvid__hwi = types.Array(types.float64, 1, 'C')
        return gfvid__hwi(*args)


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
    kmcx__udbt = bodo.utils.utils.is_array_typ(x, True)
    zzicy__gkgs = bodo.utils.utils.is_array_typ(y, True)
    fpahm__tbnf = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        fpahm__tbnf += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if kmcx__udbt and not bodo.utils.utils.is_array_typ(x, False):
        fpahm__tbnf += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if zzicy__gkgs and not bodo.utils.utils.is_array_typ(y, False):
        fpahm__tbnf += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    fpahm__tbnf += '  n = len(condition)\n'
    moune__xrml = x.dtype if kmcx__udbt else types.unliteral(x)
    ffqm__bnwr = y.dtype if zzicy__gkgs else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        moune__xrml = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        ffqm__bnwr = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    bxut__vym = get_data(x)
    mnesn__hpop = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(esl__nikxw) for
        esl__nikxw in [bxut__vym, mnesn__hpop])
    if mnesn__hpop == types.none:
        if isinstance(moune__xrml, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif bxut__vym == mnesn__hpop and not is_nullable:
        out_dtype = dtype_to_array_type(moune__xrml)
    elif moune__xrml == string_type or ffqm__bnwr == string_type:
        out_dtype = bodo.string_array_type
    elif bxut__vym == bytes_type or (kmcx__udbt and moune__xrml == bytes_type
        ) and (mnesn__hpop == bytes_type or zzicy__gkgs and ffqm__bnwr ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(moune__xrml, bodo.PDCategoricalDtype):
        out_dtype = None
    elif moune__xrml in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(moune__xrml, 1, 'C')
    elif ffqm__bnwr in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(ffqm__bnwr, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(moune__xrml), numba.np.numpy_support.
            as_dtype(ffqm__bnwr)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(moune__xrml, bodo.PDCategoricalDtype):
        iddyr__ndbkm = 'x'
    else:
        iddyr__ndbkm = 'out_dtype'
    fpahm__tbnf += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {iddyr__ndbkm}, (-1,))\n')
    if isinstance(moune__xrml, bodo.PDCategoricalDtype):
        fpahm__tbnf += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        fpahm__tbnf += """  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)
"""
    fpahm__tbnf += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    fpahm__tbnf += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if kmcx__udbt:
        fpahm__tbnf += '      if bodo.libs.array_kernels.isna(x, j):\n'
        fpahm__tbnf += '        setna(out_arr, j)\n'
        fpahm__tbnf += '        continue\n'
    if isinstance(moune__xrml, bodo.PDCategoricalDtype):
        fpahm__tbnf += '      out_codes[j] = x_codes[j]\n'
    else:
        fpahm__tbnf += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('x[j]' if kmcx__udbt else 'x'))
    fpahm__tbnf += '    else:\n'
    if zzicy__gkgs:
        fpahm__tbnf += '      if bodo.libs.array_kernels.isna(y, j):\n'
        fpahm__tbnf += '        setna(out_arr, j)\n'
        fpahm__tbnf += '        continue\n'
    if mnesn__hpop == types.none:
        if isinstance(moune__xrml, bodo.PDCategoricalDtype):
            fpahm__tbnf += '      out_codes[j] = -1\n'
        else:
            fpahm__tbnf += '      setna(out_arr, j)\n'
    else:
        fpahm__tbnf += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_timestamp({})\n'
            .format('y[j]' if zzicy__gkgs else 'y'))
    fpahm__tbnf += '  return out_arr\n'
    nrf__glaf = {}
    exec(fpahm__tbnf, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, nrf__glaf)
    dunig__bsn = nrf__glaf['_impl']
    return dunig__bsn


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
        jiyta__tqvph = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(jiyta__tqvph, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(jiyta__tqvph):
            ejqb__pgjt = jiyta__tqvph.data.dtype
        else:
            ejqb__pgjt = jiyta__tqvph.dtype
        if isinstance(ejqb__pgjt, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        ccb__anh = jiyta__tqvph
    else:
        pkggh__imaf = []
        for jiyta__tqvph in choicelist:
            if not bodo.utils.utils.is_array_typ(jiyta__tqvph, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(jiyta__tqvph):
                ejqb__pgjt = jiyta__tqvph.data.dtype
            else:
                ejqb__pgjt = jiyta__tqvph.dtype
            if isinstance(ejqb__pgjt, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            pkggh__imaf.append(ejqb__pgjt)
        if not is_common_scalar_dtype(pkggh__imaf):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        ccb__anh = choicelist[0]
    if is_series_type(ccb__anh):
        ccb__anh = ccb__anh.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, ccb__anh.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(ccb__anh, types.Array) or isinstance(ccb__anh,
        BooleanArrayType) or isinstance(ccb__anh, IntegerArrayType) or bodo
        .utils.utils.is_array_typ(ccb__anh, False) and ccb__anh.dtype in [
        bodo.string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {ccb__anh} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    gzmg__lota = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        rwvm__hgbaa = choicelist.dtype
    else:
        bqy__fhho = False
        pkggh__imaf = []
        for jiyta__tqvph in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                jiyta__tqvph, 'numpy.select()')
            if is_nullable_type(jiyta__tqvph):
                bqy__fhho = True
            if is_series_type(jiyta__tqvph):
                ejqb__pgjt = jiyta__tqvph.data.dtype
            else:
                ejqb__pgjt = jiyta__tqvph.dtype
            if isinstance(ejqb__pgjt, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            pkggh__imaf.append(ejqb__pgjt)
        mchvw__xolq, llcxs__cuq = get_common_scalar_dtype(pkggh__imaf)
        if not llcxs__cuq:
            raise BodoError('Internal error in overload_np_select')
        jtcyl__vqyuc = dtype_to_array_type(mchvw__xolq)
        if bqy__fhho:
            jtcyl__vqyuc = to_nullable_type(jtcyl__vqyuc)
        rwvm__hgbaa = jtcyl__vqyuc
    if isinstance(rwvm__hgbaa, SeriesType):
        rwvm__hgbaa = rwvm__hgbaa.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        dnstc__xji = True
    else:
        dnstc__xji = False
    dyugm__mdi = False
    sgptf__plgw = False
    if dnstc__xji:
        if isinstance(rwvm__hgbaa.dtype, types.Number):
            pass
        elif rwvm__hgbaa.dtype == types.bool_:
            sgptf__plgw = True
        else:
            dyugm__mdi = True
            rwvm__hgbaa = to_nullable_type(rwvm__hgbaa)
    elif default == types.none or is_overload_constant_nan(default):
        dyugm__mdi = True
        rwvm__hgbaa = to_nullable_type(rwvm__hgbaa)
    fpahm__tbnf = 'def np_select_impl(condlist, choicelist, default=0):\n'
    fpahm__tbnf += '  if len(condlist) != len(choicelist):\n'
    fpahm__tbnf += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    fpahm__tbnf += '  output_len = len(choicelist[0])\n'
    fpahm__tbnf += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    fpahm__tbnf += '  for i in range(output_len):\n'
    if dyugm__mdi:
        fpahm__tbnf += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif sgptf__plgw:
        fpahm__tbnf += '    out[i] = False\n'
    else:
        fpahm__tbnf += '    out[i] = default\n'
    if gzmg__lota:
        fpahm__tbnf += '  for i in range(len(condlist) - 1, -1, -1):\n'
        fpahm__tbnf += '    cond = condlist[i]\n'
        fpahm__tbnf += '    choice = choicelist[i]\n'
        fpahm__tbnf += '    out = np.where(cond, choice, out)\n'
    else:
        for akpf__lmugn in range(len(choicelist) - 1, -1, -1):
            fpahm__tbnf += f'  cond = condlist[{akpf__lmugn}]\n'
            fpahm__tbnf += f'  choice = choicelist[{akpf__lmugn}]\n'
            fpahm__tbnf += f'  out = np.where(cond, choice, out)\n'
    fpahm__tbnf += '  return out'
    nrf__glaf = dict()
    exec(fpahm__tbnf, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': rwvm__hgbaa}, nrf__glaf)
    impl = nrf__glaf['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        mpln__nmiei = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    nnsql__vhjox = dict(subset=subset, keep=keep, inplace=inplace)
    bckl__matd = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', nnsql__vhjox,
        bckl__matd, package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        kvx__icrj = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (kvx__icrj,), uim__ypxos = bodo.libs.array_kernels.drop_duplicates((
            kvx__icrj,), index, 1)
        index = bodo.utils.conversion.index_from_array(uim__ypxos)
        return bodo.hiframes.pd_series_ext.init_series(kvx__icrj, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    pgtx__vwe = element_type(S.data)
    if not is_common_scalar_dtype([pgtx__vwe, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([pgtx__vwe, right]):
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
        mpln__nmiei = np.empty(n, np.bool_)
        for akpf__lmugn in numba.parfors.parfor.internal_prange(n):
            hpqjz__buj = bodo.utils.conversion.box_if_dt64(arr[akpf__lmugn])
            if inclusive == 'both':
                mpln__nmiei[akpf__lmugn
                    ] = hpqjz__buj <= right and hpqjz__buj >= left
            else:
                mpln__nmiei[akpf__lmugn
                    ] = hpqjz__buj < right and hpqjz__buj > left
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei, index, name
            )
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    nnsql__vhjox = dict(axis=axis)
    bckl__matd = dict(axis=None)
    check_unsupported_args('Series.repeat', nnsql__vhjox, bckl__matd,
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
            uim__ypxos = bodo.utils.conversion.index_to_array(index)
            mpln__nmiei = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            ixcca__umb = bodo.libs.array_kernels.repeat_kernel(uim__ypxos,
                repeats)
            jzw__rary = bodo.utils.conversion.index_from_array(ixcca__umb)
            return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
                jzw__rary, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        uim__ypxos = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        mpln__nmiei = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        ixcca__umb = bodo.libs.array_kernels.repeat_kernel(uim__ypxos, repeats)
        jzw__rary = bodo.utils.conversion.index_from_array(ixcca__umb)
        return bodo.hiframes.pd_series_ext.init_series(mpln__nmiei,
            jzw__rary, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        esl__nikxw = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(esl__nikxw)
        htnb__gjq = {}
        for akpf__lmugn in range(n):
            hpqjz__buj = bodo.utils.conversion.box_if_dt64(esl__nikxw[
                akpf__lmugn])
            htnb__gjq[index[akpf__lmugn]] = hpqjz__buj
        return htnb__gjq
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    qph__cjzk = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            pqkqr__hkgs = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(qph__cjzk)
    elif is_literal_type(name):
        pqkqr__hkgs = get_literal_value(name)
    else:
        raise_bodo_error(qph__cjzk)
    pqkqr__hkgs = 0 if pqkqr__hkgs is None else pqkqr__hkgs

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            (pqkqr__hkgs,))
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
