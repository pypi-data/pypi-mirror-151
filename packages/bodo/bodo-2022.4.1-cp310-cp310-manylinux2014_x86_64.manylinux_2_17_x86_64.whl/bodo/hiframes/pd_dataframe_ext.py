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
            vzay__lwah = f'{len(self.data)} columns of types {set(self.data)}'
            xrbha__pldz = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            return (
                f'dataframe({vzay__lwah}, {self.index}, {xrbha__pldz}, {self.dist}, {self.is_table_format})'
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
            eqw__ugif = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            data = tuple(cnidk__sue.unify(typingctx, yhpc__emqti) if 
                cnidk__sue != yhpc__emqti else cnidk__sue for cnidk__sue,
                yhpc__emqti in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if eqw__ugif is not None and None not in data:
                return DataFrameType(data, eqw__ugif, self.columns, dist,
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
        return all(cnidk__sue.is_precise() for cnidk__sue in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        opt__hlig = self.columns.index(col_name)
        vphzv__xdz = tuple(list(self.data[:opt__hlig]) + [new_type] + list(
            self.data[opt__hlig + 1:]))
        return DataFrameType(vphzv__xdz, self.index, self.columns, self.
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
        cwj__xggz = [('data', data_typ), ('index', fe_type.df_type.index),
            ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            cwj__xggz.append(('columns', fe_type.df_type.runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, cwj__xggz)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        cwj__xggz = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, cwj__xggz)


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
        qql__molif = 'n',
        kbf__ymy = {'n': 5}
        vwzni__wek, eof__cxmu = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, qql__molif, kbf__ymy)
        twu__fdhws = eof__cxmu[0]
        if not is_overload_int(twu__fdhws):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        mqfl__vaxg = df.copy(is_table_format=False)
        return mqfl__vaxg(*eof__cxmu).replace(pysig=vwzni__wek)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        frn__tywjq = (df,) + args
        qql__molif = 'df', 'method', 'min_periods'
        kbf__ymy = {'method': 'pearson', 'min_periods': 1}
        zgxrx__bkzbq = 'method',
        vwzni__wek, eof__cxmu = bodo.utils.typing.fold_typing_args(func_name,
            frn__tywjq, kws, qql__molif, kbf__ymy, zgxrx__bkzbq)
        wdwrl__asx = eof__cxmu[2]
        if not is_overload_int(wdwrl__asx):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        cgssn__mdn = []
        rgud__oalo = []
        for axaht__hsv, zmjb__ckdo in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(zmjb__ckdo.dtype):
                cgssn__mdn.append(axaht__hsv)
                rgud__oalo.append(types.Array(types.float64, 1, 'A'))
        if len(cgssn__mdn) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        rgud__oalo = tuple(rgud__oalo)
        cgssn__mdn = tuple(cgssn__mdn)
        index_typ = bodo.utils.typing.type_col_to_index(cgssn__mdn)
        mqfl__vaxg = DataFrameType(rgud__oalo, index_typ, cgssn__mdn)
        return mqfl__vaxg(*eof__cxmu).replace(pysig=vwzni__wek)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        jjbx__fagxp = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        grz__fkm = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        tver__oqyx = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        cwy__vuv = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        qcam__myb = dict(raw=grz__fkm, result_type=tver__oqyx)
        ialp__vepf = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', qcam__myb, ialp__vepf,
            package_name='pandas', module_name='DataFrame')
        zbr__lkbbi = True
        if types.unliteral(jjbx__fagxp) == types.unicode_type:
            if not is_overload_constant_str(jjbx__fagxp):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            zbr__lkbbi = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        hyp__kazpn = get_overload_const_int(axis)
        if zbr__lkbbi and hyp__kazpn != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif hyp__kazpn not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        akkma__bgxrr = []
        for arr_typ in df.data:
            gcl__ggc = SeriesType(arr_typ.dtype, arr_typ, df.index, string_type
                )
            xlo__fugi = self.context.resolve_function_type(operator.getitem,
                (SeriesIlocType(gcl__ggc), types.int64), {}).return_type
            akkma__bgxrr.append(xlo__fugi)
        fec__guftn = types.none
        fsw__qvlef = HeterogeneousIndexType(types.BaseTuple.from_types(
            tuple(types.literal(axaht__hsv) for axaht__hsv in df.columns)),
            None)
        dtcyk__paf = types.BaseTuple.from_types(akkma__bgxrr)
        yqu__lvzq = types.Tuple([types.bool_] * len(dtcyk__paf))
        zcv__hkn = bodo.NullableTupleType(dtcyk__paf, yqu__lvzq)
        nvsn__mccwg = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if nvsn__mccwg == types.NPDatetime('ns'):
            nvsn__mccwg = bodo.pd_timestamp_type
        if nvsn__mccwg == types.NPTimedelta('ns'):
            nvsn__mccwg = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(dtcyk__paf):
            tmqp__sya = HeterogeneousSeriesType(zcv__hkn, fsw__qvlef,
                nvsn__mccwg)
        else:
            tmqp__sya = SeriesType(dtcyk__paf.dtype, zcv__hkn, fsw__qvlef,
                nvsn__mccwg)
        rjv__lqzi = tmqp__sya,
        if cwy__vuv is not None:
            rjv__lqzi += tuple(cwy__vuv.types)
        try:
            if not zbr__lkbbi:
                nqyek__zysz = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(jjbx__fagxp), self.context,
                    'DataFrame.apply', axis if hyp__kazpn == 1 else None)
            else:
                nqyek__zysz = get_const_func_output_type(jjbx__fagxp,
                    rjv__lqzi, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as nxdlj__gcoj:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                nxdlj__gcoj))
        if zbr__lkbbi:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(nqyek__zysz, (SeriesType, HeterogeneousSeriesType)
                ) and nqyek__zysz.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(nqyek__zysz, HeterogeneousSeriesType):
                xgj__sfmkr, alvat__azzq = nqyek__zysz.const_info
                if isinstance(nqyek__zysz.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    ell__hcmm = nqyek__zysz.data.tuple_typ.types
                elif isinstance(nqyek__zysz.data, types.Tuple):
                    ell__hcmm = nqyek__zysz.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                dha__uus = tuple(to_nullable_type(dtype_to_array_type(
                    dvsfr__mdj)) for dvsfr__mdj in ell__hcmm)
                krnu__btky = DataFrameType(dha__uus, df.index, alvat__azzq)
            elif isinstance(nqyek__zysz, SeriesType):
                goeh__zpews, alvat__azzq = nqyek__zysz.const_info
                dha__uus = tuple(to_nullable_type(dtype_to_array_type(
                    nqyek__zysz.dtype)) for xgj__sfmkr in range(goeh__zpews))
                krnu__btky = DataFrameType(dha__uus, df.index, alvat__azzq)
            else:
                ymsjr__uwf = get_udf_out_arr_type(nqyek__zysz)
                krnu__btky = SeriesType(ymsjr__uwf.dtype, ymsjr__uwf, df.
                    index, None)
        else:
            krnu__btky = nqyek__zysz
        kjbb__kxxmi = ', '.join("{} = ''".format(cnidk__sue) for cnidk__sue in
            kws.keys())
        hoc__iuiez = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {kjbb__kxxmi}):
"""
        hoc__iuiez += '    pass\n'
        uyfq__ygas = {}
        exec(hoc__iuiez, {}, uyfq__ygas)
        nrgd__wnci = uyfq__ygas['apply_stub']
        vwzni__wek = numba.core.utils.pysignature(nrgd__wnci)
        qqk__gfk = (jjbx__fagxp, axis, grz__fkm, tver__oqyx, cwy__vuv) + tuple(
            kws.values())
        return signature(krnu__btky, *qqk__gfk).replace(pysig=vwzni__wek)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        qql__molif = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        kbf__ymy = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        zgxrx__bkzbq = ('subplots', 'sharex', 'sharey', 'layout',
            'use_index', 'grid', 'style', 'logx', 'logy', 'loglog', 'xlim',
            'ylim', 'rot', 'colormap', 'table', 'yerr', 'xerr',
            'sort_columns', 'secondary_y', 'colorbar', 'position',
            'stacked', 'mark_right', 'include_bool', 'backend')
        vwzni__wek, eof__cxmu = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, qql__molif, kbf__ymy, zgxrx__bkzbq)
        xpk__rcdkk = eof__cxmu[2]
        if not is_overload_constant_str(xpk__rcdkk):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        wsvk__nxs = eof__cxmu[0]
        if not is_overload_none(wsvk__nxs) and not (is_overload_int(
            wsvk__nxs) or is_overload_constant_str(wsvk__nxs)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(wsvk__nxs):
            qimp__dexm = get_overload_const_str(wsvk__nxs)
            if qimp__dexm not in df.columns:
                raise BodoError(f'{func_name}: {qimp__dexm} column not found.')
        elif is_overload_int(wsvk__nxs):
            jcxfv__gzvz = get_overload_const_int(wsvk__nxs)
            if jcxfv__gzvz > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {jcxfv__gzvz} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            wsvk__nxs = df.columns[wsvk__nxs]
        cot__uio = eof__cxmu[1]
        if not is_overload_none(cot__uio) and not (is_overload_int(cot__uio
            ) or is_overload_constant_str(cot__uio)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(cot__uio):
            nsmiw__ajgn = get_overload_const_str(cot__uio)
            if nsmiw__ajgn not in df.columns:
                raise BodoError(f'{func_name}: {nsmiw__ajgn} column not found.'
                    )
        elif is_overload_int(cot__uio):
            amyw__vlt = get_overload_const_int(cot__uio)
            if amyw__vlt > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {amyw__vlt} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            cot__uio = df.columns[cot__uio]
        yioq__pmng = eof__cxmu[3]
        if not is_overload_none(yioq__pmng) and not is_tuple_like_type(
            yioq__pmng):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        ayux__aovuf = eof__cxmu[10]
        if not is_overload_none(ayux__aovuf) and not is_overload_constant_str(
            ayux__aovuf):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        bdup__duli = eof__cxmu[12]
        if not is_overload_bool(bdup__duli):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        rnkbv__wxs = eof__cxmu[17]
        if not is_overload_none(rnkbv__wxs) and not is_tuple_like_type(
            rnkbv__wxs):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        bja__mtzjn = eof__cxmu[18]
        if not is_overload_none(bja__mtzjn) and not is_tuple_like_type(
            bja__mtzjn):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        yyfs__rzj = eof__cxmu[22]
        if not is_overload_none(yyfs__rzj) and not is_overload_int(yyfs__rzj):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        dqg__vbofp = eof__cxmu[29]
        if not is_overload_none(dqg__vbofp) and not is_overload_constant_str(
            dqg__vbofp):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        nosxy__ksacu = eof__cxmu[30]
        if not is_overload_none(nosxy__ksacu) and not is_overload_constant_str(
            nosxy__ksacu):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        iccf__jwn = types.List(types.mpl_line_2d_type)
        xpk__rcdkk = get_overload_const_str(xpk__rcdkk)
        if xpk__rcdkk == 'scatter':
            if is_overload_none(wsvk__nxs) and is_overload_none(cot__uio):
                raise BodoError(
                    f'{func_name}: {xpk__rcdkk} requires an x and y column.')
            elif is_overload_none(wsvk__nxs):
                raise BodoError(
                    f'{func_name}: {xpk__rcdkk} x column is missing.')
            elif is_overload_none(cot__uio):
                raise BodoError(
                    f'{func_name}: {xpk__rcdkk} y column is missing.')
            iccf__jwn = types.mpl_path_collection_type
        elif xpk__rcdkk != 'line':
            raise BodoError(f'{func_name}: {xpk__rcdkk} plot is not supported.'
                )
        return signature(iccf__jwn, *eof__cxmu).replace(pysig=vwzni__wek)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            mjzen__tfh = df.columns.index(attr)
            arr_typ = df.data[mjzen__tfh]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            tmx__mhf = []
            vphzv__xdz = []
            abak__gxj = False
            for i, cjwqv__btty in enumerate(df.columns):
                if cjwqv__btty[0] != attr:
                    continue
                abak__gxj = True
                tmx__mhf.append(cjwqv__btty[1] if len(cjwqv__btty) == 2 else
                    cjwqv__btty[1:])
                vphzv__xdz.append(df.data[i])
            if abak__gxj:
                return DataFrameType(tuple(vphzv__xdz), df.index, tuple(
                    tmx__mhf))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        cuqq__luk = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(cuqq__luk)
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
        uirri__pyqs = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], uirri__pyqs)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    obc__wfq = builder.module
    prpe__qem = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    luyqk__vfu = cgutils.get_or_insert_function(obc__wfq, prpe__qem, name=
        '.dtor.df.{}'.format(df_type))
    if not luyqk__vfu.is_declaration:
        return luyqk__vfu
    luyqk__vfu.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(luyqk__vfu.append_basic_block())
    ygtmm__oispe = luyqk__vfu.args[0]
    fmo__zsa = context.get_value_type(payload_type).as_pointer()
    agwvy__twq = builder.bitcast(ygtmm__oispe, fmo__zsa)
    payload = context.make_helper(builder, payload_type, ref=agwvy__twq)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        sosme__sgjvu = context.get_python_api(builder)
        ubep__uzuak = sosme__sgjvu.gil_ensure()
        sosme__sgjvu.decref(payload.parent)
        sosme__sgjvu.gil_release(ubep__uzuak)
    builder.ret_void()
    return luyqk__vfu


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    hyyyd__mimxv = cgutils.create_struct_proxy(payload_type)(context, builder)
    hyyyd__mimxv.data = data_tup
    hyyyd__mimxv.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        hyyyd__mimxv.columns = colnames
    bazqk__njfel = context.get_value_type(payload_type)
    sagi__zve = context.get_abi_sizeof(bazqk__njfel)
    acz__pal = define_df_dtor(context, builder, df_type, payload_type)
    xkrkj__fnsaa = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, sagi__zve), acz__pal)
    fbvn__seq = context.nrt.meminfo_data(builder, xkrkj__fnsaa)
    bpirb__dvb = builder.bitcast(fbvn__seq, bazqk__njfel.as_pointer())
    rrxd__ivxg = cgutils.create_struct_proxy(df_type)(context, builder)
    rrxd__ivxg.meminfo = xkrkj__fnsaa
    if parent is None:
        rrxd__ivxg.parent = cgutils.get_null_value(rrxd__ivxg.parent.type)
    else:
        rrxd__ivxg.parent = parent
        hyyyd__mimxv.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            sosme__sgjvu = context.get_python_api(builder)
            ubep__uzuak = sosme__sgjvu.gil_ensure()
            sosme__sgjvu.incref(parent)
            sosme__sgjvu.gil_release(ubep__uzuak)
    builder.store(hyyyd__mimxv._getvalue(), bpirb__dvb)
    return rrxd__ivxg._getvalue()


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
        vwy__ofn = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype.
            arr_types)
    else:
        vwy__ofn = [dvsfr__mdj for dvsfr__mdj in data_typ.dtype.arr_types]
    wfnq__rndc = DataFrameType(tuple(vwy__ofn + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        daf__shmr = construct_dataframe(context, builder, df_type, data_tup,
            index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return daf__shmr
    sig = signature(wfnq__rndc, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ=None):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    goeh__zpews = len(data_tup_typ.types)
    if goeh__zpews == 0:
        column_names = ()
    elif isinstance(col_names_typ, types.TypeRef):
        column_names = col_names_typ.instance_type.columns
    else:
        column_names = get_const_tup_vals(col_names_typ)
    if goeh__zpews == 1 and isinstance(data_tup_typ.types[0], TableType):
        goeh__zpews = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == goeh__zpews, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    afeo__fobu = data_tup_typ.types
    if goeh__zpews != 0 and isinstance(data_tup_typ.types[0], TableType):
        afeo__fobu = data_tup_typ.types[0].arr_types
        is_table_format = True
    wfnq__rndc = DataFrameType(afeo__fobu, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            udtgq__yjxfs = cgutils.create_struct_proxy(wfnq__rndc.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = udtgq__yjxfs.parent
        daf__shmr = construct_dataframe(context, builder, df_type, data_tup,
            index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return daf__shmr
    sig = signature(wfnq__rndc, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        rrxd__ivxg = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, rrxd__ivxg.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        hyyyd__mimxv = get_dataframe_payload(context, builder, df_typ, args[0])
        tklk__ixiqg = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[tklk__ixiqg]
        if df_typ.is_table_format:
            udtgq__yjxfs = cgutils.create_struct_proxy(df_typ.table_type)(
                context, builder, builder.extract_value(hyyyd__mimxv.data, 0))
            swqx__goz = df_typ.table_type.type_to_blk[arr_typ]
            ziyqw__dklof = getattr(udtgq__yjxfs, f'block_{swqx__goz}')
            bmjk__iuen = ListInstance(context, builder, types.List(arr_typ),
                ziyqw__dklof)
            hew__qml = context.get_constant(types.int64, df_typ.table_type.
                block_offsets[tklk__ixiqg])
            uirri__pyqs = bmjk__iuen.getitem(hew__qml)
        else:
            uirri__pyqs = builder.extract_value(hyyyd__mimxv.data, tklk__ixiqg)
        gmnj__oadw = cgutils.alloca_once_value(builder, uirri__pyqs)
        zxz__zrx = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, gmnj__oadw, zxz__zrx)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    xkrkj__fnsaa = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, xkrkj__fnsaa)
    fmo__zsa = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, fmo__zsa)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    wfnq__rndc = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        wfnq__rndc = types.Tuple([TableType(df_typ.data)])
    sig = signature(wfnq__rndc, df_typ)

    def codegen(context, builder, signature, args):
        hyyyd__mimxv = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            hyyyd__mimxv.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        hyyyd__mimxv = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index,
            hyyyd__mimxv.index)
    wfnq__rndc = df_typ.index
    sig = signature(wfnq__rndc, df_typ)
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
        mqfl__vaxg = df.data[i]
        return mqfl__vaxg(*args)


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
        hyyyd__mimxv = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(hyyyd__mimxv.data, 0))
    return df_typ.table_type(df_typ), codegen


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        hyyyd__mimxv = get_dataframe_payload(context, builder, signature.
            args[0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, hyyyd__mimxv.columns)
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
    dtcyk__paf = self.typemap[data_tup.name]
    if any(is_tuple_like_type(dvsfr__mdj) for dvsfr__mdj in dtcyk__paf.types):
        return None
    if equiv_set.has_shape(data_tup):
        apzqp__kqfb = equiv_set.get_shape(data_tup)
        if len(apzqp__kqfb) > 1:
            equiv_set.insert_equiv(*apzqp__kqfb)
        if len(apzqp__kqfb) > 0:
            fsw__qvlef = self.typemap[index.name]
            if not isinstance(fsw__qvlef, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(apzqp__kqfb[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(apzqp__kqfb[0], len(
                apzqp__kqfb)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    mfni__qvvmu = args[0]
    data_types = self.typemap[mfni__qvvmu.name].data
    if any(is_tuple_like_type(dvsfr__mdj) for dvsfr__mdj in data_types):
        return None
    if equiv_set.has_shape(mfni__qvvmu):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            mfni__qvvmu)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    mfni__qvvmu = args[0]
    fsw__qvlef = self.typemap[mfni__qvvmu.name].index
    if isinstance(fsw__qvlef, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(mfni__qvvmu):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            mfni__qvvmu)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    mfni__qvvmu = args[0]
    if equiv_set.has_shape(mfni__qvvmu):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            mfni__qvvmu), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    mfni__qvvmu = args[0]
    if equiv_set.has_shape(mfni__qvvmu):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            mfni__qvvmu)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    tklk__ixiqg = get_overload_const_int(c_ind_typ)
    if df_typ.data[tklk__ixiqg] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        lkfqr__mecf, xgj__sfmkr, hjcq__ylm = args
        hyyyd__mimxv = get_dataframe_payload(context, builder, df_typ,
            lkfqr__mecf)
        if df_typ.is_table_format:
            udtgq__yjxfs = cgutils.create_struct_proxy(df_typ.table_type)(
                context, builder, builder.extract_value(hyyyd__mimxv.data, 0))
            swqx__goz = df_typ.table_type.type_to_blk[arr_typ]
            ziyqw__dklof = getattr(udtgq__yjxfs, f'block_{swqx__goz}')
            bmjk__iuen = ListInstance(context, builder, types.List(arr_typ),
                ziyqw__dklof)
            hew__qml = context.get_constant(types.int64, df_typ.table_type.
                block_offsets[tklk__ixiqg])
            bmjk__iuen.setitem(hew__qml, hjcq__ylm, True)
        else:
            uirri__pyqs = builder.extract_value(hyyyd__mimxv.data, tklk__ixiqg)
            context.nrt.decref(builder, df_typ.data[tklk__ixiqg], uirri__pyqs)
            hyyyd__mimxv.data = builder.insert_value(hyyyd__mimxv.data,
                hjcq__ylm, tklk__ixiqg)
            context.nrt.incref(builder, arr_typ, hjcq__ylm)
        rrxd__ivxg = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=lkfqr__mecf)
        payload_type = DataFramePayloadType(df_typ)
        agwvy__twq = context.nrt.meminfo_data(builder, rrxd__ivxg.meminfo)
        fmo__zsa = context.get_value_type(payload_type).as_pointer()
        agwvy__twq = builder.bitcast(agwvy__twq, fmo__zsa)
        builder.store(hyyyd__mimxv._getvalue(), agwvy__twq)
        return impl_ret_borrowed(context, builder, df_typ, lkfqr__mecf)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        lnv__weoxg = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        rfob__kafq = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=lnv__weoxg)
        iyf__glgb = get_dataframe_payload(context, builder, df_typ, lnv__weoxg)
        rrxd__ivxg = construct_dataframe(context, builder, signature.
            return_type, iyf__glgb.data, index_val, rfob__kafq.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), iyf__glgb.data)
        return rrxd__ivxg
    wfnq__rndc = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(wfnq__rndc, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    goeh__zpews = len(df_type.columns)
    ghatp__bpu = goeh__zpews
    yla__jall = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    owprl__pztiz = col_name not in df_type.columns
    tklk__ixiqg = goeh__zpews
    if owprl__pztiz:
        yla__jall += arr_type,
        column_names += col_name,
        ghatp__bpu += 1
    else:
        tklk__ixiqg = df_type.columns.index(col_name)
        yla__jall = tuple(arr_type if i == tklk__ixiqg else yla__jall[i] for
            i in range(goeh__zpews))

    def codegen(context, builder, signature, args):
        lkfqr__mecf, xgj__sfmkr, hjcq__ylm = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, lkfqr__mecf)
        socc__mrs = cgutils.create_struct_proxy(df_type)(context, builder,
            value=lkfqr__mecf)
        if df_type.is_table_format:
            cebk__eisc = df_type.table_type
            niy__whptt = builder.extract_value(in_dataframe_payload.data, 0)
            yxutb__wvq = TableType(yla__jall)
            ifk__erbuk = set_table_data_codegen(context, builder,
                cebk__eisc, niy__whptt, yxutb__wvq, arr_type, hjcq__ylm,
                tklk__ixiqg, owprl__pztiz)
            data_tup = context.make_tuple(builder, types.Tuple([yxutb__wvq]
                ), [ifk__erbuk])
        else:
            afeo__fobu = [(builder.extract_value(in_dataframe_payload.data,
                i) if i != tklk__ixiqg else hjcq__ylm) for i in range(
                goeh__zpews)]
            if owprl__pztiz:
                afeo__fobu.append(hjcq__ylm)
            for mfni__qvvmu, qhls__wgu in zip(afeo__fobu, yla__jall):
                context.nrt.incref(builder, qhls__wgu, mfni__qvvmu)
            data_tup = context.make_tuple(builder, types.Tuple(yla__jall),
                afeo__fobu)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        xwjst__byevw = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, socc__mrs.parent, None)
        if not owprl__pztiz and arr_type == df_type.data[tklk__ixiqg]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            agwvy__twq = context.nrt.meminfo_data(builder, socc__mrs.meminfo)
            fmo__zsa = context.get_value_type(payload_type).as_pointer()
            agwvy__twq = builder.bitcast(agwvy__twq, fmo__zsa)
            acbzz__dduro = get_dataframe_payload(context, builder, df_type,
                xwjst__byevw)
            builder.store(acbzz__dduro._getvalue(), agwvy__twq)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, yxutb__wvq, builder.
                    extract_value(data_tup, 0))
            else:
                for mfni__qvvmu, qhls__wgu in zip(afeo__fobu, yla__jall):
                    context.nrt.incref(builder, qhls__wgu, mfni__qvvmu)
        has_parent = cgutils.is_not_null(builder, socc__mrs.parent)
        with builder.if_then(has_parent):
            sosme__sgjvu = context.get_python_api(builder)
            ubep__uzuak = sosme__sgjvu.gil_ensure()
            dfgsx__qsa = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, hjcq__ylm)
            axaht__hsv = numba.core.pythonapi._BoxContext(context, builder,
                sosme__sgjvu, dfgsx__qsa)
            gnp__vphq = axaht__hsv.pyapi.from_native_value(arr_type,
                hjcq__ylm, axaht__hsv.env_manager)
            if isinstance(col_name, str):
                xfbz__vwt = context.insert_const_string(builder.module,
                    col_name)
                cjp__hfr = sosme__sgjvu.string_from_string(xfbz__vwt)
            else:
                assert isinstance(col_name, int)
                cjp__hfr = sosme__sgjvu.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            sosme__sgjvu.object_setitem(socc__mrs.parent, cjp__hfr, gnp__vphq)
            sosme__sgjvu.decref(gnp__vphq)
            sosme__sgjvu.decref(cjp__hfr)
            sosme__sgjvu.gil_release(ubep__uzuak)
        return xwjst__byevw
    wfnq__rndc = DataFrameType(yla__jall, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(wfnq__rndc, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    goeh__zpews = len(pyval.columns)
    afeo__fobu = []
    for i in range(goeh__zpews):
        xpip__qibdf = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            gnp__vphq = xpip__qibdf.array
        else:
            gnp__vphq = xpip__qibdf.values
        afeo__fobu.append(gnp__vphq)
    afeo__fobu = tuple(afeo__fobu)
    if df_type.is_table_format:
        udtgq__yjxfs = context.get_constant_generic(builder, df_type.
            table_type, Table(afeo__fobu))
        data_tup = lir.Constant.literal_struct([udtgq__yjxfs])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], cjwqv__btty) for
            i, cjwqv__btty in enumerate(afeo__fobu)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    klzr__kfreq = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, klzr__kfreq])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    xacsh__sax = context.get_constant(types.int64, -1)
    kps__ymyw = context.get_constant_null(types.voidptr)
    xkrkj__fnsaa = lir.Constant.literal_struct([xacsh__sax, kps__ymyw,
        kps__ymyw, payload, xacsh__sax])
    xkrkj__fnsaa = cgutils.global_constant(builder, '.const.meminfo',
        xkrkj__fnsaa).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([xkrkj__fnsaa, klzr__kfreq])


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
        eqw__ugif = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        eqw__ugif = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, eqw__ugif)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        vphzv__xdz = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                vphzv__xdz)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), vphzv__xdz)
    elif not fromty.is_table_format and toty.is_table_format:
        vphzv__xdz = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        vphzv__xdz = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        vphzv__xdz = _cast_df_data_keep_table_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    else:
        vphzv__xdz = _cast_df_data_keep_tuple_format(context, builder,
            fromty, toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, vphzv__xdz,
        eqw__ugif, in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    xqyff__jmkf = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        ntjlu__ghob = get_index_data_arr_types(toty.index)[0]
        xyh__czdeu = bodo.utils.transform.get_type_alloc_counts(ntjlu__ghob
            ) - 1
        pwcv__afeta = ', '.join('0' for xgj__sfmkr in range(xyh__czdeu))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(pwcv__afeta, ', ' if xyh__czdeu == 1 else ''))
        xqyff__jmkf['index_arr_type'] = ntjlu__ghob
    gltqk__ncoji = []
    for i, arr_typ in enumerate(toty.data):
        xyh__czdeu = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        pwcv__afeta = ', '.join('0' for xgj__sfmkr in range(xyh__czdeu))
        llop__fwrp = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'.
            format(i, pwcv__afeta, ', ' if xyh__czdeu == 1 else ''))
        gltqk__ncoji.append(llop__fwrp)
        xqyff__jmkf[f'arr_type{i}'] = arr_typ
    gltqk__ncoji = ', '.join(gltqk__ncoji)
    hoc__iuiez = 'def impl():\n'
    jfy__azkd = bodo.hiframes.dataframe_impl._gen_init_df(hoc__iuiez, toty.
        columns, gltqk__ncoji, index, xqyff__jmkf)
    df = context.compile_internal(builder, jfy__azkd, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    dulpv__syv = toty.table_type
    udtgq__yjxfs = cgutils.create_struct_proxy(dulpv__syv)(context, builder)
    udtgq__yjxfs.parent = in_dataframe_payload.parent
    for dvsfr__mdj, swqx__goz in dulpv__syv.type_to_blk.items():
        qvpc__ciggq = context.get_constant(types.int64, len(dulpv__syv.
            block_to_arr_ind[swqx__goz]))
        xgj__sfmkr, kfr__tajsb = ListInstance.allocate_ex(context, builder,
            types.List(dvsfr__mdj), qvpc__ciggq)
        kfr__tajsb.size = qvpc__ciggq
        setattr(udtgq__yjxfs, f'block_{swqx__goz}', kfr__tajsb.value)
    for i, dvsfr__mdj in enumerate(fromty.data):
        dqndw__aqkys = toty.data[i]
        if dvsfr__mdj != dqndw__aqkys:
            lvnr__ercz = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lvnr__ercz)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        uirri__pyqs = builder.extract_value(in_dataframe_payload.data, i)
        if dvsfr__mdj != dqndw__aqkys:
            dvg__rdoz = context.cast(builder, uirri__pyqs, dvsfr__mdj,
                dqndw__aqkys)
            lxb__krlrr = False
        else:
            dvg__rdoz = uirri__pyqs
            lxb__krlrr = True
        swqx__goz = dulpv__syv.type_to_blk[dvsfr__mdj]
        ziyqw__dklof = getattr(udtgq__yjxfs, f'block_{swqx__goz}')
        bmjk__iuen = ListInstance(context, builder, types.List(dvsfr__mdj),
            ziyqw__dklof)
        hew__qml = context.get_constant(types.int64, dulpv__syv.
            block_offsets[i])
        bmjk__iuen.setitem(hew__qml, dvg__rdoz, lxb__krlrr)
    data_tup = context.make_tuple(builder, types.Tuple([dulpv__syv]), [
        udtgq__yjxfs._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    afeo__fobu = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            lvnr__ercz = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lvnr__ercz)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            uirri__pyqs = builder.extract_value(in_dataframe_payload.data, i)
            dvg__rdoz = context.cast(builder, uirri__pyqs, fromty.data[i],
                toty.data[i])
            lxb__krlrr = False
        else:
            dvg__rdoz = builder.extract_value(in_dataframe_payload.data, i)
            lxb__krlrr = True
        if lxb__krlrr:
            context.nrt.incref(builder, toty.data[i], dvg__rdoz)
        afeo__fobu.append(dvg__rdoz)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), afeo__fobu)
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    cebk__eisc = fromty.table_type
    niy__whptt = cgutils.create_struct_proxy(cebk__eisc)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    yxutb__wvq = toty.table_type
    ifk__erbuk = cgutils.create_struct_proxy(yxutb__wvq)(context, builder)
    ifk__erbuk.parent = in_dataframe_payload.parent
    for dvsfr__mdj, swqx__goz in yxutb__wvq.type_to_blk.items():
        qvpc__ciggq = context.get_constant(types.int64, len(yxutb__wvq.
            block_to_arr_ind[swqx__goz]))
        xgj__sfmkr, kfr__tajsb = ListInstance.allocate_ex(context, builder,
            types.List(dvsfr__mdj), qvpc__ciggq)
        kfr__tajsb.size = qvpc__ciggq
        setattr(ifk__erbuk, f'block_{swqx__goz}', kfr__tajsb.value)
    for i in range(len(fromty.data)):
        axe__uttkn = fromty.data[i]
        dqndw__aqkys = toty.data[i]
        if axe__uttkn != dqndw__aqkys:
            lvnr__ercz = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lvnr__ercz)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        zhkn__ddbca = cebk__eisc.type_to_blk[axe__uttkn]
        xtih__fxayo = getattr(niy__whptt, f'block_{zhkn__ddbca}')
        lgew__ozcq = ListInstance(context, builder, types.List(axe__uttkn),
            xtih__fxayo)
        ahxe__nry = context.get_constant(types.int64, cebk__eisc.
            block_offsets[i])
        uirri__pyqs = lgew__ozcq.getitem(ahxe__nry)
        if axe__uttkn != dqndw__aqkys:
            dvg__rdoz = context.cast(builder, uirri__pyqs, axe__uttkn,
                dqndw__aqkys)
            lxb__krlrr = False
        else:
            dvg__rdoz = uirri__pyqs
            lxb__krlrr = True
        ujtw__hnuj = yxutb__wvq.type_to_blk[dvsfr__mdj]
        kfr__tajsb = getattr(ifk__erbuk, f'block_{ujtw__hnuj}')
        wkd__ybqs = ListInstance(context, builder, types.List(dqndw__aqkys),
            kfr__tajsb)
        wqf__kzg = context.get_constant(types.int64, yxutb__wvq.
            block_offsets[i])
        wkd__ybqs.setitem(wqf__kzg, dvg__rdoz, lxb__krlrr)
    data_tup = context.make_tuple(builder, types.Tuple([yxutb__wvq]), [
        ifk__erbuk._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    dulpv__syv = fromty.table_type
    udtgq__yjxfs = cgutils.create_struct_proxy(dulpv__syv)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    afeo__fobu = []
    for i, dvsfr__mdj in enumerate(toty.data):
        axe__uttkn = fromty.data[i]
        if dvsfr__mdj != axe__uttkn:
            lvnr__ercz = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*lvnr__ercz)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        swqx__goz = dulpv__syv.type_to_blk[dvsfr__mdj]
        ziyqw__dklof = getattr(udtgq__yjxfs, f'block_{swqx__goz}')
        bmjk__iuen = ListInstance(context, builder, types.List(dvsfr__mdj),
            ziyqw__dklof)
        hew__qml = context.get_constant(types.int64, dulpv__syv.
            block_offsets[i])
        uirri__pyqs = bmjk__iuen.getitem(hew__qml)
        if dvsfr__mdj != axe__uttkn:
            dvg__rdoz = context.cast(builder, uirri__pyqs, axe__uttkn,
                dvsfr__mdj)
            lxb__krlrr = False
        else:
            dvg__rdoz = uirri__pyqs
            lxb__krlrr = True
        if lxb__krlrr:
            context.nrt.incref(builder, dvsfr__mdj, dvg__rdoz)
        afeo__fobu.append(dvg__rdoz)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), afeo__fobu)
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    mturd__utrdl, gltqk__ncoji, index_arg = _get_df_args(data, index,
        columns, dtype, copy)
    zxvk__rdlw = gen_const_tup(mturd__utrdl)
    hoc__iuiez = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    hoc__iuiez += (
        '  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, {})\n'
        .format(gltqk__ncoji, index_arg, zxvk__rdlw))
    uyfq__ygas = {}
    exec(hoc__iuiez, {'bodo': bodo, 'np': np}, uyfq__ygas)
    who__yyslp = uyfq__ygas['_init_df']
    return who__yyslp


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    wfnq__rndc = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(wfnq__rndc, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    wfnq__rndc = DataFrameType(to_str_arr_if_dict_array(df_typ.data),
        df_typ.index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(wfnq__rndc, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    iat__debvx = ''
    if not is_overload_none(dtype):
        iat__debvx = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        goeh__zpews = (len(data.types) - 1) // 2
        xwj__grusg = [dvsfr__mdj.literal_value for dvsfr__mdj in data.types
            [1:goeh__zpews + 1]]
        data_val_types = dict(zip(xwj__grusg, data.types[goeh__zpews + 1:]))
        afeo__fobu = ['data[{}]'.format(i) for i in range(goeh__zpews + 1, 
            2 * goeh__zpews + 1)]
        data_dict = dict(zip(xwj__grusg, afeo__fobu))
        if is_overload_none(index):
            for i, dvsfr__mdj in enumerate(data.types[goeh__zpews + 1:]):
                if isinstance(dvsfr__mdj, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(goeh__zpews + 1 + i))
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
        euj__fpb = '.copy()' if copy else ''
        hgqit__vwpb = get_overload_const_list(columns)
        goeh__zpews = len(hgqit__vwpb)
        data_val_types = {axaht__hsv: data.copy(ndim=1) for axaht__hsv in
            hgqit__vwpb}
        afeo__fobu = ['data[:,{}]{}'.format(i, euj__fpb) for i in range(
            goeh__zpews)]
        data_dict = dict(zip(hgqit__vwpb, afeo__fobu))
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
    gltqk__ncoji = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[axaht__hsv], df_len, iat__debvx) for axaht__hsv in
        col_names))
    if len(col_names) == 0:
        gltqk__ncoji = '()'
    return col_names, gltqk__ncoji, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for axaht__hsv in col_names:
        if axaht__hsv in data_dict and is_iterable_type(data_val_types[
            axaht__hsv]):
            df_len = 'len({})'.format(data_dict[axaht__hsv])
            break
    if df_len == '0' and not index_is_none:
        df_len = f'len({index_arg})'
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(axaht__hsv in data_dict for axaht__hsv in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    ymd__tna = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len,
        dtype)
    for axaht__hsv in col_names:
        if axaht__hsv not in data_dict:
            data_dict[axaht__hsv] = ymd__tna


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
            dvsfr__mdj = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(dvsfr__mdj)
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
        eijyo__ozz = idx.literal_value
        if isinstance(eijyo__ozz, int):
            mqfl__vaxg = tup.types[eijyo__ozz]
        elif isinstance(eijyo__ozz, slice):
            mqfl__vaxg = types.BaseTuple.from_types(tup.types[eijyo__ozz])
        return signature(mqfl__vaxg, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    qtc__cmg, idx = sig.args
    idx = idx.literal_value
    tup, xgj__sfmkr = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(qtc__cmg)
        if not 0 <= idx < len(qtc__cmg):
            raise IndexError('cannot index at %d in %s' % (idx, qtc__cmg))
        owwnm__wmirk = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        grv__uyw = cgutils.unpack_tuple(builder, tup)[idx]
        owwnm__wmirk = context.make_tuple(builder, sig.return_type, grv__uyw)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, owwnm__wmirk)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, koqmf__lyd, suffix_x,
            suffix_y, is_join, indicator, _bodo_na_equal, cuikh__cyrl) = args
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        eigvw__fsf = set(left_on) & set(right_on)
        wpl__mdzk = set(left_df.columns) & set(right_df.columns)
        vwzi__badnl = wpl__mdzk - eigvw__fsf
        itay__wmrz = '$_bodo_index_' in left_on
        bnpfx__aebp = '$_bodo_index_' in right_on
        how = get_overload_const_str(koqmf__lyd)
        snpmm__pgakc = how in {'left', 'outer'}
        hqskw__atznl = how in {'right', 'outer'}
        columns = []
        data = []
        if itay__wmrz:
            mkr__njkcw = bodo.utils.typing.get_index_data_arr_types(left_df
                .index)[0]
        else:
            mkr__njkcw = left_df.data[left_df.columns.index(left_on[0])]
        if bnpfx__aebp:
            tlns__sdc = bodo.utils.typing.get_index_data_arr_types(right_df
                .index)[0]
        else:
            tlns__sdc = right_df.data[right_df.columns.index(right_on[0])]
        if itay__wmrz and not bnpfx__aebp and not is_join.literal_value:
            fgh__puyi = right_on[0]
            if fgh__puyi in left_df.columns:
                columns.append(fgh__puyi)
                if (tlns__sdc == bodo.dict_str_arr_type and mkr__njkcw ==
                    bodo.string_array_type):
                    rmfd__pwtwx = bodo.string_array_type
                else:
                    rmfd__pwtwx = tlns__sdc
                data.append(rmfd__pwtwx)
        if bnpfx__aebp and not itay__wmrz and not is_join.literal_value:
            ibps__gmxd = left_on[0]
            if ibps__gmxd in right_df.columns:
                columns.append(ibps__gmxd)
                if (mkr__njkcw == bodo.dict_str_arr_type and tlns__sdc ==
                    bodo.string_array_type):
                    rmfd__pwtwx = bodo.string_array_type
                else:
                    rmfd__pwtwx = mkr__njkcw
                data.append(rmfd__pwtwx)
        for axe__uttkn, xpip__qibdf in zip(left_df.data, left_df.columns):
            columns.append(str(xpip__qibdf) + suffix_x.literal_value if 
                xpip__qibdf in vwzi__badnl else xpip__qibdf)
            if xpip__qibdf in eigvw__fsf:
                if axe__uttkn == bodo.dict_str_arr_type:
                    axe__uttkn = right_df.data[right_df.columns.index(
                        xpip__qibdf)]
                data.append(axe__uttkn)
            else:
                if (axe__uttkn == bodo.dict_str_arr_type and xpip__qibdf in
                    left_on):
                    if bnpfx__aebp:
                        axe__uttkn = tlns__sdc
                    else:
                        wvjqz__imt = left_on.index(xpip__qibdf)
                        zgag__vuse = right_on[wvjqz__imt]
                        axe__uttkn = right_df.data[right_df.columns.index(
                            zgag__vuse)]
                if hqskw__atznl:
                    axe__uttkn = to_nullable_type(axe__uttkn)
                data.append(axe__uttkn)
        for axe__uttkn, xpip__qibdf in zip(right_df.data, right_df.columns):
            if xpip__qibdf not in eigvw__fsf:
                columns.append(str(xpip__qibdf) + suffix_y.literal_value if
                    xpip__qibdf in vwzi__badnl else xpip__qibdf)
                if (axe__uttkn == bodo.dict_str_arr_type and xpip__qibdf in
                    right_on):
                    if itay__wmrz:
                        axe__uttkn = mkr__njkcw
                    else:
                        wvjqz__imt = right_on.index(xpip__qibdf)
                        wjh__nbkd = left_on[wvjqz__imt]
                        axe__uttkn = left_df.data[left_df.columns.index(
                            wjh__nbkd)]
                if snpmm__pgakc:
                    axe__uttkn = to_nullable_type(axe__uttkn)
                data.append(axe__uttkn)
        mhjm__qhtuk = get_overload_const_bool(indicator)
        if mhjm__qhtuk:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        if itay__wmrz and bnpfx__aebp and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif itay__wmrz and not bnpfx__aebp:
            index_typ = right_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        elif bnpfx__aebp and not itay__wmrz:
            index_typ = left_df.index
            if isinstance(index_typ, bodo.hiframes.pd_index_ext.RangeIndexType
                ):
                index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types
                    .int64)
        trv__ett = DataFrameType(tuple(data), index_typ, tuple(columns))
        return signature(trv__ett, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    rrxd__ivxg = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return rrxd__ivxg._getvalue()


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
    qcam__myb = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    kbf__ymy = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', qcam__myb, kbf__ymy,
        package_name='pandas', module_name='General')
    hoc__iuiez = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        pfti__ahuud = 0
        gltqk__ncoji = []
        names = []
        for i, fydxw__luxk in enumerate(objs.types):
            assert isinstance(fydxw__luxk, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(fydxw__luxk, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                fydxw__luxk, 'pandas.concat()')
            if isinstance(fydxw__luxk, SeriesType):
                names.append(str(pfti__ahuud))
                pfti__ahuud += 1
                gltqk__ncoji.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(fydxw__luxk.columns)
                for clybe__qcza in range(len(fydxw__luxk.data)):
                    gltqk__ncoji.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, clybe__qcza))
        return bodo.hiframes.dataframe_impl._gen_init_df(hoc__iuiez, names,
            ', '.join(gltqk__ncoji), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(dvsfr__mdj, DataFrameType) for dvsfr__mdj in
            objs.types)
        pojbf__ltow = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
                'pandas.concat()')
            pojbf__ltow.extend(df.columns)
        pojbf__ltow = list(dict.fromkeys(pojbf__ltow).keys())
        vwy__ofn = {}
        for pfti__ahuud, axaht__hsv in enumerate(pojbf__ltow):
            for df in objs.types:
                if axaht__hsv in df.columns:
                    vwy__ofn['arr_typ{}'.format(pfti__ahuud)] = df.data[df.
                        columns.index(axaht__hsv)]
                    break
        assert len(vwy__ofn) == len(pojbf__ltow)
        yaua__fhoa = []
        for pfti__ahuud, axaht__hsv in enumerate(pojbf__ltow):
            args = []
            for i, df in enumerate(objs.types):
                if axaht__hsv in df.columns:
                    tklk__ixiqg = df.columns.index(axaht__hsv)
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, tklk__ixiqg))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, pfti__ahuud))
            hoc__iuiez += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(pfti__ahuud, ', '.join(args)))
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
        return bodo.hiframes.dataframe_impl._gen_init_df(hoc__iuiez,
            pojbf__ltow, ', '.join('A{}'.format(i) for i in range(len(
            pojbf__ltow))), index, vwy__ofn)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(dvsfr__mdj, SeriesType) for dvsfr__mdj in
            objs.types)
        hoc__iuiez += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            hoc__iuiez += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            hoc__iuiez += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        hoc__iuiez += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        uyfq__ygas = {}
        exec(hoc__iuiez, {'bodo': bodo, 'np': np, 'numba': numba}, uyfq__ygas)
        return uyfq__ygas['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for pfti__ahuud, axaht__hsv in enumerate(df_type.columns):
            hoc__iuiez += '  arrs{} = []\n'.format(pfti__ahuud)
            hoc__iuiez += '  for i in range(len(objs)):\n'
            hoc__iuiez += '    df = objs[i]\n'
            hoc__iuiez += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(pfti__ahuud))
            hoc__iuiez += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(pfti__ahuud))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            hoc__iuiez += '  arrs_index = []\n'
            hoc__iuiez += '  for i in range(len(objs)):\n'
            hoc__iuiez += '    df = objs[i]\n'
            hoc__iuiez += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(hoc__iuiez,
            df_type.columns, ', '.join('out_arr{}'.format(i) for i in range
            (len(df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        hoc__iuiez += '  arrs = []\n'
        hoc__iuiez += '  for i in range(len(objs)):\n'
        hoc__iuiez += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        hoc__iuiez += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            hoc__iuiez += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            hoc__iuiez += '  arrs_index = []\n'
            hoc__iuiez += '  for i in range(len(objs)):\n'
            hoc__iuiez += '    S = objs[i]\n'
            hoc__iuiez += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            hoc__iuiez += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        hoc__iuiez += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        uyfq__ygas = {}
        exec(hoc__iuiez, {'bodo': bodo, 'np': np, 'numba': numba}, uyfq__ygas)
        return uyfq__ygas['impl']
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
        wfnq__rndc = df.copy(index=index, is_table_format=False)
        return signature(wfnq__rndc, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    tqs__hnond = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return tqs__hnond._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    qcam__myb = dict(index=index, name=name)
    kbf__ymy = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', qcam__myb, kbf__ymy,
        package_name='pandas', module_name='DataFrame')

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
        vwy__ofn = (types.Array(types.int64, 1, 'C'),) + df.data
        lzrzp__ffmp = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, vwy__ofn)
        return signature(lzrzp__ffmp, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    tqs__hnond = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return tqs__hnond._getvalue()


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
    tqs__hnond = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return tqs__hnond._getvalue()


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
    tqs__hnond = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return tqs__hnond._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True, parallel
    =False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    hwx__kyggl = get_overload_const_bool(check_duplicates)
    ddj__seu = not is_overload_none(value_names)
    rgbwv__asxm = isinstance(values_tup, types.UniTuple)
    if rgbwv__asxm:
        htdfq__bssu = [to_nullable_type(values_tup.dtype)]
    else:
        htdfq__bssu = [to_nullable_type(qhls__wgu) for qhls__wgu in values_tup]
    hoc__iuiez = 'def impl(\n'
    hoc__iuiez += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, parallel=False
"""
    hoc__iuiez += '):\n'
    hoc__iuiez += '    if parallel:\n'
    apdj__mkco = ', '.join([f'array_to_info(index_tup[{i}])' for i in range
        (len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for i in
        range(len(columns_tup))] + [f'array_to_info(values_tup[{i}])' for i in
        range(len(values_tup))])
    hoc__iuiez += f'        info_list = [{apdj__mkco}]\n'
    hoc__iuiez += '        cpp_table = arr_info_list_to_table(info_list)\n'
    hoc__iuiez += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
    glesb__mwyr = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
         for i in range(len(index_tup))])
    xybxk__vom = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
         for i in range(len(columns_tup))])
    buhg__aphaz = ', '.join([
        f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
         for i in range(len(values_tup))])
    hoc__iuiez += f'        index_tup = ({glesb__mwyr},)\n'
    hoc__iuiez += f'        columns_tup = ({xybxk__vom},)\n'
    hoc__iuiez += f'        values_tup = ({buhg__aphaz},)\n'
    hoc__iuiez += '        delete_table(cpp_table)\n'
    hoc__iuiez += '        delete_table(out_cpp_table)\n'
    hoc__iuiez += '    columns_arr = columns_tup[0]\n'
    if rgbwv__asxm:
        hoc__iuiez += '    values_arrs = [arr for arr in values_tup]\n'
    hoc__iuiez += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    hoc__iuiez += '        index_tup\n'
    hoc__iuiez += '    )\n'
    hoc__iuiez += '    n_rows = len(unique_index_arr_tup[0])\n'
    hoc__iuiez += '    num_values_arrays = len(values_tup)\n'
    hoc__iuiez += '    n_unique_pivots = len(pivot_values)\n'
    if rgbwv__asxm:
        hoc__iuiez += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        hoc__iuiez += '    n_cols = n_unique_pivots\n'
    hoc__iuiez += '    col_map = {}\n'
    hoc__iuiez += '    for i in range(n_unique_pivots):\n'
    hoc__iuiez += '        if bodo.libs.array_kernels.isna(pivot_values, i):\n'
    hoc__iuiez += '            raise ValueError(\n'
    hoc__iuiez += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    hoc__iuiez += '            )\n'
    hoc__iuiez += '        col_map[pivot_values[i]] = i\n'
    eybm__gshh = False
    for i, gjd__qufej in enumerate(htdfq__bssu):
        if is_str_arr_type(gjd__qufej):
            eybm__gshh = True
            hoc__iuiez += f"""    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]
"""
            hoc__iuiez += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if eybm__gshh:
        if hwx__kyggl:
            hoc__iuiez += '    nbytes = (n_rows + 7) >> 3\n'
            hoc__iuiez += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        hoc__iuiez += '    for i in range(len(columns_arr)):\n'
        hoc__iuiez += '        col_name = columns_arr[i]\n'
        hoc__iuiez += '        pivot_idx = col_map[col_name]\n'
        hoc__iuiez += '        row_idx = row_vector[i]\n'
        if hwx__kyggl:
            hoc__iuiez += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            hoc__iuiez += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            hoc__iuiez += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            hoc__iuiez += '        else:\n'
            hoc__iuiez += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if rgbwv__asxm:
            hoc__iuiez += '        for j in range(num_values_arrays):\n'
            hoc__iuiez += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            hoc__iuiez += '            len_arr = len_arrs_0[col_idx]\n'
            hoc__iuiez += '            values_arr = values_arrs[j]\n'
            hoc__iuiez += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            hoc__iuiez += (
                '                len_arr[row_idx] = len(values_arr[i])\n')
            hoc__iuiez += (
                '                total_lens_0[col_idx] += len(values_arr[i])\n'
                )
        else:
            for i, gjd__qufej in enumerate(htdfq__bssu):
                if is_str_arr_type(gjd__qufej):
                    hoc__iuiez += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    hoc__iuiez += f"""            len_arrs_{i}[pivot_idx][row_idx] = len(values_tup[{i}][i])
"""
                    hoc__iuiez += f"""            total_lens_{i}[pivot_idx] += len(values_tup[{i}][i])
"""
    for i, gjd__qufej in enumerate(htdfq__bssu):
        if is_str_arr_type(gjd__qufej):
            hoc__iuiez += f'    data_arrs_{i} = [\n'
            hoc__iuiez += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            hoc__iuiez += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            hoc__iuiez += '        )\n'
            hoc__iuiez += '        for i in range(n_cols)\n'
            hoc__iuiez += '    ]\n'
        else:
            hoc__iuiez += f'    data_arrs_{i} = [\n'
            hoc__iuiez += f"""        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})
"""
            hoc__iuiez += '        for _ in range(n_cols)\n'
            hoc__iuiez += '    ]\n'
    if not eybm__gshh and hwx__kyggl:
        hoc__iuiez += '    nbytes = (n_rows + 7) >> 3\n'
        hoc__iuiez += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    hoc__iuiez += '    for i in range(len(columns_arr)):\n'
    hoc__iuiez += '        col_name = columns_arr[i]\n'
    hoc__iuiez += '        pivot_idx = col_map[col_name]\n'
    hoc__iuiez += '        row_idx = row_vector[i]\n'
    if not eybm__gshh and hwx__kyggl:
        hoc__iuiez += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        hoc__iuiez += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
        hoc__iuiez += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        hoc__iuiez += '        else:\n'
        hoc__iuiez += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)\n'
            )
    if rgbwv__asxm:
        hoc__iuiez += '        for j in range(num_values_arrays):\n'
        hoc__iuiez += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        hoc__iuiez += '            col_arr = data_arrs_0[col_idx]\n'
        hoc__iuiez += '            values_arr = values_arrs[j]\n'
        hoc__iuiez += (
            '            if bodo.libs.array_kernels.isna(values_arr, i):\n')
        hoc__iuiez += (
            '                bodo.libs.array_kernels.setna(col_arr, row_idx)\n'
            )
        hoc__iuiez += '            else:\n'
        hoc__iuiez += '                col_arr[row_idx] = values_arr[i]\n'
    else:
        for i, gjd__qufej in enumerate(htdfq__bssu):
            hoc__iuiez += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            hoc__iuiez += (
                f'        if bodo.libs.array_kernels.isna(values_tup[{i}], i):\n'
                )
            hoc__iuiez += (
                f'            bodo.libs.array_kernels.setna(col_arr_{i}, row_idx)\n'
                )
            hoc__iuiez += f'        else:\n'
            hoc__iuiez += (
                f'            col_arr_{i}[row_idx] = values_tup[{i}][i]\n')
    if len(index_tup) == 1:
        hoc__iuiez += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names[0])
"""
    else:
        hoc__iuiez += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names, None)
"""
    if ddj__seu:
        hoc__iuiez += '    num_rows = len(value_names) * len(pivot_values)\n'
        if is_str_arr_type(value_names):
            hoc__iuiez += '    total_chars = 0\n'
            hoc__iuiez += '    for i in range(len(value_names)):\n'
            hoc__iuiez += '        total_chars += len(value_names[i])\n'
            hoc__iuiez += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
        else:
            hoc__iuiez += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names, (-1,))
"""
        if is_str_arr_type(pivot_values):
            hoc__iuiez += '    total_chars = 0\n'
            hoc__iuiez += '    for i in range(len(pivot_values)):\n'
            hoc__iuiez += '        total_chars += len(pivot_values[i])\n'
            hoc__iuiez += """    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(value_names))
"""
        else:
            hoc__iuiez += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
        hoc__iuiez += '    for i in range(len(value_names)):\n'
        hoc__iuiez += '        for j in range(len(pivot_values)):\n'
        hoc__iuiez += (
            '            new_value_names[(i * len(pivot_values)) + j] = value_names[i]\n'
            )
        hoc__iuiez += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
        hoc__iuiez += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name), None)
"""
    else:
        hoc__iuiez += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name)
"""
    mxea__asa = ', '.join(f'data_arrs_{i}' for i in range(len(htdfq__bssu)))
    hoc__iuiez += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({mxea__asa},), n_rows)
"""
    hoc__iuiez += (
        '    return bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
        )
    hoc__iuiez += '        (table,), index, column_index\n'
    hoc__iuiez += '    )\n'
    uyfq__ygas = {}
    cofh__dia = {f'data_arr_typ_{i}': gjd__qufej for i, gjd__qufej in
        enumerate(htdfq__bssu)}
    liv__jdyhh = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, **cofh__dia}
    exec(hoc__iuiez, liv__jdyhh, uyfq__ygas)
    impl = uyfq__ygas['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    ool__wrxj = {}
    ool__wrxj['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, aan__xyr in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        ipm__nmqku = None
        if isinstance(aan__xyr, bodo.DatetimeArrayType):
            sxdi__qomrb = 'datetimetz'
            wvj__gdi = 'datetime64[ns]'
            if isinstance(aan__xyr.tz, int):
                oiiag__cbb = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(aan__xyr.tz))
            else:
                oiiag__cbb = pd.DatetimeTZDtype(tz=aan__xyr.tz).tz
            ipm__nmqku = {'timezone': pa.lib.tzinfo_to_string(oiiag__cbb)}
        elif isinstance(aan__xyr, types.Array) or aan__xyr == boolean_array:
            sxdi__qomrb = wvj__gdi = aan__xyr.dtype.name
            if wvj__gdi.startswith('datetime'):
                sxdi__qomrb = 'datetime'
        elif is_str_arr_type(aan__xyr):
            sxdi__qomrb = 'unicode'
            wvj__gdi = 'object'
        elif aan__xyr == binary_array_type:
            sxdi__qomrb = 'bytes'
            wvj__gdi = 'object'
        elif isinstance(aan__xyr, DecimalArrayType):
            sxdi__qomrb = wvj__gdi = 'object'
        elif isinstance(aan__xyr, IntegerArrayType):
            wufci__uzcov = aan__xyr.dtype.name
            if wufci__uzcov.startswith('int'):
                sxdi__qomrb = 'Int' + wufci__uzcov[3:]
            elif wufci__uzcov.startswith('uint'):
                sxdi__qomrb = 'UInt' + wufci__uzcov[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, aan__xyr))
            wvj__gdi = aan__xyr.dtype.name
        elif aan__xyr == datetime_date_array_type:
            sxdi__qomrb = 'datetime'
            wvj__gdi = 'object'
        elif isinstance(aan__xyr, (StructArrayType, ArrayItemArrayType)):
            sxdi__qomrb = 'object'
            wvj__gdi = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, aan__xyr))
        xegz__nsxo = {'name': col_name, 'field_name': col_name,
            'pandas_type': sxdi__qomrb, 'numpy_type': wvj__gdi, 'metadata':
            ipm__nmqku}
        ool__wrxj['columns'].append(xegz__nsxo)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            dhp__kdegm = '__index_level_0__'
            jrpn__ywvwg = None
        else:
            dhp__kdegm = '%s'
            jrpn__ywvwg = '%s'
        ool__wrxj['index_columns'] = [dhp__kdegm]
        ool__wrxj['columns'].append({'name': jrpn__ywvwg, 'field_name':
            dhp__kdegm, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        ool__wrxj['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        ool__wrxj['index_columns'] = []
    ool__wrxj['pandas_version'] = pd.__version__
    return ool__wrxj


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
        jtp__mmfv = []
        for jbasx__dsge in partition_cols:
            try:
                idx = df.columns.index(jbasx__dsge)
            except ValueError as awm__jhri:
                raise BodoError(
                    f'Partition column {jbasx__dsge} is not in dataframe')
            jtp__mmfv.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    xvn__wjugb = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType
        )
    mhhyc__msd = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not xvn__wjugb)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not xvn__wjugb or
        is_overload_true(_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and xvn__wjugb and not is_overload_true(_is_parallel)
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
        ccz__qfx = df.runtime_data_types
        zii__nub = len(ccz__qfx)
        ipm__nmqku = gen_pandas_parquet_metadata([''] * zii__nub, ccz__qfx,
            df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        kwr__wmdpv = ipm__nmqku['columns'][:zii__nub]
        ipm__nmqku['columns'] = ipm__nmqku['columns'][zii__nub:]
        kwr__wmdpv = [json.dumps(wsvk__nxs).replace('""', '{0}') for
            wsvk__nxs in kwr__wmdpv]
        qvwv__guvts = json.dumps(ipm__nmqku)
        zazeo__mgzm = '"columns": ['
        bzrfa__vix = qvwv__guvts.find(zazeo__mgzm)
        if bzrfa__vix == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        iwmd__vdomb = bzrfa__vix + len(zazeo__mgzm)
        erah__qske = qvwv__guvts[:iwmd__vdomb]
        qvwv__guvts = qvwv__guvts[iwmd__vdomb:]
        llhe__wsate = len(ipm__nmqku['columns'])
    else:
        qvwv__guvts = json.dumps(gen_pandas_parquet_metadata(df.columns, df
            .data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and xvn__wjugb:
        qvwv__guvts = qvwv__guvts.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            qvwv__guvts = qvwv__guvts.replace('"%s"', '%s')
    if not df.is_table_format:
        gltqk__ncoji = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    hoc__iuiez = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _is_parallel=False):
"""
    if df.is_table_format:
        hoc__iuiez += '    py_table = get_dataframe_table(df)\n'
        hoc__iuiez += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        hoc__iuiez += '    info_list = [{}]\n'.format(gltqk__ncoji)
        hoc__iuiez += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        hoc__iuiez += '    columns_index = get_dataframe_column_names(df)\n'
        hoc__iuiez += '    names_arr = index_to_array(columns_index)\n'
        hoc__iuiez += '    col_names = array_to_info(names_arr)\n'
    else:
        hoc__iuiez += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and mhhyc__msd:
        hoc__iuiez += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        rzb__btks = True
    else:
        hoc__iuiez += '    index_col = array_to_info(np.empty(0))\n'
        rzb__btks = False
    if df.has_runtime_cols:
        hoc__iuiez += '    columns_lst = []\n'
        hoc__iuiez += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            hoc__iuiez += f'    for _ in range(len(py_table.block_{i})):\n'
            hoc__iuiez += f"""        columns_lst.append({kwr__wmdpv[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            hoc__iuiez += '        num_cols += 1\n'
        if llhe__wsate:
            hoc__iuiez += "    columns_lst.append('')\n"
        hoc__iuiez += '    columns_str = ", ".join(columns_lst)\n'
        hoc__iuiez += ('    metadata = """' + erah__qske +
            '""" + columns_str + """' + qvwv__guvts + '"""\n')
    else:
        hoc__iuiez += '    metadata = """' + qvwv__guvts + '"""\n'
    hoc__iuiez += '    if compression is None:\n'
    hoc__iuiez += "        compression = 'none'\n"
    hoc__iuiez += '    if df.index.name is not None:\n'
    hoc__iuiez += '        name_ptr = df.index.name\n'
    hoc__iuiez += '    else:\n'
    hoc__iuiez += "        name_ptr = 'null'\n"
    hoc__iuiez += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    nllur__rlij = None
    if partition_cols:
        nllur__rlij = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        qygw__tgrj = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in jtp__mmfv)
        if qygw__tgrj:
            hoc__iuiez += '    cat_info_list = [{}]\n'.format(qygw__tgrj)
            hoc__iuiez += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            hoc__iuiez += '    cat_table = table\n'
        hoc__iuiez += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        hoc__iuiez += (
            f'    part_cols_idxs = np.array({jtp__mmfv}, dtype=np.int32)\n')
        hoc__iuiez += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        hoc__iuiez += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        hoc__iuiez += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        hoc__iuiez += (
            '                            unicode_to_utf8(compression),\n')
        hoc__iuiez += '                            _is_parallel,\n'
        hoc__iuiez += (
            '                            unicode_to_utf8(bucket_region),\n')
        hoc__iuiez += '                            row_group_size)\n'
        hoc__iuiez += '    delete_table_decref_arrays(table)\n'
        hoc__iuiez += '    delete_info_decref_array(index_col)\n'
        hoc__iuiez += '    delete_info_decref_array(col_names_no_partitions)\n'
        hoc__iuiez += '    delete_info_decref_array(col_names)\n'
        if qygw__tgrj:
            hoc__iuiez += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        hoc__iuiez += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        hoc__iuiez += (
            '                            table, col_names, index_col,\n')
        hoc__iuiez += '                            ' + str(rzb__btks) + ',\n'
        hoc__iuiez += (
            '                            unicode_to_utf8(metadata),\n')
        hoc__iuiez += (
            '                            unicode_to_utf8(compression),\n')
        hoc__iuiez += (
            '                            _is_parallel, 1, df.index.start,\n')
        hoc__iuiez += (
            '                            df.index.stop, df.index.step,\n')
        hoc__iuiez += (
            '                            unicode_to_utf8(name_ptr),\n')
        hoc__iuiez += (
            '                            unicode_to_utf8(bucket_region),\n')
        hoc__iuiez += '                            row_group_size)\n'
        hoc__iuiez += '    delete_table_decref_arrays(table)\n'
        hoc__iuiez += '    delete_info_decref_array(index_col)\n'
        hoc__iuiez += '    delete_info_decref_array(col_names)\n'
    else:
        hoc__iuiez += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        hoc__iuiez += (
            '                            table, col_names, index_col,\n')
        hoc__iuiez += '                            ' + str(rzb__btks) + ',\n'
        hoc__iuiez += (
            '                            unicode_to_utf8(metadata),\n')
        hoc__iuiez += (
            '                            unicode_to_utf8(compression),\n')
        hoc__iuiez += '                            _is_parallel, 0, 0, 0, 0,\n'
        hoc__iuiez += (
            '                            unicode_to_utf8(name_ptr),\n')
        hoc__iuiez += (
            '                            unicode_to_utf8(bucket_region),\n')
        hoc__iuiez += '                            row_group_size)\n'
        hoc__iuiez += '    delete_table_decref_arrays(table)\n'
        hoc__iuiez += '    delete_info_decref_array(index_col)\n'
        hoc__iuiez += '    delete_info_decref_array(col_names)\n'
    uyfq__ygas = {}
    if df.has_runtime_cols:
        sebqi__ldty = None
    else:
        for xpip__qibdf in df.columns:
            if not isinstance(xpip__qibdf, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        sebqi__ldty = pd.array(df.columns)
    exec(hoc__iuiez, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': sebqi__ldty,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': nllur__rlij, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, uyfq__ygas)
    esdrr__tjmz = uyfq__ygas['df_to_parquet']
    return esdrr__tjmz


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    jnavk__dstwx = 'all_ok'
    kuquq__rct, raq__ebyb = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        jqqqx__fflk = 100
        if chunksize is None:
            qkcz__mmhq = jqqqx__fflk
        else:
            qkcz__mmhq = min(chunksize, jqqqx__fflk)
        if _is_table_create:
            df = df.iloc[:qkcz__mmhq, :]
        else:
            df = df.iloc[qkcz__mmhq:, :]
            if len(df) == 0:
                return jnavk__dstwx
    rizfl__odil = df.columns
    try:
        if kuquq__rct == 'snowflake':
            if raq__ebyb and con.count(raq__ebyb) == 1:
                con = con.replace(raq__ebyb, quote(raq__ebyb))
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
                df.columns = [(axaht__hsv.upper() if axaht__hsv.islower() else
                    axaht__hsv) for axaht__hsv in df.columns]
            except ImportError as awm__jhri:
                jnavk__dstwx = (
                    "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires both snowflake-sqlalchemy and snowflake-connector-python. These can be installed by calling 'conda install -c conda-forge snowflake-sqlalchemy snowflake-connector-python' or 'pip install snowflake-sqlalchemy snowflake-connector-python'."
                    )
                return jnavk__dstwx
        try:
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
        except Exception as nxdlj__gcoj:
            jnavk__dstwx = nxdlj__gcoj.args[0]
        return jnavk__dstwx
    finally:
        df.columns = rizfl__odil


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
        msy__ghp = bodo.libs.distributed_api.get_rank()
        jnavk__dstwx = 'unset'
        if msy__ghp != 0:
            jnavk__dstwx = bcast_scalar(jnavk__dstwx)
        elif msy__ghp == 0:
            jnavk__dstwx = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, True, _is_parallel)
            jnavk__dstwx = bcast_scalar(jnavk__dstwx)
        if_exists = 'append'
        if _is_parallel and jnavk__dstwx == 'all_ok':
            jnavk__dstwx = to_sql_exception_guard_encaps(df, name, con,
                schema, if_exists, index, index_label, chunksize, dtype,
                method, False, _is_parallel)
        if jnavk__dstwx != 'all_ok':
            print('err_msg=', jnavk__dstwx)
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
        edzyl__olw = get_overload_const_str(path_or_buf)
        if edzyl__olw.endswith(('.gz', '.bz2', '.zip', '.xz')):
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
        anwh__abvq = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(anwh__abvq))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(anwh__abvq))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    qyj__byhbz = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    hur__sbks = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', qyj__byhbz, hur__sbks,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    hoc__iuiez = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        ewgp__vyj = data.data.dtype.categories
        hoc__iuiez += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        ewgp__vyj = data.dtype.categories
        hoc__iuiez += '  data_values = data\n'
    goeh__zpews = len(ewgp__vyj)
    hoc__iuiez += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    hoc__iuiez += '  numba.parfors.parfor.init_prange()\n'
    hoc__iuiez += '  n = len(data_values)\n'
    for i in range(goeh__zpews):
        hoc__iuiez += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    hoc__iuiez += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    hoc__iuiez += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for clybe__qcza in range(goeh__zpews):
        hoc__iuiez += '          data_arr_{}[i] = 0\n'.format(clybe__qcza)
    hoc__iuiez += '      else:\n'
    for rhlqv__vfu in range(goeh__zpews):
        hoc__iuiez += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            rhlqv__vfu)
    gltqk__ncoji = ', '.join(f'data_arr_{i}' for i in range(goeh__zpews))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(ewgp__vyj[0], np.datetime64):
        ewgp__vyj = tuple(pd.Timestamp(axaht__hsv) for axaht__hsv in ewgp__vyj)
    elif isinstance(ewgp__vyj[0], np.timedelta64):
        ewgp__vyj = tuple(pd.Timedelta(axaht__hsv) for axaht__hsv in ewgp__vyj)
    return bodo.hiframes.dataframe_impl._gen_init_df(hoc__iuiez, ewgp__vyj,
        gltqk__ncoji, index)


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
    for ztdgz__agbx in pd_unsupported:
        ifm__lgh = mod_name + '.' + ztdgz__agbx.__name__
        overload(ztdgz__agbx, no_unliteral=True)(create_unsupported_overload
            (ifm__lgh))


def _install_dataframe_unsupported():
    for tks__muwzk in dataframe_unsupported_attrs:
        iwpx__wjuq = 'DataFrame.' + tks__muwzk
        overload_attribute(DataFrameType, tks__muwzk)(
            create_unsupported_overload(iwpx__wjuq))
    for ifm__lgh in dataframe_unsupported:
        iwpx__wjuq = 'DataFrame.' + ifm__lgh + '()'
        overload_method(DataFrameType, ifm__lgh)(create_unsupported_overload
            (iwpx__wjuq))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
