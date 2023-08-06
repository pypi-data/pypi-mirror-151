import hashlib
import inspect
import warnings
import snowflake.sqlalchemy
import sqlalchemy.types as sqltypes
from sqlalchemy import exc as sa_exc
from sqlalchemy import util as sa_util
from sqlalchemy.sql import text
_check_snowflake_sqlalchemy_change = True


def _get_schema_columns(self, connection, schema, **kw):
    kkt__jgcai = {}
    prshl__mjdde, ddbg__tqmxf = self._current_database_schema(connection, **kw)
    ljqor__orj = self._denormalize_quote_join(prshl__mjdde, schema)
    try:
        imvu__yfs = self._get_schema_primary_keys(connection, ljqor__orj, **kw)
        qlu__tmosa = connection.execute(text(
            """
        SELECT /* sqlalchemy:_get_schema_columns */
                ic.table_name,
                ic.column_name,
                ic.data_type,
                ic.character_maximum_length,
                ic.numeric_precision,
                ic.numeric_scale,
                ic.is_nullable,
                ic.column_default,
                ic.is_identity,
                ic.comment
            FROM information_schema.columns ic
            WHERE ic.table_schema=:table_schema
            ORDER BY ic.ordinal_position"""
            ), {'table_schema': self.denormalize_name(schema)})
    except sa_exc.ProgrammingError as hvie__vbtyj:
        if hvie__vbtyj.orig.errno == 90030:
            return None
        raise
    for table_name, ryor__rihb, kotht__dkfg, xzl__aqc, hzebq__znt, wxvl__unian, mwjff__qbwyb, grgi__gve, qiu__wwxiu, qyfgo__ukyt in qlu__tmosa:
        table_name = self.normalize_name(table_name)
        ryor__rihb = self.normalize_name(ryor__rihb)
        if table_name not in kkt__jgcai:
            kkt__jgcai[table_name] = list()
        if ryor__rihb.startswith('sys_clustering_column'):
            continue
        pnf__tlzjc = self.ischema_names.get(kotht__dkfg, None)
        qvkqc__kmix = {}
        if pnf__tlzjc is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(kotht__dkfg, ryor__rihb))
            pnf__tlzjc = sqltypes.NULLTYPE
        elif issubclass(pnf__tlzjc, sqltypes.FLOAT):
            qvkqc__kmix['precision'] = hzebq__znt
            qvkqc__kmix['decimal_return_scale'] = wxvl__unian
        elif issubclass(pnf__tlzjc, sqltypes.Numeric):
            qvkqc__kmix['precision'] = hzebq__znt
            qvkqc__kmix['scale'] = wxvl__unian
        elif issubclass(pnf__tlzjc, (sqltypes.String, sqltypes.BINARY)):
            qvkqc__kmix['length'] = xzl__aqc
        dwuu__uur = pnf__tlzjc if isinstance(pnf__tlzjc, sqltypes.NullType
            ) else pnf__tlzjc(**qvkqc__kmix)
        jfkao__heqdu = imvu__yfs.get(table_name)
        kkt__jgcai[table_name].append({'name': ryor__rihb, 'type':
            dwuu__uur, 'nullable': mwjff__qbwyb == 'YES', 'default':
            grgi__gve, 'autoincrement': qiu__wwxiu == 'YES', 'comment':
            qyfgo__ukyt, 'primary_key': ryor__rihb in imvu__yfs[table_name]
            ['constrained_columns'] if jfkao__heqdu else False})
    return kkt__jgcai


if _check_snowflake_sqlalchemy_change:
    lines = inspect.getsource(snowflake.sqlalchemy.snowdialect.
        SnowflakeDialect._get_schema_columns)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdf39af1ac165319d3b6074e8cf9296a090a21f0e2c05b644ff8ec0e56e2d769':
        warnings.warn(
            'snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_schema_columns has changed'
            )
snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_schema_columns = (
    _get_schema_columns)


def _get_table_columns(self, connection, table_name, schema=None, **kw):
    kkt__jgcai = []
    prshl__mjdde, ddbg__tqmxf = self._current_database_schema(connection, **kw)
    ljqor__orj = self._denormalize_quote_join(prshl__mjdde, schema)
    imvu__yfs = self._get_schema_primary_keys(connection, ljqor__orj, **kw)
    qlu__tmosa = connection.execute(text(
        """
    SELECT /* sqlalchemy:get_table_columns */
            ic.table_name,
            ic.column_name,
            ic.data_type,
            ic.character_maximum_length,
            ic.numeric_precision,
            ic.numeric_scale,
            ic.is_nullable,
            ic.column_default,
            ic.is_identity,
            ic.comment
        FROM information_schema.columns ic
        WHERE ic.table_schema=:table_schema
        AND ic.table_name=:table_name
        ORDER BY ic.ordinal_position"""
        ), {'table_schema': self.denormalize_name(schema), 'table_name':
        self.denormalize_name(table_name)})
    for table_name, ryor__rihb, kotht__dkfg, xzl__aqc, hzebq__znt, wxvl__unian, mwjff__qbwyb, grgi__gve, qiu__wwxiu, qyfgo__ukyt in qlu__tmosa:
        table_name = self.normalize_name(table_name)
        ryor__rihb = self.normalize_name(ryor__rihb)
        if ryor__rihb.startswith('sys_clustering_column'):
            continue
        pnf__tlzjc = self.ischema_names.get(kotht__dkfg, None)
        qvkqc__kmix = {}
        if pnf__tlzjc is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(kotht__dkfg, ryor__rihb))
            pnf__tlzjc = sqltypes.NULLTYPE
        elif issubclass(pnf__tlzjc, sqltypes.FLOAT):
            qvkqc__kmix['precision'] = hzebq__znt
            qvkqc__kmix['decimal_return_scale'] = wxvl__unian
        elif issubclass(pnf__tlzjc, sqltypes.Numeric):
            qvkqc__kmix['precision'] = hzebq__znt
            qvkqc__kmix['scale'] = wxvl__unian
        elif issubclass(pnf__tlzjc, (sqltypes.String, sqltypes.BINARY)):
            qvkqc__kmix['length'] = xzl__aqc
        dwuu__uur = pnf__tlzjc if isinstance(pnf__tlzjc, sqltypes.NullType
            ) else pnf__tlzjc(**qvkqc__kmix)
        jfkao__heqdu = imvu__yfs.get(table_name)
        kkt__jgcai.append({'name': ryor__rihb, 'type': dwuu__uur,
            'nullable': mwjff__qbwyb == 'YES', 'default': grgi__gve,
            'autoincrement': qiu__wwxiu == 'YES', 'comment': qyfgo__ukyt if
            qyfgo__ukyt != '' else None, 'primary_key': ryor__rihb in
            imvu__yfs[table_name]['constrained_columns'] if jfkao__heqdu else
            False})
    return kkt__jgcai


if _check_snowflake_sqlalchemy_change:
    lines = inspect.getsource(snowflake.sqlalchemy.snowdialect.
        SnowflakeDialect._get_table_columns)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9ecc8a2425c655836ade4008b1b98a8fd1819f3be43ba77b0fbbfc1f8740e2be':
        warnings.warn(
            'snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_table_columns has changed'
            )
snowflake.sqlalchemy.snowdialect.SnowflakeDialect._get_table_columns = (
    _get_table_columns)
