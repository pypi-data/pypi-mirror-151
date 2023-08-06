"""
Helper functions for transformations.
"""
import itertools
import math
import operator
import types as pytypes
from collections import namedtuple
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, types
from numba.core.ir_utils import GuardException, build_definitions, compile_to_numba_ir, compute_cfg_from_blocks, find_callname, find_const, get_definition, guard, is_setitem, mk_unique_var, replace_arg_nodes, require
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import fold_arguments
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoConstUpdatedError, BodoError, can_literalize_type, get_literal_value, get_overload_const_bool, get_overload_const_list, is_literal_type, is_overload_constant_bool
from bodo.utils.utils import is_array_typ, is_assign, is_call, is_expr
ReplaceFunc = namedtuple('ReplaceFunc', ['func', 'arg_types', 'args',
    'glbls', 'inline_bodo_calls', 'run_full_pipeline', 'pre_nodes'])
bodo_types_with_params = {'ArrayItemArrayType', 'CSRMatrixType',
    'CategoricalArrayType', 'CategoricalIndexType', 'DataFrameType',
    'DatetimeIndexType', 'Decimal128Type', 'DecimalArrayType',
    'IntegerArrayType', 'IntervalArrayType', 'IntervalIndexType', 'List',
    'MapArrayType', 'NumericIndexType', 'PDCategoricalDtype',
    'PeriodIndexType', 'RangeIndexType', 'SeriesType', 'StringIndexType',
    'BinaryIndexType', 'StructArrayType', 'TimedeltaIndexType',
    'TupleArrayType'}
container_update_method_names = ('clear', 'pop', 'popitem', 'update', 'add',
    'difference_update', 'discard', 'intersection_update', 'remove',
    'symmetric_difference_update', 'append', 'extend', 'insert', 'reverse',
    'sort')
no_side_effect_call_tuples = {(int,), (list,), (set,), (dict,), (min,), (
    max,), (abs,), (len,), (bool,), (str,), ('ceil', math), ('init_series',
    'pd_series_ext', 'hiframes', bodo), ('get_series_data', 'pd_series_ext',
    'hiframes', bodo), ('get_series_index', 'pd_series_ext', 'hiframes',
    bodo), ('get_series_name', 'pd_series_ext', 'hiframes', bodo), (
    'get_index_data', 'pd_index_ext', 'hiframes', bodo), ('get_index_name',
    'pd_index_ext', 'hiframes', bodo), ('init_binary_str_index',
    'pd_index_ext', 'hiframes', bodo), ('init_numeric_index',
    'pd_index_ext', 'hiframes', bodo), ('init_categorical_index',
    'pd_index_ext', 'hiframes', bodo), ('_dti_val_finalize', 'pd_index_ext',
    'hiframes', bodo), ('init_datetime_index', 'pd_index_ext', 'hiframes',
    bodo), ('init_timedelta_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_range_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_heter_index', 'pd_index_ext', 'hiframes', bodo), (
    'get_int_arr_data', 'int_arr_ext', 'libs', bodo), ('get_int_arr_bitmap',
    'int_arr_ext', 'libs', bodo), ('init_integer_array', 'int_arr_ext',
    'libs', bodo), ('alloc_int_array', 'int_arr_ext', 'libs', bodo), (
    'inplace_eq', 'str_arr_ext', 'libs', bodo), ('get_bool_arr_data',
    'bool_arr_ext', 'libs', bodo), ('get_bool_arr_bitmap', 'bool_arr_ext',
    'libs', bodo), ('init_bool_array', 'bool_arr_ext', 'libs', bodo), (
    'alloc_bool_array', 'bool_arr_ext', 'libs', bodo), (
    'datetime_date_arr_to_dt64_arr', 'pd_timestamp_ext', 'hiframes', bodo),
    (bodo.libs.bool_arr_ext.compute_or_body,), (bodo.libs.bool_arr_ext.
    compute_and_body,), ('alloc_datetime_date_array', 'datetime_date_ext',
    'hiframes', bodo), ('alloc_datetime_timedelta_array',
    'datetime_timedelta_ext', 'hiframes', bodo), ('cat_replace',
    'pd_categorical_ext', 'hiframes', bodo), ('init_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('alloc_categorical_array',
    'pd_categorical_ext', 'hiframes', bodo), ('get_categorical_arr_codes',
    'pd_categorical_ext', 'hiframes', bodo), ('_sum_handle_nan',
    'series_kernels', 'hiframes', bodo), ('_box_cat_val', 'series_kernels',
    'hiframes', bodo), ('_mean_handle_nan', 'series_kernels', 'hiframes',
    bodo), ('_var_handle_mincount', 'series_kernels', 'hiframes', bodo), (
    '_compute_var_nan_count_ddof', 'series_kernels', 'hiframes', bodo), (
    '_sem_handle_nan', 'series_kernels', 'hiframes', bodo), ('dist_return',
    'distributed_api', 'libs', bodo), ('rep_return', 'distributed_api',
    'libs', bodo), ('init_dataframe', 'pd_dataframe_ext', 'hiframes', bodo),
    ('get_dataframe_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_table', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_column_names', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_table_data', 'table', 'hiframes', bodo), ('get_dataframe_index',
    'pd_dataframe_ext', 'hiframes', bodo), ('init_rolling',
    'pd_rolling_ext', 'hiframes', bodo), ('init_groupby', 'pd_groupby_ext',
    'hiframes', bodo), ('calc_nitems', 'array_kernels', 'libs', bodo), (
    'concat', 'array_kernels', 'libs', bodo), ('unique', 'array_kernels',
    'libs', bodo), ('nunique', 'array_kernels', 'libs', bodo), ('quantile',
    'array_kernels', 'libs', bodo), ('explode', 'array_kernels', 'libs',
    bodo), ('explode_no_index', 'array_kernels', 'libs', bodo), (
    'get_arr_lens', 'array_kernels', 'libs', bodo), (
    'str_arr_from_sequence', 'str_arr_ext', 'libs', bodo), (
    'get_str_arr_str_length', 'str_arr_ext', 'libs', bodo), (
    'parse_datetime_str', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_dt64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'dt64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'timedelta64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_timedelta64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'npy_datetimestruct_to_datetime', 'pd_timestamp_ext', 'hiframes', bodo),
    ('isna', 'array_kernels', 'libs', bodo), ('copy',), (
    'from_iterable_impl', 'typing', 'utils', bodo), ('chain', itertools), (
    'groupby',), ('rolling',), (pd.CategoricalDtype,), (bodo.hiframes.
    pd_categorical_ext.get_code_for_value,), ('asarray', np), ('int32', np),
    ('int64', np), ('float64', np), ('float32', np), ('bool_', np), ('full',
    np), ('round', np), ('isnan', np), ('isnat', np), ('arange', np), (
    'internal_prange', 'parfor', numba), ('internal_prange', 'parfor',
    'parfors', numba), ('empty_inferred', 'ndarray', 'unsafe', numba), (
    '_slice_span', 'unicode', numba), ('_normalize_slice', 'unicode', numba
    ), ('init_session_builder', 'pyspark_ext', 'libs', bodo), (
    'init_session', 'pyspark_ext', 'libs', bodo), ('init_spark_df',
    'pyspark_ext', 'libs', bodo), ('h5size', 'h5_api', 'io', bodo), (
    'pre_alloc_struct_array', 'struct_arr_ext', 'libs', bodo), (bodo.libs.
    struct_arr_ext.pre_alloc_struct_array,), ('pre_alloc_tuple_array',
    'tuple_arr_ext', 'libs', bodo), (bodo.libs.tuple_arr_ext.
    pre_alloc_tuple_array,), ('pre_alloc_array_item_array',
    'array_item_arr_ext', 'libs', bodo), (bodo.libs.array_item_arr_ext.
    pre_alloc_array_item_array,), ('dist_reduce', 'distributed_api', 'libs',
    bodo), (bodo.libs.distributed_api.dist_reduce,), (
    'pre_alloc_string_array', 'str_arr_ext', 'libs', bodo), (bodo.libs.
    str_arr_ext.pre_alloc_string_array,), ('pre_alloc_binary_array',
    'binary_arr_ext', 'libs', bodo), (bodo.libs.binary_arr_ext.
    pre_alloc_binary_array,), ('pre_alloc_map_array', 'map_arr_ext', 'libs',
    bodo), (bodo.libs.map_arr_ext.pre_alloc_map_array,), (
    'convert_dict_arr_to_int', 'dict_arr_ext', 'libs', bodo), (
    'cat_dict_str', 'dict_arr_ext', 'libs', bodo), ('str_replace',
    'dict_arr_ext', 'libs', bodo), ('dict_arr_eq', 'dict_arr_ext', 'libs',
    bodo), ('dict_arr_ne', 'dict_arr_ext', 'libs', bodo), ('str_startswith',
    'dict_arr_ext', 'libs', bodo), ('str_endswith', 'dict_arr_ext', 'libs',
    bodo), ('str_contains_non_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_series_contains_regex', 'dict_arr_ext', 'libs', bodo), ('prange',
    bodo), (bodo.prange,), ('objmode', bodo), (bodo.objmode,), (
    'get_label_dict_from_categories', 'pd_categorial_ext', 'hiframes', bodo
    ), ('get_label_dict_from_categories_no_duplicates', 'pd_categorial_ext',
    'hiframes', bodo), ('build_nullable_tuple', 'nullable_tuple_ext',
    'libs', bodo), ('generate_mappable_table_func', 'table_utils', 'utils',
    bodo)}


def remove_hiframes(rhs, lives, call_list):
    yik__crmt = tuple(call_list)
    if yik__crmt in no_side_effect_call_tuples:
        return True
    if len(call_list) == 4 and call_list[1:] == ['conversion', 'utils', bodo]:
        return True
    if isinstance(call_list[-1], pytypes.ModuleType) and call_list[-1
        ].__name__ == 'bodosql':
        return True
    if len(call_list) == 2 and call_list[0] == 'copy':
        return True
    if call_list == ['h5read', 'h5_api', 'io', bodo] and rhs.args[5
        ].name not in lives:
        return True
    if call_list == ['move_str_binary_arr_payload', 'str_arr_ext', 'libs', bodo
        ] and rhs.args[0].name not in lives:
        return True
    if call_list == ['setna', 'array_kernels', 'libs', bodo] and rhs.args[0
        ].name not in lives:
        return True
    if call_list == ['set_table_data', 'table', 'hiframes', bodo] and rhs.args[
        0].name not in lives:
        return True
    if call_list == ['ensure_column_unboxed', 'table', 'hiframes', bodo
        ] and rhs.args[0].name not in lives and rhs.args[1].name not in lives:
        return True
    if call_list == ['generate_table_nbytes', 'table_utils', 'utils', bodo
        ] and rhs.args[1].name not in lives:
        return True
    if len(yik__crmt) == 1 and tuple in getattr(yik__crmt[0], '__mro__', ()):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    jyyqb__ydr = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math':
        math}
    if extra_globals is not None:
        jyyqb__ydr.update(extra_globals)
    if not replace_globals:
        jyyqb__ydr = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, jyyqb__ydr, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[qvi__zntw.name] for qvi__zntw in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, jyyqb__ydr)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        kuac__lqms = tuple(typing_info.typemap[qvi__zntw.name] for
            qvi__zntw in args)
        vrscx__ctwzg = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, kuac__lqms, {}, {}, flags)
        vrscx__ctwzg.run()
    szgc__wzzx = f_ir.blocks.popitem()[1]
    replace_arg_nodes(szgc__wzzx, args)
    motp__usuig = szgc__wzzx.body[:-2]
    update_locs(motp__usuig[len(args):], loc)
    for stmt in motp__usuig[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        azv__nek = szgc__wzzx.body[-2]
        assert is_assign(azv__nek) and is_expr(azv__nek.value, 'cast')
        cyxu__uaolm = azv__nek.value.value
        motp__usuig.append(ir.Assign(cyxu__uaolm, ret_var, loc))
    return motp__usuig


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for uay__dhd in stmt.list_vars():
            uay__dhd.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        zkvt__pah = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        hcppw__aiuid, msghg__zav = zkvt__pah(stmt)
        return msghg__zav
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        pvg__ognu = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(pvg__ognu, ir.UndefinedType):
            iojm__aytvz = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{iojm__aytvz}' is not defined", loc=loc)
    except GuardException as xgp__tawm:
        raise BodoError(err_msg, loc=loc)
    return pvg__ognu


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    zrwrj__bjw = get_definition(func_ir, var)
    fxrp__lrtax = None
    if typemap is not None:
        fxrp__lrtax = typemap.get(var.name, None)
    if isinstance(zrwrj__bjw, ir.Arg) and arg_types is not None:
        fxrp__lrtax = arg_types[zrwrj__bjw.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(fxrp__lrtax):
        return get_literal_value(fxrp__lrtax)
    if isinstance(zrwrj__bjw, (ir.Const, ir.Global, ir.FreeVar)):
        pvg__ognu = zrwrj__bjw.value
        return pvg__ognu
    if literalize_args and isinstance(zrwrj__bjw, ir.Arg
        ) and can_literalize_type(fxrp__lrtax, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({zrwrj__bjw.index}, loc=var
            .loc, file_infos={zrwrj__bjw.index: file_info} if file_info is not
            None else None)
    if is_expr(zrwrj__bjw, 'binop'):
        if file_info and zrwrj__bjw.fn == operator.add:
            try:
                izy__haq = get_const_value_inner(func_ir, zrwrj__bjw.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(izy__haq, True)
                ddsrq__fphk = get_const_value_inner(func_ir, zrwrj__bjw.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return zrwrj__bjw.fn(izy__haq, ddsrq__fphk)
            except (GuardException, BodoConstUpdatedError) as xgp__tawm:
                pass
            try:
                ddsrq__fphk = get_const_value_inner(func_ir, zrwrj__bjw.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(ddsrq__fphk, False)
                izy__haq = get_const_value_inner(func_ir, zrwrj__bjw.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return zrwrj__bjw.fn(izy__haq, ddsrq__fphk)
            except (GuardException, BodoConstUpdatedError) as xgp__tawm:
                pass
        izy__haq = get_const_value_inner(func_ir, zrwrj__bjw.lhs, arg_types,
            typemap, updated_containers)
        ddsrq__fphk = get_const_value_inner(func_ir, zrwrj__bjw.rhs,
            arg_types, typemap, updated_containers)
        return zrwrj__bjw.fn(izy__haq, ddsrq__fphk)
    if is_expr(zrwrj__bjw, 'unary'):
        pvg__ognu = get_const_value_inner(func_ir, zrwrj__bjw.value,
            arg_types, typemap, updated_containers)
        return zrwrj__bjw.fn(pvg__ognu)
    if is_expr(zrwrj__bjw, 'getattr') and typemap:
        cyngn__gnnr = typemap.get(zrwrj__bjw.value.name, None)
        if isinstance(cyngn__gnnr, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and zrwrj__bjw.attr == 'columns':
            return pd.Index(cyngn__gnnr.columns)
        if isinstance(cyngn__gnnr, types.SliceType):
            gzvzl__abtd = get_definition(func_ir, zrwrj__bjw.value)
            require(is_call(gzvzl__abtd))
            fynr__okxh = find_callname(func_ir, gzvzl__abtd)
            kdbp__sudfu = False
            if fynr__okxh == ('_normalize_slice', 'numba.cpython.unicode'):
                require(zrwrj__bjw.attr in ('start', 'step'))
                gzvzl__abtd = get_definition(func_ir, gzvzl__abtd.args[0])
                kdbp__sudfu = True
            require(find_callname(func_ir, gzvzl__abtd) == ('slice',
                'builtins'))
            if len(gzvzl__abtd.args) == 1:
                if zrwrj__bjw.attr == 'start':
                    return 0
                if zrwrj__bjw.attr == 'step':
                    return 1
                require(zrwrj__bjw.attr == 'stop')
                return get_const_value_inner(func_ir, gzvzl__abtd.args[0],
                    arg_types, typemap, updated_containers)
            if zrwrj__bjw.attr == 'start':
                pvg__ognu = get_const_value_inner(func_ir, gzvzl__abtd.args
                    [0], arg_types, typemap, updated_containers)
                if pvg__ognu is None:
                    pvg__ognu = 0
                if kdbp__sudfu:
                    require(pvg__ognu == 0)
                return pvg__ognu
            if zrwrj__bjw.attr == 'stop':
                assert not kdbp__sudfu
                return get_const_value_inner(func_ir, gzvzl__abtd.args[1],
                    arg_types, typemap, updated_containers)
            require(zrwrj__bjw.attr == 'step')
            if len(gzvzl__abtd.args) == 2:
                return 1
            else:
                pvg__ognu = get_const_value_inner(func_ir, gzvzl__abtd.args
                    [2], arg_types, typemap, updated_containers)
                if pvg__ognu is None:
                    pvg__ognu = 1
                if kdbp__sudfu:
                    require(pvg__ognu == 1)
                return pvg__ognu
    if is_expr(zrwrj__bjw, 'getattr'):
        return getattr(get_const_value_inner(func_ir, zrwrj__bjw.value,
            arg_types, typemap, updated_containers), zrwrj__bjw.attr)
    if is_expr(zrwrj__bjw, 'getitem'):
        value = get_const_value_inner(func_ir, zrwrj__bjw.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, zrwrj__bjw.index, arg_types,
            typemap, updated_containers)
        return value[index]
    bks__lsar = guard(find_callname, func_ir, zrwrj__bjw, typemap)
    if bks__lsar is not None and len(bks__lsar) == 2 and bks__lsar[0
        ] == 'keys' and isinstance(bks__lsar[1], ir.Var):
        hgvb__gvv = zrwrj__bjw.func
        zrwrj__bjw = get_definition(func_ir, bks__lsar[1])
        dgga__zdgu = bks__lsar[1].name
        if updated_containers and dgga__zdgu in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                dgga__zdgu, updated_containers[dgga__zdgu]))
        require(is_expr(zrwrj__bjw, 'build_map'))
        vals = [uay__dhd[0] for uay__dhd in zrwrj__bjw.items]
        kml__hlnr = guard(get_definition, func_ir, hgvb__gvv)
        assert isinstance(kml__hlnr, ir.Expr) and kml__hlnr.attr == 'keys'
        kml__hlnr.attr = 'copy'
        return [get_const_value_inner(func_ir, uay__dhd, arg_types, typemap,
            updated_containers) for uay__dhd in vals]
    if is_expr(zrwrj__bjw, 'build_map'):
        return {get_const_value_inner(func_ir, uay__dhd[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            uay__dhd[1], arg_types, typemap, updated_containers) for
            uay__dhd in zrwrj__bjw.items}
    if is_expr(zrwrj__bjw, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, uay__dhd, arg_types,
            typemap, updated_containers) for uay__dhd in zrwrj__bjw.items)
    if is_expr(zrwrj__bjw, 'build_list'):
        return [get_const_value_inner(func_ir, uay__dhd, arg_types, typemap,
            updated_containers) for uay__dhd in zrwrj__bjw.items]
    if is_expr(zrwrj__bjw, 'build_set'):
        return {get_const_value_inner(func_ir, uay__dhd, arg_types, typemap,
            updated_containers) for uay__dhd in zrwrj__bjw.items}
    if bks__lsar == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, zrwrj__bjw.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if bks__lsar == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, zrwrj__bjw.args[0],
            arg_types, typemap, updated_containers))
    if bks__lsar == ('range', 'builtins') and len(zrwrj__bjw.args) == 1:
        return range(get_const_value_inner(func_ir, zrwrj__bjw.args[0],
            arg_types, typemap, updated_containers))
    if bks__lsar == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, uay__dhd,
            arg_types, typemap, updated_containers) for uay__dhd in
            zrwrj__bjw.args))
    if bks__lsar == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, zrwrj__bjw.args[0],
            arg_types, typemap, updated_containers))
    if bks__lsar == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, zrwrj__bjw.args[0],
            arg_types, typemap, updated_containers))
    if bks__lsar == ('format', 'builtins'):
        qvi__zntw = get_const_value_inner(func_ir, zrwrj__bjw.args[0],
            arg_types, typemap, updated_containers)
        bfmw__kdiz = get_const_value_inner(func_ir, zrwrj__bjw.args[1],
            arg_types, typemap, updated_containers) if len(zrwrj__bjw.args
            ) > 1 else ''
        return format(qvi__zntw, bfmw__kdiz)
    if bks__lsar in (('init_binary_str_index', 'bodo.hiframes.pd_index_ext'
        ), ('init_numeric_index', 'bodo.hiframes.pd_index_ext'), (
        'init_categorical_index', 'bodo.hiframes.pd_index_ext'), (
        'init_datetime_index', 'bodo.hiframes.pd_index_ext'), (
        'init_timedelta_index', 'bodo.hiframes.pd_index_ext'), (
        'init_heter_index', 'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, zrwrj__bjw.args[0],
            arg_types, typemap, updated_containers))
    if bks__lsar == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, zrwrj__bjw.args[0],
            arg_types, typemap, updated_containers))
    if bks__lsar == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, zrwrj__bjw.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, zrwrj__bjw.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            zrwrj__bjw.args[2], arg_types, typemap, updated_containers))
    if bks__lsar == ('len', 'builtins') and typemap and isinstance(typemap.
        get(zrwrj__bjw.args[0].name, None), types.BaseTuple):
        return len(typemap[zrwrj__bjw.args[0].name])
    if bks__lsar == ('len', 'builtins'):
        rnpdf__xkk = guard(get_definition, func_ir, zrwrj__bjw.args[0])
        if isinstance(rnpdf__xkk, ir.Expr) and rnpdf__xkk.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(rnpdf__xkk.items)
        return len(get_const_value_inner(func_ir, zrwrj__bjw.args[0],
            arg_types, typemap, updated_containers))
    if bks__lsar == ('CategoricalDtype', 'pandas'):
        kws = dict(zrwrj__bjw.kws)
        hii__embhx = get_call_expr_arg('CategoricalDtype', zrwrj__bjw.args,
            kws, 0, 'categories', '')
        rpt__yups = get_call_expr_arg('CategoricalDtype', zrwrj__bjw.args,
            kws, 1, 'ordered', False)
        if rpt__yups is not False:
            rpt__yups = get_const_value_inner(func_ir, rpt__yups, arg_types,
                typemap, updated_containers)
        if hii__embhx == '':
            hii__embhx = None
        else:
            hii__embhx = get_const_value_inner(func_ir, hii__embhx,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(hii__embhx, rpt__yups)
    if bks__lsar == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, zrwrj__bjw.args[0],
            arg_types, typemap, updated_containers))
    if bks__lsar is not None and len(bks__lsar) == 2 and bks__lsar[1
        ] == 'pandas' and bks__lsar[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, bks__lsar[0])()
    if bks__lsar is not None and len(bks__lsar) == 2 and isinstance(bks__lsar
        [1], ir.Var):
        pvg__ognu = get_const_value_inner(func_ir, bks__lsar[1], arg_types,
            typemap, updated_containers)
        args = [get_const_value_inner(func_ir, uay__dhd, arg_types, typemap,
            updated_containers) for uay__dhd in zrwrj__bjw.args]
        kws = {nsxq__ngytz[0]: get_const_value_inner(func_ir, nsxq__ngytz[1
            ], arg_types, typemap, updated_containers) for nsxq__ngytz in
            zrwrj__bjw.kws}
        return getattr(pvg__ognu, bks__lsar[0])(*args, **kws)
    if bks__lsar is not None and len(bks__lsar) == 2 and bks__lsar[1
        ] == 'bodo' and bks__lsar[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, uay__dhd, arg_types,
            typemap, updated_containers) for uay__dhd in zrwrj__bjw.args)
        kwargs = {iojm__aytvz: get_const_value_inner(func_ir, uay__dhd,
            arg_types, typemap, updated_containers) for iojm__aytvz,
            uay__dhd in dict(zrwrj__bjw.kws).items()}
        return getattr(bodo, bks__lsar[0])(*args, **kwargs)
    if is_call(zrwrj__bjw) and typemap and isinstance(typemap.get(
        zrwrj__bjw.func.name, None), types.Dispatcher):
        py_func = typemap[zrwrj__bjw.func.name].dispatcher.py_func
        require(zrwrj__bjw.vararg is None)
        args = tuple(get_const_value_inner(func_ir, uay__dhd, arg_types,
            typemap, updated_containers) for uay__dhd in zrwrj__bjw.args)
        kwargs = {iojm__aytvz: get_const_value_inner(func_ir, uay__dhd,
            arg_types, typemap, updated_containers) for iojm__aytvz,
            uay__dhd in dict(zrwrj__bjw.kws).items()}
        arg_types = tuple(bodo.typeof(uay__dhd) for uay__dhd in args)
        kw_types = {hmaj__bxsm: bodo.typeof(uay__dhd) for hmaj__bxsm,
            uay__dhd in kwargs.items()}
        require(_func_is_pure(py_func, arg_types, kw_types))
        return py_func(*args, **kwargs)
    raise GuardException('Constant value not found')


def _func_is_pure(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.ir.csv_ext import CsvReader
    from bodo.ir.json_ext import JsonReader
    from bodo.ir.parquet_ext import ParquetReader
    from bodo.ir.sql_ext import SqlReader
    f_ir, typemap, pxl__exe, pxl__exe = bodo.compiler.get_func_type_info(
        py_func, arg_types, kw_types)
    for block in f_ir.blocks.values():
        for stmt in block.body:
            if isinstance(stmt, ir.Print):
                return False
            if isinstance(stmt, (CsvReader, JsonReader, ParquetReader,
                SqlReader)):
                return False
            if is_setitem(stmt) and isinstance(guard(get_definition, f_ir,
                stmt.target), ir.Arg):
                return False
            if is_assign(stmt):
                rhs = stmt.value
                if isinstance(rhs, ir.Yield):
                    return False
                if is_call(rhs):
                    iwwl__ckrtb = guard(get_definition, f_ir, rhs.func)
                    if isinstance(iwwl__ckrtb, ir.Const) and isinstance(
                        iwwl__ckrtb.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    kut__iyn = guard(find_callname, f_ir, rhs)
                    if kut__iyn is None:
                        return False
                    func_name, agj__hzu = kut__iyn
                    if agj__hzu == 'pandas' and func_name.startswith('read_'):
                        return False
                    if kut__iyn in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if kut__iyn == ('File', 'h5py'):
                        return False
                    if isinstance(agj__hzu, ir.Var):
                        fxrp__lrtax = typemap[agj__hzu.name]
                        if isinstance(fxrp__lrtax, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(fxrp__lrtax, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(fxrp__lrtax, bodo.LoggingLoggerType):
                            return False
                        if str(fxrp__lrtax).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir, agj__hzu
                            ), ir.Arg)):
                            return False
                    if agj__hzu in ('numpy.random', 'time', 'logging',
                        'matplotlib.pyplot'):
                        return False
    return True


def fold_argument_types(pysig, args, kws):

    def normal_handler(index, param, value):
        return value

    def default_handler(index, param, default):
        return types.Omitted(default)

    def stararg_handler(index, param, values):
        return types.StarArgTuple(values)
    args = fold_arguments(pysig, args, kws, normal_handler, default_handler,
        stararg_handler)
    return args


def get_const_func_output_type(func, arg_types, kw_types, typing_context,
    target_context, is_udf=True):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
    py_func = None
    if isinstance(func, types.MakeFunctionLiteral):
        fnut__yuu = func.literal_value.code
        lztdy__iodtn = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            lztdy__iodtn = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(lztdy__iodtn, fnut__yuu)
        fix_struct_return(f_ir)
        typemap, rhz__hbpfq, qda__lzlsj, pxl__exe = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, qda__lzlsj, rhz__hbpfq = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, qda__lzlsj, rhz__hbpfq = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, qda__lzlsj, rhz__hbpfq = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(rhz__hbpfq, types.DictType):
        ukdkz__tdso = guard(get_struct_keynames, f_ir, typemap)
        if ukdkz__tdso is not None:
            rhz__hbpfq = StructType((rhz__hbpfq.value_type,) * len(
                ukdkz__tdso), ukdkz__tdso)
    if is_udf and isinstance(rhz__hbpfq, (SeriesType, HeterogeneousSeriesType)
        ):
        lhjf__qzg = numba.core.registry.cpu_target.typing_context
        wehx__kpv = numba.core.registry.cpu_target.target_context
        wmean__fbbr = bodo.transforms.series_pass.SeriesPass(f_ir,
            lhjf__qzg, wehx__kpv, typemap, qda__lzlsj, {})
        wmean__fbbr.run()
        wmean__fbbr.run()
        wmean__fbbr.run()
        gqw__ajld = compute_cfg_from_blocks(f_ir.blocks)
        axqv__ssy = [guard(_get_const_series_info, f_ir.blocks[ari__kzaft],
            f_ir, typemap) for ari__kzaft in gqw__ajld.exit_points() if
            isinstance(f_ir.blocks[ari__kzaft].body[-1], ir.Return)]
        if None in axqv__ssy or len(pd.Series(axqv__ssy).unique()) != 1:
            rhz__hbpfq.const_info = None
        else:
            rhz__hbpfq.const_info = axqv__ssy[0]
    return rhz__hbpfq


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    jocr__mnvir = block.body[-1].value
    jchm__vdoab = get_definition(f_ir, jocr__mnvir)
    require(is_expr(jchm__vdoab, 'cast'))
    jchm__vdoab = get_definition(f_ir, jchm__vdoab.value)
    require(is_call(jchm__vdoab) and find_callname(f_ir, jchm__vdoab) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    xlq__ayv = jchm__vdoab.args[1]
    wyphf__ouohl = tuple(get_const_value_inner(f_ir, xlq__ayv, typemap=typemap)
        )
    if isinstance(typemap[jocr__mnvir.name], HeterogeneousSeriesType):
        return len(typemap[jocr__mnvir.name].data), wyphf__ouohl
    zdj__pwqe = jchm__vdoab.args[0]
    koxq__pmgrs = get_definition(f_ir, zdj__pwqe)
    func_name, njpf__jud = find_callname(f_ir, koxq__pmgrs)
    if is_call(koxq__pmgrs) and bodo.utils.utils.is_alloc_callname(func_name,
        njpf__jud):
        uho__bfhrd = koxq__pmgrs.args[0]
        lmuu__fgy = get_const_value_inner(f_ir, uho__bfhrd, typemap=typemap)
        return lmuu__fgy, wyphf__ouohl
    if is_call(koxq__pmgrs) and find_callname(f_ir, koxq__pmgrs) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence',
        'bodo.libs.str_arr_ext'), ('build_nullable_tuple',
        'bodo.libs.nullable_tuple_ext')]:
        zdj__pwqe = koxq__pmgrs.args[0]
        koxq__pmgrs = get_definition(f_ir, zdj__pwqe)
    require(is_expr(koxq__pmgrs, 'build_tuple') or is_expr(koxq__pmgrs,
        'build_list'))
    return len(koxq__pmgrs.items), wyphf__ouohl


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    ryqfp__gzaj = []
    cgeg__jxgs = []
    values = []
    for hmaj__bxsm, uay__dhd in build_map.items:
        tev__fbnfc = find_const(f_ir, hmaj__bxsm)
        require(isinstance(tev__fbnfc, str))
        cgeg__jxgs.append(tev__fbnfc)
        ryqfp__gzaj.append(hmaj__bxsm)
        values.append(uay__dhd)
    yljb__mwvkr = ir.Var(scope, mk_unique_var('val_tup'), loc)
    ujzra__rrrb = ir.Assign(ir.Expr.build_tuple(values, loc), yljb__mwvkr, loc)
    f_ir._definitions[yljb__mwvkr.name] = [ujzra__rrrb.value]
    yxj__lfoo = ir.Var(scope, mk_unique_var('key_tup'), loc)
    nvz__ypzpx = ir.Assign(ir.Expr.build_tuple(ryqfp__gzaj, loc), yxj__lfoo,
        loc)
    f_ir._definitions[yxj__lfoo.name] = [nvz__ypzpx.value]
    if typemap is not None:
        typemap[yljb__mwvkr.name] = types.Tuple([typemap[uay__dhd.name] for
            uay__dhd in values])
        typemap[yxj__lfoo.name] = types.Tuple([typemap[uay__dhd.name] for
            uay__dhd in ryqfp__gzaj])
    return cgeg__jxgs, yljb__mwvkr, ujzra__rrrb, yxj__lfoo, nvz__ypzpx


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    kaxjh__seba = block.body[-1].value
    rqk__cvmw = guard(get_definition, f_ir, kaxjh__seba)
    require(is_expr(rqk__cvmw, 'cast'))
    jchm__vdoab = guard(get_definition, f_ir, rqk__cvmw.value)
    require(is_expr(jchm__vdoab, 'build_map'))
    require(len(jchm__vdoab.items) > 0)
    loc = block.loc
    scope = block.scope
    cgeg__jxgs, yljb__mwvkr, ujzra__rrrb, yxj__lfoo, nvz__ypzpx = (
        extract_keyvals_from_struct_map(f_ir, jchm__vdoab, loc, scope))
    thtqa__xacof = ir.Var(scope, mk_unique_var('conv_call'), loc)
    uww__aufb = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), thtqa__xacof, loc)
    f_ir._definitions[thtqa__xacof.name] = [uww__aufb.value]
    hnr__ayb = ir.Var(scope, mk_unique_var('struct_val'), loc)
    hez__ytztl = ir.Assign(ir.Expr.call(thtqa__xacof, [yljb__mwvkr,
        yxj__lfoo], {}, loc), hnr__ayb, loc)
    f_ir._definitions[hnr__ayb.name] = [hez__ytztl.value]
    rqk__cvmw.value = hnr__ayb
    jchm__vdoab.items = [(hmaj__bxsm, hmaj__bxsm) for hmaj__bxsm, pxl__exe in
        jchm__vdoab.items]
    block.body = block.body[:-2] + [ujzra__rrrb, nvz__ypzpx, uww__aufb,
        hez__ytztl] + block.body[-2:]
    return tuple(cgeg__jxgs)


def get_struct_keynames(f_ir, typemap):
    gqw__ajld = compute_cfg_from_blocks(f_ir.blocks)
    vhg__tkbzz = list(gqw__ajld.exit_points())[0]
    block = f_ir.blocks[vhg__tkbzz]
    require(isinstance(block.body[-1], ir.Return))
    kaxjh__seba = block.body[-1].value
    rqk__cvmw = guard(get_definition, f_ir, kaxjh__seba)
    require(is_expr(rqk__cvmw, 'cast'))
    jchm__vdoab = guard(get_definition, f_ir, rqk__cvmw.value)
    require(is_call(jchm__vdoab) and find_callname(f_ir, jchm__vdoab) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[jchm__vdoab.args[1].name])


def fix_struct_return(f_ir):
    cix__kjyb = None
    gqw__ajld = compute_cfg_from_blocks(f_ir.blocks)
    for vhg__tkbzz in gqw__ajld.exit_points():
        cix__kjyb = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            vhg__tkbzz], vhg__tkbzz)
    return cix__kjyb


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    csd__cahe = ir.Block(ir.Scope(None, loc), loc)
    csd__cahe.body = node_list
    build_definitions({(0): csd__cahe}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(uay__dhd) for uay__dhd in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    thdce__stgp = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(thdce__stgp, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for omzv__mhct in range(len(vals) - 1, -1, -1):
        uay__dhd = vals[omzv__mhct]
        if isinstance(uay__dhd, str) and uay__dhd.startswith(
            NESTED_TUP_SENTINEL):
            oljiy__rgf = int(uay__dhd[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:omzv__mhct]) + (
                tuple(vals[omzv__mhct + 1:omzv__mhct + oljiy__rgf + 1]),) +
                tuple(vals[omzv__mhct + oljiy__rgf + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    qvi__zntw = None
    if len(args) > arg_no and arg_no >= 0:
        qvi__zntw = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        qvi__zntw = kws[arg_name]
    if qvi__zntw is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return qvi__zntw


def set_call_expr_arg(var, args, kws, arg_no, arg_name, add_if_missing=False):
    if len(args) > arg_no:
        args[arg_no] = var
    elif add_if_missing or arg_name in kws:
        kws[arg_name] = var
    else:
        raise BodoError('cannot set call argument since does not exist')


def avoid_udf_inline(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    f_ir = numba.core.compiler.run_frontend(py_func, inline_closures=True)
    if '_bodo_inline' in kw_types and is_overload_constant_bool(kw_types[
        '_bodo_inline']):
        return not get_overload_const_bool(kw_types['_bodo_inline'])
    if any(isinstance(t, DataFrameType) for t in arg_types + tuple(kw_types
        .values())):
        return True
    for block in f_ir.blocks.values():
        if isinstance(block.body[-1], (ir.Raise, ir.StaticRaise)):
            return True
        for stmt in block.body:
            if isinstance(stmt, ir.EnterWith):
                return True
    return False


def replace_func(pass_info, func, args, const=False, pre_nodes=None,
    extra_globals=None, pysig=None, kws=None, inline_bodo_calls=False,
    run_full_pipeline=False):
    jyyqb__ydr = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        jyyqb__ydr.update(extra_globals)
    func.__globals__.update(jyyqb__ydr)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            qiw__jghx = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[qiw__jghx.name] = types.literal(default)
            except:
                pass_info.typemap[qiw__jghx.name] = numba.typeof(default)
            bdk__rvvoy = ir.Assign(ir.Const(default, loc), qiw__jghx, loc)
            pre_nodes.append(bdk__rvvoy)
            return qiw__jghx
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    kuac__lqms = tuple(pass_info.typemap[uay__dhd.name] for uay__dhd in args)
    if const:
        zykoq__wmt = []
        for omzv__mhct, qvi__zntw in enumerate(args):
            pvg__ognu = guard(find_const, pass_info.func_ir, qvi__zntw)
            if pvg__ognu:
                zykoq__wmt.append(types.literal(pvg__ognu))
            else:
                zykoq__wmt.append(kuac__lqms[omzv__mhct])
        kuac__lqms = tuple(zykoq__wmt)
    return ReplaceFunc(func, kuac__lqms, args, jyyqb__ydr,
        inline_bodo_calls, run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(kmr__tolam) for kmr__tolam in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        oiuy__sje = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {oiuy__sje} = 0\n', (oiuy__sje,)
    if isinstance(t, ArrayItemArrayType):
        oaa__okppo, quenc__omdlc = gen_init_varsize_alloc_sizes(t.dtype)
        oiuy__sje = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {oiuy__sje} = 0\n' + oaa__okppo, (oiuy__sje,) + quenc__omdlc
    return '', ()


def gen_varsize_item_sizes(t, item, var_names):
    if t == string_array_type:
        return '    {} += bodo.libs.str_arr_ext.get_utf8_size({})\n'.format(
            var_names[0], item)
    if isinstance(t, ArrayItemArrayType):
        return '    {} += len({})\n'.format(var_names[0], item
            ) + gen_varsize_array_counts(t.dtype, item, var_names[1:])
    return ''


def gen_varsize_array_counts(t, item, var_names):
    if t == string_array_type:
        return ('    {} += bodo.libs.str_arr_ext.get_num_total_chars({})\n'
            .format(var_names[0], item))
    return ''


def get_type_alloc_counts(t):
    if isinstance(t, (StructArrayType, TupleArrayType)):
        return 1 + sum(get_type_alloc_counts(kmr__tolam.dtype) for
            kmr__tolam in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(kmr__tolam) for kmr__tolam in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(kmr__tolam) for kmr__tolam in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    yirm__kmyd = typing_context.resolve_getattr(obj_dtype, func_name)
    if yirm__kmyd is None:
        pbg__ung = types.misc.Module(np)
        try:
            yirm__kmyd = typing_context.resolve_getattr(pbg__ung, func_name)
        except AttributeError as xgp__tawm:
            yirm__kmyd = None
        if yirm__kmyd is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return yirm__kmyd


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    yirm__kmyd = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(yirm__kmyd, types.BoundFunction):
        if axis is not None:
            reeo__pgay = yirm__kmyd.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            reeo__pgay = yirm__kmyd.get_call_type(typing_context, (), {})
        return reeo__pgay.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(yirm__kmyd):
            reeo__pgay = yirm__kmyd.get_call_type(typing_context, (
                obj_dtype,), {})
            return reeo__pgay.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    yirm__kmyd = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(yirm__kmyd, types.BoundFunction):
        eccal__dnpu = yirm__kmyd.template
        if axis is not None:
            return eccal__dnpu._overload_func(obj_dtype, axis=axis)
        else:
            return eccal__dnpu._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    rsd__yxm = get_definition(func_ir, dict_var)
    require(isinstance(rsd__yxm, ir.Expr))
    require(rsd__yxm.op == 'build_map')
    hacd__vewp = rsd__yxm.items
    ryqfp__gzaj = []
    values = []
    tqdll__kjo = False
    for omzv__mhct in range(len(hacd__vewp)):
        ict__evy, value = hacd__vewp[omzv__mhct]
        try:
            qrj__invm = get_const_value_inner(func_ir, ict__evy, arg_types,
                typemap, updated_containers)
            ryqfp__gzaj.append(qrj__invm)
            values.append(value)
        except GuardException as xgp__tawm:
            require_const_map[ict__evy] = label
            tqdll__kjo = True
    if tqdll__kjo:
        raise GuardException
    return ryqfp__gzaj, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        ryqfp__gzaj = tuple(get_const_value_inner(func_ir, t[0], args) for
            t in build_map.items)
    except GuardException as xgp__tawm:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in ryqfp__gzaj):
        raise BodoError(err_msg, loc)
    return ryqfp__gzaj


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    ryqfp__gzaj = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    sjqq__qnqbj = []
    xxy__zce = [bodo.transforms.typing_pass._create_const_var(hmaj__bxsm,
        'dict_key', scope, loc, sjqq__qnqbj) for hmaj__bxsm in ryqfp__gzaj]
    jssta__mzwqv = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        hafh__otmyv = ir.Var(scope, mk_unique_var('sentinel'), loc)
        zje__tzlid = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        sjqq__qnqbj.append(ir.Assign(ir.Const('__bodo_tup', loc),
            hafh__otmyv, loc))
        tuvt__wzl = [hafh__otmyv] + xxy__zce + jssta__mzwqv
        sjqq__qnqbj.append(ir.Assign(ir.Expr.build_tuple(tuvt__wzl, loc),
            zje__tzlid, loc))
        return (zje__tzlid,), sjqq__qnqbj
    else:
        pjq__pph = ir.Var(scope, mk_unique_var('values_tup'), loc)
        bicd__pnrmb = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        sjqq__qnqbj.append(ir.Assign(ir.Expr.build_tuple(jssta__mzwqv, loc),
            pjq__pph, loc))
        sjqq__qnqbj.append(ir.Assign(ir.Expr.build_tuple(xxy__zce, loc),
            bicd__pnrmb, loc))
        return (pjq__pph, bicd__pnrmb), sjqq__qnqbj
