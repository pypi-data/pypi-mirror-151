""" Implementation of binary operators for the different types.
    Currently implemented operators:
        arith: add, sub, mul, truediv, floordiv, mod, pow
        cmp: lt, le, eq, ne, ge, gt
"""
import operator
import numba
from numba.core import types
from numba.core.imputils import lower_builtin
from numba.core.typing.builtins import machine_ints
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type, datetime_timedelta_type
from bodo.hiframes.datetime_timedelta_ext import datetime_datetime_type, datetime_timedelta_array_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import DatetimeIndexType, HeterogeneousIndexType, is_index_type
from bodo.hiframes.pd_offsets_ext import date_offset_type, month_begin_type, month_end_type, week_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_type
from bodo.hiframes.series_impl import SeriesType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.typing import BodoError, is_overload_bool, is_str_arr_type, is_timedelta_type


class SeriesCmpOpTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        lhs, rhs = args
        if cmp_timeseries(lhs, rhs) or (isinstance(lhs, DataFrameType) or
            isinstance(rhs, DataFrameType)) or not (isinstance(lhs,
            SeriesType) or isinstance(rhs, SeriesType)):
            return
        lrvxk__cuscl = lhs.data if isinstance(lhs, SeriesType) else lhs
        dang__ohx = rhs.data if isinstance(rhs, SeriesType) else rhs
        if lrvxk__cuscl in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and dang__ohx.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            lrvxk__cuscl = dang__ohx.dtype
        elif dang__ohx in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and lrvxk__cuscl.dtype in (bodo.datetime64ns, bodo.timedelta64ns
            ):
            dang__ohx = lrvxk__cuscl.dtype
        nfo__btw = lrvxk__cuscl, dang__ohx
        jego__zny = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            seo__cyqwb = self.context.resolve_function_type(self.key,
                nfo__btw, {}).return_type
        except Exception as vhbaz__cfo:
            raise BodoError(jego__zny)
        if is_overload_bool(seo__cyqwb):
            raise BodoError(jego__zny)
        cagl__bavp = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        fjtxj__esn = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        oqk__ckowp = types.bool_
        soe__vmk = SeriesType(oqk__ckowp, seo__cyqwb, cagl__bavp, fjtxj__esn)
        return soe__vmk(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        mwx__tdhc = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if mwx__tdhc is None:
            mwx__tdhc = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, mwx__tdhc, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        lrvxk__cuscl = lhs.data if isinstance(lhs, SeriesType) else lhs
        dang__ohx = rhs.data if isinstance(rhs, SeriesType) else rhs
        nfo__btw = lrvxk__cuscl, dang__ohx
        jego__zny = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            seo__cyqwb = self.context.resolve_function_type(self.key,
                nfo__btw, {}).return_type
        except Exception as fup__bnzj:
            raise BodoError(jego__zny)
        cagl__bavp = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        fjtxj__esn = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        oqk__ckowp = seo__cyqwb.dtype
        soe__vmk = SeriesType(oqk__ckowp, seo__cyqwb, cagl__bavp, fjtxj__esn)
        return soe__vmk(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        mwx__tdhc = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if mwx__tdhc is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                mwx__tdhc = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, mwx__tdhc, sig, args)
    return lower_and_or_impl


def overload_add_operator_scalars(lhs, rhs):
    if lhs == week_type or rhs == week_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_week_offset_type(lhs, rhs))
    if lhs == month_begin_type or rhs == month_begin_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_begin_offset_type(lhs, rhs))
    if lhs == month_end_type or rhs == month_end_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_end_offset_type(lhs, rhs))
    if lhs == date_offset_type or rhs == date_offset_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_date_offset_type(lhs, rhs))
    if add_timestamp(lhs, rhs):
        return bodo.hiframes.pd_timestamp_ext.overload_add_operator_timestamp(
            lhs, rhs)
    if add_dt_td_and_dt_date(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_add_operator_datetime_date(lhs, rhs))
    if add_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_add_operator_datetime_timedelta(lhs, rhs))
    raise_error_if_not_numba_supported(operator.add, lhs, rhs)


def overload_sub_operator_scalars(lhs, rhs):
    if sub_offset_to_datetime_or_timestamp(lhs, rhs):
        return bodo.hiframes.pd_offsets_ext.overload_sub_operator_offsets(lhs,
            rhs)
    if lhs == pd_timestamp_type and rhs in [pd_timestamp_type,
        datetime_timedelta_type, pd_timedelta_type]:
        return bodo.hiframes.pd_timestamp_ext.overload_sub_operator_timestamp(
            lhs, rhs)
    if sub_dt_or_td(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_sub_operator_datetime_date(lhs, rhs))
    if sub_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_sub_operator_datetime_timedelta(lhs, rhs))
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
        return (bodo.hiframes.datetime_datetime_ext.
            overload_sub_operator_datetime_datetime(lhs, rhs))
    raise_error_if_not_numba_supported(operator.sub, lhs, rhs)


def create_overload_arith_op(op):

    def overload_arith_operator(lhs, rhs):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
            f'{op} operator')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
            f'{op} operator')
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if time_series_operation(lhs, rhs) and op in [operator.add,
            operator.sub]:
            return bodo.hiframes.series_dt_impl.create_bin_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return bodo.hiframes.series_impl.create_binary_op_overload(op)(lhs,
                rhs)
        if sub_dt_index_and_timestamp(lhs, rhs) and op == operator.sub:
            return (bodo.hiframes.pd_index_ext.
                overload_sub_operator_datetime_index(lhs, rhs))
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if args_td_and_int_array(lhs, rhs):
            return bodo.libs.int_arr_ext.get_int_array_op_pd_td(op)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if op == operator.add and (is_str_arr_type(lhs) or types.unliteral(
            lhs) == string_type):
            return bodo.libs.str_arr_ext.overload_add_operator_string_array(lhs
                , rhs)
        if op == operator.add:
            return overload_add_operator_scalars(lhs, rhs)
        if op == operator.sub:
            return overload_sub_operator_scalars(lhs, rhs)
        if op == operator.mul:
            if mul_timedelta_and_int(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mul_operator_timedelta(lhs, rhs))
            if mul_string_arr_and_int(lhs, rhs):
                return bodo.libs.str_arr_ext.overload_mul_operator_str_arr(lhs,
                    rhs)
            if mul_date_offset_and_int(lhs, rhs):
                return (bodo.hiframes.pd_offsets_ext.
                    overload_mul_date_offset_types(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op in [operator.truediv, operator.floordiv]:
            if div_timedelta_and_int(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_pd_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_pd_timedelta(lhs, rhs))
            if div_datetime_timedelta(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_dt_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_dt_timedelta(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.mod:
            if mod_timedeltas(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mod_operator_timedeltas(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.pow:
            raise_error_if_not_numba_supported(op, lhs, rhs)
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_arith_operator


def create_overload_cmp_operator(op):

    def overload_cmp_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
                f'{op} operator')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
                f'{op} operator')
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if cmp_timeseries(lhs, rhs):
            return bodo.hiframes.series_dt_impl.create_cmp_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
            f'{op} operator')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
            f'{op} operator')
        if lhs == datetime_date_array_type or rhs == datetime_date_array_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload_arr(
                op)(lhs, rhs)
        if (lhs == datetime_timedelta_array_type or rhs ==
            datetime_timedelta_array_type):
            mwx__tdhc = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return mwx__tdhc(lhs, rhs)
        if is_str_arr_type(lhs) or is_str_arr_type(rhs):
            return bodo.libs.str_arr_ext.create_binary_op_overload(op)(lhs, rhs
                )
        if isinstance(lhs, Decimal128Type) and isinstance(rhs, Decimal128Type):
            return bodo.libs.decimal_arr_ext.decimal_create_cmp_op_overload(op
                )(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if binary_array_cmp(lhs, rhs):
            return bodo.libs.binary_arr_ext.create_binary_cmp_op_overload(op)(
                lhs, rhs)
        if cmp_dt_index_to_string(lhs, rhs):
            return bodo.hiframes.pd_index_ext.overload_binop_dti_str(op)(lhs,
                rhs)
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if lhs == datetime_date_type and rhs == datetime_date_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload(op)(
                lhs, rhs)
        if can_cmp_date_datetime(lhs, rhs, op):
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
            return bodo.hiframes.datetime_datetime_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:
            return bodo.hiframes.datetime_timedelta_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if cmp_timedeltas(lhs, rhs):
            mwx__tdhc = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return mwx__tdhc(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    edz__giab = lhs == datetime_timedelta_type and rhs == datetime_date_type
    jxni__eimi = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return edz__giab or jxni__eimi


def add_timestamp(lhs, rhs):
    nzjs__drcy = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    fsiwb__hjd = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return nzjs__drcy or fsiwb__hjd


def add_datetime_and_timedeltas(lhs, rhs):
    cljsp__ijvkt = [datetime_timedelta_type, pd_timedelta_type]
    ohkz__uiwfv = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    rvt__npl = lhs in cljsp__ijvkt and rhs in cljsp__ijvkt
    radb__lbepc = (lhs == datetime_datetime_type and rhs in cljsp__ijvkt or
        rhs == datetime_datetime_type and lhs in cljsp__ijvkt)
    return rvt__npl or radb__lbepc


def mul_string_arr_and_int(lhs, rhs):
    dang__ohx = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    lrvxk__cuscl = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return dang__ohx or lrvxk__cuscl


def mul_timedelta_and_int(lhs, rhs):
    edz__giab = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    jxni__eimi = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return edz__giab or jxni__eimi


def mul_date_offset_and_int(lhs, rhs):
    lwdd__tgu = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    klyy__jrx = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return lwdd__tgu or klyy__jrx


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    brye__bmr = [datetime_datetime_type, pd_timestamp_type, datetime_date_type]
    xvg__xph = [date_offset_type, month_begin_type, month_end_type, week_type]
    return rhs in xvg__xph and lhs in brye__bmr


def sub_dt_index_and_timestamp(lhs, rhs):
    jvgah__mdf = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_type
    lqkgi__tna = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return jvgah__mdf or lqkgi__tna


def sub_dt_or_td(lhs, rhs):
    hcm__ixr = lhs == datetime_date_type and rhs == datetime_timedelta_type
    dnsd__xqji = lhs == datetime_date_type and rhs == datetime_date_type
    uaji__jan = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return hcm__ixr or dnsd__xqji or uaji__jan


def sub_datetime_and_timedeltas(lhs, rhs):
    rtji__nagim = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    ewk__nwvxq = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return rtji__nagim or ewk__nwvxq


def div_timedelta_and_int(lhs, rhs):
    rvt__npl = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    rusm__dil = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return rvt__npl or rusm__dil


def div_datetime_timedelta(lhs, rhs):
    rvt__npl = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    rusm__dil = lhs == datetime_timedelta_type and rhs == types.int64
    return rvt__npl or rusm__dil


def mod_timedeltas(lhs, rhs):
    lnw__sdj = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    ejt__kyiy = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return lnw__sdj or ejt__kyiy


def cmp_dt_index_to_string(lhs, rhs):
    jvgah__mdf = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    lqkgi__tna = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return jvgah__mdf or lqkgi__tna


def cmp_timestamp_or_date(lhs, rhs):
    yrn__hltv = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    buqnj__abqm = (lhs == bodo.hiframes.datetime_date_ext.
        datetime_date_type and rhs == pd_timestamp_type)
    vzpi__vyfz = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    bkww__kvhrb = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    erot__utiqq = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return yrn__hltv or buqnj__abqm or vzpi__vyfz or bkww__kvhrb or erot__utiqq


def cmp_timeseries(lhs, rhs):
    jqh__hgeso = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    tyz__vln = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    amweg__plp = jqh__hgeso or tyz__vln
    xoe__jnw = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    pmto__bfyqz = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    zvykt__idqz = xoe__jnw or pmto__bfyqz
    return amweg__plp or zvykt__idqz


def cmp_timedeltas(lhs, rhs):
    rvt__npl = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in rvt__npl and rhs in rvt__npl


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    pbwmh__myc = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return pbwmh__myc


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    smkd__ltqqy = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    evxbh__hyrr = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    scy__rbugm = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    yyd__oiyml = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return smkd__ltqqy or evxbh__hyrr or scy__rbugm or yyd__oiyml


def args_td_and_int_array(lhs, rhs):
    sqec__uzb = (isinstance(lhs, IntegerArrayType) or isinstance(lhs, types
        .Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance(
        rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    hzs__qiqu = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return sqec__uzb and hzs__qiqu


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        jxni__eimi = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        edz__giab = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        aimx__qmqy = jxni__eimi or edz__giab
        svoeg__glyuv = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        krltw__pxvy = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        bwbbl__gnidh = svoeg__glyuv or krltw__pxvy
        inq__ysq = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        kik__xio = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        mpx__fapa = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        zkr__cfgkb = inq__ysq or kik__xio or mpx__fapa
        tefoo__kjoet = isinstance(lhs, types.List) and isinstance(rhs,
            types.Integer) or isinstance(lhs, types.Integer) and isinstance(rhs
            , types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        ovutu__mzw = isinstance(lhs, tys) or isinstance(rhs, tys)
        fdy__xwqsm = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (aimx__qmqy or bwbbl__gnidh or zkr__cfgkb or tefoo__kjoet or
            ovutu__mzw or fdy__xwqsm)
    if op == operator.pow:
        ebyqd__axl = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        srf__ertnu = isinstance(lhs, types.Float) and isinstance(rhs, (
            types.IntegerLiteral, types.Float, types.Integer) or rhs in
            types.unsigned_domain or rhs in types.signed_domain)
        mpx__fapa = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        fdy__xwqsm = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return ebyqd__axl or srf__ertnu or mpx__fapa or fdy__xwqsm
    if op == operator.floordiv:
        kik__xio = lhs in types.real_domain and rhs in types.real_domain
        inq__ysq = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        ayae__qedk = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        rvt__npl = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, (
            types.Integer, types.Float, types.NPTimedelta))
        fdy__xwqsm = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return kik__xio or inq__ysq or ayae__qedk or rvt__npl or fdy__xwqsm
    if op == operator.truediv:
        pwnqq__jjswv = lhs in machine_ints and rhs in machine_ints
        kik__xio = lhs in types.real_domain and rhs in types.real_domain
        mpx__fapa = lhs in types.complex_domain and rhs in types.complex_domain
        inq__ysq = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        ayae__qedk = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        lms__nroft = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        rvt__npl = isinstance(lhs, types.NPTimedelta) and isinstance(rhs, (
            types.Integer, types.Float, types.NPTimedelta))
        fdy__xwqsm = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return (pwnqq__jjswv or kik__xio or mpx__fapa or inq__ysq or
            ayae__qedk or lms__nroft or rvt__npl or fdy__xwqsm)
    if op == operator.mod:
        pwnqq__jjswv = lhs in machine_ints and rhs in machine_ints
        kik__xio = lhs in types.real_domain and rhs in types.real_domain
        inq__ysq = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        ayae__qedk = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        fdy__xwqsm = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        return pwnqq__jjswv or kik__xio or inq__ysq or ayae__qedk or fdy__xwqsm
    if op == operator.add or op == operator.sub:
        aimx__qmqy = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        ltjom__wawpc = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        ggsxf__xzsn = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        zwb__spem = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        inq__ysq = isinstance(lhs, types.Integer) and isinstance(rhs, types
            .Integer)
        kik__xio = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        mpx__fapa = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        zkr__cfgkb = inq__ysq or kik__xio or mpx__fapa
        fdy__xwqsm = isinstance(lhs, types.Array) or isinstance(rhs, types.
            Array)
        khmdx__pix = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        tefoo__kjoet = isinstance(lhs, types.List) and isinstance(rhs,
            types.List)
        ybhrk__nyd = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        mvcz__wzg = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        seuf__rxfy = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        nyv__xhz = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        lubv__bqcp = ybhrk__nyd or mvcz__wzg or seuf__rxfy or nyv__xhz
        bwbbl__gnidh = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        yitz__quufm = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        tprt__wjw = bwbbl__gnidh or yitz__quufm
        nnrv__fmzw = lhs == types.NPTimedelta and rhs == types.NPDatetime
        zvzt__ihjh = (khmdx__pix or tefoo__kjoet or lubv__bqcp or tprt__wjw or
            nnrv__fmzw)
        kvu__fkq = op == operator.add and zvzt__ihjh
        return (aimx__qmqy or ltjom__wawpc or ggsxf__xzsn or zwb__spem or
            zkr__cfgkb or fdy__xwqsm or kvu__fkq)


def cmp_op_supported_by_numba(lhs, rhs):
    fdy__xwqsm = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    tefoo__kjoet = isinstance(lhs, types.ListType) and isinstance(rhs,
        types.ListType)
    aimx__qmqy = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    vcuo__fduom = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    bwbbl__gnidh = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    khmdx__pix = isinstance(lhs, types.BaseTuple) and isinstance(rhs, types
        .BaseTuple)
    zwb__spem = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    zkr__cfgkb = isinstance(lhs, types.Number) and isinstance(rhs, types.Number
        )
    oshb__kfwu = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    rijo__pdv = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    fuq__kro = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    zat__fxji = isinstance(lhs, types.EnumMember) and isinstance(rhs, types
        .EnumMember)
    hqnyw__orvhf = isinstance(lhs, types.Literal) and isinstance(rhs, types
        .Literal)
    return (tefoo__kjoet or aimx__qmqy or vcuo__fduom or bwbbl__gnidh or
        khmdx__pix or zwb__spem or zkr__cfgkb or oshb__kfwu or rijo__pdv or
        fuq__kro or fdy__xwqsm or zat__fxji or hqnyw__orvhf)


def raise_error_if_not_numba_supported(op, lhs, rhs):
    if arith_op_supported_by_numba(op, lhs, rhs):
        return
    raise BodoError(
        f'{op} operator not supported for data types {lhs} and {rhs}.')


def _install_series_and_or():
    for op in (operator.or_, operator.and_):
        infer_global(op)(SeriesAndOrTyper)
        lower_impl = lower_series_and_or(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)


_install_series_and_or()


def _install_cmp_ops():
    for op in (operator.lt, operator.eq, operator.ne, operator.ge, operator
        .gt, operator.le):
        infer_global(op)(SeriesCmpOpTemplate)
        lower_impl = series_cmp_op_lower(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)
        dtt__rljf = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(dtt__rljf)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        dtt__rljf = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(dtt__rljf)


install_arith_ops()
