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
    gld__opwhb = keyword_expr.items.copy()
    kii__sfhc = keyword_expr.value_indexes
    for xdvh__gnv, ixv__zqu in kii__sfhc.items():
        gld__opwhb[ixv__zqu] = xdvh__gnv, gld__opwhb[ixv__zqu][1]
    new_body[buildmap_idx] = None
    return gld__opwhb


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    jvtga__oashy = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    gld__opwhb = []
    kpuq__hzn = buildmap_idx + 1
    while kpuq__hzn <= search_end:
        zjrfb__hfbqj = body[kpuq__hzn]
        if not (isinstance(zjrfb__hfbqj, ir.Assign) and isinstance(
            zjrfb__hfbqj.value, ir.Const)):
            raise UnsupportedError(jvtga__oashy)
        majn__ekvq = zjrfb__hfbqj.target.name
        npq__dxn = zjrfb__hfbqj.value.value
        kpuq__hzn += 1
        erpsa__atv = True
        while kpuq__hzn <= search_end and erpsa__atv:
            ujw__iih = body[kpuq__hzn]
            if (isinstance(ujw__iih, ir.Assign) and isinstance(ujw__iih.
                value, ir.Expr) and ujw__iih.value.op == 'getattr' and 
                ujw__iih.value.value.name == buildmap_name and ujw__iih.
                value.attr == '__setitem__'):
                erpsa__atv = False
            else:
                kpuq__hzn += 1
        if erpsa__atv or kpuq__hzn == search_end:
            raise UnsupportedError(jvtga__oashy)
        nnre__xhce = body[kpuq__hzn + 1]
        if not (isinstance(nnre__xhce, ir.Assign) and isinstance(nnre__xhce
            .value, ir.Expr) and nnre__xhce.value.op == 'call' and 
            nnre__xhce.value.func.name == ujw__iih.target.name and len(
            nnre__xhce.value.args) == 2 and nnre__xhce.value.args[0].name ==
            majn__ekvq):
            raise UnsupportedError(jvtga__oashy)
        mwdai__fto = nnre__xhce.value.args[1]
        gld__opwhb.append((npq__dxn, mwdai__fto))
        new_body[kpuq__hzn] = None
        new_body[kpuq__hzn + 1] = None
        kpuq__hzn += 2
    return gld__opwhb


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    jvtga__oashy = 'CALL_FUNCTION_EX with **kwargs not supported'
    kpuq__hzn = 0
    dwsl__vzxav = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        wnki__tyvhd = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        wnki__tyvhd = vararg_stmt.target.name
    kxbul__arlq = True
    while search_end >= kpuq__hzn and kxbul__arlq:
        qetz__rbgd = body[search_end]
        if (isinstance(qetz__rbgd, ir.Assign) and qetz__rbgd.target.name ==
            wnki__tyvhd and isinstance(qetz__rbgd.value, ir.Expr) and 
            qetz__rbgd.value.op == 'build_tuple' and not qetz__rbgd.value.items
            ):
            kxbul__arlq = False
            new_body[search_end] = None
        else:
            if search_end == kpuq__hzn or not (isinstance(qetz__rbgd, ir.
                Assign) and qetz__rbgd.target.name == wnki__tyvhd and
                isinstance(qetz__rbgd.value, ir.Expr) and qetz__rbgd.value.
                op == 'binop' and qetz__rbgd.value.fn == operator.add):
                raise UnsupportedError(jvtga__oashy)
            fvd__huad = qetz__rbgd.value.lhs.name
            kwwc__qrt = qetz__rbgd.value.rhs.name
            xjejp__ppi = body[search_end - 1]
            if not (isinstance(xjejp__ppi, ir.Assign) and isinstance(
                xjejp__ppi.value, ir.Expr) and xjejp__ppi.value.op ==
                'build_tuple' and len(xjejp__ppi.value.items) == 1):
                raise UnsupportedError(jvtga__oashy)
            if xjejp__ppi.target.name == fvd__huad:
                wnki__tyvhd = kwwc__qrt
            elif xjejp__ppi.target.name == kwwc__qrt:
                wnki__tyvhd = fvd__huad
            else:
                raise UnsupportedError(jvtga__oashy)
            dwsl__vzxav.append(xjejp__ppi.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            clyy__qivd = True
            while search_end >= kpuq__hzn and clyy__qivd:
                hythr__ozq = body[search_end]
                if isinstance(hythr__ozq, ir.Assign
                    ) and hythr__ozq.target.name == wnki__tyvhd:
                    clyy__qivd = False
                else:
                    search_end -= 1
    if kxbul__arlq:
        raise UnsupportedError(jvtga__oashy)
    return dwsl__vzxav[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    jvtga__oashy = 'CALL_FUNCTION_EX with **kwargs not supported'
    for esc__waspi in func_ir.blocks.values():
        gmk__fewt = False
        new_body = []
        for fjueh__pxwf, hmxj__ivrlk in enumerate(esc__waspi.body):
            if (isinstance(hmxj__ivrlk, ir.Assign) and isinstance(
                hmxj__ivrlk.value, ir.Expr) and hmxj__ivrlk.value.op ==
                'call' and hmxj__ivrlk.value.varkwarg is not None):
                gmk__fewt = True
                bhpt__ofaj = hmxj__ivrlk.value
                args = bhpt__ofaj.args
                gld__opwhb = bhpt__ofaj.kws
                rrj__uoep = bhpt__ofaj.vararg
                ffeub__cvri = bhpt__ofaj.varkwarg
                dxy__sod = fjueh__pxwf - 1
                ftfvv__vhdkx = dxy__sod
                jpc__mxb = None
                wgiql__zyv = True
                while ftfvv__vhdkx >= 0 and wgiql__zyv:
                    jpc__mxb = esc__waspi.body[ftfvv__vhdkx]
                    if isinstance(jpc__mxb, ir.Assign
                        ) and jpc__mxb.target.name == ffeub__cvri.name:
                        wgiql__zyv = False
                    else:
                        ftfvv__vhdkx -= 1
                if gld__opwhb or wgiql__zyv or not (isinstance(jpc__mxb.
                    value, ir.Expr) and jpc__mxb.value.op == 'build_map'):
                    raise UnsupportedError(jvtga__oashy)
                if jpc__mxb.value.items:
                    gld__opwhb = _call_function_ex_replace_kws_small(jpc__mxb
                        .value, new_body, ftfvv__vhdkx)
                else:
                    gld__opwhb = _call_function_ex_replace_kws_large(esc__waspi
                        .body, ffeub__cvri.name, ftfvv__vhdkx, fjueh__pxwf -
                        1, new_body)
                dxy__sod = ftfvv__vhdkx
                if rrj__uoep is not None:
                    if args:
                        raise UnsupportedError(jvtga__oashy)
                    oayh__asnlj = dxy__sod
                    wtzu__uact = None
                    wgiql__zyv = True
                    while oayh__asnlj >= 0 and wgiql__zyv:
                        wtzu__uact = esc__waspi.body[oayh__asnlj]
                        if isinstance(wtzu__uact, ir.Assign
                            ) and wtzu__uact.target.name == rrj__uoep.name:
                            wgiql__zyv = False
                        else:
                            oayh__asnlj -= 1
                    if wgiql__zyv:
                        raise UnsupportedError(jvtga__oashy)
                    if isinstance(wtzu__uact.value, ir.Expr
                        ) and wtzu__uact.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(wtzu__uact
                            .value, new_body, oayh__asnlj)
                    else:
                        args = _call_function_ex_replace_args_large(wtzu__uact,
                            esc__waspi.body, new_body, oayh__asnlj)
                glbr__fhsio = ir.Expr.call(bhpt__ofaj.func, args,
                    gld__opwhb, bhpt__ofaj.loc, target=bhpt__ofaj.target)
                if hmxj__ivrlk.target.name in func_ir._definitions and len(
                    func_ir._definitions[hmxj__ivrlk.target.name]) == 1:
                    func_ir._definitions[hmxj__ivrlk.target.name].clear()
                func_ir._definitions[hmxj__ivrlk.target.name].append(
                    glbr__fhsio)
                hmxj__ivrlk = ir.Assign(glbr__fhsio, hmxj__ivrlk.target,
                    hmxj__ivrlk.loc)
            new_body.append(hmxj__ivrlk)
        if gmk__fewt:
            esc__waspi.body = [pnsu__npv for pnsu__npv in new_body if 
                pnsu__npv is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for esc__waspi in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        gmk__fewt = False
        for fjueh__pxwf, hmxj__ivrlk in enumerate(esc__waspi.body):
            vrevt__fro = True
            ufm__bbhp = None
            if isinstance(hmxj__ivrlk, ir.Assign) and isinstance(hmxj__ivrlk
                .value, ir.Expr):
                if hmxj__ivrlk.value.op == 'build_map':
                    ufm__bbhp = hmxj__ivrlk.target.name
                    lit_old_idx[hmxj__ivrlk.target.name] = fjueh__pxwf
                    lit_new_idx[hmxj__ivrlk.target.name] = fjueh__pxwf
                    map_updates[hmxj__ivrlk.target.name
                        ] = hmxj__ivrlk.value.items.copy()
                    vrevt__fro = False
                elif hmxj__ivrlk.value.op == 'call' and fjueh__pxwf > 0:
                    lmwtu__glf = hmxj__ivrlk.value.func.name
                    ujw__iih = esc__waspi.body[fjueh__pxwf - 1]
                    args = hmxj__ivrlk.value.args
                    if (isinstance(ujw__iih, ir.Assign) and ujw__iih.target
                        .name == lmwtu__glf and isinstance(ujw__iih.value,
                        ir.Expr) and ujw__iih.value.op == 'getattr' and 
                        ujw__iih.value.value.name in lit_old_idx):
                        tnkhv__bnx = ujw__iih.value.value.name
                        yyum__fsmfj = ujw__iih.value.attr
                        if yyum__fsmfj == '__setitem__':
                            vrevt__fro = False
                            map_updates[tnkhv__bnx].append(args)
                            new_body[-1] = None
                        elif yyum__fsmfj == 'update' and args[0
                            ].name in lit_old_idx:
                            vrevt__fro = False
                            map_updates[tnkhv__bnx].extend(map_updates[args
                                [0].name])
                            new_body[-1] = None
                        if not vrevt__fro:
                            lit_new_idx[tnkhv__bnx] = fjueh__pxwf
                            func_ir._definitions[ujw__iih.target.name].remove(
                                ujw__iih.value)
            if not (isinstance(hmxj__ivrlk, ir.Assign) and isinstance(
                hmxj__ivrlk.value, ir.Expr) and hmxj__ivrlk.value.op ==
                'getattr' and hmxj__ivrlk.value.value.name in lit_old_idx and
                hmxj__ivrlk.value.attr in ('__setitem__', 'update')):
                for tvsw__aqujy in hmxj__ivrlk.list_vars():
                    if (tvsw__aqujy.name in lit_old_idx and tvsw__aqujy.
                        name != ufm__bbhp):
                        _insert_build_map(func_ir, tvsw__aqujy.name,
                            esc__waspi.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if vrevt__fro:
                new_body.append(hmxj__ivrlk)
            else:
                func_ir._definitions[hmxj__ivrlk.target.name].remove(
                    hmxj__ivrlk.value)
                gmk__fewt = True
                new_body.append(None)
        fayo__ncuo = list(lit_old_idx.keys())
        for jrmp__ttxu in fayo__ncuo:
            _insert_build_map(func_ir, jrmp__ttxu, esc__waspi.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if gmk__fewt:
            esc__waspi.body = [pnsu__npv for pnsu__npv in new_body if 
                pnsu__npv is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    hixr__bsnr = lit_old_idx[name]
    maa__qgy = lit_new_idx[name]
    lhewp__sjb = map_updates[name]
    new_body[maa__qgy] = _build_new_build_map(func_ir, name, old_body,
        hixr__bsnr, lhewp__sjb)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    ycusd__bxu = old_body[old_lineno]
    cbdd__jrzpf = ycusd__bxu.target
    whxd__rihdu = ycusd__bxu.value
    guk__rjnb = []
    xwm__bhika = []
    for teh__ducy in new_items:
        nyhu__btgb, mswy__ibz = teh__ducy
        pfa__tdz = guard(get_definition, func_ir, nyhu__btgb)
        if isinstance(pfa__tdz, (ir.Const, ir.Global, ir.FreeVar)):
            guk__rjnb.append(pfa__tdz.value)
        udp__rohi = guard(get_definition, func_ir, mswy__ibz)
        if isinstance(udp__rohi, (ir.Const, ir.Global, ir.FreeVar)):
            xwm__bhika.append(udp__rohi.value)
        else:
            xwm__bhika.append(numba.core.interpreter._UNKNOWN_VALUE(
                mswy__ibz.name))
    kii__sfhc = {}
    if len(guk__rjnb) == len(new_items):
        lyt__dnp = {pnsu__npv: fkh__ibpg for pnsu__npv, fkh__ibpg in zip(
            guk__rjnb, xwm__bhika)}
        for fjueh__pxwf, nyhu__btgb in enumerate(guk__rjnb):
            kii__sfhc[nyhu__btgb] = fjueh__pxwf
    else:
        lyt__dnp = None
    suddc__xyq = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=lyt__dnp, value_indexes=kii__sfhc, loc=whxd__rihdu.loc)
    func_ir._definitions[name].append(suddc__xyq)
    return ir.Assign(suddc__xyq, ir.Var(cbdd__jrzpf.scope, name,
        cbdd__jrzpf.loc), suddc__xyq.loc)
