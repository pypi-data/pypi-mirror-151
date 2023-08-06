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
    recdb__gcnhq = urlparse(con_str)
    db_type = recdb__gcnhq.scheme
    yvn__qyx = recdb__gcnhq.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', yvn__qyx
    if db_type == 'mysql+pymysql':
        return 'mysql', yvn__qyx
    return db_type, yvn__qyx


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    xdf__bis = sql_node.out_vars[0].name
    drefk__lnl = sql_node.out_vars[1].name
    if xdf__bis not in lives and drefk__lnl not in lives:
        return None
    elif xdf__bis not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.type_usecol_offset = []
    elif drefk__lnl not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    return sql_node


def sql_distributed_run(sql_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        dkn__fwbt = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        vbgr__yhzbt = []
        rtnps__fgi = []
        for pqpgq__cfp in sql_node.type_usecol_offset:
            pgsf__fawtr = sql_node.df_colnames[pqpgq__cfp]
            vbgr__yhzbt.append(pgsf__fawtr)
            if isinstance(sql_node.out_types[pqpgq__cfp], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                rtnps__fgi.append(pgsf__fawtr)
        if sql_node.index_column_name:
            vbgr__yhzbt.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                rtnps__fgi.append(sql_node.index_column_name)
        nlbfx__fytoj = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', dkn__fwbt,
            nlbfx__fytoj, vbgr__yhzbt)
        if rtnps__fgi:
            lcyb__hupu = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', lcyb__hupu,
                nlbfx__fytoj, rtnps__fgi)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        lbues__eepi = set(sql_node.unsupported_columns)
        lvdx__negsz = set(sql_node.type_usecol_offset)
        ixga__blbx = lvdx__negsz & lbues__eepi
        if ixga__blbx:
            azf__vqql = sorted(ixga__blbx)
            xhbg__idr = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            bjkv__ksdfk = 0
            for ygqwc__von in azf__vqql:
                while sql_node.unsupported_columns[bjkv__ksdfk] != ygqwc__von:
                    bjkv__ksdfk += 1
                xhbg__idr.append(
                    f"Column '{sql_node.original_df_colnames[ygqwc__von]}' with unsupported arrow type {sql_node.unsupported_arrow_types[bjkv__ksdfk]}"
                    )
                bjkv__ksdfk += 1
            sbach__newt = '\n'.join(xhbg__idr)
            raise BodoError(sbach__newt, loc=sql_node.loc)
    mzhum__euroa, aeo__hxrf = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    csi__uzn = ', '.join(mzhum__euroa.values())
    drue__fqh = f'def sql_impl(sql_request, conn, {csi__uzn}):\n'
    if sql_node.filters:
        ciaa__kfjzv = []
        for znm__eczxk in sql_node.filters:
            uvywy__vyyb = [' '.join(['(', vffrz__ryx[0], vffrz__ryx[1], '{' +
                mzhum__euroa[vffrz__ryx[2].name] + '}' if isinstance(
                vffrz__ryx[2], ir.Var) else vffrz__ryx[2], ')']) for
                vffrz__ryx in znm__eczxk]
            ciaa__kfjzv.append(' ( ' + ' AND '.join(uvywy__vyyb) + ' ) ')
        wladw__lsiph = ' WHERE ' + ' OR '.join(ciaa__kfjzv)
        for pqpgq__cfp, elnf__bofe in enumerate(mzhum__euroa.values()):
            drue__fqh += f'    {elnf__bofe} = get_sql_literal({elnf__bofe})\n'
        drue__fqh += f'    sql_request = f"{{sql_request}} {wladw__lsiph}"\n'
    drue__fqh += (
        '    (table_var, index_var) = _sql_reader_py(sql_request, conn)\n')
    hxp__hzex = {}
    exec(drue__fqh, {}, hxp__hzex)
    qtr__oywxl = hxp__hzex['sql_impl']
    pxnb__fyzo = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.type_usecol_offset, typingctx, targetctx, sql_node.db_type,
        sql_node.limit, parallel, sql_node.is_select_query)
    qedmc__jueyr = compile_to_numba_ir(qtr__oywxl, {'_sql_reader_py':
        pxnb__fyzo, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type) + tuple(
        typemap[soj__fehc.name] for soj__fehc in aeo__hxrf), typemap=
        typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query:
        ott__vbtm = [sql_node.df_colnames[pqpgq__cfp] for pqpgq__cfp in
            sql_node.type_usecol_offset]
        if sql_node.index_column_name:
            ott__vbtm.append(sql_node.index_column_name)
        ljs__kug = escape_column_names(ott__vbtm, sql_node.db_type,
            sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            wve__otphh = ('SELECT ' + ljs__kug + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            wve__otphh = ('SELECT ' + ljs__kug + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        wve__otphh = sql_node.sql_request
    replace_arg_nodes(qedmc__jueyr, [ir.Const(wve__otphh, sql_node.loc), ir
        .Const(sql_node.connection, sql_node.loc)] + aeo__hxrf)
    epn__yydq = qedmc__jueyr.body[:-3]
    epn__yydq[-2].target = sql_node.out_vars[0]
    epn__yydq[-1].target = sql_node.out_vars[1]
    assert not (sql_node.index_column_name is None and not sql_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the SQL IR node is live'
    if sql_node.index_column_name is None:
        epn__yydq.pop(-1)
    elif not sql_node.type_usecol_offset:
        epn__yydq.pop(-2)
    return epn__yydq


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type in ('snowflake', 'oracle'):
        ott__vbtm = [(nukvz__dhv.upper() if nukvz__dhv in
            converted_colnames else nukvz__dhv) for nukvz__dhv in col_names]
        ljs__kug = ', '.join([f'"{nukvz__dhv}"' for nukvz__dhv in ott__vbtm])
    elif db_type == 'mysql':
        ljs__kug = ', '.join([f'`{nukvz__dhv}`' for nukvz__dhv in col_names])
    else:
        ljs__kug = ', '.join([f'"{nukvz__dhv}"' for nukvz__dhv in col_names])
    return ljs__kug


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    kawey__dnj = types.unliteral(filter_value)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(kawey__dnj,
        'Filter pushdown')
    if kawey__dnj == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(kawey__dnj, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif kawey__dnj == bodo.pd_timestamp_type:

        def impl(filter_value):
            nqiqg__ptcy = filter_value.nanosecond
            ajwbe__whw = ''
            if nqiqg__ptcy < 10:
                ajwbe__whw = '00'
            elif nqiqg__ptcy < 100:
                ajwbe__whw = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{ajwbe__whw}{nqiqg__ptcy}'"
                )
        return impl
    elif kawey__dnj == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {kawey__dnj} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float
    vjn__nty = (bodo.datetime_date_type, bodo.pd_timestamp_type, types.
        unicode_type, types.bool_)
    kawey__dnj = types.unliteral(filter_value)
    if isinstance(kawey__dnj, types.List) and (isinstance(kawey__dnj.dtype,
        scalar_isinstance) or kawey__dnj.dtype in vjn__nty):

        def impl(filter_value):
            nmncx__nlp = ', '.join([_get_snowflake_sql_literal_scalar(
                nukvz__dhv) for nukvz__dhv in filter_value])
            return f'({nmncx__nlp})'
        return impl
    elif isinstance(kawey__dnj, scalar_isinstance) or kawey__dnj in vjn__nty:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {kawey__dnj} used in filter pushdown.'
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
    except ImportError as ubbpw__phruo:
        vhtr__wfd = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(vhtr__wfd)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as ubbpw__phruo:
        vhtr__wfd = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(vhtr__wfd)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as ubbpw__phruo:
        vhtr__wfd = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(vhtr__wfd)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as ubbpw__phruo:
        vhtr__wfd = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(vhtr__wfd)


def req_limit(sql_request):
    import re
    ftyi__evdei = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    rkc__snt = ftyi__evdei.search(sql_request)
    if rkc__snt:
        return int(rkc__snt.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names, col_typs, index_column_name,
    index_column_type, type_usecol_offset, typingctx, targetctx, db_type,
    limit, parallel, is_select_query):
    jzrf__gpr = next_label()
    ott__vbtm = [col_names[pqpgq__cfp] for pqpgq__cfp in type_usecol_offset]
    ooig__bfj = [col_typs[pqpgq__cfp] for pqpgq__cfp in type_usecol_offset]
    if index_column_name:
        ott__vbtm.append(index_column_name)
        ooig__bfj.append(index_column_type)
    ktrw__igoab = None
    hmm__vdbv = None
    witbd__pkgku = types.none
    if type_usecol_offset:
        witbd__pkgku = TableType(tuple(col_typs))
    drue__fqh = 'def sql_reader_py(sql_request, conn):\n'
    if db_type == 'snowflake':
        drue__fqh += (
            f"  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})\n")

        def is_nullable(typ):
            return bodo.utils.utils.is_array_typ(typ, False
                ) and not isinstance(typ, types.Array) and not isinstance(typ,
                bodo.DatetimeArrayType)
        nzkqn__gcmqx = [int(is_nullable(col_typs[pqpgq__cfp])) for
            pqpgq__cfp in type_usecol_offset]
        if index_column_name:
            nzkqn__gcmqx.append(int(is_nullable(index_column_type)))
        drue__fqh += f"""  out_table = snowflake_read(unicode_to_utf8(sql_request), unicode_to_utf8(conn), {parallel}, {len(nzkqn__gcmqx)}, np.array({nzkqn__gcmqx}, dtype=np.int32).ctypes)
"""
        drue__fqh += '  check_and_propagate_cpp_exception()\n'
        if index_column_name:
            drue__fqh += f"""  index_var = info_to_array(info_from_table(out_table, {len(type_usecol_offset)}), index_col_typ)
"""
        else:
            drue__fqh += '  index_var = None\n'
        if type_usecol_offset:
            bjkv__ksdfk = []
            rrj__gzn = 0
            for pqpgq__cfp in range(len(col_names)):
                if rrj__gzn < len(type_usecol_offset
                    ) and pqpgq__cfp == type_usecol_offset[rrj__gzn]:
                    bjkv__ksdfk.append(rrj__gzn)
                    rrj__gzn += 1
                else:
                    bjkv__ksdfk.append(-1)
            ktrw__igoab = np.array(bjkv__ksdfk, dtype=np.int64)
            drue__fqh += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{jzrf__gpr}, py_table_type_{jzrf__gpr})
"""
        else:
            drue__fqh += '  table_var = None\n'
        drue__fqh += '  delete_table(out_table)\n'
        drue__fqh += f'  ev.finalize()\n'
    else:
        if type_usecol_offset:
            drue__fqh += f"""  type_usecols_offsets_arr_{jzrf__gpr}_2 = type_usecols_offsets_arr_{jzrf__gpr}
"""
            hmm__vdbv = np.array(type_usecol_offset, dtype=np.int64)
        drue__fqh += '  df_typeref_2 = df_typeref\n'
        drue__fqh += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            drue__fqh += '  pymysql_check()\n'
        elif db_type == 'oracle':
            drue__fqh += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            drue__fqh += '  psycopg2_check()\n'
        if parallel and is_select_query:
            drue__fqh += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                drue__fqh += f'  nb_row = {limit}\n'
            else:
                drue__fqh += '  with objmode(nb_row="int64"):\n'
                drue__fqh += f'     if rank == {MPI_ROOT}:\n'
                drue__fqh += (
                    "         sql_cons = 'select count(*) from (' + sql_request + ') x'\n"
                    )
                drue__fqh += '         frame = pd.read_sql(sql_cons, conn)\n'
                drue__fqh += '         nb_row = frame.iat[0,0]\n'
                drue__fqh += '     else:\n'
                drue__fqh += '         nb_row = 0\n'
                drue__fqh += '  nb_row = bcast_scalar(nb_row)\n'
            drue__fqh += f"""  with objmode(table_var=py_table_type_{jzrf__gpr}, index_var=index_col_typ):
"""
            drue__fqh += (
                '    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)\n'
                )
            if db_type == 'oracle':
                drue__fqh += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                drue__fqh += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            drue__fqh += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            drue__fqh += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            drue__fqh += f"""  with objmode(table_var=py_table_type_{jzrf__gpr}, index_var=index_col_typ):
"""
            drue__fqh += '    df_ret = pd.read_sql(sql_request, conn)\n'
            drue__fqh += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            drue__fqh += (
                f'    index_var = df_ret.iloc[:, {len(type_usecol_offset)}].values\n'
                )
            drue__fqh += f"""    df_ret.drop(columns=df_ret.columns[{len(type_usecol_offset)}], inplace=True)
"""
        else:
            drue__fqh += '    index_var = None\n'
        if type_usecol_offset:
            drue__fqh += f'    arrs = []\n'
            drue__fqh += f'    for i in range(df_ret.shape[1]):\n'
            drue__fqh += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            drue__fqh += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{jzrf__gpr}_2, {len(col_names)})
"""
        else:
            drue__fqh += '    table_var = None\n'
    drue__fqh += '  return (table_var, index_var)\n'
    isd__ecpwv = globals()
    isd__ecpwv.update({'bodo': bodo, f'py_table_type_{jzrf__gpr}':
        witbd__pkgku, 'index_col_typ': index_column_type})
    if db_type == 'snowflake':
        isd__ecpwv.update({'np': np, 'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'snowflake_read':
            _snowflake_read, 'info_to_array': info_to_array,
            'info_from_table': info_from_table, 'delete_table':
            delete_table, 'cpp_table_to_py_table': cpp_table_to_py_table,
            f'table_idx_{jzrf__gpr}': ktrw__igoab})
    else:
        isd__ecpwv.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(ooig__bfj), bodo.RangeIndexType(None),
            tuple(ott__vbtm)), 'Table': Table,
            f'type_usecols_offsets_arr_{jzrf__gpr}': hmm__vdbv})
    hxp__hzex = {}
    exec(drue__fqh, isd__ecpwv, hxp__hzex)
    pxnb__fyzo = hxp__hzex['sql_reader_py']
    pditl__emyb = numba.njit(pxnb__fyzo)
    compiled_funcs.append(pditl__emyb)
    return pditl__emyb


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.int64, types.voidptr))
import llvmlite.binding as ll
from bodo.io import arrow_cpp
ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
