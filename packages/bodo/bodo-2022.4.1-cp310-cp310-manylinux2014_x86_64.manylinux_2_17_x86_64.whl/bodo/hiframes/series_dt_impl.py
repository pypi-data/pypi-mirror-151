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
        sac__cnllu = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(sac__cnllu)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        iyqc__gug = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, iyqc__gug)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        gqd__pcfg, = args
        jhmc__plp = signature.return_type
        dpoui__vatt = cgutils.create_struct_proxy(jhmc__plp)(context, builder)
        dpoui__vatt.obj = gqd__pcfg
        context.nrt.incref(builder, signature.args[0], gqd__pcfg)
        return dpoui__vatt._getvalue()
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
        cqkx__prwkd = 'def impl(S_dt):\n'
        cqkx__prwkd += '    S = S_dt._obj\n'
        cqkx__prwkd += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        cqkx__prwkd += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        cqkx__prwkd += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        cqkx__prwkd += '    numba.parfors.parfor.init_prange()\n'
        cqkx__prwkd += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            cqkx__prwkd += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            cqkx__prwkd += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        cqkx__prwkd += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        cqkx__prwkd += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        cqkx__prwkd += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        cqkx__prwkd += '            continue\n'
        cqkx__prwkd += (
            '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
            )
        if field in ('year', 'month', 'day'):
            cqkx__prwkd += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            if field in ('month', 'day'):
                cqkx__prwkd += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            cqkx__prwkd += '        out_arr[i] = {}\n'.format(field)
        elif field in ('dayofyear', 'day_of_year', 'dayofweek',
            'day_of_week', 'weekday'):
            xvu__qmgss = {'dayofyear': 'get_day_of_year', 'day_of_year':
                'get_day_of_year', 'dayofweek': 'get_day_of_week',
                'day_of_week': 'get_day_of_week', 'weekday': 'get_day_of_week'}
            cqkx__prwkd += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            cqkx__prwkd += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            cqkx__prwkd += (
                """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month, day)
"""
                .format(xvu__qmgss[field]))
        elif field == 'is_leap_year':
            cqkx__prwkd += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            cqkx__prwkd += """        out_arr[i] = bodo.hiframes.pd_timestamp_ext.is_leap_year(year)
"""
        elif field in ('daysinmonth', 'days_in_month'):
            xvu__qmgss = {'days_in_month': 'get_days_in_month',
                'daysinmonth': 'get_days_in_month'}
            cqkx__prwkd += """        dt, year, days = bodo.hiframes.pd_timestamp_ext.extract_year_days(dt64)
"""
            cqkx__prwkd += """        month, day = bodo.hiframes.pd_timestamp_ext.get_month_day(year, days)
"""
            cqkx__prwkd += (
                '        out_arr[i] = bodo.hiframes.pd_timestamp_ext.{}(year, month)\n'
                .format(xvu__qmgss[field]))
        else:
            cqkx__prwkd += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            cqkx__prwkd += '        out_arr[i] = ts.' + field + '\n'
        cqkx__prwkd += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        lji__nok = {}
        exec(cqkx__prwkd, {'bodo': bodo, 'numba': numba, 'np': np}, lji__nok)
        impl = lji__nok['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        qouj__lps = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(qouj__lps)


_install_date_fields()


def create_date_method_overload(method):
    wjngc__ondrw = method in ['day_name', 'month_name']
    if wjngc__ondrw:
        cqkx__prwkd = 'def overload_method(S_dt, locale=None):\n'
        cqkx__prwkd += '    unsupported_args = dict(locale=locale)\n'
        cqkx__prwkd += '    arg_defaults = dict(locale=None)\n'
        cqkx__prwkd += '    bodo.utils.typing.check_unsupported_args(\n'
        cqkx__prwkd += f"        'Series.dt.{method}',\n"
        cqkx__prwkd += '        unsupported_args,\n'
        cqkx__prwkd += '        arg_defaults,\n'
        cqkx__prwkd += "        package_name='pandas',\n"
        cqkx__prwkd += "        module_name='Series',\n"
        cqkx__prwkd += '    )\n'
    else:
        cqkx__prwkd = 'def overload_method(S_dt):\n'
        cqkx__prwkd += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    cqkx__prwkd += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    cqkx__prwkd += '        return\n'
    if wjngc__ondrw:
        cqkx__prwkd += '    def impl(S_dt, locale=None):\n'
    else:
        cqkx__prwkd += '    def impl(S_dt):\n'
    cqkx__prwkd += '        S = S_dt._obj\n'
    cqkx__prwkd += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    cqkx__prwkd += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    cqkx__prwkd += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    cqkx__prwkd += '        numba.parfors.parfor.init_prange()\n'
    cqkx__prwkd += '        n = len(arr)\n'
    if wjngc__ondrw:
        cqkx__prwkd += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        cqkx__prwkd += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    cqkx__prwkd += (
        '        for i in numba.parfors.parfor.internal_prange(n):\n')
    cqkx__prwkd += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    cqkx__prwkd += (
        '                bodo.libs.array_kernels.setna(out_arr, i)\n')
    cqkx__prwkd += '                continue\n'
    cqkx__prwkd += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    cqkx__prwkd += f'            method_val = ts.{method}()\n'
    if wjngc__ondrw:
        cqkx__prwkd += '            out_arr[i] = method_val\n'
    else:
        cqkx__prwkd += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    cqkx__prwkd += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    cqkx__prwkd += '    return impl\n'
    lji__nok = {}
    exec(cqkx__prwkd, {'bodo': bodo, 'numba': numba, 'np': np}, lji__nok)
    overload_method = lji__nok['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        qouj__lps = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            qouj__lps)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        rgysy__mdh = S_dt._obj
        jvvqq__lgn = bodo.hiframes.pd_series_ext.get_series_data(rgysy__mdh)
        qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(rgysy__mdh)
        sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(rgysy__mdh)
        numba.parfors.parfor.init_prange()
        rqgyu__ziljd = len(jvvqq__lgn)
        vew__vlq = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            rqgyu__ziljd)
        for vkuo__ynf in numba.parfors.parfor.internal_prange(rqgyu__ziljd):
            oocgs__gjvkg = jvvqq__lgn[vkuo__ynf]
            raf__zanw = bodo.utils.conversion.box_if_dt64(oocgs__gjvkg)
            vew__vlq[vkuo__ynf] = datetime.date(raf__zanw.year, raf__zanw.
                month, raf__zanw.day)
        return bodo.hiframes.pd_series_ext.init_series(vew__vlq,
            qoof__feyfz, sac__cnllu)
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
            vui__myubk = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            nuss__jgd = 'convert_numpy_timedelta64_to_pd_timedelta'
            rwcg__dnwu = 'np.empty(n, np.int64)'
            lzk__xhue = attr
        elif attr == 'isocalendar':
            vui__myubk = ['year', 'week', 'day']
            nuss__jgd = 'convert_datetime64_to_timestamp'
            rwcg__dnwu = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            lzk__xhue = attr + '()'
        cqkx__prwkd = 'def impl(S_dt):\n'
        cqkx__prwkd += '    S = S_dt._obj\n'
        cqkx__prwkd += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        cqkx__prwkd += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        cqkx__prwkd += '    numba.parfors.parfor.init_prange()\n'
        cqkx__prwkd += '    n = len(arr)\n'
        for field in vui__myubk:
            cqkx__prwkd += '    {} = {}\n'.format(field, rwcg__dnwu)
        cqkx__prwkd += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        cqkx__prwkd += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in vui__myubk:
            cqkx__prwkd += (
                '            bodo.libs.array_kernels.setna({}, i)\n'.format
                (field))
        cqkx__prwkd += '            continue\n'
        uiwi__htbzx = '(' + '[i], '.join(vui__myubk) + '[i])'
        cqkx__prwkd += (
            '        {} = bodo.hiframes.pd_timestamp_ext.{}(arr[i]).{}\n'.
            format(uiwi__htbzx, nuss__jgd, lzk__xhue))
        lwh__gecj = '(' + ', '.join(vui__myubk) + ')'
        zan__izda = "('" + "', '".join(vui__myubk) + "')"
        cqkx__prwkd += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, {})\n'
            .format(lwh__gecj, zan__izda))
        lji__nok = {}
        exec(cqkx__prwkd, {'bodo': bodo, 'numba': numba, 'np': np}, lji__nok)
        impl = lji__nok['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    dlhad__iwehi = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, xew__kkwmn in dlhad__iwehi:
        qouj__lps = create_series_dt_df_output_overload(attr)
        xew__kkwmn(SeriesDatetimePropertiesType, attr, inline='always')(
            qouj__lps)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        cqkx__prwkd = 'def impl(S_dt):\n'
        cqkx__prwkd += '    S = S_dt._obj\n'
        cqkx__prwkd += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        cqkx__prwkd += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        cqkx__prwkd += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        cqkx__prwkd += '    numba.parfors.parfor.init_prange()\n'
        cqkx__prwkd += '    n = len(A)\n'
        cqkx__prwkd += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        cqkx__prwkd += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        cqkx__prwkd += '        if bodo.libs.array_kernels.isna(A, i):\n'
        cqkx__prwkd += '            bodo.libs.array_kernels.setna(B, i)\n'
        cqkx__prwkd += '            continue\n'
        cqkx__prwkd += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            cqkx__prwkd += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            cqkx__prwkd += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            cqkx__prwkd += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            cqkx__prwkd += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        cqkx__prwkd += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        lji__nok = {}
        exec(cqkx__prwkd, {'numba': numba, 'np': np, 'bodo': bodo}, lji__nok)
        impl = lji__nok['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        cqkx__prwkd = 'def impl(S_dt):\n'
        cqkx__prwkd += '    S = S_dt._obj\n'
        cqkx__prwkd += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        cqkx__prwkd += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        cqkx__prwkd += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        cqkx__prwkd += '    numba.parfors.parfor.init_prange()\n'
        cqkx__prwkd += '    n = len(A)\n'
        if method == 'total_seconds':
            cqkx__prwkd += '    B = np.empty(n, np.float64)\n'
        else:
            cqkx__prwkd += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        cqkx__prwkd += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        cqkx__prwkd += '        if bodo.libs.array_kernels.isna(A, i):\n'
        cqkx__prwkd += '            bodo.libs.array_kernels.setna(B, i)\n'
        cqkx__prwkd += '            continue\n'
        cqkx__prwkd += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            cqkx__prwkd += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            cqkx__prwkd += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            cqkx__prwkd += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            cqkx__prwkd += '    return B\n'
        lji__nok = {}
        exec(cqkx__prwkd, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, lji__nok)
        impl = lji__nok['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        qouj__lps = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(qouj__lps)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        qouj__lps = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            qouj__lps)


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
        rgysy__mdh = S_dt._obj
        hycr__ypbzr = bodo.hiframes.pd_series_ext.get_series_data(rgysy__mdh)
        qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(rgysy__mdh)
        sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(rgysy__mdh)
        numba.parfors.parfor.init_prange()
        rqgyu__ziljd = len(hycr__ypbzr)
        nrotx__bjbco = bodo.libs.str_arr_ext.pre_alloc_string_array(
            rqgyu__ziljd, -1)
        for rrjo__gbyq in numba.parfors.parfor.internal_prange(rqgyu__ziljd):
            if bodo.libs.array_kernels.isna(hycr__ypbzr, rrjo__gbyq):
                bodo.libs.array_kernels.setna(nrotx__bjbco, rrjo__gbyq)
                continue
            nrotx__bjbco[rrjo__gbyq] = bodo.utils.conversion.box_if_dt64(
                hycr__ypbzr[rrjo__gbyq]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(nrotx__bjbco,
            qoof__feyfz, sac__cnllu)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        rgysy__mdh = S_dt._obj
        hksbc__kxj = get_series_data(rgysy__mdh).tz_convert(tz)
        qoof__feyfz = get_series_index(rgysy__mdh)
        sac__cnllu = get_series_name(rgysy__mdh)
        return init_series(hksbc__kxj, qoof__feyfz, sac__cnllu)
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
        sjjpq__oxyv = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        isop__lxiwm = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', sjjpq__oxyv,
            isop__lxiwm, package_name='pandas', module_name='Series')
        cqkx__prwkd = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        cqkx__prwkd += '    S = S_dt._obj\n'
        cqkx__prwkd += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        cqkx__prwkd += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        cqkx__prwkd += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        cqkx__prwkd += '    numba.parfors.parfor.init_prange()\n'
        cqkx__prwkd += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            cqkx__prwkd += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        else:
            cqkx__prwkd += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        cqkx__prwkd += (
            '    for i in numba.parfors.parfor.internal_prange(n):\n')
        cqkx__prwkd += '        if bodo.libs.array_kernels.isna(A, i):\n'
        cqkx__prwkd += '            bodo.libs.array_kernels.setna(B, i)\n'
        cqkx__prwkd += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            qrh__vii = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            png__pep = 'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64'
        else:
            qrh__vii = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            png__pep = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        cqkx__prwkd += '        B[i] = {}({}(A[i]).{}(freq).value)\n'.format(
            png__pep, qrh__vii, method)
        cqkx__prwkd += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        lji__nok = {}
        exec(cqkx__prwkd, {'numba': numba, 'np': np, 'bodo': bodo}, lji__nok)
        impl = lji__nok['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    wpecb__lmvr = ['ceil', 'floor', 'round']
    for method in wpecb__lmvr:
        qouj__lps = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            qouj__lps)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                adaf__dguk = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                dpevv__cml = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    adaf__dguk)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                kqli__anauh = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                cgil__mpg = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    kqli__anauh)
                rqgyu__ziljd = len(dpevv__cml)
                rgysy__mdh = np.empty(rqgyu__ziljd, timedelta64_dtype)
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    ftvdt__htugm = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(dpevv__cml[vkuo__ynf]))
                    blis__fjs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        cgil__mpg[vkuo__ynf])
                    if ftvdt__htugm == nvv__pglqs or blis__fjs == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(ftvdt__htugm, blis__fjs)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                cgil__mpg = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                rgysy__mdh = np.empty(rqgyu__ziljd, dt64_dtype)
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    sgwfp__qcdw = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    qqjd__qlzpr = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(cgil__mpg[vkuo__ynf]))
                    if sgwfp__qcdw == nvv__pglqs or qqjd__qlzpr == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(sgwfp__qcdw, qqjd__qlzpr)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                cgil__mpg = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                rgysy__mdh = np.empty(rqgyu__ziljd, dt64_dtype)
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    sgwfp__qcdw = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    qqjd__qlzpr = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(cgil__mpg[vkuo__ynf]))
                    if sgwfp__qcdw == nvv__pglqs or qqjd__qlzpr == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(sgwfp__qcdw, qqjd__qlzpr)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                rgysy__mdh = np.empty(rqgyu__ziljd, timedelta64_dtype)
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                cwvl__yqac = rhs.value
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    sgwfp__qcdw = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if sgwfp__qcdw == nvv__pglqs or cwvl__yqac == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(sgwfp__qcdw, cwvl__yqac)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                rgysy__mdh = np.empty(rqgyu__ziljd, timedelta64_dtype)
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                cwvl__yqac = lhs.value
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    sgwfp__qcdw = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if cwvl__yqac == nvv__pglqs or sgwfp__qcdw == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(cwvl__yqac, sgwfp__qcdw)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                rgysy__mdh = np.empty(rqgyu__ziljd, dt64_dtype)
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                mimy__rmyho = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                qqjd__qlzpr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(mimy__rmyho))
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    sgwfp__qcdw = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if sgwfp__qcdw == nvv__pglqs or qqjd__qlzpr == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(sgwfp__qcdw, qqjd__qlzpr)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                rgysy__mdh = np.empty(rqgyu__ziljd, dt64_dtype)
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                mimy__rmyho = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                qqjd__qlzpr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(mimy__rmyho))
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    sgwfp__qcdw = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if sgwfp__qcdw == nvv__pglqs or qqjd__qlzpr == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(sgwfp__qcdw, qqjd__qlzpr)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                rgysy__mdh = np.empty(rqgyu__ziljd, timedelta64_dtype)
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                kbn__yixkm = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                sgwfp__qcdw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    kbn__yixkm)
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    hli__pwpp = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        jvvqq__lgn[vkuo__ynf])
                    if hli__pwpp == nvv__pglqs or sgwfp__qcdw == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(hli__pwpp, sgwfp__qcdw)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                rgysy__mdh = np.empty(rqgyu__ziljd, timedelta64_dtype)
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                kbn__yixkm = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                sgwfp__qcdw = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    kbn__yixkm)
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    hli__pwpp = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        jvvqq__lgn[vkuo__ynf])
                    if sgwfp__qcdw == nvv__pglqs or hli__pwpp == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(sgwfp__qcdw, hli__pwpp)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            saj__dsy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jvvqq__lgn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                rgysy__mdh = np.empty(rqgyu__ziljd, timedelta64_dtype)
                nvv__pglqs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(saj__dsy))
                mimy__rmyho = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                qqjd__qlzpr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(mimy__rmyho))
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    yzare__mhhb = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if qqjd__qlzpr == nvv__pglqs or yzare__mhhb == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(yzare__mhhb, qqjd__qlzpr)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            saj__dsy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jvvqq__lgn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                rgysy__mdh = np.empty(rqgyu__ziljd, timedelta64_dtype)
                nvv__pglqs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(saj__dsy))
                mimy__rmyho = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                qqjd__qlzpr = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(mimy__rmyho))
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    yzare__mhhb = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if qqjd__qlzpr == nvv__pglqs or yzare__mhhb == nvv__pglqs:
                        rnmd__hexu = nvv__pglqs
                    else:
                        rnmd__hexu = op(qqjd__qlzpr, yzare__mhhb)
                    rgysy__mdh[vkuo__ynf
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        rnmd__hexu)
                return bodo.hiframes.pd_series_ext.init_series(rgysy__mdh,
                    qoof__feyfz, sac__cnllu)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            vpx__ybpod = True
        else:
            vpx__ybpod = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            saj__dsy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jvvqq__lgn = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                vew__vlq = bodo.libs.bool_arr_ext.alloc_bool_array(rqgyu__ziljd
                    )
                nvv__pglqs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(saj__dsy))
                quo__wtz = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                kduf__xakbe = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(quo__wtz))
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    kluqz__ozcc = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if kluqz__ozcc == nvv__pglqs or kduf__xakbe == nvv__pglqs:
                        rnmd__hexu = vpx__ybpod
                    else:
                        rnmd__hexu = op(kluqz__ozcc, kduf__xakbe)
                    vew__vlq[vkuo__ynf] = rnmd__hexu
                return bodo.hiframes.pd_series_ext.init_series(vew__vlq,
                    qoof__feyfz, sac__cnllu)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            saj__dsy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                jvvqq__lgn = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                vew__vlq = bodo.libs.bool_arr_ext.alloc_bool_array(rqgyu__ziljd
                    )
                nvv__pglqs = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(saj__dsy))
                dvzsy__keoj = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                kluqz__ozcc = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(dvzsy__keoj))
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    kduf__xakbe = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if kluqz__ozcc == nvv__pglqs or kduf__xakbe == nvv__pglqs:
                        rnmd__hexu = vpx__ybpod
                    else:
                        rnmd__hexu = op(kluqz__ozcc, kduf__xakbe)
                    vew__vlq[vkuo__ynf] = rnmd__hexu
                return bodo.hiframes.pd_series_ext.init_series(vew__vlq,
                    qoof__feyfz, sac__cnllu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                vew__vlq = bodo.libs.bool_arr_ext.alloc_bool_array(rqgyu__ziljd
                    )
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    kluqz__ozcc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if kluqz__ozcc == nvv__pglqs or rhs.value == nvv__pglqs:
                        rnmd__hexu = vpx__ybpod
                    else:
                        rnmd__hexu = op(kluqz__ozcc, rhs.value)
                    vew__vlq[vkuo__ynf] = rnmd__hexu
                return bodo.hiframes.pd_series_ext.init_series(vew__vlq,
                    qoof__feyfz, sac__cnllu)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type and
            bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs)):
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                rqgyu__ziljd = len(jvvqq__lgn)
                vew__vlq = bodo.libs.bool_arr_ext.alloc_bool_array(rqgyu__ziljd
                    )
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    kduf__xakbe = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if kduf__xakbe == nvv__pglqs or lhs.value == nvv__pglqs:
                        rnmd__hexu = vpx__ybpod
                    else:
                        rnmd__hexu = op(lhs.value, kduf__xakbe)
                    vew__vlq[vkuo__ynf] = rnmd__hexu
                return bodo.hiframes.pd_series_ext.init_series(vew__vlq,
                    qoof__feyfz, sac__cnllu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                rqgyu__ziljd = len(jvvqq__lgn)
                vew__vlq = bodo.libs.bool_arr_ext.alloc_bool_array(rqgyu__ziljd
                    )
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                pbdp__pwnac = (bodo.hiframes.pd_timestamp_ext.
                    parse_datetime_str(rhs))
                shpih__kml = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    pbdp__pwnac)
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    kluqz__ozcc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if kluqz__ozcc == nvv__pglqs or shpih__kml == nvv__pglqs:
                        rnmd__hexu = vpx__ybpod
                    else:
                        rnmd__hexu = op(kluqz__ozcc, shpih__kml)
                    vew__vlq[vkuo__ynf] = rnmd__hexu
                return bodo.hiframes.pd_series_ext.init_series(vew__vlq,
                    qoof__feyfz, sac__cnllu)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            saj__dsy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                xecn__mgy = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                jvvqq__lgn = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    xecn__mgy)
                qoof__feyfz = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                sac__cnllu = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                rqgyu__ziljd = len(jvvqq__lgn)
                vew__vlq = bodo.libs.bool_arr_ext.alloc_bool_array(rqgyu__ziljd
                    )
                nvv__pglqs = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    saj__dsy)
                pbdp__pwnac = (bodo.hiframes.pd_timestamp_ext.
                    parse_datetime_str(lhs))
                shpih__kml = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    pbdp__pwnac)
                for vkuo__ynf in numba.parfors.parfor.internal_prange(
                    rqgyu__ziljd):
                    kbn__yixkm = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(jvvqq__lgn[vkuo__ynf]))
                    if kbn__yixkm == nvv__pglqs or shpih__kml == nvv__pglqs:
                        rnmd__hexu = vpx__ybpod
                    else:
                        rnmd__hexu = op(shpih__kml, kbn__yixkm)
                    vew__vlq[vkuo__ynf] = rnmd__hexu
                return bodo.hiframes.pd_series_ext.init_series(vew__vlq,
                    qoof__feyfz, sac__cnllu)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for cpjqd__ydlw in series_dt_unsupported_attrs:
        yzdl__zdym = 'Series.dt.' + cpjqd__ydlw
        overload_attribute(SeriesDatetimePropertiesType, cpjqd__ydlw)(
            create_unsupported_overload(yzdl__zdym))
    for rsjc__xbgj in series_dt_unsupported_methods:
        yzdl__zdym = 'Series.dt.' + rsjc__xbgj
        overload_method(SeriesDatetimePropertiesType, rsjc__xbgj,
            no_unliteral=True)(create_unsupported_overload(yzdl__zdym))


_install_series_dt_unsupported()
