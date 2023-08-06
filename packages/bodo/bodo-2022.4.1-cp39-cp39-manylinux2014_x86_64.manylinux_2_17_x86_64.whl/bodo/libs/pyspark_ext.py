"""
Support for PySpark APIs in Bodo JIT functions
"""
from collections import namedtuple
import numba
import numba.cpython.tupleobj
import numpy as np
import pyspark
import pyspark.sql.functions as F
from numba.core import cgutils, ir_utils, types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, infer_global, signature
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_overload_const_list, get_overload_const_str, is_overload_constant_list, is_overload_constant_str, is_overload_true
ANON_SENTINEL = 'bodo_field_'


class SparkSessionType(types.Opaque):

    def __init__(self):
        super(SparkSessionType, self).__init__(name='SparkSessionType')


spark_session_type = SparkSessionType()
register_model(SparkSessionType)(models.OpaqueModel)


class SparkSessionBuilderType(types.Opaque):

    def __init__(self):
        super(SparkSessionBuilderType, self).__init__(name=
            'SparkSessionBuilderType')


spark_session_builder_type = SparkSessionBuilderType()
register_model(SparkSessionBuilderType)(models.OpaqueModel)


@intrinsic
def init_session(typingctx=None):

    def codegen(context, builder, signature, args):
        return context.get_constant_null(spark_session_type)
    return spark_session_type(), codegen


@intrinsic
def init_session_builder(typingctx=None):

    def codegen(context, builder, signature, args):
        return context.get_constant_null(spark_session_builder_type)
    return spark_session_builder_type(), codegen


@overload_method(SparkSessionBuilderType, 'appName', no_unliteral=True)
def overload_appName(A, s):
    return lambda A, s: A


@overload_method(SparkSessionBuilderType, 'getOrCreate', inline='always',
    no_unliteral=True)
def overload_getOrCreate(A):
    return lambda A: bodo.libs.pyspark_ext.init_session()


@typeof_impl.register(pyspark.sql.session.SparkSession)
def typeof_session(val, c):
    return spark_session_type


@box(SparkSessionType)
def box_spark_session(typ, val, c):
    ftks__nut = c.context.insert_const_string(c.builder.module, 'pyspark')
    zjnw__dhl = c.pyapi.import_module_noblock(ftks__nut)
    ntjp__soi = c.pyapi.object_getattr_string(zjnw__dhl, 'sql')
    kttio__zdh = c.pyapi.object_getattr_string(ntjp__soi, 'SparkSession')
    rqofi__deuqf = c.pyapi.object_getattr_string(kttio__zdh, 'builder')
    mietq__glzsb = c.pyapi.call_method(rqofi__deuqf, 'getOrCreate', ())
    c.pyapi.decref(zjnw__dhl)
    c.pyapi.decref(ntjp__soi)
    c.pyapi.decref(kttio__zdh)
    c.pyapi.decref(rqofi__deuqf)
    return mietq__glzsb


@unbox(SparkSessionType)
def unbox_spark_session(typ, obj, c):
    return NativeValue(c.context.get_constant_null(spark_session_type))


@lower_constant(SparkSessionType)
def lower_constant_spark_session(context, builder, ty, pyval):
    return context.get_constant_null(spark_session_type)


class RowType(types.BaseNamedTuple):

    def __init__(self, types, fields):
        self.types = tuple(types)
        self.count = len(self.types)
        self.fields = tuple(fields)
        self.instance_class = namedtuple('Row', fields)
        txk__xzvwm = 'Row({})'.format(', '.join(
            f'{cini__zolfq}:{mqnhw__gesm}' for cini__zolfq, mqnhw__gesm in
            zip(self.fields, self.types)))
        super(RowType, self).__init__(txk__xzvwm)

    @property
    def key(self):
        return self.fields, self.types

    def __getitem__(self, i):
        return self.types[i]

    def __len__(self):
        return len(self.types)

    def __iter__(self):
        return iter(self.types)


@register_model(RowType)
class RowModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bji__tkprp = [(cini__zolfq, mqnhw__gesm) for cini__zolfq,
            mqnhw__gesm in zip(fe_type.fields, fe_type.types)]
        super(RowModel, self).__init__(dmm, fe_type, bji__tkprp)


@typeof_impl.register(pyspark.sql.types.Row)
def typeof_row(val, c):
    fields = val.__fields__ if hasattr(val, '__fields__') else tuple(
        f'{ANON_SENTINEL}{i}' for i in range(len(val)))
    return RowType(tuple(numba.typeof(aptbc__vsz) for aptbc__vsz in val),
        fields)


@box(RowType)
def box_row(typ, val, c):
    bimy__tyi = c.pyapi.unserialize(c.pyapi.serialize_object(pyspark.sql.
        types.Row))
    if all(cini__zolfq.startswith(ANON_SENTINEL) for cini__zolfq in typ.fields
        ):
        xfikd__sixk = [c.box(mqnhw__gesm, c.builder.extract_value(val, i)) for
            i, mqnhw__gesm in enumerate(typ.types)]
        keqt__jde = c.pyapi.call_function_objargs(bimy__tyi, xfikd__sixk)
        for obj in xfikd__sixk:
            c.pyapi.decref(obj)
        c.pyapi.decref(bimy__tyi)
        return keqt__jde
    args = c.pyapi.tuple_pack([])
    xfikd__sixk = []
    mks__paoxa = []
    for i, mqnhw__gesm in enumerate(typ.types):
        rvqy__uig = c.builder.extract_value(val, i)
        obj = c.box(mqnhw__gesm, rvqy__uig)
        mks__paoxa.append((typ.fields[i], obj))
        xfikd__sixk.append(obj)
    kws = c.pyapi.dict_pack(mks__paoxa)
    keqt__jde = c.pyapi.call(bimy__tyi, args, kws)
    for obj in xfikd__sixk:
        c.pyapi.decref(obj)
    c.pyapi.decref(bimy__tyi)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    return keqt__jde


@infer_global(pyspark.sql.types.Row)
class RowConstructor(AbstractTemplate):

    def generic(self, args, kws):
        if args and kws:
            raise BodoError(
                'pyspark.sql.types.Row: Cannot use both args and kwargs to create Row'
                )
        nepz__kdldp = ', '.join(f'arg{i}' for i in range(len(args)))
        ekerg__ffgl = ', '.join(f"{drww__stkan} = ''" for drww__stkan in kws)
        func_text = f'def row_stub({nepz__kdldp}{ekerg__ffgl}):\n'
        func_text += '    pass\n'
        xbrxj__jzp = {}
        exec(func_text, {}, xbrxj__jzp)
        qggx__mln = xbrxj__jzp['row_stub']
        qwea__arw = numba.core.utils.pysignature(qggx__mln)
        if args:
            whwa__fes = RowType(args, tuple(f'{ANON_SENTINEL}{i}' for i in
                range(len(args))))
            return signature(whwa__fes, *args).replace(pysig=qwea__arw)
        kws = dict(kws)
        whwa__fes = RowType(tuple(kws.values()), tuple(kws.keys()))
        return signature(whwa__fes, *kws.values()).replace(pysig=qwea__arw)


lower_builtin(pyspark.sql.types.Row, types.VarArg(types.Any))(numba.cpython
    .tupleobj.namedtuple_constructor)


class SparkDataFrameType(types.Type):

    def __init__(self, df):
        self.df = df
        super(SparkDataFrameType, self).__init__(f'SparkDataFrame({df})')

    @property
    def key(self):
        return self.df

    def copy(self):
        return SparkDataFrameType(self.df)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SparkDataFrameType)
class SparkDataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bji__tkprp = [('df', fe_type.df)]
        super(SparkDataFrameModel, self).__init__(dmm, fe_type, bji__tkprp)


make_attribute_wrapper(SparkDataFrameType, 'df', '_df')


@intrinsic
def init_spark_df(typingctx, df_typ=None):

    def codegen(context, builder, sig, args):
        df, = args
        spark_df = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        spark_df.df = df
        context.nrt.incref(builder, sig.args[0], df)
        return spark_df._getvalue()
    return SparkDataFrameType(df_typ)(df_typ), codegen


@overload_method(SparkSessionType, 'createDataFrame', inline='always',
    no_unliteral=True)
def overload_create_df(sp_session, data, schema=None, samplingRatio=None,
    verifySchema=True):
    check_runtime_cols_unsupported(data, 'spark.createDataFrame()')
    if isinstance(data, DataFrameType):

        def impl_df(sp_session, data, schema=None, samplingRatio=None,
            verifySchema=True):
            data = bodo.scatterv(data, warn_if_dist=False)
            return bodo.libs.pyspark_ext.init_spark_df(data)
        return impl_df
    if not (isinstance(data, types.List) and isinstance(data.dtype, RowType)):
        raise BodoError(
            f"SparkSession.createDataFrame(): 'data' should be a Pandas dataframe or list of Rows, not {data}"
            )
    geu__kujxa = data.dtype.fields
    ofrcv__axcsj = len(data.dtype.types)
    func_text = (
        'def impl(sp_session, data, schema=None, samplingRatio=None, verifySchema=True):\n'
        )
    func_text += f'  n = len(data)\n'
    pfva__pqcs = []
    for i, mqnhw__gesm in enumerate(data.dtype.types):
        ethqe__bgv = dtype_to_array_type(mqnhw__gesm)
        func_text += (
            f'  A{i} = bodo.utils.utils.alloc_type(n, arr_typ{i}, (-1,))\n')
        pfva__pqcs.append(ethqe__bgv)
    func_text += f'  for i in range(n):\n'
    func_text += f'    r = data[i]\n'
    for i in range(ofrcv__axcsj):
        func_text += (
            f'    A{i}[i] = bodo.utils.conversion.unbox_if_timestamp(r[{i}])\n'
            )
    qmcg__xwqk = '({}{})'.format(', '.join(f'A{i}' for i in range(
        ofrcv__axcsj)), ',' if len(geu__kujxa) == 1 else '')
    func_text += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)\n'
        )
    func_text += f"""  pdf = bodo.hiframes.pd_dataframe_ext.init_dataframe({qmcg__xwqk}, index, {geu__kujxa})
"""
    func_text += f'  pdf = bodo.scatterv(pdf)\n'
    func_text += f'  return bodo.libs.pyspark_ext.init_spark_df(pdf)\n'
    xbrxj__jzp = {}
    qktx__hvbk = {'bodo': bodo}
    for i in range(ofrcv__axcsj):
        qktx__hvbk[f'arr_typ{i}'] = pfva__pqcs[i]
    exec(func_text, qktx__hvbk, xbrxj__jzp)
    impl = xbrxj__jzp['impl']
    return impl


@overload_method(SparkDataFrameType, 'toPandas', inline='always',
    no_unliteral=True)
def overload_to_pandas(spark_df, _is_bodo_dist=False):
    if is_overload_true(_is_bodo_dist):
        return lambda spark_df, _is_bodo_dist=False: spark_df._df

    def impl(spark_df, _is_bodo_dist=False):
        return bodo.gatherv(spark_df._df, warn_if_rep=False)
    return impl


@overload_method(SparkDataFrameType, 'limit', inline='always', no_unliteral
    =True)
def overload_limit(spark_df, num):

    def impl(spark_df, num):
        return bodo.libs.pyspark_ext.init_spark_df(spark_df._df.iloc[:num])
    return impl


def _df_to_rows(df):
    pass


@overload(_df_to_rows)
def overload_df_to_rows(df):
    func_text = 'def impl(df):\n'
    for i in range(len(df.columns)):
        func_text += (
            f'  A{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    func_text += '  n = len(df)\n'
    func_text += '  out = []\n'
    func_text += '  for i in range(n):\n'
    tidsm__wutd = ', '.join(f'{c}=A{i}[i]' for i, c in enumerate(df.columns))
    func_text += f'    out.append(Row({tidsm__wutd}))\n'
    func_text += '  return out\n'
    xbrxj__jzp = {}
    qktx__hvbk = {'bodo': bodo, 'Row': pyspark.sql.types.Row}
    exec(func_text, qktx__hvbk, xbrxj__jzp)
    impl = xbrxj__jzp['impl']
    return impl


@overload_method(SparkDataFrameType, 'collect', inline='always',
    no_unliteral=True)
def overload_collect(spark_df):

    def impl(spark_df):
        data = bodo.gatherv(spark_df._df, warn_if_rep=False)
        return _df_to_rows(data)
    return impl


@overload_method(SparkDataFrameType, 'take', inline='always', no_unliteral=True
    )
def overload_take(spark_df, num):

    def impl(spark_df, num):
        return spark_df.limit(num).collect()
    return impl


@infer_getattr
class SparkDataFrameAttribute(AttributeTemplate):
    key = SparkDataFrameType

    def generic_resolve(self, sdf, attr):
        if attr in sdf.df.columns:
            return ColumnType(ExprType('col', (attr,)))


SparkDataFrameAttribute._no_unliteral = True


@overload_method(SparkDataFrameType, 'select', no_unliteral=True)
def overload_df_select(spark_df, *cols):
    return _gen_df_select(spark_df, cols)


def _gen_df_select(spark_df, cols, avoid_stararg=False):
    df_type = spark_df.df
    if isinstance(cols, tuple) and len(cols) == 1 and isinstance(cols[0], (
        types.StarArgTuple, types.StarArgUniTuple)):
        cols = cols[0]
    if len(cols) == 1 and is_overload_constant_list(cols[0]):
        cols = get_overload_const_list(cols[0])
    func_text = f"def impl(spark_df, {'' if avoid_stararg else '*cols'}):\n"
    func_text += '  df = spark_df._df\n'
    out_col_names = []
    out_data = []
    for col in cols:
        col = get_overload_const_str(col) if is_overload_constant_str(col
            ) else col
        out_col_names.append(_get_col_name(col))
        data, ipd__efv = _gen_col_code(col, df_type)
        func_text += ipd__efv
        out_data.append(data)
    return _gen_init_spark_df(func_text, out_data, out_col_names)


def _gen_init_spark_df(func_text, out_data, out_col_names):
    qmcg__xwqk = '({}{})'.format(', '.join(out_data), ',' if len(out_data) ==
        1 else '')
    ughj__pfk = '0' if not out_data else f'len({out_data[0]})'
    func_text += f'  n = {ughj__pfk}\n'
    func_text += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)\n'
        )
    func_text += f"""  pdf = bodo.hiframes.pd_dataframe_ext.init_dataframe({qmcg__xwqk}, index, {tuple(out_col_names)})
"""
    func_text += f'  return bodo.libs.pyspark_ext.init_spark_df(pdf)\n'
    xbrxj__jzp = {}
    qktx__hvbk = {'bodo': bodo, 'np': np}
    exec(func_text, qktx__hvbk, xbrxj__jzp)
    impl = xbrxj__jzp['impl']
    return impl


@overload_method(SparkDataFrameType, 'show', inline='always', no_unliteral=True
    )
def overload_show(spark_df, n=20, truncate=True, vertical=False):
    voti__btia = dict(truncate=truncate, vertical=vertical)
    wisv__emxkh = dict(truncate=True, vertical=False)
    check_unsupported_args('SparkDataFrameType.show', voti__btia, wisv__emxkh)

    def impl(spark_df, n=20, truncate=True, vertical=False):
        print(spark_df._df.head(n))
    return impl


@overload_method(SparkDataFrameType, 'printSchema', inline='always',
    no_unliteral=True)
def overload_print_schema(spark_df):

    def impl(spark_df):
        print(spark_df._df.dtypes)
    return impl


@overload_method(SparkDataFrameType, 'withColumn', inline='always',
    no_unliteral=True)
def overload_with_column(spark_df, colName, col):
    _check_column(col)
    if not is_overload_constant_str(colName):
        raise BodoError(
            f"SparkDataFrame.withColumn(): 'colName' should be a constant string, not {colName}"
            )
    col_name = get_overload_const_str(colName)
    snzsy__pqi = spark_df.df.columns
    nzdot__zpcg = snzsy__pqi if col_name in snzsy__pqi else snzsy__pqi + (
        col_name,)
    nmk__tjj, nwdoh__wbj = _gen_col_code(col, spark_df.df)
    out_data = [(nmk__tjj if c == col_name else
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {snzsy__pqi.index(c)})'
        ) for c in nzdot__zpcg]
    func_text = 'def impl(spark_df, colName, col):\n'
    func_text += '  df = spark_df._df\n'
    func_text += nwdoh__wbj
    return _gen_init_spark_df(func_text, out_data, nzdot__zpcg)


@overload_method(SparkDataFrameType, 'withColumnRenamed', inline='always',
    no_unliteral=True)
def overload_with_column_renamed(spark_df, existing, new):
    if not (is_overload_constant_str(existing) and is_overload_constant_str
        (new)):
        raise BodoError(
            f"SparkDataFrame.withColumnRenamed(): 'existing' and 'new' should be a constant strings, not ({existing}, {new})"
            )
    bax__dfb = get_overload_const_str(existing)
    xiwy__ahovs = get_overload_const_str(new)
    snzsy__pqi = spark_df.df.columns
    nzdot__zpcg = tuple(xiwy__ahovs if c == bax__dfb else c for c in snzsy__pqi
        )
    out_data = [f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
         for i in range(len(snzsy__pqi))]
    func_text = 'def impl(spark_df, existing, new):\n'
    func_text += '  df = spark_df._df\n'
    return _gen_init_spark_df(func_text, out_data, nzdot__zpcg)


@overload_attribute(SparkDataFrameType, 'columns', inline='always')
def overload_dataframe_columns(spark_df):
    stmq__ptjho = list(str(drww__stkan) for drww__stkan in spark_df.df.columns)
    func_text = 'def impl(spark_df):\n'
    func_text += f'  return {stmq__ptjho}\n'
    xbrxj__jzp = {}
    exec(func_text, {}, xbrxj__jzp)
    impl = xbrxj__jzp['impl']
    return impl


class ColumnType(types.Type):

    def __init__(self, expr):
        self.expr = expr
        super(ColumnType, self).__init__(f'Column({expr})')

    @property
    def key(self):
        return self.expr

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


register_model(ColumnType)(models.OpaqueModel)


class ExprType(types.Type):

    def __init__(self, op, children):
        self.op = op
        self.children = children
        super(ExprType, self).__init__(f'{op}({children})')

    @property
    def key(self):
        return self.op, self.children

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


register_model(ExprType)(models.OpaqueModel)


@intrinsic
def init_col_from_name(typingctx, col=None):
    assert is_overload_constant_str(col)
    fxvuz__pnb = get_overload_const_str(col)
    atqp__rnzc = ColumnType(ExprType('col', (fxvuz__pnb,)))

    def codegen(context, builder, signature, args):
        return context.get_constant_null(atqp__rnzc)
    return atqp__rnzc(col), codegen


@overload(F.col, no_unliteral=True)
@overload(F.column, no_unliteral=True)
def overload_f_col(col):
    if not is_overload_constant_str(col):
        raise BodoError(
            f'pyspark.sql.functions.col(): column name should be a constant string, not {col}'
            )
    return lambda col: init_col_from_name(col)


@intrinsic
def init_f_sum(typingctx, col=None):
    atqp__rnzc = ColumnType(ExprType('sum', (col.expr,)))

    def codegen(context, builder, signature, args):
        return context.get_constant_null(atqp__rnzc)
    return atqp__rnzc(col), codegen


@overload(F.sum, no_unliteral=True)
def overload_f_sum(col):
    if is_overload_constant_str(col):
        return lambda col: init_f_sum(init_col_from_name(col))
    if not isinstance(col, ColumnType):
        raise BodoError(
            f'pyspark.sql.functions.sum(): input should be a Column object or a constant string, not {col}'
            )
    return lambda col: init_f_sum(col)


def _get_col_name(col):
    if isinstance(col, str):
        return col
    _check_column(col)
    return _get_col_name_exr(col.expr)


def _get_col_name_exr(expr):
    if expr.op == 'sum':
        return f'sum({_get_col_name_exr(expr.children[0])})'
    assert expr.op == 'col'
    return expr.children[0]


def _gen_col_code(col, df_type):
    if isinstance(col, str):
        return _gen_col_code_colname(col, df_type)
    _check_column(col)
    return _gen_col_code_expr(col.expr, df_type)


def _gen_col_code_expr(expr, df_type):
    if expr.op == 'col':
        return _gen_col_code_colname(expr.children[0], df_type)
    if expr.op == 'sum':
        ydf__otcek, nyk__jjo = _gen_col_code_expr(expr.children[0], df_type)
        i = ir_utils.next_label()
        func_text = f"""  A{i} = np.asarray([bodo.libs.array_ops.array_op_sum({ydf__otcek}, True, 0)])
"""
        return f'A{i}', nyk__jjo + func_text


def _gen_col_code_colname(col_name, df_type):
    sfs__mytgl = df_type.columns.index(col_name)
    i = ir_utils.next_label()
    func_text = (
        f'  A{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {sfs__mytgl})\n'
        )
    return f'A{i}', func_text


def _check_column(col):
    if not isinstance(col, ColumnType):
        raise BodoError('Column object expected')
