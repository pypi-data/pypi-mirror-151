"""
Implementation of DataFrame attributes and methods using overload.
"""
import operator
import re
import warnings
from collections import namedtuple
from typing import Tuple
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, ir, types
from numba.core.imputils import RefType, impl_ret_borrowed, impl_ret_new_ref, iternext_impl, lower_builtin
from numba.core.ir_utils import mk_unique_var, next_label
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_getattr, models, overload, overload_attribute, overload_method, register_model, type_callable
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import _no_input, datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported, handle_inplace_df_type_change
from bodo.hiframes.pd_index_ext import DatetimeIndexType, RangeIndexType, StringIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array, boolean_dtype
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils.transform import bodo_types_with_params, gen_const_tup, no_side_effect_call_tuples
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, dtype_to_array_type, ensure_constant_arg, ensure_constant_values, get_index_data_arr_types, get_index_names, get_literal_value, get_nullable_and_non_nullable_types, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_overload_constant_dict, get_overload_constant_series, is_common_scalar_dtype, is_literal_type, is_overload_bool, is_overload_bool_list, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_series, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, parse_dtype, raise_bodo_error, unliteral_val
from bodo.utils.utils import is_array_typ


@overload_attribute(DataFrameType, 'index', inline='always')
def overload_dataframe_index(df):
    return lambda df: bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)


def generate_col_to_index_func_text(col_names: Tuple):
    if all(isinstance(a, str) for a in col_names) or all(isinstance(a,
        bytes) for a in col_names):
        alht__spqr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({alht__spqr})\n'
            )
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    drcci__rvyym = 'def impl(df):\n'
    if df.has_runtime_cols:
        drcci__rvyym += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        fdj__pgqq = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        drcci__rvyym += f'  return {fdj__pgqq}'
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo}, ukhx__aqlzo)
    impl = ukhx__aqlzo['impl']
    return impl


@overload_attribute(DataFrameType, 'values')
def overload_dataframe_values(df):
    check_runtime_cols_unsupported(df, 'DataFrame.values')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.values')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.values: only supported for dataframes containing numeric values'
            )
    ajxgl__wnzb = len(df.columns)
    sdzx__eff = set(i for i in range(ajxgl__wnzb) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in sdzx__eff else '') for i in
        range(ajxgl__wnzb))
    drcci__rvyym = 'def f(df):\n'.format()
    drcci__rvyym += '    return np.stack(({},), 1)\n'.format(data_args)
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo, 'np': np}, ukhx__aqlzo)
    uwehm__kdjb = ukhx__aqlzo['f']
    return uwehm__kdjb


@overload_method(DataFrameType, 'to_numpy', inline='always', no_unliteral=True)
def overload_dataframe_to_numpy(df, dtype=None, copy=False, na_value=_no_input
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.to_numpy()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.to_numpy()')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.to_numpy(): only supported for dataframes containing numeric values'
            )
    mlc__nacu = {'dtype': dtype, 'na_value': na_value}
    fwlnm__tsyl = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', mlc__nacu, fwlnm__tsyl,
        package_name='pandas', module_name='DataFrame')

    def impl(df, dtype=None, copy=False, na_value=_no_input):
        return df.values
    return impl


@overload_attribute(DataFrameType, 'ndim', inline='always')
def overload_dataframe_ndim(df):
    return lambda df: 2


@overload_attribute(DataFrameType, 'size')
def overload_dataframe_size(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            yay__clv = bodo.hiframes.table.compute_num_runtime_columns(t)
            return yay__clv * len(t)
        return impl
    ncols = len(df.columns)
    return lambda df: ncols * len(df)


@lower_getattr(DataFrameType, 'shape')
def lower_dataframe_shape(context, builder, typ, val):
    impl = overload_dataframe_shape(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def overload_dataframe_shape(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            yay__clv = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), yay__clv
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    drcci__rvyym = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    beyh__kzomw = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    drcci__rvyym += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{beyh__kzomw}), {index}, None)
"""
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo}, ukhx__aqlzo)
    impl = ukhx__aqlzo['impl']
    return impl


@overload_attribute(DataFrameType, 'empty')
def overload_dataframe_empty(df):
    check_runtime_cols_unsupported(df, 'DataFrame.empty')
    if len(df.columns) == 0:
        return lambda df: True
    return lambda df: len(df) == 0


@overload_method(DataFrameType, 'assign', no_unliteral=True)
def overload_dataframe_assign(df, **kwargs):
    check_runtime_cols_unsupported(df, 'DataFrame.assign()')
    raise_bodo_error('Invalid df.assign() call')


@overload_method(DataFrameType, 'insert', no_unliteral=True)
def overload_dataframe_insert(df, loc, column, value, allow_duplicates=False):
    check_runtime_cols_unsupported(df, 'DataFrame.insert()')
    raise_bodo_error('Invalid df.insert() call')


def _get_dtype_str(dtype):
    if isinstance(dtype, types.Function):
        if dtype.key[0] == str:
            return "'str'"
        elif dtype.key[0] == float:
            return 'float'
        elif dtype.key[0] == int:
            return 'int'
        elif dtype.key[0] == bool:
            return 'bool'
        else:
            raise BodoError(f'invalid dtype: {dtype}')
    if isinstance(dtype, types.DTypeSpec):
        dtype = dtype.dtype
    if isinstance(dtype, types.functions.NumberClass):
        return f"'{dtype.key}'"
    if isinstance(dtype, types.PyObject) or dtype in (object, 'object'):
        return "'object'"
    if dtype in (bodo.libs.str_arr_ext.string_dtype, pd.StringDtype()):
        return 'str'
    return f"'{dtype}'"


@overload_method(DataFrameType, 'astype', inline='always', no_unliteral=True)
def overload_dataframe_astype(df, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True, _bodo_object_typeref=None):
    check_runtime_cols_unsupported(df, 'DataFrame.astype()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.astype()')
    mlc__nacu = {'copy': copy, 'errors': errors}
    fwlnm__tsyl = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', mlc__nacu, fwlnm__tsyl,
        package_name='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        gqt__bsq = _bodo_object_typeref.instance_type
        assert isinstance(gqt__bsq, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        extra_globals = {}
        tquv__utc = {}
        for i, name in enumerate(gqt__bsq.columns):
            arr_typ = gqt__bsq.data[i]
            if isinstance(arr_typ, IntegerArrayType):
                zfsfp__aay = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
            elif arr_typ == boolean_array:
                zfsfp__aay = boolean_dtype
            else:
                zfsfp__aay = arr_typ.dtype
            extra_globals[f'_bodo_schema{i}'] = zfsfp__aay
            tquv__utc[name] = f'_bodo_schema{i}'
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {tquv__utc[utksr__kqk]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if utksr__kqk in tquv__utc else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, utksr__kqk in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        zcoxz__ovr = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(zcoxz__ovr[utksr__kqk])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if utksr__kqk in zcoxz__ovr else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, utksr__kqk in enumerate(df.columns))
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    header = """def impl(df, dtype, copy=True, errors='raise', _bodo_nan_to_str=True, _bodo_object_typeref=None):
"""
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'copy', inline='always', no_unliteral=True)
def overload_dataframe_copy(df, deep=True):
    check_runtime_cols_unsupported(df, 'DataFrame.copy()')
    qhjq__xfa = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(deep):
            qhjq__xfa.append(arr + '.copy()')
        elif is_overload_false(deep):
            qhjq__xfa.append(arr)
        else:
            qhjq__xfa.append(f'{arr}.copy() if deep else {arr}')
    header = 'def impl(df, deep=True):\n'
    return _gen_init_df(header, df.columns, ', '.join(qhjq__xfa))


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    mlc__nacu = {'index': index, 'level': level, 'errors': errors}
    fwlnm__tsyl = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', mlc__nacu, fwlnm__tsyl,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.rename(): 'inplace' keyword only supports boolean constant assignment"
            )
    if not is_overload_none(mapper):
        if not is_overload_none(columns):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'mapper' and 'columns'"
                )
        if not (is_overload_constant_int(axis) and get_overload_const_int(
            axis) == 1):
            raise BodoError(
                "DataFrame.rename(): 'mapper' only supported with axis=1")
        if not is_overload_constant_dict(mapper):
            raise_bodo_error(
                "'mapper' argument to DataFrame.rename() should be a constant dictionary"
                )
        duizr__shuz = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        duizr__shuz = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    jfmy__yyot = [duizr__shuz.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))]
    qhjq__xfa = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(copy):
            qhjq__xfa.append(arr + '.copy()')
        elif is_overload_false(copy):
            qhjq__xfa.append(arr)
        else:
            qhjq__xfa.append(f'{arr}.copy() if copy else {arr}')
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    return _gen_init_df(header, jfmy__yyot, ', '.join(qhjq__xfa))


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    jwp__wguco = not is_overload_none(items)
    nbmi__zhvp = not is_overload_none(like)
    twu__wyxad = not is_overload_none(regex)
    kxihw__ejgp = jwp__wguco ^ nbmi__zhvp ^ twu__wyxad
    uwnlp__yrad = not (jwp__wguco or nbmi__zhvp or twu__wyxad)
    if uwnlp__yrad:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not kxihw__ejgp:
        raise BodoError(
            'DataFrame.filter(): keyword arguments `items`, `like`, and `regex` are mutually exclusive'
            )
    if is_overload_none(axis):
        axis = 'columns'
    if is_overload_constant_str(axis):
        axis = get_overload_const_str(axis)
        if axis not in {'index', 'columns'}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either "index" or "columns" if string'
                )
        jgse__dvfk = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        jgse__dvfk = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert jgse__dvfk in {0, 1}
    drcci__rvyym = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if jgse__dvfk == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if jgse__dvfk == 1:
        vyu__xpp = []
        cmc__qniz = []
        lwt__vveq = []
        if jwp__wguco:
            if is_overload_constant_list(items):
                slgyn__dydza = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if nbmi__zhvp:
            if is_overload_constant_str(like):
                lxb__lsdx = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if twu__wyxad:
            if is_overload_constant_str(regex):
                jagjm__srcgw = get_overload_const_str(regex)
                jreww__vbhnh = re.compile(jagjm__srcgw)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, utksr__kqk in enumerate(df.columns):
            if not is_overload_none(items
                ) and utksr__kqk in slgyn__dydza or not is_overload_none(like
                ) and lxb__lsdx in str(utksr__kqk) or not is_overload_none(
                regex) and jreww__vbhnh.search(str(utksr__kqk)):
                cmc__qniz.append(utksr__kqk)
                lwt__vveq.append(i)
        for i in lwt__vveq:
            var_name = f'data_{i}'
            vyu__xpp.append(var_name)
            drcci__rvyym += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(vyu__xpp)
        return _gen_init_df(drcci__rvyym, cmc__qniz, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        hic__bna = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([hic__bna] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': hic__bna}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


@overload_method(DataFrameType, 'select_dtypes', inline='always',
    no_unliteral=True)
def overload_dataframe_select_dtypes(df, include=None, exclude=None):
    check_runtime_cols_unsupported(df, 'DataFrame.select_dtypes')
    reybk__kfm = is_overload_none(include)
    idww__kpknw = is_overload_none(exclude)
    uzz__zhb = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if reybk__kfm and idww__kpknw:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not reybk__kfm:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            ceyb__nct = [dtype_to_array_type(parse_dtype(elem, uzz__zhb)) for
                elem in include]
        elif is_legal_input(include):
            ceyb__nct = [dtype_to_array_type(parse_dtype(include, uzz__zhb))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        ceyb__nct = get_nullable_and_non_nullable_types(ceyb__nct)
        xpu__jtip = tuple(utksr__kqk for i, utksr__kqk in enumerate(df.
            columns) if df.data[i] in ceyb__nct)
    else:
        xpu__jtip = df.columns
    if not idww__kpknw:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            rgitv__dfm = [dtype_to_array_type(parse_dtype(elem, uzz__zhb)) for
                elem in exclude]
        elif is_legal_input(exclude):
            rgitv__dfm = [dtype_to_array_type(parse_dtype(exclude, uzz__zhb))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        rgitv__dfm = get_nullable_and_non_nullable_types(rgitv__dfm)
        xpu__jtip = tuple(utksr__kqk for utksr__kqk in xpu__jtip if df.data
            [df.columns.index(utksr__kqk)] not in rgitv__dfm)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(utksr__kqk)})'
         for utksr__kqk in xpu__jtip)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, xpu__jtip, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        hic__bna = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([hic__bna] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': hic__bna}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'~bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})) == False'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals, out_df_type=out_df_type)


def overload_dataframe_head(df, n=5):
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:n]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:n]'
    return _gen_init_df(header, df.columns, data_args, index)


@lower_builtin('df.head', DataFrameType, types.Integer)
@lower_builtin('df.head', DataFrameType, types.Omitted)
def dataframe_head_lower(context, builder, sig, args):
    impl = overload_dataframe_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'tail', inline='always', no_unliteral=True)
def overload_dataframe_tail(df, n=5):
    check_runtime_cols_unsupported(df, 'DataFrame.tail()')
    if not is_overload_int(n):
        raise BodoError("Dataframe.tail(): 'n' must be an Integer")
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[m:]' for
        i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    header += '  m = bodo.hiframes.series_impl.tail_slice(len(df), n)\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[m:]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'first', inline='always', no_unliteral=True)
def overload_dataframe_first(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.first()')
    mxd__rqxpb = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in mxd__rqxpb:
        raise BodoError(
            "DataFrame.first(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.first()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:valid_entries]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:valid_entries]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    start_date = df_index[0]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, start_date, False)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'last', inline='always', no_unliteral=True)
def overload_dataframe_last(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.last()')
    mxd__rqxpb = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in mxd__rqxpb:
        raise BodoError(
            "DataFrame.last(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.last()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[len(df)-valid_entries:]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[len(df)-valid_entries:]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    final_date = df_index[-1]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, final_date, True)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'to_string', no_unliteral=True)
def to_string_overload(df, buf=None, columns=None, col_space=None, header=
    True, index=True, na_rep='NaN', formatters=None, float_format=None,
    sparsify=None, index_names=True, justify=None, max_rows=None, min_rows=
    None, max_cols=None, show_dimensions=False, decimal='.', line_width=
    None, max_colwidth=None, encoding=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_string()')

    def impl(df, buf=None, columns=None, col_space=None, header=True, index
        =True, na_rep='NaN', formatters=None, float_format=None, sparsify=
        None, index_names=True, justify=None, max_rows=None, min_rows=None,
        max_cols=None, show_dimensions=False, decimal='.', line_width=None,
        max_colwidth=None, encoding=None):
        with numba.objmode(res='string'):
            res = df.to_string(buf=buf, columns=columns, col_space=
                col_space, header=header, index=index, na_rep=na_rep,
                formatters=formatters, float_format=float_format, sparsify=
                sparsify, index_names=index_names, justify=justify,
                max_rows=max_rows, min_rows=min_rows, max_cols=max_cols,
                show_dimensions=show_dimensions, decimal=decimal,
                line_width=line_width, max_colwidth=max_colwidth, encoding=
                encoding)
        return res
    return impl


@overload_method(DataFrameType, 'isin', inline='always', no_unliteral=True)
def overload_dataframe_isin(df, values):
    check_runtime_cols_unsupported(df, 'DataFrame.isin()')
    from bodo.utils.typing import is_iterable_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.isin()')
    drcci__rvyym = 'def impl(df, values):\n'
    svoni__fxf = {}
    irc__mdgl = False
    if isinstance(values, DataFrameType):
        irc__mdgl = True
        for i, utksr__kqk in enumerate(df.columns):
            if utksr__kqk in values.columns:
                vnfh__fnqhb = 'val{}'.format(i)
                drcci__rvyym += (
                    """  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {})
"""
                    .format(vnfh__fnqhb, values.columns.index(utksr__kqk)))
                svoni__fxf[utksr__kqk] = vnfh__fnqhb
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        svoni__fxf = {utksr__kqk: 'values' for utksr__kqk in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        vnfh__fnqhb = 'data{}'.format(i)
        drcci__rvyym += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(vnfh__fnqhb, i))
        data.append(vnfh__fnqhb)
    kak__xhuqe = ['out{}'.format(i) for i in range(len(df.columns))]
    odfd__uhvq = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    rkb__avgc = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    qra__sjnx = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, dhz__dag) in enumerate(zip(df.columns, data)):
        if cname in svoni__fxf:
            gwn__verv = svoni__fxf[cname]
            if irc__mdgl:
                drcci__rvyym += odfd__uhvq.format(dhz__dag, gwn__verv,
                    kak__xhuqe[i])
            else:
                drcci__rvyym += rkb__avgc.format(dhz__dag, gwn__verv,
                    kak__xhuqe[i])
        else:
            drcci__rvyym += qra__sjnx.format(kak__xhuqe[i])
    return _gen_init_df(drcci__rvyym, df.columns, ','.join(kak__xhuqe))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    ajxgl__wnzb = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(ajxgl__wnzb))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    kmbt__hobdj = [utksr__kqk for utksr__kqk, pgoa__ohwe in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(pgoa__ohwe.
        dtype)]
    assert len(kmbt__hobdj) != 0
    bghp__yugdm = ''
    if not any(pgoa__ohwe == types.float64 for pgoa__ohwe in df.data):
        bghp__yugdm = '.astype(np.float64)'
    wdf__lqs = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(utksr__kqk), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(utksr__kqk)], IntegerArrayType) or
        df.data[df.columns.index(utksr__kqk)] == boolean_array else '') for
        utksr__kqk in kmbt__hobdj)
    lvz__lizx = 'np.stack(({},), 1){}'.format(wdf__lqs, bghp__yugdm)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        kmbt__hobdj)))
    index = f'{generate_col_to_index_func_text(kmbt__hobdj)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(lvz__lizx)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, kmbt__hobdj, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    zdnpn__vnd = dict(ddof=ddof)
    dpg__lsg = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    mhz__ejb = '1' if is_overload_none(min_periods) else 'min_periods'
    kmbt__hobdj = [utksr__kqk for utksr__kqk, pgoa__ohwe in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(pgoa__ohwe.
        dtype)]
    if len(kmbt__hobdj) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    bghp__yugdm = ''
    if not any(pgoa__ohwe == types.float64 for pgoa__ohwe in df.data):
        bghp__yugdm = '.astype(np.float64)'
    wdf__lqs = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(utksr__kqk), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(utksr__kqk)], IntegerArrayType) or
        df.data[df.columns.index(utksr__kqk)] == boolean_array else '') for
        utksr__kqk in kmbt__hobdj)
    lvz__lizx = 'np.stack(({},), 1){}'.format(wdf__lqs, bghp__yugdm)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        kmbt__hobdj)))
    index = f'pd.Index({kmbt__hobdj})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(lvz__lizx)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        mhz__ejb)
    return _gen_init_df(header, kmbt__hobdj, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    zdnpn__vnd = dict(axis=axis, level=level, numeric_only=numeric_only)
    dpg__lsg = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    drcci__rvyym = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    drcci__rvyym += '  data = np.array([{}])\n'.format(data_args)
    fdj__pgqq = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    drcci__rvyym += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {fdj__pgqq})\n'
        )
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo, 'np': np}, ukhx__aqlzo)
    impl = ukhx__aqlzo['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    zdnpn__vnd = dict(axis=axis)
    dpg__lsg = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    drcci__rvyym = 'def impl(df, axis=0, dropna=True):\n'
    drcci__rvyym += '  data = np.asarray(({},))\n'.format(data_args)
    fdj__pgqq = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(df
        .columns)
    drcci__rvyym += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {fdj__pgqq})\n'
        )
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo, 'np': np}, ukhx__aqlzo)
    impl = ukhx__aqlzo['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    zdnpn__vnd = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    dpg__lsg = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    zdnpn__vnd = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    dpg__lsg = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    zdnpn__vnd = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    dpg__lsg = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    zdnpn__vnd = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    dpg__lsg = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    zdnpn__vnd = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    dpg__lsg = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    zdnpn__vnd = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    dpg__lsg = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    zdnpn__vnd = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    dpg__lsg = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    zdnpn__vnd = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    dpg__lsg = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    zdnpn__vnd = dict(numeric_only=numeric_only, interpolation=interpolation)
    dpg__lsg = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    zdnpn__vnd = dict(axis=axis, skipna=skipna)
    dpg__lsg = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for pxtf__rycff in df.data:
        if not (bodo.utils.utils.is_np_array_typ(pxtf__rycff) and (
            pxtf__rycff.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(pxtf__rycff.dtype, (types.Number, types.Boolean))) or
            isinstance(pxtf__rycff, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or pxtf__rycff in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {pxtf__rycff} not supported.'
                )
        if isinstance(pxtf__rycff, bodo.CategoricalArrayType
            ) and not pxtf__rycff.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    zdnpn__vnd = dict(axis=axis, skipna=skipna)
    dpg__lsg = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for pxtf__rycff in df.data:
        if not (bodo.utils.utils.is_np_array_typ(pxtf__rycff) and (
            pxtf__rycff.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(pxtf__rycff.dtype, (types.Number, types.Boolean))) or
            isinstance(pxtf__rycff, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or pxtf__rycff in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {pxtf__rycff} not supported.'
                )
        if isinstance(pxtf__rycff, bodo.CategoricalArrayType
            ) and not pxtf__rycff.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmin(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmin', axis=axis)


@overload_method(DataFrameType, 'infer_objects', inline='always')
def overload_dataframe_infer_objects(df):
    check_runtime_cols_unsupported(df, 'DataFrame.infer_objects()')
    return lambda df: df.copy()


def _gen_reduce_impl(df, func_name, args=None, axis=None):
    args = '' if is_overload_none(args) else args
    if is_overload_none(axis):
        axis = 0
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
    else:
        raise_bodo_error(
            f'DataFrame.{func_name}: axis must be a constant Integer')
    assert axis in (0, 1), f'invalid axis argument for DataFrame.{func_name}'
    if func_name in ('idxmax', 'idxmin'):
        out_colnames = df.columns
    else:
        kmbt__hobdj = tuple(utksr__kqk for utksr__kqk, pgoa__ohwe in zip(df
            .columns, df.data) if bodo.utils.typing.
            _is_pandas_numeric_dtype(pgoa__ohwe.dtype))
        out_colnames = kmbt__hobdj
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            shb__enx = [numba.np.numpy_support.as_dtype(df.data[df.columns.
                index(utksr__kqk)].dtype) for utksr__kqk in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(shb__enx, []))
    except NotImplementedError as sgdlu__bhso:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    hqy__yryi = ''
    if func_name in ('sum', 'prod'):
        hqy__yryi = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    drcci__rvyym = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, hqy__yryi))
    if func_name == 'quantile':
        drcci__rvyym = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        drcci__rvyym = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        drcci__rvyym += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        drcci__rvyym += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        ukhx__aqlzo)
    impl = ukhx__aqlzo['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    ashr__xfdrh = ''
    if func_name in ('min', 'max'):
        ashr__xfdrh = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        ashr__xfdrh = ', dtype=np.float32'
    rgdb__fmiqw = f'bodo.libs.array_ops.array_op_{func_name}'
    oxryq__hzuu = ''
    if func_name in ['sum', 'prod']:
        oxryq__hzuu = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        oxryq__hzuu = 'index'
    elif func_name == 'quantile':
        oxryq__hzuu = 'q'
    elif func_name in ['std', 'var']:
        oxryq__hzuu = 'True, ddof'
    elif func_name == 'median':
        oxryq__hzuu = 'True'
    data_args = ', '.join(
        f'{rgdb__fmiqw}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(utksr__kqk)}), {oxryq__hzuu})'
         for utksr__kqk in out_colnames)
    drcci__rvyym = ''
    if func_name in ('idxmax', 'idxmin'):
        drcci__rvyym += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        drcci__rvyym += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        drcci__rvyym += '  data = np.asarray(({},){})\n'.format(data_args,
            ashr__xfdrh)
    drcci__rvyym += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return drcci__rvyym


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    qtk__mhar = [df_type.columns.index(utksr__kqk) for utksr__kqk in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in qtk__mhar)
    kyfb__yfd = '\n        '.join(f'row[{i}] = arr_{qtk__mhar[i]}[i]' for i in
        range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    afq__hrgte = f'len(arr_{qtk__mhar[0]})'
    pyrhv__eahq = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum':
        'np.nansum', 'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in pyrhv__eahq:
        jviej__grbgl = pyrhv__eahq[func_name]
        ake__qbqtc = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        drcci__rvyym = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {afq__hrgte}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{ake__qbqtc})
    for i in numba.parfors.parfor.internal_prange(n):
        {kyfb__yfd}
        A[i] = {jviej__grbgl}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return drcci__rvyym
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    zdnpn__vnd = dict(fill_method=fill_method, limit=limit, freq=freq)
    dpg__lsg = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.pct_change()')
    data_args = ', '.join(
        f'bodo.hiframes.rolling.pct_change(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = (
        "def impl(df, periods=1, fill_method='pad', limit=None, freq=None):\n")
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumprod', inline='always', no_unliteral=True)
def overload_dataframe_cumprod(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumprod()')
    zdnpn__vnd = dict(axis=axis, skipna=skipna)
    dpg__lsg = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumprod()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumprod()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumsum', inline='always', no_unliteral=True)
def overload_dataframe_cumsum(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumsum()')
    zdnpn__vnd = dict(skipna=skipna)
    dpg__lsg = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumsum()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumsum()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


def _is_describe_type(data):
    return isinstance(data, IntegerArrayType) or isinstance(data, types.Array
        ) and isinstance(data.dtype, types.Number
        ) or data.dtype == bodo.datetime64ns


@overload_method(DataFrameType, 'describe', inline='always', no_unliteral=True)
def overload_dataframe_describe(df, percentiles=None, include=None, exclude
    =None, datetime_is_numeric=True):
    check_runtime_cols_unsupported(df, 'DataFrame.describe()')
    zdnpn__vnd = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    dpg__lsg = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    kmbt__hobdj = [utksr__kqk for utksr__kqk, pgoa__ohwe in zip(df.columns,
        df.data) if _is_describe_type(pgoa__ohwe)]
    if len(kmbt__hobdj) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    czjy__ora = sum(df.data[df.columns.index(utksr__kqk)].dtype == bodo.
        datetime64ns for utksr__kqk in kmbt__hobdj)

    def _get_describe(col_ind):
        yfbm__jsal = df.data[col_ind].dtype == bodo.datetime64ns
        if czjy__ora and czjy__ora != len(kmbt__hobdj):
            if yfbm__jsal:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for utksr__kqk in kmbt__hobdj:
        col_ind = df.columns.index(utksr__kqk)
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.columns.index(utksr__kqk)) for
        utksr__kqk in kmbt__hobdj)
    qtho__uawrj = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if czjy__ora == len(kmbt__hobdj):
        qtho__uawrj = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif czjy__ora:
        qtho__uawrj = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({qtho__uawrj})'
    return _gen_init_df(header, kmbt__hobdj, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    zdnpn__vnd = dict(axis=axis, convert=convert, is_copy=is_copy)
    dpg__lsg = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[indices_t]'
        .format(i) for i in range(len(df.columns)))
    header = 'def impl(df, indices, axis=0, convert=None, is_copy=True):\n'
    header += (
        '  indices_t = bodo.utils.conversion.coerce_to_ndarray(indices)\n')
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[indices_t]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'shift', inline='always', no_unliteral=True)
def overload_dataframe_shift(df, periods=1, freq=None, axis=0, fill_value=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.shift()')
    zdnpn__vnd = dict(freq=freq, axis=axis, fill_value=fill_value)
    dpg__lsg = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for heef__inpp in df.data:
        if not is_supported_shift_array_type(heef__inpp):
            raise BodoError(
                f'Dataframe.shift() column input type {heef__inpp.dtype} not supported yet.'
                )
    if not is_overload_int(periods):
        raise BodoError(
            "DataFrame.shift(): 'periods' input must be an integer.")
    data_args = ', '.join(
        f'bodo.hiframes.rolling.shift(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = 'def impl(df, periods=1, freq=None, axis=0, fill_value=None):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'diff', inline='always', no_unliteral=True)
def overload_dataframe_diff(df, periods=1, axis=0):
    check_runtime_cols_unsupported(df, 'DataFrame.diff()')
    zdnpn__vnd = dict(axis=axis)
    dpg__lsg = dict(axis=0)
    check_unsupported_args('DataFrame.diff', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for heef__inpp in df.data:
        if not (isinstance(heef__inpp, types.Array) and (isinstance(
            heef__inpp.dtype, types.Number) or heef__inpp.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {heef__inpp.dtype} not supported.'
                )
    if not is_overload_int(periods):
        raise BodoError("DataFrame.diff(): 'periods' input must be an integer."
            )
    header = 'def impl(df, periods=1, axis= 0):\n'
    for i in range(len(df.columns)):
        header += (
            f'  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    data_args = ', '.join(
        f'bodo.hiframes.series_impl.dt64_arr_sub(data_{i}, bodo.hiframes.rolling.shift(data_{i}, periods, False))'
         if df.data[i] == types.Array(bodo.datetime64ns, 1, 'C') else
        f'data_{i} - bodo.hiframes.rolling.shift(data_{i}, periods, False)' for
        i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'explode', inline='always', no_unliteral=True)
def overload_dataframe_explode(df, column, ignore_index=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.explode()')
    hhuyp__mgp = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(hhuyp__mgp)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        blo__wkf = get_overload_const_list(column)
    else:
        blo__wkf = [get_literal_value(column)]
    vzsy__jmh = {utksr__kqk: i for i, utksr__kqk in enumerate(df.columns)}
    pdk__tvisg = [vzsy__jmh[utksr__kqk] for utksr__kqk in blo__wkf]
    for i in pdk__tvisg:
        if not isinstance(df.data[i], ArrayItemArrayType) and df.data[i
            ].dtype != string_array_split_view_type:
            raise BodoError(
                f'DataFrame.explode(): columns must have array-like entries')
    n = len(df.columns)
    header = 'def impl(df, column, ignore_index=False):\n'
    header += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    header += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    for i in range(n):
        header += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    header += (
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{pdk__tvisg[0]})\n'
        )
    for i in range(n):
        if i in pdk__tvisg:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.explode_no_index(data{i}, counts)\n'
                )
        else:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.repeat_kernel(data{i}, counts)\n'
                )
    header += (
        '  new_index = bodo.libs.array_kernels.repeat_kernel(index_arr, counts)\n'
        )
    data_args = ', '.join(f'out_data{i}' for i in range(n))
    index = 'bodo.utils.conversion.convert_to_index(new_index)'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'set_index', inline='always', no_unliteral=True
    )
def overload_dataframe_set_index(df, keys, drop=True, append=False, inplace
    =False, verify_integrity=False):
    check_runtime_cols_unsupported(df, 'DataFrame.set_index()')
    mlc__nacu = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    fwlnm__tsyl = {'inplace': False, 'append': False, 'verify_integrity': False
        }
    check_unsupported_args('DataFrame.set_index', mlc__nacu, fwlnm__tsyl,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_str(keys):
        raise_bodo_error(
            "DataFrame.set_index(): 'keys' must be a constant string")
    col_name = get_overload_const_str(keys)
    col_ind = df.columns.index(col_name)
    header = """def impl(df, keys, drop=True, append=False, inplace=False, verify_integrity=False):
"""
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'.format(
        i) for i in range(len(df.columns)) if i != col_ind)
    columns = tuple(utksr__kqk for utksr__kqk in df.columns if utksr__kqk !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    mlc__nacu = {'inplace': inplace}
    fwlnm__tsyl = {'inplace': False}
    check_unsupported_args('query', mlc__nacu, fwlnm__tsyl, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        jbpl__syzu = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[jbpl__syzu]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    mlc__nacu = {'subset': subset, 'keep': keep}
    fwlnm__tsyl = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', mlc__nacu, fwlnm__tsyl,
        package_name='pandas', module_name='DataFrame')
    ajxgl__wnzb = len(df.columns)
    drcci__rvyym = "def impl(df, subset=None, keep='first'):\n"
    for i in range(ajxgl__wnzb):
        drcci__rvyym += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    kxxyl__hiayh = ', '.join(f'data_{i}' for i in range(ajxgl__wnzb))
    kxxyl__hiayh += ',' if ajxgl__wnzb == 1 else ''
    drcci__rvyym += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({kxxyl__hiayh}))\n'
        )
    drcci__rvyym += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    drcci__rvyym += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo}, ukhx__aqlzo)
    impl = ukhx__aqlzo['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    mlc__nacu = {'keep': keep, 'inplace': inplace, 'ignore_index': ignore_index
        }
    fwlnm__tsyl = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    jxx__rqgd = []
    if is_overload_constant_list(subset):
        jxx__rqgd = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        jxx__rqgd = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        jxx__rqgd = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    uyn__wzkgg = []
    for col_name in jxx__rqgd:
        if col_name not in df.columns:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        uyn__wzkgg.append(df.columns.index(col_name))
    check_unsupported_args('DataFrame.drop_duplicates', mlc__nacu,
        fwlnm__tsyl, package_name='pandas', module_name='DataFrame')
    eie__tai = []
    if uyn__wzkgg:
        for mdsg__brweo in uyn__wzkgg:
            if isinstance(df.data[mdsg__brweo], bodo.MapArrayType):
                eie__tai.append(df.columns[mdsg__brweo])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                eie__tai.append(col_name)
    if eie__tai:
        raise BodoError(f'DataFrame.drop_duplicates(): Columns {eie__tai} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    ajxgl__wnzb = len(df.columns)
    fywmv__qqaxf = ['data_{}'.format(i) for i in uyn__wzkgg]
    xao__jeq = ['data_{}'.format(i) for i in range(ajxgl__wnzb) if i not in
        uyn__wzkgg]
    if fywmv__qqaxf:
        ksex__dbzov = len(fywmv__qqaxf)
    else:
        ksex__dbzov = ajxgl__wnzb
    bttpe__ffxkf = ', '.join(fywmv__qqaxf + xao__jeq)
    data_args = ', '.join('data_{}'.format(i) for i in range(ajxgl__wnzb))
    drcci__rvyym = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(ajxgl__wnzb):
        drcci__rvyym += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    drcci__rvyym += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(bttpe__ffxkf, index, ksex__dbzov))
    drcci__rvyym += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(drcci__rvyym, df.columns, data_args, 'index')


def create_dataframe_mask_where_overload(func_name):

    def overload_dataframe_mask_where(df, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
            f'DataFrame.{func_name}()')
        _validate_arguments_mask_where(f'DataFrame.{func_name}', df, cond,
            other, inplace, axis, level, errors, try_cast)
        header = """def impl(df, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False):
"""
        if func_name == 'mask':
            header += '  cond = ~cond\n'
        gen_all_false = [False]
        if cond.ndim == 1:
            cond_str = lambda i, _: 'cond'
        elif cond.ndim == 2:
            if isinstance(cond, DataFrameType):
                kuz__irbc = {utksr__kqk: i for i, utksr__kqk in enumerate(
                    cond.columns)}

                def cond_str(i, gen_all_false):
                    if df.columns[i] in kuz__irbc:
                        return (
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(cond, {kuz__irbc[df.columns[i]]})'
                            )
                    else:
                        gen_all_false[0] = True
                        return 'all_false'
            elif isinstance(cond, types.Array):
                cond_str = lambda i, _: f'cond[:,{i}]'
        if not hasattr(other, 'ndim') or other.ndim == 1:
            eud__nqpuv = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                other_map = {utksr__kqk: i for i, utksr__kqk in enumerate(
                    other.columns)}
                eud__nqpuv = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other_map[df.columns[i]]})'
                     if df.columns[i] in other_map else 'None')
            elif isinstance(other, types.Array):
                eud__nqpuv = lambda i: f'other[:,{i}]'
        ajxgl__wnzb = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {eud__nqpuv(i)})'
             for i in range(ajxgl__wnzb))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        ziz__ltis = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(ziz__ltis)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    zdnpn__vnd = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    dpg__lsg = dict(inplace=False, level=None, errors='raise', try_cast=False)
    check_unsupported_args(f'{func_name}', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        (cond.ndim == 1 or cond.ndim == 2) and cond.dtype == types.bool_
        ) and not (isinstance(cond, DataFrameType) and cond.ndim == 2 and
        all(cond.data[i].dtype == types.bool_ for i in range(len(df.columns)))
        ):
        raise BodoError(
            f"{func_name}(): 'cond' argument must be a DataFrame, Series, 1- or 2-dimensional array of booleans"
            )
    ajxgl__wnzb = len(df.columns)
    if hasattr(other, 'ndim') and (other.ndim != 1 or other.ndim != 2):
        if other.ndim == 2:
            if not isinstance(other, (DataFrameType, types.Array)):
                raise BodoError(
                    f"{func_name}(): 'other', if 2-dimensional, must be a DataFrame or array."
                    )
        elif other.ndim != 1:
            raise BodoError(
                f"{func_name}(): 'other' must be either 1 or 2-dimensional")
    if isinstance(other, DataFrameType):
        other_map = {utksr__kqk: i for i, utksr__kqk in enumerate(other.
            columns)}
        for i in range(ajxgl__wnzb):
            if df.columns[i] in other_map:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], other.data[other_map[df.columns[i]]]
                    )
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(ajxgl__wnzb):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other.data)
    else:
        for i in range(ajxgl__wnzb):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other, max_ndim=2)


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None,
    out_df_type=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    if out_df_type is not None:
        extra_globals['out_df_type'] = out_df_type
        dlp__olhvv = 'out_df_type'
    else:
        dlp__olhvv = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    drcci__rvyym = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {dlp__olhvv})
"""
    ukhx__aqlzo = {}
    hffe__ihir = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    hffe__ihir.update(extra_globals)
    exec(drcci__rvyym, hffe__ihir, ukhx__aqlzo)
    impl = ukhx__aqlzo['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        fws__hoiw = pd.Index(lhs.columns)
        lagt__lzgmv = pd.Index(rhs.columns)
        hdff__txm, gosw__jsdif, ehxd__yqyay = fws__hoiw.join(lagt__lzgmv,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(hdff__txm), gosw__jsdif, ehxd__yqyay
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        cgvko__logsj = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        skgxc__vel = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, cgvko__logsj)
        check_runtime_cols_unsupported(rhs, cgvko__logsj)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                hdff__txm, gosw__jsdif, ehxd__yqyay = _get_binop_columns(lhs,
                    rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {zpnd__cezug}) {cgvko__logsj}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {inox__vnz})'
                     if zpnd__cezug != -1 and inox__vnz != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for zpnd__cezug, inox__vnz in zip(gosw__jsdif,
                    ehxd__yqyay))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, hdff__txm, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            giju__sod = []
            uiqb__qdab = []
            if op in skgxc__vel:
                for i, roju__fib in enumerate(lhs.data):
                    if is_common_scalar_dtype([roju__fib.dtype, rhs]):
                        giju__sod.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {cgvko__logsj} rhs'
                            )
                    else:
                        fytmv__hbv = f'arr{i}'
                        uiqb__qdab.append(fytmv__hbv)
                        giju__sod.append(fytmv__hbv)
                data_args = ', '.join(giju__sod)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {cgvko__logsj} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(uiqb__qdab) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {fytmv__hbv} = np.empty(n, dtype=np.bool_)\n' for
                    fytmv__hbv in uiqb__qdab)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(fytmv__hbv, 
                    op == operator.ne) for fytmv__hbv in uiqb__qdab)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            giju__sod = []
            uiqb__qdab = []
            if op in skgxc__vel:
                for i, roju__fib in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, roju__fib.dtype]):
                        giju__sod.append(
                            f'lhs {cgvko__logsj} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        fytmv__hbv = f'arr{i}'
                        uiqb__qdab.append(fytmv__hbv)
                        giju__sod.append(fytmv__hbv)
                data_args = ', '.join(giju__sod)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, cgvko__logsj) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(uiqb__qdab) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(fytmv__hbv) for fytmv__hbv in uiqb__qdab)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(fytmv__hbv, 
                    op == operator.ne) for fytmv__hbv in uiqb__qdab)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(rhs)'
            return _gen_init_df(header, rhs.columns, data_args, index)
    return overload_dataframe_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        ziz__ltis = create_binary_op_overload(op)
        overload(op)(ziz__ltis)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        cgvko__logsj = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, cgvko__logsj)
        check_runtime_cols_unsupported(right, cgvko__logsj)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                hdff__txm, _, ehxd__yqyay = _get_binop_columns(left, right,
                    True)
                drcci__rvyym = 'def impl(left, right):\n'
                for i, inox__vnz in enumerate(ehxd__yqyay):
                    if inox__vnz == -1:
                        drcci__rvyym += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    drcci__rvyym += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    drcci__rvyym += f"""  df_arr{i} {cgvko__logsj} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {inox__vnz})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    hdff__txm)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(drcci__rvyym, hdff__txm, data_args,
                    index, extra_globals={'float64_arr_type': types.Array(
                    types.float64, 1, 'C')})
            drcci__rvyym = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                drcci__rvyym += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                drcci__rvyym += '  df_arr{0} {1} right\n'.format(i,
                    cgvko__logsj)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(drcci__rvyym, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        ziz__ltis = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(ziz__ltis)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            cgvko__logsj = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, cgvko__logsj)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, cgvko__logsj) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        ziz__ltis = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(ziz__ltis)


_install_unary_ops()


def overload_isna(obj):
    check_runtime_cols_unsupported(obj, 'pd.isna()')
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj):
        return lambda obj: obj.isna()
    if is_array_typ(obj):

        def impl(obj):
            numba.parfors.parfor.init_prange()
            n = len(obj)
            dqsn__sfo = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                dqsn__sfo[i] = bodo.libs.array_kernels.isna(obj, i)
            return dqsn__sfo
        return impl


overload(pd.isna, inline='always')(overload_isna)
overload(pd.isnull, inline='always')(overload_isna)


@overload(pd.isna)
@overload(pd.isnull)
def overload_isna_scalar(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj) or is_array_typ(
        obj):
        return
    if isinstance(obj, (types.List, types.UniTuple)):

        def impl(obj):
            n = len(obj)
            dqsn__sfo = np.empty(n, np.bool_)
            for i in range(n):
                dqsn__sfo[i] = pd.isna(obj[i])
            return dqsn__sfo
        return impl
    obj = types.unliteral(obj)
    if obj == bodo.string_type:
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Integer):
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Float):
        return lambda obj: np.isnan(obj)
    if isinstance(obj, (types.NPDatetime, types.NPTimedelta)):
        return lambda obj: np.isnat(obj)
    if obj == types.none:
        return lambda obj: unliteral_val(True)
    if isinstance(obj, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_dt64(obj.value))
    if obj == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(obj.value))
    if isinstance(obj, types.Optional):
        return lambda obj: obj is None
    return lambda obj: unliteral_val(False)


@overload(operator.setitem, no_unliteral=True)
def overload_setitem_arr_none(A, idx, val):
    if is_array_typ(A, False) and isinstance(idx, types.Integer
        ) and val == types.none:
        return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)


def overload_notna(obj):
    check_runtime_cols_unsupported(obj, 'pd.notna()')
    if isinstance(obj, (DataFrameType, SeriesType)):
        return lambda obj: obj.notna()
    if isinstance(obj, (types.List, types.UniTuple)) or is_array_typ(obj,
        include_index_series=True):
        return lambda obj: ~pd.isna(obj)
    return lambda obj: not pd.isna(obj)


overload(pd.notna, inline='always', no_unliteral=True)(overload_notna)
overload(pd.notnull, inline='always', no_unliteral=True)(overload_notna)


def _get_pd_dtype_str(t):
    if t.dtype == types.NPDatetime('ns'):
        return "'datetime64[ns]'"
    return bodo.ir.csv_ext._get_pd_dtype_str(t)


@overload_method(DataFrameType, 'replace', inline='always', no_unliteral=True)
def overload_dataframe_replace(df, to_replace=None, value=None, inplace=
    False, limit=None, regex=False, method='pad'):
    check_runtime_cols_unsupported(df, 'DataFrame.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.replace()')
    if is_overload_none(to_replace):
        raise BodoError('replace(): to_replace value of None is not supported')
    mlc__nacu = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    fwlnm__tsyl = {'inplace': False, 'limit': None, 'regex': False,
        'method': 'pad'}
    check_unsupported_args('replace', mlc__nacu, fwlnm__tsyl, package_name=
        'pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    lsr__jie = str(expr_node)
    return lsr__jie.startswith('left.') or lsr__jie.startswith('right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    wpxol__xvo = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (wpxol__xvo,))
    wepqr__atfub = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        dgr__lvgg = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        pxk__eqt = {('NOT_NA', wepqr__atfub(roju__fib)): roju__fib for
            roju__fib in null_set}
        dkqd__fyavl, _, _ = _parse_query_expr(dgr__lvgg, env, [], [], None,
            join_cleaned_cols=pxk__eqt)
        leyd__cst = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            sicxe__rcx = pd.core.computation.ops.BinOp('&', dkqd__fyavl,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = leyd__cst
        return sicxe__rcx

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                bwer__qich = set()
                pogqg__wnad = set()
                uxecx__yoxz = _insert_NA_cond_body(expr_node.lhs, bwer__qich)
                qovav__ezvp = _insert_NA_cond_body(expr_node.rhs, pogqg__wnad)
                duq__ldec = bwer__qich.intersection(pogqg__wnad)
                bwer__qich.difference_update(duq__ldec)
                pogqg__wnad.difference_update(duq__ldec)
                null_set.update(duq__ldec)
                expr_node.lhs = append_null_checks(uxecx__yoxz, bwer__qich)
                expr_node.rhs = append_null_checks(qovav__ezvp, pogqg__wnad)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            lbd__vmuuz = expr_node.name
            rhh__ncm, col_name = lbd__vmuuz.split('.')
            if rhh__ncm == 'left':
                frks__gkhom = left_columns
                data = left_data
            else:
                frks__gkhom = right_columns
                data = right_data
            ikz__wbufq = data[frks__gkhom.index(col_name)]
            if bodo.utils.typing.is_nullable(ikz__wbufq):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    lrf__dhf = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        rvrz__qetf = str(expr_node.lhs)
        hhpxx__tam = str(expr_node.rhs)
        if rvrz__qetf.startswith('left.') and hhpxx__tam.startswith('left.'
            ) or rvrz__qetf.startswith('right.') and hhpxx__tam.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [rvrz__qetf.split('.')[1]]
        right_on = [hhpxx__tam.split('.')[1]]
        if rvrz__qetf.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        mmszd__enzc, biyoj__spmo, vsdwc__kejq = _extract_equal_conds(expr_node
            .lhs)
        zupr__qql, uov__ghkd, zawsv__hrbzd = _extract_equal_conds(expr_node.rhs
            )
        left_on = mmszd__enzc + zupr__qql
        right_on = biyoj__spmo + uov__ghkd
        if vsdwc__kejq is None:
            return left_on, right_on, zawsv__hrbzd
        if zawsv__hrbzd is None:
            return left_on, right_on, vsdwc__kejq
        expr_node.lhs = vsdwc__kejq
        expr_node.rhs = zawsv__hrbzd
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    wpxol__xvo = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (wpxol__xvo,))
    duizr__shuz = dict()
    wepqr__atfub = pd.core.computation.parsing.clean_column_name
    for name, wkx__vrja in (('left', left_columns), ('right', right_columns)):
        for roju__fib in wkx__vrja:
            rai__ovsxf = wepqr__atfub(roju__fib)
            fbr__rruca = name, rai__ovsxf
            if fbr__rruca in duizr__shuz:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{roju__fib}' and '{duizr__shuz[rai__ovsxf]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            duizr__shuz[fbr__rruca] = roju__fib
    ldba__uzz, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=duizr__shuz)
    left_on, right_on, vhv__rfz = _extract_equal_conds(ldba__uzz.terms)
    return left_on, right_on, _insert_NA_cond(vhv__rfz, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    zdnpn__vnd = dict(sort=sort, copy=copy, validate=validate)
    dpg__lsg = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    hnvbr__ixb = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    ttgv__utke = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in hnvbr__ixb and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, rtqec__omow = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if rtqec__omow is None:
                    ttgv__utke = ''
                else:
                    ttgv__utke = str(rtqec__omow)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = hnvbr__ixb
        right_keys = hnvbr__ixb
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    if (not left_on or not right_on) and not is_overload_none(on):
        raise BodoError(
            f"DataFrame.merge(): Merge condition '{get_overload_const_str(on)}' requires a cross join to implement, but cross join is not supported."
            )
    if not is_overload_bool(indicator):
        raise_bodo_error(
            'DataFrame.merge(): indicator must be a constant boolean')
    indicator_val = get_overload_const_bool(indicator)
    if not is_overload_bool(_bodo_na_equal):
        raise_bodo_error(
            'DataFrame.merge(): bodo extension _bodo_na_equal must be a constant boolean'
            )
    sjg__tqh = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        pqsq__gtg = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        pqsq__gtg = list(get_overload_const_list(suffixes))
    suffix_x = pqsq__gtg[0]
    suffix_y = pqsq__gtg[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    drcci__rvyym = (
        "def _impl(left, right, how='inner', on=None, left_on=None,\n")
    drcci__rvyym += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    drcci__rvyym += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    drcci__rvyym += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, sjg__tqh, ttgv__utke))
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo}, ukhx__aqlzo)
    _impl = ukhx__aqlzo['_impl']
    return _impl


def common_validate_merge_merge_asof_spec(name_func, left, right, on,
    left_on, right_on, left_index, right_index, suffixes):
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError(name_func + '() requires dataframe inputs')
    valid_dataframe_column_types = (ArrayItemArrayType, MapArrayType,
        StructArrayType, CategoricalArrayType, types.Array,
        IntegerArrayType, DecimalArrayType, IntervalArrayType, bodo.
        DatetimeArrayType)
    hrt__xvac = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    rmnpg__uoxgt = {get_overload_const_str(fqr__xuhv) for fqr__xuhv in (
        left_on, right_on, on) if is_overload_constant_str(fqr__xuhv)}
    for df in (left, right):
        for i, roju__fib in enumerate(df.data):
            if not isinstance(roju__fib, valid_dataframe_column_types
                ) and roju__fib not in hrt__xvac:
                raise BodoError(
                    f'{name_func}(): use of column with {type(roju__fib)} in merge unsupported'
                    )
            if df.columns[i] in rmnpg__uoxgt and isinstance(roju__fib,
                MapArrayType):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        pqsq__gtg = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        pqsq__gtg = list(get_overload_const_list(suffixes))
    if len(pqsq__gtg) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    hnvbr__ixb = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        jktf__qoe = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            jktf__qoe = on_str not in hnvbr__ixb and ('left.' in on_str or 
                'right.' in on_str)
        if len(hnvbr__ixb) == 0 and not jktf__qoe:
            raise_bodo_error(name_func +
                '(): No common columns to perform merge on. Merge options: left_on={lon}, right_on={ron}, left_index={lidx}, right_index={ridx}'
                .format(lon=is_overload_true(left_on), ron=is_overload_true
                (right_on), lidx=is_overload_true(left_index), ridx=
                is_overload_true(right_index)))
        if not is_overload_none(left_on) or not is_overload_none(right_on):
            raise BodoError(name_func +
                '(): Can only pass argument "on" OR "left_on" and "right_on", not a combination of both.'
                )
    if (is_overload_true(left_index) or not is_overload_none(left_on)
        ) and is_overload_none(right_on) and not is_overload_true(right_index):
        raise BodoError(name_func +
            '(): Must pass right_on or right_index=True')
    if (is_overload_true(right_index) or not is_overload_none(right_on)
        ) and is_overload_none(left_on) and not is_overload_true(left_index):
        raise BodoError(name_func + '(): Must pass left_on or left_index=True')


def validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
    right_index, sort, suffixes, copy, indicator, validate):
    common_validate_merge_merge_asof_spec('merge', left, right, on, left_on,
        right_on, left_index, right_index, suffixes)
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))


def validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
    right_index, by, left_by, right_by, suffixes, tolerance,
    allow_exact_matches, direction):
    common_validate_merge_merge_asof_spec('merge_asof', left, right, on,
        left_on, right_on, left_index, right_index, suffixes)
    if not is_overload_true(allow_exact_matches):
        raise BodoError(
            'merge_asof(): allow_exact_matches parameter only supports default value True'
            )
    if not is_overload_none(tolerance):
        raise BodoError(
            'merge_asof(): tolerance parameter only supports default value None'
            )
    if not is_overload_none(by):
        raise BodoError(
            'merge_asof(): by parameter only supports default value None')
    if not is_overload_none(left_by):
        raise BodoError(
            'merge_asof(): left_by parameter only supports default value None')
    if not is_overload_none(right_by):
        raise BodoError(
            'merge_asof(): right_by parameter only supports default value None'
            )
    if not is_overload_constant_str(direction):
        raise BodoError(
            'merge_asof(): direction parameter should be of type str')
    else:
        direction = get_overload_const_str(direction)
        if direction != 'backward':
            raise BodoError(
                "merge_asof(): direction parameter only supports default value 'backward'"
                )


def validate_merge_asof_keys_length(left_on, right_on, left_index,
    right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if not is_overload_none(left_on) and is_overload_true(right_index):
        raise BodoError(
            'merge(): right_index = True and specifying left_on is not suppported yet.'
            )
    if not is_overload_none(right_on) and is_overload_true(left_index):
        raise BodoError(
            'merge(): left_index = True and specifying right_on is not suppported yet.'
            )


def validate_keys_length(left_index, right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if is_overload_true(right_index):
        if len(left_keys) != 1:
            raise BodoError(
                'merge(): len(left_on) must equal the number of levels in the index of "right", which is 1'
                )
    if is_overload_true(left_index):
        if len(right_keys) != 1:
            raise BodoError(
                'merge(): len(right_on) must equal the number of levels in the index of "left", which is 1'
                )


def validate_keys_dtypes(left, right, left_index, right_index, left_keys,
    right_keys):
    izuzr__bdj = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            eiq__eyw = left.index
            fcua__rmgs = isinstance(eiq__eyw, StringIndexType)
            mxbwt__dvzn = right.index
            whhyj__ffgi = isinstance(mxbwt__dvzn, StringIndexType)
        elif is_overload_true(left_index):
            eiq__eyw = left.index
            fcua__rmgs = isinstance(eiq__eyw, StringIndexType)
            mxbwt__dvzn = right.data[right.columns.index(right_keys[0])]
            whhyj__ffgi = mxbwt__dvzn.dtype == string_type
        elif is_overload_true(right_index):
            eiq__eyw = left.data[left.columns.index(left_keys[0])]
            fcua__rmgs = eiq__eyw.dtype == string_type
            mxbwt__dvzn = right.index
            whhyj__ffgi = isinstance(mxbwt__dvzn, StringIndexType)
        if fcua__rmgs and whhyj__ffgi:
            return
        eiq__eyw = eiq__eyw.dtype
        mxbwt__dvzn = mxbwt__dvzn.dtype
        try:
            gez__vqzxg = izuzr__bdj.resolve_function_type(operator.eq, (
                eiq__eyw, mxbwt__dvzn), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=eiq__eyw, rk_dtype=mxbwt__dvzn))
    else:
        for assid__efq, oktyr__xcf in zip(left_keys, right_keys):
            eiq__eyw = left.data[left.columns.index(assid__efq)].dtype
            owe__oxne = left.data[left.columns.index(assid__efq)]
            mxbwt__dvzn = right.data[right.columns.index(oktyr__xcf)].dtype
            vketk__qykc = right.data[right.columns.index(oktyr__xcf)]
            if owe__oxne == vketk__qykc:
                continue
            btq__uuhj = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=assid__efq, lk_dtype=eiq__eyw, rk=oktyr__xcf,
                rk_dtype=mxbwt__dvzn))
            lmvz__zdbji = eiq__eyw == string_type
            fcp__pfcaq = mxbwt__dvzn == string_type
            if lmvz__zdbji ^ fcp__pfcaq:
                raise_bodo_error(btq__uuhj)
            try:
                gez__vqzxg = izuzr__bdj.resolve_function_type(operator.eq,
                    (eiq__eyw, mxbwt__dvzn), {})
            except:
                raise_bodo_error(btq__uuhj)


def validate_keys(keys, df):
    rxj__hpaiz = set(keys).difference(set(df.columns))
    if len(rxj__hpaiz) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in rxj__hpaiz:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {rxj__hpaiz} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    zdnpn__vnd = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    dpg__lsg = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort)
    how = get_overload_const_str(how)
    if not is_overload_none(on):
        left_keys = get_overload_const_list(on)
    else:
        left_keys = ['$_bodo_index_']
    right_keys = ['$_bodo_index_']
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    drcci__rvyym = "def _impl(left, other, on=None, how='left',\n"
    drcci__rvyym += "    lsuffix='', rsuffix='', sort=False):\n"
    drcci__rvyym += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo}, ukhx__aqlzo)
    _impl = ukhx__aqlzo['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        kwjzo__vjjgk = get_overload_const_list(on)
        validate_keys(kwjzo__vjjgk, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    hnvbr__ixb = tuple(set(left.columns) & set(other.columns))
    if len(hnvbr__ixb) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=hnvbr__ixb))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    jii__aspmv = set(left_keys) & set(right_keys)
    imt__gnh = set(left_columns) & set(right_columns)
    sngfj__yobqx = imt__gnh - jii__aspmv
    lxq__qcn = set(left_columns) - imt__gnh
    ipa__hmgi = set(right_columns) - imt__gnh
    kmsa__wfv = {}

    def insertOutColumn(col_name):
        if col_name in kmsa__wfv:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        kmsa__wfv[col_name] = 0
    for qofz__unzg in jii__aspmv:
        insertOutColumn(qofz__unzg)
    for qofz__unzg in sngfj__yobqx:
        njor__zem = str(qofz__unzg) + suffix_x
        jqiz__ypcc = str(qofz__unzg) + suffix_y
        insertOutColumn(njor__zem)
        insertOutColumn(jqiz__ypcc)
    for qofz__unzg in lxq__qcn:
        insertOutColumn(qofz__unzg)
    for qofz__unzg in ipa__hmgi:
        insertOutColumn(qofz__unzg)
    if indicator_val:
        insertOutColumn('_merge')


@overload(pd.merge_asof, inline='always', no_unliteral=True)
def overload_dataframe_merge_asof(left, right, on=None, left_on=None,
    right_on=None, left_index=False, right_index=False, by=None, left_by=
    None, right_by=None, suffixes=('_x', '_y'), tolerance=None,
    allow_exact_matches=True, direction='backward'):
    validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
        right_index, by, left_by, right_by, suffixes, tolerance,
        allow_exact_matches, direction)
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError('merge_asof() requires dataframe inputs')
    hnvbr__ixb = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = hnvbr__ixb
        right_keys = hnvbr__ixb
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    validate_merge_asof_keys_length(left_on, right_on, left_index,
        right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    if isinstance(suffixes, tuple):
        pqsq__gtg = suffixes
    if is_overload_constant_list(suffixes):
        pqsq__gtg = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        pqsq__gtg = suffixes.value
    suffix_x = pqsq__gtg[0]
    suffix_y = pqsq__gtg[1]
    drcci__rvyym = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    drcci__rvyym += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    drcci__rvyym += (
        "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n")
    drcci__rvyym += "    allow_exact_matches=True, direction='backward'):\n"
    drcci__rvyym += '  suffix_x = suffixes[0]\n'
    drcci__rvyym += '  suffix_y = suffixes[1]\n'
    drcci__rvyym += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo}, ukhx__aqlzo)
    _impl = ukhx__aqlzo['_impl']
    return _impl


@overload_method(DataFrameType, 'groupby', inline='always', no_unliteral=True)
def overload_dataframe_groupby(df, by=None, axis=0, level=None, as_index=
    True, sort=False, group_keys=True, squeeze=False, observed=True, dropna
    =True):
    check_runtime_cols_unsupported(df, 'DataFrame.groupby()')
    validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
        squeeze, observed, dropna)

    def _impl(df, by=None, axis=0, level=None, as_index=True, sort=False,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        return bodo.hiframes.pd_groupby_ext.init_groupby(df, by, as_index,
            dropna)
    return _impl


def validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
    squeeze, observed, dropna):
    if is_overload_none(by):
        raise BodoError("groupby(): 'by' must be supplied.")
    if not is_overload_zero(axis):
        raise BodoError(
            "groupby(): 'axis' parameter only supports integer value 0.")
    if not is_overload_none(level):
        raise BodoError(
            "groupby(): 'level' is not supported since MultiIndex is not supported."
            )
    if not is_literal_type(by) and not is_overload_constant_list(by):
        raise_bodo_error(
            f"groupby(): 'by' parameter only supports a constant column label or column labels, not {by}."
            )
    if len(set(get_overload_const_list(by)).difference(set(df.columns))) > 0:
        raise_bodo_error(
            "groupby(): invalid key {} for 'by' (not available in columns {})."
            .format(get_overload_const_list(by), df.columns))
    if not is_overload_constant_bool(as_index):
        raise_bodo_error(
            "groupby(): 'as_index' parameter must be a constant bool, not {}."
            .format(as_index))
    if not is_overload_constant_bool(dropna):
        raise_bodo_error(
            "groupby(): 'dropna' parameter must be a constant bool, not {}."
            .format(dropna))
    zdnpn__vnd = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    mkdbk__voul = dict(sort=False, group_keys=True, squeeze=False, observed
        =True)
    check_unsupported_args('Dataframe.groupby', zdnpn__vnd, mkdbk__voul,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    hlfy__wuh = func_name == 'DataFrame.pivot_table'
    if hlfy__wuh:
        if is_overload_none(index) or not is_literal_type(index):
            raise_bodo_error(
                f"DataFrame.pivot_table(): 'index' argument is required and must be constant column labels"
                )
    elif not is_overload_none(index) and not is_literal_type(index):
        raise_bodo_error(
            f"{func_name}(): if 'index' argument is provided it must be constant column labels"
            )
    if is_overload_none(columns) or not is_literal_type(columns):
        raise_bodo_error(
            f"{func_name}(): 'columns' argument is required and must be a constant column label"
            )
    if not is_overload_none(values) and not is_literal_type(values):
        raise_bodo_error(
            f"{func_name}(): if 'values' argument is provided it must be constant column labels"
            )
    ize__bxe = get_literal_value(columns)
    if isinstance(ize__bxe, (list, tuple)):
        if len(ize__bxe) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {ize__bxe}"
                )
        ize__bxe = ize__bxe[0]
    if ize__bxe not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {ize__bxe} not found in DataFrame {df}."
            )
    cwovk__xgwff = {utksr__kqk: i for i, utksr__kqk in enumerate(df.columns)}
    coyxf__evum = cwovk__xgwff[ize__bxe]
    if is_overload_none(index):
        wcgfp__lui = []
        vssg__ajqaj = []
    else:
        vssg__ajqaj = get_literal_value(index)
        if not isinstance(vssg__ajqaj, (list, tuple)):
            vssg__ajqaj = [vssg__ajqaj]
        wcgfp__lui = []
        for index in vssg__ajqaj:
            if index not in cwovk__xgwff:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            wcgfp__lui.append(cwovk__xgwff[index])
    if not (all(isinstance(utksr__kqk, int) for utksr__kqk in vssg__ajqaj) or
        all(isinstance(utksr__kqk, str) for utksr__kqk in vssg__ajqaj)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        reg__qdprz = []
        stg__rnwf = []
        aphn__zecrm = wcgfp__lui + [coyxf__evum]
        for i, utksr__kqk in enumerate(df.columns):
            if i not in aphn__zecrm:
                reg__qdprz.append(i)
                stg__rnwf.append(utksr__kqk)
    else:
        stg__rnwf = get_literal_value(values)
        if not isinstance(stg__rnwf, (list, tuple)):
            stg__rnwf = [stg__rnwf]
        reg__qdprz = []
        for val in stg__rnwf:
            if val not in cwovk__xgwff:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            reg__qdprz.append(cwovk__xgwff[val])
    if all(isinstance(utksr__kqk, int) for utksr__kqk in stg__rnwf):
        stg__rnwf = np.array(stg__rnwf, 'int64')
    elif all(isinstance(utksr__kqk, str) for utksr__kqk in stg__rnwf):
        stg__rnwf = pd.array(stg__rnwf, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    xdzm__ored = set(reg__qdprz) | set(wcgfp__lui) | {coyxf__evum}
    if len(xdzm__ored) != len(reg__qdprz) + len(wcgfp__lui) + 1:
        raise BodoError(
            f"{func_name}(): 'index', 'columns', and 'values' must all refer to different columns"
            )

    def check_valid_index_typ(index_column):
        if isinstance(index_column, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType, bodo.
            IntervalArrayType)):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column must have scalar rows"
                )
        if isinstance(index_column, bodo.CategoricalArrayType):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column does not support categorical data"
                )
    if len(wcgfp__lui) == 0:
        index = df.index
        if isinstance(index, MultiIndexType):
            raise BodoError(
                f"{func_name}(): 'index' cannot be None with a DataFrame with a multi-index"
                )
        if not isinstance(index, RangeIndexType):
            check_valid_index_typ(index.data)
        if not is_literal_type(df.index.name_typ):
            raise BodoError(
                f"{func_name}(): If 'index' is None, the name of the DataFrame's Index must be constant at compile-time"
                )
    else:
        for mjems__aip in wcgfp__lui:
            index_column = df.data[mjems__aip]
            check_valid_index_typ(index_column)
    uaj__sesu = df.data[coyxf__evum]
    if isinstance(uaj__sesu, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(uaj__sesu, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for fjm__cvdl in reg__qdprz:
        znh__fwrk = df.data[fjm__cvdl]
        if isinstance(znh__fwrk, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or znh__fwrk == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (vssg__ajqaj, ize__bxe, stg__rnwf, wcgfp__lui, coyxf__evum,
        reg__qdprz)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (vssg__ajqaj, ize__bxe, stg__rnwf, mjems__aip, coyxf__evum, vbrgq__vvhrt
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(vssg__ajqaj) == 0:
        if is_overload_none(data.index.name_typ):
            vssg__ajqaj = [None]
        else:
            vssg__ajqaj = [get_literal_value(data.index.name_typ)]
    if len(stg__rnwf) == 1:
        nyna__urbdy = None
    else:
        nyna__urbdy = stg__rnwf
    drcci__rvyym = 'def impl(data, index=None, columns=None, values=None):\n'
    drcci__rvyym += (
        f'    pivot_values = data.iloc[:, {coyxf__evum}].unique()\n')
    drcci__rvyym += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(mjems__aip) == 0:
        drcci__rvyym += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        drcci__rvyym += '        (\n'
        for swpvc__hhbf in mjems__aip:
            drcci__rvyym += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {swpvc__hhbf}),
"""
        drcci__rvyym += '        ),\n'
    drcci__rvyym += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {coyxf__evum}),),
"""
    drcci__rvyym += '        (\n'
    for fjm__cvdl in vbrgq__vvhrt:
        drcci__rvyym += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {fjm__cvdl}),
"""
    drcci__rvyym += '        ),\n'
    drcci__rvyym += '        pivot_values,\n'
    drcci__rvyym += '        index_lit_tup,\n'
    drcci__rvyym += '        columns_lit,\n'
    drcci__rvyym += '        values_name_const,\n'
    drcci__rvyym += '    )\n'
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo, 'index_lit_tup': tuple(vssg__ajqaj),
        'columns_lit': ize__bxe, 'values_name_const': nyna__urbdy}, ukhx__aqlzo
        )
    impl = ukhx__aqlzo['impl']
    return impl


@overload(pd.pivot_table, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot_table', inline='always',
    no_unliteral=True)
def overload_dataframe_pivot_table(data, values=None, index=None, columns=
    None, aggfunc='mean', fill_value=None, margins=False, dropna=True,
    margins_name='All', observed=False, sort=True, _pivot_values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot_table()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot_table()')
    zdnpn__vnd = dict(fill_value=fill_value, margins=margins, dropna=dropna,
        margins_name=margins_name, observed=observed, sort=sort)
    dpg__lsg = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    if _pivot_values is None:
        (vssg__ajqaj, ize__bxe, stg__rnwf, mjems__aip, coyxf__evum,
            vbrgq__vvhrt) = (pivot_error_checking(data, index, columns,
            values, 'DataFrame.pivot_table'))
        if len(stg__rnwf) == 1:
            nyna__urbdy = None
        else:
            nyna__urbdy = stg__rnwf
        drcci__rvyym = 'def impl(\n'
        drcci__rvyym += '    data,\n'
        drcci__rvyym += '    values=None,\n'
        drcci__rvyym += '    index=None,\n'
        drcci__rvyym += '    columns=None,\n'
        drcci__rvyym += '    aggfunc="mean",\n'
        drcci__rvyym += '    fill_value=None,\n'
        drcci__rvyym += '    margins=False,\n'
        drcci__rvyym += '    dropna=True,\n'
        drcci__rvyym += '    margins_name="All",\n'
        drcci__rvyym += '    observed=False,\n'
        drcci__rvyym += '    sort=True,\n'
        drcci__rvyym += '    _pivot_values=None,\n'
        drcci__rvyym += '):\n'
        thqmq__efj = mjems__aip + [coyxf__evum] + vbrgq__vvhrt
        drcci__rvyym += f'    data = data.iloc[:, {thqmq__efj}]\n'
        bxz__mmmaf = vssg__ajqaj + [ize__bxe]
        drcci__rvyym += (
            f'    data = data.groupby({bxz__mmmaf!r}, as_index=False).agg(aggfunc)\n'
            )
        drcci__rvyym += (
            f'    pivot_values = data.iloc[:, {len(mjems__aip)}].unique()\n')
        drcci__rvyym += (
            '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n')
        drcci__rvyym += '        (\n'
        for i in range(0, len(mjems__aip)):
            drcci__rvyym += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        drcci__rvyym += '        ),\n'
        drcci__rvyym += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(mjems__aip)}),),
"""
        drcci__rvyym += '        (\n'
        for i in range(len(mjems__aip) + 1, len(vbrgq__vvhrt) + len(
            mjems__aip) + 1):
            drcci__rvyym += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        drcci__rvyym += '        ),\n'
        drcci__rvyym += '        pivot_values,\n'
        drcci__rvyym += '        index_lit_tup,\n'
        drcci__rvyym += '        columns_lit,\n'
        drcci__rvyym += '        values_name_const,\n'
        drcci__rvyym += '        check_duplicates=False,\n'
        drcci__rvyym += '    )\n'
        ukhx__aqlzo = {}
        exec(drcci__rvyym, {'bodo': bodo, 'numba': numba, 'index_lit_tup':
            tuple(vssg__ajqaj), 'columns_lit': ize__bxe,
            'values_name_const': nyna__urbdy}, ukhx__aqlzo)
        impl = ukhx__aqlzo['impl']
        return impl
    if aggfunc == 'mean':

        def _impl(data, values=None, index=None, columns=None, aggfunc=
            'mean', fill_value=None, margins=False, dropna=True,
            margins_name='All', observed=False, sort=True, _pivot_values=None):
            return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(data,
                values, index, columns, 'mean', _pivot_values)
        return _impl

    def _impl(data, values=None, index=None, columns=None, aggfunc='mean',
        fill_value=None, margins=False, dropna=True, margins_name='All',
        observed=False, sort=True, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.pivot_table_dummy(data, values,
            index, columns, aggfunc, _pivot_values)
    return _impl


@overload(pd.melt, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'melt', inline='always', no_unliteral=True)
def overload_dataframe_melt(frame, id_vars=None, value_vars=None, var_name=
    None, value_name='value', col_level=None, ignore_index=True):
    zdnpn__vnd = dict(var_name=var_name, value_name=value_name, col_level=
        col_level, ignore_index=ignore_index)
    dpg__lsg = dict(var_name=None, value_name='value', col_level=None,
        ignore_index=True)
    check_unsupported_args('DataFrame.melt', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(frame, DataFrameType):
        raise BodoError("pandas.melt(): 'frame' argument must be a DataFrame")
    if not is_overload_none(id_vars) and not is_literal_type(id_vars):
        raise BodoError(
            "DataFrame.melt(): 'id_vars', if specified, must be a literal")
    if not is_overload_none(value_vars) and not is_literal_type(value_vars):
        raise BodoError(
            "DataFrame.melt(): 'value_vars', if specified, must be a literal")
    mds__xuht = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(mds__xuht, (list, tuple)):
        mds__xuht = [mds__xuht]
    for utksr__kqk in mds__xuht:
        if utksr__kqk not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {utksr__kqk} not found in {frame}"
                )
    duizr__shuz = {utksr__kqk: i for i, utksr__kqk in enumerate(frame.columns)}
    ddzic__nvayr = [duizr__shuz[i] for i in mds__xuht]
    if is_overload_none(value_vars):
        rbyek__ssxzc = []
        yat__pahp = []
        for i, utksr__kqk in enumerate(frame.columns):
            if i not in ddzic__nvayr:
                rbyek__ssxzc.append(i)
                yat__pahp.append(utksr__kqk)
    else:
        yat__pahp = get_literal_value(value_vars)
        if not isinstance(yat__pahp, (list, tuple)):
            yat__pahp = [yat__pahp]
        yat__pahp = [v for v in yat__pahp if v not in mds__xuht]
        if not yat__pahp:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        rbyek__ssxzc = []
        for val in yat__pahp:
            if val not in duizr__shuz:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            rbyek__ssxzc.append(duizr__shuz[val])
    for utksr__kqk in yat__pahp:
        if utksr__kqk not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {utksr__kqk} not found in {frame}"
                )
    if not (all(isinstance(utksr__kqk, int) for utksr__kqk in yat__pahp) or
        all(isinstance(utksr__kqk, str) for utksr__kqk in yat__pahp)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    bjh__qayx = frame.data[rbyek__ssxzc[0]]
    pmsbe__quxux = [frame.data[i].dtype for i in rbyek__ssxzc]
    rbyek__ssxzc = np.array(rbyek__ssxzc, dtype=np.int64)
    ddzic__nvayr = np.array(ddzic__nvayr, dtype=np.int64)
    _, iax__qoee = bodo.utils.typing.get_common_scalar_dtype(pmsbe__quxux)
    if not iax__qoee:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': yat__pahp, 'val_type': bjh__qayx}
    header = 'def impl(\n'
    header += '  frame,\n'
    header += '  id_vars=None,\n'
    header += '  value_vars=None,\n'
    header += '  var_name=None,\n'
    header += "  value_name='value',\n"
    header += '  col_level=None,\n'
    header += '  ignore_index=True,\n'
    header += '):\n'
    header += (
        '  dummy_id = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, 0)\n'
        )
    if frame.is_table_format and all(v == bjh__qayx.dtype for v in pmsbe__quxux
        ):
        extra_globals['value_idxs'] = rbyek__ssxzc
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(yat__pahp) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {rbyek__ssxzc[0]})
"""
    else:
        lpuya__pezrp = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in rbyek__ssxzc)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({lpuya__pezrp},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in ddzic__nvayr:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(yat__pahp)})\n'
            )
    wwlt__cdkf = ', '.join(f'out_id{i}' for i in ddzic__nvayr) + (', ' if 
        len(ddzic__nvayr) > 0 else '')
    data_args = wwlt__cdkf + 'var_col, val_col'
    columns = tuple(mds__xuht + ['variable', 'value'])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(yat__pahp)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    zdnpn__vnd = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    dpg__lsg = dict(values=None, rownames=None, colnames=None, aggfunc=None,
        margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(index,
        'pandas.crosstab()')
    if not isinstance(index, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'index' argument only supported for Series types, found {index}"
            )
    if not isinstance(columns, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'columns' argument only supported for Series types, found {columns}"
            )

    def _impl(index, columns, values=None, rownames=None, colnames=None,
        aggfunc=None, margins=False, margins_name='All', dropna=True,
        normalize=False, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.crosstab_dummy(index, columns,
            _pivot_values)
    return _impl


@overload_method(DataFrameType, 'sort_values', inline='always',
    no_unliteral=True)
def overload_dataframe_sort_values(df, by, axis=0, ascending=True, inplace=
    False, kind='quicksort', na_position='last', ignore_index=False, key=
    None, _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_values()')
    zdnpn__vnd = dict(ignore_index=ignore_index, key=key)
    dpg__lsg = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'sort_values')
    validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
        na_position)

    def _impl(df, by, axis=0, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', ignore_index=False, key=None,
        _bodo_transformed=False):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df, by,
            ascending, inplace, na_position)
    return _impl


def validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
    na_position):
    if is_overload_none(by) or not is_literal_type(by
        ) and not is_overload_constant_list(by):
        raise_bodo_error(
            "sort_values(): 'by' parameter only supports a constant column label or column labels. by={}"
            .format(by))
    ntub__hxvp = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        ntub__hxvp.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        ryv__npuis = [get_overload_const_tuple(by)]
    else:
        ryv__npuis = get_overload_const_list(by)
    ryv__npuis = set((k, '') if (k, '') in ntub__hxvp else k for k in
        ryv__npuis)
    if len(ryv__npuis.difference(ntub__hxvp)) > 0:
        oqs__owdg = list(set(get_overload_const_list(by)).difference(
            ntub__hxvp))
        raise_bodo_error(f'sort_values(): invalid keys {oqs__owdg} for by.')
    if not is_overload_zero(axis):
        raise_bodo_error(
            "sort_values(): 'axis' parameter only supports integer value 0.")
    if not is_overload_bool(ascending) and not is_overload_bool_list(ascending
        ):
        raise_bodo_error(
            "sort_values(): 'ascending' parameter must be of type bool or list of bool, not {}."
            .format(ascending))
    if not is_overload_bool(inplace):
        raise_bodo_error(
            "sort_values(): 'inplace' parameter must be of type bool, not {}."
            .format(inplace))
    if kind != 'quicksort' and not isinstance(kind, types.Omitted):
        warnings.warn(BodoWarning(
            'sort_values(): specifying sorting algorithm is not supported in Bodo. Bodo uses stable sort.'
            ))
    if is_overload_constant_str(na_position):
        na_position = get_overload_const_str(na_position)
        if na_position not in ('first', 'last'):
            raise BodoError(
                "sort_values(): na_position should either be 'first' or 'last'"
                )
    elif is_overload_constant_list(na_position):
        hrm__acbs = get_overload_const_list(na_position)
        for na_position in hrm__acbs:
            if na_position not in ('first', 'last'):
                raise BodoError(
                    "sort_values(): Every value in na_position should either be 'first' or 'last'"
                    )
    else:
        raise_bodo_error(
            f'sort_values(): na_position parameter must be a literal constant of type str or a constant list of str with 1 entry per key column, not {na_position}'
            )
    na_position = get_overload_const_str(na_position)
    if na_position not in ['first', 'last']:
        raise BodoError(
            "sort_values(): na_position should either be 'first' or 'last'")


@overload_method(DataFrameType, 'sort_index', inline='always', no_unliteral
    =True)
def overload_dataframe_sort_index(df, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_index()')
    zdnpn__vnd = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    dpg__lsg = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_bool(ascending):
        raise BodoError(
            "DataFrame.sort_index(): 'ascending' parameter must be of type bool"
            )
    if not is_overload_bool(inplace):
        raise BodoError(
            "DataFrame.sort_index(): 'inplace' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "DataFrame.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def _impl(df, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df,
            '$_bodo_index_', ascending, inplace, na_position)
    return _impl


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    check_runtime_cols_unsupported(df, 'DataFrame.fillna()')
    zdnpn__vnd = dict(limit=limit, downcast=downcast)
    dpg__lsg = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    yaf__yomc = not is_overload_none(value)
    tbdw__amjq = not is_overload_none(method)
    if yaf__yomc and tbdw__amjq:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not yaf__yomc and not tbdw__amjq:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if yaf__yomc:
        adj__smvsa = 'value=value'
    else:
        adj__smvsa = 'method=method'
    data_args = [(
        f"df['{utksr__kqk}'].fillna({adj__smvsa}, inplace=inplace)" if
        isinstance(utksr__kqk, str) else
        f'df[{utksr__kqk}].fillna({adj__smvsa}, inplace=inplace)') for
        utksr__kqk in df.columns]
    drcci__rvyym = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        drcci__rvyym += '  ' + '  \n'.join(data_args) + '\n'
        ukhx__aqlzo = {}
        exec(drcci__rvyym, {}, ukhx__aqlzo)
        impl = ukhx__aqlzo['impl']
        return impl
    else:
        return _gen_init_df(drcci__rvyym, df.columns, ', '.join(pgoa__ohwe +
            '.values' for pgoa__ohwe in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    zdnpn__vnd = dict(col_level=col_level, col_fill=col_fill)
    dpg__lsg = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'reset_index')
    if not _is_all_levels(df, level):
        raise_bodo_error(
            'DataFrame.reset_index(): only dropping all index levels supported'
            )
    if not is_overload_constant_bool(drop):
        raise BodoError(
            "DataFrame.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.reset_index(): 'inplace' parameter should be a constant boolean value"
            )
    drcci__rvyym = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    drcci__rvyym += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(df), 1, None)\n'
        )
    drop = is_overload_true(drop)
    inplace = is_overload_true(inplace)
    columns = df.columns
    data_args = [
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}\n'.
        format(i, '' if inplace else '.copy()') for i in range(len(df.columns))
        ]
    if not drop:
        xrbip__wita = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            xrbip__wita)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            drcci__rvyym += (
                '  m_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
                )
            thozc__ytzjf = ['m_index._data[{}]'.format(i) for i in range(df
                .index.nlevels)]
            data_args = thozc__ytzjf + data_args
        else:
            bdmx__humd = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [bdmx__humd] + data_args
    return _gen_init_df(drcci__rvyym, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    dato__akiok = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and dato__akiok == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(dato__akiok))


@overload_method(DataFrameType, 'dropna', inline='always', no_unliteral=True)
def overload_dataframe_dropna(df, axis=0, how='any', thresh=None, subset=
    None, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.dropna()')
    if not is_overload_constant_bool(inplace) or is_overload_true(inplace):
        raise BodoError('DataFrame.dropna(): inplace=True is not supported')
    if not is_overload_zero(axis):
        raise_bodo_error(f'df.dropna(): only axis=0 supported')
    ensure_constant_values('dropna', 'how', how, ('any', 'all'))
    if is_overload_none(subset):
        cvtby__qmtqk = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        pitr__klzz = get_overload_const_list(subset)
        cvtby__qmtqk = []
        for ezcp__kjv in pitr__klzz:
            if ezcp__kjv not in df.columns:
                raise_bodo_error(
                    f"df.dropna(): column '{ezcp__kjv}' not in data frame columns {df}"
                    )
            cvtby__qmtqk.append(df.columns.index(ezcp__kjv))
    ajxgl__wnzb = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(ajxgl__wnzb))
    drcci__rvyym = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(ajxgl__wnzb):
        drcci__rvyym += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    drcci__rvyym += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in cvtby__qmtqk)))
    drcci__rvyym += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(drcci__rvyym, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    zdnpn__vnd = dict(index=index, level=level, errors=errors)
    dpg__lsg = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', zdnpn__vnd, dpg__lsg,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'drop')
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "DataFrame.drop(): 'inplace' parameter should be a constant bool")
    if not is_overload_none(labels):
        if not is_overload_none(columns):
            raise BodoError(
                "Dataframe.drop(): Cannot specify both 'labels' and 'columns'")
        if not is_overload_constant_int(axis) or get_overload_const_int(axis
            ) != 1:
            raise_bodo_error('DataFrame.drop(): only axis=1 supported')
        if is_overload_constant_str(labels):
            pht__crkw = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            pht__crkw = get_overload_const_list(labels)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    else:
        if is_overload_none(columns):
            raise BodoError(
                "DataFrame.drop(): Need to specify at least one of 'labels' or 'columns'"
                )
        if is_overload_constant_str(columns):
            pht__crkw = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            pht__crkw = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for utksr__kqk in pht__crkw:
        if utksr__kqk not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(utksr__kqk, df.columns))
    if len(set(pht__crkw)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    jfmy__yyot = tuple(utksr__kqk for utksr__kqk in df.columns if 
        utksr__kqk not in pht__crkw)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(utksr__kqk), '.copy()' if not inplace else
        '') for utksr__kqk in jfmy__yyot)
    drcci__rvyym = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    drcci__rvyym += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(drcci__rvyym, jfmy__yyot, data_args, index)


@overload_method(DataFrameType, 'append', inline='always', no_unliteral=True)
def overload_dataframe_append(df, other, ignore_index=False,
    verify_integrity=False, sort=None):
    check_runtime_cols_unsupported(df, 'DataFrame.append()')
    check_runtime_cols_unsupported(other, 'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'DataFrame.append()')
    if isinstance(other, DataFrameType):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df, other), ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.BaseTuple):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df,) + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.List) and isinstance(other.dtype, DataFrameType
        ):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat([df] + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    raise BodoError(
        'invalid df.append() input. Only dataframe and list/tuple of dataframes supported'
        )


@overload_method(DataFrameType, 'sample', inline='always', no_unliteral=True)
def overload_dataframe_sample(df, n=None, frac=None, replace=False, weights
    =None, random_state=None, axis=None, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sample()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sample()')
    zdnpn__vnd = dict(random_state=random_state, weights=weights, axis=axis,
        ignore_index=ignore_index)
    rdo__vcz = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', zdnpn__vnd, rdo__vcz,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    ajxgl__wnzb = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(ajxgl__wnzb))
    wjzd__vomc = ', '.join('rhs_data_{}'.format(i) for i in range(ajxgl__wnzb))
    drcci__rvyym = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    drcci__rvyym += '  if (frac == 1 or n == len(df)) and not replace:\n'
    drcci__rvyym += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(ajxgl__wnzb):
        drcci__rvyym += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    drcci__rvyym += '  if frac is None:\n'
    drcci__rvyym += '    frac_d = -1.0\n'
    drcci__rvyym += '  else:\n'
    drcci__rvyym += '    frac_d = frac\n'
    drcci__rvyym += '  if n is None:\n'
    drcci__rvyym += '    n_i = 0\n'
    drcci__rvyym += '  else:\n'
    drcci__rvyym += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    drcci__rvyym += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({wjzd__vomc},), {index}, n_i, frac_d, replace)
"""
    drcci__rvyym += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(drcci__rvyym, df.
        columns, data_args, 'index')


@numba.njit
def _sizeof_fmt(num, size_qualifier=''):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f}{size_qualifier} {x}'
        num /= 1024.0
    return f'{num:3.1f}{size_qualifier} PB'


@overload_method(DataFrameType, 'info', no_unliteral=True)
def overload_dataframe_info(df, verbose=None, buf=None, max_cols=None,
    memory_usage=None, show_counts=None, null_counts=None):
    check_runtime_cols_unsupported(df, 'DataFrame.info()')
    mlc__nacu = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    fwlnm__tsyl = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', mlc__nacu, fwlnm__tsyl,
        package_name='pandas', module_name='DataFrame')
    qndnr__rbvf = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            dhn__jzagj = qndnr__rbvf + '\n'
            dhn__jzagj += 'Index: 0 entries\n'
            dhn__jzagj += 'Empty DataFrame'
            print(dhn__jzagj)
        return _info_impl
    else:
        drcci__rvyym = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        drcci__rvyym += '    ncols = df.shape[1]\n'
        drcci__rvyym += f'    lines = "{qndnr__rbvf}\\n"\n'
        drcci__rvyym += f'    lines += "{df.index}: "\n'
        drcci__rvyym += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            drcci__rvyym += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            drcci__rvyym += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            drcci__rvyym += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        drcci__rvyym += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        drcci__rvyym += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        drcci__rvyym += '    column_width = max(space, 7)\n'
        drcci__rvyym += '    column= "Column"\n'
        drcci__rvyym += '    underl= "------"\n'
        drcci__rvyym += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        drcci__rvyym += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        drcci__rvyym += '    mem_size = 0\n'
        drcci__rvyym += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        drcci__rvyym += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        drcci__rvyym += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        jgtr__xdoh = dict()
        for i in range(len(df.columns)):
            drcci__rvyym += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            sue__lozzx = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                sue__lozzx = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                xmfst__nklt = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                sue__lozzx = f'{xmfst__nklt[:-7]}'
            drcci__rvyym += f'    col_dtype[{i}] = "{sue__lozzx}"\n'
            if sue__lozzx in jgtr__xdoh:
                jgtr__xdoh[sue__lozzx] += 1
            else:
                jgtr__xdoh[sue__lozzx] = 1
            drcci__rvyym += f'    col_name[{i}] = "{df.columns[i]}"\n'
            drcci__rvyym += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        drcci__rvyym += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        drcci__rvyym += '    for i in column_info:\n'
        drcci__rvyym += "        lines += f'{i}\\n'\n"
        zycnn__ejwgs = ', '.join(f'{k}({jgtr__xdoh[k]})' for k in sorted(
            jgtr__xdoh))
        drcci__rvyym += f"    lines += 'dtypes: {zycnn__ejwgs}\\n'\n"
        drcci__rvyym += '    mem_size += df.index.nbytes\n'
        drcci__rvyym += '    total_size = _sizeof_fmt(mem_size)\n'
        drcci__rvyym += "    lines += f'memory usage: {total_size}'\n"
        drcci__rvyym += '    print(lines)\n'
        ukhx__aqlzo = {}
        exec(drcci__rvyym, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, ukhx__aqlzo)
        _info_impl = ukhx__aqlzo['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    drcci__rvyym = 'def impl(df, index=True, deep=False):\n'
    kqf__hwzpw = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes')
    qcbo__nnl = is_overload_true(index)
    columns = df.columns
    if qcbo__nnl:
        columns = ('Index',) + columns
    if len(columns) == 0:
        aikry__dmjxy = ()
    elif all(isinstance(utksr__kqk, int) for utksr__kqk in columns):
        aikry__dmjxy = np.array(columns, 'int64')
    elif all(isinstance(utksr__kqk, str) for utksr__kqk in columns):
        aikry__dmjxy = pd.array(columns, 'string')
    else:
        aikry__dmjxy = columns
    if df.is_table_format:
        onic__enz = int(qcbo__nnl)
        yay__clv = len(columns)
        drcci__rvyym += f'  nbytes_arr = np.empty({yay__clv}, np.int64)\n'
        drcci__rvyym += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        drcci__rvyym += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {onic__enz})
"""
        if qcbo__nnl:
            drcci__rvyym += f'  nbytes_arr[0] = {kqf__hwzpw}\n'
        drcci__rvyym += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if qcbo__nnl:
            data = f'{kqf__hwzpw},{data}'
        else:
            beyh__kzomw = ',' if len(columns) == 1 else ''
            data = f'{data}{beyh__kzomw}'
        drcci__rvyym += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        aikry__dmjxy}, ukhx__aqlzo)
    impl = ukhx__aqlzo['impl']
    return impl


@overload(pd.read_excel, no_unliteral=True)
def overload_read_excel(io, sheet_name=0, header=0, names=None, index_col=
    None, usecols=None, squeeze=False, dtype=None, engine=None, converters=
    None, true_values=None, false_values=None, skiprows=None, nrows=None,
    na_values=None, keep_default_na=True, na_filter=True, verbose=False,
    parse_dates=False, date_parser=None, thousands=None, comment=None,
    skipfooter=0, convert_float=True, mangle_dupe_cols=True, _bodo_df_type=None
    ):
    df_type = _bodo_df_type.instance_type
    pjyu__nwtt = 'read_excel_df{}'.format(next_label())
    setattr(types, pjyu__nwtt, df_type)
    qoipa__hze = False
    if is_overload_constant_list(parse_dates):
        qoipa__hze = get_overload_const_list(parse_dates)
    udnl__qoj = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    drcci__rvyym = f"""
def impl(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=True,
    mangle_dupe_cols=True,
    _bodo_df_type=None,
):
    with numba.objmode(df="{pjyu__nwtt}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{udnl__qoj}}},
            engine=engine,
            converters=converters,
            true_values=true_values,
            false_values=false_values,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            keep_default_na=keep_default_na,
            na_filter=na_filter,
            verbose=verbose,
            parse_dates={qoipa__hze},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    ukhx__aqlzo = {}
    exec(drcci__rvyym, globals(), ukhx__aqlzo)
    impl = ukhx__aqlzo['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as sgdlu__bhso:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    drcci__rvyym = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    drcci__rvyym += (
        '    ylabel=None, title=None, legend=True, fontsize=None, \n')
    drcci__rvyym += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        drcci__rvyym += '   fig, ax = plt.subplots()\n'
    else:
        drcci__rvyym += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        drcci__rvyym += '   fig.set_figwidth(figsize[0])\n'
        drcci__rvyym += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        drcci__rvyym += '   xlabel = x\n'
    drcci__rvyym += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        drcci__rvyym += '   ylabel = y\n'
    else:
        drcci__rvyym += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        drcci__rvyym += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        drcci__rvyym += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    drcci__rvyym += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            drcci__rvyym += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            mubf__fkmi = get_overload_const_str(x)
            brq__cnd = df.columns.index(mubf__fkmi)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if brq__cnd != i:
                        drcci__rvyym += f"""   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])
"""
        else:
            drcci__rvyym += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        drcci__rvyym += '   ax.scatter(df[x], df[y], s=20)\n'
        drcci__rvyym += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        drcci__rvyym += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        drcci__rvyym += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        drcci__rvyym += '   ax.legend()\n'
    drcci__rvyym += '   return ax\n'
    ukhx__aqlzo = {}
    exec(drcci__rvyym, {'bodo': bodo, 'plt': plt}, ukhx__aqlzo)
    impl = ukhx__aqlzo['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for jeuts__jdk in df_typ.data:
        if not (isinstance(jeuts__jdk, IntegerArrayType) or isinstance(
            jeuts__jdk.dtype, types.Number) or jeuts__jdk.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns)):
            return False
    return True


def typeref_to_type(v):
    if isinstance(v, types.BaseTuple):
        return types.BaseTuple.from_types(tuple(typeref_to_type(a) for a in v))
    return v.instance_type if isinstance(v, (types.TypeRef, types.NumberClass)
        ) else v


def _install_typer_for_type(type_name, typ):

    @type_callable(typ)
    def type_call_type(context):

        def typer(*args, **kws):
            args = tuple(typeref_to_type(v) for v in args)
            kws = {name: typeref_to_type(v) for name, v in kws.items()}
            return types.TypeRef(typ(*args, **kws))
        return typer
    no_side_effect_call_tuples.add((type_name, bodo))
    no_side_effect_call_tuples.add((typ,))


def _install_type_call_typers():
    for type_name in bodo_types_with_params:
        typ = getattr(bodo, type_name)
        _install_typer_for_type(type_name, typ)


_install_type_call_typers()


def set_df_col(df, cname, arr, inplace):
    df[cname] = arr


@infer_global(set_df_col)
class SetDfColInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 4
        assert isinstance(args[1], types.Literal)
        cbrqq__akofd = args[0]
        mjqi__xsdaq = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        nrj__godew = cbrqq__akofd
        check_runtime_cols_unsupported(cbrqq__akofd, 'set_df_col()')
        if isinstance(cbrqq__akofd, DataFrameType):
            index = cbrqq__akofd.index
            if len(cbrqq__akofd.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(cbrqq__akofd.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if mjqi__xsdaq in cbrqq__akofd.columns:
                jfmy__yyot = cbrqq__akofd.columns
                gvawb__kuey = cbrqq__akofd.columns.index(mjqi__xsdaq)
                zans__klfm = list(cbrqq__akofd.data)
                zans__klfm[gvawb__kuey] = val
                zans__klfm = tuple(zans__klfm)
            else:
                jfmy__yyot = cbrqq__akofd.columns + (mjqi__xsdaq,)
                zans__klfm = cbrqq__akofd.data + (val,)
            nrj__godew = DataFrameType(zans__klfm, index, jfmy__yyot,
                cbrqq__akofd.dist, cbrqq__akofd.is_table_format)
        return nrj__godew(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    kfyh__zgc = {}

    def _rewrite_membership_op(self, node, left, right):
        evd__lcv = node.op
        op = self.visit(evd__lcv)
        return op, evd__lcv, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    sda__vzob = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in sda__vzob:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in sda__vzob:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        cifn__pjxtf = node.attr
        value = node.value
        rjy__efyii = pd.core.computation.ops.LOCAL_TAG
        if cifn__pjxtf in ('str', 'dt'):
            try:
                vpoqd__tuut = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as btqkj__mqf:
                col_name = btqkj__mqf.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            vpoqd__tuut = str(self.visit(value))
        fbr__rruca = vpoqd__tuut, cifn__pjxtf
        if fbr__rruca in join_cleaned_cols:
            cifn__pjxtf = join_cleaned_cols[fbr__rruca]
        name = vpoqd__tuut + '.' + cifn__pjxtf
        if name.startswith(rjy__efyii):
            name = name[len(rjy__efyii):]
        if cifn__pjxtf in ('str', 'dt'):
            lln__zpzf = columns[cleaned_columns.index(vpoqd__tuut)]
            kfyh__zgc[lln__zpzf] = vpoqd__tuut
            self.env.scope[name] = 0
            return self.term_type(rjy__efyii + name, self.env)
        sda__vzob.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in sda__vzob:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        geg__yrrgn = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        mjqi__xsdaq = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(geg__yrrgn), mjqi__xsdaq))

    def op__str__(self):
        ubqw__xsyg = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            vre__cjd)) for vre__cjd in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(ubqw__xsyg)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(ubqw__xsyg)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(ubqw__xsyg))
    jwn__tey = pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op
    vum__vfq = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    cgi__hncw = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    rshwe__plwg = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    ozmf__pfn = pd.core.computation.ops.Term.__str__
    zmtl__uwq = pd.core.computation.ops.MathCall.__str__
    cdws__muuk = pd.core.computation.ops.Op.__str__
    leyd__cst = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
    try:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            _rewrite_membership_op)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            _maybe_evaluate_binop)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = (
            visit_Attribute)
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = lambda self, left, right: (left, right)
        pd.core.computation.ops.Term.__str__ = __str__
        pd.core.computation.ops.MathCall.__str__ = math__str__
        pd.core.computation.ops.Op.__str__ = op__str__
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        ldba__uzz = pd.core.computation.expr.Expr(expr, env=env)
        hwqp__ixszc = str(ldba__uzz)
    except pd.core.computation.ops.UndefinedVariableError as btqkj__mqf:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == btqkj__mqf.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {btqkj__mqf}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            jwn__tey)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            vum__vfq)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = cgi__hncw
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = rshwe__plwg
        pd.core.computation.ops.Term.__str__ = ozmf__pfn
        pd.core.computation.ops.MathCall.__str__ = zmtl__uwq
        pd.core.computation.ops.Op.__str__ = cdws__muuk
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            leyd__cst)
    irt__oftz = pd.core.computation.parsing.clean_column_name
    kfyh__zgc.update({utksr__kqk: irt__oftz(utksr__kqk) for utksr__kqk in
        columns if irt__oftz(utksr__kqk) in ldba__uzz.names})
    return ldba__uzz, hwqp__ixszc, kfyh__zgc


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        cct__rivww = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(cct__rivww))
        pmlv__rue = namedtuple('Pandas', col_names)
        vbp__kfmb = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], pmlv__rue)
        super(DataFrameTupleIterator, self).__init__(name, vbp__kfmb)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_series_dtype(arr_typ):
    if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return pd_timestamp_type
    return arr_typ.dtype


def get_itertuples():
    pass


@infer_global(get_itertuples)
class TypeIterTuples(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) % 2 == 0, 'name and column pairs expected'
        col_names = [a.literal_value for a in args[:len(args) // 2]]
        qdx__wlgdt = [if_series_to_array_type(a) for a in args[len(args) // 2:]
            ]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        qdx__wlgdt = [types.Array(types.int64, 1, 'C')] + qdx__wlgdt
        vohf__fpwl = DataFrameTupleIterator(col_names, qdx__wlgdt)
        return vohf__fpwl(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qqnwn__twv = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            qqnwn__twv)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    net__znye = args[len(args) // 2:]
    mklo__sbrb = sig.args[len(sig.args) // 2:]
    vgykp__xgky = context.make_helper(builder, sig.return_type)
    yhcna__wprzi = context.get_constant(types.intp, 0)
    fhu__auykk = cgutils.alloca_once_value(builder, yhcna__wprzi)
    vgykp__xgky.index = fhu__auykk
    for i, arr in enumerate(net__znye):
        setattr(vgykp__xgky, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(net__znye, mklo__sbrb):
        context.nrt.incref(builder, arr_typ, arr)
    res = vgykp__xgky._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    pgkb__ega, = sig.args
    oew__msh, = args
    vgykp__xgky = context.make_helper(builder, pgkb__ega, value=oew__msh)
    wdqw__gry = signature(types.intp, pgkb__ega.array_types[1])
    fvois__rdsah = context.compile_internal(builder, lambda a: len(a),
        wdqw__gry, [vgykp__xgky.array0])
    index = builder.load(vgykp__xgky.index)
    amlkc__xrr = builder.icmp_signed('<', index, fvois__rdsah)
    result.set_valid(amlkc__xrr)
    with builder.if_then(amlkc__xrr):
        values = [index]
        for i, arr_typ in enumerate(pgkb__ega.array_types[1:]):
            get__tgx = getattr(vgykp__xgky, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                pisnv__uva = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    pisnv__uva, [get__tgx, index])
            else:
                pisnv__uva = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    pisnv__uva, [get__tgx, index])
            values.append(val)
        value = context.make_tuple(builder, pgkb__ega.yield_type, values)
        result.yield_(value)
        bxkzs__wub = cgutils.increment_index(builder, index)
        builder.store(bxkzs__wub, vgykp__xgky.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    twid__nakun = ir.Assign(rhs, lhs, expr.loc)
    aanoz__jju = lhs
    rymlq__qur = []
    hoxco__xuo = []
    wzdf__aagx = typ.count
    for i in range(wzdf__aagx):
        dqhtp__qjlo = ir.Var(aanoz__jju.scope, mk_unique_var('{}_size{}'.
            format(aanoz__jju.name, i)), aanoz__jju.loc)
        dqfw__lygm = ir.Expr.static_getitem(lhs, i, None, aanoz__jju.loc)
        self.calltypes[dqfw__lygm] = None
        rymlq__qur.append(ir.Assign(dqfw__lygm, dqhtp__qjlo, aanoz__jju.loc))
        self._define(equiv_set, dqhtp__qjlo, types.intp, dqfw__lygm)
        hoxco__xuo.append(dqhtp__qjlo)
    tgr__kvf = tuple(hoxco__xuo)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        tgr__kvf, pre=[twid__nakun] + rymlq__qur)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
