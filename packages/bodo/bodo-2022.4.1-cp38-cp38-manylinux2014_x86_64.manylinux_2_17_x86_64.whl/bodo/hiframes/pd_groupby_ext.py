"""Support for Pandas Groupby operations
"""
import operator
from enum import Enum
import numba
import numpy as np
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType, RangeIndexType
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, get_groupby_labels, get_null_shuffle_info, get_shuffle_info, info_from_table, info_to_array, reverse_shuffle_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import gen_const_tup, get_call_expr_arg, get_const_func_output_type
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_index_name_types, get_literal_value, get_overload_const_bool, get_overload_const_func, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, get_udf_error_msg, get_udf_out_arr_type, is_dtype_nullable, is_literal_type, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, list_cumulative, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
from bodo.utils.utils import dt_err, is_expr


class DataFrameGroupByType(types.Type):

    def __init__(self, df_type, keys, selection, as_index, dropna=True,
        explicit_select=False, series_select=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df_type,
            'pandas.groupby()')
        self.df_type = df_type
        self.keys = keys
        self.selection = selection
        self.as_index = as_index
        self.dropna = dropna
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(DataFrameGroupByType, self).__init__(name=
            f'DataFrameGroupBy({df_type}, {keys}, {selection}, {as_index}, {dropna}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return DataFrameGroupByType(self.df_type, self.keys, self.selection,
            self.as_index, self.dropna, self.explicit_select, self.
            series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFrameGroupByType)
class GroupbyModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        giis__qyqnz = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, giis__qyqnz)


make_attribute_wrapper(DataFrameGroupByType, 'obj', 'obj')


def validate_udf(func_name, func):
    if not isinstance(func, (types.functions.MakeFunctionLiteral, bodo.
        utils.typing.FunctionLiteral, types.Dispatcher, CPUDispatcher)):
        raise_bodo_error(
            f"Groupby.{func_name}: 'func' must be user defined function")


@intrinsic
def init_groupby(typingctx, obj_type, by_type, as_index_type=None,
    dropna_type=None):

    def codegen(context, builder, signature, args):
        ydwfl__yqs = args[0]
        wdk__uhxds = signature.return_type
        xepi__poh = cgutils.create_struct_proxy(wdk__uhxds)(context, builder)
        xepi__poh.obj = ydwfl__yqs
        context.nrt.incref(builder, signature.args[0], ydwfl__yqs)
        return xepi__poh._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for zjru__sqd in keys:
        selection.remove(zjru__sqd)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    wdk__uhxds = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return wdk__uhxds(obj_type, by_type, as_index_type, dropna_type), codegen


@lower_builtin('groupby.count', types.VarArg(types.Any))
@lower_builtin('groupby.size', types.VarArg(types.Any))
@lower_builtin('groupby.apply', types.VarArg(types.Any))
@lower_builtin('groupby.agg', types.VarArg(types.Any))
def lower_groupby_count_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@infer
class StaticGetItemDataFrameGroupBy(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        grpby, jgmpd__qgs = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(jgmpd__qgs, (tuple, list)):
                if len(set(jgmpd__qgs).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(jgmpd__qgs).difference(set(grpby.
                        df_type.columns))))
                selection = jgmpd__qgs
            else:
                if jgmpd__qgs not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(jgmpd__qgs))
                selection = jgmpd__qgs,
                series_select = True
            qgu__plnva = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(qgu__plnva, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, jgmpd__qgs = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            jgmpd__qgs):
            qgu__plnva = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(jgmpd__qgs)), {}).return_type
            return signature(qgu__plnva, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    arr_type = to_str_arr_if_dict_array(arr_type)
    waep__harno = arr_type == ArrayItemArrayType(string_array_type)
    jwxxm__klxv = arr_type.dtype
    if isinstance(jwxxm__klxv, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {jwxxm__klxv} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(jwxxm__klxv, (
        Decimal128Type, types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {jwxxm__klxv} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(jwxxm__klxv
        , (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(jwxxm__klxv, (types.Integer, types.Float, types.Boolean)
        ):
        if waep__harno or jwxxm__klxv == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(jwxxm__klxv, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not jwxxm__klxv.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {jwxxm__klxv} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(jwxxm__klxv, types.Boolean) and func_name in {'cumsum',
        'sum', 'mean', 'std', 'var'}:
        return (None,
            f'groupby built-in functions {func_name} does not support boolean column'
            )
    if func_name in {'idxmin', 'idxmax'}:
        return dtype_to_array_type(get_index_data_arr_types(index_type)[0].
            dtype), 'ok'
    if func_name in {'count', 'nunique'}:
        return dtype_to_array_type(types.int64), 'ok'
    else:
        return arr_type, 'ok'


def get_pivot_output_dtype(arr_type, func_name, index_type=None):
    jwxxm__klxv = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(jwxxm__klxv, (
            types.Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(jwxxm__klxv, types.Integer):
            return IntDtype(jwxxm__klxv)
        return jwxxm__klxv
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        zzp__vot = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{zzp__vot}'."
            )
    elif len(args) > len_args:
        raise BodoError(
            f'Groupby.{func_name}() takes {len_args + 1} positional argument but {len(args)} were given.'
            )


class ColumnType(Enum):
    KeyColumn = 0
    NumericalColumn = 1
    NonNumericalColumn = 2


def get_keys_not_as_index(grp, out_columns, out_data, out_column_type,
    multi_level_names=False):
    for zjru__sqd in grp.keys:
        if multi_level_names:
            dmtwe__chzvp = zjru__sqd, ''
        else:
            dmtwe__chzvp = zjru__sqd
        pxku__sfsml = grp.df_type.columns.index(zjru__sqd)
        data = to_str_arr_if_dict_array(grp.df_type.data[pxku__sfsml])
        out_columns.append(dmtwe__chzvp)
        out_data.append(data)
        out_column_type.append(ColumnType.KeyColumn.value)


def get_agg_typ(grp, args, func_name, typing_context, target_context, func=
    None, kws=None):
    index = RangeIndexType(types.none)
    out_data = []
    out_columns = []
    out_column_type = []
    if func_name == 'head':
        grp.as_index = True
    if not grp.as_index:
        get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
    elif func_name == 'head':
        if grp.df_type.index == index:
            index = NumericIndexType(types.int64, types.none)
        else:
            index = grp.df_type.index
    elif len(grp.keys) > 1:
        xmuj__clbdn = tuple(grp.df_type.columns.index(grp.keys[jqt__ydi]) for
            jqt__ydi in range(len(grp.keys)))
        snpax__iia = tuple(grp.df_type.data[pxku__sfsml] for pxku__sfsml in
            xmuj__clbdn)
        snpax__iia = tuple(to_str_arr_if_dict_array(oopwa__tga) for
            oopwa__tga in snpax__iia)
        index = MultiIndexType(snpax__iia, tuple(types.StringLiteral(
            zjru__sqd) for zjru__sqd in grp.keys))
    else:
        pxku__sfsml = grp.df_type.columns.index(grp.keys[0])
        xhzpl__oezck = to_str_arr_if_dict_array(grp.df_type.data[pxku__sfsml])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(xhzpl__oezck,
            types.StringLiteral(grp.keys[0]))
    txqa__fzg = {}
    yann__qaey = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        txqa__fzg[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for potdz__vlvs in columns:
            pxku__sfsml = grp.df_type.columns.index(potdz__vlvs)
            data = grp.df_type.data[pxku__sfsml]
            data = to_str_arr_if_dict_array(data)
            tcry__wlmjg = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                tcry__wlmjg = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    adgu__qepug = SeriesType(data.dtype, data, None,
                        string_type)
                    kvpo__csxrq = get_const_func_output_type(func, (
                        adgu__qepug,), {}, typing_context, target_context)
                    if kvpo__csxrq != ArrayItemArrayType(string_array_type):
                        kvpo__csxrq = dtype_to_array_type(kvpo__csxrq)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=potdz__vlvs, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    lrcty__fsbz = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    jldxl__rhb = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    zgjdw__dsgeb = dict(numeric_only=lrcty__fsbz, min_count
                        =jldxl__rhb)
                    arc__wzmx = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        zgjdw__dsgeb, arc__wzmx, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    lrcty__fsbz = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    jldxl__rhb = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    zgjdw__dsgeb = dict(numeric_only=lrcty__fsbz, min_count
                        =jldxl__rhb)
                    arc__wzmx = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        zgjdw__dsgeb, arc__wzmx, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    lrcty__fsbz = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    zgjdw__dsgeb = dict(numeric_only=lrcty__fsbz)
                    arc__wzmx = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        zgjdw__dsgeb, arc__wzmx, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    rnsnt__siu = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    lugq__kdht = args[1] if len(args) > 1 else kws.pop('skipna'
                        , True)
                    zgjdw__dsgeb = dict(axis=rnsnt__siu, skipna=lugq__kdht)
                    arc__wzmx = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        zgjdw__dsgeb, arc__wzmx, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    yvhp__gzub = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    zgjdw__dsgeb = dict(ddof=yvhp__gzub)
                    arc__wzmx = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        zgjdw__dsgeb, arc__wzmx, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                kvpo__csxrq, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                nlkh__dcxq = to_str_arr_if_dict_array(kvpo__csxrq)
                out_data.append(nlkh__dcxq)
                out_columns.append(potdz__vlvs)
                if func_name == 'agg':
                    kegxk__ynmp = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    txqa__fzg[potdz__vlvs, kegxk__ynmp] = potdz__vlvs
                else:
                    txqa__fzg[potdz__vlvs, func_name] = potdz__vlvs
                out_column_type.append(tcry__wlmjg)
            else:
                yann__qaey.append(err_msg)
    if func_name == 'sum':
        emjks__lfrjw = any([(qyc__kzr == ColumnType.NumericalColumn.value) for
            qyc__kzr in out_column_type])
        if emjks__lfrjw:
            out_data = [qyc__kzr for qyc__kzr, lpyn__lpvug in zip(out_data,
                out_column_type) if lpyn__lpvug != ColumnType.
                NonNumericalColumn.value]
            out_columns = [qyc__kzr for qyc__kzr, lpyn__lpvug in zip(
                out_columns, out_column_type) if lpyn__lpvug != ColumnType.
                NonNumericalColumn.value]
            txqa__fzg = {}
            for potdz__vlvs in out_columns:
                if grp.as_index is False and potdz__vlvs in grp.keys:
                    continue
                txqa__fzg[potdz__vlvs, func_name] = potdz__vlvs
    vunti__sezf = len(yann__qaey)
    if len(out_data) == 0:
        if vunti__sezf == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(vunti__sezf, ' was' if vunti__sezf == 1 else
                's were', ','.join(yann__qaey)))
    shhh__hiww = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            ihlcm__yuq = IntDtype(out_data[0].dtype)
        else:
            ihlcm__yuq = out_data[0].dtype
        hzbt__vjro = (types.none if func_name == 'size' else types.
            StringLiteral(grp.selection[0]))
        shhh__hiww = SeriesType(ihlcm__yuq, index=index, name_typ=hzbt__vjro)
    return signature(shhh__hiww, *args), txqa__fzg


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    nvkvv__hdt = True
    if isinstance(f_val, str):
        nvkvv__hdt = False
        olun__dzfe = f_val
    elif is_overload_constant_str(f_val):
        nvkvv__hdt = False
        olun__dzfe = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        nvkvv__hdt = False
        olun__dzfe = bodo.utils.typing.get_builtin_function_name(f_val)
    if not nvkvv__hdt:
        if olun__dzfe not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {olun__dzfe}')
        qgu__plnva = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(qgu__plnva, (), olun__dzfe, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            rsxz__tejp = types.functions.MakeFunctionLiteral(f_val)
        else:
            rsxz__tejp = f_val
        validate_udf('agg', rsxz__tejp)
        func = get_overload_const_func(rsxz__tejp, None)
        tqfv__zmwzp = func.code if hasattr(func, 'code') else func.__code__
        olun__dzfe = tqfv__zmwzp.co_name
        qgu__plnva = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(qgu__plnva, (), 'agg', typing_context,
            target_context, rsxz__tejp)[0].return_type
    return olun__dzfe, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    gmw__mboz = kws and all(isinstance(ghxc__vir, types.Tuple) and len(
        ghxc__vir) == 2 for ghxc__vir in kws.values())
    if is_overload_none(func) and not gmw__mboz:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not gmw__mboz:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    hnaz__psl = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if gmw__mboz or is_overload_constant_dict(func):
        if gmw__mboz:
            adary__fgq = [get_literal_value(sxpel__xxe) for sxpel__xxe,
                lomxs__ddpi in kws.values()]
            nozi__kjnmh = [get_literal_value(idddi__adt) for lomxs__ddpi,
                idddi__adt in kws.values()]
        else:
            rcsvz__tgn = get_overload_constant_dict(func)
            adary__fgq = tuple(rcsvz__tgn.keys())
            nozi__kjnmh = tuple(rcsvz__tgn.values())
        if 'head' in nozi__kjnmh:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(potdz__vlvs not in grp.selection and potdz__vlvs not in grp.
            keys for potdz__vlvs in adary__fgq):
            raise_bodo_error(
                f'Selected column names {adary__fgq} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            nozi__kjnmh)
        if gmw__mboz and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        txqa__fzg = {}
        out_columns = []
        out_data = []
        out_column_type = []
        ibsuu__wfewd = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for sdkww__ivmx, f_val in zip(adary__fgq, nozi__kjnmh):
            if isinstance(f_val, (tuple, list)):
                ful__ygck = 0
                for rsxz__tejp in f_val:
                    olun__dzfe, out_tp = get_agg_funcname_and_outtyp(grp,
                        sdkww__ivmx, rsxz__tejp, typing_context, target_context
                        )
                    hnaz__psl = olun__dzfe in list_cumulative
                    if olun__dzfe == '<lambda>' and len(f_val) > 1:
                        olun__dzfe = '<lambda_' + str(ful__ygck) + '>'
                        ful__ygck += 1
                    out_columns.append((sdkww__ivmx, olun__dzfe))
                    txqa__fzg[sdkww__ivmx, olun__dzfe
                        ] = sdkww__ivmx, olun__dzfe
                    _append_out_type(grp, out_data, out_tp)
            else:
                olun__dzfe, out_tp = get_agg_funcname_and_outtyp(grp,
                    sdkww__ivmx, f_val, typing_context, target_context)
                hnaz__psl = olun__dzfe in list_cumulative
                if multi_level_names:
                    out_columns.append((sdkww__ivmx, olun__dzfe))
                    txqa__fzg[sdkww__ivmx, olun__dzfe
                        ] = sdkww__ivmx, olun__dzfe
                elif not gmw__mboz:
                    out_columns.append(sdkww__ivmx)
                    txqa__fzg[sdkww__ivmx, olun__dzfe] = sdkww__ivmx
                elif gmw__mboz:
                    ibsuu__wfewd.append(olun__dzfe)
                _append_out_type(grp, out_data, out_tp)
        if gmw__mboz:
            for jqt__ydi, cbz__cjlw in enumerate(kws.keys()):
                out_columns.append(cbz__cjlw)
                txqa__fzg[adary__fgq[jqt__ydi], ibsuu__wfewd[jqt__ydi]
                    ] = cbz__cjlw
        if hnaz__psl:
            index = grp.df_type.index
        else:
            index = out_tp.index
        shhh__hiww = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(shhh__hiww, *args), txqa__fzg
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one functions supplied'
                )
        assert len(func) > 0
        out_data = []
        out_columns = []
        out_column_type = []
        ful__ygck = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        txqa__fzg = {}
        arf__yfwe = grp.selection[0]
        for f_val in func.types:
            olun__dzfe, out_tp = get_agg_funcname_and_outtyp(grp, arf__yfwe,
                f_val, typing_context, target_context)
            hnaz__psl = olun__dzfe in list_cumulative
            if olun__dzfe == '<lambda>':
                olun__dzfe = '<lambda_' + str(ful__ygck) + '>'
                ful__ygck += 1
            out_columns.append(olun__dzfe)
            txqa__fzg[arf__yfwe, olun__dzfe] = olun__dzfe
            _append_out_type(grp, out_data, out_tp)
        if hnaz__psl:
            index = grp.df_type.index
        else:
            index = out_tp.index
        shhh__hiww = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(shhh__hiww, *args), txqa__fzg
    olun__dzfe = ''
    if types.unliteral(func) == types.unicode_type:
        olun__dzfe = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        olun__dzfe = bodo.utils.typing.get_builtin_function_name(func)
    if olun__dzfe:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, olun__dzfe, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        rnsnt__siu = args[0] if len(args) > 0 else kws.pop('axis', 0)
        lrcty__fsbz = args[1] if len(args) > 1 else kws.pop('numeric_only',
            False)
        lugq__kdht = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        zgjdw__dsgeb = dict(axis=rnsnt__siu, numeric_only=lrcty__fsbz)
        arc__wzmx = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', zgjdw__dsgeb,
            arc__wzmx, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        lnnns__qwn = args[0] if len(args) > 0 else kws.pop('periods', 1)
        vvf__hul = args[1] if len(args) > 1 else kws.pop('freq', None)
        rnsnt__siu = args[2] if len(args) > 2 else kws.pop('axis', 0)
        bigt__ywe = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        zgjdw__dsgeb = dict(freq=vvf__hul, axis=rnsnt__siu, fill_value=
            bigt__ywe)
        arc__wzmx = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', zgjdw__dsgeb,
            arc__wzmx, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        ftels__xhjz = args[0] if len(args) > 0 else kws.pop('func', None)
        jvh__snr = kws.pop('engine', None)
        flaw__amde = kws.pop('engine_kwargs', None)
        zgjdw__dsgeb = dict(engine=jvh__snr, engine_kwargs=flaw__amde)
        arc__wzmx = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', zgjdw__dsgeb,
            arc__wzmx, package_name='pandas', module_name='GroupBy')
    txqa__fzg = {}
    for potdz__vlvs in grp.selection:
        out_columns.append(potdz__vlvs)
        txqa__fzg[potdz__vlvs, name_operation] = potdz__vlvs
        pxku__sfsml = grp.df_type.columns.index(potdz__vlvs)
        data = grp.df_type.data[pxku__sfsml]
        data = to_str_arr_if_dict_array(data)
        if name_operation == 'cumprod':
            if not isinstance(data.dtype, (types.Integer, types.Float)):
                raise BodoError(msg)
        if name_operation == 'cumsum':
            if data.dtype != types.unicode_type and data != ArrayItemArrayType(
                string_array_type) and not isinstance(data.dtype, (types.
                Integer, types.Float)):
                raise BodoError(msg)
        if name_operation in ('cummin', 'cummax'):
            if not isinstance(data.dtype, types.Integer
                ) and not is_dtype_nullable(data.dtype):
                raise BodoError(msg)
        if name_operation == 'shift':
            if isinstance(data, (TupleArrayType, ArrayItemArrayType)):
                raise BodoError(msg)
            if isinstance(data.dtype, bodo.hiframes.datetime_timedelta_ext.
                DatetimeTimeDeltaType):
                raise BodoError(
                    f"""column type of {data.dtype} is not supported in groupby built-in function shift.
{dt_err}"""
                    )
        if name_operation == 'transform':
            kvpo__csxrq, err_msg = get_groupby_output_dtype(data,
                get_literal_value(ftels__xhjz), grp.df_type.index)
            if err_msg == 'ok':
                data = kvpo__csxrq
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    shhh__hiww = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        shhh__hiww = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(shhh__hiww, *args), txqa__fzg


def resolve_gb(grp, args, kws, func_name, typing_context, target_context,
    err_msg=''):
    if func_name in set(list_cumulative) | {'shift', 'transform'}:
        return resolve_transformative(grp, args, kws, err_msg, func_name)
    elif func_name in {'agg', 'aggregate'}:
        return resolve_agg(grp, args, kws, typing_context, target_context)
    else:
        return get_agg_typ(grp, args, func_name, typing_context,
            target_context, kws=kws)


@infer_getattr
class DataframeGroupByAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameGroupByType
    _attr_set = None

    @bound_function('groupby.agg', no_unliteral=True)
    def resolve_agg(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.aggregate', no_unliteral=True)
    def resolve_aggregate(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.sum', no_unliteral=True)
    def resolve_sum(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'sum', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.count', no_unliteral=True)
    def resolve_count(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'count', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.nunique', no_unliteral=True)
    def resolve_nunique(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'nunique', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.median', no_unliteral=True)
    def resolve_median(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'median', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.mean', no_unliteral=True)
    def resolve_mean(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'mean', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.min', no_unliteral=True)
    def resolve_min(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'min', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.max', no_unliteral=True)
    def resolve_max(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'max', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.prod', no_unliteral=True)
    def resolve_prod(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'prod', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.var', no_unliteral=True)
    def resolve_var(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'var', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.std', no_unliteral=True)
    def resolve_std(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'std', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.first', no_unliteral=True)
    def resolve_first(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'first', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.last', no_unliteral=True)
    def resolve_last(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'last', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmin', no_unliteral=True)
    def resolve_idxmin(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmin', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmax', no_unliteral=True)
    def resolve_idxmax(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmax', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.size', no_unliteral=True)
    def resolve_size(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'size', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.cumsum', no_unliteral=True)
    def resolve_cumsum(self, grp, args, kws):
        msg = (
            'Groupby.cumsum() only supports columns of types integer, float, string or liststring'
            )
        return resolve_gb(grp, args, kws, 'cumsum', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cumprod', no_unliteral=True)
    def resolve_cumprod(self, grp, args, kws):
        msg = (
            'Groupby.cumprod() only supports columns of types integer and float'
            )
        return resolve_gb(grp, args, kws, 'cumprod', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummin', no_unliteral=True)
    def resolve_cummin(self, grp, args, kws):
        msg = (
            'Groupby.cummin() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummin', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummax', no_unliteral=True)
    def resolve_cummax(self, grp, args, kws):
        msg = (
            'Groupby.cummax() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummax', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.shift', no_unliteral=True)
    def resolve_shift(self, grp, args, kws):
        msg = (
            'Column type of list/tuple is not supported in groupby built-in function shift'
            )
        return resolve_gb(grp, args, kws, 'shift', self.context, numba.core
            .registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.pipe', no_unliteral=True)
    def resolve_pipe(self, grp, args, kws):
        return resolve_obj_pipe(self, grp, args, kws, 'GroupBy')

    @bound_function('groupby.transform', no_unliteral=True)
    def resolve_transform(self, grp, args, kws):
        msg = (
            'Groupby.transform() only supports sum, count, min, max, mean, and std operations'
            )
        return resolve_gb(grp, args, kws, 'transform', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.head', no_unliteral=True)
    def resolve_head(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'head', self.context, numba.core.
            registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.apply', no_unliteral=True)
    def resolve_apply(self, grp, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws.pop('func', None)
        f_args = tuple(args[1:]) if len(args) > 0 else ()
        hxk__drika = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        nnww__mkr = isinstance(hxk__drika, (SeriesType,
            HeterogeneousSeriesType)
            ) and hxk__drika.const_info is not None or not isinstance(
            hxk__drika, (SeriesType, DataFrameType))
        if nnww__mkr:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                tqhrs__sszl = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                xmuj__clbdn = tuple(grp.df_type.columns.index(grp.keys[
                    jqt__ydi]) for jqt__ydi in range(len(grp.keys)))
                snpax__iia = tuple(grp.df_type.data[pxku__sfsml] for
                    pxku__sfsml in xmuj__clbdn)
                snpax__iia = tuple(to_str_arr_if_dict_array(oopwa__tga) for
                    oopwa__tga in snpax__iia)
                tqhrs__sszl = MultiIndexType(snpax__iia, tuple(types.
                    literal(zjru__sqd) for zjru__sqd in grp.keys))
            else:
                pxku__sfsml = grp.df_type.columns.index(grp.keys[0])
                xhzpl__oezck = grp.df_type.data[pxku__sfsml]
                xhzpl__oezck = to_str_arr_if_dict_array(xhzpl__oezck)
                tqhrs__sszl = bodo.hiframes.pd_index_ext.array_type_to_index(
                    xhzpl__oezck, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            bpy__hvb = tuple(grp.df_type.data[grp.df_type.columns.index(
                potdz__vlvs)] for potdz__vlvs in grp.keys)
            bpy__hvb = tuple(to_str_arr_if_dict_array(oopwa__tga) for
                oopwa__tga in bpy__hvb)
            ujqg__ojjsv = tuple(types.literal(ghxc__vir) for ghxc__vir in
                grp.keys) + get_index_name_types(hxk__drika.index)
            if not grp.as_index:
                bpy__hvb = types.Array(types.int64, 1, 'C'),
                ujqg__ojjsv = (types.none,) + get_index_name_types(hxk__drika
                    .index)
            tqhrs__sszl = MultiIndexType(bpy__hvb +
                get_index_data_arr_types(hxk__drika.index), ujqg__ojjsv)
        if nnww__mkr:
            if isinstance(hxk__drika, HeterogeneousSeriesType):
                lomxs__ddpi, mjrkh__hyu = hxk__drika.const_info
                if isinstance(hxk__drika.data, bodo.libs.nullable_tuple_ext
                    .NullableTupleType):
                    ixtx__vcn = hxk__drika.data.tuple_typ.types
                elif isinstance(hxk__drika.data, types.Tuple):
                    ixtx__vcn = hxk__drika.data.types
                magy__cycyi = tuple(to_nullable_type(dtype_to_array_type(
                    oopwa__tga)) for oopwa__tga in ixtx__vcn)
                cxn__frt = DataFrameType(out_data + magy__cycyi,
                    tqhrs__sszl, out_columns + mjrkh__hyu)
            elif isinstance(hxk__drika, SeriesType):
                fhcd__vmm, mjrkh__hyu = hxk__drika.const_info
                magy__cycyi = tuple(to_nullable_type(dtype_to_array_type(
                    hxk__drika.dtype)) for lomxs__ddpi in range(fhcd__vmm))
                cxn__frt = DataFrameType(out_data + magy__cycyi,
                    tqhrs__sszl, out_columns + mjrkh__hyu)
            else:
                diub__yucgh = get_udf_out_arr_type(hxk__drika)
                if not grp.as_index:
                    cxn__frt = DataFrameType(out_data + (diub__yucgh,),
                        tqhrs__sszl, out_columns + ('',))
                else:
                    cxn__frt = SeriesType(diub__yucgh.dtype, diub__yucgh,
                        tqhrs__sszl, None)
        elif isinstance(hxk__drika, SeriesType):
            cxn__frt = SeriesType(hxk__drika.dtype, hxk__drika.data,
                tqhrs__sszl, hxk__drika.name_typ)
        else:
            cxn__frt = DataFrameType(hxk__drika.data, tqhrs__sszl,
                hxk__drika.columns)
        jciq__qtjk = gen_apply_pysig(len(f_args), kws.keys())
        xtni__jrzqo = (func, *f_args) + tuple(kws.values())
        return signature(cxn__frt, *xtni__jrzqo).replace(pysig=jciq__qtjk)

    def generic_resolve(self, grpby, attr):
        if self._is_existing_attr(attr):
            return
        if attr not in grpby.df_type.columns:
            raise_bodo_error(
                f'groupby: invalid attribute {attr} (column not found in dataframe or unsupported function)'
                )
        return DataFrameGroupByType(grpby.df_type, grpby.keys, (attr,),
            grpby.as_index, grpby.dropna, True, True)


def _get_groupby_apply_udf_out_type(func, grp, f_args, kws, typing_context,
    target_context):
    som__urdlw = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            sdkww__ivmx = grp.selection[0]
            diub__yucgh = som__urdlw.data[som__urdlw.columns.index(sdkww__ivmx)
                ]
            diub__yucgh = to_str_arr_if_dict_array(diub__yucgh)
            yqxhq__jix = SeriesType(diub__yucgh.dtype, diub__yucgh,
                som__urdlw.index, types.literal(sdkww__ivmx))
        else:
            noeyg__sjboo = tuple(som__urdlw.data[som__urdlw.columns.index(
                potdz__vlvs)] for potdz__vlvs in grp.selection)
            noeyg__sjboo = tuple(to_str_arr_if_dict_array(oopwa__tga) for
                oopwa__tga in noeyg__sjboo)
            yqxhq__jix = DataFrameType(noeyg__sjboo, som__urdlw.index,
                tuple(grp.selection))
    else:
        yqxhq__jix = som__urdlw
    indh__uno = yqxhq__jix,
    indh__uno += tuple(f_args)
    try:
        hxk__drika = get_const_func_output_type(func, indh__uno, kws,
            typing_context, target_context)
    except Exception as kiu__njryl:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', kiu__njryl),
            getattr(kiu__njryl, 'loc', None))
    return hxk__drika


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    indh__uno = (grp,) + f_args
    try:
        hxk__drika = get_const_func_output_type(func, indh__uno, kws, self.
            context, numba.core.registry.cpu_target.target_context, False)
    except Exception as kiu__njryl:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', kiu__njryl
            ), getattr(kiu__njryl, 'loc', None))
    jciq__qtjk = gen_apply_pysig(len(f_args), kws.keys())
    xtni__jrzqo = (func, *f_args) + tuple(kws.values())
    return signature(hxk__drika, *xtni__jrzqo).replace(pysig=jciq__qtjk)


def gen_apply_pysig(n_args, kws):
    zofpt__mkq = ', '.join(f'arg{jqt__ydi}' for jqt__ydi in range(n_args))
    zofpt__mkq = zofpt__mkq + ', ' if zofpt__mkq else ''
    ixktg__jtzwk = ', '.join(f"{arqu__vhnrg} = ''" for arqu__vhnrg in kws)
    ollw__fsrx = f'def apply_stub(func, {zofpt__mkq}{ixktg__jtzwk}):\n'
    ollw__fsrx += '    pass\n'
    nlefd__mar = {}
    exec(ollw__fsrx, {}, nlefd__mar)
    bkuhb__mzp = nlefd__mar['apply_stub']
    return numba.core.utils.pysignature(bkuhb__mzp)


def pivot_table_dummy(df, values, index, columns, aggfunc, _pivot_values):
    return 0


@infer_global(pivot_table_dummy)
class PivotTableTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, values, index, columns, aggfunc, _pivot_values = args
        if not (is_overload_constant_str(values) and
            is_overload_constant_str(index) and is_overload_constant_str(
            columns)):
            raise BodoError(
                "pivot_table() only support string constants for 'values', 'index' and 'columns' arguments"
                )
        values = values.literal_value
        index = index.literal_value
        columns = columns.literal_value
        data = df.data[df.columns.index(values)]
        data = to_str_arr_if_dict_array(data)
        kvpo__csxrq = get_pivot_output_dtype(data, aggfunc.literal_value)
        cvsx__jej = dtype_to_array_type(kvpo__csxrq)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/pandas.html'
                )
        axw__kldpo = _pivot_values.meta
        sqvt__htg = len(axw__kldpo)
        pxku__sfsml = df.columns.index(index)
        xhzpl__oezck = df.data[pxku__sfsml]
        xhzpl__oezck = to_str_arr_if_dict_array(xhzpl__oezck)
        euvq__emtx = bodo.hiframes.pd_index_ext.array_type_to_index(
            xhzpl__oezck, types.StringLiteral(index))
        ajo__kcqug = DataFrameType((cvsx__jej,) * sqvt__htg, euvq__emtx,
            tuple(axw__kldpo))
        return signature(ajo__kcqug, *args)


PivotTableTyper._no_unliteral = True


@lower_builtin(pivot_table_dummy, types.VarArg(types.Any))
def lower_pivot_table_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        cvsx__jej = types.Array(types.int64, 1, 'C')
        axw__kldpo = _pivot_values.meta
        sqvt__htg = len(axw__kldpo)
        euvq__emtx = bodo.hiframes.pd_index_ext.array_type_to_index(
            to_str_arr_if_dict_array(index.data), types.StringLiteral('index'))
        ajo__kcqug = DataFrameType((cvsx__jej,) * sqvt__htg, euvq__emtx,
            tuple(axw__kldpo))
        return signature(ajo__kcqug, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    ollw__fsrx = 'def impl(keys, dropna, _is_parallel):\n'
    ollw__fsrx += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    ollw__fsrx += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{jqt__ydi}])' for jqt__ydi in range(len(keys.
        types))))
    ollw__fsrx += '    table = arr_info_list_to_table(info_list)\n'
    ollw__fsrx += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    ollw__fsrx += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    ollw__fsrx += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    ollw__fsrx += '    delete_table_decref_arrays(table)\n'
    ollw__fsrx += '    ev.finalize()\n'
    ollw__fsrx += '    return sort_idx, group_labels, ngroups\n'
    nlefd__mar = {}
    exec(ollw__fsrx, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, nlefd__mar)
    ske__eocf = nlefd__mar['impl']
    return ske__eocf


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    hdl__eha = len(labels)
    mgrg__yrdco = np.zeros(ngroups, dtype=np.int64)
    ycs__levt = np.zeros(ngroups, dtype=np.int64)
    vjcdn__vcjwa = 0
    clput__yfvr = 0
    for jqt__ydi in range(hdl__eha):
        yvdw__hwd = labels[jqt__ydi]
        if yvdw__hwd < 0:
            vjcdn__vcjwa += 1
        else:
            clput__yfvr += 1
            if jqt__ydi == hdl__eha - 1 or yvdw__hwd != labels[jqt__ydi + 1]:
                mgrg__yrdco[yvdw__hwd] = vjcdn__vcjwa
                ycs__levt[yvdw__hwd] = vjcdn__vcjwa + clput__yfvr
                vjcdn__vcjwa += clput__yfvr
                clput__yfvr = 0
    return mgrg__yrdco, ycs__levt


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    ske__eocf, lomxs__ddpi = gen_shuffle_dataframe(df, keys, _is_parallel)
    return ske__eocf


def gen_shuffle_dataframe(df, keys, _is_parallel):
    fhcd__vmm = len(df.columns)
    vmesr__btm = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    ollw__fsrx = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        ollw__fsrx += '  return df, keys, get_null_shuffle_info()\n'
        nlefd__mar = {}
        exec(ollw__fsrx, {'get_null_shuffle_info': get_null_shuffle_info},
            nlefd__mar)
        ske__eocf = nlefd__mar['impl']
        return ske__eocf
    for jqt__ydi in range(fhcd__vmm):
        ollw__fsrx += f"""  in_arr{jqt__ydi} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {jqt__ydi})
"""
    ollw__fsrx += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    ollw__fsrx += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{jqt__ydi}])' for jqt__ydi in range(vmesr__btm
        )), ', '.join(f'array_to_info(in_arr{jqt__ydi})' for jqt__ydi in
        range(fhcd__vmm)), 'array_to_info(in_index_arr)')
    ollw__fsrx += '  table = arr_info_list_to_table(info_list)\n'
    ollw__fsrx += (
        f'  out_table = shuffle_table(table, {vmesr__btm}, _is_parallel, 1)\n')
    for jqt__ydi in range(vmesr__btm):
        ollw__fsrx += f"""  out_key{jqt__ydi} = info_to_array(info_from_table(out_table, {jqt__ydi}), keys{jqt__ydi}_typ)
"""
    for jqt__ydi in range(fhcd__vmm):
        ollw__fsrx += f"""  out_arr{jqt__ydi} = info_to_array(info_from_table(out_table, {jqt__ydi + vmesr__btm}), in_arr{jqt__ydi}_typ)
"""
    ollw__fsrx += f"""  out_arr_index = info_to_array(info_from_table(out_table, {vmesr__btm + fhcd__vmm}), ind_arr_typ)
"""
    ollw__fsrx += '  shuffle_info = get_shuffle_info(out_table)\n'
    ollw__fsrx += '  delete_table(out_table)\n'
    ollw__fsrx += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{jqt__ydi}' for jqt__ydi in range(fhcd__vmm))
    ollw__fsrx += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    ollw__fsrx += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    ollw__fsrx += '  return out_df, ({},), shuffle_info\n'.format(', '.join
        (f'out_key{jqt__ydi}' for jqt__ydi in range(vmesr__btm)))
    uydbg__dmsle = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, 'ind_arr_typ': types.Array(types.int64, 1, 'C') if
        isinstance(df.index, RangeIndexType) else df.index.data}
    uydbg__dmsle.update({f'keys{jqt__ydi}_typ': keys.types[jqt__ydi] for
        jqt__ydi in range(vmesr__btm)})
    uydbg__dmsle.update({f'in_arr{jqt__ydi}_typ': df.data[jqt__ydi] for
        jqt__ydi in range(fhcd__vmm)})
    nlefd__mar = {}
    exec(ollw__fsrx, uydbg__dmsle, nlefd__mar)
    ske__eocf = nlefd__mar['impl']
    return ske__eocf, uydbg__dmsle


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        kwo__xnlxm = len(data.array_types)
        ollw__fsrx = 'def impl(data, shuffle_info):\n'
        ollw__fsrx += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{jqt__ydi}])' for jqt__ydi in range(
            kwo__xnlxm)))
        ollw__fsrx += '  table = arr_info_list_to_table(info_list)\n'
        ollw__fsrx += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for jqt__ydi in range(kwo__xnlxm):
            ollw__fsrx += f"""  out_arr{jqt__ydi} = info_to_array(info_from_table(out_table, {jqt__ydi}), data._data[{jqt__ydi}])
"""
        ollw__fsrx += '  delete_table(out_table)\n'
        ollw__fsrx += '  delete_table(table)\n'
        ollw__fsrx += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{jqt__ydi}' for jqt__ydi in range(
            kwo__xnlxm))))
        nlefd__mar = {}
        exec(ollw__fsrx, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, nlefd__mar)
        ske__eocf = nlefd__mar['impl']
        return ske__eocf
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            zmfb__ispz = bodo.utils.conversion.index_to_array(data)
            nlkh__dcxq = reverse_shuffle(zmfb__ispz, shuffle_info)
            return bodo.utils.conversion.index_from_array(nlkh__dcxq)
        return impl_index

    def impl_arr(data, shuffle_info):
        qhfei__tqx = [array_to_info(data)]
        uyar__jjn = arr_info_list_to_table(qhfei__tqx)
        msazm__drkuu = reverse_shuffle_table(uyar__jjn, shuffle_info)
        nlkh__dcxq = info_to_array(info_from_table(msazm__drkuu, 0), data)
        delete_table(msazm__drkuu)
        delete_table(uyar__jjn)
        return nlkh__dcxq
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    zgjdw__dsgeb = dict(normalize=normalize, sort=sort, bins=bins, dropna=
        dropna)
    arc__wzmx = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', zgjdw__dsgeb, arc__wzmx,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    gure__arl = get_overload_const_bool(ascending)
    dsak__catl = grp.selection[0]
    ollw__fsrx = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    enxg__ujwfc = (
        f"lambda S: S.value_counts(ascending={gure__arl}, _index_name='{dsak__catl}')"
        )
    ollw__fsrx += f'    return grp.apply({enxg__ujwfc})\n'
    nlefd__mar = {}
    exec(ollw__fsrx, {'bodo': bodo}, nlefd__mar)
    ske__eocf = nlefd__mar['impl']
    return ske__eocf


groupby_unsupported_attr = {'groups', 'indices'}
groupby_unsupported = {'__iter__', 'get_group', 'all', 'any', 'bfill',
    'backfill', 'cumcount', 'cummax', 'cummin', 'cumprod', 'ffill',
    'ngroup', 'nth', 'ohlc', 'pad', 'rank', 'pct_change', 'sem', 'tail',
    'corr', 'cov', 'describe', 'diff', 'fillna', 'filter', 'hist', 'mad',
    'plot', 'quantile', 'resample', 'sample', 'skew', 'take', 'tshift'}
series_only_unsupported_attrs = {'is_monotonic_increasing',
    'is_monotonic_decreasing'}
series_only_unsupported = {'nlargest', 'nsmallest', 'unique'}
dataframe_only_unsupported = {'corrwith', 'boxplot'}


def _install_groupby_unsupported():
    for lnwu__ktbh in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, lnwu__ktbh, no_unliteral=True
            )(create_unsupported_overload(f'DataFrameGroupBy.{lnwu__ktbh}'))
    for lnwu__ktbh in groupby_unsupported:
        overload_method(DataFrameGroupByType, lnwu__ktbh, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{lnwu__ktbh}'))
    for lnwu__ktbh in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, lnwu__ktbh, no_unliteral=True
            )(create_unsupported_overload(f'SeriesGroupBy.{lnwu__ktbh}'))
    for lnwu__ktbh in series_only_unsupported:
        overload_method(DataFrameGroupByType, lnwu__ktbh, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{lnwu__ktbh}'))
    for lnwu__ktbh in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, lnwu__ktbh, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{lnwu__ktbh}'))


_install_groupby_unsupported()
