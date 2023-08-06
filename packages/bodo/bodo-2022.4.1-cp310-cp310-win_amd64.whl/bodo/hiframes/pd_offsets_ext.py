"""
Implement support for the various classes in pd.tseries.offsets.
"""
import operator
import llvmlite.binding as ll
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.pd_timestamp_ext import get_days_in_month, pd_timestamp_type
from bodo.libs import hdatetime_ext
from bodo.utils.typing import BodoError, create_unsupported_overload, is_overload_none
ll.add_symbol('box_date_offset', hdatetime_ext.box_date_offset)
ll.add_symbol('unbox_date_offset', hdatetime_ext.unbox_date_offset)


class MonthBeginType(types.Type):

    def __init__(self):
        super(MonthBeginType, self).__init__(name='MonthBeginType()')


month_begin_type = MonthBeginType()


@typeof_impl.register(pd.tseries.offsets.MonthBegin)
def typeof_month_begin(val, c):
    return month_begin_type


@register_model(MonthBeginType)
class MonthBeginModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        htpc__unj = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, htpc__unj)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    abeb__jsmxy = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    asx__xvvru = c.pyapi.long_from_longlong(abeb__jsmxy.n)
    wuqvx__pqdvz = c.pyapi.from_native_value(types.boolean, abeb__jsmxy.
        normalize, c.env_manager)
    tyxu__awaxs = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    bjwlf__zqd = c.pyapi.call_function_objargs(tyxu__awaxs, (asx__xvvru,
        wuqvx__pqdvz))
    c.pyapi.decref(asx__xvvru)
    c.pyapi.decref(wuqvx__pqdvz)
    c.pyapi.decref(tyxu__awaxs)
    return bjwlf__zqd


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    asx__xvvru = c.pyapi.object_getattr_string(val, 'n')
    wuqvx__pqdvz = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(asx__xvvru)
    normalize = c.pyapi.to_native_value(types.bool_, wuqvx__pqdvz).value
    abeb__jsmxy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    abeb__jsmxy.n = n
    abeb__jsmxy.normalize = normalize
    c.pyapi.decref(asx__xvvru)
    c.pyapi.decref(wuqvx__pqdvz)
    ihvxi__wbwvf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(abeb__jsmxy._getvalue(), is_error=ihvxi__wbwvf)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        abeb__jsmxy = cgutils.create_struct_proxy(typ)(context, builder)
        abeb__jsmxy.n = args[0]
        abeb__jsmxy.normalize = args[1]
        return abeb__jsmxy._getvalue()
    return MonthBeginType()(n, normalize), codegen


make_attribute_wrapper(MonthBeginType, 'n', 'n')
make_attribute_wrapper(MonthBeginType, 'normalize', 'normalize')


@register_jitable
def calculate_month_begin_date(year, month, day, n):
    if n <= 0:
        if day > 1:
            n += 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = 1
    return year, month, day


def overload_add_operator_month_begin_offset_type(lhs, rhs):
    if lhs == month_begin_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_begin_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_begin_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_begin_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


class MonthEndType(types.Type):

    def __init__(self):
        super(MonthEndType, self).__init__(name='MonthEndType()')


month_end_type = MonthEndType()


@typeof_impl.register(pd.tseries.offsets.MonthEnd)
def typeof_month_end(val, c):
    return month_end_type


@register_model(MonthEndType)
class MonthEndModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        htpc__unj = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, htpc__unj)


@box(MonthEndType)
def box_month_end(typ, val, c):
    hllco__mbnu = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    asx__xvvru = c.pyapi.long_from_longlong(hllco__mbnu.n)
    wuqvx__pqdvz = c.pyapi.from_native_value(types.boolean, hllco__mbnu.
        normalize, c.env_manager)
    scp__uapuh = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    bjwlf__zqd = c.pyapi.call_function_objargs(scp__uapuh, (asx__xvvru,
        wuqvx__pqdvz))
    c.pyapi.decref(asx__xvvru)
    c.pyapi.decref(wuqvx__pqdvz)
    c.pyapi.decref(scp__uapuh)
    return bjwlf__zqd


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    asx__xvvru = c.pyapi.object_getattr_string(val, 'n')
    wuqvx__pqdvz = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(asx__xvvru)
    normalize = c.pyapi.to_native_value(types.bool_, wuqvx__pqdvz).value
    hllco__mbnu = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hllco__mbnu.n = n
    hllco__mbnu.normalize = normalize
    c.pyapi.decref(asx__xvvru)
    c.pyapi.decref(wuqvx__pqdvz)
    ihvxi__wbwvf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hllco__mbnu._getvalue(), is_error=ihvxi__wbwvf)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        hllco__mbnu = cgutils.create_struct_proxy(typ)(context, builder)
        hllco__mbnu.n = args[0]
        hllco__mbnu.normalize = args[1]
        return hllco__mbnu._getvalue()
    return MonthEndType()(n, normalize), codegen


make_attribute_wrapper(MonthEndType, 'n', 'n')
make_attribute_wrapper(MonthEndType, 'normalize', 'normalize')


@lower_constant(MonthBeginType)
@lower_constant(MonthEndType)
def lower_constant_month_end(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    return lir.Constant.literal_struct([n, normalize])


@register_jitable
def calculate_month_end_date(year, month, day, n):
    if n > 0:
        hllco__mbnu = get_days_in_month(year, month)
        if hllco__mbnu > day:
            n -= 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = get_days_in_month(year, month)
    return year, month, day


def overload_add_operator_month_end_offset_type(lhs, rhs):
    if lhs == month_end_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_end_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond)
        return impl
    if lhs == month_end_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == month_end_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_mul_date_offset_types(lhs, rhs):
    if lhs == month_begin_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthBegin(lhs.n * rhs, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthEnd(lhs.n * rhs, lhs.normalize)
    if lhs == week_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.Week(lhs.n * rhs, lhs.normalize, lhs.
                weekday)
    if lhs == date_offset_type:

        def impl(lhs, rhs):
            n = lhs.n * rhs
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    if rhs in [week_type, month_end_type, month_begin_type, date_offset_type]:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl
    return impl


class DateOffsetType(types.Type):

    def __init__(self):
        super(DateOffsetType, self).__init__(name='DateOffsetType()')


date_offset_type = DateOffsetType()
date_offset_fields = ['years', 'months', 'weeks', 'days', 'hours',
    'minutes', 'seconds', 'microseconds', 'nanoseconds', 'year', 'month',
    'day', 'weekday', 'hour', 'minute', 'second', 'microsecond', 'nanosecond']


@typeof_impl.register(pd.tseries.offsets.DateOffset)
def type_of_date_offset(val, c):
    return date_offset_type


@register_model(DateOffsetType)
class DateOffsetModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        htpc__unj = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, htpc__unj)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    grveh__jlhj = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    yphuw__inu = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for fxg__gskxb, dwste__rlb in enumerate(date_offset_fields):
        c.builder.store(getattr(grveh__jlhj, dwste__rlb), c.builder.
            inttoptr(c.builder.add(c.builder.ptrtoint(yphuw__inu, lir.
            IntType(64)), lir.Constant(lir.IntType(64), 8 * fxg__gskxb)),
            lir.IntType(64).as_pointer()))
    btkff__bsq = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    ljvwc__cbudc = cgutils.get_or_insert_function(c.builder.module,
        btkff__bsq, name='box_date_offset')
    shjvh__acvv = c.builder.call(ljvwc__cbudc, [grveh__jlhj.n, grveh__jlhj.
        normalize, yphuw__inu, grveh__jlhj.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return shjvh__acvv


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    asx__xvvru = c.pyapi.object_getattr_string(val, 'n')
    wuqvx__pqdvz = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(asx__xvvru)
    normalize = c.pyapi.to_native_value(types.bool_, wuqvx__pqdvz).value
    yphuw__inu = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    btkff__bsq = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    tpkhj__abp = cgutils.get_or_insert_function(c.builder.module,
        btkff__bsq, name='unbox_date_offset')
    has_kws = c.builder.call(tpkhj__abp, [val, yphuw__inu])
    grveh__jlhj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    grveh__jlhj.n = n
    grveh__jlhj.normalize = normalize
    for fxg__gskxb, dwste__rlb in enumerate(date_offset_fields):
        setattr(grveh__jlhj, dwste__rlb, c.builder.load(c.builder.inttoptr(
            c.builder.add(c.builder.ptrtoint(yphuw__inu, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * fxg__gskxb)), lir.IntType(64)
            .as_pointer())))
    grveh__jlhj.has_kws = has_kws
    c.pyapi.decref(asx__xvvru)
    c.pyapi.decref(wuqvx__pqdvz)
    ihvxi__wbwvf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(grveh__jlhj._getvalue(), is_error=ihvxi__wbwvf)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    rsty__ayna = [n, normalize]
    has_kws = False
    lmt__euw = [0] * 9 + [-1] * 9
    for fxg__gskxb, dwste__rlb in enumerate(date_offset_fields):
        if hasattr(pyval, dwste__rlb):
            zxtvp__ykl = context.get_constant(types.int64, getattr(pyval,
                dwste__rlb))
            has_kws = True
        else:
            zxtvp__ykl = context.get_constant(types.int64, lmt__euw[fxg__gskxb]
                )
        rsty__ayna.append(zxtvp__ykl)
    has_kws = context.get_constant(types.boolean, has_kws)
    rsty__ayna.append(has_kws)
    return lir.Constant.literal_struct(rsty__ayna)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    zij__fmr = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for drk__xqnq in zij__fmr:
        if not is_overload_none(drk__xqnq):
            has_kws = True
            break

    def impl(n=1, normalize=False, years=None, months=None, weeks=None,
        days=None, hours=None, minutes=None, seconds=None, microseconds=
        None, nanoseconds=None, year=None, month=None, day=None, weekday=
        None, hour=None, minute=None, second=None, microsecond=None,
        nanosecond=None):
        years = 0 if years is None else years
        months = 0 if months is None else months
        weeks = 0 if weeks is None else weeks
        days = 0 if days is None else days
        hours = 0 if hours is None else hours
        minutes = 0 if minutes is None else minutes
        seconds = 0 if seconds is None else seconds
        microseconds = 0 if microseconds is None else microseconds
        nanoseconds = 0 if nanoseconds is None else nanoseconds
        year = -1 if year is None else year
        month = -1 if month is None else month
        weekday = -1 if weekday is None else weekday
        day = -1 if day is None else day
        hour = -1 if hour is None else hour
        minute = -1 if minute is None else minute
        second = -1 if second is None else second
        microsecond = -1 if microsecond is None else microsecond
        nanosecond = -1 if nanosecond is None else nanosecond
        return init_date_offset(n, normalize, years, months, weeks, days,
            hours, minutes, seconds, microseconds, nanoseconds, year, month,
            day, weekday, hour, minute, second, microsecond, nanosecond,
            has_kws)
    return impl


@intrinsic
def init_date_offset(typingctx, n, normalize, years, months, weeks, days,
    hours, minutes, seconds, microseconds, nanoseconds, year, month, day,
    weekday, hour, minute, second, microsecond, nanosecond, has_kws):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        grveh__jlhj = cgutils.create_struct_proxy(typ)(context, builder)
        grveh__jlhj.n = args[0]
        grveh__jlhj.normalize = args[1]
        grveh__jlhj.years = args[2]
        grveh__jlhj.months = args[3]
        grveh__jlhj.weeks = args[4]
        grveh__jlhj.days = args[5]
        grveh__jlhj.hours = args[6]
        grveh__jlhj.minutes = args[7]
        grveh__jlhj.seconds = args[8]
        grveh__jlhj.microseconds = args[9]
        grveh__jlhj.nanoseconds = args[10]
        grveh__jlhj.year = args[11]
        grveh__jlhj.month = args[12]
        grveh__jlhj.day = args[13]
        grveh__jlhj.weekday = args[14]
        grveh__jlhj.hour = args[15]
        grveh__jlhj.minute = args[16]
        grveh__jlhj.second = args[17]
        grveh__jlhj.microsecond = args[18]
        grveh__jlhj.nanosecond = args[19]
        grveh__jlhj.has_kws = args[20]
        return grveh__jlhj._getvalue()
    return DateOffsetType()(n, normalize, years, months, weeks, days, hours,
        minutes, seconds, microseconds, nanoseconds, year, month, day,
        weekday, hour, minute, second, microsecond, nanosecond, has_kws
        ), codegen


make_attribute_wrapper(DateOffsetType, 'n', 'n')
make_attribute_wrapper(DateOffsetType, 'normalize', 'normalize')
make_attribute_wrapper(DateOffsetType, 'years', '_years')
make_attribute_wrapper(DateOffsetType, 'months', '_months')
make_attribute_wrapper(DateOffsetType, 'weeks', '_weeks')
make_attribute_wrapper(DateOffsetType, 'days', '_days')
make_attribute_wrapper(DateOffsetType, 'hours', '_hours')
make_attribute_wrapper(DateOffsetType, 'minutes', '_minutes')
make_attribute_wrapper(DateOffsetType, 'seconds', '_seconds')
make_attribute_wrapper(DateOffsetType, 'microseconds', '_microseconds')
make_attribute_wrapper(DateOffsetType, 'nanoseconds', '_nanoseconds')
make_attribute_wrapper(DateOffsetType, 'year', '_year')
make_attribute_wrapper(DateOffsetType, 'month', '_month')
make_attribute_wrapper(DateOffsetType, 'weekday', '_weekday')
make_attribute_wrapper(DateOffsetType, 'day', '_day')
make_attribute_wrapper(DateOffsetType, 'hour', '_hour')
make_attribute_wrapper(DateOffsetType, 'minute', '_minute')
make_attribute_wrapper(DateOffsetType, 'second', '_second')
make_attribute_wrapper(DateOffsetType, 'microsecond', '_microsecond')
make_attribute_wrapper(DateOffsetType, 'nanosecond', '_nanosecond')
make_attribute_wrapper(DateOffsetType, 'has_kws', '_has_kws')


@register_jitable
def relative_delta_addition(dateoffset, ts):
    if dateoffset._has_kws:
        jco__vcuj = -1 if dateoffset.n < 0 else 1
        for dhxvn__fwd in range(np.abs(dateoffset.n)):
            year = ts.year
            month = ts.month
            day = ts.day
            hour = ts.hour
            minute = ts.minute
            second = ts.second
            microsecond = ts.microsecond
            nanosecond = ts.nanosecond
            if dateoffset._year != -1:
                year = dateoffset._year
            year += jco__vcuj * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += jco__vcuj * dateoffset._months
            year, month, zyz__yng = calculate_month_end_date(year, month,
                day, 0)
            if day > zyz__yng:
                day = zyz__yng
            if dateoffset._day != -1:
                day = dateoffset._day
            if dateoffset._hour != -1:
                hour = dateoffset._hour
            if dateoffset._minute != -1:
                minute = dateoffset._minute
            if dateoffset._second != -1:
                second = dateoffset._second
            if dateoffset._microsecond != -1:
                microsecond = dateoffset._microsecond
            if dateoffset._nanosecond != -1:
                nanosecond = dateoffset._nanosecond
            ts = pd.Timestamp(year=year, month=month, day=day, hour=hour,
                minute=minute, second=second, microsecond=microsecond,
                nanosecond=nanosecond)
            khdci__fqfa = pd.Timedelta(days=dateoffset._days + 7 *
                dateoffset._weeks, hours=dateoffset._hours, minutes=
                dateoffset._minutes, seconds=dateoffset._seconds,
                microseconds=dateoffset._microseconds)
            khdci__fqfa = khdci__fqfa + pd.Timedelta(dateoffset.
                _nanoseconds, unit='ns')
            if jco__vcuj == -1:
                khdci__fqfa = -khdci__fqfa
            ts = ts + khdci__fqfa
            if dateoffset._weekday != -1:
                xoxv__glf = ts.weekday()
                ergns__ygze = (dateoffset._weekday - xoxv__glf) % 7
                ts = ts + pd.Timedelta(days=ergns__ygze)
        return ts
    else:
        return pd.Timedelta(days=dateoffset.n) + ts


def overload_add_operator_date_offset_type(lhs, rhs):
    if lhs == date_offset_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, rhs)
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs == date_offset_type and rhs in [datetime_date_type,
        datetime_datetime_type]:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, pd.Timestamp(rhs))
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == date_offset_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_sub_operator_offsets(lhs, rhs):
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs in [date_offset_type, month_begin_type, month_end_type,
        week_type]:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


@overload(operator.neg, no_unliteral=True)
def overload_neg(lhs):
    if lhs == month_begin_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthBegin(-lhs.n, lhs.normalize)
    elif lhs == month_end_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthEnd(-lhs.n, lhs.normalize)
    elif lhs == week_type:

        def impl(lhs):
            return pd.tseries.offsets.Week(-lhs.n, lhs.normalize, lhs.weekday)
    elif lhs == date_offset_type:

        def impl(lhs):
            n = -lhs.n
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    else:
        return
    return impl


def is_offsets_type(val):
    return val in [date_offset_type, month_begin_type, month_end_type,
        week_type]


class WeekType(types.Type):

    def __init__(self):
        super(WeekType, self).__init__(name='WeekType()')


week_type = WeekType()


@typeof_impl.register(pd.tseries.offsets.Week)
def typeof_week(val, c):
    return week_type


@register_model(WeekType)
class WeekModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        htpc__unj = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, htpc__unj)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        kdx__pcffd = -1 if weekday is None else weekday
        return init_week(n, normalize, kdx__pcffd)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        qeedq__ehkpv = cgutils.create_struct_proxy(typ)(context, builder)
        qeedq__ehkpv.n = args[0]
        qeedq__ehkpv.normalize = args[1]
        qeedq__ehkpv.weekday = args[2]
        return qeedq__ehkpv._getvalue()
    return WeekType()(n, normalize, weekday), codegen


@lower_constant(WeekType)
def lower_constant_week(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    if pyval.weekday is not None:
        weekday = context.get_constant(types.int64, pyval.weekday)
    else:
        weekday = context.get_constant(types.int64, -1)
    return lir.Constant.literal_struct([n, normalize, weekday])


@box(WeekType)
def box_week(typ, val, c):
    qeedq__ehkpv = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    asx__xvvru = c.pyapi.long_from_longlong(qeedq__ehkpv.n)
    wuqvx__pqdvz = c.pyapi.from_native_value(types.boolean, qeedq__ehkpv.
        normalize, c.env_manager)
    ralv__ucula = c.pyapi.long_from_longlong(qeedq__ehkpv.weekday)
    uodqx__tfcmp = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    nhh__ryc = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -1
        ), qeedq__ehkpv.weekday)
    with c.builder.if_else(nhh__ryc) as (irts__unw, lpt__nrbys):
        with irts__unw:
            syduu__meslf = c.pyapi.call_function_objargs(uodqx__tfcmp, (
                asx__xvvru, wuqvx__pqdvz, ralv__ucula))
            ngar__aedyd = c.builder.block
        with lpt__nrbys:
            wzv__ghsuo = c.pyapi.call_function_objargs(uodqx__tfcmp, (
                asx__xvvru, wuqvx__pqdvz))
            ijh__viout = c.builder.block
    bjwlf__zqd = c.builder.phi(syduu__meslf.type)
    bjwlf__zqd.add_incoming(syduu__meslf, ngar__aedyd)
    bjwlf__zqd.add_incoming(wzv__ghsuo, ijh__viout)
    c.pyapi.decref(ralv__ucula)
    c.pyapi.decref(asx__xvvru)
    c.pyapi.decref(wuqvx__pqdvz)
    c.pyapi.decref(uodqx__tfcmp)
    return bjwlf__zqd


@unbox(WeekType)
def unbox_week(typ, val, c):
    asx__xvvru = c.pyapi.object_getattr_string(val, 'n')
    wuqvx__pqdvz = c.pyapi.object_getattr_string(val, 'normalize')
    ralv__ucula = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(asx__xvvru)
    normalize = c.pyapi.to_native_value(types.bool_, wuqvx__pqdvz).value
    fnm__tfv = c.pyapi.make_none()
    ocp__lquq = c.builder.icmp_unsigned('==', ralv__ucula, fnm__tfv)
    with c.builder.if_else(ocp__lquq) as (lpt__nrbys, irts__unw):
        with irts__unw:
            syduu__meslf = c.pyapi.long_as_longlong(ralv__ucula)
            ngar__aedyd = c.builder.block
        with lpt__nrbys:
            wzv__ghsuo = lir.Constant(lir.IntType(64), -1)
            ijh__viout = c.builder.block
    bjwlf__zqd = c.builder.phi(syduu__meslf.type)
    bjwlf__zqd.add_incoming(syduu__meslf, ngar__aedyd)
    bjwlf__zqd.add_incoming(wzv__ghsuo, ijh__viout)
    qeedq__ehkpv = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qeedq__ehkpv.n = n
    qeedq__ehkpv.normalize = normalize
    qeedq__ehkpv.weekday = bjwlf__zqd
    c.pyapi.decref(asx__xvvru)
    c.pyapi.decref(wuqvx__pqdvz)
    c.pyapi.decref(ralv__ucula)
    ihvxi__wbwvf = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qeedq__ehkpv._getvalue(), is_error=ihvxi__wbwvf)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            izb__ahz = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                ypqco__hkt = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                ypqco__hkt = rhs
            return ypqco__hkt + izb__ahz
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            izb__ahz = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                ypqco__hkt = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                ypqco__hkt = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return ypqco__hkt + izb__ahz
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            izb__ahz = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            return rhs + izb__ahz
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ] and rhs == week_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


@register_jitable
def calculate_week_date(n, weekday, other_weekday):
    if weekday == -1:
        return pd.Timedelta(weeks=n)
    if weekday != other_weekday:
        dplc__gnn = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=dplc__gnn)


date_offset_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
date_offset_unsupported = {'__call__', 'rollback', 'rollforward',
    'is_month_start', 'is_month_end', 'apply', 'apply_index', 'copy',
    'isAnchored', 'onOffset', 'is_anchored', 'is_on_offset',
    'is_quarter_start', 'is_quarter_end', 'is_year_start', 'is_year_end'}
month_end_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_end_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
month_begin_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_begin_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
week_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos', 'rule_code'}
week_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
offsets_unsupported = {pd.tseries.offsets.BusinessDay, pd.tseries.offsets.
    BDay, pd.tseries.offsets.BusinessHour, pd.tseries.offsets.
    CustomBusinessDay, pd.tseries.offsets.CDay, pd.tseries.offsets.
    CustomBusinessHour, pd.tseries.offsets.BusinessMonthEnd, pd.tseries.
    offsets.BMonthEnd, pd.tseries.offsets.BusinessMonthBegin, pd.tseries.
    offsets.BMonthBegin, pd.tseries.offsets.CustomBusinessMonthEnd, pd.
    tseries.offsets.CBMonthEnd, pd.tseries.offsets.CustomBusinessMonthBegin,
    pd.tseries.offsets.CBMonthBegin, pd.tseries.offsets.SemiMonthEnd, pd.
    tseries.offsets.SemiMonthBegin, pd.tseries.offsets.WeekOfMonth, pd.
    tseries.offsets.LastWeekOfMonth, pd.tseries.offsets.BQuarterEnd, pd.
    tseries.offsets.BQuarterBegin, pd.tseries.offsets.QuarterEnd, pd.
    tseries.offsets.QuarterBegin, pd.tseries.offsets.BYearEnd, pd.tseries.
    offsets.BYearBegin, pd.tseries.offsets.YearEnd, pd.tseries.offsets.
    YearBegin, pd.tseries.offsets.FY5253, pd.tseries.offsets.FY5253Quarter,
    pd.tseries.offsets.Easter, pd.tseries.offsets.Tick, pd.tseries.offsets.
    Day, pd.tseries.offsets.Hour, pd.tseries.offsets.Minute, pd.tseries.
    offsets.Second, pd.tseries.offsets.Milli, pd.tseries.offsets.Micro, pd.
    tseries.offsets.Nano}
frequencies_unsupported = {pd.tseries.frequencies.to_offset}


def _install_date_offsets_unsupported():
    for yuaj__brx in date_offset_unsupported_attrs:
        yisii__jaopd = 'pandas.tseries.offsets.DateOffset.' + yuaj__brx
        overload_attribute(DateOffsetType, yuaj__brx)(
            create_unsupported_overload(yisii__jaopd))
    for yuaj__brx in date_offset_unsupported:
        yisii__jaopd = 'pandas.tseries.offsets.DateOffset.' + yuaj__brx
        overload_method(DateOffsetType, yuaj__brx)(create_unsupported_overload
            (yisii__jaopd))


def _install_month_begin_unsupported():
    for yuaj__brx in month_begin_unsupported_attrs:
        yisii__jaopd = 'pandas.tseries.offsets.MonthBegin.' + yuaj__brx
        overload_attribute(MonthBeginType, yuaj__brx)(
            create_unsupported_overload(yisii__jaopd))
    for yuaj__brx in month_begin_unsupported:
        yisii__jaopd = 'pandas.tseries.offsets.MonthBegin.' + yuaj__brx
        overload_method(MonthBeginType, yuaj__brx)(create_unsupported_overload
            (yisii__jaopd))


def _install_month_end_unsupported():
    for yuaj__brx in date_offset_unsupported_attrs:
        yisii__jaopd = 'pandas.tseries.offsets.MonthEnd.' + yuaj__brx
        overload_attribute(MonthEndType, yuaj__brx)(create_unsupported_overload
            (yisii__jaopd))
    for yuaj__brx in date_offset_unsupported:
        yisii__jaopd = 'pandas.tseries.offsets.MonthEnd.' + yuaj__brx
        overload_method(MonthEndType, yuaj__brx)(create_unsupported_overload
            (yisii__jaopd))


def _install_week_unsupported():
    for yuaj__brx in week_unsupported_attrs:
        yisii__jaopd = 'pandas.tseries.offsets.Week.' + yuaj__brx
        overload_attribute(WeekType, yuaj__brx)(create_unsupported_overload
            (yisii__jaopd))
    for yuaj__brx in week_unsupported:
        yisii__jaopd = 'pandas.tseries.offsets.Week.' + yuaj__brx
        overload_method(WeekType, yuaj__brx)(create_unsupported_overload(
            yisii__jaopd))


def _install_offsets_unsupported():
    for zxtvp__ykl in offsets_unsupported:
        yisii__jaopd = 'pandas.tseries.offsets.' + zxtvp__ykl.__name__
        overload(zxtvp__ykl)(create_unsupported_overload(yisii__jaopd))


def _install_frequencies_unsupported():
    for zxtvp__ykl in frequencies_unsupported:
        yisii__jaopd = 'pandas.tseries.frequencies.' + zxtvp__ykl.__name__
        overload(zxtvp__ykl)(create_unsupported_overload(yisii__jaopd))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
