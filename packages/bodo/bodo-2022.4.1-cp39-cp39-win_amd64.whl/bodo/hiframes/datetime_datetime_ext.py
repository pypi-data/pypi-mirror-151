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
        nbzhe__ajh = [('year', types.int64), ('month', types.int64), ('day',
            types.int64), ('hour', types.int64), ('minute', types.int64), (
            'second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, nbzhe__ajh)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    lnam__aclu = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    wvglv__rdqyq = c.pyapi.long_from_longlong(lnam__aclu.year)
    qagxr__boo = c.pyapi.long_from_longlong(lnam__aclu.month)
    rwej__kdq = c.pyapi.long_from_longlong(lnam__aclu.day)
    zir__flmxj = c.pyapi.long_from_longlong(lnam__aclu.hour)
    hqa__rmaum = c.pyapi.long_from_longlong(lnam__aclu.minute)
    gvsyc__oak = c.pyapi.long_from_longlong(lnam__aclu.second)
    olago__bltqt = c.pyapi.long_from_longlong(lnam__aclu.microsecond)
    hrecc__mehne = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        datetime))
    ljkih__kmd = c.pyapi.call_function_objargs(hrecc__mehne, (wvglv__rdqyq,
        qagxr__boo, rwej__kdq, zir__flmxj, hqa__rmaum, gvsyc__oak,
        olago__bltqt))
    c.pyapi.decref(wvglv__rdqyq)
    c.pyapi.decref(qagxr__boo)
    c.pyapi.decref(rwej__kdq)
    c.pyapi.decref(zir__flmxj)
    c.pyapi.decref(hqa__rmaum)
    c.pyapi.decref(gvsyc__oak)
    c.pyapi.decref(olago__bltqt)
    c.pyapi.decref(hrecc__mehne)
    return ljkih__kmd


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    wvglv__rdqyq = c.pyapi.object_getattr_string(val, 'year')
    qagxr__boo = c.pyapi.object_getattr_string(val, 'month')
    rwej__kdq = c.pyapi.object_getattr_string(val, 'day')
    zir__flmxj = c.pyapi.object_getattr_string(val, 'hour')
    hqa__rmaum = c.pyapi.object_getattr_string(val, 'minute')
    gvsyc__oak = c.pyapi.object_getattr_string(val, 'second')
    olago__bltqt = c.pyapi.object_getattr_string(val, 'microsecond')
    lnam__aclu = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lnam__aclu.year = c.pyapi.long_as_longlong(wvglv__rdqyq)
    lnam__aclu.month = c.pyapi.long_as_longlong(qagxr__boo)
    lnam__aclu.day = c.pyapi.long_as_longlong(rwej__kdq)
    lnam__aclu.hour = c.pyapi.long_as_longlong(zir__flmxj)
    lnam__aclu.minute = c.pyapi.long_as_longlong(hqa__rmaum)
    lnam__aclu.second = c.pyapi.long_as_longlong(gvsyc__oak)
    lnam__aclu.microsecond = c.pyapi.long_as_longlong(olago__bltqt)
    c.pyapi.decref(wvglv__rdqyq)
    c.pyapi.decref(qagxr__boo)
    c.pyapi.decref(rwej__kdq)
    c.pyapi.decref(zir__flmxj)
    c.pyapi.decref(hqa__rmaum)
    c.pyapi.decref(gvsyc__oak)
    c.pyapi.decref(olago__bltqt)
    ljqr__fqyn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lnam__aclu._getvalue(), is_error=ljqr__fqyn)


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
        lnam__aclu = cgutils.create_struct_proxy(typ)(context, builder)
        lnam__aclu.year = args[0]
        lnam__aclu.month = args[1]
        lnam__aclu.day = args[2]
        lnam__aclu.hour = args[3]
        lnam__aclu.minute = args[4]
        lnam__aclu.second = args[5]
        lnam__aclu.microsecond = args[6]
        return lnam__aclu._getvalue()
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
                y, rvp__xrqec = lhs.year, rhs.year
                igw__uemey, zjcv__hqqw = lhs.month, rhs.month
                d, pksq__swlrn = lhs.day, rhs.day
                uhir__qbo, ufyqk__ktyyk = lhs.hour, rhs.hour
                xxgq__aql, bzytc__dkc = lhs.minute, rhs.minute
                boyi__hlej, srtk__ozk = lhs.second, rhs.second
                mltn__apb, esqp__qpx = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, igw__uemey, d, uhir__qbo, xxgq__aql,
                    boyi__hlej, mltn__apb), (rvp__xrqec, zjcv__hqqw,
                    pksq__swlrn, ufyqk__ktyyk, bzytc__dkc, srtk__ozk,
                    esqp__qpx)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            nxzcm__uwv = lhs.toordinal()
            haaak__wkket = rhs.toordinal()
            bzftq__wplec = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            crpnv__oua = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            nwd__vov = datetime.timedelta(nxzcm__uwv - haaak__wkket, 
                bzftq__wplec - crpnv__oua, lhs.microsecond - rhs.microsecond)
            return nwd__vov
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    zmli__aewz = context.make_helper(builder, fromty, value=val)
    dfks__kekl = cgutils.as_bool_bit(builder, zmli__aewz.valid)
    with builder.if_else(dfks__kekl) as (zzc__tvl, taj__vyrk):
        with zzc__tvl:
            tic__fphta = context.cast(builder, zmli__aewz.data, fromty.type,
                toty)
            ywfqc__lvyv = builder.block
        with taj__vyrk:
            ite__xgewd = numba.np.npdatetime.NAT
            prpp__leytb = builder.block
    ljkih__kmd = builder.phi(tic__fphta.type)
    ljkih__kmd.add_incoming(tic__fphta, ywfqc__lvyv)
    ljkih__kmd.add_incoming(ite__xgewd, prpp__leytb)
    return ljkih__kmd
