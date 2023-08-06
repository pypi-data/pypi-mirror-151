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
        uhc__icgrq = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, uhc__icgrq)


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
        jtifp__cdnd = args[0]
        sujs__mkx = signature.return_type
        fdmjh__akx = cgutils.create_struct_proxy(sujs__mkx)(context, builder)
        fdmjh__akx.obj = jtifp__cdnd
        context.nrt.incref(builder, signature.args[0], jtifp__cdnd)
        return fdmjh__akx._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for txbkc__czakn in keys:
        selection.remove(txbkc__czakn)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    sujs__mkx = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False)
    return sujs__mkx(obj_type, by_type, as_index_type, dropna_type), codegen


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
        grpby, lyztv__qba = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(lyztv__qba, (tuple, list)):
                if len(set(lyztv__qba).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(lyztv__qba).difference(set(grpby.
                        df_type.columns))))
                selection = lyztv__qba
            else:
                if lyztv__qba not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(lyztv__qba))
                selection = lyztv__qba,
                series_select = True
            iuvcm__ldst = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True, series_select)
            return signature(iuvcm__ldst, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, lyztv__qba = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            lyztv__qba):
            iuvcm__ldst = StaticGetItemDataFrameGroupBy.generic(self, (
                grpby, get_literal_value(lyztv__qba)), {}).return_type
            return signature(iuvcm__ldst, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    arr_type = to_str_arr_if_dict_array(arr_type)
    kaqq__uii = arr_type == ArrayItemArrayType(string_array_type)
    mhr__awm = arr_type.dtype
    if isinstance(mhr__awm, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {mhr__awm} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(mhr__awm, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    if func_name in ('first', 'last', 'sum', 'prod', 'min', 'max', 'count',
        'nunique', 'head') and isinstance(arr_type, (TupleArrayType,
        ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {mhr__awm} is not supported in groupby built-in function {func_name}'
            )
    if func_name in {'median', 'mean', 'var', 'std'} and isinstance(mhr__awm,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    if not isinstance(mhr__awm, (types.Integer, types.Float, types.Boolean)):
        if kaqq__uii or mhr__awm == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(mhr__awm, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not mhr__awm.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {mhr__awm} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(mhr__awm, types.Boolean) and func_name in {'cumsum',
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
    mhr__awm = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(mhr__awm, (types
            .Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(mhr__awm, types.Integer):
            return IntDtype(mhr__awm)
        return mhr__awm
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        zzkgx__jkhsv = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{zzkgx__jkhsv}'."
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
    for txbkc__czakn in grp.keys:
        if multi_level_names:
            gmqea__omz = txbkc__czakn, ''
        else:
            gmqea__omz = txbkc__czakn
        fsjs__pccq = grp.df_type.columns.index(txbkc__czakn)
        data = to_str_arr_if_dict_array(grp.df_type.data[fsjs__pccq])
        out_columns.append(gmqea__omz)
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
        okgy__hrn = tuple(grp.df_type.columns.index(grp.keys[lvsqg__zot]) for
            lvsqg__zot in range(len(grp.keys)))
        mzgca__iebj = tuple(grp.df_type.data[fsjs__pccq] for fsjs__pccq in
            okgy__hrn)
        mzgca__iebj = tuple(to_str_arr_if_dict_array(lks__cqmci) for
            lks__cqmci in mzgca__iebj)
        index = MultiIndexType(mzgca__iebj, tuple(types.StringLiteral(
            txbkc__czakn) for txbkc__czakn in grp.keys))
    else:
        fsjs__pccq = grp.df_type.columns.index(grp.keys[0])
        ebrsd__iop = to_str_arr_if_dict_array(grp.df_type.data[fsjs__pccq])
        index = bodo.hiframes.pd_index_ext.array_type_to_index(ebrsd__iop,
            types.StringLiteral(grp.keys[0]))
    jepft__ttgp = {}
    vjha__lnaz = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        jepft__ttgp[None, 'size'] = 'size'
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for tarph__lxhn in columns:
            fsjs__pccq = grp.df_type.columns.index(tarph__lxhn)
            data = grp.df_type.data[fsjs__pccq]
            data = to_str_arr_if_dict_array(data)
            fdvs__sxsz = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType)
                ) and isinstance(data.dtype, (types.Integer, types.Float)):
                fdvs__sxsz = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    sjim__ams = SeriesType(data.dtype, data, None, string_type)
                    rhrk__zeob = get_const_func_output_type(func, (
                        sjim__ams,), {}, typing_context, target_context)
                    if rhrk__zeob != ArrayItemArrayType(string_array_type):
                        rhrk__zeob = dtype_to_array_type(rhrk__zeob)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=tarph__lxhn, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    jhylt__pops = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    icahp__lnovn = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    jsabf__abok = dict(numeric_only=jhylt__pops, min_count=
                        icahp__lnovn)
                    cgik__have = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        jsabf__abok, cgik__have, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    jhylt__pops = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    icahp__lnovn = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    jsabf__abok = dict(numeric_only=jhylt__pops, min_count=
                        icahp__lnovn)
                    cgik__have = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        jsabf__abok, cgik__have, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    jhylt__pops = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    jsabf__abok = dict(numeric_only=jhylt__pops)
                    cgik__have = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        jsabf__abok, cgik__have, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    zsyyt__tku = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    wpn__snvu = args[1] if len(args) > 1 else kws.pop('skipna',
                        True)
                    jsabf__abok = dict(axis=zsyyt__tku, skipna=wpn__snvu)
                    cgik__have = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        jsabf__abok, cgik__have, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    bco__inzvl = args[0] if len(args) > 0 else kws.pop('ddof',
                        1)
                    jsabf__abok = dict(ddof=bco__inzvl)
                    cgik__have = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        jsabf__abok, cgik__have, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                rhrk__zeob, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                ese__mnn = to_str_arr_if_dict_array(rhrk__zeob)
                out_data.append(ese__mnn)
                out_columns.append(tarph__lxhn)
                if func_name == 'agg':
                    vii__bln = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    jepft__ttgp[tarph__lxhn, vii__bln] = tarph__lxhn
                else:
                    jepft__ttgp[tarph__lxhn, func_name] = tarph__lxhn
                out_column_type.append(fdvs__sxsz)
            else:
                vjha__lnaz.append(err_msg)
    if func_name == 'sum':
        hibr__mionm = any([(vpx__sla == ColumnType.NumericalColumn.value) for
            vpx__sla in out_column_type])
        if hibr__mionm:
            out_data = [vpx__sla for vpx__sla, nosjb__dnyc in zip(out_data,
                out_column_type) if nosjb__dnyc != ColumnType.
                NonNumericalColumn.value]
            out_columns = [vpx__sla for vpx__sla, nosjb__dnyc in zip(
                out_columns, out_column_type) if nosjb__dnyc != ColumnType.
                NonNumericalColumn.value]
            jepft__ttgp = {}
            for tarph__lxhn in out_columns:
                if grp.as_index is False and tarph__lxhn in grp.keys:
                    continue
                jepft__ttgp[tarph__lxhn, func_name] = tarph__lxhn
    ywn__xaq = len(vjha__lnaz)
    if len(out_data) == 0:
        if ywn__xaq == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(ywn__xaq, ' was' if ywn__xaq == 1 else 's were',
                ','.join(vjha__lnaz)))
    oqvjb__uccq = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index):
        if isinstance(out_data[0], IntegerArrayType):
            yrstj__sfl = IntDtype(out_data[0].dtype)
        else:
            yrstj__sfl = out_data[0].dtype
        tbh__xdvb = types.none if func_name == 'size' else types.StringLiteral(
            grp.selection[0])
        oqvjb__uccq = SeriesType(yrstj__sfl, index=index, name_typ=tbh__xdvb)
    return signature(oqvjb__uccq, *args), jepft__ttgp


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context, target_context
    ):
    barb__fhj = True
    if isinstance(f_val, str):
        barb__fhj = False
        aeon__yhz = f_val
    elif is_overload_constant_str(f_val):
        barb__fhj = False
        aeon__yhz = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        barb__fhj = False
        aeon__yhz = bodo.utils.typing.get_builtin_function_name(f_val)
    if not barb__fhj:
        if aeon__yhz not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {aeon__yhz}')
        iuvcm__ldst = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(iuvcm__ldst, (), aeon__yhz, typing_context,
            target_context)[0].return_type
    else:
        if is_expr(f_val, 'make_function'):
            kgcz__xclol = types.functions.MakeFunctionLiteral(f_val)
        else:
            kgcz__xclol = f_val
        validate_udf('agg', kgcz__xclol)
        func = get_overload_const_func(kgcz__xclol, None)
        zdw__ret = func.code if hasattr(func, 'code') else func.__code__
        aeon__yhz = zdw__ret.co_name
        iuvcm__ldst = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True)
        out_tp = get_agg_typ(iuvcm__ldst, (), 'agg', typing_context,
            target_context, kgcz__xclol)[0].return_type
    return aeon__yhz, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    ijfqv__obvl = kws and all(isinstance(veqv__avjme, types.Tuple) and len(
        veqv__avjme) == 2 for veqv__avjme in kws.values())
    if is_overload_none(func) and not ijfqv__obvl:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not ijfqv__obvl:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    yctzg__nlqz = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if ijfqv__obvl or is_overload_constant_dict(func):
        if ijfqv__obvl:
            upwdl__iojk = [get_literal_value(kvyr__lmvj) for kvyr__lmvj,
                gtyrs__xebng in kws.values()]
            whiua__pdq = [get_literal_value(hbymw__rwi) for gtyrs__xebng,
                hbymw__rwi in kws.values()]
        else:
            fkp__ako = get_overload_constant_dict(func)
            upwdl__iojk = tuple(fkp__ako.keys())
            whiua__pdq = tuple(fkp__ako.values())
        if 'head' in whiua__pdq:
            raise BodoError(
                'Groupby.agg()/aggregate(): head cannot be mixed with other groupby operations.'
                )
        if any(tarph__lxhn not in grp.selection and tarph__lxhn not in grp.
            keys for tarph__lxhn in upwdl__iojk):
            raise_bodo_error(
                f'Selected column names {upwdl__iojk} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            whiua__pdq)
        if ijfqv__obvl and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        jepft__ttgp = {}
        out_columns = []
        out_data = []
        out_column_type = []
        tjtw__raf = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for laa__yyk, f_val in zip(upwdl__iojk, whiua__pdq):
            if isinstance(f_val, (tuple, list)):
                oizzx__hcmz = 0
                for kgcz__xclol in f_val:
                    aeon__yhz, out_tp = get_agg_funcname_and_outtyp(grp,
                        laa__yyk, kgcz__xclol, typing_context, target_context)
                    yctzg__nlqz = aeon__yhz in list_cumulative
                    if aeon__yhz == '<lambda>' and len(f_val) > 1:
                        aeon__yhz = '<lambda_' + str(oizzx__hcmz) + '>'
                        oizzx__hcmz += 1
                    out_columns.append((laa__yyk, aeon__yhz))
                    jepft__ttgp[laa__yyk, aeon__yhz] = laa__yyk, aeon__yhz
                    _append_out_type(grp, out_data, out_tp)
            else:
                aeon__yhz, out_tp = get_agg_funcname_and_outtyp(grp,
                    laa__yyk, f_val, typing_context, target_context)
                yctzg__nlqz = aeon__yhz in list_cumulative
                if multi_level_names:
                    out_columns.append((laa__yyk, aeon__yhz))
                    jepft__ttgp[laa__yyk, aeon__yhz] = laa__yyk, aeon__yhz
                elif not ijfqv__obvl:
                    out_columns.append(laa__yyk)
                    jepft__ttgp[laa__yyk, aeon__yhz] = laa__yyk
                elif ijfqv__obvl:
                    tjtw__raf.append(aeon__yhz)
                _append_out_type(grp, out_data, out_tp)
        if ijfqv__obvl:
            for lvsqg__zot, piv__fogqi in enumerate(kws.keys()):
                out_columns.append(piv__fogqi)
                jepft__ttgp[upwdl__iojk[lvsqg__zot], tjtw__raf[lvsqg__zot]
                    ] = piv__fogqi
        if yctzg__nlqz:
            index = grp.df_type.index
        else:
            index = out_tp.index
        oqvjb__uccq = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(oqvjb__uccq, *args), jepft__ttgp
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
        oizzx__hcmz = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        jepft__ttgp = {}
        tqjwd__eoaqg = grp.selection[0]
        for f_val in func.types:
            aeon__yhz, out_tp = get_agg_funcname_and_outtyp(grp,
                tqjwd__eoaqg, f_val, typing_context, target_context)
            yctzg__nlqz = aeon__yhz in list_cumulative
            if aeon__yhz == '<lambda>':
                aeon__yhz = '<lambda_' + str(oizzx__hcmz) + '>'
                oizzx__hcmz += 1
            out_columns.append(aeon__yhz)
            jepft__ttgp[tqjwd__eoaqg, aeon__yhz] = aeon__yhz
            _append_out_type(grp, out_data, out_tp)
        if yctzg__nlqz:
            index = grp.df_type.index
        else:
            index = out_tp.index
        oqvjb__uccq = DataFrameType(tuple(out_data), index, tuple(out_columns))
        return signature(oqvjb__uccq, *args), jepft__ttgp
    aeon__yhz = ''
    if types.unliteral(func) == types.unicode_type:
        aeon__yhz = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        aeon__yhz = bodo.utils.typing.get_builtin_function_name(func)
    if aeon__yhz:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, aeon__yhz, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = grp.df_type.index
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        zsyyt__tku = args[0] if len(args) > 0 else kws.pop('axis', 0)
        jhylt__pops = args[1] if len(args) > 1 else kws.pop('numeric_only',
            False)
        wpn__snvu = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        jsabf__abok = dict(axis=zsyyt__tku, numeric_only=jhylt__pops)
        cgik__have = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', jsabf__abok,
            cgik__have, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        luq__rpa = args[0] if len(args) > 0 else kws.pop('periods', 1)
        fnml__cvke = args[1] if len(args) > 1 else kws.pop('freq', None)
        zsyyt__tku = args[2] if len(args) > 2 else kws.pop('axis', 0)
        zfx__oye = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        jsabf__abok = dict(freq=fnml__cvke, axis=zsyyt__tku, fill_value=
            zfx__oye)
        cgik__have = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', jsabf__abok,
            cgik__have, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        cmp__gty = args[0] if len(args) > 0 else kws.pop('func', None)
        qiz__xxew = kws.pop('engine', None)
        xbj__ulzgv = kws.pop('engine_kwargs', None)
        jsabf__abok = dict(engine=qiz__xxew, engine_kwargs=xbj__ulzgv)
        cgik__have = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', jsabf__abok,
            cgik__have, package_name='pandas', module_name='GroupBy')
    jepft__ttgp = {}
    for tarph__lxhn in grp.selection:
        out_columns.append(tarph__lxhn)
        jepft__ttgp[tarph__lxhn, name_operation] = tarph__lxhn
        fsjs__pccq = grp.df_type.columns.index(tarph__lxhn)
        data = grp.df_type.data[fsjs__pccq]
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
            rhrk__zeob, err_msg = get_groupby_output_dtype(data,
                get_literal_value(cmp__gty), grp.df_type.index)
            if err_msg == 'ok':
                data = rhrk__zeob
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    oqvjb__uccq = DataFrameType(tuple(out_data), index, tuple(out_columns))
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        oqvjb__uccq = SeriesType(out_data[0].dtype, data=out_data[0], index
            =index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(oqvjb__uccq, *args), jepft__ttgp


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
        dce__kfgq = _get_groupby_apply_udf_out_type(func, grp, f_args, kws,
            self.context, numba.core.registry.cpu_target.target_context)
        ynbz__hys = isinstance(dce__kfgq, (SeriesType, HeterogeneousSeriesType)
            ) and dce__kfgq.const_info is not None or not isinstance(dce__kfgq,
            (SeriesType, DataFrameType))
        if ynbz__hys:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                xbfjg__wwbw = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                okgy__hrn = tuple(grp.df_type.columns.index(grp.keys[
                    lvsqg__zot]) for lvsqg__zot in range(len(grp.keys)))
                mzgca__iebj = tuple(grp.df_type.data[fsjs__pccq] for
                    fsjs__pccq in okgy__hrn)
                mzgca__iebj = tuple(to_str_arr_if_dict_array(lks__cqmci) for
                    lks__cqmci in mzgca__iebj)
                xbfjg__wwbw = MultiIndexType(mzgca__iebj, tuple(types.
                    literal(txbkc__czakn) for txbkc__czakn in grp.keys))
            else:
                fsjs__pccq = grp.df_type.columns.index(grp.keys[0])
                ebrsd__iop = grp.df_type.data[fsjs__pccq]
                ebrsd__iop = to_str_arr_if_dict_array(ebrsd__iop)
                xbfjg__wwbw = bodo.hiframes.pd_index_ext.array_type_to_index(
                    ebrsd__iop, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            mzz__kghse = tuple(grp.df_type.data[grp.df_type.columns.index(
                tarph__lxhn)] for tarph__lxhn in grp.keys)
            mzz__kghse = tuple(to_str_arr_if_dict_array(lks__cqmci) for
                lks__cqmci in mzz__kghse)
            ozqr__rwje = tuple(types.literal(veqv__avjme) for veqv__avjme in
                grp.keys) + get_index_name_types(dce__kfgq.index)
            if not grp.as_index:
                mzz__kghse = types.Array(types.int64, 1, 'C'),
                ozqr__rwje = (types.none,) + get_index_name_types(dce__kfgq
                    .index)
            xbfjg__wwbw = MultiIndexType(mzz__kghse +
                get_index_data_arr_types(dce__kfgq.index), ozqr__rwje)
        if ynbz__hys:
            if isinstance(dce__kfgq, HeterogeneousSeriesType):
                gtyrs__xebng, qxvrd__deyq = dce__kfgq.const_info
                if isinstance(dce__kfgq.data, bodo.libs.nullable_tuple_ext.
                    NullableTupleType):
                    gwd__ghxg = dce__kfgq.data.tuple_typ.types
                elif isinstance(dce__kfgq.data, types.Tuple):
                    gwd__ghxg = dce__kfgq.data.types
                faip__ilv = tuple(to_nullable_type(dtype_to_array_type(
                    lks__cqmci)) for lks__cqmci in gwd__ghxg)
                iygou__mksy = DataFrameType(out_data + faip__ilv,
                    xbfjg__wwbw, out_columns + qxvrd__deyq)
            elif isinstance(dce__kfgq, SeriesType):
                tstvt__crya, qxvrd__deyq = dce__kfgq.const_info
                faip__ilv = tuple(to_nullable_type(dtype_to_array_type(
                    dce__kfgq.dtype)) for gtyrs__xebng in range(tstvt__crya))
                iygou__mksy = DataFrameType(out_data + faip__ilv,
                    xbfjg__wwbw, out_columns + qxvrd__deyq)
            else:
                tblqt__erny = get_udf_out_arr_type(dce__kfgq)
                if not grp.as_index:
                    iygou__mksy = DataFrameType(out_data + (tblqt__erny,),
                        xbfjg__wwbw, out_columns + ('',))
                else:
                    iygou__mksy = SeriesType(tblqt__erny.dtype, tblqt__erny,
                        xbfjg__wwbw, None)
        elif isinstance(dce__kfgq, SeriesType):
            iygou__mksy = SeriesType(dce__kfgq.dtype, dce__kfgq.data,
                xbfjg__wwbw, dce__kfgq.name_typ)
        else:
            iygou__mksy = DataFrameType(dce__kfgq.data, xbfjg__wwbw,
                dce__kfgq.columns)
        uls__rbuog = gen_apply_pysig(len(f_args), kws.keys())
        afoqy__eqcfn = (func, *f_args) + tuple(kws.values())
        return signature(iygou__mksy, *afoqy__eqcfn).replace(pysig=uls__rbuog)

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
    exps__xhdh = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            laa__yyk = grp.selection[0]
            tblqt__erny = exps__xhdh.data[exps__xhdh.columns.index(laa__yyk)]
            tblqt__erny = to_str_arr_if_dict_array(tblqt__erny)
            mby__vsbd = SeriesType(tblqt__erny.dtype, tblqt__erny,
                exps__xhdh.index, types.literal(laa__yyk))
        else:
            wgrfq__rigl = tuple(exps__xhdh.data[exps__xhdh.columns.index(
                tarph__lxhn)] for tarph__lxhn in grp.selection)
            wgrfq__rigl = tuple(to_str_arr_if_dict_array(lks__cqmci) for
                lks__cqmci in wgrfq__rigl)
            mby__vsbd = DataFrameType(wgrfq__rigl, exps__xhdh.index, tuple(
                grp.selection))
    else:
        mby__vsbd = exps__xhdh
    lcdsq__ettp = mby__vsbd,
    lcdsq__ettp += tuple(f_args)
    try:
        dce__kfgq = get_const_func_output_type(func, lcdsq__ettp, kws,
            typing_context, target_context)
    except Exception as cmcj__xnym:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', cmcj__xnym),
            getattr(cmcj__xnym, 'loc', None))
    return dce__kfgq


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    lcdsq__ettp = (grp,) + f_args
    try:
        dce__kfgq = get_const_func_output_type(func, lcdsq__ettp, kws, self
            .context, numba.core.registry.cpu_target.target_context, False)
    except Exception as cmcj__xnym:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', cmcj__xnym
            ), getattr(cmcj__xnym, 'loc', None))
    uls__rbuog = gen_apply_pysig(len(f_args), kws.keys())
    afoqy__eqcfn = (func, *f_args) + tuple(kws.values())
    return signature(dce__kfgq, *afoqy__eqcfn).replace(pysig=uls__rbuog)


def gen_apply_pysig(n_args, kws):
    bzk__ecevg = ', '.join(f'arg{lvsqg__zot}' for lvsqg__zot in range(n_args))
    bzk__ecevg = bzk__ecevg + ', ' if bzk__ecevg else ''
    iswli__vfkw = ', '.join(f"{iixi__mhmps} = ''" for iixi__mhmps in kws)
    vxrq__liecn = f'def apply_stub(func, {bzk__ecevg}{iswli__vfkw}):\n'
    vxrq__liecn += '    pass\n'
    vdrrx__khxfc = {}
    exec(vxrq__liecn, {}, vdrrx__khxfc)
    gbbt__vlzo = vdrrx__khxfc['apply_stub']
    return numba.core.utils.pysignature(gbbt__vlzo)


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
        rhrk__zeob = get_pivot_output_dtype(data, aggfunc.literal_value)
        mndw__sbpy = dtype_to_array_type(rhrk__zeob)
        if is_overload_none(_pivot_values):
            raise_bodo_error(
                'Dataframe.pivot_table() requires explicit annotation to determine output columns. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/pandas.html'
                )
        uisb__kswln = _pivot_values.meta
        eycm__qmc = len(uisb__kswln)
        fsjs__pccq = df.columns.index(index)
        ebrsd__iop = df.data[fsjs__pccq]
        ebrsd__iop = to_str_arr_if_dict_array(ebrsd__iop)
        yuyi__aiyun = bodo.hiframes.pd_index_ext.array_type_to_index(ebrsd__iop
            , types.StringLiteral(index))
        iryi__aysb = DataFrameType((mndw__sbpy,) * eycm__qmc, yuyi__aiyun,
            tuple(uisb__kswln))
        return signature(iryi__aysb, *args)


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
        mndw__sbpy = types.Array(types.int64, 1, 'C')
        uisb__kswln = _pivot_values.meta
        eycm__qmc = len(uisb__kswln)
        yuyi__aiyun = bodo.hiframes.pd_index_ext.array_type_to_index(
            to_str_arr_if_dict_array(index.data), types.StringLiteral('index'))
        iryi__aysb = DataFrameType((mndw__sbpy,) * eycm__qmc, yuyi__aiyun,
            tuple(uisb__kswln))
        return signature(iryi__aysb, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    vxrq__liecn = 'def impl(keys, dropna, _is_parallel):\n'
    vxrq__liecn += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    vxrq__liecn += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{lvsqg__zot}])' for lvsqg__zot in range(len(
        keys.types))))
    vxrq__liecn += '    table = arr_info_list_to_table(info_list)\n'
    vxrq__liecn += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    vxrq__liecn += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    vxrq__liecn += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    vxrq__liecn += '    delete_table_decref_arrays(table)\n'
    vxrq__liecn += '    ev.finalize()\n'
    vxrq__liecn += '    return sort_idx, group_labels, ngroups\n'
    vdrrx__khxfc = {}
    exec(vxrq__liecn, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, vdrrx__khxfc
        )
    nnsew__hnqu = vdrrx__khxfc['impl']
    return nnsew__hnqu


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    cdnv__tfht = len(labels)
    xjvu__gxaog = np.zeros(ngroups, dtype=np.int64)
    ixiy__qrhbu = np.zeros(ngroups, dtype=np.int64)
    luq__tejm = 0
    gtb__fed = 0
    for lvsqg__zot in range(cdnv__tfht):
        bufns__nmes = labels[lvsqg__zot]
        if bufns__nmes < 0:
            luq__tejm += 1
        else:
            gtb__fed += 1
            if lvsqg__zot == cdnv__tfht - 1 or bufns__nmes != labels[
                lvsqg__zot + 1]:
                xjvu__gxaog[bufns__nmes] = luq__tejm
                ixiy__qrhbu[bufns__nmes] = luq__tejm + gtb__fed
                luq__tejm += gtb__fed
                gtb__fed = 0
    return xjvu__gxaog, ixiy__qrhbu


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    nnsew__hnqu, gtyrs__xebng = gen_shuffle_dataframe(df, keys, _is_parallel)
    return nnsew__hnqu


def gen_shuffle_dataframe(df, keys, _is_parallel):
    tstvt__crya = len(df.columns)
    rhsb__cisk = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    vxrq__liecn = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        vxrq__liecn += '  return df, keys, get_null_shuffle_info()\n'
        vdrrx__khxfc = {}
        exec(vxrq__liecn, {'get_null_shuffle_info': get_null_shuffle_info},
            vdrrx__khxfc)
        nnsew__hnqu = vdrrx__khxfc['impl']
        return nnsew__hnqu
    for lvsqg__zot in range(tstvt__crya):
        vxrq__liecn += f"""  in_arr{lvsqg__zot} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {lvsqg__zot})
"""
    vxrq__liecn += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    vxrq__liecn += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{lvsqg__zot}])' for lvsqg__zot in range(
        rhsb__cisk)), ', '.join(f'array_to_info(in_arr{lvsqg__zot})' for
        lvsqg__zot in range(tstvt__crya)), 'array_to_info(in_index_arr)')
    vxrq__liecn += '  table = arr_info_list_to_table(info_list)\n'
    vxrq__liecn += (
        f'  out_table = shuffle_table(table, {rhsb__cisk}, _is_parallel, 1)\n')
    for lvsqg__zot in range(rhsb__cisk):
        vxrq__liecn += f"""  out_key{lvsqg__zot} = info_to_array(info_from_table(out_table, {lvsqg__zot}), keys{lvsqg__zot}_typ)
"""
    for lvsqg__zot in range(tstvt__crya):
        vxrq__liecn += f"""  out_arr{lvsqg__zot} = info_to_array(info_from_table(out_table, {lvsqg__zot + rhsb__cisk}), in_arr{lvsqg__zot}_typ)
"""
    vxrq__liecn += f"""  out_arr_index = info_to_array(info_from_table(out_table, {rhsb__cisk + tstvt__crya}), ind_arr_typ)
"""
    vxrq__liecn += '  shuffle_info = get_shuffle_info(out_table)\n'
    vxrq__liecn += '  delete_table(out_table)\n'
    vxrq__liecn += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{lvsqg__zot}' for lvsqg__zot in range(
        tstvt__crya))
    vxrq__liecn += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    vxrq__liecn += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, {gen_const_tup(df.columns)})
"""
    vxrq__liecn += '  return out_df, ({},), shuffle_info\n'.format(', '.
        join(f'out_key{lvsqg__zot}' for lvsqg__zot in range(rhsb__cisk)))
    iav__onk = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, 'ind_arr_typ': types.Array(types.int64, 1, 'C') if
        isinstance(df.index, RangeIndexType) else df.index.data}
    iav__onk.update({f'keys{lvsqg__zot}_typ': keys.types[lvsqg__zot] for
        lvsqg__zot in range(rhsb__cisk)})
    iav__onk.update({f'in_arr{lvsqg__zot}_typ': df.data[lvsqg__zot] for
        lvsqg__zot in range(tstvt__crya)})
    vdrrx__khxfc = {}
    exec(vxrq__liecn, iav__onk, vdrrx__khxfc)
    nnsew__hnqu = vdrrx__khxfc['impl']
    return nnsew__hnqu, iav__onk


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        rsqk__wquxp = len(data.array_types)
        vxrq__liecn = 'def impl(data, shuffle_info):\n'
        vxrq__liecn += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{lvsqg__zot}])' for lvsqg__zot in
            range(rsqk__wquxp)))
        vxrq__liecn += '  table = arr_info_list_to_table(info_list)\n'
        vxrq__liecn += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for lvsqg__zot in range(rsqk__wquxp):
            vxrq__liecn += f"""  out_arr{lvsqg__zot} = info_to_array(info_from_table(out_table, {lvsqg__zot}), data._data[{lvsqg__zot}])
"""
        vxrq__liecn += '  delete_table(out_table)\n'
        vxrq__liecn += '  delete_table(table)\n'
        vxrq__liecn += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{lvsqg__zot}' for lvsqg__zot in range
            (rsqk__wquxp))))
        vdrrx__khxfc = {}
        exec(vxrq__liecn, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, vdrrx__khxfc)
        nnsew__hnqu = vdrrx__khxfc['impl']
        return nnsew__hnqu
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            ard__mpvt = bodo.utils.conversion.index_to_array(data)
            ese__mnn = reverse_shuffle(ard__mpvt, shuffle_info)
            return bodo.utils.conversion.index_from_array(ese__mnn)
        return impl_index

    def impl_arr(data, shuffle_info):
        axu__lget = [array_to_info(data)]
        poq__leob = arr_info_list_to_table(axu__lget)
        rtmh__mgogt = reverse_shuffle_table(poq__leob, shuffle_info)
        ese__mnn = info_to_array(info_from_table(rtmh__mgogt, 0), data)
        delete_table(rtmh__mgogt)
        delete_table(poq__leob)
        return ese__mnn
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    jsabf__abok = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna
        )
    cgik__have = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', jsabf__abok, cgik__have,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    epykf__hcrj = get_overload_const_bool(ascending)
    qgklt__mgwmf = grp.selection[0]
    vxrq__liecn = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    qmsp__swgav = (
        f"lambda S: S.value_counts(ascending={epykf__hcrj}, _index_name='{qgklt__mgwmf}')"
        )
    vxrq__liecn += f'    return grp.apply({qmsp__swgav})\n'
    vdrrx__khxfc = {}
    exec(vxrq__liecn, {'bodo': bodo}, vdrrx__khxfc)
    nnsew__hnqu = vdrrx__khxfc['impl']
    return nnsew__hnqu


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
    for nycik__amiad in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, nycik__amiad, no_unliteral
            =True)(create_unsupported_overload(
            f'DataFrameGroupBy.{nycik__amiad}'))
    for nycik__amiad in groupby_unsupported:
        overload_method(DataFrameGroupByType, nycik__amiad, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{nycik__amiad}'))
    for nycik__amiad in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, nycik__amiad, no_unliteral
            =True)(create_unsupported_overload(f'SeriesGroupBy.{nycik__amiad}')
            )
    for nycik__amiad in series_only_unsupported:
        overload_method(DataFrameGroupByType, nycik__amiad, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{nycik__amiad}'))
    for nycik__amiad in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, nycik__amiad, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{nycik__amiad}'))


_install_groupby_unsupported()
