"""
Common IR extension functions for connectors such as CSV, Parquet and JSON readers.
"""
from collections import defaultdict
import numba
from numba.core import ir, types
from numba.core.ir_utils import replace_vars_inner, visit_vars_inner
from numba.extending import box, models, register_model
from bodo.hiframes.table import TableType
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import get_live_column_nums_block
from bodo.utils.utils import debug_prints


def connector_array_analysis(node, equiv_set, typemap, array_analysis):
    abv__vstd = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    fkom__hbc = []
    for lpq__zpud in node.out_vars:
        typ = typemap[lpq__zpud.name]
        if typ == types.none:
            continue
        yjs__kfw = array_analysis._gen_shape_call(equiv_set, lpq__zpud, typ
            .ndim, None, abv__vstd)
        equiv_set.insert_equiv(lpq__zpud, yjs__kfw)
        fkom__hbc.append(yjs__kfw[0])
        equiv_set.define(lpq__zpud, set())
    if len(fkom__hbc) > 1:
        equiv_set.insert_equiv(*fkom__hbc)
    return [], abv__vstd


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        lffq__zte = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        lffq__zte = Distribution.OneD_Var
    else:
        lffq__zte = Distribution.OneD
    for joia__jxbl in node.out_vars:
        if joia__jxbl.name in array_dists:
            lffq__zte = Distribution(min(lffq__zte.value, array_dists[
                joia__jxbl.name].value))
    for joia__jxbl in node.out_vars:
        array_dists[joia__jxbl.name] = lffq__zte


def connector_typeinfer(node, typeinferer):
    if node.connector_typ == 'csv':
        if node.chunksize is not None:
            typeinferer.lock_type(node.out_vars[0].name, node.out_types[0],
                loc=node.loc)
        else:
            typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(
                node.out_types)), loc=node.loc)
            typeinferer.lock_type(node.out_vars[1].name, node.
                index_column_typ, loc=node.loc)
        return
    if node.connector_typ in ('parquet', 'sql'):
        typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(node.
            out_types)), loc=node.loc)
        typeinferer.lock_type(node.out_vars[1].name, node.index_column_type,
            loc=node.loc)
        return
    for lpq__zpud, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(lpq__zpud.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    wig__cjztn = []
    for lpq__zpud in node.out_vars:
        xsxqs__ayy = visit_vars_inner(lpq__zpud, callback, cbdata)
        wig__cjztn.append(xsxqs__ayy)
    node.out_vars = wig__cjztn
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for hnp__xvvzu in node.filters:
            for odu__ewegc in range(len(hnp__xvvzu)):
                val = hnp__xvvzu[odu__ewegc]
                hnp__xvvzu[odu__ewegc] = val[0], val[1], visit_vars_inner(val
                    [2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({joia__jxbl.name for joia__jxbl in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for ygu__qfq in node.filters:
            for joia__jxbl in ygu__qfq:
                if isinstance(joia__jxbl[2], ir.Var):
                    use_set.add(joia__jxbl[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    fifw__vaox = set(joia__jxbl.name for joia__jxbl in node.out_vars)
    return set(), fifw__vaox


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    wig__cjztn = []
    for lpq__zpud in node.out_vars:
        xsxqs__ayy = replace_vars_inner(lpq__zpud, var_dict)
        wig__cjztn.append(xsxqs__ayy)
    node.out_vars = wig__cjztn
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for hnp__xvvzu in node.filters:
            for odu__ewegc in range(len(hnp__xvvzu)):
                val = hnp__xvvzu[odu__ewegc]
                hnp__xvvzu[odu__ewegc] = val[0], val[1], replace_vars_inner(val
                    [2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for lpq__zpud in node.out_vars:
        vup__xpjl = definitions[lpq__zpud.name]
        if node not in vup__xpjl:
            vup__xpjl.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        ugm__fen = []
        bvhr__gayr = [joia__jxbl[2] for ygu__qfq in filters for joia__jxbl in
            ygu__qfq]
        rxbp__oqcgr = set()
        for cmmjg__rujr in bvhr__gayr:
            if isinstance(cmmjg__rujr, ir.Var):
                if cmmjg__rujr.name not in rxbp__oqcgr:
                    ugm__fen.append(cmmjg__rujr)
                rxbp__oqcgr.add(cmmjg__rujr.name)
        return {joia__jxbl.name: f'f{odu__ewegc}' for odu__ewegc,
            joia__jxbl in enumerate(ugm__fen)}, ugm__fen
    else:
        return {}, []


class StreamReaderType(types.Opaque):

    def __init__(self):
        super(StreamReaderType, self).__init__(name='StreamReaderType')


stream_reader_type = StreamReaderType()
register_model(StreamReaderType)(models.OpaqueModel)


@box(StreamReaderType)
def box_stream_reader(typ, val, c):
    c.pyapi.incref(val)
    return val


def trim_extra_used_columns(used_columns, num_columns):
    gfmu__qld = len(used_columns)
    for odu__ewegc in range(len(used_columns) - 1, -1, -1):
        if used_columns[odu__ewegc] < num_columns:
            break
        gfmu__qld = odu__ewegc
    return used_columns[:gfmu__qld]


def cast_float_to_nullable(df, df_type):
    import bodo
    rpw__uju = {}
    for odu__ewegc, tidp__rkdgx in enumerate(df_type.data):
        if isinstance(tidp__rkdgx, bodo.IntegerArrayType):
            bktw__ltv = tidp__rkdgx.get_pandas_scalar_type_instance
            if bktw__ltv not in rpw__uju:
                rpw__uju[bktw__ltv] = []
            rpw__uju[bktw__ltv].append(df.columns[odu__ewegc])
    for typ, zzsj__cdwm in rpw__uju.items():
        df[zzsj__cdwm] = df[zzsj__cdwm].astype(typ)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    sqffq__xhlma = node.out_vars[0].name
    assert isinstance(typemap[sqffq__xhlma], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, ugm__eyozu = get_live_column_nums_block(column_live_map,
            equiv_vars, sqffq__xhlma)
        used_columns = trim_extra_used_columns(used_columns, len(possible_cols)
            )
        if not ugm__eyozu and not used_columns:
            used_columns = [0]
        if not ugm__eyozu and len(used_columns) != len(node.type_usecol_offset
            ):
            node.type_usecol_offset = used_columns
            return True
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    rak__bllw = False
    if array_dists is not None:
        bztq__fbrk = node.out_vars[0].name
        rak__bllw = array_dists[bztq__fbrk] in (Distribution.OneD,
            Distribution.OneD_Var)
        wmqp__sny = node.out_vars[1].name
        assert typemap[wmqp__sny
            ] == types.none or not rak__bllw or array_dists[wmqp__sny] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return rak__bllw
