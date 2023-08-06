"""
transforms the IR to handle bytecode issues in Python 3.10. This
should be removed once https://github.com/numba/numba/pull/7866
is included in Numba 0.56
"""
import operator
import numba
from numba.core import ir
from numba.core.compiler_machinery import FunctionPass, register_pass
from numba.core.errors import UnsupportedError
from numba.core.ir_utils import dprint_func_ir, get_definition, guard


@register_pass(mutates_CFG=False, analysis_only=False)
class Bodo310ByteCodePass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        dprint_func_ir(state.func_ir,
            'starting Bodo 3.10 Bytecode optimizations pass')
        peep_hole_call_function_ex_to_call_function_kw(state.func_ir)
        peep_hole_fuse_dict_add_updates(state.func_ir)
        return True


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    byc__ejv = keyword_expr.items.copy()
    nzxyz__nvzqh = keyword_expr.value_indexes
    for wgin__yoxll, pjg__oinws in nzxyz__nvzqh.items():
        byc__ejv[pjg__oinws] = wgin__yoxll, byc__ejv[pjg__oinws][1]
    new_body[buildmap_idx] = None
    return byc__ejv


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    lcth__wzrrv = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    byc__ejv = []
    jnp__fnda = buildmap_idx + 1
    while jnp__fnda <= search_end:
        cpxdg__vxoe = body[jnp__fnda]
        if not (isinstance(cpxdg__vxoe, ir.Assign) and isinstance(
            cpxdg__vxoe.value, ir.Const)):
            raise UnsupportedError(lcth__wzrrv)
        ivll__qvx = cpxdg__vxoe.target.name
        cxkw__hhek = cpxdg__vxoe.value.value
        jnp__fnda += 1
        fktw__ytw = True
        while jnp__fnda <= search_end and fktw__ytw:
            aemoh__baq = body[jnp__fnda]
            if (isinstance(aemoh__baq, ir.Assign) and isinstance(aemoh__baq
                .value, ir.Expr) and aemoh__baq.value.op == 'getattr' and 
                aemoh__baq.value.value.name == buildmap_name and aemoh__baq
                .value.attr == '__setitem__'):
                fktw__ytw = False
            else:
                jnp__fnda += 1
        if fktw__ytw or jnp__fnda == search_end:
            raise UnsupportedError(lcth__wzrrv)
        wrpz__rqvxu = body[jnp__fnda + 1]
        if not (isinstance(wrpz__rqvxu, ir.Assign) and isinstance(
            wrpz__rqvxu.value, ir.Expr) and wrpz__rqvxu.value.op == 'call' and
            wrpz__rqvxu.value.func.name == aemoh__baq.target.name and len(
            wrpz__rqvxu.value.args) == 2 and wrpz__rqvxu.value.args[0].name ==
            ivll__qvx):
            raise UnsupportedError(lcth__wzrrv)
        nkpj__blody = wrpz__rqvxu.value.args[1]
        byc__ejv.append((cxkw__hhek, nkpj__blody))
        new_body[jnp__fnda] = None
        new_body[jnp__fnda + 1] = None
        jnp__fnda += 2
    return byc__ejv


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    lcth__wzrrv = 'CALL_FUNCTION_EX with **kwargs not supported'
    jnp__fnda = 0
    jzur__wdnft = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        snhcy__rsepp = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        snhcy__rsepp = vararg_stmt.target.name
    xsp__mad = True
    while search_end >= jnp__fnda and xsp__mad:
        brl__nxdw = body[search_end]
        if (isinstance(brl__nxdw, ir.Assign) and brl__nxdw.target.name ==
            snhcy__rsepp and isinstance(brl__nxdw.value, ir.Expr) and 
            brl__nxdw.value.op == 'build_tuple' and not brl__nxdw.value.items):
            xsp__mad = False
            new_body[search_end] = None
        else:
            if search_end == jnp__fnda or not (isinstance(brl__nxdw, ir.
                Assign) and brl__nxdw.target.name == snhcy__rsepp and
                isinstance(brl__nxdw.value, ir.Expr) and brl__nxdw.value.op ==
                'binop' and brl__nxdw.value.fn == operator.add):
                raise UnsupportedError(lcth__wzrrv)
            mocb__kxdf = brl__nxdw.value.lhs.name
            jvt__xul = brl__nxdw.value.rhs.name
            fqz__iwlf = body[search_end - 1]
            if not (isinstance(fqz__iwlf, ir.Assign) and isinstance(
                fqz__iwlf.value, ir.Expr) and fqz__iwlf.value.op ==
                'build_tuple' and len(fqz__iwlf.value.items) == 1):
                raise UnsupportedError(lcth__wzrrv)
            if fqz__iwlf.target.name == mocb__kxdf:
                snhcy__rsepp = jvt__xul
            elif fqz__iwlf.target.name == jvt__xul:
                snhcy__rsepp = mocb__kxdf
            else:
                raise UnsupportedError(lcth__wzrrv)
            jzur__wdnft.append(fqz__iwlf.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            yve__izx = True
            while search_end >= jnp__fnda and yve__izx:
                ufek__hyaz = body[search_end]
                if isinstance(ufek__hyaz, ir.Assign
                    ) and ufek__hyaz.target.name == snhcy__rsepp:
                    yve__izx = False
                else:
                    search_end -= 1
    if xsp__mad:
        raise UnsupportedError(lcth__wzrrv)
    return jzur__wdnft[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    lcth__wzrrv = 'CALL_FUNCTION_EX with **kwargs not supported'
    for nnwl__bjsu in func_ir.blocks.values():
        qooqm__pom = False
        new_body = []
        for cyp__plavt, pqr__frap in enumerate(nnwl__bjsu.body):
            if (isinstance(pqr__frap, ir.Assign) and isinstance(pqr__frap.
                value, ir.Expr) and pqr__frap.value.op == 'call' and 
                pqr__frap.value.varkwarg is not None):
                qooqm__pom = True
                xkizn__hovo = pqr__frap.value
                args = xkizn__hovo.args
                byc__ejv = xkizn__hovo.kws
                xknu__hhk = xkizn__hovo.vararg
                siyvu__lobs = xkizn__hovo.varkwarg
                quale__vdr = cyp__plavt - 1
                bba__csc = quale__vdr
                cpl__bxobc = None
                mewst__acx = True
                while bba__csc >= 0 and mewst__acx:
                    cpl__bxobc = nnwl__bjsu.body[bba__csc]
                    if isinstance(cpl__bxobc, ir.Assign
                        ) and cpl__bxobc.target.name == siyvu__lobs.name:
                        mewst__acx = False
                    else:
                        bba__csc -= 1
                if byc__ejv or mewst__acx or not (isinstance(cpl__bxobc.
                    value, ir.Expr) and cpl__bxobc.value.op == 'build_map'):
                    raise UnsupportedError(lcth__wzrrv)
                if cpl__bxobc.value.items:
                    byc__ejv = _call_function_ex_replace_kws_small(cpl__bxobc
                        .value, new_body, bba__csc)
                else:
                    byc__ejv = _call_function_ex_replace_kws_large(nnwl__bjsu
                        .body, siyvu__lobs.name, bba__csc, cyp__plavt - 1,
                        new_body)
                quale__vdr = bba__csc
                if xknu__hhk is not None:
                    if args:
                        raise UnsupportedError(lcth__wzrrv)
                    nnrqu__tpz = quale__vdr
                    evvb__yxc = None
                    mewst__acx = True
                    while nnrqu__tpz >= 0 and mewst__acx:
                        evvb__yxc = nnwl__bjsu.body[nnrqu__tpz]
                        if isinstance(evvb__yxc, ir.Assign
                            ) and evvb__yxc.target.name == xknu__hhk.name:
                            mewst__acx = False
                        else:
                            nnrqu__tpz -= 1
                    if mewst__acx:
                        raise UnsupportedError(lcth__wzrrv)
                    if isinstance(evvb__yxc.value, ir.Expr
                        ) and evvb__yxc.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(evvb__yxc
                            .value, new_body, nnrqu__tpz)
                    else:
                        args = _call_function_ex_replace_args_large(evvb__yxc,
                            nnwl__bjsu.body, new_body, nnrqu__tpz)
                huye__ghahp = ir.Expr.call(xkizn__hovo.func, args, byc__ejv,
                    xkizn__hovo.loc, target=xkizn__hovo.target)
                if pqr__frap.target.name in func_ir._definitions and len(
                    func_ir._definitions[pqr__frap.target.name]) == 1:
                    func_ir._definitions[pqr__frap.target.name].clear()
                func_ir._definitions[pqr__frap.target.name].append(huye__ghahp)
                pqr__frap = ir.Assign(huye__ghahp, pqr__frap.target,
                    pqr__frap.loc)
            new_body.append(pqr__frap)
        if qooqm__pom:
            nnwl__bjsu.body = [mdds__xijx for mdds__xijx in new_body if 
                mdds__xijx is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for nnwl__bjsu in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        qooqm__pom = False
        for cyp__plavt, pqr__frap in enumerate(nnwl__bjsu.body):
            tehw__jtd = True
            oat__krro = None
            if isinstance(pqr__frap, ir.Assign) and isinstance(pqr__frap.
                value, ir.Expr):
                if pqr__frap.value.op == 'build_map':
                    oat__krro = pqr__frap.target.name
                    lit_old_idx[pqr__frap.target.name] = cyp__plavt
                    lit_new_idx[pqr__frap.target.name] = cyp__plavt
                    map_updates[pqr__frap.target.name
                        ] = pqr__frap.value.items.copy()
                    tehw__jtd = False
                elif pqr__frap.value.op == 'call' and cyp__plavt > 0:
                    qnih__vex = pqr__frap.value.func.name
                    aemoh__baq = nnwl__bjsu.body[cyp__plavt - 1]
                    args = pqr__frap.value.args
                    if (isinstance(aemoh__baq, ir.Assign) and aemoh__baq.
                        target.name == qnih__vex and isinstance(aemoh__baq.
                        value, ir.Expr) and aemoh__baq.value.op ==
                        'getattr' and aemoh__baq.value.value.name in
                        lit_old_idx):
                        hwf__rhdj = aemoh__baq.value.value.name
                        dctc__nar = aemoh__baq.value.attr
                        if dctc__nar == '__setitem__':
                            tehw__jtd = False
                            map_updates[hwf__rhdj].append(args)
                            new_body[-1] = None
                        elif dctc__nar == 'update' and args[0
                            ].name in lit_old_idx:
                            tehw__jtd = False
                            map_updates[hwf__rhdj].extend(map_updates[args[
                                0].name])
                            new_body[-1] = None
                        if not tehw__jtd:
                            lit_new_idx[hwf__rhdj] = cyp__plavt
                            func_ir._definitions[aemoh__baq.target.name
                                ].remove(aemoh__baq.value)
            if not (isinstance(pqr__frap, ir.Assign) and isinstance(
                pqr__frap.value, ir.Expr) and pqr__frap.value.op ==
                'getattr' and pqr__frap.value.value.name in lit_old_idx and
                pqr__frap.value.attr in ('__setitem__', 'update')):
                for aputo__uqza in pqr__frap.list_vars():
                    if (aputo__uqza.name in lit_old_idx and aputo__uqza.
                        name != oat__krro):
                        _insert_build_map(func_ir, aputo__uqza.name,
                            nnwl__bjsu.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if tehw__jtd:
                new_body.append(pqr__frap)
            else:
                func_ir._definitions[pqr__frap.target.name].remove(pqr__frap
                    .value)
                qooqm__pom = True
                new_body.append(None)
        iafch__abaqm = list(lit_old_idx.keys())
        for odhd__iuo in iafch__abaqm:
            _insert_build_map(func_ir, odhd__iuo, nnwl__bjsu.body, new_body,
                lit_old_idx, lit_new_idx, map_updates)
        if qooqm__pom:
            nnwl__bjsu.body = [mdds__xijx for mdds__xijx in new_body if 
                mdds__xijx is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    bsdk__socmo = lit_old_idx[name]
    kfmje__zvtf = lit_new_idx[name]
    wkf__pyal = map_updates[name]
    new_body[kfmje__zvtf] = _build_new_build_map(func_ir, name, old_body,
        bsdk__socmo, wkf__pyal)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    dwap__gmui = old_body[old_lineno]
    aucs__owge = dwap__gmui.target
    rpick__cgxo = dwap__gmui.value
    ndd__goqjp = []
    zpn__qoeh = []
    for sja__gmtde in new_items:
        wolfb__sfurc, abad__ugtmo = sja__gmtde
        jeftd__geuf = guard(get_definition, func_ir, wolfb__sfurc)
        if isinstance(jeftd__geuf, (ir.Const, ir.Global, ir.FreeVar)):
            ndd__goqjp.append(jeftd__geuf.value)
        ahbcm__jin = guard(get_definition, func_ir, abad__ugtmo)
        if isinstance(ahbcm__jin, (ir.Const, ir.Global, ir.FreeVar)):
            zpn__qoeh.append(ahbcm__jin.value)
        else:
            zpn__qoeh.append(numba.core.interpreter._UNKNOWN_VALUE(
                abad__ugtmo.name))
    nzxyz__nvzqh = {}
    if len(ndd__goqjp) == len(new_items):
        odr__blw = {mdds__xijx: htm__uhv for mdds__xijx, htm__uhv in zip(
            ndd__goqjp, zpn__qoeh)}
        for cyp__plavt, wolfb__sfurc in enumerate(ndd__goqjp):
            nzxyz__nvzqh[wolfb__sfurc] = cyp__plavt
    else:
        odr__blw = None
    kgkir__hejsa = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=odr__blw, value_indexes=nzxyz__nvzqh, loc=rpick__cgxo.loc
        )
    func_ir._definitions[name].append(kgkir__hejsa)
    return ir.Assign(kgkir__hejsa, ir.Var(aucs__owge.scope, name,
        aucs__owge.loc), kgkir__hejsa.loc)
