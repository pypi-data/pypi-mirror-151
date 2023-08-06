"""IR node for the groupby, pivot and cross_tabulation"""
import ctypes
import operator
import types as pytypes
from collections import defaultdict, namedtuple
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, compiler, ir, ir_utils, types
from numba.core.analysis import compute_use_defs
from numba.core.ir_utils import build_definitions, compile_to_numba_ir, find_callname, find_const, find_topo_order, get_definition, get_ir_of_code, get_name_var_table, guard, is_getitem, mk_unique_var, next_label, remove_dels, replace_arg_nodes, replace_var_names, replace_vars_inner, visit_vars_inner
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin
from numba.parfors.parfor import Parfor, unwrap_parfor_blocks, wrap_parfor_blocks
import bodo
from bodo.hiframes.datetime_date_ext import DatetimeDateArrayType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, groupby_and_aggregate, info_from_table, info_to_array, pivot_groupby_and_aggregate
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, pre_alloc_array_item_array
from bodo.libs.binary_arr_ext import BinaryArrayType, pre_alloc_binary_array
from bodo.libs.bool_arr_ext import BooleanArrayType
from bodo.libs.decimal_arr_ext import DecimalArrayType, alloc_decimal_array
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.transform import get_call_expr_arg
from bodo.utils.typing import BodoError, decode_if_dict_array, get_literal_value, get_overload_const_func, get_overload_const_str, get_overload_constant_dict, is_overload_constant_dict, is_overload_constant_str, list_cumulative, to_str_arr_if_dict_array
from bodo.utils.utils import debug_prints, incref, is_assign, is_call_assign, is_expr, is_null_pointer, is_var_assign, sanitize_varname, unliteral_all
gb_agg_cfunc = {}
gb_agg_cfunc_addr = {}


@intrinsic
def add_agg_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        sig = func.signature
        if sig == types.none(types.voidptr):
            cqrtr__vqwd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            rvlzt__nwzoq = cgutils.get_or_insert_function(builder.module,
                cqrtr__vqwd, sym._literal_value)
            builder.call(rvlzt__nwzoq, [context.get_constant_null(sig.args[0])]
                )
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            cqrtr__vqwd = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            rvlzt__nwzoq = cgutils.get_or_insert_function(builder.module,
                cqrtr__vqwd, sym._literal_value)
            builder.call(rvlzt__nwzoq, [context.get_constant(types.int64, 0
                ), context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            cqrtr__vqwd = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            rvlzt__nwzoq = cgutils.get_or_insert_function(builder.module,
                cqrtr__vqwd, sym._literal_value)
            builder.call(rvlzt__nwzoq, [context.get_constant_null(sig.args[
                0]), context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        context.add_linking_libs([gb_agg_cfunc[sym._literal_value]._library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_agg_udf_addr(name):
    with numba.objmode(addr='int64'):
        addr = gb_agg_cfunc_addr[name]
    return addr


class AggUDFStruct(object):

    def __init__(self, regular_udf_funcs=None, general_udf_funcs=None):
        assert regular_udf_funcs is not None or general_udf_funcs is not None
        self.regular_udfs = False
        self.general_udfs = False
        self.regular_udf_cfuncs = None
        self.general_udf_cfunc = None
        if regular_udf_funcs is not None:
            (self.var_typs, self.init_func, self.update_all_func, self.
                combine_all_func, self.eval_all_func) = regular_udf_funcs
            self.regular_udfs = True
        if general_udf_funcs is not None:
            self.general_udf_funcs = general_udf_funcs
            self.general_udfs = True

    def set_regular_cfuncs(self, update_cb, combine_cb, eval_cb):
        assert self.regular_udfs and self.regular_udf_cfuncs is None
        self.regular_udf_cfuncs = [update_cb, combine_cb, eval_cb]

    def set_general_cfunc(self, general_udf_cb):
        assert self.general_udfs and self.general_udf_cfunc is None
        self.general_udf_cfunc = general_udf_cb


AggFuncStruct = namedtuple('AggFuncStruct', ['func', 'ftype'])
supported_agg_funcs = ['no_op', 'head', 'transform', 'size', 'shift', 'sum',
    'count', 'nunique', 'median', 'cumsum', 'cumprod', 'cummin', 'cummax',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'idxmin', 'idxmax',
    'var', 'std', 'udf', 'gen_udf']
supported_transform_funcs = ['no_op', 'sum', 'count', 'nunique', 'median',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'var', 'std']


def get_agg_func(func_ir, func_name, rhs, series_type=None, typemap=None):
    if func_name == 'no_op':
        raise BodoError('Unknown aggregation function used in groupby.')
    if series_type is None:
        series_type = SeriesType(types.float64)
    if func_name in {'var', 'std'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 3
        func.ncols_post_shuffle = 4
        return func
    if func_name in {'first', 'last'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        return func
    if func_name in {'idxmin', 'idxmax'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 2
        func.ncols_post_shuffle = 2
        return func
    if func_name in supported_agg_funcs[:-8]:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        hudhm__ssswh = True
        bvc__xctvc = 1
        nbt__ngvmv = -1
        if isinstance(rhs, ir.Expr):
            for ujptu__uobc in rhs.kws:
                if func_name in list_cumulative:
                    if ujptu__uobc[0] == 'skipna':
                        hudhm__ssswh = guard(find_const, func_ir,
                            ujptu__uobc[1])
                        if not isinstance(hudhm__ssswh, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if ujptu__uobc[0] == 'dropna':
                        hudhm__ssswh = guard(find_const, func_ir,
                            ujptu__uobc[1])
                        if not isinstance(hudhm__ssswh, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            bvc__xctvc = get_call_expr_arg('shift', rhs.args, dict(rhs.kws),
                0, 'periods', bvc__xctvc)
            bvc__xctvc = guard(find_const, func_ir, bvc__xctvc)
        if func_name == 'head':
            nbt__ngvmv = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(nbt__ngvmv, int):
                nbt__ngvmv = guard(find_const, func_ir, nbt__ngvmv)
            if nbt__ngvmv < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = hudhm__ssswh
        func.periods = bvc__xctvc
        func.head_n = nbt__ngvmv
        if func_name == 'transform':
            kws = dict(rhs.kws)
            teuxr__jrve = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            irrss__lmgh = typemap[teuxr__jrve.name]
            rneqx__ioby = None
            if isinstance(irrss__lmgh, str):
                rneqx__ioby = irrss__lmgh
            elif is_overload_constant_str(irrss__lmgh):
                rneqx__ioby = get_overload_const_str(irrss__lmgh)
            elif bodo.utils.typing.is_builtin_function(irrss__lmgh):
                rneqx__ioby = bodo.utils.typing.get_builtin_function_name(
                    irrss__lmgh)
            if rneqx__ioby not in bodo.ir.aggregate.supported_transform_funcs[:
                ]:
                raise BodoError(f'unsupported transform function {rneqx__ioby}'
                    )
            func.transform_func = supported_agg_funcs.index(rneqx__ioby)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    teuxr__jrve = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if teuxr__jrve == '':
        irrss__lmgh = types.none
    else:
        irrss__lmgh = typemap[teuxr__jrve.name]
    if is_overload_constant_dict(irrss__lmgh):
        hex__fawk = get_overload_constant_dict(irrss__lmgh)
        muqy__uao = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in hex__fawk.values()]
        return muqy__uao
    if irrss__lmgh == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(irrss__lmgh, types.BaseTuple):
        muqy__uao = []
        hhqv__mzub = 0
        for t in irrss__lmgh.types:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                muqy__uao.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>':
                    func.fname = '<lambda_' + str(hhqv__mzub) + '>'
                    hhqv__mzub += 1
                muqy__uao.append(func)
        return [muqy__uao]
    if is_overload_constant_str(irrss__lmgh):
        func_name = get_overload_const_str(irrss__lmgh)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(irrss__lmgh):
        func_name = bodo.utils.typing.get_builtin_function_name(irrss__lmgh)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    assert typemap is not None, 'typemap is required for agg UDF handling'
    func = _get_const_agg_func(typemap[rhs.args[0].name], func_ir)
    func.ftype = 'udf'
    func.fname = _get_udf_name(func)
    return func


def get_agg_func_udf(func_ir, f_val, rhs, series_type, typemap):
    if isinstance(f_val, str):
        return get_agg_func(func_ir, f_val, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(f_val):
        func_name = bodo.utils.typing.get_builtin_function_name(f_val)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if isinstance(f_val, (tuple, list)):
        hhqv__mzub = 0
        tvabi__djao = []
        for lnoot__tebuf in f_val:
            func = get_agg_func_udf(func_ir, lnoot__tebuf, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{hhqv__mzub}>'
                hhqv__mzub += 1
            tvabi__djao.append(func)
        return tvabi__djao
    else:
        assert is_expr(f_val, 'make_function') or isinstance(f_val, (numba.
            core.registry.CPUDispatcher, types.Dispatcher))
        assert typemap is not None, 'typemap is required for agg UDF handling'
        func = _get_const_agg_func(f_val, func_ir)
        func.ftype = 'udf'
        func.fname = _get_udf_name(func)
        return func


def _get_udf_name(func):
    code = func.code if hasattr(func, 'code') else func.__code__
    rneqx__ioby = code.co_name
    return rneqx__ioby


def _get_const_agg_func(func_typ, func_ir):
    agg_func = get_overload_const_func(func_typ, func_ir)
    if is_expr(agg_func, 'make_function'):

        def agg_func_wrapper(A):
            return A
        agg_func_wrapper.__code__ = agg_func.code
        agg_func = agg_func_wrapper
        return agg_func
    return agg_func


@infer_global(type)
class TypeDt64(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if len(args) == 1 and isinstance(args[0], (types.NPDatetime, types.
            NPTimedelta)):
            nvm__ylvy = types.DType(args[0])
            return signature(nvm__ylvy, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    qeall__gcvci = nobs_a + nobs_b
    ekt__qotfn = (nobs_a * mean_a + nobs_b * mean_b) / qeall__gcvci
    wqtxf__kwdv = mean_b - mean_a
    wvfuv__ikf = (ssqdm_a + ssqdm_b + wqtxf__kwdv * wqtxf__kwdv * nobs_a *
        nobs_b / qeall__gcvci)
    return wvfuv__ikf, ekt__qotfn, qeall__gcvci


def __special_combine(*args):
    return


@infer_global(__special_combine)
class SpecialCombineTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *unliteral_all(args))


@lower_builtin(__special_combine, types.VarArg(types.Any))
def lower_special_combine(context, builder, sig, args):
    return context.get_dummy_value()


class Aggregate(ir.Stmt):

    def __init__(self, df_out, df_in, key_names, gb_info_in, gb_info_out,
        out_key_vars, df_out_vars, df_in_vars, key_arrs, input_has_index,
        same_index, return_key, loc, func_name, dropna=True, pivot_arr=None,
        pivot_values=None, is_crosstab=False):
        self.df_out = df_out
        self.df_in = df_in
        self.key_names = key_names
        self.gb_info_in = gb_info_in
        self.gb_info_out = gb_info_out
        self.out_key_vars = out_key_vars
        self.df_out_vars = df_out_vars
        self.df_in_vars = df_in_vars
        self.key_arrs = key_arrs
        self.input_has_index = input_has_index
        self.same_index = same_index
        self.return_key = return_key
        self.loc = loc
        self.func_name = func_name
        self.dropna = dropna
        self.pivot_arr = pivot_arr
        self.pivot_values = pivot_values
        self.is_crosstab = is_crosstab

    def __repr__(self):
        cmg__fnm = ''
        for rkhje__syl, lsux__mrcu in self.df_out_vars.items():
            cmg__fnm += "'{}':{}, ".format(rkhje__syl, lsux__mrcu.name)
        oha__dkt = '{}{{{}}}'.format(self.df_out, cmg__fnm)
        iqz__pvxj = ''
        for rkhje__syl, lsux__mrcu in self.df_in_vars.items():
            iqz__pvxj += "'{}':{}, ".format(rkhje__syl, lsux__mrcu.name)
        aghl__ldt = '{}{{{}}}'.format(self.df_in, iqz__pvxj)
        gajik__vgqma = 'pivot {}:{}'.format(self.pivot_arr.name, self.
            pivot_values) if self.pivot_arr is not None else ''
        key_names = ','.join(self.key_names)
        hatz__fdrs = ','.join([lsux__mrcu.name for lsux__mrcu in self.key_arrs]
            )
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(oha__dkt,
            aghl__ldt, key_names, hatz__fdrs, gajik__vgqma)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        old__slm, qaae__res = self.gb_info_out.pop(out_col_name)
        if old__slm is None and not self.is_crosstab:
            return
        wwjrq__hvduh = self.gb_info_in[old__slm]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for uakvf__iybbs, (func, cmg__fnm) in enumerate(wwjrq__hvduh):
                try:
                    cmg__fnm.remove(out_col_name)
                    if len(cmg__fnm) == 0:
                        wwjrq__hvduh.pop(uakvf__iybbs)
                        break
                except ValueError as bkdo__hyx:
                    continue
        else:
            for uakvf__iybbs, (func, fka__uco) in enumerate(wwjrq__hvduh):
                if fka__uco == out_col_name:
                    wwjrq__hvduh.pop(uakvf__iybbs)
                    break
        if len(wwjrq__hvduh) == 0:
            self.gb_info_in.pop(old__slm)
            self.df_in_vars.pop(old__slm)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({lsux__mrcu.name for lsux__mrcu in aggregate_node.key_arrs})
    use_set.update({lsux__mrcu.name for lsux__mrcu in aggregate_node.
        df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({lsux__mrcu.name for lsux__mrcu in aggregate_node.
        df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({lsux__mrcu.name for lsux__mrcu in aggregate_node.
            out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    pbehx__wlsz = [zbgid__jws for zbgid__jws, ndp__zya in aggregate_node.
        df_out_vars.items() if ndp__zya.name not in lives]
    for qydkf__izurr in pbehx__wlsz:
        aggregate_node.remove_out_col(qydkf__izurr)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(lsux__mrcu.name not in lives for
        lsux__mrcu in out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    eme__anf = set(lsux__mrcu.name for lsux__mrcu in aggregate_node.
        df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        eme__anf.update({lsux__mrcu.name for lsux__mrcu in aggregate_node.
            out_key_vars})
    return set(), eme__anf


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for uakvf__iybbs in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[uakvf__iybbs] = replace_vars_inner(
            aggregate_node.key_arrs[uakvf__iybbs], var_dict)
    for zbgid__jws in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[zbgid__jws] = replace_vars_inner(
            aggregate_node.df_in_vars[zbgid__jws], var_dict)
    for zbgid__jws in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[zbgid__jws] = replace_vars_inner(
            aggregate_node.df_out_vars[zbgid__jws], var_dict)
    if aggregate_node.out_key_vars is not None:
        for uakvf__iybbs in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[uakvf__iybbs] = replace_vars_inner(
                aggregate_node.out_key_vars[uakvf__iybbs], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for uakvf__iybbs in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[uakvf__iybbs] = visit_vars_inner(aggregate_node
            .key_arrs[uakvf__iybbs], callback, cbdata)
    for zbgid__jws in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[zbgid__jws] = visit_vars_inner(aggregate_node
            .df_in_vars[zbgid__jws], callback, cbdata)
    for zbgid__jws in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[zbgid__jws] = visit_vars_inner(
            aggregate_node.df_out_vars[zbgid__jws], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for uakvf__iybbs in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[uakvf__iybbs] = visit_vars_inner(
                aggregate_node.out_key_vars[uakvf__iybbs], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    uuks__dgrlc = []
    for yiaa__scnds in aggregate_node.key_arrs:
        iqquq__qlfq = equiv_set.get_shape(yiaa__scnds)
        if iqquq__qlfq:
            uuks__dgrlc.append(iqquq__qlfq[0])
    if aggregate_node.pivot_arr is not None:
        iqquq__qlfq = equiv_set.get_shape(aggregate_node.pivot_arr)
        if iqquq__qlfq:
            uuks__dgrlc.append(iqquq__qlfq[0])
    for ndp__zya in aggregate_node.df_in_vars.values():
        iqquq__qlfq = equiv_set.get_shape(ndp__zya)
        if iqquq__qlfq:
            uuks__dgrlc.append(iqquq__qlfq[0])
    if len(uuks__dgrlc) > 1:
        equiv_set.insert_equiv(*uuks__dgrlc)
    sju__mzsy = []
    uuks__dgrlc = []
    wiqf__etybq = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        wiqf__etybq.extend(aggregate_node.out_key_vars)
    for ndp__zya in wiqf__etybq:
        ght__yripn = typemap[ndp__zya.name]
        rsx__hcx = array_analysis._gen_shape_call(equiv_set, ndp__zya,
            ght__yripn.ndim, None, sju__mzsy)
        equiv_set.insert_equiv(ndp__zya, rsx__hcx)
        uuks__dgrlc.append(rsx__hcx[0])
        equiv_set.define(ndp__zya, set())
    if len(uuks__dgrlc) > 1:
        equiv_set.insert_equiv(*uuks__dgrlc)
    return [], sju__mzsy


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    dyq__vwp = Distribution.OneD
    for ndp__zya in aggregate_node.df_in_vars.values():
        dyq__vwp = Distribution(min(dyq__vwp.value, array_dists[ndp__zya.
            name].value))
    for yiaa__scnds in aggregate_node.key_arrs:
        dyq__vwp = Distribution(min(dyq__vwp.value, array_dists[yiaa__scnds
            .name].value))
    if aggregate_node.pivot_arr is not None:
        dyq__vwp = Distribution(min(dyq__vwp.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = dyq__vwp
    for ndp__zya in aggregate_node.df_in_vars.values():
        array_dists[ndp__zya.name] = dyq__vwp
    for yiaa__scnds in aggregate_node.key_arrs:
        array_dists[yiaa__scnds.name] = dyq__vwp
    ico__yqkx = Distribution.OneD_Var
    for ndp__zya in aggregate_node.df_out_vars.values():
        if ndp__zya.name in array_dists:
            ico__yqkx = Distribution(min(ico__yqkx.value, array_dists[
                ndp__zya.name].value))
    if aggregate_node.out_key_vars is not None:
        for ndp__zya in aggregate_node.out_key_vars:
            if ndp__zya.name in array_dists:
                ico__yqkx = Distribution(min(ico__yqkx.value, array_dists[
                    ndp__zya.name].value))
    ico__yqkx = Distribution(min(ico__yqkx.value, dyq__vwp.value))
    for ndp__zya in aggregate_node.df_out_vars.values():
        array_dists[ndp__zya.name] = ico__yqkx
    if aggregate_node.out_key_vars is not None:
        for unge__bqcts in aggregate_node.out_key_vars:
            array_dists[unge__bqcts.name] = ico__yqkx
    if ico__yqkx != Distribution.OneD_Var:
        for yiaa__scnds in aggregate_node.key_arrs:
            array_dists[yiaa__scnds.name] = ico__yqkx
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = ico__yqkx
        for ndp__zya in aggregate_node.df_in_vars.values():
            array_dists[ndp__zya.name] = ico__yqkx


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for ndp__zya in agg_node.df_out_vars.values():
        definitions[ndp__zya.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for unge__bqcts in agg_node.out_key_vars:
            definitions[unge__bqcts.name].append(agg_node)
    return definitions


ir_utils.build_defs_extensions[Aggregate] = build_agg_definitions


def __update_redvars():
    pass


@infer_global(__update_redvars)
class UpdateDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __combine_redvars():
    pass


@infer_global(__combine_redvars)
class CombineDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __eval_res():
    pass


@infer_global(__eval_res)
class EvalDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(args[0].dtype, *args)


def agg_distributed_run(agg_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    if array_dists is not None:
        parallel = True
        for lsux__mrcu in (list(agg_node.df_in_vars.values()) + list(
            agg_node.df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[lsux__mrcu.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                lsux__mrcu.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    gjp__hji = tuple(typemap[lsux__mrcu.name] for lsux__mrcu in agg_node.
        key_arrs)
    nepdt__uicm = [lsux__mrcu for nzoe__recb, lsux__mrcu in agg_node.
        df_in_vars.items()]
    nsgg__wnt = [lsux__mrcu for nzoe__recb, lsux__mrcu in agg_node.
        df_out_vars.items()]
    in_col_typs = []
    muqy__uao = []
    if agg_node.pivot_arr is not None:
        for old__slm, wwjrq__hvduh in agg_node.gb_info_in.items():
            for func, qaae__res in wwjrq__hvduh:
                if old__slm is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[old__slm
                        ].name])
                muqy__uao.append(func)
    else:
        for old__slm, func in agg_node.gb_info_out.values():
            if old__slm is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[old__slm].name])
            muqy__uao.append(func)
    out_col_typs = tuple(typemap[lsux__mrcu.name] for lsux__mrcu in nsgg__wnt)
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(gjp__hji + tuple(typemap[lsux__mrcu.name] for
        lsux__mrcu in nepdt__uicm) + (pivot_typ,))
    in_col_typs = [to_str_arr_if_dict_array(t) for t in in_col_typs]
    vkoz__wupbi = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for uakvf__iybbs, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            vkoz__wupbi.update({f'in_cat_dtype_{uakvf__iybbs}': in_col_typ})
    for uakvf__iybbs, puad__xjae in enumerate(out_col_typs):
        if isinstance(puad__xjae, bodo.CategoricalArrayType):
            vkoz__wupbi.update({f'out_cat_dtype_{uakvf__iybbs}': puad__xjae})
    udf_func_struct = get_udf_func_struct(muqy__uao, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    ipwei__ddr = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    vkoz__wupbi.update({'pd': pd, 'pre_alloc_string_array':
        pre_alloc_string_array, 'pre_alloc_binary_array':
        pre_alloc_binary_array, 'pre_alloc_array_item_array':
        pre_alloc_array_item_array, 'string_array_type': string_array_type,
        'alloc_decimal_array': alloc_decimal_array, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'coerce_to_array': bodo.utils.conversion.coerce_to_array,
        'groupby_and_aggregate': groupby_and_aggregate,
        'pivot_groupby_and_aggregate': pivot_groupby_and_aggregate,
        'info_from_table': info_from_table, 'info_to_array': info_to_array,
        'delete_info_decref_array': delete_info_decref_array,
        'delete_table': delete_table, 'add_agg_cfunc_sym':
        add_agg_cfunc_sym, 'get_agg_udf_addr': get_agg_udf_addr,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'decode_if_dict_array': decode_if_dict_array, 'out_typs': out_col_typs}
        )
    if udf_func_struct is not None:
        if udf_func_struct.regular_udfs:
            vkoz__wupbi.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            vkoz__wupbi.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    wkxmu__pko = compile_to_numba_ir(ipwei__ddr, vkoz__wupbi, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    oha__owxsz = []
    if agg_node.pivot_arr is None:
        taoi__vrcvn = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        okrt__qxajg = ir.Var(taoi__vrcvn, mk_unique_var('dummy_none'), loc)
        typemap[okrt__qxajg.name] = types.none
        oha__owxsz.append(ir.Assign(ir.Const(None, loc), okrt__qxajg, loc))
        nepdt__uicm.append(okrt__qxajg)
    else:
        nepdt__uicm.append(agg_node.pivot_arr)
    replace_arg_nodes(wkxmu__pko, agg_node.key_arrs + nepdt__uicm)
    lvh__eepus = wkxmu__pko.body[-3]
    assert is_assign(lvh__eepus) and isinstance(lvh__eepus.value, ir.Expr
        ) and lvh__eepus.value.op == 'build_tuple'
    oha__owxsz += wkxmu__pko.body[:-3]
    wiqf__etybq = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        wiqf__etybq += agg_node.out_key_vars
    for uakvf__iybbs, kew__evya in enumerate(wiqf__etybq):
        xgksk__cbqk = lvh__eepus.value.items[uakvf__iybbs]
        oha__owxsz.append(ir.Assign(xgksk__cbqk, kew__evya, kew__evya.loc))
    return oha__owxsz


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        ogu__oqi = args[0]
        dtype = types.Tuple([t.dtype for t in ogu__oqi.types]) if isinstance(
            ogu__oqi, types.BaseTuple) else ogu__oqi.dtype
        if isinstance(ogu__oqi, types.BaseTuple) and len(ogu__oqi.types) == 1:
            dtype = ogu__oqi.types[0].dtype
        return signature(types.Set(dtype), *args)


@lower_builtin(get_numba_set, types.Any)
def lower_get_numba_set(context, builder, sig, args):
    return numba.cpython.setobj.set_empty_constructor(context, builder, sig,
        args)


@infer_global(bool)
class BoolNoneTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        acn__zlhf = args[0]
        if acn__zlhf == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    eskzy__rhh = context.compile_internal(builder, lambda a: False, sig, args)
    return eskzy__rhh


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        lytot__sczwd = IntDtype(t.dtype).name
        assert lytot__sczwd.endswith('Dtype()')
        lytot__sczwd = lytot__sczwd[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{lytot__sczwd}'))"
            )
    elif isinstance(t, BooleanArrayType):
        return (
            'bodo.libs.bool_arr_ext.init_bool_array(np.empty(0, np.bool_), np.empty(0, np.uint8))'
            )
    elif isinstance(t, StringArrayType):
        return 'pre_alloc_string_array(1, 1)'
    elif isinstance(t, BinaryArrayType):
        return 'pre_alloc_binary_array(1, 1)'
    elif t == ArrayItemArrayType(string_array_type):
        return 'pre_alloc_array_item_array(1, (1, 1), string_array_type)'
    elif isinstance(t, DecimalArrayType):
        return 'alloc_decimal_array(1, {}, {})'.format(t.precision, t.scale)
    elif isinstance(t, DatetimeDateArrayType):
        return (
            'bodo.hiframes.datetime_date_ext.init_datetime_date_array(np.empty(1, np.int64), np.empty(1, np.uint8))'
            )
    elif isinstance(t, bodo.CategoricalArrayType):
        if t.dtype.categories is None:
            raise BodoError(
                'Groupby agg operations on Categorical types require constant categories'
                )
        icu__flmhl = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {icu__flmhl}_cat_dtype_{colnum})')
    else:
        return 'np.empty(1, {})'.format(_get_np_dtype(t.dtype))


def _get_np_dtype(t):
    if t == types.bool_:
        return 'np.bool_'
    if t == types.NPDatetime('ns'):
        return 'dt64_dtype'
    if t == types.NPTimedelta('ns'):
        return 'td64_dtype'
    return 'np.{}'.format(t)


def gen_update_cb(udf_func_struct, allfuncs, n_keys, data_in_typs_,
    out_data_typs, do_combine, func_idx_to_in_col, label_suffix):
    nvcuz__jwpo = udf_func_struct.var_typs
    ldmxh__svcu = len(nvcuz__jwpo)
    ctu__ryr = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    ctu__ryr += '    if is_null_pointer(in_table):\n'
    ctu__ryr += '        return\n'
    ctu__ryr += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in nvcuz__jwpo]), 
        ',' if len(nvcuz__jwpo) == 1 else '')
    rtuhs__yxjpp = n_keys
    mkfvu__ytnkb = []
    redvar_offsets = []
    wix__oajnb = []
    if do_combine:
        for uakvf__iybbs, lnoot__tebuf in enumerate(allfuncs):
            if lnoot__tebuf.ftype != 'udf':
                rtuhs__yxjpp += lnoot__tebuf.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(rtuhs__yxjpp, rtuhs__yxjpp +
                    lnoot__tebuf.n_redvars))
                rtuhs__yxjpp += lnoot__tebuf.n_redvars
                wix__oajnb.append(data_in_typs_[func_idx_to_in_col[
                    uakvf__iybbs]])
                mkfvu__ytnkb.append(func_idx_to_in_col[uakvf__iybbs] + n_keys)
    else:
        for uakvf__iybbs, lnoot__tebuf in enumerate(allfuncs):
            if lnoot__tebuf.ftype != 'udf':
                rtuhs__yxjpp += lnoot__tebuf.ncols_post_shuffle
            else:
                redvar_offsets += list(range(rtuhs__yxjpp + 1, rtuhs__yxjpp +
                    1 + lnoot__tebuf.n_redvars))
                rtuhs__yxjpp += lnoot__tebuf.n_redvars + 1
                wix__oajnb.append(data_in_typs_[func_idx_to_in_col[
                    uakvf__iybbs]])
                mkfvu__ytnkb.append(func_idx_to_in_col[uakvf__iybbs] + n_keys)
    assert len(redvar_offsets) == ldmxh__svcu
    ezen__gjmzb = len(wix__oajnb)
    zzca__roxf = []
    for uakvf__iybbs, t in enumerate(wix__oajnb):
        zzca__roxf.append(_gen_dummy_alloc(t, uakvf__iybbs, True))
    ctu__ryr += '    data_in_dummy = ({}{})\n'.format(','.join(zzca__roxf),
        ',' if len(wix__oajnb) == 1 else '')
    ctu__ryr += """
    # initialize redvar cols
"""
    ctu__ryr += '    init_vals = __init_func()\n'
    for uakvf__iybbs in range(ldmxh__svcu):
        ctu__ryr += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(uakvf__iybbs, redvar_offsets[uakvf__iybbs], uakvf__iybbs))
        ctu__ryr += '    incref(redvar_arr_{})\n'.format(uakvf__iybbs)
        ctu__ryr += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            uakvf__iybbs, uakvf__iybbs)
    ctu__ryr += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(uakvf__iybbs) for uakvf__iybbs in range(ldmxh__svcu)]), ',' if
        ldmxh__svcu == 1 else '')
    ctu__ryr += '\n'
    for uakvf__iybbs in range(ezen__gjmzb):
        ctu__ryr += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(uakvf__iybbs, mkfvu__ytnkb[uakvf__iybbs], uakvf__iybbs))
        ctu__ryr += '    incref(data_in_{})\n'.format(uakvf__iybbs)
    ctu__ryr += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(uakvf__iybbs) for uakvf__iybbs in range(ezen__gjmzb)]), ',' if
        ezen__gjmzb == 1 else '')
    ctu__ryr += '\n'
    ctu__ryr += '    for i in range(len(data_in_0)):\n'
    ctu__ryr += '        w_ind = row_to_group[i]\n'
    ctu__ryr += '        if w_ind != -1:\n'
    ctu__ryr += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    hsqff__hid = {}
    exec(ctu__ryr, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, hsqff__hid)
    return hsqff__hid['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    nvcuz__jwpo = udf_func_struct.var_typs
    ldmxh__svcu = len(nvcuz__jwpo)
    ctu__ryr = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    ctu__ryr += '    if is_null_pointer(in_table):\n'
    ctu__ryr += '        return\n'
    ctu__ryr += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in nvcuz__jwpo]), 
        ',' if len(nvcuz__jwpo) == 1 else '')
    kos__cec = n_keys
    wueuq__jgln = n_keys
    xrz__qzvw = []
    qkqq__dmpj = []
    for lnoot__tebuf in allfuncs:
        if lnoot__tebuf.ftype != 'udf':
            kos__cec += lnoot__tebuf.ncols_pre_shuffle
            wueuq__jgln += lnoot__tebuf.ncols_post_shuffle
        else:
            xrz__qzvw += list(range(kos__cec, kos__cec + lnoot__tebuf.
                n_redvars))
            qkqq__dmpj += list(range(wueuq__jgln + 1, wueuq__jgln + 1 +
                lnoot__tebuf.n_redvars))
            kos__cec += lnoot__tebuf.n_redvars
            wueuq__jgln += 1 + lnoot__tebuf.n_redvars
    assert len(xrz__qzvw) == ldmxh__svcu
    ctu__ryr += """
    # initialize redvar cols
"""
    ctu__ryr += '    init_vals = __init_func()\n'
    for uakvf__iybbs in range(ldmxh__svcu):
        ctu__ryr += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(uakvf__iybbs, qkqq__dmpj[uakvf__iybbs], uakvf__iybbs))
        ctu__ryr += '    incref(redvar_arr_{})\n'.format(uakvf__iybbs)
        ctu__ryr += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(
            uakvf__iybbs, uakvf__iybbs)
    ctu__ryr += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(uakvf__iybbs) for uakvf__iybbs in range(ldmxh__svcu)]), ',' if
        ldmxh__svcu == 1 else '')
    ctu__ryr += '\n'
    for uakvf__iybbs in range(ldmxh__svcu):
        ctu__ryr += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(uakvf__iybbs, xrz__qzvw[uakvf__iybbs], uakvf__iybbs))
        ctu__ryr += '    incref(recv_redvar_arr_{})\n'.format(uakvf__iybbs)
    ctu__ryr += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(uakvf__iybbs) for uakvf__iybbs in range
        (ldmxh__svcu)]), ',' if ldmxh__svcu == 1 else '')
    ctu__ryr += '\n'
    if ldmxh__svcu:
        ctu__ryr += '    for i in range(len(recv_redvar_arr_0)):\n'
        ctu__ryr += '        w_ind = row_to_group[i]\n'
        ctu__ryr += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)\n'
            )
    hsqff__hid = {}
    exec(ctu__ryr, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, hsqff__hid)
    return hsqff__hid['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    nvcuz__jwpo = udf_func_struct.var_typs
    ldmxh__svcu = len(nvcuz__jwpo)
    rtuhs__yxjpp = n_keys
    redvar_offsets = []
    cwq__snm = []
    out_data_typs = []
    for uakvf__iybbs, lnoot__tebuf in enumerate(allfuncs):
        if lnoot__tebuf.ftype != 'udf':
            rtuhs__yxjpp += lnoot__tebuf.ncols_post_shuffle
        else:
            cwq__snm.append(rtuhs__yxjpp)
            redvar_offsets += list(range(rtuhs__yxjpp + 1, rtuhs__yxjpp + 1 +
                lnoot__tebuf.n_redvars))
            rtuhs__yxjpp += 1 + lnoot__tebuf.n_redvars
            out_data_typs.append(out_data_typs_[uakvf__iybbs])
    assert len(redvar_offsets) == ldmxh__svcu
    ezen__gjmzb = len(out_data_typs)
    ctu__ryr = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    ctu__ryr += '    if is_null_pointer(table):\n'
    ctu__ryr += '        return\n'
    ctu__ryr += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in nvcuz__jwpo]), 
        ',' if len(nvcuz__jwpo) == 1 else '')
    ctu__ryr += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for uakvf__iybbs in range(ldmxh__svcu):
        ctu__ryr += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(uakvf__iybbs, redvar_offsets[uakvf__iybbs], uakvf__iybbs))
        ctu__ryr += '    incref(redvar_arr_{})\n'.format(uakvf__iybbs)
    ctu__ryr += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(uakvf__iybbs) for uakvf__iybbs in range(ldmxh__svcu)]), ',' if
        ldmxh__svcu == 1 else '')
    ctu__ryr += '\n'
    for uakvf__iybbs in range(ezen__gjmzb):
        ctu__ryr += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(uakvf__iybbs, cwq__snm[uakvf__iybbs], uakvf__iybbs))
        ctu__ryr += '    incref(data_out_{})\n'.format(uakvf__iybbs)
    ctu__ryr += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(uakvf__iybbs) for uakvf__iybbs in range(ezen__gjmzb)]), ',' if
        ezen__gjmzb == 1 else '')
    ctu__ryr += '\n'
    ctu__ryr += '    for i in range(len(data_out_0)):\n'
    ctu__ryr += '        __eval_res(redvars, data_out, i)\n'
    hsqff__hid = {}
    exec(ctu__ryr, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, hsqff__hid)
    return hsqff__hid['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    rtuhs__yxjpp = n_keys
    rhv__uotm = []
    for uakvf__iybbs, lnoot__tebuf in enumerate(allfuncs):
        if lnoot__tebuf.ftype == 'gen_udf':
            rhv__uotm.append(rtuhs__yxjpp)
            rtuhs__yxjpp += 1
        elif lnoot__tebuf.ftype != 'udf':
            rtuhs__yxjpp += lnoot__tebuf.ncols_post_shuffle
        else:
            rtuhs__yxjpp += lnoot__tebuf.n_redvars + 1
    ctu__ryr = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    ctu__ryr += '    if num_groups == 0:\n'
    ctu__ryr += '        return\n'
    for uakvf__iybbs, func in enumerate(udf_func_struct.general_udf_funcs):
        ctu__ryr += '    # col {}\n'.format(uakvf__iybbs)
        ctu__ryr += (
            '    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)\n'
            .format(rhv__uotm[uakvf__iybbs], uakvf__iybbs))
        ctu__ryr += '    incref(out_col)\n'
        ctu__ryr += '    for j in range(num_groups):\n'
        ctu__ryr += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(uakvf__iybbs, uakvf__iybbs))
        ctu__ryr += '        incref(in_col)\n'
        ctu__ryr += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(uakvf__iybbs))
    vkoz__wupbi = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    oez__ige = 0
    for uakvf__iybbs, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[oez__ige]
        vkoz__wupbi['func_{}'.format(oez__ige)] = func
        vkoz__wupbi['in_col_{}_typ'.format(oez__ige)] = in_col_typs[
            func_idx_to_in_col[uakvf__iybbs]]
        vkoz__wupbi['out_col_{}_typ'.format(oez__ige)] = out_col_typs[
            uakvf__iybbs]
        oez__ige += 1
    hsqff__hid = {}
    exec(ctu__ryr, vkoz__wupbi, hsqff__hid)
    lnoot__tebuf = hsqff__hid['bodo_gb_apply_general_udfs{}'.format(
        label_suffix)]
    zsdaz__lzpnc = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(zsdaz__lzpnc, nopython=True)(lnoot__tebuf)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    sgi__bfbcu = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        hkrvx__klkuu = 1
    else:
        hkrvx__klkuu = len(agg_node.pivot_values)
    tzdg__dsda = tuple('key_' + sanitize_varname(rkhje__syl) for rkhje__syl in
        agg_node.key_names)
    aac__qek = {rkhje__syl: 'in_{}'.format(sanitize_varname(rkhje__syl)) for
        rkhje__syl in agg_node.gb_info_in.keys() if rkhje__syl is not None}
    ftey__aud = {rkhje__syl: ('out_' + sanitize_varname(rkhje__syl)) for
        rkhje__syl in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    dpfqd__djpw = ', '.join(tzdg__dsda)
    hpay__ayz = ', '.join(aac__qek.values())
    if hpay__ayz != '':
        hpay__ayz = ', ' + hpay__ayz
    ctu__ryr = 'def agg_top({}{}{}, pivot_arr):\n'.format(dpfqd__djpw,
        hpay__ayz, ', index_arg' if agg_node.input_has_index else '')
    for a in (tzdg__dsda + tuple(aac__qek.values())):
        ctu__ryr += f'    {a} = decode_if_dict_array({a})\n'
    if sgi__bfbcu:
        ctu__ryr += f'    pivot_arr = decode_if_dict_array(pivot_arr)\n'
        lmr__kizaj = []
        for old__slm, wwjrq__hvduh in agg_node.gb_info_in.items():
            if old__slm is not None:
                for func, qaae__res in wwjrq__hvduh:
                    lmr__kizaj.append(aac__qek[old__slm])
    else:
        lmr__kizaj = tuple(aac__qek[old__slm] for old__slm, qaae__res in
            agg_node.gb_info_out.values() if old__slm is not None)
    dvym__qenc = tzdg__dsda + tuple(lmr__kizaj)
    ctu__ryr += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in dvym__qenc), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    ctu__ryr += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    tky__mdw = []
    func_idx_to_in_col = []
    nim__vis = []
    hudhm__ssswh = False
    kuo__jrt = 1
    nbt__ngvmv = -1
    omyux__wsgj = 0
    ybg__glt = 0
    if not sgi__bfbcu:
        muqy__uao = [func for qaae__res, func in agg_node.gb_info_out.values()]
    else:
        muqy__uao = [func for func, qaae__res in wwjrq__hvduh for
            wwjrq__hvduh in agg_node.gb_info_in.values()]
    for hwi__ggy, func in enumerate(muqy__uao):
        tky__mdw.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            omyux__wsgj += 1
        if hasattr(func, 'skipdropna'):
            hudhm__ssswh = func.skipdropna
        if func.ftype == 'shift':
            kuo__jrt = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            ybg__glt = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            nbt__ngvmv = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(hwi__ggy)
        if func.ftype == 'udf':
            nim__vis.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            nim__vis.append(0)
            do_combine = False
    tky__mdw.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == hkrvx__klkuu, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * hkrvx__klkuu, 'invalid number of groupby outputs'
    if omyux__wsgj > 0:
        if omyux__wsgj != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    for uakvf__iybbs, rkhje__syl in enumerate(agg_node.gb_info_out.keys()):
        tze__tsol = ftey__aud[rkhje__syl] + '_dummy'
        puad__xjae = out_col_typs[uakvf__iybbs]
        old__slm, func = agg_node.gb_info_out[rkhje__syl]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(puad__xjae, bodo.
            CategoricalArrayType):
            ctu__ryr += '    {} = {}\n'.format(tze__tsol, aac__qek[old__slm])
        elif udf_func_struct is not None:
            ctu__ryr += '    {} = {}\n'.format(tze__tsol, _gen_dummy_alloc(
                puad__xjae, uakvf__iybbs, False))
    if udf_func_struct is not None:
        ndjr__vtd = next_label()
        if udf_func_struct.regular_udfs:
            zsdaz__lzpnc = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            tolr__tsc = numba.cfunc(zsdaz__lzpnc, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, ndjr__vtd))
            sipra__jixg = numba.cfunc(zsdaz__lzpnc, nopython=True)(
                gen_combine_cb(udf_func_struct, allfuncs, n_keys,
                out_col_typs, ndjr__vtd))
            zbgs__abn = numba.cfunc('void(voidptr)', nopython=True)(gen_eval_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, ndjr__vtd))
            udf_func_struct.set_regular_cfuncs(tolr__tsc, sipra__jixg,
                zbgs__abn)
            for qwcx__pbme in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[qwcx__pbme.native_name] = qwcx__pbme
                gb_agg_cfunc_addr[qwcx__pbme.native_name] = qwcx__pbme.address
        if udf_func_struct.general_udfs:
            dnt__gorw = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col,
                ndjr__vtd)
            udf_func_struct.set_general_cfunc(dnt__gorw)
        cdf__yofov = []
        zfx__jqpi = 0
        uakvf__iybbs = 0
        for tze__tsol, lnoot__tebuf in zip(ftey__aud.values(), allfuncs):
            if lnoot__tebuf.ftype in ('udf', 'gen_udf'):
                cdf__yofov.append(tze__tsol + '_dummy')
                for kbi__xev in range(zfx__jqpi, zfx__jqpi + nim__vis[
                    uakvf__iybbs]):
                    cdf__yofov.append('data_redvar_dummy_' + str(kbi__xev))
                zfx__jqpi += nim__vis[uakvf__iybbs]
                uakvf__iybbs += 1
        if udf_func_struct.regular_udfs:
            nvcuz__jwpo = udf_func_struct.var_typs
            for uakvf__iybbs, t in enumerate(nvcuz__jwpo):
                ctu__ryr += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(uakvf__iybbs, _get_np_dtype(t)))
        ctu__ryr += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in cdf__yofov))
        ctu__ryr += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            ctu__ryr += "    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".format(
                tolr__tsc.native_name)
            ctu__ryr += "    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".format(
                sipra__jixg.native_name)
            ctu__ryr += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                zbgs__abn.native_name)
            ctu__ryr += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(tolr__tsc.native_name))
            ctu__ryr += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(sipra__jixg.native_name))
            ctu__ryr += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n".
                format(zbgs__abn.native_name))
        else:
            ctu__ryr += '    cpp_cb_update_addr = 0\n'
            ctu__ryr += '    cpp_cb_combine_addr = 0\n'
            ctu__ryr += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            qwcx__pbme = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[qwcx__pbme.native_name] = qwcx__pbme
            gb_agg_cfunc_addr[qwcx__pbme.native_name] = qwcx__pbme.address
            ctu__ryr += "    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".format(
                qwcx__pbme.native_name)
            ctu__ryr += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(qwcx__pbme.native_name))
        else:
            ctu__ryr += '    cpp_cb_general_addr = 0\n'
    else:
        ctu__ryr += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        ctu__ryr += '    cpp_cb_update_addr = 0\n'
        ctu__ryr += '    cpp_cb_combine_addr = 0\n'
        ctu__ryr += '    cpp_cb_eval_addr = 0\n'
        ctu__ryr += '    cpp_cb_general_addr = 0\n'
    ctu__ryr += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(lnoot__tebuf.ftype)) for
        lnoot__tebuf in allfuncs] + ['0']))
    ctu__ryr += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(str
        (tky__mdw))
    if len(nim__vis) > 0:
        ctu__ryr += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(str
            (nim__vis))
    else:
        ctu__ryr += '    udf_ncols = np.array([0], np.int32)\n'
    if sgi__bfbcu:
        ctu__ryr += '    arr_type = coerce_to_array({})\n'.format(agg_node.
            pivot_values)
        ctu__ryr += '    arr_info = array_to_info(arr_type)\n'
        ctu__ryr += '    dispatch_table = arr_info_list_to_table([arr_info])\n'
        ctu__ryr += '    pivot_info = array_to_info(pivot_arr)\n'
        ctu__ryr += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        ctu__ryr += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, hudhm__ssswh, agg_node.return_key, agg_node.
            same_index))
        ctu__ryr += '    delete_info_decref_array(pivot_info)\n'
        ctu__ryr += '    delete_info_decref_array(arr_info)\n'
    else:
        ctu__ryr += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel,
            hudhm__ssswh, kuo__jrt, ybg__glt, nbt__ngvmv, agg_node.
            return_key, agg_node.same_index, agg_node.dropna))
    uzfu__mhkr = 0
    if agg_node.return_key:
        for uakvf__iybbs, ucv__nuo in enumerate(tzdg__dsda):
            ctu__ryr += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(ucv__nuo, uzfu__mhkr, ucv__nuo))
            uzfu__mhkr += 1
    for uakvf__iybbs, tze__tsol in enumerate(ftey__aud.values()):
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(puad__xjae, bodo.
            CategoricalArrayType):
            ctu__ryr += f"""    {tze__tsol} = info_to_array(info_from_table(out_table, {uzfu__mhkr}), {tze__tsol + '_dummy'})
"""
        else:
            ctu__ryr += f"""    {tze__tsol} = info_to_array(info_from_table(out_table, {uzfu__mhkr}), out_typs[{uakvf__iybbs}])
"""
        uzfu__mhkr += 1
    if agg_node.same_index:
        ctu__ryr += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(uzfu__mhkr))
        uzfu__mhkr += 1
    ctu__ryr += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    ctu__ryr += '    delete_table_decref_arrays(table)\n'
    ctu__ryr += '    delete_table_decref_arrays(udf_table_dummy)\n'
    ctu__ryr += '    delete_table(out_table)\n'
    ctu__ryr += f'    ev_clean.finalize()\n'
    rejnt__dmcw = tuple(ftey__aud.values())
    if agg_node.return_key:
        rejnt__dmcw += tuple(tzdg__dsda)
    ctu__ryr += '    return ({},{})\n'.format(', '.join(rejnt__dmcw), 
        ' out_index_arg,' if agg_node.same_index else '')
    hsqff__hid = {}
    exec(ctu__ryr, {'out_typs': out_col_typs}, hsqff__hid)
    cyc__ovxi = hsqff__hid['agg_top']
    return cyc__ovxi


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for cnf__ici in block.body:
            if is_call_assign(cnf__ici) and find_callname(f_ir, cnf__ici.value
                ) == ('len', 'builtins') and cnf__ici.value.args[0
                ].name == f_ir.arg_names[0]:
                mtjcm__ssy = get_definition(f_ir, cnf__ici.value.func)
                mtjcm__ssy.name = 'dummy_agg_count'
                mtjcm__ssy.value = dummy_agg_count
    uolg__ujp = get_name_var_table(f_ir.blocks)
    fpkeb__fjne = {}
    for name, qaae__res in uolg__ujp.items():
        fpkeb__fjne[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, fpkeb__fjne)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    cgxwc__syao = numba.core.compiler.Flags()
    cgxwc__syao.nrt = True
    twf__hlb = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, cgxwc__syao)
    twf__hlb.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, jiwo__dre, calltypes, qaae__res = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    ows__dygui = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    thto__fejr = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    zesz__cocf = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    awxxl__krar = zesz__cocf(typemap, calltypes)
    pm = thto__fejr(typingctx, targetctx, None, f_ir, typemap, jiwo__dre,
        calltypes, awxxl__krar, {}, cgxwc__syao, None)
    vqwji__fcy = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = thto__fejr(typingctx, targetctx, None, f_ir, typemap, jiwo__dre,
        calltypes, awxxl__krar, {}, cgxwc__syao, vqwji__fcy)
    lridb__scyo = numba.core.typed_passes.InlineOverloads()
    lridb__scyo.run_pass(pm)
    unvdk__phpe = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    unvdk__phpe.run()
    for block in f_ir.blocks.values():
        for cnf__ici in block.body:
            if is_assign(cnf__ici) and isinstance(cnf__ici.value, (ir.Arg,
                ir.Var)) and isinstance(typemap[cnf__ici.target.name],
                SeriesType):
                ght__yripn = typemap.pop(cnf__ici.target.name)
                typemap[cnf__ici.target.name] = ght__yripn.data
            if is_call_assign(cnf__ici) and find_callname(f_ir, cnf__ici.value
                ) == ('get_series_data', 'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[cnf__ici.target.name].remove(cnf__ici.value)
                cnf__ici.value = cnf__ici.value.args[0]
                f_ir._definitions[cnf__ici.target.name].append(cnf__ici.value)
            if is_call_assign(cnf__ici) and find_callname(f_ir, cnf__ici.value
                ) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[cnf__ici.target.name].remove(cnf__ici.value)
                cnf__ici.value = ir.Const(False, cnf__ici.loc)
                f_ir._definitions[cnf__ici.target.name].append(cnf__ici.value)
            if is_call_assign(cnf__ici) and find_callname(f_ir, cnf__ici.value
                ) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[cnf__ici.target.name].remove(cnf__ici.value)
                cnf__ici.value = ir.Const(False, cnf__ici.loc)
                f_ir._definitions[cnf__ici.target.name].append(cnf__ici.value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    zobzl__qhhwc = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, ows__dygui)
    zobzl__qhhwc.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    pnu__ukkcq = numba.core.compiler.StateDict()
    pnu__ukkcq.func_ir = f_ir
    pnu__ukkcq.typemap = typemap
    pnu__ukkcq.calltypes = calltypes
    pnu__ukkcq.typingctx = typingctx
    pnu__ukkcq.targetctx = targetctx
    pnu__ukkcq.return_type = jiwo__dre
    numba.core.rewrites.rewrite_registry.apply('after-inference', pnu__ukkcq)
    frsx__uoh = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        jiwo__dre, typingctx, targetctx, ows__dygui, cgxwc__syao, {})
    frsx__uoh.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            mirkk__qok = ctypes.pythonapi.PyCell_Get
            mirkk__qok.restype = ctypes.py_object
            mirkk__qok.argtypes = ctypes.py_object,
            hex__fawk = tuple(mirkk__qok(syeq__rqhmb) for syeq__rqhmb in
                closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            hex__fawk = closure.items
        assert len(code.co_freevars) == len(hex__fawk)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, hex__fawk)


class RegularUDFGenerator(object):

    def __init__(self, in_col_types, out_col_types, pivot_typ, pivot_values,
        is_crosstab, typingctx, targetctx):
        self.in_col_types = in_col_types
        self.out_col_types = out_col_types
        self.pivot_typ = pivot_typ
        self.pivot_values = pivot_values
        self.is_crosstab = is_crosstab
        self.typingctx = typingctx
        self.targetctx = targetctx
        self.all_reduce_vars = []
        self.all_vartypes = []
        self.all_init_nodes = []
        self.all_eval_funcs = []
        self.all_update_funcs = []
        self.all_combine_funcs = []
        self.curr_offset = 0
        self.redvar_offsets = [0]

    def add_udf(self, in_col_typ, func):
        wkkbg__bdl = SeriesType(in_col_typ.dtype, in_col_typ, None, string_type
            )
        f_ir, pm = compile_to_optimized_ir(func, (wkkbg__bdl,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        lcbm__eezlt, arr_var = _rm_arg_agg_block(block, pm.typemap)
        stn__qxqe = -1
        for uakvf__iybbs, cnf__ici in enumerate(lcbm__eezlt):
            if isinstance(cnf__ici, numba.parfors.parfor.Parfor):
                assert stn__qxqe == -1, 'only one parfor for aggregation function'
                stn__qxqe = uakvf__iybbs
        parfor = None
        if stn__qxqe != -1:
            parfor = lcbm__eezlt[stn__qxqe]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = lcbm__eezlt[:stn__qxqe] + parfor.init_block.body
        eval_nodes = lcbm__eezlt[stn__qxqe + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for cnf__ici in init_nodes:
            if is_assign(cnf__ici) and cnf__ici.target.name in redvars:
                ind = redvars.index(cnf__ici.target.name)
                reduce_vars[ind] = cnf__ici.target
        var_types = [pm.typemap[lsux__mrcu] for lsux__mrcu in redvars]
        lus__rdc = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        folkw__rsv = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        qixwn__cdx = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(qixwn__cdx)
        self.all_update_funcs.append(folkw__rsv)
        self.all_combine_funcs.append(lus__rdc)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        aabd__iec = gen_init_func(self.all_init_nodes, self.all_reduce_vars,
            self.all_vartypes, self.typingctx, self.targetctx)
        vnnrv__hegn = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        ohrqw__jxkp = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        ijzne__geoa = gen_all_eval_func(self.all_eval_funcs, self.
            all_vartypes, self.redvar_offsets, self.out_col_types, self.
            typingctx, self.targetctx, self.pivot_values)
        return (self.all_vartypes, aabd__iec, vnnrv__hegn, ohrqw__jxkp,
            ijzne__geoa)


class GeneralUDFGenerator(object):

    def __init__(self):
        self.funcs = []

    def add_udf(self, func):
        self.funcs.append(bodo.jit(distributed=False)(func))
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        func.n_redvars = 0

    def gen_all_func(self):
        if len(self.funcs) > 0:
            return self.funcs
        else:
            return None


def get_udf_func_struct(agg_func, input_has_index, in_col_types,
    out_col_types, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab):
    if is_crosstab and len(in_col_types) == 0:
        in_col_types = [types.Array(types.intp, 1, 'C')]
    ixcj__qqar = []
    for t, lnoot__tebuf in zip(in_col_types, agg_func):
        ixcj__qqar.append((t, lnoot__tebuf))
    qxtx__fbp = RegularUDFGenerator(in_col_types, out_col_types, pivot_typ,
        pivot_values, is_crosstab, typingctx, targetctx)
    qut__rwoy = GeneralUDFGenerator()
    for in_col_typ, func in ixcj__qqar:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            qxtx__fbp.add_udf(in_col_typ, func)
        except:
            qut__rwoy.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = qxtx__fbp.gen_all_func()
    general_udf_funcs = qut__rwoy.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    ukorv__fnibb = compute_use_defs(parfor.loop_body)
    aaaa__holva = set()
    for nbltq__mmyq in ukorv__fnibb.usemap.values():
        aaaa__holva |= nbltq__mmyq
    yhc__zfg = set()
    for nbltq__mmyq in ukorv__fnibb.defmap.values():
        yhc__zfg |= nbltq__mmyq
    jxmrq__gyegp = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    jxmrq__gyegp.body = eval_nodes
    zbs__btv = compute_use_defs({(0): jxmrq__gyegp})
    ytvk__kha = zbs__btv.usemap[0]
    vwkrk__anv = set()
    gosxu__lrkt = []
    wqgaw__owvw = []
    for cnf__ici in reversed(init_nodes):
        iebh__umtwu = {lsux__mrcu.name for lsux__mrcu in cnf__ici.list_vars()}
        if is_assign(cnf__ici):
            lsux__mrcu = cnf__ici.target.name
            iebh__umtwu.remove(lsux__mrcu)
            if (lsux__mrcu in aaaa__holva and lsux__mrcu not in vwkrk__anv and
                lsux__mrcu not in ytvk__kha and lsux__mrcu not in yhc__zfg):
                wqgaw__owvw.append(cnf__ici)
                aaaa__holva |= iebh__umtwu
                yhc__zfg.add(lsux__mrcu)
                continue
        vwkrk__anv |= iebh__umtwu
        gosxu__lrkt.append(cnf__ici)
    wqgaw__owvw.reverse()
    gosxu__lrkt.reverse()
    obdhv__yimg = min(parfor.loop_body.keys())
    gkzu__szoa = parfor.loop_body[obdhv__yimg]
    gkzu__szoa.body = wqgaw__owvw + gkzu__szoa.body
    return gosxu__lrkt


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    qemwb__uoke = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    dqpq__ogcm = set()
    argzj__pian = []
    for cnf__ici in init_nodes:
        if is_assign(cnf__ici) and isinstance(cnf__ici.value, ir.Global
            ) and isinstance(cnf__ici.value.value, pytypes.FunctionType
            ) and cnf__ici.value.value in qemwb__uoke:
            dqpq__ogcm.add(cnf__ici.target.name)
        elif is_call_assign(cnf__ici
            ) and cnf__ici.value.func.name in dqpq__ogcm:
            pass
        else:
            argzj__pian.append(cnf__ici)
    init_nodes = argzj__pian
    xlwd__tfp = types.Tuple(var_types)
    ipkpy__wclf = lambda : None
    f_ir = compile_to_numba_ir(ipkpy__wclf, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    wpa__viyjj = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    oivu__ldu = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc), wpa__viyjj,
        loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [oivu__ldu] + block.body
    block.body[-2].value.value = wpa__viyjj
    qpy__jrfzl = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        xlwd__tfp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    cele__jqv = numba.core.target_extension.dispatcher_registry[cpu_target](
        ipkpy__wclf)
    cele__jqv.add_overload(qpy__jrfzl)
    return cele__jqv


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    sjvr__urkd = len(update_funcs)
    sxpts__whfl = len(in_col_types)
    if pivot_values is not None:
        assert sxpts__whfl == 1
    ctu__ryr = 'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n'
    if pivot_values is not None:
        ttkv__riqb = redvar_offsets[sxpts__whfl]
        ctu__ryr += '  pv = pivot_arr[i]\n'
        for kbi__xev, dlnh__lapsi in enumerate(pivot_values):
            uanh__aaf = 'el' if kbi__xev != 0 else ''
            ctu__ryr += "  {}if pv == '{}':\n".format(uanh__aaf, dlnh__lapsi)
            bfu__iuwhu = ttkv__riqb * kbi__xev
            rvnk__sad = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                uakvf__iybbs) for uakvf__iybbs in range(bfu__iuwhu +
                redvar_offsets[0], bfu__iuwhu + redvar_offsets[1])])
            wjkp__rggdf = 'data_in[0][i]'
            if is_crosstab:
                wjkp__rggdf = '0'
            ctu__ryr += '    {} = update_vars_0({}, {})\n'.format(rvnk__sad,
                rvnk__sad, wjkp__rggdf)
    else:
        for kbi__xev in range(sjvr__urkd):
            rvnk__sad = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                uakvf__iybbs) for uakvf__iybbs in range(redvar_offsets[
                kbi__xev], redvar_offsets[kbi__xev + 1])])
            if rvnk__sad:
                ctu__ryr += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(rvnk__sad, kbi__xev, rvnk__sad, 0 if 
                    sxpts__whfl == 1 else kbi__xev))
    ctu__ryr += '  return\n'
    vkoz__wupbi = {}
    for uakvf__iybbs, lnoot__tebuf in enumerate(update_funcs):
        vkoz__wupbi['update_vars_{}'.format(uakvf__iybbs)] = lnoot__tebuf
    hsqff__hid = {}
    exec(ctu__ryr, vkoz__wupbi, hsqff__hid)
    pmcti__oduyv = hsqff__hid['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(pmcti__oduyv)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    nqdny__gim = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    arg_typs = nqdny__gim, nqdny__gim, types.intp, types.intp, pivot_typ
    sgeb__ogiq = len(redvar_offsets) - 1
    ttkv__riqb = redvar_offsets[sgeb__ogiq]
    ctu__ryr = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert sgeb__ogiq == 1
        for gpjtq__eygt in range(len(pivot_values)):
            bfu__iuwhu = ttkv__riqb * gpjtq__eygt
            rvnk__sad = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                uakvf__iybbs) for uakvf__iybbs in range(bfu__iuwhu +
                redvar_offsets[0], bfu__iuwhu + redvar_offsets[1])])
            hili__qaud = ', '.join(['recv_arrs[{}][i]'.format(uakvf__iybbs) for
                uakvf__iybbs in range(bfu__iuwhu + redvar_offsets[0], 
                bfu__iuwhu + redvar_offsets[1])])
            ctu__ryr += '  {} = combine_vars_0({}, {})\n'.format(rvnk__sad,
                rvnk__sad, hili__qaud)
    else:
        for kbi__xev in range(sgeb__ogiq):
            rvnk__sad = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                uakvf__iybbs) for uakvf__iybbs in range(redvar_offsets[
                kbi__xev], redvar_offsets[kbi__xev + 1])])
            hili__qaud = ', '.join(['recv_arrs[{}][i]'.format(uakvf__iybbs) for
                uakvf__iybbs in range(redvar_offsets[kbi__xev],
                redvar_offsets[kbi__xev + 1])])
            if hili__qaud:
                ctu__ryr += '  {} = combine_vars_{}({}, {})\n'.format(rvnk__sad
                    , kbi__xev, rvnk__sad, hili__qaud)
    ctu__ryr += '  return\n'
    vkoz__wupbi = {}
    for uakvf__iybbs, lnoot__tebuf in enumerate(combine_funcs):
        vkoz__wupbi['combine_vars_{}'.format(uakvf__iybbs)] = lnoot__tebuf
    hsqff__hid = {}
    exec(ctu__ryr, vkoz__wupbi, hsqff__hid)
    wvwht__fnanj = hsqff__hid['combine_all_f']
    f_ir = compile_to_numba_ir(wvwht__fnanj, vkoz__wupbi)
    ohrqw__jxkp = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    cele__jqv = numba.core.target_extension.dispatcher_registry[cpu_target](
        wvwht__fnanj)
    cele__jqv.add_overload(ohrqw__jxkp)
    return cele__jqv


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    nqdny__gim = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types]
        )
    out_col_typs = types.Tuple(out_col_typs)
    sgeb__ogiq = len(redvar_offsets) - 1
    ttkv__riqb = redvar_offsets[sgeb__ogiq]
    ctu__ryr = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert sgeb__ogiq == 1
        for kbi__xev in range(len(pivot_values)):
            bfu__iuwhu = ttkv__riqb * kbi__xev
            rvnk__sad = ', '.join(['redvar_arrs[{}][j]'.format(uakvf__iybbs
                ) for uakvf__iybbs in range(bfu__iuwhu + redvar_offsets[0],
                bfu__iuwhu + redvar_offsets[1])])
            ctu__ryr += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(kbi__xev
                , rvnk__sad)
    else:
        for kbi__xev in range(sgeb__ogiq):
            rvnk__sad = ', '.join(['redvar_arrs[{}][j]'.format(uakvf__iybbs
                ) for uakvf__iybbs in range(redvar_offsets[kbi__xev],
                redvar_offsets[kbi__xev + 1])])
            ctu__ryr += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                kbi__xev, kbi__xev, rvnk__sad)
    ctu__ryr += '  return\n'
    vkoz__wupbi = {}
    for uakvf__iybbs, lnoot__tebuf in enumerate(eval_funcs):
        vkoz__wupbi['eval_vars_{}'.format(uakvf__iybbs)] = lnoot__tebuf
    hsqff__hid = {}
    exec(ctu__ryr, vkoz__wupbi, hsqff__hid)
    khp__dtgad = hsqff__hid['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(khp__dtgad)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    tzzx__qrzfh = len(var_types)
    lfow__nchix = [f'in{uakvf__iybbs}' for uakvf__iybbs in range(tzzx__qrzfh)]
    xlwd__tfp = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    dmij__qgg = xlwd__tfp(0)
    ctu__ryr = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        lfow__nchix))
    hsqff__hid = {}
    exec(ctu__ryr, {'_zero': dmij__qgg}, hsqff__hid)
    rxeb__mxdpc = hsqff__hid['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(rxeb__mxdpc, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': dmij__qgg}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    fbw__auts = []
    for uakvf__iybbs, lsux__mrcu in enumerate(reduce_vars):
        fbw__auts.append(ir.Assign(block.body[uakvf__iybbs].target,
            lsux__mrcu, lsux__mrcu.loc))
        for sghbo__cpixp in lsux__mrcu.versioned_names:
            fbw__auts.append(ir.Assign(lsux__mrcu, ir.Var(lsux__mrcu.scope,
                sghbo__cpixp, lsux__mrcu.loc), lsux__mrcu.loc))
    block.body = block.body[:tzzx__qrzfh] + fbw__auts + eval_nodes
    qixwn__cdx = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        xlwd__tfp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    cele__jqv = numba.core.target_extension.dispatcher_registry[cpu_target](
        rxeb__mxdpc)
    cele__jqv.add_overload(qixwn__cdx)
    return cele__jqv


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    tzzx__qrzfh = len(redvars)
    jeua__dujua = [f'v{uakvf__iybbs}' for uakvf__iybbs in range(tzzx__qrzfh)]
    lfow__nchix = [f'in{uakvf__iybbs}' for uakvf__iybbs in range(tzzx__qrzfh)]
    ctu__ryr = 'def agg_combine({}):\n'.format(', '.join(jeua__dujua +
        lfow__nchix))
    socw__trwff = wrap_parfor_blocks(parfor)
    aihr__kebi = find_topo_order(socw__trwff)
    aihr__kebi = aihr__kebi[1:]
    unwrap_parfor_blocks(parfor)
    hxxp__fpwis = {}
    hossg__lbdh = []
    for xmqk__cdvw in aihr__kebi:
        aoh__mqab = parfor.loop_body[xmqk__cdvw]
        for cnf__ici in aoh__mqab.body:
            if is_call_assign(cnf__ici) and guard(find_callname, f_ir,
                cnf__ici.value) == ('__special_combine', 'bodo.ir.aggregate'):
                args = cnf__ici.value.args
                whktv__hex = []
                sutd__cuiab = []
                for lsux__mrcu in args[:-1]:
                    ind = redvars.index(lsux__mrcu.name)
                    hossg__lbdh.append(ind)
                    whktv__hex.append('v{}'.format(ind))
                    sutd__cuiab.append('in{}'.format(ind))
                lvy__ksf = '__special_combine__{}'.format(len(hxxp__fpwis))
                ctu__ryr += '    ({},) = {}({})\n'.format(', '.join(
                    whktv__hex), lvy__ksf, ', '.join(whktv__hex + sutd__cuiab))
                camk__flgl = ir.Expr.call(args[-1], [], (), aoh__mqab.loc)
                wjo__rtg = guard(find_callname, f_ir, camk__flgl)
                assert wjo__rtg == ('_var_combine', 'bodo.ir.aggregate')
                wjo__rtg = bodo.ir.aggregate._var_combine
                hxxp__fpwis[lvy__ksf] = wjo__rtg
            if is_assign(cnf__ici) and cnf__ici.target.name in redvars:
                zuk__jcyo = cnf__ici.target.name
                ind = redvars.index(zuk__jcyo)
                if ind in hossg__lbdh:
                    continue
                if len(f_ir._definitions[zuk__jcyo]) == 2:
                    var_def = f_ir._definitions[zuk__jcyo][0]
                    ctu__ryr += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[zuk__jcyo][1]
                    ctu__ryr += _match_reduce_def(var_def, f_ir, ind)
    ctu__ryr += '    return {}'.format(', '.join(['v{}'.format(uakvf__iybbs
        ) for uakvf__iybbs in range(tzzx__qrzfh)]))
    hsqff__hid = {}
    exec(ctu__ryr, {}, hsqff__hid)
    vfhw__vxjpm = hsqff__hid['agg_combine']
    arg_typs = tuple(2 * var_types)
    vkoz__wupbi = {'numba': numba, 'bodo': bodo, 'np': np}
    vkoz__wupbi.update(hxxp__fpwis)
    f_ir = compile_to_numba_ir(vfhw__vxjpm, vkoz__wupbi, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=pm.
        typemap, calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    xlwd__tfp = pm.typemap[block.body[-1].value.name]
    lus__rdc = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        xlwd__tfp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    cele__jqv = numba.core.target_extension.dispatcher_registry[cpu_target](
        vfhw__vxjpm)
    cele__jqv.add_overload(lus__rdc)
    return cele__jqv


def _match_reduce_def(var_def, f_ir, ind):
    ctu__ryr = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        ctu__ryr = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        sci__prqm = guard(find_callname, f_ir, var_def)
        if sci__prqm == ('min', 'builtins'):
            ctu__ryr = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if sci__prqm == ('max', 'builtins'):
            ctu__ryr = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return ctu__ryr


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    tzzx__qrzfh = len(redvars)
    avyj__upe = 1
    rdln__earc = []
    for uakvf__iybbs in range(avyj__upe):
        btt__ais = ir.Var(arr_var.scope, f'$input{uakvf__iybbs}', arr_var.loc)
        rdln__earc.append(btt__ais)
    uznlj__dqhgw = parfor.loop_nests[0].index_variable
    xzqw__ray = [0] * tzzx__qrzfh
    for aoh__mqab in parfor.loop_body.values():
        uctuo__tksz = []
        for cnf__ici in aoh__mqab.body:
            if is_var_assign(cnf__ici
                ) and cnf__ici.value.name == uznlj__dqhgw.name:
                continue
            if is_getitem(cnf__ici
                ) and cnf__ici.value.value.name == arr_var.name:
                cnf__ici.value = rdln__earc[0]
            if is_call_assign(cnf__ici) and guard(find_callname, pm.func_ir,
                cnf__ici.value) == ('isna', 'bodo.libs.array_kernels'
                ) and cnf__ici.value.args[0].name == arr_var.name:
                cnf__ici.value = ir.Const(False, cnf__ici.target.loc)
            if is_assign(cnf__ici) and cnf__ici.target.name in redvars:
                ind = redvars.index(cnf__ici.target.name)
                xzqw__ray[ind] = cnf__ici.target
            uctuo__tksz.append(cnf__ici)
        aoh__mqab.body = uctuo__tksz
    jeua__dujua = ['v{}'.format(uakvf__iybbs) for uakvf__iybbs in range(
        tzzx__qrzfh)]
    lfow__nchix = ['in{}'.format(uakvf__iybbs) for uakvf__iybbs in range(
        avyj__upe)]
    ctu__ryr = 'def agg_update({}):\n'.format(', '.join(jeua__dujua +
        lfow__nchix))
    ctu__ryr += '    __update_redvars()\n'
    ctu__ryr += '    return {}'.format(', '.join(['v{}'.format(uakvf__iybbs
        ) for uakvf__iybbs in range(tzzx__qrzfh)]))
    hsqff__hid = {}
    exec(ctu__ryr, {}, hsqff__hid)
    ennaf__wjvrk = hsqff__hid['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * avyj__upe)
    f_ir = compile_to_numba_ir(ennaf__wjvrk, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    onrgi__ufrrs = f_ir.blocks.popitem()[1].body
    xlwd__tfp = pm.typemap[onrgi__ufrrs[-1].value.name]
    socw__trwff = wrap_parfor_blocks(parfor)
    aihr__kebi = find_topo_order(socw__trwff)
    aihr__kebi = aihr__kebi[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    gkzu__szoa = f_ir.blocks[aihr__kebi[0]]
    qnb__oewik = f_ir.blocks[aihr__kebi[-1]]
    kyc__jrj = onrgi__ufrrs[:tzzx__qrzfh + avyj__upe]
    if tzzx__qrzfh > 1:
        xuy__ham = onrgi__ufrrs[-3:]
        assert is_assign(xuy__ham[0]) and isinstance(xuy__ham[0].value, ir.Expr
            ) and xuy__ham[0].value.op == 'build_tuple'
    else:
        xuy__ham = onrgi__ufrrs[-2:]
    for uakvf__iybbs in range(tzzx__qrzfh):
        rcmc__eehb = onrgi__ufrrs[uakvf__iybbs].target
        spr__hhm = ir.Assign(rcmc__eehb, xzqw__ray[uakvf__iybbs],
            rcmc__eehb.loc)
        kyc__jrj.append(spr__hhm)
    for uakvf__iybbs in range(tzzx__qrzfh, tzzx__qrzfh + avyj__upe):
        rcmc__eehb = onrgi__ufrrs[uakvf__iybbs].target
        spr__hhm = ir.Assign(rcmc__eehb, rdln__earc[uakvf__iybbs -
            tzzx__qrzfh], rcmc__eehb.loc)
        kyc__jrj.append(spr__hhm)
    gkzu__szoa.body = kyc__jrj + gkzu__szoa.body
    jjgg__gcb = []
    for uakvf__iybbs in range(tzzx__qrzfh):
        rcmc__eehb = onrgi__ufrrs[uakvf__iybbs].target
        spr__hhm = ir.Assign(xzqw__ray[uakvf__iybbs], rcmc__eehb,
            rcmc__eehb.loc)
        jjgg__gcb.append(spr__hhm)
    qnb__oewik.body += jjgg__gcb + xuy__ham
    zod__nppdg = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        xlwd__tfp, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    cele__jqv = numba.core.target_extension.dispatcher_registry[cpu_target](
        ennaf__wjvrk)
    cele__jqv.add_overload(zod__nppdg)
    return cele__jqv


def _rm_arg_agg_block(block, typemap):
    lcbm__eezlt = []
    arr_var = None
    for uakvf__iybbs, cnf__ici in enumerate(block.body):
        if is_assign(cnf__ici) and isinstance(cnf__ici.value, ir.Arg):
            arr_var = cnf__ici.target
            hzj__dtgf = typemap[arr_var.name]
            if not isinstance(hzj__dtgf, types.ArrayCompatible):
                lcbm__eezlt += block.body[uakvf__iybbs + 1:]
                break
            djll__vfwe = block.body[uakvf__iybbs + 1]
            assert is_assign(djll__vfwe) and isinstance(djll__vfwe.value,
                ir.Expr
                ) and djll__vfwe.value.op == 'getattr' and djll__vfwe.value.attr == 'shape' and djll__vfwe.value.value.name == arr_var.name
            fjtya__jqy = djll__vfwe.target
            zeegf__rfjgo = block.body[uakvf__iybbs + 2]
            assert is_assign(zeegf__rfjgo) and isinstance(zeegf__rfjgo.
                value, ir.Expr
                ) and zeegf__rfjgo.value.op == 'static_getitem' and zeegf__rfjgo.value.value.name == fjtya__jqy.name
            lcbm__eezlt += block.body[uakvf__iybbs + 3:]
            break
        lcbm__eezlt.append(cnf__ici)
    return lcbm__eezlt, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    socw__trwff = wrap_parfor_blocks(parfor)
    aihr__kebi = find_topo_order(socw__trwff)
    aihr__kebi = aihr__kebi[1:]
    unwrap_parfor_blocks(parfor)
    for xmqk__cdvw in reversed(aihr__kebi):
        for cnf__ici in reversed(parfor.loop_body[xmqk__cdvw].body):
            if isinstance(cnf__ici, ir.Assign) and (cnf__ici.target.name in
                parfor_params or cnf__ici.target.name in var_to_param):
                iwzlz__hrzsc = cnf__ici.target.name
                rhs = cnf__ici.value
                urjkb__kdw = (iwzlz__hrzsc if iwzlz__hrzsc in parfor_params
                     else var_to_param[iwzlz__hrzsc])
                fit__sqjfz = []
                if isinstance(rhs, ir.Var):
                    fit__sqjfz = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    fit__sqjfz = [lsux__mrcu.name for lsux__mrcu in
                        cnf__ici.value.list_vars()]
                param_uses[urjkb__kdw].extend(fit__sqjfz)
                for lsux__mrcu in fit__sqjfz:
                    var_to_param[lsux__mrcu] = urjkb__kdw
            if isinstance(cnf__ici, Parfor):
                get_parfor_reductions(cnf__ici, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for gytb__lgn, fit__sqjfz in param_uses.items():
        if gytb__lgn in fit__sqjfz and gytb__lgn not in reduce_varnames:
            reduce_varnames.append(gytb__lgn)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
