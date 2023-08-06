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
        mpevy__pjfwf = [('value', types.int64)]
        super(PDTimeDeltaModel, self).__init__(dmm, fe_type, mpevy__pjfwf)


@box(PDTimeDeltaType)
def box_pd_timedelta(typ, val, c):
    ymy__qmzg = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    hjhm__wnp = c.pyapi.long_from_longlong(ymy__qmzg.value)
    ltzjk__vbqdm = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timedelta))
    res = c.pyapi.call_function_objargs(ltzjk__vbqdm, (hjhm__wnp,))
    c.pyapi.decref(hjhm__wnp)
    c.pyapi.decref(ltzjk__vbqdm)
    return res


@unbox(PDTimeDeltaType)
def unbox_pd_timedelta(typ, val, c):
    hjhm__wnp = c.pyapi.object_getattr_string(val, 'value')
    cojt__ztpcm = c.pyapi.long_as_longlong(hjhm__wnp)
    ymy__qmzg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ymy__qmzg.value = cojt__ztpcm
    c.pyapi.decref(hjhm__wnp)
    ftu__etpvb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ymy__qmzg._getvalue(), is_error=ftu__etpvb)


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
            cfqu__lzd = 1000 * microseconds
            return init_pd_timedelta(cfqu__lzd)
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
            cfqu__lzd = 1000 * microseconds
            return init_pd_timedelta(cfqu__lzd)
        return impl_timedelta_datetime
    if not is_overload_constant_str(unit):
        raise BodoError('pd.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    tjl__gpkv, luhbv__jtiiv = pd._libs.tslibs.conversion.precision_from_unit(
        unit)

    def impl_timedelta(value=_no_input, unit='ns', days=0, seconds=0,
        microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return init_pd_timedelta(value * tjl__gpkv)
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
            ljcnw__dvoco = (rhs.microseconds + (rhs.seconds + rhs.days * 60 *
                60 * 24) * 1000 * 1000) * 1000
            val = lhs.value + ljcnw__dvoco
            return pd.Timedelta(val)
        return impl
    if lhs == datetime_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            sun__vqzg = (lhs.microseconds + (lhs.seconds + lhs.days * 60 * 
                60 * 24) * 1000 * 1000) * 1000
            val = sun__vqzg + rhs.value
            return pd.Timedelta(val)
        return impl
    if lhs == pd_timedelta_type and rhs == datetime_datetime_type:
        from bodo.hiframes.pd_timestamp_ext import compute_pd_timestamp

        def impl(lhs, rhs):
            vksdn__mfeq = rhs.toordinal()
            zwntt__aegzc = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            rqaik__gmuai = rhs.microsecond
            qfs__lygl = lhs.value // 1000
            call__nkwng = lhs.nanoseconds
            tjmf__ypx = rqaik__gmuai + qfs__lygl
            heydf__iyq = 1000000 * (vksdn__mfeq * 86400 + zwntt__aegzc
                ) + tjmf__ypx
            etkx__cmsdx = call__nkwng
            return compute_pd_timestamp(heydf__iyq, etkx__cmsdx)
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
            ulg__lvz = datetime.timedelta(rhs.toordinal(), hours=rhs.hour,
                minutes=rhs.minute, seconds=rhs.second, microseconds=rhs.
                microsecond)
            ulg__lvz = ulg__lvz + lhs
            hgr__uxt, sqw__oakw = divmod(ulg__lvz.seconds, 3600)
            gkq__lbl, sqr__iegj = divmod(sqw__oakw, 60)
            if 0 < ulg__lvz.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(ulg__lvz
                    .days)
                return datetime.datetime(d.year, d.month, d.day, hgr__uxt,
                    gkq__lbl, sqr__iegj, ulg__lvz.microseconds)
            raise OverflowError('result out of range')
        return impl
    if lhs == datetime_datetime_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            ulg__lvz = datetime.timedelta(lhs.toordinal(), hours=lhs.hour,
                minutes=lhs.minute, seconds=lhs.second, microseconds=lhs.
                microsecond)
            ulg__lvz = ulg__lvz + rhs
            hgr__uxt, sqw__oakw = divmod(ulg__lvz.seconds, 3600)
            gkq__lbl, sqr__iegj = divmod(sqw__oakw, 60)
            if 0 < ulg__lvz.days <= _MAXORDINAL:
                d = bodo.hiframes.datetime_date_ext.fromordinal_impl(ulg__lvz
                    .days)
                return datetime.datetime(d.year, d.month, d.day, hgr__uxt,
                    gkq__lbl, sqr__iegj, ulg__lvz.microseconds)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_timedelta(lhs, rhs):
    if lhs == pd_timedelta_type and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            qll__jmvv = lhs.value - rhs.value
            return pd.Timedelta(qll__jmvv)
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
            vypk__uzbd = lhs
            numba.parfors.parfor.init_prange()
            n = len(vypk__uzbd)
            A = alloc_datetime_timedelta_array(n)
            for qfoi__pkvhu in numba.parfors.parfor.internal_prange(n):
                A[qfoi__pkvhu] = vypk__uzbd[qfoi__pkvhu] - rhs
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
            rvuez__hjwsd = _to_microseconds(lhs) % _to_microseconds(rhs)
            return datetime.timedelta(0, 0, rvuez__hjwsd)
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
            vxsq__dth, rvuez__hjwsd = divmod(lhs.value, rhs.value)
            return vxsq__dth, pd.Timedelta(rvuez__hjwsd)
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
        mpevy__pjfwf = [('days', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64)]
        super(DatetimeTimeDeltaModel, self).__init__(dmm, fe_type, mpevy__pjfwf
            )


@box(DatetimeTimeDeltaType)
def box_datetime_timedelta(typ, val, c):
    ymy__qmzg = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ygl__uos = c.pyapi.long_from_longlong(ymy__qmzg.days)
    fxub__eeh = c.pyapi.long_from_longlong(ymy__qmzg.seconds)
    rlti__khr = c.pyapi.long_from_longlong(ymy__qmzg.microseconds)
    ltzjk__vbqdm = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.
        timedelta))
    res = c.pyapi.call_function_objargs(ltzjk__vbqdm, (ygl__uos, fxub__eeh,
        rlti__khr))
    c.pyapi.decref(ygl__uos)
    c.pyapi.decref(fxub__eeh)
    c.pyapi.decref(rlti__khr)
    c.pyapi.decref(ltzjk__vbqdm)
    return res


@unbox(DatetimeTimeDeltaType)
def unbox_datetime_timedelta(typ, val, c):
    ygl__uos = c.pyapi.object_getattr_string(val, 'days')
    fxub__eeh = c.pyapi.object_getattr_string(val, 'seconds')
    rlti__khr = c.pyapi.object_getattr_string(val, 'microseconds')
    bves__wute = c.pyapi.long_as_longlong(ygl__uos)
    kujqb__ntuiu = c.pyapi.long_as_longlong(fxub__eeh)
    iszx__fggb = c.pyapi.long_as_longlong(rlti__khr)
    ymy__qmzg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ymy__qmzg.days = bves__wute
    ymy__qmzg.seconds = kujqb__ntuiu
    ymy__qmzg.microseconds = iszx__fggb
    c.pyapi.decref(ygl__uos)
    c.pyapi.decref(fxub__eeh)
    c.pyapi.decref(rlti__khr)
    ftu__etpvb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ymy__qmzg._getvalue(), is_error=ftu__etpvb)


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
    vxsq__dth, rvuez__hjwsd = divmod(a, b)
    rvuez__hjwsd *= 2
    codv__cdjba = rvuez__hjwsd > b if b > 0 else rvuez__hjwsd < b
    if codv__cdjba or rvuez__hjwsd == b and vxsq__dth % 2 == 1:
        vxsq__dth += 1
    return vxsq__dth


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
                ntq__jqu = _cmp(_getstate(lhs), _getstate(rhs))
                return op(ntq__jqu, 0)
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
            vxsq__dth, rvuez__hjwsd = divmod(_to_microseconds(lhs),
                _to_microseconds(rhs))
            return vxsq__dth, datetime.timedelta(0, 0, rvuez__hjwsd)
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
    mdhlg__vrv = datetime.timedelta(0)

    def impl(timedelta):
        return timedelta != mdhlg__vrv
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
        mpevy__pjfwf = [('days_data', days_data_type), ('seconds_data',
            seconds_data_type), ('microseconds_data',
            microseconds_data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, mpevy__pjfwf)


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
    pwlm__oktyt = types.Array(types.intp, 1, 'C')
    hgwg__cqap = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        pwlm__oktyt, [n])
    rkyix__gucvy = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        pwlm__oktyt, [n])
    ptq__ahgyb = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        pwlm__oktyt, [n])
    hlv__axdc = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64
        ), 7)), lir.Constant(lir.IntType(64), 8))
    ujc__dakrq = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [hlv__axdc])
    zkf__kddv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer()])
    ppid__eaa = cgutils.get_or_insert_function(c.builder.module, zkf__kddv,
        name='unbox_datetime_timedelta_array')
    c.builder.call(ppid__eaa, [val, n, hgwg__cqap.data, rkyix__gucvy.data,
        ptq__ahgyb.data, ujc__dakrq.data])
    scyon__phn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    scyon__phn.days_data = hgwg__cqap._getvalue()
    scyon__phn.seconds_data = rkyix__gucvy._getvalue()
    scyon__phn.microseconds_data = ptq__ahgyb._getvalue()
    scyon__phn.null_bitmap = ujc__dakrq._getvalue()
    ftu__etpvb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(scyon__phn._getvalue(), is_error=ftu__etpvb)


@box(DatetimeTimeDeltaArrayType)
def box_datetime_timedelta_array(typ, val, c):
    vypk__uzbd = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    hgwg__cqap = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, vypk__uzbd.days_data)
    rkyix__gucvy = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
        .context, c.builder, vypk__uzbd.seconds_data).data
    ptq__ahgyb = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, vypk__uzbd.microseconds_data).data
    weqt__ofy = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, vypk__uzbd.null_bitmap).data
    n = c.builder.extract_value(hgwg__cqap.shape, 0)
    zkf__kddv = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(64).as_pointer(), lir.IntType
        (64).as_pointer(), lir.IntType(8).as_pointer()])
    twbg__dnfx = cgutils.get_or_insert_function(c.builder.module, zkf__kddv,
        name='box_datetime_timedelta_array')
    ohtd__texx = c.builder.call(twbg__dnfx, [n, hgwg__cqap.data,
        rkyix__gucvy, ptq__ahgyb, weqt__ofy])
    c.context.nrt.decref(c.builder, typ, val)
    return ohtd__texx


@intrinsic
def init_datetime_timedelta_array(typingctx, days_data, seconds_data,
    microseconds_data, nulls=None):
    assert days_data == types.Array(types.int64, 1, 'C')
    assert seconds_data == types.Array(types.int64, 1, 'C')
    assert microseconds_data == types.Array(types.int64, 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        rddqa__szl, yvip__utik, kkzq__rgju, lpj__fxhi = args
        xkexk__ftd = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        xkexk__ftd.days_data = rddqa__szl
        xkexk__ftd.seconds_data = yvip__utik
        xkexk__ftd.microseconds_data = kkzq__rgju
        xkexk__ftd.null_bitmap = lpj__fxhi
        context.nrt.incref(builder, signature.args[0], rddqa__szl)
        context.nrt.incref(builder, signature.args[1], yvip__utik)
        context.nrt.incref(builder, signature.args[2], kkzq__rgju)
        context.nrt.incref(builder, signature.args[3], lpj__fxhi)
        return xkexk__ftd._getvalue()
    pzxta__teef = datetime_timedelta_array_type(days_data, seconds_data,
        microseconds_data, nulls)
    return pzxta__teef, codegen


@lower_constant(DatetimeTimeDeltaArrayType)
def lower_constant_datetime_timedelta_arr(context, builder, typ, pyval):
    n = len(pyval)
    hgwg__cqap = np.empty(n, np.int64)
    rkyix__gucvy = np.empty(n, np.int64)
    ptq__ahgyb = np.empty(n, np.int64)
    iiknr__tephs = np.empty(n + 7 >> 3, np.uint8)
    for qfoi__pkvhu, s in enumerate(pyval):
        kllb__mclj = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(iiknr__tephs, qfoi__pkvhu, int
            (not kllb__mclj))
        if not kllb__mclj:
            hgwg__cqap[qfoi__pkvhu] = s.days
            rkyix__gucvy[qfoi__pkvhu] = s.seconds
            ptq__ahgyb[qfoi__pkvhu] = s.microseconds
    xlk__xhx = context.get_constant_generic(builder, days_data_type, hgwg__cqap
        )
    mgw__ido = context.get_constant_generic(builder, seconds_data_type,
        rkyix__gucvy)
    gshz__aspy = context.get_constant_generic(builder,
        microseconds_data_type, ptq__ahgyb)
    bobvy__bkrr = context.get_constant_generic(builder, nulls_type,
        iiknr__tephs)
    return lir.Constant.literal_struct([xlk__xhx, mgw__ido, gshz__aspy,
        bobvy__bkrr])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_timedelta_array(n):
    hgwg__cqap = np.empty(n, dtype=np.int64)
    rkyix__gucvy = np.empty(n, dtype=np.int64)
    ptq__ahgyb = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_timedelta_array(hgwg__cqap, rkyix__gucvy,
        ptq__ahgyb, nulls)


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
            osfiy__hxl = bodo.utils.conversion.coerce_to_ndarray(ind)
            rdfcd__pqly = A._null_bitmap
            rjsx__saz = A._days_data[osfiy__hxl]
            jpopf__rpsjj = A._seconds_data[osfiy__hxl]
            rwd__otie = A._microseconds_data[osfiy__hxl]
            n = len(rjsx__saz)
            pzssi__ilspq = get_new_null_mask_bool_index(rdfcd__pqly, ind, n)
            return init_datetime_timedelta_array(rjsx__saz, jpopf__rpsjj,
                rwd__otie, pzssi__ilspq)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            osfiy__hxl = bodo.utils.conversion.coerce_to_ndarray(ind)
            rdfcd__pqly = A._null_bitmap
            rjsx__saz = A._days_data[osfiy__hxl]
            jpopf__rpsjj = A._seconds_data[osfiy__hxl]
            rwd__otie = A._microseconds_data[osfiy__hxl]
            n = len(rjsx__saz)
            pzssi__ilspq = get_new_null_mask_int_index(rdfcd__pqly,
                osfiy__hxl, n)
            return init_datetime_timedelta_array(rjsx__saz, jpopf__rpsjj,
                rwd__otie, pzssi__ilspq)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            n = len(A._days_data)
            rdfcd__pqly = A._null_bitmap
            rjsx__saz = np.ascontiguousarray(A._days_data[ind])
            jpopf__rpsjj = np.ascontiguousarray(A._seconds_data[ind])
            rwd__otie = np.ascontiguousarray(A._microseconds_data[ind])
            pzssi__ilspq = get_new_null_mask_slice_index(rdfcd__pqly, ind, n)
            return init_datetime_timedelta_array(rjsx__saz, jpopf__rpsjj,
                rwd__otie, pzssi__ilspq)
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
    ydsa__ficsw = (
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
            raise BodoError(ydsa__ficsw)
    if not (is_iterable_type(val) and val.dtype == bodo.
        datetime_timedelta_type or types.unliteral(val) ==
        datetime_timedelta_type):
        raise BodoError(ydsa__ficsw)
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_arr_ind_scalar(A, ind, val):
                n = len(A)
                for qfoi__pkvhu in range(n):
                    A._days_data[ind[qfoi__pkvhu]] = val._days
                    A._seconds_data[ind[qfoi__pkvhu]] = val._seconds
                    A._microseconds_data[ind[qfoi__pkvhu]] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[qfoi__pkvhu], 1)
            return impl_arr_ind_scalar
        else:

            def impl_arr_ind(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(val._days_data)
                for qfoi__pkvhu in range(n):
                    A._days_data[ind[qfoi__pkvhu]] = val._days_data[qfoi__pkvhu
                        ]
                    A._seconds_data[ind[qfoi__pkvhu]] = val._seconds_data[
                        qfoi__pkvhu]
                    A._microseconds_data[ind[qfoi__pkvhu]
                        ] = val._microseconds_data[qfoi__pkvhu]
                    brg__mea = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                        ._null_bitmap, qfoi__pkvhu)
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        ind[qfoi__pkvhu], brg__mea)
            return impl_arr_ind
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_bool_ind_mask_scalar(A, ind, val):
                n = len(ind)
                for qfoi__pkvhu in range(n):
                    if not bodo.libs.array_kernels.isna(ind, qfoi__pkvhu
                        ) and ind[qfoi__pkvhu]:
                        A._days_data[qfoi__pkvhu] = val._days
                        A._seconds_data[qfoi__pkvhu] = val._seconds
                        A._microseconds_data[qfoi__pkvhu] = val._microseconds
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            qfoi__pkvhu, 1)
            return impl_bool_ind_mask_scalar
        else:

            def impl_bool_ind_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(ind)
                ftx__mzsg = 0
                for qfoi__pkvhu in range(n):
                    if not bodo.libs.array_kernels.isna(ind, qfoi__pkvhu
                        ) and ind[qfoi__pkvhu]:
                        A._days_data[qfoi__pkvhu] = val._days_data[ftx__mzsg]
                        A._seconds_data[qfoi__pkvhu] = val._seconds_data[
                            ftx__mzsg]
                        A._microseconds_data[qfoi__pkvhu
                            ] = val._microseconds_data[ftx__mzsg]
                        brg__mea = bodo.libs.int_arr_ext.get_bit_bitmap_arr(val
                            ._null_bitmap, ftx__mzsg)
                        bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                            qfoi__pkvhu, brg__mea)
                        ftx__mzsg += 1
            return impl_bool_ind_mask
    if isinstance(ind, types.SliceType):
        if types.unliteral(val) == datetime_timedelta_type:

            def impl_slice_scalar(A, ind, val):
                fyu__clq = numba.cpython.unicode._normalize_slice(ind, len(A))
                for qfoi__pkvhu in range(fyu__clq.start, fyu__clq.stop,
                    fyu__clq.step):
                    A._days_data[qfoi__pkvhu] = val._days
                    A._seconds_data[qfoi__pkvhu] = val._seconds
                    A._microseconds_data[qfoi__pkvhu] = val._microseconds
                    bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap,
                        qfoi__pkvhu, 1)
            return impl_slice_scalar
        else:

            def impl_slice_mask(A, ind, val):
                val = bodo.utils.conversion.coerce_to_array(val,
                    use_nullable_array=True)
                n = len(A._days_data)
                A._days_data[ind] = val._days_data
                A._seconds_data[ind] = val._seconds_data
                A._microseconds_data[ind] = val._microseconds_data
                biif__qqein = val._null_bitmap.copy()
                setitem_slice_index_null_bits(A._null_bitmap, biif__qqein,
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
            vypk__uzbd = arg1
            numba.parfors.parfor.init_prange()
            n = len(vypk__uzbd)
            A = alloc_datetime_timedelta_array(n)
            for qfoi__pkvhu in numba.parfors.parfor.internal_prange(n):
                A[qfoi__pkvhu] = vypk__uzbd[qfoi__pkvhu] - arg2
            return A
        return impl


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            ujjpe__cbu = True
        else:
            ujjpe__cbu = False
        if (lhs == datetime_timedelta_array_type and rhs ==
            datetime_timedelta_array_type):

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                pkckm__odx = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for qfoi__pkvhu in numba.parfors.parfor.internal_prange(n):
                    ehmtl__gcpoo = bodo.libs.array_kernels.isna(lhs,
                        qfoi__pkvhu)
                    npy__qcnlw = bodo.libs.array_kernels.isna(rhs, qfoi__pkvhu)
                    if ehmtl__gcpoo or npy__qcnlw:
                        bgor__nfzr = ujjpe__cbu
                    else:
                        bgor__nfzr = op(lhs[qfoi__pkvhu], rhs[qfoi__pkvhu])
                    pkckm__odx[qfoi__pkvhu] = bgor__nfzr
                return pkckm__odx
            return impl
        elif lhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                pkckm__odx = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for qfoi__pkvhu in numba.parfors.parfor.internal_prange(n):
                    brg__mea = bodo.libs.array_kernels.isna(lhs, qfoi__pkvhu)
                    if brg__mea:
                        bgor__nfzr = ujjpe__cbu
                    else:
                        bgor__nfzr = op(lhs[qfoi__pkvhu], rhs)
                    pkckm__odx[qfoi__pkvhu] = bgor__nfzr
                return pkckm__odx
            return impl
        elif rhs == datetime_timedelta_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                pkckm__odx = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for qfoi__pkvhu in numba.parfors.parfor.internal_prange(n):
                    brg__mea = bodo.libs.array_kernels.isna(rhs, qfoi__pkvhu)
                    if brg__mea:
                        bgor__nfzr = ujjpe__cbu
                    else:
                        bgor__nfzr = op(lhs, rhs[qfoi__pkvhu])
                    pkckm__odx[qfoi__pkvhu] = bgor__nfzr
                return pkckm__odx
            return impl
    return overload_date_arr_cmp


timedelta_unsupported_attrs = ['asm8', 'resolution_string', 'freq',
    'is_populated']
timedelta_unsupported_methods = ['isoformat']


def _intstall_pd_timedelta_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for rcxm__mayv in timedelta_unsupported_attrs:
        fknpl__epetl = 'pandas.Timedelta.' + rcxm__mayv
        overload_attribute(PDTimeDeltaType, rcxm__mayv)(
            create_unsupported_overload(fknpl__epetl))
    for dry__dugk in timedelta_unsupported_methods:
        fknpl__epetl = 'pandas.Timedelta.' + dry__dugk
        overload_method(PDTimeDeltaType, dry__dugk)(create_unsupported_overload
            (fknpl__epetl + '()'))


_intstall_pd_timedelta_unsupported()
