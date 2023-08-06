"""
Indexing support for pd.DataFrame type.
"""
import operator
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.utils.transform import gen_const_tup
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_list, get_overload_const_str, is_immutable_array, is_list_like_index_type, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, raise_bodo_error


@infer_global(operator.getitem)
class DataFrameGetItemTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        check_runtime_cols_unsupported(args[0], 'DataFrame getitem (df[])')
        if isinstance(args[0], DataFrameType):
            return self.typecheck_df_getitem(args)
        elif isinstance(args[0], DataFrameLocType):
            return self.typecheck_loc_getitem(args)
        else:
            return

    def typecheck_loc_getitem(self, args):
        I = args[0]
        idx = args[1]
        df = I.df_type
        if isinstance(df.columns[0], tuple):
            raise_bodo_error(
                'DataFrame.loc[] getitem (location-based indexing) with multi-indexed columns not supported yet'
                )
        if is_list_like_index_type(idx) and idx.dtype == types.bool_:
            pqjy__toq = idx
            fyioe__zykg = df.data
            mfsgv__jfrkx = df.columns
            bie__aduvl = self.replace_range_with_numeric_idx_if_needed(df,
                pqjy__toq)
            spke__xwhoa = DataFrameType(fyioe__zykg, bie__aduvl, mfsgv__jfrkx)
            return spke__xwhoa(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            retz__ainxr = idx.types[0]
            xfggh__ate = idx.types[1]
            if isinstance(retz__ainxr, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(xfggh__ate):
                    fxeia__xgci = get_overload_const_str(xfggh__ate)
                    if fxeia__xgci not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, fxeia__xgci))
                    loinu__hnxv = df.columns.index(fxeia__xgci)
                    return df.data[loinu__hnxv].dtype(*args)
                if isinstance(xfggh__ate, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(retz__ainxr
                ) and retz__ainxr.dtype == types.bool_ or isinstance(
                retz__ainxr, types.SliceType):
                bie__aduvl = self.replace_range_with_numeric_idx_if_needed(df,
                    retz__ainxr)
                if is_overload_constant_str(xfggh__ate):
                    ftbey__xjch = get_overload_const_str(xfggh__ate)
                    if ftbey__xjch not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {ftbey__xjch}'
                            )
                    loinu__hnxv = df.columns.index(ftbey__xjch)
                    yxmqq__ulv = df.data[loinu__hnxv]
                    peqto__sabl = yxmqq__ulv.dtype
                    fxi__ams = types.literal(df.columns[loinu__hnxv])
                    spke__xwhoa = bodo.SeriesType(peqto__sabl, yxmqq__ulv,
                        bie__aduvl, fxi__ams)
                    return spke__xwhoa(*args)
                if isinstance(xfggh__ate, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                elif is_overload_constant_list(xfggh__ate):
                    vkek__sadzb = get_overload_const_list(xfggh__ate)
                    rzp__ijbm = types.unliteral(xfggh__ate)
                    if rzp__ijbm.dtype == types.bool_:
                        if len(df.columns) != len(vkek__sadzb):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {vkek__sadzb} has {len(vkek__sadzb)} values'
                                )
                        ach__kdahg = []
                        iaheh__hbvyn = []
                        for tcj__vrez in range(len(vkek__sadzb)):
                            if vkek__sadzb[tcj__vrez]:
                                ach__kdahg.append(df.columns[tcj__vrez])
                                iaheh__hbvyn.append(df.data[tcj__vrez])
                        dxa__znur = tuple()
                        spke__xwhoa = DataFrameType(tuple(iaheh__hbvyn),
                            bie__aduvl, tuple(ach__kdahg))
                        return spke__xwhoa(*args)
                    elif rzp__ijbm.dtype == bodo.string_type:
                        dxa__znur, iaheh__hbvyn = self.get_kept_cols_and_data(
                            df, vkek__sadzb)
                        spke__xwhoa = DataFrameType(iaheh__hbvyn,
                            bie__aduvl, dxa__znur)
                        return spke__xwhoa(*args)
        raise_bodo_error(
            f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet. If you are trying to select a subset of the columns by passing a list of column names, that list must be a compile time constant. See https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
            )

    def typecheck_df_getitem(self, args):
        df = args[0]
        ind = args[1]
        if is_overload_constant_str(ind) or is_overload_constant_int(ind):
            ind_val = get_overload_const_str(ind) if is_overload_constant_str(
                ind) else get_overload_const_int(ind)
            if isinstance(df.columns[0], tuple):
                ach__kdahg = []
                iaheh__hbvyn = []
                for tcj__vrez, vajkd__xahw in enumerate(df.columns):
                    if vajkd__xahw[0] != ind_val:
                        continue
                    ach__kdahg.append(vajkd__xahw[1] if len(vajkd__xahw) ==
                        2 else vajkd__xahw[1:])
                    iaheh__hbvyn.append(df.data[tcj__vrez])
                yxmqq__ulv = tuple(iaheh__hbvyn)
                aiz__iony = df.index
                efgs__tjb = tuple(ach__kdahg)
                spke__xwhoa = DataFrameType(yxmqq__ulv, aiz__iony, efgs__tjb)
                return spke__xwhoa(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                loinu__hnxv = df.columns.index(ind_val)
                yxmqq__ulv = df.data[loinu__hnxv]
                peqto__sabl = yxmqq__ulv.dtype
                aiz__iony = df.index
                fxi__ams = types.literal(df.columns[loinu__hnxv])
                spke__xwhoa = bodo.SeriesType(peqto__sabl, yxmqq__ulv,
                    aiz__iony, fxi__ams)
                return spke__xwhoa(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            yxmqq__ulv = df.data
            aiz__iony = self.replace_range_with_numeric_idx_if_needed(df, ind)
            efgs__tjb = df.columns
            spke__xwhoa = DataFrameType(yxmqq__ulv, aiz__iony, efgs__tjb,
                is_table_format=df.is_table_format)
            return spke__xwhoa(*args)
        elif is_overload_constant_list(ind):
            uctsp__ijc = get_overload_const_list(ind)
            efgs__tjb, yxmqq__ulv = self.get_kept_cols_and_data(df, uctsp__ijc)
            aiz__iony = df.index
            spke__xwhoa = DataFrameType(yxmqq__ulv, aiz__iony, efgs__tjb)
            return spke__xwhoa(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for vjs__zdn in cols_to_keep_list:
            if vjs__zdn not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(vjs__zdn, df.columns))
        efgs__tjb = tuple(cols_to_keep_list)
        yxmqq__ulv = tuple(df.data[df.columns.index(wfs__iic)] for wfs__iic in
            efgs__tjb)
        return efgs__tjb, yxmqq__ulv

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        bie__aduvl = bodo.hiframes.pd_index_ext.NumericIndexType(types.
            int64, df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return bie__aduvl


DataFrameGetItemTemplate._no_unliteral = True


@lower_builtin(operator.getitem, DataFrameType, types.Any)
def getitem_df_lower(context, builder, sig, args):
    impl = df_getitem_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_getitem_overload(df, ind):
    if not isinstance(df, DataFrameType):
        return
    if is_overload_constant_str(ind) or is_overload_constant_int(ind):
        ind_val = get_overload_const_str(ind) if is_overload_constant_str(ind
            ) else get_overload_const_int(ind)
        if isinstance(df.columns[0], tuple):
            ach__kdahg = []
            iaheh__hbvyn = []
            for tcj__vrez, vajkd__xahw in enumerate(df.columns):
                if vajkd__xahw[0] != ind_val:
                    continue
                ach__kdahg.append(vajkd__xahw[1] if len(vajkd__xahw) == 2 else
                    vajkd__xahw[1:])
                iaheh__hbvyn.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(tcj__vrez))
            duuhe__dwp = 'def impl(df, ind):\n'
            spxwl__cksq = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(duuhe__dwp,
                ach__kdahg, ', '.join(iaheh__hbvyn), spxwl__cksq)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        uctsp__ijc = get_overload_const_list(ind)
        for vjs__zdn in uctsp__ijc:
            if vjs__zdn not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(vjs__zdn, df.columns))
        iaheh__hbvyn = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}).copy()'
            .format(df.columns.index(vjs__zdn)) for vjs__zdn in uctsp__ijc)
        duuhe__dwp = 'def impl(df, ind):\n'
        spxwl__cksq = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(duuhe__dwp,
            uctsp__ijc, iaheh__hbvyn, spxwl__cksq)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        duuhe__dwp = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            duuhe__dwp += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        spxwl__cksq = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            iaheh__hbvyn = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            iaheh__hbvyn = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(vjs__zdn)})[ind]'
                 for vjs__zdn in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(duuhe__dwp, df.
            columns, iaheh__hbvyn, spxwl__cksq, out_df_type=df)
    raise_bodo_error('df[] getitem using {} not supported'.format(ind))


@overload(operator.setitem, no_unliteral=True)
def df_setitem_overload(df, idx, val):
    check_runtime_cols_unsupported(df, 'DataFrame setitem (df[])')
    if not isinstance(df, DataFrameType):
        return
    raise_bodo_error('DataFrame setitem: transform necessary')


class DataFrameILocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        wfs__iic = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(wfs__iic)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qcl__edbqi = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, qcl__edbqi)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        khzu__fimtm, = args
        dcg__vgkl = signature.return_type
        bunhg__vdk = cgutils.create_struct_proxy(dcg__vgkl)(context, builder)
        bunhg__vdk.obj = khzu__fimtm
        context.nrt.incref(builder, signature.args[0], khzu__fimtm)
        return bunhg__vdk._getvalue()
    return DataFrameILocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iloc')
def overload_dataframe_iloc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iloc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iloc(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iloc_getitem(I, idx):
    if not isinstance(I, DataFrameILocType):
        return
    df = I.df_type
    if isinstance(idx, types.Integer):
        return _gen_iloc_getitem_row_impl(df, df.columns, 'idx')
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and not isinstance(
        idx[1], types.SliceType):
        if not (is_overload_constant_list(idx.types[1]) or
            is_overload_constant_int(idx.types[1])):
            raise_bodo_error(
                'idx2 in df.iloc[idx1, idx2] should be a constant integer or constant list of integers. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                )
        dcyu__gggxi = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            wca__sqkm = get_overload_const_int(idx.types[1])
            if wca__sqkm < 0 or wca__sqkm >= dcyu__gggxi:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            mzg__owyc = [wca__sqkm]
        else:
            is_out_series = False
            mzg__owyc = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >=
                dcyu__gggxi for ind in mzg__owyc):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[mzg__owyc])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                wca__sqkm = mzg__owyc[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, wca__sqkm)[
                        idx[0]])
                return impl
            return _gen_iloc_getitem_row_impl(df, col_names, 'idx[0]')
        if is_list_like_index_type(idx.types[0]) and isinstance(idx.types[0
            ].dtype, (types.Integer, types.Boolean)) or isinstance(idx.
            types[0], types.SliceType):
            return _gen_iloc_getitem_bool_slice_impl(df, col_names, idx.
                types[0], 'idx[0]', is_out_series)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
        Integer, types.Boolean)) or isinstance(idx, types.SliceType):
        return _gen_iloc_getitem_bool_slice_impl(df, df.columns, idx, 'idx',
            False)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):
        raise_bodo_error(
            'slice2 in df.iloc[slice1,slice2] should be constant. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
            )
    raise_bodo_error(f'df.iloc[] getitem using {idx} not supported')


def _gen_iloc_getitem_bool_slice_impl(df, col_names, idx_typ, idx,
    is_out_series):
    duuhe__dwp = 'def impl(I, idx):\n'
    duuhe__dwp += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        duuhe__dwp += f'  idx_t = {idx}\n'
    else:
        duuhe__dwp += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    spxwl__cksq = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
    iaheh__hbvyn = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(vjs__zdn)})[idx_t]'
         for vjs__zdn in col_names)
    if is_out_series:
        ncug__owrfg = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        duuhe__dwp += f"""  return bodo.hiframes.pd_series_ext.init_series({iaheh__hbvyn}, {spxwl__cksq}, {ncug__owrfg})
"""
        ynqpo__gesvm = {}
        exec(duuhe__dwp, {'bodo': bodo}, ynqpo__gesvm)
        return ynqpo__gesvm['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(duuhe__dwp, col_names,
        iaheh__hbvyn, spxwl__cksq)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    duuhe__dwp = 'def impl(I, idx):\n'
    duuhe__dwp += '  df = I._obj\n'
    rhkg__cbibu = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(vjs__zdn)})[{idx}]'
         for vjs__zdn in col_names)
    duuhe__dwp += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    duuhe__dwp += f"""  return bodo.hiframes.pd_series_ext.init_series(({rhkg__cbibu},), row_idx, None)
"""
    ynqpo__gesvm = {}
    exec(duuhe__dwp, {'bodo': bodo}, ynqpo__gesvm)
    impl = ynqpo__gesvm['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def df_iloc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameILocType):
        return
    raise_bodo_error(
        f'DataFrame.iloc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameLocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        wfs__iic = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(wfs__iic)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qcl__edbqi = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, qcl__edbqi)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        khzu__fimtm, = args
        taef__oxwj = signature.return_type
        yej__ojq = cgutils.create_struct_proxy(taef__oxwj)(context, builder)
        yej__ojq.obj = khzu__fimtm
        context.nrt.incref(builder, signature.args[0], khzu__fimtm)
        return yej__ojq._getvalue()
    return DataFrameLocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'loc')
def overload_dataframe_loc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.loc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_loc(df)


@lower_builtin(operator.getitem, DataFrameLocType, types.Any)
def loc_getitem_lower(context, builder, sig, args):
    impl = overload_loc_getitem(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def overload_loc_getitem(I, idx):
    if not isinstance(I, DataFrameLocType):
        return
    df = I.df_type
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        duuhe__dwp = 'def impl(I, idx):\n'
        duuhe__dwp += '  df = I._obj\n'
        duuhe__dwp += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        spxwl__cksq = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        iaheh__hbvyn = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx_t]'
            .format(df.columns.index(vjs__zdn)) for vjs__zdn in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(duuhe__dwp, df.
            columns, iaheh__hbvyn, spxwl__cksq)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        mzby__kil = idx.types[1]
        if is_overload_constant_str(mzby__kil):
            wmskl__ict = get_overload_const_str(mzby__kil)
            wca__sqkm = df.columns.index(wmskl__ict)

            def impl_col_name(I, idx):
                df = I._obj
                spxwl__cksq = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_index(df))
                wywy__thb = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, wca__sqkm)
                return bodo.hiframes.pd_series_ext.init_series(wywy__thb,
                    spxwl__cksq, wmskl__ict).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(mzby__kil):
            col_idx_list = get_overload_const_list(mzby__kil)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(vjs__zdn in df.columns for
                vjs__zdn in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        col_idx_list = list(pd.Series(df.columns, dtype=object)[col_idx_list])
    iaheh__hbvyn = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx[0]]'
        .format(df.columns.index(vjs__zdn)) for vjs__zdn in col_idx_list)
    spxwl__cksq = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    duuhe__dwp = 'def impl(I, idx):\n'
    duuhe__dwp += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(duuhe__dwp,
        col_idx_list, iaheh__hbvyn, spxwl__cksq)


@overload(operator.setitem, no_unliteral=True)
def df_loc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameLocType):
        return
    raise_bodo_error(
        f'DataFrame.loc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameIatType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        wfs__iic = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(wfs__iic)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qcl__edbqi = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, qcl__edbqi)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        khzu__fimtm, = args
        ijonk__dfv = signature.return_type
        wlr__prgfu = cgutils.create_struct_proxy(ijonk__dfv)(context, builder)
        wlr__prgfu.obj = khzu__fimtm
        context.nrt.incref(builder, signature.args[0], khzu__fimtm)
        return wlr__prgfu._getvalue()
    return DataFrameIatType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iat')
def overload_dataframe_iat(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iat')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iat(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iat_getitem(I, idx):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat getitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                )
        wca__sqkm = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            wywy__thb = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                wca__sqkm)
            return wywy__thb[idx[0]]
        return impl_col_ind
    raise BodoError('df.iat[] getitem using {} not supported'.format(idx))


@overload(operator.setitem, no_unliteral=True)
def overload_iat_setitem(I, idx, val):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat setitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
                )
        wca__sqkm = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[wca__sqkm]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            wywy__thb = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                wca__sqkm)
            wywy__thb[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    wlr__prgfu = cgutils.create_struct_proxy(fromty)(context, builder, val)
    pvuxo__zztoo = context.cast(builder, wlr__prgfu.obj, fromty.df_type,
        toty.df_type)
    rjior__ksirv = cgutils.create_struct_proxy(toty)(context, builder)
    rjior__ksirv.obj = pvuxo__zztoo
    return rjior__ksirv._getvalue()
