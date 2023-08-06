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
    itjm__yxoxl = tuple(call_list)
    if itjm__yxoxl in no_side_effect_call_tuples:
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
    if len(itjm__yxoxl) == 1 and tuple in getattr(itjm__yxoxl[0], '__mro__', ()
        ):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=True):
    hls__olqju = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd, 'math':
        math}
    if extra_globals is not None:
        hls__olqju.update(extra_globals)
    if not replace_globals:
        hls__olqju = func.__globals__
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, hls__olqju, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[hexs__kmh.name] for hexs__kmh in args),
            typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, hls__olqju)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        zkpx__vtk = tuple(typing_info.typemap[hexs__kmh.name] for hexs__kmh in
            args)
        fua__wrpb = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, zkpx__vtk, {}, {}, flags)
        fua__wrpb.run()
    xwkd__axy = f_ir.blocks.popitem()[1]
    replace_arg_nodes(xwkd__axy, args)
    zax__tfze = xwkd__axy.body[:-2]
    update_locs(zax__tfze[len(args):], loc)
    for stmt in zax__tfze[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        dgd__hhdhy = xwkd__axy.body[-2]
        assert is_assign(dgd__hhdhy) and is_expr(dgd__hhdhy.value, 'cast')
        ylfel__tfaid = dgd__hhdhy.value.value
        zax__tfze.append(ir.Assign(ylfel__tfaid, ret_var, loc))
    return zax__tfze


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for rtxn__rsj in stmt.list_vars():
            rtxn__rsj.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        vfz__xju = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        jdhyp__pxnb, wrb__eujd = vfz__xju(stmt)
        return wrb__eujd
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        miu__ycgr = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(miu__ycgr, ir.UndefinedType):
            uehth__jgrhd = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{uehth__jgrhd}' is not defined", loc=loc)
    except GuardException as gmdug__aju:
        raise BodoError(err_msg, loc=loc)
    return miu__ycgr


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    mxqs__zbvt = get_definition(func_ir, var)
    qofet__xtiv = None
    if typemap is not None:
        qofet__xtiv = typemap.get(var.name, None)
    if isinstance(mxqs__zbvt, ir.Arg) and arg_types is not None:
        qofet__xtiv = arg_types[mxqs__zbvt.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(qofet__xtiv):
        return get_literal_value(qofet__xtiv)
    if isinstance(mxqs__zbvt, (ir.Const, ir.Global, ir.FreeVar)):
        miu__ycgr = mxqs__zbvt.value
        return miu__ycgr
    if literalize_args and isinstance(mxqs__zbvt, ir.Arg
        ) and can_literalize_type(qofet__xtiv, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({mxqs__zbvt.index}, loc=var
            .loc, file_infos={mxqs__zbvt.index: file_info} if file_info is not
            None else None)
    if is_expr(mxqs__zbvt, 'binop'):
        if file_info and mxqs__zbvt.fn == operator.add:
            try:
                ldbsv__bbz = get_const_value_inner(func_ir, mxqs__zbvt.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(ldbsv__bbz, True)
                gxi__lawr = get_const_value_inner(func_ir, mxqs__zbvt.rhs,
                    arg_types, typemap, updated_containers, file_info)
                return mxqs__zbvt.fn(ldbsv__bbz, gxi__lawr)
            except (GuardException, BodoConstUpdatedError) as gmdug__aju:
                pass
            try:
                gxi__lawr = get_const_value_inner(func_ir, mxqs__zbvt.rhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(gxi__lawr, False)
                ldbsv__bbz = get_const_value_inner(func_ir, mxqs__zbvt.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return mxqs__zbvt.fn(ldbsv__bbz, gxi__lawr)
            except (GuardException, BodoConstUpdatedError) as gmdug__aju:
                pass
        ldbsv__bbz = get_const_value_inner(func_ir, mxqs__zbvt.lhs,
            arg_types, typemap, updated_containers)
        gxi__lawr = get_const_value_inner(func_ir, mxqs__zbvt.rhs,
            arg_types, typemap, updated_containers)
        return mxqs__zbvt.fn(ldbsv__bbz, gxi__lawr)
    if is_expr(mxqs__zbvt, 'unary'):
        miu__ycgr = get_const_value_inner(func_ir, mxqs__zbvt.value,
            arg_types, typemap, updated_containers)
        return mxqs__zbvt.fn(miu__ycgr)
    if is_expr(mxqs__zbvt, 'getattr') and typemap:
        hsas__zxvxd = typemap.get(mxqs__zbvt.value.name, None)
        if isinstance(hsas__zxvxd, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and mxqs__zbvt.attr == 'columns':
            return pd.Index(hsas__zxvxd.columns)
        if isinstance(hsas__zxvxd, types.SliceType):
            atx__jlbms = get_definition(func_ir, mxqs__zbvt.value)
            require(is_call(atx__jlbms))
            hkorg__jlg = find_callname(func_ir, atx__jlbms)
            ngt__sntg = False
            if hkorg__jlg == ('_normalize_slice', 'numba.cpython.unicode'):
                require(mxqs__zbvt.attr in ('start', 'step'))
                atx__jlbms = get_definition(func_ir, atx__jlbms.args[0])
                ngt__sntg = True
            require(find_callname(func_ir, atx__jlbms) == ('slice', 'builtins')
                )
            if len(atx__jlbms.args) == 1:
                if mxqs__zbvt.attr == 'start':
                    return 0
                if mxqs__zbvt.attr == 'step':
                    return 1
                require(mxqs__zbvt.attr == 'stop')
                return get_const_value_inner(func_ir, atx__jlbms.args[0],
                    arg_types, typemap, updated_containers)
            if mxqs__zbvt.attr == 'start':
                miu__ycgr = get_const_value_inner(func_ir, atx__jlbms.args[
                    0], arg_types, typemap, updated_containers)
                if miu__ycgr is None:
                    miu__ycgr = 0
                if ngt__sntg:
                    require(miu__ycgr == 0)
                return miu__ycgr
            if mxqs__zbvt.attr == 'stop':
                assert not ngt__sntg
                return get_const_value_inner(func_ir, atx__jlbms.args[1],
                    arg_types, typemap, updated_containers)
            require(mxqs__zbvt.attr == 'step')
            if len(atx__jlbms.args) == 2:
                return 1
            else:
                miu__ycgr = get_const_value_inner(func_ir, atx__jlbms.args[
                    2], arg_types, typemap, updated_containers)
                if miu__ycgr is None:
                    miu__ycgr = 1
                if ngt__sntg:
                    require(miu__ycgr == 1)
                return miu__ycgr
    if is_expr(mxqs__zbvt, 'getattr'):
        return getattr(get_const_value_inner(func_ir, mxqs__zbvt.value,
            arg_types, typemap, updated_containers), mxqs__zbvt.attr)
    if is_expr(mxqs__zbvt, 'getitem'):
        value = get_const_value_inner(func_ir, mxqs__zbvt.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, mxqs__zbvt.index, arg_types,
            typemap, updated_containers)
        return value[index]
    emn__scwdi = guard(find_callname, func_ir, mxqs__zbvt, typemap)
    if emn__scwdi is not None and len(emn__scwdi) == 2 and emn__scwdi[0
        ] == 'keys' and isinstance(emn__scwdi[1], ir.Var):
        wpzdx__ujzhq = mxqs__zbvt.func
        mxqs__zbvt = get_definition(func_ir, emn__scwdi[1])
        fyrld__dhhff = emn__scwdi[1].name
        if updated_containers and fyrld__dhhff in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                fyrld__dhhff, updated_containers[fyrld__dhhff]))
        require(is_expr(mxqs__zbvt, 'build_map'))
        vals = [rtxn__rsj[0] for rtxn__rsj in mxqs__zbvt.items]
        iwu__rhczw = guard(get_definition, func_ir, wpzdx__ujzhq)
        assert isinstance(iwu__rhczw, ir.Expr) and iwu__rhczw.attr == 'keys'
        iwu__rhczw.attr = 'copy'
        return [get_const_value_inner(func_ir, rtxn__rsj, arg_types,
            typemap, updated_containers) for rtxn__rsj in vals]
    if is_expr(mxqs__zbvt, 'build_map'):
        return {get_const_value_inner(func_ir, rtxn__rsj[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            rtxn__rsj[1], arg_types, typemap, updated_containers) for
            rtxn__rsj in mxqs__zbvt.items}
    if is_expr(mxqs__zbvt, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, rtxn__rsj, arg_types,
            typemap, updated_containers) for rtxn__rsj in mxqs__zbvt.items)
    if is_expr(mxqs__zbvt, 'build_list'):
        return [get_const_value_inner(func_ir, rtxn__rsj, arg_types,
            typemap, updated_containers) for rtxn__rsj in mxqs__zbvt.items]
    if is_expr(mxqs__zbvt, 'build_set'):
        return {get_const_value_inner(func_ir, rtxn__rsj, arg_types,
            typemap, updated_containers) for rtxn__rsj in mxqs__zbvt.items}
    if emn__scwdi == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, mxqs__zbvt.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if emn__scwdi == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, mxqs__zbvt.args[0],
            arg_types, typemap, updated_containers))
    if emn__scwdi == ('range', 'builtins') and len(mxqs__zbvt.args) == 1:
        return range(get_const_value_inner(func_ir, mxqs__zbvt.args[0],
            arg_types, typemap, updated_containers))
    if emn__scwdi == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, rtxn__rsj,
            arg_types, typemap, updated_containers) for rtxn__rsj in
            mxqs__zbvt.args))
    if emn__scwdi == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, mxqs__zbvt.args[0],
            arg_types, typemap, updated_containers))
    if emn__scwdi == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, mxqs__zbvt.args[0],
            arg_types, typemap, updated_containers))
    if emn__scwdi == ('format', 'builtins'):
        hexs__kmh = get_const_value_inner(func_ir, mxqs__zbvt.args[0],
            arg_types, typemap, updated_containers)
        wef__ndslz = get_const_value_inner(func_ir, mxqs__zbvt.args[1],
            arg_types, typemap, updated_containers) if len(mxqs__zbvt.args
            ) > 1 else ''
        return format(hexs__kmh, wef__ndslz)
    if emn__scwdi in (('init_binary_str_index',
        'bodo.hiframes.pd_index_ext'), ('init_numeric_index',
        'bodo.hiframes.pd_index_ext'), ('init_categorical_index',
        'bodo.hiframes.pd_index_ext'), ('init_datetime_index',
        'bodo.hiframes.pd_index_ext'), ('init_timedelta_index',
        'bodo.hiframes.pd_index_ext'), ('init_heter_index',
        'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, mxqs__zbvt.args[0],
            arg_types, typemap, updated_containers))
    if emn__scwdi == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, mxqs__zbvt.args[0],
            arg_types, typemap, updated_containers))
    if emn__scwdi == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, mxqs__zbvt.args
            [0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, mxqs__zbvt.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            mxqs__zbvt.args[2], arg_types, typemap, updated_containers))
    if emn__scwdi == ('len', 'builtins') and typemap and isinstance(typemap
        .get(mxqs__zbvt.args[0].name, None), types.BaseTuple):
        return len(typemap[mxqs__zbvt.args[0].name])
    if emn__scwdi == ('len', 'builtins'):
        dkge__nuwb = guard(get_definition, func_ir, mxqs__zbvt.args[0])
        if isinstance(dkge__nuwb, ir.Expr) and dkge__nuwb.op in ('build_tuple',
            'build_list', 'build_set', 'build_map'):
            return len(dkge__nuwb.items)
        return len(get_const_value_inner(func_ir, mxqs__zbvt.args[0],
            arg_types, typemap, updated_containers))
    if emn__scwdi == ('CategoricalDtype', 'pandas'):
        kws = dict(mxqs__zbvt.kws)
        dezw__ycuef = get_call_expr_arg('CategoricalDtype', mxqs__zbvt.args,
            kws, 0, 'categories', '')
        owsv__mplku = get_call_expr_arg('CategoricalDtype', mxqs__zbvt.args,
            kws, 1, 'ordered', False)
        if owsv__mplku is not False:
            owsv__mplku = get_const_value_inner(func_ir, owsv__mplku,
                arg_types, typemap, updated_containers)
        if dezw__ycuef == '':
            dezw__ycuef = None
        else:
            dezw__ycuef = get_const_value_inner(func_ir, dezw__ycuef,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(dezw__ycuef, owsv__mplku)
    if emn__scwdi == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, mxqs__zbvt.args[0],
            arg_types, typemap, updated_containers))
    if emn__scwdi is not None and len(emn__scwdi) == 2 and emn__scwdi[1
        ] == 'pandas' and emn__scwdi[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, emn__scwdi[0])()
    if emn__scwdi is not None and len(emn__scwdi) == 2 and isinstance(
        emn__scwdi[1], ir.Var):
        miu__ycgr = get_const_value_inner(func_ir, emn__scwdi[1], arg_types,
            typemap, updated_containers)
        args = [get_const_value_inner(func_ir, rtxn__rsj, arg_types,
            typemap, updated_containers) for rtxn__rsj in mxqs__zbvt.args]
        kws = {hlbr__bwgb[0]: get_const_value_inner(func_ir, hlbr__bwgb[1],
            arg_types, typemap, updated_containers) for hlbr__bwgb in
            mxqs__zbvt.kws}
        return getattr(miu__ycgr, emn__scwdi[0])(*args, **kws)
    if emn__scwdi is not None and len(emn__scwdi) == 2 and emn__scwdi[1
        ] == 'bodo' and emn__scwdi[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, rtxn__rsj, arg_types,
            typemap, updated_containers) for rtxn__rsj in mxqs__zbvt.args)
        kwargs = {uehth__jgrhd: get_const_value_inner(func_ir, rtxn__rsj,
            arg_types, typemap, updated_containers) for uehth__jgrhd,
            rtxn__rsj in dict(mxqs__zbvt.kws).items()}
        return getattr(bodo, emn__scwdi[0])(*args, **kwargs)
    if is_call(mxqs__zbvt) and typemap and isinstance(typemap.get(
        mxqs__zbvt.func.name, None), types.Dispatcher):
        py_func = typemap[mxqs__zbvt.func.name].dispatcher.py_func
        require(mxqs__zbvt.vararg is None)
        args = tuple(get_const_value_inner(func_ir, rtxn__rsj, arg_types,
            typemap, updated_containers) for rtxn__rsj in mxqs__zbvt.args)
        kwargs = {uehth__jgrhd: get_const_value_inner(func_ir, rtxn__rsj,
            arg_types, typemap, updated_containers) for uehth__jgrhd,
            rtxn__rsj in dict(mxqs__zbvt.kws).items()}
        arg_types = tuple(bodo.typeof(rtxn__rsj) for rtxn__rsj in args)
        kw_types = {tgtgy__jalaz: bodo.typeof(rtxn__rsj) for tgtgy__jalaz,
            rtxn__rsj in kwargs.items()}
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
    f_ir, typemap, pdhb__yvv, pdhb__yvv = bodo.compiler.get_func_type_info(
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
                    tcxcr__rne = guard(get_definition, f_ir, rhs.func)
                    if isinstance(tcxcr__rne, ir.Const) and isinstance(
                        tcxcr__rne.value, numba.core.dispatcher.
                        ObjModeLiftedWith):
                        return False
                    omhq__vydlb = guard(find_callname, f_ir, rhs)
                    if omhq__vydlb is None:
                        return False
                    func_name, qsh__xmzug = omhq__vydlb
                    if qsh__xmzug == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if omhq__vydlb in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if omhq__vydlb == ('File', 'h5py'):
                        return False
                    if isinstance(qsh__xmzug, ir.Var):
                        qofet__xtiv = typemap[qsh__xmzug.name]
                        if isinstance(qofet__xtiv, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(qofet__xtiv, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(qofet__xtiv, bodo.LoggingLoggerType):
                            return False
                        if str(qofet__xtiv).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            qsh__xmzug), ir.Arg)):
                            return False
                    if qsh__xmzug in ('numpy.random', 'time', 'logging',
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
        kaic__khq = func.literal_value.code
        umb__qgec = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            umb__qgec = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(umb__qgec, kaic__khq)
        fix_struct_return(f_ir)
        typemap, dlicc__aej, exna__vlczf, pdhb__yvv = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, exna__vlczf, dlicc__aej = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, exna__vlczf, dlicc__aej = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, exna__vlczf, dlicc__aej = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(dlicc__aej, types.DictType):
        xgxfx__lpvb = guard(get_struct_keynames, f_ir, typemap)
        if xgxfx__lpvb is not None:
            dlicc__aej = StructType((dlicc__aej.value_type,) * len(
                xgxfx__lpvb), xgxfx__lpvb)
    if is_udf and isinstance(dlicc__aej, (SeriesType, HeterogeneousSeriesType)
        ):
        fbl__sob = numba.core.registry.cpu_target.typing_context
        zka__nnwx = numba.core.registry.cpu_target.target_context
        qqooc__irxy = bodo.transforms.series_pass.SeriesPass(f_ir, fbl__sob,
            zka__nnwx, typemap, exna__vlczf, {})
        qqooc__irxy.run()
        qqooc__irxy.run()
        qqooc__irxy.run()
        mtfvx__pvg = compute_cfg_from_blocks(f_ir.blocks)
        qmyim__sbijm = [guard(_get_const_series_info, f_ir.blocks[
            iacm__mutl], f_ir, typemap) for iacm__mutl in mtfvx__pvg.
            exit_points() if isinstance(f_ir.blocks[iacm__mutl].body[-1],
            ir.Return)]
        if None in qmyim__sbijm or len(pd.Series(qmyim__sbijm).unique()) != 1:
            dlicc__aej.const_info = None
        else:
            dlicc__aej.const_info = qmyim__sbijm[0]
    return dlicc__aej


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    kyw__tcc = block.body[-1].value
    lcqj__mgzn = get_definition(f_ir, kyw__tcc)
    require(is_expr(lcqj__mgzn, 'cast'))
    lcqj__mgzn = get_definition(f_ir, lcqj__mgzn.value)
    require(is_call(lcqj__mgzn) and find_callname(f_ir, lcqj__mgzn) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    xaec__mjjw = lcqj__mgzn.args[1]
    pqsxo__uodyt = tuple(get_const_value_inner(f_ir, xaec__mjjw, typemap=
        typemap))
    if isinstance(typemap[kyw__tcc.name], HeterogeneousSeriesType):
        return len(typemap[kyw__tcc.name].data), pqsxo__uodyt
    ysf__hlpf = lcqj__mgzn.args[0]
    gzo__ropc = get_definition(f_ir, ysf__hlpf)
    func_name, pdtk__rqt = find_callname(f_ir, gzo__ropc)
    if is_call(gzo__ropc) and bodo.utils.utils.is_alloc_callname(func_name,
        pdtk__rqt):
        yuk__hew = gzo__ropc.args[0]
        yskp__wkaah = get_const_value_inner(f_ir, yuk__hew, typemap=typemap)
        return yskp__wkaah, pqsxo__uodyt
    if is_call(gzo__ropc) and find_callname(f_ir, gzo__ropc) in [('asarray',
        'numpy'), ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'), (
        'build_nullable_tuple', 'bodo.libs.nullable_tuple_ext')]:
        ysf__hlpf = gzo__ropc.args[0]
        gzo__ropc = get_definition(f_ir, ysf__hlpf)
    require(is_expr(gzo__ropc, 'build_tuple') or is_expr(gzo__ropc,
        'build_list'))
    return len(gzo__ropc.items), pqsxo__uodyt


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    rxu__uexz = []
    bkc__isy = []
    values = []
    for tgtgy__jalaz, rtxn__rsj in build_map.items:
        pyaew__dspoi = find_const(f_ir, tgtgy__jalaz)
        require(isinstance(pyaew__dspoi, str))
        bkc__isy.append(pyaew__dspoi)
        rxu__uexz.append(tgtgy__jalaz)
        values.append(rtxn__rsj)
    nkcio__nerev = ir.Var(scope, mk_unique_var('val_tup'), loc)
    ylb__xyp = ir.Assign(ir.Expr.build_tuple(values, loc), nkcio__nerev, loc)
    f_ir._definitions[nkcio__nerev.name] = [ylb__xyp.value]
    yjpro__jqxhf = ir.Var(scope, mk_unique_var('key_tup'), loc)
    kxdb__epnaw = ir.Assign(ir.Expr.build_tuple(rxu__uexz, loc),
        yjpro__jqxhf, loc)
    f_ir._definitions[yjpro__jqxhf.name] = [kxdb__epnaw.value]
    if typemap is not None:
        typemap[nkcio__nerev.name] = types.Tuple([typemap[rtxn__rsj.name] for
            rtxn__rsj in values])
        typemap[yjpro__jqxhf.name] = types.Tuple([typemap[rtxn__rsj.name] for
            rtxn__rsj in rxu__uexz])
    return bkc__isy, nkcio__nerev, ylb__xyp, yjpro__jqxhf, kxdb__epnaw


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    hiusx__ltqm = block.body[-1].value
    pjsey__bmf = guard(get_definition, f_ir, hiusx__ltqm)
    require(is_expr(pjsey__bmf, 'cast'))
    lcqj__mgzn = guard(get_definition, f_ir, pjsey__bmf.value)
    require(is_expr(lcqj__mgzn, 'build_map'))
    require(len(lcqj__mgzn.items) > 0)
    loc = block.loc
    scope = block.scope
    bkc__isy, nkcio__nerev, ylb__xyp, yjpro__jqxhf, kxdb__epnaw = (
        extract_keyvals_from_struct_map(f_ir, lcqj__mgzn, loc, scope))
    khp__wew = ir.Var(scope, mk_unique_var('conv_call'), loc)
    satc__esjsz = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), khp__wew, loc)
    f_ir._definitions[khp__wew.name] = [satc__esjsz.value]
    cwdbg__msgzp = ir.Var(scope, mk_unique_var('struct_val'), loc)
    cox__fhdpj = ir.Assign(ir.Expr.call(khp__wew, [nkcio__nerev,
        yjpro__jqxhf], {}, loc), cwdbg__msgzp, loc)
    f_ir._definitions[cwdbg__msgzp.name] = [cox__fhdpj.value]
    pjsey__bmf.value = cwdbg__msgzp
    lcqj__mgzn.items = [(tgtgy__jalaz, tgtgy__jalaz) for tgtgy__jalaz,
        pdhb__yvv in lcqj__mgzn.items]
    block.body = block.body[:-2] + [ylb__xyp, kxdb__epnaw, satc__esjsz,
        cox__fhdpj] + block.body[-2:]
    return tuple(bkc__isy)


def get_struct_keynames(f_ir, typemap):
    mtfvx__pvg = compute_cfg_from_blocks(f_ir.blocks)
    ttw__qgr = list(mtfvx__pvg.exit_points())[0]
    block = f_ir.blocks[ttw__qgr]
    require(isinstance(block.body[-1], ir.Return))
    hiusx__ltqm = block.body[-1].value
    pjsey__bmf = guard(get_definition, f_ir, hiusx__ltqm)
    require(is_expr(pjsey__bmf, 'cast'))
    lcqj__mgzn = guard(get_definition, f_ir, pjsey__bmf.value)
    require(is_call(lcqj__mgzn) and find_callname(f_ir, lcqj__mgzn) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[lcqj__mgzn.args[1].name])


def fix_struct_return(f_ir):
    aeihh__dlah = None
    mtfvx__pvg = compute_cfg_from_blocks(f_ir.blocks)
    for ttw__qgr in mtfvx__pvg.exit_points():
        aeihh__dlah = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            ttw__qgr], ttw__qgr)
    return aeihh__dlah


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    dtloh__txwbe = ir.Block(ir.Scope(None, loc), loc)
    dtloh__txwbe.body = node_list
    build_definitions({(0): dtloh__txwbe}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(rtxn__rsj) for rtxn__rsj in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    ups__cuqit = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(ups__cuqit, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for obe__fyl in range(len(vals) - 1, -1, -1):
        rtxn__rsj = vals[obe__fyl]
        if isinstance(rtxn__rsj, str) and rtxn__rsj.startswith(
            NESTED_TUP_SENTINEL):
            ykini__inp = int(rtxn__rsj[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:obe__fyl]) + (
                tuple(vals[obe__fyl + 1:obe__fyl + ykini__inp + 1]),) +
                tuple(vals[obe__fyl + ykini__inp + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    hexs__kmh = None
    if len(args) > arg_no and arg_no >= 0:
        hexs__kmh = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        hexs__kmh = kws[arg_name]
    if hexs__kmh is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return hexs__kmh


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
    hls__olqju = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        hls__olqju.update(extra_globals)
    func.__globals__.update(hls__olqju)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            yetlf__xhjf = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[yetlf__xhjf.name] = types.literal(default)
            except:
                pass_info.typemap[yetlf__xhjf.name] = numba.typeof(default)
            jzy__qnnuu = ir.Assign(ir.Const(default, loc), yetlf__xhjf, loc)
            pre_nodes.append(jzy__qnnuu)
            return yetlf__xhjf
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    zkpx__vtk = tuple(pass_info.typemap[rtxn__rsj.name] for rtxn__rsj in args)
    if const:
        lfuy__cwls = []
        for obe__fyl, hexs__kmh in enumerate(args):
            miu__ycgr = guard(find_const, pass_info.func_ir, hexs__kmh)
            if miu__ycgr:
                lfuy__cwls.append(types.literal(miu__ycgr))
            else:
                lfuy__cwls.append(zkpx__vtk[obe__fyl])
        zkpx__vtk = tuple(lfuy__cwls)
    return ReplaceFunc(func, zkpx__vtk, args, hls__olqju, inline_bodo_calls,
        run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(zumz__dbcb) for zumz__dbcb in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        ydzs__jwh = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {ydzs__jwh} = 0\n', (ydzs__jwh,)
    if isinstance(t, ArrayItemArrayType):
        bvl__zjp, dvexl__yle = gen_init_varsize_alloc_sizes(t.dtype)
        ydzs__jwh = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {ydzs__jwh} = 0\n' + bvl__zjp, (ydzs__jwh,) + dvexl__yle
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
        return 1 + sum(get_type_alloc_counts(zumz__dbcb.dtype) for
            zumz__dbcb in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(zumz__dbcb) for zumz__dbcb in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(zumz__dbcb) for zumz__dbcb in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    ljs__actbh = typing_context.resolve_getattr(obj_dtype, func_name)
    if ljs__actbh is None:
        mrf__tio = types.misc.Module(np)
        try:
            ljs__actbh = typing_context.resolve_getattr(mrf__tio, func_name)
        except AttributeError as gmdug__aju:
            ljs__actbh = None
        if ljs__actbh is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return ljs__actbh


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    ljs__actbh = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(ljs__actbh, types.BoundFunction):
        if axis is not None:
            spttc__qzh = ljs__actbh.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            spttc__qzh = ljs__actbh.get_call_type(typing_context, (), {})
        return spttc__qzh.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(ljs__actbh):
            spttc__qzh = ljs__actbh.get_call_type(typing_context, (
                obj_dtype,), {})
            return spttc__qzh.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    ljs__actbh = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(ljs__actbh, types.BoundFunction):
        ljn__osjbj = ljs__actbh.template
        if axis is not None:
            return ljn__osjbj._overload_func(obj_dtype, axis=axis)
        else:
            return ljn__osjbj._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    srpv__qfpg = get_definition(func_ir, dict_var)
    require(isinstance(srpv__qfpg, ir.Expr))
    require(srpv__qfpg.op == 'build_map')
    gkeo__pii = srpv__qfpg.items
    rxu__uexz = []
    values = []
    ypu__osfcf = False
    for obe__fyl in range(len(gkeo__pii)):
        shc__jtkuc, value = gkeo__pii[obe__fyl]
        try:
            gybzm__ktz = get_const_value_inner(func_ir, shc__jtkuc,
                arg_types, typemap, updated_containers)
            rxu__uexz.append(gybzm__ktz)
            values.append(value)
        except GuardException as gmdug__aju:
            require_const_map[shc__jtkuc] = label
            ypu__osfcf = True
    if ypu__osfcf:
        raise GuardException
    return rxu__uexz, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        rxu__uexz = tuple(get_const_value_inner(func_ir, t[0], args) for t in
            build_map.items)
    except GuardException as gmdug__aju:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in rxu__uexz):
        raise BodoError(err_msg, loc)
    return rxu__uexz


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    rxu__uexz = _get_const_keys_from_dict(args, func_ir, build_map, err_msg,
        loc)
    vksoz__xfbbs = []
    sze__mhhox = [bodo.transforms.typing_pass._create_const_var(
        tgtgy__jalaz, 'dict_key', scope, loc, vksoz__xfbbs) for
        tgtgy__jalaz in rxu__uexz]
    xprxq__xtcdl = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        ose__umjuz = ir.Var(scope, mk_unique_var('sentinel'), loc)
        zdfg__xbpni = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        vksoz__xfbbs.append(ir.Assign(ir.Const('__bodo_tup', loc),
            ose__umjuz, loc))
        gcfcy__ujy = [ose__umjuz] + sze__mhhox + xprxq__xtcdl
        vksoz__xfbbs.append(ir.Assign(ir.Expr.build_tuple(gcfcy__ujy, loc),
            zdfg__xbpni, loc))
        return (zdfg__xbpni,), vksoz__xfbbs
    else:
        ejzvh__imtpz = ir.Var(scope, mk_unique_var('values_tup'), loc)
        xmhd__angd = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        vksoz__xfbbs.append(ir.Assign(ir.Expr.build_tuple(xprxq__xtcdl, loc
            ), ejzvh__imtpz, loc))
        vksoz__xfbbs.append(ir.Assign(ir.Expr.build_tuple(sze__mhhox, loc),
            xmhd__angd, loc))
        return (ejzvh__imtpz, xmhd__angd), vksoz__xfbbs
