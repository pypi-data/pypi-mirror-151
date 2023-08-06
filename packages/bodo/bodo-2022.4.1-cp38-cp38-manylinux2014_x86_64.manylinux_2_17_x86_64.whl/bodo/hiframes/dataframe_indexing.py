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
            qjhfd__mmt = idx
            oxmh__pgqq = df.data
            ixhg__glpai = df.columns
            nkot__sxa = self.replace_range_with_numeric_idx_if_needed(df,
                qjhfd__mmt)
            xth__lepmu = DataFrameType(oxmh__pgqq, nkot__sxa, ixhg__glpai)
            return xth__lepmu(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            osics__mkg = idx.types[0]
            iggbc__rkqyl = idx.types[1]
            if isinstance(osics__mkg, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(iggbc__rkqyl):
                    ozd__bwwk = get_overload_const_str(iggbc__rkqyl)
                    if ozd__bwwk not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, ozd__bwwk))
                    qoquw__qhbsx = df.columns.index(ozd__bwwk)
                    return df.data[qoquw__qhbsx].dtype(*args)
                if isinstance(iggbc__rkqyl, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(osics__mkg
                ) and osics__mkg.dtype == types.bool_ or isinstance(osics__mkg,
                types.SliceType):
                nkot__sxa = self.replace_range_with_numeric_idx_if_needed(df,
                    osics__mkg)
                if is_overload_constant_str(iggbc__rkqyl):
                    dqyt__fpyd = get_overload_const_str(iggbc__rkqyl)
                    if dqyt__fpyd not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {dqyt__fpyd}'
                            )
                    qoquw__qhbsx = df.columns.index(dqyt__fpyd)
                    zvy__asbvb = df.data[qoquw__qhbsx]
                    dbrp__aaxri = zvy__asbvb.dtype
                    dbb__iyn = types.literal(df.columns[qoquw__qhbsx])
                    xth__lepmu = bodo.SeriesType(dbrp__aaxri, zvy__asbvb,
                        nkot__sxa, dbb__iyn)
                    return xth__lepmu(*args)
                if isinstance(iggbc__rkqyl, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html.'
                        )
                elif is_overload_constant_list(iggbc__rkqyl):
                    obqnc__nlran = get_overload_const_list(iggbc__rkqyl)
                    bvg__trec = types.unliteral(iggbc__rkqyl)
                    if bvg__trec.dtype == types.bool_:
                        if len(df.columns) != len(obqnc__nlran):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {obqnc__nlran} has {len(obqnc__nlran)} values'
                                )
                        lhxn__zgav = []
                        ukd__ept = []
                        for nrk__smap in range(len(obqnc__nlran)):
                            if obqnc__nlran[nrk__smap]:
                                lhxn__zgav.append(df.columns[nrk__smap])
                                ukd__ept.append(df.data[nrk__smap])
                        mua__zrwos = tuple()
                        xth__lepmu = DataFrameType(tuple(ukd__ept),
                            nkot__sxa, tuple(lhxn__zgav))
                        return xth__lepmu(*args)
                    elif bvg__trec.dtype == bodo.string_type:
                        mua__zrwos, ukd__ept = self.get_kept_cols_and_data(df,
                            obqnc__nlran)
                        xth__lepmu = DataFrameType(ukd__ept, nkot__sxa,
                            mua__zrwos)
                        return xth__lepmu(*args)
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
                lhxn__zgav = []
                ukd__ept = []
                for nrk__smap, rmorn__vnbnq in enumerate(df.columns):
                    if rmorn__vnbnq[0] != ind_val:
                        continue
                    lhxn__zgav.append(rmorn__vnbnq[1] if len(rmorn__vnbnq) ==
                        2 else rmorn__vnbnq[1:])
                    ukd__ept.append(df.data[nrk__smap])
                zvy__asbvb = tuple(ukd__ept)
                pdc__cuyxy = df.index
                jyuyv__pzd = tuple(lhxn__zgav)
                xth__lepmu = DataFrameType(zvy__asbvb, pdc__cuyxy, jyuyv__pzd)
                return xth__lepmu(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                qoquw__qhbsx = df.columns.index(ind_val)
                zvy__asbvb = df.data[qoquw__qhbsx]
                dbrp__aaxri = zvy__asbvb.dtype
                pdc__cuyxy = df.index
                dbb__iyn = types.literal(df.columns[qoquw__qhbsx])
                xth__lepmu = bodo.SeriesType(dbrp__aaxri, zvy__asbvb,
                    pdc__cuyxy, dbb__iyn)
                return xth__lepmu(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            zvy__asbvb = df.data
            pdc__cuyxy = self.replace_range_with_numeric_idx_if_needed(df, ind)
            jyuyv__pzd = df.columns
            xth__lepmu = DataFrameType(zvy__asbvb, pdc__cuyxy, jyuyv__pzd,
                is_table_format=df.is_table_format)
            return xth__lepmu(*args)
        elif is_overload_constant_list(ind):
            cjzf__tllzi = get_overload_const_list(ind)
            jyuyv__pzd, zvy__asbvb = self.get_kept_cols_and_data(df,
                cjzf__tllzi)
            pdc__cuyxy = df.index
            xth__lepmu = DataFrameType(zvy__asbvb, pdc__cuyxy, jyuyv__pzd)
            return xth__lepmu(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/source/programming_with_bodo/require_constants.html'
            )

    def get_kept_cols_and_data(self, df, cols_to_keep_list):
        for rgr__yptun in cols_to_keep_list:
            if rgr__yptun not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(rgr__yptun, df.columns))
        jyuyv__pzd = tuple(cols_to_keep_list)
        zvy__asbvb = tuple(df.data[df.columns.index(tjjvl__fksui)] for
            tjjvl__fksui in jyuyv__pzd)
        return jyuyv__pzd, zvy__asbvb

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        nkot__sxa = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64,
            df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return nkot__sxa


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
            lhxn__zgav = []
            ukd__ept = []
            for nrk__smap, rmorn__vnbnq in enumerate(df.columns):
                if rmorn__vnbnq[0] != ind_val:
                    continue
                lhxn__zgav.append(rmorn__vnbnq[1] if len(rmorn__vnbnq) == 2
                     else rmorn__vnbnq[1:])
                ukd__ept.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(nrk__smap))
            ithm__ptvdq = 'def impl(df, ind):\n'
            hbk__zcqbe = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(ithm__ptvdq,
                lhxn__zgav, ', '.join(ukd__ept), hbk__zcqbe)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        cjzf__tllzi = get_overload_const_list(ind)
        for rgr__yptun in cjzf__tllzi:
            if rgr__yptun not in df.columns:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(rgr__yptun, df.columns))
        ukd__ept = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}).copy()'
            .format(df.columns.index(rgr__yptun)) for rgr__yptun in cjzf__tllzi
            )
        ithm__ptvdq = 'def impl(df, ind):\n'
        hbk__zcqbe = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(ithm__ptvdq,
            cjzf__tllzi, ukd__ept, hbk__zcqbe)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        ithm__ptvdq = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            ithm__ptvdq += (
                '  ind = bodo.utils.conversion.coerce_to_ndarray(ind)\n')
        hbk__zcqbe = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            ukd__ept = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            ukd__ept = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(rgr__yptun)})[ind]'
                 for rgr__yptun in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(ithm__ptvdq, df.
            columns, ukd__ept, hbk__zcqbe, out_df_type=df)
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
        tjjvl__fksui = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(tjjvl__fksui)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kef__asa = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, kef__asa)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        gpea__xirvl, = args
        rqde__eeyu = signature.return_type
        yarra__rbk = cgutils.create_struct_proxy(rqde__eeyu)(context, builder)
        yarra__rbk.obj = gpea__xirvl
        context.nrt.incref(builder, signature.args[0], gpea__xirvl)
        return yarra__rbk._getvalue()
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
        jmbdy__ftrk = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            wvefh__igy = get_overload_const_int(idx.types[1])
            if wvefh__igy < 0 or wvefh__igy >= jmbdy__ftrk:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            esnbk__umrh = [wvefh__igy]
        else:
            is_out_series = False
            esnbk__umrh = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >=
                jmbdy__ftrk for ind in esnbk__umrh):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[esnbk__umrh])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                wvefh__igy = esnbk__umrh[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, wvefh__igy)
                        [idx[0]])
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
    ithm__ptvdq = 'def impl(I, idx):\n'
    ithm__ptvdq += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        ithm__ptvdq += f'  idx_t = {idx}\n'
    else:
        ithm__ptvdq += (
            f'  idx_t = bodo.utils.conversion.coerce_to_ndarray({idx})\n')
    hbk__zcqbe = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
    ukd__ept = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(rgr__yptun)})[idx_t]'
         for rgr__yptun in col_names)
    if is_out_series:
        pchyc__jpju = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        ithm__ptvdq += f"""  return bodo.hiframes.pd_series_ext.init_series({ukd__ept}, {hbk__zcqbe}, {pchyc__jpju})
"""
        klcax__xixua = {}
        exec(ithm__ptvdq, {'bodo': bodo}, klcax__xixua)
        return klcax__xixua['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(ithm__ptvdq, col_names,
        ukd__ept, hbk__zcqbe)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    ithm__ptvdq = 'def impl(I, idx):\n'
    ithm__ptvdq += '  df = I._obj\n'
    jtc__ebj = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.columns.index(rgr__yptun)})[{idx}]'
         for rgr__yptun in col_names)
    ithm__ptvdq += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    ithm__ptvdq += f"""  return bodo.hiframes.pd_series_ext.init_series(({jtc__ebj},), row_idx, None)
"""
    klcax__xixua = {}
    exec(ithm__ptvdq, {'bodo': bodo}, klcax__xixua)
    impl = klcax__xixua['impl']
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
        tjjvl__fksui = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(tjjvl__fksui)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kef__asa = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, kef__asa)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        gpea__xirvl, = args
        vnt__ogq = signature.return_type
        mse__eaf = cgutils.create_struct_proxy(vnt__ogq)(context, builder)
        mse__eaf.obj = gpea__xirvl
        context.nrt.incref(builder, signature.args[0], gpea__xirvl)
        return mse__eaf._getvalue()
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
        ithm__ptvdq = 'def impl(I, idx):\n'
        ithm__ptvdq += '  df = I._obj\n'
        ithm__ptvdq += (
            '  idx_t = bodo.utils.conversion.coerce_to_ndarray(idx)\n')
        hbk__zcqbe = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        ukd__ept = ', '.join(
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx_t]'
            .format(df.columns.index(rgr__yptun)) for rgr__yptun in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(ithm__ptvdq, df.
            columns, ukd__ept, hbk__zcqbe)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        xfsb__quka = idx.types[1]
        if is_overload_constant_str(xfsb__quka):
            vdt__lifw = get_overload_const_str(xfsb__quka)
            wvefh__igy = df.columns.index(vdt__lifw)

            def impl_col_name(I, idx):
                df = I._obj
                hbk__zcqbe = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_index(df))
                fyvg__zbdl = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, wvefh__igy)
                return bodo.hiframes.pd_series_ext.init_series(fyvg__zbdl,
                    hbk__zcqbe, vdt__lifw).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(xfsb__quka):
            col_idx_list = get_overload_const_list(xfsb__quka)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(rgr__yptun in df.columns for
                rgr__yptun in col_idx_list):
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
    ukd__ept = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[idx[0]]'
        .format(df.columns.index(rgr__yptun)) for rgr__yptun in col_idx_list)
    hbk__zcqbe = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    ithm__ptvdq = 'def impl(I, idx):\n'
    ithm__ptvdq += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(ithm__ptvdq,
        col_idx_list, ukd__ept, hbk__zcqbe)


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
        tjjvl__fksui = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(tjjvl__fksui)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kef__asa = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, kef__asa)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        gpea__xirvl, = args
        pzyja__ymt = signature.return_type
        qjv__hok = cgutils.create_struct_proxy(pzyja__ymt)(context, builder)
        qjv__hok.obj = gpea__xirvl
        context.nrt.incref(builder, signature.args[0], gpea__xirvl)
        return qjv__hok._getvalue()
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
        wvefh__igy = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            fyvg__zbdl = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                wvefh__igy)
            return fyvg__zbdl[idx[0]]
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
        wvefh__igy = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[wvefh__igy]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            fyvg__zbdl = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                wvefh__igy)
            fyvg__zbdl[idx[0]] = bodo.utils.conversion.unbox_if_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    qjv__hok = cgutils.create_struct_proxy(fromty)(context, builder, val)
    mda__feuw = context.cast(builder, qjv__hok.obj, fromty.df_type, toty.
        df_type)
    vueki__njmq = cgutils.create_struct_proxy(toty)(context, builder)
    vueki__njmq.obj = mda__feuw
    return vueki__njmq._getvalue()
