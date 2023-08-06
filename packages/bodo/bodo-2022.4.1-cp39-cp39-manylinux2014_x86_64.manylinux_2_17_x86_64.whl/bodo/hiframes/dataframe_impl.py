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
        roh__gsaup = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({roh__gsaup})\n'
            )
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    vspxg__oba = 'def impl(df):\n'
    if df.has_runtime_cols:
        vspxg__oba += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        sgzy__xitgy = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        vspxg__oba += f'  return {sgzy__xitgy}'
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo}, gybiy__ltryi)
    impl = gybiy__ltryi['impl']
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
    itm__pmac = len(df.columns)
    yyhv__qkmb = set(i for i in range(itm__pmac) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in yyhv__qkmb else '') for i in
        range(itm__pmac))
    vspxg__oba = 'def f(df):\n'.format()
    vspxg__oba += '    return np.stack(({},), 1)\n'.format(data_args)
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo, 'np': np}, gybiy__ltryi)
    mturo__xtz = gybiy__ltryi['f']
    return mturo__xtz


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
    szm__btlav = {'dtype': dtype, 'na_value': na_value}
    tvrqn__rjkmh = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', szm__btlav, tvrqn__rjkmh,
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
            ant__tss = bodo.hiframes.table.compute_num_runtime_columns(t)
            return ant__tss * len(t)
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
            ant__tss = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), ant__tss
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), types.int64(ncols))


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.dtypes')
    vspxg__oba = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    pxn__bhuf = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    vspxg__oba += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{pxn__bhuf}), {index}, None)
"""
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo}, gybiy__ltryi)
    impl = gybiy__ltryi['impl']
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
    szm__btlav = {'copy': copy, 'errors': errors}
    tvrqn__rjkmh = {'copy': True, 'errors': 'raise'}
    check_unsupported_args('df.astype', szm__btlav, tvrqn__rjkmh,
        package_name='pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    extra_globals = None
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        zjl__qhr = _bodo_object_typeref.instance_type
        assert isinstance(zjl__qhr, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        extra_globals = {}
        nmyb__ivj = {}
        for i, name in enumerate(zjl__qhr.columns):
            arr_typ = zjl__qhr.data[i]
            if isinstance(arr_typ, IntegerArrayType):
                qedd__hbjvu = bodo.libs.int_arr_ext.IntDtype(arr_typ.dtype)
            elif arr_typ == boolean_array:
                qedd__hbjvu = boolean_dtype
            else:
                qedd__hbjvu = arr_typ.dtype
            extra_globals[f'_bodo_schema{i}'] = qedd__hbjvu
            nmyb__ivj[name] = f'_bodo_schema{i}'
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {nmyb__ivj[vyf__jlczl]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if vyf__jlczl in nmyb__ivj else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, vyf__jlczl in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        gghuf__vxk = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(gghuf__vxk[vyf__jlczl])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             if vyf__jlczl in gghuf__vxk else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for
            i, vyf__jlczl in enumerate(df.columns))
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
    ogep__jdimu = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(deep):
            ogep__jdimu.append(arr + '.copy()')
        elif is_overload_false(deep):
            ogep__jdimu.append(arr)
        else:
            ogep__jdimu.append(f'{arr}.copy() if deep else {arr}')
    header = 'def impl(df, deep=True):\n'
    return _gen_init_df(header, df.columns, ', '.join(ogep__jdimu))


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    szm__btlav = {'index': index, 'level': level, 'errors': errors}
    tvrqn__rjkmh = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', szm__btlav, tvrqn__rjkmh,
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
        eyhdm__lxxg = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        eyhdm__lxxg = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    jndv__ugmxf = [eyhdm__lxxg.get(df.columns[i], df.columns[i]) for i in
        range(len(df.columns))]
    ogep__jdimu = []
    for i in range(len(df.columns)):
        arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
        if is_overload_true(copy):
            ogep__jdimu.append(arr + '.copy()')
        elif is_overload_false(copy):
            ogep__jdimu.append(arr)
        else:
            ogep__jdimu.append(f'{arr}.copy() if copy else {arr}')
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    return _gen_init_df(header, jndv__ugmxf, ', '.join(ogep__jdimu))


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    srew__qgdbd = not is_overload_none(items)
    lbc__upk = not is_overload_none(like)
    hru__pddzp = not is_overload_none(regex)
    jftpi__ajy = srew__qgdbd ^ lbc__upk ^ hru__pddzp
    dwyxf__lad = not (srew__qgdbd or lbc__upk or hru__pddzp)
    if dwyxf__lad:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not jftpi__ajy:
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
        bxpqj__ycvcy = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        bxpqj__ycvcy = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert bxpqj__ycvcy in {0, 1}
    vspxg__oba = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if bxpqj__ycvcy == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if bxpqj__ycvcy == 1:
        vek__pvv = []
        xvy__mnxa = []
        dkoa__sjsfm = []
        if srew__qgdbd:
            if is_overload_constant_list(items):
                kttj__wqdu = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if lbc__upk:
            if is_overload_constant_str(like):
                uipu__tyy = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if hru__pddzp:
            if is_overload_constant_str(regex):
                dimpd__jodo = get_overload_const_str(regex)
                avjk__wccow = re.compile(dimpd__jodo)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, vyf__jlczl in enumerate(df.columns):
            if not is_overload_none(items
                ) and vyf__jlczl in kttj__wqdu or not is_overload_none(like
                ) and uipu__tyy in str(vyf__jlczl) or not is_overload_none(
                regex) and avjk__wccow.search(str(vyf__jlczl)):
                xvy__mnxa.append(vyf__jlczl)
                dkoa__sjsfm.append(i)
        for i in dkoa__sjsfm:
            var_name = f'data_{i}'
            vek__pvv.append(var_name)
            vspxg__oba += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(vek__pvv)
        return _gen_init_df(vspxg__oba, xvy__mnxa, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        ubih__praks = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([ubih__praks] * len(df.data)), df
            .index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': ubih__praks}
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
    pnghi__wgli = is_overload_none(include)
    tqidm__jcypx = is_overload_none(exclude)
    ykoc__sptq = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if pnghi__wgli and tqidm__jcypx:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not pnghi__wgli:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            vlr__vzas = [dtype_to_array_type(parse_dtype(elem, ykoc__sptq)) for
                elem in include]
        elif is_legal_input(include):
            vlr__vzas = [dtype_to_array_type(parse_dtype(include, ykoc__sptq))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        vlr__vzas = get_nullable_and_non_nullable_types(vlr__vzas)
        pwrr__fyxv = tuple(vyf__jlczl for i, vyf__jlczl in enumerate(df.
            columns) if df.data[i] in vlr__vzas)
    else:
        pwrr__fyxv = df.columns
    if not tqidm__jcypx:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            geju__smamj = [dtype_to_array_type(parse_dtype(elem, ykoc__sptq
                )) for elem in exclude]
        elif is_legal_input(exclude):
            geju__smamj = [dtype_to_array_type(parse_dtype(exclude,
                ykoc__sptq))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        geju__smamj = get_nullable_and_non_nullable_types(geju__smamj)
        pwrr__fyxv = tuple(vyf__jlczl for vyf__jlczl in pwrr__fyxv if df.
            data[df.columns.index(vyf__jlczl)] not in geju__smamj)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(vyf__jlczl)})'
         for vyf__jlczl in pwrr__fyxv)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, pwrr__fyxv, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    out_df_type = None
    if df.is_table_format:
        ubih__praks = types.Array(types.bool_, 1, 'C')
        out_df_type = DataFrameType(tuple([ubih__praks] * len(df.data)), df
            .index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': ubih__praks}
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
    tov__khgyy = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in tov__khgyy:
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
    tov__khgyy = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in tov__khgyy:
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
    vspxg__oba = 'def impl(df, values):\n'
    zcx__jll = {}
    xjurx__wcaqi = False
    if isinstance(values, DataFrameType):
        xjurx__wcaqi = True
        for i, vyf__jlczl in enumerate(df.columns):
            if vyf__jlczl in values.columns:
                dmp__iuzsv = 'val{}'.format(i)
                vspxg__oba += (
                    """  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {})
"""
                    .format(dmp__iuzsv, values.columns.index(vyf__jlczl)))
                zcx__jll[vyf__jlczl] = dmp__iuzsv
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        zcx__jll = {vyf__jlczl: 'values' for vyf__jlczl in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        dmp__iuzsv = 'data{}'.format(i)
        vspxg__oba += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(dmp__iuzsv, i))
        data.append(dmp__iuzsv)
    izlux__bby = ['out{}'.format(i) for i in range(len(df.columns))]
    pazt__lslk = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    lkaj__psd = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    edw__smy = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, duk__yfabt) in enumerate(zip(df.columns, data)):
        if cname in zcx__jll:
            qxu__gpq = zcx__jll[cname]
            if xjurx__wcaqi:
                vspxg__oba += pazt__lslk.format(duk__yfabt, qxu__gpq,
                    izlux__bby[i])
            else:
                vspxg__oba += lkaj__psd.format(duk__yfabt, qxu__gpq,
                    izlux__bby[i])
        else:
            vspxg__oba += edw__smy.format(izlux__bby[i])
    return _gen_init_df(vspxg__oba, df.columns, ','.join(izlux__bby))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    itm__pmac = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(itm__pmac))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    qrsnq__laii = [vyf__jlczl for vyf__jlczl, tflb__bml in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(tflb__bml.dtype)
        ]
    assert len(qrsnq__laii) != 0
    iraq__fvx = ''
    if not any(tflb__bml == types.float64 for tflb__bml in df.data):
        iraq__fvx = '.astype(np.float64)'
    otmym__rko = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(vyf__jlczl), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(vyf__jlczl)], IntegerArrayType) or
        df.data[df.columns.index(vyf__jlczl)] == boolean_array else '') for
        vyf__jlczl in qrsnq__laii)
    lev__lyhb = 'np.stack(({},), 1){}'.format(otmym__rko, iraq__fvx)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        qrsnq__laii)))
    index = f'{generate_col_to_index_func_text(qrsnq__laii)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(lev__lyhb)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, qrsnq__laii, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    fls__qwkzq = dict(ddof=ddof)
    tmng__cern = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    ohx__iddfi = '1' if is_overload_none(min_periods) else 'min_periods'
    qrsnq__laii = [vyf__jlczl for vyf__jlczl, tflb__bml in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(tflb__bml.dtype)
        ]
    if len(qrsnq__laii) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    iraq__fvx = ''
    if not any(tflb__bml == types.float64 for tflb__bml in df.data):
        iraq__fvx = '.astype(np.float64)'
    otmym__rko = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(vyf__jlczl), '.astype(np.float64)' if 
        isinstance(df.data[df.columns.index(vyf__jlczl)], IntegerArrayType) or
        df.data[df.columns.index(vyf__jlczl)] == boolean_array else '') for
        vyf__jlczl in qrsnq__laii)
    lev__lyhb = 'np.stack(({},), 1){}'.format(otmym__rko, iraq__fvx)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        qrsnq__laii)))
    index = f'pd.Index({qrsnq__laii})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(lev__lyhb)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        ohx__iddfi)
    return _gen_init_df(header, qrsnq__laii, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    fls__qwkzq = dict(axis=axis, level=level, numeric_only=numeric_only)
    tmng__cern = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    vspxg__oba = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    vspxg__oba += '  data = np.array([{}])\n'.format(data_args)
    sgzy__xitgy = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    vspxg__oba += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {sgzy__xitgy})\n'
        )
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo, 'np': np}, gybiy__ltryi)
    impl = gybiy__ltryi['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    fls__qwkzq = dict(axis=axis)
    tmng__cern = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    vspxg__oba = 'def impl(df, axis=0, dropna=True):\n'
    vspxg__oba += '  data = np.asarray(({},))\n'.format(data_args)
    sgzy__xitgy = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    vspxg__oba += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {sgzy__xitgy})\n'
        )
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo, 'np': np}, gybiy__ltryi)
    impl = gybiy__ltryi['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    fls__qwkzq = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    tmng__cern = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    fls__qwkzq = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    tmng__cern = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    fls__qwkzq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    tmng__cern = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    fls__qwkzq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    tmng__cern = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    fls__qwkzq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    tmng__cern = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    fls__qwkzq = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    tmng__cern = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    fls__qwkzq = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    tmng__cern = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    fls__qwkzq = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    tmng__cern = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    fls__qwkzq = dict(numeric_only=numeric_only, interpolation=interpolation)
    tmng__cern = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    fls__qwkzq = dict(axis=axis, skipna=skipna)
    tmng__cern = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for qykz__tqjhp in df.data:
        if not (bodo.utils.utils.is_np_array_typ(qykz__tqjhp) and (
            qykz__tqjhp.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(qykz__tqjhp.dtype, (types.Number, types.Boolean))) or
            isinstance(qykz__tqjhp, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or qykz__tqjhp in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {qykz__tqjhp} not supported.'
                )
        if isinstance(qykz__tqjhp, bodo.CategoricalArrayType
            ) and not qykz__tqjhp.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    fls__qwkzq = dict(axis=axis, skipna=skipna)
    tmng__cern = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for qykz__tqjhp in df.data:
        if not (bodo.utils.utils.is_np_array_typ(qykz__tqjhp) and (
            qykz__tqjhp.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(qykz__tqjhp.dtype, (types.Number, types.Boolean))) or
            isinstance(qykz__tqjhp, (bodo.IntegerArrayType, bodo.
            CategoricalArrayType)) or qykz__tqjhp in [bodo.boolean_array,
            bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {qykz__tqjhp} not supported.'
                )
        if isinstance(qykz__tqjhp, bodo.CategoricalArrayType
            ) and not qykz__tqjhp.dtype.ordered:
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
        qrsnq__laii = tuple(vyf__jlczl for vyf__jlczl, tflb__bml in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (tflb__bml.dtype))
        out_colnames = qrsnq__laii
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            fhw__ymb = [numba.np.numpy_support.as_dtype(df.data[df.columns.
                index(vyf__jlczl)].dtype) for vyf__jlczl in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(fhw__ymb, []))
    except NotImplementedError as ndcm__yrd:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    wse__jzw = ''
    if func_name in ('sum', 'prod'):
        wse__jzw = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    vspxg__oba = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, wse__jzw))
    if func_name == 'quantile':
        vspxg__oba = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        vspxg__oba = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        vspxg__oba += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        vspxg__oba += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        gybiy__ltryi)
    impl = gybiy__ltryi['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    fbwm__mul = ''
    if func_name in ('min', 'max'):
        fbwm__mul = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        fbwm__mul = ', dtype=np.float32'
    rte__nlmnr = f'bodo.libs.array_ops.array_op_{func_name}'
    uhgs__hum = ''
    if func_name in ['sum', 'prod']:
        uhgs__hum = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        uhgs__hum = 'index'
    elif func_name == 'quantile':
        uhgs__hum = 'q'
    elif func_name in ['std', 'var']:
        uhgs__hum = 'True, ddof'
    elif func_name == 'median':
        uhgs__hum = 'True'
    data_args = ', '.join(
        f'{rte__nlmnr}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(vyf__jlczl)}), {uhgs__hum})'
         for vyf__jlczl in out_colnames)
    vspxg__oba = ''
    if func_name in ('idxmax', 'idxmin'):
        vspxg__oba += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        vspxg__oba += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        vspxg__oba += '  data = np.asarray(({},){})\n'.format(data_args,
            fbwm__mul)
    vspxg__oba += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return vspxg__oba


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    pkhjk__nxgr = [df_type.columns.index(vyf__jlczl) for vyf__jlczl in
        out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in pkhjk__nxgr)
    osbj__baoc = '\n        '.join(f'row[{i}] = arr_{pkhjk__nxgr[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    bvrgn__adxer = f'len(arr_{pkhjk__nxgr[0]})'
    muay__jrkf = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum':
        'np.nansum', 'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in muay__jrkf:
        bkxvx__vgon = muay__jrkf[func_name]
        sljq__tux = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        vspxg__oba = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {bvrgn__adxer}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{sljq__tux})
    for i in numba.parfors.parfor.internal_prange(n):
        {osbj__baoc}
        A[i] = {bkxvx__vgon}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return vspxg__oba
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    fls__qwkzq = dict(fill_method=fill_method, limit=limit, freq=freq)
    tmng__cern = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', fls__qwkzq, tmng__cern,
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
    fls__qwkzq = dict(axis=axis, skipna=skipna)
    tmng__cern = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', fls__qwkzq, tmng__cern,
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
    fls__qwkzq = dict(skipna=skipna)
    tmng__cern = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', fls__qwkzq, tmng__cern,
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
    fls__qwkzq = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    tmng__cern = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    qrsnq__laii = [vyf__jlczl for vyf__jlczl, tflb__bml in zip(df.columns,
        df.data) if _is_describe_type(tflb__bml)]
    if len(qrsnq__laii) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    oub__kbfa = sum(df.data[df.columns.index(vyf__jlczl)].dtype == bodo.
        datetime64ns for vyf__jlczl in qrsnq__laii)

    def _get_describe(col_ind):
        gqs__vnlsd = df.data[col_ind].dtype == bodo.datetime64ns
        if oub__kbfa and oub__kbfa != len(qrsnq__laii):
            if gqs__vnlsd:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for vyf__jlczl in qrsnq__laii:
        col_ind = df.columns.index(vyf__jlczl)
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.columns.index(vyf__jlczl)) for
        vyf__jlczl in qrsnq__laii)
    avjs__dkkvx = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if oub__kbfa == len(qrsnq__laii):
        avjs__dkkvx = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif oub__kbfa:
        avjs__dkkvx = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({avjs__dkkvx})'
    return _gen_init_df(header, qrsnq__laii, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    fls__qwkzq = dict(axis=axis, convert=convert, is_copy=is_copy)
    tmng__cern = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', fls__qwkzq, tmng__cern,
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
    fls__qwkzq = dict(freq=freq, axis=axis, fill_value=fill_value)
    tmng__cern = dict(freq=None, axis=0, fill_value=None)
    check_unsupported_args('DataFrame.shift', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for jjyvx__imhq in df.data:
        if not is_supported_shift_array_type(jjyvx__imhq):
            raise BodoError(
                f'Dataframe.shift() column input type {jjyvx__imhq.dtype} not supported yet.'
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
    fls__qwkzq = dict(axis=axis)
    tmng__cern = dict(axis=0)
    check_unsupported_args('DataFrame.diff', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for jjyvx__imhq in df.data:
        if not (isinstance(jjyvx__imhq, types.Array) and (isinstance(
            jjyvx__imhq.dtype, types.Number) or jjyvx__imhq.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {jjyvx__imhq.dtype} not supported.'
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
    jsnmw__lrixj = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(jsnmw__lrixj)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        pxdm__otzn = get_overload_const_list(column)
    else:
        pxdm__otzn = [get_literal_value(column)]
    yfb__psme = {vyf__jlczl: i for i, vyf__jlczl in enumerate(df.columns)}
    hgew__blhf = [yfb__psme[vyf__jlczl] for vyf__jlczl in pxdm__otzn]
    for i in hgew__blhf:
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
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{hgew__blhf[0]})\n'
        )
    for i in range(n):
        if i in hgew__blhf:
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
    szm__btlav = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    tvrqn__rjkmh = {'inplace': False, 'append': False, 'verify_integrity': 
        False}
    check_unsupported_args('DataFrame.set_index', szm__btlav, tvrqn__rjkmh,
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
    columns = tuple(vyf__jlczl for vyf__jlczl in df.columns if vyf__jlczl !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    szm__btlav = {'inplace': inplace}
    tvrqn__rjkmh = {'inplace': False}
    check_unsupported_args('query', szm__btlav, tvrqn__rjkmh, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        cnob__oasg = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[cnob__oasg]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    szm__btlav = {'subset': subset, 'keep': keep}
    tvrqn__rjkmh = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', szm__btlav, tvrqn__rjkmh,
        package_name='pandas', module_name='DataFrame')
    itm__pmac = len(df.columns)
    vspxg__oba = "def impl(df, subset=None, keep='first'):\n"
    for i in range(itm__pmac):
        vspxg__oba += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    nwwc__hxfl = ', '.join(f'data_{i}' for i in range(itm__pmac))
    nwwc__hxfl += ',' if itm__pmac == 1 else ''
    vspxg__oba += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({nwwc__hxfl}))\n')
    vspxg__oba += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    vspxg__oba += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo}, gybiy__ltryi)
    impl = gybiy__ltryi['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    szm__btlav = {'keep': keep, 'inplace': inplace, 'ignore_index':
        ignore_index}
    tvrqn__rjkmh = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    qace__bvb = []
    if is_overload_constant_list(subset):
        qace__bvb = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        qace__bvb = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        qace__bvb = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    rorl__uwdt = []
    for col_name in qace__bvb:
        if col_name not in df.columns:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        rorl__uwdt.append(df.columns.index(col_name))
    check_unsupported_args('DataFrame.drop_duplicates', szm__btlav,
        tvrqn__rjkmh, package_name='pandas', module_name='DataFrame')
    zse__ydjgl = []
    if rorl__uwdt:
        for scjz__ldz in rorl__uwdt:
            if isinstance(df.data[scjz__ldz], bodo.MapArrayType):
                zse__ydjgl.append(df.columns[scjz__ldz])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                zse__ydjgl.append(col_name)
    if zse__ydjgl:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {zse__ydjgl} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    itm__pmac = len(df.columns)
    gjc__izlb = ['data_{}'.format(i) for i in rorl__uwdt]
    gvrqd__oal = ['data_{}'.format(i) for i in range(itm__pmac) if i not in
        rorl__uwdt]
    if gjc__izlb:
        vgw__misd = len(gjc__izlb)
    else:
        vgw__misd = itm__pmac
    lrmfm__aeqq = ', '.join(gjc__izlb + gvrqd__oal)
    data_args = ', '.join('data_{}'.format(i) for i in range(itm__pmac))
    vspxg__oba = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(itm__pmac):
        vspxg__oba += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    vspxg__oba += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(lrmfm__aeqq, index, vgw__misd))
    vspxg__oba += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(vspxg__oba, df.columns, data_args, 'index')


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
                yvgvw__rjk = {vyf__jlczl: i for i, vyf__jlczl in enumerate(
                    cond.columns)}

                def cond_str(i, gen_all_false):
                    if df.columns[i] in yvgvw__rjk:
                        return (
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(cond, {yvgvw__rjk[df.columns[i]]})'
                            )
                    else:
                        gen_all_false[0] = True
                        return 'all_false'
            elif isinstance(cond, types.Array):
                cond_str = lambda i, _: f'cond[:,{i}]'
        if not hasattr(other, 'ndim') or other.ndim == 1:
            qftv__lnse = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                other_map = {vyf__jlczl: i for i, vyf__jlczl in enumerate(
                    other.columns)}
                qftv__lnse = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other_map[df.columns[i]]})'
                     if df.columns[i] in other_map else 'None')
            elif isinstance(other, types.Array):
                qftv__lnse = lambda i: f'other[:,{i}]'
        itm__pmac = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {qftv__lnse(i)})'
             for i in range(itm__pmac))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        fms__vpp = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(fms__vpp)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    fls__qwkzq = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    tmng__cern = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', fls__qwkzq, tmng__cern,
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
    itm__pmac = len(df.columns)
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
        other_map = {vyf__jlczl: i for i, vyf__jlczl in enumerate(other.
            columns)}
        for i in range(itm__pmac):
            if df.columns[i] in other_map:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], other.data[other_map[df.columns[i]]]
                    )
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(itm__pmac):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , df.data[i], other.data)
    else:
        for i in range(itm__pmac):
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
        wqp__pqxv = 'out_df_type'
    else:
        wqp__pqxv = gen_const_tup(columns)
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    vspxg__oba = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, {wqp__pqxv})
"""
    gybiy__ltryi = {}
    byo__rlf = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba}
    byo__rlf.update(extra_globals)
    exec(vspxg__oba, byo__rlf, gybiy__ltryi)
    impl = gybiy__ltryi['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        qcc__bwnmp = pd.Index(lhs.columns)
        afe__brv = pd.Index(rhs.columns)
        xxv__gor, wkm__fzvxz, bythl__kwkr = qcc__bwnmp.join(afe__brv, how=
            'left' if is_inplace else 'outer', level=None, return_indexers=True
            )
        return tuple(xxv__gor), wkm__fzvxz, bythl__kwkr
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        brmse__lqyxn = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        xzvl__misxr = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, brmse__lqyxn)
        check_runtime_cols_unsupported(rhs, brmse__lqyxn)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                xxv__gor, wkm__fzvxz, bythl__kwkr = _get_binop_columns(lhs, rhs
                    )
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {fxqil__hgbjb}) {brmse__lqyxn}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {jgo__szzq})'
                     if fxqil__hgbjb != -1 and jgo__szzq != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for fxqil__hgbjb, jgo__szzq in zip(wkm__fzvxz,
                    bythl__kwkr))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, xxv__gor, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            fxoye__mqhc = []
            yvb__ici = []
            if op in xzvl__misxr:
                for i, lkzvh__bmuo in enumerate(lhs.data):
                    if is_common_scalar_dtype([lkzvh__bmuo.dtype, rhs]):
                        fxoye__mqhc.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {brmse__lqyxn} rhs'
                            )
                    else:
                        axi__tbc = f'arr{i}'
                        yvb__ici.append(axi__tbc)
                        fxoye__mqhc.append(axi__tbc)
                data_args = ', '.join(fxoye__mqhc)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {brmse__lqyxn} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(yvb__ici) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {axi__tbc} = np.empty(n, dtype=np.bool_)\n' for
                    axi__tbc in yvb__ici)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(axi__tbc, op ==
                    operator.ne) for axi__tbc in yvb__ici)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            fxoye__mqhc = []
            yvb__ici = []
            if op in xzvl__misxr:
                for i, lkzvh__bmuo in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, lkzvh__bmuo.dtype]):
                        fxoye__mqhc.append(
                            f'lhs {brmse__lqyxn} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        axi__tbc = f'arr{i}'
                        yvb__ici.append(axi__tbc)
                        fxoye__mqhc.append(axi__tbc)
                data_args = ', '.join(fxoye__mqhc)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, brmse__lqyxn) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(yvb__ici) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(axi__tbc) for axi__tbc in yvb__ici)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(axi__tbc, op ==
                    operator.ne) for axi__tbc in yvb__ici)
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
        fms__vpp = create_binary_op_overload(op)
        overload(op)(fms__vpp)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        brmse__lqyxn = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, brmse__lqyxn)
        check_runtime_cols_unsupported(right, brmse__lqyxn)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                xxv__gor, _, bythl__kwkr = _get_binop_columns(left, right, True
                    )
                vspxg__oba = 'def impl(left, right):\n'
                for i, jgo__szzq in enumerate(bythl__kwkr):
                    if jgo__szzq == -1:
                        vspxg__oba += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    vspxg__oba += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    vspxg__oba += f"""  df_arr{i} {brmse__lqyxn} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {jgo__szzq})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    xxv__gor)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(vspxg__oba, xxv__gor, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            vspxg__oba = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                vspxg__oba += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                vspxg__oba += '  df_arr{0} {1} right\n'.format(i, brmse__lqyxn)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(vspxg__oba, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        fms__vpp = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(fms__vpp)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            brmse__lqyxn = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, brmse__lqyxn)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, brmse__lqyxn) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        fms__vpp = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(fms__vpp)


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
            bzq__sdaxp = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                bzq__sdaxp[i] = bodo.libs.array_kernels.isna(obj, i)
            return bzq__sdaxp
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
            bzq__sdaxp = np.empty(n, np.bool_)
            for i in range(n):
                bzq__sdaxp[i] = pd.isna(obj[i])
            return bzq__sdaxp
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
    szm__btlav = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    tvrqn__rjkmh = {'inplace': False, 'limit': None, 'regex': False,
        'method': 'pad'}
    check_unsupported_args('replace', szm__btlav, tvrqn__rjkmh,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    fpt__hihgp = str(expr_node)
    return fpt__hihgp.startswith('left.') or fpt__hihgp.startswith('right.')


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    imxe__irf = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (imxe__irf,))
    zxsqf__sptro = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        jjaas__onqsi = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        fyhqk__jca = {('NOT_NA', zxsqf__sptro(lkzvh__bmuo)): lkzvh__bmuo for
            lkzvh__bmuo in null_set}
        zdy__igj, _, _ = _parse_query_expr(jjaas__onqsi, env, [], [], None,
            join_cleaned_cols=fyhqk__jca)
        jtlmm__dgev = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            snd__hpsp = pd.core.computation.ops.BinOp('&', zdy__igj, expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = jtlmm__dgev
        return snd__hpsp

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                lxn__gvtj = set()
                ndmh__vqqna = set()
                eil__uin = _insert_NA_cond_body(expr_node.lhs, lxn__gvtj)
                atggd__fms = _insert_NA_cond_body(expr_node.rhs, ndmh__vqqna)
                ezfz__xyh = lxn__gvtj.intersection(ndmh__vqqna)
                lxn__gvtj.difference_update(ezfz__xyh)
                ndmh__vqqna.difference_update(ezfz__xyh)
                null_set.update(ezfz__xyh)
                expr_node.lhs = append_null_checks(eil__uin, lxn__gvtj)
                expr_node.rhs = append_null_checks(atggd__fms, ndmh__vqqna)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            xuk__egsbv = expr_node.name
            bizg__uppi, col_name = xuk__egsbv.split('.')
            if bizg__uppi == 'left':
                gev__pljh = left_columns
                data = left_data
            else:
                gev__pljh = right_columns
                data = right_data
            zmtn__iuon = data[gev__pljh.index(col_name)]
            if bodo.utils.typing.is_nullable(zmtn__iuon):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    qazqr__pczgq = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        qttcy__otfw = str(expr_node.lhs)
        rizxr__sph = str(expr_node.rhs)
        if qttcy__otfw.startswith('left.') and rizxr__sph.startswith('left.'
            ) or qttcy__otfw.startswith('right.') and rizxr__sph.startswith(
            'right.'):
            return [], [], expr_node
        left_on = [qttcy__otfw.split('.')[1]]
        right_on = [rizxr__sph.split('.')[1]]
        if qttcy__otfw.startswith('right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        fjyex__zsotu, yek__vqau, crm__kurx = _extract_equal_conds(expr_node.lhs
            )
        yyddo__xefm, bctkf__clyyn, fzyr__fsx = _extract_equal_conds(expr_node
            .rhs)
        left_on = fjyex__zsotu + yyddo__xefm
        right_on = yek__vqau + bctkf__clyyn
        if crm__kurx is None:
            return left_on, right_on, fzyr__fsx
        if fzyr__fsx is None:
            return left_on, right_on, crm__kurx
        expr_node.lhs = crm__kurx
        expr_node.rhs = fzyr__fsx
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    imxe__irf = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (imxe__irf,))
    eyhdm__lxxg = dict()
    zxsqf__sptro = pd.core.computation.parsing.clean_column_name
    for name, anf__vamv in (('left', left_columns), ('right', right_columns)):
        for lkzvh__bmuo in anf__vamv:
            bzo__ftdjl = zxsqf__sptro(lkzvh__bmuo)
            ghndh__mvkl = name, bzo__ftdjl
            if ghndh__mvkl in eyhdm__lxxg:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{lkzvh__bmuo}' and '{eyhdm__lxxg[bzo__ftdjl]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            eyhdm__lxxg[ghndh__mvkl] = lkzvh__bmuo
    xbk__vzqcw, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=eyhdm__lxxg)
    left_on, right_on, foha__rko = _extract_equal_conds(xbk__vzqcw.terms)
    return left_on, right_on, _insert_NA_cond(foha__rko, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    fls__qwkzq = dict(sort=sort, copy=copy, validate=validate)
    tmng__cern = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    rxs__hgwjd = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    tgmd__ubjnp = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in rxs__hgwjd and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, osmn__aajy = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if osmn__aajy is None:
                    tgmd__ubjnp = ''
                else:
                    tgmd__ubjnp = str(osmn__aajy)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = rxs__hgwjd
        right_keys = rxs__hgwjd
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
    tlvbw__cxv = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        ntwas__bmpad = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        ntwas__bmpad = list(get_overload_const_list(suffixes))
    suffix_x = ntwas__bmpad[0]
    suffix_y = ntwas__bmpad[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    vspxg__oba = "def _impl(left, right, how='inner', on=None, left_on=None,\n"
    vspxg__oba += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    vspxg__oba += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    vspxg__oba += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, tlvbw__cxv, tgmd__ubjnp))
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo}, gybiy__ltryi)
    _impl = gybiy__ltryi['_impl']
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
    wdn__thh = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    hdov__qvfc = {get_overload_const_str(azptr__sasj) for azptr__sasj in (
        left_on, right_on, on) if is_overload_constant_str(azptr__sasj)}
    for df in (left, right):
        for i, lkzvh__bmuo in enumerate(df.data):
            if not isinstance(lkzvh__bmuo, valid_dataframe_column_types
                ) and lkzvh__bmuo not in wdn__thh:
                raise BodoError(
                    f'{name_func}(): use of column with {type(lkzvh__bmuo)} in merge unsupported'
                    )
            if df.columns[i] in hdov__qvfc and isinstance(lkzvh__bmuo,
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
        ntwas__bmpad = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        ntwas__bmpad = list(get_overload_const_list(suffixes))
    if len(ntwas__bmpad) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    rxs__hgwjd = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        mihq__rkkra = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            mihq__rkkra = on_str not in rxs__hgwjd and ('left.' in on_str or
                'right.' in on_str)
        if len(rxs__hgwjd) == 0 and not mihq__rkkra:
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
    kmb__oalrm = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            rfm__alj = left.index
            kraa__pukau = isinstance(rfm__alj, StringIndexType)
            wvgqv__oayu = right.index
            ifg__kxd = isinstance(wvgqv__oayu, StringIndexType)
        elif is_overload_true(left_index):
            rfm__alj = left.index
            kraa__pukau = isinstance(rfm__alj, StringIndexType)
            wvgqv__oayu = right.data[right.columns.index(right_keys[0])]
            ifg__kxd = wvgqv__oayu.dtype == string_type
        elif is_overload_true(right_index):
            rfm__alj = left.data[left.columns.index(left_keys[0])]
            kraa__pukau = rfm__alj.dtype == string_type
            wvgqv__oayu = right.index
            ifg__kxd = isinstance(wvgqv__oayu, StringIndexType)
        if kraa__pukau and ifg__kxd:
            return
        rfm__alj = rfm__alj.dtype
        wvgqv__oayu = wvgqv__oayu.dtype
        try:
            yrbja__crv = kmb__oalrm.resolve_function_type(operator.eq, (
                rfm__alj, wvgqv__oayu), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=rfm__alj, rk_dtype=wvgqv__oayu))
    else:
        for dns__jpb, nvht__eeqgu in zip(left_keys, right_keys):
            rfm__alj = left.data[left.columns.index(dns__jpb)].dtype
            kwcl__ekk = left.data[left.columns.index(dns__jpb)]
            wvgqv__oayu = right.data[right.columns.index(nvht__eeqgu)].dtype
            evyjr__cfll = right.data[right.columns.index(nvht__eeqgu)]
            if kwcl__ekk == evyjr__cfll:
                continue
            iry__foqk = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=dns__jpb, lk_dtype=rfm__alj, rk=nvht__eeqgu,
                rk_dtype=wvgqv__oayu))
            syeg__xrd = rfm__alj == string_type
            sra__nxpw = wvgqv__oayu == string_type
            if syeg__xrd ^ sra__nxpw:
                raise_bodo_error(iry__foqk)
            try:
                yrbja__crv = kmb__oalrm.resolve_function_type(operator.eq,
                    (rfm__alj, wvgqv__oayu), {})
            except:
                raise_bodo_error(iry__foqk)


def validate_keys(keys, df):
    tfb__qvv = set(keys).difference(set(df.columns))
    if len(tfb__qvv) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in tfb__qvv:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {tfb__qvv} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    fls__qwkzq = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    tmng__cern = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', fls__qwkzq, tmng__cern,
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
    vspxg__oba = "def _impl(left, other, on=None, how='left',\n"
    vspxg__oba += "    lsuffix='', rsuffix='', sort=False):\n"
    vspxg__oba += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo}, gybiy__ltryi)
    _impl = gybiy__ltryi['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        ehe__zusk = get_overload_const_list(on)
        validate_keys(ehe__zusk, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    rxs__hgwjd = tuple(set(left.columns) & set(other.columns))
    if len(rxs__hgwjd) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=rxs__hgwjd))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    vhhbv__riptb = set(left_keys) & set(right_keys)
    tiw__pqnz = set(left_columns) & set(right_columns)
    ilbs__ngeim = tiw__pqnz - vhhbv__riptb
    rcf__eus = set(left_columns) - tiw__pqnz
    yzbd__hkgnu = set(right_columns) - tiw__pqnz
    cil__uovbo = {}

    def insertOutColumn(col_name):
        if col_name in cil__uovbo:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        cil__uovbo[col_name] = 0
    for aocm__xsfiz in vhhbv__riptb:
        insertOutColumn(aocm__xsfiz)
    for aocm__xsfiz in ilbs__ngeim:
        jzzh__pivcp = str(aocm__xsfiz) + suffix_x
        gfo__onkha = str(aocm__xsfiz) + suffix_y
        insertOutColumn(jzzh__pivcp)
        insertOutColumn(gfo__onkha)
    for aocm__xsfiz in rcf__eus:
        insertOutColumn(aocm__xsfiz)
    for aocm__xsfiz in yzbd__hkgnu:
        insertOutColumn(aocm__xsfiz)
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
    rxs__hgwjd = tuple(sorted(set(left.columns) & set(right.columns), key=
        lambda k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = rxs__hgwjd
        right_keys = rxs__hgwjd
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
        ntwas__bmpad = suffixes
    if is_overload_constant_list(suffixes):
        ntwas__bmpad = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        ntwas__bmpad = suffixes.value
    suffix_x = ntwas__bmpad[0]
    suffix_y = ntwas__bmpad[1]
    vspxg__oba = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    vspxg__oba += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    vspxg__oba += "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n"
    vspxg__oba += "    allow_exact_matches=True, direction='backward'):\n"
    vspxg__oba += '  suffix_x = suffixes[0]\n'
    vspxg__oba += '  suffix_y = suffixes[1]\n'
    vspxg__oba += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo}, gybiy__ltryi)
    _impl = gybiy__ltryi['_impl']
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
    fls__qwkzq = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    jjfcv__zobyx = dict(sort=False, group_keys=True, squeeze=False,
        observed=True)
    check_unsupported_args('Dataframe.groupby', fls__qwkzq, jjfcv__zobyx,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    dstk__commg = func_name == 'DataFrame.pivot_table'
    if dstk__commg:
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
    sjpe__isdgm = get_literal_value(columns)
    if isinstance(sjpe__isdgm, (list, tuple)):
        if len(sjpe__isdgm) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {sjpe__isdgm}"
                )
        sjpe__isdgm = sjpe__isdgm[0]
    if sjpe__isdgm not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {sjpe__isdgm} not found in DataFrame {df}."
            )
    qfqh__yexcm = {vyf__jlczl: i for i, vyf__jlczl in enumerate(df.columns)}
    vckfb__msml = qfqh__yexcm[sjpe__isdgm]
    if is_overload_none(index):
        mzr__aoya = []
        qsipu__doj = []
    else:
        qsipu__doj = get_literal_value(index)
        if not isinstance(qsipu__doj, (list, tuple)):
            qsipu__doj = [qsipu__doj]
        mzr__aoya = []
        for index in qsipu__doj:
            if index not in qfqh__yexcm:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            mzr__aoya.append(qfqh__yexcm[index])
    if not (all(isinstance(vyf__jlczl, int) for vyf__jlczl in qsipu__doj) or
        all(isinstance(vyf__jlczl, str) for vyf__jlczl in qsipu__doj)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        tblb__lal = []
        yatnp__yldse = []
        zet__vdee = mzr__aoya + [vckfb__msml]
        for i, vyf__jlczl in enumerate(df.columns):
            if i not in zet__vdee:
                tblb__lal.append(i)
                yatnp__yldse.append(vyf__jlczl)
    else:
        yatnp__yldse = get_literal_value(values)
        if not isinstance(yatnp__yldse, (list, tuple)):
            yatnp__yldse = [yatnp__yldse]
        tblb__lal = []
        for val in yatnp__yldse:
            if val not in qfqh__yexcm:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            tblb__lal.append(qfqh__yexcm[val])
    if all(isinstance(vyf__jlczl, int) for vyf__jlczl in yatnp__yldse):
        yatnp__yldse = np.array(yatnp__yldse, 'int64')
    elif all(isinstance(vyf__jlczl, str) for vyf__jlczl in yatnp__yldse):
        yatnp__yldse = pd.array(yatnp__yldse, 'string')
    else:
        raise BodoError(
            f"{func_name}(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    uqy__kkhkz = set(tblb__lal) | set(mzr__aoya) | {vckfb__msml}
    if len(uqy__kkhkz) != len(tblb__lal) + len(mzr__aoya) + 1:
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
    if len(mzr__aoya) == 0:
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
        for gixg__hah in mzr__aoya:
            index_column = df.data[gixg__hah]
            check_valid_index_typ(index_column)
    who__uoxmd = df.data[vckfb__msml]
    if isinstance(who__uoxmd, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(who__uoxmd, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for jssr__nqg in tblb__lal:
        psww__csx = df.data[jssr__nqg]
        if isinstance(psww__csx, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or psww__csx == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (qsipu__doj, sjpe__isdgm, yatnp__yldse, mzr__aoya, vckfb__msml,
        tblb__lal)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (qsipu__doj, sjpe__isdgm, yatnp__yldse, gixg__hah, vckfb__msml, jycr__cecin
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(qsipu__doj) == 0:
        if is_overload_none(data.index.name_typ):
            qsipu__doj = [None]
        else:
            qsipu__doj = [get_literal_value(data.index.name_typ)]
    if len(yatnp__yldse) == 1:
        zxs__dzrf = None
    else:
        zxs__dzrf = yatnp__yldse
    vspxg__oba = 'def impl(data, index=None, columns=None, values=None):\n'
    vspxg__oba += f'    pivot_values = data.iloc[:, {vckfb__msml}].unique()\n'
    vspxg__oba += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(gixg__hah) == 0:
        vspxg__oba += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        vspxg__oba += '        (\n'
        for oyy__kkcpl in gixg__hah:
            vspxg__oba += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {oyy__kkcpl}),
"""
        vspxg__oba += '        ),\n'
    vspxg__oba += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {vckfb__msml}),),
"""
    vspxg__oba += '        (\n'
    for jssr__nqg in jycr__cecin:
        vspxg__oba += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {jssr__nqg}),
"""
    vspxg__oba += '        ),\n'
    vspxg__oba += '        pivot_values,\n'
    vspxg__oba += '        index_lit_tup,\n'
    vspxg__oba += '        columns_lit,\n'
    vspxg__oba += '        values_name_const,\n'
    vspxg__oba += '    )\n'
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo, 'index_lit_tup': tuple(qsipu__doj),
        'columns_lit': sjpe__isdgm, 'values_name_const': zxs__dzrf},
        gybiy__ltryi)
    impl = gybiy__ltryi['impl']
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
    fls__qwkzq = dict(fill_value=fill_value, margins=margins, dropna=dropna,
        margins_name=margins_name, observed=observed, sort=sort)
    tmng__cern = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    if _pivot_values is None:
        (qsipu__doj, sjpe__isdgm, yatnp__yldse, gixg__hah, vckfb__msml,
            jycr__cecin) = (pivot_error_checking(data, index, columns,
            values, 'DataFrame.pivot_table'))
        if len(yatnp__yldse) == 1:
            zxs__dzrf = None
        else:
            zxs__dzrf = yatnp__yldse
        vspxg__oba = 'def impl(\n'
        vspxg__oba += '    data,\n'
        vspxg__oba += '    values=None,\n'
        vspxg__oba += '    index=None,\n'
        vspxg__oba += '    columns=None,\n'
        vspxg__oba += '    aggfunc="mean",\n'
        vspxg__oba += '    fill_value=None,\n'
        vspxg__oba += '    margins=False,\n'
        vspxg__oba += '    dropna=True,\n'
        vspxg__oba += '    margins_name="All",\n'
        vspxg__oba += '    observed=False,\n'
        vspxg__oba += '    sort=True,\n'
        vspxg__oba += '    _pivot_values=None,\n'
        vspxg__oba += '):\n'
        towyt__tpx = gixg__hah + [vckfb__msml] + jycr__cecin
        vspxg__oba += f'    data = data.iloc[:, {towyt__tpx}]\n'
        yqg__ywy = qsipu__doj + [sjpe__isdgm]
        vspxg__oba += (
            f'    data = data.groupby({yqg__ywy!r}, as_index=False).agg(aggfunc)\n'
            )
        vspxg__oba += (
            f'    pivot_values = data.iloc[:, {len(gixg__hah)}].unique()\n')
        vspxg__oba += '    return bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
        vspxg__oba += '        (\n'
        for i in range(0, len(gixg__hah)):
            vspxg__oba += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        vspxg__oba += '        ),\n'
        vspxg__oba += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(gixg__hah)}),),
"""
        vspxg__oba += '        (\n'
        for i in range(len(gixg__hah) + 1, len(jycr__cecin) + len(gixg__hah
            ) + 1):
            vspxg__oba += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
        vspxg__oba += '        ),\n'
        vspxg__oba += '        pivot_values,\n'
        vspxg__oba += '        index_lit_tup,\n'
        vspxg__oba += '        columns_lit,\n'
        vspxg__oba += '        values_name_const,\n'
        vspxg__oba += '        check_duplicates=False,\n'
        vspxg__oba += '    )\n'
        gybiy__ltryi = {}
        exec(vspxg__oba, {'bodo': bodo, 'numba': numba, 'index_lit_tup':
            tuple(qsipu__doj), 'columns_lit': sjpe__isdgm,
            'values_name_const': zxs__dzrf}, gybiy__ltryi)
        impl = gybiy__ltryi['impl']
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
    fls__qwkzq = dict(var_name=var_name, value_name=value_name, col_level=
        col_level, ignore_index=ignore_index)
    tmng__cern = dict(var_name=None, value_name='value', col_level=None,
        ignore_index=True)
    check_unsupported_args('DataFrame.melt', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(frame, DataFrameType):
        raise BodoError("pandas.melt(): 'frame' argument must be a DataFrame")
    if not is_overload_none(id_vars) and not is_literal_type(id_vars):
        raise BodoError(
            "DataFrame.melt(): 'id_vars', if specified, must be a literal")
    if not is_overload_none(value_vars) and not is_literal_type(value_vars):
        raise BodoError(
            "DataFrame.melt(): 'value_vars', if specified, must be a literal")
    rlf__ucabo = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(rlf__ucabo, (list, tuple)):
        rlf__ucabo = [rlf__ucabo]
    for vyf__jlczl in rlf__ucabo:
        if vyf__jlczl not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {vyf__jlczl} not found in {frame}"
                )
    eyhdm__lxxg = {vyf__jlczl: i for i, vyf__jlczl in enumerate(frame.columns)}
    rqhu__wnomy = [eyhdm__lxxg[i] for i in rlf__ucabo]
    if is_overload_none(value_vars):
        lpl__hjc = []
        mudpv__nuqy = []
        for i, vyf__jlczl in enumerate(frame.columns):
            if i not in rqhu__wnomy:
                lpl__hjc.append(i)
                mudpv__nuqy.append(vyf__jlczl)
    else:
        mudpv__nuqy = get_literal_value(value_vars)
        if not isinstance(mudpv__nuqy, (list, tuple)):
            mudpv__nuqy = [mudpv__nuqy]
        mudpv__nuqy = [v for v in mudpv__nuqy if v not in rlf__ucabo]
        if not mudpv__nuqy:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        lpl__hjc = []
        for val in mudpv__nuqy:
            if val not in eyhdm__lxxg:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            lpl__hjc.append(eyhdm__lxxg[val])
    for vyf__jlczl in mudpv__nuqy:
        if vyf__jlczl not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {vyf__jlczl} not found in {frame}"
                )
    if not (all(isinstance(vyf__jlczl, int) for vyf__jlczl in mudpv__nuqy) or
        all(isinstance(vyf__jlczl, str) for vyf__jlczl in mudpv__nuqy)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    lexcp__koqtr = frame.data[lpl__hjc[0]]
    vdue__eeqtt = [frame.data[i].dtype for i in lpl__hjc]
    lpl__hjc = np.array(lpl__hjc, dtype=np.int64)
    rqhu__wnomy = np.array(rqhu__wnomy, dtype=np.int64)
    _, zpv__mfrx = bodo.utils.typing.get_common_scalar_dtype(vdue__eeqtt)
    if not zpv__mfrx:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': mudpv__nuqy, 'val_type':
        lexcp__koqtr}
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
    if frame.is_table_format and all(v == lexcp__koqtr.dtype for v in
        vdue__eeqtt):
        extra_globals['value_idxs'] = lpl__hjc
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(mudpv__nuqy) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {lpl__hjc[0]})
"""
    else:
        wmc__phuvf = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in lpl__hjc)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({wmc__phuvf},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in rqhu__wnomy:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(mudpv__nuqy)})\n'
            )
    jxl__ktnhd = ', '.join(f'out_id{i}' for i in rqhu__wnomy) + (', ' if 
        len(rqhu__wnomy) > 0 else '')
    data_args = jxl__ktnhd + 'var_col, val_col'
    columns = tuple(rlf__ucabo + ['variable', 'value'])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(mudpv__nuqy)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    fls__qwkzq = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    tmng__cern = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', fls__qwkzq, tmng__cern,
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
    fls__qwkzq = dict(ignore_index=ignore_index, key=key)
    tmng__cern = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', fls__qwkzq, tmng__cern,
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
    hiqyd__lodu = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        hiqyd__lodu.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        mts__zjki = [get_overload_const_tuple(by)]
    else:
        mts__zjki = get_overload_const_list(by)
    mts__zjki = set((k, '') if (k, '') in hiqyd__lodu else k for k in mts__zjki
        )
    if len(mts__zjki.difference(hiqyd__lodu)) > 0:
        onas__nhbe = list(set(get_overload_const_list(by)).difference(
            hiqyd__lodu))
        raise_bodo_error(f'sort_values(): invalid keys {onas__nhbe} for by.')
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
        tzwie__exf = get_overload_const_list(na_position)
        for na_position in tzwie__exf:
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
    fls__qwkzq = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    tmng__cern = dict(axis=0, level=None, kind='quicksort', sort_remaining=
        True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', fls__qwkzq, tmng__cern,
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
    fls__qwkzq = dict(limit=limit, downcast=downcast)
    tmng__cern = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', fls__qwkzq, tmng__cern,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    hru__krlqz = not is_overload_none(value)
    mqedi__xtmn = not is_overload_none(method)
    if hru__krlqz and mqedi__xtmn:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not hru__krlqz and not mqedi__xtmn:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if hru__krlqz:
        whfcq__usmzf = 'value=value'
    else:
        whfcq__usmzf = 'method=method'
    data_args = [(
        f"df['{vyf__jlczl}'].fillna({whfcq__usmzf}, inplace=inplace)" if
        isinstance(vyf__jlczl, str) else
        f'df[{vyf__jlczl}].fillna({whfcq__usmzf}, inplace=inplace)') for
        vyf__jlczl in df.columns]
    vspxg__oba = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        vspxg__oba += '  ' + '  \n'.join(data_args) + '\n'
        gybiy__ltryi = {}
        exec(vspxg__oba, {}, gybiy__ltryi)
        impl = gybiy__ltryi['impl']
        return impl
    else:
        return _gen_init_df(vspxg__oba, df.columns, ', '.join(tflb__bml +
            '.values' for tflb__bml in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    fls__qwkzq = dict(col_level=col_level, col_fill=col_fill)
    tmng__cern = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', fls__qwkzq, tmng__cern,
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
    vspxg__oba = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    vspxg__oba += (
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
        jpf__wbke = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            jpf__wbke)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            vspxg__oba += (
                '  m_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
                )
            fiagh__bqs = ['m_index._data[{}]'.format(i) for i in range(df.
                index.nlevels)]
            data_args = fiagh__bqs + data_args
        else:
            jilnu__olqg = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [jilnu__olqg] + data_args
    return _gen_init_df(vspxg__oba, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    rqssu__ufyzu = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and rqssu__ufyzu == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(rqssu__ufyzu))


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
        hvo__qwd = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        lzs__ueqjf = get_overload_const_list(subset)
        hvo__qwd = []
        for xct__imp in lzs__ueqjf:
            if xct__imp not in df.columns:
                raise_bodo_error(
                    f"df.dropna(): column '{xct__imp}' not in data frame columns {df}"
                    )
            hvo__qwd.append(df.columns.index(xct__imp))
    itm__pmac = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(itm__pmac))
    vspxg__oba = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(itm__pmac):
        vspxg__oba += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    vspxg__oba += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in hvo__qwd)))
    vspxg__oba += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(vspxg__oba, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    fls__qwkzq = dict(index=index, level=level, errors=errors)
    tmng__cern = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', fls__qwkzq, tmng__cern,
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
            hqh__nxpn = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            hqh__nxpn = get_overload_const_list(labels)
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
            hqh__nxpn = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            hqh__nxpn = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for vyf__jlczl in hqh__nxpn:
        if vyf__jlczl not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(vyf__jlczl, df.columns))
    if len(set(hqh__nxpn)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    jndv__ugmxf = tuple(vyf__jlczl for vyf__jlczl in df.columns if 
        vyf__jlczl not in hqh__nxpn)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.columns.index(vyf__jlczl), '.copy()' if not inplace else
        '') for vyf__jlczl in jndv__ugmxf)
    vspxg__oba = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    vspxg__oba += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(vspxg__oba, jndv__ugmxf, data_args, index)


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
    fls__qwkzq = dict(random_state=random_state, weights=weights, axis=axis,
        ignore_index=ignore_index)
    slcg__iuwq = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', fls__qwkzq, slcg__iuwq,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    itm__pmac = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(itm__pmac))
    kxhvi__nwi = ', '.join('rhs_data_{}'.format(i) for i in range(itm__pmac))
    vspxg__oba = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    vspxg__oba += '  if (frac == 1 or n == len(df)) and not replace:\n'
    vspxg__oba += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(itm__pmac):
        vspxg__oba += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    vspxg__oba += '  if frac is None:\n'
    vspxg__oba += '    frac_d = -1.0\n'
    vspxg__oba += '  else:\n'
    vspxg__oba += '    frac_d = frac\n'
    vspxg__oba += '  if n is None:\n'
    vspxg__oba += '    n_i = 0\n'
    vspxg__oba += '  else:\n'
    vspxg__oba += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    vspxg__oba += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({kxhvi__nwi},), {index}, n_i, frac_d, replace)
"""
    vspxg__oba += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(vspxg__oba, df.columns,
        data_args, 'index')


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
    szm__btlav = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    tvrqn__rjkmh = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', szm__btlav, tvrqn__rjkmh,
        package_name='pandas', module_name='DataFrame')
    hxflz__bmue = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            uchr__yks = hxflz__bmue + '\n'
            uchr__yks += 'Index: 0 entries\n'
            uchr__yks += 'Empty DataFrame'
            print(uchr__yks)
        return _info_impl
    else:
        vspxg__oba = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        vspxg__oba += '    ncols = df.shape[1]\n'
        vspxg__oba += f'    lines = "{hxflz__bmue}\\n"\n'
        vspxg__oba += f'    lines += "{df.index}: "\n'
        vspxg__oba += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            vspxg__oba += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            vspxg__oba += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            vspxg__oba += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        vspxg__oba += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        vspxg__oba += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        vspxg__oba += '    column_width = max(space, 7)\n'
        vspxg__oba += '    column= "Column"\n'
        vspxg__oba += '    underl= "------"\n'
        vspxg__oba += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        vspxg__oba += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        vspxg__oba += '    mem_size = 0\n'
        vspxg__oba += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        vspxg__oba += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        vspxg__oba += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        kzeu__dtd = dict()
        for i in range(len(df.columns)):
            vspxg__oba += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            ebin__oqr = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                ebin__oqr = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                ngk__lid = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                ebin__oqr = f'{ngk__lid[:-7]}'
            vspxg__oba += f'    col_dtype[{i}] = "{ebin__oqr}"\n'
            if ebin__oqr in kzeu__dtd:
                kzeu__dtd[ebin__oqr] += 1
            else:
                kzeu__dtd[ebin__oqr] = 1
            vspxg__oba += f'    col_name[{i}] = "{df.columns[i]}"\n'
            vspxg__oba += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        vspxg__oba += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        vspxg__oba += '    for i in column_info:\n'
        vspxg__oba += "        lines += f'{i}\\n'\n"
        uuv__levy = ', '.join(f'{k}({kzeu__dtd[k]})' for k in sorted(kzeu__dtd)
            )
        vspxg__oba += f"    lines += 'dtypes: {uuv__levy}\\n'\n"
        vspxg__oba += '    mem_size += df.index.nbytes\n'
        vspxg__oba += '    total_size = _sizeof_fmt(mem_size)\n'
        vspxg__oba += "    lines += f'memory usage: {total_size}'\n"
        vspxg__oba += '    print(lines)\n'
        gybiy__ltryi = {}
        exec(vspxg__oba, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, gybiy__ltryi)
        _info_impl = gybiy__ltryi['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    vspxg__oba = 'def impl(df, index=True, deep=False):\n'
    lrt__juy = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes'
    cyniz__ksp = is_overload_true(index)
    columns = df.columns
    if cyniz__ksp:
        columns = ('Index',) + columns
    if len(columns) == 0:
        mgp__swgv = ()
    elif all(isinstance(vyf__jlczl, int) for vyf__jlczl in columns):
        mgp__swgv = np.array(columns, 'int64')
    elif all(isinstance(vyf__jlczl, str) for vyf__jlczl in columns):
        mgp__swgv = pd.array(columns, 'string')
    else:
        mgp__swgv = columns
    if df.is_table_format:
        kudpg__uhvl = int(cyniz__ksp)
        ant__tss = len(columns)
        vspxg__oba += f'  nbytes_arr = np.empty({ant__tss}, np.int64)\n'
        vspxg__oba += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        vspxg__oba += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {kudpg__uhvl})
"""
        if cyniz__ksp:
            vspxg__oba += f'  nbytes_arr[0] = {lrt__juy}\n'
        vspxg__oba += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if cyniz__ksp:
            data = f'{lrt__juy},{data}'
        else:
            pxn__bhuf = ',' if len(columns) == 1 else ''
            data = f'{data}{pxn__bhuf}'
        vspxg__oba += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        mgp__swgv}, gybiy__ltryi)
    impl = gybiy__ltryi['impl']
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
    wnfmx__xwb = 'read_excel_df{}'.format(next_label())
    setattr(types, wnfmx__xwb, df_type)
    ikz__yruyh = False
    if is_overload_constant_list(parse_dates):
        ikz__yruyh = get_overload_const_list(parse_dates)
    xgt__llz = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    vspxg__oba = f"""
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
    with numba.objmode(df="{wnfmx__xwb}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{xgt__llz}}},
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
            parse_dates={ikz__yruyh},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    gybiy__ltryi = {}
    exec(vspxg__oba, globals(), gybiy__ltryi)
    impl = gybiy__ltryi['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as ndcm__yrd:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    vspxg__oba = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    vspxg__oba += '    ylabel=None, title=None, legend=True, fontsize=None, \n'
    vspxg__oba += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        vspxg__oba += '   fig, ax = plt.subplots()\n'
    else:
        vspxg__oba += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        vspxg__oba += '   fig.set_figwidth(figsize[0])\n'
        vspxg__oba += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        vspxg__oba += '   xlabel = x\n'
    vspxg__oba += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        vspxg__oba += '   ylabel = y\n'
    else:
        vspxg__oba += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        vspxg__oba += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        vspxg__oba += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    vspxg__oba += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            vspxg__oba += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            qbzsb__qdgq = get_overload_const_str(x)
            rxyjy__fvsy = df.columns.index(qbzsb__qdgq)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if rxyjy__fvsy != i:
                        vspxg__oba += (
                            f'   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])\n'
                            )
        else:
            vspxg__oba += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        vspxg__oba += '   ax.scatter(df[x], df[y], s=20)\n'
        vspxg__oba += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        vspxg__oba += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        vspxg__oba += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        vspxg__oba += '   ax.legend()\n'
    vspxg__oba += '   return ax\n'
    gybiy__ltryi = {}
    exec(vspxg__oba, {'bodo': bodo, 'plt': plt}, gybiy__ltryi)
    impl = gybiy__ltryi['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for fymbl__orey in df_typ.data:
        if not (isinstance(fymbl__orey, IntegerArrayType) or isinstance(
            fymbl__orey.dtype, types.Number) or fymbl__orey.dtype in (bodo.
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
        oqniw__krq = args[0]
        djr__suyc = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        oprn__hgcuo = oqniw__krq
        check_runtime_cols_unsupported(oqniw__krq, 'set_df_col()')
        if isinstance(oqniw__krq, DataFrameType):
            index = oqniw__krq.index
            if len(oqniw__krq.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(oqniw__krq.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if not is_array_typ(val):
                val = dtype_to_array_type(val)
            if djr__suyc in oqniw__krq.columns:
                jndv__ugmxf = oqniw__krq.columns
                zpy__muo = oqniw__krq.columns.index(djr__suyc)
                ewkbd__kaf = list(oqniw__krq.data)
                ewkbd__kaf[zpy__muo] = val
                ewkbd__kaf = tuple(ewkbd__kaf)
            else:
                jndv__ugmxf = oqniw__krq.columns + (djr__suyc,)
                ewkbd__kaf = oqniw__krq.data + (val,)
            oprn__hgcuo = DataFrameType(ewkbd__kaf, index, jndv__ugmxf,
                oqniw__krq.dist, oqniw__krq.is_table_format)
        return oprn__hgcuo(*args)


SetDfColInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    rgghp__mpso = {}

    def _rewrite_membership_op(self, node, left, right):
        duebr__ntr = node.op
        op = self.visit(duebr__ntr)
        return op, duebr__ntr, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    oyew__zckym = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in oyew__zckym:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in oyew__zckym:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing(self.name)

    def visit_Attribute(self, node, **kwargs):
        sdd__hfcn = node.attr
        value = node.value
        uumm__nfxa = pd.core.computation.ops.LOCAL_TAG
        if sdd__hfcn in ('str', 'dt'):
            try:
                mss__kkij = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as croz__feru:
                col_name = croz__feru.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            mss__kkij = str(self.visit(value))
        ghndh__mvkl = mss__kkij, sdd__hfcn
        if ghndh__mvkl in join_cleaned_cols:
            sdd__hfcn = join_cleaned_cols[ghndh__mvkl]
        name = mss__kkij + '.' + sdd__hfcn
        if name.startswith(uumm__nfxa):
            name = name[len(uumm__nfxa):]
        if sdd__hfcn in ('str', 'dt'):
            tfd__idm = columns[cleaned_columns.index(mss__kkij)]
            rgghp__mpso[tfd__idm] = mss__kkij
            self.env.scope[name] = 0
            return self.term_type(uumm__nfxa + name, self.env)
        oyew__zckym.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in oyew__zckym:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        nkvkf__pipp = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        djr__suyc = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(nkvkf__pipp), djr__suyc))

    def op__str__(self):
        jcre__upy = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            vap__edv)) for vap__edv in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(jcre__upy)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(jcre__upy)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(jcre__upy))
    wol__aft = pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op
    hgda__fcpcq = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_evaluate_binop)
    fnt__fgc = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    noj__pmbpv = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    vqdv__eskt = pd.core.computation.ops.Term.__str__
    nzzrh__netzf = pd.core.computation.ops.MathCall.__str__
    tfbi__rgnyu = pd.core.computation.ops.Op.__str__
    jtlmm__dgev = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
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
        xbk__vzqcw = pd.core.computation.expr.Expr(expr, env=env)
        jbzdr__ntvi = str(xbk__vzqcw)
    except pd.core.computation.ops.UndefinedVariableError as croz__feru:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == croz__feru.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {croz__feru}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            wol__aft)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            hgda__fcpcq)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = fnt__fgc
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = noj__pmbpv
        pd.core.computation.ops.Term.__str__ = vqdv__eskt
        pd.core.computation.ops.MathCall.__str__ = nzzrh__netzf
        pd.core.computation.ops.Op.__str__ = tfbi__rgnyu
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            jtlmm__dgev)
    zvk__aiv = pd.core.computation.parsing.clean_column_name
    rgghp__mpso.update({vyf__jlczl: zvk__aiv(vyf__jlczl) for vyf__jlczl in
        columns if zvk__aiv(vyf__jlczl) in xbk__vzqcw.names})
    return xbk__vzqcw, jbzdr__ntvi, rgghp__mpso


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        ycszj__tvu = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(ycszj__tvu))
        ibv__ybb = namedtuple('Pandas', col_names)
        nak__ugbt = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], ibv__ybb)
        super(DataFrameTupleIterator, self).__init__(name, nak__ugbt)

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
        arwrm__wtgv = [if_series_to_array_type(a) for a in args[len(args) //
            2:]]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        arwrm__wtgv = [types.Array(types.int64, 1, 'C')] + arwrm__wtgv
        ueb__cnlyg = DataFrameTupleIterator(col_names, arwrm__wtgv)
        return ueb__cnlyg(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kavyn__rlyp = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            kavyn__rlyp)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    kskeu__chc = args[len(args) // 2:]
    tnwe__vsuqi = sig.args[len(sig.args) // 2:]
    oue__ewb = context.make_helper(builder, sig.return_type)
    xgltu__jrfks = context.get_constant(types.intp, 0)
    ndwdp__bvyjn = cgutils.alloca_once_value(builder, xgltu__jrfks)
    oue__ewb.index = ndwdp__bvyjn
    for i, arr in enumerate(kskeu__chc):
        setattr(oue__ewb, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(kskeu__chc, tnwe__vsuqi):
        context.nrt.incref(builder, arr_typ, arr)
    res = oue__ewb._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    lbzz__wno, = sig.args
    vyo__jafyb, = args
    oue__ewb = context.make_helper(builder, lbzz__wno, value=vyo__jafyb)
    oxm__xph = signature(types.intp, lbzz__wno.array_types[1])
    iuwk__ubzf = context.compile_internal(builder, lambda a: len(a),
        oxm__xph, [oue__ewb.array0])
    index = builder.load(oue__ewb.index)
    dqhg__zkjh = builder.icmp_signed('<', index, iuwk__ubzf)
    result.set_valid(dqhg__zkjh)
    with builder.if_then(dqhg__zkjh):
        values = [index]
        for i, arr_typ in enumerate(lbzz__wno.array_types[1:]):
            bpr__pkty = getattr(oue__ewb, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                ymqe__ygxim = signature(pd_timestamp_type, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    ymqe__ygxim, [bpr__pkty, index])
            else:
                ymqe__ygxim = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    ymqe__ygxim, [bpr__pkty, index])
            values.append(val)
        value = context.make_tuple(builder, lbzz__wno.yield_type, values)
        result.yield_(value)
        qhgm__rlsg = cgutils.increment_index(builder, index)
        builder.store(qhgm__rlsg, oue__ewb.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    ibzg__obh = ir.Assign(rhs, lhs, expr.loc)
    iemkk__lkq = lhs
    smtoy__ccay = []
    xkdsv__rdqcv = []
    ldpa__bptq = typ.count
    for i in range(ldpa__bptq):
        mqlo__msnr = ir.Var(iemkk__lkq.scope, mk_unique_var('{}_size{}'.
            format(iemkk__lkq.name, i)), iemkk__lkq.loc)
        trx__goejh = ir.Expr.static_getitem(lhs, i, None, iemkk__lkq.loc)
        self.calltypes[trx__goejh] = None
        smtoy__ccay.append(ir.Assign(trx__goejh, mqlo__msnr, iemkk__lkq.loc))
        self._define(equiv_set, mqlo__msnr, types.intp, trx__goejh)
        xkdsv__rdqcv.append(mqlo__msnr)
    vgin__cvqpt = tuple(xkdsv__rdqcv)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        vgin__cvqpt, pre=[ibzg__obh] + smtoy__ccay)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
