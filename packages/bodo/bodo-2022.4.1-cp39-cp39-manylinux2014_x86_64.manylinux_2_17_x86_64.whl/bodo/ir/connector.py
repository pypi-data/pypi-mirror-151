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
    vdg__emsx = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    mkic__ynd = []
    for ofzm__tla in node.out_vars:
        typ = typemap[ofzm__tla.name]
        if typ == types.none:
            continue
        qrhoj__mfl = array_analysis._gen_shape_call(equiv_set, ofzm__tla,
            typ.ndim, None, vdg__emsx)
        equiv_set.insert_equiv(ofzm__tla, qrhoj__mfl)
        mkic__ynd.append(qrhoj__mfl[0])
        equiv_set.define(ofzm__tla, set())
    if len(mkic__ynd) > 1:
        equiv_set.insert_equiv(*mkic__ynd)
    return [], vdg__emsx


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        zwhe__eqxf = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        zwhe__eqxf = Distribution.OneD_Var
    else:
        zwhe__eqxf = Distribution.OneD
    for sqoa__xho in node.out_vars:
        if sqoa__xho.name in array_dists:
            zwhe__eqxf = Distribution(min(zwhe__eqxf.value, array_dists[
                sqoa__xho.name].value))
    for sqoa__xho in node.out_vars:
        array_dists[sqoa__xho.name] = zwhe__eqxf


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
    for ofzm__tla, typ in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(ofzm__tla.name, typ, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    cfjo__zvypc = []
    for ofzm__tla in node.out_vars:
        crf__pjrhc = visit_vars_inner(ofzm__tla, callback, cbdata)
        cfjo__zvypc.append(crf__pjrhc)
    node.out_vars = cfjo__zvypc
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for bbak__dgz in node.filters:
            for opm__ssi in range(len(bbak__dgz)):
                val = bbak__dgz[opm__ssi]
                bbak__dgz[opm__ssi] = val[0], val[1], visit_vars_inner(val[
                    2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({sqoa__xho.name for sqoa__xho in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for cwbj__dvjmt in node.filters:
            for sqoa__xho in cwbj__dvjmt:
                if isinstance(sqoa__xho[2], ir.Var):
                    use_set.add(sqoa__xho[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    bmdh__wxxp = set(sqoa__xho.name for sqoa__xho in node.out_vars)
    return set(), bmdh__wxxp


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    cfjo__zvypc = []
    for ofzm__tla in node.out_vars:
        crf__pjrhc = replace_vars_inner(ofzm__tla, var_dict)
        cfjo__zvypc.append(crf__pjrhc)
    node.out_vars = cfjo__zvypc
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for bbak__dgz in node.filters:
            for opm__ssi in range(len(bbak__dgz)):
                val = bbak__dgz[opm__ssi]
                bbak__dgz[opm__ssi] = val[0], val[1], replace_vars_inner(val
                    [2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for ofzm__tla in node.out_vars:
        vcgnt__rcvtv = definitions[ofzm__tla.name]
        if node not in vcgnt__rcvtv:
            vcgnt__rcvtv.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        cjp__qkjrq = []
        ycyt__zusw = [sqoa__xho[2] for cwbj__dvjmt in filters for sqoa__xho in
            cwbj__dvjmt]
        oyht__dassm = set()
        for pdk__dpfop in ycyt__zusw:
            if isinstance(pdk__dpfop, ir.Var):
                if pdk__dpfop.name not in oyht__dassm:
                    cjp__qkjrq.append(pdk__dpfop)
                oyht__dassm.add(pdk__dpfop.name)
        return {sqoa__xho.name: f'f{opm__ssi}' for opm__ssi, sqoa__xho in
            enumerate(cjp__qkjrq)}, cjp__qkjrq
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
    lfcs__pudg = len(used_columns)
    for opm__ssi in range(len(used_columns) - 1, -1, -1):
        if used_columns[opm__ssi] < num_columns:
            break
        lfcs__pudg = opm__ssi
    return used_columns[:lfcs__pudg]


def cast_float_to_nullable(df, df_type):
    import bodo
    xwko__cvt = {}
    for opm__ssi, douu__wikd in enumerate(df_type.data):
        if isinstance(douu__wikd, bodo.IntegerArrayType):
            rbxhy__ioop = douu__wikd.get_pandas_scalar_type_instance
            if rbxhy__ioop not in xwko__cvt:
                xwko__cvt[rbxhy__ioop] = []
            xwko__cvt[rbxhy__ioop].append(df.columns[opm__ssi])
    for typ, jyte__odbf in xwko__cvt.items():
        df[jyte__odbf] = df[jyte__odbf].astype(typ)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols):
    assert len(node.out_vars) == 2, f'invalid {nodename} node'
    yerrm__mqoel = node.out_vars[0].name
    assert isinstance(typemap[yerrm__mqoel], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, nmsg__tmm = get_live_column_nums_block(column_live_map,
            equiv_vars, yerrm__mqoel)
        used_columns = trim_extra_used_columns(used_columns, len(possible_cols)
            )
        if not nmsg__tmm and not used_columns:
            used_columns = [0]
        if not nmsg__tmm and len(used_columns) != len(node.type_usecol_offset):
            node.type_usecol_offset = used_columns
            return True
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    yud__yhfnr = False
    if array_dists is not None:
        leud__avh = node.out_vars[0].name
        yud__yhfnr = array_dists[leud__avh] in (Distribution.OneD,
            Distribution.OneD_Var)
        jqi__psw = node.out_vars[1].name
        assert typemap[jqi__psw
            ] == types.none or not yud__yhfnr or array_dists[jqi__psw] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return yud__yhfnr
