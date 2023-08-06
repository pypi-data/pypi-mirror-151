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
    bppjf__tgfj = {}
    jhvwi__ogz, rvx__jfwo = self._current_database_schema(connection, **kw)
    zhje__mdens = self._denormalize_quote_join(jhvwi__ogz, schema)
    try:
        bhdo__gxhyx = self._get_schema_primary_keys(connection, zhje__mdens,
            **kw)
        nga__sys = connection.execute(text(
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
    except sa_exc.ProgrammingError as fhe__rbtay:
        if fhe__rbtay.orig.errno == 90030:
            return None
        raise
    for table_name, lyib__yrdy, dikd__tdo, koq__grse, zzu__ppg, jxpkw__ohvlq, mykxh__hfi, ptvfx__faya, aha__huitz, qhotw__jcxq in nga__sys:
        table_name = self.normalize_name(table_name)
        lyib__yrdy = self.normalize_name(lyib__yrdy)
        if table_name not in bppjf__tgfj:
            bppjf__tgfj[table_name] = list()
        if lyib__yrdy.startswith('sys_clustering_column'):
            continue
        gav__dwr = self.ischema_names.get(dikd__tdo, None)
        blwpu__gksgq = {}
        if gav__dwr is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(dikd__tdo, lyib__yrdy))
            gav__dwr = sqltypes.NULLTYPE
        elif issubclass(gav__dwr, sqltypes.FLOAT):
            blwpu__gksgq['precision'] = zzu__ppg
            blwpu__gksgq['decimal_return_scale'] = jxpkw__ohvlq
        elif issubclass(gav__dwr, sqltypes.Numeric):
            blwpu__gksgq['precision'] = zzu__ppg
            blwpu__gksgq['scale'] = jxpkw__ohvlq
        elif issubclass(gav__dwr, (sqltypes.String, sqltypes.BINARY)):
            blwpu__gksgq['length'] = koq__grse
        jylns__gliie = gav__dwr if isinstance(gav__dwr, sqltypes.NullType
            ) else gav__dwr(**blwpu__gksgq)
        qsqzw__nxdg = bhdo__gxhyx.get(table_name)
        bppjf__tgfj[table_name].append({'name': lyib__yrdy, 'type':
            jylns__gliie, 'nullable': mykxh__hfi == 'YES', 'default':
            ptvfx__faya, 'autoincrement': aha__huitz == 'YES', 'comment':
            qhotw__jcxq, 'primary_key': lyib__yrdy in bhdo__gxhyx[
            table_name]['constrained_columns'] if qsqzw__nxdg else False})
    return bppjf__tgfj


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
    bppjf__tgfj = []
    jhvwi__ogz, rvx__jfwo = self._current_database_schema(connection, **kw)
    zhje__mdens = self._denormalize_quote_join(jhvwi__ogz, schema)
    bhdo__gxhyx = self._get_schema_primary_keys(connection, zhje__mdens, **kw)
    nga__sys = connection.execute(text(
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
    for table_name, lyib__yrdy, dikd__tdo, koq__grse, zzu__ppg, jxpkw__ohvlq, mykxh__hfi, ptvfx__faya, aha__huitz, qhotw__jcxq in nga__sys:
        table_name = self.normalize_name(table_name)
        lyib__yrdy = self.normalize_name(lyib__yrdy)
        if lyib__yrdy.startswith('sys_clustering_column'):
            continue
        gav__dwr = self.ischema_names.get(dikd__tdo, None)
        blwpu__gksgq = {}
        if gav__dwr is None:
            sa_util.warn("Did not recognize type '{}' of column '{}'".
                format(dikd__tdo, lyib__yrdy))
            gav__dwr = sqltypes.NULLTYPE
        elif issubclass(gav__dwr, sqltypes.FLOAT):
            blwpu__gksgq['precision'] = zzu__ppg
            blwpu__gksgq['decimal_return_scale'] = jxpkw__ohvlq
        elif issubclass(gav__dwr, sqltypes.Numeric):
            blwpu__gksgq['precision'] = zzu__ppg
            blwpu__gksgq['scale'] = jxpkw__ohvlq
        elif issubclass(gav__dwr, (sqltypes.String, sqltypes.BINARY)):
            blwpu__gksgq['length'] = koq__grse
        jylns__gliie = gav__dwr if isinstance(gav__dwr, sqltypes.NullType
            ) else gav__dwr(**blwpu__gksgq)
        qsqzw__nxdg = bhdo__gxhyx.get(table_name)
        bppjf__tgfj.append({'name': lyib__yrdy, 'type': jylns__gliie,
            'nullable': mykxh__hfi == 'YES', 'default': ptvfx__faya,
            'autoincrement': aha__huitz == 'YES', 'comment': qhotw__jcxq if
            qhotw__jcxq != '' else None, 'primary_key': lyib__yrdy in
            bhdo__gxhyx[table_name]['constrained_columns'] if qsqzw__nxdg else
            False})
    return bppjf__tgfj


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
