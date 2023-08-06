"""
Numba monkey patches to fix issues related to Bodo. Should be imported before any
other module in bodo package.
"""
import copy
import functools
import hashlib
import inspect
import itertools
import operator
import os
import re
import sys
import textwrap
import traceback
import types as pytypes
import warnings
from collections import OrderedDict
from collections.abc import Sequence
from contextlib import ExitStack
import numba
import numba.core.boxing
import numba.core.inline_closurecall
import numba.core.typing.listdecl
import numba.np.linalg
from numba.core import analysis, cgutils, errors, ir, ir_utils, types
from numba.core.compiler import Compiler
from numba.core.errors import ForceLiteralArg, LiteralTypingError, TypingError
from numba.core.ir_utils import GuardException, _create_function_from_code_obj, analysis, build_definitions, find_callname, guard, has_no_side_effect, mk_unique_var, remove_dead_extensions, replace_vars_inner, require, visit_vars_extensions, visit_vars_inner
from numba.core.types import literal
from numba.core.types.functions import _bt_as_lines, _ResolutionFailures, _termcolor, _unlit_non_poison
from numba.core.typing.templates import AbstractTemplate, Signature, _EmptyImplementationEntry, _inline_info, _OverloadAttributeTemplate, infer_global, signature
from numba.core.typing.typeof import Purpose, typeof
from numba.experimental.jitclass import base as jitclass_base
from numba.experimental.jitclass import decorators as jitclass_decorators
from numba.extending import NativeValue, lower_builtin, typeof_impl
from numba.parfors.parfor import get_expr_args
from bodo.utils.python_310_bytecode_pass import Bodo310ByteCodePass, peep_hole_call_function_ex_to_call_function_kw, peep_hole_fuse_dict_add_updates
from bodo.utils.typing import BodoError, get_overload_const_str, is_overload_constant_str, raise_bodo_error
_check_numba_change = False
numba.core.typing.templates._IntrinsicTemplate.prefer_literal = True


def run_frontend(func, inline_closures=False, emit_dels=False):
    from numba.core.utils import PYVERSION
    ozkzs__tiuj = numba.core.bytecode.FunctionIdentity.from_function(func)
    bqidu__noezp = numba.core.interpreter.Interpreter(ozkzs__tiuj)
    ttv__xfyby = numba.core.bytecode.ByteCode(func_id=ozkzs__tiuj)
    func_ir = bqidu__noezp.interpret(ttv__xfyby)
    if PYVERSION == (3, 10):
        func_ir = peep_hole_call_function_ex_to_call_function_kw(func_ir)
        func_ir = peep_hole_fuse_dict_add_updates(func_ir)
    if inline_closures:
        from numba.core.inline_closurecall import InlineClosureCallPass


        class DummyPipeline:

            def __init__(self, f_ir):
                self.state = numba.core.compiler.StateDict()
                self.state.typingctx = None
                self.state.targetctx = None
                self.state.args = None
                self.state.func_ir = f_ir
                self.state.typemap = None
                self.state.return_type = None
                self.state.calltypes = None
        numba.core.rewrites.rewrite_registry.apply('before-inference',
            DummyPipeline(func_ir).state)
        yyy__aafp = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        yyy__aafp.run()
    frf__kwt = numba.core.postproc.PostProcessor(func_ir)
    frf__kwt.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, ffxd__ducvt in visit_vars_extensions.items():
        if isinstance(stmt, t):
            ffxd__ducvt(stmt, callback, cbdata)
            return
    if isinstance(stmt, ir.Assign):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Arg):
        stmt.name = visit_vars_inner(stmt.name, callback, cbdata)
    elif isinstance(stmt, ir.Return):
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Raise):
        stmt.exception = visit_vars_inner(stmt.exception, callback, cbdata)
    elif isinstance(stmt, ir.Branch):
        stmt.cond = visit_vars_inner(stmt.cond, callback, cbdata)
    elif isinstance(stmt, ir.Jump):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
    elif isinstance(stmt, ir.Del):
        var = ir.Var(None, stmt.value, stmt.loc)
        var = visit_vars_inner(var, callback, cbdata)
        stmt.value = var.name
    elif isinstance(stmt, ir.DelAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
    elif isinstance(stmt, ir.SetAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.DelItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
    elif isinstance(stmt, ir.StaticSetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index_var = visit_vars_inner(stmt.index_var, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.SetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Print):
        stmt.args = [visit_vars_inner(x, callback, cbdata) for x in stmt.args]
        stmt.vararg = visit_vars_inner(stmt.vararg, callback, cbdata)
    else:
        pass
    return


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.visit_vars_stmt)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '52b7b645ba65c35f3cf564f936e113261db16a2dff1e80fbee2459af58844117':
        warnings.warn('numba.core.ir_utils.visit_vars_stmt has changed')
numba.core.ir_utils.visit_vars_stmt = visit_vars_stmt
old_run_pass = numba.core.typed_passes.InlineOverloads.run_pass


def InlineOverloads_run_pass(self, state):
    import bodo
    bodo.compiler.bodo_overload_inline_pass(state.func_ir, state.typingctx,
        state.targetctx, state.typemap, state.calltypes)
    return old_run_pass(self, state)


numba.core.typed_passes.InlineOverloads.run_pass = InlineOverloads_run_pass
from numba.core.ir_utils import _add_alias, alias_analysis_extensions, alias_func_extensions
_immutable_type_class = (types.Number, types.scalars._NPDatetimeBase, types
    .iterators.RangeType, types.UnicodeType)


def is_immutable_type(var, typemap):
    if typemap is None or var not in typemap:
        return False
    typ = typemap[var]
    if isinstance(typ, _immutable_type_class):
        return True
    if isinstance(typ, types.BaseTuple) and all(isinstance(t,
        _immutable_type_class) for t in typ.types):
        return True
    return False


def find_potential_aliases(blocks, args, typemap, func_ir, alias_map=None,
    arg_aliases=None):
    if alias_map is None:
        alias_map = {}
    if arg_aliases is None:
        arg_aliases = set(a for a in args if not is_immutable_type(a, typemap))
    func_ir._definitions = build_definitions(func_ir.blocks)
    hba__cwbi = ['ravel', 'transpose', 'reshape']
    for rnfas__urdut in blocks.values():
        for ylxly__wxzqv in rnfas__urdut.body:
            if type(ylxly__wxzqv) in alias_analysis_extensions:
                ffxd__ducvt = alias_analysis_extensions[type(ylxly__wxzqv)]
                ffxd__ducvt(ylxly__wxzqv, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(ylxly__wxzqv, ir.Assign):
                vcaxe__rfjzz = ylxly__wxzqv.value
                hgfbn__mql = ylxly__wxzqv.target.name
                if is_immutable_type(hgfbn__mql, typemap):
                    continue
                if isinstance(vcaxe__rfjzz, ir.Var
                    ) and hgfbn__mql != vcaxe__rfjzz.name:
                    _add_alias(hgfbn__mql, vcaxe__rfjzz.name, alias_map,
                        arg_aliases)
                if isinstance(vcaxe__rfjzz, ir.Expr) and (vcaxe__rfjzz.op ==
                    'cast' or vcaxe__rfjzz.op in ['getitem', 'static_getitem']
                    ):
                    _add_alias(hgfbn__mql, vcaxe__rfjzz.value.name,
                        alias_map, arg_aliases)
                if isinstance(vcaxe__rfjzz, ir.Expr
                    ) and vcaxe__rfjzz.op == 'inplace_binop':
                    _add_alias(hgfbn__mql, vcaxe__rfjzz.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(vcaxe__rfjzz, ir.Expr
                    ) and vcaxe__rfjzz.op == 'getattr' and vcaxe__rfjzz.attr in [
                    'T', 'ctypes', 'flat']:
                    _add_alias(hgfbn__mql, vcaxe__rfjzz.value.name,
                        alias_map, arg_aliases)
                if (isinstance(vcaxe__rfjzz, ir.Expr) and vcaxe__rfjzz.op ==
                    'getattr' and vcaxe__rfjzz.attr not in ['shape'] and 
                    vcaxe__rfjzz.value.name in arg_aliases):
                    _add_alias(hgfbn__mql, vcaxe__rfjzz.value.name,
                        alias_map, arg_aliases)
                if isinstance(vcaxe__rfjzz, ir.Expr
                    ) and vcaxe__rfjzz.op == 'getattr' and vcaxe__rfjzz.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(hgfbn__mql, vcaxe__rfjzz.value.name,
                        alias_map, arg_aliases)
                if isinstance(vcaxe__rfjzz, ir.Expr) and vcaxe__rfjzz.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(hgfbn__mql, typemap):
                    for uzup__brwwh in vcaxe__rfjzz.items:
                        _add_alias(hgfbn__mql, uzup__brwwh.name, alias_map,
                            arg_aliases)
                if isinstance(vcaxe__rfjzz, ir.Expr
                    ) and vcaxe__rfjzz.op == 'call':
                    kfeej__vdj = guard(find_callname, func_ir, vcaxe__rfjzz,
                        typemap)
                    if kfeej__vdj is None:
                        continue
                    qdxao__hxc, wnbqo__kjp = kfeej__vdj
                    if kfeej__vdj in alias_func_extensions:
                        uwyi__jpngo = alias_func_extensions[kfeej__vdj]
                        uwyi__jpngo(hgfbn__mql, vcaxe__rfjzz.args,
                            alias_map, arg_aliases)
                    if wnbqo__kjp == 'numpy' and qdxao__hxc in hba__cwbi:
                        _add_alias(hgfbn__mql, vcaxe__rfjzz.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(wnbqo__kjp, ir.Var
                        ) and qdxao__hxc in hba__cwbi:
                        _add_alias(hgfbn__mql, wnbqo__kjp.name, alias_map,
                            arg_aliases)
    ivxqj__ung = copy.deepcopy(alias_map)
    for uzup__brwwh in ivxqj__ung:
        for yflhz__anhp in ivxqj__ung[uzup__brwwh]:
            alias_map[uzup__brwwh] |= alias_map[yflhz__anhp]
        for yflhz__anhp in ivxqj__ung[uzup__brwwh]:
            alias_map[yflhz__anhp] = alias_map[uzup__brwwh]
    return alias_map, arg_aliases


if _check_numba_change:
    lines = inspect.getsource(ir_utils.find_potential_aliases)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e6cf3e0f502f903453eb98346fc6854f87dc4ea1ac62f65c2d6aef3bf690b6c5':
        warnings.warn('ir_utils.find_potential_aliases has changed')
ir_utils.find_potential_aliases = find_potential_aliases
numba.parfors.array_analysis.find_potential_aliases = find_potential_aliases
if _check_numba_change:
    lines = inspect.getsource(ir_utils.dead_code_elimination)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '40a8626300a1a17523944ec7842b093c91258bbc60844bbd72191a35a4c366bf':
        warnings.warn('ir_utils.dead_code_elimination has changed')


def mini_dce(func_ir, typemap=None, alias_map=None, arg_aliases=None):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    cozr__opwpi = compute_cfg_from_blocks(func_ir.blocks)
    egd__pcx = compute_use_defs(func_ir.blocks)
    fqdk__hpux = compute_live_map(cozr__opwpi, func_ir.blocks, egd__pcx.
        usemap, egd__pcx.defmap)
    gzck__dfo = True
    while gzck__dfo:
        gzck__dfo = False
        for rfm__xaha, block in func_ir.blocks.items():
            lives = {uzup__brwwh.name for uzup__brwwh in block.terminator.
                list_vars()}
            for byc__ranpc, ppvc__gnftl in cozr__opwpi.successors(rfm__xaha):
                lives |= fqdk__hpux[byc__ranpc]
            tmpq__jrhmp = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    hgfbn__mql = stmt.target
                    ifpy__dkl = stmt.value
                    if hgfbn__mql.name not in lives:
                        if isinstance(ifpy__dkl, ir.Expr
                            ) and ifpy__dkl.op == 'make_function':
                            continue
                        if isinstance(ifpy__dkl, ir.Expr
                            ) and ifpy__dkl.op == 'getattr':
                            continue
                        if isinstance(ifpy__dkl, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(hgfbn__mql,
                            None), types.Function):
                            continue
                        if isinstance(ifpy__dkl, ir.Expr
                            ) and ifpy__dkl.op == 'build_map':
                            continue
                        if isinstance(ifpy__dkl, ir.Expr
                            ) and ifpy__dkl.op == 'build_tuple':
                            continue
                    if isinstance(ifpy__dkl, ir.Var
                        ) and hgfbn__mql.name == ifpy__dkl.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    xuzgt__kuorm = analysis.ir_extension_usedefs[type(stmt)]
                    iblz__mgrqv, mpvlw__jeb = xuzgt__kuorm(stmt)
                    lives -= mpvlw__jeb
                    lives |= iblz__mgrqv
                else:
                    lives |= {uzup__brwwh.name for uzup__brwwh in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(hgfbn__mql.name)
                tmpq__jrhmp.append(stmt)
            tmpq__jrhmp.reverse()
            if len(block.body) != len(tmpq__jrhmp):
                gzck__dfo = True
            block.body = tmpq__jrhmp


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    pqrt__qmj = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (pqrt__qmj,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    clvu__azqt = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), clvu__azqt)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '7f6974584cb10e49995b652827540cc6732e497c0b9f8231b44fd83fcc1c0a83':
        warnings.warn(
            'numba.core.typing.templates.make_overload_template has changed')
numba.core.typing.templates.make_overload_template = make_overload_template


def _resolve(self, typ, attr):
    if self._attr != attr:
        return None
    if isinstance(typ, types.TypeRef):
        assert typ == self.key
    else:
        assert isinstance(typ, self.key)


    class MethodTemplate(AbstractTemplate):
        key = self.key, attr
        _inline = self._inline
        _no_unliteral = getattr(self, '_no_unliteral', False)
        _overload_func = staticmethod(self._overload_func)
        _inline_overloads = self._inline_overloads
        prefer_literal = self.prefer_literal

        def generic(_, args, kws):
            args = (typ,) + tuple(args)
            fnty = self._get_function_type(self.context, typ)
            sig = self._get_signature(self.context, fnty, args, kws)
            sig = sig.replace(pysig=numba.core.utils.pysignature(self.
                _overload_func))
            for qdi__rmqo in fnty.templates:
                self._inline_overloads.update(qdi__rmqo._inline_overloads)
            if sig is not None:
                return sig.as_method()
    return types.BoundFunction(MethodTemplate, typ)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadMethodTemplate._resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ce8e0935dc939d0867ef969e1ed2975adb3533a58a4133fcc90ae13c4418e4d6':
        warnings.warn(
            'numba.core.typing.templates._OverloadMethodTemplate._resolve has changed'
            )
numba.core.typing.templates._OverloadMethodTemplate._resolve = _resolve


def make_overload_attribute_template(typ, attr, overload_func, inline,
    prefer_literal=False, base=_OverloadAttributeTemplate, **kwargs):
    assert isinstance(typ, types.Type) or issubclass(typ, types.Type)
    name = 'OverloadAttributeTemplate_%s_%s' % (typ, attr)
    no_unliteral = kwargs.pop('no_unliteral', False)
    clvu__azqt = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), clvu__azqt)
    return obj


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_attribute_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f066c38c482d6cf8bf5735a529c3264118ba9b52264b24e58aad12a6b1960f5d':
        warnings.warn(
            'numba.core.typing.templates.make_overload_attribute_template has changed'
            )
numba.core.typing.templates.make_overload_attribute_template = (
    make_overload_attribute_template)


def generic(self, args, kws):
    from numba.core.typed_passes import PreLowerStripPhis
    uadoz__nakl, fxe__hzxd = self._get_impl(args, kws)
    if uadoz__nakl is None:
        return
    wvfet__jmt = types.Dispatcher(uadoz__nakl)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        orq__uahi = uadoz__nakl._compiler
        flags = compiler.Flags()
        qjqpo__spm = orq__uahi.targetdescr.typing_context
        njgpq__rpdf = orq__uahi.targetdescr.target_context
        nqau__fdj = orq__uahi.pipeline_class(qjqpo__spm, njgpq__rpdf, None,
            None, None, flags, None)
        lfck__uoiy = InlineWorker(qjqpo__spm, njgpq__rpdf, orq__uahi.locals,
            nqau__fdj, flags, None)
        mewb__yhyb = wvfet__jmt.dispatcher.get_call_template
        qdi__rmqo, ztvr__esu, foin__luuo, kws = mewb__yhyb(fxe__hzxd, kws)
        if foin__luuo in self._inline_overloads:
            return self._inline_overloads[foin__luuo]['iinfo'].signature
        ir = lfck__uoiy.run_untyped_passes(wvfet__jmt.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, njgpq__rpdf, ir, foin__luuo, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, foin__luuo, None)
        self._inline_overloads[sig.args] = {'folded_args': foin__luuo}
        lwkxc__pequ = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = lwkxc__pequ
        if not self._inline.is_always_inline:
            sig = wvfet__jmt.get_call_type(self.context, fxe__hzxd, kws)
            self._compiled_overloads[sig.args] = wvfet__jmt.get_overload(sig)
        xyk__bzfqk = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': foin__luuo,
            'iinfo': xyk__bzfqk}
    else:
        sig = wvfet__jmt.get_call_type(self.context, fxe__hzxd, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = wvfet__jmt.get_overload(sig)
    return sig


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5d453a6d0215ebf0bab1279ff59eb0040b34938623be99142ce20acc09cdeb64':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate.generic has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate.generic = generic


def bound_function(template_key, no_unliteral=False):

    def wrapper(method_resolver):

        @functools.wraps(method_resolver)
        def attribute_resolver(self, ty):


            class MethodTemplate(AbstractTemplate):
                key = template_key

                def generic(_, args, kws):
                    sig = method_resolver(self, ty, args, kws)
                    if sig is not None and sig.recvr is None:
                        sig = sig.replace(recvr=ty)
                    return sig
            MethodTemplate._no_unliteral = no_unliteral
            return types.BoundFunction(MethodTemplate, ty)
        return attribute_resolver
    return wrapper


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.bound_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a2feefe64eae6a15c56affc47bf0c1d04461f9566913442d539452b397103322':
        warnings.warn('numba.core.typing.templates.bound_function has changed')
numba.core.typing.templates.bound_function = bound_function


def get_call_type(self, context, args, kws):
    from numba.core import utils
    loz__rptnp = [True, False]
    kecvm__xlh = [False, True]
    xrhi__yind = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    kev__kio = get_local_target(context)
    vnu__ocek = utils.order_by_target_specificity(kev__kio, self.templates,
        fnkey=self.key[0])
    self._depth += 1
    for klbpr__ybgqk in vnu__ocek:
        nllly__ozjf = klbpr__ybgqk(context)
        qult__hqmb = loz__rptnp if nllly__ozjf.prefer_literal else kecvm__xlh
        qult__hqmb = [True] if getattr(nllly__ozjf, '_no_unliteral', False
            ) else qult__hqmb
        for bnjhj__gyem in qult__hqmb:
            try:
                if bnjhj__gyem:
                    sig = nllly__ozjf.apply(args, kws)
                else:
                    klk__fnar = tuple([_unlit_non_poison(a) for a in args])
                    duc__dzhfy = {elbkp__vuvnb: _unlit_non_poison(
                        uzup__brwwh) for elbkp__vuvnb, uzup__brwwh in kws.
                        items()}
                    sig = nllly__ozjf.apply(klk__fnar, duc__dzhfy)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    xrhi__yind.add_error(nllly__ozjf, False, e, bnjhj__gyem)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = nllly__ozjf.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    wkrm__ktld = getattr(nllly__ozjf, 'cases', None)
                    if wkrm__ktld is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            wkrm__ktld)
                    else:
                        msg = 'No match.'
                    xrhi__yind.add_error(nllly__ozjf, True, msg, bnjhj__gyem)
    xrhi__yind.raise_error()


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BaseFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '25f038a7216f8e6f40068ea81e11fd9af8ad25d19888f7304a549941b01b7015':
        warnings.warn(
            'numba.core.types.functions.BaseFunction.get_call_type has changed'
            )
numba.core.types.functions.BaseFunction.get_call_type = get_call_type
bodo_typing_error_info = """
This is often caused by the use of unsupported features or typing issues.
See https://docs.bodo.ai/
"""


def get_call_type2(self, context, args, kws):
    qdi__rmqo = self.template(context)
    aqvy__www = None
    rofqu__lmen = None
    uqoh__lixls = None
    qult__hqmb = [True, False] if qdi__rmqo.prefer_literal else [False, True]
    qult__hqmb = [True] if getattr(qdi__rmqo, '_no_unliteral', False
        ) else qult__hqmb
    for bnjhj__gyem in qult__hqmb:
        if bnjhj__gyem:
            try:
                uqoh__lixls = qdi__rmqo.apply(args, kws)
            except Exception as jyvj__rdqgr:
                if isinstance(jyvj__rdqgr, errors.ForceLiteralArg):
                    raise jyvj__rdqgr
                aqvy__www = jyvj__rdqgr
                uqoh__lixls = None
            else:
                break
        else:
            stuc__owz = tuple([_unlit_non_poison(a) for a in args])
            nnnez__eoyzh = {elbkp__vuvnb: _unlit_non_poison(uzup__brwwh) for
                elbkp__vuvnb, uzup__brwwh in kws.items()}
            wxc__cjerl = stuc__owz == args and kws == nnnez__eoyzh
            if not wxc__cjerl and uqoh__lixls is None:
                try:
                    uqoh__lixls = qdi__rmqo.apply(stuc__owz, nnnez__eoyzh)
                except Exception as jyvj__rdqgr:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(
                        jyvj__rdqgr, errors.NumbaError):
                        raise jyvj__rdqgr
                    if isinstance(jyvj__rdqgr, errors.ForceLiteralArg):
                        if qdi__rmqo.prefer_literal:
                            raise jyvj__rdqgr
                    rofqu__lmen = jyvj__rdqgr
                else:
                    break
    if uqoh__lixls is None and (rofqu__lmen is not None or aqvy__www is not
        None):
        ajr__xnlxn = '- Resolution failure for {} arguments:\n{}\n'
        gsz__eqhvc = _termcolor.highlight(ajr__xnlxn)
        if numba.core.config.DEVELOPER_MODE:
            wjbu__qvir = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    mvgd__xckx = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    mvgd__xckx = ['']
                vajd__umvsx = '\n{}'.format(2 * wjbu__qvir)
                wxbu__fei = _termcolor.reset(vajd__umvsx + vajd__umvsx.join
                    (_bt_as_lines(mvgd__xckx)))
                return _termcolor.reset(wxbu__fei)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            jehv__arwbw = str(e)
            jehv__arwbw = jehv__arwbw if jehv__arwbw else str(repr(e)
                ) + add_bt(e)
            sbpqw__xygeu = errors.TypingError(textwrap.dedent(jehv__arwbw))
            return gsz__eqhvc.format(literalness, str(sbpqw__xygeu))
        import bodo
        if isinstance(aqvy__www, bodo.utils.typing.BodoError):
            raise aqvy__www
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', aqvy__www) +
                nested_msg('non-literal', rofqu__lmen))
        else:
            if 'missing a required argument' in aqvy__www.msg:
                msg = 'missing a required argument'
            else:
                msg = 'Compilation error for '
                if isinstance(self.this, bodo.hiframes.pd_dataframe_ext.
                    DataFrameType):
                    msg += 'DataFrame.'
                elif isinstance(self.this, bodo.hiframes.pd_series_ext.
                    SeriesType):
                    msg += 'Series.'
                msg += f'{self.typing_key[1]}().{bodo_typing_error_info}'
            raise errors.TypingError(msg, loc=aqvy__www.loc)
    return uqoh__lixls


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BoundFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '502cd77c0084452e903a45a0f1f8107550bfbde7179363b57dabd617ce135f4a':
        warnings.warn(
            'numba.core.types.functions.BoundFunction.get_call_type has changed'
            )
numba.core.types.functions.BoundFunction.get_call_type = get_call_type2


def string_from_string_and_size(self, string, size):
    from llvmlite import ir as lir
    fnty = lir.FunctionType(self.pyobj, [self.cstring, self.py_ssize_t])
    qdxao__hxc = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=qdxao__hxc)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            dawl__nigcn = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), dawl__nigcn)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    taq__yznr = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            taq__yznr.append(types.Omitted(a.value))
        else:
            taq__yznr.append(self.typeof_pyval(a))
    xdttp__geckt = None
    try:
        error = None
        xdttp__geckt = self.compile(tuple(taq__yznr))
    except errors.ForceLiteralArg as e:
        aezw__fgpa = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if aezw__fgpa:
            spg__yrel = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            qer__iohb = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(aezw__fgpa))
            raise errors.CompilerError(spg__yrel.format(qer__iohb))
        fxe__hzxd = []
        try:
            for i, uzup__brwwh in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        fxe__hzxd.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        fxe__hzxd.append(types.literal(args[i]))
                else:
                    fxe__hzxd.append(args[i])
            args = fxe__hzxd
        except (OSError, FileNotFoundError) as rkdw__rxmp:
            error = FileNotFoundError(str(rkdw__rxmp) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                xdttp__geckt = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        mejsg__weyox = []
        for i, mkeg__trju in enumerate(args):
            val = mkeg__trju.value if isinstance(mkeg__trju, numba.core.
                dispatcher.OmittedArg) else mkeg__trju
            try:
                gzql__vshas = typeof(val, Purpose.argument)
            except ValueError as bljrv__jkaq:
                mejsg__weyox.append((i, str(bljrv__jkaq)))
            else:
                if gzql__vshas is None:
                    mejsg__weyox.append((i,
                        f'cannot determine Numba type of value {val}'))
        if mejsg__weyox:
            watfs__bcq = '\n'.join(f'- argument {i}: {dvj__bgba}' for i,
                dvj__bgba in mejsg__weyox)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{watfs__bcq}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                pme__bruh = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                dmv__tyz = False
                for ddlp__pceij in pme__bruh:
                    if ddlp__pceij in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        dmv__tyz = True
                        break
                if not dmv__tyz:
                    msg = f'{str(e)}'
                msg += '\n' + e.loc.strformat() + '\n'
                e.patch_message(msg)
        error_rewrite(e, 'typing')
    except errors.UnsupportedError as e:
        error_rewrite(e, 'unsupported_error')
    except (errors.NotDefinedError, errors.RedefinedError, errors.
        VerificationError) as e:
        error_rewrite(e, 'interpreter')
    except errors.ConstantInferenceError as e:
        error_rewrite(e, 'constant_inference')
    except bodo.utils.typing.BodoError as e:
        error = bodo.utils.typing.BodoError(str(e))
    except Exception as e:
        if numba.core.config.SHOW_HELP:
            if hasattr(e, 'patch_message'):
                dawl__nigcn = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), dawl__nigcn)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return xdttp__geckt


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher._DispatcherBase.
        _compile_for_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5cdfbf0b13a528abf9f0408e70f67207a03e81d610c26b1acab5b2dc1f79bf06':
        warnings.warn(
            'numba.core.dispatcher._DispatcherBase._compile_for_args has changed'
            )
numba.core.dispatcher._DispatcherBase._compile_for_args = _compile_for_args


def resolve_gb_agg_funcs(cres):
    from bodo.ir.aggregate import gb_agg_cfunc_addr
    for sea__ytnt in cres.library._codegen._engine._defined_symbols:
        if sea__ytnt.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in sea__ytnt and (
            'bodo_gb_udf_update_local' in sea__ytnt or 
            'bodo_gb_udf_combine' in sea__ytnt or 'bodo_gb_udf_eval' in
            sea__ytnt or 'bodo_gb_apply_general_udfs' in sea__ytnt):
            gb_agg_cfunc_addr[sea__ytnt
                ] = cres.library.get_pointer_to_function(sea__ytnt)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for sea__ytnt in cres.library._codegen._engine._defined_symbols:
        if sea__ytnt.startswith('cfunc') and ('get_join_cond_addr' not in
            sea__ytnt or 'bodo_join_gen_cond' in sea__ytnt):
            join_gen_cond_cfunc_addr[sea__ytnt
                ] = cres.library.get_pointer_to_function(sea__ytnt)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    uadoz__nakl = self._get_dispatcher_for_current_target()
    if uadoz__nakl is not self:
        return uadoz__nakl.compile(sig)
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        if not self._can_compile:
            raise RuntimeError('compilation disabled')
        with self._compiling_counter:
            args, return_type = sigutils.normalize_signature(sig)
            gac__ceect = self.overloads.get(tuple(args))
            if gac__ceect is not None:
                return gac__ceect.entry_point
            cres = self._cache.load_overload(sig, self.targetctx)
            if cres is not None:
                resolve_gb_agg_funcs(cres)
                resolve_join_general_cond_funcs(cres)
                self._cache_hits[sig] += 1
                if not cres.objectmode:
                    self.targetctx.insert_user_function(cres.entry_point,
                        cres.fndesc, [cres.library])
                self.add_overload(cres)
                return cres.entry_point
            self._cache_misses[sig] += 1
            mymjs__edl = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=mymjs__edl):
                try:
                    cres = self._compiler.compile(args, return_type)
                except errors.ForceLiteralArg as e:

                    def folded(args, kws):
                        return self._compiler.fold_argument_types(args, kws)[1]
                    raise e.bind_fold_arguments(folded)
                self.add_overload(cres)
            self._cache.save_overload(sig, cres)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.Dispatcher.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '934ec993577ea3b1c7dd2181ac02728abf8559fd42c17062cc821541b092ff8f':
        warnings.warn('numba.core.dispatcher.Dispatcher.compile has changed')
numba.core.dispatcher.Dispatcher.compile = compile


def _get_module_for_linking(self):
    import llvmlite.binding as ll
    self._ensure_finalized()
    if self._shared_module is not None:
        return self._shared_module
    gvwdi__lpl = self._final_module
    paoc__arwe = []
    zgn__vktc = 0
    for fn in gvwdi__lpl.functions:
        zgn__vktc += 1
        if not fn.is_declaration and fn.linkage == ll.Linkage.external:
            if 'get_agg_udf_addr' not in fn.name:
                if 'bodo_gb_udf_update_local' in fn.name:
                    continue
                if 'bodo_gb_udf_combine' in fn.name:
                    continue
                if 'bodo_gb_udf_eval' in fn.name:
                    continue
                if 'bodo_gb_apply_general_udfs' in fn.name:
                    continue
            if 'get_join_cond_addr' not in fn.name:
                if 'bodo_join_gen_cond' in fn.name:
                    continue
            paoc__arwe.append(fn.name)
    if zgn__vktc == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if paoc__arwe:
        gvwdi__lpl = gvwdi__lpl.clone()
        for name in paoc__arwe:
            gvwdi__lpl.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = gvwdi__lpl
    return gvwdi__lpl


if _check_numba_change:
    lines = inspect.getsource(numba.core.codegen.CPUCodeLibrary.
        _get_module_for_linking)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '56dde0e0555b5ec85b93b97c81821bce60784515a1fbf99e4542e92d02ff0a73':
        warnings.warn(
            'numba.core.codegen.CPUCodeLibrary._get_module_for_linking has changed'
            )
numba.core.codegen.CPUCodeLibrary._get_module_for_linking = (
    _get_module_for_linking)


def propagate(self, typeinfer):
    import bodo
    errors = []
    for svevq__ksk in self.constraints:
        loc = svevq__ksk.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                svevq__ksk(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                vihy__ugteb = numba.core.errors.TypingError(str(e), loc=
                    svevq__ksk.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(vihy__ugteb, e))
            except bodo.utils.typing.BodoError as e:
                if loc not in e.locs_in_msg:
                    errors.append(bodo.utils.typing.BodoError(str(e.msg) +
                        '\n' + loc.strformat() + '\n', locs_in_msg=e.
                        locs_in_msg + [loc]))
                else:
                    errors.append(bodo.utils.typing.BodoError(e.msg,
                        locs_in_msg=e.locs_in_msg))
            except Exception as e:
                from numba.core import utils
                if utils.use_old_style_errors():
                    numba.core.typeinfer._logger.debug('captured error',
                        exc_info=e)
                    msg = """Internal error at {con}.
{err}
Enable logging at debug level for details."""
                    vihy__ugteb = numba.core.errors.TypingError(msg.format(
                        con=svevq__ksk, err=str(e)), loc=svevq__ksk.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(vihy__ugteb, e))
                elif utils.use_new_style_errors():
                    raise e
                else:
                    msg = (
                        f"Unknown CAPTURED_ERRORS style: '{numba.core.config.CAPTURED_ERRORS}'."
                        )
                    assert 0, msg
    return errors


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.ConstraintNetwork.propagate)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e73635eeba9ba43cb3372f395b747ae214ce73b729fb0adba0a55237a1cb063':
        warnings.warn(
            'numba.core.typeinfer.ConstraintNetwork.propagate has changed')
numba.core.typeinfer.ConstraintNetwork.propagate = propagate


def raise_error(self):
    import bodo
    for ogxq__wfmsz in self._failures.values():
        for xzh__xjcz in ogxq__wfmsz:
            if isinstance(xzh__xjcz.error, ForceLiteralArg):
                raise xzh__xjcz.error
            if isinstance(xzh__xjcz.error, bodo.utils.typing.BodoError):
                raise xzh__xjcz.error
    raise TypingError(self.format())


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.
        _ResolutionFailures.raise_error)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84b89430f5c8b46cfc684804e6037f00a0f170005cd128ad245551787b2568ea':
        warnings.warn(
            'numba.core.types.functions._ResolutionFailures.raise_error has changed'
            )
numba.core.types.functions._ResolutionFailures.raise_error = raise_error


def bodo_remove_dead_block(block, lives, call_table, arg_aliases, alias_map,
    alias_set, func_ir, typemap):
    from bodo.transforms.distributed_pass import saved_array_analysis
    from bodo.utils.utils import is_array_typ, is_expr
    mufyk__nxxm = False
    tmpq__jrhmp = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        jdns__xijzs = set()
        treua__apvf = lives & alias_set
        for uzup__brwwh in treua__apvf:
            jdns__xijzs |= alias_map[uzup__brwwh]
        lives_n_aliases = lives | jdns__xijzs | arg_aliases
        if type(stmt) in remove_dead_extensions:
            ffxd__ducvt = remove_dead_extensions[type(stmt)]
            stmt = ffxd__ducvt(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                mufyk__nxxm = True
                continue
        if isinstance(stmt, ir.Assign):
            hgfbn__mql = stmt.target
            ifpy__dkl = stmt.value
            if hgfbn__mql.name not in lives and has_no_side_effect(ifpy__dkl,
                lives_n_aliases, call_table):
                mufyk__nxxm = True
                continue
            if saved_array_analysis and hgfbn__mql.name in lives and is_expr(
                ifpy__dkl, 'getattr'
                ) and ifpy__dkl.attr == 'shape' and is_array_typ(typemap[
                ifpy__dkl.value.name]) and ifpy__dkl.value.name not in lives:
                kwwqu__pzyon = {uzup__brwwh: elbkp__vuvnb for elbkp__vuvnb,
                    uzup__brwwh in func_ir.blocks.items()}
                if block in kwwqu__pzyon:
                    rfm__xaha = kwwqu__pzyon[block]
                    niet__oxlt = saved_array_analysis.get_equiv_set(rfm__xaha)
                    liub__bthn = niet__oxlt.get_equiv_set(ifpy__dkl.value)
                    if liub__bthn is not None:
                        for uzup__brwwh in liub__bthn:
                            if uzup__brwwh.endswith('#0'):
                                uzup__brwwh = uzup__brwwh[:-2]
                            if uzup__brwwh in typemap and is_array_typ(typemap
                                [uzup__brwwh]) and uzup__brwwh in lives:
                                ifpy__dkl.value = ir.Var(ifpy__dkl.value.
                                    scope, uzup__brwwh, ifpy__dkl.value.loc)
                                mufyk__nxxm = True
                                break
            if isinstance(ifpy__dkl, ir.Var
                ) and hgfbn__mql.name == ifpy__dkl.name:
                mufyk__nxxm = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                mufyk__nxxm = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            xuzgt__kuorm = analysis.ir_extension_usedefs[type(stmt)]
            iblz__mgrqv, mpvlw__jeb = xuzgt__kuorm(stmt)
            lives -= mpvlw__jeb
            lives |= iblz__mgrqv
        else:
            lives |= {uzup__brwwh.name for uzup__brwwh in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                qmje__hsis = set()
                if isinstance(ifpy__dkl, ir.Expr):
                    qmje__hsis = {uzup__brwwh.name for uzup__brwwh in
                        ifpy__dkl.list_vars()}
                if hgfbn__mql.name not in qmje__hsis:
                    lives.remove(hgfbn__mql.name)
        tmpq__jrhmp.append(stmt)
    tmpq__jrhmp.reverse()
    block.body = tmpq__jrhmp
    return mufyk__nxxm


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            uhpvx__afok, = args
            if isinstance(uhpvx__afok, types.IterableType):
                dtype = uhpvx__afok.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), uhpvx__afok)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    fbswh__dgcof = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (fbswh__dgcof, self.dtype)
    super(types.Set, self).__init__(name=name)


types.Set.__init__ = Set__init__


@lower_builtin(operator.eq, types.UnicodeType, types.UnicodeType)
def eq_str(context, builder, sig, args):
    func = numba.cpython.unicode.unicode_eq(*sig.args)
    return context.compile_internal(builder, func, sig, args)


numba.parfors.parfor.push_call_vars = (lambda blocks, saved_globals,
    saved_getattrs, typemap, nested=False: None)


def maybe_literal(value):
    if isinstance(value, (list, dict, pytypes.FunctionType)):
        return
    if isinstance(value, tuple):
        try:
            return types.Tuple([literal(x) for x in value])
        except LiteralTypingError as vbqb__gcjw:
            return
    try:
        return literal(value)
    except LiteralTypingError as vbqb__gcjw:
        return


if _check_numba_change:
    lines = inspect.getsource(types.maybe_literal)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8fb2fd93acf214b28e33e37d19dc2f7290a42792ec59b650553ac278854b5081':
        warnings.warn('types.maybe_literal has changed')
types.maybe_literal = maybe_literal
types.misc.maybe_literal = maybe_literal


def CacheImpl__init__(self, py_func):
    self._lineno = py_func.__code__.co_firstlineno
    try:
        img__uckz = py_func.__qualname__
    except AttributeError as vbqb__gcjw:
        img__uckz = py_func.__name__
    kzeqz__sra = inspect.getfile(py_func)
    for cls in self._locator_classes:
        cizna__tcvp = cls.from_function(py_func, kzeqz__sra)
        if cizna__tcvp is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (img__uckz, kzeqz__sra))
    self._locator = cizna__tcvp
    oron__ecf = inspect.getfile(py_func)
    jlvdr__dxmp = os.path.splitext(os.path.basename(oron__ecf))[0]
    if kzeqz__sra.startswith('<ipython-'):
        qmlzm__yrs = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', jlvdr__dxmp, count=1)
        if qmlzm__yrs == jlvdr__dxmp:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        jlvdr__dxmp = qmlzm__yrs
    nuyek__vcqe = '%s.%s' % (jlvdr__dxmp, img__uckz)
    vlj__ept = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(nuyek__vcqe, vlj__ept)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    ctrg__bvcm = list(filter(lambda a: self._istuple(a.name), args))
    if len(ctrg__bvcm) == 2 and fn.__name__ == 'add':
        ygaz__xot = self.typemap[ctrg__bvcm[0].name]
        cnvqw__mewsm = self.typemap[ctrg__bvcm[1].name]
        if ygaz__xot.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                ctrg__bvcm[1]))
        if cnvqw__mewsm.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                ctrg__bvcm[0]))
        try:
            dknh__ekcb = [equiv_set.get_shape(x) for x in ctrg__bvcm]
            if None in dknh__ekcb:
                return None
            bzt__ist = sum(dknh__ekcb, ())
            return ArrayAnalysis.AnalyzeResult(shape=bzt__ist)
        except GuardException as vbqb__gcjw:
            return None
    kwxmf__cyiqz = list(filter(lambda a: self._isarray(a.name), args))
    require(len(kwxmf__cyiqz) > 0)
    pbryb__idl = [x.name for x in kwxmf__cyiqz]
    vti__fxnco = [self.typemap[x.name].ndim for x in kwxmf__cyiqz]
    hzdgu__dej = max(vti__fxnco)
    require(hzdgu__dej > 0)
    dknh__ekcb = [equiv_set.get_shape(x) for x in kwxmf__cyiqz]
    if any(a is None for a in dknh__ekcb):
        return ArrayAnalysis.AnalyzeResult(shape=kwxmf__cyiqz[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, kwxmf__cyiqz))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, dknh__ekcb,
        pbryb__idl)


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_broadcast)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6c91fec038f56111338ea2b08f5f0e7f61ebdab1c81fb811fe26658cc354e40f':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast has changed'
            )
numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast = (
    _analyze_broadcast)


def slice_size(self, index, dsize, equiv_set, scope, stmts):
    return None, None


numba.parfors.array_analysis.ArrayAnalysis.slice_size = slice_size


def convert_code_obj_to_function(code_obj, caller_ir):
    import bodo
    pfcgo__sbgk = code_obj.code
    sdqk__tvfij = len(pfcgo__sbgk.co_freevars)
    sto__hgd = pfcgo__sbgk.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        kxev__ndkli, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        sto__hgd = [uzup__brwwh.name for uzup__brwwh in kxev__ndkli]
    vkf__ommqm = caller_ir.func_id.func.__globals__
    try:
        vkf__ommqm = getattr(code_obj, 'globals', vkf__ommqm)
    except KeyError as vbqb__gcjw:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/source/programming_with_bodo/bodo_api_reference/udfs.html"
        )
    miq__ecae = []
    for x in sto__hgd:
        try:
            oikwu__rat = caller_ir.get_definition(x)
        except KeyError as vbqb__gcjw:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(oikwu__rat, (ir.Const, ir.Global, ir.FreeVar)):
            val = oikwu__rat.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                pqrt__qmj = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                vkf__ommqm[pqrt__qmj] = bodo.jit(distributed=False)(val)
                vkf__ommqm[pqrt__qmj].is_nested_func = True
                val = pqrt__qmj
            if isinstance(val, CPUDispatcher):
                pqrt__qmj = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                vkf__ommqm[pqrt__qmj] = val
                val = pqrt__qmj
            miq__ecae.append(val)
        elif isinstance(oikwu__rat, ir.Expr
            ) and oikwu__rat.op == 'make_function':
            xzlyd__bzi = convert_code_obj_to_function(oikwu__rat, caller_ir)
            pqrt__qmj = ir_utils.mk_unique_var('nested_func').replace('.', '_')
            vkf__ommqm[pqrt__qmj] = bodo.jit(distributed=False)(xzlyd__bzi)
            vkf__ommqm[pqrt__qmj].is_nested_func = True
            miq__ecae.append(pqrt__qmj)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    oeo__dgw = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        miq__ecae)])
    euj__ozad = ','.join([('c_%d' % i) for i in range(sdqk__tvfij)])
    zzpkc__zsycd = list(pfcgo__sbgk.co_varnames)
    bsq__ebpix = 0
    yuhib__qtj = pfcgo__sbgk.co_argcount
    jvv__jpby = caller_ir.get_definition(code_obj.defaults)
    if jvv__jpby is not None:
        if isinstance(jvv__jpby, tuple):
            d = [caller_ir.get_definition(x).value for x in jvv__jpby]
            tnq__gkq = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in jvv__jpby.items]
            tnq__gkq = tuple(d)
        bsq__ebpix = len(tnq__gkq)
    oihb__uhzh = yuhib__qtj - bsq__ebpix
    agmwl__ukx = ','.join([('%s' % zzpkc__zsycd[i]) for i in range(oihb__uhzh)]
        )
    if bsq__ebpix:
        bqpf__wogxv = [('%s = %s' % (zzpkc__zsycd[i + oihb__uhzh], tnq__gkq
            [i])) for i in range(bsq__ebpix)]
        agmwl__ukx += ', '
        agmwl__ukx += ', '.join(bqpf__wogxv)
    return _create_function_from_code_obj(pfcgo__sbgk, oeo__dgw, agmwl__ukx,
        euj__ozad, vkf__ommqm)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.convert_code_obj_to_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b840769812418d589460e924a15477e83e7919aac8a3dcb0188ff447344aa8ac':
        warnings.warn(
            'numba.core.ir_utils.convert_code_obj_to_function has changed')
numba.core.ir_utils.convert_code_obj_to_function = convert_code_obj_to_function
numba.core.untyped_passes.convert_code_obj_to_function = (
    convert_code_obj_to_function)


def passmanager_run(self, state):
    from numba.core.compiler import _EarlyPipelineCompletion
    if not self.finalized:
        raise RuntimeError('Cannot run non-finalised pipeline')
    from numba.core.compiler_machinery import CompilerPass, _pass_registry
    import bodo
    for kpbq__qhbmf, (uadc__onwko, rbcue__oiq) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % rbcue__oiq)
            kxvq__rzu = _pass_registry.get(uadc__onwko).pass_inst
            if isinstance(kxvq__rzu, CompilerPass):
                self._runPass(kpbq__qhbmf, kxvq__rzu, state)
            else:
                raise BaseException('Legacy pass in use')
        except _EarlyPipelineCompletion as e:
            raise e
        except bodo.utils.typing.BodoError as e:
            raise
        except Exception as e:
            if numba.core.config.DEVELOPER_MODE:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                msg = 'Failed in %s mode pipeline (step: %s)' % (self.
                    pipeline_name, rbcue__oiq)
                edr__asocl = self._patch_error(msg, e)
                raise edr__asocl
            else:
                raise e


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler_machinery.PassManager.run)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '43505782e15e690fd2d7e53ea716543bec37aa0633502956864edf649e790cdb':
        warnings.warn(
            'numba.core.compiler_machinery.PassManager.run has changed')
numba.core.compiler_machinery.PassManager.run = passmanager_run
if _check_numba_change:
    lines = inspect.getsource(numba.np.ufunc.parallel._launch_threads)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a57ef28c4168fdd436a5513bba4351ebc6d9fba76c5819f44046431a79b9030f':
        warnings.warn('numba.np.ufunc.parallel._launch_threads has changed')
numba.np.ufunc.parallel._launch_threads = lambda : None


def get_reduce_nodes(reduction_node, nodes, func_ir):
    udup__okvgj = None
    mpvlw__jeb = {}

    def lookup(var, already_seen, varonly=True):
        val = mpvlw__jeb.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    mvb__fki = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        hgfbn__mql = stmt.target
        ifpy__dkl = stmt.value
        mpvlw__jeb[hgfbn__mql.name] = ifpy__dkl
        if isinstance(ifpy__dkl, ir.Var) and ifpy__dkl.name in mpvlw__jeb:
            ifpy__dkl = lookup(ifpy__dkl, set())
        if isinstance(ifpy__dkl, ir.Expr):
            oqin__afeu = set(lookup(uzup__brwwh, set(), True).name for
                uzup__brwwh in ifpy__dkl.list_vars())
            if name in oqin__afeu:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(ifpy__dkl)]
                wagtp__qndt = [x for x, fhh__bfu in args if fhh__bfu.name !=
                    name]
                args = [(x, fhh__bfu) for x, fhh__bfu in args if x !=
                    fhh__bfu.name]
                trld__nicyf = dict(args)
                if len(wagtp__qndt) == 1:
                    trld__nicyf[wagtp__qndt[0]] = ir.Var(hgfbn__mql.scope, 
                        name + '#init', hgfbn__mql.loc)
                replace_vars_inner(ifpy__dkl, trld__nicyf)
                udup__okvgj = nodes[i:]
                break
    return udup__okvgj


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_reduce_nodes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a05b52aff9cb02e595a510cd34e973857303a71097fc5530567cb70ca183ef3b':
        warnings.warn('numba.parfors.parfor.get_reduce_nodes has changed')
numba.parfors.parfor.get_reduce_nodes = get_reduce_nodes


def _can_reorder_stmts(stmt, next_stmt, func_ir, call_table, alias_map,
    arg_aliases):
    from numba.parfors.parfor import Parfor, expand_aliases, is_assert_equiv
    if isinstance(stmt, Parfor) and not isinstance(next_stmt, Parfor
        ) and not isinstance(next_stmt, ir.Print) and (not isinstance(
        next_stmt, ir.Assign) or has_no_side_effect(next_stmt.value, set(),
        call_table) or guard(is_assert_equiv, func_ir, next_stmt.value)):
        ymwtu__agjey = expand_aliases({uzup__brwwh.name for uzup__brwwh in
            stmt.list_vars()}, alias_map, arg_aliases)
        dsfj__fvsi = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        omjjk__bdttc = expand_aliases({uzup__brwwh.name for uzup__brwwh in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        lcb__dejil = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(dsfj__fvsi & omjjk__bdttc | lcb__dejil & ymwtu__agjey) == 0:
            return True
    return False


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor._can_reorder_stmts)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '18caa9a01b21ab92b4f79f164cfdbc8574f15ea29deedf7bafdf9b0e755d777c':
        warnings.warn('numba.parfors.parfor._can_reorder_stmts has changed')
numba.parfors.parfor._can_reorder_stmts = _can_reorder_stmts


def get_parfor_writes(parfor, func_ir):
    from numba.parfors.parfor import Parfor
    assert isinstance(parfor, Parfor)
    uyf__qpq = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            uyf__qpq.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                uyf__qpq.update(get_parfor_writes(stmt, func_ir))
    return uyf__qpq


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    uyf__qpq = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        uyf__qpq.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        uyf__qpq = {uzup__brwwh.name for uzup__brwwh in stmt.df_out_vars.
            values()}
        if stmt.out_key_vars is not None:
            uyf__qpq.update({uzup__brwwh.name for uzup__brwwh in stmt.
                out_key_vars})
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        uyf__qpq = {uzup__brwwh.name for uzup__brwwh in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        uyf__qpq = {uzup__brwwh.name for uzup__brwwh in stmt.out_data_vars.
            values()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            uyf__qpq.update({uzup__brwwh.name for uzup__brwwh in stmt.
                out_key_arrs})
            uyf__qpq.update({uzup__brwwh.name for uzup__brwwh in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        kfeej__vdj = guard(find_callname, func_ir, stmt.value)
        if kfeej__vdj in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext')):
            uyf__qpq.add(stmt.value.args[0].name)
        if kfeej__vdj == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            uyf__qpq.add(stmt.value.args[1].name)
    return uyf__qpq


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.get_stmt_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1a7a80b64c9a0eb27e99dc8eaae187bde379d4da0b74c84fbf87296d87939974':
        warnings.warn('numba.core.ir_utils.get_stmt_writes has changed')


def patch_message(self, new_message):
    self.msg = new_message
    self.args = (new_message,) + self.args[1:]


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.patch_message)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ed189a428a7305837e76573596d767b6e840e99f75c05af6941192e0214fa899':
        warnings.warn('numba.core.errors.NumbaError.patch_message has changed')
numba.core.errors.NumbaError.patch_message = patch_message


def add_context(self, msg):
    if numba.core.config.DEVELOPER_MODE:
        self.contexts.append(msg)
        ffxd__ducvt = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        rxats__xqq = ffxd__ducvt.format(self, msg)
        self.args = rxats__xqq,
    else:
        ffxd__ducvt = _termcolor.errmsg('{0}')
        rxats__xqq = ffxd__ducvt.format(self)
        self.args = rxats__xqq,
    return self


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.add_context)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6a388d87788f8432c2152ac55ca9acaa94dbc3b55be973b2cf22dd4ee7179ab8':
        warnings.warn('numba.core.errors.NumbaError.add_context has changed')
numba.core.errors.NumbaError.add_context = add_context


def _get_dist_spec_from_options(spec, **options):
    from bodo.transforms.distributed_analysis import Distribution
    dist_spec = {}
    if 'distributed' in options:
        for pua__agpsv in options['distributed']:
            dist_spec[pua__agpsv] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for pua__agpsv in options['distributed_block']:
            dist_spec[pua__agpsv] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    uwlr__oxpik = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, ftm__hqxci in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(ftm__hqxci)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    sobws__ymh = {}
    for ifieb__nfu in reversed(inspect.getmro(cls)):
        sobws__ymh.update(ifieb__nfu.__dict__)
    kesqg__git, dlmv__fqr, apq__ednxk, xfvbj__retu = {}, {}, {}, {}
    for elbkp__vuvnb, uzup__brwwh in sobws__ymh.items():
        if isinstance(uzup__brwwh, pytypes.FunctionType):
            kesqg__git[elbkp__vuvnb] = uzup__brwwh
        elif isinstance(uzup__brwwh, property):
            dlmv__fqr[elbkp__vuvnb] = uzup__brwwh
        elif isinstance(uzup__brwwh, staticmethod):
            apq__ednxk[elbkp__vuvnb] = uzup__brwwh
        else:
            xfvbj__retu[elbkp__vuvnb] = uzup__brwwh
    ocjn__nfrbc = (set(kesqg__git) | set(dlmv__fqr) | set(apq__ednxk)) & set(
        spec)
    if ocjn__nfrbc:
        raise NameError('name shadowing: {0}'.format(', '.join(ocjn__nfrbc)))
    dpl__zzz = xfvbj__retu.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(xfvbj__retu)
    if xfvbj__retu:
        msg = 'class members are not yet supported: {0}'
        oxk__vscc = ', '.join(xfvbj__retu.keys())
        raise TypeError(msg.format(oxk__vscc))
    for elbkp__vuvnb, uzup__brwwh in dlmv__fqr.items():
        if uzup__brwwh.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(
                elbkp__vuvnb))
    jit_methods = {elbkp__vuvnb: bodo.jit(returns_maybe_distributed=
        uwlr__oxpik)(uzup__brwwh) for elbkp__vuvnb, uzup__brwwh in
        kesqg__git.items()}
    jit_props = {}
    for elbkp__vuvnb, uzup__brwwh in dlmv__fqr.items():
        clvu__azqt = {}
        if uzup__brwwh.fget:
            clvu__azqt['get'] = bodo.jit(uzup__brwwh.fget)
        if uzup__brwwh.fset:
            clvu__azqt['set'] = bodo.jit(uzup__brwwh.fset)
        jit_props[elbkp__vuvnb] = clvu__azqt
    jit_static_methods = {elbkp__vuvnb: bodo.jit(uzup__brwwh.__func__) for 
        elbkp__vuvnb, uzup__brwwh in apq__ednxk.items()}
    nfm__niucr = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    sje__jgil = dict(class_type=nfm__niucr, __doc__=dpl__zzz)
    sje__jgil.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), sje__jgil)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, nfm__niucr)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(nfm__niucr, typingctx, targetctx).register()
    as_numba_type.register(cls, nfm__niucr.instance_type)
    return cls


if _check_numba_change:
    lines = inspect.getsource(jitclass_base.register_class_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '005e6e2e89a47f77a19ba86305565050d4dbc2412fc4717395adf2da348671a9':
        warnings.warn('jitclass_base.register_class_type has changed')
jitclass_base.register_class_type = register_class_type


def ClassType__init__(self, class_def, ctor_template_cls, struct,
    jit_methods, jit_props, jit_static_methods, dist_spec=None):
    if dist_spec is None:
        dist_spec = {}
    self.class_name = class_def.__name__
    self.class_doc = class_def.__doc__
    self._ctor_template_class = ctor_template_cls
    self.jit_methods = jit_methods
    self.jit_props = jit_props
    self.jit_static_methods = jit_static_methods
    self.struct = struct
    self.dist_spec = dist_spec
    eajrw__xfqzw = ','.join('{0}:{1}'.format(elbkp__vuvnb, uzup__brwwh) for
        elbkp__vuvnb, uzup__brwwh in struct.items())
    qkk__fiwpq = ','.join('{0}:{1}'.format(elbkp__vuvnb, uzup__brwwh) for 
        elbkp__vuvnb, uzup__brwwh in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), eajrw__xfqzw, qkk__fiwpq)
    super(types.misc.ClassType, self).__init__(name)


if _check_numba_change:
    lines = inspect.getsource(types.misc.ClassType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2b848ea82946c88f540e81f93ba95dfa7cd66045d944152a337fe2fc43451c30':
        warnings.warn('types.misc.ClassType.__init__ has changed')
types.misc.ClassType.__init__ = ClassType__init__


def jitclass(cls_or_spec=None, spec=None, **options):
    if cls_or_spec is not None and spec is None and not isinstance(cls_or_spec,
        type):
        spec = cls_or_spec
        cls_or_spec = None

    def wrap(cls):
        if numba.core.config.DISABLE_JIT:
            return cls
        else:
            from numba.experimental.jitclass.base import ClassBuilder
            return register_class_type(cls, spec, types.ClassType,
                ClassBuilder, **options)
    if cls_or_spec is None:
        return wrap
    else:
        return wrap(cls_or_spec)


if _check_numba_change:
    lines = inspect.getsource(jitclass_decorators.jitclass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '265f1953ee5881d1a5d90238d3c932cd300732e41495657e65bf51e59f7f4af5':
        warnings.warn('jitclass_decorators.jitclass has changed')


def CallConstraint_resolve(self, typeinfer, typevars, fnty):
    assert fnty
    context = typeinfer.context
    wddwi__kflew = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if wddwi__kflew is None:
        return
    qnu__xkvp, rzzzn__xut = wddwi__kflew
    for a in itertools.chain(qnu__xkvp, rzzzn__xut.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, qnu__xkvp, rzzzn__xut)
    except ForceLiteralArg as e:
        fgl__zuzcw = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(fgl__zuzcw, self.kws)
        saitw__ibnho = set()
        upw__sil = set()
        eeli__wghs = {}
        for kpbq__qhbmf in e.requested_args:
            jwmgo__cdbuw = typeinfer.func_ir.get_definition(folded[kpbq__qhbmf]
                )
            if isinstance(jwmgo__cdbuw, ir.Arg):
                saitw__ibnho.add(jwmgo__cdbuw.index)
                if jwmgo__cdbuw.index in e.file_infos:
                    eeli__wghs[jwmgo__cdbuw.index] = e.file_infos[jwmgo__cdbuw
                        .index]
            else:
                upw__sil.add(kpbq__qhbmf)
        if upw__sil:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif saitw__ibnho:
            raise ForceLiteralArg(saitw__ibnho, loc=self.loc, file_infos=
                eeli__wghs)
    if sig is None:
        dzqqp__qeg = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in qnu__xkvp]
        args += [('%s=%s' % (elbkp__vuvnb, uzup__brwwh)) for elbkp__vuvnb,
            uzup__brwwh in sorted(rzzzn__xut.items())]
        tqgbp__tat = dzqqp__qeg.format(fnty, ', '.join(map(str, args)))
        jqso__uflsh = context.explain_function_type(fnty)
        msg = '\n'.join([tqgbp__tat, jqso__uflsh])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        wepbk__kljcs = context.unify_pairs(sig.recvr, fnty.this)
        if wepbk__kljcs is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if wepbk__kljcs is not None and wepbk__kljcs.is_precise():
            bodor__neoru = fnty.copy(this=wepbk__kljcs)
            typeinfer.propagate_refined_type(self.func, bodor__neoru)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            zxlew__xogdl = target.getone()
            if context.unify_pairs(zxlew__xogdl, sig.return_type
                ) == zxlew__xogdl:
                sig = sig.replace(return_type=zxlew__xogdl)
    self.signature = sig
    self._add_refine_map(typeinfer, typevars, sig)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.CallConstraint.resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c78cd8ffc64b836a6a2ddf0362d481b52b9d380c5249920a87ff4da052ce081f':
        warnings.warn('numba.core.typeinfer.CallConstraint.resolve has changed'
            )
numba.core.typeinfer.CallConstraint.resolve = CallConstraint_resolve


def ForceLiteralArg__init__(self, arg_indices, fold_arguments=None, loc=
    None, file_infos=None):
    super(ForceLiteralArg, self).__init__(
        'Pseudo-exception to force literal arguments in the dispatcher',
        loc=loc)
    self.requested_args = frozenset(arg_indices)
    self.fold_arguments = fold_arguments
    if file_infos is None:
        self.file_infos = {}
    else:
        self.file_infos = file_infos


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b241d5e36a4cf7f4c73a7ad3238693612926606c7a278cad1978070b82fb55ef':
        warnings.warn('numba.core.errors.ForceLiteralArg.__init__ has changed')
numba.core.errors.ForceLiteralArg.__init__ = ForceLiteralArg__init__


def ForceLiteralArg_bind_fold_arguments(self, fold_arguments):
    e = ForceLiteralArg(self.requested_args, fold_arguments, loc=self.loc,
        file_infos=self.file_infos)
    return numba.core.utils.chain_exception(e, self)


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.
        bind_fold_arguments)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e93cca558f7c604a47214a8f2ec33ee994104cb3e5051166f16d7cc9315141d':
        warnings.warn(
            'numba.core.errors.ForceLiteralArg.bind_fold_arguments has changed'
            )
numba.core.errors.ForceLiteralArg.bind_fold_arguments = (
    ForceLiteralArg_bind_fold_arguments)


def ForceLiteralArg_combine(self, other):
    if not isinstance(other, ForceLiteralArg):
        spg__yrel = '*other* must be a {} but got a {} instead'
        raise TypeError(spg__yrel.format(ForceLiteralArg, type(other)))
    return ForceLiteralArg(self.requested_args | other.requested_args,
        file_infos={**self.file_infos, **other.file_infos})


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.combine)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '49bf06612776f5d755c1c7d1c5eb91831a57665a8fed88b5651935f3bf33e899':
        warnings.warn('numba.core.errors.ForceLiteralArg.combine has changed')
numba.core.errors.ForceLiteralArg.combine = ForceLiteralArg_combine


def _get_global_type(self, gv):
    from bodo.utils.typing import FunctionLiteral
    ty = self._lookup_global(gv)
    if ty is not None:
        return ty
    if isinstance(gv, pytypes.ModuleType):
        return types.Module(gv)
    if isinstance(gv, pytypes.FunctionType):
        return FunctionLiteral(gv)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.
        _get_global_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8ffe6b81175d1eecd62a37639b5005514b4477d88f35f5b5395041ac8c945a4a':
        warnings.warn(
            'numba.core.typing.context.BaseContext._get_global_type has changed'
            )
numba.core.typing.context.BaseContext._get_global_type = _get_global_type


def _legalize_args(self, func_ir, args, kwargs, loc, func_globals,
    func_closures):
    from numba.core import sigutils
    from bodo.utils.transform import get_const_value_inner
    if args:
        raise errors.CompilerError(
            "objectmode context doesn't take any positional arguments")
    qzlx__aze = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for elbkp__vuvnb, uzup__brwwh in kwargs.items():
        sblsu__ecu = None
        try:
            jper__effxp = ir.Var(ir.Scope(None, loc), ir_utils.
                mk_unique_var('dummy'), loc)
            func_ir._definitions[jper__effxp.name] = [uzup__brwwh]
            sblsu__ecu = get_const_value_inner(func_ir, jper__effxp)
            func_ir._definitions.pop(jper__effxp.name)
            if isinstance(sblsu__ecu, str):
                sblsu__ecu = sigutils._parse_signature_string(sblsu__ecu)
            if isinstance(sblsu__ecu, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {elbkp__vuvnb} is annotated as type class {sblsu__ecu}."""
                    )
            assert isinstance(sblsu__ecu, types.Type)
            if isinstance(sblsu__ecu, (types.List, types.Set)):
                sblsu__ecu = sblsu__ecu.copy(reflected=False)
            qzlx__aze[elbkp__vuvnb] = sblsu__ecu
        except BodoError as vbqb__gcjw:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(sblsu__ecu, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(uzup__brwwh, ir.Global):
                    msg = f'Global {uzup__brwwh.name!r} is not defined.'
                if isinstance(uzup__brwwh, ir.FreeVar):
                    msg = f'Freevar {uzup__brwwh.name!r} is not defined.'
            if isinstance(uzup__brwwh, ir.Expr
                ) and uzup__brwwh.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=elbkp__vuvnb, msg=msg, loc=loc)
    for name, typ in qzlx__aze.items():
        self._legalize_arg_type(name, typ, loc)
    return qzlx__aze


if _check_numba_change:
    lines = inspect.getsource(numba.core.withcontexts._ObjModeContextType.
        _legalize_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '867c9ba7f1bcf438be56c38e26906bb551f59a99f853a9f68b71208b107c880e':
        warnings.warn(
            'numba.core.withcontexts._ObjModeContextType._legalize_args has changed'
            )
numba.core.withcontexts._ObjModeContextType._legalize_args = _legalize_args


def op_FORMAT_VALUE_byteflow(self, state, inst):
    flags = inst.arg
    if flags & 3 != 0:
        msg = 'str/repr/ascii conversion in f-strings not supported yet'
        raise errors.UnsupportedError(msg, loc=self.get_debug_loc(inst.lineno))
    format_spec = None
    if flags & 4 == 4:
        format_spec = state.pop()
    value = state.pop()
    fmtvar = state.make_temp()
    res = state.make_temp()
    state.append(inst, value=value, res=res, fmtvar=fmtvar, format_spec=
        format_spec)
    state.push(res)


def op_BUILD_STRING_byteflow(self, state, inst):
    rlh__ftoy = inst.arg
    assert rlh__ftoy > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(rlh__ftoy)]))
    tmps = [state.make_temp() for _ in range(rlh__ftoy - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    ojdo__fqhs = ir.Global('format', format, loc=self.loc)
    self.store(value=ojdo__fqhs, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    wch__sozxh = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=wch__sozxh, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    rlh__ftoy = inst.arg
    assert rlh__ftoy > 0, 'invalid BUILD_STRING count'
    cgcql__kpblj = self.get(strings[0])
    for other, rmq__wsnfj in zip(strings[1:], tmps):
        other = self.get(other)
        vcaxe__rfjzz = ir.Expr.binop(operator.add, lhs=cgcql__kpblj, rhs=
            other, loc=self.loc)
        self.store(vcaxe__rfjzz, rmq__wsnfj)
        cgcql__kpblj = self.get(rmq__wsnfj)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    jnz__xaa = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, jnz__xaa])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    xiikj__pema = mk_unique_var(f'{var_name}')
    spvie__nup = xiikj__pema.replace('<', '_').replace('>', '_')
    spvie__nup = spvie__nup.replace('.', '_').replace('$', '_v')
    return spvie__nup


if _check_numba_change:
    lines = inspect.getsource(numba.core.inline_closurecall.
        _created_inlined_var_name)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0d91aac55cd0243e58809afe9d252562f9ae2899cde1112cc01a46804e01821e':
        warnings.warn(
            'numba.core.inline_closurecall._created_inlined_var_name has changed'
            )
numba.core.inline_closurecall._created_inlined_var_name = (
    _created_inlined_var_name)


def resolve_number___call__(self, classty):
    import numpy as np
    from numba.core.typing.templates import make_callable_template
    import bodo
    ty = classty.instance_type
    if isinstance(ty, types.NPDatetime):

        def typer(val1, val2):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(val1,
                'numpy.datetime64')
            if val1 == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
                if not is_overload_constant_str(val2):
                    raise_bodo_error(
                        "datetime64(): 'units' must be a 'str' specifying 'ns'"
                        )
                hwyy__tbwg = get_overload_const_str(val2)
                if hwyy__tbwg != 'ns':
                    raise BodoError("datetime64(): 'units' must be 'ns'")
                return types.NPDatetime('ns')
    else:

        def typer(val):
            if isinstance(val, (types.BaseTuple, types.Sequence)):
                fnty = self.context.resolve_value_type(np.array)
                sig = fnty.get_call_type(self.context, (val, types.DType(ty
                    )), {})
                return sig.return_type
            elif isinstance(val, (types.Number, types.Boolean, types.
                IntEnumMember)):
                return ty
            elif val == types.unicode_type:
                return ty
            elif isinstance(val, (types.NPDatetime, types.NPTimedelta)):
                if ty.bitwidth == 64:
                    return ty
                else:
                    msg = (
                        f'Cannot cast {val} to {ty} as {ty} is not 64 bits wide.'
                        )
                    raise errors.TypingError(msg)
            elif isinstance(val, types.Array
                ) and val.ndim == 0 and val.dtype == ty:
                return ty
            else:
                msg = f'Casting {val} to {ty} directly is unsupported.'
                if isinstance(val, types.Array):
                    msg += f" Try doing '<array>.astype(np.{ty})' instead"
                raise errors.TypingError(msg)
    return types.Function(make_callable_template(key=ty, typer=typer))


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.
        NumberClassAttribute.resolve___call__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdaf0c7d0820130481bb2bd922985257b9281b670f0bafffe10e51cabf0d5081':
        warnings.warn(
            'numba.core.typing.builtins.NumberClassAttribute.resolve___call__ has changed'
            )
numba.core.typing.builtins.NumberClassAttribute.resolve___call__ = (
    resolve_number___call__)


def on_assign(self, states, assign):
    if assign.target.name == states['varname']:
        scope = states['scope']
        ivdx__vbnk = states['defmap']
        if len(ivdx__vbnk) == 0:
            bmfyb__luub = assign.target
            numba.core.ssa._logger.debug('first assign: %s', bmfyb__luub)
            if bmfyb__luub.name not in scope.localvars:
                bmfyb__luub = scope.define(assign.target.name, loc=assign.loc)
        else:
            bmfyb__luub = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=bmfyb__luub, value=assign.value, loc=
            assign.loc)
        ivdx__vbnk[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    invay__sdxv = []
    for elbkp__vuvnb, uzup__brwwh in typing.npydecl.registry.globals:
        if elbkp__vuvnb == func:
            invay__sdxv.append(uzup__brwwh)
    for elbkp__vuvnb, uzup__brwwh in typing.templates.builtin_registry.globals:
        if elbkp__vuvnb == func:
            invay__sdxv.append(uzup__brwwh)
    if len(invay__sdxv) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return invay__sdxv


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    ugme__rcq = {}
    xtjvk__ygxtq = find_topo_order(blocks)
    qycrv__yfqnd = {}
    for rfm__xaha in xtjvk__ygxtq:
        block = blocks[rfm__xaha]
        tmpq__jrhmp = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                hgfbn__mql = stmt.target.name
                ifpy__dkl = stmt.value
                if (ifpy__dkl.op == 'getattr' and ifpy__dkl.attr in
                    arr_math and isinstance(typemap[ifpy__dkl.value.name],
                    types.npytypes.Array)):
                    ifpy__dkl = stmt.value
                    fhzb__ygo = ifpy__dkl.value
                    ugme__rcq[hgfbn__mql] = fhzb__ygo
                    scope = fhzb__ygo.scope
                    loc = fhzb__ygo.loc
                    kbqp__xlovq = ir.Var(scope, mk_unique_var('$np_g_var'), loc
                        )
                    typemap[kbqp__xlovq.name] = types.misc.Module(numpy)
                    sgbor__jek = ir.Global('np', numpy, loc)
                    cjet__vnvm = ir.Assign(sgbor__jek, kbqp__xlovq, loc)
                    ifpy__dkl.value = kbqp__xlovq
                    tmpq__jrhmp.append(cjet__vnvm)
                    func_ir._definitions[kbqp__xlovq.name] = [sgbor__jek]
                    func = getattr(numpy, ifpy__dkl.attr)
                    ldc__lhz = get_np_ufunc_typ_lst(func)
                    qycrv__yfqnd[hgfbn__mql] = ldc__lhz
                if ifpy__dkl.op == 'call' and ifpy__dkl.func.name in ugme__rcq:
                    fhzb__ygo = ugme__rcq[ifpy__dkl.func.name]
                    vyotw__ggs = calltypes.pop(ifpy__dkl)
                    zek__mqug = vyotw__ggs.args[:len(ifpy__dkl.args)]
                    xvnq__mtice = {name: typemap[uzup__brwwh.name] for name,
                        uzup__brwwh in ifpy__dkl.kws}
                    aeao__krj = qycrv__yfqnd[ifpy__dkl.func.name]
                    zvya__qlkou = None
                    for qbp__eav in aeao__krj:
                        try:
                            zvya__qlkou = qbp__eav.get_call_type(typingctx,
                                [typemap[fhzb__ygo.name]] + list(zek__mqug),
                                xvnq__mtice)
                            typemap.pop(ifpy__dkl.func.name)
                            typemap[ifpy__dkl.func.name] = qbp__eav
                            calltypes[ifpy__dkl] = zvya__qlkou
                            break
                        except Exception as vbqb__gcjw:
                            pass
                    if zvya__qlkou is None:
                        raise TypeError(
                            f'No valid template found for {ifpy__dkl.func.name}'
                            )
                    ifpy__dkl.args = [fhzb__ygo] + ifpy__dkl.args
            tmpq__jrhmp.append(stmt)
        block.body = tmpq__jrhmp


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    gkro__cjtbk = ufunc.nin
    tefz__kzpd = ufunc.nout
    oihb__uhzh = ufunc.nargs
    assert oihb__uhzh == gkro__cjtbk + tefz__kzpd
    if len(args) < gkro__cjtbk:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            gkro__cjtbk))
    if len(args) > oihb__uhzh:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), oihb__uhzh)
            )
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    sri__hexhb = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    uoyu__ahdb = max(sri__hexhb)
    sdzvb__dqepv = args[gkro__cjtbk:]
    if not all(d == uoyu__ahdb for d in sri__hexhb[gkro__cjtbk:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(ridye__eapv, types.ArrayCompatible) and not
        isinstance(ridye__eapv, types.Bytes) for ridye__eapv in sdzvb__dqepv):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(ridye__eapv.mutable for ridye__eapv in sdzvb__dqepv):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    dsfkq__iycl = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    kndz__vxkny = None
    if uoyu__ahdb > 0 and len(sdzvb__dqepv) < ufunc.nout:
        kndz__vxkny = 'C'
        jcoen__qpfsn = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in jcoen__qpfsn and 'F' in jcoen__qpfsn:
            kndz__vxkny = 'F'
    return dsfkq__iycl, sdzvb__dqepv, uoyu__ahdb, kndz__vxkny


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.Numpy_rules_ufunc.
        _handle_inputs)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4b97c64ad9c3d50e082538795054f35cf6d2fe962c3ca40e8377a4601b344d5c':
        warnings.warn('Numpy_rules_ufunc._handle_inputs has changed')
numba.core.typing.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)
numba.np.ufunc.dufunc.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)


def DictType__init__(self, keyty, valty, initial_value=None):
    from numba.types import DictType, InitialValue, NoneType, Optional, Tuple, TypeRef, unliteral
    assert not isinstance(keyty, TypeRef)
    assert not isinstance(valty, TypeRef)
    keyty = unliteral(keyty)
    valty = unliteral(valty)
    if isinstance(keyty, (Optional, NoneType)):
        ouob__ccw = 'Dict.key_type cannot be of type {}'
        raise TypingError(ouob__ccw.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        ouob__ccw = 'Dict.value_type cannot be of type {}'
        raise TypingError(ouob__ccw.format(valty))
    self.key_type = keyty
    self.value_type = valty
    self.keyvalue_type = Tuple([keyty, valty])
    name = '{}[{},{}]<iv={}>'.format(self.__class__.__name__, keyty, valty,
        initial_value)
    super(DictType, self).__init__(name)
    InitialValue.__init__(self, initial_value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.DictType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '475acd71224bd51526750343246e064ff071320c0d10c17b8b8ac81d5070d094':
        warnings.warn('DictType.__init__ has changed')
numba.core.types.containers.DictType.__init__ = DictType__init__


def _legalize_arg_types(self, args):
    for i, a in enumerate(args, start=1):
        if isinstance(a, types.Dispatcher):
            msg = (
                'Does not support function type inputs into with-context for arg {}'
                )
            raise errors.TypingError(msg.format(i))


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.ObjModeLiftedWith.
        _legalize_arg_types)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4793f44ebc7da8843e8f298e08cd8a5428b4b84b89fd9d5c650273fdb8fee5ee':
        warnings.warn('ObjModeLiftedWith._legalize_arg_types has changed')
numba.core.dispatcher.ObjModeLiftedWith._legalize_arg_types = (
    _legalize_arg_types)


def _overload_template_get_impl(self, args, kws):
    mrwy__nxoy = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[mrwy__nxoy]
        return impl, args
    except KeyError as vbqb__gcjw:
        pass
    impl, args = self._build_impl(mrwy__nxoy, args, kws)
    return impl, args


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate._get_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4e27d07b214ca16d6e8ed88f70d886b6b095e160d8f77f8df369dd4ed2eb3fae':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate._get_impl has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate._get_impl = (
    _overload_template_get_impl)


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        rel__fnh = find_topo_order(parfor.loop_body)
    fze__zenc = rel__fnh[0]
    ugahy__igctl = {}
    _update_parfor_get_setitems(parfor.loop_body[fze__zenc].body, parfor.
        index_var, alias_map, ugahy__igctl, lives_n_aliases)
    tnwgl__rlevy = set(ugahy__igctl.keys())
    for waa__evfa in rel__fnh:
        if waa__evfa == fze__zenc:
            continue
        for stmt in parfor.loop_body[waa__evfa].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            brqi__zwqqh = set(uzup__brwwh.name for uzup__brwwh in stmt.
                list_vars())
            kyilp__sikc = brqi__zwqqh & tnwgl__rlevy
            for a in kyilp__sikc:
                ugahy__igctl.pop(a, None)
    for waa__evfa in rel__fnh:
        if waa__evfa == fze__zenc:
            continue
        block = parfor.loop_body[waa__evfa]
        lquk__cdat = ugahy__igctl.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            lquk__cdat, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    bjrk__hwmqg = max(blocks.keys())
    yhqh__gswc, mqpns__crc = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    qjk__rdlzv = ir.Jump(yhqh__gswc, ir.Loc('parfors_dummy', -1))
    blocks[bjrk__hwmqg].body.append(qjk__rdlzv)
    cozr__opwpi = compute_cfg_from_blocks(blocks)
    egd__pcx = compute_use_defs(blocks)
    fqdk__hpux = compute_live_map(cozr__opwpi, blocks, egd__pcx.usemap,
        egd__pcx.defmap)
    alias_set = set(alias_map.keys())
    for rfm__xaha, block in blocks.items():
        tmpq__jrhmp = []
        toit__bsnj = {uzup__brwwh.name for uzup__brwwh in block.terminator.
            list_vars()}
        for byc__ranpc, ppvc__gnftl in cozr__opwpi.successors(rfm__xaha):
            toit__bsnj |= fqdk__hpux[byc__ranpc]
        for stmt in reversed(block.body):
            jdns__xijzs = toit__bsnj & alias_set
            for uzup__brwwh in jdns__xijzs:
                toit__bsnj |= alias_map[uzup__brwwh]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in toit__bsnj and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                kfeej__vdj = guard(find_callname, func_ir, stmt.value)
                if kfeej__vdj == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in toit__bsnj and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            toit__bsnj |= {uzup__brwwh.name for uzup__brwwh in stmt.list_vars()
                }
            tmpq__jrhmp.append(stmt)
        tmpq__jrhmp.reverse()
        block.body = tmpq__jrhmp
    typemap.pop(mqpns__crc.name)
    blocks[bjrk__hwmqg].body.pop()

    def trim_empty_parfor_branches(parfor):
        gzck__dfo = False
        blocks = parfor.loop_body.copy()
        for rfm__xaha, block in blocks.items():
            if len(block.body):
                wgywq__fyn = block.body[-1]
                if isinstance(wgywq__fyn, ir.Branch):
                    if len(blocks[wgywq__fyn.truebr].body) == 1 and len(blocks
                        [wgywq__fyn.falsebr].body) == 1:
                        amq__jztvh = blocks[wgywq__fyn.truebr].body[0]
                        bqdn__wsbta = blocks[wgywq__fyn.falsebr].body[0]
                        if isinstance(amq__jztvh, ir.Jump) and isinstance(
                            bqdn__wsbta, ir.Jump
                            ) and amq__jztvh.target == bqdn__wsbta.target:
                            parfor.loop_body[rfm__xaha].body[-1] = ir.Jump(
                                amq__jztvh.target, wgywq__fyn.loc)
                            gzck__dfo = True
                    elif len(blocks[wgywq__fyn.truebr].body) == 1:
                        amq__jztvh = blocks[wgywq__fyn.truebr].body[0]
                        if isinstance(amq__jztvh, ir.Jump
                            ) and amq__jztvh.target == wgywq__fyn.falsebr:
                            parfor.loop_body[rfm__xaha].body[-1] = ir.Jump(
                                amq__jztvh.target, wgywq__fyn.loc)
                            gzck__dfo = True
                    elif len(blocks[wgywq__fyn.falsebr].body) == 1:
                        bqdn__wsbta = blocks[wgywq__fyn.falsebr].body[0]
                        if isinstance(bqdn__wsbta, ir.Jump
                            ) and bqdn__wsbta.target == wgywq__fyn.truebr:
                            parfor.loop_body[rfm__xaha].body[-1] = ir.Jump(
                                bqdn__wsbta.target, wgywq__fyn.loc)
                            gzck__dfo = True
        return gzck__dfo
    gzck__dfo = True
    while gzck__dfo:
        """
        Process parfor body recursively.
        Note that this is the only place in this function that uses the
        argument lives instead of lives_n_aliases.  The former does not
        include the aliases of live variables but only the live variable
        names themselves.  See a comment in this function for how that
        is used.
        """
        remove_dead_parfor_recursive(parfor, lives, arg_aliases, alias_map,
            func_ir, typemap)
        simplify_parfor_body_CFG(func_ir.blocks)
        gzck__dfo = trim_empty_parfor_branches(parfor)
    aiig__rsmg = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        aiig__rsmg &= len(block.body) == 0
    if aiig__rsmg:
        return None
    return parfor


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.remove_dead_parfor)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1c9b008a7ead13e988e1efe67618d8f87f0b9f3d092cc2cd6bfcd806b1fdb859':
        warnings.warn('remove_dead_parfor has changed')
numba.parfors.parfor.remove_dead_parfor = remove_dead_parfor
numba.core.ir_utils.remove_dead_extensions[numba.parfors.parfor.Parfor
    ] = remove_dead_parfor


def simplify_parfor_body_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import simplify_CFG
    from numba.parfors.parfor import Parfor
    vht__rdwfc = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                vht__rdwfc += 1
                parfor = stmt
                zuvm__zsdyk = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = zuvm__zsdyk.scope
                loc = ir.Loc('parfors_dummy', -1)
                cnz__dcjz = ir.Var(scope, mk_unique_var('$const'), loc)
                zuvm__zsdyk.body.append(ir.Assign(ir.Const(0, loc),
                    cnz__dcjz, loc))
                zuvm__zsdyk.body.append(ir.Return(cnz__dcjz, loc))
                cozr__opwpi = compute_cfg_from_blocks(parfor.loop_body)
                for ngrmt__qwd in cozr__opwpi.dead_nodes():
                    del parfor.loop_body[ngrmt__qwd]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                zuvm__zsdyk = parfor.loop_body[max(parfor.loop_body.keys())]
                zuvm__zsdyk.body.pop()
                zuvm__zsdyk.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return vht__rdwfc


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def _lifted_compile(self, sig):
    import numba.core.event as ev
    from numba.core import compiler, sigutils
    from numba.core.compiler_lock import global_compiler_lock
    from numba.core.ir_utils import remove_dels
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        with self._compiling_counter:
            flags = self.flags
            args, return_type = sigutils.normalize_signature(sig)
            gac__ceect = self.overloads.get(tuple(args))
            if gac__ceect is not None:
                return gac__ceect.entry_point
            self._pre_compile(args, return_type, flags)
            vbwji__tzpcu = self.func_ir
            mymjs__edl = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=mymjs__edl):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=vbwji__tzpcu, args=
                    args, return_type=return_type, flags=flags, locals=self
                    .locals, lifted=(), lifted_from=self.lifted_from,
                    is_lifted_loop=True)
                if cres.typing_error is not None and not flags.enable_pyobject:
                    raise cres.typing_error
                self.add_overload(cres)
            remove_dels(self.func_ir.blocks)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.LiftedCode.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1351ebc5d8812dc8da167b30dad30eafb2ca9bf191b49aaed6241c21e03afff1':
        warnings.warn('numba.core.dispatcher.LiftedCode.compile has changed')
numba.core.dispatcher.LiftedCode.compile = _lifted_compile


def compile_ir(typingctx, targetctx, func_ir, args, return_type, flags,
    locals, lifted=(), lifted_from=None, is_lifted_loop=False, library=None,
    pipeline_class=Compiler):
    if is_lifted_loop:
        ywubi__mpe = copy.deepcopy(flags)
        ywubi__mpe.no_rewrites = True

        def compile_local(the_ir, the_flags):
            bvf__hws = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return bvf__hws.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        rdch__nrl = compile_local(func_ir, ywubi__mpe)
        llcry__jpp = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    llcry__jpp = compile_local(func_ir, flags)
                except Exception as vbqb__gcjw:
                    pass
        if llcry__jpp is not None:
            cres = llcry__jpp
        else:
            cres = rdch__nrl
        return cres
    else:
        bvf__hws = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return bvf__hws.compile_ir(func_ir=func_ir, lifted=lifted,
            lifted_from=lifted_from)


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.compile_ir)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c48ce5493f4c43326e8cbdd46f3ea038b2b9045352d9d25894244798388e5e5b':
        warnings.warn('numba.core.compiler.compile_ir has changed')
numba.core.compiler.compile_ir = compile_ir


def make_constant_array(self, builder, typ, ary):
    import math
    from llvmlite import ir as lir
    dlky__lmbg = self.get_data_type(typ.dtype)
    fbgc__mitqx = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        fbgc__mitqx):
        msi__ahyul = ary.ctypes.data
        uanlz__gwujn = self.add_dynamic_addr(builder, msi__ahyul, info=str(
            type(msi__ahyul)))
        euxo__mjcx = self.add_dynamic_addr(builder, id(ary), info=str(type(
            ary)))
        self.global_arrays.append(ary)
    else:
        ihkac__hdjp = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            ihkac__hdjp = ihkac__hdjp.view('int64')
        val = bytearray(ihkac__hdjp.data)
        hxrzb__qdrt = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val
            )
        uanlz__gwujn = cgutils.global_constant(builder, '.const.array.data',
            hxrzb__qdrt)
        uanlz__gwujn.align = self.get_abi_alignment(dlky__lmbg)
        euxo__mjcx = None
    elbaz__ppql = self.get_value_type(types.intp)
    hpt__iubga = [self.get_constant(types.intp, vdiq__oir) for vdiq__oir in
        ary.shape]
    nuqtm__ahyw = lir.Constant(lir.ArrayType(elbaz__ppql, len(hpt__iubga)),
        hpt__iubga)
    avq__jgkhg = [self.get_constant(types.intp, vdiq__oir) for vdiq__oir in
        ary.strides]
    gqyr__fhnms = lir.Constant(lir.ArrayType(elbaz__ppql, len(avq__jgkhg)),
        avq__jgkhg)
    fpfjj__daf = self.get_constant(types.intp, ary.dtype.itemsize)
    anue__yro = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        anue__yro, fpfjj__daf, uanlz__gwujn.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), nuqtm__ahyw, gqyr__fhnms])


if _check_numba_change:
    lines = inspect.getsource(numba.core.base.BaseContext.make_constant_array)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5721b5360b51f782f79bd794f7bf4d48657911ecdc05c30db22fd55f15dad821':
        warnings.warn(
            'numba.core.base.BaseContext.make_constant_array has changed')
numba.core.base.BaseContext.make_constant_array = make_constant_array


def _define_atomic_inc_dec(module, op, ordering):
    from llvmlite import ir as lir
    from numba.core.runtime.nrtdynmod import _word_type
    etj__efmu = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    nneah__oyg = lir.Function(module, etj__efmu, name='nrt_atomic_{0}'.
        format(op))
    [ows__mqov] = nneah__oyg.args
    wdzr__iwi = nneah__oyg.append_basic_block()
    builder = lir.IRBuilder(wdzr__iwi)
    ukx__aibyb = lir.Constant(_word_type, 1)
    if False:
        prny__uacuu = builder.atomic_rmw(op, ows__mqov, ukx__aibyb,
            ordering=ordering)
        res = getattr(builder, op)(prny__uacuu, ukx__aibyb)
        builder.ret(res)
    else:
        prny__uacuu = builder.load(ows__mqov)
        xmw__okv = getattr(builder, op)(prny__uacuu, ukx__aibyb)
        lgxk__unuh = builder.icmp_signed('!=', prny__uacuu, lir.Constant(
            prny__uacuu.type, -1))
        with cgutils.if_likely(builder, lgxk__unuh):
            builder.store(xmw__okv, ows__mqov)
        builder.ret(xmw__okv)
    return nneah__oyg


if _check_numba_change:
    lines = inspect.getsource(numba.core.runtime.nrtdynmod.
        _define_atomic_inc_dec)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9cc02c532b2980b6537b702f5608ea603a1ff93c6d3c785ae2cf48bace273f48':
        warnings.warn(
            'numba.core.runtime.nrtdynmod._define_atomic_inc_dec has changed')
numba.core.runtime.nrtdynmod._define_atomic_inc_dec = _define_atomic_inc_dec


def NativeLowering_run_pass(self, state):
    from llvmlite import binding as llvm
    from numba.core import funcdesc, lowering
    from numba.core.typed_passes import fallback_context
    if state.library is None:
        qebrb__jsr = state.targetctx.codegen()
        state.library = qebrb__jsr.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    bqidu__noezp = state.func_ir
    typemap = state.typemap
    qmpsc__kvx = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    nzuq__sia = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            bqidu__noezp, typemap, qmpsc__kvx, calltypes, mangler=targetctx
            .mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            kuu__zbn = lowering.Lower(targetctx, library, fndesc,
                bqidu__noezp, metadata=metadata)
            kuu__zbn.lower()
            if not flags.no_cpython_wrapper:
                kuu__zbn.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(qmpsc__kvx, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        kuu__zbn.create_cfunc_wrapper()
            env = kuu__zbn.env
            nojjo__mkulp = kuu__zbn.call_helper
            del kuu__zbn
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, nojjo__mkulp, cfunc=None,
                env=env)
        else:
            ulcr__vbw = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(ulcr__vbw, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, nojjo__mkulp, cfunc=
                ulcr__vbw, env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        stazg__plld = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = stazg__plld - nzuq__sia
        metadata['llvm_pass_timings'] = library.recorded_timings
    return True


if _check_numba_change:
    lines = inspect.getsource(numba.core.typed_passes.NativeLowering.run_pass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a777ce6ce1bb2b1cbaa3ac6c2c0e2adab69a9c23888dff5f1cbb67bfb176b5de':
        warnings.warn(
            'numba.core.typed_passes.NativeLowering.run_pass has changed')
numba.core.typed_passes.NativeLowering.run_pass = NativeLowering_run_pass


def _python_list_to_native(typ, obj, c, size, listptr, errorptr):
    from llvmlite import ir as lir
    from numba.core.boxing import _NumbaTypeHelper
    from numba.cpython import listobj

    def check_element_type(nth, itemobj, expected_typobj):
        rbfdf__wuey = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, rbfdf__wuey),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            gxqx__med.do_break()
        ssoe__biu = c.builder.icmp_signed('!=', rbfdf__wuey, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(ssoe__biu, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, rbfdf__wuey)
                c.pyapi.decref(rbfdf__wuey)
                gxqx__med.do_break()
        c.pyapi.decref(rbfdf__wuey)
    kmgp__sonb, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(kmgp__sonb, likely=True) as (qfdub__zaxt,
        svgx__tbdev):
        with qfdub__zaxt:
            list.size = size
            bqodf__snj = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                bqodf__snj), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        bqodf__snj))
                    with cgutils.for_range(c.builder, size) as gxqx__med:
                        itemobj = c.pyapi.list_getitem(obj, gxqx__med.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        lwk__cbngw = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(lwk__cbngw.is_error, likely=
                            False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            gxqx__med.do_break()
                        list.setitem(gxqx__med.index, lwk__cbngw.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with svgx__tbdev:
            c.builder.store(cgutils.true_bit, errorptr)
    with c.builder.if_then(c.builder.load(errorptr)):
        c.context.nrt.decref(c.builder, typ, list.value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.boxing._python_list_to_native)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f8e546df8b07adfe74a16b6aafb1d4fddbae7d3516d7944b3247cc7c9b7ea88a':
        warnings.warn('numba.core.boxing._python_list_to_native has changed')
numba.core.boxing._python_list_to_native = _python_list_to_native


def make_string_from_constant(context, builder, typ, literal_string):
    from llvmlite import ir as lir
    from numba.cpython.hashing import _Py_hash_t
    from numba.cpython.unicode import compile_time_get_string_data
    ceq__vgzl, zpa__sxg, ceaef__gaahc, ajuah__sbozm, agnsx__erywo = (
        compile_time_get_string_data(literal_string))
    gvwdi__lpl = builder.module
    gv = context.insert_const_bytes(gvwdi__lpl, ceq__vgzl)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        zpa__sxg), context.get_constant(types.int32, ceaef__gaahc), context
        .get_constant(types.uint32, ajuah__sbozm), context.get_constant(
        _Py_hash_t, -1), context.get_constant_null(types.MemInfoPointer(
        types.voidptr)), context.get_constant_null(types.pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    dnzdj__oslgd = None
    if isinstance(shape, types.Integer):
        dnzdj__oslgd = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(vdiq__oir, (types.Integer, types.IntEnumMember)) for
            vdiq__oir in shape):
            dnzdj__oslgd = len(shape)
    return dnzdj__oslgd


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.parse_shape)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e62e3ff09d36df5ac9374055947d6a8be27160ce32960d3ef6cb67f89bd16429':
        warnings.warn('numba.core.typing.npydecl.parse_shape has changed')
numba.core.typing.npydecl.parse_shape = parse_shape


def _get_names(self, obj):
    if isinstance(obj, ir.Var) or isinstance(obj, str):
        name = obj if isinstance(obj, str) else obj.name
        if name not in self.typemap:
            return name,
        typ = self.typemap[name]
        if isinstance(typ, (types.BaseTuple, types.ArrayCompatible)):
            dnzdj__oslgd = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if dnzdj__oslgd == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(
                    dnzdj__oslgd))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            pbryb__idl = self._get_names(x)
            if len(pbryb__idl) != 0:
                return pbryb__idl[0]
            return pbryb__idl
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    pbryb__idl = self._get_names(obj)
    if len(pbryb__idl) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(pbryb__idl[0])


def get_equiv_set(self, obj):
    pbryb__idl = self._get_names(obj)
    if len(pbryb__idl) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(pbryb__idl[0])


if _check_numba_change:
    for name, orig, new, hash in ((
        'numba.parfors.array_analysis.ShapeEquivSet._get_names', numba.
        parfors.array_analysis.ShapeEquivSet._get_names, _get_names,
        '8c9bf136109028d5445fd0a82387b6abeb70c23b20b41e2b50c34ba5359516ee'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const',
        numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const,
        get_equiv_const,
        'bef410ca31a9e29df9ee74a4a27d339cc332564e4a237828b8a4decf625ce44e'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set', numba.
        parfors.array_analysis.ShapeEquivSet.get_equiv_set, get_equiv_set,
        'ec936d340c488461122eb74f28a28b88227cb1f1bca2b9ba3c19258cfe1eb40a')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
numba.parfors.array_analysis.ShapeEquivSet._get_names = _get_names
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const = get_equiv_const
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set = get_equiv_set


def raise_on_unsupported_feature(func_ir, typemap):
    import numpy
    zenv__zzjp = []
    for vxgk__bmx in func_ir.arg_names:
        if vxgk__bmx in typemap and isinstance(typemap[vxgk__bmx], types.
            containers.UniTuple) and typemap[vxgk__bmx].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(vxgk__bmx))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for ydz__zdymr in func_ir.blocks.values():
        for stmt in ydz__zdymr.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    mgg__ajjc = getattr(val, 'code', None)
                    if mgg__ajjc is not None:
                        if getattr(val, 'closure', None) is not None:
                            kclvw__naqk = (
                                '<creating a function from a closure>')
                            vcaxe__rfjzz = ''
                        else:
                            kclvw__naqk = mgg__ajjc.co_name
                            vcaxe__rfjzz = '(%s) ' % kclvw__naqk
                    else:
                        kclvw__naqk = '<could not ascertain use case>'
                        vcaxe__rfjzz = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (kclvw__naqk, vcaxe__rfjzz))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                geyh__fcqx = False
                if isinstance(val, pytypes.FunctionType):
                    geyh__fcqx = val in {numba.gdb, numba.gdb_init}
                if not geyh__fcqx:
                    geyh__fcqx = getattr(val, '_name', '') == 'gdb_internal'
                if geyh__fcqx:
                    zenv__zzjp.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    drwp__okgtm = func_ir.get_definition(var)
                    yklx__krnmg = guard(find_callname, func_ir, drwp__okgtm)
                    if yklx__krnmg and yklx__krnmg[1] == 'numpy':
                        ty = getattr(numpy, yklx__krnmg[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    ttjiq__uwhvt = '' if var.startswith('$'
                        ) else "'{}' ".format(var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(ttjiq__uwhvt), loc=stmt.loc)
            if isinstance(stmt.value, ir.Global):
                ty = typemap[stmt.target.name]
                msg = (
                    "The use of a %s type, assigned to variable '%s' in globals, is not supported as globals are considered compile-time constants and there is no known way to compile a %s type as a constant."
                    )
                if isinstance(ty, types.ListType):
                    raise TypingError(msg % (ty, stmt.value.name, ty), loc=
                        stmt.loc)
            if isinstance(stmt.value, ir.Yield) and not func_ir.is_generator:
                msg = 'The use of generator expressions is unsupported.'
                raise errors.UnsupportedError(msg, loc=stmt.loc)
    if len(zenv__zzjp) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        hjrsf__ozwg = '\n'.join([x.strformat() for x in zenv__zzjp])
        raise errors.UnsupportedError(msg % hjrsf__ozwg)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.raise_on_unsupported_feature)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '237a4fe8395a40899279c718bc3754102cd2577463ef2f48daceea78d79b2d5e':
        warnings.warn(
            'numba.core.ir_utils.raise_on_unsupported_feature has changed')
numba.core.ir_utils.raise_on_unsupported_feature = raise_on_unsupported_feature
numba.core.typed_passes.raise_on_unsupported_feature = (
    raise_on_unsupported_feature)


@typeof_impl.register(dict)
def _typeof_dict(val, c):
    if len(val) == 0:
        raise ValueError('Cannot type empty dict')
    elbkp__vuvnb, uzup__brwwh = next(iter(val.items()))
    otkzr__nylwa = typeof_impl(elbkp__vuvnb, c)
    jfqpb__crf = typeof_impl(uzup__brwwh, c)
    if otkzr__nylwa is None or jfqpb__crf is None:
        raise ValueError(
            f'Cannot type dict element type {type(elbkp__vuvnb)}, {type(uzup__brwwh)}'
            )
    return types.DictType(otkzr__nylwa, jfqpb__crf)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    mzab__myf = cgutils.alloca_once_value(c.builder, val)
    zak__lja = c.pyapi.object_hasattr_string(val, '_opaque')
    fzk__mtu = c.builder.icmp_unsigned('==', zak__lja, lir.Constant(
        zak__lja.type, 0))
    hhwjs__petfr = typ.key_type
    cveds__dhtux = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(hhwjs__petfr, cveds__dhtux)

    def copy_dict(out_dict, in_dict):
        for elbkp__vuvnb, uzup__brwwh in in_dict.items():
            out_dict[elbkp__vuvnb] = uzup__brwwh
    with c.builder.if_then(fzk__mtu):
        ocx__gssi = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        eyfln__letix = c.pyapi.call_function_objargs(ocx__gssi, [])
        kimf__zpjtn = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(kimf__zpjtn, [eyfln__letix, val])
        c.builder.store(eyfln__letix, mzab__myf)
    val = c.builder.load(mzab__myf)
    qbhel__nyawo = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    vkcr__kzg = c.pyapi.object_type(val)
    zsa__jqf = c.builder.icmp_unsigned('==', vkcr__kzg, qbhel__nyawo)
    with c.builder.if_else(zsa__jqf) as (xykm__bqqb, vber__itq):
        with xykm__bqqb:
            fbave__mfn = c.pyapi.object_getattr_string(val, '_opaque')
            psez__kes = types.MemInfoPointer(types.voidptr)
            lwk__cbngw = c.unbox(psez__kes, fbave__mfn)
            mi = lwk__cbngw.value
            taq__yznr = psez__kes, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *taq__yznr)
            vnrcu__bolw = context.get_constant_null(taq__yznr[1])
            args = mi, vnrcu__bolw
            gdmqu__dqbcy, aova__vbf = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, aova__vbf)
            c.pyapi.decref(fbave__mfn)
            ssd__kowhl = c.builder.basic_block
        with vber__itq:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", vkcr__kzg, qbhel__nyawo)
            mjzv__bouoi = c.builder.basic_block
    gvnnc__agpwz = c.builder.phi(aova__vbf.type)
    annn__kbh = c.builder.phi(gdmqu__dqbcy.type)
    gvnnc__agpwz.add_incoming(aova__vbf, ssd__kowhl)
    gvnnc__agpwz.add_incoming(aova__vbf.type(None), mjzv__bouoi)
    annn__kbh.add_incoming(gdmqu__dqbcy, ssd__kowhl)
    annn__kbh.add_incoming(cgutils.true_bit, mjzv__bouoi)
    c.pyapi.decref(qbhel__nyawo)
    c.pyapi.decref(vkcr__kzg)
    with c.builder.if_then(fzk__mtu):
        c.pyapi.decref(val)
    return NativeValue(gvnnc__agpwz, is_error=annn__kbh)


import numba.typed.typeddict
if _check_numba_change:
    lines = inspect.getsource(numba.core.pythonapi._unboxers.functions[
        numba.core.types.DictType])
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5f6f183b94dc57838538c668a54c2476576c85d8553843f3219f5162c61e7816':
        warnings.warn('unbox_dicttype has changed')
numba.core.pythonapi._unboxers.functions[types.DictType] = unbox_dicttype


def op_DICT_UPDATE_byteflow(self, state, inst):
    value = state.pop()
    index = inst.arg
    target = state.peek(index)
    updatevar = state.make_temp()
    res = state.make_temp()
    state.append(inst, target=target, value=value, updatevar=updatevar, res=res
        )


if _check_numba_change:
    if hasattr(numba.core.byteflow.TraceRunner, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_DICT_UPDATE has changed')
numba.core.byteflow.TraceRunner.op_DICT_UPDATE = op_DICT_UPDATE_byteflow


def op_DICT_UPDATE_interpreter(self, inst, target, value, updatevar, res):
    from numba.core import ir
    target = self.get(target)
    value = self.get(value)
    lxbg__xvvpk = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=lxbg__xvvpk, name=updatevar)
    trpza__eve = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=trpza__eve, name=res)


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_DICT_UPDATE has changed')
numba.core.interpreter.Interpreter.op_DICT_UPDATE = op_DICT_UPDATE_interpreter


@numba.extending.overload_method(numba.core.types.DictType, 'update')
def ol_dict_update(d, other):
    if not isinstance(d, numba.core.types.DictType):
        return
    if not isinstance(other, numba.core.types.DictType):
        return

    def impl(d, other):
        for elbkp__vuvnb, uzup__brwwh in other.items():
            d[elbkp__vuvnb] = uzup__brwwh
    return impl


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'ol_dict_update'):
        warnings.warn('numba.typed.dictobject.ol_dict_update has changed')


def op_CALL_FUNCTION_EX_byteflow(self, state, inst):
    from numba.core.utils import PYVERSION
    if inst.arg & 1 and PYVERSION != (3, 10):
        errmsg = 'CALL_FUNCTION_EX with **kwargs not supported'
        raise errors.UnsupportedError(errmsg)
    if inst.arg & 1:
        varkwarg = state.pop()
    else:
        varkwarg = None
    vararg = state.pop()
    func = state.pop()
    res = state.make_temp()
    state.append(inst, func=func, vararg=vararg, varkwarg=varkwarg, res=res)
    state.push(res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.byteflow.TraceRunner.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '349e7cfd27f5dab80fe15a7728c5f098f3f225ba8512d84331e39d01e863c6d4':
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX has changed')
numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_byteflow)


def op_CALL_FUNCTION_EX_interpreter(self, inst, func, vararg, varkwarg, res):
    func = self.get(func)
    vararg = self.get(vararg)
    if varkwarg is not None:
        varkwarg = self.get(varkwarg)
    vcaxe__rfjzz = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(vcaxe__rfjzz, res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.interpreter.Interpreter.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84846e5318ab7ccc8f9abaae6ab9e0ca879362648196f9d4b0ffb91cf2e01f5d':
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX has changed'
            )
numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_interpreter)


@classmethod
def ir_expr_call(cls, func, args, kws, loc, vararg=None, varkwarg=None,
    target=None):
    assert isinstance(func, ir.Var)
    assert isinstance(loc, ir.Loc)
    op = 'call'
    return cls(op=op, loc=loc, func=func, args=args, kws=kws, vararg=vararg,
        varkwarg=varkwarg, target=target)


if _check_numba_change:
    lines = inspect.getsource(ir.Expr.call)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '665601d0548d4f648d454492e542cb8aa241107a8df6bc68d0eec664c9ada738':
        warnings.warn('ir.Expr.call has changed')
ir.Expr.call = ir_expr_call


@staticmethod
def define_untyped_pipeline(state, name='untyped'):
    from numba.core.compiler_machinery import PassManager
    from numba.core.untyped_passes import DeadBranchPrune, FindLiterallyCalls, FixupArgs, GenericRewrites, InlineClosureLikes, InlineInlinables, IRProcessing, LiteralPropagationSubPipelinePass, LiteralUnroll, MakeFunctionToJitFunction, ReconstructSSA, RewriteSemanticConstants, TranslateByteCode, WithLifting
    from numba.core.utils import PYVERSION
    bon__nddqc = PassManager(name)
    if state.func_ir is None:
        bon__nddqc.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            bon__nddqc.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        bon__nddqc.add_pass(FixupArgs, 'fix up args')
    bon__nddqc.add_pass(IRProcessing, 'processing IR')
    bon__nddqc.add_pass(WithLifting, 'Handle with contexts')
    bon__nddqc.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        bon__nddqc.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        bon__nddqc.add_pass(DeadBranchPrune, 'dead branch pruning')
        bon__nddqc.add_pass(GenericRewrites, 'nopython rewrites')
    bon__nddqc.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    bon__nddqc.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        bon__nddqc.add_pass(DeadBranchPrune, 'dead branch pruning')
    bon__nddqc.add_pass(FindLiterallyCalls, 'find literally calls')
    bon__nddqc.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        bon__nddqc.add_pass(ReconstructSSA, 'ssa')
    bon__nddqc.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    bon__nddqc.finalize()
    return bon__nddqc


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fc5a0665658cc30588a78aca984ac2d323d5d3a45dce538cc62688530c772896':
        warnings.warn(
            'numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline has changed'
            )
numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline = (
    define_untyped_pipeline)


def mul_list_generic(self, args, kws):
    a, senbl__okmf = args
    if isinstance(a, types.List) and isinstance(senbl__okmf, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(senbl__okmf, types.List):
        return signature(senbl__okmf, types.intp, senbl__okmf)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.listdecl.MulList.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '95882385a8ffa67aa576e8169b9ee6b3197e0ad3d5def4b47fa65ce8cd0f1575':
        warnings.warn('numba.core.typing.listdecl.MulList.generic has changed')
numba.core.typing.listdecl.MulList.generic = mul_list_generic


@lower_builtin(operator.mul, types.Integer, types.List)
def list_mul(context, builder, sig, args):
    from llvmlite import ir as lir
    from numba.core.imputils import impl_ret_new_ref
    from numba.cpython.listobj import ListInstance
    if isinstance(sig.args[0], types.List):
        ebmq__sql, act__bok = 0, 1
    else:
        ebmq__sql, act__bok = 1, 0
    cdqoe__cnnv = ListInstance(context, builder, sig.args[ebmq__sql], args[
        ebmq__sql])
    iblf__ulb = cdqoe__cnnv.size
    rumsu__ffhpn = args[act__bok]
    bqodf__snj = lir.Constant(rumsu__ffhpn.type, 0)
    rumsu__ffhpn = builder.select(cgutils.is_neg_int(builder, rumsu__ffhpn),
        bqodf__snj, rumsu__ffhpn)
    anue__yro = builder.mul(rumsu__ffhpn, iblf__ulb)
    rdzy__cbhl = ListInstance.allocate(context, builder, sig.return_type,
        anue__yro)
    rdzy__cbhl.size = anue__yro
    with cgutils.for_range_slice(builder, bqodf__snj, anue__yro, iblf__ulb,
        inc=True) as (zyvv__ltbqh, _):
        with cgutils.for_range(builder, iblf__ulb) as gxqx__med:
            value = cdqoe__cnnv.getitem(gxqx__med.index)
            rdzy__cbhl.setitem(builder.add(gxqx__med.index, zyvv__ltbqh),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, rdzy__cbhl.value
        )


def unify_pairs(self, first, second):
    from numba.core.typeconv import Conversion
    if first == second:
        return first
    if first is types.undefined:
        return second
    elif second is types.undefined:
        return first
    if first is types.unknown or second is types.unknown:
        return types.unknown
    eclzr__twsk = first.unify(self, second)
    if eclzr__twsk is not None:
        return eclzr__twsk
    eclzr__twsk = second.unify(self, first)
    if eclzr__twsk is not None:
        return eclzr__twsk
    ymbx__oca = self.can_convert(fromty=first, toty=second)
    if ymbx__oca is not None and ymbx__oca <= Conversion.safe:
        return second
    ymbx__oca = self.can_convert(fromty=second, toty=first)
    if ymbx__oca is not None and ymbx__oca <= Conversion.safe:
        return first
    if isinstance(first, types.Literal) or isinstance(second, types.Literal):
        first = types.unliteral(first)
        second = types.unliteral(second)
        return self.unify_pairs(first, second)
    return None


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.unify_pairs
        )
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f0eaf4cfdf1537691de26efd24d7e320f7c3f10d35e9aefe70cb946b3be0008c':
        warnings.warn(
            'numba.core.typing.context.BaseContext.unify_pairs has changed')
numba.core.typing.context.BaseContext.unify_pairs = unify_pairs


def _native_set_to_python_list(typ, payload, c):
    from llvmlite import ir
    anue__yro = payload.used
    listobj = c.pyapi.list_new(anue__yro)
    kmgp__sonb = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(kmgp__sonb, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(anue__yro.
            type, 0))
        with payload._iterate() as gxqx__med:
            i = c.builder.load(index)
            item = gxqx__med.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return kmgp__sonb, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    jowji__avxl = h.type
    njsur__vdm = self.mask
    dtype = self._ty.dtype
    qjqpo__spm = context.typing_context
    fnty = qjqpo__spm.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(qjqpo__spm, (dtype, dtype), {})
    res__gfd = context.get_function(fnty, sig)
    ptzeo__exa = ir.Constant(jowji__avxl, 1)
    bpmm__kjcd = ir.Constant(jowji__avxl, 5)
    beha__luxei = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, njsur__vdm))
    if for_insert:
        rngwe__hjd = njsur__vdm.type(-1)
        pkus__vxc = cgutils.alloca_once_value(builder, rngwe__hjd)
    izvaj__nliyk = builder.append_basic_block('lookup.body')
    tuo__wzn = builder.append_basic_block('lookup.found')
    llmve__rtb = builder.append_basic_block('lookup.not_found')
    kgmaz__ufkbp = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        bveba__gxnr = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, bveba__gxnr)):
            jznfy__uipa = res__gfd(builder, (item, entry.key))
            with builder.if_then(jznfy__uipa):
                builder.branch(tuo__wzn)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, bveba__gxnr)):
            builder.branch(llmve__rtb)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, bveba__gxnr)):
                thdkk__xoes = builder.load(pkus__vxc)
                thdkk__xoes = builder.select(builder.icmp_unsigned('==',
                    thdkk__xoes, rngwe__hjd), i, thdkk__xoes)
                builder.store(thdkk__xoes, pkus__vxc)
    with cgutils.for_range(builder, ir.Constant(jowji__avxl, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, ptzeo__exa)
        i = builder.and_(i, njsur__vdm)
        builder.store(i, index)
    builder.branch(izvaj__nliyk)
    with builder.goto_block(izvaj__nliyk):
        i = builder.load(index)
        check_entry(i)
        rswq__vmj = builder.load(beha__luxei)
        rswq__vmj = builder.lshr(rswq__vmj, bpmm__kjcd)
        i = builder.add(ptzeo__exa, builder.mul(i, bpmm__kjcd))
        i = builder.and_(njsur__vdm, builder.add(i, rswq__vmj))
        builder.store(i, index)
        builder.store(rswq__vmj, beha__luxei)
        builder.branch(izvaj__nliyk)
    with builder.goto_block(llmve__rtb):
        if for_insert:
            i = builder.load(index)
            thdkk__xoes = builder.load(pkus__vxc)
            i = builder.select(builder.icmp_unsigned('==', thdkk__xoes,
                rngwe__hjd), i, thdkk__xoes)
            builder.store(i, index)
        builder.branch(kgmaz__ufkbp)
    with builder.goto_block(tuo__wzn):
        builder.branch(kgmaz__ufkbp)
    builder.position_at_end(kgmaz__ufkbp)
    geyh__fcqx = builder.phi(ir.IntType(1), 'found')
    geyh__fcqx.add_incoming(cgutils.true_bit, tuo__wzn)
    geyh__fcqx.add_incoming(cgutils.false_bit, llmve__rtb)
    return geyh__fcqx, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    kbvmu__jwvsz = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    ljnq__bzx = payload.used
    ptzeo__exa = ir.Constant(ljnq__bzx.type, 1)
    ljnq__bzx = payload.used = builder.add(ljnq__bzx, ptzeo__exa)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, kbvmu__jwvsz), likely=True):
        payload.fill = builder.add(payload.fill, ptzeo__exa)
    if do_resize:
        self.upsize(ljnq__bzx)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    geyh__fcqx, i = payload._lookup(item, h, for_insert=True)
    vzwn__jiub = builder.not_(geyh__fcqx)
    with builder.if_then(vzwn__jiub):
        entry = payload.get_entry(i)
        kbvmu__jwvsz = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        ljnq__bzx = payload.used
        ptzeo__exa = ir.Constant(ljnq__bzx.type, 1)
        ljnq__bzx = payload.used = builder.add(ljnq__bzx, ptzeo__exa)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, kbvmu__jwvsz), likely=True):
            payload.fill = builder.add(payload.fill, ptzeo__exa)
        if do_resize:
            self.upsize(ljnq__bzx)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    ljnq__bzx = payload.used
    ptzeo__exa = ir.Constant(ljnq__bzx.type, 1)
    ljnq__bzx = payload.used = self._builder.sub(ljnq__bzx, ptzeo__exa)
    if do_resize:
        self.downsize(ljnq__bzx)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    ssj__feybx = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, ssj__feybx)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    ivwn__agd = payload
    kmgp__sonb = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(kmgp__sonb), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with ivwn__agd._iterate() as gxqx__med:
        entry = gxqx__med.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(ivwn__agd.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as gxqx__med:
        entry = gxqx__med.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    kmgp__sonb = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(kmgp__sonb), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    kmgp__sonb = cgutils.alloca_once_value(builder, cgutils.true_bit)
    jowji__avxl = context.get_value_type(types.intp)
    bqodf__snj = ir.Constant(jowji__avxl, 0)
    ptzeo__exa = ir.Constant(jowji__avxl, 1)
    taf__jigcb = context.get_data_type(types.SetPayload(self._ty))
    zub__gdnp = context.get_abi_sizeof(taf__jigcb)
    lhfo__waboo = self._entrysize
    zub__gdnp -= lhfo__waboo
    tnudd__hbklk, chl__muwx = cgutils.muladd_with_overflow(builder,
        nentries, ir.Constant(jowji__avxl, lhfo__waboo), ir.Constant(
        jowji__avxl, zub__gdnp))
    with builder.if_then(chl__muwx, likely=False):
        builder.store(cgutils.false_bit, kmgp__sonb)
    with builder.if_then(builder.load(kmgp__sonb), likely=True):
        if realloc:
            fuqfi__nad = self._set.meminfo
            ows__mqov = context.nrt.meminfo_varsize_alloc(builder,
                fuqfi__nad, size=tnudd__hbklk)
            qdkl__wivkl = cgutils.is_null(builder, ows__mqov)
        else:
            mgn__trick = _imp_dtor(context, builder.module, self._ty)
            fuqfi__nad = context.nrt.meminfo_new_varsize_dtor(builder,
                tnudd__hbklk, builder.bitcast(mgn__trick, cgutils.voidptr_t))
            qdkl__wivkl = cgutils.is_null(builder, fuqfi__nad)
        with builder.if_else(qdkl__wivkl, likely=False) as (djuo__jxnnr,
            qfdub__zaxt):
            with djuo__jxnnr:
                builder.store(cgutils.false_bit, kmgp__sonb)
            with qfdub__zaxt:
                if not realloc:
                    self._set.meminfo = fuqfi__nad
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, tnudd__hbklk, 255)
                payload.used = bqodf__snj
                payload.fill = bqodf__snj
                payload.finger = bqodf__snj
                awc__ram = builder.sub(nentries, ptzeo__exa)
                payload.mask = awc__ram
    return builder.load(kmgp__sonb)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    kmgp__sonb = cgutils.alloca_once_value(builder, cgutils.true_bit)
    jowji__avxl = context.get_value_type(types.intp)
    bqodf__snj = ir.Constant(jowji__avxl, 0)
    ptzeo__exa = ir.Constant(jowji__avxl, 1)
    taf__jigcb = context.get_data_type(types.SetPayload(self._ty))
    zub__gdnp = context.get_abi_sizeof(taf__jigcb)
    lhfo__waboo = self._entrysize
    zub__gdnp -= lhfo__waboo
    njsur__vdm = src_payload.mask
    nentries = builder.add(ptzeo__exa, njsur__vdm)
    tnudd__hbklk = builder.add(ir.Constant(jowji__avxl, zub__gdnp), builder
        .mul(ir.Constant(jowji__avxl, lhfo__waboo), nentries))
    with builder.if_then(builder.load(kmgp__sonb), likely=True):
        mgn__trick = _imp_dtor(context, builder.module, self._ty)
        fuqfi__nad = context.nrt.meminfo_new_varsize_dtor(builder,
            tnudd__hbklk, builder.bitcast(mgn__trick, cgutils.voidptr_t))
        qdkl__wivkl = cgutils.is_null(builder, fuqfi__nad)
        with builder.if_else(qdkl__wivkl, likely=False) as (djuo__jxnnr,
            qfdub__zaxt):
            with djuo__jxnnr:
                builder.store(cgutils.false_bit, kmgp__sonb)
            with qfdub__zaxt:
                self._set.meminfo = fuqfi__nad
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = bqodf__snj
                payload.mask = njsur__vdm
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, lhfo__waboo)
                with src_payload._iterate() as gxqx__med:
                    context.nrt.incref(builder, self._ty.dtype, gxqx__med.
                        entry.key)
    return builder.load(kmgp__sonb)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    zgywv__uqd = context.get_value_type(types.voidptr)
    aute__jsaec = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [zgywv__uqd, aute__jsaec, zgywv__uqd]
        )
    qdxao__hxc = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=qdxao__hxc)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        lvl__ajko = builder.bitcast(fn.args[0], cgutils.voidptr_t.as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, lvl__ajko)
        with payload._iterate() as gxqx__med:
            entry = gxqx__med.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    ggpyw__iuma, = sig.args
    kxev__ndkli, = args
    qxkdf__elsj = numba.core.imputils.call_len(context, builder,
        ggpyw__iuma, kxev__ndkli)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, qxkdf__elsj)
    with numba.core.imputils.for_iter(context, builder, ggpyw__iuma,
        kxev__ndkli) as gxqx__med:
        inst.add(gxqx__med.value)
        context.nrt.decref(builder, set_type.dtype, gxqx__med.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    ggpyw__iuma = sig.args[1]
    kxev__ndkli = args[1]
    qxkdf__elsj = numba.core.imputils.call_len(context, builder,
        ggpyw__iuma, kxev__ndkli)
    if qxkdf__elsj is not None:
        jruqi__qxmuz = builder.add(inst.payload.used, qxkdf__elsj)
        inst.upsize(jruqi__qxmuz)
    with numba.core.imputils.for_iter(context, builder, ggpyw__iuma,
        kxev__ndkli) as gxqx__med:
        ezjt__xujh = context.cast(builder, gxqx__med.value, ggpyw__iuma.
            dtype, inst.dtype)
        inst.add(ezjt__xujh)
        context.nrt.decref(builder, ggpyw__iuma.dtype, gxqx__med.value)
    if qxkdf__elsj is not None:
        inst.downsize(inst.payload.used)
    return context.get_dummy_value()


if _check_numba_change:
    for name, orig, hash in ((
        'numba.core.boxing._native_set_to_python_list', numba.core.boxing.
        _native_set_to_python_list,
        'b47f3d5e582c05d80899ee73e1c009a7e5121e7a660d42cb518bb86933f3c06f'),
        ('numba.cpython.setobj._SetPayload._lookup', numba.cpython.setobj.
        _SetPayload._lookup,
        'c797b5399d7b227fe4eea3a058b3d3103f59345699388afb125ae47124bee395'),
        ('numba.cpython.setobj.SetInstance._add_entry', numba.cpython.
        setobj.SetInstance._add_entry,
        'c5ed28a5fdb453f242e41907cb792b66da2df63282c17abe0b68fc46782a7f94'),
        ('numba.cpython.setobj.SetInstance._add_key', numba.cpython.setobj.
        SetInstance._add_key,
        '324d6172638d02a361cfa0ca7f86e241e5a56a008d4ab581a305f9ae5ea4a75f'),
        ('numba.cpython.setobj.SetInstance._remove_entry', numba.cpython.
        setobj.SetInstance._remove_entry,
        '2c441b00daac61976e673c0e738e8e76982669bd2851951890dd40526fa14da1'),
        ('numba.cpython.setobj.SetInstance.pop', numba.cpython.setobj.
        SetInstance.pop,
        '1a7b7464cbe0577f2a38f3af9acfef6d4d25d049b1e216157275fbadaab41d1b'),
        ('numba.cpython.setobj.SetInstance._resize', numba.cpython.setobj.
        SetInstance._resize,
        '5ca5c2ba4f8c4bf546fde106b9c2656d4b22a16d16e163fb64c5d85ea4d88746'),
        ('numba.cpython.setobj.SetInstance._replace_payload', numba.cpython
        .setobj.SetInstance._replace_payload,
        'ada75a6c85828bff69c8469538c1979801f560a43fb726221a9c21bf208ae78d'),
        ('numba.cpython.setobj.SetInstance._allocate_payload', numba.
        cpython.setobj.SetInstance._allocate_payload,
        '2e80c419df43ebc71075b4f97fc1701c10dbc576aed248845e176b8d5829e61b'),
        ('numba.cpython.setobj.SetInstance._copy_payload', numba.cpython.
        setobj.SetInstance._copy_payload,
        '0885ac36e1eb5a0a0fc4f5d91e54b2102b69e536091fed9f2610a71d225193ec'),
        ('numba.cpython.setobj.set_constructor', numba.cpython.setobj.
        set_constructor,
        '3d521a60c3b8eaf70aa0f7267427475dfddd8f5e5053b5bfe309bb5f1891b0ce'),
        ('numba.cpython.setobj.set_update', numba.cpython.setobj.set_update,
        '965c4f7f7abcea5cbe0491b602e6d4bcb1800fa1ec39b1ffccf07e1bc56051c3')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.boxing._native_set_to_python_list = _native_set_to_python_list
numba.cpython.setobj._SetPayload._lookup = _lookup
numba.cpython.setobj.SetInstance._add_entry = _add_entry
numba.cpython.setobj.SetInstance._add_key = _add_key
numba.cpython.setobj.SetInstance._remove_entry = _remove_entry
numba.cpython.setobj.SetInstance.pop = pop
numba.cpython.setobj.SetInstance._resize = _resize
numba.cpython.setobj.SetInstance._replace_payload = _replace_payload
numba.cpython.setobj.SetInstance._allocate_payload = _allocate_payload
numba.cpython.setobj.SetInstance._copy_payload = _copy_payload


def _reduce(self):
    libdata = self.library.serialize_using_object_code()
    typeann = str(self.type_annotation)
    fndesc = self.fndesc
    fndesc.typemap = fndesc.calltypes = None
    referenced_envs = self._find_referenced_environments()
    hdnus__gszsx = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, hdnus__gszsx, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    ulcr__vbw = target_context.get_executable(library, fndesc, env)
    crmel__jdtu = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=ulcr__vbw, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return crmel__jdtu


if _check_numba_change:
    for name, orig, hash in (('numba.core.compiler.CompileResult._reduce',
        numba.core.compiler.CompileResult._reduce,
        '5f86eacfa5202c202b3dc200f1a7a9b6d3f9d1ec16d43a52cb2d580c34fbfa82'),
        ('numba.core.compiler.CompileResult._rebuild', numba.core.compiler.
        CompileResult._rebuild,
        '44fa9dc2255883ab49195d18c3cca8c0ad715d0dd02033bd7e2376152edc4e84')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.compiler.CompileResult._reduce = _reduce
numba.core.compiler.CompileResult._rebuild = _rebuild
