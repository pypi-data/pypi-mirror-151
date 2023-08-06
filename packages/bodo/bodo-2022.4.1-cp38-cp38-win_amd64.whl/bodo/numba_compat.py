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
    fthvn__pzytp = numba.core.bytecode.FunctionIdentity.from_function(func)
    mwur__tlum = numba.core.interpreter.Interpreter(fthvn__pzytp)
    oclh__lij = numba.core.bytecode.ByteCode(func_id=fthvn__pzytp)
    func_ir = mwur__tlum.interpret(oclh__lij)
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
        heiev__nlci = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        heiev__nlci.run()
    hla__auc = numba.core.postproc.PostProcessor(func_ir)
    hla__auc.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, qcxiw__zwyy in visit_vars_extensions.items():
        if isinstance(stmt, t):
            qcxiw__zwyy(stmt, callback, cbdata)
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
    cmrya__ybaq = ['ravel', 'transpose', 'reshape']
    for ojsy__flvkd in blocks.values():
        for cckga__cjbpd in ojsy__flvkd.body:
            if type(cckga__cjbpd) in alias_analysis_extensions:
                qcxiw__zwyy = alias_analysis_extensions[type(cckga__cjbpd)]
                qcxiw__zwyy(cckga__cjbpd, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(cckga__cjbpd, ir.Assign):
                nqt__bttm = cckga__cjbpd.value
                lroso__zgtso = cckga__cjbpd.target.name
                if is_immutable_type(lroso__zgtso, typemap):
                    continue
                if isinstance(nqt__bttm, ir.Var
                    ) and lroso__zgtso != nqt__bttm.name:
                    _add_alias(lroso__zgtso, nqt__bttm.name, alias_map,
                        arg_aliases)
                if isinstance(nqt__bttm, ir.Expr) and (nqt__bttm.op ==
                    'cast' or nqt__bttm.op in ['getitem', 'static_getitem']):
                    _add_alias(lroso__zgtso, nqt__bttm.value.name,
                        alias_map, arg_aliases)
                if isinstance(nqt__bttm, ir.Expr
                    ) and nqt__bttm.op == 'inplace_binop':
                    _add_alias(lroso__zgtso, nqt__bttm.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(nqt__bttm, ir.Expr
                    ) and nqt__bttm.op == 'getattr' and nqt__bttm.attr in ['T',
                    'ctypes', 'flat']:
                    _add_alias(lroso__zgtso, nqt__bttm.value.name,
                        alias_map, arg_aliases)
                if isinstance(nqt__bttm, ir.Expr
                    ) and nqt__bttm.op == 'getattr' and nqt__bttm.attr not in [
                    'shape'] and nqt__bttm.value.name in arg_aliases:
                    _add_alias(lroso__zgtso, nqt__bttm.value.name,
                        alias_map, arg_aliases)
                if isinstance(nqt__bttm, ir.Expr
                    ) and nqt__bttm.op == 'getattr' and nqt__bttm.attr in (
                    'loc', 'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(lroso__zgtso, nqt__bttm.value.name,
                        alias_map, arg_aliases)
                if isinstance(nqt__bttm, ir.Expr) and nqt__bttm.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(lroso__zgtso, typemap):
                    for eiy__rqh in nqt__bttm.items:
                        _add_alias(lroso__zgtso, eiy__rqh.name, alias_map,
                            arg_aliases)
                if isinstance(nqt__bttm, ir.Expr) and nqt__bttm.op == 'call':
                    tjm__ggz = guard(find_callname, func_ir, nqt__bttm, typemap
                        )
                    if tjm__ggz is None:
                        continue
                    kzgt__omxtl, vqjbi__wtj = tjm__ggz
                    if tjm__ggz in alias_func_extensions:
                        egcu__zvgd = alias_func_extensions[tjm__ggz]
                        egcu__zvgd(lroso__zgtso, nqt__bttm.args, alias_map,
                            arg_aliases)
                    if vqjbi__wtj == 'numpy' and kzgt__omxtl in cmrya__ybaq:
                        _add_alias(lroso__zgtso, nqt__bttm.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(vqjbi__wtj, ir.Var
                        ) and kzgt__omxtl in cmrya__ybaq:
                        _add_alias(lroso__zgtso, vqjbi__wtj.name, alias_map,
                            arg_aliases)
    akrpz__blr = copy.deepcopy(alias_map)
    for eiy__rqh in akrpz__blr:
        for mbxzz__lmhyi in akrpz__blr[eiy__rqh]:
            alias_map[eiy__rqh] |= alias_map[mbxzz__lmhyi]
        for mbxzz__lmhyi in akrpz__blr[eiy__rqh]:
            alias_map[mbxzz__lmhyi] = alias_map[eiy__rqh]
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
    rwlo__paxn = compute_cfg_from_blocks(func_ir.blocks)
    kgb__jqffs = compute_use_defs(func_ir.blocks)
    ofbfh__wceq = compute_live_map(rwlo__paxn, func_ir.blocks, kgb__jqffs.
        usemap, kgb__jqffs.defmap)
    sxh__migmz = True
    while sxh__migmz:
        sxh__migmz = False
        for dboh__cva, block in func_ir.blocks.items():
            lives = {eiy__rqh.name for eiy__rqh in block.terminator.list_vars()
                }
            for pciig__muq, ajsc__eth in rwlo__paxn.successors(dboh__cva):
                lives |= ofbfh__wceq[pciig__muq]
            rkqy__pcbra = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    lroso__zgtso = stmt.target
                    ykc__elsh = stmt.value
                    if lroso__zgtso.name not in lives:
                        if isinstance(ykc__elsh, ir.Expr
                            ) and ykc__elsh.op == 'make_function':
                            continue
                        if isinstance(ykc__elsh, ir.Expr
                            ) and ykc__elsh.op == 'getattr':
                            continue
                        if isinstance(ykc__elsh, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(lroso__zgtso,
                            None), types.Function):
                            continue
                        if isinstance(ykc__elsh, ir.Expr
                            ) and ykc__elsh.op == 'build_map':
                            continue
                        if isinstance(ykc__elsh, ir.Expr
                            ) and ykc__elsh.op == 'build_tuple':
                            continue
                    if isinstance(ykc__elsh, ir.Var
                        ) and lroso__zgtso.name == ykc__elsh.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    big__ifhf = analysis.ir_extension_usedefs[type(stmt)]
                    kblyl__qkyf, xpd__dqkc = big__ifhf(stmt)
                    lives -= xpd__dqkc
                    lives |= kblyl__qkyf
                else:
                    lives |= {eiy__rqh.name for eiy__rqh in stmt.list_vars()}
                    if isinstance(stmt, ir.Assign):
                        lives.remove(lroso__zgtso.name)
                rkqy__pcbra.append(stmt)
            rkqy__pcbra.reverse()
            if len(block.body) != len(rkqy__pcbra):
                sxh__migmz = True
            block.body = rkqy__pcbra


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    kan__xqqn = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (kan__xqqn,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    yuu__vvbzv = dict(key=func, _overload_func=staticmethod(overload_func),
        _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), yuu__vvbzv)


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
            for zwpep__kwjpn in fnty.templates:
                self._inline_overloads.update(zwpep__kwjpn._inline_overloads)
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
    yuu__vvbzv = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), yuu__vvbzv)
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
    dnilj__fng, two__rinv = self._get_impl(args, kws)
    if dnilj__fng is None:
        return
    fujyd__nhwjf = types.Dispatcher(dnilj__fng)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        dkvva__xqyy = dnilj__fng._compiler
        flags = compiler.Flags()
        eupiv__pfspn = dkvva__xqyy.targetdescr.typing_context
        xgzx__ktzqi = dkvva__xqyy.targetdescr.target_context
        jhyz__wfw = dkvva__xqyy.pipeline_class(eupiv__pfspn, xgzx__ktzqi,
            None, None, None, flags, None)
        yigkr__adcq = InlineWorker(eupiv__pfspn, xgzx__ktzqi, dkvva__xqyy.
            locals, jhyz__wfw, flags, None)
        jrd__ezj = fujyd__nhwjf.dispatcher.get_call_template
        zwpep__kwjpn, hhoa__lnjy, cdmjj__klse, kws = jrd__ezj(two__rinv, kws)
        if cdmjj__klse in self._inline_overloads:
            return self._inline_overloads[cdmjj__klse]['iinfo'].signature
        ir = yigkr__adcq.run_untyped_passes(fujyd__nhwjf.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, xgzx__ktzqi, ir, cdmjj__klse, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, cdmjj__klse, None)
        self._inline_overloads[sig.args] = {'folded_args': cdmjj__klse}
        dht__keyrr = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = dht__keyrr
        if not self._inline.is_always_inline:
            sig = fujyd__nhwjf.get_call_type(self.context, two__rinv, kws)
            self._compiled_overloads[sig.args] = fujyd__nhwjf.get_overload(sig)
        udnmq__yeo = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': cdmjj__klse,
            'iinfo': udnmq__yeo}
    else:
        sig = fujyd__nhwjf.get_call_type(self.context, two__rinv, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = fujyd__nhwjf.get_overload(sig)
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
    fxux__znh = [True, False]
    mfvpv__hdp = [False, True]
    axks__mwaab = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    aqvc__agujt = get_local_target(context)
    iked__ehe = utils.order_by_target_specificity(aqvc__agujt, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for ofoq__yvio in iked__ehe:
        fqbkx__istl = ofoq__yvio(context)
        zcyq__auzk = fxux__znh if fqbkx__istl.prefer_literal else mfvpv__hdp
        zcyq__auzk = [True] if getattr(fqbkx__istl, '_no_unliteral', False
            ) else zcyq__auzk
        for cqa__ophq in zcyq__auzk:
            try:
                if cqa__ophq:
                    sig = fqbkx__istl.apply(args, kws)
                else:
                    ugsd__gaj = tuple([_unlit_non_poison(a) for a in args])
                    kpw__woz = {whr__oqcmo: _unlit_non_poison(eiy__rqh) for
                        whr__oqcmo, eiy__rqh in kws.items()}
                    sig = fqbkx__istl.apply(ugsd__gaj, kpw__woz)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    axks__mwaab.add_error(fqbkx__istl, False, e, cqa__ophq)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = fqbkx__istl.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    hgo__zwbf = getattr(fqbkx__istl, 'cases', None)
                    if hgo__zwbf is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            hgo__zwbf)
                    else:
                        msg = 'No match.'
                    axks__mwaab.add_error(fqbkx__istl, True, msg, cqa__ophq)
    axks__mwaab.raise_error()


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
    zwpep__kwjpn = self.template(context)
    psf__xbiu = None
    pqk__waidj = None
    fkm__nuzj = None
    zcyq__auzk = [True, False] if zwpep__kwjpn.prefer_literal else [False, True
        ]
    zcyq__auzk = [True] if getattr(zwpep__kwjpn, '_no_unliteral', False
        ) else zcyq__auzk
    for cqa__ophq in zcyq__auzk:
        if cqa__ophq:
            try:
                fkm__nuzj = zwpep__kwjpn.apply(args, kws)
            except Exception as qln__kwu:
                if isinstance(qln__kwu, errors.ForceLiteralArg):
                    raise qln__kwu
                psf__xbiu = qln__kwu
                fkm__nuzj = None
            else:
                break
        else:
            ytb__fszxx = tuple([_unlit_non_poison(a) for a in args])
            jsh__lyjta = {whr__oqcmo: _unlit_non_poison(eiy__rqh) for 
                whr__oqcmo, eiy__rqh in kws.items()}
            iih__litgj = ytb__fszxx == args and kws == jsh__lyjta
            if not iih__litgj and fkm__nuzj is None:
                try:
                    fkm__nuzj = zwpep__kwjpn.apply(ytb__fszxx, jsh__lyjta)
                except Exception as qln__kwu:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(qln__kwu
                        , errors.NumbaError):
                        raise qln__kwu
                    if isinstance(qln__kwu, errors.ForceLiteralArg):
                        if zwpep__kwjpn.prefer_literal:
                            raise qln__kwu
                    pqk__waidj = qln__kwu
                else:
                    break
    if fkm__nuzj is None and (pqk__waidj is not None or psf__xbiu is not None):
        pcl__hkjk = '- Resolution failure for {} arguments:\n{}\n'
        qwztt__wjf = _termcolor.highlight(pcl__hkjk)
        if numba.core.config.DEVELOPER_MODE:
            exggo__xce = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    cvaaf__xruzq = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    cvaaf__xruzq = ['']
                aoes__hnqt = '\n{}'.format(2 * exggo__xce)
                ccmtf__qwxv = _termcolor.reset(aoes__hnqt + aoes__hnqt.join
                    (_bt_as_lines(cvaaf__xruzq)))
                return _termcolor.reset(ccmtf__qwxv)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            pwjk__mtr = str(e)
            pwjk__mtr = pwjk__mtr if pwjk__mtr else str(repr(e)) + add_bt(e)
            psy__qvlu = errors.TypingError(textwrap.dedent(pwjk__mtr))
            return qwztt__wjf.format(literalness, str(psy__qvlu))
        import bodo
        if isinstance(psf__xbiu, bodo.utils.typing.BodoError):
            raise psf__xbiu
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', psf__xbiu) +
                nested_msg('non-literal', pqk__waidj))
        else:
            if 'missing a required argument' in psf__xbiu.msg:
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
            raise errors.TypingError(msg, loc=psf__xbiu.loc)
    return fkm__nuzj


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
    kzgt__omxtl = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=kzgt__omxtl)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            avaa__neb = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), avaa__neb)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    qrmf__sveq = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            qrmf__sveq.append(types.Omitted(a.value))
        else:
            qrmf__sveq.append(self.typeof_pyval(a))
    fdx__ifct = None
    try:
        error = None
        fdx__ifct = self.compile(tuple(qrmf__sveq))
    except errors.ForceLiteralArg as e:
        dquxn__bjzo = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if dquxn__bjzo:
            ebwyk__imp = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            bgm__fgk = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(dquxn__bjzo))
            raise errors.CompilerError(ebwyk__imp.format(bgm__fgk))
        two__rinv = []
        try:
            for i, eiy__rqh in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        two__rinv.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        two__rinv.append(types.literal(args[i]))
                else:
                    two__rinv.append(args[i])
            args = two__rinv
        except (OSError, FileNotFoundError) as vmyny__ggrwk:
            error = FileNotFoundError(str(vmyny__ggrwk) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                fdx__ifct = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        eeyn__xsucw = []
        for i, trwu__zmin in enumerate(args):
            val = trwu__zmin.value if isinstance(trwu__zmin, numba.core.
                dispatcher.OmittedArg) else trwu__zmin
            try:
                jmzxc__misaj = typeof(val, Purpose.argument)
            except ValueError as fxg__ffxlw:
                eeyn__xsucw.append((i, str(fxg__ffxlw)))
            else:
                if jmzxc__misaj is None:
                    eeyn__xsucw.append((i,
                        f'cannot determine Numba type of value {val}'))
        if eeyn__xsucw:
            fnymx__zmunj = '\n'.join(f'- argument {i}: {vzd__brt}' for i,
                vzd__brt in eeyn__xsucw)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{fnymx__zmunj}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                uyiaz__uhj = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                frv__oxug = False
                for fvumd__fter in uyiaz__uhj:
                    if fvumd__fter in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        frv__oxug = True
                        break
                if not frv__oxug:
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
                avaa__neb = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), avaa__neb)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return fdx__ifct


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
    for jmca__hquq in cres.library._codegen._engine._defined_symbols:
        if jmca__hquq.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in jmca__hquq and (
            'bodo_gb_udf_update_local' in jmca__hquq or 
            'bodo_gb_udf_combine' in jmca__hquq or 'bodo_gb_udf_eval' in
            jmca__hquq or 'bodo_gb_apply_general_udfs' in jmca__hquq):
            gb_agg_cfunc_addr[jmca__hquq
                ] = cres.library.get_pointer_to_function(jmca__hquq)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for jmca__hquq in cres.library._codegen._engine._defined_symbols:
        if jmca__hquq.startswith('cfunc') and ('get_join_cond_addr' not in
            jmca__hquq or 'bodo_join_gen_cond' in jmca__hquq):
            join_gen_cond_cfunc_addr[jmca__hquq
                ] = cres.library.get_pointer_to_function(jmca__hquq)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    dnilj__fng = self._get_dispatcher_for_current_target()
    if dnilj__fng is not self:
        return dnilj__fng.compile(sig)
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
            xjwk__tbech = self.overloads.get(tuple(args))
            if xjwk__tbech is not None:
                return xjwk__tbech.entry_point
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
            hwlr__erxg = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=hwlr__erxg):
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
    xyex__pvojk = self._final_module
    cfsz__htrc = []
    fiiw__zmp = 0
    for fn in xyex__pvojk.functions:
        fiiw__zmp += 1
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
            cfsz__htrc.append(fn.name)
    if fiiw__zmp == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if cfsz__htrc:
        xyex__pvojk = xyex__pvojk.clone()
        for name in cfsz__htrc:
            xyex__pvojk.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = xyex__pvojk
    return xyex__pvojk


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
    for wilhd__llq in self.constraints:
        loc = wilhd__llq.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                wilhd__llq(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                tkmcf__qtu = numba.core.errors.TypingError(str(e), loc=
                    wilhd__llq.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(tkmcf__qtu, e))
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
                    tkmcf__qtu = numba.core.errors.TypingError(msg.format(
                        con=wilhd__llq, err=str(e)), loc=wilhd__llq.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(tkmcf__qtu, e))
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
    for ciw__nzpf in self._failures.values():
        for ieg__ryp in ciw__nzpf:
            if isinstance(ieg__ryp.error, ForceLiteralArg):
                raise ieg__ryp.error
            if isinstance(ieg__ryp.error, bodo.utils.typing.BodoError):
                raise ieg__ryp.error
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
    kpl__hvc = False
    rkqy__pcbra = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        ppopi__xhqpw = set()
        ogpjv__tiwlm = lives & alias_set
        for eiy__rqh in ogpjv__tiwlm:
            ppopi__xhqpw |= alias_map[eiy__rqh]
        lives_n_aliases = lives | ppopi__xhqpw | arg_aliases
        if type(stmt) in remove_dead_extensions:
            qcxiw__zwyy = remove_dead_extensions[type(stmt)]
            stmt = qcxiw__zwyy(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                kpl__hvc = True
                continue
        if isinstance(stmt, ir.Assign):
            lroso__zgtso = stmt.target
            ykc__elsh = stmt.value
            if lroso__zgtso.name not in lives and has_no_side_effect(ykc__elsh,
                lives_n_aliases, call_table):
                kpl__hvc = True
                continue
            if saved_array_analysis and lroso__zgtso.name in lives and is_expr(
                ykc__elsh, 'getattr'
                ) and ykc__elsh.attr == 'shape' and is_array_typ(typemap[
                ykc__elsh.value.name]) and ykc__elsh.value.name not in lives:
                ftsn__gbbxd = {eiy__rqh: whr__oqcmo for whr__oqcmo,
                    eiy__rqh in func_ir.blocks.items()}
                if block in ftsn__gbbxd:
                    dboh__cva = ftsn__gbbxd[block]
                    vjheb__xupyk = saved_array_analysis.get_equiv_set(dboh__cva
                        )
                    uvxl__fpfz = vjheb__xupyk.get_equiv_set(ykc__elsh.value)
                    if uvxl__fpfz is not None:
                        for eiy__rqh in uvxl__fpfz:
                            if eiy__rqh.endswith('#0'):
                                eiy__rqh = eiy__rqh[:-2]
                            if eiy__rqh in typemap and is_array_typ(typemap
                                [eiy__rqh]) and eiy__rqh in lives:
                                ykc__elsh.value = ir.Var(ykc__elsh.value.
                                    scope, eiy__rqh, ykc__elsh.value.loc)
                                kpl__hvc = True
                                break
            if isinstance(ykc__elsh, ir.Var
                ) and lroso__zgtso.name == ykc__elsh.name:
                kpl__hvc = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                kpl__hvc = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            big__ifhf = analysis.ir_extension_usedefs[type(stmt)]
            kblyl__qkyf, xpd__dqkc = big__ifhf(stmt)
            lives -= xpd__dqkc
            lives |= kblyl__qkyf
        else:
            lives |= {eiy__rqh.name for eiy__rqh in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                xua__zffg = set()
                if isinstance(ykc__elsh, ir.Expr):
                    xua__zffg = {eiy__rqh.name for eiy__rqh in ykc__elsh.
                        list_vars()}
                if lroso__zgtso.name not in xua__zffg:
                    lives.remove(lroso__zgtso.name)
        rkqy__pcbra.append(stmt)
    rkqy__pcbra.reverse()
    block.body = rkqy__pcbra
    return kpl__hvc


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            szh__fgbm, = args
            if isinstance(szh__fgbm, types.IterableType):
                dtype = szh__fgbm.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), szh__fgbm)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    pnmct__ycf = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (pnmct__ycf, self.dtype)
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
        except LiteralTypingError as ygd__ahl:
            return
    try:
        return literal(value)
    except LiteralTypingError as ygd__ahl:
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
        xqz__hfz = py_func.__qualname__
    except AttributeError as ygd__ahl:
        xqz__hfz = py_func.__name__
    kkvss__zlv = inspect.getfile(py_func)
    for cls in self._locator_classes:
        etry__vspfw = cls.from_function(py_func, kkvss__zlv)
        if etry__vspfw is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (xqz__hfz, kkvss__zlv))
    self._locator = etry__vspfw
    vtkna__sga = inspect.getfile(py_func)
    gswlf__fah = os.path.splitext(os.path.basename(vtkna__sga))[0]
    if kkvss__zlv.startswith('<ipython-'):
        sayuo__knd = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', gswlf__fah, count=1)
        if sayuo__knd == gswlf__fah:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        gswlf__fah = sayuo__knd
    cvf__ior = '%s.%s' % (gswlf__fah, xqz__hfz)
    ipoh__qpq = getattr(sys, 'abiflags', '')
    self._filename_base = self.get_filename_base(cvf__ior, ipoh__qpq)


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    vlgrm__qitm = list(filter(lambda a: self._istuple(a.name), args))
    if len(vlgrm__qitm) == 2 and fn.__name__ == 'add':
        xcj__yxc = self.typemap[vlgrm__qitm[0].name]
        trit__qhvnp = self.typemap[vlgrm__qitm[1].name]
        if xcj__yxc.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                vlgrm__qitm[1]))
        if trit__qhvnp.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                vlgrm__qitm[0]))
        try:
            xdq__dih = [equiv_set.get_shape(x) for x in vlgrm__qitm]
            if None in xdq__dih:
                return None
            mtpzx__epcn = sum(xdq__dih, ())
            return ArrayAnalysis.AnalyzeResult(shape=mtpzx__epcn)
        except GuardException as ygd__ahl:
            return None
    trqu__bekh = list(filter(lambda a: self._isarray(a.name), args))
    require(len(trqu__bekh) > 0)
    ijcd__gazqm = [x.name for x in trqu__bekh]
    hlbx__qzyf = [self.typemap[x.name].ndim for x in trqu__bekh]
    ttvg__plts = max(hlbx__qzyf)
    require(ttvg__plts > 0)
    xdq__dih = [equiv_set.get_shape(x) for x in trqu__bekh]
    if any(a is None for a in xdq__dih):
        return ArrayAnalysis.AnalyzeResult(shape=trqu__bekh[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, trqu__bekh))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, xdq__dih,
        ijcd__gazqm)


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
    zhe__chtj = code_obj.code
    ybac__jvp = len(zhe__chtj.co_freevars)
    ovzd__byjnt = zhe__chtj.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        dxhs__lgb, op = ir_utils.find_build_sequence(caller_ir, code_obj.
            closure)
        assert op == 'build_tuple'
        ovzd__byjnt = [eiy__rqh.name for eiy__rqh in dxhs__lgb]
    xcc__dmf = caller_ir.func_id.func.__globals__
    try:
        xcc__dmf = getattr(code_obj, 'globals', xcc__dmf)
    except KeyError as ygd__ahl:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/source/programming_with_bodo/bodo_api_reference/udfs.html"
        )
    vjh__vuas = []
    for x in ovzd__byjnt:
        try:
            eqwjs__lvt = caller_ir.get_definition(x)
        except KeyError as ygd__ahl:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(eqwjs__lvt, (ir.Const, ir.Global, ir.FreeVar)):
            val = eqwjs__lvt.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                kan__xqqn = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                xcc__dmf[kan__xqqn] = bodo.jit(distributed=False)(val)
                xcc__dmf[kan__xqqn].is_nested_func = True
                val = kan__xqqn
            if isinstance(val, CPUDispatcher):
                kan__xqqn = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                xcc__dmf[kan__xqqn] = val
                val = kan__xqqn
            vjh__vuas.append(val)
        elif isinstance(eqwjs__lvt, ir.Expr
            ) and eqwjs__lvt.op == 'make_function':
            jjov__ymtkn = convert_code_obj_to_function(eqwjs__lvt, caller_ir)
            kan__xqqn = ir_utils.mk_unique_var('nested_func').replace('.', '_')
            xcc__dmf[kan__xqqn] = bodo.jit(distributed=False)(jjov__ymtkn)
            xcc__dmf[kan__xqqn].is_nested_func = True
            vjh__vuas.append(kan__xqqn)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    iiaf__eiar = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        vjh__vuas)])
    fkzu__hpjy = ','.join([('c_%d' % i) for i in range(ybac__jvp)])
    arlfz__zhte = list(zhe__chtj.co_varnames)
    fsj__pvx = 0
    mzb__dgyg = zhe__chtj.co_argcount
    fsdc__ocwry = caller_ir.get_definition(code_obj.defaults)
    if fsdc__ocwry is not None:
        if isinstance(fsdc__ocwry, tuple):
            d = [caller_ir.get_definition(x).value for x in fsdc__ocwry]
            qgaap__kbmd = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in fsdc__ocwry.items]
            qgaap__kbmd = tuple(d)
        fsj__pvx = len(qgaap__kbmd)
    oeh__dij = mzb__dgyg - fsj__pvx
    ajyk__tuwvm = ','.join([('%s' % arlfz__zhte[i]) for i in range(oeh__dij)])
    if fsj__pvx:
        udr__oqq = [('%s = %s' % (arlfz__zhte[i + oeh__dij], qgaap__kbmd[i]
            )) for i in range(fsj__pvx)]
        ajyk__tuwvm += ', '
        ajyk__tuwvm += ', '.join(udr__oqq)
    return _create_function_from_code_obj(zhe__chtj, iiaf__eiar,
        ajyk__tuwvm, fkzu__hpjy, xcc__dmf)


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
    for dah__mexxm, (cga__yocjt, yfkrl__yfrns) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % yfkrl__yfrns)
            ybml__psaap = _pass_registry.get(cga__yocjt).pass_inst
            if isinstance(ybml__psaap, CompilerPass):
                self._runPass(dah__mexxm, ybml__psaap, state)
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
                    pipeline_name, yfkrl__yfrns)
                aktzm__nsf = self._patch_error(msg, e)
                raise aktzm__nsf
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
    xig__mqh = None
    xpd__dqkc = {}

    def lookup(var, already_seen, varonly=True):
        val = xpd__dqkc.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    szy__qrsu = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        lroso__zgtso = stmt.target
        ykc__elsh = stmt.value
        xpd__dqkc[lroso__zgtso.name] = ykc__elsh
        if isinstance(ykc__elsh, ir.Var) and ykc__elsh.name in xpd__dqkc:
            ykc__elsh = lookup(ykc__elsh, set())
        if isinstance(ykc__elsh, ir.Expr):
            ucx__osoxb = set(lookup(eiy__rqh, set(), True).name for
                eiy__rqh in ykc__elsh.list_vars())
            if name in ucx__osoxb:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(ykc__elsh)]
                ythvw__cau = [x for x, ithg__fijhg in args if ithg__fijhg.
                    name != name]
                args = [(x, ithg__fijhg) for x, ithg__fijhg in args if x !=
                    ithg__fijhg.name]
                bnihv__kydjk = dict(args)
                if len(ythvw__cau) == 1:
                    bnihv__kydjk[ythvw__cau[0]] = ir.Var(lroso__zgtso.scope,
                        name + '#init', lroso__zgtso.loc)
                replace_vars_inner(ykc__elsh, bnihv__kydjk)
                xig__mqh = nodes[i:]
                break
    return xig__mqh


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
        uwi__cbjsc = expand_aliases({eiy__rqh.name for eiy__rqh in stmt.
            list_vars()}, alias_map, arg_aliases)
        srumb__okv = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        ijtrx__fvw = expand_aliases({eiy__rqh.name for eiy__rqh in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        ngdnq__pqk = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(srumb__okv & ijtrx__fvw | ngdnq__pqk & uwi__cbjsc) == 0:
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
    zckn__yihs = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            zckn__yihs.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                zckn__yihs.update(get_parfor_writes(stmt, func_ir))
    return zckn__yihs


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    zckn__yihs = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        zckn__yihs.add(stmt.target.name)
    if isinstance(stmt, bodo.ir.aggregate.Aggregate):
        zckn__yihs = {eiy__rqh.name for eiy__rqh in stmt.df_out_vars.values()}
        if stmt.out_key_vars is not None:
            zckn__yihs.update({eiy__rqh.name for eiy__rqh in stmt.out_key_vars}
                )
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        zckn__yihs = {eiy__rqh.name for eiy__rqh in stmt.out_vars}
    if isinstance(stmt, bodo.ir.join.Join):
        zckn__yihs = {eiy__rqh.name for eiy__rqh in stmt.out_data_vars.values()
            }
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            zckn__yihs.update({eiy__rqh.name for eiy__rqh in stmt.out_key_arrs}
                )
            zckn__yihs.update({eiy__rqh.name for eiy__rqh in stmt.
                df_out_vars.values()})
    if is_call_assign(stmt):
        tjm__ggz = guard(find_callname, func_ir, stmt.value)
        if tjm__ggz in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'), (
            'setna', 'bodo.libs.array_kernels'), ('str_arr_item_to_numeric',
            'bodo.libs.str_arr_ext'), ('str_arr_setitem_int_to_str',
            'bodo.libs.str_arr_ext'), ('str_arr_setitem_NA_str',
            'bodo.libs.str_arr_ext'), ('str_arr_set_not_na',
            'bodo.libs.str_arr_ext'), ('get_str_arr_item_copy',
            'bodo.libs.str_arr_ext'), ('set_bit_to_arr',
            'bodo.libs.int_arr_ext')):
            zckn__yihs.add(stmt.value.args[0].name)
        if tjm__ggz == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            zckn__yihs.add(stmt.value.args[1].name)
    return zckn__yihs


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
        qcxiw__zwyy = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        sjnb__iguvs = qcxiw__zwyy.format(self, msg)
        self.args = sjnb__iguvs,
    else:
        qcxiw__zwyy = _termcolor.errmsg('{0}')
        sjnb__iguvs = qcxiw__zwyy.format(self)
        self.args = sjnb__iguvs,
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
        for gldbq__xgh in options['distributed']:
            dist_spec[gldbq__xgh] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for gldbq__xgh in options['distributed_block']:
            dist_spec[gldbq__xgh] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    uef__anor = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, fqi__qcsaa in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(fqi__qcsaa)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    vxfz__gypp = {}
    for jlzl__hvdj in reversed(inspect.getmro(cls)):
        vxfz__gypp.update(jlzl__hvdj.__dict__)
    vbr__hhngd, vhxq__oktpe, ikcc__cqv, fiupw__nya = {}, {}, {}, {}
    for whr__oqcmo, eiy__rqh in vxfz__gypp.items():
        if isinstance(eiy__rqh, pytypes.FunctionType):
            vbr__hhngd[whr__oqcmo] = eiy__rqh
        elif isinstance(eiy__rqh, property):
            vhxq__oktpe[whr__oqcmo] = eiy__rqh
        elif isinstance(eiy__rqh, staticmethod):
            ikcc__cqv[whr__oqcmo] = eiy__rqh
        else:
            fiupw__nya[whr__oqcmo] = eiy__rqh
    smvqr__onrl = (set(vbr__hhngd) | set(vhxq__oktpe) | set(ikcc__cqv)) & set(
        spec)
    if smvqr__onrl:
        raise NameError('name shadowing: {0}'.format(', '.join(smvqr__onrl)))
    hngoh__expe = fiupw__nya.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(fiupw__nya)
    if fiupw__nya:
        msg = 'class members are not yet supported: {0}'
        khzwg__cfd = ', '.join(fiupw__nya.keys())
        raise TypeError(msg.format(khzwg__cfd))
    for whr__oqcmo, eiy__rqh in vhxq__oktpe.items():
        if eiy__rqh.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(whr__oqcmo))
    jit_methods = {whr__oqcmo: bodo.jit(returns_maybe_distributed=uef__anor
        )(eiy__rqh) for whr__oqcmo, eiy__rqh in vbr__hhngd.items()}
    jit_props = {}
    for whr__oqcmo, eiy__rqh in vhxq__oktpe.items():
        yuu__vvbzv = {}
        if eiy__rqh.fget:
            yuu__vvbzv['get'] = bodo.jit(eiy__rqh.fget)
        if eiy__rqh.fset:
            yuu__vvbzv['set'] = bodo.jit(eiy__rqh.fset)
        jit_props[whr__oqcmo] = yuu__vvbzv
    jit_static_methods = {whr__oqcmo: bodo.jit(eiy__rqh.__func__) for 
        whr__oqcmo, eiy__rqh in ikcc__cqv.items()}
    fzvg__ceuvu = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    ept__zluf = dict(class_type=fzvg__ceuvu, __doc__=hngoh__expe)
    ept__zluf.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), ept__zluf)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, fzvg__ceuvu)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(fzvg__ceuvu, typingctx, targetctx).register()
    as_numba_type.register(cls, fzvg__ceuvu.instance_type)
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
    psbjz__kvu = ','.join('{0}:{1}'.format(whr__oqcmo, eiy__rqh) for 
        whr__oqcmo, eiy__rqh in struct.items())
    yor__eyo = ','.join('{0}:{1}'.format(whr__oqcmo, eiy__rqh) for 
        whr__oqcmo, eiy__rqh in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), psbjz__kvu, yor__eyo)
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
    vom__spoky = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if vom__spoky is None:
        return
    xvua__zdpub, hvbkh__twva = vom__spoky
    for a in itertools.chain(xvua__zdpub, hvbkh__twva.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, xvua__zdpub, hvbkh__twva)
    except ForceLiteralArg as e:
        qzjji__wyt = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(qzjji__wyt, self.kws)
        ppfp__blkv = set()
        xspo__ctb = set()
        nnv__wgjys = {}
        for dah__mexxm in e.requested_args:
            zuxsw__caaxm = typeinfer.func_ir.get_definition(folded[dah__mexxm])
            if isinstance(zuxsw__caaxm, ir.Arg):
                ppfp__blkv.add(zuxsw__caaxm.index)
                if zuxsw__caaxm.index in e.file_infos:
                    nnv__wgjys[zuxsw__caaxm.index] = e.file_infos[zuxsw__caaxm
                        .index]
            else:
                xspo__ctb.add(dah__mexxm)
        if xspo__ctb:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif ppfp__blkv:
            raise ForceLiteralArg(ppfp__blkv, loc=self.loc, file_infos=
                nnv__wgjys)
    if sig is None:
        ccz__ctu = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in xvua__zdpub]
        args += [('%s=%s' % (whr__oqcmo, eiy__rqh)) for whr__oqcmo,
            eiy__rqh in sorted(hvbkh__twva.items())]
        vpwmg__mrgbc = ccz__ctu.format(fnty, ', '.join(map(str, args)))
        bjhy__iiphc = context.explain_function_type(fnty)
        msg = '\n'.join([vpwmg__mrgbc, bjhy__iiphc])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        cyo__lun = context.unify_pairs(sig.recvr, fnty.this)
        if cyo__lun is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if cyo__lun is not None and cyo__lun.is_precise():
            kly__hru = fnty.copy(this=cyo__lun)
            typeinfer.propagate_refined_type(self.func, kly__hru)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            megyu__hunt = target.getone()
            if context.unify_pairs(megyu__hunt, sig.return_type
                ) == megyu__hunt:
                sig = sig.replace(return_type=megyu__hunt)
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
        ebwyk__imp = '*other* must be a {} but got a {} instead'
        raise TypeError(ebwyk__imp.format(ForceLiteralArg, type(other)))
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
    uajv__xjaq = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for whr__oqcmo, eiy__rqh in kwargs.items():
        rji__asxe = None
        try:
            nxp__cqqk = ir.Var(ir.Scope(None, loc), ir_utils.mk_unique_var(
                'dummy'), loc)
            func_ir._definitions[nxp__cqqk.name] = [eiy__rqh]
            rji__asxe = get_const_value_inner(func_ir, nxp__cqqk)
            func_ir._definitions.pop(nxp__cqqk.name)
            if isinstance(rji__asxe, str):
                rji__asxe = sigutils._parse_signature_string(rji__asxe)
            if isinstance(rji__asxe, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {whr__oqcmo} is annotated as type class {rji__asxe}."""
                    )
            assert isinstance(rji__asxe, types.Type)
            if isinstance(rji__asxe, (types.List, types.Set)):
                rji__asxe = rji__asxe.copy(reflected=False)
            uajv__xjaq[whr__oqcmo] = rji__asxe
        except BodoError as ygd__ahl:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(rji__asxe, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(eiy__rqh, ir.Global):
                    msg = f'Global {eiy__rqh.name!r} is not defined.'
                if isinstance(eiy__rqh, ir.FreeVar):
                    msg = f'Freevar {eiy__rqh.name!r} is not defined.'
            if isinstance(eiy__rqh, ir.Expr) and eiy__rqh.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=whr__oqcmo, msg=msg, loc=loc)
    for name, typ in uajv__xjaq.items():
        self._legalize_arg_type(name, typ, loc)
    return uajv__xjaq


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
    bih__opycv = inst.arg
    assert bih__opycv > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(bih__opycv)]))
    tmps = [state.make_temp() for _ in range(bih__opycv - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    upaa__hrcld = ir.Global('format', format, loc=self.loc)
    self.store(value=upaa__hrcld, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    gcp__zfpjr = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=gcp__zfpjr, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    bih__opycv = inst.arg
    assert bih__opycv > 0, 'invalid BUILD_STRING count'
    yaaru__zbiy = self.get(strings[0])
    for other, ufef__hqeb in zip(strings[1:], tmps):
        other = self.get(other)
        nqt__bttm = ir.Expr.binop(operator.add, lhs=yaaru__zbiy, rhs=other,
            loc=self.loc)
        self.store(nqt__bttm, ufef__hqeb)
        yaaru__zbiy = self.get(ufef__hqeb)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    miknp__idgb = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, miknp__idgb])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    kuqm__qvc = mk_unique_var(f'{var_name}')
    dwc__tlhmj = kuqm__qvc.replace('<', '_').replace('>', '_')
    dwc__tlhmj = dwc__tlhmj.replace('.', '_').replace('$', '_v')
    return dwc__tlhmj


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
                ixd__gwls = get_overload_const_str(val2)
                if ixd__gwls != 'ns':
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
        suyu__ijqrp = states['defmap']
        if len(suyu__ijqrp) == 0:
            fnpgc__roypr = assign.target
            numba.core.ssa._logger.debug('first assign: %s', fnpgc__roypr)
            if fnpgc__roypr.name not in scope.localvars:
                fnpgc__roypr = scope.define(assign.target.name, loc=assign.loc)
        else:
            fnpgc__roypr = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=fnpgc__roypr, value=assign.value, loc=
            assign.loc)
        suyu__ijqrp[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    ifs__ogrw = []
    for whr__oqcmo, eiy__rqh in typing.npydecl.registry.globals:
        if whr__oqcmo == func:
            ifs__ogrw.append(eiy__rqh)
    for whr__oqcmo, eiy__rqh in typing.templates.builtin_registry.globals:
        if whr__oqcmo == func:
            ifs__ogrw.append(eiy__rqh)
    if len(ifs__ogrw) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return ifs__ogrw


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    gsqlc__tqlzr = {}
    bdkcv__zftqy = find_topo_order(blocks)
    hxwv__gmkgp = {}
    for dboh__cva in bdkcv__zftqy:
        block = blocks[dboh__cva]
        rkqy__pcbra = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                lroso__zgtso = stmt.target.name
                ykc__elsh = stmt.value
                if (ykc__elsh.op == 'getattr' and ykc__elsh.attr in
                    arr_math and isinstance(typemap[ykc__elsh.value.name],
                    types.npytypes.Array)):
                    ykc__elsh = stmt.value
                    whf__ocft = ykc__elsh.value
                    gsqlc__tqlzr[lroso__zgtso] = whf__ocft
                    scope = whf__ocft.scope
                    loc = whf__ocft.loc
                    xrs__tuhrw = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[xrs__tuhrw.name] = types.misc.Module(numpy)
                    eds__aazrb = ir.Global('np', numpy, loc)
                    hdr__pjy = ir.Assign(eds__aazrb, xrs__tuhrw, loc)
                    ykc__elsh.value = xrs__tuhrw
                    rkqy__pcbra.append(hdr__pjy)
                    func_ir._definitions[xrs__tuhrw.name] = [eds__aazrb]
                    func = getattr(numpy, ykc__elsh.attr)
                    dru__iovs = get_np_ufunc_typ_lst(func)
                    hxwv__gmkgp[lroso__zgtso] = dru__iovs
                if (ykc__elsh.op == 'call' and ykc__elsh.func.name in
                    gsqlc__tqlzr):
                    whf__ocft = gsqlc__tqlzr[ykc__elsh.func.name]
                    iwpm__jxkim = calltypes.pop(ykc__elsh)
                    kbpnj__che = iwpm__jxkim.args[:len(ykc__elsh.args)]
                    wstwj__rkqr = {name: typemap[eiy__rqh.name] for name,
                        eiy__rqh in ykc__elsh.kws}
                    kqtu__uleff = hxwv__gmkgp[ykc__elsh.func.name]
                    gqad__fgk = None
                    for cpsoi__kpuf in kqtu__uleff:
                        try:
                            gqad__fgk = cpsoi__kpuf.get_call_type(typingctx,
                                [typemap[whf__ocft.name]] + list(kbpnj__che
                                ), wstwj__rkqr)
                            typemap.pop(ykc__elsh.func.name)
                            typemap[ykc__elsh.func.name] = cpsoi__kpuf
                            calltypes[ykc__elsh] = gqad__fgk
                            break
                        except Exception as ygd__ahl:
                            pass
                    if gqad__fgk is None:
                        raise TypeError(
                            f'No valid template found for {ykc__elsh.func.name}'
                            )
                    ykc__elsh.args = [whf__ocft] + ykc__elsh.args
            rkqy__pcbra.append(stmt)
        block.body = rkqy__pcbra


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    mgyjy__xskt = ufunc.nin
    fclhj__lgc = ufunc.nout
    oeh__dij = ufunc.nargs
    assert oeh__dij == mgyjy__xskt + fclhj__lgc
    if len(args) < mgyjy__xskt:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args),
            mgyjy__xskt))
    if len(args) > oeh__dij:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), oeh__dij))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    vkzow__mdi = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    phb__bthj = max(vkzow__mdi)
    iagrk__hdpg = args[mgyjy__xskt:]
    if not all(d == phb__bthj for d in vkzow__mdi[mgyjy__xskt:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(eikj__nica, types.ArrayCompatible) and not
        isinstance(eikj__nica, types.Bytes) for eikj__nica in iagrk__hdpg):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(eikj__nica.mutable for eikj__nica in iagrk__hdpg):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    ome__tkuh = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    zinwl__obxpq = None
    if phb__bthj > 0 and len(iagrk__hdpg) < ufunc.nout:
        zinwl__obxpq = 'C'
        nazvg__rkmjs = [(x.layout if isinstance(x, types.ArrayCompatible) and
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in nazvg__rkmjs and 'F' in nazvg__rkmjs:
            zinwl__obxpq = 'F'
    return ome__tkuh, iagrk__hdpg, phb__bthj, zinwl__obxpq


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
        hbfz__wupwp = 'Dict.key_type cannot be of type {}'
        raise TypingError(hbfz__wupwp.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        hbfz__wupwp = 'Dict.value_type cannot be of type {}'
        raise TypingError(hbfz__wupwp.format(valty))
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
    hlu__opu = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[hlu__opu]
        return impl, args
    except KeyError as ygd__ahl:
        pass
    impl, args = self._build_impl(hlu__opu, args, kws)
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
        ytm__gwy = find_topo_order(parfor.loop_body)
    hrkpu__mpcfc = ytm__gwy[0]
    bcqx__seib = {}
    _update_parfor_get_setitems(parfor.loop_body[hrkpu__mpcfc].body, parfor
        .index_var, alias_map, bcqx__seib, lives_n_aliases)
    mvrqy__dvub = set(bcqx__seib.keys())
    for edkk__nyxzd in ytm__gwy:
        if edkk__nyxzd == hrkpu__mpcfc:
            continue
        for stmt in parfor.loop_body[edkk__nyxzd].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            wrq__ice = set(eiy__rqh.name for eiy__rqh in stmt.list_vars())
            nfs__adfdm = wrq__ice & mvrqy__dvub
            for a in nfs__adfdm:
                bcqx__seib.pop(a, None)
    for edkk__nyxzd in ytm__gwy:
        if edkk__nyxzd == hrkpu__mpcfc:
            continue
        block = parfor.loop_body[edkk__nyxzd]
        cjgtb__dwxee = bcqx__seib.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            cjgtb__dwxee, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    vvh__axany = max(blocks.keys())
    buf__omwyo, ehsk__fhks = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    hetk__yowm = ir.Jump(buf__omwyo, ir.Loc('parfors_dummy', -1))
    blocks[vvh__axany].body.append(hetk__yowm)
    rwlo__paxn = compute_cfg_from_blocks(blocks)
    kgb__jqffs = compute_use_defs(blocks)
    ofbfh__wceq = compute_live_map(rwlo__paxn, blocks, kgb__jqffs.usemap,
        kgb__jqffs.defmap)
    alias_set = set(alias_map.keys())
    for dboh__cva, block in blocks.items():
        rkqy__pcbra = []
        wrbbd__xumci = {eiy__rqh.name for eiy__rqh in block.terminator.
            list_vars()}
        for pciig__muq, ajsc__eth in rwlo__paxn.successors(dboh__cva):
            wrbbd__xumci |= ofbfh__wceq[pciig__muq]
        for stmt in reversed(block.body):
            ppopi__xhqpw = wrbbd__xumci & alias_set
            for eiy__rqh in ppopi__xhqpw:
                wrbbd__xumci |= alias_map[eiy__rqh]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in wrbbd__xumci and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                tjm__ggz = guard(find_callname, func_ir, stmt.value)
                if tjm__ggz == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in wrbbd__xumci and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            wrbbd__xumci |= {eiy__rqh.name for eiy__rqh in stmt.list_vars()}
            rkqy__pcbra.append(stmt)
        rkqy__pcbra.reverse()
        block.body = rkqy__pcbra
    typemap.pop(ehsk__fhks.name)
    blocks[vvh__axany].body.pop()

    def trim_empty_parfor_branches(parfor):
        sxh__migmz = False
        blocks = parfor.loop_body.copy()
        for dboh__cva, block in blocks.items():
            if len(block.body):
                wzqo__ini = block.body[-1]
                if isinstance(wzqo__ini, ir.Branch):
                    if len(blocks[wzqo__ini.truebr].body) == 1 and len(blocks
                        [wzqo__ini.falsebr].body) == 1:
                        sjrxu__mzvky = blocks[wzqo__ini.truebr].body[0]
                        qrh__mawxz = blocks[wzqo__ini.falsebr].body[0]
                        if isinstance(sjrxu__mzvky, ir.Jump) and isinstance(
                            qrh__mawxz, ir.Jump
                            ) and sjrxu__mzvky.target == qrh__mawxz.target:
                            parfor.loop_body[dboh__cva].body[-1] = ir.Jump(
                                sjrxu__mzvky.target, wzqo__ini.loc)
                            sxh__migmz = True
                    elif len(blocks[wzqo__ini.truebr].body) == 1:
                        sjrxu__mzvky = blocks[wzqo__ini.truebr].body[0]
                        if isinstance(sjrxu__mzvky, ir.Jump
                            ) and sjrxu__mzvky.target == wzqo__ini.falsebr:
                            parfor.loop_body[dboh__cva].body[-1] = ir.Jump(
                                sjrxu__mzvky.target, wzqo__ini.loc)
                            sxh__migmz = True
                    elif len(blocks[wzqo__ini.falsebr].body) == 1:
                        qrh__mawxz = blocks[wzqo__ini.falsebr].body[0]
                        if isinstance(qrh__mawxz, ir.Jump
                            ) and qrh__mawxz.target == wzqo__ini.truebr:
                            parfor.loop_body[dboh__cva].body[-1] = ir.Jump(
                                qrh__mawxz.target, wzqo__ini.loc)
                            sxh__migmz = True
        return sxh__migmz
    sxh__migmz = True
    while sxh__migmz:
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
        sxh__migmz = trim_empty_parfor_branches(parfor)
    xvf__izsq = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        xvf__izsq &= len(block.body) == 0
    if xvf__izsq:
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
    kaxxl__osgfh = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                kaxxl__osgfh += 1
                parfor = stmt
                ogozr__acvj = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = ogozr__acvj.scope
                loc = ir.Loc('parfors_dummy', -1)
                rga__tjzz = ir.Var(scope, mk_unique_var('$const'), loc)
                ogozr__acvj.body.append(ir.Assign(ir.Const(0, loc),
                    rga__tjzz, loc))
                ogozr__acvj.body.append(ir.Return(rga__tjzz, loc))
                rwlo__paxn = compute_cfg_from_blocks(parfor.loop_body)
                for rmol__npz in rwlo__paxn.dead_nodes():
                    del parfor.loop_body[rmol__npz]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                ogozr__acvj = parfor.loop_body[max(parfor.loop_body.keys())]
                ogozr__acvj.body.pop()
                ogozr__acvj.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return kaxxl__osgfh


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
            xjwk__tbech = self.overloads.get(tuple(args))
            if xjwk__tbech is not None:
                return xjwk__tbech.entry_point
            self._pre_compile(args, return_type, flags)
            whbx__sxj = self.func_ir
            hwlr__erxg = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=hwlr__erxg):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=whbx__sxj, args=args,
                    return_type=return_type, flags=flags, locals=self.
                    locals, lifted=(), lifted_from=self.lifted_from,
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
        mdll__pwmoc = copy.deepcopy(flags)
        mdll__pwmoc.no_rewrites = True

        def compile_local(the_ir, the_flags):
            sthty__nlzdl = pipeline_class(typingctx, targetctx, library,
                args, return_type, the_flags, locals)
            return sthty__nlzdl.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        zcd__nej = compile_local(func_ir, mdll__pwmoc)
        vdkad__lzpir = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    vdkad__lzpir = compile_local(func_ir, flags)
                except Exception as ygd__ahl:
                    pass
        if vdkad__lzpir is not None:
            cres = vdkad__lzpir
        else:
            cres = zcd__nej
        return cres
    else:
        sthty__nlzdl = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return sthty__nlzdl.compile_ir(func_ir=func_ir, lifted=lifted,
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
    uxn__yhvb = self.get_data_type(typ.dtype)
    esdo__jxwp = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        esdo__jxwp):
        xhj__gzgac = ary.ctypes.data
        xnmy__njb = self.add_dynamic_addr(builder, xhj__gzgac, info=str(
            type(xhj__gzgac)))
        ipkr__ovlr = self.add_dynamic_addr(builder, id(ary), info=str(type(
            ary)))
        self.global_arrays.append(ary)
    else:
        rinue__klxqc = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            rinue__klxqc = rinue__klxqc.view('int64')
        val = bytearray(rinue__klxqc.data)
        kxetq__dxr = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)), val)
        xnmy__njb = cgutils.global_constant(builder, '.const.array.data',
            kxetq__dxr)
        xnmy__njb.align = self.get_abi_alignment(uxn__yhvb)
        ipkr__ovlr = None
    tku__dif = self.get_value_type(types.intp)
    uecn__xuosr = [self.get_constant(types.intp, dsu__vtrh) for dsu__vtrh in
        ary.shape]
    kxbk__gnjd = lir.Constant(lir.ArrayType(tku__dif, len(uecn__xuosr)),
        uecn__xuosr)
    ifb__hyuc = [self.get_constant(types.intp, dsu__vtrh) for dsu__vtrh in
        ary.strides]
    vvzbr__uoblz = lir.Constant(lir.ArrayType(tku__dif, len(ifb__hyuc)),
        ifb__hyuc)
    kjqz__shr = self.get_constant(types.intp, ary.dtype.itemsize)
    kkl__eoitw = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        kkl__eoitw, kjqz__shr, xnmy__njb.bitcast(self.get_value_type(types.
        CPointer(typ.dtype))), kxbk__gnjd, vvzbr__uoblz])


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
    idq__hrt = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    meji__uae = lir.Function(module, idq__hrt, name='nrt_atomic_{0}'.format(op)
        )
    [szg__sami] = meji__uae.args
    vqe__cdkxp = meji__uae.append_basic_block()
    builder = lir.IRBuilder(vqe__cdkxp)
    osep__nouu = lir.Constant(_word_type, 1)
    if False:
        uyvrh__uxtqg = builder.atomic_rmw(op, szg__sami, osep__nouu,
            ordering=ordering)
        res = getattr(builder, op)(uyvrh__uxtqg, osep__nouu)
        builder.ret(res)
    else:
        uyvrh__uxtqg = builder.load(szg__sami)
        psrpz__mrqbr = getattr(builder, op)(uyvrh__uxtqg, osep__nouu)
        xxp__ydl = builder.icmp_signed('!=', uyvrh__uxtqg, lir.Constant(
            uyvrh__uxtqg.type, -1))
        with cgutils.if_likely(builder, xxp__ydl):
            builder.store(psrpz__mrqbr, szg__sami)
        builder.ret(psrpz__mrqbr)
    return meji__uae


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
        yxyj__mkgbg = state.targetctx.codegen()
        state.library = yxyj__mkgbg.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    mwur__tlum = state.func_ir
    typemap = state.typemap
    pph__sefk = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    uicsb__ghv = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            mwur__tlum, typemap, pph__sefk, calltypes, mangler=targetctx.
            mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            vbqxb__kowv = lowering.Lower(targetctx, library, fndesc,
                mwur__tlum, metadata=metadata)
            vbqxb__kowv.lower()
            if not flags.no_cpython_wrapper:
                vbqxb__kowv.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(pph__sefk, (types.Optional, types.Generator)
                        ):
                        pass
                    else:
                        vbqxb__kowv.create_cfunc_wrapper()
            env = vbqxb__kowv.env
            qlsf__ksx = vbqxb__kowv.call_helper
            del vbqxb__kowv
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, qlsf__ksx, cfunc=None, env=env)
        else:
            oxt__dhg = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(oxt__dhg, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, qlsf__ksx, cfunc=oxt__dhg,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        som__vqh = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = som__vqh - uicsb__ghv
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
        vnbc__hthwl = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, vnbc__hthwl),
            likely=False):
            c.builder.store(cgutils.true_bit, errorptr)
            wmpqm__ytvsx.do_break()
        vxf__hve = c.builder.icmp_signed('!=', vnbc__hthwl, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(vxf__hve, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, vnbc__hthwl)
                c.pyapi.decref(vnbc__hthwl)
                wmpqm__ytvsx.do_break()
        c.pyapi.decref(vnbc__hthwl)
    qqivv__gsy, list = listobj.ListInstance.allocate_ex(c.context, c.
        builder, typ, size)
    with c.builder.if_else(qqivv__gsy, likely=True) as (qiax__ryeo,
        mfjem__bjotg):
        with qiax__ryeo:
            list.size = size
            riwsb__lfmxf = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                riwsb__lfmxf), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        riwsb__lfmxf))
                    with cgutils.for_range(c.builder, size) as wmpqm__ytvsx:
                        itemobj = c.pyapi.list_getitem(obj, wmpqm__ytvsx.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        bkjvp__cgje = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(bkjvp__cgje.is_error, likely
                            =False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            wmpqm__ytvsx.do_break()
                        list.setitem(wmpqm__ytvsx.index, bkjvp__cgje.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with mfjem__bjotg:
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
    wmd__mpcia, peud__ivwvj, edsx__bqgsy, vlneu__ynvf, dmcw__pfv = (
        compile_time_get_string_data(literal_string))
    xyex__pvojk = builder.module
    gv = context.insert_const_bytes(xyex__pvojk, wmd__mpcia)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        peud__ivwvj), context.get_constant(types.int32, edsx__bqgsy),
        context.get_constant(types.uint32, vlneu__ynvf), context.
        get_constant(_Py_hash_t, -1), context.get_constant_null(types.
        MemInfoPointer(types.voidptr)), context.get_constant_null(types.
        pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    bomj__uucr = None
    if isinstance(shape, types.Integer):
        bomj__uucr = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(dsu__vtrh, (types.Integer, types.IntEnumMember)) for
            dsu__vtrh in shape):
            bomj__uucr = len(shape)
    return bomj__uucr


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
            bomj__uucr = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if bomj__uucr == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(bomj__uucr)
                    )
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            ijcd__gazqm = self._get_names(x)
            if len(ijcd__gazqm) != 0:
                return ijcd__gazqm[0]
            return ijcd__gazqm
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    ijcd__gazqm = self._get_names(obj)
    if len(ijcd__gazqm) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(ijcd__gazqm[0])


def get_equiv_set(self, obj):
    ijcd__gazqm = self._get_names(obj)
    if len(ijcd__gazqm) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(ijcd__gazqm[0])


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
    izekl__stm = []
    for krosv__vrl in func_ir.arg_names:
        if krosv__vrl in typemap and isinstance(typemap[krosv__vrl], types.
            containers.UniTuple) and typemap[krosv__vrl].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(krosv__vrl))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for frsa__gsyv in func_ir.blocks.values():
        for stmt in frsa__gsyv.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    cll__iibm = getattr(val, 'code', None)
                    if cll__iibm is not None:
                        if getattr(val, 'closure', None) is not None:
                            zjmj__avje = '<creating a function from a closure>'
                            nqt__bttm = ''
                        else:
                            zjmj__avje = cll__iibm.co_name
                            nqt__bttm = '(%s) ' % zjmj__avje
                    else:
                        zjmj__avje = '<could not ascertain use case>'
                        nqt__bttm = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (zjmj__avje, nqt__bttm))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                tyipu__wriw = False
                if isinstance(val, pytypes.FunctionType):
                    tyipu__wriw = val in {numba.gdb, numba.gdb_init}
                if not tyipu__wriw:
                    tyipu__wriw = getattr(val, '_name', '') == 'gdb_internal'
                if tyipu__wriw:
                    izekl__stm.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    pwflj__ynmot = func_ir.get_definition(var)
                    hljdf__fqjc = guard(find_callname, func_ir, pwflj__ynmot)
                    if hljdf__fqjc and hljdf__fqjc[1] == 'numpy':
                        ty = getattr(numpy, hljdf__fqjc[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    hcwv__ymx = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(hcwv__ymx), loc=stmt.loc)
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
    if len(izekl__stm) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        fdbky__kowln = '\n'.join([x.strformat() for x in izekl__stm])
        raise errors.UnsupportedError(msg % fdbky__kowln)


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
    whr__oqcmo, eiy__rqh = next(iter(val.items()))
    jgttp__agro = typeof_impl(whr__oqcmo, c)
    jzu__zjey = typeof_impl(eiy__rqh, c)
    if jgttp__agro is None or jzu__zjey is None:
        raise ValueError(
            f'Cannot type dict element type {type(whr__oqcmo)}, {type(eiy__rqh)}'
            )
    return types.DictType(jgttp__agro, jzu__zjey)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    qde__nmgbg = cgutils.alloca_once_value(c.builder, val)
    wqd__qzy = c.pyapi.object_hasattr_string(val, '_opaque')
    bav__vddyz = c.builder.icmp_unsigned('==', wqd__qzy, lir.Constant(
        wqd__qzy.type, 0))
    sbvf__jyj = typ.key_type
    ktozr__lik = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(sbvf__jyj, ktozr__lik)

    def copy_dict(out_dict, in_dict):
        for whr__oqcmo, eiy__rqh in in_dict.items():
            out_dict[whr__oqcmo] = eiy__rqh
    with c.builder.if_then(bav__vddyz):
        esapb__ocfe = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        yurmi__iojgf = c.pyapi.call_function_objargs(esapb__ocfe, [])
        gacy__rik = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(gacy__rik, [yurmi__iojgf, val])
        c.builder.store(yurmi__iojgf, qde__nmgbg)
    val = c.builder.load(qde__nmgbg)
    srqgr__qbk = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    vtg__sigoj = c.pyapi.object_type(val)
    zxgv__qcztg = c.builder.icmp_unsigned('==', vtg__sigoj, srqgr__qbk)
    with c.builder.if_else(zxgv__qcztg) as (mzom__jwrjf, gge__cxn):
        with mzom__jwrjf:
            upk__vlis = c.pyapi.object_getattr_string(val, '_opaque')
            pysy__mqzo = types.MemInfoPointer(types.voidptr)
            bkjvp__cgje = c.unbox(pysy__mqzo, upk__vlis)
            mi = bkjvp__cgje.value
            qrmf__sveq = pysy__mqzo, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *qrmf__sveq)
            burky__uey = context.get_constant_null(qrmf__sveq[1])
            args = mi, burky__uey
            smd__yls, utvj__ugo = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, utvj__ugo)
            c.pyapi.decref(upk__vlis)
            ywu__qxpzk = c.builder.basic_block
        with gge__cxn:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", vtg__sigoj, srqgr__qbk)
            wec__hxjvb = c.builder.basic_block
    skkai__aei = c.builder.phi(utvj__ugo.type)
    djvki__ctlz = c.builder.phi(smd__yls.type)
    skkai__aei.add_incoming(utvj__ugo, ywu__qxpzk)
    skkai__aei.add_incoming(utvj__ugo.type(None), wec__hxjvb)
    djvki__ctlz.add_incoming(smd__yls, ywu__qxpzk)
    djvki__ctlz.add_incoming(cgutils.true_bit, wec__hxjvb)
    c.pyapi.decref(srqgr__qbk)
    c.pyapi.decref(vtg__sigoj)
    with c.builder.if_then(bav__vddyz):
        c.pyapi.decref(val)
    return NativeValue(skkai__aei, is_error=djvki__ctlz)


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
    qfvll__bkxrd = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=qfvll__bkxrd, name=updatevar)
    ueokf__twe = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=ueokf__twe, name=res)


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
        for whr__oqcmo, eiy__rqh in other.items():
            d[whr__oqcmo] = eiy__rqh
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
    nqt__bttm = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(nqt__bttm, res)


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
    esx__flgi = PassManager(name)
    if state.func_ir is None:
        esx__flgi.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            esx__flgi.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        esx__flgi.add_pass(FixupArgs, 'fix up args')
    esx__flgi.add_pass(IRProcessing, 'processing IR')
    esx__flgi.add_pass(WithLifting, 'Handle with contexts')
    esx__flgi.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        esx__flgi.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        esx__flgi.add_pass(DeadBranchPrune, 'dead branch pruning')
        esx__flgi.add_pass(GenericRewrites, 'nopython rewrites')
    esx__flgi.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    esx__flgi.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        esx__flgi.add_pass(DeadBranchPrune, 'dead branch pruning')
    esx__flgi.add_pass(FindLiterallyCalls, 'find literally calls')
    esx__flgi.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        esx__flgi.add_pass(ReconstructSSA, 'ssa')
    esx__flgi.add_pass(LiteralPropagationSubPipelinePass, 'Literal propagation'
        )
    esx__flgi.finalize()
    return esx__flgi


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
    a, ucoj__swzh = args
    if isinstance(a, types.List) and isinstance(ucoj__swzh, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(ucoj__swzh, types.List):
        return signature(ucoj__swzh, types.intp, ucoj__swzh)


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
        mverq__laqyx, lrg__tuvrh = 0, 1
    else:
        mverq__laqyx, lrg__tuvrh = 1, 0
    adna__hqwx = ListInstance(context, builder, sig.args[mverq__laqyx],
        args[mverq__laqyx])
    frp__jov = adna__hqwx.size
    xfxey__snl = args[lrg__tuvrh]
    riwsb__lfmxf = lir.Constant(xfxey__snl.type, 0)
    xfxey__snl = builder.select(cgutils.is_neg_int(builder, xfxey__snl),
        riwsb__lfmxf, xfxey__snl)
    kkl__eoitw = builder.mul(xfxey__snl, frp__jov)
    vyl__hpp = ListInstance.allocate(context, builder, sig.return_type,
        kkl__eoitw)
    vyl__hpp.size = kkl__eoitw
    with cgutils.for_range_slice(builder, riwsb__lfmxf, kkl__eoitw,
        frp__jov, inc=True) as (ier__csitv, _):
        with cgutils.for_range(builder, frp__jov) as wmpqm__ytvsx:
            value = adna__hqwx.getitem(wmpqm__ytvsx.index)
            vyl__hpp.setitem(builder.add(wmpqm__ytvsx.index, ier__csitv),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, vyl__hpp.value)


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
    pmbeu__rxmhw = first.unify(self, second)
    if pmbeu__rxmhw is not None:
        return pmbeu__rxmhw
    pmbeu__rxmhw = second.unify(self, first)
    if pmbeu__rxmhw is not None:
        return pmbeu__rxmhw
    rbk__jdhqp = self.can_convert(fromty=first, toty=second)
    if rbk__jdhqp is not None and rbk__jdhqp <= Conversion.safe:
        return second
    rbk__jdhqp = self.can_convert(fromty=second, toty=first)
    if rbk__jdhqp is not None and rbk__jdhqp <= Conversion.safe:
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
    kkl__eoitw = payload.used
    listobj = c.pyapi.list_new(kkl__eoitw)
    qqivv__gsy = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(qqivv__gsy, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(kkl__eoitw
            .type, 0))
        with payload._iterate() as wmpqm__ytvsx:
            i = c.builder.load(index)
            item = wmpqm__ytvsx.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return qqivv__gsy, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    huoy__gdu = h.type
    ezgfx__usjv = self.mask
    dtype = self._ty.dtype
    eupiv__pfspn = context.typing_context
    fnty = eupiv__pfspn.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(eupiv__pfspn, (dtype, dtype), {})
    tunhe__bcx = context.get_function(fnty, sig)
    jsxdw__jwqml = ir.Constant(huoy__gdu, 1)
    zdq__zpdmd = ir.Constant(huoy__gdu, 5)
    unnma__iwc = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, ezgfx__usjv))
    if for_insert:
        ooigf__hhizv = ezgfx__usjv.type(-1)
        ttwa__tez = cgutils.alloca_once_value(builder, ooigf__hhizv)
    ewa__moz = builder.append_basic_block('lookup.body')
    pbo__tyw = builder.append_basic_block('lookup.found')
    atr__kms = builder.append_basic_block('lookup.not_found')
    qjrr__zlour = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        ukz__xqm = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, ukz__xqm)):
            vmiff__gces = tunhe__bcx(builder, (item, entry.key))
            with builder.if_then(vmiff__gces):
                builder.branch(pbo__tyw)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, ukz__xqm)):
            builder.branch(atr__kms)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, ukz__xqm)):
                mlvc__mfvcy = builder.load(ttwa__tez)
                mlvc__mfvcy = builder.select(builder.icmp_unsigned('==',
                    mlvc__mfvcy, ooigf__hhizv), i, mlvc__mfvcy)
                builder.store(mlvc__mfvcy, ttwa__tez)
    with cgutils.for_range(builder, ir.Constant(huoy__gdu, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, jsxdw__jwqml)
        i = builder.and_(i, ezgfx__usjv)
        builder.store(i, index)
    builder.branch(ewa__moz)
    with builder.goto_block(ewa__moz):
        i = builder.load(index)
        check_entry(i)
        ylxqb__hbog = builder.load(unnma__iwc)
        ylxqb__hbog = builder.lshr(ylxqb__hbog, zdq__zpdmd)
        i = builder.add(jsxdw__jwqml, builder.mul(i, zdq__zpdmd))
        i = builder.and_(ezgfx__usjv, builder.add(i, ylxqb__hbog))
        builder.store(i, index)
        builder.store(ylxqb__hbog, unnma__iwc)
        builder.branch(ewa__moz)
    with builder.goto_block(atr__kms):
        if for_insert:
            i = builder.load(index)
            mlvc__mfvcy = builder.load(ttwa__tez)
            i = builder.select(builder.icmp_unsigned('==', mlvc__mfvcy,
                ooigf__hhizv), i, mlvc__mfvcy)
            builder.store(i, index)
        builder.branch(qjrr__zlour)
    with builder.goto_block(pbo__tyw):
        builder.branch(qjrr__zlour)
    builder.position_at_end(qjrr__zlour)
    tyipu__wriw = builder.phi(ir.IntType(1), 'found')
    tyipu__wriw.add_incoming(cgutils.true_bit, pbo__tyw)
    tyipu__wriw.add_incoming(cgutils.false_bit, atr__kms)
    return tyipu__wriw, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    ebeu__dco = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    tjm__yea = payload.used
    jsxdw__jwqml = ir.Constant(tjm__yea.type, 1)
    tjm__yea = payload.used = builder.add(tjm__yea, jsxdw__jwqml)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, ebeu__dco), likely=True):
        payload.fill = builder.add(payload.fill, jsxdw__jwqml)
    if do_resize:
        self.upsize(tjm__yea)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    tyipu__wriw, i = payload._lookup(item, h, for_insert=True)
    zibdi__hxdcb = builder.not_(tyipu__wriw)
    with builder.if_then(zibdi__hxdcb):
        entry = payload.get_entry(i)
        ebeu__dco = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        tjm__yea = payload.used
        jsxdw__jwqml = ir.Constant(tjm__yea.type, 1)
        tjm__yea = payload.used = builder.add(tjm__yea, jsxdw__jwqml)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, ebeu__dco), likely=True):
            payload.fill = builder.add(payload.fill, jsxdw__jwqml)
        if do_resize:
            self.upsize(tjm__yea)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    tjm__yea = payload.used
    jsxdw__jwqml = ir.Constant(tjm__yea.type, 1)
    tjm__yea = payload.used = self._builder.sub(tjm__yea, jsxdw__jwqml)
    if do_resize:
        self.downsize(tjm__yea)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    gxp__xvgxp = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, gxp__xvgxp)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    ngsvi__onfgh = payload
    qqivv__gsy = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(qqivv__gsy), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with ngsvi__onfgh._iterate() as wmpqm__ytvsx:
        entry = wmpqm__ytvsx.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(ngsvi__onfgh.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as wmpqm__ytvsx:
        entry = wmpqm__ytvsx.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    qqivv__gsy = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(qqivv__gsy), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    qqivv__gsy = cgutils.alloca_once_value(builder, cgutils.true_bit)
    huoy__gdu = context.get_value_type(types.intp)
    riwsb__lfmxf = ir.Constant(huoy__gdu, 0)
    jsxdw__jwqml = ir.Constant(huoy__gdu, 1)
    ilh__qpexi = context.get_data_type(types.SetPayload(self._ty))
    czzj__sile = context.get_abi_sizeof(ilh__qpexi)
    dajo__gku = self._entrysize
    czzj__sile -= dajo__gku
    ejcl__hwyn, zhsjk__fnxbv = cgutils.muladd_with_overflow(builder,
        nentries, ir.Constant(huoy__gdu, dajo__gku), ir.Constant(huoy__gdu,
        czzj__sile))
    with builder.if_then(zhsjk__fnxbv, likely=False):
        builder.store(cgutils.false_bit, qqivv__gsy)
    with builder.if_then(builder.load(qqivv__gsy), likely=True):
        if realloc:
            qcy__sxgyx = self._set.meminfo
            szg__sami = context.nrt.meminfo_varsize_alloc(builder,
                qcy__sxgyx, size=ejcl__hwyn)
            hpri__pbj = cgutils.is_null(builder, szg__sami)
        else:
            mipv__suoer = _imp_dtor(context, builder.module, self._ty)
            qcy__sxgyx = context.nrt.meminfo_new_varsize_dtor(builder,
                ejcl__hwyn, builder.bitcast(mipv__suoer, cgutils.voidptr_t))
            hpri__pbj = cgutils.is_null(builder, qcy__sxgyx)
        with builder.if_else(hpri__pbj, likely=False) as (niym__awen,
            qiax__ryeo):
            with niym__awen:
                builder.store(cgutils.false_bit, qqivv__gsy)
            with qiax__ryeo:
                if not realloc:
                    self._set.meminfo = qcy__sxgyx
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, ejcl__hwyn, 255)
                payload.used = riwsb__lfmxf
                payload.fill = riwsb__lfmxf
                payload.finger = riwsb__lfmxf
                ila__hwjn = builder.sub(nentries, jsxdw__jwqml)
                payload.mask = ila__hwjn
    return builder.load(qqivv__gsy)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    qqivv__gsy = cgutils.alloca_once_value(builder, cgutils.true_bit)
    huoy__gdu = context.get_value_type(types.intp)
    riwsb__lfmxf = ir.Constant(huoy__gdu, 0)
    jsxdw__jwqml = ir.Constant(huoy__gdu, 1)
    ilh__qpexi = context.get_data_type(types.SetPayload(self._ty))
    czzj__sile = context.get_abi_sizeof(ilh__qpexi)
    dajo__gku = self._entrysize
    czzj__sile -= dajo__gku
    ezgfx__usjv = src_payload.mask
    nentries = builder.add(jsxdw__jwqml, ezgfx__usjv)
    ejcl__hwyn = builder.add(ir.Constant(huoy__gdu, czzj__sile), builder.
        mul(ir.Constant(huoy__gdu, dajo__gku), nentries))
    with builder.if_then(builder.load(qqivv__gsy), likely=True):
        mipv__suoer = _imp_dtor(context, builder.module, self._ty)
        qcy__sxgyx = context.nrt.meminfo_new_varsize_dtor(builder,
            ejcl__hwyn, builder.bitcast(mipv__suoer, cgutils.voidptr_t))
        hpri__pbj = cgutils.is_null(builder, qcy__sxgyx)
        with builder.if_else(hpri__pbj, likely=False) as (niym__awen,
            qiax__ryeo):
            with niym__awen:
                builder.store(cgutils.false_bit, qqivv__gsy)
            with qiax__ryeo:
                self._set.meminfo = qcy__sxgyx
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = riwsb__lfmxf
                payload.mask = ezgfx__usjv
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, dajo__gku)
                with src_payload._iterate() as wmpqm__ytvsx:
                    context.nrt.incref(builder, self._ty.dtype,
                        wmpqm__ytvsx.entry.key)
    return builder.load(qqivv__gsy)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    roe__woy = context.get_value_type(types.voidptr)
    jypgf__wytni = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [roe__woy, jypgf__wytni, roe__woy])
    kzgt__omxtl = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=kzgt__omxtl)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        pxdvl__bugk = builder.bitcast(fn.args[0], cgutils.voidptr_t.
            as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, pxdvl__bugk)
        with payload._iterate() as wmpqm__ytvsx:
            entry = wmpqm__ytvsx.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    adbw__nekgd, = sig.args
    dxhs__lgb, = args
    meoq__ufz = numba.core.imputils.call_len(context, builder, adbw__nekgd,
        dxhs__lgb)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, meoq__ufz)
    with numba.core.imputils.for_iter(context, builder, adbw__nekgd, dxhs__lgb
        ) as wmpqm__ytvsx:
        inst.add(wmpqm__ytvsx.value)
        context.nrt.decref(builder, set_type.dtype, wmpqm__ytvsx.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    adbw__nekgd = sig.args[1]
    dxhs__lgb = args[1]
    meoq__ufz = numba.core.imputils.call_len(context, builder, adbw__nekgd,
        dxhs__lgb)
    if meoq__ufz is not None:
        qfwk__xirl = builder.add(inst.payload.used, meoq__ufz)
        inst.upsize(qfwk__xirl)
    with numba.core.imputils.for_iter(context, builder, adbw__nekgd, dxhs__lgb
        ) as wmpqm__ytvsx:
        kkb__tmq = context.cast(builder, wmpqm__ytvsx.value, adbw__nekgd.
            dtype, inst.dtype)
        inst.add(kkb__tmq)
        context.nrt.decref(builder, adbw__nekgd.dtype, wmpqm__ytvsx.value)
    if meoq__ufz is not None:
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
    pospn__gvou = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, pospn__gvou, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    oxt__dhg = target_context.get_executable(library, fndesc, env)
    tasyk__xqlq = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=oxt__dhg, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return tasyk__xqlq


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
