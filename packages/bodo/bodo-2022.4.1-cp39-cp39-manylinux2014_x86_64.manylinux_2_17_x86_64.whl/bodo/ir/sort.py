"""IR node for the data sorting"""
from collections import defaultdict
import numba
import numpy as np
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, mk_unique_var, replace_arg_nodes, replace_vars_inner, visit_vars_inner
import bodo
import bodo.libs.timsort
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, sort_values_table
from bodo.libs.str_arr_ext import cp_str_list_to_array, to_list_if_immutable_arr
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.utils.utils import debug_prints, gen_getitem
MIN_SAMPLES = 1000000
samplePointsPerPartitionHint = 20
MPI_ROOT = 0


class Sort(ir.Stmt):

    def __init__(self, df_in, df_out, key_arrs, out_key_arrs, df_in_vars,
        df_out_vars, inplace, loc, ascending_list=True, na_position='last'):
        self.df_in = df_in
        self.df_out = df_out
        self.key_arrs = key_arrs
        self.out_key_arrs = out_key_arrs
        self.df_in_vars = df_in_vars
        self.df_out_vars = df_out_vars
        self.inplace = inplace
        if isinstance(na_position, str):
            if na_position == 'last':
                self.na_position_b = (True,) * len(key_arrs)
            else:
                self.na_position_b = (False,) * len(key_arrs)
        else:
            self.na_position_b = tuple([(True if qib__kli == 'last' else 
                False) for qib__kli in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        dgk__wdzxa = ''
        for eezbr__vftvi, nutkq__eno in self.df_in_vars.items():
            dgk__wdzxa += "'{}':{}, ".format(eezbr__vftvi, nutkq__eno.name)
        vmkbu__giov = '{}{{{}}}'.format(self.df_in, dgk__wdzxa)
        hxl__bht = ''
        for eezbr__vftvi, nutkq__eno in self.df_out_vars.items():
            hxl__bht += "'{}':{}, ".format(eezbr__vftvi, nutkq__eno.name)
        xzf__fgnwr = '{}{{{}}}'.format(self.df_out, hxl__bht)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(
            nutkq__eno.name for nutkq__eno in self.key_arrs), vmkbu__giov,
            ', '.join(nutkq__eno.name for nutkq__eno in self.out_key_arrs),
            xzf__fgnwr)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    zzec__rnfo = []
    vni__ympyd = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for kbpq__guub in vni__ympyd:
        ctkty__uuuj = equiv_set.get_shape(kbpq__guub)
        if ctkty__uuuj is not None:
            zzec__rnfo.append(ctkty__uuuj[0])
    if len(zzec__rnfo) > 1:
        equiv_set.insert_equiv(*zzec__rnfo)
    bdm__asyb = []
    zzec__rnfo = []
    wzx__awpl = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for kbpq__guub in wzx__awpl:
        ptigh__out = typemap[kbpq__guub.name]
        jhckx__pegxb = array_analysis._gen_shape_call(equiv_set, kbpq__guub,
            ptigh__out.ndim, None, bdm__asyb)
        equiv_set.insert_equiv(kbpq__guub, jhckx__pegxb)
        zzec__rnfo.append(jhckx__pegxb[0])
        equiv_set.define(kbpq__guub, set())
    if len(zzec__rnfo) > 1:
        equiv_set.insert_equiv(*zzec__rnfo)
    return [], bdm__asyb


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    vni__ympyd = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    ljj__wpg = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    izv__hpi = Distribution.OneD
    for kbpq__guub in vni__ympyd:
        izv__hpi = Distribution(min(izv__hpi.value, array_dists[kbpq__guub.
            name].value))
    ahyd__ggz = Distribution(min(izv__hpi.value, Distribution.OneD_Var.value))
    for kbpq__guub in ljj__wpg:
        if kbpq__guub.name in array_dists:
            ahyd__ggz = Distribution(min(ahyd__ggz.value, array_dists[
                kbpq__guub.name].value))
    if ahyd__ggz != Distribution.OneD_Var:
        izv__hpi = ahyd__ggz
    for kbpq__guub in vni__ympyd:
        array_dists[kbpq__guub.name] = izv__hpi
    for kbpq__guub in ljj__wpg:
        array_dists[kbpq__guub.name] = ahyd__ggz
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for jgu__qddhk, dwqx__omqj in zip(sort_node.key_arrs, sort_node.
        out_key_arrs):
        typeinferer.constraints.append(typeinfer.Propagate(dst=dwqx__omqj.
            name, src=jgu__qddhk.name, loc=sort_node.loc))
    for szza__ngl, kbpq__guub in sort_node.df_in_vars.items():
        jbh__fskv = sort_node.df_out_vars[szza__ngl]
        typeinferer.constraints.append(typeinfer.Propagate(dst=jbh__fskv.
            name, src=kbpq__guub.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for kbpq__guub in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[kbpq__guub.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for cthy__mwko in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[cthy__mwko] = visit_vars_inner(sort_node.
            key_arrs[cthy__mwko], callback, cbdata)
        sort_node.out_key_arrs[cthy__mwko] = visit_vars_inner(sort_node.
            out_key_arrs[cthy__mwko], callback, cbdata)
    for szza__ngl in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[szza__ngl] = visit_vars_inner(sort_node.
            df_in_vars[szza__ngl], callback, cbdata)
    for szza__ngl in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[szza__ngl] = visit_vars_inner(sort_node.
            df_out_vars[szza__ngl], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    kwor__mlpkw = []
    for szza__ngl, kbpq__guub in sort_node.df_out_vars.items():
        if kbpq__guub.name not in lives:
            kwor__mlpkw.append(szza__ngl)
    for vpw__nerzj in kwor__mlpkw:
        sort_node.df_in_vars.pop(vpw__nerzj)
        sort_node.df_out_vars.pop(vpw__nerzj)
    if len(sort_node.df_out_vars) == 0 and all(nutkq__eno.name not in lives for
        nutkq__eno in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({nutkq__eno.name for nutkq__eno in sort_node.key_arrs})
    use_set.update({nutkq__eno.name for nutkq__eno in sort_node.df_in_vars.
        values()})
    if not sort_node.inplace:
        def_set.update({nutkq__eno.name for nutkq__eno in sort_node.
            out_key_arrs})
        def_set.update({nutkq__eno.name for nutkq__eno in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    ilo__qzba = set()
    if not sort_node.inplace:
        ilo__qzba = set(nutkq__eno.name for nutkq__eno in sort_node.
            df_out_vars.values())
        ilo__qzba.update({nutkq__eno.name for nutkq__eno in sort_node.
            out_key_arrs})
    return set(), ilo__qzba


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for cthy__mwko in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[cthy__mwko] = replace_vars_inner(sort_node.
            key_arrs[cthy__mwko], var_dict)
        sort_node.out_key_arrs[cthy__mwko] = replace_vars_inner(sort_node.
            out_key_arrs[cthy__mwko], var_dict)
    for szza__ngl in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[szza__ngl] = replace_vars_inner(sort_node.
            df_in_vars[szza__ngl], var_dict)
    for szza__ngl in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[szza__ngl] = replace_vars_inner(sort_node.
            df_out_vars[szza__ngl], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    bfatk__mggl = False
    uzl__rma = list(sort_node.df_in_vars.values())
    wzx__awpl = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        bfatk__mggl = True
        for nutkq__eno in (sort_node.key_arrs + sort_node.out_key_arrs +
            uzl__rma + wzx__awpl):
            if array_dists[nutkq__eno.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                nutkq__eno.name] != distributed_pass.Distribution.OneD_Var:
                bfatk__mggl = False
    loc = sort_node.loc
    ovqon__hczr = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        ovekx__kwx = []
        for nutkq__eno in key_arrs:
            jriuj__iji = _copy_array_nodes(nutkq__eno, nodes, typingctx,
                targetctx, typemap, calltypes)
            ovekx__kwx.append(jriuj__iji)
        key_arrs = ovekx__kwx
        cewv__zjnj = []
        for nutkq__eno in uzl__rma:
            kop__dbbwm = _copy_array_nodes(nutkq__eno, nodes, typingctx,
                targetctx, typemap, calltypes)
            cewv__zjnj.append(kop__dbbwm)
        uzl__rma = cewv__zjnj
    key_name_args = [f'key{cthy__mwko}' for cthy__mwko in range(len(key_arrs))]
    stf__vbfm = ', '.join(key_name_args)
    col_name_args = [f'c{cthy__mwko}' for cthy__mwko in range(len(uzl__rma))]
    gin__hwz = ', '.join(col_name_args)
    jdrd__nsdl = 'def f({}, {}):\n'.format(stf__vbfm, gin__hwz)
    jdrd__nsdl += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, bfatk__mggl)
    jdrd__nsdl += '  return key_arrs, data\n'
    aguc__hah = {}
    exec(jdrd__nsdl, {}, aguc__hah)
    veuv__hex = aguc__hah['f']
    nljh__ohtsq = types.Tuple([typemap[nutkq__eno.name] for nutkq__eno in
        key_arrs])
    piagm__foqeq = types.Tuple([typemap[nutkq__eno.name] for nutkq__eno in
        uzl__rma])
    jku__xmtxl = compile_to_numba_ir(veuv__hex, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(nljh__ohtsq.types) + list(
        piagm__foqeq.types)), typemap=typemap, calltypes=calltypes
        ).blocks.popitem()[1]
    replace_arg_nodes(jku__xmtxl, key_arrs + uzl__rma)
    nodes += jku__xmtxl.body[:-2]
    yrjrt__ekahx = nodes[-1].target
    kjwr__lxfp = ir.Var(ovqon__hczr, mk_unique_var('key_data'), loc)
    typemap[kjwr__lxfp.name] = nljh__ohtsq
    gen_getitem(kjwr__lxfp, yrjrt__ekahx, 0, calltypes, nodes)
    ksn__wevsz = ir.Var(ovqon__hczr, mk_unique_var('sort_data'), loc)
    typemap[ksn__wevsz.name] = piagm__foqeq
    gen_getitem(ksn__wevsz, yrjrt__ekahx, 1, calltypes, nodes)
    for cthy__mwko, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, kjwr__lxfp, cthy__mwko, calltypes, nodes)
    for cthy__mwko, var in enumerate(wzx__awpl):
        gen_getitem(var, ksn__wevsz, cthy__mwko, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    jku__xmtxl = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(jku__xmtxl, [var])
    nodes += jku__xmtxl.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    jdrd__nsdl = ''
    godtt__qfa = len(key_name_args)
    dzsf__rkjei = ['array_to_info({})'.format(yjd__jap) for yjd__jap in
        key_name_args] + ['array_to_info({})'.format(yjd__jap) for yjd__jap in
        col_name_args]
    jdrd__nsdl += '  info_list_total = [{}]\n'.format(','.join(dzsf__rkjei))
    jdrd__nsdl += '  table_total = arr_info_list_to_table(info_list_total)\n'
    jdrd__nsdl += '  vect_ascending = np.array([{}])\n'.format(','.join('1' if
        eed__waium else '0' for eed__waium in ascending_list))
    jdrd__nsdl += '  na_position = np.array([{}])\n'.format(','.join('1' if
        eed__waium else '0' for eed__waium in na_position_b))
    jdrd__nsdl += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(godtt__qfa, parallel_b))
    krv__ksbp = 0
    qaf__eorn = []
    for yjd__jap in key_name_args:
        qaf__eorn.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(krv__ksbp, yjd__jap))
        krv__ksbp += 1
    jdrd__nsdl += '  key_arrs = ({},)\n'.format(','.join(qaf__eorn))
    lal__fji = []
    for yjd__jap in col_name_args:
        lal__fji.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(krv__ksbp, yjd__jap))
        krv__ksbp += 1
    if len(lal__fji) > 0:
        jdrd__nsdl += '  data = ({},)\n'.format(','.join(lal__fji))
    else:
        jdrd__nsdl += '  data = ()\n'
    jdrd__nsdl += '  delete_table(out_table)\n'
    jdrd__nsdl += '  delete_table(table_total)\n'
    return jdrd__nsdl
