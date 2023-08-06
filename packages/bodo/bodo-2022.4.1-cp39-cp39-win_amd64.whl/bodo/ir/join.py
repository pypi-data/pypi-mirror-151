"""IR node for the join and merge"""
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes, replace_vars_inner, visit_vars_inner
from numba.extending import intrinsic, overload
import bodo
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, hash_join_table, info_from_table, info_to_array
from bodo.libs.int_arr_ext import IntDtype
from bodo.libs.str_arr_ext import cp_str_list_to_array, to_list_if_immutable_arr
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.typing import BodoError, dtype_to_array_type, find_common_np_dtype, is_dtype_nullable, is_nullable_type, is_str_arr_type, to_nullable_type
from bodo.utils.utils import alloc_arr_tup, debug_prints, is_null_pointer
join_gen_cond_cfunc = {}
join_gen_cond_cfunc_addr = {}


@intrinsic
def add_join_gen_cond_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        uacj__gkd = func.signature
        vsiwk__temah = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        fxcuf__htd = cgutils.get_or_insert_function(builder.module,
            vsiwk__temah, sym._literal_value)
        builder.call(fxcuf__htd, [context.get_constant_null(uacj__gkd.args[
            0]), context.get_constant_null(uacj__gkd.args[1]), context.
            get_constant_null(uacj__gkd.args[2]), context.get_constant_null
            (uacj__gkd.args[3]), context.get_constant_null(uacj__gkd.args[4
            ]), context.get_constant_null(uacj__gkd.args[5]), context.
            get_constant(types.int64, 0), context.get_constant(types.int64, 0)]
            )
        context.add_linking_libs([join_gen_cond_cfunc[sym._literal_value].
            _library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_join_cond_addr(name):
    with numba.objmode(addr='int64'):
        addr = join_gen_cond_cfunc_addr[name]
    return addr


class Join(ir.Stmt):

    def __init__(self, df_out, left_df, right_df, left_keys, right_keys,
        out_data_vars, left_vars, right_vars, how, suffix_x, suffix_y, loc,
        is_left, is_right, is_join, left_index, right_index, indicator,
        is_na_equal, gen_cond_expr):
        self.df_out = df_out
        self.left_df = left_df
        self.right_df = right_df
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.out_data_vars = out_data_vars
        self.left_vars = left_vars
        self.right_vars = right_vars
        self.how = how
        self.suffix_x = suffix_x
        self.suffix_y = suffix_y
        self.loc = loc
        self.is_left = is_left
        self.is_right = is_right
        self.is_join = is_join
        self.left_index = left_index
        self.right_index = right_index
        self.indicator = indicator
        self.is_na_equal = is_na_equal
        self.gen_cond_expr = gen_cond_expr
        self.left_cond_cols = set(xpxp__bhttq for xpxp__bhttq in left_vars.
            keys() if f'(left.{xpxp__bhttq})' in gen_cond_expr)
        self.right_cond_cols = set(xpxp__bhttq for xpxp__bhttq in
            right_vars.keys() if f'(right.{xpxp__bhttq})' in gen_cond_expr)
        aivyi__rwtog = set(left_keys) & set(right_keys)
        lsjyu__mkjvn = set(left_vars.keys()) & set(right_vars.keys())
        qpnj__jdnq = lsjyu__mkjvn - aivyi__rwtog
        vect_same_key = []
        n_keys = len(left_keys)
        for xkh__huaar in range(n_keys):
            veqhi__mvnj = left_keys[xkh__huaar]
            satv__rodz = right_keys[xkh__huaar]
            vect_same_key.append(veqhi__mvnj == satv__rodz)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(xpxp__bhttq) + suffix_x if xpxp__bhttq in
            qpnj__jdnq else xpxp__bhttq): ('left', xpxp__bhttq) for
            xpxp__bhttq in left_vars.keys()}
        self.column_origins.update({(str(xpxp__bhttq) + suffix_y if 
            xpxp__bhttq in qpnj__jdnq else xpxp__bhttq): ('right',
            xpxp__bhttq) for xpxp__bhttq in right_vars.keys()})
        if '$_bodo_index_' in qpnj__jdnq:
            qpnj__jdnq.remove('$_bodo_index_')
        self.add_suffix = qpnj__jdnq

    def __repr__(self):
        xxsz__kxov = ''
        for xpxp__bhttq, nonp__rpyim in self.out_data_vars.items():
            xxsz__kxov += "'{}':{}, ".format(xpxp__bhttq, nonp__rpyim.name)
        urrmm__hgnw = '{}{{{}}}'.format(self.df_out, xxsz__kxov)
        efivk__pfbu = ''
        for xpxp__bhttq, nonp__rpyim in self.left_vars.items():
            efivk__pfbu += "'{}':{}, ".format(xpxp__bhttq, nonp__rpyim.name)
        ouhsq__zwtp = '{}{{{}}}'.format(self.left_df, efivk__pfbu)
        efivk__pfbu = ''
        for xpxp__bhttq, nonp__rpyim in self.right_vars.items():
            efivk__pfbu += "'{}':{}, ".format(xpxp__bhttq, nonp__rpyim.name)
        wfern__ajf = '{}{{{}}}'.format(self.right_df, efivk__pfbu)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, urrmm__hgnw, ouhsq__zwtp, wfern__ajf)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    nedj__zps = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    kpu__qnj = []
    gndyq__bgfl = list(join_node.left_vars.values())
    for nwfkm__ysf in gndyq__bgfl:
        teo__ddwm = typemap[nwfkm__ysf.name]
        wxvu__bnwd = equiv_set.get_shape(nwfkm__ysf)
        if wxvu__bnwd:
            kpu__qnj.append(wxvu__bnwd[0])
    if len(kpu__qnj) > 1:
        equiv_set.insert_equiv(*kpu__qnj)
    kpu__qnj = []
    gndyq__bgfl = list(join_node.right_vars.values())
    for nwfkm__ysf in gndyq__bgfl:
        teo__ddwm = typemap[nwfkm__ysf.name]
        wxvu__bnwd = equiv_set.get_shape(nwfkm__ysf)
        if wxvu__bnwd:
            kpu__qnj.append(wxvu__bnwd[0])
    if len(kpu__qnj) > 1:
        equiv_set.insert_equiv(*kpu__qnj)
    kpu__qnj = []
    for nwfkm__ysf in join_node.out_data_vars.values():
        teo__ddwm = typemap[nwfkm__ysf.name]
        cddov__hprz = array_analysis._gen_shape_call(equiv_set, nwfkm__ysf,
            teo__ddwm.ndim, None, nedj__zps)
        equiv_set.insert_equiv(nwfkm__ysf, cddov__hprz)
        kpu__qnj.append(cddov__hprz[0])
        equiv_set.define(nwfkm__ysf, set())
    if len(kpu__qnj) > 1:
        equiv_set.insert_equiv(*kpu__qnj)
    return [], nedj__zps


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    cusxj__iypom = Distribution.OneD
    qnoiw__sesj = Distribution.OneD
    for nwfkm__ysf in join_node.left_vars.values():
        cusxj__iypom = Distribution(min(cusxj__iypom.value, array_dists[
            nwfkm__ysf.name].value))
    for nwfkm__ysf in join_node.right_vars.values():
        qnoiw__sesj = Distribution(min(qnoiw__sesj.value, array_dists[
            nwfkm__ysf.name].value))
    ekx__tpoq = Distribution.OneD_Var
    for nwfkm__ysf in join_node.out_data_vars.values():
        if nwfkm__ysf.name in array_dists:
            ekx__tpoq = Distribution(min(ekx__tpoq.value, array_dists[
                nwfkm__ysf.name].value))
    hgz__ijfuf = Distribution(min(ekx__tpoq.value, cusxj__iypom.value))
    sfasj__xwayn = Distribution(min(ekx__tpoq.value, qnoiw__sesj.value))
    ekx__tpoq = Distribution(max(hgz__ijfuf.value, sfasj__xwayn.value))
    for nwfkm__ysf in join_node.out_data_vars.values():
        array_dists[nwfkm__ysf.name] = ekx__tpoq
    if ekx__tpoq != Distribution.OneD_Var:
        cusxj__iypom = ekx__tpoq
        qnoiw__sesj = ekx__tpoq
    for nwfkm__ysf in join_node.left_vars.values():
        array_dists[nwfkm__ysf.name] = cusxj__iypom
    for nwfkm__ysf in join_node.right_vars.values():
        array_dists[nwfkm__ysf.name] = qnoiw__sesj
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    aivyi__rwtog = set(join_node.left_keys) & set(join_node.right_keys)
    lsjyu__mkjvn = set(join_node.left_vars.keys()) & set(join_node.
        right_vars.keys())
    qpnj__jdnq = lsjyu__mkjvn - aivyi__rwtog
    for djwlk__ayas, swm__itr in join_node.out_data_vars.items():
        if join_node.indicator and djwlk__ayas == '_merge':
            continue
        if not djwlk__ayas in join_node.column_origins:
            raise BodoError('join(): The variable ' + djwlk__ayas +
                ' is absent from the output')
        uqvs__fvpui = join_node.column_origins[djwlk__ayas]
        if uqvs__fvpui[0] == 'left':
            nwfkm__ysf = join_node.left_vars[uqvs__fvpui[1]]
        else:
            nwfkm__ysf = join_node.right_vars[uqvs__fvpui[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=swm__itr.
            name, src=nwfkm__ysf.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for rhu__vtvf in list(join_node.left_vars.keys()):
        join_node.left_vars[rhu__vtvf] = visit_vars_inner(join_node.
            left_vars[rhu__vtvf], callback, cbdata)
    for rhu__vtvf in list(join_node.right_vars.keys()):
        join_node.right_vars[rhu__vtvf] = visit_vars_inner(join_node.
            right_vars[rhu__vtvf], callback, cbdata)
    for rhu__vtvf in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[rhu__vtvf] = visit_vars_inner(join_node.
            out_data_vars[rhu__vtvf], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    vivg__knz = []
    cbvkj__eemn = True
    for rhu__vtvf, nwfkm__ysf in join_node.out_data_vars.items():
        if nwfkm__ysf.name in lives:
            cbvkj__eemn = False
            continue
        if rhu__vtvf == '$_bodo_index_':
            continue
        if join_node.indicator and rhu__vtvf == '_merge':
            vivg__knz.append('_merge')
            join_node.indicator = False
            continue
        xmd__auhhd, jes__lcggj = join_node.column_origins[rhu__vtvf]
        if (xmd__auhhd == 'left' and jes__lcggj not in join_node.left_keys and
            jes__lcggj not in join_node.left_cond_cols):
            join_node.left_vars.pop(jes__lcggj)
            vivg__knz.append(rhu__vtvf)
        if (xmd__auhhd == 'right' and jes__lcggj not in join_node.
            right_keys and jes__lcggj not in join_node.right_cond_cols):
            join_node.right_vars.pop(jes__lcggj)
            vivg__knz.append(rhu__vtvf)
    for cname in vivg__knz:
        join_node.out_data_vars.pop(cname)
    if cbvkj__eemn:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({nonp__rpyim.name for nonp__rpyim in join_node.left_vars
        .values()})
    use_set.update({nonp__rpyim.name for nonp__rpyim in join_node.
        right_vars.values()})
    def_set.update({nonp__rpyim.name for nonp__rpyim in join_node.
        out_data_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    ulhak__hjl = set(nonp__rpyim.name for nonp__rpyim in join_node.
        out_data_vars.values())
    return set(), ulhak__hjl


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for rhu__vtvf in list(join_node.left_vars.keys()):
        join_node.left_vars[rhu__vtvf] = replace_vars_inner(join_node.
            left_vars[rhu__vtvf], var_dict)
    for rhu__vtvf in list(join_node.right_vars.keys()):
        join_node.right_vars[rhu__vtvf] = replace_vars_inner(join_node.
            right_vars[rhu__vtvf], var_dict)
    for rhu__vtvf in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[rhu__vtvf] = replace_vars_inner(join_node.
            out_data_vars[rhu__vtvf], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for nwfkm__ysf in join_node.out_data_vars.values():
        definitions[nwfkm__ysf.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    icgxm__eiv = tuple(join_node.left_vars[xpxp__bhttq] for xpxp__bhttq in
        join_node.left_keys)
    aksen__pwo = tuple(join_node.right_vars[xpxp__bhttq] for xpxp__bhttq in
        join_node.right_keys)
    tkuu__ujd = tuple(join_node.left_vars.keys())
    xinmo__ptgnr = tuple(join_node.right_vars.keys())
    hkp__awnz = ()
    ovlpc__qtp = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        fuak__aupbm = join_node.right_keys[0]
        if fuak__aupbm in tkuu__ujd:
            ovlpc__qtp = fuak__aupbm,
            hkp__awnz = join_node.right_vars[fuak__aupbm],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        fuak__aupbm = join_node.left_keys[0]
        if fuak__aupbm in xinmo__ptgnr:
            ovlpc__qtp = fuak__aupbm,
            hkp__awnz = join_node.left_vars[fuak__aupbm],
            optional_column = True
    nklg__itlr = tuple(join_node.out_data_vars[cname] for cname in ovlpc__qtp)
    gpy__xzsqw = tuple(nonp__rpyim for yhj__czyh, nonp__rpyim in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if yhj__czyh
         not in join_node.left_keys)
    jxyls__zuvar = tuple(nonp__rpyim for yhj__czyh, nonp__rpyim in sorted(
        join_node.right_vars.items(), key=lambda a: str(a[0])) if yhj__czyh
         not in join_node.right_keys)
    autn__usvcj = (hkp__awnz + icgxm__eiv + aksen__pwo + gpy__xzsqw +
        jxyls__zuvar)
    ogvgb__zuof = tuple(typemap[nonp__rpyim.name] for nonp__rpyim in
        autn__usvcj)
    ilvg__mtgm = tuple('opti_c' + str(vkrpx__sji) for vkrpx__sji in range(
        len(hkp__awnz)))
    left_other_names = tuple('t1_c' + str(vkrpx__sji) for vkrpx__sji in
        range(len(gpy__xzsqw)))
    right_other_names = tuple('t2_c' + str(vkrpx__sji) for vkrpx__sji in
        range(len(jxyls__zuvar)))
    left_other_types = tuple([typemap[xpxp__bhttq.name] for xpxp__bhttq in
        gpy__xzsqw])
    right_other_types = tuple([typemap[xpxp__bhttq.name] for xpxp__bhttq in
        jxyls__zuvar])
    left_key_names = tuple('t1_key' + str(vkrpx__sji) for vkrpx__sji in
        range(n_keys))
    right_key_names = tuple('t2_key' + str(vkrpx__sji) for vkrpx__sji in
        range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(ilvg__mtgm[
        0]) if len(ilvg__mtgm) == 1 else '', ','.join(left_key_names), ','.
        join(right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[nonp__rpyim.name] for nonp__rpyim in
        icgxm__eiv)
    right_key_types = tuple(typemap[nonp__rpyim.name] for nonp__rpyim in
        aksen__pwo)
    for vkrpx__sji in range(n_keys):
        glbs[f'key_type_{vkrpx__sji}'] = _match_join_key_types(left_key_types
            [vkrpx__sji], right_key_types[vkrpx__sji], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[vkrpx__sji]}, key_type_{vkrpx__sji})'
         for vkrpx__sji in range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[vkrpx__sji]}, key_type_{vkrpx__sji})'
         for vkrpx__sji in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    olx__hjmk = []
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            mql__zmsyh = str(cname) + join_node.suffix_x
        else:
            mql__zmsyh = cname
        assert mql__zmsyh in join_node.out_data_vars
        olx__hjmk.append(join_node.out_data_vars[mql__zmsyh])
    for vkrpx__sji, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[vkrpx__sji] and not join_node.is_join:
            if cname in join_node.add_suffix:
                mql__zmsyh = str(cname) + join_node.suffix_y
            else:
                mql__zmsyh = cname
            assert mql__zmsyh in join_node.out_data_vars
            olx__hjmk.append(join_node.out_data_vars[mql__zmsyh])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                mql__zmsyh = str(cname) + join_node.suffix_x
            else:
                mql__zmsyh = str(cname) + join_node.suffix_y
        else:
            mql__zmsyh = cname
        return join_node.out_data_vars[mql__zmsyh]
    fyhzk__wvecs = nklg__itlr + tuple(olx__hjmk)
    fyhzk__wvecs += tuple(_get_out_col_var(yhj__czyh, True) for yhj__czyh,
        nonp__rpyim in sorted(join_node.left_vars.items(), key=lambda a:
        str(a[0])) if yhj__czyh not in join_node.left_keys)
    fyhzk__wvecs += tuple(_get_out_col_var(yhj__czyh, False) for yhj__czyh,
        nonp__rpyim in sorted(join_node.right_vars.items(), key=lambda a:
        str(a[0])) if yhj__czyh not in join_node.right_keys)
    if join_node.indicator:
        fyhzk__wvecs += _get_out_col_var('_merge', False),
    idtx__nwzsw = [('t3_c' + str(vkrpx__sji)) for vkrpx__sji in range(len(
        fyhzk__wvecs))]
    general_cond_cfunc, left_col_nums, right_col_nums = (
        _gen_general_cond_cfunc(join_node, typemap))
    if join_node.how == 'asof':
        if left_parallel or right_parallel:
            assert left_parallel and right_parallel
            func_text += """    t2_keys, data_right = parallel_asof_comm(t1_keys, t2_keys, data_right)
"""
        func_text += """    out_t1_keys, out_t2_keys, out_data_left, out_data_right = bodo.ir.join.local_merge_asof(t1_keys, t2_keys, data_left, data_right)
"""
    else:
        func_text += _gen_local_hash_join(optional_column, left_key_names,
            right_key_names, left_key_types, right_key_types,
            left_other_names, right_other_names, left_other_types,
            right_other_types, join_node.vect_same_key, join_node.is_left,
            join_node.is_right, join_node.is_join, left_parallel,
            right_parallel, glbs, [typemap[nonp__rpyim.name] for
            nonp__rpyim in fyhzk__wvecs], join_node.loc, join_node.
            indicator, join_node.is_na_equal, general_cond_cfunc,
            left_col_nums, right_col_nums)
    if join_node.how == 'asof':
        for vkrpx__sji in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(vkrpx__sji,
                vkrpx__sji)
        for vkrpx__sji in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                vkrpx__sji, vkrpx__sji)
        for vkrpx__sji in range(n_keys):
            func_text += (
                f'    t1_keys_{vkrpx__sji} = out_t1_keys[{vkrpx__sji}]\n')
        for vkrpx__sji in range(n_keys):
            func_text += (
                f'    t2_keys_{vkrpx__sji} = out_t2_keys[{vkrpx__sji}]\n')
    idx = 0
    if optional_column:
        func_text += f'    {idtx__nwzsw[idx]} = opti_0\n'
        idx += 1
    for vkrpx__sji in range(n_keys):
        func_text += f'    {idtx__nwzsw[idx]} = t1_keys_{vkrpx__sji}\n'
        idx += 1
    for vkrpx__sji in range(n_keys):
        if not join_node.vect_same_key[vkrpx__sji] and not join_node.is_join:
            func_text += f'    {idtx__nwzsw[idx]} = t2_keys_{vkrpx__sji}\n'
            idx += 1
    for vkrpx__sji in range(len(left_other_names)):
        func_text += f'    {idtx__nwzsw[idx]} = left_{vkrpx__sji}\n'
        idx += 1
    for vkrpx__sji in range(len(right_other_names)):
        func_text += f'    {idtx__nwzsw[idx]} = right_{vkrpx__sji}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {idtx__nwzsw[idx]} = indicator_col\n'
        idx += 1
    ncj__ssp = {}
    exec(func_text, {}, ncj__ssp)
    ysnwh__jfpp = ncj__ssp['f']
    glbs.update({'bodo': bodo, 'np': np, 'pd': pd,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'parallel_asof_comm':
        parallel_asof_comm, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'hash_join_table':
        hash_join_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'add_join_gen_cond_cfunc_sym': add_join_gen_cond_cfunc_sym,
        'get_join_cond_addr': get_join_cond_addr})
    if general_cond_cfunc:
        glbs.update({'general_cond_cfunc': general_cond_cfunc})
    dbhq__dto = compile_to_numba_ir(ysnwh__jfpp, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=ogvgb__zuof, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(dbhq__dto, autn__usvcj)
    dha__ojlnb = dbhq__dto.body[:-3]
    for vkrpx__sji in range(len(fyhzk__wvecs)):
        dha__ojlnb[-len(fyhzk__wvecs) + vkrpx__sji].target = fyhzk__wvecs[
            vkrpx__sji]
    return dha__ojlnb


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    vpbca__rlxni = next_label()
    bwsu__nimm = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    akclg__szlqf = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{vpbca__rlxni}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        bwsu__nimm, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        akclg__szlqf, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    ncj__ssp = {}
    exec(func_text, table_getitem_funcs, ncj__ssp)
    stpcj__bzv = ncj__ssp[f'bodo_join_gen_cond{vpbca__rlxni}']
    tvxw__dqmn = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    uzar__jir = numba.cfunc(tvxw__dqmn, nopython=True)(stpcj__bzv)
    join_gen_cond_cfunc[uzar__jir.native_name] = uzar__jir
    join_gen_cond_cfunc_addr[uzar__jir.native_name] = uzar__jir.address
    return uzar__jir, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    lhqcg__xqwo = []
    for xpxp__bhttq, nlr__huly in col_to_ind.items():
        cname = f'({table_name}.{xpxp__bhttq})'
        if cname not in expr:
            continue
        aorw__kzhws = f'getitem_{table_name}_val_{nlr__huly}'
        aoei__pmbh = f'_bodo_{table_name}_val_{nlr__huly}'
        waljm__rnmul = typemap[col_vars[xpxp__bhttq].name]
        if is_str_arr_type(waljm__rnmul):
            func_text += f"""  {aoei__pmbh}, {aoei__pmbh}_size = {aorw__kzhws}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {aoei__pmbh} = bodo.libs.str_arr_ext.decode_utf8({aoei__pmbh}, {aoei__pmbh}_size)
"""
        else:
            func_text += (
                f'  {aoei__pmbh} = {aorw__kzhws}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[aorw__kzhws
            ] = bodo.libs.array._gen_row_access_intrinsic(waljm__rnmul,
            nlr__huly)
        expr = expr.replace(cname, aoei__pmbh)
        rcbo__raqo = f'({na_check_name}.{table_name}.{xpxp__bhttq})'
        if rcbo__raqo in expr:
            imn__myge = f'nacheck_{table_name}_val_{nlr__huly}'
            ejdb__rbmd = f'_bodo_isna_{table_name}_val_{nlr__huly}'
            if (isinstance(waljm__rnmul, bodo.libs.int_arr_ext.
                IntegerArrayType) or waljm__rnmul == bodo.libs.bool_arr_ext
                .boolean_array or is_str_arr_type(waljm__rnmul)):
                func_text += f"""  {ejdb__rbmd} = {imn__myge}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += (
                    f'  {ejdb__rbmd} = {imn__myge}({table_name}_data1, {table_name}_ind)\n'
                    )
            table_getitem_funcs[imn__myge
                ] = bodo.libs.array._gen_row_na_check_intrinsic(waljm__rnmul,
                nlr__huly)
            expr = expr.replace(rcbo__raqo, ejdb__rbmd)
        if nlr__huly >= n_keys:
            lhqcg__xqwo.append(nlr__huly)
    return expr, func_text, lhqcg__xqwo


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {xpxp__bhttq: vkrpx__sji for vkrpx__sji, xpxp__bhttq in
        enumerate(key_names)}
    vkrpx__sji = n_keys
    for xpxp__bhttq in sorted(col_vars, key=lambda a: str(a)):
        if xpxp__bhttq in key_names:
            continue
        col_to_ind[xpxp__bhttq] = vkrpx__sji
        vkrpx__sji += 1
    return col_to_ind


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as vwz__bgoh:
        if is_str_arr_type(t1) and is_str_arr_type(t2):
            return bodo.string_array_type
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    tgic__ayr = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[nonp__rpyim.name] in tgic__ayr for
        nonp__rpyim in join_node.left_vars.values())
    right_parallel = all(array_dists[nonp__rpyim.name] in tgic__ayr for
        nonp__rpyim in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[nonp__rpyim.name] in tgic__ayr for
            nonp__rpyim in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[nonp__rpyim.name] in tgic__ayr for
            nonp__rpyim in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[nonp__rpyim.name] in tgic__ayr for
            nonp__rpyim in join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    uefyt__jdu = []
    for vkrpx__sji in range(len(left_key_names)):
        oit__kuefz = _match_join_key_types(left_key_types[vkrpx__sji],
            right_key_types[vkrpx__sji], loc)
        uefyt__jdu.append(needs_typechange(oit__kuefz, is_right,
            vect_same_key[vkrpx__sji]))
    for vkrpx__sji in range(len(left_other_names)):
        uefyt__jdu.append(needs_typechange(left_other_types[vkrpx__sji],
            is_right, False))
    for vkrpx__sji in range(len(right_key_names)):
        if not vect_same_key[vkrpx__sji] and not is_join:
            oit__kuefz = _match_join_key_types(left_key_types[vkrpx__sji],
                right_key_types[vkrpx__sji], loc)
            uefyt__jdu.append(needs_typechange(oit__kuefz, is_left, False))
    for vkrpx__sji in range(len(right_other_names)):
        uefyt__jdu.append(needs_typechange(right_other_types[vkrpx__sji],
            is_left, False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                cfk__yjt = IntDtype(in_type.dtype).name
                assert cfk__yjt.endswith('Dtype()')
                cfk__yjt = cfk__yjt[:-7]
                cofpz__isxg = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{cfk__yjt}"))
"""
                jprlg__cis = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                cofpz__isxg = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                jprlg__cis = f'typ_{idx}'
        elif in_type == bodo.string_array_type:
            cofpz__isxg = (
                f'    typ_{idx} = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)\n'
                )
            jprlg__cis = f'typ_{idx}'
        else:
            cofpz__isxg = ''
            jprlg__cis = in_name
        return cofpz__isxg, jprlg__cis
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    pif__mop = []
    for vkrpx__sji in range(n_keys):
        pif__mop.append('t1_keys[{}]'.format(vkrpx__sji))
    for vkrpx__sji in range(len(left_other_names)):
        pif__mop.append('data_left[{}]'.format(vkrpx__sji))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in pif__mop))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    sjk__gea = []
    for vkrpx__sji in range(n_keys):
        sjk__gea.append('t2_keys[{}]'.format(vkrpx__sji))
    for vkrpx__sji in range(len(right_other_names)):
        sjk__gea.append('data_right[{}]'.format(vkrpx__sji))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in sjk__gea))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        tieke__fei else '0' for tieke__fei in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if tieke__fei else '0' for tieke__fei in uefyt__jdu))
    func_text += f"""    left_table_cond_columns = np.array({left_col_nums if len(left_col_nums) > 0 else [-1]}, dtype=np.int64)
"""
    func_text += f"""    right_table_cond_columns = np.array({right_col_nums if len(right_col_nums) > 0 else [-1]}, dtype=np.int64)
"""
    if general_cond_cfunc:
        func_text += f"""    cfunc_cond = add_join_gen_cond_cfunc_sym(general_cond_cfunc, '{general_cond_cfunc.native_name}')
"""
        func_text += (
            f"    cfunc_cond = get_join_cond_addr('{general_cond_cfunc.native_name}')\n"
            )
    else:
        func_text += '    cfunc_cond = 0\n'
    func_text += (
        """    out_table = hash_join_table(table_left, table_right, {}, {}, {}, {}, {}, vect_same_key.ctypes, vect_need_typechange.ctypes, {}, {}, {}, {}, {}, {}, cfunc_cond, left_table_cond_columns.ctypes, {}, right_table_cond_columns.ctypes, {})
"""
        .format(left_parallel, right_parallel, n_keys, len(left_other_names
        ), len(right_other_names), is_left, is_right, is_join,
        optional_column, indicator, is_na_equal, len(left_col_nums), len(
        right_col_nums)))
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    idx = 0
    if optional_column:
        wol__pekh = get_out_type(idx, out_types[idx], 'opti_c0', False, False)
        func_text += wol__pekh[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        func_text += f"""    opti_0 = info_to_array(info_from_table(out_table, {idx}), {wol__pekh[1]})
"""
        idx += 1
    for vkrpx__sji, xeu__zhkt in enumerate(left_key_names):
        oit__kuefz = _match_join_key_types(left_key_types[vkrpx__sji],
            right_key_types[vkrpx__sji], loc)
        wol__pekh = get_out_type(idx, oit__kuefz, f't1_keys[{vkrpx__sji}]',
            is_right, vect_same_key[vkrpx__sji])
        func_text += wol__pekh[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        if oit__kuefz != left_key_types[vkrpx__sji] and left_key_types[
            vkrpx__sji] != bodo.dict_str_arr_type:
            func_text += f"""    t1_keys_{vkrpx__sji} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {wol__pekh[1]}), out_type_{idx})
"""
        else:
            func_text += f"""    t1_keys_{vkrpx__sji} = info_to_array(info_from_table(out_table, {idx}), {wol__pekh[1]})
"""
        idx += 1
    for vkrpx__sji, xeu__zhkt in enumerate(left_other_names):
        wol__pekh = get_out_type(idx, left_other_types[vkrpx__sji],
            xeu__zhkt, is_right, False)
        func_text += wol__pekh[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(vkrpx__sji, idx, wol__pekh[1]))
        idx += 1
    for vkrpx__sji, xeu__zhkt in enumerate(right_key_names):
        if not vect_same_key[vkrpx__sji] and not is_join:
            oit__kuefz = _match_join_key_types(left_key_types[vkrpx__sji],
                right_key_types[vkrpx__sji], loc)
            wol__pekh = get_out_type(idx, oit__kuefz,
                f't2_keys[{vkrpx__sji}]', is_left, False)
            func_text += wol__pekh[0]
            glbs[f'out_type_{idx}'] = out_types[idx - len(left_other_names)]
            if oit__kuefz != right_key_types[vkrpx__sji] and right_key_types[
                vkrpx__sji] != bodo.dict_str_arr_type:
                func_text += f"""    t2_keys_{vkrpx__sji} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {wol__pekh[1]}), out_type_{idx})
"""
            else:
                func_text += f"""    t2_keys_{vkrpx__sji} = info_to_array(info_from_table(out_table, {idx}), {wol__pekh[1]})
"""
            idx += 1
    for vkrpx__sji, xeu__zhkt in enumerate(right_other_names):
        wol__pekh = get_out_type(idx, right_other_types[vkrpx__sji],
            xeu__zhkt, is_left, False)
        func_text += wol__pekh[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(vkrpx__sji, idx, wol__pekh[1]))
        idx += 1
    if indicator:
        func_text += f"""    typ_{idx} = pd.Categorical(values=['both'], categories=('left_only', 'right_only', 'both'))
"""
        func_text += f"""    indicator_col = info_to_array(info_from_table(out_table, {idx}), typ_{idx})
"""
        idx += 1
    func_text += '    delete_table(out_table)\n'
    return func_text


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    mpgj__pjd = bodo.libs.distributed_api.get_size()
    qeub__jmf = np.empty(mpgj__pjd, left_key_arrs[0].dtype)
    fbyf__zfhzh = np.empty(mpgj__pjd, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(qeub__jmf, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(fbyf__zfhzh, left_key_arrs[0][-1])
    ced__wutxy = np.zeros(mpgj__pjd, np.int32)
    hyg__wno = np.zeros(mpgj__pjd, np.int32)
    ahne__pntwz = np.zeros(mpgj__pjd, np.int32)
    jfcdd__gdf = right_key_arrs[0][0]
    oxuy__ktm = right_key_arrs[0][-1]
    avri__cfoz = -1
    vkrpx__sji = 0
    while vkrpx__sji < mpgj__pjd - 1 and fbyf__zfhzh[vkrpx__sji] < jfcdd__gdf:
        vkrpx__sji += 1
    while vkrpx__sji < mpgj__pjd and qeub__jmf[vkrpx__sji] <= oxuy__ktm:
        avri__cfoz, snwo__wqkf = _count_overlap(right_key_arrs[0],
            qeub__jmf[vkrpx__sji], fbyf__zfhzh[vkrpx__sji])
        if avri__cfoz != 0:
            avri__cfoz -= 1
            snwo__wqkf += 1
        ced__wutxy[vkrpx__sji] = snwo__wqkf
        hyg__wno[vkrpx__sji] = avri__cfoz
        vkrpx__sji += 1
    while vkrpx__sji < mpgj__pjd:
        ced__wutxy[vkrpx__sji] = 1
        hyg__wno[vkrpx__sji] = len(right_key_arrs[0]) - 1
        vkrpx__sji += 1
    bodo.libs.distributed_api.alltoall(ced__wutxy, ahne__pntwz, 1)
    mzdfy__ymdvo = ahne__pntwz.sum()
    wunu__kxle = np.empty(mzdfy__ymdvo, right_key_arrs[0].dtype)
    jhohw__zysc = alloc_arr_tup(mzdfy__ymdvo, right_data)
    raesa__ckyj = bodo.ir.join.calc_disp(ahne__pntwz)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], wunu__kxle,
        ced__wutxy, ahne__pntwz, hyg__wno, raesa__ckyj)
    bodo.libs.distributed_api.alltoallv_tup(right_data, jhohw__zysc,
        ced__wutxy, ahne__pntwz, hyg__wno, raesa__ckyj)
    return (wunu__kxle,), jhohw__zysc


@numba.njit
def _count_overlap(r_key_arr, start, end):
    snwo__wqkf = 0
    avri__cfoz = 0
    xsl__thw = 0
    while xsl__thw < len(r_key_arr) and r_key_arr[xsl__thw] < start:
        avri__cfoz += 1
        xsl__thw += 1
    while xsl__thw < len(r_key_arr) and start <= r_key_arr[xsl__thw] <= end:
        xsl__thw += 1
        snwo__wqkf += 1
    return avri__cfoz, snwo__wqkf


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    rcw__yvw = np.empty_like(arr)
    rcw__yvw[0] = 0
    for vkrpx__sji in range(1, len(arr)):
        rcw__yvw[vkrpx__sji] = rcw__yvw[vkrpx__sji - 1] + arr[vkrpx__sji - 1]
    return rcw__yvw


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    gagn__ajfkm = len(left_keys[0])
    goic__tkr = len(right_keys[0])
    akw__ixw = alloc_arr_tup(gagn__ajfkm, left_keys)
    hqka__atwov = alloc_arr_tup(gagn__ajfkm, right_keys)
    pun__tay = alloc_arr_tup(gagn__ajfkm, data_left)
    yfrc__mbly = alloc_arr_tup(gagn__ajfkm, data_right)
    tfwl__wfr = 0
    aram__bxq = 0
    for tfwl__wfr in range(gagn__ajfkm):
        if aram__bxq < 0:
            aram__bxq = 0
        while aram__bxq < goic__tkr and getitem_arr_tup(right_keys, aram__bxq
            ) <= getitem_arr_tup(left_keys, tfwl__wfr):
            aram__bxq += 1
        aram__bxq -= 1
        setitem_arr_tup(akw__ixw, tfwl__wfr, getitem_arr_tup(left_keys,
            tfwl__wfr))
        setitem_arr_tup(pun__tay, tfwl__wfr, getitem_arr_tup(data_left,
            tfwl__wfr))
        if aram__bxq >= 0:
            setitem_arr_tup(hqka__atwov, tfwl__wfr, getitem_arr_tup(
                right_keys, aram__bxq))
            setitem_arr_tup(yfrc__mbly, tfwl__wfr, getitem_arr_tup(
                data_right, aram__bxq))
        else:
            bodo.libs.array_kernels.setna_tup(hqka__atwov, tfwl__wfr)
            bodo.libs.array_kernels.setna_tup(yfrc__mbly, tfwl__wfr)
    return akw__ixw, hqka__atwov, pun__tay, yfrc__mbly


def copy_arr_tup(arrs):
    return tuple(a.copy() for a in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    snwo__wqkf = arrs.count
    func_text = 'def f(arrs):\n'
    func_text += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(vkrpx__sji) for vkrpx__sji in range(snwo__wqkf)))
    ncj__ssp = {}
    exec(func_text, {}, ncj__ssp)
    utu__fqew = ncj__ssp['f']
    return utu__fqew
