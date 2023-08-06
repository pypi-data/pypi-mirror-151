"""
Implementation of pd.read_sql in BODO.
We piggyback on the pandas implementation. Future plan is to have a faster
version for this task.
"""
from urllib.parse import urlparse
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.table import Table, TableType
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.distributed_api import bcast, bcast_scalar
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_and_propagate_cpp_exception
MPI_ROOT = 0


class SqlReader(ir.Stmt):

    def __init__(self, sql_request, connection, df_out, df_colnames,
        out_vars, out_types, converted_colnames, db_type, loc,
        unsupported_columns, unsupported_arrow_types, is_select_query,
        index_column_name, index_column_type):
        self.connector_typ = 'sql'
        self.sql_request = sql_request
        self.connection = connection
        self.df_out = df_out
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.converted_colnames = converted_colnames
        self.loc = loc
        self.limit = req_limit(sql_request)
        self.db_type = db_type
        self.filters = None
        self.unsupported_columns = unsupported_columns
        self.unsupported_arrow_types = unsupported_arrow_types
        self.is_select_query = is_select_query
        self.index_column_name = index_column_name
        self.index_column_type = index_column_type
        self.type_usecol_offset = list(range(len(df_colnames)))

    def __repr__(self):
        return (
            f'{self.df_out} = ReadSql(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, vars={self.out_vars}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, type_usecol_offset={self.type_usecol_offset},)'
            )


def parse_dbtype(con_str):
    vike__ufsb = urlparse(con_str)
    db_type = vike__ufsb.scheme
    ixl__ynx = vike__ufsb.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', ixl__ynx
    if db_type == 'mysql+pymysql':
        return 'mysql', ixl__ynx
    return db_type, ixl__ynx


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    esks__ewmro = sql_node.out_vars[0].name
    xtb__lyqm = sql_node.out_vars[1].name
    if esks__ewmro not in lives and xtb__lyqm not in lives:
        return None
    elif esks__ewmro not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.type_usecol_offset = []
    elif xtb__lyqm not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        xrf__cajlg = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        zyil__xbdju = []
        gmvdc__csis = []
        for dgge__dunu in sql_node.type_usecol_offset:
            akyx__xseqt = sql_node.df_colnames[dgge__dunu]
            zyil__xbdju.append(akyx__xseqt)
            if isinstance(sql_node.out_types[dgge__dunu], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                gmvdc__csis.append(akyx__xseqt)
        if sql_node.index_column_name:
            zyil__xbdju.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                gmvdc__csis.append(sql_node.index_column_name)
        oar__mec = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', xrf__cajlg,
            oar__mec, zyil__xbdju)
        if gmvdc__csis:
            tgzg__lvwur = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                tgzg__lvwur, oar__mec, gmvdc__csis)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        ghor__lbo = set(sql_node.unsupported_columns)
        sxut__ezcyg = set(sql_node.type_usecol_offset)
        joas__yrszd = sxut__ezcyg & ghor__lbo
        if joas__yrszd:
            kyk__llq = sorted(joas__yrszd)
            djhcl__mpgpu = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            ufqi__djpuo = 0
            for mhgj__ceshk in kyk__llq:
                while sql_node.unsupported_columns[ufqi__djpuo] != mhgj__ceshk:
                    ufqi__djpuo += 1
                djhcl__mpgpu.append(
                    f"Column '{sql_node.original_df_colnames[mhgj__ceshk]}' with unsupported arrow type {sql_node.unsupported_arrow_types[ufqi__djpuo]}"
                    )
                ufqi__djpuo += 1
            debzf__gzsjw = '\n'.join(djhcl__mpgpu)
            raise BodoError(debzf__gzsjw, loc=sql_node.loc)
    fcs__kmyyd, zbikw__luuko = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    iztu__exle = ', '.join(fcs__kmyyd.values())
    wgmbl__tezc = f'def sql_impl(sql_request, conn, {iztu__exle}):\n'
    if sql_node.filters:
        nsfja__jhdb = []
        for xhxvb__wztcc in sql_node.filters:
            qow__ibv = [' '.join(['(', jqiu__spry[0], jqiu__spry[1], '{' +
                fcs__kmyyd[jqiu__spry[2].name] + '}' if isinstance(
                jqiu__spry[2], ir.Var) else jqiu__spry[2], ')']) for
                jqiu__spry in xhxvb__wztcc]
            nsfja__jhdb.append(' ( ' + ' AND '.join(qow__ibv) + ' ) ')
        nmjx__zvvf = ' WHERE ' + ' OR '.join(nsfja__jhdb)
        for dgge__dunu, wjpq__okcd in enumerate(fcs__kmyyd.values()):
            wgmbl__tezc += (
                f'    {wjpq__okcd} = get_sql_literal({wjpq__okcd})\n')
        wgmbl__tezc += f'    sql_request = f"{{sql_request}} {nmjx__zvvf}"\n'
    wgmbl__tezc += (
        '    (table_var, index_var) = _sql_reader_py(sql_request, conn)\n')
    kto__aedy = {}
    exec(wgmbl__tezc, {}, kto__aedy)
    ajgfs__ribi = kto__aedy['sql_impl']
    rak__sgnp = _gen_sql_reader_py(sql_node.df_colnames, sql_node.out_types,
        sql_node.index_column_name, sql_node.index_column_type, sql_node.
        type_usecol_offset, typingctx, targetctx, sql_node.db_type,
        sql_node.limit, parallel, sql_node.is_select_query)
    jxhn__owez = compile_to_numba_ir(ajgfs__ribi, {'_sql_reader_py':
        rak__sgnp, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type) + tuple(
        typemap[mvbo__dunuz.name] for mvbo__dunuz in zbikw__luuko), typemap
        =typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query:
        nbh__sxasa = [sql_node.df_colnames[dgge__dunu] for dgge__dunu in
            sql_node.type_usecol_offset]
        if sql_node.index_column_name:
            nbh__sxasa.append(sql_node.index_column_name)
        wfna__hijk = escape_column_names(nbh__sxasa, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            cxr__kosfx = ('SELECT ' + wfna__hijk + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            cxr__kosfx = ('SELECT ' + wfna__hijk + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        cxr__kosfx = sql_node.sql_request
    replace_arg_nodes(jxhn__owez, [ir.Const(cxr__kosfx, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc)] + zbikw__luuko)
    rbeh__fbdhy = jxhn__owez.body[:-3]
    rbeh__fbdhy[-2].target = sql_node.out_vars[0]
    rbeh__fbdhy[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        rbeh__fbdhy.pop(-1)
    elif not sql_node.type_usecol_offset:
        rbeh__fbdhy.pop(-2)
    return rbeh__fbdhy


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        nbh__sxasa = [(ccyx__luxz.upper() if ccyx__luxz in
            converted_colnames else ccyx__luxz) for ccyx__luxz in col_names]
        wfna__hijk = ', '.join([f'"{ccyx__luxz}"' for ccyx__luxz in nbh__sxasa]
            )
    elif db_type == 'mysql':
        wfna__hijk = ', '.join([f'`{ccyx__luxz}`' for ccyx__luxz in col_names])
    else:
        wfna__hijk = ', '.join([f'"{ccyx__luxz}"' for ccyx__luxz in col_names])
    return wfna__hijk


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    uiyh__rdsa = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(uiyh__rdsa,
        'Filter pushdown')
    if uiyh__rdsa == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(uiyh__rdsa, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif uiyh__rdsa == bodo.pd_timestamp_type:

        def impl(filter_value):
            fgtf__kwexw = filter_value.nanosecond
            dxbw__mqv = ''
            if fgtf__kwexw < 10:
                dxbw__mqv = '00'
            elif fgtf__kwexw < 100:
                dxbw__mqv = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{dxbw__mqv}{fgtf__kwexw}'"
                )
        return impl
    elif uiyh__rdsa == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {uiyh__rdsa} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    pegnq__loa = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    uiyh__rdsa = types.unliteral(filter_value)
    if isinstance(uiyh__rdsa, types.List) and (isinstance(uiyh__rdsa.dtype,
        scalar_isinstance) or uiyh__rdsa.dtype in pegnq__loa):

        def impl(filter_value):
            auss__wbjma = ', '.join([_get_snowflake_sql_literal_scalar(
                ccyx__luxz) for ccyx__luxz in filter_value])
            return f'({auss__wbjma})'
        return impl
    elif isinstance(uiyh__rdsa, scalar_isinstance) or uiyh__rdsa in pegnq__loa:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {uiyh__rdsa} used in filter pushdown.'
            )


def sql_remove_dead_column(sql_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(sql_node,
        column_live_map, equiv_vars, typemap, 'SQLReader', sql_node.df_colnames
        )


numba.parfors.array_analysis.array_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[SqlReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[SqlReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[SqlReader] = remove_dead_sql
numba.core.analysis.ir_extension_usedefs[SqlReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[SqlReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[SqlReader] = sql_distributed_run
remove_dead_column_extensions[SqlReader] = sql_remove_dead_column
ir_extension_table_column_use[SqlReader
    ] = bodo.ir.connector.connector_table_column_use
compiled_funcs = []


@numba.njit
def sqlalchemy_check():
    with numba.objmode():
        sqlalchemy_check_()


def sqlalchemy_check_():
    try:
        import sqlalchemy
    except ImportError as ossj__spbm:
        rxj__qiul = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(rxj__qiul)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as ossj__spbm:
        rxj__qiul = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(rxj__qiul)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as ossj__spbm:
        rxj__qiul = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(rxj__qiul)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as ossj__spbm:
        rxj__qiul = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(rxj__qiul)


def req_limit(sql_request):
    import re
    tgt__bhl = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    nnfja__kxplt = tgt__bhl.search(sql_request)
    if nnfja__kxplt:
        return int(nnfja__kxplt.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, index_column_name,
    index_column_type, type_usecol_offset, typingctx, targetctx, db_type,
    limit, parallel, is_select_query):
    rujk__eadj = next_label()
    nbh__sxasa = [col_names[dgge__dunu] for dgge__dunu in type_usecol_offset]
    lshj__yrlq = [col_typs[dgge__dunu] for dgge__dunu in type_usecol_offset]
    if index_column_name:
        nbh__sxasa.append(index_column_name)
        lshj__yrlq.append(index_column_type)
    abzr__ddog = None
    bgnca__mbq = None
    zpavz__trcqe = types.none
    if type_usecol_offset:
        zpavz__trcqe = TableType(tuple(col_typs))
    wgmbl__tezc = 'def sql_reader_py(sql_request, conn):\n'
    if db_type == 'snowflake':
        wgmbl__tezc += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")

        def is_nullable(typ):
            return bodo.utils.utils.is_array_typ(typ, False
                ) and not isinstance(typ, types.Array) and not isinstance(typ,
                bodo.DatetimeArrayType)
        jmwt__shyub = [int(is_nullable(col_typs[dgge__dunu])) for
            dgge__dunu in type_usecol_offset]
        if index_column_name:
            jmwt__shyub.append(int(is_nullable(index_column_type)))
        wgmbl__tezc += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(jmwt__shyub)}, np.array({jmwt__shyub}, dtype=np.int32).ctypes)
"""
        wgmbl__tezc += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            wgmbl__tezc += f"""  index_var = info_to_array(info_from_table(out_table, {len(type_usecol_offset)}), index_col_typ)
"""
        else:
            wgmbl__tezc += '  index_var = None\n'
        if type_usecol_offset:
            ufqi__djpuo = []
            oox__ynfc = 0
            for dgge__dunu in range(len(col_names)):
                if oox__ynfc < len(type_usecol_offset
                    ) and dgge__dunu == type_usecol_offset[oox__ynfc]:
                    ufqi__djpuo.append(oox__ynfc)
                    oox__ynfc += 1
                else:
                    ufqi__djpuo.append(-1)
            abzr__ddog = np.array(ufqi__djpuo, dtype=np.int64)
            wgmbl__tezc += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{rujk__eadj}, py_table_type_{rujk__eadj})
"""
        else:
            wgmbl__tezc += '  table_var = None\n'
        wgmbl__tezc += '  delete_table(out_table)\n'
        wgmbl__tezc += f'  ev.finalize()\n'
    else:
        if type_usecol_offset:
            wgmbl__tezc += f"""  type_usecols_offsets_arr_{rujk__eadj}_2 = type_usecols_offsets_arr_{rujk__eadj}
"""
            bgnca__mbq = np.array(type_usecol_offset, dtype=np.int64)
        wgmbl__tezc += '  df_typeref_2 = df_typeref\n'
        wgmbl__tezc += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            wgmbl__tezc += '  pymysql_check()\n'
        elif db_type == 'oracle':
            wgmbl__tezc += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            wgmbl__tezc += '  psycopg2_check()\n'
        if parallel and is_select_query:
            wgmbl__tezc += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                wgmbl__tezc += f'  nb_row = {limit}\n'
            else:
                wgmbl__tezc += '  with objmode(nb_row="int64"):\n'
                wgmbl__tezc += f'     if rank == {MPI_ROOT}:\n'
                wgmbl__tezc += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                wgmbl__tezc += '         frame = pd.read_sql(sql_cons, conn)\n'
                wgmbl__tezc += '         nb_row = frame.iat[0,0]\n'
                wgmbl__tezc += '     else:\n'
                wgmbl__tezc += '         nb_row = 0\n'
                wgmbl__tezc += '  nb_row = bcast_scalar(nb_row)\n'
            wgmbl__tezc += f"""  with objmode(table_var=py_table_type_{rujk__eadj}, index_var=index_col_typ):
"""
            wgmbl__tezc += """    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)
"""
            if db_type == 'oracle':
                wgmbl__tezc += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                wgmbl__tezc += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            wgmbl__tezc += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            wgmbl__tezc += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            wgmbl__tezc += f"""  with objmode(table_var=py_table_type_{rujk__eadj}, index_var=index_col_typ):
"""
            wgmbl__tezc += '    df_ret = pd.read_sql(sql_request, conn)\n'
            wgmbl__tezc += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            wgmbl__tezc += (
                f'    index_var = df_ret.iloc[:, {len(type_usecol_offset)}].values\n'
                )
            wgmbl__tezc += f"""    df_ret.drop(columns=df_ret.columns[{len(type_usecol_offset)}], inplace=True)
"""
        else:
            wgmbl__tezc += '    index_var = None\n'
        if type_usecol_offset:
            wgmbl__tezc += f'    arrs = []\n'
            wgmbl__tezc += f'    for i in range(df_ret.shape[1]):\n'
            wgmbl__tezc += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            wgmbl__tezc += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{rujk__eadj}_2, {len(col_names)})
"""
        else:
            wgmbl__tezc += '    table_var = None\n'
    wgmbl__tezc += '  return (table_var, index_var)\n'
    nideq__rbqji = globals()
    nideq__rbqji.update({'bodo': bodo, f'py_table_type_{rujk__eadj}':
        zpavz__trcqe, 'index_col_typ': index_column_type})
    if db_type == 'snowflake':
        nideq__rbqji.update({'np': np, 'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'snowflake_read':
            _snowflake_read, 'info_to_array': info_to_array,
            'info_from_table': info_from_table, 'delete_table':
            delete_table, 'cpp_table_to_py_table': cpp_table_to_py_table,
            f'table_idx_{rujk__eadj}': abzr__ddog})
    else:
        nideq__rbqji.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(lshj__yrlq), bodo.RangeIndexType(None),
            tuple(nbh__sxasa)), 'Table': Table,
            f'type_usecols_offsets_arr_{rujk__eadj}': bgnca__mbq})
    kto__aedy = {}
    exec(wgmbl__tezc, nideq__rbqji, kto__aedy)
    rak__sgnp = kto__aedy['sql_reader_py']
    rumj__bghkq = numba.njit(rak__sgnp)
    compiled_funcs.append(rumj__bghkq)
    return rumj__bghkq


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.int64, types.voidptr))
import llvmlite.binding as ll
from bodo.io import arrow_cpp
ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
