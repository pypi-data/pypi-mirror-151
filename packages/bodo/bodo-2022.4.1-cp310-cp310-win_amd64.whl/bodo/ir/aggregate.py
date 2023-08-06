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
            mifvt__vsji = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            egk__vja = cgutils.get_or_insert_function(builder.module,
                mifvt__vsji, sym._literal_value)
            builder.call(egk__vja, [context.get_constant_null(sig.args[0])])
        elif sig == types.none(types.int64, types.voidptr, types.voidptr):
            mifvt__vsji = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            egk__vja = cgutils.get_or_insert_function(builder.module,
                mifvt__vsji, sym._literal_value)
            builder.call(egk__vja, [context.get_constant(types.int64, 0),
                context.get_constant_null(sig.args[1]), context.
                get_constant_null(sig.args[2])])
        else:
            mifvt__vsji = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            egk__vja = cgutils.get_or_insert_function(builder.module,
                mifvt__vsji, sym._literal_value)
            builder.call(egk__vja, [context.get_constant_null(sig.args[0]),
                context.get_constant_null(sig.args[1]), context.
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
        pkiy__mda = True
        wgo__dsq = 1
        gxzt__rue = -1
        if isinstance(rhs, ir.Expr):
            for vvgp__hhkzt in rhs.kws:
                if func_name in list_cumulative:
                    if vvgp__hhkzt[0] == 'skipna':
                        pkiy__mda = guard(find_const, func_ir, vvgp__hhkzt[1])
                        if not isinstance(pkiy__mda, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if vvgp__hhkzt[0] == 'dropna':
                        pkiy__mda = guard(find_const, func_ir, vvgp__hhkzt[1])
                        if not isinstance(pkiy__mda, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            wgo__dsq = get_call_expr_arg('shift', rhs.args, dict(rhs.kws), 
                0, 'periods', wgo__dsq)
            wgo__dsq = guard(find_const, func_ir, wgo__dsq)
        if func_name == 'head':
            gxzt__rue = get_call_expr_arg('head', rhs.args, dict(rhs.kws), 
                0, 'n', 5)
            if not isinstance(gxzt__rue, int):
                gxzt__rue = guard(find_const, func_ir, gxzt__rue)
            if gxzt__rue < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = pkiy__mda
        func.periods = wgo__dsq
        func.head_n = gxzt__rue
        if func_name == 'transform':
            kws = dict(rhs.kws)
            qxqp__anjwb = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            dgij__otru = typemap[qxqp__anjwb.name]
            lua__fpgmo = None
            if isinstance(dgij__otru, str):
                lua__fpgmo = dgij__otru
            elif is_overload_constant_str(dgij__otru):
                lua__fpgmo = get_overload_const_str(dgij__otru)
            elif bodo.utils.typing.is_builtin_function(dgij__otru):
                lua__fpgmo = bodo.utils.typing.get_builtin_function_name(
                    dgij__otru)
            if lua__fpgmo not in bodo.ir.aggregate.supported_transform_funcs[:
                ]:
                raise BodoError(f'unsupported transform function {lua__fpgmo}')
            func.transform_func = supported_agg_funcs.index(lua__fpgmo)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    qxqp__anjwb = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if qxqp__anjwb == '':
        dgij__otru = types.none
    else:
        dgij__otru = typemap[qxqp__anjwb.name]
    if is_overload_constant_dict(dgij__otru):
        hub__yxhgw = get_overload_constant_dict(dgij__otru)
        qlugl__tnnp = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in hub__yxhgw.values()]
        return qlugl__tnnp
    if dgij__otru == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(dgij__otru, types.BaseTuple):
        qlugl__tnnp = []
        oxyqi__wbhc = 0
        for t in dgij__otru.types:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                qlugl__tnnp.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>':
                    func.fname = '<lambda_' + str(oxyqi__wbhc) + '>'
                    oxyqi__wbhc += 1
                qlugl__tnnp.append(func)
        return [qlugl__tnnp]
    if is_overload_constant_str(dgij__otru):
        func_name = get_overload_const_str(dgij__otru)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(dgij__otru):
        func_name = bodo.utils.typing.get_builtin_function_name(dgij__otru)
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
        oxyqi__wbhc = 0
        mkl__zpsjr = []
        for hfq__tcof in f_val:
            func = get_agg_func_udf(func_ir, hfq__tcof, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{oxyqi__wbhc}>'
                oxyqi__wbhc += 1
            mkl__zpsjr.append(func)
        return mkl__zpsjr
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
    lua__fpgmo = code.co_name
    return lua__fpgmo


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
            szflp__fmww = types.DType(args[0])
            return signature(szflp__fmww, *args)


@numba.njit(no_cpython_wrapper=True)
def _var_combine(ssqdm_a, mean_a, nobs_a, ssqdm_b, mean_b, nobs_b):
    kklsf__tbzoy = nobs_a + nobs_b
    xar__bbijx = (nobs_a * mean_a + nobs_b * mean_b) / kklsf__tbzoy
    wbeiq__ekwp = mean_b - mean_a
    hzxgu__mwwj = (ssqdm_a + ssqdm_b + wbeiq__ekwp * wbeiq__ekwp * nobs_a *
        nobs_b / kklsf__tbzoy)
    return hzxgu__mwwj, xar__bbijx, kklsf__tbzoy


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
        wzfdr__vwvj = ''
        for jcbru__rnm, xeqje__khll in self.df_out_vars.items():
            wzfdr__vwvj += "'{}':{}, ".format(jcbru__rnm, xeqje__khll.name)
        hnwez__cuyj = '{}{{{}}}'.format(self.df_out, wzfdr__vwvj)
        whx__fjjr = ''
        for jcbru__rnm, xeqje__khll in self.df_in_vars.items():
            whx__fjjr += "'{}':{}, ".format(jcbru__rnm, xeqje__khll.name)
        ptgur__dgq = '{}{{{}}}'.format(self.df_in, whx__fjjr)
        emqp__uoo = 'pivot {}:{}'.format(self.pivot_arr.name, self.pivot_values
            ) if self.pivot_arr is not None else ''
        key_names = ','.join(self.key_names)
        ksf__thkxv = ','.join([xeqje__khll.name for xeqje__khll in self.
            key_arrs])
        return 'aggregate: {} = {} [key: {}:{}] {}'.format(hnwez__cuyj,
            ptgur__dgq, key_names, ksf__thkxv, emqp__uoo)

    def remove_out_col(self, out_col_name):
        self.df_out_vars.pop(out_col_name)
        gjuht__kqe, vmy__dnmvo = self.gb_info_out.pop(out_col_name)
        if gjuht__kqe is None and not self.is_crosstab:
            return
        yzcjp__ouk = self.gb_info_in[gjuht__kqe]
        if self.pivot_arr is not None:
            self.pivot_values.remove(out_col_name)
            for thj__rrz, (func, wzfdr__vwvj) in enumerate(yzcjp__ouk):
                try:
                    wzfdr__vwvj.remove(out_col_name)
                    if len(wzfdr__vwvj) == 0:
                        yzcjp__ouk.pop(thj__rrz)
                        break
                except ValueError as bkic__dim:
                    continue
        else:
            for thj__rrz, (func, bldo__jho) in enumerate(yzcjp__ouk):
                if bldo__jho == out_col_name:
                    yzcjp__ouk.pop(thj__rrz)
                    break
        if len(yzcjp__ouk) == 0:
            self.gb_info_in.pop(gjuht__kqe)
            self.df_in_vars.pop(gjuht__kqe)


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({xeqje__khll.name for xeqje__khll in aggregate_node.
        key_arrs})
    use_set.update({xeqje__khll.name for xeqje__khll in aggregate_node.
        df_in_vars.values()})
    if aggregate_node.pivot_arr is not None:
        use_set.add(aggregate_node.pivot_arr.name)
    def_set.update({xeqje__khll.name for xeqje__khll in aggregate_node.
        df_out_vars.values()})
    if aggregate_node.out_key_vars is not None:
        def_set.update({xeqje__khll.name for xeqje__khll in aggregate_node.
            out_key_vars})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(aggregate_node, lives_no_aliases, lives,
    arg_aliases, alias_map, func_ir, typemap):
    wyr__qegy = [agqk__plv for agqk__plv, zsncd__jvqk in aggregate_node.
        df_out_vars.items() if zsncd__jvqk.name not in lives]
    for viquv__filnx in wyr__qegy:
        aggregate_node.remove_out_col(viquv__filnx)
    out_key_vars = aggregate_node.out_key_vars
    if out_key_vars is not None and all(xeqje__khll.name not in lives for
        xeqje__khll in out_key_vars):
        aggregate_node.out_key_vars = None
    if len(aggregate_node.df_out_vars
        ) == 0 and aggregate_node.out_key_vars is None:
        return None
    return aggregate_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    tymxl__wfr = set(xeqje__khll.name for xeqje__khll in aggregate_node.
        df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        tymxl__wfr.update({xeqje__khll.name for xeqje__khll in
            aggregate_node.out_key_vars})
    return set(), tymxl__wfr


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for thj__rrz in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[thj__rrz] = replace_vars_inner(aggregate_node
            .key_arrs[thj__rrz], var_dict)
    for agqk__plv in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[agqk__plv] = replace_vars_inner(
            aggregate_node.df_in_vars[agqk__plv], var_dict)
    for agqk__plv in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[agqk__plv] = replace_vars_inner(
            aggregate_node.df_out_vars[agqk__plv], var_dict)
    if aggregate_node.out_key_vars is not None:
        for thj__rrz in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[thj__rrz] = replace_vars_inner(
                aggregate_node.out_key_vars[thj__rrz], var_dict)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = replace_vars_inner(aggregate_node.
            pivot_arr, var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    if debug_prints():
        print('visiting aggregate vars for:', aggregate_node)
        print('cbdata: ', sorted(cbdata.items()))
    for thj__rrz in range(len(aggregate_node.key_arrs)):
        aggregate_node.key_arrs[thj__rrz] = visit_vars_inner(aggregate_node
            .key_arrs[thj__rrz], callback, cbdata)
    for agqk__plv in list(aggregate_node.df_in_vars.keys()):
        aggregate_node.df_in_vars[agqk__plv] = visit_vars_inner(aggregate_node
            .df_in_vars[agqk__plv], callback, cbdata)
    for agqk__plv in list(aggregate_node.df_out_vars.keys()):
        aggregate_node.df_out_vars[agqk__plv] = visit_vars_inner(aggregate_node
            .df_out_vars[agqk__plv], callback, cbdata)
    if aggregate_node.out_key_vars is not None:
        for thj__rrz in range(len(aggregate_node.out_key_vars)):
            aggregate_node.out_key_vars[thj__rrz] = visit_vars_inner(
                aggregate_node.out_key_vars[thj__rrz], callback, cbdata)
    if aggregate_node.pivot_arr is not None:
        aggregate_node.pivot_arr = visit_vars_inner(aggregate_node.
            pivot_arr, callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    assert len(aggregate_node.df_out_vars
        ) > 0 or aggregate_node.out_key_vars is not None or aggregate_node.is_crosstab, 'empty aggregate in array analysis'
    pfo__lusev = []
    for oep__lus in aggregate_node.key_arrs:
        hzu__rkl = equiv_set.get_shape(oep__lus)
        if hzu__rkl:
            pfo__lusev.append(hzu__rkl[0])
    if aggregate_node.pivot_arr is not None:
        hzu__rkl = equiv_set.get_shape(aggregate_node.pivot_arr)
        if hzu__rkl:
            pfo__lusev.append(hzu__rkl[0])
    for zsncd__jvqk in aggregate_node.df_in_vars.values():
        hzu__rkl = equiv_set.get_shape(zsncd__jvqk)
        if hzu__rkl:
            pfo__lusev.append(hzu__rkl[0])
    if len(pfo__lusev) > 1:
        equiv_set.insert_equiv(*pfo__lusev)
    ymvd__dwag = []
    pfo__lusev = []
    gqkyq__bkh = list(aggregate_node.df_out_vars.values())
    if aggregate_node.out_key_vars is not None:
        gqkyq__bkh.extend(aggregate_node.out_key_vars)
    for zsncd__jvqk in gqkyq__bkh:
        lskk__wtzs = typemap[zsncd__jvqk.name]
        mwwxt__becsq = array_analysis._gen_shape_call(equiv_set,
            zsncd__jvqk, lskk__wtzs.ndim, None, ymvd__dwag)
        equiv_set.insert_equiv(zsncd__jvqk, mwwxt__becsq)
        pfo__lusev.append(mwwxt__becsq[0])
        equiv_set.define(zsncd__jvqk, set())
    if len(pfo__lusev) > 1:
        equiv_set.insert_equiv(*pfo__lusev)
    return [], ymvd__dwag


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    tyo__gtj = Distribution.OneD
    for zsncd__jvqk in aggregate_node.df_in_vars.values():
        tyo__gtj = Distribution(min(tyo__gtj.value, array_dists[zsncd__jvqk
            .name].value))
    for oep__lus in aggregate_node.key_arrs:
        tyo__gtj = Distribution(min(tyo__gtj.value, array_dists[oep__lus.
            name].value))
    if aggregate_node.pivot_arr is not None:
        tyo__gtj = Distribution(min(tyo__gtj.value, array_dists[
            aggregate_node.pivot_arr.name].value))
        array_dists[aggregate_node.pivot_arr.name] = tyo__gtj
    for zsncd__jvqk in aggregate_node.df_in_vars.values():
        array_dists[zsncd__jvqk.name] = tyo__gtj
    for oep__lus in aggregate_node.key_arrs:
        array_dists[oep__lus.name] = tyo__gtj
    udsc__xuc = Distribution.OneD_Var
    for zsncd__jvqk in aggregate_node.df_out_vars.values():
        if zsncd__jvqk.name in array_dists:
            udsc__xuc = Distribution(min(udsc__xuc.value, array_dists[
                zsncd__jvqk.name].value))
    if aggregate_node.out_key_vars is not None:
        for zsncd__jvqk in aggregate_node.out_key_vars:
            if zsncd__jvqk.name in array_dists:
                udsc__xuc = Distribution(min(udsc__xuc.value, array_dists[
                    zsncd__jvqk.name].value))
    udsc__xuc = Distribution(min(udsc__xuc.value, tyo__gtj.value))
    for zsncd__jvqk in aggregate_node.df_out_vars.values():
        array_dists[zsncd__jvqk.name] = udsc__xuc
    if aggregate_node.out_key_vars is not None:
        for gus__piw in aggregate_node.out_key_vars:
            array_dists[gus__piw.name] = udsc__xuc
    if udsc__xuc != Distribution.OneD_Var:
        for oep__lus in aggregate_node.key_arrs:
            array_dists[oep__lus.name] = udsc__xuc
        if aggregate_node.pivot_arr is not None:
            array_dists[aggregate_node.pivot_arr.name] = udsc__xuc
        for zsncd__jvqk in aggregate_node.df_in_vars.values():
            array_dists[zsncd__jvqk.name] = udsc__xuc


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for zsncd__jvqk in agg_node.df_out_vars.values():
        definitions[zsncd__jvqk.name].append(agg_node)
    if agg_node.out_key_vars is not None:
        for gus__piw in agg_node.out_key_vars:
            definitions[gus__piw.name].append(agg_node)
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
        for xeqje__khll in (list(agg_node.df_in_vars.values()) + list(
            agg_node.df_out_vars.values()) + agg_node.key_arrs):
            if array_dists[xeqje__khll.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                xeqje__khll.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    vmfg__pilte = tuple(typemap[xeqje__khll.name] for xeqje__khll in
        agg_node.key_arrs)
    jagam__pynt = [xeqje__khll for rxxe__tcjf, xeqje__khll in agg_node.
        df_in_vars.items()]
    qdz__niw = [xeqje__khll for rxxe__tcjf, xeqje__khll in agg_node.
        df_out_vars.items()]
    in_col_typs = []
    qlugl__tnnp = []
    if agg_node.pivot_arr is not None:
        for gjuht__kqe, yzcjp__ouk in agg_node.gb_info_in.items():
            for func, vmy__dnmvo in yzcjp__ouk:
                if gjuht__kqe is not None:
                    in_col_typs.append(typemap[agg_node.df_in_vars[
                        gjuht__kqe].name])
                qlugl__tnnp.append(func)
    else:
        for gjuht__kqe, func in agg_node.gb_info_out.values():
            if gjuht__kqe is not None:
                in_col_typs.append(typemap[agg_node.df_in_vars[gjuht__kqe].
                    name])
            qlugl__tnnp.append(func)
    out_col_typs = tuple(typemap[xeqje__khll.name] for xeqje__khll in qdz__niw)
    pivot_typ = types.none if agg_node.pivot_arr is None else typemap[agg_node
        .pivot_arr.name]
    arg_typs = tuple(vmfg__pilte + tuple(typemap[xeqje__khll.name] for
        xeqje__khll in jagam__pynt) + (pivot_typ,))
    in_col_typs = [to_str_arr_if_dict_array(t) for t in in_col_typs]
    abnjj__yrd = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for thj__rrz, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            abnjj__yrd.update({f'in_cat_dtype_{thj__rrz}': in_col_typ})
    for thj__rrz, skgy__jtb in enumerate(out_col_typs):
        if isinstance(skgy__jtb, bodo.CategoricalArrayType):
            abnjj__yrd.update({f'out_cat_dtype_{thj__rrz}': skgy__jtb})
    udf_func_struct = get_udf_func_struct(qlugl__tnnp, agg_node.
        input_has_index, in_col_typs, out_col_typs, typingctx, targetctx,
        pivot_typ, agg_node.pivot_values, agg_node.is_crosstab)
    sody__qlbb = gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
        parallel, udf_func_struct)
    abnjj__yrd.update({'pd': pd, 'pre_alloc_string_array':
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
            abnjj__yrd.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            abnjj__yrd.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    sir__rlcle = compile_to_numba_ir(sody__qlbb, abnjj__yrd, typingctx=
        typingctx, targetctx=targetctx, arg_typs=arg_typs, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    kxgn__fgls = []
    if agg_node.pivot_arr is None:
        mwfm__vxmvs = agg_node.key_arrs[0].scope
        loc = agg_node.loc
        btqa__rct = ir.Var(mwfm__vxmvs, mk_unique_var('dummy_none'), loc)
        typemap[btqa__rct.name] = types.none
        kxgn__fgls.append(ir.Assign(ir.Const(None, loc), btqa__rct, loc))
        jagam__pynt.append(btqa__rct)
    else:
        jagam__pynt.append(agg_node.pivot_arr)
    replace_arg_nodes(sir__rlcle, agg_node.key_arrs + jagam__pynt)
    bli__yexf = sir__rlcle.body[-3]
    assert is_assign(bli__yexf) and isinstance(bli__yexf.value, ir.Expr
        ) and bli__yexf.value.op == 'build_tuple'
    kxgn__fgls += sir__rlcle.body[:-3]
    gqkyq__bkh = list(agg_node.df_out_vars.values())
    if agg_node.out_key_vars is not None:
        gqkyq__bkh += agg_node.out_key_vars
    for thj__rrz, psq__jnpaq in enumerate(gqkyq__bkh):
        gaya__gqtdp = bli__yexf.value.items[thj__rrz]
        kxgn__fgls.append(ir.Assign(gaya__gqtdp, psq__jnpaq, psq__jnpaq.loc))
    return kxgn__fgls


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def get_numba_set(dtype):
    pass


@infer_global(get_numba_set)
class GetNumbaSetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        gkdk__ycgw = args[0]
        dtype = types.Tuple([t.dtype for t in gkdk__ycgw.types]) if isinstance(
            gkdk__ycgw, types.BaseTuple) else gkdk__ycgw.dtype
        if isinstance(gkdk__ycgw, types.BaseTuple) and len(gkdk__ycgw.types
            ) == 1:
            dtype = gkdk__ycgw.types[0].dtype
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
        svty__rjqz = args[0]
        if svty__rjqz == types.none:
            return signature(types.boolean, *args)


@lower_builtin(bool, types.none)
def lower_column_mean_impl(context, builder, sig, args):
    rlmee__evyak = context.compile_internal(builder, lambda a: False, sig, args
        )
    return rlmee__evyak


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        ipz__tuf = IntDtype(t.dtype).name
        assert ipz__tuf.endswith('Dtype()')
        ipz__tuf = ipz__tuf[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{ipz__tuf}'))"
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
        akyj__lapm = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {akyj__lapm}_cat_dtype_{colnum})')
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
    lsia__npfq = udf_func_struct.var_typs
    ebmzv__ynz = len(lsia__npfq)
    jtjil__xja = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    jtjil__xja += '    if is_null_pointer(in_table):\n'
    jtjil__xja += '        return\n'
    jtjil__xja += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in lsia__npfq]), 
        ',' if len(lsia__npfq) == 1 else '')
    jdovv__tbhv = n_keys
    yba__vmwa = []
    redvar_offsets = []
    byc__gwguz = []
    if do_combine:
        for thj__rrz, hfq__tcof in enumerate(allfuncs):
            if hfq__tcof.ftype != 'udf':
                jdovv__tbhv += hfq__tcof.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(jdovv__tbhv, jdovv__tbhv +
                    hfq__tcof.n_redvars))
                jdovv__tbhv += hfq__tcof.n_redvars
                byc__gwguz.append(data_in_typs_[func_idx_to_in_col[thj__rrz]])
                yba__vmwa.append(func_idx_to_in_col[thj__rrz] + n_keys)
    else:
        for thj__rrz, hfq__tcof in enumerate(allfuncs):
            if hfq__tcof.ftype != 'udf':
                jdovv__tbhv += hfq__tcof.ncols_post_shuffle
            else:
                redvar_offsets += list(range(jdovv__tbhv + 1, jdovv__tbhv +
                    1 + hfq__tcof.n_redvars))
                jdovv__tbhv += hfq__tcof.n_redvars + 1
                byc__gwguz.append(data_in_typs_[func_idx_to_in_col[thj__rrz]])
                yba__vmwa.append(func_idx_to_in_col[thj__rrz] + n_keys)
    assert len(redvar_offsets) == ebmzv__ynz
    rmx__pdrf = len(byc__gwguz)
    klgl__rkayb = []
    for thj__rrz, t in enumerate(byc__gwguz):
        klgl__rkayb.append(_gen_dummy_alloc(t, thj__rrz, True))
    jtjil__xja += '    data_in_dummy = ({}{})\n'.format(','.join(
        klgl__rkayb), ',' if len(byc__gwguz) == 1 else '')
    jtjil__xja += """
    # initialize redvar cols
"""
    jtjil__xja += '    init_vals = __init_func()\n'
    for thj__rrz in range(ebmzv__ynz):
        jtjil__xja += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(thj__rrz, redvar_offsets[thj__rrz], thj__rrz))
        jtjil__xja += '    incref(redvar_arr_{})\n'.format(thj__rrz)
        jtjil__xja += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(thj__rrz
            , thj__rrz)
    jtjil__xja += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(thj__rrz) for thj__rrz in range(ebmzv__ynz)]), ',' if 
        ebmzv__ynz == 1 else '')
    jtjil__xja += '\n'
    for thj__rrz in range(rmx__pdrf):
        jtjil__xja += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(thj__rrz, yba__vmwa[thj__rrz], thj__rrz))
        jtjil__xja += '    incref(data_in_{})\n'.format(thj__rrz)
    jtjil__xja += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(thj__rrz) for thj__rrz in range(rmx__pdrf)]), ',' if 
        rmx__pdrf == 1 else '')
    jtjil__xja += '\n'
    jtjil__xja += '    for i in range(len(data_in_0)):\n'
    jtjil__xja += '        w_ind = row_to_group[i]\n'
    jtjil__xja += '        if w_ind != -1:\n'
    jtjil__xja += (
        '            __update_redvars(redvars, data_in, w_ind, i, pivot_arr=None)\n'
        )
    yexvx__gcb = {}
    exec(jtjil__xja, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yexvx__gcb)
    return yexvx__gcb['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, out_data_typs,
    label_suffix):
    lsia__npfq = udf_func_struct.var_typs
    ebmzv__ynz = len(lsia__npfq)
    jtjil__xja = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    jtjil__xja += '    if is_null_pointer(in_table):\n'
    jtjil__xja += '        return\n'
    jtjil__xja += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in lsia__npfq]), 
        ',' if len(lsia__npfq) == 1 else '')
    ecg__jbj = n_keys
    hlet__bxhgw = n_keys
    zxm__jfo = []
    tzl__bzwhq = []
    for hfq__tcof in allfuncs:
        if hfq__tcof.ftype != 'udf':
            ecg__jbj += hfq__tcof.ncols_pre_shuffle
            hlet__bxhgw += hfq__tcof.ncols_post_shuffle
        else:
            zxm__jfo += list(range(ecg__jbj, ecg__jbj + hfq__tcof.n_redvars))
            tzl__bzwhq += list(range(hlet__bxhgw + 1, hlet__bxhgw + 1 +
                hfq__tcof.n_redvars))
            ecg__jbj += hfq__tcof.n_redvars
            hlet__bxhgw += 1 + hfq__tcof.n_redvars
    assert len(zxm__jfo) == ebmzv__ynz
    jtjil__xja += """
    # initialize redvar cols
"""
    jtjil__xja += '    init_vals = __init_func()\n'
    for thj__rrz in range(ebmzv__ynz):
        jtjil__xja += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(thj__rrz, tzl__bzwhq[thj__rrz], thj__rrz))
        jtjil__xja += '    incref(redvar_arr_{})\n'.format(thj__rrz)
        jtjil__xja += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(thj__rrz
            , thj__rrz)
    jtjil__xja += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(thj__rrz) for thj__rrz in range(ebmzv__ynz)]), ',' if 
        ebmzv__ynz == 1 else '')
    jtjil__xja += '\n'
    for thj__rrz in range(ebmzv__ynz):
        jtjil__xja += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(thj__rrz, zxm__jfo[thj__rrz], thj__rrz))
        jtjil__xja += '    incref(recv_redvar_arr_{})\n'.format(thj__rrz)
    jtjil__xja += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(thj__rrz) for thj__rrz in range(
        ebmzv__ynz)]), ',' if ebmzv__ynz == 1 else '')
    jtjil__xja += '\n'
    if ebmzv__ynz:
        jtjil__xja += '    for i in range(len(recv_redvar_arr_0)):\n'
        jtjil__xja += '        w_ind = row_to_group[i]\n'
        jtjil__xja += """        __combine_redvars(redvars, recv_redvars, w_ind, i, pivot_arr=None)
"""
    yexvx__gcb = {}
    exec(jtjil__xja, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yexvx__gcb)
    return yexvx__gcb['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    lsia__npfq = udf_func_struct.var_typs
    ebmzv__ynz = len(lsia__npfq)
    jdovv__tbhv = n_keys
    redvar_offsets = []
    apow__tfug = []
    out_data_typs = []
    for thj__rrz, hfq__tcof in enumerate(allfuncs):
        if hfq__tcof.ftype != 'udf':
            jdovv__tbhv += hfq__tcof.ncols_post_shuffle
        else:
            apow__tfug.append(jdovv__tbhv)
            redvar_offsets += list(range(jdovv__tbhv + 1, jdovv__tbhv + 1 +
                hfq__tcof.n_redvars))
            jdovv__tbhv += 1 + hfq__tcof.n_redvars
            out_data_typs.append(out_data_typs_[thj__rrz])
    assert len(redvar_offsets) == ebmzv__ynz
    rmx__pdrf = len(out_data_typs)
    jtjil__xja = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    jtjil__xja += '    if is_null_pointer(table):\n'
    jtjil__xja += '        return\n'
    jtjil__xja += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in lsia__npfq]), 
        ',' if len(lsia__npfq) == 1 else '')
    jtjil__xja += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        out_data_typs]), ',' if len(out_data_typs) == 1 else '')
    for thj__rrz in range(ebmzv__ynz):
        jtjil__xja += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(thj__rrz, redvar_offsets[thj__rrz], thj__rrz))
        jtjil__xja += '    incref(redvar_arr_{})\n'.format(thj__rrz)
    jtjil__xja += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'
        .format(thj__rrz) for thj__rrz in range(ebmzv__ynz)]), ',' if 
        ebmzv__ynz == 1 else '')
    jtjil__xja += '\n'
    for thj__rrz in range(rmx__pdrf):
        jtjil__xja += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(thj__rrz, apow__tfug[thj__rrz], thj__rrz))
        jtjil__xja += '    incref(data_out_{})\n'.format(thj__rrz)
    jtjil__xja += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(thj__rrz) for thj__rrz in range(rmx__pdrf)]), ',' if 
        rmx__pdrf == 1 else '')
    jtjil__xja += '\n'
    jtjil__xja += '    for i in range(len(data_out_0)):\n'
    jtjil__xja += '        __eval_res(redvars, data_out, i)\n'
    yexvx__gcb = {}
    exec(jtjil__xja, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, yexvx__gcb)
    return yexvx__gcb['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    jdovv__tbhv = n_keys
    nhv__dkryt = []
    for thj__rrz, hfq__tcof in enumerate(allfuncs):
        if hfq__tcof.ftype == 'gen_udf':
            nhv__dkryt.append(jdovv__tbhv)
            jdovv__tbhv += 1
        elif hfq__tcof.ftype != 'udf':
            jdovv__tbhv += hfq__tcof.ncols_post_shuffle
        else:
            jdovv__tbhv += hfq__tcof.n_redvars + 1
    jtjil__xja = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    jtjil__xja += '    if num_groups == 0:\n'
    jtjil__xja += '        return\n'
    for thj__rrz, func in enumerate(udf_func_struct.general_udf_funcs):
        jtjil__xja += '    # col {}\n'.format(thj__rrz)
        jtjil__xja += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(nhv__dkryt[thj__rrz], thj__rrz))
        jtjil__xja += '    incref(out_col)\n'
        jtjil__xja += '    for j in range(num_groups):\n'
        jtjil__xja += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(thj__rrz, thj__rrz))
        jtjil__xja += '        incref(in_col)\n'
        jtjil__xja += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(thj__rrz))
    abnjj__yrd = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    bmro__ezgg = 0
    for thj__rrz, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[bmro__ezgg]
        abnjj__yrd['func_{}'.format(bmro__ezgg)] = func
        abnjj__yrd['in_col_{}_typ'.format(bmro__ezgg)] = in_col_typs[
            func_idx_to_in_col[thj__rrz]]
        abnjj__yrd['out_col_{}_typ'.format(bmro__ezgg)] = out_col_typs[thj__rrz
            ]
        bmro__ezgg += 1
    yexvx__gcb = {}
    exec(jtjil__xja, abnjj__yrd, yexvx__gcb)
    hfq__tcof = yexvx__gcb['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    xoq__tpwp = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(xoq__tpwp, nopython=True)(hfq__tcof)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs, parallel,
    udf_func_struct):
    tzfdi__omq = agg_node.pivot_arr is not None
    if agg_node.same_index:
        assert agg_node.input_has_index
    if agg_node.pivot_values is None:
        tyolv__gprjy = 1
    else:
        tyolv__gprjy = len(agg_node.pivot_values)
    kdrb__astns = tuple('key_' + sanitize_varname(jcbru__rnm) for
        jcbru__rnm in agg_node.key_names)
    pvu__eopko = {jcbru__rnm: 'in_{}'.format(sanitize_varname(jcbru__rnm)) for
        jcbru__rnm in agg_node.gb_info_in.keys() if jcbru__rnm is not None}
    rjfal__nzj = {jcbru__rnm: ('out_' + sanitize_varname(jcbru__rnm)) for
        jcbru__rnm in agg_node.gb_info_out.keys()}
    n_keys = len(agg_node.key_names)
    qdn__dwwji = ', '.join(kdrb__astns)
    fjzu__nyr = ', '.join(pvu__eopko.values())
    if fjzu__nyr != '':
        fjzu__nyr = ', ' + fjzu__nyr
    jtjil__xja = 'def agg_top({}{}{}, pivot_arr):\n'.format(qdn__dwwji,
        fjzu__nyr, ', index_arg' if agg_node.input_has_index else '')
    for a in (kdrb__astns + tuple(pvu__eopko.values())):
        jtjil__xja += f'    {a} = decode_if_dict_array({a})\n'
    if tzfdi__omq:
        jtjil__xja += f'    pivot_arr = decode_if_dict_array(pivot_arr)\n'
        japh__tjiye = []
        for gjuht__kqe, yzcjp__ouk in agg_node.gb_info_in.items():
            if gjuht__kqe is not None:
                for func, vmy__dnmvo in yzcjp__ouk:
                    japh__tjiye.append(pvu__eopko[gjuht__kqe])
    else:
        japh__tjiye = tuple(pvu__eopko[gjuht__kqe] for gjuht__kqe,
            vmy__dnmvo in agg_node.gb_info_out.values() if gjuht__kqe is not
            None)
    iyag__szxqy = kdrb__astns + tuple(japh__tjiye)
    jtjil__xja += '    info_list = [{}{}{}]\n'.format(', '.join(
        'array_to_info({})'.format(a) for a in iyag__szxqy), 
        ', array_to_info(index_arg)' if agg_node.input_has_index else '', 
        ', array_to_info(pivot_arr)' if agg_node.is_crosstab else '')
    jtjil__xja += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    ioj__msr = []
    func_idx_to_in_col = []
    rkk__kavg = []
    pkiy__mda = False
    waq__bkr = 1
    gxzt__rue = -1
    ojnql__mxy = 0
    ubqr__sfuir = 0
    if not tzfdi__omq:
        qlugl__tnnp = [func for vmy__dnmvo, func in agg_node.gb_info_out.
            values()]
    else:
        qlugl__tnnp = [func for func, vmy__dnmvo in yzcjp__ouk for
            yzcjp__ouk in agg_node.gb_info_in.values()]
    for pgayo__cib, func in enumerate(qlugl__tnnp):
        ioj__msr.append(len(allfuncs))
        if func.ftype in {'median', 'nunique'}:
            do_combine = False
        if func.ftype in list_cumulative:
            ojnql__mxy += 1
        if hasattr(func, 'skipdropna'):
            pkiy__mda = func.skipdropna
        if func.ftype == 'shift':
            waq__bkr = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            ubqr__sfuir = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            gxzt__rue = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(pgayo__cib)
        if func.ftype == 'udf':
            rkk__kavg.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            rkk__kavg.append(0)
            do_combine = False
    ioj__msr.append(len(allfuncs))
    if agg_node.is_crosstab:
        assert len(agg_node.gb_info_out
            ) == tyolv__gprjy, 'invalid number of groupby outputs for pivot'
    else:
        assert len(agg_node.gb_info_out) == len(allfuncs
            ) * tyolv__gprjy, 'invalid number of groupby outputs'
    if ojnql__mxy > 0:
        if ojnql__mxy != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    for thj__rrz, jcbru__rnm in enumerate(agg_node.gb_info_out.keys()):
        hmfg__hxwy = rjfal__nzj[jcbru__rnm] + '_dummy'
        skgy__jtb = out_col_typs[thj__rrz]
        gjuht__kqe, func = agg_node.gb_info_out[jcbru__rnm]
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(skgy__jtb, bodo.CategoricalArrayType
            ):
            jtjil__xja += '    {} = {}\n'.format(hmfg__hxwy, pvu__eopko[
                gjuht__kqe])
        elif udf_func_struct is not None:
            jtjil__xja += '    {} = {}\n'.format(hmfg__hxwy,
                _gen_dummy_alloc(skgy__jtb, thj__rrz, False))
    if udf_func_struct is not None:
        mjudo__zwl = next_label()
        if udf_func_struct.regular_udfs:
            xoq__tpwp = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            jjen__eemc = numba.cfunc(xoq__tpwp, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs,
                out_col_typs, do_combine, func_idx_to_in_col, mjudo__zwl))
            ihizr__uhsn = numba.cfunc(xoq__tpwp, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, out_col_typs, mjudo__zwl))
            hdho__drld = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_col_typs,
                mjudo__zwl))
            udf_func_struct.set_regular_cfuncs(jjen__eemc, ihizr__uhsn,
                hdho__drld)
            for dznj__ygr in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[dznj__ygr.native_name] = dznj__ygr
                gb_agg_cfunc_addr[dznj__ygr.native_name] = dznj__ygr.address
        if udf_func_struct.general_udfs:
            vjngb__xfsl = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, out_col_typs, func_idx_to_in_col,
                mjudo__zwl)
            udf_func_struct.set_general_cfunc(vjngb__xfsl)
        khr__laim = []
        rhimr__flt = 0
        thj__rrz = 0
        for hmfg__hxwy, hfq__tcof in zip(rjfal__nzj.values(), allfuncs):
            if hfq__tcof.ftype in ('udf', 'gen_udf'):
                khr__laim.append(hmfg__hxwy + '_dummy')
                for gqvs__goa in range(rhimr__flt, rhimr__flt + rkk__kavg[
                    thj__rrz]):
                    khr__laim.append('data_redvar_dummy_' + str(gqvs__goa))
                rhimr__flt += rkk__kavg[thj__rrz]
                thj__rrz += 1
        if udf_func_struct.regular_udfs:
            lsia__npfq = udf_func_struct.var_typs
            for thj__rrz, t in enumerate(lsia__npfq):
                jtjil__xja += ('    data_redvar_dummy_{} = np.empty(1, {})\n'
                    .format(thj__rrz, _get_np_dtype(t)))
        jtjil__xja += '    out_info_list_dummy = [{}]\n'.format(', '.join(
            'array_to_info({})'.format(a) for a in khr__laim))
        jtjil__xja += (
            '    udf_table_dummy = arr_info_list_to_table(out_info_list_dummy)\n'
            )
        if udf_func_struct.regular_udfs:
            jtjil__xja += ("    add_agg_cfunc_sym(cpp_cb_update, '{}')\n".
                format(jjen__eemc.native_name))
            jtjil__xja += ("    add_agg_cfunc_sym(cpp_cb_combine, '{}')\n".
                format(ihizr__uhsn.native_name))
            jtjil__xja += "    add_agg_cfunc_sym(cpp_cb_eval, '{}')\n".format(
                hdho__drld.native_name)
            jtjil__xja += ("    cpp_cb_update_addr = get_agg_udf_addr('{}')\n"
                .format(jjen__eemc.native_name))
            jtjil__xja += ("    cpp_cb_combine_addr = get_agg_udf_addr('{}')\n"
                .format(ihizr__uhsn.native_name))
            jtjil__xja += ("    cpp_cb_eval_addr = get_agg_udf_addr('{}')\n"
                .format(hdho__drld.native_name))
        else:
            jtjil__xja += '    cpp_cb_update_addr = 0\n'
            jtjil__xja += '    cpp_cb_combine_addr = 0\n'
            jtjil__xja += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            dznj__ygr = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[dznj__ygr.native_name] = dznj__ygr
            gb_agg_cfunc_addr[dznj__ygr.native_name] = dznj__ygr.address
            jtjil__xja += ("    add_agg_cfunc_sym(cpp_cb_general, '{}')\n".
                format(dznj__ygr.native_name))
            jtjil__xja += ("    cpp_cb_general_addr = get_agg_udf_addr('{}')\n"
                .format(dznj__ygr.native_name))
        else:
            jtjil__xja += '    cpp_cb_general_addr = 0\n'
    else:
        jtjil__xja += """    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])
"""
        jtjil__xja += '    cpp_cb_update_addr = 0\n'
        jtjil__xja += '    cpp_cb_combine_addr = 0\n'
        jtjil__xja += '    cpp_cb_eval_addr = 0\n'
        jtjil__xja += '    cpp_cb_general_addr = 0\n'
    jtjil__xja += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(
        ', '.join([str(supported_agg_funcs.index(hfq__tcof.ftype)) for
        hfq__tcof in allfuncs] + ['0']))
    jtjil__xja += '    func_offsets = np.array({}, dtype=np.int32)\n'.format(
        str(ioj__msr))
    if len(rkk__kavg) > 0:
        jtjil__xja += '    udf_ncols = np.array({}, dtype=np.int32)\n'.format(
            str(rkk__kavg))
    else:
        jtjil__xja += '    udf_ncols = np.array([0], np.int32)\n'
    if tzfdi__omq:
        jtjil__xja += '    arr_type = coerce_to_array({})\n'.format(agg_node
            .pivot_values)
        jtjil__xja += '    arr_info = array_to_info(arr_type)\n'
        jtjil__xja += (
            '    dispatch_table = arr_info_list_to_table([arr_info])\n')
        jtjil__xja += '    pivot_info = array_to_info(pivot_arr)\n'
        jtjil__xja += (
            '    dispatch_info = arr_info_list_to_table([pivot_info])\n')
        jtjil__xja += (
            """    out_table = pivot_groupby_and_aggregate(table, {}, dispatch_table, dispatch_info, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, agg_node.
            is_crosstab, pkiy__mda, agg_node.return_key, agg_node.same_index))
        jtjil__xja += '    delete_info_decref_array(pivot_info)\n'
        jtjil__xja += '    delete_info_decref_array(arr_info)\n'
    else:
        jtjil__xja += (
            """    out_table = groupby_and_aggregate(table, {}, {}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {}, {}, {}, {}, {}, {}, {}, {}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy)
"""
            .format(n_keys, agg_node.input_has_index, parallel, pkiy__mda,
            waq__bkr, ubqr__sfuir, gxzt__rue, agg_node.return_key, agg_node
            .same_index, agg_node.dropna))
    tvy__elzej = 0
    if agg_node.return_key:
        for thj__rrz, auw__cpc in enumerate(kdrb__astns):
            jtjil__xja += (
                '    {} = info_to_array(info_from_table(out_table, {}), {})\n'
                .format(auw__cpc, tvy__elzej, auw__cpc))
            tvy__elzej += 1
    for thj__rrz, hmfg__hxwy in enumerate(rjfal__nzj.values()):
        if isinstance(func, pytypes.SimpleNamespace) and func.fname in ['min',
            'max', 'shift'] and isinstance(skgy__jtb, bodo.CategoricalArrayType
            ):
            jtjil__xja += f"""    {hmfg__hxwy} = info_to_array(info_from_table(out_table, {tvy__elzej}), {hmfg__hxwy + '_dummy'})
"""
        else:
            jtjil__xja += f"""    {hmfg__hxwy} = info_to_array(info_from_table(out_table, {tvy__elzej}), out_typs[{thj__rrz}])
"""
        tvy__elzej += 1
    if agg_node.same_index:
        jtjil__xja += (
            """    out_index_arg = info_to_array(info_from_table(out_table, {}), index_arg)
"""
            .format(tvy__elzej))
        tvy__elzej += 1
    jtjil__xja += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    jtjil__xja += '    delete_table_decref_arrays(table)\n'
    jtjil__xja += '    delete_table_decref_arrays(udf_table_dummy)\n'
    jtjil__xja += '    delete_table(out_table)\n'
    jtjil__xja += f'    ev_clean.finalize()\n'
    cmfpv__wti = tuple(rjfal__nzj.values())
    if agg_node.return_key:
        cmfpv__wti += tuple(kdrb__astns)
    jtjil__xja += '    return ({},{})\n'.format(', '.join(cmfpv__wti), 
        ' out_index_arg,' if agg_node.same_index else '')
    yexvx__gcb = {}
    exec(jtjil__xja, {'out_typs': out_col_typs}, yexvx__gcb)
    wzcz__haez = yexvx__gcb['agg_top']
    return wzcz__haez


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for duy__dfdqh in block.body:
            if is_call_assign(duy__dfdqh) and find_callname(f_ir,
                duy__dfdqh.value) == ('len', 'builtins'
                ) and duy__dfdqh.value.args[0].name == f_ir.arg_names[0]:
                gnvcd__jjs = get_definition(f_ir, duy__dfdqh.value.func)
                gnvcd__jjs.name = 'dummy_agg_count'
                gnvcd__jjs.value = dummy_agg_count
    sjaop__jvwdr = get_name_var_table(f_ir.blocks)
    zogze__iyk = {}
    for name, vmy__dnmvo in sjaop__jvwdr.items():
        zogze__iyk[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, zogze__iyk)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    baup__tng = numba.core.compiler.Flags()
    baup__tng.nrt = True
    xdc__ncegm = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, baup__tng)
    xdc__ncegm.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, zqimc__zlj, calltypes, vmy__dnmvo = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    gwm__rxir = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    tdani__nbsed = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    saiju__ofn = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    dfwu__ocfw = saiju__ofn(typemap, calltypes)
    pm = tdani__nbsed(typingctx, targetctx, None, f_ir, typemap, zqimc__zlj,
        calltypes, dfwu__ocfw, {}, baup__tng, None)
    eemz__zglz = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = tdani__nbsed(typingctx, targetctx, None, f_ir, typemap, zqimc__zlj,
        calltypes, dfwu__ocfw, {}, baup__tng, eemz__zglz)
    arrx__rtj = numba.core.typed_passes.InlineOverloads()
    arrx__rtj.run_pass(pm)
    pnwo__hny = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    pnwo__hny.run()
    for block in f_ir.blocks.values():
        for duy__dfdqh in block.body:
            if is_assign(duy__dfdqh) and isinstance(duy__dfdqh.value, (ir.
                Arg, ir.Var)) and isinstance(typemap[duy__dfdqh.target.name
                ], SeriesType):
                lskk__wtzs = typemap.pop(duy__dfdqh.target.name)
                typemap[duy__dfdqh.target.name] = lskk__wtzs.data
            if is_call_assign(duy__dfdqh) and find_callname(f_ir,
                duy__dfdqh.value) == ('get_series_data',
                'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[duy__dfdqh.target.name].remove(duy__dfdqh
                    .value)
                duy__dfdqh.value = duy__dfdqh.value.args[0]
                f_ir._definitions[duy__dfdqh.target.name].append(duy__dfdqh
                    .value)
            if is_call_assign(duy__dfdqh) and find_callname(f_ir,
                duy__dfdqh.value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[duy__dfdqh.target.name].remove(duy__dfdqh
                    .value)
                duy__dfdqh.value = ir.Const(False, duy__dfdqh.loc)
                f_ir._definitions[duy__dfdqh.target.name].append(duy__dfdqh
                    .value)
            if is_call_assign(duy__dfdqh) and find_callname(f_ir,
                duy__dfdqh.value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[duy__dfdqh.target.name].remove(duy__dfdqh
                    .value)
                duy__dfdqh.value = ir.Const(False, duy__dfdqh.loc)
                f_ir._definitions[duy__dfdqh.target.name].append(duy__dfdqh
                    .value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    cbyo__ber = numba.parfors.parfor.PreParforPass(f_ir, typemap, calltypes,
        typingctx, targetctx, gwm__rxir)
    cbyo__ber.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    iqi__ekp = numba.core.compiler.StateDict()
    iqi__ekp.func_ir = f_ir
    iqi__ekp.typemap = typemap
    iqi__ekp.calltypes = calltypes
    iqi__ekp.typingctx = typingctx
    iqi__ekp.targetctx = targetctx
    iqi__ekp.return_type = zqimc__zlj
    numba.core.rewrites.rewrite_registry.apply('after-inference', iqi__ekp)
    gvh__kbtz = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        zqimc__zlj, typingctx, targetctx, gwm__rxir, baup__tng, {})
    gvh__kbtz.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            twj__iznbf = ctypes.pythonapi.PyCell_Get
            twj__iznbf.restype = ctypes.py_object
            twj__iznbf.argtypes = ctypes.py_object,
            hub__yxhgw = tuple(twj__iznbf(ozsia__vudjz) for ozsia__vudjz in
                closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            hub__yxhgw = closure.items
        assert len(code.co_freevars) == len(hub__yxhgw)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, hub__yxhgw
            )


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
        qxeoa__btewm = SeriesType(in_col_typ.dtype, in_col_typ, None,
            string_type)
        f_ir, pm = compile_to_optimized_ir(func, (qxeoa__btewm,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        jsr__loy, arr_var = _rm_arg_agg_block(block, pm.typemap)
        wqtbf__bmdw = -1
        for thj__rrz, duy__dfdqh in enumerate(jsr__loy):
            if isinstance(duy__dfdqh, numba.parfors.parfor.Parfor):
                assert wqtbf__bmdw == -1, 'only one parfor for aggregation function'
                wqtbf__bmdw = thj__rrz
        parfor = None
        if wqtbf__bmdw != -1:
            parfor = jsr__loy[wqtbf__bmdw]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = jsr__loy[:wqtbf__bmdw] + parfor.init_block.body
        eval_nodes = jsr__loy[wqtbf__bmdw + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for duy__dfdqh in init_nodes:
            if is_assign(duy__dfdqh) and duy__dfdqh.target.name in redvars:
                ind = redvars.index(duy__dfdqh.target.name)
                reduce_vars[ind] = duy__dfdqh.target
        var_types = [pm.typemap[xeqje__khll] for xeqje__khll in redvars]
        xfrfj__eeqiq = gen_combine_func(f_ir, parfor, redvars,
            var_to_redvar, var_types, arr_var, pm, self.typingctx, self.
            targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        btuxi__sdc = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        fdwax__yhs = gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types,
            pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(fdwax__yhs)
        self.all_update_funcs.append(btuxi__sdc)
        self.all_combine_funcs.append(xfrfj__eeqiq)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        self.all_vartypes = self.all_vartypes * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_vartypes
        self.all_reduce_vars = self.all_reduce_vars * len(self.pivot_values
            ) if self.pivot_values is not None else self.all_reduce_vars
        nlxf__pbpm = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        rafu__qtege = gen_all_update_func(self.all_update_funcs, self.
            all_vartypes, self.in_col_types, self.redvar_offsets, self.
            typingctx, self.targetctx, self.pivot_typ, self.pivot_values,
            self.is_crosstab)
        pgec__cttjg = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.
            targetctx, self.pivot_typ, self.pivot_values)
        itld__zejs = gen_all_eval_func(self.all_eval_funcs, self.
            all_vartypes, self.redvar_offsets, self.out_col_types, self.
            typingctx, self.targetctx, self.pivot_values)
        return (self.all_vartypes, nlxf__pbpm, rafu__qtege, pgec__cttjg,
            itld__zejs)


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
    zjehi__cveoo = []
    for t, hfq__tcof in zip(in_col_types, agg_func):
        zjehi__cveoo.append((t, hfq__tcof))
    kuw__zkgb = RegularUDFGenerator(in_col_types, out_col_types, pivot_typ,
        pivot_values, is_crosstab, typingctx, targetctx)
    xtb__ajpsb = GeneralUDFGenerator()
    for in_col_typ, func in zjehi__cveoo:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            kuw__zkgb.add_udf(in_col_typ, func)
        except:
            xtb__ajpsb.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = kuw__zkgb.gen_all_func()
    general_udf_funcs = xtb__ajpsb.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    klyy__mxzrw = compute_use_defs(parfor.loop_body)
    bpiw__bza = set()
    for tvzzk__jak in klyy__mxzrw.usemap.values():
        bpiw__bza |= tvzzk__jak
    xyr__dzyc = set()
    for tvzzk__jak in klyy__mxzrw.defmap.values():
        xyr__dzyc |= tvzzk__jak
    pnt__sxh = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    pnt__sxh.body = eval_nodes
    uqzeu__iwj = compute_use_defs({(0): pnt__sxh})
    hgzab__oti = uqzeu__iwj.usemap[0]
    jilul__nya = set()
    mjyz__fozsp = []
    mxjjq__rrhsb = []
    for duy__dfdqh in reversed(init_nodes):
        peu__nshy = {xeqje__khll.name for xeqje__khll in duy__dfdqh.list_vars()
            }
        if is_assign(duy__dfdqh):
            xeqje__khll = duy__dfdqh.target.name
            peu__nshy.remove(xeqje__khll)
            if (xeqje__khll in bpiw__bza and xeqje__khll not in jilul__nya and
                xeqje__khll not in hgzab__oti and xeqje__khll not in xyr__dzyc
                ):
                mxjjq__rrhsb.append(duy__dfdqh)
                bpiw__bza |= peu__nshy
                xyr__dzyc.add(xeqje__khll)
                continue
        jilul__nya |= peu__nshy
        mjyz__fozsp.append(duy__dfdqh)
    mxjjq__rrhsb.reverse()
    mjyz__fozsp.reverse()
    pord__ifhy = min(parfor.loop_body.keys())
    ldo__omq = parfor.loop_body[pord__ifhy]
    ldo__omq.body = mxjjq__rrhsb + ldo__omq.body
    return mjyz__fozsp


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    khdf__vlu = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    dimub__hpoix = set()
    akc__tsfjo = []
    for duy__dfdqh in init_nodes:
        if is_assign(duy__dfdqh) and isinstance(duy__dfdqh.value, ir.Global
            ) and isinstance(duy__dfdqh.value.value, pytypes.FunctionType
            ) and duy__dfdqh.value.value in khdf__vlu:
            dimub__hpoix.add(duy__dfdqh.target.name)
        elif is_call_assign(duy__dfdqh
            ) and duy__dfdqh.value.func.name in dimub__hpoix:
            pass
        else:
            akc__tsfjo.append(duy__dfdqh)
    init_nodes = akc__tsfjo
    zifu__qmd = types.Tuple(var_types)
    wemhu__dss = lambda : None
    f_ir = compile_to_numba_ir(wemhu__dss, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    feqtk__msv = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    zfum__fkmy = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        feqtk__msv, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [zfum__fkmy] + block.body
    block.body[-2].value.value = feqtk__msv
    htuc__oxs = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        zifu__qmd, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    vvts__lees = numba.core.target_extension.dispatcher_registry[cpu_target](
        wemhu__dss)
    vvts__lees.add_overload(htuc__oxs)
    return vvts__lees


def gen_all_update_func(update_funcs, reduce_var_types, in_col_types,
    redvar_offsets, typingctx, targetctx, pivot_typ, pivot_values, is_crosstab
    ):
    nifl__ojplm = len(update_funcs)
    ddmxm__hjt = len(in_col_types)
    if pivot_values is not None:
        assert ddmxm__hjt == 1
    jtjil__xja = (
        'def update_all_f(redvar_arrs, data_in, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        zvcf__plfj = redvar_offsets[ddmxm__hjt]
        jtjil__xja += '  pv = pivot_arr[i]\n'
        for gqvs__goa, syph__nrcj in enumerate(pivot_values):
            lbj__nbur = 'el' if gqvs__goa != 0 else ''
            jtjil__xja += "  {}if pv == '{}':\n".format(lbj__nbur, syph__nrcj)
            zrdv__aktv = zvcf__plfj * gqvs__goa
            nqcy__nnfk = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                thj__rrz) for thj__rrz in range(zrdv__aktv + redvar_offsets
                [0], zrdv__aktv + redvar_offsets[1])])
            yae__obu = 'data_in[0][i]'
            if is_crosstab:
                yae__obu = '0'
            jtjil__xja += '    {} = update_vars_0({}, {})\n'.format(nqcy__nnfk,
                nqcy__nnfk, yae__obu)
    else:
        for gqvs__goa in range(nifl__ojplm):
            nqcy__nnfk = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                thj__rrz) for thj__rrz in range(redvar_offsets[gqvs__goa],
                redvar_offsets[gqvs__goa + 1])])
            if nqcy__nnfk:
                jtjil__xja += ('  {} = update_vars_{}({},  data_in[{}][i])\n'
                    .format(nqcy__nnfk, gqvs__goa, nqcy__nnfk, 0 if 
                    ddmxm__hjt == 1 else gqvs__goa))
    jtjil__xja += '  return\n'
    abnjj__yrd = {}
    for thj__rrz, hfq__tcof in enumerate(update_funcs):
        abnjj__yrd['update_vars_{}'.format(thj__rrz)] = hfq__tcof
    yexvx__gcb = {}
    exec(jtjil__xja, abnjj__yrd, yexvx__gcb)
    ykp__ndlpf = yexvx__gcb['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(ykp__ndlpf)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx, pivot_typ, pivot_values):
    ofl__rsr = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types])
    arg_typs = ofl__rsr, ofl__rsr, types.intp, types.intp, pivot_typ
    kjd__iomz = len(redvar_offsets) - 1
    zvcf__plfj = redvar_offsets[kjd__iomz]
    jtjil__xja = (
        'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i, pivot_arr):\n')
    if pivot_values is not None:
        assert kjd__iomz == 1
        for ngydd__qrj in range(len(pivot_values)):
            zrdv__aktv = zvcf__plfj * ngydd__qrj
            nqcy__nnfk = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                thj__rrz) for thj__rrz in range(zrdv__aktv + redvar_offsets
                [0], zrdv__aktv + redvar_offsets[1])])
            nxuxt__gycxc = ', '.join(['recv_arrs[{}][i]'.format(thj__rrz) for
                thj__rrz in range(zrdv__aktv + redvar_offsets[0], 
                zrdv__aktv + redvar_offsets[1])])
            jtjil__xja += '  {} = combine_vars_0({}, {})\n'.format(nqcy__nnfk,
                nqcy__nnfk, nxuxt__gycxc)
    else:
        for gqvs__goa in range(kjd__iomz):
            nqcy__nnfk = ', '.join(['redvar_arrs[{}][w_ind]'.format(
                thj__rrz) for thj__rrz in range(redvar_offsets[gqvs__goa],
                redvar_offsets[gqvs__goa + 1])])
            nxuxt__gycxc = ', '.join(['recv_arrs[{}][i]'.format(thj__rrz) for
                thj__rrz in range(redvar_offsets[gqvs__goa], redvar_offsets
                [gqvs__goa + 1])])
            if nxuxt__gycxc:
                jtjil__xja += '  {} = combine_vars_{}({}, {})\n'.format(
                    nqcy__nnfk, gqvs__goa, nqcy__nnfk, nxuxt__gycxc)
    jtjil__xja += '  return\n'
    abnjj__yrd = {}
    for thj__rrz, hfq__tcof in enumerate(combine_funcs):
        abnjj__yrd['combine_vars_{}'.format(thj__rrz)] = hfq__tcof
    yexvx__gcb = {}
    exec(jtjil__xja, abnjj__yrd, yexvx__gcb)
    viq__kvqm = yexvx__gcb['combine_all_f']
    f_ir = compile_to_numba_ir(viq__kvqm, abnjj__yrd)
    pgec__cttjg = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    vvts__lees = numba.core.target_extension.dispatcher_registry[cpu_target](
        viq__kvqm)
    vvts__lees.add_overload(pgec__cttjg)
    return vvts__lees


def gen_all_eval_func(eval_funcs, reduce_var_types, redvar_offsets,
    out_col_typs, typingctx, targetctx, pivot_values):
    ofl__rsr = types.Tuple([types.Array(t, 1, 'C') for t in reduce_var_types])
    out_col_typs = types.Tuple(out_col_typs)
    kjd__iomz = len(redvar_offsets) - 1
    zvcf__plfj = redvar_offsets[kjd__iomz]
    jtjil__xja = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    if pivot_values is not None:
        assert kjd__iomz == 1
        for gqvs__goa in range(len(pivot_values)):
            zrdv__aktv = zvcf__plfj * gqvs__goa
            nqcy__nnfk = ', '.join(['redvar_arrs[{}][j]'.format(thj__rrz) for
                thj__rrz in range(zrdv__aktv + redvar_offsets[0], 
                zrdv__aktv + redvar_offsets[1])])
            jtjil__xja += '  out_arrs[{}][j] = eval_vars_0({})\n'.format(
                gqvs__goa, nqcy__nnfk)
    else:
        for gqvs__goa in range(kjd__iomz):
            nqcy__nnfk = ', '.join(['redvar_arrs[{}][j]'.format(thj__rrz) for
                thj__rrz in range(redvar_offsets[gqvs__goa], redvar_offsets
                [gqvs__goa + 1])])
            jtjil__xja += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(
                gqvs__goa, gqvs__goa, nqcy__nnfk)
    jtjil__xja += '  return\n'
    abnjj__yrd = {}
    for thj__rrz, hfq__tcof in enumerate(eval_funcs):
        abnjj__yrd['eval_vars_{}'.format(thj__rrz)] = hfq__tcof
    yexvx__gcb = {}
    exec(jtjil__xja, abnjj__yrd, yexvx__gcb)
    bqvd__oofu = yexvx__gcb['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(bqvd__oofu)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    aud__kxqu = len(var_types)
    bwsc__jerah = [f'in{thj__rrz}' for thj__rrz in range(aud__kxqu)]
    zifu__qmd = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    orngn__qbc = zifu__qmd(0)
    jtjil__xja = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        bwsc__jerah))
    yexvx__gcb = {}
    exec(jtjil__xja, {'_zero': orngn__qbc}, yexvx__gcb)
    cge__jcyi = yexvx__gcb['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(cge__jcyi, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': orngn__qbc}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    dcxfu__mfl = []
    for thj__rrz, xeqje__khll in enumerate(reduce_vars):
        dcxfu__mfl.append(ir.Assign(block.body[thj__rrz].target,
            xeqje__khll, xeqje__khll.loc))
        for hcks__idulz in xeqje__khll.versioned_names:
            dcxfu__mfl.append(ir.Assign(xeqje__khll, ir.Var(xeqje__khll.
                scope, hcks__idulz, xeqje__khll.loc), xeqje__khll.loc))
    block.body = block.body[:aud__kxqu] + dcxfu__mfl + eval_nodes
    fdwax__yhs = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        zifu__qmd, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    vvts__lees = numba.core.target_extension.dispatcher_registry[cpu_target](
        cge__jcyi)
    vvts__lees.add_overload(fdwax__yhs)
    return vvts__lees


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    aud__kxqu = len(redvars)
    glgph__mfkjs = [f'v{thj__rrz}' for thj__rrz in range(aud__kxqu)]
    bwsc__jerah = [f'in{thj__rrz}' for thj__rrz in range(aud__kxqu)]
    jtjil__xja = 'def agg_combine({}):\n'.format(', '.join(glgph__mfkjs +
        bwsc__jerah))
    onw__tchp = wrap_parfor_blocks(parfor)
    juxui__dkc = find_topo_order(onw__tchp)
    juxui__dkc = juxui__dkc[1:]
    unwrap_parfor_blocks(parfor)
    itobn__mhay = {}
    cihko__hib = []
    for kgw__qgvz in juxui__dkc:
        kcrbn__mdoko = parfor.loop_body[kgw__qgvz]
        for duy__dfdqh in kcrbn__mdoko.body:
            if is_call_assign(duy__dfdqh) and guard(find_callname, f_ir,
                duy__dfdqh.value) == ('__special_combine', 'bodo.ir.aggregate'
                ):
                args = duy__dfdqh.value.args
                gqb__zkr = []
                snuj__dxtp = []
                for xeqje__khll in args[:-1]:
                    ind = redvars.index(xeqje__khll.name)
                    cihko__hib.append(ind)
                    gqb__zkr.append('v{}'.format(ind))
                    snuj__dxtp.append('in{}'.format(ind))
                jhkkf__bsfk = '__special_combine__{}'.format(len(itobn__mhay))
                jtjil__xja += '    ({},) = {}({})\n'.format(', '.join(
                    gqb__zkr), jhkkf__bsfk, ', '.join(gqb__zkr + snuj__dxtp))
                fkl__gbhrb = ir.Expr.call(args[-1], [], (), kcrbn__mdoko.loc)
                uiue__lypig = guard(find_callname, f_ir, fkl__gbhrb)
                assert uiue__lypig == ('_var_combine', 'bodo.ir.aggregate')
                uiue__lypig = bodo.ir.aggregate._var_combine
                itobn__mhay[jhkkf__bsfk] = uiue__lypig
            if is_assign(duy__dfdqh) and duy__dfdqh.target.name in redvars:
                fkq__tjr = duy__dfdqh.target.name
                ind = redvars.index(fkq__tjr)
                if ind in cihko__hib:
                    continue
                if len(f_ir._definitions[fkq__tjr]) == 2:
                    var_def = f_ir._definitions[fkq__tjr][0]
                    jtjil__xja += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[fkq__tjr][1]
                    jtjil__xja += _match_reduce_def(var_def, f_ir, ind)
    jtjil__xja += '    return {}'.format(', '.join(['v{}'.format(thj__rrz) for
        thj__rrz in range(aud__kxqu)]))
    yexvx__gcb = {}
    exec(jtjil__xja, {}, yexvx__gcb)
    amuyq__cstp = yexvx__gcb['agg_combine']
    arg_typs = tuple(2 * var_types)
    abnjj__yrd = {'numba': numba, 'bodo': bodo, 'np': np}
    abnjj__yrd.update(itobn__mhay)
    f_ir = compile_to_numba_ir(amuyq__cstp, abnjj__yrd, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    zifu__qmd = pm.typemap[block.body[-1].value.name]
    xfrfj__eeqiq = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        zifu__qmd, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    vvts__lees = numba.core.target_extension.dispatcher_registry[cpu_target](
        amuyq__cstp)
    vvts__lees.add_overload(xfrfj__eeqiq)
    return vvts__lees


def _match_reduce_def(var_def, f_ir, ind):
    jtjil__xja = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        jtjil__xja = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        mhtru__awbad = guard(find_callname, f_ir, var_def)
        if mhtru__awbad == ('min', 'builtins'):
            jtjil__xja = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if mhtru__awbad == ('max', 'builtins'):
            jtjil__xja = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return jtjil__xja


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    aud__kxqu = len(redvars)
    pfgn__sdzhv = 1
    gsb__iapo = []
    for thj__rrz in range(pfgn__sdzhv):
        esuf__okns = ir.Var(arr_var.scope, f'$input{thj__rrz}', arr_var.loc)
        gsb__iapo.append(esuf__okns)
    anw__fdhi = parfor.loop_nests[0].index_variable
    hdcli__bfo = [0] * aud__kxqu
    for kcrbn__mdoko in parfor.loop_body.values():
        luout__jaxfy = []
        for duy__dfdqh in kcrbn__mdoko.body:
            if is_var_assign(duy__dfdqh
                ) and duy__dfdqh.value.name == anw__fdhi.name:
                continue
            if is_getitem(duy__dfdqh
                ) and duy__dfdqh.value.value.name == arr_var.name:
                duy__dfdqh.value = gsb__iapo[0]
            if is_call_assign(duy__dfdqh) and guard(find_callname, pm.
                func_ir, duy__dfdqh.value) == ('isna',
                'bodo.libs.array_kernels') and duy__dfdqh.value.args[0
                ].name == arr_var.name:
                duy__dfdqh.value = ir.Const(False, duy__dfdqh.target.loc)
            if is_assign(duy__dfdqh) and duy__dfdqh.target.name in redvars:
                ind = redvars.index(duy__dfdqh.target.name)
                hdcli__bfo[ind] = duy__dfdqh.target
            luout__jaxfy.append(duy__dfdqh)
        kcrbn__mdoko.body = luout__jaxfy
    glgph__mfkjs = ['v{}'.format(thj__rrz) for thj__rrz in range(aud__kxqu)]
    bwsc__jerah = ['in{}'.format(thj__rrz) for thj__rrz in range(pfgn__sdzhv)]
    jtjil__xja = 'def agg_update({}):\n'.format(', '.join(glgph__mfkjs +
        bwsc__jerah))
    jtjil__xja += '    __update_redvars()\n'
    jtjil__xja += '    return {}'.format(', '.join(['v{}'.format(thj__rrz) for
        thj__rrz in range(aud__kxqu)]))
    yexvx__gcb = {}
    exec(jtjil__xja, {}, yexvx__gcb)
    gek__hcklo = yexvx__gcb['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * pfgn__sdzhv)
    f_ir = compile_to_numba_ir(gek__hcklo, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    unbq__eidyh = f_ir.blocks.popitem()[1].body
    zifu__qmd = pm.typemap[unbq__eidyh[-1].value.name]
    onw__tchp = wrap_parfor_blocks(parfor)
    juxui__dkc = find_topo_order(onw__tchp)
    juxui__dkc = juxui__dkc[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    ldo__omq = f_ir.blocks[juxui__dkc[0]]
    lplo__hmrj = f_ir.blocks[juxui__dkc[-1]]
    wxq__ojftp = unbq__eidyh[:aud__kxqu + pfgn__sdzhv]
    if aud__kxqu > 1:
        fti__cbwfz = unbq__eidyh[-3:]
        assert is_assign(fti__cbwfz[0]) and isinstance(fti__cbwfz[0].value,
            ir.Expr) and fti__cbwfz[0].value.op == 'build_tuple'
    else:
        fti__cbwfz = unbq__eidyh[-2:]
    for thj__rrz in range(aud__kxqu):
        eeum__hiwiu = unbq__eidyh[thj__rrz].target
        yhor__pqa = ir.Assign(eeum__hiwiu, hdcli__bfo[thj__rrz],
            eeum__hiwiu.loc)
        wxq__ojftp.append(yhor__pqa)
    for thj__rrz in range(aud__kxqu, aud__kxqu + pfgn__sdzhv):
        eeum__hiwiu = unbq__eidyh[thj__rrz].target
        yhor__pqa = ir.Assign(eeum__hiwiu, gsb__iapo[thj__rrz - aud__kxqu],
            eeum__hiwiu.loc)
        wxq__ojftp.append(yhor__pqa)
    ldo__omq.body = wxq__ojftp + ldo__omq.body
    bhtry__efok = []
    for thj__rrz in range(aud__kxqu):
        eeum__hiwiu = unbq__eidyh[thj__rrz].target
        yhor__pqa = ir.Assign(hdcli__bfo[thj__rrz], eeum__hiwiu,
            eeum__hiwiu.loc)
        bhtry__efok.append(yhor__pqa)
    lplo__hmrj.body += bhtry__efok + fti__cbwfz
    ayugx__pberp = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        zifu__qmd, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    vvts__lees = numba.core.target_extension.dispatcher_registry[cpu_target](
        gek__hcklo)
    vvts__lees.add_overload(ayugx__pberp)
    return vvts__lees


def _rm_arg_agg_block(block, typemap):
    jsr__loy = []
    arr_var = None
    for thj__rrz, duy__dfdqh in enumerate(block.body):
        if is_assign(duy__dfdqh) and isinstance(duy__dfdqh.value, ir.Arg):
            arr_var = duy__dfdqh.target
            gyt__bzznz = typemap[arr_var.name]
            if not isinstance(gyt__bzznz, types.ArrayCompatible):
                jsr__loy += block.body[thj__rrz + 1:]
                break
            otxi__yhl = block.body[thj__rrz + 1]
            assert is_assign(otxi__yhl) and isinstance(otxi__yhl.value, ir.Expr
                ) and otxi__yhl.value.op == 'getattr' and otxi__yhl.value.attr == 'shape' and otxi__yhl.value.value.name == arr_var.name
            rgafu__dqq = otxi__yhl.target
            cxa__fwbdy = block.body[thj__rrz + 2]
            assert is_assign(cxa__fwbdy) and isinstance(cxa__fwbdy.value,
                ir.Expr
                ) and cxa__fwbdy.value.op == 'static_getitem' and cxa__fwbdy.value.value.name == rgafu__dqq.name
            jsr__loy += block.body[thj__rrz + 3:]
            break
        jsr__loy.append(duy__dfdqh)
    return jsr__loy, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    onw__tchp = wrap_parfor_blocks(parfor)
    juxui__dkc = find_topo_order(onw__tchp)
    juxui__dkc = juxui__dkc[1:]
    unwrap_parfor_blocks(parfor)
    for kgw__qgvz in reversed(juxui__dkc):
        for duy__dfdqh in reversed(parfor.loop_body[kgw__qgvz].body):
            if isinstance(duy__dfdqh, ir.Assign) and (duy__dfdqh.target.
                name in parfor_params or duy__dfdqh.target.name in var_to_param
                ):
                uepv__xfh = duy__dfdqh.target.name
                rhs = duy__dfdqh.value
                vgm__vbf = (uepv__xfh if uepv__xfh in parfor_params else
                    var_to_param[uepv__xfh])
                tovri__ucjlh = []
                if isinstance(rhs, ir.Var):
                    tovri__ucjlh = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    tovri__ucjlh = [xeqje__khll.name for xeqje__khll in
                        duy__dfdqh.value.list_vars()]
                param_uses[vgm__vbf].extend(tovri__ucjlh)
                for xeqje__khll in tovri__ucjlh:
                    var_to_param[xeqje__khll] = vgm__vbf
            if isinstance(duy__dfdqh, Parfor):
                get_parfor_reductions(duy__dfdqh, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for kdu__zkh, tovri__ucjlh in param_uses.items():
        if kdu__zkh in tovri__ucjlh and kdu__zkh not in reduce_varnames:
            reduce_varnames.append(kdu__zkh)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
