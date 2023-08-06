"""Array implementation for string objects, which are usually immutable.
The characters are stored in a contingous data array, and an offsets array marks the
the individual strings. For example:
value:             ['a', 'bc', '', 'abc', None, 'bb']
data:              [a, b, c, a, b, c, b, b]
offsets:           [0, 1, 3, 3, 6, 6, 8]
"""
import glob
import operator
import numba
import numba.core.typing.typeof
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.unsafe.bytes import memcpy_region
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, pre_alloc_binary_array
from bodo.libs.str_ext import memcmp, string_type, unicode_to_utf8_and_len
from bodo.utils.typing import BodoArrayIterator, BodoError, decode_if_dict_array, is_list_like_index_type, is_overload_constant_int, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
use_pd_string_array = False
char_type = types.uint8
char_arr_type = types.Array(char_type, 1, 'C')
offset_arr_type = types.Array(offset_type, 1, 'C')
null_bitmap_arr_type = types.Array(types.uint8, 1, 'C')
data_ctypes_type = types.ArrayCTypes(char_arr_type)
offset_ctypes_type = types.ArrayCTypes(offset_arr_type)


class StringArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(StringArrayType, self).__init__(name='StringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    def copy(self):
        return StringArrayType()


string_array_type = StringArrayType()


@typeof_impl.register(pd.arrays.StringArray)
def typeof_string_array(val, c):
    return string_array_type


@register_model(BinaryArrayType)
@register_model(StringArrayType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        adqj__vidkb = ArrayItemArrayType(char_arr_type)
        ttsjl__hagtq = [('data', adqj__vidkb)]
        models.StructModel.__init__(self, dmm, fe_type, ttsjl__hagtq)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        whrus__ydr, = args
        sqpk__ifn = context.make_helper(builder, string_array_type)
        sqpk__ifn.data = whrus__ydr
        context.nrt.incref(builder, data_typ, whrus__ydr)
        return sqpk__ifn._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    uicgp__vhk = c.context.insert_const_string(c.builder.module, 'pandas')
    hwmyq__wjwkh = c.pyapi.import_module_noblock(uicgp__vhk)
    fuhay__cyk = c.pyapi.call_method(hwmyq__wjwkh, 'StringDtype', ())
    c.pyapi.decref(hwmyq__wjwkh)
    return fuhay__cyk


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        opo__zmfw = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs, rhs)
        if opo__zmfw is not None:
            return opo__zmfw
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                iofg__uuw = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(iofg__uuw)
                for i in numba.parfors.parfor.internal_prange(iofg__uuw):
                    if bodo.libs.array_kernels.isna(lhs, i
                        ) or bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_both
        if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

            def impl_left(lhs, rhs):
                numba.parfors.parfor.init_prange()
                iofg__uuw = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(iofg__uuw)
                for i in numba.parfors.parfor.internal_prange(iofg__uuw):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs)
                    out_arr[i] = val
                return out_arr
            return impl_left
        if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

            def impl_right(lhs, rhs):
                numba.parfors.parfor.init_prange()
                iofg__uuw = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(iofg__uuw)
                for i in numba.parfors.parfor.internal_prange(iofg__uuw):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs, rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_right
        raise_bodo_error(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_string_array_binary_op


def overload_add_operator_string_array(lhs, rhs):
    ejgsz__rpak = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    ptj__bjj = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and ptj__bjj or ejgsz__rpak and is_str_arr_type(rhs
        ):

        def impl_both(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j
                    ) or bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs[j]
            return out_arr
        return impl_both
    if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

        def impl_left(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs
            return out_arr
        return impl_left
    if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

        def impl_right(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(rhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs + rhs[j]
            return out_arr
        return impl_right


def overload_mul_operator_str_arr(lhs, rhs):
    if is_str_arr_type(lhs) and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] * rhs
            return out_arr
        return impl
    if isinstance(lhs, types.Integer) and is_str_arr_type(rhs):

        def impl(lhs, rhs):
            return rhs * lhs
        return impl


def _get_str_binary_arr_payload(context, builder, arr_value, arr_typ):
    assert arr_typ == string_array_type or arr_typ == binary_array_type
    tvt__cjtfn = context.make_helper(builder, arr_typ, arr_value)
    adqj__vidkb = ArrayItemArrayType(char_arr_type)
    bim__kvadl = _get_array_item_arr_payload(context, builder, adqj__vidkb,
        tvt__cjtfn.data)
    return bim__kvadl


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return bim__kvadl.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        zeb__sjn = context.make_helper(builder, offset_arr_type, bim__kvadl
            .offsets).data
        return _get_num_total_chars(builder, zeb__sjn, bim__kvadl.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        ppdov__mtsfr = context.make_helper(builder, offset_arr_type,
            bim__kvadl.offsets)
        dgu__cea = context.make_helper(builder, offset_ctypes_type)
        dgu__cea.data = builder.bitcast(ppdov__mtsfr.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        dgu__cea.meminfo = ppdov__mtsfr.meminfo
        fuhay__cyk = dgu__cea._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            fuhay__cyk)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        whrus__ydr = context.make_helper(builder, char_arr_type, bim__kvadl
            .data)
        dgu__cea = context.make_helper(builder, data_ctypes_type)
        dgu__cea.data = whrus__ydr.data
        dgu__cea.meminfo = whrus__ydr.meminfo
        fuhay__cyk = dgu__cea._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, fuhay__cyk
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        mjr__tvpa, ind = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            mjr__tvpa, sig.args[0])
        whrus__ydr = context.make_helper(builder, char_arr_type, bim__kvadl
            .data)
        dgu__cea = context.make_helper(builder, data_ctypes_type)
        dgu__cea.data = builder.gep(whrus__ydr.data, [ind])
        dgu__cea.meminfo = whrus__ydr.meminfo
        fuhay__cyk = dgu__cea._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, fuhay__cyk
            )
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        gmekp__seyp, ypugl__zixd, gdinz__oomrs, vcmjl__pljqz = args
        tko__mgb = builder.bitcast(builder.gep(gmekp__seyp, [ypugl__zixd]),
            lir.IntType(8).as_pointer())
        mskt__lxij = builder.bitcast(builder.gep(gdinz__oomrs, [
            vcmjl__pljqz]), lir.IntType(8).as_pointer())
        bslb__jjra = builder.load(mskt__lxij)
        builder.store(bslb__jjra, tko__mgb)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        wiz__wty = context.make_helper(builder, null_bitmap_arr_type,
            bim__kvadl.null_bitmap)
        dgu__cea = context.make_helper(builder, data_ctypes_type)
        dgu__cea.data = wiz__wty.data
        dgu__cea.meminfo = wiz__wty.meminfo
        fuhay__cyk = dgu__cea._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, fuhay__cyk
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        zeb__sjn = context.make_helper(builder, offset_arr_type, bim__kvadl
            .offsets).data
        return builder.load(builder.gep(zeb__sjn, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, bim__kvadl.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        msutq__olzax, ind = args
        if in_bitmap_typ == data_ctypes_type:
            dgu__cea = context.make_helper(builder, data_ctypes_type,
                msutq__olzax)
            msutq__olzax = dgu__cea.data
        return builder.load(builder.gep(msutq__olzax, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        msutq__olzax, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            dgu__cea = context.make_helper(builder, data_ctypes_type,
                msutq__olzax)
            msutq__olzax = dgu__cea.data
        builder.store(val, builder.gep(msutq__olzax, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        plubt__addb = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        scka__etzzk = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        jzwle__auqv = context.make_helper(builder, offset_arr_type,
            plubt__addb.offsets).data
        dfrmu__qudz = context.make_helper(builder, offset_arr_type,
            scka__etzzk.offsets).data
        uvv__lmc = context.make_helper(builder, char_arr_type, plubt__addb.data
            ).data
        ghqce__fgh = context.make_helper(builder, char_arr_type,
            scka__etzzk.data).data
        vmy__nesjx = context.make_helper(builder, null_bitmap_arr_type,
            plubt__addb.null_bitmap).data
        qtsaq__tzb = context.make_helper(builder, null_bitmap_arr_type,
            scka__etzzk.null_bitmap).data
        pdk__dvhx = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, dfrmu__qudz, jzwle__auqv, pdk__dvhx)
        cgutils.memcpy(builder, ghqce__fgh, uvv__lmc, builder.load(builder.
            gep(jzwle__auqv, [ind])))
        gtk__msv = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        vtwkt__eecgt = builder.lshr(gtk__msv, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, qtsaq__tzb, vmy__nesjx, vtwkt__eecgt)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        plubt__addb = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        scka__etzzk = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        jzwle__auqv = context.make_helper(builder, offset_arr_type,
            plubt__addb.offsets).data
        uvv__lmc = context.make_helper(builder, char_arr_type, plubt__addb.data
            ).data
        ghqce__fgh = context.make_helper(builder, char_arr_type,
            scka__etzzk.data).data
        num_total_chars = _get_num_total_chars(builder, jzwle__auqv,
            plubt__addb.n_arrays)
        cgutils.memcpy(builder, ghqce__fgh, uvv__lmc, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        plubt__addb = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        scka__etzzk = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        jzwle__auqv = context.make_helper(builder, offset_arr_type,
            plubt__addb.offsets).data
        dfrmu__qudz = context.make_helper(builder, offset_arr_type,
            scka__etzzk.offsets).data
        vmy__nesjx = context.make_helper(builder, null_bitmap_arr_type,
            plubt__addb.null_bitmap).data
        iofg__uuw = plubt__addb.n_arrays
        jpz__qums = context.get_constant(offset_type, 0)
        updd__jljz = cgutils.alloca_once_value(builder, jpz__qums)
        with cgutils.for_range(builder, iofg__uuw) as uec__ueq:
            rfhsr__acey = lower_is_na(context, builder, vmy__nesjx,
                uec__ueq.index)
            with cgutils.if_likely(builder, builder.not_(rfhsr__acey)):
                rvcw__vmo = builder.load(builder.gep(jzwle__auqv, [uec__ueq
                    .index]))
                mdaie__bqw = builder.load(updd__jljz)
                builder.store(rvcw__vmo, builder.gep(dfrmu__qudz, [mdaie__bqw])
                    )
                builder.store(builder.add(mdaie__bqw, lir.Constant(context.
                    get_value_type(offset_type), 1)), updd__jljz)
        mdaie__bqw = builder.load(updd__jljz)
        rvcw__vmo = builder.load(builder.gep(jzwle__auqv, [iofg__uuw]))
        builder.store(rvcw__vmo, builder.gep(dfrmu__qudz, [mdaie__bqw]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        ciee__ftkr, ind, str, pifbj__qoax = args
        ciee__ftkr = context.make_array(sig.args[0])(context, builder,
            ciee__ftkr)
        cce__qab = builder.gep(ciee__ftkr.data, [ind])
        cgutils.raw_memcpy(builder, cce__qab, str, pifbj__qoax, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        cce__qab, ind, etec__euwzj, pifbj__qoax = args
        cce__qab = builder.gep(cce__qab, [ind])
        cgutils.raw_memcpy(builder, cce__qab, etec__euwzj, pifbj__qoax, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    qzo__afdia = np.int64(getitem_str_offset(A, i))
    nzpcv__xdcok = np.int64(getitem_str_offset(A, i + 1))
    l = nzpcv__xdcok - qzo__afdia
    tic__vxc = get_data_ptr_ind(A, qzo__afdia)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(tic__vxc, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_copy(B, j, A, i):
    if j == 0:
        setitem_str_offset(B, 0, 0)
    jpocy__bml = getitem_str_offset(A, i)
    uprgd__lofz = getitem_str_offset(A, i + 1)
    wdin__dqa = uprgd__lofz - jpocy__bml
    nic__orx = getitem_str_offset(B, j)
    swtcx__wvm = nic__orx + wdin__dqa
    setitem_str_offset(B, j + 1, swtcx__wvm)
    if str_arr_is_na(A, i):
        str_arr_set_na(B, j)
    else:
        str_arr_set_not_na(B, j)
    if wdin__dqa != 0:
        whrus__ydr = B._data
        bodo.libs.array_item_arr_ext.ensure_data_capacity(whrus__ydr, np.
            int64(nic__orx), np.int64(swtcx__wvm))
        qoe__ngadh = get_data_ptr(B).data
        jfao__yzaue = get_data_ptr(A).data
        memcpy_region(qoe__ngadh, nic__orx, jfao__yzaue, jpocy__bml,
            wdin__dqa, 1)


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    iofg__uuw = len(str_arr)
    xexb__blbr = np.empty(iofg__uuw, np.bool_)
    for i in range(iofg__uuw):
        xexb__blbr[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return xexb__blbr


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            iofg__uuw = len(data)
            l = []
            for i in range(iofg__uuw):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        kzdg__myd = data.count
        fgye__ltw = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(kzdg__myd)]
        if is_overload_true(str_null_bools):
            fgye__ltw += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(kzdg__myd) if is_str_arr_type(data.types[i]) or data.
                types[i] == binary_array_type]
        pfo__amti = 'def f(data, str_null_bools=None):\n'
        pfo__amti += '  return ({}{})\n'.format(', '.join(fgye__ltw), ',' if
            kzdg__myd == 1 else '')
        udj__dtkt = {}
        exec(pfo__amti, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, udj__dtkt)
        nete__ytzsf = udj__dtkt['f']
        return nete__ytzsf
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                iofg__uuw = len(list_data)
                for i in range(iofg__uuw):
                    etec__euwzj = list_data[i]
                    str_arr[i] = etec__euwzj
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                iofg__uuw = len(list_data)
                for i in range(iofg__uuw):
                    etec__euwzj = list_data[i]
                    str_arr[i] = etec__euwzj
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        kzdg__myd = str_arr.count
        fpybf__ril = 0
        pfo__amti = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(kzdg__myd):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                pfo__amti += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, kzdg__myd + fpybf__ril))
                fpybf__ril += 1
            else:
                pfo__amti += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        pfo__amti += '  return\n'
        udj__dtkt = {}
        exec(pfo__amti, {'cp_str_list_to_array': cp_str_list_to_array},
            udj__dtkt)
        toul__ivovv = udj__dtkt['f']
        return toul__ivovv
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            iofg__uuw = len(str_list)
            str_arr = pre_alloc_string_array(iofg__uuw, -1)
            for i in range(iofg__uuw):
                etec__euwzj = str_list[i]
                str_arr[i] = etec__euwzj
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            iofg__uuw = len(A)
            esp__vxcp = 0
            for i in range(iofg__uuw):
                etec__euwzj = A[i]
                esp__vxcp += get_utf8_size(etec__euwzj)
            return esp__vxcp
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        iofg__uuw = len(arr)
        n_chars = num_total_chars(arr)
        jagzz__dor = pre_alloc_string_array(iofg__uuw, np.int64(n_chars))
        copy_str_arr_slice(jagzz__dor, arr, iofg__uuw)
        return jagzz__dor
    return copy_impl


@overload(len, no_unliteral=True)
def str_arr_len_overload(str_arr):
    if str_arr == string_array_type:

        def str_arr_len(str_arr):
            return str_arr.size
        return str_arr_len


@overload_attribute(StringArrayType, 'size')
def str_arr_size_overload(str_arr):
    return lambda str_arr: len(str_arr._data)


@overload_attribute(StringArrayType, 'shape')
def str_arr_shape_overload(str_arr):
    return lambda str_arr: (str_arr.size,)


@overload_attribute(StringArrayType, 'nbytes')
def str_arr_nbytes_overload(str_arr):
    return lambda str_arr: str_arr._data.nbytes


@overload_method(types.Array, 'tolist', no_unliteral=True)
@overload_method(StringArrayType, 'tolist', no_unliteral=True)
def overload_to_list(arr):
    return lambda arr: list(arr)


import llvmlite.binding as ll
from llvmlite import ir as lir
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('setitem_string_array', hstr_ext.setitem_string_array)
ll.add_symbol('is_na', hstr_ext.is_na)
ll.add_symbol('string_array_from_sequence', array_ext.
    string_array_from_sequence)
ll.add_symbol('pd_array_from_string_array', hstr_ext.pd_array_from_string_array
    )
ll.add_symbol('np_array_from_string_array', hstr_ext.np_array_from_string_array
    )
ll.add_symbol('convert_len_arr_to_offset32', hstr_ext.
    convert_len_arr_to_offset32)
ll.add_symbol('convert_len_arr_to_offset', hstr_ext.convert_len_arr_to_offset)
ll.add_symbol('set_string_array_range', hstr_ext.set_string_array_range)
ll.add_symbol('str_arr_to_int64', hstr_ext.str_arr_to_int64)
ll.add_symbol('str_arr_to_float64', hstr_ext.str_arr_to_float64)
ll.add_symbol('get_utf8_size', hstr_ext.get_utf8_size)
ll.add_symbol('print_str_arr', hstr_ext.print_str_arr)
ll.add_symbol('inplace_int64_to_str', hstr_ext.inplace_int64_to_str)
inplace_int64_to_str = types.ExternalFunction('inplace_int64_to_str', types
    .void(types.voidptr, types.int64, types.int64))
convert_len_arr_to_offset32 = types.ExternalFunction(
    'convert_len_arr_to_offset32', types.void(types.voidptr, types.intp))
convert_len_arr_to_offset = types.ExternalFunction('convert_len_arr_to_offset',
    types.void(types.voidptr, types.voidptr, types.intp))
setitem_string_array = types.ExternalFunction('setitem_string_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, offset_type, offset_type, types.intp))
_get_utf8_size = types.ExternalFunction('get_utf8_size', types.intp(types.
    voidptr, types.intp, offset_type))
_print_str_arr = types.ExternalFunction('print_str_arr', types.void(types.
    uint64, types.uint64, types.CPointer(offset_type), types.CPointer(
    char_type)))


@numba.generated_jit(nopython=True)
def empty_str_arr(in_seq):
    pfo__amti = 'def f(in_seq):\n'
    pfo__amti += '    n_strs = len(in_seq)\n'
    pfo__amti += '    A = pre_alloc_string_array(n_strs, -1)\n'
    pfo__amti += '    return A\n'
    udj__dtkt = {}
    exec(pfo__amti, {'pre_alloc_string_array': pre_alloc_string_array},
        udj__dtkt)
    rioh__vsoud = udj__dtkt['f']
    return rioh__vsoud


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        avnlg__xvd = 'pre_alloc_binary_array'
    else:
        avnlg__xvd = 'pre_alloc_string_array'
    pfo__amti = 'def f(in_seq):\n'
    pfo__amti += '    n_strs = len(in_seq)\n'
    pfo__amti += f'    A = {avnlg__xvd}(n_strs, -1)\n'
    pfo__amti += '    for i in range(n_strs):\n'
    pfo__amti += '        A[i] = in_seq[i]\n'
    pfo__amti += '    return A\n'
    udj__dtkt = {}
    exec(pfo__amti, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, udj__dtkt)
    rioh__vsoud = udj__dtkt['f']
    return rioh__vsoud


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        fazlp__hqahv = builder.add(bim__kvadl.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        zavzr__hpu = builder.lshr(lir.Constant(lir.IntType(64), offset_type
            .bitwidth), lir.Constant(lir.IntType(64), 3))
        vtwkt__eecgt = builder.mul(fazlp__hqahv, zavzr__hpu)
        aecgz__uqu = context.make_array(offset_arr_type)(context, builder,
            bim__kvadl.offsets).data
        cgutils.memset(builder, aecgz__uqu, vtwkt__eecgt, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        osh__vrtw = bim__kvadl.n_arrays
        vtwkt__eecgt = builder.lshr(builder.add(osh__vrtw, lir.Constant(lir
            .IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        pjvd__qjjm = context.make_array(null_bitmap_arr_type)(context,
            builder, bim__kvadl.null_bitmap).data
        cgutils.memset(builder, pjvd__qjjm, vtwkt__eecgt, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@numba.njit
def pre_alloc_string_array(n_strs, n_chars):
    if n_chars is None:
        n_chars = -1
    str_arr = init_str_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_strs), (np.int64(n_chars),),
        char_arr_type))
    if n_chars == 0:
        set_all_offsets_to_0(str_arr)
    return str_arr


@register_jitable
def gen_na_str_array_lens(n_strs, total_len, len_arr):
    str_arr = pre_alloc_string_array(n_strs, total_len)
    set_bitmap_all_NA(str_arr)
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    tvds__pnjfu = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        pdcck__ludb = len(len_arr)
        for i in range(pdcck__ludb):
            offsets[i] = tvds__pnjfu
            tvds__pnjfu += len_arr[i]
        offsets[pdcck__ludb] = tvds__pnjfu
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    ath__qkd = i // 8
    uktd__svc = getitem_str_bitmap(bits, ath__qkd)
    uktd__svc ^= np.uint8(-np.uint8(bit_is_set) ^ uktd__svc) & kBitmask[i % 8]
    setitem_str_bitmap(bits, ath__qkd, uktd__svc)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    ckaf__sdqge = get_null_bitmap_ptr(out_str_arr)
    jnc__yllr = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        blmh__mjft = get_bit_bitmap(jnc__yllr, j)
        set_bit_to(ckaf__sdqge, out_start + j, blmh__mjft)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, mjr__tvpa, sct__rsm, nvfkn__fplgo = args
        plubt__addb = _get_str_binary_arr_payload(context, builder,
            mjr__tvpa, string_array_type)
        scka__etzzk = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        jzwle__auqv = context.make_helper(builder, offset_arr_type,
            plubt__addb.offsets).data
        dfrmu__qudz = context.make_helper(builder, offset_arr_type,
            scka__etzzk.offsets).data
        uvv__lmc = context.make_helper(builder, char_arr_type, plubt__addb.data
            ).data
        ghqce__fgh = context.make_helper(builder, char_arr_type,
            scka__etzzk.data).data
        num_total_chars = _get_num_total_chars(builder, jzwle__auqv,
            plubt__addb.n_arrays)
        dfm__pipr = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        dxvtz__bzjhd = cgutils.get_or_insert_function(builder.module,
            dfm__pipr, name='set_string_array_range')
        builder.call(dxvtz__bzjhd, [dfrmu__qudz, ghqce__fgh, jzwle__auqv,
            uvv__lmc, sct__rsm, nvfkn__fplgo, plubt__addb.n_arrays,
            num_total_chars])
        wkupk__djknv = context.typing_context.resolve_value_type(
            copy_nulls_range)
        prs__kfsc = wkupk__djknv.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        hbxp__plne = context.get_function(wkupk__djknv, prs__kfsc)
        hbxp__plne(builder, (out_arr, mjr__tvpa, sct__rsm))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    qacpo__osqd = c.context.make_helper(c.builder, typ, val)
    adqj__vidkb = ArrayItemArrayType(char_arr_type)
    bim__kvadl = _get_array_item_arr_payload(c.context, c.builder,
        adqj__vidkb, qacpo__osqd.data)
    dubh__bpfx = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    jvjt__xfbu = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        jvjt__xfbu = 'pd_array_from_string_array'
    dfm__pipr = lir.FunctionType(c.context.get_argument_type(types.pyobject
        ), [lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
        lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
        IntType(32)])
    ego__swx = cgutils.get_or_insert_function(c.builder.module, dfm__pipr,
        name=jvjt__xfbu)
    zeb__sjn = c.context.make_array(offset_arr_type)(c.context, c.builder,
        bim__kvadl.offsets).data
    tic__vxc = c.context.make_array(char_arr_type)(c.context, c.builder,
        bim__kvadl.data).data
    pjvd__qjjm = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, bim__kvadl.null_bitmap).data
    arr = c.builder.call(ego__swx, [bim__kvadl.n_arrays, zeb__sjn, tic__vxc,
        pjvd__qjjm, dubh__bpfx])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        pjvd__qjjm = context.make_array(null_bitmap_arr_type)(context,
            builder, bim__kvadl.null_bitmap).data
        uhvrw__ves = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        nqiqt__rldax = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        uktd__svc = builder.load(builder.gep(pjvd__qjjm, [uhvrw__ves],
            inbounds=True))
        wnxyk__zuenz = lir.ArrayType(lir.IntType(8), 8)
        clevv__jawp = cgutils.alloca_once_value(builder, lir.Constant(
            wnxyk__zuenz, (1, 2, 4, 8, 16, 32, 64, 128)))
        smc__ipjxy = builder.load(builder.gep(clevv__jawp, [lir.Constant(
            lir.IntType(64), 0), nqiqt__rldax], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(uktd__svc,
            smc__ipjxy), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        uhvrw__ves = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        nqiqt__rldax = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        pjvd__qjjm = context.make_array(null_bitmap_arr_type)(context,
            builder, bim__kvadl.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, bim__kvadl.
            offsets).data
        obfj__nlgp = builder.gep(pjvd__qjjm, [uhvrw__ves], inbounds=True)
        uktd__svc = builder.load(obfj__nlgp)
        wnxyk__zuenz = lir.ArrayType(lir.IntType(8), 8)
        clevv__jawp = cgutils.alloca_once_value(builder, lir.Constant(
            wnxyk__zuenz, (1, 2, 4, 8, 16, 32, 64, 128)))
        smc__ipjxy = builder.load(builder.gep(clevv__jawp, [lir.Constant(
            lir.IntType(64), 0), nqiqt__rldax], inbounds=True))
        smc__ipjxy = builder.xor(smc__ipjxy, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(uktd__svc, smc__ipjxy), obfj__nlgp)
        if str_arr_typ == string_array_type:
            cpg__ltle = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            ejxss__fjaf = builder.icmp_unsigned('!=', cpg__ltle, bim__kvadl
                .n_arrays)
            with builder.if_then(ejxss__fjaf):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [cpg__ltle]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        uhvrw__ves = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        nqiqt__rldax = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        pjvd__qjjm = context.make_array(null_bitmap_arr_type)(context,
            builder, bim__kvadl.null_bitmap).data
        obfj__nlgp = builder.gep(pjvd__qjjm, [uhvrw__ves], inbounds=True)
        uktd__svc = builder.load(obfj__nlgp)
        wnxyk__zuenz = lir.ArrayType(lir.IntType(8), 8)
        clevv__jawp = cgutils.alloca_once_value(builder, lir.Constant(
            wnxyk__zuenz, (1, 2, 4, 8, 16, 32, 64, 128)))
        smc__ipjxy = builder.load(builder.gep(clevv__jawp, [lir.Constant(
            lir.IntType(64), 0), nqiqt__rldax], inbounds=True))
        builder.store(builder.or_(uktd__svc, smc__ipjxy), obfj__nlgp)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        vtwkt__eecgt = builder.udiv(builder.add(bim__kvadl.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        pjvd__qjjm = context.make_array(null_bitmap_arr_type)(context,
            builder, bim__kvadl.null_bitmap).data
        cgutils.memset(builder, pjvd__qjjm, vtwkt__eecgt, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    zfavv__ynb = context.make_helper(builder, string_array_type, str_arr)
    adqj__vidkb = ArrayItemArrayType(char_arr_type)
    xxlzt__okfq = context.make_helper(builder, adqj__vidkb, zfavv__ynb.data)
    dcv__vmdjo = ArrayItemArrayPayloadType(adqj__vidkb)
    xomgx__upazl = context.nrt.meminfo_data(builder, xxlzt__okfq.meminfo)
    vxbmk__rwah = builder.bitcast(xomgx__upazl, context.get_value_type(
        dcv__vmdjo).as_pointer())
    return vxbmk__rwah


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        cup__oid, nit__bvko = args
        hvte__fatb = _get_str_binary_arr_data_payload_ptr(context, builder,
            nit__bvko)
        vnkw__igphc = _get_str_binary_arr_data_payload_ptr(context, builder,
            cup__oid)
        xgl__ubbeh = _get_str_binary_arr_payload(context, builder,
            nit__bvko, sig.args[1])
        ezvb__pqtac = _get_str_binary_arr_payload(context, builder,
            cup__oid, sig.args[0])
        context.nrt.incref(builder, char_arr_type, xgl__ubbeh.data)
        context.nrt.incref(builder, offset_arr_type, xgl__ubbeh.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, xgl__ubbeh.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, ezvb__pqtac.data)
        context.nrt.decref(builder, offset_arr_type, ezvb__pqtac.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, ezvb__pqtac.
            null_bitmap)
        builder.store(builder.load(hvte__fatb), vnkw__igphc)
        return context.get_dummy_value()
    return types.none(to_arr_typ, from_arr_typ), codegen


dummy_use = numba.njit(lambda a: None)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_utf8_size(s):
    if isinstance(s, types.StringLiteral):
        l = len(s.literal_value.encode())
        return lambda s: l

    def impl(s):
        if s is None:
            return 0
        s = bodo.utils.indexing.unoptional(s)
        if s._is_ascii == 1:
            return len(s)
        iofg__uuw = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return iofg__uuw
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, cce__qab, yybm__infrd = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder, arr, sig
            .args[0])
        offsets = context.make_helper(builder, offset_arr_type, bim__kvadl.
            offsets).data
        data = context.make_helper(builder, char_arr_type, bim__kvadl.data
            ).data
        dfm__pipr = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        szvfe__xfkkb = cgutils.get_or_insert_function(builder.module,
            dfm__pipr, name='setitem_string_array')
        ylmm__mwlok = context.get_constant(types.int32, -1)
        qfru__yze = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, bim__kvadl
            .n_arrays)
        builder.call(szvfe__xfkkb, [offsets, data, num_total_chars, builder
            .extract_value(cce__qab, 0), yybm__infrd, ylmm__mwlok,
            qfru__yze, ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    dfm__pipr = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64)])
    mpsc__cel = cgutils.get_or_insert_function(builder.module, dfm__pipr,
        name='is_na')
    return builder.call(mpsc__cel, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        tko__mgb, mskt__lxij, kzdg__myd, dllsz__ziitg = args
        cgutils.raw_memcpy(builder, tko__mgb, mskt__lxij, kzdg__myd,
            dllsz__ziitg)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.voidptr, types.intp, types.intp
        ), codegen


@numba.njit
def print_str_arr(arr):
    _print_str_arr(num_strings(arr), num_total_chars(arr), get_offset_ptr(
        arr), get_data_ptr(arr))


def inplace_eq(A, i, val):
    return A[i] == val


@overload(inplace_eq)
def inplace_eq_overload(A, ind, val):

    def impl(A, ind, val):
        vqnfv__yxu, uoh__cypk = unicode_to_utf8_and_len(val)
        ogmbi__nrfqp = getitem_str_offset(A, ind)
        oep__kxia = getitem_str_offset(A, ind + 1)
        bacf__mxcph = oep__kxia - ogmbi__nrfqp
        if bacf__mxcph != uoh__cypk:
            return False
        cce__qab = get_data_ptr_ind(A, ogmbi__nrfqp)
        return memcmp(cce__qab, vqnfv__yxu, uoh__cypk) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        ogmbi__nrfqp = getitem_str_offset(A, ind)
        bacf__mxcph = bodo.libs.str_ext.int_to_str_len(val)
        hygy__fwnt = ogmbi__nrfqp + bacf__mxcph
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            ogmbi__nrfqp, hygy__fwnt)
        cce__qab = get_data_ptr_ind(A, ogmbi__nrfqp)
        inplace_int64_to_str(cce__qab, bacf__mxcph, val)
        setitem_str_offset(A, ind + 1, ogmbi__nrfqp + bacf__mxcph)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        cce__qab, = args
        sbf__rwt = context.insert_const_string(builder.module, '<NA>')
        yrj__htn = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, cce__qab, sbf__rwt, yrj__htn, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    bgg__nwdg = len('<NA>')

    def impl(A, ind):
        ogmbi__nrfqp = getitem_str_offset(A, ind)
        hygy__fwnt = ogmbi__nrfqp + bgg__nwdg
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            ogmbi__nrfqp, hygy__fwnt)
        cce__qab = get_data_ptr_ind(A, ogmbi__nrfqp)
        inplace_set_NA_str(cce__qab)
        setitem_str_offset(A, ind + 1, ogmbi__nrfqp + bgg__nwdg)
        str_arr_set_not_na(A, ind)
    return impl


@overload(operator.getitem, no_unliteral=True)
def str_arr_getitem_int(A, ind):
    if A != string_array_type:
        return
    if isinstance(ind, types.Integer):

        def str_arr_getitem_impl(A, ind):
            if ind < 0:
                ind += A.size
            ogmbi__nrfqp = getitem_str_offset(A, ind)
            oep__kxia = getitem_str_offset(A, ind + 1)
            yybm__infrd = oep__kxia - ogmbi__nrfqp
            cce__qab = get_data_ptr_ind(A, ogmbi__nrfqp)
            xqb__jgij = decode_utf8(cce__qab, yybm__infrd)
            return xqb__jgij
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            iofg__uuw = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(iofg__uuw):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            qoe__ngadh = get_data_ptr(out_arr).data
            jfao__yzaue = get_data_ptr(A).data
            fpybf__ril = 0
            mdaie__bqw = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(iofg__uuw):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    lvki__nbe = get_str_arr_item_length(A, i)
                    if lvki__nbe == 1:
                        copy_single_char(qoe__ngadh, mdaie__bqw,
                            jfao__yzaue, getitem_str_offset(A, i))
                    else:
                        memcpy_region(qoe__ngadh, mdaie__bqw, jfao__yzaue,
                            getitem_str_offset(A, i), lvki__nbe, 1)
                    mdaie__bqw += lvki__nbe
                    setitem_str_offset(out_arr, fpybf__ril + 1, mdaie__bqw)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, fpybf__ril)
                    else:
                        str_arr_set_not_na(out_arr, fpybf__ril)
                    fpybf__ril += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            iofg__uuw = len(ind)
            out_arr = pre_alloc_string_array(iofg__uuw, -1)
            fpybf__ril = 0
            for i in range(iofg__uuw):
                etec__euwzj = A[ind[i]]
                out_arr[fpybf__ril] = etec__euwzj
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, fpybf__ril)
                fpybf__ril += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            iofg__uuw = len(A)
            uhl__wwmy = numba.cpython.unicode._normalize_slice(ind, iofg__uuw)
            zqxa__vrc = numba.cpython.unicode._slice_span(uhl__wwmy)
            if uhl__wwmy.step == 1:
                ogmbi__nrfqp = getitem_str_offset(A, uhl__wwmy.start)
                oep__kxia = getitem_str_offset(A, uhl__wwmy.stop)
                n_chars = oep__kxia - ogmbi__nrfqp
                jagzz__dor = pre_alloc_string_array(zqxa__vrc, np.int64(
                    n_chars))
                for i in range(zqxa__vrc):
                    jagzz__dor[i] = A[uhl__wwmy.start + i]
                    if str_arr_is_na(A, uhl__wwmy.start + i):
                        str_arr_set_na(jagzz__dor, i)
                return jagzz__dor
            else:
                jagzz__dor = pre_alloc_string_array(zqxa__vrc, -1)
                for i in range(zqxa__vrc):
                    jagzz__dor[i] = A[uhl__wwmy.start + i * uhl__wwmy.step]
                    if str_arr_is_na(A, uhl__wwmy.start + i * uhl__wwmy.step):
                        str_arr_set_na(jagzz__dor, i)
                return jagzz__dor
        return str_arr_slice_impl
    raise BodoError(
        f'getitem for StringArray with indexing type {ind} not supported.')


dummy_use = numba.njit(lambda a: None)


@overload(operator.setitem)
def str_arr_setitem(A, idx, val):
    if A != string_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    cwuv__tckq = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(cwuv__tckq)
        issnt__zklcp = 4

        def impl_scalar(A, idx, val):
            cgdm__zei = (val._length if val._is_ascii else issnt__zklcp *
                val._length)
            whrus__ydr = A._data
            ogmbi__nrfqp = np.int64(getitem_str_offset(A, idx))
            hygy__fwnt = ogmbi__nrfqp + cgdm__zei
            bodo.libs.array_item_arr_ext.ensure_data_capacity(whrus__ydr,
                ogmbi__nrfqp, hygy__fwnt)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                hygy__fwnt, val._data, val._length, val._kind, val.
                _is_ascii, idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                uhl__wwmy = numba.cpython.unicode._normalize_slice(idx, len(A))
                qzo__afdia = uhl__wwmy.start
                whrus__ydr = A._data
                ogmbi__nrfqp = np.int64(getitem_str_offset(A, qzo__afdia))
                hygy__fwnt = ogmbi__nrfqp + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(whrus__ydr,
                    ogmbi__nrfqp, hygy__fwnt)
                set_string_array_range(A, val, qzo__afdia, ogmbi__nrfqp)
                wzlxv__wnpv = 0
                for i in range(uhl__wwmy.start, uhl__wwmy.stop, uhl__wwmy.step
                    ):
                    if str_arr_is_na(val, wzlxv__wnpv):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    wzlxv__wnpv += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                igm__bgnfp = str_list_to_array(val)
                A[idx] = igm__bgnfp
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                uhl__wwmy = numba.cpython.unicode._normalize_slice(idx, len(A))
                for i in range(uhl__wwmy.start, uhl__wwmy.stop, uhl__wwmy.step
                    ):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(cwuv__tckq)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                iofg__uuw = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(iofg__uuw, -1)
                for i in numba.parfors.parfor.internal_prange(iofg__uuw):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        out_arr[i] = val
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_scalar
        elif val == string_array_type or isinstance(val, types.Array
            ) and isinstance(val.dtype, types.UnicodeCharSeq):

            def impl_bool_arr(A, idx, val):
                iofg__uuw = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(iofg__uuw, -1)
                utfqb__cakwb = 0
                for i in numba.parfors.parfor.internal_prange(iofg__uuw):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, utfqb__cakwb):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, utfqb__cakwb)
                        else:
                            out_arr[i] = str(val[utfqb__cakwb])
                        utfqb__cakwb += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(cwuv__tckq)
    raise BodoError(cwuv__tckq)


@overload_attribute(StringArrayType, 'dtype')
def overload_str_arr_dtype(A):
    return lambda A: pd.StringDtype()


@overload_attribute(StringArrayType, 'ndim')
def overload_str_arr_ndim(A):
    return lambda A: 1


@overload_method(StringArrayType, 'astype', no_unliteral=True)
def overload_str_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "StringArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.Function) and dtype.key[0] == str:
        return lambda A, dtype, copy=True: A
    zxrq__behhl = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(zxrq__behhl, (types.Float, types.Integer)
        ) and zxrq__behhl not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(zxrq__behhl, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            iofg__uuw = len(A)
            B = np.empty(iofg__uuw, zxrq__behhl)
            for i in numba.parfors.parfor.internal_prange(iofg__uuw):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif zxrq__behhl == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            iofg__uuw = len(A)
            B = np.empty(iofg__uuw, zxrq__behhl)
            for i in numba.parfors.parfor.internal_prange(iofg__uuw):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif zxrq__behhl == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            iofg__uuw = len(A)
            B = np.empty(iofg__uuw, zxrq__behhl)
            for i in numba.parfors.parfor.internal_prange(iofg__uuw):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            iofg__uuw = len(A)
            B = np.empty(iofg__uuw, zxrq__behhl)
            for i in numba.parfors.parfor.internal_prange(iofg__uuw):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        cce__qab, yybm__infrd = args
        mafv__ynybn = context.get_python_api(builder)
        ypn__iehzd = mafv__ynybn.string_from_string_and_size(cce__qab,
            yybm__infrd)
        jpeq__tamx = mafv__ynybn.to_native_value(string_type, ypn__iehzd).value
        jfoh__kocz = cgutils.create_struct_proxy(string_type)(context,
            builder, jpeq__tamx)
        jfoh__kocz.hash = jfoh__kocz.hash.type(-1)
        mafv__ynybn.decref(ypn__iehzd)
        return jfoh__kocz._getvalue()
    return string_type(types.voidptr, types.intp), codegen


def get_arr_data_ptr(arr, ind):
    return arr


@overload(get_arr_data_ptr, no_unliteral=True)
def overload_get_arr_data_ptr(arr, ind):
    assert isinstance(types.unliteral(ind), types.Integer)
    if isinstance(arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(arr, ind):
            return bodo.hiframes.split_impl.get_c_arr_ptr(arr._data.ctypes, ind
                )
        return impl_int
    assert isinstance(arr, types.Array)

    def impl_np(arr, ind):
        return bodo.hiframes.split_impl.get_c_arr_ptr(arr.ctypes, ind)
    return impl_np


def set_to_numeric_out_na_err(out_arr, out_ind, err_code):
    pass


@overload(set_to_numeric_out_na_err)
def set_to_numeric_out_na_err_overload(out_arr, out_ind, err_code):
    if isinstance(out_arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(out_arr, out_ind, err_code):
            bodo.libs.int_arr_ext.set_bit_to_arr(out_arr._null_bitmap,
                out_ind, 0 if err_code == -1 else 1)
        return impl_int
    assert isinstance(out_arr, types.Array)
    if isinstance(out_arr.dtype, types.Float):

        def impl_np(out_arr, out_ind, err_code):
            if err_code == -1:
                out_arr[out_ind] = np.nan
        return impl_np
    return lambda out_arr, out_ind, err_code: None


@numba.njit(no_cpython_wrapper=True)
def str_arr_item_to_numeric(out_arr, out_ind, str_arr, ind):
    str_arr = decode_if_dict_array(str_arr)
    err_code = _str_arr_item_to_numeric(get_arr_data_ptr(out_arr, out_ind),
        str_arr, ind, out_arr.dtype)
    set_to_numeric_out_na_err(out_arr, out_ind, err_code)


@intrinsic
def _str_arr_item_to_numeric(typingctx, out_ptr_t, str_arr_t, ind_t,
    out_dtype_t=None):
    assert str_arr_t == string_array_type, '_str_arr_item_to_numeric: str arr expected'
    assert ind_t == types.int64, '_str_arr_item_to_numeric: integer index expected'

    def codegen(context, builder, sig, args):
        mcpdm__jyn, arr, ind, gcp__zpe = args
        bim__kvadl = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, bim__kvadl.
            offsets).data
        data = context.make_helper(builder, char_arr_type, bim__kvadl.data
            ).data
        dfm__pipr = lir.FunctionType(lir.IntType(32), [mcpdm__jyn.type, lir
            .IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        our__mne = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            our__mne = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        zst__nsbbi = cgutils.get_or_insert_function(builder.module,
            dfm__pipr, our__mne)
        return builder.call(zst__nsbbi, [mcpdm__jyn, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    dubh__bpfx = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    dfm__pipr = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer(), lir.IntType(32)])
    gazh__nhfj = cgutils.get_or_insert_function(c.builder.module, dfm__pipr,
        name='string_array_from_sequence')
    vfjp__aupt = c.builder.call(gazh__nhfj, [val, dubh__bpfx])
    adqj__vidkb = ArrayItemArrayType(char_arr_type)
    xxlzt__okfq = c.context.make_helper(c.builder, adqj__vidkb)
    xxlzt__okfq.meminfo = vfjp__aupt
    zfavv__ynb = c.context.make_helper(c.builder, typ)
    whrus__ydr = xxlzt__okfq._getvalue()
    zfavv__ynb.data = whrus__ydr
    denw__oxok = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(zfavv__ynb._getvalue(), is_error=denw__oxok)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    iofg__uuw = len(pyval)
    mdaie__bqw = 0
    idod__niw = np.empty(iofg__uuw + 1, np_offset_type)
    glhv__dmoiz = []
    zrjuq__kte = np.empty(iofg__uuw + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        idod__niw[i] = mdaie__bqw
        dhw__ycdt = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(zrjuq__kte, i, int(not dhw__ycdt))
        if dhw__ycdt:
            continue
        wofaf__ebsbx = list(s.encode()) if isinstance(s, str) else list(s)
        glhv__dmoiz.extend(wofaf__ebsbx)
        mdaie__bqw += len(wofaf__ebsbx)
    idod__niw[iofg__uuw] = mdaie__bqw
    wizg__vzj = np.array(glhv__dmoiz, np.uint8)
    pyr__oqzi = context.get_constant(types.int64, iofg__uuw)
    bolxb__gawf = context.get_constant_generic(builder, char_arr_type,
        wizg__vzj)
    lex__ypnjv = context.get_constant_generic(builder, offset_arr_type,
        idod__niw)
    ttrg__fyj = context.get_constant_generic(builder, null_bitmap_arr_type,
        zrjuq__kte)
    bim__kvadl = lir.Constant.literal_struct([pyr__oqzi, bolxb__gawf,
        lex__ypnjv, ttrg__fyj])
    bim__kvadl = cgutils.global_constant(builder, '.const.payload', bim__kvadl
        ).bitcast(cgutils.voidptr_t)
    xec__uywni = context.get_constant(types.int64, -1)
    ntv__eqptz = context.get_constant_null(types.voidptr)
    soybr__znbum = lir.Constant.literal_struct([xec__uywni, ntv__eqptz,
        ntv__eqptz, bim__kvadl, xec__uywni])
    soybr__znbum = cgutils.global_constant(builder, '.const.meminfo',
        soybr__znbum).bitcast(cgutils.voidptr_t)
    whrus__ydr = lir.Constant.literal_struct([soybr__znbum])
    zfavv__ynb = lir.Constant.literal_struct([whrus__ydr])
    return zfavv__ynb


def pre_alloc_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_str_arr_ext_pre_alloc_string_array
    ) = pre_alloc_str_arr_equiv


@overload(glob.glob, no_unliteral=True)
def overload_glob_glob(pathname, recursive=False):

    def _glob_glob_impl(pathname, recursive=False):
        with numba.objmode(l='list_str_type'):
            l = glob.glob(pathname, recursive=recursive)
        return l
    return _glob_glob_impl
