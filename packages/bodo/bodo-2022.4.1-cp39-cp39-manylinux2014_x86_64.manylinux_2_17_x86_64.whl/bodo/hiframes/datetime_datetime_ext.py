import datetime
import numba
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
"""
Implementation is based on
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""


class DatetimeDatetimeType(types.Type):

    def __init__(self):
        super(DatetimeDatetimeType, self).__init__(name=
            'DatetimeDatetimeType()')


datetime_datetime_type = DatetimeDatetimeType()
types.datetime_datetime_type = datetime_datetime_type


@typeof_impl.register(datetime.datetime)
def typeof_datetime_datetime(val, c):
    return datetime_datetime_type


@register_model(DatetimeDatetimeType)
class DatetimeDateTimeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        cddq__jog = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, cddq__jog)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    tjdw__hly = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    vxjiu__pfb = c.pyapi.long_from_longlong(tjdw__hly.year)
    mpbra__ybkgd = c.pyapi.long_from_longlong(tjdw__hly.month)
    udes__xsbdq = c.pyapi.long_from_longlong(tjdw__hly.day)
    jyis__boloy = c.pyapi.long_from_longlong(tjdw__hly.hour)
    zrb__liz = c.pyapi.long_from_longlong(tjdw__hly.minute)
    kmqpe__agutm = c.pyapi.long_from_longlong(tjdw__hly.second)
    lijbu__wkv = c.pyapi.long_from_longlong(tjdw__hly.microsecond)
    ktcst__rgg = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    xsh__ojlyy = c.pyapi.call_function_objargs(ktcst__rgg, (vxjiu__pfb,
        mpbra__ybkgd, udes__xsbdq, jyis__boloy, zrb__liz, kmqpe__agutm,
        lijbu__wkv))
    c.pyapi.decref(vxjiu__pfb)
    c.pyapi.decref(mpbra__ybkgd)
    c.pyapi.decref(udes__xsbdq)
    c.pyapi.decref(jyis__boloy)
    c.pyapi.decref(zrb__liz)
    c.pyapi.decref(kmqpe__agutm)
    c.pyapi.decref(lijbu__wkv)
    c.pyapi.decref(ktcst__rgg)
    return xsh__ojlyy


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    vxjiu__pfb = c.pyapi.object_getattr_string(val, 'year')
    mpbra__ybkgd = c.pyapi.object_getattr_string(val, 'month')
    udes__xsbdq = c.pyapi.object_getattr_string(val, 'day')
    jyis__boloy = c.pyapi.object_getattr_string(val, 'hour')
    zrb__liz = c.pyapi.object_getattr_string(val, 'minute')
    kmqpe__agutm = c.pyapi.object_getattr_string(val, 'second')
    lijbu__wkv = c.pyapi.object_getattr_string(val, 'microsecond')
    tjdw__hly = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    tjdw__hly.year = c.pyapi.long_as_longlong(vxjiu__pfb)
    tjdw__hly.month = c.pyapi.long_as_longlong(mpbra__ybkgd)
    tjdw__hly.day = c.pyapi.long_as_longlong(udes__xsbdq)
    tjdw__hly.hour = c.pyapi.long_as_longlong(jyis__boloy)
    tjdw__hly.minute = c.pyapi.long_as_longlong(zrb__liz)
    tjdw__hly.second = c.pyapi.long_as_longlong(kmqpe__agutm)
    tjdw__hly.microsecond = c.pyapi.long_as_longlong(lijbu__wkv)
    c.pyapi.decref(vxjiu__pfb)
    c.pyapi.decref(mpbra__ybkgd)
    c.pyapi.decref(udes__xsbdq)
    c.pyapi.decref(jyis__boloy)
    c.pyapi.decref(zrb__liz)
    c.pyapi.decref(kmqpe__agutm)
    c.pyapi.decref(lijbu__wkv)
    ssvyw__cfttm = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(tjdw__hly._getvalue(), is_error=ssvyw__cfttm)


@lower_constant(DatetimeDatetimeType)
def constant_datetime(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    return lir.Constant.literal_struct([year, month, day, hour, minute,
        second, microsecond])


@overload(datetime.datetime, no_unliteral=True)
def datetime_datetime(year, month, day, hour=0, minute=0, second=0,
    microsecond=0):

    def impl_datetime(year, month, day, hour=0, minute=0, second=0,
        microsecond=0):
        return init_datetime(year, month, day, hour, minute, second,
            microsecond)
    return impl_datetime


@intrinsic
def init_datetime(typingctx, year, month, day, hour, minute, second,
    microsecond):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        tjdw__hly = cgutils.create_struct_proxy(typ)(context, builder)
        tjdw__hly.year = args[0]
        tjdw__hly.month = args[1]
        tjdw__hly.day = args[2]
        tjdw__hly.hour = args[3]
        tjdw__hly.minute = args[4]
        tjdw__hly.second = args[5]
        tjdw__hly.microsecond = args[6]
        return tjdw__hly._getvalue()
    return DatetimeDatetimeType()(year, month, day, hour, minute, second,
        microsecond), codegen


make_attribute_wrapper(DatetimeDatetimeType, 'year', '_year')
make_attribute_wrapper(DatetimeDatetimeType, 'month', '_month')
make_attribute_wrapper(DatetimeDatetimeType, 'day', '_day')
make_attribute_wrapper(DatetimeDatetimeType, 'hour', '_hour')
make_attribute_wrapper(DatetimeDatetimeType, 'minute', '_minute')
make_attribute_wrapper(DatetimeDatetimeType, 'second', '_second')
make_attribute_wrapper(DatetimeDatetimeType, 'microsecond', '_microsecond')


@overload_attribute(DatetimeDatetimeType, 'year')
def datetime_get_year(dt):

    def impl(dt):
        return dt._year
    return impl


@overload_attribute(DatetimeDatetimeType, 'month')
def datetime_get_month(dt):

    def impl(dt):
        return dt._month
    return impl


@overload_attribute(DatetimeDatetimeType, 'day')
def datetime_get_day(dt):

    def impl(dt):
        return dt._day
    return impl


@overload_attribute(DatetimeDatetimeType, 'hour')
def datetime_get_hour(dt):

    def impl(dt):
        return dt._hour
    return impl


@overload_attribute(DatetimeDatetimeType, 'minute')
def datetime_get_minute(dt):

    def impl(dt):
        return dt._minute
    return impl


@overload_attribute(DatetimeDatetimeType, 'second')
def datetime_get_second(dt):

    def impl(dt):
        return dt._second
    return impl


@overload_attribute(DatetimeDatetimeType, 'microsecond')
def datetime_get_microsecond(dt):

    def impl(dt):
        return dt._microsecond
    return impl


@overload_method(DatetimeDatetimeType, 'date', no_unliteral=True)
def date(dt):

    def impl(dt):
        return datetime.date(dt.year, dt.month, dt.day)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.now()
    return d


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.today()
    return d


@register_jitable
def strptime_impl(date_string, dtformat):
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.strptime(date_string, dtformat)
    return d


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def create_cmp_op_overload(op):

    def overload_datetime_cmp(lhs, rhs):
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

            def impl(lhs, rhs):
                y, txo__kqawd = lhs.year, rhs.year
                qhyy__lcwli, nqa__mbll = lhs.month, rhs.month
                d, xiiat__aesfu = lhs.day, rhs.day
                ihen__hvj, xuf__dtl = lhs.hour, rhs.hour
                pruxp__pdve, qbu__ock = lhs.minute, rhs.minute
                dwd__aqci, vbht__ble = lhs.second, rhs.second
                hmobg__isjr, xsyif__ozr = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, qhyy__lcwli, d, ihen__hvj, pruxp__pdve,
                    dwd__aqci, hmobg__isjr), (txo__kqawd, nqa__mbll,
                    xiiat__aesfu, xuf__dtl, qbu__ock, vbht__ble, xsyif__ozr
                    )), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            hup__cqqly = lhs.toordinal()
            yab__mqoj = rhs.toordinal()
            latac__dny = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            lbiva__lgcu = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            ojda__wuas = datetime.timedelta(hup__cqqly - yab__mqoj, 
                latac__dny - lbiva__lgcu, lhs.microsecond - rhs.microsecond)
            return ojda__wuas
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    lffxh__gwwc = context.make_helper(builder, fromty, value=val)
    kxnw__wcfdd = cgutils.as_bool_bit(builder, lffxh__gwwc.valid)
    with builder.if_else(kxnw__wcfdd) as (gtl__ugvw, oho__gggf):
        with gtl__ugvw:
            wwvlj__qrqbb = context.cast(builder, lffxh__gwwc.data, fromty.
                type, toty)
            hied__mbwn = builder.block
        with oho__gggf:
            oxxl__rknis = numba.np.npdatetime.NAT
            sfz__fhsen = builder.block
    xsh__ojlyy = builder.phi(wwvlj__qrqbb.type)
    xsh__ojlyy.add_incoming(wwvlj__qrqbb, hied__mbwn)
    xsh__ojlyy.add_incoming(oxxl__rknis, sfz__fhsen)
    return xsh__ojlyy
