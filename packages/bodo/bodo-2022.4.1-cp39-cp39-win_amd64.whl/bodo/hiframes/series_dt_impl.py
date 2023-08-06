"""
Support for Series.dt attributes and methods
"""
import datetime
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_series_ext import SeriesType, get_series_data, get_series_index, get_series_name, init_series
from bodo.libs.pd_datetime_arr_ext import PandasDatetimeTZDtype
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, raise_bodo_error
dt64_dtype = np.dtype('datetime64[ns]')
timedelta64_dtype = np.dtype('timedelta64[ns]')


class SeriesDatetimePropertiesType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        wgx__stb = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(wgx__stb)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        moi__pohq = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, moi__pohq)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        qji__cmz, = args
        zmmnz__til = signature.return_type
        zmun__rwlwo = cgutils.create_struct_proxy(zmmnz__til)(context, builder)
        zmun__rwlwo.obj = qji__cmz
        context.nrt.incref(builder, signature.args[0], qji__cmz)
        return zmun__rwlwo._getvalue()
    return SeriesDatetimePropertiesType(obj)(obj), codegen


@overload_attribute(SeriesType, 'dt')
def overload_series_dt(s):
    if not (bodo.hiframes.pd_series_ext.is_dt64_series_typ(s) or bodo.
        hiframes.pd_series_ext.is_timedelta64_series_typ(s)):
        raise_bodo_error('Can only use .dt accessor with datetimelike values.')
    return lambda s: bodo.hiframes.series_dt_impl.init_series_dt_properties(s)


def create_date_field_overload(field):

    def overload_field(S_dt):
        if S_dt.stype.dtype != types.NPDatetime('ns') and not isinstance(S_dt
            .stype.dtype, PandasDatetimeTZDtype):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{field}')
        dmgk__acaau = 'def impl(S_dt):\n'
        dmgk__acaau += '    S = S_dt._obj\n'
        dmgk__acaau += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        dmgk__acaau += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dmgk__acaau += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        dmgk__acaau += '    numba.parfors.parfor.init_prange()\n'
        dmgk__acaau += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            dmgk__acaau += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            dmgk__acaau += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        dmgk__acaau += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        dmgk__acaau += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        dmgk__acaau += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        dmgk__acaau += '            continue\n'
        dmgk__acaau += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            dmgk__acaau += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                dmgk__acaau += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            dmgk__acaau += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            jjb__vrgu = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            dmgk__acaau += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            dmgk__acaau += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            dmgk__acaau += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(jjb__vrgu[field]))
        elif field == 'is_leap_year':
            dmgk__acaau += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            dmgk__acaau += """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)
"""
        elif field in ('daysinmonth', 'days_in_month'):
            jjb__vrgu = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            dmgk__acaau += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            dmgk__acaau += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            dmgk__acaau += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(jjb__vrgu[field]))
        else:
            dmgk__acaau += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            dmgk__acaau += '        out_arr[i] = ts.' + field + '\n'
        dmgk__acaau += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        oyyt__pfe = {}
        exec(dmgk__acaau, {'bodo': bodo, 'numba': numba, 'np': np}, oyyt__pfe)
        impl = oyyt__pfe['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        xjia__upwn = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(xjia__upwn)


_install_date_fields()


def create_date_method_overload(method):
    rnqkp__xwejr = method in ['day_name', 'month_name']
    if rnqkp__xwejr:
        dmgk__acaau = 'def overload_method(S_dt, locale=None):\n'
        dmgk__acaau += '    unsupported_args = dict(locale=locale)\n'
        dmgk__acaau += '    arg_defaults = dict(locale=None)\n'
        dmgk__acaau += '    bodo.utils.typing.check_unsupported_args(\n'
        dmgk__acaau += f"        'Series.dt.{method}',\n"
        dmgk__acaau += '        unsupported_args,\n'
        dmgk__acaau += '        arg_defaults,\n'
        dmgk__acaau += "        package_name='pandas',\n"
        dmgk__acaau += "        module_name='Series',\n"
        dmgk__acaau += '    )\n'
    else:
        dmgk__acaau = 'def overload_method(S_dt):\n'
        dmgk__acaau += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    dmgk__acaau += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    dmgk__acaau += '        return\n'
    if rnqkp__xwejr:
        dmgk__acaau += '    def impl(S_dt, locale=None):\n'
    else:
        dmgk__acaau += '    def impl(S_dt):\n'
    dmgk__acaau += '        S = S_dt._obj\n'
    dmgk__acaau += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    dmgk__acaau += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    dmgk__acaau += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    dmgk__acaau += '        numba.parfors.parfor.init_prange()\n'
    dmgk__acaau += '        n = len(arr)\n'
    if rnqkp__xwejr:
        dmgk__acaau += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        dmgk__acaau += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    dmgk__acaau += (
        '        for i in numba.parfors.parfor.internal_prange(n):\n')
    dmgk__acaau += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    dmgk__acaau += (
        '                bodo.libs.array_kernels.setna(out_arr, i)\n')
    dmgk__acaau += '                continue\n'
    dmgk__acaau += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    dmgk__acaau += f'            method_val = ts.{method}()\n'
    if rnqkp__xwejr:
        dmgk__acaau += '            out_arr[i] = method_val\n'
    else:
        dmgk__acaau += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    dmgk__acaau += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    dmgk__acaau += '    return impl\n'
    oyyt__pfe = {}
    exec(dmgk__acaau, {'bodo': bodo, 'numba': numba, 'np': np}, oyyt__pfe)
    overload_method = oyyt__pfe['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        xjia__upwn = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            xjia__upwn)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        ndelt__hvh = S_dt._obj
        zlkr__tzs = bodo.hiframes.pd_series_ext.get_series_data(ndelt__hvh)
        zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(ndelt__hvh)
        wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(ndelt__hvh)
        numba.parfors.parfor.init_prange()
        tjns__npb = len(zlkr__tzs)
        wwzd__gukv = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            tjns__npb)
        for uxady__luo in numba.parfors.parfor.internal_prange(tjns__npb):
            bqhe__lbngo = zlkr__tzs[uxady__luo]
            nue__tipgk = bodo.utils.conversion.box_if_dt64(bqhe__lbngo)
            wwzd__gukv[uxady__luo] = datetime.date(nue__tipgk.year,
                nue__tipgk.month, nue__tipgk.day)
        return bodo.hiframes.pd_series_ext.init_series(wwzd__gukv, zfo__zzg,
            wgx__stb)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{attr}')
        if attr == 'components':
            unlqc__nyvkc = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            vff__spxhu = 'convert_numpy_timedelta64_to_pd_timedelta'
            icn__dnx = 'np.empty(n, np.int64)'
            rfri__oiggp = attr
        elif attr == 'isocalendar':
            unlqc__nyvkc = ['year', 'week', 'day']
            vff__spxhu = 'convert_datetime64_to_timestamp'
            icn__dnx = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            rfri__oiggp = attr + '()'
        dmgk__acaau = 'def impl(S_dt):\n'
        dmgk__acaau += '    S = S_dt._obj\n'
        dmgk__acaau += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        dmgk__acaau += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dmgk__acaau += '    numba.parfors.parfor.init_prange()\n'
        dmgk__acaau += '    n = len(arr)\n'
        for field in unlqc__nyvkc:
            dmgk__acaau += '    {} = {}\n'.format(field, icn__dnx)
        dmgk__acaau += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        dmgk__acaau += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in unlqc__nyvkc:
            dmgk__acaau += (
                '            bodo.libs.array_kernels.setna({}, i)\n'.format
                (field))
        dmgk__acaau += '            continue\n'
        len__xztrh = '(' + '[i], '.join(unlqc__nyvkc) + '[i])'
        dmgk__acaau += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(len__xztrh, vff__spxhu, rfri__oiggp))
        iekn__xye = '(' + ', '.join(unlqc__nyvkc) + ')'
        dnzr__yyxiu = "('" + "', '".join(unlqc__nyvkc) + "')"
        dmgk__acaau += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(iekn__xye, dnzr__yyxiu))
        oyyt__pfe = {}
        exec(dmgk__acaau, {'bodo': bodo, 'numba': numba, 'np': np}, oyyt__pfe)
        impl = oyyt__pfe['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    iraj__kenx = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, wcn__uxfi in iraj__kenx:
        xjia__upwn = create_series_dt_df_output_overload(attr)
        wcn__uxfi(SeriesDatetimePropertiesType, attr, inline='always')(
            xjia__upwn)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        dmgk__acaau = 'def impl(S_dt):\n'
        dmgk__acaau += '    S = S_dt._obj\n'
        dmgk__acaau += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        dmgk__acaau += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dmgk__acaau += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        dmgk__acaau += '    numba.parfors.parfor.init_prange()\n'
        dmgk__acaau += '    n = len(A)\n'
        dmgk__acaau += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        dmgk__acaau += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        dmgk__acaau += '        if bodo.libs.array_kernels.isna(A, i):\n'
        dmgk__acaau += '            bodo.libs.array_kernels.setna(B, i)\n'
        dmgk__acaau += '            continue\n'
        dmgk__acaau += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            dmgk__acaau += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            dmgk__acaau += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            dmgk__acaau += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            dmgk__acaau += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        dmgk__acaau += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        oyyt__pfe = {}
        exec(dmgk__acaau, {'numba': numba, 'np': np, 'bodo': bodo}, oyyt__pfe)
        impl = oyyt__pfe['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        dmgk__acaau = 'def impl(S_dt):\n'
        dmgk__acaau += '    S = S_dt._obj\n'
        dmgk__acaau += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        dmgk__acaau += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dmgk__acaau += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        dmgk__acaau += '    numba.parfors.parfor.init_prange()\n'
        dmgk__acaau += '    n = len(A)\n'
        if method == 'total_seconds':
            dmgk__acaau += '    B = np.empty(n, np.float64)\n'
        else:
            dmgk__acaau += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        dmgk__acaau += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        dmgk__acaau += '        if bodo.libs.array_kernels.isna(A, i):\n'
        dmgk__acaau += '            bodo.libs.array_kernels.setna(B, i)\n'
        dmgk__acaau += '            continue\n'
        dmgk__acaau += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            dmgk__acaau += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            dmgk__acaau += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            dmgk__acaau += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            dmgk__acaau += '    return B\n'
        oyyt__pfe = {}
        exec(dmgk__acaau, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, oyyt__pfe)
        impl = oyyt__pfe['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        xjia__upwn = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(xjia__upwn)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        xjia__upwn = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            xjia__upwn)


_install_S_dt_timedelta_methods()


@overload_method(SeriesDatetimePropertiesType, 'strftime', inline='always',
    no_unliteral=True)
def dt_strftime(S_dt, date_format):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return
    if types.unliteral(date_format) != types.unicode_type:
        raise BodoError(
            "Series.str.strftime(): 'date_format' argument must be a string")

    def impl(S_dt, date_format):
        ndelt__hvh = S_dt._obj
        pyats__kixu = bodo.hiframes.pd_series_ext.get_series_data(ndelt__hvh)
        zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(ndelt__hvh)
        wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(ndelt__hvh)
        numba.parfors.parfor.init_prange()
        tjns__npb = len(pyats__kixu)
        utlbu__ezts = bodo.libs.str_arr_ext.pre_alloc_string_array(tjns__npb,
            -1)
        for yqdkv__phvs in numba.parfors.parfor.internal_prange(tjns__npb):
            if bodo.libs.array_kernels.isna(pyats__kixu, yqdkv__phvs):
                bodo.libs.array_kernels.setna(utlbu__ezts, yqdkv__phvs)
                continue
            utlbu__ezts[yqdkv__phvs] = bodo.utils.conversion.box_if_dt64(
                pyats__kixu[yqdkv__phvs]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(utlbu__ezts,
            zfo__zzg, wgx__stb)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        ndelt__hvh = S_dt._obj
        sxqn__frj = get_series_data(ndelt__hvh).tz_convert(tz)
        zfo__zzg = get_series_index(ndelt__hvh)
        wgx__stb = get_series_name(ndelt__hvh)
        return init_series(sxqn__frj, zfo__zzg, wgx__stb)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
            f'Series.dt.{method}()')
        cydtt__dlhxq = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        voysx__eqg = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', cydtt__dlhxq,
            voysx__eqg, package_name='pandas', module_name='Series')
        dmgk__acaau = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        dmgk__acaau += '    S = S_dt._obj\n'
        dmgk__acaau += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        dmgk__acaau += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        dmgk__acaau += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        dmgk__acaau += '    numba.parfors.parfor.init_prange()\n'
        dmgk__acaau += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            dmgk__acaau += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            dmgk__acaau += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        dmgk__acaau += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        dmgk__acaau += '        if bodo.libs.array_kernels.isna(A, i):\n'
        dmgk__acaau += '            bodo.libs.array_kernels.setna(B, i)\n'
        dmgk__acaau += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            iribz__yuh = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            krqzd__pib = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            iribz__yuh = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            krqzd__pib = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        dmgk__acaau += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            krqzd__pib, iribz__yuh, method)
        dmgk__acaau += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        oyyt__pfe = {}
        exec(dmgk__acaau, {'numba': numba, 'np': np, 'bodo': bodo}, oyyt__pfe)
        impl = oyyt__pfe['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    rnlj__pvzl = ['ceil', 'floor', 'round']
    for method in rnlj__pvzl:
        xjia__upwn = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            xjia__upwn)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                esd__irur = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                jzg__qwd = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    esd__irur)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                uuyxa__mjat = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                ljlm__zbi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    uuyxa__mjat)
                tjns__npb = len(jzg__qwd)
                ndelt__hvh = np.empty(tjns__npb, timedelta64_dtype)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    sml__chq = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        jzg__qwd[uxady__luo])
                    pnzf__sepdr = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(ljlm__zbi[uxady__luo]))
                    if sml__chq == epeam__xvs or pnzf__sepdr == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(sml__chq, pnzf__sepdr)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                ljlm__zbi = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                tjns__npb = len(zlkr__tzs)
                ndelt__hvh = np.empty(tjns__npb, dt64_dtype)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    pihm__uspou = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zlkr__tzs[uxady__luo]))
                    wevf__udi = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(ljlm__zbi[uxady__luo]))
                    if pihm__uspou == epeam__xvs or wevf__udi == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(pihm__uspou, wevf__udi)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                ljlm__zbi = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                tjns__npb = len(zlkr__tzs)
                ndelt__hvh = np.empty(tjns__npb, dt64_dtype)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    pihm__uspou = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zlkr__tzs[uxady__luo]))
                    wevf__udi = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(ljlm__zbi[uxady__luo]))
                    if pihm__uspou == epeam__xvs or wevf__udi == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(pihm__uspou, wevf__udi)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tjns__npb = len(zlkr__tzs)
                ndelt__hvh = np.empty(tjns__npb, timedelta64_dtype)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                ktw__icu = rhs.value
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    pihm__uspou = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zlkr__tzs[uxady__luo]))
                    if pihm__uspou == epeam__xvs or ktw__icu == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(pihm__uspou, ktw__icu)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tjns__npb = len(zlkr__tzs)
                ndelt__hvh = np.empty(tjns__npb, timedelta64_dtype)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                ktw__icu = lhs.value
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    pihm__uspou = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zlkr__tzs[uxady__luo]))
                    if ktw__icu == epeam__xvs or pihm__uspou == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(ktw__icu, pihm__uspou)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tjns__npb = len(zlkr__tzs)
                ndelt__hvh = np.empty(tjns__npb, dt64_dtype)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                lot__lzcxu = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                wevf__udi = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(lot__lzcxu))
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    pihm__uspou = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zlkr__tzs[uxady__luo]))
                    if pihm__uspou == epeam__xvs or wevf__udi == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(pihm__uspou, wevf__udi)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tjns__npb = len(zlkr__tzs)
                ndelt__hvh = np.empty(tjns__npb, dt64_dtype)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                lot__lzcxu = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                wevf__udi = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(lot__lzcxu))
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    pihm__uspou = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zlkr__tzs[uxady__luo]))
                    if pihm__uspou == epeam__xvs or wevf__udi == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(pihm__uspou, wevf__udi)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tjns__npb = len(zlkr__tzs)
                ndelt__hvh = np.empty(tjns__npb, timedelta64_dtype)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                cwtgl__qoq = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                pihm__uspou = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    cwtgl__qoq)
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    ocdyj__tkxzh = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zlkr__tzs[uxady__luo]))
                    if ocdyj__tkxzh == epeam__xvs or pihm__uspou == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(ocdyj__tkxzh, pihm__uspou)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tjns__npb = len(zlkr__tzs)
                ndelt__hvh = np.empty(tjns__npb, timedelta64_dtype)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                cwtgl__qoq = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                pihm__uspou = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    cwtgl__qoq)
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    ocdyj__tkxzh = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zlkr__tzs[uxady__luo]))
                    if pihm__uspou == epeam__xvs or ocdyj__tkxzh == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(pihm__uspou, ocdyj__tkxzh)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            thkm__ewtq = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zlkr__tzs = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tjns__npb = len(zlkr__tzs)
                ndelt__hvh = np.empty(tjns__npb, timedelta64_dtype)
                epeam__xvs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(thkm__ewtq))
                lot__lzcxu = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                wevf__udi = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(lot__lzcxu))
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    nwy__jgmz = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zlkr__tzs[uxady__luo]))
                    if wevf__udi == epeam__xvs or nwy__jgmz == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(nwy__jgmz, wevf__udi)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            thkm__ewtq = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zlkr__tzs = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tjns__npb = len(zlkr__tzs)
                ndelt__hvh = np.empty(tjns__npb, timedelta64_dtype)
                epeam__xvs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(thkm__ewtq))
                lot__lzcxu = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                wevf__udi = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(lot__lzcxu))
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    nwy__jgmz = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zlkr__tzs[uxady__luo]))
                    if wevf__udi == epeam__xvs or nwy__jgmz == epeam__xvs:
                        blpo__tdfh = epeam__xvs
                    else:
                        blpo__tdfh = op(wevf__udi, nwy__jgmz)
                    ndelt__hvh[uxady__luo
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        blpo__tdfh)
                return bodo.hiframes.pd_series_ext.init_series(ndelt__hvh,
                    zfo__zzg, wgx__stb)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            ccvrx__refga = True
        else:
            ccvrx__refga = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            thkm__ewtq = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zlkr__tzs = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tjns__npb = len(zlkr__tzs)
                wwzd__gukv = bodo.libs.bool_arr_ext.alloc_bool_array(tjns__npb)
                epeam__xvs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(thkm__ewtq))
                ycb__unp = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                sdw__ethe = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ycb__unp))
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    avf__phrg = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zlkr__tzs[uxady__luo]))
                    if avf__phrg == epeam__xvs or sdw__ethe == epeam__xvs:
                        blpo__tdfh = ccvrx__refga
                    else:
                        blpo__tdfh = op(avf__phrg, sdw__ethe)
                    wwzd__gukv[uxady__luo] = blpo__tdfh
                return bodo.hiframes.pd_series_ext.init_series(wwzd__gukv,
                    zfo__zzg, wgx__stb)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            thkm__ewtq = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                zlkr__tzs = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tjns__npb = len(zlkr__tzs)
                wwzd__gukv = bodo.libs.bool_arr_ext.alloc_bool_array(tjns__npb)
                epeam__xvs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(thkm__ewtq))
                sfx__qawf = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                avf__phrg = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(sfx__qawf))
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    sdw__ethe = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(zlkr__tzs[uxady__luo]))
                    if avf__phrg == epeam__xvs or sdw__ethe == epeam__xvs:
                        blpo__tdfh = ccvrx__refga
                    else:
                        blpo__tdfh = op(avf__phrg, sdw__ethe)
                    wwzd__gukv[uxady__luo] = blpo__tdfh
                return bodo.hiframes.pd_series_ext.init_series(wwzd__gukv,
                    zfo__zzg, wgx__stb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                tjns__npb = len(zlkr__tzs)
                wwzd__gukv = bodo.libs.bool_arr_ext.alloc_bool_array(tjns__npb)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    avf__phrg = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zlkr__tzs[uxady__luo])
                    if avf__phrg == epeam__xvs or rhs.value == epeam__xvs:
                        blpo__tdfh = ccvrx__refga
                    else:
                        blpo__tdfh = op(avf__phrg, rhs.value)
                    wwzd__gukv[uxady__luo] = blpo__tdfh
                return bodo.hiframes.pd_series_ext.init_series(wwzd__gukv,
                    zfo__zzg, wgx__stb)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                tjns__npb = len(zlkr__tzs)
                wwzd__gukv = bodo.libs.bool_arr_ext.alloc_bool_array(tjns__npb)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    sdw__ethe = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zlkr__tzs[uxady__luo])
                    if sdw__ethe == epeam__xvs or lhs.value == epeam__xvs:
                        blpo__tdfh = ccvrx__refga
                    else:
                        blpo__tdfh = op(lhs.value, sdw__ethe)
                    wwzd__gukv[uxady__luo] = blpo__tdfh
                return bodo.hiframes.pd_series_ext.init_series(wwzd__gukv,
                    zfo__zzg, wgx__stb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                tjns__npb = len(zlkr__tzs)
                wwzd__gukv = bodo.libs.bool_arr_ext.alloc_bool_array(tjns__npb)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                ucscm__qwr = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                uhr__gvw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ucscm__qwr)
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    avf__phrg = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        zlkr__tzs[uxady__luo])
                    if avf__phrg == epeam__xvs or uhr__gvw == epeam__xvs:
                        blpo__tdfh = ccvrx__refga
                    else:
                        blpo__tdfh = op(avf__phrg, uhr__gvw)
                    wwzd__gukv[uxady__luo] = blpo__tdfh
                return bodo.hiframes.pd_series_ext.init_series(wwzd__gukv,
                    zfo__zzg, wgx__stb)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            thkm__ewtq = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                hxrue__wkn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                zlkr__tzs = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    hxrue__wkn)
                zfo__zzg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                wgx__stb = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                tjns__npb = len(zlkr__tzs)
                wwzd__gukv = bodo.libs.bool_arr_ext.alloc_bool_array(tjns__npb)
                epeam__xvs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    thkm__ewtq)
                ucscm__qwr = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                uhr__gvw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    ucscm__qwr)
                for uxady__luo in numba.parfors.parfor.internal_prange(
                    tjns__npb):
                    cwtgl__qoq = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(zlkr__tzs[uxady__luo]))
                    if cwtgl__qoq == epeam__xvs or uhr__gvw == epeam__xvs:
                        blpo__tdfh = ccvrx__refga
                    else:
                        blpo__tdfh = op(uhr__gvw, cwtgl__qoq)
                    wwzd__gukv[uxady__luo] = blpo__tdfh
                return bodo.hiframes.pd_series_ext.init_series(wwzd__gukv,
                    zfo__zzg, wgx__stb)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for egy__ngedh in series_dt_unsupported_attrs:
        pihft__lahev = 'Series.dt.' + egy__ngedh
        overload_attribute(SeriesDatetimePropertiesType, egy__ngedh)(
            create_unsupported_overload(pihft__lahev))
    for fitjo__fwkrw in series_dt_unsupported_methods:
        pihft__lahev = 'Series.dt.' + fitjo__fwkrw
        overload_method(SeriesDatetimePropertiesType, fitjo__fwkrw,
            no_unliteral=True)(create_unsupported_overload(pihft__lahev))


_install_series_dt_unsupported()
