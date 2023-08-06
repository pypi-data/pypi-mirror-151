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
        tleha__pdand = 'bodo' if distributed else 'bodo_seq'
        tleha__pdand = (tleha__pdand + '_inline' if inline_calls_pass else
            tleha__pdand)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state,
            tleha__pdand)
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
    for ndu__rnaas, (fsclo__nufv, uhpi__qttyf) in enumerate(pm.passes):
        if fsclo__nufv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(ndu__rnaas, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for ndu__rnaas, (fsclo__nufv, uhpi__qttyf) in enumerate(pm.passes):
        if fsclo__nufv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[ndu__rnaas] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for ndu__rnaas, (fsclo__nufv, uhpi__qttyf) in enumerate(pm.passes):
        if fsclo__nufv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(ndu__rnaas)
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
    fmym__wykrj = guard(get_definition, func_ir, rhs.func)
    if isinstance(fmym__wykrj, (ir.Global, ir.FreeVar, ir.Const)):
        tzjc__fyqhg = fmym__wykrj.value
    else:
        bdts__xaoc = guard(find_callname, func_ir, rhs)
        if not (bdts__xaoc and isinstance(bdts__xaoc[0], str) and
            isinstance(bdts__xaoc[1], str)):
            return
        func_name, func_mod = bdts__xaoc
        try:
            import importlib
            dlpbd__dayog = importlib.import_module(func_mod)
            tzjc__fyqhg = getattr(dlpbd__dayog, func_name)
        except:
            return
    if isinstance(tzjc__fyqhg, CPUDispatcher) and issubclass(tzjc__fyqhg.
        _compiler.pipeline_class, BodoCompiler
        ) and tzjc__fyqhg._compiler.pipeline_class != BodoCompilerUDF:
        tzjc__fyqhg._compiler.pipeline_class = BodoCompilerUDF
        tzjc__fyqhg.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for zde__xaek in block.body:
                if is_call_assign(zde__xaek):
                    _convert_bodo_dispatcher_to_udf(zde__xaek.value, state.
                        func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        qdqy__gzpoi = UntypedPass(state.func_ir, state.typingctx, state.
            args, state.locals, state.metadata, state.flags)
        qdqy__gzpoi.run()
        return True


def _update_definitions(func_ir, node_list):
    zcj__gcqde = ir.Loc('', 0)
    hxsg__gdcr = ir.Block(ir.Scope(None, zcj__gcqde), zcj__gcqde)
    hxsg__gdcr.body = node_list
    build_definitions({(0): hxsg__gdcr}, func_ir._definitions)


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
        lah__fnq = 'overload_series_' + rhs.attr
        zvfc__ehge = getattr(bodo.hiframes.series_impl, lah__fnq)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        lah__fnq = 'overload_dataframe_' + rhs.attr
        zvfc__ehge = getattr(bodo.hiframes.dataframe_impl, lah__fnq)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    uqeez__qgmm = zvfc__ehge(rhs_type)
    igkvx__rjr = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    hlbx__zlzz = compile_func_single_block(uqeez__qgmm, (rhs.value,), stmt.
        target, igkvx__rjr)
    _update_definitions(func_ir, hlbx__zlzz)
    new_body += hlbx__zlzz
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
        xan__uiijy = tuple(typemap[lqmny__ghsll.name] for lqmny__ghsll in
            rhs.args)
        sflh__ykzfp = {tleha__pdand: typemap[lqmny__ghsll.name] for 
            tleha__pdand, lqmny__ghsll in dict(rhs.kws).items()}
        uqeez__qgmm = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*xan__uiijy, **sflh__ykzfp)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        xan__uiijy = tuple(typemap[lqmny__ghsll.name] for lqmny__ghsll in
            rhs.args)
        sflh__ykzfp = {tleha__pdand: typemap[lqmny__ghsll.name] for 
            tleha__pdand, lqmny__ghsll in dict(rhs.kws).items()}
        uqeez__qgmm = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*xan__uiijy, **sflh__ykzfp)
    else:
        return False
    zljyo__ukii = replace_func(pass_info, uqeez__qgmm, rhs.args, pysig=
        numba.core.utils.pysignature(uqeez__qgmm), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    knm__ebwt, uhpi__qttyf = inline_closure_call(func_ir, zljyo__ukii.glbls,
        block, len(new_body), zljyo__ukii.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=zljyo__ukii.arg_types, typemap=
        typemap, calltypes=calltypes, work_list=work_list)
    for enavt__awxvt in knm__ebwt.values():
        enavt__awxvt.loc = rhs.loc
        update_locs(enavt__awxvt.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    abtld__nynv = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = abtld__nynv(func_ir, typemap)
    taw__qrhl = func_ir.blocks
    work_list = list((omvrk__oarf, taw__qrhl[omvrk__oarf]) for omvrk__oarf in
        reversed(taw__qrhl.keys()))
    while work_list:
        uefw__rfxdo, block = work_list.pop()
        new_body = []
        rhqoa__augj = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                bdts__xaoc = guard(find_callname, func_ir, rhs, typemap)
                if bdts__xaoc is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = bdts__xaoc
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    rhqoa__augj = True
                    break
            new_body.append(stmt)
        if not rhqoa__augj:
            taw__qrhl[uefw__rfxdo].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        nkgdp__kqh = DistributedPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.return_type,
            state.metadata, state.flags)
        state.return_type = nkgdp__kqh.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        dea__boz = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        dea__boz.run()
        dea__boz.run()
        dea__boz.run()
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        uie__gph = 0
        xjau__zyqk = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            uie__gph = int(os.environ[xjau__zyqk])
        except:
            pass
        if uie__gph > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(uie__gph, state.
                metadata)
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
        igkvx__rjr = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, igkvx__rjr)
        for block in state.func_ir.blocks.values():
            new_body = []
            for zde__xaek in block.body:
                if type(zde__xaek) in distributed_run_extensions:
                    jpk__vzq = distributed_run_extensions[type(zde__xaek)]
                    yjfl__aiyr = jpk__vzq(zde__xaek, None, state.typemap,
                        state.calltypes, state.typingctx, state.targetctx)
                    new_body += yjfl__aiyr
                elif is_call_assign(zde__xaek):
                    rhs = zde__xaek.value
                    bdts__xaoc = guard(find_callname, state.func_ir, rhs)
                    if bdts__xaoc == ('gatherv', 'bodo') or bdts__xaoc == (
                        'allgatherv', 'bodo'):
                        kwghx__txh = state.typemap[zde__xaek.target.name]
                        kico__pxtd = state.typemap[rhs.args[0].name]
                        if isinstance(kico__pxtd, types.Array) and isinstance(
                            kwghx__txh, types.Array):
                            sshmv__owjng = kico__pxtd.copy(readonly=False)
                            znu__tbzs = kwghx__txh.copy(readonly=False)
                            if sshmv__owjng == znu__tbzs:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), zde__xaek.target, igkvx__rjr)
                                continue
                        if (kwghx__txh != kico__pxtd and 
                            to_str_arr_if_dict_array(kwghx__txh) ==
                            to_str_arr_if_dict_array(kico__pxtd)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), zde__xaek.target,
                                igkvx__rjr, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            zde__xaek.value = rhs.args[0]
                    new_body.append(zde__xaek)
                else:
                    new_body.append(zde__xaek)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        gplc__lhlv = TableColumnDelPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes)
        return gplc__lhlv.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    dvm__mdot = set()
    while work_list:
        uefw__rfxdo, block = work_list.pop()
        dvm__mdot.add(uefw__rfxdo)
        for i, arlz__tst in enumerate(block.body):
            if isinstance(arlz__tst, ir.Assign):
                zbz__wsrnu = arlz__tst.value
                if isinstance(zbz__wsrnu, ir.Expr) and zbz__wsrnu.op == 'call':
                    fmym__wykrj = guard(get_definition, func_ir, zbz__wsrnu
                        .func)
                    if isinstance(fmym__wykrj, (ir.Global, ir.FreeVar)
                        ) and isinstance(fmym__wykrj.value, CPUDispatcher
                        ) and issubclass(fmym__wykrj.value._compiler.
                        pipeline_class, BodoCompiler):
                        gkg__onqw = fmym__wykrj.value.py_func
                        arg_types = None
                        if typingctx:
                            upxwz__oxp = dict(zbz__wsrnu.kws)
                            bge__myobu = tuple(typemap[lqmny__ghsll.name] for
                                lqmny__ghsll in zbz__wsrnu.args)
                            zlfm__thgow = {gxla__xozwn: typemap[
                                lqmny__ghsll.name] for gxla__xozwn,
                                lqmny__ghsll in upxwz__oxp.items()}
                            uhpi__qttyf, arg_types = (fmym__wykrj.value.
                                fold_argument_types(bge__myobu, zlfm__thgow))
                        uhpi__qttyf, uxvd__vjg = inline_closure_call(func_ir,
                            gkg__onqw.__globals__, block, i, gkg__onqw,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((uxvd__vjg[gxla__xozwn].name,
                            lqmny__ghsll) for gxla__xozwn, lqmny__ghsll in
                            fmym__wykrj.value.locals.items() if gxla__xozwn in
                            uxvd__vjg)
                        break
    return dvm__mdot


def udf_jit(signature_or_function=None, **options):
    doony__frkjq = {'comprehension': True, 'setitem': False,
        'inplace_binop': False, 'reduction': True, 'numpy': True, 'stencil':
        False, 'fusion': True}
    return numba.njit(signature_or_function, parallel=doony__frkjq,
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
    for ndu__rnaas, (fsclo__nufv, uhpi__qttyf) in enumerate(pm.passes):
        if fsclo__nufv == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:ndu__rnaas + 1]
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
    rvkk__uejy = None
    loqrt__hah = None
    _locals = {}
    vtlg__wuues = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(vtlg__wuues, arg_types,
        kw_types)
    jfr__uug = numba.core.compiler.Flags()
    ghfce__uqcy = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    pplgk__lge = {'nopython': True, 'boundscheck': False, 'parallel':
        ghfce__uqcy}
    numba.core.registry.cpu_target.options.parse_as_flags(jfr__uug, pplgk__lge)
    buki__rapv = TyperCompiler(typingctx, targetctx, rvkk__uejy, args,
        loqrt__hah, jfr__uug, _locals)
    return buki__rapv.compile_extra(func)
