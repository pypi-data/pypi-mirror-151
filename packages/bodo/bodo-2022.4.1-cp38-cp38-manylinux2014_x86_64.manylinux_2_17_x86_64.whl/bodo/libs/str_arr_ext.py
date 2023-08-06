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
        gxjx__ozp = ArrayItemArrayType(char_arr_type)
        uhwy__ppbgy = [('data', gxjx__ozp)]
        models.StructModel.__init__(self, dmm, fe_type, uhwy__ppbgy)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        mxvy__yyn, = args
        gbvi__lnjd = context.make_helper(builder, string_array_type)
        gbvi__lnjd.data = mxvy__yyn
        context.nrt.incref(builder, data_typ, mxvy__yyn)
        return gbvi__lnjd._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    dyox__bzqfd = c.context.insert_const_string(c.builder.module, 'pandas')
    maz__rea = c.pyapi.import_module_noblock(dyox__bzqfd)
    begqb__jiajc = c.pyapi.call_method(maz__rea, 'StringDtype', ())
    c.pyapi.decref(maz__rea)
    return begqb__jiajc


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        doiy__orqa = bodo.libs.dict_arr_ext.get_binary_op_overload(op, lhs, rhs
            )
        if doiy__orqa is not None:
            return doiy__orqa
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                henl__hunsw = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(henl__hunsw)
                for i in numba.parfors.parfor.internal_prange(henl__hunsw):
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
                henl__hunsw = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(henl__hunsw)
                for i in numba.parfors.parfor.internal_prange(henl__hunsw):
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
                henl__hunsw = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(henl__hunsw)
                for i in numba.parfors.parfor.internal_prange(henl__hunsw):
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
    ovts__qier = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    nfs__bzcji = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and nfs__bzcji or ovts__qier and is_str_arr_type(
        rhs):

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
    bbbjl__kbz = context.make_helper(builder, arr_typ, arr_value)
    gxjx__ozp = ArrayItemArrayType(char_arr_type)
    jrl__sqon = _get_array_item_arr_payload(context, builder, gxjx__ozp,
        bbbjl__kbz.data)
    return jrl__sqon


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return jrl__sqon.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        smqic__uzxcb = context.make_helper(builder, offset_arr_type,
            jrl__sqon.offsets).data
        return _get_num_total_chars(builder, smqic__uzxcb, jrl__sqon.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        hhu__zfgfx = context.make_helper(builder, offset_arr_type,
            jrl__sqon.offsets)
        wscyo__ckxk = context.make_helper(builder, offset_ctypes_type)
        wscyo__ckxk.data = builder.bitcast(hhu__zfgfx.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        wscyo__ckxk.meminfo = hhu__zfgfx.meminfo
        begqb__jiajc = wscyo__ckxk._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            begqb__jiajc)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        mxvy__yyn = context.make_helper(builder, char_arr_type, jrl__sqon.data)
        wscyo__ckxk = context.make_helper(builder, data_ctypes_type)
        wscyo__ckxk.data = mxvy__yyn.data
        wscyo__ckxk.meminfo = mxvy__yyn.meminfo
        begqb__jiajc = wscyo__ckxk._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            begqb__jiajc)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        jqsew__ufgn, ind = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            jqsew__ufgn, sig.args[0])
        mxvy__yyn = context.make_helper(builder, char_arr_type, jrl__sqon.data)
        wscyo__ckxk = context.make_helper(builder, data_ctypes_type)
        wscyo__ckxk.data = builder.gep(mxvy__yyn.data, [ind])
        wscyo__ckxk.meminfo = mxvy__yyn.meminfo
        begqb__jiajc = wscyo__ckxk._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            begqb__jiajc)
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        mfu__dfknj, ybopk__amc, xfzs__dleu, zpxwy__iyebn = args
        thn__gnz = builder.bitcast(builder.gep(mfu__dfknj, [ybopk__amc]),
            lir.IntType(8).as_pointer())
        rlgpx__rvh = builder.bitcast(builder.gep(xfzs__dleu, [zpxwy__iyebn]
            ), lir.IntType(8).as_pointer())
        iwnbh__nsyhv = builder.load(rlgpx__rvh)
        builder.store(iwnbh__nsyhv, thn__gnz)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        nhe__kcig = context.make_helper(builder, null_bitmap_arr_type,
            jrl__sqon.null_bitmap)
        wscyo__ckxk = context.make_helper(builder, data_ctypes_type)
        wscyo__ckxk.data = nhe__kcig.data
        wscyo__ckxk.meminfo = nhe__kcig.meminfo
        begqb__jiajc = wscyo__ckxk._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type,
            begqb__jiajc)
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        smqic__uzxcb = context.make_helper(builder, offset_arr_type,
            jrl__sqon.offsets).data
        return builder.load(builder.gep(smqic__uzxcb, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, jrl__sqon.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        ixk__pfo, ind = args
        if in_bitmap_typ == data_ctypes_type:
            wscyo__ckxk = context.make_helper(builder, data_ctypes_type,
                ixk__pfo)
            ixk__pfo = wscyo__ckxk.data
        return builder.load(builder.gep(ixk__pfo, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        ixk__pfo, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            wscyo__ckxk = context.make_helper(builder, data_ctypes_type,
                ixk__pfo)
            ixk__pfo = wscyo__ckxk.data
        builder.store(val, builder.gep(ixk__pfo, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        dykl__pqqxy = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        lusnt__ori = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        kiky__zyt = context.make_helper(builder, offset_arr_type,
            dykl__pqqxy.offsets).data
        hnh__iqvik = context.make_helper(builder, offset_arr_type,
            lusnt__ori.offsets).data
        ucx__yrof = context.make_helper(builder, char_arr_type, dykl__pqqxy
            .data).data
        yejzy__eopxm = context.make_helper(builder, char_arr_type,
            lusnt__ori.data).data
        ulrzb__cvb = context.make_helper(builder, null_bitmap_arr_type,
            dykl__pqqxy.null_bitmap).data
        ugg__qdpjr = context.make_helper(builder, null_bitmap_arr_type,
            lusnt__ori.null_bitmap).data
        rxfur__nwe = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, hnh__iqvik, kiky__zyt, rxfur__nwe)
        cgutils.memcpy(builder, yejzy__eopxm, ucx__yrof, builder.load(
            builder.gep(kiky__zyt, [ind])))
        nyt__vbs = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        mkm__qtcs = builder.lshr(nyt__vbs, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, ugg__qdpjr, ulrzb__cvb, mkm__qtcs)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        dykl__pqqxy = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        lusnt__ori = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        kiky__zyt = context.make_helper(builder, offset_arr_type,
            dykl__pqqxy.offsets).data
        ucx__yrof = context.make_helper(builder, char_arr_type, dykl__pqqxy
            .data).data
        yejzy__eopxm = context.make_helper(builder, char_arr_type,
            lusnt__ori.data).data
        num_total_chars = _get_num_total_chars(builder, kiky__zyt,
            dykl__pqqxy.n_arrays)
        cgutils.memcpy(builder, yejzy__eopxm, ucx__yrof, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        dykl__pqqxy = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        lusnt__ori = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        kiky__zyt = context.make_helper(builder, offset_arr_type,
            dykl__pqqxy.offsets).data
        hnh__iqvik = context.make_helper(builder, offset_arr_type,
            lusnt__ori.offsets).data
        ulrzb__cvb = context.make_helper(builder, null_bitmap_arr_type,
            dykl__pqqxy.null_bitmap).data
        henl__hunsw = dykl__pqqxy.n_arrays
        pui__qdc = context.get_constant(offset_type, 0)
        arsd__oov = cgutils.alloca_once_value(builder, pui__qdc)
        with cgutils.for_range(builder, henl__hunsw) as fbcr__dlma:
            yfhm__pufs = lower_is_na(context, builder, ulrzb__cvb,
                fbcr__dlma.index)
            with cgutils.if_likely(builder, builder.not_(yfhm__pufs)):
                fmej__rta = builder.load(builder.gep(kiky__zyt, [fbcr__dlma
                    .index]))
                iqhu__znd = builder.load(arsd__oov)
                builder.store(fmej__rta, builder.gep(hnh__iqvik, [iqhu__znd]))
                builder.store(builder.add(iqhu__znd, lir.Constant(context.
                    get_value_type(offset_type), 1)), arsd__oov)
        iqhu__znd = builder.load(arsd__oov)
        fmej__rta = builder.load(builder.gep(kiky__zyt, [henl__hunsw]))
        builder.store(fmej__rta, builder.gep(hnh__iqvik, [iqhu__znd]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        bzv__lato, ind, str, hdwzr__ydtk = args
        bzv__lato = context.make_array(sig.args[0])(context, builder, bzv__lato
            )
        pbgle__wsm = builder.gep(bzv__lato.data, [ind])
        cgutils.raw_memcpy(builder, pbgle__wsm, str, hdwzr__ydtk, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        pbgle__wsm, ind, winhe__wajz, hdwzr__ydtk = args
        pbgle__wsm = builder.gep(pbgle__wsm, [ind])
        cgutils.raw_memcpy(builder, pbgle__wsm, winhe__wajz, hdwzr__ydtk, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_length(A, i):
    return np.int64(getitem_str_offset(A, i + 1) - getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    ubo__afsi = np.int64(getitem_str_offset(A, i))
    xna__cag = np.int64(getitem_str_offset(A, i + 1))
    l = xna__cag - ubo__afsi
    ttdlr__rkv = get_data_ptr_ind(A, ubo__afsi)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(ttdlr__rkv, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_copy(B, j, A, i):
    if j == 0:
        setitem_str_offset(B, 0, 0)
    ffqvj__uhkg = getitem_str_offset(A, i)
    czrh__vprm = getitem_str_offset(A, i + 1)
    mgcqn__lcyww = czrh__vprm - ffqvj__uhkg
    gwb__bbhw = getitem_str_offset(B, j)
    yrca__jbu = gwb__bbhw + mgcqn__lcyww
    setitem_str_offset(B, j + 1, yrca__jbu)
    if str_arr_is_na(A, i):
        str_arr_set_na(B, j)
    else:
        str_arr_set_not_na(B, j)
    if mgcqn__lcyww != 0:
        mxvy__yyn = B._data
        bodo.libs.array_item_arr_ext.ensure_data_capacity(mxvy__yyn, np.
            int64(gwb__bbhw), np.int64(yrca__jbu))
        goy__mjd = get_data_ptr(B).data
        tvn__dvw = get_data_ptr(A).data
        memcpy_region(goy__mjd, gwb__bbhw, tvn__dvw, ffqvj__uhkg,
            mgcqn__lcyww, 1)


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    henl__hunsw = len(str_arr)
    gph__oslp = np.empty(henl__hunsw, np.bool_)
    for i in range(henl__hunsw):
        gph__oslp[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return gph__oslp


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            henl__hunsw = len(data)
            l = []
            for i in range(henl__hunsw):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        oqi__gqjyb = data.count
        pjytc__manj = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(oqi__gqjyb)]
        if is_overload_true(str_null_bools):
            pjytc__manj += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(oqi__gqjyb) if is_str_arr_type(data.types[i]) or data
                .types[i] == binary_array_type]
        vdzzs__bxrtz = 'def f(data, str_null_bools=None):\n'
        vdzzs__bxrtz += '  return ({}{})\n'.format(', '.join(pjytc__manj), 
            ',' if oqi__gqjyb == 1 else '')
        hlt__inm = {}
        exec(vdzzs__bxrtz, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, hlt__inm)
        rmehe__ghjxs = hlt__inm['f']
        return rmehe__ghjxs
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                henl__hunsw = len(list_data)
                for i in range(henl__hunsw):
                    winhe__wajz = list_data[i]
                    str_arr[i] = winhe__wajz
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                henl__hunsw = len(list_data)
                for i in range(henl__hunsw):
                    winhe__wajz = list_data[i]
                    str_arr[i] = winhe__wajz
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        oqi__gqjyb = str_arr.count
        ptqn__ijbq = 0
        vdzzs__bxrtz = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(oqi__gqjyb):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                vdzzs__bxrtz += (
                    """  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])
"""
                    .format(i, i, oqi__gqjyb + ptqn__ijbq))
                ptqn__ijbq += 1
            else:
                vdzzs__bxrtz += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        vdzzs__bxrtz += '  return\n'
        hlt__inm = {}
        exec(vdzzs__bxrtz, {'cp_str_list_to_array': cp_str_list_to_array},
            hlt__inm)
        ayj__vne = hlt__inm['f']
        return ayj__vne
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            henl__hunsw = len(str_list)
            str_arr = pre_alloc_string_array(henl__hunsw, -1)
            for i in range(henl__hunsw):
                winhe__wajz = str_list[i]
                str_arr[i] = winhe__wajz
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            henl__hunsw = len(A)
            wiab__hma = 0
            for i in range(henl__hunsw):
                winhe__wajz = A[i]
                wiab__hma += get_utf8_size(winhe__wajz)
            return wiab__hma
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        henl__hunsw = len(arr)
        n_chars = num_total_chars(arr)
        nxfj__psc = pre_alloc_string_array(henl__hunsw, np.int64(n_chars))
        copy_str_arr_slice(nxfj__psc, arr, henl__hunsw)
        return nxfj__psc
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
    vdzzs__bxrtz = 'def f(in_seq):\n'
    vdzzs__bxrtz += '    n_strs = len(in_seq)\n'
    vdzzs__bxrtz += '    A = pre_alloc_string_array(n_strs, -1)\n'
    vdzzs__bxrtz += '    return A\n'
    hlt__inm = {}
    exec(vdzzs__bxrtz, {'pre_alloc_string_array': pre_alloc_string_array},
        hlt__inm)
    kpnei__kxouv = hlt__inm['f']
    return kpnei__kxouv


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        jecpf__xlw = 'pre_alloc_binary_array'
    else:
        jecpf__xlw = 'pre_alloc_string_array'
    vdzzs__bxrtz = 'def f(in_seq):\n'
    vdzzs__bxrtz += '    n_strs = len(in_seq)\n'
    vdzzs__bxrtz += f'    A = {jecpf__xlw}(n_strs, -1)\n'
    vdzzs__bxrtz += '    for i in range(n_strs):\n'
    vdzzs__bxrtz += '        A[i] = in_seq[i]\n'
    vdzzs__bxrtz += '    return A\n'
    hlt__inm = {}
    exec(vdzzs__bxrtz, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, hlt__inm)
    kpnei__kxouv = hlt__inm['f']
    return kpnei__kxouv


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        zgr__tklas = builder.add(jrl__sqon.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        huu__mnj = builder.lshr(lir.Constant(lir.IntType(64), offset_type.
            bitwidth), lir.Constant(lir.IntType(64), 3))
        mkm__qtcs = builder.mul(zgr__tklas, huu__mnj)
        ivocw__tqsda = context.make_array(offset_arr_type)(context, builder,
            jrl__sqon.offsets).data
        cgutils.memset(builder, ivocw__tqsda, mkm__qtcs, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        sit__hcws = jrl__sqon.n_arrays
        mkm__qtcs = builder.lshr(builder.add(sit__hcws, lir.Constant(lir.
            IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        bxubk__pog = context.make_array(null_bitmap_arr_type)(context,
            builder, jrl__sqon.null_bitmap).data
        cgutils.memset(builder, bxubk__pog, mkm__qtcs, 0)
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
    merq__ouczl = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        bqhjy__kywv = len(len_arr)
        for i in range(bqhjy__kywv):
            offsets[i] = merq__ouczl
            merq__ouczl += len_arr[i]
        offsets[bqhjy__kywv] = merq__ouczl
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    uvl__sdobi = i // 8
    azqw__njqzm = getitem_str_bitmap(bits, uvl__sdobi)
    azqw__njqzm ^= np.uint8(-np.uint8(bit_is_set) ^ azqw__njqzm) & kBitmask[
        i % 8]
    setitem_str_bitmap(bits, uvl__sdobi, azqw__njqzm)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    gghc__uybf = get_null_bitmap_ptr(out_str_arr)
    pzf__juu = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        xywmi__kvvb = get_bit_bitmap(pzf__juu, j)
        set_bit_to(gghc__uybf, out_start + j, xywmi__kvvb)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, jqsew__ufgn, jcfuv__nhdgd, yzo__insxm = args
        dykl__pqqxy = _get_str_binary_arr_payload(context, builder,
            jqsew__ufgn, string_array_type)
        lusnt__ori = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        kiky__zyt = context.make_helper(builder, offset_arr_type,
            dykl__pqqxy.offsets).data
        hnh__iqvik = context.make_helper(builder, offset_arr_type,
            lusnt__ori.offsets).data
        ucx__yrof = context.make_helper(builder, char_arr_type, dykl__pqqxy
            .data).data
        yejzy__eopxm = context.make_helper(builder, char_arr_type,
            lusnt__ori.data).data
        num_total_chars = _get_num_total_chars(builder, kiky__zyt,
            dykl__pqqxy.n_arrays)
        nhhkd__cugzc = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        gdyeb__xbs = cgutils.get_or_insert_function(builder.module,
            nhhkd__cugzc, name='set_string_array_range')
        builder.call(gdyeb__xbs, [hnh__iqvik, yejzy__eopxm, kiky__zyt,
            ucx__yrof, jcfuv__nhdgd, yzo__insxm, dykl__pqqxy.n_arrays,
            num_total_chars])
        kinqa__ahvo = context.typing_context.resolve_value_type(
            copy_nulls_range)
        mbdzi__egw = kinqa__ahvo.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        jbhr__qklys = context.get_function(kinqa__ahvo, mbdzi__egw)
        jbhr__qklys(builder, (out_arr, jqsew__ufgn, jcfuv__nhdgd))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    ijnel__cgnm = c.context.make_helper(c.builder, typ, val)
    gxjx__ozp = ArrayItemArrayType(char_arr_type)
    jrl__sqon = _get_array_item_arr_payload(c.context, c.builder, gxjx__ozp,
        ijnel__cgnm.data)
    wral__hft = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    kvy__funrl = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        kvy__funrl = 'pd_array_from_string_array'
    nhhkd__cugzc = lir.FunctionType(c.context.get_argument_type(types.
        pyobject), [lir.IntType(64), lir.IntType(offset_type.bitwidth).
        as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
        as_pointer(), lir.IntType(32)])
    poajj__dyvwi = cgutils.get_or_insert_function(c.builder.module,
        nhhkd__cugzc, name=kvy__funrl)
    smqic__uzxcb = c.context.make_array(offset_arr_type)(c.context, c.
        builder, jrl__sqon.offsets).data
    ttdlr__rkv = c.context.make_array(char_arr_type)(c.context, c.builder,
        jrl__sqon.data).data
    bxubk__pog = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, jrl__sqon.null_bitmap).data
    arr = c.builder.call(poajj__dyvwi, [jrl__sqon.n_arrays, smqic__uzxcb,
        ttdlr__rkv, bxubk__pog, wral__hft])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        bxubk__pog = context.make_array(null_bitmap_arr_type)(context,
            builder, jrl__sqon.null_bitmap).data
        ffcv__row = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        leiq__oqz = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        azqw__njqzm = builder.load(builder.gep(bxubk__pog, [ffcv__row],
            inbounds=True))
        vrhh__xhglq = lir.ArrayType(lir.IntType(8), 8)
        ksx__namqi = cgutils.alloca_once_value(builder, lir.Constant(
            vrhh__xhglq, (1, 2, 4, 8, 16, 32, 64, 128)))
        kto__jkjey = builder.load(builder.gep(ksx__namqi, [lir.Constant(lir
            .IntType(64), 0), leiq__oqz], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(azqw__njqzm,
            kto__jkjey), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ffcv__row = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        leiq__oqz = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        bxubk__pog = context.make_array(null_bitmap_arr_type)(context,
            builder, jrl__sqon.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, jrl__sqon.
            offsets).data
        jat__iwm = builder.gep(bxubk__pog, [ffcv__row], inbounds=True)
        azqw__njqzm = builder.load(jat__iwm)
        vrhh__xhglq = lir.ArrayType(lir.IntType(8), 8)
        ksx__namqi = cgutils.alloca_once_value(builder, lir.Constant(
            vrhh__xhglq, (1, 2, 4, 8, 16, 32, 64, 128)))
        kto__jkjey = builder.load(builder.gep(ksx__namqi, [lir.Constant(lir
            .IntType(64), 0), leiq__oqz], inbounds=True))
        kto__jkjey = builder.xor(kto__jkjey, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(azqw__njqzm, kto__jkjey), jat__iwm)
        if str_arr_typ == string_array_type:
            iue__kqwx = builder.add(ind, lir.Constant(lir.IntType(64), 1))
            qncv__swbep = builder.icmp_unsigned('!=', iue__kqwx, jrl__sqon.
                n_arrays)
            with builder.if_then(qncv__swbep):
                builder.store(builder.load(builder.gep(offsets, [ind])),
                    builder.gep(offsets, [iue__kqwx]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        ffcv__row = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        leiq__oqz = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        bxubk__pog = context.make_array(null_bitmap_arr_type)(context,
            builder, jrl__sqon.null_bitmap).data
        jat__iwm = builder.gep(bxubk__pog, [ffcv__row], inbounds=True)
        azqw__njqzm = builder.load(jat__iwm)
        vrhh__xhglq = lir.ArrayType(lir.IntType(8), 8)
        ksx__namqi = cgutils.alloca_once_value(builder, lir.Constant(
            vrhh__xhglq, (1, 2, 4, 8, 16, 32, 64, 128)))
        kto__jkjey = builder.load(builder.gep(ksx__namqi, [lir.Constant(lir
            .IntType(64), 0), leiq__oqz], inbounds=True))
        builder.store(builder.or_(azqw__njqzm, kto__jkjey), jat__iwm)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        mkm__qtcs = builder.udiv(builder.add(jrl__sqon.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        bxubk__pog = context.make_array(null_bitmap_arr_type)(context,
            builder, jrl__sqon.null_bitmap).data
        cgutils.memset(builder, bxubk__pog, mkm__qtcs, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    fblb__qsqb = context.make_helper(builder, string_array_type, str_arr)
    gxjx__ozp = ArrayItemArrayType(char_arr_type)
    hmd__jos = context.make_helper(builder, gxjx__ozp, fblb__qsqb.data)
    orhv__rlly = ArrayItemArrayPayloadType(gxjx__ozp)
    goyb__anjp = context.nrt.meminfo_data(builder, hmd__jos.meminfo)
    aoemi__kli = builder.bitcast(goyb__anjp, context.get_value_type(
        orhv__rlly).as_pointer())
    return aoemi__kli


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        lem__iwfw, hvrhj__ftciq = args
        ebk__yqx = _get_str_binary_arr_data_payload_ptr(context, builder,
            hvrhj__ftciq)
        gts__jpi = _get_str_binary_arr_data_payload_ptr(context, builder,
            lem__iwfw)
        wbm__nxjh = _get_str_binary_arr_payload(context, builder,
            hvrhj__ftciq, sig.args[1])
        fnf__dso = _get_str_binary_arr_payload(context, builder, lem__iwfw,
            sig.args[0])
        context.nrt.incref(builder, char_arr_type, wbm__nxjh.data)
        context.nrt.incref(builder, offset_arr_type, wbm__nxjh.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, wbm__nxjh.null_bitmap
            )
        context.nrt.decref(builder, char_arr_type, fnf__dso.data)
        context.nrt.decref(builder, offset_arr_type, fnf__dso.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, fnf__dso.null_bitmap)
        builder.store(builder.load(ebk__yqx), gts__jpi)
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
        henl__hunsw = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return henl__hunsw
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, pbgle__wsm, fcuh__mvf = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder, arr, sig.
            args[0])
        offsets = context.make_helper(builder, offset_arr_type, jrl__sqon.
            offsets).data
        data = context.make_helper(builder, char_arr_type, jrl__sqon.data).data
        nhhkd__cugzc = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        dsdoe__bhbht = cgutils.get_or_insert_function(builder.module,
            nhhkd__cugzc, name='setitem_string_array')
        esqkl__uvgh = context.get_constant(types.int32, -1)
        cep__quo = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, jrl__sqon.
            n_arrays)
        builder.call(dsdoe__bhbht, [offsets, data, num_total_chars, builder
            .extract_value(pbgle__wsm, 0), fcuh__mvf, esqkl__uvgh, cep__quo,
            ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    nhhkd__cugzc = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
        as_pointer(), lir.IntType(64)])
    ddnjo__xpkj = cgutils.get_or_insert_function(builder.module,
        nhhkd__cugzc, name='is_na')
    return builder.call(ddnjo__xpkj, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        thn__gnz, rlgpx__rvh, oqi__gqjyb, vrss__fcro = args
        cgutils.raw_memcpy(builder, thn__gnz, rlgpx__rvh, oqi__gqjyb,
            vrss__fcro)
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
        qzf__tzzp, vac__iuyp = unicode_to_utf8_and_len(val)
        uyz__stqew = getitem_str_offset(A, ind)
        adtnv__gqz = getitem_str_offset(A, ind + 1)
        jtt__slxno = adtnv__gqz - uyz__stqew
        if jtt__slxno != vac__iuyp:
            return False
        pbgle__wsm = get_data_ptr_ind(A, uyz__stqew)
        return memcmp(pbgle__wsm, qzf__tzzp, vac__iuyp) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        uyz__stqew = getitem_str_offset(A, ind)
        jtt__slxno = bodo.libs.str_ext.int_to_str_len(val)
        wkus__bhy = uyz__stqew + jtt__slxno
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            uyz__stqew, wkus__bhy)
        pbgle__wsm = get_data_ptr_ind(A, uyz__stqew)
        inplace_int64_to_str(pbgle__wsm, jtt__slxno, val)
        setitem_str_offset(A, ind + 1, uyz__stqew + jtt__slxno)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        pbgle__wsm, = args
        knd__rdr = context.insert_const_string(builder.module, '<NA>')
        cgxn__yvlp = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, pbgle__wsm, knd__rdr, cgxn__yvlp, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    hopnj__ithu = len('<NA>')

    def impl(A, ind):
        uyz__stqew = getitem_str_offset(A, ind)
        wkus__bhy = uyz__stqew + hopnj__ithu
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            uyz__stqew, wkus__bhy)
        pbgle__wsm = get_data_ptr_ind(A, uyz__stqew)
        inplace_set_NA_str(pbgle__wsm)
        setitem_str_offset(A, ind + 1, uyz__stqew + hopnj__ithu)
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
            uyz__stqew = getitem_str_offset(A, ind)
            adtnv__gqz = getitem_str_offset(A, ind + 1)
            fcuh__mvf = adtnv__gqz - uyz__stqew
            pbgle__wsm = get_data_ptr_ind(A, uyz__stqew)
            eilkf__kavl = decode_utf8(pbgle__wsm, fcuh__mvf)
            return eilkf__kavl
        return str_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_ndarray(ind)
            henl__hunsw = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(henl__hunsw):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            goy__mjd = get_data_ptr(out_arr).data
            tvn__dvw = get_data_ptr(A).data
            ptqn__ijbq = 0
            iqhu__znd = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(henl__hunsw):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    icw__vczy = get_str_arr_item_length(A, i)
                    if icw__vczy == 1:
                        copy_single_char(goy__mjd, iqhu__znd, tvn__dvw,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(goy__mjd, iqhu__znd, tvn__dvw,
                            getitem_str_offset(A, i), icw__vczy, 1)
                    iqhu__znd += icw__vczy
                    setitem_str_offset(out_arr, ptqn__ijbq + 1, iqhu__znd)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, ptqn__ijbq)
                    else:
                        str_arr_set_not_na(out_arr, ptqn__ijbq)
                    ptqn__ijbq += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            henl__hunsw = len(ind)
            out_arr = pre_alloc_string_array(henl__hunsw, -1)
            ptqn__ijbq = 0
            for i in range(henl__hunsw):
                winhe__wajz = A[ind[i]]
                out_arr[ptqn__ijbq] = winhe__wajz
                if str_arr_is_na(A, ind[i]):
                    str_arr_set_na(out_arr, ptqn__ijbq)
                ptqn__ijbq += 1
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            henl__hunsw = len(A)
            hpllr__jhcku = numba.cpython.unicode._normalize_slice(ind,
                henl__hunsw)
            oseko__ipjl = numba.cpython.unicode._slice_span(hpllr__jhcku)
            if hpllr__jhcku.step == 1:
                uyz__stqew = getitem_str_offset(A, hpllr__jhcku.start)
                adtnv__gqz = getitem_str_offset(A, hpllr__jhcku.stop)
                n_chars = adtnv__gqz - uyz__stqew
                nxfj__psc = pre_alloc_string_array(oseko__ipjl, np.int64(
                    n_chars))
                for i in range(oseko__ipjl):
                    nxfj__psc[i] = A[hpllr__jhcku.start + i]
                    if str_arr_is_na(A, hpllr__jhcku.start + i):
                        str_arr_set_na(nxfj__psc, i)
                return nxfj__psc
            else:
                nxfj__psc = pre_alloc_string_array(oseko__ipjl, -1)
                for i in range(oseko__ipjl):
                    nxfj__psc[i] = A[hpllr__jhcku.start + i * hpllr__jhcku.step
                        ]
                    if str_arr_is_na(A, hpllr__jhcku.start + i *
                        hpllr__jhcku.step):
                        str_arr_set_na(nxfj__psc, i)
                return nxfj__psc
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
    von__jku = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(von__jku)
        fnugv__gnhxw = 4

        def impl_scalar(A, idx, val):
            jopr__tazal = (val._length if val._is_ascii else fnugv__gnhxw *
                val._length)
            mxvy__yyn = A._data
            uyz__stqew = np.int64(getitem_str_offset(A, idx))
            wkus__bhy = uyz__stqew + jopr__tazal
            bodo.libs.array_item_arr_ext.ensure_data_capacity(mxvy__yyn,
                uyz__stqew, wkus__bhy)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                wkus__bhy, val._data, val._length, val._kind, val._is_ascii,
                idx)
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                hpllr__jhcku = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                ubo__afsi = hpllr__jhcku.start
                mxvy__yyn = A._data
                uyz__stqew = np.int64(getitem_str_offset(A, ubo__afsi))
                wkus__bhy = uyz__stqew + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(mxvy__yyn,
                    uyz__stqew, wkus__bhy)
                set_string_array_range(A, val, ubo__afsi, uyz__stqew)
                vvipw__hsb = 0
                for i in range(hpllr__jhcku.start, hpllr__jhcku.stop,
                    hpllr__jhcku.step):
                    if str_arr_is_na(val, vvipw__hsb):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    vvipw__hsb += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                hesbu__rrujb = str_list_to_array(val)
                A[idx] = hesbu__rrujb
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                hpllr__jhcku = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                for i in range(hpllr__jhcku.start, hpllr__jhcku.stop,
                    hpllr__jhcku.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(von__jku)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                henl__hunsw = len(A)
                idx = bodo.utils.conversion.coerce_to_ndarray(idx)
                out_arr = pre_alloc_string_array(henl__hunsw, -1)
                for i in numba.parfors.parfor.internal_prange(henl__hunsw):
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
                henl__hunsw = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(henl__hunsw, -1)
                vncho__sdicc = 0
                for i in numba.parfors.parfor.internal_prange(henl__hunsw):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, vncho__sdicc):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, vncho__sdicc)
                        else:
                            out_arr[i] = str(val[vncho__sdicc])
                        vncho__sdicc += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(von__jku)
    raise BodoError(von__jku)


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
    zblz__yhsp = parse_dtype(dtype, 'StringArray.astype')
    if not isinstance(zblz__yhsp, (types.Float, types.Integer)
        ) and zblz__yhsp not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(zblz__yhsp, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            henl__hunsw = len(A)
            B = np.empty(henl__hunsw, zblz__yhsp)
            for i in numba.parfors.parfor.internal_prange(henl__hunsw):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif zblz__yhsp == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            henl__hunsw = len(A)
            B = np.empty(henl__hunsw, zblz__yhsp)
            for i in numba.parfors.parfor.internal_prange(henl__hunsw):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif zblz__yhsp == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            henl__hunsw = len(A)
            B = np.empty(henl__hunsw, zblz__yhsp)
            for i in numba.parfors.parfor.internal_prange(henl__hunsw):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            henl__hunsw = len(A)
            B = np.empty(henl__hunsw, zblz__yhsp)
            for i in numba.parfors.parfor.internal_prange(henl__hunsw):
                B[i] = int(A[i])
            return B
        return impl_int


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        pbgle__wsm, fcuh__mvf = args
        nhl__trgew = context.get_python_api(builder)
        vtnrg__anzhd = nhl__trgew.string_from_string_and_size(pbgle__wsm,
            fcuh__mvf)
        dwdg__ekl = nhl__trgew.to_native_value(string_type, vtnrg__anzhd).value
        izp__dpz = cgutils.create_struct_proxy(string_type)(context,
            builder, dwdg__ekl)
        izp__dpz.hash = izp__dpz.hash.type(-1)
        nhl__trgew.decref(vtnrg__anzhd)
        return izp__dpz._getvalue()
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
        fzky__fty, arr, ind, dyeu__bjzi = args
        jrl__sqon = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, jrl__sqon.
            offsets).data
        data = context.make_helper(builder, char_arr_type, jrl__sqon.data).data
        nhhkd__cugzc = lir.FunctionType(lir.IntType(32), [fzky__fty.type,
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        eodjo__xckd = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            eodjo__xckd = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        inui__ari = cgutils.get_or_insert_function(builder.module,
            nhhkd__cugzc, eodjo__xckd)
        return builder.call(inui__ari, [fzky__fty, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    wral__hft = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    nhhkd__cugzc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(32)])
    ddnp__robr = cgutils.get_or_insert_function(c.builder.module,
        nhhkd__cugzc, name='string_array_from_sequence')
    lnku__ltjfu = c.builder.call(ddnp__robr, [val, wral__hft])
    gxjx__ozp = ArrayItemArrayType(char_arr_type)
    hmd__jos = c.context.make_helper(c.builder, gxjx__ozp)
    hmd__jos.meminfo = lnku__ltjfu
    fblb__qsqb = c.context.make_helper(c.builder, typ)
    mxvy__yyn = hmd__jos._getvalue()
    fblb__qsqb.data = mxvy__yyn
    rdgah__rhae = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(fblb__qsqb._getvalue(), is_error=rdgah__rhae)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    henl__hunsw = len(pyval)
    iqhu__znd = 0
    luwj__tzbu = np.empty(henl__hunsw + 1, np_offset_type)
    htra__pzuf = []
    pdrch__yohxx = np.empty(henl__hunsw + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        luwj__tzbu[i] = iqhu__znd
        ijci__shi = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(pdrch__yohxx, i, int(not
            ijci__shi))
        if ijci__shi:
            continue
        aupl__wjleo = list(s.encode()) if isinstance(s, str) else list(s)
        htra__pzuf.extend(aupl__wjleo)
        iqhu__znd += len(aupl__wjleo)
    luwj__tzbu[henl__hunsw] = iqhu__znd
    cuzpz__zzvjo = np.array(htra__pzuf, np.uint8)
    zzqr__xwdar = context.get_constant(types.int64, henl__hunsw)
    wkbs__ugxu = context.get_constant_generic(builder, char_arr_type,
        cuzpz__zzvjo)
    jdc__cpar = context.get_constant_generic(builder, offset_arr_type,
        luwj__tzbu)
    gcz__vbdlg = context.get_constant_generic(builder, null_bitmap_arr_type,
        pdrch__yohxx)
    jrl__sqon = lir.Constant.literal_struct([zzqr__xwdar, wkbs__ugxu,
        jdc__cpar, gcz__vbdlg])
    jrl__sqon = cgutils.global_constant(builder, '.const.payload', jrl__sqon
        ).bitcast(cgutils.voidptr_t)
    wir__uee = context.get_constant(types.int64, -1)
    oblu__dky = context.get_constant_null(types.voidptr)
    lar__vlk = lir.Constant.literal_struct([wir__uee, oblu__dky, oblu__dky,
        jrl__sqon, wir__uee])
    lar__vlk = cgutils.global_constant(builder, '.const.meminfo', lar__vlk
        ).bitcast(cgutils.voidptr_t)
    mxvy__yyn = lir.Constant.literal_struct([lar__vlk])
    fblb__qsqb = lir.Constant.literal_struct([mxvy__yyn])
    return fblb__qsqb


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
