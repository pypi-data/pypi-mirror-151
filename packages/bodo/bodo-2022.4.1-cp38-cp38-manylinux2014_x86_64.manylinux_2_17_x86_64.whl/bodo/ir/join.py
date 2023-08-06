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
        bdxl__iwhj = func.signature
        yxb__rkv = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        ekvvy__lcq = cgutils.get_or_insert_function(builder.module,
            yxb__rkv, sym._literal_value)
        builder.call(ekvvy__lcq, [context.get_constant_null(bdxl__iwhj.args
            [0]), context.get_constant_null(bdxl__iwhj.args[1]), context.
            get_constant_null(bdxl__iwhj.args[2]), context.
            get_constant_null(bdxl__iwhj.args[3]), context.
            get_constant_null(bdxl__iwhj.args[4]), context.
            get_constant_null(bdxl__iwhj.args[5]), context.get_constant(
            types.int64, 0), context.get_constant(types.int64, 0)])
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
        self.left_cond_cols = set(qfu__kdwd for qfu__kdwd in left_vars.keys
            () if f'(left.{qfu__kdwd})' in gen_cond_expr)
        self.right_cond_cols = set(qfu__kdwd for qfu__kdwd in right_vars.
            keys() if f'(right.{qfu__kdwd})' in gen_cond_expr)
        lzt__ldq = set(left_keys) & set(right_keys)
        epw__mucfq = set(left_vars.keys()) & set(right_vars.keys())
        ynexh__ovlnn = epw__mucfq - lzt__ldq
        vect_same_key = []
        n_keys = len(left_keys)
        for sxqlh__udst in range(n_keys):
            rww__pqkk = left_keys[sxqlh__udst]
            ofxmy__vuvv = right_keys[sxqlh__udst]
            vect_same_key.append(rww__pqkk == ofxmy__vuvv)
        self.vect_same_key = vect_same_key
        self.column_origins = {(str(qfu__kdwd) + suffix_x if qfu__kdwd in
            ynexh__ovlnn else qfu__kdwd): ('left', qfu__kdwd) for qfu__kdwd in
            left_vars.keys()}
        self.column_origins.update({(str(qfu__kdwd) + suffix_y if qfu__kdwd in
            ynexh__ovlnn else qfu__kdwd): ('right', qfu__kdwd) for
            qfu__kdwd in right_vars.keys()})
        if '$_bodo_index_' in ynexh__ovlnn:
            ynexh__ovlnn.remove('$_bodo_index_')
        self.add_suffix = ynexh__ovlnn

    def __repr__(self):
        mkt__hpu = ''
        for qfu__kdwd, fmsk__sgfwl in self.out_data_vars.items():
            mkt__hpu += "'{}':{}, ".format(qfu__kdwd, fmsk__sgfwl.name)
        hruto__yzgs = '{}{{{}}}'.format(self.df_out, mkt__hpu)
        npyg__uipij = ''
        for qfu__kdwd, fmsk__sgfwl in self.left_vars.items():
            npyg__uipij += "'{}':{}, ".format(qfu__kdwd, fmsk__sgfwl.name)
        ntfe__slmcx = '{}{{{}}}'.format(self.left_df, npyg__uipij)
        npyg__uipij = ''
        for qfu__kdwd, fmsk__sgfwl in self.right_vars.items():
            npyg__uipij += "'{}':{}, ".format(qfu__kdwd, fmsk__sgfwl.name)
        gdqcy__cov = '{}{{{}}}'.format(self.right_df, npyg__uipij)
        return 'join [{}={}]: {} , {}, {}'.format(self.left_keys, self.
            right_keys, hruto__yzgs, ntfe__slmcx, gdqcy__cov)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    rwams__soe = []
    assert len(join_node.out_data_vars) > 0, 'empty join in array analysis'
    vkkfr__ctyjh = []
    zzda__vzm = list(join_node.left_vars.values())
    for ezii__buj in zzda__vzm:
        jqfkn__rkkpe = typemap[ezii__buj.name]
        yug__movyd = equiv_set.get_shape(ezii__buj)
        if yug__movyd:
            vkkfr__ctyjh.append(yug__movyd[0])
    if len(vkkfr__ctyjh) > 1:
        equiv_set.insert_equiv(*vkkfr__ctyjh)
    vkkfr__ctyjh = []
    zzda__vzm = list(join_node.right_vars.values())
    for ezii__buj in zzda__vzm:
        jqfkn__rkkpe = typemap[ezii__buj.name]
        yug__movyd = equiv_set.get_shape(ezii__buj)
        if yug__movyd:
            vkkfr__ctyjh.append(yug__movyd[0])
    if len(vkkfr__ctyjh) > 1:
        equiv_set.insert_equiv(*vkkfr__ctyjh)
    vkkfr__ctyjh = []
    for ezii__buj in join_node.out_data_vars.values():
        jqfkn__rkkpe = typemap[ezii__buj.name]
        pihg__qsu = array_analysis._gen_shape_call(equiv_set, ezii__buj,
            jqfkn__rkkpe.ndim, None, rwams__soe)
        equiv_set.insert_equiv(ezii__buj, pihg__qsu)
        vkkfr__ctyjh.append(pihg__qsu[0])
        equiv_set.define(ezii__buj, set())
    if len(vkkfr__ctyjh) > 1:
        equiv_set.insert_equiv(*vkkfr__ctyjh)
    return [], rwams__soe


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    vavkc__kijb = Distribution.OneD
    nod__cktat = Distribution.OneD
    for ezii__buj in join_node.left_vars.values():
        vavkc__kijb = Distribution(min(vavkc__kijb.value, array_dists[
            ezii__buj.name].value))
    for ezii__buj in join_node.right_vars.values():
        nod__cktat = Distribution(min(nod__cktat.value, array_dists[
            ezii__buj.name].value))
    kml__xcqxm = Distribution.OneD_Var
    for ezii__buj in join_node.out_data_vars.values():
        if ezii__buj.name in array_dists:
            kml__xcqxm = Distribution(min(kml__xcqxm.value, array_dists[
                ezii__buj.name].value))
    yxrro__eco = Distribution(min(kml__xcqxm.value, vavkc__kijb.value))
    ofiz__noml = Distribution(min(kml__xcqxm.value, nod__cktat.value))
    kml__xcqxm = Distribution(max(yxrro__eco.value, ofiz__noml.value))
    for ezii__buj in join_node.out_data_vars.values():
        array_dists[ezii__buj.name] = kml__xcqxm
    if kml__xcqxm != Distribution.OneD_Var:
        vavkc__kijb = kml__xcqxm
        nod__cktat = kml__xcqxm
    for ezii__buj in join_node.left_vars.values():
        array_dists[ezii__buj.name] = vavkc__kijb
    for ezii__buj in join_node.right_vars.values():
        array_dists[ezii__buj.name] = nod__cktat
    return


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def join_typeinfer(join_node, typeinferer):
    lzt__ldq = set(join_node.left_keys) & set(join_node.right_keys)
    epw__mucfq = set(join_node.left_vars.keys()) & set(join_node.right_vars
        .keys())
    ynexh__ovlnn = epw__mucfq - lzt__ldq
    for nhzrn__gwobg, eznum__etf in join_node.out_data_vars.items():
        if join_node.indicator and nhzrn__gwobg == '_merge':
            continue
        if not nhzrn__gwobg in join_node.column_origins:
            raise BodoError('join(): The variable ' + nhzrn__gwobg +
                ' is absent from the output')
        butlv__rzpk = join_node.column_origins[nhzrn__gwobg]
        if butlv__rzpk[0] == 'left':
            ezii__buj = join_node.left_vars[butlv__rzpk[1]]
        else:
            ezii__buj = join_node.right_vars[butlv__rzpk[1]]
        typeinferer.constraints.append(typeinfer.Propagate(dst=eznum__etf.
            name, src=ezii__buj.name, loc=join_node.loc))
    return


typeinfer.typeinfer_extensions[Join] = join_typeinfer


def visit_vars_join(join_node, callback, cbdata):
    if debug_prints():
        print('visiting join vars for:', join_node)
        print('cbdata: ', sorted(cbdata.items()))
    for avgk__vkcm in list(join_node.left_vars.keys()):
        join_node.left_vars[avgk__vkcm] = visit_vars_inner(join_node.
            left_vars[avgk__vkcm], callback, cbdata)
    for avgk__vkcm in list(join_node.right_vars.keys()):
        join_node.right_vars[avgk__vkcm] = visit_vars_inner(join_node.
            right_vars[avgk__vkcm], callback, cbdata)
    for avgk__vkcm in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[avgk__vkcm] = visit_vars_inner(join_node.
            out_data_vars[avgk__vkcm], callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    nbqfu__nsn = []
    caklj__brry = True
    for avgk__vkcm, ezii__buj in join_node.out_data_vars.items():
        if ezii__buj.name in lives:
            caklj__brry = False
            continue
        if avgk__vkcm == '$_bodo_index_':
            continue
        if join_node.indicator and avgk__vkcm == '_merge':
            nbqfu__nsn.append('_merge')
            join_node.indicator = False
            continue
        nyw__amnho, sjvmr__ftnn = join_node.column_origins[avgk__vkcm]
        if (nyw__amnho == 'left' and sjvmr__ftnn not in join_node.left_keys and
            sjvmr__ftnn not in join_node.left_cond_cols):
            join_node.left_vars.pop(sjvmr__ftnn)
            nbqfu__nsn.append(avgk__vkcm)
        if (nyw__amnho == 'right' and sjvmr__ftnn not in join_node.
            right_keys and sjvmr__ftnn not in join_node.right_cond_cols):
            join_node.right_vars.pop(sjvmr__ftnn)
            nbqfu__nsn.append(avgk__vkcm)
    for cname in nbqfu__nsn:
        join_node.out_data_vars.pop(cname)
    if caklj__brry:
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({fmsk__sgfwl.name for fmsk__sgfwl in join_node.left_vars
        .values()})
    use_set.update({fmsk__sgfwl.name for fmsk__sgfwl in join_node.
        right_vars.values()})
    def_set.update({fmsk__sgfwl.name for fmsk__sgfwl in join_node.
        out_data_vars.values()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    ctela__hfiw = set(fmsk__sgfwl.name for fmsk__sgfwl in join_node.
        out_data_vars.values())
    return set(), ctela__hfiw


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for avgk__vkcm in list(join_node.left_vars.keys()):
        join_node.left_vars[avgk__vkcm] = replace_vars_inner(join_node.
            left_vars[avgk__vkcm], var_dict)
    for avgk__vkcm in list(join_node.right_vars.keys()):
        join_node.right_vars[avgk__vkcm] = replace_vars_inner(join_node.
            right_vars[avgk__vkcm], var_dict)
    for avgk__vkcm in list(join_node.out_data_vars.keys()):
        join_node.out_data_vars[avgk__vkcm] = replace_vars_inner(join_node.
            out_data_vars[avgk__vkcm], var_dict)
    return


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for ezii__buj in join_node.out_data_vars.values():
        definitions[ezii__buj.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    n_keys = len(join_node.left_keys)
    kiepk__jae = tuple(join_node.left_vars[qfu__kdwd] for qfu__kdwd in
        join_node.left_keys)
    nqf__yltpm = tuple(join_node.right_vars[qfu__kdwd] for qfu__kdwd in
        join_node.right_keys)
    ksaxw__fodpt = tuple(join_node.left_vars.keys())
    xtr__dogm = tuple(join_node.right_vars.keys())
    acnk__spxu = ()
    nag__rzrc = ()
    optional_column = False
    if (join_node.left_index and not join_node.right_index and not
        join_node.is_join):
        swma__yyjg = join_node.right_keys[0]
        if swma__yyjg in ksaxw__fodpt:
            nag__rzrc = swma__yyjg,
            acnk__spxu = join_node.right_vars[swma__yyjg],
            optional_column = True
    if (join_node.right_index and not join_node.left_index and not
        join_node.is_join):
        swma__yyjg = join_node.left_keys[0]
        if swma__yyjg in xtr__dogm:
            nag__rzrc = swma__yyjg,
            acnk__spxu = join_node.left_vars[swma__yyjg],
            optional_column = True
    twfu__crl = tuple(join_node.out_data_vars[cname] for cname in nag__rzrc)
    eayc__dwm = tuple(fmsk__sgfwl for nzek__rnyox, fmsk__sgfwl in sorted(
        join_node.left_vars.items(), key=lambda a: str(a[0])) if 
        nzek__rnyox not in join_node.left_keys)
    dosee__xal = tuple(fmsk__sgfwl for nzek__rnyox, fmsk__sgfwl in sorted(
        join_node.right_vars.items(), key=lambda a: str(a[0])) if 
        nzek__rnyox not in join_node.right_keys)
    qwyi__uzdg = acnk__spxu + kiepk__jae + nqf__yltpm + eayc__dwm + dosee__xal
    bjcp__nngx = tuple(typemap[fmsk__sgfwl.name] for fmsk__sgfwl in qwyi__uzdg)
    cooy__jlcxf = tuple('opti_c' + str(veo__owxn) for veo__owxn in range(
        len(acnk__spxu)))
    left_other_names = tuple('t1_c' + str(veo__owxn) for veo__owxn in range
        (len(eayc__dwm)))
    right_other_names = tuple('t2_c' + str(veo__owxn) for veo__owxn in
        range(len(dosee__xal)))
    left_other_types = tuple([typemap[qfu__kdwd.name] for qfu__kdwd in
        eayc__dwm])
    right_other_types = tuple([typemap[qfu__kdwd.name] for qfu__kdwd in
        dosee__xal])
    left_key_names = tuple('t1_key' + str(veo__owxn) for veo__owxn in range
        (n_keys))
    right_key_names = tuple('t2_key' + str(veo__owxn) for veo__owxn in
        range(n_keys))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}{}, {},{}{}{}):\n'.format('{},'.format(cooy__jlcxf
        [0]) if len(cooy__jlcxf) == 1 else '', ','.join(left_key_names),
        ','.join(right_key_names), ','.join(left_other_names), ',' if len(
        left_other_names) != 0 else '', ','.join(right_other_names))
    left_key_types = tuple(typemap[fmsk__sgfwl.name] for fmsk__sgfwl in
        kiepk__jae)
    right_key_types = tuple(typemap[fmsk__sgfwl.name] for fmsk__sgfwl in
        nqf__yltpm)
    for veo__owxn in range(n_keys):
        glbs[f'key_type_{veo__owxn}'] = _match_join_key_types(left_key_types
            [veo__owxn], right_key_types[veo__owxn], loc)
    func_text += '    t1_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({left_key_names[veo__owxn]}, key_type_{veo__owxn})'
         for veo__owxn in range(n_keys)))
    func_text += '    t2_keys = ({},)\n'.format(', '.join(
        f'bodo.utils.utils.astype({right_key_names[veo__owxn]}, key_type_{veo__owxn})'
         for veo__owxn in range(n_keys)))
    func_text += '    data_left = ({}{})\n'.format(','.join(
        left_other_names), ',' if len(left_other_names) != 0 else '')
    func_text += '    data_right = ({}{})\n'.format(','.join(
        right_other_names), ',' if len(right_other_names) != 0 else '')
    dib__wus = []
    for cname in join_node.left_keys:
        if cname in join_node.add_suffix:
            fvv__mrob = str(cname) + join_node.suffix_x
        else:
            fvv__mrob = cname
        assert fvv__mrob in join_node.out_data_vars
        dib__wus.append(join_node.out_data_vars[fvv__mrob])
    for veo__owxn, cname in enumerate(join_node.right_keys):
        if not join_node.vect_same_key[veo__owxn] and not join_node.is_join:
            if cname in join_node.add_suffix:
                fvv__mrob = str(cname) + join_node.suffix_y
            else:
                fvv__mrob = cname
            assert fvv__mrob in join_node.out_data_vars
            dib__wus.append(join_node.out_data_vars[fvv__mrob])

    def _get_out_col_var(cname, is_left):
        if cname in join_node.add_suffix:
            if is_left:
                fvv__mrob = str(cname) + join_node.suffix_x
            else:
                fvv__mrob = str(cname) + join_node.suffix_y
        else:
            fvv__mrob = cname
        return join_node.out_data_vars[fvv__mrob]
    nassl__hgt = twfu__crl + tuple(dib__wus)
    nassl__hgt += tuple(_get_out_col_var(nzek__rnyox, True) for nzek__rnyox,
        fmsk__sgfwl in sorted(join_node.left_vars.items(), key=lambda a:
        str(a[0])) if nzek__rnyox not in join_node.left_keys)
    nassl__hgt += tuple(_get_out_col_var(nzek__rnyox, False) for 
        nzek__rnyox, fmsk__sgfwl in sorted(join_node.right_vars.items(),
        key=lambda a: str(a[0])) if nzek__rnyox not in join_node.right_keys)
    if join_node.indicator:
        nassl__hgt += _get_out_col_var('_merge', False),
    wxe__nwga = [('t3_c' + str(veo__owxn)) for veo__owxn in range(len(
        nassl__hgt))]
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
            right_parallel, glbs, [typemap[fmsk__sgfwl.name] for
            fmsk__sgfwl in nassl__hgt], join_node.loc, join_node.indicator,
            join_node.is_na_equal, general_cond_cfunc, left_col_nums,
            right_col_nums)
    if join_node.how == 'asof':
        for veo__owxn in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(veo__owxn,
                veo__owxn)
        for veo__owxn in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(veo__owxn
                , veo__owxn)
        for veo__owxn in range(n_keys):
            func_text += (
                f'    t1_keys_{veo__owxn} = out_t1_keys[{veo__owxn}]\n')
        for veo__owxn in range(n_keys):
            func_text += (
                f'    t2_keys_{veo__owxn} = out_t2_keys[{veo__owxn}]\n')
    idx = 0
    if optional_column:
        func_text += f'    {wxe__nwga[idx]} = opti_0\n'
        idx += 1
    for veo__owxn in range(n_keys):
        func_text += f'    {wxe__nwga[idx]} = t1_keys_{veo__owxn}\n'
        idx += 1
    for veo__owxn in range(n_keys):
        if not join_node.vect_same_key[veo__owxn] and not join_node.is_join:
            func_text += f'    {wxe__nwga[idx]} = t2_keys_{veo__owxn}\n'
            idx += 1
    for veo__owxn in range(len(left_other_names)):
        func_text += f'    {wxe__nwga[idx]} = left_{veo__owxn}\n'
        idx += 1
    for veo__owxn in range(len(right_other_names)):
        func_text += f'    {wxe__nwga[idx]} = right_{veo__owxn}\n'
        idx += 1
    if join_node.indicator:
        func_text += f'    {wxe__nwga[idx]} = indicator_col\n'
        idx += 1
    ygzli__mui = {}
    exec(func_text, {}, ygzli__mui)
    tsuwr__vezdc = ygzli__mui['f']
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
    qxi__ekxl = compile_to_numba_ir(tsuwr__vezdc, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=bjcp__nngx, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(qxi__ekxl, qwyi__uzdg)
    hfqs__bgk = qxi__ekxl.body[:-3]
    for veo__owxn in range(len(nassl__hgt)):
        hfqs__bgk[-len(nassl__hgt) + veo__owxn].target = nassl__hgt[veo__owxn]
    return hfqs__bgk


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    circc__xwrmb = next_label()
    onm__tuq = _get_col_to_ind(join_node.left_keys, join_node.left_vars)
    kwalf__kuuak = _get_col_to_ind(join_node.right_keys, join_node.right_vars)
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{circc__xwrmb}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        onm__tuq, typemap, join_node.left_vars, table_getitem_funcs,
        func_text, 'left', len(join_node.left_keys), na_check_name)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        kwalf__kuuak, typemap, join_node.right_vars, table_getitem_funcs,
        func_text, 'right', len(join_node.right_keys), na_check_name)
    func_text += f'  return {expr}'
    ygzli__mui = {}
    exec(func_text, table_getitem_funcs, ygzli__mui)
    goj__xpbvd = ygzli__mui[f'bodo_join_gen_cond{circc__xwrmb}']
    jmlpw__biri = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    upli__qpxn = numba.cfunc(jmlpw__biri, nopython=True)(goj__xpbvd)
    join_gen_cond_cfunc[upli__qpxn.native_name] = upli__qpxn
    join_gen_cond_cfunc_addr[upli__qpxn.native_name] = upli__qpxn.address
    return upli__qpxn, left_col_nums, right_col_nums


def _replace_column_accesses(expr, col_to_ind, typemap, col_vars,
    table_getitem_funcs, func_text, table_name, n_keys, na_check_name):
    xtf__ocvqu = []
    for qfu__kdwd, iwnrx__xza in col_to_ind.items():
        cname = f'({table_name}.{qfu__kdwd})'
        if cname not in expr:
            continue
        rujbc__luncu = f'getitem_{table_name}_val_{iwnrx__xza}'
        uceqr__afi = f'_bodo_{table_name}_val_{iwnrx__xza}'
        sqr__jdekm = typemap[col_vars[qfu__kdwd].name]
        if is_str_arr_type(sqr__jdekm):
            func_text += f"""  {uceqr__afi}, {uceqr__afi}_size = {rujbc__luncu}({table_name}_table, {table_name}_ind)
"""
            func_text += f"""  {uceqr__afi} = bodo.libs.str_arr_ext.decode_utf8({uceqr__afi}, {uceqr__afi}_size)
"""
        else:
            func_text += (
                f'  {uceqr__afi} = {rujbc__luncu}({table_name}_data1, {table_name}_ind)\n'
                )
        table_getitem_funcs[rujbc__luncu
            ] = bodo.libs.array._gen_row_access_intrinsic(sqr__jdekm,
            iwnrx__xza)
        expr = expr.replace(cname, uceqr__afi)
        ilvek__mrz = f'({na_check_name}.{table_name}.{qfu__kdwd})'
        if ilvek__mrz in expr:
            qhyu__bhes = f'nacheck_{table_name}_val_{iwnrx__xza}'
            vqiz__lxkwx = f'_bodo_isna_{table_name}_val_{iwnrx__xza}'
            if (isinstance(sqr__jdekm, bodo.libs.int_arr_ext.
                IntegerArrayType) or sqr__jdekm == bodo.libs.bool_arr_ext.
                boolean_array or is_str_arr_type(sqr__jdekm)):
                func_text += f"""  {vqiz__lxkwx} = {qhyu__bhes}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {vqiz__lxkwx} = {qhyu__bhes}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[qhyu__bhes
                ] = bodo.libs.array._gen_row_na_check_intrinsic(sqr__jdekm,
                iwnrx__xza)
            expr = expr.replace(ilvek__mrz, vqiz__lxkwx)
        if iwnrx__xza >= n_keys:
            xtf__ocvqu.append(iwnrx__xza)
    return expr, func_text, xtf__ocvqu


def _get_col_to_ind(key_names, col_vars):
    n_keys = len(key_names)
    col_to_ind = {qfu__kdwd: veo__owxn for veo__owxn, qfu__kdwd in
        enumerate(key_names)}
    veo__owxn = n_keys
    for qfu__kdwd in sorted(col_vars, key=lambda a: str(a)):
        if qfu__kdwd in key_names:
            continue
        col_to_ind[qfu__kdwd] = veo__owxn
        veo__owxn += 1
    return col_to_ind


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as nav__sesay:
        if is_str_arr_type(t1) and is_str_arr_type(t2):
            return bodo.string_array_type
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    ydbyd__gxbgh = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[fmsk__sgfwl.name] in ydbyd__gxbgh for
        fmsk__sgfwl in join_node.left_vars.values())
    right_parallel = all(array_dists[fmsk__sgfwl.name] in ydbyd__gxbgh for
        fmsk__sgfwl in join_node.right_vars.values())
    if not left_parallel:
        assert not any(array_dists[fmsk__sgfwl.name] in ydbyd__gxbgh for
            fmsk__sgfwl in join_node.left_vars.values())
    if not right_parallel:
        assert not any(array_dists[fmsk__sgfwl.name] in ydbyd__gxbgh for
            fmsk__sgfwl in join_node.right_vars.values())
    if left_parallel or right_parallel:
        assert all(array_dists[fmsk__sgfwl.name] in ydbyd__gxbgh for
            fmsk__sgfwl in join_node.out_data_vars.values())
    return left_parallel, right_parallel


def _gen_local_hash_join(optional_column, left_key_names, right_key_names,
    left_key_types, right_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, vect_same_key, is_left, is_right,
    is_join, left_parallel, right_parallel, glbs, out_types, loc, indicator,
    is_na_equal, general_cond_cfunc, left_col_nums, right_col_nums):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    bottl__jibo = []
    for veo__owxn in range(len(left_key_names)):
        pskmr__pcpi = _match_join_key_types(left_key_types[veo__owxn],
            right_key_types[veo__owxn], loc)
        bottl__jibo.append(needs_typechange(pskmr__pcpi, is_right,
            vect_same_key[veo__owxn]))
    for veo__owxn in range(len(left_other_names)):
        bottl__jibo.append(needs_typechange(left_other_types[veo__owxn],
            is_right, False))
    for veo__owxn in range(len(right_key_names)):
        if not vect_same_key[veo__owxn] and not is_join:
            pskmr__pcpi = _match_join_key_types(left_key_types[veo__owxn],
                right_key_types[veo__owxn], loc)
            bottl__jibo.append(needs_typechange(pskmr__pcpi, is_left, False))
    for veo__owxn in range(len(right_other_names)):
        bottl__jibo.append(needs_typechange(right_other_types[veo__owxn],
            is_left, False))

    def get_out_type(idx, in_type, in_name, need_nullable, is_same_key):
        if isinstance(in_type, types.Array) and not is_dtype_nullable(in_type
            .dtype) and need_nullable and not is_same_key:
            if isinstance(in_type.dtype, types.Integer):
                pnpjs__wpgb = IntDtype(in_type.dtype).name
                assert pnpjs__wpgb.endswith('Dtype()')
                pnpjs__wpgb = pnpjs__wpgb[:-7]
                uiz__rxp = f"""    typ_{idx} = bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype="{pnpjs__wpgb}"))
"""
                hgx__pvo = f'typ_{idx}'
            else:
                assert in_type.dtype == types.bool_, 'unexpected non-nullable type in join'
                uiz__rxp = (
                    f'    typ_{idx} = bodo.libs.bool_arr_ext.alloc_bool_array(1)\n'
                    )
                hgx__pvo = f'typ_{idx}'
        elif in_type == bodo.string_array_type:
            uiz__rxp = (
                f'    typ_{idx} = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)\n'
                )
            hgx__pvo = f'typ_{idx}'
        else:
            uiz__rxp = ''
            hgx__pvo = in_name
        return uiz__rxp, hgx__pvo
    n_keys = len(left_key_names)
    func_text = '    # beginning of _gen_local_hash_join\n'
    teb__ofc = []
    for veo__owxn in range(n_keys):
        teb__ofc.append('t1_keys[{}]'.format(veo__owxn))
    for veo__owxn in range(len(left_other_names)):
        teb__ofc.append('data_left[{}]'.format(veo__owxn))
    func_text += '    info_list_total_l = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in teb__ofc))
    func_text += '    table_left = arr_info_list_to_table(info_list_total_l)\n'
    acz__kglm = []
    for veo__owxn in range(n_keys):
        acz__kglm.append('t2_keys[{}]'.format(veo__owxn))
    for veo__owxn in range(len(right_other_names)):
        acz__kglm.append('data_right[{}]'.format(veo__owxn))
    func_text += '    info_list_total_r = [{}]\n'.format(','.join(
        'array_to_info({})'.format(a) for a in acz__kglm))
    func_text += (
        '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    func_text += '    vect_same_key = np.array([{}])\n'.format(','.join('1' if
        uxw__lif else '0' for uxw__lif in vect_same_key))
    func_text += '    vect_need_typechange = np.array([{}])\n'.format(','.
        join('1' if uxw__lif else '0' for uxw__lif in bottl__jibo))
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
        artw__ixmb = get_out_type(idx, out_types[idx], 'opti_c0', False, False)
        func_text += artw__ixmb[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        func_text += f"""    opti_0 = info_to_array(info_from_table(out_table, {idx}), {artw__ixmb[1]})
"""
        idx += 1
    for veo__owxn, lhe__pbs in enumerate(left_key_names):
        pskmr__pcpi = _match_join_key_types(left_key_types[veo__owxn],
            right_key_types[veo__owxn], loc)
        artw__ixmb = get_out_type(idx, pskmr__pcpi, f't1_keys[{veo__owxn}]',
            is_right, vect_same_key[veo__owxn])
        func_text += artw__ixmb[0]
        glbs[f'out_type_{idx}'] = out_types[idx]
        if pskmr__pcpi != left_key_types[veo__owxn] and left_key_types[
            veo__owxn] != bodo.dict_str_arr_type:
            func_text += f"""    t1_keys_{veo__owxn} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {artw__ixmb[1]}), out_type_{idx})
"""
        else:
            func_text += f"""    t1_keys_{veo__owxn} = info_to_array(info_from_table(out_table, {idx}), {artw__ixmb[1]})
"""
        idx += 1
    for veo__owxn, lhe__pbs in enumerate(left_other_names):
        artw__ixmb = get_out_type(idx, left_other_types[veo__owxn],
            lhe__pbs, is_right, False)
        func_text += artw__ixmb[0]
        func_text += (
            '    left_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(veo__owxn, idx, artw__ixmb[1]))
        idx += 1
    for veo__owxn, lhe__pbs in enumerate(right_key_names):
        if not vect_same_key[veo__owxn] and not is_join:
            pskmr__pcpi = _match_join_key_types(left_key_types[veo__owxn],
                right_key_types[veo__owxn], loc)
            artw__ixmb = get_out_type(idx, pskmr__pcpi,
                f't2_keys[{veo__owxn}]', is_left, False)
            func_text += artw__ixmb[0]
            glbs[f'out_type_{idx}'] = out_types[idx - len(left_other_names)]
            if pskmr__pcpi != right_key_types[veo__owxn] and right_key_types[
                veo__owxn] != bodo.dict_str_arr_type:
                func_text += f"""    t2_keys_{veo__owxn} = bodo.utils.utils.astype(info_to_array(info_from_table(out_table, {idx}), {artw__ixmb[1]}), out_type_{idx})
"""
            else:
                func_text += f"""    t2_keys_{veo__owxn} = info_to_array(info_from_table(out_table, {idx}), {artw__ixmb[1]})
"""
            idx += 1
    for veo__owxn, lhe__pbs in enumerate(right_other_names):
        artw__ixmb = get_out_type(idx, right_other_types[veo__owxn],
            lhe__pbs, is_left, False)
        func_text += artw__ixmb[0]
        func_text += (
            '    right_{} = info_to_array(info_from_table(out_table, {}), {})\n'
            .format(veo__owxn, idx, artw__ixmb[1]))
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
    yok__msz = bodo.libs.distributed_api.get_size()
    ukyy__kes = np.empty(yok__msz, left_key_arrs[0].dtype)
    fxeh__yiii = np.empty(yok__msz, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(ukyy__kes, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(fxeh__yiii, left_key_arrs[0][-1])
    derp__kbjg = np.zeros(yok__msz, np.int32)
    xdi__ets = np.zeros(yok__msz, np.int32)
    oou__xhglf = np.zeros(yok__msz, np.int32)
    euaxn__ztw = right_key_arrs[0][0]
    thg__ufgej = right_key_arrs[0][-1]
    ewsoa__gvk = -1
    veo__owxn = 0
    while veo__owxn < yok__msz - 1 and fxeh__yiii[veo__owxn] < euaxn__ztw:
        veo__owxn += 1
    while veo__owxn < yok__msz and ukyy__kes[veo__owxn] <= thg__ufgej:
        ewsoa__gvk, pihus__ujecj = _count_overlap(right_key_arrs[0],
            ukyy__kes[veo__owxn], fxeh__yiii[veo__owxn])
        if ewsoa__gvk != 0:
            ewsoa__gvk -= 1
            pihus__ujecj += 1
        derp__kbjg[veo__owxn] = pihus__ujecj
        xdi__ets[veo__owxn] = ewsoa__gvk
        veo__owxn += 1
    while veo__owxn < yok__msz:
        derp__kbjg[veo__owxn] = 1
        xdi__ets[veo__owxn] = len(right_key_arrs[0]) - 1
        veo__owxn += 1
    bodo.libs.distributed_api.alltoall(derp__kbjg, oou__xhglf, 1)
    ohzb__dbbp = oou__xhglf.sum()
    zpa__bzjm = np.empty(ohzb__dbbp, right_key_arrs[0].dtype)
    ugz__djlhc = alloc_arr_tup(ohzb__dbbp, right_data)
    javav__ynq = bodo.ir.join.calc_disp(oou__xhglf)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], zpa__bzjm,
        derp__kbjg, oou__xhglf, xdi__ets, javav__ynq)
    bodo.libs.distributed_api.alltoallv_tup(right_data, ugz__djlhc,
        derp__kbjg, oou__xhglf, xdi__ets, javav__ynq)
    return (zpa__bzjm,), ugz__djlhc


@numba.njit
def _count_overlap(r_key_arr, start, end):
    pihus__ujecj = 0
    ewsoa__gvk = 0
    jzvlr__mympw = 0
    while jzvlr__mympw < len(r_key_arr) and r_key_arr[jzvlr__mympw] < start:
        ewsoa__gvk += 1
        jzvlr__mympw += 1
    while jzvlr__mympw < len(r_key_arr) and start <= r_key_arr[jzvlr__mympw
        ] <= end:
        jzvlr__mympw += 1
        pihus__ujecj += 1
    return ewsoa__gvk, pihus__ujecj


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    umlpm__cdh = np.empty_like(arr)
    umlpm__cdh[0] = 0
    for veo__owxn in range(1, len(arr)):
        umlpm__cdh[veo__owxn] = umlpm__cdh[veo__owxn - 1] + arr[veo__owxn - 1]
    return umlpm__cdh


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    hryb__uyos = len(left_keys[0])
    rdc__szsix = len(right_keys[0])
    ozmtk__ghse = alloc_arr_tup(hryb__uyos, left_keys)
    yvgf__zmxxe = alloc_arr_tup(hryb__uyos, right_keys)
    zsen__cszy = alloc_arr_tup(hryb__uyos, data_left)
    okl__ymdbb = alloc_arr_tup(hryb__uyos, data_right)
    shjpe__xaxw = 0
    gwf__ezg = 0
    for shjpe__xaxw in range(hryb__uyos):
        if gwf__ezg < 0:
            gwf__ezg = 0
        while gwf__ezg < rdc__szsix and getitem_arr_tup(right_keys, gwf__ezg
            ) <= getitem_arr_tup(left_keys, shjpe__xaxw):
            gwf__ezg += 1
        gwf__ezg -= 1
        setitem_arr_tup(ozmtk__ghse, shjpe__xaxw, getitem_arr_tup(left_keys,
            shjpe__xaxw))
        setitem_arr_tup(zsen__cszy, shjpe__xaxw, getitem_arr_tup(data_left,
            shjpe__xaxw))
        if gwf__ezg >= 0:
            setitem_arr_tup(yvgf__zmxxe, shjpe__xaxw, getitem_arr_tup(
                right_keys, gwf__ezg))
            setitem_arr_tup(okl__ymdbb, shjpe__xaxw, getitem_arr_tup(
                data_right, gwf__ezg))
        else:
            bodo.libs.array_kernels.setna_tup(yvgf__zmxxe, shjpe__xaxw)
            bodo.libs.array_kernels.setna_tup(okl__ymdbb, shjpe__xaxw)
    return ozmtk__ghse, yvgf__zmxxe, zsen__cszy, okl__ymdbb


def copy_arr_tup(arrs):
    return tuple(a.copy() for a in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    pihus__ujecj = arrs.count
    func_text = 'def f(arrs):\n'
    func_text += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(veo__owxn) for veo__owxn in range(pihus__ujecj)))
    ygzli__mui = {}
    exec(func_text, {}, ygzli__mui)
    muqay__xkqe = ygzli__mui['f']
    return muqay__xkqe
