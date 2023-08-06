from urllib.parse import parse_qsl, urlparse
import pyarrow as pa
import snowflake.connector
import bodo
from bodo.utils import tracing
FIELD_TYPE_TO_PA_TYPE = [pa.int64(), pa.float64(), pa.string(), pa.date32(),
    pa.timestamp('ns'), pa.string(), pa.timestamp('ns'), pa.timestamp('ns'),
    pa.timestamp('ns'), pa.string(), pa.string(), pa.binary(), pa.time64(
    'ns'), pa.bool_()]


def get_connection_params(conn_str):
    import json
    zjh__mmlx = urlparse(conn_str)
    gqkw__zxm = {}
    if zjh__mmlx.username:
        gqkw__zxm['user'] = zjh__mmlx.username
    if zjh__mmlx.password:
        gqkw__zxm['password'] = zjh__mmlx.password
    if zjh__mmlx.hostname:
        gqkw__zxm['account'] = zjh__mmlx.hostname
    if zjh__mmlx.port:
        gqkw__zxm['port'] = zjh__mmlx.port
    if zjh__mmlx.path:
        vaxxg__zohwx = zjh__mmlx.path
        if vaxxg__zohwx.startswith('/'):
            vaxxg__zohwx = vaxxg__zohwx[1:]
        nmtg__mhcku, schema = vaxxg__zohwx.split('/')
        gqkw__zxm['database'] = nmtg__mhcku
        if schema:
            gqkw__zxm['schema'] = schema
    if zjh__mmlx.query:
        for lbfkt__emgu, xoy__zahe in parse_qsl(zjh__mmlx.query):
            gqkw__zxm[lbfkt__emgu] = xoy__zahe
            if lbfkt__emgu == 'session_parameters':
                gqkw__zxm[lbfkt__emgu] = json.loads(xoy__zahe)
    gqkw__zxm['application'] = 'bodo'
    return gqkw__zxm


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for xpagr__txa in batches:
            xpagr__txa._bodo_num_rows = xpagr__txa.rowcount
            self._bodo_total_rows += xpagr__txa._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    uin__lwe = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    lrr__sdm = MPI.COMM_WORLD
    cargz__huh = tracing.Event('snowflake_connect', is_parallel=False)
    snrt__mbnap = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**snrt__mbnap)
    cargz__huh.finalize()
    if bodo.get_rank() == 0:
        sim__gzsfr = conn.cursor()
        ynjb__pwn = tracing.Event('get_schema', is_parallel=False)
        uvj__eti = f'select * from ({query}) x LIMIT {100}'
        vdfiu__qvsq = sim__gzsfr.execute(uvj__eti).fetch_arrow_all()
        if vdfiu__qvsq is None:
            kuxj__jqfj = sim__gzsfr.describe(query)
            wsunp__gymsc = [pa.field(ygdx__vokh.name, FIELD_TYPE_TO_PA_TYPE
                [ygdx__vokh.type_code]) for ygdx__vokh in kuxj__jqfj]
            schema = pa.schema(wsunp__gymsc)
        else:
            schema = vdfiu__qvsq.schema
        ynjb__pwn.finalize()
        baeqw__prnx = tracing.Event('execute_query', is_parallel=False)
        sim__gzsfr.execute(query)
        baeqw__prnx.finalize()
        batches = sim__gzsfr.get_result_batches()
        lrr__sdm.bcast((batches, schema))
    else:
        batches, schema = lrr__sdm.bcast(None)
    qpclz__csonz = SnowflakeDataset(batches, schema, conn)
    uin__lwe.finalize()
    return qpclz__csonz
