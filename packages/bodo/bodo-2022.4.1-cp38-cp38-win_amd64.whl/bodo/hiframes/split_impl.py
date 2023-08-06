import operator
import llvmlite.binding as ll
import numba
import numba.core.typing.typeof
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, impl_ret_new_ref
from numba.extending import box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, _memcpy, char_arr_type, get_data_ptr, null_bitmap_arr_type, offset_arr_type, string_array_type
ll.add_symbol('array_setitem', hstr_ext.array_setitem)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
ll.add_symbol('dtor_str_arr_split_view', hstr_ext.dtor_str_arr_split_view)
ll.add_symbol('str_arr_split_view_impl', hstr_ext.str_arr_split_view_impl)
ll.add_symbol('str_arr_split_view_alloc', hstr_ext.str_arr_split_view_alloc)
char_typ = types.uint8
data_ctypes_type = types.ArrayCTypes(types.Array(char_typ, 1, 'C'))
offset_ctypes_type = types.ArrayCTypes(types.Array(offset_type, 1, 'C'))


class StringArraySplitViewType(types.ArrayCompatible):

    def __init__(self):
        super(StringArraySplitViewType, self).__init__(name=
            'StringArraySplitViewType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_array_type

    def copy(self):
        return StringArraySplitViewType()


string_array_split_view_type = StringArraySplitViewType()


class StringArraySplitViewPayloadType(types.Type):

    def __init__(self):
        super(StringArraySplitViewPayloadType, self).__init__(name=
            'StringArraySplitViewPayloadType()')


str_arr_split_view_payload_type = StringArraySplitViewPayloadType()


@register_model(StringArraySplitViewPayloadType)
class StringArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        moy__kmrk = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, moy__kmrk)


str_arr_model_members = [('num_items', types.uint64), ('index_offsets',
    types.CPointer(offset_type)), ('data_offsets', types.CPointer(
    offset_type)), ('data', data_ctypes_type), ('null_bitmap', types.
    CPointer(char_typ)), ('meminfo', types.MemInfoPointer(
    str_arr_split_view_payload_type))]


@register_model(StringArraySplitViewType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        models.StructModel.__init__(self, dmm, fe_type, str_arr_model_members)


make_attribute_wrapper(StringArraySplitViewType, 'num_items', '_num_items')
make_attribute_wrapper(StringArraySplitViewType, 'index_offsets',
    '_index_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data_offsets',
    '_data_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data', '_data')
make_attribute_wrapper(StringArraySplitViewType, 'null_bitmap', '_null_bitmap')


def construct_str_arr_split_view(context, builder):
    yblpm__svtd = context.get_value_type(str_arr_split_view_payload_type)
    shu__ntqwk = context.get_abi_sizeof(yblpm__svtd)
    cmxjr__than = context.get_value_type(types.voidptr)
    ipgr__ecjz = context.get_value_type(types.uintp)
    ylglr__myta = lir.FunctionType(lir.VoidType(), [cmxjr__than, ipgr__ecjz,
        cmxjr__than])
    jia__pap = cgutils.get_or_insert_function(builder.module, ylglr__myta,
        name='dtor_str_arr_split_view')
    ifkh__lyc = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, shu__ntqwk), jia__pap)
    phgx__atksj = context.nrt.meminfo_data(builder, ifkh__lyc)
    vjudi__xssz = builder.bitcast(phgx__atksj, yblpm__svtd.as_pointer())
    return ifkh__lyc, vjudi__xssz


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        nteel__ime, pmxrp__fns = args
        ifkh__lyc, vjudi__xssz = construct_str_arr_split_view(context, builder)
        whfyz__vnnni = _get_str_binary_arr_payload(context, builder,
            nteel__ime, string_array_type)
        musc__wlyju = lir.FunctionType(lir.VoidType(), [vjudi__xssz.type,
            lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        flppy__vjnkq = cgutils.get_or_insert_function(builder.module,
            musc__wlyju, name='str_arr_split_view_impl')
        qzco__iwexa = context.make_helper(builder, offset_arr_type,
            whfyz__vnnni.offsets).data
        muxh__bln = context.make_helper(builder, char_arr_type,
            whfyz__vnnni.data).data
        wiv__ndk = context.make_helper(builder, null_bitmap_arr_type,
            whfyz__vnnni.null_bitmap).data
        rbfex__zpbi = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(flppy__vjnkq, [vjudi__xssz, whfyz__vnnni.n_arrays,
            qzco__iwexa, muxh__bln, wiv__ndk, rbfex__zpbi])
        uaju__atek = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(vjudi__xssz))
        ybjr__bfa = context.make_helper(builder, string_array_split_view_type)
        ybjr__bfa.num_items = whfyz__vnnni.n_arrays
        ybjr__bfa.index_offsets = uaju__atek.index_offsets
        ybjr__bfa.data_offsets = uaju__atek.data_offsets
        ybjr__bfa.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [nteel__ime])
        ybjr__bfa.null_bitmap = uaju__atek.null_bitmap
        ybjr__bfa.meminfo = ifkh__lyc
        wysu__bkuth = ybjr__bfa._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, wysu__bkuth)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    njvqu__ydstg = context.make_helper(builder,
        string_array_split_view_type, val)
    xblka__ameig = context.insert_const_string(builder.module, 'numpy')
    vyomn__xex = c.pyapi.import_module_noblock(xblka__ameig)
    dtype = c.pyapi.object_getattr_string(vyomn__xex, 'object_')
    wqpnm__euppa = builder.sext(njvqu__ydstg.num_items, c.pyapi.longlong)
    bepcf__gkg = c.pyapi.long_from_longlong(wqpnm__euppa)
    xqne__inpfk = c.pyapi.call_method(vyomn__xex, 'ndarray', (bepcf__gkg,
        dtype))
    unqz__ousn = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    mnq__ctjf = c.pyapi._get_function(unqz__ousn, name='array_getptr1')
    lznps__pcpc = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    xicvm__ofl = c.pyapi._get_function(lznps__pcpc, name='array_setitem')
    xbxh__oet = c.pyapi.object_getattr_string(vyomn__xex, 'nan')
    with cgutils.for_range(builder, njvqu__ydstg.num_items) as bxgfy__kkm:
        str_ind = bxgfy__kkm.index
        clmtq__siq = builder.sext(builder.load(builder.gep(njvqu__ydstg.
            index_offsets, [str_ind])), lir.IntType(64))
        emjb__cgq = builder.sext(builder.load(builder.gep(njvqu__ydstg.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        kjmw__moan = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        gzjxm__iazwm = builder.gep(njvqu__ydstg.null_bitmap, [kjmw__moan])
        gnz__clsw = builder.load(gzjxm__iazwm)
        sebk__xtlor = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(gnz__clsw, sebk__xtlor), lir.
            Constant(lir.IntType(8), 1))
        bbm__dicu = builder.sub(emjb__cgq, clmtq__siq)
        bbm__dicu = builder.sub(bbm__dicu, bbm__dicu.type(1))
        hut__dbmx = builder.call(mnq__ctjf, [xqne__inpfk, str_ind])
        aawef__dbj = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(aawef__dbj) as (qgp__xmo, uhpy__kdch):
            with qgp__xmo:
                alm__mwc = c.pyapi.list_new(bbm__dicu)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    alm__mwc), likely=True):
                    with cgutils.for_range(c.builder, bbm__dicu) as bxgfy__kkm:
                        npace__cikaw = builder.add(clmtq__siq, bxgfy__kkm.index
                            )
                        data_start = builder.load(builder.gep(njvqu__ydstg.
                            data_offsets, [npace__cikaw]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        rbqq__wnbvg = builder.load(builder.gep(njvqu__ydstg
                            .data_offsets, [builder.add(npace__cikaw,
                            npace__cikaw.type(1))]))
                        todxv__xklv = builder.gep(builder.extract_value(
                            njvqu__ydstg.data, 0), [data_start])
                        laaxj__namj = builder.sext(builder.sub(rbqq__wnbvg,
                            data_start), lir.IntType(64))
                        esrlj__pevxh = c.pyapi.string_from_string_and_size(
                            todxv__xklv, laaxj__namj)
                        c.pyapi.list_setitem(alm__mwc, bxgfy__kkm.index,
                            esrlj__pevxh)
                builder.call(xicvm__ofl, [xqne__inpfk, hut__dbmx, alm__mwc])
            with uhpy__kdch:
                builder.call(xicvm__ofl, [xqne__inpfk, hut__dbmx, xbxh__oet])
    c.pyapi.decref(vyomn__xex)
    c.pyapi.decref(dtype)
    c.pyapi.decref(xbxh__oet)
    return xqne__inpfk


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        emdhh__etp, azzd__qkm, todxv__xklv = args
        ifkh__lyc, vjudi__xssz = construct_str_arr_split_view(context, builder)
        musc__wlyju = lir.FunctionType(lir.VoidType(), [vjudi__xssz.type,
            lir.IntType(64), lir.IntType(64)])
        flppy__vjnkq = cgutils.get_or_insert_function(builder.module,
            musc__wlyju, name='str_arr_split_view_alloc')
        builder.call(flppy__vjnkq, [vjudi__xssz, emdhh__etp, azzd__qkm])
        uaju__atek = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(vjudi__xssz))
        ybjr__bfa = context.make_helper(builder, string_array_split_view_type)
        ybjr__bfa.num_items = emdhh__etp
        ybjr__bfa.index_offsets = uaju__atek.index_offsets
        ybjr__bfa.data_offsets = uaju__atek.data_offsets
        ybjr__bfa.data = todxv__xklv
        ybjr__bfa.null_bitmap = uaju__atek.null_bitmap
        context.nrt.incref(builder, data_t, todxv__xklv)
        ybjr__bfa.meminfo = ifkh__lyc
        wysu__bkuth = ybjr__bfa._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, wysu__bkuth)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        ggvdn__ohpe, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            ggvdn__ohpe = builder.extract_value(ggvdn__ohpe, 0)
        return builder.bitcast(builder.gep(ggvdn__ohpe, [ind]), lir.IntType
            (8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        ggvdn__ohpe, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            ggvdn__ohpe = builder.extract_value(ggvdn__ohpe, 0)
        return builder.load(builder.gep(ggvdn__ohpe, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        ggvdn__ohpe, ind, amxqm__cjqct = args
        scjbg__qyw = builder.gep(ggvdn__ohpe, [ind])
        builder.store(amxqm__cjqct, scjbg__qyw)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        kmvhz__mneeb, ind = args
        zaxjx__wwclt = context.make_helper(builder, arr_ctypes_t, kmvhz__mneeb)
        wku__ukl = context.make_helper(builder, arr_ctypes_t)
        wku__ukl.data = builder.gep(zaxjx__wwclt.data, [ind])
        wku__ukl.meminfo = zaxjx__wwclt.meminfo
        bjle__qkyf = wku__ukl._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, bjle__qkyf)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    araud__yez = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not araud__yez:
        return 0, 0, 0
    npace__cikaw = getitem_c_arr(arr._index_offsets, item_ind)
    ypyjg__maofg = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    zqpw__bney = ypyjg__maofg - npace__cikaw
    if str_ind >= zqpw__bney:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, npace__cikaw + str_ind)
    data_start += 1
    if npace__cikaw + str_ind == 0:
        data_start = 0
    rbqq__wnbvg = getitem_c_arr(arr._data_offsets, npace__cikaw + str_ind + 1)
    zixs__wasv = rbqq__wnbvg - data_start
    return 1, data_start, zixs__wasv


@numba.njit(no_cpython_wrapper=True)
def get_split_view_data_ptr(arr, data_start):
    return get_array_ctypes_ptr(arr._data, data_start)


@overload(len, no_unliteral=True)
def str_arr_split_view_len_overload(arr):
    if arr == string_array_split_view_type:
        return lambda arr: np.int64(arr._num_items)


@overload_attribute(StringArraySplitViewType, 'shape')
def overload_split_view_arr_shape(A):
    return lambda A: (np.int64(A._num_items),)


@overload(operator.getitem, no_unliteral=True)
def str_arr_split_view_getitem_overload(A, ind):
    if A != string_array_split_view_type:
        return
    if A == string_array_split_view_type and isinstance(ind, types.Integer):
        brm__rzd = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            npace__cikaw = getitem_c_arr(A._index_offsets, ind)
            ypyjg__maofg = getitem_c_arr(A._index_offsets, ind + 1)
            rncl__lasmp = ypyjg__maofg - npace__cikaw - 1
            nteel__ime = bodo.libs.str_arr_ext.pre_alloc_string_array(
                rncl__lasmp, -1)
            for wepgi__cux in range(rncl__lasmp):
                data_start = getitem_c_arr(A._data_offsets, npace__cikaw +
                    wepgi__cux)
                data_start += 1
                if npace__cikaw + wepgi__cux == 0:
                    data_start = 0
                rbqq__wnbvg = getitem_c_arr(A._data_offsets, npace__cikaw +
                    wepgi__cux + 1)
                zixs__wasv = rbqq__wnbvg - data_start
                scjbg__qyw = get_array_ctypes_ptr(A._data, data_start)
                gpu__jtwe = bodo.libs.str_arr_ext.decode_utf8(scjbg__qyw,
                    zixs__wasv)
                nteel__ime[wepgi__cux] = gpu__jtwe
            return nteel__ime
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        xxg__anjwz = offset_type.bitwidth // 8

        def _impl(A, ind):
            rncl__lasmp = len(A)
            if rncl__lasmp != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            emdhh__etp = 0
            azzd__qkm = 0
            for wepgi__cux in range(rncl__lasmp):
                if ind[wepgi__cux]:
                    emdhh__etp += 1
                    npace__cikaw = getitem_c_arr(A._index_offsets, wepgi__cux)
                    ypyjg__maofg = getitem_c_arr(A._index_offsets, 
                        wepgi__cux + 1)
                    azzd__qkm += ypyjg__maofg - npace__cikaw
            xqne__inpfk = pre_alloc_str_arr_view(emdhh__etp, azzd__qkm, A._data
                )
            item_ind = 0
            geor__hdj = 0
            for wepgi__cux in range(rncl__lasmp):
                if ind[wepgi__cux]:
                    npace__cikaw = getitem_c_arr(A._index_offsets, wepgi__cux)
                    ypyjg__maofg = getitem_c_arr(A._index_offsets, 
                        wepgi__cux + 1)
                    udftz__fsb = ypyjg__maofg - npace__cikaw
                    setitem_c_arr(xqne__inpfk._index_offsets, item_ind,
                        geor__hdj)
                    scjbg__qyw = get_c_arr_ptr(A._data_offsets, npace__cikaw)
                    htl__ycf = get_c_arr_ptr(xqne__inpfk._data_offsets,
                        geor__hdj)
                    _memcpy(htl__ycf, scjbg__qyw, udftz__fsb, xxg__anjwz)
                    araud__yez = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, wepgi__cux)
                    bodo.libs.int_arr_ext.set_bit_to_arr(xqne__inpfk.
                        _null_bitmap, item_ind, araud__yez)
                    item_ind += 1
                    geor__hdj += udftz__fsb
            setitem_c_arr(xqne__inpfk._index_offsets, item_ind, geor__hdj)
            return xqne__inpfk
        return _impl
