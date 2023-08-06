"""
Implement pd.DataFrame typing and data model handling.
"""
import json
import operator
from urllib.parse import quote
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.cpython.listobj import ListInstance
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_index_ext import HeterogeneousIndexType, NumericIndexType, RangeIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.series_indexing import SeriesIlocType
from bodo.hiframes.table import Table, TableType, decode_if_dict_table, get_table_data, set_table_data_codegen
from bodo.io import json_cpp
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_table_to_cpp_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.distributed_api import bcast_scalar
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_from_sequence
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.conversion import fix_arr_dtype, index_to_array
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import gen_const_tup, get_const_func_output_type, get_const_tup_vals
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, create_unsupported_overload, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_iterable_type, is_literal_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_str_arr_type, is_tuple_like_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
from bodo.utils.utils import is_null_pointer
_json_write = types.ExternalFunction('json_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.bool_,
    types.voidptr))
ll.add_symbol('json_write', json_cpp.json_write)


class DataFrameType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, data=None, index=None, columns=None, dist=None,
        is_table_format=False):
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        if index is None:
            index = RangeIndexType(types.none)
        self.index = index
        self.columns = columns
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        self.is_table_format = is_table_format
        if columns is None:
            assert is_table_format, 'Determining columns at runtime is only supported for DataFrame with table format'
            self.table_type = TableType(tuple(data[:-1]), True)
        else:
            self.table_type = TableType(data) if is_table_format else None
        super(DataFrameType, self).__init__(name=
            f'dataframe({data}, {index}, {columns}, {dist}, {is_table_format})'
            )

    def __str__(self):
        if not self.has_runtime_cols and len(self.columns) > 20:
            psh__iry = f'{len(self.data)} columns of types {set(self.data)}'
            ago__rccde = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({psh__iry}, {self.index}, {ago__rccde}, {self.dist}, {self.is_table_format})'
                )
        return super().__str__()

    def copy(self, data=None, index=None, columns=None, dist=None,
        is_table_format=None):
        if data is None:
            data = self.data
        if columns is None:
            columns = self.columns
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if is_table_format is None:
            is_table_format = self.is_table_format
        return DataFrameType(data, index, columns, dist, is_table_format)

    @property
    def has_runtime_cols(self):
        return self.columns is None

    @property
    def runtime_colname_typ(self):
        return self.data[-1] if self.has_runtime_cols else None

    @property
    def runtime_data_types(self):
        return self.data[:-1] if self.has_runtime_cols else self.data

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return (self.data, self.index, self.columns, self.dist, self.
            is_table_format)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if (isinstance(other, DataFrameType) and len(other.data) == len(
            self.data) and other.columns == self.columns and other.
            has_runtime_cols == self.has_runtime_cols):
            brs__xtpxz = (self.index if self.index == other.index else self
                .index.unify(typingctx, other.index))
            data = tuple(xwfr__wrtnw.unify(typingctx, ttr__sbsmj) if 
                xwfr__wrtnw != ttr__sbsmj else xwfr__wrtnw for xwfr__wrtnw,
                ttr__sbsmj in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if brs__xtpxz is not None and None not in data:
                return DataFrameType(data, brs__xtpxz, self.columns, dist,
                    self.is_table_format)
        if isinstance(other, DataFrameType) and len(self.data
            ) == 0 and not self.has_runtime_cols:
            return other

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, DataFrameType) and self.data == other.data and
            self.index == other.index and self.columns == other.columns and
            self.dist != other.dist and self.has_runtime_cols == other.
            has_runtime_cols):
            return Conversion.safe

    def is_precise(self):
        return all(xwfr__wrtnw.is_precise() for xwfr__wrtnw in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        kzxp__muc = self.columns.index(col_name)
        xbdrv__rcxwu = tuple(list(self.data[:kzxp__muc]) + [new_type] +
            list(self.data[kzxp__muc + 1:]))
        return DataFrameType(xbdrv__rcxwu, self.index, self.columns, self.
            dist, self.is_table_format)


def check_runtime_cols_unsupported(df, func_name):
    if isinstance(df, DataFrameType) and df.has_runtime_cols:
        raise BodoError(
            f'{func_name} on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information.'
            )


class DataFramePayloadType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        super(DataFramePayloadType, self).__init__(name=
            f'DataFramePayloadType({df_type})')

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFramePayloadType)
class DataFramePayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        data_typ = types.Tuple(fe_type.df_type.data)
        if fe_type.df_type.is_table_format:
            data_typ = types.Tuple([fe_type.df_type.table_type])
        oxz__qqad = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            oxz__qqad.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, oxz__qqad)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        oxz__qqad = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, oxz__qqad)


make_attribute_wrapper(DataFrameType, 'meminfo', '_meminfo')


@infer_getattr
class DataFrameAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])

    @bound_function('df.head')
    def resolve_head(self, df, args, kws):
        func_name = 'DataFrame.head'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        rakd__lqdce = 'n',
        altp__vekqz = {'n': 5}
        ngyfz__uxy, dovc__nlhl = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, rakd__lqdce, altp__vekqz)
        kaqdn__ovgf = dovc__nlhl[0]
        if not is_overload_int(kaqdn__ovgf):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        svygb__rxx = df.copy(is_table_format=False)
        return svygb__rxx(*dovc__nlhl).replace(pysig=ngyfz__uxy)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        lqi__shij = (df,) + args
        rakd__lqdce = 'df', 'method', 'min_periods'
        altp__vekqz = {'method': 'pearson', 'min_periods': 1}
        vqy__bte = 'method',
        ngyfz__uxy, dovc__nlhl = bodo.utils.typing.fold_typing_args(func_name,
            lqi__shij, kws, rakd__lqdce, altp__vekqz, vqy__bte)
        txehl__xyhaw = dovc__nlhl[2]
        if not is_overload_int(txehl__xyhaw):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        bhz__njph = []
        flxj__kpz = []
        for xnvss__xxnh, bgg__sfbln in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(bgg__sfbln.dtype):
                bhz__njph.append(xnvss__xxnh)
                flxj__kpz.append(types.Array(types.float64, 1, 'A'))
        if len(bhz__njph) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        flxj__kpz = tuple(flxj__kpz)
        bhz__njph = tuple(bhz__njph)
        index_typ = bodo.utils.typing.type_col_to_index(bhz__njph)
        svygb__rxx = DataFrameType(flxj__kpz, index_typ, bhz__njph)
        return svygb__rxx(*dovc__nlhl).replace(pysig=ngyfz__uxy)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        hva__wzzfy = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        bprxa__ccbfw = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        qalzj__nwuu = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        usnzr__qucze = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        dmbpr__axuki = dict(raw=bprxa__ccbfw, result_type=qalzj__nwuu)
        ajurd__invt = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', dmbpr__axuki, ajurd__invt,
            package_name='pandas', module_name='DataFrame')
        dvrv__ilve = True
        if types.unliteral(hva__wzzfy) == types.unicode_type:
            if not is_overload_constant_str(hva__wzzfy):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            dvrv__ilve = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        ppiww__grs = get_overload_const_int(axis)
        if dvrv__ilve and ppiww__grs != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif ppiww__grs not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        cnony__sknx = []
        for arr_typ in df.data:
            espkk__udoux = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            gfdc__qowui = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(espkk__udoux), types.int64), {}
                ).return_type
            cnony__sknx.append(gfdc__qowui)
        yvun__wfgtw = types.none
        skap__eiz = HeterogeneousIndexType(types.BaseTuple.from_types(tuple
            (types.literal(xnvss__xxnh) for xnvss__xxnh in df.columns)), None)
        esx__uxw = types.BaseTuple.from_types(cnony__sknx)
        vaacg__cnz = types.Tuple([types.bool_] * len(esx__uxw))
        igzg__qurgy = bodo.NullableTupleType(esx__uxw, vaacg__cnz)
        iyfk__awi = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if iyfk__awi == types.NPDatetime('ns'):
            iyfk__awi = bodo.pd_timestamp_type
        if iyfk__awi == types.NPTimedelta('ns'):
            iyfk__awi = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(esx__uxw):
            yct__spbkj = HeterogeneousSeriesType(igzg__qurgy, skap__eiz,
                iyfk__awi)
        else:
            yct__spbkj = SeriesType(esx__uxw.dtype, igzg__qurgy, skap__eiz,
                iyfk__awi)
        qfoo__tmpwt = yct__spbkj,
        if usnzr__qucze is not None:
            qfoo__tmpwt += tuple(usnzr__qucze.types)
        try:
            if not dvrv__ilve:
                ywug__hsm = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(hva__wzzfy), self.context,
                    'DataFrame.apply', axis if ppiww__grs == 1 else None)
            else:
                ywug__hsm = get_const_func_output_type(hva__wzzfy,
                    qfoo__tmpwt, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as vdtjl__yuvor:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                vdtjl__yuvor))
        if dvrv__ilve:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(ywug__hsm, (SeriesType, HeterogeneousSeriesType)
                ) and ywug__hsm.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(ywug__hsm, HeterogeneousSeriesType):
                osutq__ouj, mnua__pfqj = ywug__hsm.const_info
                if isinstance(ywug__hsm.data, bodo.libs.nullable_tuple_ext.
                    NullableTupleType):
                    ynvi__ddqy = ywug__hsm.data.tuple_typ.types
                elif isinstance(ywug__hsm.data, types.Tuple):
                    ynvi__ddqy = ywug__hsm.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                uce__ggo = tuple(to_nullable_type(dtype_to_array_type(
                    hcghy__fxy)) for hcghy__fxy in ynvi__ddqy)
                nnial__zqsa = DataFrameType(uce__ggo, df.index, mnua__pfqj)
            elif isinstance(ywug__hsm, SeriesType):
                awxcq__afiy, mnua__pfqj = ywug__hsm.const_info
                uce__ggo = tuple(to_nullable_type(dtype_to_array_type(
                    ywug__hsm.dtype)) for osutq__ouj in range(awxcq__afiy))
                nnial__zqsa = DataFrameType(uce__ggo, df.index, mnua__pfqj)
            else:
                sxdgj__cfso = get_udf_out_arr_type(ywug__hsm)
                nnial__zqsa = SeriesType(sxdgj__cfso.dtype, sxdgj__cfso, df
                    .index, None)
        else:
            nnial__zqsa = ywug__hsm
        vpj__ylxx = ', '.join("{} = ''".format(xwfr__wrtnw) for xwfr__wrtnw in
            kws.keys())
        hhcaj__zytxc = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {vpj__ylxx}):
"""
        hhcaj__zytxc += '    pass\n'
        ynpu__vztt = {}
        exec(hhcaj__zytxc, {}, ynpu__vztt)
        klws__hvq = ynpu__vztt['apply_stub']
        ngyfz__uxy = numba.core.utils.pysignature(klws__hvq)
        hoa__gxb = (hva__wzzfy, axis, bprxa__ccbfw, qalzj__nwuu, usnzr__qucze
            ) + tuple(kws.values())
        return signature(nnial__zqsa, *hoa__gxb).replace(pysig=ngyfz__uxy)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        rakd__lqdce = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        altp__vekqz = {'x': None, 'y': None, 'kind': 'line', 'figsize':
            None, 'ax': None, 'subplots': False, 'sharex': None, 'sharey': 
            False, 'layout': None, 'use_index': True, 'title': None, 'grid':
            None, 'legend': True, 'style': None, 'logx': False, 'logy': 
            False, 'loglog': False, 'xticks': None, 'yticks': None, 'xlim':
            None, 'ylim': None, 'rot': None, 'fontsize': None, 'colormap':
            None, 'table': False, 'yerr': None, 'xerr': None, 'secondary_y':
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        vqy__bte = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        ngyfz__uxy, dovc__nlhl = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, rakd__lqdce, altp__vekqz, vqy__bte)
        iqrn__qsb = dovc__nlhl[2]
        if not is_overload_constant_str(iqrn__qsb):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        ingz__vkj = dovc__nlhl[0]
        if not is_overload_none(ingz__vkj) and not (is_overload_int(
            ingz__vkj) or is_overload_constant_str(ingz__vkj)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(ingz__vkj):
            adf__ixmbh = get_overload_const_str(ingz__vkj)
            if adf__ixmbh not in df.columns:
                raise BodoError(f'{func_name}: {adf__ixmbh} column not found.')
        elif is_overload_int(ingz__vkj):
            loqri__hojr = get_overload_const_int(ingz__vkj)
            if loqri__hojr > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {loqri__hojr} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            ingz__vkj = df.columns[ingz__vkj]
        zqcsc__evcgi = dovc__nlhl[1]
        if not is_overload_none(zqcsc__evcgi) and not (is_overload_int(
            zqcsc__evcgi) or is_overload_constant_str(zqcsc__evcgi)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(zqcsc__evcgi):
            qyq__fco = get_overload_const_str(zqcsc__evcgi)
            if qyq__fco not in df.columns:
                raise BodoError(f'{func_name}: {qyq__fco} column not found.')
        elif is_overload_int(zqcsc__evcgi):
            ijeo__cvqno = get_overload_const_int(zqcsc__evcgi)
            if ijeo__cvqno > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {ijeo__cvqno} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            zqcsc__evcgi = df.columns[zqcsc__evcgi]
        rchqw__lurzm = dovc__nlhl[3]
        if not is_overload_none(rchqw__lurzm) and not is_tuple_like_type(
            rchqw__lurzm):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        cuwp__qsi = dovc__nlhl[10]
        if not is_overload_none(cuwp__qsi) and not is_overload_constant_str(
            cuwp__qsi):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        hmpn__rrd = dovc__nlhl[12]
        if not is_overload_bool(hmpn__rrd):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        ynjvd__eekk = dovc__nlhl[17]
        if not is_overload_none(ynjvd__eekk) and not is_tuple_like_type(
            ynjvd__eekk):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        npup__jmwjq = dovc__nlhl[18]
        if not is_overload_none(npup__jmwjq) and not is_tuple_like_type(
            npup__jmwjq):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        krxhc__pcgj = dovc__nlhl[22]
        if not is_overload_none(krxhc__pcgj) and not is_overload_int(
            krxhc__pcgj):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        oix__whwq = dovc__nlhl[29]
        if not is_overload_none(oix__whwq) and not is_overload_constant_str(
            oix__whwq):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        jexpo__yqzvk = dovc__nlhl[30]
        if not is_overload_none(jexpo__yqzvk) and not is_overload_constant_str(
            jexpo__yqzvk):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        nbg__btmqd = types.List(types.mpl_line_2d_type)
        iqrn__qsb = get_overload_const_str(iqrn__qsb)
        if iqrn__qsb == 'scatter':
            if is_overload_none(ingz__vkj) and is_overload_none(zqcsc__evcgi):
                raise BodoError(
                    f'{func_name}: {iqrn__qsb} requires an x and y column.')
            elif is_overload_none(ingz__vkj):
                raise BodoError(
                    f'{func_name}: {iqrn__qsb} x column is missing.')
            elif is_overload_none(zqcsc__evcgi):
                raise BodoError(
                    f'{func_name}: {iqrn__qsb} y column is missing.')
            nbg__btmqd = types.mpl_path_collection_type
        elif iqrn__qsb != 'line':
            raise BodoError(f'{func_name}: {iqrn__qsb} plot is not supported.')
        return signature(nbg__btmqd, *dovc__nlhl).replace(pysig=ngyfz__uxy)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            ikgx__giv = df.columns.index(attr)
            arr_typ = df.data[ikgx__giv]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            afj__htop = []
            xbdrv__rcxwu = []
            vfkh__wkjt = False
            for i, qvnx__wxv in enumerate(df.columns):
                if qvnx__wxv[0] != attr:
                    continue
                vfkh__wkjt = True
                afj__htop.append(qvnx__wxv[1] if len(qvnx__wxv) == 2 else
                    qvnx__wxv[1:])
                xbdrv__rcxwu.append(df.data[i])
            if vfkh__wkjt:
                return DataFrameType(tuple(xbdrv__rcxwu), df.index, tuple(
                    afj__htop))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        pok__xpql = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(pok__xpql)
        return lambda tup, idx: tup[val_ind]


def decref_df_data(context, builder, payload, df_type):
    if df_type.is_table_format:
        context.nrt.decref(builder, df_type.table_type, builder.
            extract_value(payload.data, 0))
        context.nrt.decref(builder, df_type.index, payload.index)
        if df_type.has_runtime_cols:
            context.nrt.decref(builder, df_type.data[-1], payload.columns)
        return
    for i in range(len(df_type.data)):
        ecgc__egr = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], ecgc__egr)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    ael__qquc = builder.module
    dows__cwdfz = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    skr__mla = cgutils.get_or_insert_function(ael__qquc, dows__cwdfz, name=
        '.dtor.df.{}'.format(df_type))
    if not skr__mla.is_declaration:
        return skr__mla
    skr__mla.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(skr__mla.append_basic_block())
    kmdn__uzqg = skr__mla.args[0]
    vlltq__yzg = context.get_value_type(payload_type).as_pointer()
    sob__zwiq = builder.bitcast(kmdn__uzqg, vlltq__yzg)
    payload = context.make_helper(builder, payload_type, ref=sob__zwiq)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        fvskx__dafxs = context.get_python_api(builder)
        bweda__fjh = fvskx__dafxs.gil_ensure()
        fvskx__dafxs.decref(payload.parent)
        fvskx__dafxs.gil_release(bweda__fjh)
    builder.ret_void()
    return skr__mla


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    gedh__mzyak = cgutils.create_struct_proxy(payload_type)(context, builder)
    gedh__mzyak.data = data_tup
    gedh__mzyak.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        gedh__mzyak.columns = colnames
    nianq__ifq = context.get_value_type(payload_type)
    odgjj__jio = context.get_abi_sizeof(nianq__ifq)
    cyr__dish = define_df_dtor(context, builder, df_type, payload_type)
    zser__lvbh = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, odgjj__jio), cyr__dish)
    alo__lsk = context.nrt.meminfo_data(builder, zser__lvbh)
    sjpd__dax = builder.bitcast(alo__lsk, nianq__ifq.as_pointer())
    ejsez__cvgxl = cgutils.create_struct_proxy(df_type)(context, builder)
    ejsez__cvgxl.meminfo = zser__lvbh
    if parent is None:
        ejsez__cvgxl.parent = cgutils.get_null_value(ejsez__cvgxl.parent.type)
    else:
        ejsez__cvgxl.parent = parent
        gedh__mzyak.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            fvskx__dafxs = context.get_python_api(builder)
            bweda__fjh = fvskx__dafxs.gil_ensure()
            fvskx__dafxs.incref(parent)
            fvskx__dafxs.gil_release(bweda__fjh)
    builder.store(gedh__mzyak._getvalue(), sjpd__dax)
    return ejsez__cvgxl._getvalue()


@intrinsic
def init_runtime_cols_dataframe(typingctx, data_typ, index_typ,
    colnames_index_typ=None):
    assert isinstance(data_typ, types.BaseTuple) and isinstance(data_typ.
        dtype, TableType
        ) and data_typ.dtype.has_runtime_cols, 'init_runtime_cols_dataframe must be called with a table that determines columns at runtime.'
    assert bodo.hiframes.pd_index_ext.is_pd_index_type(colnames_index_typ
        ) or isinstance(colnames_index_typ, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType), 'Column names must be an index'
    if isinstance(data_typ.dtype.arr_types, types.UniTuple):
        mstkw__ujnnb = [data_typ.dtype.arr_types.dtype] * len(data_typ.
            dtype.arr_types)
    else:
        mstkw__ujnnb = [hcghy__fxy for hcghy__fxy in data_typ.dtype.arr_types]
    rpa__rbz = DataFrameType(tuple(mstkw__ujnnb + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        zofm__ufgoo = construct_dataframe(context, builder, df_type,
            data_tup, index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return zofm__ufgoo
    sig = signature(rpa__rbz, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    awxcq__afiy = len(data_tup_typ.types)
    if awxcq__afiy == 0:
        column_names = ()
    elif isinstance(col_names_typ, types.TypeRef):
        column_names = col_names_typ.instance_type.columns
    else:
        column_names = get_const_tup_vals(col_names_typ)
    if awxcq__afiy == 1 and isinstance(data_tup_typ.types[0], TableType):
        awxcq__afiy = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == awxcq__afiy, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    jyaw__mbtzk = data_tup_typ.types
    if awxcq__afiy != 0 and isinstance(data_tup_typ.types[0], TableType):
        jyaw__mbtzk = data_tup_typ.types[0].arr_types
        is_table_format = True
    rpa__rbz = DataFrameType(jyaw__mbtzk, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            djt__pgj = cgutils.create_struct_proxy(rpa__rbz.table_type)(context
                , builder, builder.extract_value(data_tup, 0))
            parent = djt__pgj.parent
        zofm__ufgoo = construct_dataframe(context, builder, df_type,
            data_tup, index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return zofm__ufgoo
    sig = signature(rpa__rbz, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        ejsez__cvgxl = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, ejsez__cvgxl.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        gedh__mzyak = get_dataframe_payload(context, builder, df_typ, args[0])
        lge__sbfm = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[lge__sbfm]
        if df_typ.is_table_format:
            djt__pgj = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(gedh__mzyak.data, 0))
            ynx__jria = df_typ.table_type.type_to_blk[arr_typ]
            ulqn__fcnel = getattr(djt__pgj, f'block_{ynx__jria}')
            laupx__higwc = ListInstance(context, builder, types.List(
                arr_typ), ulqn__fcnel)
            ndom__hue = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[lge__sbfm])
            ecgc__egr = laupx__higwc.getitem(ndom__hue)
        else:
            ecgc__egr = builder.extract_value(gedh__mzyak.data, lge__sbfm)
        ymaxt__svlv = cgutils.alloca_once_value(builder, ecgc__egr)
        pnm__bxvl = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, ymaxt__svlv, pnm__bxvl)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    zser__lvbh = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, zser__lvbh)
    vlltq__yzg = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, vlltq__yzg)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    rpa__rbz = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        rpa__rbz = types.Tuple([TableType(df_typ.data)])
    sig = signature(rpa__rbz, df_typ)

    def codegen(context, builder, signature, args):
        gedh__mzyak = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            gedh__mzyak.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        gedh__mzyak = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index,
            gedh__mzyak.index)
    rpa__rbz = df_typ.index
    sig = signature(rpa__rbz, df_typ)
    return sig, codegen


def get_dataframe_data(df, i):
    return df[i]


@infer_global(get_dataframe_data)
class GetDataFrameDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        if not is_overload_constant_int(args[1]):
            raise_bodo_error(
                'Selecting a DataFrame column requires a constant column label'
                )
        df = args[0]
        check_runtime_cols_unsupported(df, 'get_dataframe_data')
        i = get_overload_const_int(args[1])
        svygb__rxx = df.data[i]
        return svygb__rxx(*args)


GetDataFrameDataInfer.prefer_literal = True


def get_dataframe_data_impl(df, i):
    if df.is_table_format:

        def _impl(df, i):
            if has_parent(df) and _column_needs_unboxing(df, i):
                bodo.hiframes.boxing.unbox_dataframe_column(df, i)
            return get_table_data(_get_dataframe_data(df)[0], i)
        return _impl

    def _impl(df, i):
        if has_parent(df) and _column_needs_unboxing(df, i):
            bodo.hiframes.boxing.unbox_dataframe_column(df, i)
        return _get_dataframe_data(df)[i]
    return _impl


@intrinsic
def get_dataframe_table(typingctx, df_typ=None):
    assert df_typ.is_table_format, 'get_dataframe_table() expects table format'

    def codegen(context, builder, signature, args):
        gedh__mzyak = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(gedh__mzyak.data, 0))
    return df_typ.table_type(df_typ), codegen


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        gedh__mzyak = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, gedh__mzyak.columns)
    return df_typ.runtime_colname_typ(df_typ), codegen


@lower_builtin(get_dataframe_data, DataFrameType, types.IntegerLiteral)
def lower_get_dataframe_data(context, builder, sig, args):
    impl = get_dataframe_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_dataframe_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_index',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_table',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func


def alias_ext_init_dataframe(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 3
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_dataframe',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_init_dataframe


def init_dataframe_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 3 and not kws
    data_tup = args[0]
    index = args[1]
    esx__uxw = self.typemap[data_tup.name]
    if any(is_tuple_like_type(hcghy__fxy) for hcghy__fxy in esx__uxw.types):
        return None
    if equiv_set.has_shape(data_tup):
        hynh__vjlr = equiv_set.get_shape(data_tup)
        if len(hynh__vjlr) > 1:
            equiv_set.insert_equiv(*hynh__vjlr)
        if len(hynh__vjlr) > 0:
            skap__eiz = self.typemap[index.name]
            if not isinstance(skap__eiz, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(hynh__vjlr[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(hynh__vjlr[0], len(
                hynh__vjlr)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    pyqr__tyiab = args[0]
    data_types = self.typemap[pyqr__tyiab.name].data
    if any(is_tuple_like_type(hcghy__fxy) for hcghy__fxy in data_types):
        return None
    if equiv_set.has_shape(pyqr__tyiab):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            pyqr__tyiab)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    pyqr__tyiab = args[0]
    skap__eiz = self.typemap[pyqr__tyiab.name].index
    if isinstance(skap__eiz, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(pyqr__tyiab):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            pyqr__tyiab)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    pyqr__tyiab = args[0]
    if equiv_set.has_shape(pyqr__tyiab):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            pyqr__tyiab), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    pyqr__tyiab = args[0]
    if equiv_set.has_shape(pyqr__tyiab):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            pyqr__tyiab)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    lge__sbfm = get_overload_const_int(c_ind_typ)
    if df_typ.data[lge__sbfm] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        diilt__hgch, osutq__ouj, glel__hxdh = args
        gedh__mzyak = get_dataframe_payload(context, builder, df_typ,
            diilt__hgch)
        if df_typ.is_table_format:
            djt__pgj = cgutils.create_struct_proxy(df_typ.table_type)(context,
                builder, builder.extract_value(gedh__mzyak.data, 0))
            ynx__jria = df_typ.table_type.type_to_blk[arr_typ]
            ulqn__fcnel = getattr(djt__pgj, f'block_{ynx__jria}')
            laupx__higwc = ListInstance(context, builder, types.List(
                arr_typ), ulqn__fcnel)
            ndom__hue = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[lge__sbfm])
            laupx__higwc.setitem(ndom__hue, glel__hxdh, True)
        else:
            ecgc__egr = builder.extract_value(gedh__mzyak.data, lge__sbfm)
            context.nrt.decref(builder, df_typ.data[lge__sbfm], ecgc__egr)
            gedh__mzyak.data = builder.insert_value(gedh__mzyak.data,
                glel__hxdh, lge__sbfm)
            context.nrt.incref(builder, arr_typ, glel__hxdh)
        ejsez__cvgxl = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=diilt__hgch)
        payload_type = DataFramePayloadType(df_typ)
        sob__zwiq = context.nrt.meminfo_data(builder, ejsez__cvgxl.meminfo)
        vlltq__yzg = context.get_value_type(payload_type).as_pointer()
        sob__zwiq = builder.bitcast(sob__zwiq, vlltq__yzg)
        builder.store(gedh__mzyak._getvalue(), sob__zwiq)
        return impl_ret_borrowed(context, builder, df_typ, diilt__hgch)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        rxhwi__tan = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        kkn__qpvkw = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=rxhwi__tan)
        ygswp__gdzbt = get_dataframe_payload(context, builder, df_typ,
            rxhwi__tan)
        ejsez__cvgxl = construct_dataframe(context, builder, signature.
            return_type, ygswp__gdzbt.data, index_val, kkn__qpvkw.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), ygswp__gdzbt.data)
        return ejsez__cvgxl
    rpa__rbz = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(rpa__rbz, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    awxcq__afiy = len(df_type.columns)
    ldt__bqaz = awxcq__afiy
    btoh__ehge = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    upzue__ufahy = col_name not in df_type.columns
    lge__sbfm = awxcq__afiy
    if upzue__ufahy:
        btoh__ehge += arr_type,
        column_names += col_name,
        ldt__bqaz += 1
    else:
        lge__sbfm = df_type.columns.index(col_name)
        btoh__ehge = tuple(arr_type if i == lge__sbfm else btoh__ehge[i] for
            i in range(awxcq__afiy))

    def codegen(context, builder, signature, args):
        diilt__hgch, osutq__ouj, glel__hxdh = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, diilt__hgch)
        hxy__tgtg = cgutils.create_struct_proxy(df_type)(context, builder,
            value=diilt__hgch)
        if df_type.is_table_format:
            jov__qqn = df_type.table_type
            qsnx__usc = builder.extract_value(in_dataframe_payload.data, 0)
            boc__csph = TableType(btoh__ehge)
            lpye__zgmhm = set_table_data_codegen(context, builder, jov__qqn,
                qsnx__usc, boc__csph, arr_type, glel__hxdh, lge__sbfm,
                upzue__ufahy)
            data_tup = context.make_tuple(builder, types.Tuple([boc__csph]),
                [lpye__zgmhm])
        else:
            jyaw__mbtzk = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != lge__sbfm else glel__hxdh) for i in range(
                awxcq__afiy)]
            if upzue__ufahy:
                jyaw__mbtzk.append(glel__hxdh)
            for pyqr__tyiab, ywd__nnuge in zip(jyaw__mbtzk, btoh__ehge):
                context.nrt.incref(builder, ywd__nnuge, pyqr__tyiab)
            data_tup = context.make_tuple(builder, types.Tuple(btoh__ehge),
                jyaw__mbtzk)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        jvph__yghn = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, hxy__tgtg.parent, None)
        if not upzue__ufahy and arr_type == df_type.data[lge__sbfm]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            sob__zwiq = context.nrt.meminfo_data(builder, hxy__tgtg.meminfo)
            vlltq__yzg = context.get_value_type(payload_type).as_pointer()
            sob__zwiq = builder.bitcast(sob__zwiq, vlltq__yzg)
            tkkl__fsjb = get_dataframe_payload(context, builder, df_type,
                jvph__yghn)
            builder.store(tkkl__fsjb._getvalue(), sob__zwiq)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, boc__csph, builder.
                    extract_value(data_tup, 0))
            else:
                for pyqr__tyiab, ywd__nnuge in zip(jyaw__mbtzk, btoh__ehge):
                    context.nrt.incref(builder, ywd__nnuge, pyqr__tyiab)
        has_parent = cgutils.is_not_null(builder, hxy__tgtg.parent)
        with builder.if_then(has_parent):
            fvskx__dafxs = context.get_python_api(builder)
            bweda__fjh = fvskx__dafxs.gil_ensure()
            vykuy__lea = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, glel__hxdh)
            xnvss__xxnh = numba.core.pythonapi._BoxContext(context, builder,
                fvskx__dafxs, vykuy__lea)
            jyt__sdojp = xnvss__xxnh.pyapi.from_native_value(arr_type,
                glel__hxdh, xnvss__xxnh.env_manager)
            if isinstance(col_name, str):
                leudd__bvxy = context.insert_const_string(builder.module,
                    col_name)
                eav__rqhau = fvskx__dafxs.string_from_string(leudd__bvxy)
            else:
                assert isinstance(col_name, int)
                eav__rqhau = fvskx__dafxs.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            fvskx__dafxs.object_setitem(hxy__tgtg.parent, eav__rqhau,
                jyt__sdojp)
            fvskx__dafxs.decref(jyt__sdojp)
            fvskx__dafxs.decref(eav__rqhau)
            fvskx__dafxs.gil_release(bweda__fjh)
        return jvph__yghn
    rpa__rbz = DataFrameType(btoh__ehge, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(rpa__rbz, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    awxcq__afiy = len(pyval.columns)
    jyaw__mbtzk = []
    for i in range(awxcq__afiy):
        iflfb__ddsn = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            jyt__sdojp = iflfb__ddsn.array
        else:
            jyt__sdojp = iflfb__ddsn.values
        jyaw__mbtzk.append(jyt__sdojp)
    jyaw__mbtzk = tuple(jyaw__mbtzk)
    if df_type.is_table_format:
        djt__pgj = context.get_constant_generic(builder, df_type.table_type,
            Table(jyaw__mbtzk))
        data_tup = lir.Constant.literal_struct([djt__pgj])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], qvnx__wxv) for i,
            qvnx__wxv in enumerate(jyaw__mbtzk)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    urkd__lsz = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, urkd__lsz])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    nxwmu__dbk = context.get_constant(types.int64, -1)
    mhkj__dbxgs = context.get_constant_null(types.voidptr)
    zser__lvbh = lir.Constant.literal_struct([nxwmu__dbk, mhkj__dbxgs,
        mhkj__dbxgs, payload, nxwmu__dbk])
    zser__lvbh = cgutils.global_constant(builder, '.const.meminfo', zser__lvbh
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([zser__lvbh, urkd__lsz])


@lower_cast(DataFrameType, DataFrameType)
def cast_df_to_df(context, builder, fromty, toty, val):
    if (fromty.data == toty.data and fromty.index == toty.index and fromty.
        columns == toty.columns and fromty.is_table_format == toty.
        is_table_format and fromty.dist != toty.dist and fromty.
        has_runtime_cols == toty.has_runtime_cols):
        return val
    if not fromty.has_runtime_cols and not toty.has_runtime_cols and len(fromty
        .data) == 0 and len(toty.columns):
        return _cast_empty_df(context, builder, toty)
    if len(fromty.data) != len(toty.data) or fromty.data != toty.data and any(
        context.typing_context.unify_pairs(fromty.data[i], toty.data[i]) is
        None for i in range(len(fromty.data))
        ) or fromty.has_runtime_cols != toty.has_runtime_cols:
        raise BodoError(f'Invalid dataframe cast from {fromty} to {toty}')
    in_dataframe_payload = get_dataframe_payload(context, builder, fromty, val)
    if isinstance(fromty.index, RangeIndexType) and isinstance(toty.index,
        NumericIndexType):
        brs__xtpxz = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        brs__xtpxz = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, brs__xtpxz)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        xbdrv__rcxwu = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                xbdrv__rcxwu)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), xbdrv__rcxwu)
    elif not fromty.is_table_format and toty.is_table_format:
        xbdrv__rcxwu = _cast_df_data_to_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        xbdrv__rcxwu = _cast_df_data_to_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        xbdrv__rcxwu = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        xbdrv__rcxwu = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, xbdrv__rcxwu,
        brs__xtpxz, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    kzq__byrg = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        zugt__txsog = get_index_data_arr_types(toty.index)[0]
        fyao__ryry = bodo.utils.transform.get_type_alloc_counts(zugt__txsog
            ) - 1
        jhy__zgcxl = ', '.join('0' for osutq__ouj in range(fyao__ryry))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(jhy__zgcxl, ', ' if fyao__ryry == 1 else ''))
        kzq__byrg['index_arr_type'] = zugt__txsog
    sgb__ybf = []
    for i, arr_typ in enumerate(toty.data):
        fyao__ryry = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        jhy__zgcxl = ', '.join('0' for osutq__ouj in range(fyao__ryry))
        vedla__ylhy = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'
            .format(i, jhy__zgcxl, ', ' if fyao__ryry == 1 else ''))
        sgb__ybf.append(vedla__ylhy)
        kzq__byrg[f'arr_type{i}'] = arr_typ
    sgb__ybf = ', '.join(sgb__ybf)
    hhcaj__zytxc = 'def impl():\n'
    bmi__lmht = bodo.hiframes.dataframe_impl._gen_init_df(hhcaj__zytxc,
        toty.columns, sgb__ybf, index, kzq__byrg)
    df = context.compile_internal(builder, bmi__lmht, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    htu__duou = toty.table_type
    djt__pgj = cgutils.create_struct_proxy(htu__duou)(context, builder)
    djt__pgj.parent = in_dataframe_payload.parent
    for hcghy__fxy, ynx__jria in htu__duou.type_to_blk.items():
        msyl__dbrv = context.get_constant(types.int64, len(htu__duou.
            block_to_arr_ind[ynx__jria]))
        osutq__ouj, nme__czse = ListInstance.allocate_ex(context, builder,
            types.List(hcghy__fxy), msyl__dbrv)
        nme__czse.size = msyl__dbrv
        setattr(djt__pgj, f'block_{ynx__jria}', nme__czse.value)
    for i, hcghy__fxy in enumerate(fromty.data):
        wqb__bmhv = toty.data[i]
        if hcghy__fxy != wqb__bmhv:
            lhzuf__eju = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lhzuf__eju)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ecgc__egr = builder.extract_value(in_dataframe_payload.data, i)
        if hcghy__fxy != wqb__bmhv:
            mdxsh__pduev = context.cast(builder, ecgc__egr, hcghy__fxy,
                wqb__bmhv)
            dtasg__ysajm = False
        else:
            mdxsh__pduev = ecgc__egr
            dtasg__ysajm = True
        ynx__jria = htu__duou.type_to_blk[hcghy__fxy]
        ulqn__fcnel = getattr(djt__pgj, f'block_{ynx__jria}')
        laupx__higwc = ListInstance(context, builder, types.List(hcghy__fxy
            ), ulqn__fcnel)
        ndom__hue = context.get_constant(types.int64, htu__duou.
            block_offsets[i])
        laupx__higwc.setitem(ndom__hue, mdxsh__pduev, dtasg__ysajm)
    data_tup = context.make_tuple(builder, types.Tuple([htu__duou]), [
        djt__pgj._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    jyaw__mbtzk = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            lhzuf__eju = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lhzuf__eju)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            ecgc__egr = builder.extract_value(in_dataframe_payload.data, i)
            mdxsh__pduev = context.cast(builder, ecgc__egr, fromty.data[i],
                toty.data[i])
            dtasg__ysajm = False
        else:
            mdxsh__pduev = builder.extract_value(in_dataframe_payload.data, i)
            dtasg__ysajm = True
        if dtasg__ysajm:
            context.nrt.incref(builder, toty.data[i], mdxsh__pduev)
        jyaw__mbtzk.append(mdxsh__pduev)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), jyaw__mbtzk)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    jov__qqn = fromty.table_type
    qsnx__usc = cgutils.create_struct_proxy(jov__qqn)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    boc__csph = toty.table_type
    lpye__zgmhm = cgutils.create_struct_proxy(boc__csph)(context, builder)
    lpye__zgmhm.parent = in_dataframe_payload.parent
    for hcghy__fxy, ynx__jria in boc__csph.type_to_blk.items():
        msyl__dbrv = context.get_constant(types.int64, len(boc__csph.
            block_to_arr_ind[ynx__jria]))
        osutq__ouj, nme__czse = ListInstance.allocate_ex(context, builder,
            types.List(hcghy__fxy), msyl__dbrv)
        nme__czse.size = msyl__dbrv
        setattr(lpye__zgmhm, f'block_{ynx__jria}', nme__czse.value)
    for i in range(len(fromty.data)):
        omd__vhs = fromty.data[i]
        wqb__bmhv = toty.data[i]
        if omd__vhs != wqb__bmhv:
            lhzuf__eju = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lhzuf__eju)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ipovf__boj = jov__qqn.type_to_blk[omd__vhs]
        yzy__ebpx = getattr(qsnx__usc, f'block_{ipovf__boj}')
        autti__cwln = ListInstance(context, builder, types.List(omd__vhs),
            yzy__ebpx)
        kxrs__sgp = context.get_constant(types.int64, jov__qqn.block_offsets[i]
            )
        ecgc__egr = autti__cwln.getitem(kxrs__sgp)
        if omd__vhs != wqb__bmhv:
            mdxsh__pduev = context.cast(builder, ecgc__egr, omd__vhs, wqb__bmhv
                )
            dtasg__ysajm = False
        else:
            mdxsh__pduev = ecgc__egr
            dtasg__ysajm = True
        lyf__vqqq = boc__csph.type_to_blk[hcghy__fxy]
        nme__czse = getattr(lpye__zgmhm, f'block_{lyf__vqqq}')
        tmfj__zfxyq = ListInstance(context, builder, types.List(wqb__bmhv),
            nme__czse)
        wvinp__ghln = context.get_constant(types.int64, boc__csph.
            block_offsets[i])
        tmfj__zfxyq.setitem(wvinp__ghln, mdxsh__pduev, dtasg__ysajm)
    data_tup = context.make_tuple(builder, types.Tuple([boc__csph]), [
        lpye__zgmhm._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    htu__duou = fromty.table_type
    djt__pgj = cgutils.create_struct_proxy(htu__duou)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    jyaw__mbtzk = []
    for i, hcghy__fxy in enumerate(toty.data):
        omd__vhs = fromty.data[i]
        if hcghy__fxy != omd__vhs:
            lhzuf__eju = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lhzuf__eju)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ynx__jria = htu__duou.type_to_blk[hcghy__fxy]
        ulqn__fcnel = getattr(djt__pgj, f'block_{ynx__jria}')
        laupx__higwc = ListInstance(context, builder, types.List(hcghy__fxy
            ), ulqn__fcnel)
        ndom__hue = context.get_constant(types.int64, htu__duou.
            block_offsets[i])
        ecgc__egr = laupx__higwc.getitem(ndom__hue)
        if hcghy__fxy != omd__vhs:
            mdxsh__pduev = context.cast(builder, ecgc__egr, omd__vhs,
                hcghy__fxy)
            dtasg__ysajm = False
        else:
            mdxsh__pduev = ecgc__egr
            dtasg__ysajm = True
        if dtasg__ysajm:
            context.nrt.incref(builder, hcghy__fxy, mdxsh__pduev)
        jyaw__mbtzk.append(mdxsh__pduev)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), jyaw__mbtzk)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    aoanq__vhuzk, sgb__ybf, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    xdwh__twfk = gen_const_tup(aoanq__vhuzk)
    hhcaj__zytxc = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    hhcaj__zytxc += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(sgb__ybf, index_arg, xdwh__twfk))
    ynpu__vztt = {}
    exec(hhcaj__zytxc, {'bodo': bodo, 'np': np}, ynpu__vztt)
    sok__sfbj = ynpu__vztt['_init_df']
    return sok__sfbj


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    rpa__rbz = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(rpa__rbz, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    rpa__rbz = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ.
        index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(rpa__rbz, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    qle__ucd = ''
    if not is_overload_none(dtype):
        qle__ucd = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        awxcq__afiy = (len(data.types) - 1) // 2
        eeguj__ysdk = [hcghy__fxy.literal_value for hcghy__fxy in data.
            types[1:awxcq__afiy + 1]]
        data_val_types = dict(zip(eeguj__ysdk, data.types[awxcq__afiy + 1:]))
        jyaw__mbtzk = ['data[{}]'.format(i) for i in range(awxcq__afiy + 1,
            2 * awxcq__afiy + 1)]
        data_dict = dict(zip(eeguj__ysdk, jyaw__mbtzk))
        if is_overload_none(index):
            for i, hcghy__fxy in enumerate(data.types[awxcq__afiy + 1:]):
                if isinstance(hcghy__fxy, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(awxcq__afiy + 1 + i))
                    index_is_none = False
                    break
    elif is_overload_none(data):
        data_dict = {}
        data_val_types = {}
    else:
        if not (isinstance(data, types.Array) and data.ndim == 2):
            raise BodoError(
                'pd.DataFrame() only supports constant dictionary and array input'
                )
        if is_overload_none(columns):
            raise BodoError(
                "pd.DataFrame() 'columns' argument is required when an array is passed as data"
                )
        hmqi__eksfx = '.copy()' if copy else ''
        pguu__faxom = get_overload_const_list(columns)
        awxcq__afiy = len(pguu__faxom)
        data_val_types = {xnvss__xxnh: data.copy(ndim=1) for xnvss__xxnh in
            pguu__faxom}
        jyaw__mbtzk = ['data[:,{}]{}'.format(i, hmqi__eksfx) for i in range
            (awxcq__afiy)]
        data_dict = dict(zip(pguu__faxom, jyaw__mbtzk))
    if is_overload_none(columns):
        col_names = data_dict.keys()
    else:
        col_names = get_overload_const_list(columns)
    df_len = _get_df_len_from_info(data_dict, data_val_types, col_names,
        index_is_none, index_arg)
    _fill_null_arrays(data_dict, col_names, df_len, dtype)
    if index_is_none:
        if is_overload_none(data):
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_binary_str_index(bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0))'
                )
        else:
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, {}, 1, None)'
                .format(df_len))
    sgb__ybf = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[xnvss__xxnh], df_len, qle__ucd) for xnvss__xxnh in
        col_names))
    if len(col_names) == 0:
        sgb__ybf = '()'
    return col_names, sgb__ybf, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for xnvss__xxnh in col_names:
        if xnvss__xxnh in data_dict and is_iterable_type(data_val_types[
            xnvss__xxnh]):
            df_len = 'len({})'.format(data_dict[xnvss__xxnh])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(xnvss__xxnh in data_dict for xnvss__xxnh in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    obut__jbux = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for xnvss__xxnh in col_names:
        if xnvss__xxnh not in data_dict:
            data_dict[xnvss__xxnh] = obut__jbux


@infer_global(len)
class LenTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        if isinstance(args[0], (DataFrameType, bodo.TableType)):
            return types.int64(*args)


@lower_builtin(len, DataFrameType)
def table_len_lower(context, builder, sig, args):
    impl = df_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_len_overload(df):
    if not isinstance(df, DataFrameType):
        return
    if df.has_runtime_cols:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            hcghy__fxy = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(hcghy__fxy)
        return impl
    if len(df.columns) == 0:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
        return impl

    def impl(df):
        if is_null_pointer(df._meminfo):
            return 0
        return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 0))
    return impl


@infer_global(operator.getitem)
class GetItemTuple(AbstractTemplate):
    key = operator.getitem

    def generic(self, args, kws):
        tup, idx = args
        if not isinstance(tup, types.BaseTuple) or not isinstance(idx,
            types.IntegerLiteral):
            return
        zygif__xqui = idx.literal_value
        if isinstance(zygif__xqui, int):
            svygb__rxx = tup.types[zygif__xqui]
        elif isinstance(zygif__xqui, slice):
            svygb__rxx = types.BaseTuple.from_types(tup.types[zygif__xqui])
        return signature(svygb__rxx, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    pyqcr__yqa, idx = sig.args
    idx = idx.literal_value
    tup, osutq__ouj = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(pyqcr__yqa)
        if not 0 <= idx < len(pyqcr__yqa):
            raise IndexError('cannot index at %d in %s' % (idx, pyqcr__yqa))
        ykt__dqstd = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        fuo__zfhn = cgutils.unpack_tuple(builder, tup)[idx]
        ykt__dqstd = context.make_tuple(builder, sig.return_type, fuo__zfhn)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, ykt__dqstd)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, guz__uri, suffix_x, suffix_y,
            is_join, indicator, _bodo_na_equal, nwe__kgnp) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        agms__cqe = set(left_on) & set(right_on)
        rofi__fpld = set(left_df.columns) & set(right_df.columns)
        rjvk__ppvm = rofi__fpld - agms__cqe
        zkkrr__upxq = '$_bodo_index_' in left_on
        mmmf__xduvy = '$_bodo_index_' in right_on
        how = get_overload_const_str(guz__uri)
        tizq__blesv = how in {'left', 'outer'}
        cmy__dkaej = how in {'right', 'outer'}
        columns = []
        data = []
        if zkkrr__upxq:
            mmao__lfwl = bodo.utils.typing.get_index_data_arr_types(left_df
                .index)[0]
        else:
            mmao__lfwl = left_df.data[left_df.columns.index(left_on[0])]
        if mmmf__xduvy:
            sjysw__pmx = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            sjysw__pmx = right_df.data[right_df.columns.index(right_on[0])]
        if zkkrr__upxq and not mmmf__xduvy and not is_join.literal_value:
            ywi__znar = right_on[0]
            if ywi__znar in left_df.columns:
                columns.append(ywi__znar)
                if (sjysw__pmx == bodo.dict_str_arr_type and mmao__lfwl ==
                    bodo.string_array_type):
                    kqwvh__wmveq = bodo.string_array_type
                else:
                    kqwvh__wmveq = sjysw__pmx
                data.append(kqwvh__wmveq)
        if mmmf__xduvy and not zkkrr__upxq and not is_join.literal_value:
            pudb__jsw = left_on[0]
            if pudb__jsw in right_df.columns:
                columns.append(pudb__jsw)
                if (mmao__lfwl == bodo.dict_str_arr_type and sjysw__pmx ==
                    bodo.string_array_type):
                    kqwvh__wmveq = bodo.string_array_type
                else:
                    kqwvh__wmveq = mmao__lfwl
                data.append(kqwvh__wmveq)
        for omd__vhs, iflfb__ddsn in zip(left_df.data, left_df.columns):
            columns.append(str(iflfb__ddsn) + suffix_x.literal_value if 
                iflfb__ddsn in rjvk__ppvm else iflfb__ddsn)
            if iflfb__ddsn in agms__cqe:
                if omd__vhs == bodo.dict_str_arr_type:
                    omd__vhs = right_df.data[right_df.columns.index(
                        iflfb__ddsn)]
                data.append(omd__vhs)
            else:
                if (omd__vhs == bodo.dict_str_arr_type and iflfb__ddsn in
                    left_on):
                    if mmmf__xduvy:
                        omd__vhs = sjysw__pmx
                    else:
                        wqr__nen = left_on.index(iflfb__ddsn)
                        ahiw__htzk = right_on[wqr__nen]
                        omd__vhs = right_df.data[right_df.columns.index(
                            ahiw__htzk)]
                if cmy__dkaej:
                    omd__vhs = to_nullable_type(omd__vhs)
                data.append(omd__vhs)
        for omd__vhs, iflfb__ddsn in zip(right_df.data, right_df.columns):
            if iflfb__ddsn not in agms__cqe:
                columns.append(str(iflfb__ddsn) + suffix_y.literal_value if
                    iflfb__ddsn in rjvk__ppvm else iflfb__ddsn)
                if (omd__vhs == bodo.dict_str_arr_type and iflfb__ddsn in
                    right_on):
                    if zkkrr__upxq:
                        omd__vhs = mmao__lfwl
                    else:
                        wqr__nen = right_on.index(iflfb__ddsn)
                        rewc__oczyn = left_on[wqr__nen]
                        omd__vhs = left_df.data[left_df.columns.index(
                            rewc__oczyn)]
                if tizq__blesv:
                    omd__vhs = to_nullable_type(omd__vhs)
                data.append(omd__vhs)
        mshpb__igneu = get_overload_const_bool(indicator)
        if mshpb__igneu:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        if zkkrr__upxq and mmmf__xduvy and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif zkkrr__upxq and not mmmf__xduvy:
            index_typ = right_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif mmmf__xduvy and not zkkrr__upxq:
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        mcade__bvz = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(mcade__bvz, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    ejsez__cvgxl = cgutils.create_struct_proxy(sig.return_type)(context,
        builder)
    return ejsez__cvgxl._getvalue()


@overload(pd.concat, inline='always', no_unliteral=True)
def concat_overload(objs, axis=0, join='outer', join_axes=None,
    ignore_index=False, keys=None, levels=None, names=None,
    verify_integrity=False, sort=None, copy=True):
    if not is_overload_constant_int(axis):
        raise BodoError("pd.concat(): 'axis' should be a constant integer")
    if not is_overload_constant_bool(ignore_index):
        raise BodoError(
            "pd.concat(): 'ignore_index' should be a constant boolean")
    axis = get_overload_const_int(axis)
    ignore_index = is_overload_true(ignore_index)
    dmbpr__axuki = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    altp__vekqz = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', dmbpr__axuki, altp__vekqz,
        package_name='pandas', module_name='General')
    hhcaj__zytxc = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        jcyk__rpcz = 0
        sgb__ybf = []
        names = []
        for i, fyd__mxo in enumerate(objs.types):
            assert isinstance(fyd__mxo, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(fyd__mxo, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(fyd__mxo,
                'pandas.concat()')
            if isinstance(fyd__mxo, SeriesType):
                names.append(str(jcyk__rpcz))
                jcyk__rpcz += 1
                sgb__ybf.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(fyd__mxo.columns)
                for zcw__pgnwz in range(len(fyd__mxo.data)):
                    sgb__ybf.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, zcw__pgnwz))
        return bodo.hiframes.dataframe_impl._gen_init_df(hhcaj__zytxc,
            names, ', '.join(sgb__ybf), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(hcghy__fxy, DataFrameType) for hcghy__fxy in
            objs.types)
        uah__eeri = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            uah__eeri.extend(df.columns)
        uah__eeri = list(dict.fromkeys(uah__eeri).keys())
        mstkw__ujnnb = {}
        for jcyk__rpcz, xnvss__xxnh in enumerate(uah__eeri):
            for df in objs.types:
                if xnvss__xxnh in df.columns:
                    mstkw__ujnnb['arr_typ{}'.format(jcyk__rpcz)] = df.data[df
                        .columns.index(xnvss__xxnh)]
                    break
        assert len(mstkw__ujnnb) == len(uah__eeri)
        uhwo__loci = []
        for jcyk__rpcz, xnvss__xxnh in enumerate(uah__eeri):
            args = []
            for i, df in enumerate(objs.types):
                if xnvss__xxnh in df.columns:
                    lge__sbfm = df.columns.index(xnvss__xxnh)
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, lge__sbfm))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, jcyk__rpcz))
            hhcaj__zytxc += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(jcyk__rpcz, ', '.join(args)))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(A0), 1, None)'
                )
        else:
            index = (
                """bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)) if len(objs[i].
                columns) > 0)))
        return bodo.hiframes.dataframe_impl._gen_init_df(hhcaj__zytxc,
            uah__eeri, ', '.join('A{}'.format(i) for i in range(len(
            uah__eeri))), index, mstkw__ujnnb)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(hcghy__fxy, SeriesType) for hcghy__fxy in
            objs.types)
        hhcaj__zytxc += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            hhcaj__zytxc += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            hhcaj__zytxc += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        hhcaj__zytxc += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        ynpu__vztt = {}
        exec(hhcaj__zytxc, {'bodo': bodo, 'np': np, 'numba': numba}, ynpu__vztt
            )
        return ynpu__vztt['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for jcyk__rpcz, xnvss__xxnh in enumerate(df_type.columns):
            hhcaj__zytxc += '  arrs{} = []\n'.format(jcyk__rpcz)
            hhcaj__zytxc += '  for i in range(len(objs)):\n'
            hhcaj__zytxc += '    df = objs[i]\n'
            hhcaj__zytxc += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(jcyk__rpcz))
            hhcaj__zytxc += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(jcyk__rpcz))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            hhcaj__zytxc += '  arrs_index = []\n'
            hhcaj__zytxc += '  for i in range(len(objs)):\n'
            hhcaj__zytxc += '    df = objs[i]\n'
            hhcaj__zytxc += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(hhcaj__zytxc,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        hhcaj__zytxc += '  arrs = []\n'
        hhcaj__zytxc += '  for i in range(len(objs)):\n'
        hhcaj__zytxc += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        hhcaj__zytxc += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            hhcaj__zytxc += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            hhcaj__zytxc += '  arrs_index = []\n'
            hhcaj__zytxc += '  for i in range(len(objs)):\n'
            hhcaj__zytxc += '    S = objs[i]\n'
            hhcaj__zytxc += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            hhcaj__zytxc += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        hhcaj__zytxc += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        ynpu__vztt = {}
        exec(hhcaj__zytxc, {'bodo': bodo, 'np': np, 'numba': numba}, ynpu__vztt
            )
        return ynpu__vztt['impl']
    raise BodoError('pd.concat(): input type {} not supported yet'.format(objs)
        )


def sort_values_dummy(df, by, ascending, inplace, na_position):
    return df.sort_values(by, ascending=ascending, inplace=inplace,
        na_position=na_position)


@infer_global(sort_values_dummy)
class SortDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, by, ascending, inplace, na_position = args
        index = df.index
        if isinstance(index, bodo.hiframes.pd_index_ext.RangeIndexType):
            index = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64)
        rpa__rbz = df.copy(index=index, is_table_format=False)
        return signature(rpa__rbz, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    uvlb__zrws = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return uvlb__zrws._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    dmbpr__axuki = dict(index=index, name=name)
    altp__vekqz = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', dmbpr__axuki,
        altp__vekqz, package_name='pandas', module_name='DataFrame')

    def _impl(df, index=True, name='Pandas'):
        return bodo.hiframes.pd_dataframe_ext.itertuples_dummy(df)
    return _impl


def itertuples_dummy(df):
    return df


@infer_global(itertuples_dummy)
class ItertuplesDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, = args
        assert 'Index' not in df.columns
        columns = ('Index',) + df.columns
        mstkw__ujnnb = (types.Array(types.int64, 1, 'C'),) + df.data
        llkfm__umbli = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, mstkw__ujnnb)
        return signature(llkfm__umbli, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    uvlb__zrws = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return uvlb__zrws._getvalue()


def query_dummy(df, expr):
    return df.eval(expr)


@infer_global(query_dummy)
class QueryDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=RangeIndexType(types
            .none)), *args)


@lower_builtin(query_dummy, types.VarArg(types.Any))
def lower_query_dummy(context, builder, sig, args):
    uvlb__zrws = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return uvlb__zrws._getvalue()


def val_isin_dummy(S, vals):
    return S in vals


def val_notin_dummy(S, vals):
    return S not in vals


@infer_global(val_isin_dummy)
@infer_global(val_notin_dummy)
class ValIsinTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=args[0].index), *args)


@lower_builtin(val_isin_dummy, types.VarArg(types.Any))
@lower_builtin(val_notin_dummy, types.VarArg(types.Any))
def lower_val_isin_dummy(context, builder, sig, args):
    uvlb__zrws = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return uvlb__zrws._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True, parallel
    =False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    ncjmn__okmgv = get_overload_const_bool(check_duplicates)
    cnyv__ogltg = not is_overload_none(value_names)
    gwwp__efmb = isinstance(values_tup, types.UniTuple)
    if gwwp__efmb:
        brwgq__mnbmm = [to_nullable_type(values_tup.dtype)]
    else:
        brwgq__mnbmm = [to_nullable_type(ywd__nnuge) for ywd__nnuge in
            values_tup]
    hhcaj__zytxc = 'def impl(\n'
    hhcaj__zytxc += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, parallel=False
"""
    hhcaj__zytxc += '):\n'
    hhcaj__zytxc += '    if parallel:\n'
    gevqo__wjcqg = ', '.join([f'array_to_info(index_tup[{i}])' for i in
        range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    hhcaj__zytxc += f'        info_list = [{gevqo__wjcqg}]\n'
    hhcaj__zytxc += '        cpp_table = arr_info_list_to_table(info_list)\n'
    hhcaj__zytxc += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
    jmqye__mppc = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    yeb__prmo = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    jcetn__gjhr = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    hhcaj__zytxc += f'        index_tup = ({jmqye__mppc},)\n'
    hhcaj__zytxc += f'        columns_tup = ({yeb__prmo},)\n'
    hhcaj__zytxc += f'        values_tup = ({jcetn__gjhr},)\n'
    hhcaj__zytxc += '        delete_table(cpp_table)\n'
    hhcaj__zytxc += '        delete_table(out_cpp_table)\n'
    hhcaj__zytxc += '    columns_arr = columns_tup[0]\n'
    if gwwp__efmb:
        hhcaj__zytxc += '    values_arrs = [arr for arr in values_tup]\n'
    hhcaj__zytxc += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    hhcaj__zytxc += '        index_tup\n'
    hhcaj__zytxc += '    )\n'
    hhcaj__zytxc += '    n_rows = len(unique_index_arr_tup[0])\n'
    hhcaj__zytxc += '    num_values_arrays = len(values_tup)\n'
    hhcaj__zytxc += '    n_unique_pivots = len(pivot_values)\n'
    if gwwp__efmb:
        hhcaj__zytxc += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        hhcaj__zytxc += '    n_cols = n_unique_pivots\n'
    hhcaj__zytxc += '    col_map = {}\n'
    hhcaj__zytxc += '    for i in range(n_unique_pivots):\n'
    hhcaj__zytxc += (
        '        if bodo.libs.array_kernels.isna(pivot_values, i):\n')
    hhcaj__zytxc += '            raise ValueError(\n'
    hhcaj__zytxc += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    hhcaj__zytxc += '            )\n'
    hhcaj__zytxc += '        col_map[pivot_values[i]] = i\n'
    olsgt__aulz = False
    for i, fdlv__eyog in enumerate(brwgq__mnbmm):
        if is_str_arr_type(fdlv__eyog):
            olsgt__aulz = True
            hhcaj__zytxc += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            hhcaj__zytxc += (
                f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n')
    if olsgt__aulz:
        if ncjmn__okmgv:
            hhcaj__zytxc += '    nbytes = (n_rows + 7) >> 3\n'
            hhcaj__zytxc += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        hhcaj__zytxc += '    for i in range(len(columns_arr)):\n'
        hhcaj__zytxc += '        col_name = columns_arr[i]\n'
        hhcaj__zytxc += '        pivot_idx = col_map[col_name]\n'
        hhcaj__zytxc += '        row_idx = row_vector[i]\n'
        if ncjmn__okmgv:
            hhcaj__zytxc += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            hhcaj__zytxc += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            hhcaj__zytxc += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            hhcaj__zytxc += '        else:\n'
            hhcaj__zytxc += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if gwwp__efmb:
            hhcaj__zytxc += '        for j in range(num_values_arrays):\n'
            hhcaj__zytxc += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            hhcaj__zytxc += '            len_arr = len_arrs_0[col_idx]\n'
            hhcaj__zytxc += '            values_arr = values_arrs[j]\n'
            hhcaj__zytxc += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            hhcaj__zytxc += (
                '                len_arr[row_idx] = len(values_arr[i])\n')
            hhcaj__zytxc += (
                '                total_lens_0[col_idx] += len(values_arr[i])\n'
                )
        else:
            for i, fdlv__eyog in enumerate(brwgq__mnbmm):
                if is_str_arr_type(fdlv__eyog):
                    hhcaj__zytxc += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    hhcaj__zytxc += f"""            len_arrs_{i}[pivot_idx][row_idx] = len(values_tup[{i}][i])
"""
                    hhcaj__zytxc += f"""            total_lens_{i}[pivot_idx] += len(values_tup[{i}][i])
"""
    for i, fdlv__eyog in enumerate(brwgq__mnbmm):
        if is_str_arr_type(fdlv__eyog):
            hhcaj__zytxc += f'    data_arrs_{i} = [\n'
            hhcaj__zytxc += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            hhcaj__zytxc += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            hhcaj__zytxc += '        )\n'
            hhcaj__zytxc += '        for i in range(n_cols)\n'
            hhcaj__zytxc += '    ]\n'
        else:
            hhcaj__zytxc += f'    data_arrs_{i} = [\n'
            hhcaj__zytxc += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            hhcaj__zytxc += '        for _ in range(n_cols)\n'
            hhcaj__zytxc += '    ]\n'
    if not olsgt__aulz and ncjmn__okmgv:
        hhcaj__zytxc += '    nbytes = (n_rows + 7) >> 3\n'
        hhcaj__zytxc += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    hhcaj__zytxc += '    for i in range(len(columns_arr)):\n'
    hhcaj__zytxc += '        col_name = columns_arr[i]\n'
    hhcaj__zytxc += '        pivot_idx = col_map[col_name]\n'
    hhcaj__zytxc += '        row_idx = row_vector[i]\n'
    if not olsgt__aulz and ncjmn__okmgv:
        hhcaj__zytxc += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        hhcaj__zytxc += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        hhcaj__zytxc += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        hhcaj__zytxc += '        else:\n'
        hhcaj__zytxc += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
    if gwwp__efmb:
        hhcaj__zytxc += '        for j in range(num_values_arrays):\n'
        hhcaj__zytxc += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        hhcaj__zytxc += '            col_arr = data_arrs_0[col_idx]\n'
        hhcaj__zytxc += '            values_arr = values_arrs[j]\n'
        hhcaj__zytxc += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        hhcaj__zytxc += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        hhcaj__zytxc += '            else:\n'
        hhcaj__zytxc += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, fdlv__eyog in enumerate(brwgq__mnbmm):
            hhcaj__zytxc += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            hhcaj__zytxc += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            hhcaj__zytxc += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            hhcaj__zytxc += f'        else:\n'
            hhcaj__zytxc += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_tup) == 1:
        hhcaj__zytxc += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names[0])
"""
    else:
        hhcaj__zytxc += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names, None)
"""
    if cnyv__ogltg:
        hhcaj__zytxc += '    num_rows = len(value_names) * len(pivot_values)\n'
        if is_str_arr_type(value_names):
            hhcaj__zytxc += '    total_chars = 0\n'
            hhcaj__zytxc += '    for i in range(len(value_names)):\n'
            hhcaj__zytxc += '        total_chars += len(value_names[i])\n'
            hhcaj__zytxc += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            hhcaj__zytxc += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if is_str_arr_type(pivot_values):
            hhcaj__zytxc += '    total_chars = 0\n'
            hhcaj__zytxc += '    for i in range(len(pivot_values)):\n'
            hhcaj__zytxc += '        total_chars += len(pivot_values[i])\n'
            hhcaj__zytxc += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            hhcaj__zytxc += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        hhcaj__zytxc += '    for i in range(len(value_names)):\n'
        hhcaj__zytxc += '        for j in range(len(pivot_values)):\n'
        hhcaj__zytxc += """            new_value_names[(i * len(pivot_values)) + j] = value_names[i]
"""
        hhcaj__zytxc += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
        hhcaj__zytxc += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        hhcaj__zytxc += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    utu__hcwwe = ', '.join(f'data_arrs_{i}' for i in range(len(brwgq__mnbmm)))
    hhcaj__zytxc += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({utu__hcwwe},), n_rows)
"""
    hhcaj__zytxc += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    hhcaj__zytxc += '        (table,), index, column_index\n'
    hhcaj__zytxc += '    )\n'
    ynpu__vztt = {}
    mli__nvn = {f'data_arr_typ_{i}': fdlv__eyog for i, fdlv__eyog in
        enumerate(brwgq__mnbmm)}
    zgt__xjsse = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **mli__nvn}
    exec(hhcaj__zytxc, zgt__xjsse, ynpu__vztt)
    impl = ynpu__vztt['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    zgcbc__kvt = {}
    zgcbc__kvt['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, kwe__njc in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        koa__fgz = None
        if isinstance(kwe__njc, bodo.DatetimeArrayType):
            drb__juoen = 'datetimetz'
            qxtk__pro = 'datetime64[ns]'
            if isinstance(kwe__njc.tz, int):
                mphjy__tsdt = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(kwe__njc.tz))
            else:
                mphjy__tsdt = pd.DatetimeTZDtype(tz=kwe__njc.tz).tz
            koa__fgz = {'timezone': pa.lib.tzinfo_to_string(mphjy__tsdt)}
        elif isinstance(kwe__njc, types.Array) or kwe__njc == boolean_array:
            drb__juoen = qxtk__pro = kwe__njc.dtype.name
            if qxtk__pro.startswith('datetime'):
                drb__juoen = 'datetime'
        elif is_str_arr_type(kwe__njc):
            drb__juoen = 'unicode'
            qxtk__pro = 'object'
        elif kwe__njc == binary_array_type:
            drb__juoen = 'bytes'
            qxtk__pro = 'object'
        elif isinstance(kwe__njc, DecimalArrayType):
            drb__juoen = qxtk__pro = 'object'
        elif isinstance(kwe__njc, IntegerArrayType):
            yyw__qtlmh = kwe__njc.dtype.name
            if yyw__qtlmh.startswith('int'):
                drb__juoen = 'Int' + yyw__qtlmh[3:]
            elif yyw__qtlmh.startswith('uint'):
                drb__juoen = 'UInt' + yyw__qtlmh[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, kwe__njc))
            qxtk__pro = kwe__njc.dtype.name
        elif kwe__njc == datetime_date_array_type:
            drb__juoen = 'datetime'
            qxtk__pro = 'object'
        elif isinstance(kwe__njc, (StructArrayType, ArrayItemArrayType)):
            drb__juoen = 'object'
            qxtk__pro = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, kwe__njc))
        xvp__iciwb = {'name': col_name, 'field_name': col_name,
            'pandas_type': drb__juoen, 'numpy_type': qxtk__pro, 'metadata':
            koa__fgz}
        zgcbc__kvt['columns'].append(xvp__iciwb)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            ovwrs__ryqz = '__index_level_0__'
            dhghm__rcru = None
        else:
            ovwrs__ryqz = '%s'
            dhghm__rcru = '%s'
        zgcbc__kvt['index_columns'] = [ovwrs__ryqz]
        zgcbc__kvt['columns'].append({'name': dhghm__rcru, 'field_name':
            ovwrs__ryqz, 'pandas_type': index.pandas_type_name,
            'numpy_type': index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        zgcbc__kvt['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        zgcbc__kvt['index_columns'] = []
    zgcbc__kvt['pandas_version'] = pd.__version__
    return zgcbc__kvt


@overload_method(DataFrameType, 'to_parquet', no_unliteral=True)
def to_parquet_overload(df, path, engine='auto', compression='snappy',
    index=None, partition_cols=None, storage_options=None, row_group_size=-
    1, _is_parallel=False):
    check_unsupported_args('DataFrame.to_parquet', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if df.has_runtime_cols and not is_overload_none(partition_cols):
        raise BodoError(
            f"DataFrame.to_parquet(): Providing 'partition_cols' on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information."
            )
    if not is_overload_none(engine) and get_overload_const_str(engine) not in (
        'auto', 'pyarrow'):
        raise BodoError('DataFrame.to_parquet(): only pyarrow engine supported'
            )
    if not is_overload_none(compression) and get_overload_const_str(compression
        ) not in {'snappy', 'gzip', 'brotli'}:
        raise BodoError('to_parquet(): Unsupported compression: ' + str(
            get_overload_const_str(compression)))
    if not is_overload_none(partition_cols):
        partition_cols = get_overload_const_list(partition_cols)
        fiqdx__xfsbf = []
        for wdh__yms in partition_cols:
            try:
                idx = df.columns.index(wdh__yms)
            except ValueError as eeipk__bjo:
                raise BodoError(
                    f'Partition column {wdh__yms} is not in dataframe')
            fiqdx__xfsbf.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    noqk__wtn = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType)
    nzizk__vmabb = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not noqk__wtn)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not noqk__wtn or is_overload_true
        (_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and noqk__wtn and not is_overload_true(_is_parallel)
    if df.has_runtime_cols:
        if isinstance(df.runtime_colname_typ, MultiIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): Not supported with MultiIndex runtime column names. Please return the DataFrame to regular Python to update typing information.'
                )
        if not isinstance(df.runtime_colname_typ, bodo.hiframes.
            pd_index_ext.StringIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): parquet must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
        tqpq__lurov = df.runtime_data_types
        zcy__zein = len(tqpq__lurov)
        koa__fgz = gen_pandas_parquet_metadata([''] * zcy__zein,
            tqpq__lurov, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        nvre__brd = koa__fgz['columns'][:zcy__zein]
        koa__fgz['columns'] = koa__fgz['columns'][zcy__zein:]
        nvre__brd = [json.dumps(ingz__vkj).replace('""', '{0}') for
            ingz__vkj in nvre__brd]
        bvvyx__vgp = json.dumps(koa__fgz)
        bub__wjmse = '"columns": ['
        kpoie__efmss = bvvyx__vgp.find(bub__wjmse)
        if kpoie__efmss == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        yat__vgs = kpoie__efmss + len(bub__wjmse)
        gmruf__zgt = bvvyx__vgp[:yat__vgs]
        bvvyx__vgp = bvvyx__vgp[yat__vgs:]
        dievy__mkokf = len(koa__fgz['columns'])
    else:
        bvvyx__vgp = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and noqk__wtn:
        bvvyx__vgp = bvvyx__vgp.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            bvvyx__vgp = bvvyx__vgp.replace('"%s"', '%s')
    if not df.is_table_format:
        sgb__ybf = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    hhcaj__zytxc = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _is_parallel=False):
"""
    if df.is_table_format:
        hhcaj__zytxc += '    py_table = get_dataframe_table(df)\n'
        hhcaj__zytxc += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        hhcaj__zytxc += '    info_list = [{}]\n'.format(sgb__ybf)
        hhcaj__zytxc += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        hhcaj__zytxc += '    columns_index = get_dataframe_column_names(df)\n'
        hhcaj__zytxc += '    names_arr = index_to_array(columns_index)\n'
        hhcaj__zytxc += '    col_names = array_to_info(names_arr)\n'
    else:
        hhcaj__zytxc += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and nzizk__vmabb:
        hhcaj__zytxc += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        pzku__jqa = True
    else:
        hhcaj__zytxc += '    index_col = array_to_info(np.empty(0))\n'
        pzku__jqa = False
    if df.has_runtime_cols:
        hhcaj__zytxc += '    columns_lst = []\n'
        hhcaj__zytxc += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            hhcaj__zytxc += f'    for _ in range(len(py_table.block_{i})):\n'
            hhcaj__zytxc += f"""        columns_lst.append({nvre__brd[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            hhcaj__zytxc += '        num_cols += 1\n'
        if dievy__mkokf:
            hhcaj__zytxc += "    columns_lst.append('')\n"
        hhcaj__zytxc += '    columns_str = ", ".join(columns_lst)\n'
        hhcaj__zytxc += ('    metadata = """' + gmruf__zgt +
            '""" + columns_str + """' + bvvyx__vgp + '"""\n')
    else:
        hhcaj__zytxc += '    metadata = """' + bvvyx__vgp + '"""\n'
    hhcaj__zytxc += '    if compression is None:\n'
    hhcaj__zytxc += "        compression = 'none'\n"
    hhcaj__zytxc += '    if df.index.name is not None:\n'
    hhcaj__zytxc += '        name_ptr = df.index.name\n'
    hhcaj__zytxc += '    else:\n'
    hhcaj__zytxc += "        name_ptr = 'null'\n"
    hhcaj__zytxc += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    aslry__xxy = None
    if partition_cols:
        aslry__xxy = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        qdsmc__arr = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in fiqdx__xfsbf)
        if qdsmc__arr:
            hhcaj__zytxc += '    cat_info_list = [{}]\n'.format(qdsmc__arr)
            hhcaj__zytxc += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            hhcaj__zytxc += '    cat_table = table\n'
        hhcaj__zytxc += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        hhcaj__zytxc += (
            f'    part_cols_idxs = np.array({fiqdx__xfsbf}, dtype=np.int32)\n')
        hhcaj__zytxc += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        hhcaj__zytxc += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        hhcaj__zytxc += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        hhcaj__zytxc += (
            '                            unicode_to_utf8(compression),\n')
        hhcaj__zytxc += '                            _is_parallel,\n'
        hhcaj__zytxc += (
            '                            unicode_to_utf8(bucket_region),\n')
        hhcaj__zytxc += '                            row_group_size)\n'
        hhcaj__zytxc += '    delete_table_decref_arrays(table)\n'
        hhcaj__zytxc += '    delete_info_decref_array(index_col)\n'
        hhcaj__zytxc += (
            '    delete_info_decref_array(col_names_no_partitions)\n')
        hhcaj__zytxc += '    delete_info_decref_array(col_names)\n'
        if qdsmc__arr:
            hhcaj__zytxc += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        hhcaj__zytxc += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        hhcaj__zytxc += (
            '                            table, col_names, index_col,\n')
        hhcaj__zytxc += '                            ' + str(pzku__jqa) + ',\n'
        hhcaj__zytxc += (
            '                            unicode_to_utf8(metadata),\n')
        hhcaj__zytxc += (
            '                            unicode_to_utf8(compression),\n')
        hhcaj__zytxc += (
            '                            _is_parallel, 1, df.index.start,\n')
        hhcaj__zytxc += (
            '                            df.index.stop, df.index.step,\n')
        hhcaj__zytxc += (
            '                            unicode_to_utf8(name_ptr),\n')
        hhcaj__zytxc += (
            '                            unicode_to_utf8(bucket_region),\n')
        hhcaj__zytxc += '                            row_group_size)\n'
        hhcaj__zytxc += '    delete_table_decref_arrays(table)\n'
        hhcaj__zytxc += '    delete_info_decref_array(index_col)\n'
        hhcaj__zytxc += '    delete_info_decref_array(col_names)\n'
    else:
        hhcaj__zytxc += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        hhcaj__zytxc += (
            '                            table, col_names, index_col,\n')
        hhcaj__zytxc += '                            ' + str(pzku__jqa) + ',\n'
        hhcaj__zytxc += (
            '                            unicode_to_utf8(metadata),\n')
        hhcaj__zytxc += (
            '                            unicode_to_utf8(compression),\n')
        hhcaj__zytxc += (
            '                            _is_parallel, 0, 0, 0, 0,\n')
        hhcaj__zytxc += (
            '                            unicode_to_utf8(name_ptr),\n')
        hhcaj__zytxc += (
            '                            unicode_to_utf8(bucket_region),\n')
        hhcaj__zytxc += '                            row_group_size)\n'
        hhcaj__zytxc += '    delete_table_decref_arrays(table)\n'
        hhcaj__zytxc += '    delete_info_decref_array(index_col)\n'
        hhcaj__zytxc += '    delete_info_decref_array(col_names)\n'
    ynpu__vztt = {}
    if df.has_runtime_cols:
        fytfc__oaohs = None
    else:
        for iflfb__ddsn in df.columns:
            if not isinstance(iflfb__ddsn, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        fytfc__oaohs = pd.array(df.columns)
    exec(hhcaj__zytxc, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': fytfc__oaohs,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': aslry__xxy, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, ynpu__vztt)
    rkcz__vay = ynpu__vztt['df_to_parquet']
    return rkcz__vay


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    ojffl__xgsu = 'all_ok'
    nqww__pfi, lvell__vyen = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        cwl__qwbm = 100
        if chunksize is None:
            fdjtu__pxubc = cwl__qwbm
        else:
            fdjtu__pxubc = min(chunksize, cwl__qwbm)
        if _is_table_create:
            df = df.iloc[:fdjtu__pxubc, :]
        else:
            df = df.iloc[fdjtu__pxubc:, :]
            if len(df) == 0:
                return ojffl__xgsu
    ddw__gul = df.columns
    try:
        if nqww__pfi == 'snowflake':
            if lvell__vyen and con.count(lvell__vyen) == 1:
                con = con.replace(lvell__vyen, quote(lvell__vyen))
            try:
                from snowflake.connector.pandas_tools import pd_writer
                from bodo import snowflake_sqlalchemy_compat
                if method is not None and _is_table_create and bodo.get_rank(
                    ) == 0:
                    import warnings
                    from bodo.utils.typing import BodoWarning
                    warnings.warn(BodoWarning(
                        'DataFrame.to_sql(): method argument is not supported with Snowflake. Bodo always uses snowflake.connector.pandas_tools.pd_writer to write data.'
                        ))
                method = pd_writer
                df.columns = [(xnvss__xxnh.upper() if xnvss__xxnh.islower()
                     else xnvss__xxnh) for xnvss__xxnh in df.columns]
            except ImportError as eeipk__bjo:
                ojffl__xgsu = (
                    "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires both snowflake-sqlalchemy and snowflake-connector-python. These can be installed by calling 'conda install -c conda-forge snowflake-sqlalchemy snowflake-connector-python' or 'pip install snowflake-sqlalchemy snowflake-connector-python'."
                    )
                return ojffl__xgsu
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as vdtjl__yuvor:
            ojffl__xgsu = vdtjl__yuvor.args[0]
        return ojffl__xgsu
    finally:
        df.columns = ddw__gul


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    with numba.objmode(out='unicode_type'):
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
    return out


@overload_method(DataFrameType, 'to_sql')
def to_sql_overload(df, name, con, schema=None, if_exists='fail', index=
    True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_parallel=False):
    check_runtime_cols_unsupported(df, 'DataFrame.to_sql()')
    if is_overload_none(schema):
        if bodo.get_rank() == 0:
            import warnings
            warnings.warn(BodoWarning(
                f'DataFrame.to_sql(): schema argument is recommended to avoid permission issues when writing the table.'
                ))
    if not (is_overload_none(chunksize) or isinstance(chunksize, types.Integer)
        ):
        raise BodoError(
            "DataFrame.to_sql(): 'chunksize' argument must be an integer if provided."
            )

    def _impl(df, name, con, schema=None, if_exists='fail', index=True,
        index_label=None, chunksize=None, dtype=None, method=None,
        _is_parallel=False):
        nscz__cvd = bodo.libs.distributed_api.get_rank()
        ojffl__xgsu = 'unset'
        if nscz__cvd != 0:
            ojffl__xgsu = bcast_scalar(ojffl__xgsu)
        elif nscz__cvd == 0:
            ojffl__xgsu = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, True, _is_parallel)
            ojffl__xgsu = bcast_scalar(ojffl__xgsu)
        if_exists = 'append'
        if _is_parallel and ojffl__xgsu == 'all_ok':
            ojffl__xgsu = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, False, _is_parallel)
        if ojffl__xgsu != 'all_ok':
            print('err_msg=', ojffl__xgsu)
            raise ValueError('error in to_sql() operation')
    return _impl


@overload_method(DataFrameType, 'to_csv', no_unliteral=True)
def to_csv_overload(df, path_or_buf=None, sep=',', na_rep='', float_format=
    None, columns=None, header=True, index=True, index_label=None, mode='w',
    encoding=None, compression=None, quoting=None, quotechar='"',
    line_terminator=None, chunksize=None, date_format=None, doublequote=
    True, escapechar=None, decimal='.', errors='strict', storage_options=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_csv()')
    check_unsupported_args('DataFrame.to_csv', {'encoding': encoding,
        'mode': mode, 'errors': errors, 'storage_options': storage_options},
        {'encoding': None, 'mode': 'w', 'errors': 'strict',
        'storage_options': None}, package_name='pandas', module_name='IO')
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "DataFrame.to_csv(): 'path_or_buf' argument should be None or string"
            )
    if not is_overload_none(compression):
        raise BodoError(
            "DataFrame.to_csv(): 'compression' argument supports only None, which is the default in JIT code."
            )
    if is_overload_constant_str(path_or_buf):
        lfisn__twv = get_overload_const_str(path_or_buf)
        if lfisn__twv.endswith(('.gz', '.bz2', '.zip', '.xz')):
            import warnings
            from bodo.utils.typing import BodoWarning
            warnings.warn(BodoWarning(
                "DataFrame.to_csv(): 'compression' argument defaults to None in JIT code, which is the only supported value."
                ))
    if not (is_overload_none(columns) or isinstance(columns, (types.List,
        types.Tuple))):
        raise BodoError(
            "DataFrame.to_csv(): 'columns' argument must be list a or tuple type."
            )
    if is_overload_none(path_or_buf):

        def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=
            None, columns=None, header=True, index=True, index_label=None,
            mode='w', encoding=None, compression=None, quoting=None,
            quotechar='"', line_terminator=None, chunksize=None,
            date_format=None, doublequote=True, escapechar=None, decimal=
            '.', errors='strict', storage_options=None):
            with numba.objmode(D='unicode_type'):
                D = df.to_csv(path_or_buf, sep, na_rep, float_format,
                    columns, header, index, index_label, mode, encoding,
                    compression, quoting, quotechar, line_terminator,
                    chunksize, date_format, doublequote, escapechar,
                    decimal, errors, storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=None,
        columns=None, header=True, index=True, index_label=None, mode='w',
        encoding=None, compression=None, quoting=None, quotechar='"',
        line_terminator=None, chunksize=None, date_format=None, doublequote
        =True, escapechar=None, decimal='.', errors='strict',
        storage_options=None):
        with numba.objmode(D='unicode_type'):
            D = df.to_csv(None, sep, na_rep, float_format, columns, header,
                index, index_label, mode, encoding, compression, quoting,
                quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors, storage_options)
        bodo.io.fs_io.csv_write(path_or_buf, D)
    return _impl


@overload_method(DataFrameType, 'to_json', no_unliteral=True)
def to_json_overload(df, path_or_buf=None, orient='records', date_format=
    None, double_precision=10, force_ascii=True, date_unit='ms',
    default_handler=None, lines=True, compression='infer', index=True,
    indent=None, storage_options=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_json()')
    check_unsupported_args('DataFrame.to_json', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if path_or_buf is None or path_or_buf == types.none:

        def _impl(df, path_or_buf=None, orient='records', date_format=None,
            double_precision=10, force_ascii=True, date_unit='ms',
            default_handler=None, lines=True, compression='infer', index=
            True, indent=None, storage_options=None):
            with numba.objmode(D='unicode_type'):
                D = df.to_json(path_or_buf, orient, date_format,
                    double_precision, force_ascii, date_unit,
                    default_handler, lines, compression, index, indent,
                    storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, orient='records', date_format=None,
        double_precision=10, force_ascii=True, date_unit='ms',
        default_handler=None, lines=True, compression='infer', index=True,
        indent=None, storage_options=None):
        with numba.objmode(D='unicode_type'):
            D = df.to_json(None, orient, date_format, double_precision,
                force_ascii, date_unit, default_handler, lines, compression,
                index, indent, storage_options)
        ocam__fnqbm = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(ocam__fnqbm))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(ocam__fnqbm))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    cjhwm__fqwi = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    lvjj__fczmm = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', cjhwm__fqwi, lvjj__fczmm,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    hhcaj__zytxc = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        xciqx__joar = data.data.dtype.categories
        hhcaj__zytxc += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        xciqx__joar = data.dtype.categories
        hhcaj__zytxc += '  data_values = data\n'
    awxcq__afiy = len(xciqx__joar)
    hhcaj__zytxc += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    hhcaj__zytxc += '  numba.parfors.parfor.init_prange()\n'
    hhcaj__zytxc += '  n = len(data_values)\n'
    for i in range(awxcq__afiy):
        hhcaj__zytxc += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    hhcaj__zytxc += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    hhcaj__zytxc += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for zcw__pgnwz in range(awxcq__afiy):
        hhcaj__zytxc += '          data_arr_{}[i] = 0\n'.format(zcw__pgnwz)
    hhcaj__zytxc += '      else:\n'
    for lxlug__evvgi in range(awxcq__afiy):
        hhcaj__zytxc += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            lxlug__evvgi)
    sgb__ybf = ', '.join(f'data_arr_{i}' for i in range(awxcq__afiy))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(xciqx__joar[0], np.datetime64):
        xciqx__joar = tuple(pd.Timestamp(xnvss__xxnh) for xnvss__xxnh in
            xciqx__joar)
    elif isinstance(xciqx__joar[0], np.timedelta64):
        xciqx__joar = tuple(pd.Timedelta(xnvss__xxnh) for xnvss__xxnh in
            xciqx__joar)
    return bodo.hiframes.dataframe_impl._gen_init_df(hhcaj__zytxc,
        xciqx__joar, sgb__ybf, index)


def categorical_can_construct_dataframe(val):
    if isinstance(val, CategoricalArrayType):
        return val.dtype.categories is not None
    elif isinstance(val, SeriesType) and isinstance(val.data,
        CategoricalArrayType):
        return val.data.dtype.categories is not None
    return False


def handle_inplace_df_type_change(inplace, _bodo_transformed, func_name):
    if is_overload_false(_bodo_transformed
        ) and bodo.transforms.typing_pass.in_partial_typing and (
        is_overload_true(inplace) or not is_overload_constant_bool(inplace)):
        bodo.transforms.typing_pass.typing_transform_required = True
        raise Exception('DataFrame.{}(): transform necessary for inplace'.
            format(func_name))


pd_unsupported = (pd.read_pickle, pd.read_table, pd.read_fwf, pd.
    read_clipboard, pd.ExcelFile, pd.read_html, pd.read_xml, pd.read_hdf,
    pd.read_feather, pd.read_orc, pd.read_sas, pd.read_spss, pd.
    read_sql_table, pd.read_sql_query, pd.read_gbq, pd.read_stata, pd.
    ExcelWriter, pd.json_normalize, pd.merge_ordered, pd.factorize, pd.
    wide_to_long, pd.bdate_range, pd.period_range, pd.infer_freq, pd.
    interval_range, pd.eval, pd.test, pd.Grouper)
pd_util_unsupported = pd.util.hash_array, pd.util.hash_pandas_object
dataframe_unsupported = ['set_flags', 'convert_dtypes', 'bool', '__iter__',
    'items', 'iteritems', 'keys', 'iterrows', 'lookup', 'pop', 'xs', 'get',
    'add', 'sub', 'mul', 'div', 'truediv', 'floordiv', 'mod', 'pow', 'dot',
    'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv', 'rfloordiv', 'rmod', 'rpow',
    'lt', 'gt', 'le', 'ge', 'ne', 'eq', 'combine', 'combine_first',
    'subtract', 'divide', 'multiply', 'applymap', 'agg', 'aggregate',
    'transform', 'expanding', 'ewm', 'all', 'any', 'clip', 'corrwith',
    'cummax', 'cummin', 'eval', 'kurt', 'kurtosis', 'mad', 'mode', 'rank',
    'round', 'sem', 'skew', 'value_counts', 'add_prefix', 'add_suffix',
    'align', 'at_time', 'between_time', 'equals', 'reindex', 'reindex_like',
    'rename_axis', 'set_axis', 'truncate', 'backfill', 'bfill', 'ffill',
    'interpolate', 'pad', 'droplevel', 'reorder_levels', 'nlargest',
    'nsmallest', 'swaplevel', 'stack', 'unstack', 'swapaxes', 'squeeze',
    'to_xarray', 'T', 'transpose', 'compare', 'update', 'asfreq', 'asof',
    'slice_shift', 'tshift', 'first_valid_index', 'last_valid_index',
    'resample', 'to_period', 'to_timestamp', 'tz_convert', 'tz_localize',
    'boxplot', 'hist', 'from_dict', 'from_records', 'to_pickle', 'to_hdf',
    'to_dict', 'to_excel', 'to_html', 'to_feather', 'to_latex', 'to_stata',
    'to_gbq', 'to_records', 'to_clipboard', 'to_markdown', 'to_xml']
dataframe_unsupported_attrs = ['at', 'attrs', 'axes', 'flags', 'style',
    'sparse']


def _install_pd_unsupported(mod_name, pd_unsupported):
    for ipgwx__wdna in pd_unsupported:
        rov__wiqy = mod_name + '.' + ipgwx__wdna.__name__
        overload(ipgwx__wdna, no_unliteral=True)(create_unsupported_overload
            (rov__wiqy))


def _install_dataframe_unsupported():
    for ohik__ogxv in dataframe_unsupported_attrs:
        sjx__yiso = 'DataFrame.' + ohik__ogxv
        overload_attribute(DataFrameType, ohik__ogxv)(
            create_unsupported_overload(sjx__yiso))
    for rov__wiqy in dataframe_unsupported:
        sjx__yiso = 'DataFrame.' + rov__wiqy + '()'
        overload_method(DataFrameType, rov__wiqy)(create_unsupported_overload
            (sjx__yiso))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
