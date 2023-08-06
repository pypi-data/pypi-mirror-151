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
    rib__ytfc = urlparse(conn_str)
    swrk__otp = {}
    if rib__ytfc.username:
        swrk__otp['user'] = rib__ytfc.username
    if rib__ytfc.password:
        swrk__otp['password'] = rib__ytfc.password
    if rib__ytfc.hostname:
        swrk__otp['account'] = rib__ytfc.hostname
    if rib__ytfc.port:
        swrk__otp['port'] = rib__ytfc.port
    if rib__ytfc.path:
        pjm__wbuqp = rib__ytfc.path
        if pjm__wbuqp.startswith('/'):
            pjm__wbuqp = pjm__wbuqp[1:]
        xdsn__que, schema = pjm__wbuqp.split('/')
        swrk__otp['database'] = xdsn__que
        if schema:
            swrk__otp['schema'] = schema
    if rib__ytfc.query:
        for qzsjq__lra, wkv__pir in parse_qsl(rib__ytfc.query):
            swrk__otp[qzsjq__lra] = wkv__pir
            if qzsjq__lra == 'session_parameters':
                swrk__otp[qzsjq__lra] = json.loads(wkv__pir)
    swrk__otp['application'] = 'bodo'
    return swrk__otp


class SnowflakeDataset(object):

    def __init__(self, batches, schema, conn):
        self.pieces = batches
        self._bodo_total_rows = 0
        for cktr__yzgmm in batches:
            cktr__yzgmm._bodo_num_rows = cktr__yzgmm.rowcount
            self._bodo_total_rows += cktr__yzgmm._bodo_num_rows
        self.schema = schema
        self.conn = conn


def get_dataset(query, conn_str):
    qfxti__pwvtw = tracing.Event('get_snowflake_dataset')
    from mpi4py import MPI
    jcxep__fby = MPI.COMM_WORLD
    jbgze__ify = tracing.Event('snowflake_connect', is_parallel=False)
    akt__uwsu = get_connection_params(conn_str)
    conn = snowflake.connector.connect(**akt__uwsu)
    jbgze__ify.finalize()
    if bodo.get_rank() == 0:
        paccy__wlv = conn.cursor()
        slvp__bsm = tracing.Event('get_schema', is_parallel=False)
        vtkf__ctzo = f'select * from ({query}) x LIMIT {100}'
        aptln__seqqa = paccy__wlv.execute(vtkf__ctzo).fetch_arrow_all()
        if aptln__seqqa is None:
            ojhf__ugk = paccy__wlv.describe(query)
            qfhed__qbt = [pa.field(jadhs__aucmj.name, FIELD_TYPE_TO_PA_TYPE
                [jadhs__aucmj.type_code]) for jadhs__aucmj in ojhf__ugk]
            schema = pa.schema(qfhed__qbt)
        else:
            schema = aptln__seqqa.schema
        slvp__bsm.finalize()
        qep__pbaq = tracing.Event('execute_query', is_parallel=False)
        paccy__wlv.execute(query)
        qep__pbaq.finalize()
        batches = paccy__wlv.get_result_batches()
        jcxep__fby.bcast((batches, schema))
    else:
        batches, schema = jcxep__fby.bcast(None)
    rfe__uxqni = SnowflakeDataset(batches, schema, conn)
    qfxti__pwvtw.finalize()
    return rfe__uxqni
