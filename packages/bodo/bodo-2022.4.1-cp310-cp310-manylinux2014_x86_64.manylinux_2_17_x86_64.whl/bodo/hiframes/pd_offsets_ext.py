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
        xupq__jrldf = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, xupq__jrldf)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    tbk__hpa = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    jqy__slivp = c.pyapi.long_from_longlong(tbk__hpa.n)
    mvor__zmwgv = c.pyapi.from_native_value(types.boolean, tbk__hpa.
        normalize, c.env_manager)
    ttgw__dfx = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    tbxjg__rjedq = c.pyapi.call_function_objargs(ttgw__dfx, (jqy__slivp,
        mvor__zmwgv))
    c.pyapi.decref(jqy__slivp)
    c.pyapi.decref(mvor__zmwgv)
    c.pyapi.decref(ttgw__dfx)
    return tbxjg__rjedq


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    jqy__slivp = c.pyapi.object_getattr_string(val, 'n')
    mvor__zmwgv = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(jqy__slivp)
    normalize = c.pyapi.to_native_value(types.bool_, mvor__zmwgv).value
    tbk__hpa = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    tbk__hpa.n = n
    tbk__hpa.normalize = normalize
    c.pyapi.decref(jqy__slivp)
    c.pyapi.decref(mvor__zmwgv)
    xvf__jwz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(tbk__hpa._getvalue(), is_error=xvf__jwz)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        tbk__hpa = cgutils.create_struct_proxy(typ)(context, builder)
        tbk__hpa.n = args[0]
        tbk__hpa.normalize = args[1]
        return tbk__hpa._getvalue()
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
        xupq__jrldf = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, xupq__jrldf)


@box(MonthEndType)
def box_month_end(typ, val, c):
    krb__fncyl = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jqy__slivp = c.pyapi.long_from_longlong(krb__fncyl.n)
    mvor__zmwgv = c.pyapi.from_native_value(types.boolean, krb__fncyl.
        normalize, c.env_manager)
    ynn__xxozh = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    tbxjg__rjedq = c.pyapi.call_function_objargs(ynn__xxozh, (jqy__slivp,
        mvor__zmwgv))
    c.pyapi.decref(jqy__slivp)
    c.pyapi.decref(mvor__zmwgv)
    c.pyapi.decref(ynn__xxozh)
    return tbxjg__rjedq


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    jqy__slivp = c.pyapi.object_getattr_string(val, 'n')
    mvor__zmwgv = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(jqy__slivp)
    normalize = c.pyapi.to_native_value(types.bool_, mvor__zmwgv).value
    krb__fncyl = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    krb__fncyl.n = n
    krb__fncyl.normalize = normalize
    c.pyapi.decref(jqy__slivp)
    c.pyapi.decref(mvor__zmwgv)
    xvf__jwz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(krb__fncyl._getvalue(), is_error=xvf__jwz)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        krb__fncyl = cgutils.create_struct_proxy(typ)(context, builder)
        krb__fncyl.n = args[0]
        krb__fncyl.normalize = args[1]
        return krb__fncyl._getvalue()
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
        krb__fncyl = get_days_in_month(year, month)
        if krb__fncyl > day:
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
        xupq__jrldf = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, xupq__jrldf)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    bte__mnqm = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    mfspg__rkc = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for nss__fzg, mpja__nsqz in enumerate(date_offset_fields):
        c.builder.store(getattr(bte__mnqm, mpja__nsqz), c.builder.inttoptr(
            c.builder.add(c.builder.ptrtoint(mfspg__rkc, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * nss__fzg)), lir.IntType(64).
            as_pointer()))
    bps__fnlto = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    vxb__vmh = cgutils.get_or_insert_function(c.builder.module, bps__fnlto,
        name='box_date_offset')
    vkn__bpotp = c.builder.call(vxb__vmh, [bte__mnqm.n, bte__mnqm.normalize,
        mfspg__rkc, bte__mnqm.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return vkn__bpotp


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    jqy__slivp = c.pyapi.object_getattr_string(val, 'n')
    mvor__zmwgv = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(jqy__slivp)
    normalize = c.pyapi.to_native_value(types.bool_, mvor__zmwgv).value
    mfspg__rkc = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    bps__fnlto = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer()])
    glgvy__aan = cgutils.get_or_insert_function(c.builder.module,
        bps__fnlto, name='unbox_date_offset')
    has_kws = c.builder.call(glgvy__aan, [val, mfspg__rkc])
    bte__mnqm = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bte__mnqm.n = n
    bte__mnqm.normalize = normalize
    for nss__fzg, mpja__nsqz in enumerate(date_offset_fields):
        setattr(bte__mnqm, mpja__nsqz, c.builder.load(c.builder.inttoptr(c.
            builder.add(c.builder.ptrtoint(mfspg__rkc, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * nss__fzg)), lir.IntType(64).
            as_pointer())))
    bte__mnqm.has_kws = has_kws
    c.pyapi.decref(jqy__slivp)
    c.pyapi.decref(mvor__zmwgv)
    xvf__jwz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bte__mnqm._getvalue(), is_error=xvf__jwz)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    mhhz__ltrm = [n, normalize]
    has_kws = False
    jmz__wltlr = [0] * 9 + [-1] * 9
    for nss__fzg, mpja__nsqz in enumerate(date_offset_fields):
        if hasattr(pyval, mpja__nsqz):
            yaw__dzqq = context.get_constant(types.int64, getattr(pyval,
                mpja__nsqz))
            has_kws = True
        else:
            yaw__dzqq = context.get_constant(types.int64, jmz__wltlr[nss__fzg])
        mhhz__ltrm.append(yaw__dzqq)
    has_kws = context.get_constant(types.boolean, has_kws)
    mhhz__ltrm.append(has_kws)
    return lir.Constant.literal_struct(mhhz__ltrm)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    hmvba__rlp = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for ofibg__tzh in hmvba__rlp:
        if not is_overload_none(ofibg__tzh):
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
        bte__mnqm = cgutils.create_struct_proxy(typ)(context, builder)
        bte__mnqm.n = args[0]
        bte__mnqm.normalize = args[1]
        bte__mnqm.years = args[2]
        bte__mnqm.months = args[3]
        bte__mnqm.weeks = args[4]
        bte__mnqm.days = args[5]
        bte__mnqm.hours = args[6]
        bte__mnqm.minutes = args[7]
        bte__mnqm.seconds = args[8]
        bte__mnqm.microseconds = args[9]
        bte__mnqm.nanoseconds = args[10]
        bte__mnqm.year = args[11]
        bte__mnqm.month = args[12]
        bte__mnqm.day = args[13]
        bte__mnqm.weekday = args[14]
        bte__mnqm.hour = args[15]
        bte__mnqm.minute = args[16]
        bte__mnqm.second = args[17]
        bte__mnqm.microsecond = args[18]
        bte__mnqm.nanosecond = args[19]
        bte__mnqm.has_kws = args[20]
        return bte__mnqm._getvalue()
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
        euypv__iiam = -1 if dateoffset.n < 0 else 1
        for jxcw__ogrgq in range(np.abs(dateoffset.n)):
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
            year += euypv__iiam * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += euypv__iiam * dateoffset._months
            year, month, rvz__nhdqg = calculate_month_end_date(year, month,
                day, 0)
            if day > rvz__nhdqg:
                day = rvz__nhdqg
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
            hstu__cxv = pd.Timedelta(days=dateoffset._days + 7 * dateoffset
                ._weeks, hours=dateoffset._hours, minutes=dateoffset.
                _minutes, seconds=dateoffset._seconds, microseconds=
                dateoffset._microseconds)
            hstu__cxv = hstu__cxv + pd.Timedelta(dateoffset._nanoseconds,
                unit='ns')
            if euypv__iiam == -1:
                hstu__cxv = -hstu__cxv
            ts = ts + hstu__cxv
            if dateoffset._weekday != -1:
                wjs__zvzpu = ts.weekday()
                kqrwc__qgf = (dateoffset._weekday - wjs__zvzpu) % 7
                ts = ts + pd.Timedelta(days=kqrwc__qgf)
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
        xupq__jrldf = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, xupq__jrldf)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        usoj__tgwgb = -1 if weekday is None else weekday
        return init_week(n, normalize, usoj__tgwgb)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        lmghx__shvw = cgutils.create_struct_proxy(typ)(context, builder)
        lmghx__shvw.n = args[0]
        lmghx__shvw.normalize = args[1]
        lmghx__shvw.weekday = args[2]
        return lmghx__shvw._getvalue()
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
    lmghx__shvw = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    jqy__slivp = c.pyapi.long_from_longlong(lmghx__shvw.n)
    mvor__zmwgv = c.pyapi.from_native_value(types.boolean, lmghx__shvw.
        normalize, c.env_manager)
    wgg__nbq = c.pyapi.long_from_longlong(lmghx__shvw.weekday)
    iftgi__hyo = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    dfz__kucu = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), -
        1), lmghx__shvw.weekday)
    with c.builder.if_else(dfz__kucu) as (lhu__tspea, bmdi__ejx):
        with lhu__tspea:
            kvz__lje = c.pyapi.call_function_objargs(iftgi__hyo, (
                jqy__slivp, mvor__zmwgv, wgg__nbq))
            vws__lowl = c.builder.block
        with bmdi__ejx:
            fifw__cqt = c.pyapi.call_function_objargs(iftgi__hyo, (
                jqy__slivp, mvor__zmwgv))
            ecgen__ioa = c.builder.block
    tbxjg__rjedq = c.builder.phi(kvz__lje.type)
    tbxjg__rjedq.add_incoming(kvz__lje, vws__lowl)
    tbxjg__rjedq.add_incoming(fifw__cqt, ecgen__ioa)
    c.pyapi.decref(wgg__nbq)
    c.pyapi.decref(jqy__slivp)
    c.pyapi.decref(mvor__zmwgv)
    c.pyapi.decref(iftgi__hyo)
    return tbxjg__rjedq


@unbox(WeekType)
def unbox_week(typ, val, c):
    jqy__slivp = c.pyapi.object_getattr_string(val, 'n')
    mvor__zmwgv = c.pyapi.object_getattr_string(val, 'normalize')
    wgg__nbq = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(jqy__slivp)
    normalize = c.pyapi.to_native_value(types.bool_, mvor__zmwgv).value
    cwv__pdwhm = c.pyapi.make_none()
    xuqra__kbwi = c.builder.icmp_unsigned('==', wgg__nbq, cwv__pdwhm)
    with c.builder.if_else(xuqra__kbwi) as (bmdi__ejx, lhu__tspea):
        with lhu__tspea:
            kvz__lje = c.pyapi.long_as_longlong(wgg__nbq)
            vws__lowl = c.builder.block
        with bmdi__ejx:
            fifw__cqt = lir.Constant(lir.IntType(64), -1)
            ecgen__ioa = c.builder.block
    tbxjg__rjedq = c.builder.phi(kvz__lje.type)
    tbxjg__rjedq.add_incoming(kvz__lje, vws__lowl)
    tbxjg__rjedq.add_incoming(fifw__cqt, ecgen__ioa)
    lmghx__shvw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lmghx__shvw.n = n
    lmghx__shvw.normalize = normalize
    lmghx__shvw.weekday = tbxjg__rjedq
    c.pyapi.decref(jqy__slivp)
    c.pyapi.decref(mvor__zmwgv)
    c.pyapi.decref(wgg__nbq)
    xvf__jwz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lmghx__shvw._getvalue(), is_error=xvf__jwz)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and rhs == pd_timestamp_type:

        def impl(lhs, rhs):
            ovc__tnnl = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                spx__uzfx = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                spx__uzfx = rhs
            return spx__uzfx + ovc__tnnl
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            ovc__tnnl = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            if lhs.normalize:
                spx__uzfx = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day)
            else:
                spx__uzfx = pd.Timestamp(year=rhs.year, month=rhs.month,
                    day=rhs.day, hour=rhs.hour, minute=rhs.minute, second=
                    rhs.second, microsecond=rhs.microsecond)
            return spx__uzfx + ovc__tnnl
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            ovc__tnnl = calculate_week_date(lhs.n, lhs.weekday, rhs.weekday())
            return rhs + ovc__tnnl
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
        tky__mbj = (weekday - other_weekday) % 7
        if n > 0:
            n = n - 1
    return pd.Timedelta(weeks=n, days=tky__mbj)


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
    for fuqz__gowz in date_offset_unsupported_attrs:
        uzro__ysni = 'pandas.tseries.offsets.DateOffset.' + fuqz__gowz
        overload_attribute(DateOffsetType, fuqz__gowz)(
            create_unsupported_overload(uzro__ysni))
    for fuqz__gowz in date_offset_unsupported:
        uzro__ysni = 'pandas.tseries.offsets.DateOffset.' + fuqz__gowz
        overload_method(DateOffsetType, fuqz__gowz)(create_unsupported_overload
            (uzro__ysni))


def _install_month_begin_unsupported():
    for fuqz__gowz in month_begin_unsupported_attrs:
        uzro__ysni = 'pandas.tseries.offsets.MonthBegin.' + fuqz__gowz
        overload_attribute(MonthBeginType, fuqz__gowz)(
            create_unsupported_overload(uzro__ysni))
    for fuqz__gowz in month_begin_unsupported:
        uzro__ysni = 'pandas.tseries.offsets.MonthBegin.' + fuqz__gowz
        overload_method(MonthBeginType, fuqz__gowz)(create_unsupported_overload
            (uzro__ysni))


def _install_month_end_unsupported():
    for fuqz__gowz in date_offset_unsupported_attrs:
        uzro__ysni = 'pandas.tseries.offsets.MonthEnd.' + fuqz__gowz
        overload_attribute(MonthEndType, fuqz__gowz)(
            create_unsupported_overload(uzro__ysni))
    for fuqz__gowz in date_offset_unsupported:
        uzro__ysni = 'pandas.tseries.offsets.MonthEnd.' + fuqz__gowz
        overload_method(MonthEndType, fuqz__gowz)(create_unsupported_overload
            (uzro__ysni))


def _install_week_unsupported():
    for fuqz__gowz in week_unsupported_attrs:
        uzro__ysni = 'pandas.tseries.offsets.Week.' + fuqz__gowz
        overload_attribute(WeekType, fuqz__gowz)(create_unsupported_overload
            (uzro__ysni))
    for fuqz__gowz in week_unsupported:
        uzro__ysni = 'pandas.tseries.offsets.Week.' + fuqz__gowz
        overload_method(WeekType, fuqz__gowz)(create_unsupported_overload(
            uzro__ysni))


def _install_offsets_unsupported():
    for yaw__dzqq in offsets_unsupported:
        uzro__ysni = 'pandas.tseries.offsets.' + yaw__dzqq.__name__
        overload(yaw__dzqq)(create_unsupported_overload(uzro__ysni))


def _install_frequencies_unsupported():
    for yaw__dzqq in frequencies_unsupported:
        uzro__ysni = 'pandas.tseries.frequencies.' + yaw__dzqq.__name__
        overload(yaw__dzqq)(create_unsupported_overload(uzro__ysni))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
