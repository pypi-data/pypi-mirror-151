"""typing for rolling window functions
"""
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model
import bodo
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.hiframes.pd_groupby_ext import DataFrameGroupByType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.rolling import supported_rolling_funcs, unsupported_rolling_methods
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, get_literal_value, is_const_func_type, is_literal_type, is_overload_bool, is_overload_constant_str, is_overload_int, is_overload_none, raise_bodo_error


class RollingType(types.Type):

    def __init__(self, obj_type, window_type, on, selection,
        explicit_select=False, series_select=False):
        if isinstance(obj_type, bodo.SeriesType):
            wbs__mkat = 'Series'
        else:
            wbs__mkat = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{wbs__mkat}.rolling()')
        self.obj_type = obj_type
        self.window_type = window_type
        self.on = on
        self.selection = selection
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(RollingType, self).__init__(name=
            f'RollingType({obj_type}, {window_type}, {on}, {selection}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return RollingType(self.obj_type, self.window_type, self.on, self.
            selection, self.explicit_select, self.series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(RollingType)
class RollingModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        aip__qrfac = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, aip__qrfac)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    htczu__iqq = dict(win_type=win_type, axis=axis, closed=closed)
    tdkpr__apuw = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', htczu__iqq, tdkpr__apuw,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(df, window, min_periods, center, on)

    def impl(df, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(df, window,
            min_periods, center, on)
    return impl


@overload_method(SeriesType, 'rolling', inline='always', no_unliteral=True)
def overload_series_rolling(S, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    htczu__iqq = dict(win_type=win_type, axis=axis, closed=closed)
    tdkpr__apuw = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', htczu__iqq, tdkpr__apuw,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(S, window, min_periods, center, on)

    def impl(S, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(S, window,
            min_periods, center, on)
    return impl


@intrinsic
def init_rolling(typingctx, obj_type, window_type, min_periods_type,
    center_type, on_type=None):

    def codegen(context, builder, signature, args):
        vkly__dwl, fwyvm__zxg, sjnz__giu, drvg__lgz, pbbr__kpiox = args
        oqpz__xde = signature.return_type
        uas__lfrvl = cgutils.create_struct_proxy(oqpz__xde)(context, builder)
        uas__lfrvl.obj = vkly__dwl
        uas__lfrvl.window = fwyvm__zxg
        uas__lfrvl.min_periods = sjnz__giu
        uas__lfrvl.center = drvg__lgz
        context.nrt.incref(builder, signature.args[0], vkly__dwl)
        context.nrt.incref(builder, signature.args[1], fwyvm__zxg)
        context.nrt.incref(builder, signature.args[2], sjnz__giu)
        context.nrt.incref(builder, signature.args[3], drvg__lgz)
        return uas__lfrvl._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    oqpz__xde = RollingType(obj_type, window_type, on, selection, False)
    return oqpz__xde(obj_type, window_type, min_periods_type, center_type,
        on_type), codegen


def _handle_default_min_periods(min_periods, window):
    return min_periods


@overload(_handle_default_min_periods)
def overload_handle_default_min_periods(min_periods, window):
    if is_overload_none(min_periods):
        if isinstance(window, types.Integer):
            return lambda min_periods, window: window
        else:
            return lambda min_periods, window: 1
    else:
        return lambda min_periods, window: min_periods


def _gen_df_rolling_out_data(rolling):
    nonht__nix = not isinstance(rolling.window_type, types.Integer)
    gxgk__tqdz = 'variable' if nonht__nix else 'fixed'
    dwlc__eyj = 'None'
    if nonht__nix:
        dwlc__eyj = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    kmtu__nvjn = []
    oxd__dsi = 'on_arr, ' if nonht__nix else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{gxgk__tqdz}(bodo.hiframes.pd_series_ext.get_series_data(df), {oxd__dsi}index_arr, window, minp, center, func, raw)'
            , dwlc__eyj, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    ralv__cop = rolling.obj_type.data
    out_cols = []
    for olsx__wiw in rolling.selection:
        qdhhu__hfpl = rolling.obj_type.columns.index(olsx__wiw)
        if olsx__wiw == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            zwnjo__spxj = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {qdhhu__hfpl})'
                )
            out_cols.append(olsx__wiw)
        else:
            if not isinstance(ralv__cop[qdhhu__hfpl].dtype, (types.Boolean,
                types.Number)):
                continue
            zwnjo__spxj = (
                f'bodo.hiframes.rolling.rolling_{gxgk__tqdz}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {qdhhu__hfpl}), {oxd__dsi}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(olsx__wiw)
        kmtu__nvjn.append(zwnjo__spxj)
    return ', '.join(kmtu__nvjn), dwlc__eyj, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    htczu__iqq = dict(engine=engine, engine_kwargs=engine_kwargs, args=args,
        kwargs=kwargs)
    tdkpr__apuw = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', htczu__iqq, tdkpr__apuw,
        package_name='pandas', module_name='Window')
    if not is_const_func_type(func):
        raise BodoError(
            f"Rolling.apply(): 'func' parameter must be a function, not {func} (builtin functions not supported yet)."
            )
    if not is_overload_bool(raw):
        raise BodoError(
            f"Rolling.apply(): 'raw' parameter must be bool, not {raw}.")
    return _gen_rolling_impl(rolling, 'apply')


@overload_method(DataFrameGroupByType, 'rolling', inline='always',
    no_unliteral=True)
def groupby_rolling_overload(grp, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None, method='single'):
    htczu__iqq = dict(win_type=win_type, axis=axis, closed=closed, method=
        method)
    tdkpr__apuw = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', htczu__iqq, tdkpr__apuw,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(grp, window, min_periods, center, on)

    def _impl(grp, window, min_periods=None, center=False, win_type=None,
        on=None, axis=0, closed=None, method='single'):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(grp, window,
            min_periods, center, on)
    return _impl


def _gen_rolling_impl(rolling, fname, other=None):
    if isinstance(rolling.obj_type, DataFrameGroupByType):
        dxu__std = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        uim__qfpj = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{jcv__cluwd}'" if
                isinstance(jcv__cluwd, str) else f'{jcv__cluwd}' for
                jcv__cluwd in rolling.selection if jcv__cluwd != rolling.on))
        pneas__csddo = tyg__cgp = ''
        if fname == 'apply':
            pneas__csddo = 'func, raw, args, kwargs'
            tyg__cgp = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            pneas__csddo = tyg__cgp = 'other, pairwise'
        if fname == 'cov':
            pneas__csddo = tyg__cgp = 'other, pairwise, ddof'
        gund__hnp = (
            f'lambda df, window, minp, center, {pneas__csddo}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {uim__qfpj}){selection}.{fname}({tyg__cgp})'
            )
        dxu__std += f"""  return rolling.obj.apply({gund__hnp}, rolling.window, rolling.min_periods, rolling.center, {pneas__csddo})
"""
        zthb__syrzx = {}
        exec(dxu__std, {'bodo': bodo}, zthb__syrzx)
        impl = zthb__syrzx['impl']
        return impl
    tvdvs__ozgb = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if tvdvs__ozgb else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if tvdvs__ozgb else rolling.obj_type.columns
        other_cols = None if tvdvs__ozgb else other.columns
        kmtu__nvjn, dwlc__eyj = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        kmtu__nvjn, dwlc__eyj, out_cols = _gen_df_rolling_out_data(rolling)
    svpaf__kfk = tvdvs__ozgb or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    bhgy__eex = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    bhgy__eex += '  df = rolling.obj\n'
    bhgy__eex += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if tvdvs__ozgb else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    wbs__mkat = 'None'
    if tvdvs__ozgb:
        wbs__mkat = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif svpaf__kfk:
        olsx__wiw = (set(out_cols) - set([rolling.on])).pop()
        wbs__mkat = f"'{olsx__wiw}'" if isinstance(olsx__wiw, str) else str(
            olsx__wiw)
    bhgy__eex += f'  name = {wbs__mkat}\n'
    bhgy__eex += '  window = rolling.window\n'
    bhgy__eex += '  center = rolling.center\n'
    bhgy__eex += '  minp = rolling.min_periods\n'
    bhgy__eex += f'  on_arr = {dwlc__eyj}\n'
    if fname == 'apply':
        bhgy__eex += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        bhgy__eex += f"  func = '{fname}'\n"
        bhgy__eex += f'  index_arr = None\n'
        bhgy__eex += f'  raw = False\n'
    if svpaf__kfk:
        bhgy__eex += (
            f'  return bodo.hiframes.pd_series_ext.init_series({kmtu__nvjn}, index, name)'
            )
        zthb__syrzx = {}
        duvb__wklro = {'bodo': bodo}
        exec(bhgy__eex, duvb__wklro, zthb__syrzx)
        impl = zthb__syrzx['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(bhgy__eex, out_cols,
        kmtu__nvjn)


def _get_rolling_func_args(fname):
    if fname == 'apply':
        return (
            'func, raw=False, engine=None, engine_kwargs=None, args=None, kwargs=None\n'
            )
    elif fname == 'corr':
        return 'other=None, pairwise=None, ddof=1\n'
    elif fname == 'cov':
        return 'other=None, pairwise=None, ddof=1\n'
    return ''


def create_rolling_overload(fname):

    def overload_rolling_func(rolling):
        return _gen_rolling_impl(rolling, fname)
    return overload_rolling_func


def _install_rolling_methods():
    for fname in supported_rolling_funcs:
        if fname in ('apply', 'corr', 'cov'):
            continue
        dzml__ugbdo = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(dzml__ugbdo)


def _install_rolling_unsupported_methods():
    for fname in unsupported_rolling_methods:
        overload_method(RollingType, fname, no_unliteral=True)(
            create_unsupported_overload(
            f'pandas.core.window.rolling.Rolling.{fname}()'))


_install_rolling_methods()
_install_rolling_unsupported_methods()


def _get_corr_cov_out_cols(rolling, other, func_name):
    if not isinstance(other, DataFrameType):
        raise_bodo_error(
            f"DataFrame.rolling.{func_name}(): requires providing a DataFrame for 'other'"
            )
    ezb__aqm = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(ezb__aqm) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    nonht__nix = not isinstance(window_type, types.Integer)
    dwlc__eyj = 'None'
    if nonht__nix:
        dwlc__eyj = 'bodo.utils.conversion.index_to_array(index)'
    oxd__dsi = 'on_arr, ' if nonht__nix else ''
    kmtu__nvjn = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {oxd__dsi}window, minp, center)'
            , dwlc__eyj)
    for olsx__wiw in out_cols:
        if olsx__wiw in df_cols and olsx__wiw in other_cols:
            ihwu__faqy = df_cols.index(olsx__wiw)
            kqh__now = other_cols.index(olsx__wiw)
            zwnjo__spxj = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ihwu__faqy}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {kqh__now}), {oxd__dsi}window, minp, center)'
                )
        else:
            zwnjo__spxj = 'np.full(len(df), np.nan)'
        kmtu__nvjn.append(zwnjo__spxj)
    return ', '.join(kmtu__nvjn), dwlc__eyj


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    egk__ykyx = {'pairwise': pairwise, 'ddof': ddof}
    maepd__efcp = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        egk__ykyx, maepd__efcp, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    egk__ykyx = {'ddof': ddof, 'pairwise': pairwise}
    maepd__efcp = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        egk__ykyx, maepd__efcp, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, lmwc__gbjk = args
        if isinstance(rolling, RollingType):
            ezb__aqm = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(lmwc__gbjk, (tuple, list)):
                if len(set(lmwc__gbjk).difference(set(ezb__aqm))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(lmwc__gbjk).difference(set(ezb__aqm))))
                selection = list(lmwc__gbjk)
            else:
                if lmwc__gbjk not in ezb__aqm:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(lmwc__gbjk))
                selection = [lmwc__gbjk]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            vfngr__ucgjg = RollingType(rolling.obj_type, rolling.
                window_type, rolling.on, tuple(selection), True, series_select)
            return signature(vfngr__ucgjg, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        ezb__aqm = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            ezb__aqm = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            ezb__aqm = rolling.obj_type.columns
        if attr in ezb__aqm:
            return RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, (attr,) if rolling.on is None else (attr,
                rolling.on), True, True)


def _validate_rolling_args(obj, window, min_periods, center, on):
    assert isinstance(obj, (SeriesType, DataFrameType, DataFrameGroupByType)
        ), 'invalid rolling obj'
    func_name = 'Series' if isinstance(obj, SeriesType
        ) else 'DataFrame' if isinstance(obj, DataFrameType
        ) else 'DataFrameGroupBy'
    if not (is_overload_int(window) or is_overload_constant_str(window) or 
        window == bodo.string_type or window in (pd_timedelta_type,
        datetime_timedelta_type)):
        raise BodoError(
            f"{func_name}.rolling(): 'window' should be int or time offset (str, pd.Timedelta, datetime.timedelta), not {window}"
            )
    if not is_overload_bool(center):
        raise BodoError(
            f'{func_name}.rolling(): center must be a boolean, not {center}')
    if not (is_overload_none(min_periods) or isinstance(min_periods, types.
        Integer)):
        raise BodoError(
            f'{func_name}.rolling(): min_periods must be an integer, not {min_periods}'
            )
    if isinstance(obj, SeriesType) and not is_overload_none(on):
        raise BodoError(
            f"{func_name}.rolling(): 'on' not supported for Series yet (can use a DataFrame instead)."
            )
    fmj__ifp = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    ralv__cop = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in fmj__ifp):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        pfamd__hpyvr = ralv__cop[fmj__ifp.index(get_literal_value(on))]
        if not isinstance(pfamd__hpyvr, types.Array
            ) or pfamd__hpyvr.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(kdi__vvi.dtype, (types.Boolean, types.Number)) for
        kdi__vvi in ralv__cop):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
