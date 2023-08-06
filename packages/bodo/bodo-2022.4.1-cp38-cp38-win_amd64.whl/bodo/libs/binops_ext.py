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
        cgup__srjl = lhs.data if isinstance(lhs, SeriesType) else lhs
        frs__ocqtz = rhs.data if isinstance(rhs, SeriesType) else rhs
        if cgup__srjl in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and frs__ocqtz.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            cgup__srjl = frs__ocqtz.dtype
        elif frs__ocqtz in (bodo.pd_timestamp_type, bodo.pd_timedelta_type
            ) and cgup__srjl.dtype in (bodo.datetime64ns, bodo.timedelta64ns):
            frs__ocqtz = cgup__srjl.dtype
        sgq__frm = cgup__srjl, frs__ocqtz
        qcydb__jtxbl = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            oqiq__vkisa = self.context.resolve_function_type(self.key,
                sgq__frm, {}).return_type
        except Exception as gduk__nti:
            raise BodoError(qcydb__jtxbl)
        if is_overload_bool(oqiq__vkisa):
            raise BodoError(qcydb__jtxbl)
        nkpsf__irneo = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        taulb__lrmas = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        tkqb__kftrl = types.bool_
        palv__oipxl = SeriesType(tkqb__kftrl, oqiq__vkisa, nkpsf__irneo,
            taulb__lrmas)
        return palv__oipxl(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        onfdt__exyr = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if onfdt__exyr is None:
            onfdt__exyr = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, onfdt__exyr, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        cgup__srjl = lhs.data if isinstance(lhs, SeriesType) else lhs
        frs__ocqtz = rhs.data if isinstance(rhs, SeriesType) else rhs
        sgq__frm = cgup__srjl, frs__ocqtz
        qcydb__jtxbl = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            oqiq__vkisa = self.context.resolve_function_type(self.key,
                sgq__frm, {}).return_type
        except Exception as rug__qgiyt:
            raise BodoError(qcydb__jtxbl)
        nkpsf__irneo = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        taulb__lrmas = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        tkqb__kftrl = oqiq__vkisa.dtype
        palv__oipxl = SeriesType(tkqb__kftrl, oqiq__vkisa, nkpsf__irneo,
            taulb__lrmas)
        return palv__oipxl(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        onfdt__exyr = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if onfdt__exyr is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                onfdt__exyr = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, onfdt__exyr, sig, args)
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
            onfdt__exyr = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return onfdt__exyr(lhs, rhs)
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
            onfdt__exyr = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return onfdt__exyr(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    lcep__spj = lhs == datetime_timedelta_type and rhs == datetime_date_type
    bcai__dujn = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return lcep__spj or bcai__dujn


def add_timestamp(lhs, rhs):
    wpa__zomoq = lhs == pd_timestamp_type and is_timedelta_type(rhs)
    vtk__rsra = is_timedelta_type(lhs) and rhs == pd_timestamp_type
    return wpa__zomoq or vtk__rsra


def add_datetime_and_timedeltas(lhs, rhs):
    xmy__yhdp = [datetime_timedelta_type, pd_timedelta_type]
    xzmmt__zbx = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    jttj__vfm = lhs in xmy__yhdp and rhs in xmy__yhdp
    hnx__abz = (lhs == datetime_datetime_type and rhs in xmy__yhdp or rhs ==
        datetime_datetime_type and lhs in xmy__yhdp)
    return jttj__vfm or hnx__abz


def mul_string_arr_and_int(lhs, rhs):
    frs__ocqtz = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    cgup__srjl = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return frs__ocqtz or cgup__srjl


def mul_timedelta_and_int(lhs, rhs):
    lcep__spj = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    bcai__dujn = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return lcep__spj or bcai__dujn


def mul_date_offset_and_int(lhs, rhs):
    skl__yhmy = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    kaj__fqt = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return skl__yhmy or kaj__fqt


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    sfmoc__jyq = [datetime_datetime_type, pd_timestamp_type, datetime_date_type
        ]
    gzlko__kqqfr = [date_offset_type, month_begin_type, month_end_type,
        week_type]
    return rhs in gzlko__kqqfr and lhs in sfmoc__jyq


def sub_dt_index_and_timestamp(lhs, rhs):
    lhei__fuzlj = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_type
    swipw__rsgt = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_type
    return lhei__fuzlj or swipw__rsgt


def sub_dt_or_td(lhs, rhs):
    kkod__gpolw = lhs == datetime_date_type and rhs == datetime_timedelta_type
    wnj__zqmvq = lhs == datetime_date_type and rhs == datetime_date_type
    dxln__rje = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return kkod__gpolw or wnj__zqmvq or dxln__rje


def sub_datetime_and_timedeltas(lhs, rhs):
    kfv__gwwoq = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    iedc__afi = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return kfv__gwwoq or iedc__afi


def div_timedelta_and_int(lhs, rhs):
    jttj__vfm = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    iltwb__lcm = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return jttj__vfm or iltwb__lcm


def div_datetime_timedelta(lhs, rhs):
    jttj__vfm = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    iltwb__lcm = lhs == datetime_timedelta_type and rhs == types.int64
    return jttj__vfm or iltwb__lcm


def mod_timedeltas(lhs, rhs):
    nmbyv__nbygn = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    jiddo__sjg = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return nmbyv__nbygn or jiddo__sjg


def cmp_dt_index_to_string(lhs, rhs):
    lhei__fuzlj = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    swipw__rsgt = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return lhei__fuzlj or swipw__rsgt


def cmp_timestamp_or_date(lhs, rhs):
    usonw__blr = (lhs == pd_timestamp_type and rhs == bodo.hiframes.
        datetime_date_ext.datetime_date_type)
    lfxr__uurz = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        rhs == pd_timestamp_type)
    lye__xgud = lhs == pd_timestamp_type and rhs == pd_timestamp_type
    rvzkw__gksgf = lhs == pd_timestamp_type and rhs == bodo.datetime64ns
    ofu__nqqn = rhs == pd_timestamp_type and lhs == bodo.datetime64ns
    return usonw__blr or lfxr__uurz or lye__xgud or rvzkw__gksgf or ofu__nqqn


def cmp_timeseries(lhs, rhs):
    dnza__ktuu = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type or lhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    rysxr__zwuu = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type or rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_type)
    occt__vzvvy = dnza__ktuu or rysxr__zwuu
    msm__fpa = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    crduc__jnecc = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    rcwi__ssoak = msm__fpa or crduc__jnecc
    return occt__vzvvy or rcwi__ssoak


def cmp_timedeltas(lhs, rhs):
    jttj__vfm = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in jttj__vfm and rhs in jttj__vfm


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    lgzvy__tvsl = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_type]
    return lgzvy__tvsl


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    cxbni__fyzr = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    jrv__hgk = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    palyf__pyt = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    yqw__sjm = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return cxbni__fyzr or jrv__hgk or palyf__pyt or yqw__sjm


def args_td_and_int_array(lhs, rhs):
    onn__sloa = (isinstance(lhs, IntegerArrayType) or isinstance(lhs, types
        .Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance(
        rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    iptc__jgci = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return onn__sloa and iptc__jgci


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        bcai__dujn = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        lcep__spj = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        llmx__ygxha = bcai__dujn or lcep__spj
        sgqoi__llvb = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        qum__qox = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        orx__oox = sgqoi__llvb or qum__qox
        ojd__zpzra = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        pudm__taht = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        xbgai__aqsp = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        frh__gzu = ojd__zpzra or pudm__taht or xbgai__aqsp
        bxw__iusk = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        afjy__qmf = isinstance(lhs, tys) or isinstance(rhs, tys)
        ykafg__egil = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (llmx__ygxha or orx__oox or frh__gzu or bxw__iusk or
            afjy__qmf or ykafg__egil)
    if op == operator.pow:
        ztcmx__whj = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        laqr__zks = isinstance(lhs, types.Float) and isinstance(rhs, (types
            .IntegerLiteral, types.Float, types.Integer) or rhs in types.
            unsigned_domain or rhs in types.signed_domain)
        xbgai__aqsp = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        ykafg__egil = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return ztcmx__whj or laqr__zks or xbgai__aqsp or ykafg__egil
    if op == operator.floordiv:
        pudm__taht = lhs in types.real_domain and rhs in types.real_domain
        ojd__zpzra = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        vmujw__obj = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        jttj__vfm = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        ykafg__egil = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (pudm__taht or ojd__zpzra or vmujw__obj or jttj__vfm or
            ykafg__egil)
    if op == operator.truediv:
        msbk__alvyh = lhs in machine_ints and rhs in machine_ints
        pudm__taht = lhs in types.real_domain and rhs in types.real_domain
        xbgai__aqsp = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        ojd__zpzra = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        vmujw__obj = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        eil__zmzpk = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        jttj__vfm = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        ykafg__egil = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (msbk__alvyh or pudm__taht or xbgai__aqsp or ojd__zpzra or
            vmujw__obj or eil__zmzpk or jttj__vfm or ykafg__egil)
    if op == operator.mod:
        msbk__alvyh = lhs in machine_ints and rhs in machine_ints
        pudm__taht = lhs in types.real_domain and rhs in types.real_domain
        ojd__zpzra = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        vmujw__obj = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        ykafg__egil = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        return (msbk__alvyh or pudm__taht or ojd__zpzra or vmujw__obj or
            ykafg__egil)
    if op == operator.add or op == operator.sub:
        llmx__ygxha = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        enqf__aup = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        stu__qmlr = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        cahf__rncmb = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        ojd__zpzra = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        pudm__taht = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        xbgai__aqsp = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        frh__gzu = ojd__zpzra or pudm__taht or xbgai__aqsp
        ykafg__egil = isinstance(lhs, types.Array) or isinstance(rhs, types
            .Array)
        rvd__fxclp = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        bxw__iusk = isinstance(lhs, types.List) and isinstance(rhs, types.List)
        xfva__zol = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        wlncv__ayjvk = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs
            , types.UnicodeType)
        blbvl__zmis = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        wqz__acuj = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        yfunc__seq = xfva__zol or wlncv__ayjvk or blbvl__zmis or wqz__acuj
        orx__oox = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        njpnv__bwq = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        ctu__uilh = orx__oox or njpnv__bwq
        yxtyq__bpj = lhs == types.NPTimedelta and rhs == types.NPDatetime
        tal__tgpl = (rvd__fxclp or bxw__iusk or yfunc__seq or ctu__uilh or
            yxtyq__bpj)
        jfn__hopha = op == operator.add and tal__tgpl
        return (llmx__ygxha or enqf__aup or stu__qmlr or cahf__rncmb or
            frh__gzu or ykafg__egil or jfn__hopha)


def cmp_op_supported_by_numba(lhs, rhs):
    ykafg__egil = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    bxw__iusk = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    llmx__ygxha = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    lnsm__gbkc = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    orx__oox = isinstance(lhs, unicode_types) and isinstance(rhs, unicode_types
        )
    rvd__fxclp = isinstance(lhs, types.BaseTuple) and isinstance(rhs, types
        .BaseTuple)
    cahf__rncmb = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    frh__gzu = isinstance(lhs, types.Number) and isinstance(rhs, types.Number)
    ufep__penb = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    twg__mlvl = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    fgsg__bbpq = isinstance(lhs, types.DictType) and isinstance(rhs, types.
        DictType)
    mmfel__lry = isinstance(lhs, types.EnumMember) and isinstance(rhs,
        types.EnumMember)
    jjolh__igkiv = isinstance(lhs, types.Literal) and isinstance(rhs, types
        .Literal)
    return (bxw__iusk or llmx__ygxha or lnsm__gbkc or orx__oox or
        rvd__fxclp or cahf__rncmb or frh__gzu or ufep__penb or twg__mlvl or
        fgsg__bbpq or ykafg__egil or mmfel__lry or jjolh__igkiv)


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
        xmy__syoju = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(xmy__syoju)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        xmy__syoju = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(xmy__syoju)


install_arith_ops()
