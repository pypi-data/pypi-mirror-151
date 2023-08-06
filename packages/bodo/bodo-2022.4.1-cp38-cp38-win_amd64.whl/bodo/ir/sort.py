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
            self.na_position_b = tuple([(True if ijzac__kqqfh == 'last' else
                False) for ijzac__kqqfh in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_arrs)
        self.ascending_list = ascending_list
        self.loc = loc

    def __repr__(self):
        lmazp__xgtme = ''
        for wth__hyvq, eyudg__nmy in self.df_in_vars.items():
            lmazp__xgtme += "'{}':{}, ".format(wth__hyvq, eyudg__nmy.name)
        vlgii__ullxc = '{}{{{}}}'.format(self.df_in, lmazp__xgtme)
        jpwif__gxn = ''
        for wth__hyvq, eyudg__nmy in self.df_out_vars.items():
            jpwif__gxn += "'{}':{}, ".format(wth__hyvq, eyudg__nmy.name)
        yuobv__uvti = '{}{{{}}}'.format(self.df_out, jpwif__gxn)
        return 'sort: [key: {}] {} [key: {}] {}'.format(', '.join(
            eyudg__nmy.name for eyudg__nmy in self.key_arrs), vlgii__ullxc,
            ', '.join(eyudg__nmy.name for eyudg__nmy in self.out_key_arrs),
            yuobv__uvti)


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    vkze__tqv = []
    nfqt__svmqr = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    for kvvc__xhskd in nfqt__svmqr:
        sqwb__zevs = equiv_set.get_shape(kvvc__xhskd)
        if sqwb__zevs is not None:
            vkze__tqv.append(sqwb__zevs[0])
    if len(vkze__tqv) > 1:
        equiv_set.insert_equiv(*vkze__tqv)
    bfj__pjqb = []
    vkze__tqv = []
    xadi__ysjxo = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    for kvvc__xhskd in xadi__ysjxo:
        tla__omoca = typemap[kvvc__xhskd.name]
        zcqrm__xafe = array_analysis._gen_shape_call(equiv_set, kvvc__xhskd,
            tla__omoca.ndim, None, bfj__pjqb)
        equiv_set.insert_equiv(kvvc__xhskd, zcqrm__xafe)
        vkze__tqv.append(zcqrm__xafe[0])
        equiv_set.define(kvvc__xhskd, set())
    if len(vkze__tqv) > 1:
        equiv_set.insert_equiv(*vkze__tqv)
    return [], bfj__pjqb


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    nfqt__svmqr = sort_node.key_arrs + list(sort_node.df_in_vars.values())
    yrxwv__hfye = sort_node.out_key_arrs + list(sort_node.df_out_vars.values())
    bxttn__kkk = Distribution.OneD
    for kvvc__xhskd in nfqt__svmqr:
        bxttn__kkk = Distribution(min(bxttn__kkk.value, array_dists[
            kvvc__xhskd.name].value))
    qkwer__tzud = Distribution(min(bxttn__kkk.value, Distribution.OneD_Var.
        value))
    for kvvc__xhskd in yrxwv__hfye:
        if kvvc__xhskd.name in array_dists:
            qkwer__tzud = Distribution(min(qkwer__tzud.value, array_dists[
                kvvc__xhskd.name].value))
    if qkwer__tzud != Distribution.OneD_Var:
        bxttn__kkk = qkwer__tzud
    for kvvc__xhskd in nfqt__svmqr:
        array_dists[kvvc__xhskd.name] = bxttn__kkk
    for kvvc__xhskd in yrxwv__hfye:
        array_dists[kvvc__xhskd.name] = qkwer__tzud
    return


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for uyply__plipp, qnzyn__tmq in zip(sort_node.key_arrs, sort_node.
        out_key_arrs):
        typeinferer.constraints.append(typeinfer.Propagate(dst=qnzyn__tmq.
            name, src=uyply__plipp.name, loc=sort_node.loc))
    for nig__uvptt, kvvc__xhskd in sort_node.df_in_vars.items():
        thudu__gqs = sort_node.df_out_vars[nig__uvptt]
        typeinferer.constraints.append(typeinfer.Propagate(dst=thudu__gqs.
            name, src=kvvc__xhskd.name, loc=sort_node.loc))
    return


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for kvvc__xhskd in (sort_node.out_key_arrs + list(sort_node.
            df_out_vars.values())):
            definitions[kvvc__xhskd.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    if debug_prints():
        print('visiting sort vars for:', sort_node)
        print('cbdata: ', sorted(cbdata.items()))
    for duux__ijy in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[duux__ijy] = visit_vars_inner(sort_node.key_arrs
            [duux__ijy], callback, cbdata)
        sort_node.out_key_arrs[duux__ijy] = visit_vars_inner(sort_node.
            out_key_arrs[duux__ijy], callback, cbdata)
    for nig__uvptt in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[nig__uvptt] = visit_vars_inner(sort_node.
            df_in_vars[nig__uvptt], callback, cbdata)
    for nig__uvptt in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[nig__uvptt] = visit_vars_inner(sort_node.
            df_out_vars[nig__uvptt], callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    lmrrh__lrvod = []
    for nig__uvptt, kvvc__xhskd in sort_node.df_out_vars.items():
        if kvvc__xhskd.name not in lives:
            lmrrh__lrvod.append(nig__uvptt)
    for ouvd__cuyh in lmrrh__lrvod:
        sort_node.df_in_vars.pop(ouvd__cuyh)
        sort_node.df_out_vars.pop(ouvd__cuyh)
    if len(sort_node.df_out_vars) == 0 and all(eyudg__nmy.name not in lives for
        eyudg__nmy in sort_node.out_key_arrs):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({eyudg__nmy.name for eyudg__nmy in sort_node.key_arrs})
    use_set.update({eyudg__nmy.name for eyudg__nmy in sort_node.df_in_vars.
        values()})
    if not sort_node.inplace:
        def_set.update({eyudg__nmy.name for eyudg__nmy in sort_node.
            out_key_arrs})
        def_set.update({eyudg__nmy.name for eyudg__nmy in sort_node.
            df_out_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    ncapj__ezlpw = set()
    if not sort_node.inplace:
        ncapj__ezlpw = set(eyudg__nmy.name for eyudg__nmy in sort_node.
            df_out_vars.values())
        ncapj__ezlpw.update({eyudg__nmy.name for eyudg__nmy in sort_node.
            out_key_arrs})
    return set(), ncapj__ezlpw


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for duux__ijy in range(len(sort_node.key_arrs)):
        sort_node.key_arrs[duux__ijy] = replace_vars_inner(sort_node.
            key_arrs[duux__ijy], var_dict)
        sort_node.out_key_arrs[duux__ijy] = replace_vars_inner(sort_node.
            out_key_arrs[duux__ijy], var_dict)
    for nig__uvptt in list(sort_node.df_in_vars.keys()):
        sort_node.df_in_vars[nig__uvptt] = replace_vars_inner(sort_node.
            df_in_vars[nig__uvptt], var_dict)
    for nig__uvptt in list(sort_node.df_out_vars.keys()):
        sort_node.df_out_vars[nig__uvptt] = replace_vars_inner(sort_node.
            df_out_vars[nig__uvptt], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    xqei__dkpl = False
    ivsxx__yumn = list(sort_node.df_in_vars.values())
    xadi__ysjxo = list(sort_node.df_out_vars.values())
    if array_dists is not None:
        xqei__dkpl = True
        for eyudg__nmy in (sort_node.key_arrs + sort_node.out_key_arrs +
            ivsxx__yumn + xadi__ysjxo):
            if array_dists[eyudg__nmy.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                eyudg__nmy.name] != distributed_pass.Distribution.OneD_Var:
                xqei__dkpl = False
    loc = sort_node.loc
    dtd__aope = sort_node.key_arrs[0].scope
    nodes = []
    key_arrs = sort_node.key_arrs
    if not sort_node.inplace:
        fqaqs__zorgh = []
        for eyudg__nmy in key_arrs:
            nparp__nlek = _copy_array_nodes(eyudg__nmy, nodes, typingctx,
                targetctx, typemap, calltypes)
            fqaqs__zorgh.append(nparp__nlek)
        key_arrs = fqaqs__zorgh
        ujaz__zev = []
        for eyudg__nmy in ivsxx__yumn:
            mhos__esxy = _copy_array_nodes(eyudg__nmy, nodes, typingctx,
                targetctx, typemap, calltypes)
            ujaz__zev.append(mhos__esxy)
        ivsxx__yumn = ujaz__zev
    key_name_args = [f'key{duux__ijy}' for duux__ijy in range(len(key_arrs))]
    msmre__zsyjd = ', '.join(key_name_args)
    col_name_args = [f'c{duux__ijy}' for duux__ijy in range(len(ivsxx__yumn))]
    rkk__onkg = ', '.join(col_name_args)
    wpbjk__meboh = 'def f({}, {}):\n'.format(msmre__zsyjd, rkk__onkg)
    wpbjk__meboh += get_sort_cpp_section(key_name_args, col_name_args,
        sort_node.ascending_list, sort_node.na_position_b, xqei__dkpl)
    wpbjk__meboh += '  return key_arrs, data\n'
    hykor__nwa = {}
    exec(wpbjk__meboh, {}, hykor__nwa)
    gylp__hmtsq = hykor__nwa['f']
    ybm__sximb = types.Tuple([typemap[eyudg__nmy.name] for eyudg__nmy in
        key_arrs])
    sasn__abol = types.Tuple([typemap[eyudg__nmy.name] for eyudg__nmy in
        ivsxx__yumn])
    ezvax__zpxb = compile_to_numba_ir(gylp__hmtsq, {'bodo': bodo, 'np': np,
        'to_list_if_immutable_arr': to_list_if_immutable_arr,
        'cp_str_list_to_array': cp_str_list_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'sort_values_table':
        sort_values_table, 'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=tuple(list(ybm__sximb.types) + list(sasn__abol.
        types)), typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(ezvax__zpxb, key_arrs + ivsxx__yumn)
    nodes += ezvax__zpxb.body[:-2]
    aomp__oxjo = nodes[-1].target
    akteq__sjlfg = ir.Var(dtd__aope, mk_unique_var('key_data'), loc)
    typemap[akteq__sjlfg.name] = ybm__sximb
    gen_getitem(akteq__sjlfg, aomp__oxjo, 0, calltypes, nodes)
    lorfo__xotlg = ir.Var(dtd__aope, mk_unique_var('sort_data'), loc)
    typemap[lorfo__xotlg.name] = sasn__abol
    gen_getitem(lorfo__xotlg, aomp__oxjo, 1, calltypes, nodes)
    for duux__ijy, var in enumerate(sort_node.out_key_arrs):
        gen_getitem(var, akteq__sjlfg, duux__ijy, calltypes, nodes)
    for duux__ijy, var in enumerate(xadi__ysjxo):
        gen_getitem(var, lorfo__xotlg, duux__ijy, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes):

    def _impl(arr):
        return arr.copy()
    ezvax__zpxb = compile_to_numba_ir(_impl, {}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(ezvax__zpxb, [var])
    nodes += ezvax__zpxb.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(key_name_args, col_name_args, ascending_list,
    na_position_b, parallel_b):
    wpbjk__meboh = ''
    fxaap__ovv = len(key_name_args)
    wnh__zrok = ['array_to_info({})'.format(tbs__shu) for tbs__shu in
        key_name_args] + ['array_to_info({})'.format(tbs__shu) for tbs__shu in
        col_name_args]
    wpbjk__meboh += '  info_list_total = [{}]\n'.format(','.join(wnh__zrok))
    wpbjk__meboh += '  table_total = arr_info_list_to_table(info_list_total)\n'
    wpbjk__meboh += '  vect_ascending = np.array([{}])\n'.format(','.join(
        '1' if umx__owqv else '0' for umx__owqv in ascending_list))
    wpbjk__meboh += '  na_position = np.array([{}])\n'.format(','.join('1' if
        umx__owqv else '0' for umx__owqv in na_position_b))
    wpbjk__meboh += (
        """  out_table = sort_values_table(table_total, {}, vect_ascending.ctypes, na_position.ctypes, {})
"""
        .format(fxaap__ovv, parallel_b))
    asd__nkcu = 0
    zcwv__hgxq = []
    for tbs__shu in key_name_args:
        zcwv__hgxq.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(asd__nkcu, tbs__shu))
        asd__nkcu += 1
    wpbjk__meboh += '  key_arrs = ({},)\n'.format(','.join(zcwv__hgxq))
    usp__nrbox = []
    for tbs__shu in col_name_args:
        usp__nrbox.append('info_to_array(info_from_table(out_table, {}), {})'
            .format(asd__nkcu, tbs__shu))
        asd__nkcu += 1
    if len(usp__nrbox) > 0:
        wpbjk__meboh += '  data = ({},)\n'.format(','.join(usp__nrbox))
    else:
        wpbjk__meboh += '  data = ()\n'
    wpbjk__meboh += '  delete_table(out_table)\n'
    wpbjk__meboh += '  delete_table(table_total)\n'
    return wpbjk__meboh
