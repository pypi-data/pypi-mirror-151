"""Numba extension support for datetime.timedelta objects and their arrays.
"""
import datetime
import operator
from collections import namedtuple
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import get_new_null_mask_bool_index, get_new_null_mask_int_index, get_new_null_mask_slice_index, setitem_slice_index_null_bits
from bodo.utils.typing import BodoError, get_overload_const_str, is_iterable_type, is_list_like_index_type, is_overload_constant_str
ll.add_symbol('box_datetime_timedelta_array', hdatetime_ext.
    box_datetime_timedelta_array)
ll.add_symbol('unbox_datetime_timedelta_array', hdatetime_ext.
    unbox_datetime_timedelta_array)


class NoInput:
    pass


_no_input = NoInput()


class NoInputType(types.Type):

    def __init__(self):
        super(NoInputType, self).__init__(name='NoInput')


register_model(NoInputType)(models.OpaqueModel)


@typeof_impl.register(NoInput)
def _typ_no_input(val, c):
    return NoInputType()


@lower_constant(NoInputType)
def constant_no_input(context, builder, ty, pyval):
    return context.get_dummy_value()


class PDTimeDeltaType(types.Type):

    def __init__(self):
        super(PDTimeDeltaType, self).__init__(name='PDTimeDeltaType()')


pd_timedelta_type = PDTimeDeltaType()
types.pd_timedelta_type = pd_timedelta_type


@typeof_impl.register(pd.Timedelta)
def typeof_pd_timedelta(val, c):
    return pd_timedelta_type


@register_model(PDTimeDeltaType)
class PDTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pqwta__rep = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, pqwta__rep)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    suad__dcoe = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    sno__sqjv = c.pyapi.long_from_longlong(suad__dcoe.value)
    unnyg__ynvv = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(unnyg__ynvv, (sno__sqjv,))
    c.pyapi.decref(sno__sqjv)
    c.pyapi.decref(unnyg__ynvv)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    sno__sqjv = c.pyapi.object_getattr_string(val, 'value')
    tdf__vnzx = c.pyapi.long_as_longlong(sno__sqjv)
    suad__dcoe = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    suad__dcoe.value = tdf__vnzx
    c.pyapi.decref(sno__sqjv)
    cqv__clymc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(suad__dcoe._getvalue(), is_error=cqv__clymc)


@lower_constant(PDTimeDeltaType)
def lower_constant_pd_timedelta(context, builder, ty, pyval):
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct([value])


@overload(pd.Timedelta, no_unliteral=True)
def pd_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
    microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    if value == _no_input:

        def impl_timedelta_kw(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            days += weeks * 7
            hours += days * 24
            minutes += 60 * hours
            seconds += 60 * minutes
            milliseconds += 1000 * seconds
            microseconds += 1000 * milliseconds
            qusm__ska = 1000 * microseconds
            return init_pd_timedelta(qusm__ska)
        return impl_timedelta_kw
    if value == bodo.string_type or is_overload_constant_str(value):

        def impl_str(value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
            with numba.objmode(res='pd_timedelta_type'):
                res = pd.Timedelta(value)
            return res
        return impl_str
    if value == pd_timedelta_type:
        return (lambda value=_no_input, unit='ns', days=0, seconds=0,
            microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0: value)
    if value == datetime_timedelta_type:

        def impl_timedelta_datetime(value=_no_input, unit='ns', days=0,
            seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0,
            weeks=0):
            days = value.days
            seconds = 60 * 60 * 24 * days + value.seconds
            microseconds = 1000 * 1000 * seconds + value.microseconds
            qusm__ska = 1000 * microseconds
            return init_pd_timedelta(qusm__ska)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    crlo__howj, xeq__cgofa = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * crlo__howj)
    return impl_timedelta


@intrinsic
def init_pd_timedelta(typingctx, value):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.value = args[0]
        return timedelta._getvalue()
    return PDTimeDeltaType()(value), codegen


make_attribute_wrapper(PDTimeDeltaType, 'value', '_value')


@overload_attribute(PDTimeDeltaType, 'value')
@overload_attribute(PDTimeDeltaType, 'delta')
def pd_timedelta_get_value(td):

    def impl(td):
        return td._value
    return impl


@overload_attribute(PDTimeDeltaType, 'days')
def pd_timedelta_get_days(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000 * 60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'seconds')
def pd_timedelta_get_seconds(td):

    def impl(td):
        return td._value // (1000 * 1000 * 1000) % (60 * 60 * 24)
    return impl


@overload_attribute(PDTimeDeltaType, 'microseconds')
def pd_timedelta_get_microseconds(td):

    def impl(td):
        return td._value // 1000 % 1000000
    return impl


@overload_attribute(PDTimeDeltaType, 'nanoseconds')
def pd_timedelta_get_nanoseconds(td):

    def impl(td):
        return td._value % 1000
    return impl


@register_jitable
def _to_hours_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60 * 60) % 24


@register_jitable
def _to_minutes_pd_td(td):
    return td._value // (1000 * 1000 * 1000 * 60) % 60


@register_jitable
def _to_seconds_pd_td(td):
    return td._value // (1000 * 1000 * 1000) % 60


@register_jitable
def _to_milliseconds_pd_td(td):
    return td._value // (1000 * 1000) % 1000


@register_jitable
def _to_microseconds_pd_td(td):
    return td._value // 1000 % 1000


Components = namedtuple('Components', ['days', 'hours', 'minutes',
    'seconds', 'milliseconds', 'microseconds', 'nanoseconds'], defaults=[0,
    0, 0, 0, 0, 0, 0])


@overload_attribute(PDTimeDeltaType, 'components', no_unliteral=True)
def pd_timedelta_get_components(td):

    def impl(td):
        a = Components(td.days, _to_hours_pd_td(td), _to_minutes_pd_td(td),
            _to_seconds_pd_td(td), _to_milliseconds_pd_td(td),
            _to_microseconds_pd_td(td), td.nanoseconds)
        return a
    return impl


@overload_method(PDTimeDeltaType, '__hash__', no_unliteral=True)
def pd_td___hash__(td):

    def impl(td):
        return hash(td._value)
    return impl


@overload_method(PDTimeDeltaType, 'to_numpy', no_unliteral=True)
@overload_method(PDTimeDeltaType, 'to_timedelta64', no_unliteral=True)
def pd_td_to_numpy(td):
    from bodo.hiframes.pd_timestamp_ext import integer_to_timedelta64

    def impl(td):
        return integer_to_timedelta64(td.value)
    return impl


@overload_method(PDTimeDeltaType, 'to_pytimedelta', no_unliteral=True)
def pd_td_to_pytimedelta(td):

    def impl(td):
        return datetime.timedelta(microseconds=np.int64(td._value / 1000))
    return impl


@overload_method(PDTimeDeltaType, 'total_seconds', no_unliteral=True)
def pd_td_total_seconds(td):

    def impl(td):
        return td._value // 1000 / 10 ** 6
    return impl


def overload_add_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            val = lhs.value + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            dskmr__lut = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + dskmr__lut
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            ppv__syu = (lhs.microseconds + (lhs.seconds + lhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = ppv__syu + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            hmvg__lnqv = rhs.toordinal()
            dld__nwh = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            guy__hxj = rhs.microsecond
            ebr__sdha = lhs.value // 1000
            tctj__rqcc = lhs.nanoseconds
            kahyr__ewdwh = guy__hxj + ebr__sdha
            lxqnb__krrp = 1000000 * (hmvg__lnqv * 86400 + dld__nwh
                ) + kahyr__ewdwh
            mywaa__xjepk = tctj__rqcc
            return compute_pd_timestamp(lxqnb__krrp, mywaa__xjepk)
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + rhs.to_pytimedelta()
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days + rhs.days
            s = lhs.seconds + rhs.seconds
            us = lhs.microseconds + rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            zwdvw__stch = datetime.timedelta(rhs.toordinal(), hours=rhs.
                hour, minutes=rhs.minute, seconds=rhs.second, microseconds=
                rhs.microsecond)
            zwdvw__stch = zwdvw__stch + lhs
            eriab__qct, vrnp__bqst = divmod(zwdvw__stch.seconds, 3600)
            hdvlz__afgp, aft__cval = divmod(vrnp__bqst, 60)
            if 0 < zwdvw__stch.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(
                    zwdvw__stch.days)
                return datetime.datetime(d.year, d.month, d.day, eriab__qct,
                    hdvlz__afgp, aft__cval, zwdvw__stch.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            zwdvw__stch = datetime.timedelta(lhs.toordinal(), hours=lhs.
                hour, minutes=lhs.minute, seconds=lhs.second, microseconds=
                lhs.microsecond)
            zwdvw__stch = zwdvw__stch + rhs
            eriab__qct, vrnp__bqst = divmod(zwdvw__stch.seconds, 3600)
            hdvlz__afgp, aft__cval = divmod(vrnp__bqst, 60)
            if 0 < zwdvw__stch.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(
                    zwdvw__stch.days)
                return datetime.datetime(d.year, d.month, d.day, eriab__qct,
                    hdvlz__afgp, aft__cval, zwdvw__stch.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            moyo__aemiu = lhs.value - rhs.value
            return pd.Timedelta(moyo__aemiu)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_datetime_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs.days - rhs.days
            s = lhs.seconds - rhs.seconds
            us = lhs.microseconds - rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl
    if lhs == datetime_timedelta_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            wki__dqcsn = lhs
            numba.parfors.parfor.init_prange()
            n = len(wki__dqcsn)
            A = alloc_datetime_timedelta_array(n)
            for wzswy__kvs in numba.parfors.parfor.internal_prange(n):
                A[wzswy__kvs] = wki__dqcsn[wzswy__kvs] - rhs
            return A
        return impl


def overload_mul_operator_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value * rhs)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(rhs.value * lhs)
        return impl
    if lhs == datetime_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            d = lhs.days * rhs
            s = lhs.seconds * rhs
            us = lhs.microseconds * rhs
            return datetime.timedelta(d, s, us)
        return impl
    elif isinstance(lhs, types.Integer) and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            d = lhs * rhs.days
            s = lhs * rhs.seconds
            us = lhs * rhs.microseconds
            return datetime.timedelta(d, s, us)
        return impl


def overload_floordiv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value // rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value // rhs)
        return impl


def overload_truediv_operator_pd_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs.value / rhs.value
        return impl
    elif lhs == pd_timedelta_type and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            return pd.Timedelta(int(lhs.value / rhs))
        return impl


def overload_mod_operator_timedeltas(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return pd.Timedelta(lhs.value % rhs.value)
        return impl
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            qqptq__fmld = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, qqptq__fmld)
        return impl


def pd_create_cmp_op_overload(op):

    def overload_pd_timedelta_cmp(lhs, rhs):
        if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

            def impl(lhs, rhs):
                return op(lhs.value, rhs.value)
            return impl
        if lhs == pd_timedelta_type and rhs == bodo.timedelta64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(lhs.value), rhs)
        if lhs == bodo.timedelta64ns and rhs == pd_timedelta_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_timedelta64(rhs.value))
    return overload_pd_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def pd_timedelta_neg(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return pd.Timedelta(-lhs.value)
        return impl


@overload(operator.pos, no_unliteral=True)
def pd_timedelta_pos(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def pd_timedelta_divmod(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            uilyu__ezqy, qqptq__fmld = divmod(lhs.value, rhs.value)
            return uilyu__ezqy, pd.Timedelta(qqptq__fmld)
        return impl


@overload(abs, no_unliteral=True)
def pd_timedelta_abs(lhs):
    if lhs == pd_timedelta_type:

        def impl(lhs):
            if lhs.value < 0:
                return -lhs
            else:
                return lhs
        return impl


class DatetimeTimeDeltaType(types.Type):

    def __init__(self):
        super(DatetimeTimeDeltaType, self).__init__(name=
            'DatetimeTimeDeltaType()')


datetime_timedelta_type = DatetimeTimeDeltaType()


@typeof_impl.register(datetime.timedelta)
def typeof_datetime_timedelta(val, c):
    return datetime_timedelta_type


@register_model(DatetimeTimeDeltaType)
class DatetimeTimeDeltaModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pqwta__rep = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, pqwta__rep)


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    suad__dcoe = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    djibx__hlng = c.pyapi.long_from_longlong(suad__dcoe.days)
    ntppq__tlvu = c.pyapi.long_from_longlong(suad__dcoe.seconds)
    egsv__smlob = c.pyapi.long_from_longlong(suad__dcoe.microseconds)
    unnyg__ynvv = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(unnyg__ynvv, (djibx__hlng,
        ntppq__tlvu, egsv__smlob))
    c.pyapi.decref(djibx__hlng)
    c.pyapi.decref(ntppq__tlvu)
    c.pyapi.decref(egsv__smlob)
    c.pyapi.decref(unnyg__ynvv)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    djibx__hlng = c.pyapi.object_getattr_string(val, 'days')
    ntppq__tlvu = c.pyapi.object_getattr_string(val, 'seconds')
    egsv__smlob = c.pyapi.object_getattr_string(val, 'microseconds')
    mvdr__asdbl = c.pyapi.long_as_longlong(djibx__hlng)
    wvbu__mqebm = c.pyapi.long_as_longlong(ntppq__tlvu)
    igdbc__lgirh = c.pyapi.long_as_longlong(egsv__smlob)
    suad__dcoe = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    suad__dcoe.days = mvdr__asdbl
    suad__dcoe.seconds = wvbu__mqebm
    suad__dcoe.microseconds = igdbc__lgirh
    c.pyapi.decref(djibx__hlng)
    c.pyapi.decref(ntppq__tlvu)
    c.pyapi.decref(egsv__smlob)
    cqv__clymc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(suad__dcoe._getvalue(), is_error=cqv__clymc)


@lower_constant(DatetimeTimeDeltaType)
def lower_constant_datetime_timedelta(context, builder, ty, pyval):
    days = context.get_constant(types.int64, pyval.days)
    seconds = context.get_constant(types.int64, pyval.seconds)
    microseconds = context.get_constant(types.int64, pyval.microseconds)
    return lir.Constant.literal_struct([days, seconds, microseconds])


@overload(datetime.timedelta, no_unliteral=True)
def datetime_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
    minutes=0, hours=0, weeks=0):

    def impl_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0,
        minutes=0, hours=0, weeks=0):
        d = s = us = 0
        days += weeks * 7
        seconds += minutes * 60 + hours * 3600
        microseconds += milliseconds * 1000
        d = days
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += int(seconds)
        seconds, us = divmod(microseconds, 1000000)
        days, seconds = divmod(seconds, 24 * 3600)
        d += days
        s += seconds
        return init_timedelta(d, s, us)
    return impl_timedelta


@intrinsic
def init_timedelta(typingctx, d, s, us):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        timedelta = cgutils.create_struct_proxy(typ)(context, builder)
        timedelta.days = args[0]
        timedelta.seconds = args[1]
        timedelta.microseconds = args[2]
        return timedelta._getvalue()
    return DatetimeTimeDeltaType()(d, s, us), codegen


make_attribute_wrapper(DatetimeTimeDeltaType, 'days', '_days')
make_attribute_wrapper(DatetimeTimeDeltaType, 'seconds', '_seconds')
make_attribute_wrapper(DatetimeTimeDeltaType, 'microseconds', '_microseconds')


@overload_attribute(DatetimeTimeDeltaType, 'days')
def timedelta_get_days(td):

    def impl(td):
        return td._days
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'seconds')
def timedelta_get_seconds(td):

    def impl(td):
        return td._seconds
    return impl


@overload_attribute(DatetimeTimeDeltaType, 'microseconds')
def timedelta_get_microseconds(td):

    def impl(td):
        return td._microseconds
    return impl


@overload_method(DatetimeTimeDeltaType, 'total_seconds', no_unliteral=True)
def total_seconds(td):

    def impl(td):
        return ((td._days * 86400 + td._seconds) * 10 ** 6 + td._microseconds
            ) / 10 ** 6
    return impl


@overload_method(DatetimeTimeDeltaType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        return hash((td._days, td._seconds, td._microseconds))
    return impl


@register_jitable
def _to_nanoseconds(td):
    return np.int64(((td._days * 86400 + td._seconds) * 1000000 + td.
        _microseconds) * 1000)


@register_jitable
def _to_microseconds(td):
    return (td._days * (24 * 3600) + td._seconds) * 1000000 + td._microseconds


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@register_jitable
def _getstate(td):
    return td._days, td._seconds, td._microseconds


@register_jitable
def _divide_and_round(a, b):
    uilyu__ezqy, qqptq__fmld = divmod(a, b)
    qqptq__fmld *= 2
    rir__vaz = qqptq__fmld > b if b > 0 else qqptq__fmld < b
    if rir__vaz or qqptq__fmld == b and uilyu__ezqy % 2 == 1:
        uilyu__ezqy += 1
    return uilyu__ezqy


_MAXORDINAL = 3652059


def overload_floordiv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us // _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, us // rhs)
        return impl


def overload_truediv_operator_dt_timedelta(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return us / _to_microseconds(rhs)
        return impl
    elif lhs == datetime_timedelta_type and rhs == types.int64:

        def impl(lhs, rhs):
            us = _to_microseconds(lhs)
            return datetime.timedelta(0, 0, _divide_and_round(us, rhs))
        return impl


def create_cmp_op_overload(op):

    def overload_timedelta_cmp(lhs, rhs):
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

            def impl(lhs, rhs):
                mxenf__drzi = _cmp(_getstate(lhs), _getstate(rhs))
                return op(mxenf__drzi, 0)
            return impl
    return overload_timedelta_cmp


@overload(operator.neg, no_unliteral=True)
def timedelta_neg(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return datetime.timedelta(-lhs.days, -lhs.seconds, -lhs.
                microseconds)
        return impl


@overload(operator.pos, no_unliteral=True)
def timedelta_pos(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            return lhs
        return impl


@overload(divmod, no_unliteral=True)
def timedelta_divmod(lhs, rhs):
    if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            uilyu__ezqy, qqptq__fmld = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return uilyu__ezqy, datetime.timedelta(0, 0, qqptq__fmld)
        return impl


@overload(abs, no_unliteral=True)
def timedelta_abs(lhs):
    if lhs == datetime_timedelta_type:

        def impl(lhs):
            if lhs.days < 0:
                return -lhs
            else:
                return lhs
        return impl


@intrinsic
def cast_numpy_timedelta_to_int(typingctx, val=None):
    assert val in (types.NPTimedelta('ns'), types.int64)

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(val), codegen


@overload(bool, no_unliteral=True)
def timedelta_to_bool(timedelta):
    if timedelta != datetime_timedelta_type:
        return
    qmdyv__mwba = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != qmdyv__mwba
    return impl


class DatetimeTimeDeltaArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeTimeDeltaArrayType, self).__init__(name=
            'DatetimeTimeDeltaArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_timedelta_type

    def copy(self):
        return DatetimeTimeDeltaArrayType()


datetime_timedelta_array_type = DatetimeTimeDeltaArrayType()
types.datetime_timedelta_array_type = datetime_timedelta_array_type
days_data_type = types.Array(types.int64, 1, 'C')
seconds_data_type = types.Array(types.int64, 1, 'C')
microseconds_data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeTimeDeltaArrayType)
class DatetimeTimeDeltaArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pqwta__rep = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, pqwta__rep)


make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'days_data', '_days_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'seconds_data',
    '_seconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'microseconds_data',
    '_microseconds_data')
make_attribute_wrapper(DatetimeTimeDeltaArrayType, 'null_bitmap',
    '_null_bitmap')


@overload_method(DatetimeTimeDeltaArrayType, 'copy', no_unliteral=True)
def overload_datetime_timedelta_arr_copy(A):
    return (lambda A: bodo.hiframes.datetime_timedelta_ext.
        init_datetime_timedelta_array(A._days_data.copy(), A._seconds_data.
        copy(), A._microseconds_data.copy(), A._null_bitmap.copy()))


@unbox(DatetimeTimeDeltaArrayType)
def unbox_datetime_timedelta_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    qjugy__qhb = types.Array(types.intp, 1, 'C')
    ozky__epboh = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        qjugy__qhb, [n])
    dypws__wqhhc = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        qjugy__qhb, [n])
    isnnh__colu = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        qjugy__qhb, [n])
    wih__txou = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    rxps__mkxg = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [wih__txou])
    luczq__agbzp = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (8).as_pointer()])
    obcek__zkk = cgutils.get_or_insert_function(c.builder.module,
        luczq__agbzp, name='unbox_datetime_timedelta_array')
    c.builder.call(obcek__zkk, [val, n, ozky__epboh.data, dypws__wqhhc.data,
        isnnh__colu.data, rxps__mkxg.data])
    ymqsf__zpgvb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ymqsf__zpgvb.days_data = ozky__epboh._getvalue()
    ymqsf__zpgvb.seconds_data = dypws__wqhhc._getvalue()
    ymqsf__zpgvb.microseconds_data = isnnh__colu._getvalue()
    ymqsf__zpgvb.null_bitmap = rxps__mkxg._getvalue()
    cqv__clymc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ymqsf__zpgvb._getvalue(), is_error=cqv__clymc)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    wki__dqcsn = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    ozky__epboh = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, wki__dqcsn.days_data)
    dypws__wqhhc = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
        .context, c.builder, wki__dqcsn.seconds_data).data
    isnnh__colu = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, wki__dqcsn.microseconds_data).data
    jrho__faw = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, wki__dqcsn.null_bitmap).data
    n = c.builder.extract_value(ozky__epboh.shape, 0)
    luczq__agbzp = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    kzt__bgicj = cgutils.get_or_insert_function(c.builder.module,
        luczq__agbzp, name='box_datetime_timedelta_array')
    fzdsw__mfrr = c.builder.call(kzt__bgicj, [n, ozky__epboh.data,
        dypws__wqhhc, isnnh__colu, jrho__faw])
    c.context.nrt.decref(c.builder, typ, val)
    return fzdsw__mfrr


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        rjecf__sqfr, eqsfk__vsog, qlcwo__yaz, oll__xxad = args
        ymwd__rbgbd = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        ymwd__rbgbd.days_data = rjecf__sqfr
        ymwd__rbgbd.seconds_data = eqsfk__vsog
        ymwd__rbgbd.microseconds_data = qlcwo__yaz
        ymwd__rbgbd.null_bitmap = oll__xxad
        context.nrt.incref(builder, signature.args[0], rjecf__sqfr)
        context.nrt.incref(builder, signature.args[1], eqsfk__vsog)
        context.nrt.incref(builder, signature.args[2], qlcwo__yaz)
        context.nrt.incref(builder, signature.args[3], oll__xxad)
        return ymwd__rbgbd._getvalue()
    rhen__smvo = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return rhen__smvo, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    ozky__epboh = np.empty(n, np.int64)
    dypws__wqhhc = np.empty(n, np.int64)
    isnnh__colu = np.empty(n, np.int64)
    zrovg__xom = np.empty(n + 7 >> 3, np.uint8)
    for wzswy__kvs, s in enumerate(pyval):
        uzby__tmv = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(zrovg__xom, wzswy__kvs, int(
            not uzby__tmv))
        if not uzby__tmv:
            ozky__epboh[wzswy__kvs] = s.days
            dypws__wqhhc[wzswy__kvs] = s.seconds
            isnnh__colu[wzswy__kvs] = s.microseconds
    crl__dwxrt = context.get_constant_generic(builder, days_data_type,
        ozky__epboh)
    yxn__koe = context.get_constant_generic(builder, seconds_data_type,
        dypws__wqhhc)
    vhxwo__tdd = context.get_constant_generic(builder,
        microseconds_data_type, isnnh__colu)
    ddt__ecer = context.get_constant_generic(builder, nulls_type, zrovg__xom)
    return lir.Constant.literal_struct([crl__dwxrt, yxn__koe, vhxwo__tdd,
        ddt__ecer])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    ozky__epboh = np.empty(n, dtype=np.int64)
    dypws__wqhhc = np.empty(n, dtype=np.int64)
    isnnh__colu = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(ozky__epboh, dypws__wqhhc,
        isnnh__colu, nulls)


def alloc_datetime_timedelta_array_equiv(self, scope, equiv_set, loc, args, kws
    ):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_timedelta_ext_alloc_datetime_timedelta_array
    ) = alloc_datetime_timedelta_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_timedelta_arr_getitem(A, ind):
    if A != datetime_timedelta_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl_int(A, ind):
            return datetime.timedelta(days=A._days_data[ind], seconds=A.
                _seconds_data[ind], microseconds=A._microseconds_data[ind])
        return impl_int
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            hbaq__zbo = bodo.utils.conversion.coerce_to_ndarray(ind)
            evdj__unh = A._null_bitmap
            rpg__uhhg = A._days_data[hbaq__zbo]
            xrax__npozz = A._seconds_data[hbaq__zbo]
            vtcl__ypgwn = A._microseconds_data[hbaq__zbo]
            n = len(rpg__uhhg)
            ufns__misxn = get_new_null_mask_bool_index(evdj__unh, ind, n)
            return init_datetime_timedelta_array(rpg__uhhg, xrax__npozz,
                vtcl__ypgwn, ufns__misxn)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            hbaq__zbo = bodo.utils.conversion.coerce_to_ndarray(ind)
            evdj__unh = A._null_bitmap
            rpg__uhhg = A._days_data[hbaq__zbo]
            xrax__npozz = A._seconds_data[hbaq__zbo]
            vtcl__ypgwn = A._microseconds_data[hbaq__zbo]
            n = len(rpg__uhhg)
            ufns__misxn = get_new_null_mask_int_index(evdj__unh, hbaq__zbo, n)
            return init_datetime_timedelta_array(rpg__uhhg, xrax__npozz,
                vtcl__ypgwn, ufns__misxn)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            evdj__unh = A._null_bitmap
            rpg__uhhg = np.ascontiguousarray(A._days_data[ind])
            xrax__npozz = np.ascontiguousarray(A._seconds_data[ind])
            vtcl__ypgwn = np.ascontiguousarray(A._microseconds_data[ind])
            ufns__misxn = get_new_null_mask_slice_index(evdj__unh, ind, n)
            return init_datetime_timedelta_array(rpg__uhhg, xrax__npozz,
                vtcl__ypgwn, ufns__misxn)
        return impl_slice
    raise BodoError(
        f'getitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(operator.setitem, no_unliteral=True)
def dt_timedelta_arr_setitem(A, ind, val):
    if A != datetime_timedelta_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    ewnki__tfm = (
        f"setitem for DatetimeTimedeltaArray with indexing type {ind} received an incorrect 'value' type {val}."
        )
    if isinstance(ind, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl(A, ind, val):
                A._days_data[ind] = val._days
                A._seconds_data[ind] = val._seconds
                A._microseconds_data[ind] = val._microseconds
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, ind, 1)
            return impl
        else:
            raise BodoError(ewnki__tfm)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(ewnki__tfm)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for wzswy__kvs in range(n):
                    A._days_data[ind[wzswy__kvs]] = val._days
                    A._seconds_data[ind[wzswy__kvs]] = val._seconds
                    A._microseconds_data[ind[wzswy__kvs]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[wzswy__kvs], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for wzswy__kvs in range(n):
                    A._days_data[ind[wzswy__kvs]] = val._days_data[wzswy__kvs]
                    A._seconds_data[ind[wzswy__kvs]] = val._seconds_data[
                        wzswy__kvs]
                    A._microseconds_data[ind[wzswy__kvs]
                        ] = val._microseconds_data[wzswy__kvs]
                    wow__ulb = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, wzswy__kvs)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[wzswy__kvs], wow__ulb)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for wzswy__kvs in range(n):
                    if not bodo.libs.array_kernels.isna(ind, wzswy__kvs
                        ) and ind[wzswy__kvs]:
                        A._days_data[wzswy__kvs] = val._days
                        A._seconds_data[wzswy__kvs] = val._seconds
                        A._microseconds_data[wzswy__kvs] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            wzswy__kvs, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                fdmx__wcop = 0
                for wzswy__kvs in range(n):
                    if not bodo.libs.array_kernels.isna(ind, wzswy__kvs
                        ) and ind[wzswy__kvs]:
                        A._days_data[wzswy__kvs] = val._days_data[fdmx__wcop]
                        A._seconds_data[wzswy__kvs] = val._seconds_data[
                            fdmx__wcop]
                        A._microseconds_data[wzswy__kvs
                            ] = val._microseconds_data[fdmx__wcop]
                        wow__ulb = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                            ._null_bitmap, fdmx__wcop)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            wzswy__kvs, wow__ulb)
                        fdmx__wcop += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                zqysn__wos = numba.cpython.unicode._normalize_slice(ind, len(A)
                    )
                for wzswy__kvs in range(zqysn__wos.start, zqysn__wos.stop,
                    zqysn__wos.step):
                    A._days_data[wzswy__kvs] = val._days
                    A._seconds_data[wzswy__kvs] = val._seconds
                    A._microseconds_data[wzswy__kvs] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        wzswy__kvs, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                abmhp__uuy = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, abmhp__uuy,
                    ind, n)
            return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeTimedeltaArray with indexing type {ind} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_timedelta_arr(A):
    if A == datetime_timedelta_array_type:
        return lambda A: len(A._days_data)


@overload_attribute(DatetimeTimeDeltaArrayType, 'shape')
def overload_datetime_timedelta_arr_shape(A):
    return lambda A: (len(A._days_data),)


@overload_attribute(DatetimeTimeDeltaArrayType, 'nbytes')
def timedelta_arr_nbytes_overload(A):
    return (lambda A: A._days_data.nbytes + A._seconds_data.nbytes + A.
        _microseconds_data.nbytes + A._null_bitmap.nbytes)


def overload_datetime_timedelta_arr_sub(arg1, arg2):
    if (arg1 == datetime_timedelta_array_type and arg2 ==
        datetime_timedelta_type):

        def impl(arg1, arg2):
            wki__dqcsn = arg1
            numba.parfors.parfor.init_prange()
            n = len(wki__dqcsn)
            A = alloc_datetime_timedelta_array(n)
            for wzswy__kvs in numba.parfors.parfor.internal_prange(n):
                A[wzswy__kvs] = wki__dqcsn[wzswy__kvs] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            plttv__kjx = True
        else:
            plttv__kjx = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                tkvdn__dhlit = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for wzswy__kvs in numba.parfors.parfor.internal_prange(n):
                    fxnvi__wxei = bodo.libs.array_kernels.isna(lhs, wzswy__kvs)
                    bsmx__belbn = bodo.libs.array_kernels.isna(rhs, wzswy__kvs)
                    if fxnvi__wxei or bsmx__belbn:
                        ahhn__nym = plttv__kjx
                    else:
                        ahhn__nym = op(lhs[wzswy__kvs], rhs[wzswy__kvs])
                    tkvdn__dhlit[wzswy__kvs] = ahhn__nym
                return tkvdn__dhlit
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                tkvdn__dhlit = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for wzswy__kvs in numba.parfors.parfor.internal_prange(n):
                    wow__ulb = bodo.libs.array_kernels.isna(lhs, wzswy__kvs)
                    if wow__ulb:
                        ahhn__nym = plttv__kjx
                    else:
                        ahhn__nym = op(lhs[wzswy__kvs], rhs)
                    tkvdn__dhlit[wzswy__kvs] = ahhn__nym
                return tkvdn__dhlit
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                tkvdn__dhlit = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for wzswy__kvs in numba.parfors.parfor.internal_prange(n):
                    wow__ulb = bodo.libs.array_kernels.isna(rhs, wzswy__kvs)
                    if wow__ulb:
                        ahhn__nym = plttv__kjx
                    else:
                        ahhn__nym = op(lhs, rhs[wzswy__kvs])
                    tkvdn__dhlit[wzswy__kvs] = ahhn__nym
                return tkvdn__dhlit
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for hpfo__qphrd in timedelta_unsupported_attrs:
        kgwxl__mged = 'pandas.Timedelta.' + hpfo__qphrd
        overload_attribute(PDTimeDeltaType, hpfo__qphrd)(
            create_unsupported_overload(kgwxl__mged))
    for ibm__thnt in timedelta_unsupported_methods:
        kgwxl__mged = 'pandas.Timedelta.' + ibm__thnt
        overload_method(PDTimeDeltaType, ibm__thnt)(create_unsupported_overload
            (kgwxl__mged + '()'))


_intstall_pd_timedelta_unsupported()
