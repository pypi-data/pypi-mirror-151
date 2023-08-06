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
            ipg__slgfi = 'Series'
        else:
            ipg__slgfi = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{ipg__slgfi}.rolling()')
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
        uvha__vywui = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, uvha__vywui)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    cgkr__iwh = dict(win_type=win_type, axis=axis, closed=closed)
    nmbhz__jcboh = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', cgkr__iwh, nmbhz__jcboh,
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
    cgkr__iwh = dict(win_type=win_type, axis=axis, closed=closed)
    nmbhz__jcboh = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', cgkr__iwh, nmbhz__jcboh,
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
        ldld__tzmwh, uwi__cxpus, lutfs__udz, zsjk__zluam, pqz__ipju = args
        uuoi__ibm = signature.return_type
        dpasf__xdk = cgutils.create_struct_proxy(uuoi__ibm)(context, builder)
        dpasf__xdk.obj = ldld__tzmwh
        dpasf__xdk.window = uwi__cxpus
        dpasf__xdk.min_periods = lutfs__udz
        dpasf__xdk.center = zsjk__zluam
        context.nrt.incref(builder, signature.args[0], ldld__tzmwh)
        context.nrt.incref(builder, signature.args[1], uwi__cxpus)
        context.nrt.incref(builder, signature.args[2], lutfs__udz)
        context.nrt.incref(builder, signature.args[3], zsjk__zluam)
        return dpasf__xdk._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    uuoi__ibm = RollingType(obj_type, window_type, on, selection, False)
    return uuoi__ibm(obj_type, window_type, min_periods_type, center_type,
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
    etuur__fbln = not isinstance(rolling.window_type, types.Integer)
    pllv__vmret = 'variable' if etuur__fbln else 'fixed'
    hjpyn__oqs = 'None'
    if etuur__fbln:
        hjpyn__oqs = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    xyo__oukxb = []
    eun__nkw = 'on_arr, ' if etuur__fbln else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{pllv__vmret}(bodo.hiframes.pd_series_ext.get_series_data(df), {eun__nkw}index_arr, window, minp, center, func, raw)'
            , hjpyn__oqs, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    tlj__abc = rolling.obj_type.data
    out_cols = []
    for aodyt__wbr in rolling.selection:
        bcxm__foeh = rolling.obj_type.columns.index(aodyt__wbr)
        if aodyt__wbr == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            fmoin__dmnk = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {bcxm__foeh})'
                )
            out_cols.append(aodyt__wbr)
        else:
            if not isinstance(tlj__abc[bcxm__foeh].dtype, (types.Boolean,
                types.Number)):
                continue
            fmoin__dmnk = (
                f'bodo.hiframes.rolling.rolling_{pllv__vmret}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {bcxm__foeh}), {eun__nkw}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(aodyt__wbr)
        xyo__oukxb.append(fmoin__dmnk)
    return ', '.join(xyo__oukxb), hjpyn__oqs, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    cgkr__iwh = dict(engine=engine, engine_kwargs=engine_kwargs, args=args,
        kwargs=kwargs)
    nmbhz__jcboh = dict(engine=None, engine_kwargs=None, args=None, kwargs=None
        )
    check_unsupported_args('Rolling.apply', cgkr__iwh, nmbhz__jcboh,
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
    cgkr__iwh = dict(win_type=win_type, axis=axis, closed=closed, method=method
        )
    nmbhz__jcboh = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', cgkr__iwh, nmbhz__jcboh,
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
        tukxw__jhlx = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        kumeh__std = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{mssph__ruu}'" if
                isinstance(mssph__ruu, str) else f'{mssph__ruu}' for
                mssph__ruu in rolling.selection if mssph__ruu != rolling.on))
        dsqr__vzzrz = nczhn__afewf = ''
        if fname == 'apply':
            dsqr__vzzrz = 'func, raw, args, kwargs'
            nczhn__afewf = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            dsqr__vzzrz = nczhn__afewf = 'other, pairwise'
        if fname == 'cov':
            dsqr__vzzrz = nczhn__afewf = 'other, pairwise, ddof'
        ypoo__bfj = (
            f'lambda df, window, minp, center, {dsqr__vzzrz}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {kumeh__std}){selection}.{fname}({nczhn__afewf})'
            )
        tukxw__jhlx += f"""  return rolling.obj.apply({ypoo__bfj}, rolling.window, rolling.min_periods, rolling.center, {dsqr__vzzrz})
"""
        htlfw__xzu = {}
        exec(tukxw__jhlx, {'bodo': bodo}, htlfw__xzu)
        impl = htlfw__xzu['impl']
        return impl
    hgitx__mwwz = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if hgitx__mwwz else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if hgitx__mwwz else rolling.obj_type.columns
        other_cols = None if hgitx__mwwz else other.columns
        xyo__oukxb, hjpyn__oqs = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        xyo__oukxb, hjpyn__oqs, out_cols = _gen_df_rolling_out_data(rolling)
    ios__wqggk = hgitx__mwwz or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    yxc__jgu = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    yxc__jgu += '  df = rolling.obj\n'
    yxc__jgu += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if hgitx__mwwz else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    ipg__slgfi = 'None'
    if hgitx__mwwz:
        ipg__slgfi = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif ios__wqggk:
        aodyt__wbr = (set(out_cols) - set([rolling.on])).pop()
        ipg__slgfi = f"'{aodyt__wbr}'" if isinstance(aodyt__wbr, str) else str(
            aodyt__wbr)
    yxc__jgu += f'  name = {ipg__slgfi}\n'
    yxc__jgu += '  window = rolling.window\n'
    yxc__jgu += '  center = rolling.center\n'
    yxc__jgu += '  minp = rolling.min_periods\n'
    yxc__jgu += f'  on_arr = {hjpyn__oqs}\n'
    if fname == 'apply':
        yxc__jgu += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        yxc__jgu += f"  func = '{fname}'\n"
        yxc__jgu += f'  index_arr = None\n'
        yxc__jgu += f'  raw = False\n'
    if ios__wqggk:
        yxc__jgu += (
            f'  return bodo.hiframes.pd_series_ext.init_series({xyo__oukxb}, index, name)'
            )
        htlfw__xzu = {}
        lnn__brxcl = {'bodo': bodo}
        exec(yxc__jgu, lnn__brxcl, htlfw__xzu)
        impl = htlfw__xzu['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(yxc__jgu, out_cols,
        xyo__oukxb)


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
        qyio__guau = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(qyio__guau)


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
    kxlyz__xohu = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(kxlyz__xohu) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    etuur__fbln = not isinstance(window_type, types.Integer)
    hjpyn__oqs = 'None'
    if etuur__fbln:
        hjpyn__oqs = 'bodo.utils.conversion.index_to_array(index)'
    eun__nkw = 'on_arr, ' if etuur__fbln else ''
    xyo__oukxb = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {eun__nkw}window, minp, center)'
            , hjpyn__oqs)
    for aodyt__wbr in out_cols:
        if aodyt__wbr in df_cols and aodyt__wbr in other_cols:
            opi__qclx = df_cols.index(aodyt__wbr)
            xclkb__xgof = other_cols.index(aodyt__wbr)
            fmoin__dmnk = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {opi__qclx}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {xclkb__xgof}), {eun__nkw}window, minp, center)'
                )
        else:
            fmoin__dmnk = 'np.full(len(df), np.nan)'
        xyo__oukxb.append(fmoin__dmnk)
    return ', '.join(xyo__oukxb), hjpyn__oqs


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    iqfe__unhbd = {'pairwise': pairwise, 'ddof': ddof}
    mjmk__ubtk = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        iqfe__unhbd, mjmk__ubtk, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    iqfe__unhbd = {'ddof': ddof, 'pairwise': pairwise}
    mjmk__ubtk = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        iqfe__unhbd, mjmk__ubtk, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, shmec__wlhro = args
        if isinstance(rolling, RollingType):
            kxlyz__xohu = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(shmec__wlhro, (tuple, list)):
                if len(set(shmec__wlhro).difference(set(kxlyz__xohu))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(shmec__wlhro).difference(set(kxlyz__xohu)))
                        )
                selection = list(shmec__wlhro)
            else:
                if shmec__wlhro not in kxlyz__xohu:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(shmec__wlhro))
                selection = [shmec__wlhro]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            qlbyj__mrixq = RollingType(rolling.obj_type, rolling.
                window_type, rolling.on, tuple(selection), True, series_select)
            return signature(qlbyj__mrixq, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        kxlyz__xohu = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            kxlyz__xohu = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            kxlyz__xohu = rolling.obj_type.columns
        if attr in kxlyz__xohu:
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
    uxza__avamx = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    tlj__abc = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in uxza__avamx):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        xea__djroo = tlj__abc[uxza__avamx.index(get_literal_value(on))]
        if not isinstance(xea__djroo, types.Array
            ) or xea__djroo.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(ywso__xpcr.dtype, (types.Boolean, types.Number)) for
        ywso__xpcr in tlj__abc):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
