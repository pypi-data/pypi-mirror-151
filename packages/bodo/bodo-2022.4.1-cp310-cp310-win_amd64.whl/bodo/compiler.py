"""
Defines Bodo's compiler pipeline.
"""
import os
import warnings
from collections import namedtuple
import numba
from numba.core import ir, ir_utils, types
from numba.core.compiler import DefaultPassBuilder
from numba.core.compiler_machinery import AnalysisPass, FunctionPass, register_pass
from numba.core.inline_closurecall import inline_closure_call
from numba.core.ir_utils import build_definitions, find_callname, get_definition, guard
from numba.core.registry import CPUDispatcher
from numba.core.typed_passes import DumpParforDiagnostics, InlineOverloads, IRLegalization, NopythonTypeInference, ParforPass, PreParforPass
from numba.core.untyped_passes import MakeFunctionToJitFunction, ReconstructSSA, WithLifting
import bodo
import bodo.hiframes.dataframe_indexing
import bodo.hiframes.datetime_datetime_ext
import bodo.hiframes.datetime_timedelta_ext
import bodo.io
import bodo.libs
import bodo.libs.array_kernels
import bodo.libs.int_arr_ext
import bodo.libs.re_ext
import bodo.libs.spark_extra
import bodo.transforms
import bodo.transforms.series_pass
import bodo.transforms.untyped_pass
import bodo.utils
import bodo.utils.table_utils
import bodo.utils.typing
from bodo.transforms.series_pass import SeriesPass
from bodo.transforms.table_column_del_pass import TableColumnDelPass
from bodo.transforms.typing_pass import BodoTypeInference
from bodo.transforms.untyped_pass import UntypedPass
from bodo.utils.utils import is_assign, is_call_assign, is_expr
numba.core.config.DISABLE_PERFORMANCE_WARNINGS = 1
from numba.core.errors import NumbaExperimentalFeatureWarning, NumbaPendingDeprecationWarning
warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
inline_all_calls = False


class BodoCompiler(numba.core.compiler.CompilerBase):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=True,
            inline_calls_pass=inline_all_calls)

    def _create_bodo_pipeline(self, distributed=True, inline_calls_pass=
        False, udf_pipeline=False):
        egb__rgk = 'bodo' if distributed else 'bodo_seq'
        egb__rgk = egb__rgk + '_inline' if inline_calls_pass else egb__rgk
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, egb__rgk)
        if inline_calls_pass:
            pm.add_pass_after(InlinePass, WithLifting)
        if udf_pipeline:
            pm.add_pass_after(ConvertCallsUDFPass, WithLifting)
        add_pass_before(pm, BodoUntypedPass, ReconstructSSA)
        replace_pass(pm, BodoTypeInference, NopythonTypeInference)
        remove_pass(pm, MakeFunctionToJitFunction)
        add_pass_before(pm, BodoSeriesPass, PreParforPass)
        if distributed:
            pm.add_pass_after(BodoDistributedPass, ParforPass)
        else:
            pm.add_pass_after(LowerParforSeq, ParforPass)
            pm.add_pass_after(LowerBodoIRExtSeq, LowerParforSeq)
        add_pass_before(pm, BodoTableColumnDelPass, IRLegalization)
        pm.add_pass_after(BodoDumpDistDiagnosticsPass, DumpParforDiagnostics)
        pm.finalize()
        return [pm]


def add_pass_before(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for xlatp__mtqf, (ofl__mmq, avl__ipniz) in enumerate(pm.passes):
        if ofl__mmq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(xlatp__mtqf, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for xlatp__mtqf, (ofl__mmq, avl__ipniz) in enumerate(pm.passes):
        if ofl__mmq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[xlatp__mtqf] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for xlatp__mtqf, (ofl__mmq, avl__ipniz) in enumerate(pm.passes):
        if ofl__mmq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(xlatp__mtqf)
    pm._finalized = False


@register_pass(mutates_CFG=True, analysis_only=False)
class InlinePass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        inline_calls(state.func_ir, state.locals)
        state.func_ir.blocks = ir_utils.simplify_CFG(state.func_ir.blocks)
        return True


def _convert_bodo_dispatcher_to_udf(rhs, func_ir):
    uxmw__qyxs = guard(get_definition, func_ir, rhs.func)
    if isinstance(uxmw__qyxs, (ir.Global, ir.FreeVar, ir.Const)):
        bddjt__bawvh = uxmw__qyxs.value
    else:
        svxqo__bte = guard(find_callname, func_ir, rhs)
        if not (svxqo__bte and isinstance(svxqo__bte[0], str) and
            isinstance(svxqo__bte[1], str)):
            return
        func_name, func_mod = svxqo__bte
        try:
            import importlib
            xxm__dopmc = importlib.import_module(func_mod)
            bddjt__bawvh = getattr(xxm__dopmc, func_name)
        except:
            return
    if isinstance(bddjt__bawvh, CPUDispatcher) and issubclass(bddjt__bawvh.
        _compiler.pipeline_class, BodoCompiler
        ) and bddjt__bawvh._compiler.pipeline_class != BodoCompilerUDF:
        bddjt__bawvh._compiler.pipeline_class = BodoCompilerUDF
        bddjt__bawvh.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for bmanj__klbvc in block.body:
                if is_call_assign(bmanj__klbvc):
                    _convert_bodo_dispatcher_to_udf(bmanj__klbvc.value,
                        state.func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        rxhp__tihgh = UntypedPass(state.func_ir, state.typingctx, state.
            args, state.locals, state.metadata, state.flags)
        rxhp__tihgh.run()
        return True


def _update_definitions(func_ir, node_list):
    jcywg__ovkkw = ir.Loc('', 0)
    scpij__afrf = ir.Block(ir.Scope(None, jcywg__ovkkw), jcywg__ovkkw)
    scpij__afrf.body = node_list
    build_definitions({(0): scpij__afrf}, func_ir._definitions)


_series_inline_attrs = {'values', 'shape', 'size', 'empty', 'name', 'index',
    'dtype'}
_series_no_inline_methods = {'to_list', 'tolist', 'rolling', 'to_csv',
    'count', 'fillna', 'to_dict', 'map', 'apply', 'pipe', 'combine',
    'bfill', 'ffill', 'pad', 'backfill', 'mask', 'where'}
_series_method_alias = {'isnull': 'isna', 'product': 'prod', 'kurtosis':
    'kurt', 'is_monotonic': 'is_monotonic_increasing', 'notnull': 'notna'}
_dataframe_no_inline_methods = {'apply', 'itertuples', 'pipe', 'to_parquet',
    'to_sql', 'to_csv', 'to_json', 'assign', 'to_string', 'query',
    'rolling', 'mask', 'where'}
TypingInfo = namedtuple('TypingInfo', ['typingctx', 'targetctx', 'typemap',
    'calltypes', 'curr_loc'])


def _inline_bodo_getattr(stmt, rhs, rhs_type, new_body, func_ir, typingctx,
    targetctx, typemap, calltypes):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import compile_func_single_block
    if isinstance(rhs_type, SeriesType) and rhs.attr in _series_inline_attrs:
        mcr__symt = 'overload_series_' + rhs.attr
        hunak__mfs = getattr(bodo.hiframes.series_impl, mcr__symt)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        mcr__symt = 'overload_dataframe_' + rhs.attr
        hunak__mfs = getattr(bodo.hiframes.dataframe_impl, mcr__symt)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    nxtdl__cxt = hunak__mfs(rhs_type)
    cnl__djgu = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    ixqgr__xdc = compile_func_single_block(nxtdl__cxt, (rhs.value,), stmt.
        target, cnl__djgu)
    _update_definitions(func_ir, ixqgr__xdc)
    new_body += ixqgr__xdc
    return True


def _inline_bodo_call(rhs, i, func_mod, func_name, pass_info, new_body,
    block, typingctx, targetctx, calltypes, work_list):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import replace_func, update_locs
    func_ir = pass_info.func_ir
    typemap = pass_info.typemap
    if isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        SeriesType) and func_name not in _series_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        if (func_name in bodo.hiframes.series_impl.explicit_binop_funcs or 
            func_name.startswith('r') and func_name[1:] in bodo.hiframes.
            series_impl.explicit_binop_funcs):
            return False
        rhs.args.insert(0, func_mod)
        udt__nichm = tuple(typemap[bfowt__ddmyv.name] for bfowt__ddmyv in
            rhs.args)
        ykxl__mvjy = {egb__rgk: typemap[bfowt__ddmyv.name] for egb__rgk,
            bfowt__ddmyv in dict(rhs.kws).items()}
        nxtdl__cxt = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*udt__nichm, **ykxl__mvjy)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        udt__nichm = tuple(typemap[bfowt__ddmyv.name] for bfowt__ddmyv in
            rhs.args)
        ykxl__mvjy = {egb__rgk: typemap[bfowt__ddmyv.name] for egb__rgk,
            bfowt__ddmyv in dict(rhs.kws).items()}
        nxtdl__cxt = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*udt__nichm, **ykxl__mvjy)
    else:
        return False
    uylvx__rmep = replace_func(pass_info, nxtdl__cxt, rhs.args, pysig=numba
        .core.utils.pysignature(nxtdl__cxt), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    kek__pycav, avl__ipniz = inline_closure_call(func_ir, uylvx__rmep.glbls,
        block, len(new_body), uylvx__rmep.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=uylvx__rmep.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for swv__bsq in kek__pycav.values():
        swv__bsq.loc = rhs.loc
        update_locs(swv__bsq.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    tman__aipat = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = tman__aipat(func_ir, typemap)
    xsrr__hhx = func_ir.blocks
    work_list = list((pqqdj__lsajn, xsrr__hhx[pqqdj__lsajn]) for
        pqqdj__lsajn in reversed(xsrr__hhx.keys()))
    while work_list:
        apfn__jyyez, block = work_list.pop()
        new_body = []
        atutw__qrem = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                svxqo__bte = guard(find_callname, func_ir, rhs, typemap)
                if svxqo__bte is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = svxqo__bte
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    atutw__qrem = True
                    break
            new_body.append(stmt)
        if not atutw__qrem:
            xsrr__hhx[apfn__jyyez].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        goxss__mul = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = goxss__mul.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        vzuou__wjs = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        vzuou__wjs.run()
        vzuou__wjs.run()
        vzuou__wjs.run()
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        nioj__nnx = 0
        lwkaz__kpojo = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            nioj__nnx = int(os.environ[lwkaz__kpojo])
        except:
            pass
        if nioj__nnx > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(nioj__nnx, state
                .metadata)
        return True


class BodoCompilerSeq(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False,
            inline_calls_pass=inline_all_calls)


class BodoCompilerUDF(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False, udf_pipeline=True)


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerParforSeq(FunctionPass):
    _name = 'bodo_lower_parfor_seq_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bodo.transforms.distributed_pass.lower_parfor_sequential(state.
            typingctx, state.func_ir, state.typemap, state.calltypes, state
            .metadata)
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerBodoIRExtSeq(FunctionPass):
    _name = 'bodo_lower_ir_ext_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        from bodo.transforms.distributed_pass import distributed_run_extensions
        from bodo.transforms.table_column_del_pass import remove_dead_table_columns
        from bodo.utils.transform import compile_func_single_block
        from bodo.utils.typing import decode_if_dict_array, to_str_arr_if_dict_array
        state.func_ir._definitions = build_definitions(state.func_ir.blocks)
        cnl__djgu = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, cnl__djgu)
        for block in state.func_ir.blocks.values():
            new_body = []
            for bmanj__klbvc in block.body:
                if type(bmanj__klbvc) in distributed_run_extensions:
                    xkqzg__mpdxa = distributed_run_extensions[type(
                        bmanj__klbvc)]
                    egx__whhf = xkqzg__mpdxa(bmanj__klbvc, None, state.
                        typemap, state.calltypes, state.typingctx, state.
                        targetctx)
                    new_body += egx__whhf
                elif is_call_assign(bmanj__klbvc):
                    rhs = bmanj__klbvc.value
                    svxqo__bte = guard(find_callname, state.func_ir, rhs)
                    if svxqo__bte == ('gatherv', 'bodo') or svxqo__bte == (
                        'allgatherv', 'bodo'):
                        fdn__tlhoy = state.typemap[bmanj__klbvc.target.name]
                        qsezz__aepya = state.typemap[rhs.args[0].name]
                        if isinstance(qsezz__aepya, types.Array
                            ) and isinstance(fdn__tlhoy, types.Array):
                            hnftd__pisrp = qsezz__aepya.copy(readonly=False)
                            idwn__oypyc = fdn__tlhoy.copy(readonly=False)
                            if hnftd__pisrp == idwn__oypyc:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), bmanj__klbvc.target, cnl__djgu)
                                continue
                        if (fdn__tlhoy != qsezz__aepya and 
                            to_str_arr_if_dict_array(fdn__tlhoy) ==
                            to_str_arr_if_dict_array(qsezz__aepya)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), bmanj__klbvc.target,
                                cnl__djgu, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            bmanj__klbvc.value = rhs.args[0]
                    new_body.append(bmanj__klbvc)
                else:
                    new_body.append(bmanj__klbvc)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        rof__nmwjy = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return rof__nmwjy.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    qcyt__jyiya = set()
    while work_list:
        apfn__jyyez, block = work_list.pop()
        qcyt__jyiya.add(apfn__jyyez)
        for i, ppj__stw in enumerate(block.body):
            if isinstance(ppj__stw, ir.Assign):
                rocj__nmkmw = ppj__stw.value
                if isinstance(rocj__nmkmw, ir.Expr
                    ) and rocj__nmkmw.op == 'call':
                    uxmw__qyxs = guard(get_definition, func_ir, rocj__nmkmw
                        .func)
                    if isinstance(uxmw__qyxs, (ir.Global, ir.FreeVar)
                        ) and isinstance(uxmw__qyxs.value, CPUDispatcher
                        ) and issubclass(uxmw__qyxs.value._compiler.
                        pipeline_class, BodoCompiler):
                        iqs__pqfyy = uxmw__qyxs.value.py_func
                        arg_types = None
                        if typingctx:
                            pmd__pms = dict(rocj__nmkmw.kws)
                            qzkr__rtrl = tuple(typemap[bfowt__ddmyv.name] for
                                bfowt__ddmyv in rocj__nmkmw.args)
                            xhn__gjg = {svzr__mcvq: typemap[bfowt__ddmyv.
                                name] for svzr__mcvq, bfowt__ddmyv in
                                pmd__pms.items()}
                            avl__ipniz, arg_types = (uxmw__qyxs.value.
                                fold_argument_types(qzkr__rtrl, xhn__gjg))
                        avl__ipniz, uoo__oyn = inline_closure_call(func_ir,
                            iqs__pqfyy.__globals__, block, i, iqs__pqfyy,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((uoo__oyn[svzr__mcvq].name,
                            bfowt__ddmyv) for svzr__mcvq, bfowt__ddmyv in
                            uxmw__qyxs.value.locals.items() if svzr__mcvq in
                            uoo__oyn)
                        break
    return qcyt__jyiya


def udf_jit(signature_or_function=None, **options):
    odbje__bfjj = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=odbje__bfjj,
        pipeline_class=bodo.compiler.BodoCompilerUDF, **options)


def is_udf_call(func_type):
    return isinstance(func_type, numba.core.types.Dispatcher
        ) and func_type.dispatcher._compiler.pipeline_class == BodoCompilerUDF


def is_user_dispatcher(func_type):
    return isinstance(func_type, numba.core.types.functions.ObjModeDispatcher
        ) or isinstance(func_type, numba.core.types.Dispatcher) and issubclass(
        func_type.dispatcher._compiler.pipeline_class, BodoCompiler)


@register_pass(mutates_CFG=False, analysis_only=True)
class DummyCR(FunctionPass):
    _name = 'bodo_dummy_cr'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        state.cr = (state.func_ir, state.typemap, state.calltypes, state.
            return_type)
        return True


def remove_passes_after(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for xlatp__mtqf, (ofl__mmq, avl__ipniz) in enumerate(pm.passes):
        if ofl__mmq == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:xlatp__mtqf + 1]
    pm._finalized = False


class TyperCompiler(BodoCompiler):

    def define_pipelines(self):
        [pm] = self._create_bodo_pipeline()
        remove_passes_after(pm, InlineOverloads)
        pm.add_pass_after(DummyCR, InlineOverloads)
        pm.finalize()
        return [pm]


def get_func_type_info(func, arg_types, kw_types):
    typingctx = numba.core.registry.cpu_target.typing_context
    targetctx = numba.core.registry.cpu_target.target_context
    brnf__evu = None
    dds__gxgp = None
    _locals = {}
    yhw__peyww = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(yhw__peyww, arg_types,
        kw_types)
    jel__dhzri = numba.core.compiler.Flags()
    nxtbm__nqk = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    rinjk__xac = {'nopython': True, 'boundscheck': False, 'parallel':
        nxtbm__nqk}
    numba.core.registry.cpu_target.options.parse_as_flags(jel__dhzri,
        rinjk__xac)
    pkcgx__uiuow = TyperCompiler(typingctx, targetctx, brnf__evu, args,
        dds__gxgp, jel__dhzri, _locals)
    return pkcgx__uiuow.compile_extra(func)
