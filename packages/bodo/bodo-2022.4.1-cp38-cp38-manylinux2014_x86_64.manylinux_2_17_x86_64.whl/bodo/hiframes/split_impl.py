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
        lxz__hvjjz = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, lxz__hvjjz)


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
    pzdq__mump = context.get_value_type(str_arr_split_view_payload_type)
    gvy__nrlzr = context.get_abi_sizeof(pzdq__mump)
    nzlf__sckn = context.get_value_type(types.voidptr)
    sgu__qjk = context.get_value_type(types.uintp)
    ioizc__lvben = lir.FunctionType(lir.VoidType(), [nzlf__sckn, sgu__qjk,
        nzlf__sckn])
    itxvp__yvq = cgutils.get_or_insert_function(builder.module,
        ioizc__lvben, name='dtor_str_arr_split_view')
    wqk__yvzx = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, gvy__nrlzr), itxvp__yvq)
    obpdf__oohl = context.nrt.meminfo_data(builder, wqk__yvzx)
    loogp__lryfz = builder.bitcast(obpdf__oohl, pzdq__mump.as_pointer())
    return wqk__yvzx, loogp__lryfz


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        cki__sctw, wqu__fzvhr = args
        wqk__yvzx, loogp__lryfz = construct_str_arr_split_view(context, builder
            )
        atxqc__zri = _get_str_binary_arr_payload(context, builder,
            cki__sctw, string_array_type)
        laoe__spzu = lir.FunctionType(lir.VoidType(), [loogp__lryfz.type,
            lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        rqvk__pfkn = cgutils.get_or_insert_function(builder.module,
            laoe__spzu, name='str_arr_split_view_impl')
        hkymv__oqe = context.make_helper(builder, offset_arr_type,
            atxqc__zri.offsets).data
        bnq__rdl = context.make_helper(builder, char_arr_type, atxqc__zri.data
            ).data
        cgmf__aoyx = context.make_helper(builder, null_bitmap_arr_type,
            atxqc__zri.null_bitmap).data
        ciera__bqr = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(rqvk__pfkn, [loogp__lryfz, atxqc__zri.n_arrays,
            hkymv__oqe, bnq__rdl, cgmf__aoyx, ciera__bqr])
        xcpw__jbpmx = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(loogp__lryfz))
        zwzj__mmpw = context.make_helper(builder, string_array_split_view_type)
        zwzj__mmpw.num_items = atxqc__zri.n_arrays
        zwzj__mmpw.index_offsets = xcpw__jbpmx.index_offsets
        zwzj__mmpw.data_offsets = xcpw__jbpmx.data_offsets
        zwzj__mmpw.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [cki__sctw])
        zwzj__mmpw.null_bitmap = xcpw__jbpmx.null_bitmap
        zwzj__mmpw.meminfo = wqk__yvzx
        jsmew__lpsje = zwzj__mmpw._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, jsmew__lpsje)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    jvjt__vbx = context.make_helper(builder, string_array_split_view_type, val)
    slzj__dxwgl = context.insert_const_string(builder.module, 'numpy')
    vsfhi__vjer = c.pyapi.import_module_noblock(slzj__dxwgl)
    dtype = c.pyapi.object_getattr_string(vsfhi__vjer, 'object_')
    blmom__prlll = builder.sext(jvjt__vbx.num_items, c.pyapi.longlong)
    egczx__fvqj = c.pyapi.long_from_longlong(blmom__prlll)
    itgw__stajw = c.pyapi.call_method(vsfhi__vjer, 'ndarray', (egczx__fvqj,
        dtype))
    ctnyz__wmxc = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    lkxrh__smmaz = c.pyapi._get_function(ctnyz__wmxc, name='array_getptr1')
    bev__rfern = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    xtz__ldonh = c.pyapi._get_function(bev__rfern, name='array_setitem')
    zdel__asss = c.pyapi.object_getattr_string(vsfhi__vjer, 'nan')
    with cgutils.for_range(builder, jvjt__vbx.num_items) as hzi__mbb:
        str_ind = hzi__mbb.index
        gpbsd__byfba = builder.sext(builder.load(builder.gep(jvjt__vbx.
            index_offsets, [str_ind])), lir.IntType(64))
        qlwvp__rwspo = builder.sext(builder.load(builder.gep(jvjt__vbx.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        daexk__wwd = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        ziwne__vmk = builder.gep(jvjt__vbx.null_bitmap, [daexk__wwd])
        plg__iyd = builder.load(ziwne__vmk)
        kwxl__ulk = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(plg__iyd, kwxl__ulk), lir.Constant(
            lir.IntType(8), 1))
        wlwax__drghb = builder.sub(qlwvp__rwspo, gpbsd__byfba)
        wlwax__drghb = builder.sub(wlwax__drghb, wlwax__drghb.type(1))
        rtkss__nvu = builder.call(lkxrh__smmaz, [itgw__stajw, str_ind])
        eezh__iolax = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(eezh__iolax) as (nflmb__rtgr, lki__yuv):
            with nflmb__rtgr:
                pdng__iblmq = c.pyapi.list_new(wlwax__drghb)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    pdng__iblmq), likely=True):
                    with cgutils.for_range(c.builder, wlwax__drghb
                        ) as hzi__mbb:
                        vbq__sea = builder.add(gpbsd__byfba, hzi__mbb.index)
                        data_start = builder.load(builder.gep(jvjt__vbx.
                            data_offsets, [vbq__sea]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        irvmr__oaoec = builder.load(builder.gep(jvjt__vbx.
                            data_offsets, [builder.add(vbq__sea, vbq__sea.
                            type(1))]))
                        rsjmz__jwt = builder.gep(builder.extract_value(
                            jvjt__vbx.data, 0), [data_start])
                        frtb__uylgv = builder.sext(builder.sub(irvmr__oaoec,
                            data_start), lir.IntType(64))
                        hiypd__xqxpl = c.pyapi.string_from_string_and_size(
                            rsjmz__jwt, frtb__uylgv)
                        c.pyapi.list_setitem(pdng__iblmq, hzi__mbb.index,
                            hiypd__xqxpl)
                builder.call(xtz__ldonh, [itgw__stajw, rtkss__nvu, pdng__iblmq]
                    )
            with lki__yuv:
                builder.call(xtz__ldonh, [itgw__stajw, rtkss__nvu, zdel__asss])
    c.pyapi.decref(vsfhi__vjer)
    c.pyapi.decref(dtype)
    c.pyapi.decref(zdel__asss)
    return itgw__stajw


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        boovy__gfh, tmkbv__xgjz, rsjmz__jwt = args
        wqk__yvzx, loogp__lryfz = construct_str_arr_split_view(context, builder
            )
        laoe__spzu = lir.FunctionType(lir.VoidType(), [loogp__lryfz.type,
            lir.IntType(64), lir.IntType(64)])
        rqvk__pfkn = cgutils.get_or_insert_function(builder.module,
            laoe__spzu, name='str_arr_split_view_alloc')
        builder.call(rqvk__pfkn, [loogp__lryfz, boovy__gfh, tmkbv__xgjz])
        xcpw__jbpmx = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(loogp__lryfz))
        zwzj__mmpw = context.make_helper(builder, string_array_split_view_type)
        zwzj__mmpw.num_items = boovy__gfh
        zwzj__mmpw.index_offsets = xcpw__jbpmx.index_offsets
        zwzj__mmpw.data_offsets = xcpw__jbpmx.data_offsets
        zwzj__mmpw.data = rsjmz__jwt
        zwzj__mmpw.null_bitmap = xcpw__jbpmx.null_bitmap
        context.nrt.incref(builder, data_t, rsjmz__jwt)
        zwzj__mmpw.meminfo = wqk__yvzx
        jsmew__lpsje = zwzj__mmpw._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, jsmew__lpsje)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        yxeqr__ndkcx, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            yxeqr__ndkcx = builder.extract_value(yxeqr__ndkcx, 0)
        return builder.bitcast(builder.gep(yxeqr__ndkcx, [ind]), lir.
            IntType(8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        yxeqr__ndkcx, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            yxeqr__ndkcx = builder.extract_value(yxeqr__ndkcx, 0)
        return builder.load(builder.gep(yxeqr__ndkcx, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        yxeqr__ndkcx, ind, jmimq__swqk = args
        ogrq__yuicz = builder.gep(yxeqr__ndkcx, [ind])
        builder.store(jmimq__swqk, ogrq__yuicz)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        bybgh__eqxew, ind = args
        uimqt__jcb = context.make_helper(builder, arr_ctypes_t, bybgh__eqxew)
        vaxhu__rzr = context.make_helper(builder, arr_ctypes_t)
        vaxhu__rzr.data = builder.gep(uimqt__jcb.data, [ind])
        vaxhu__rzr.meminfo = uimqt__jcb.meminfo
        fqr__vfw = vaxhu__rzr._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, fqr__vfw)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    boug__tvv = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not boug__tvv:
        return 0, 0, 0
    vbq__sea = getitem_c_arr(arr._index_offsets, item_ind)
    lxr__npkee = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    rij__suwd = lxr__npkee - vbq__sea
    if str_ind >= rij__suwd:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, vbq__sea + str_ind)
    data_start += 1
    if vbq__sea + str_ind == 0:
        data_start = 0
    irvmr__oaoec = getitem_c_arr(arr._data_offsets, vbq__sea + str_ind + 1)
    dsuti__lxfe = irvmr__oaoec - data_start
    return 1, data_start, dsuti__lxfe


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
        hlp__iyym = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            vbq__sea = getitem_c_arr(A._index_offsets, ind)
            lxr__npkee = getitem_c_arr(A._index_offsets, ind + 1)
            dey__whasc = lxr__npkee - vbq__sea - 1
            cki__sctw = bodo.libs.str_arr_ext.pre_alloc_string_array(dey__whasc
                , -1)
            for bag__yxjp in range(dey__whasc):
                data_start = getitem_c_arr(A._data_offsets, vbq__sea +
                    bag__yxjp)
                data_start += 1
                if vbq__sea + bag__yxjp == 0:
                    data_start = 0
                irvmr__oaoec = getitem_c_arr(A._data_offsets, vbq__sea +
                    bag__yxjp + 1)
                dsuti__lxfe = irvmr__oaoec - data_start
                ogrq__yuicz = get_array_ctypes_ptr(A._data, data_start)
                uflr__ssub = bodo.libs.str_arr_ext.decode_utf8(ogrq__yuicz,
                    dsuti__lxfe)
                cki__sctw[bag__yxjp] = uflr__ssub
            return cki__sctw
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        kyy__xyfz = offset_type.bitwidth // 8

        def _impl(A, ind):
            dey__whasc = len(A)
            if dey__whasc != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            boovy__gfh = 0
            tmkbv__xgjz = 0
            for bag__yxjp in range(dey__whasc):
                if ind[bag__yxjp]:
                    boovy__gfh += 1
                    vbq__sea = getitem_c_arr(A._index_offsets, bag__yxjp)
                    lxr__npkee = getitem_c_arr(A._index_offsets, bag__yxjp + 1)
                    tmkbv__xgjz += lxr__npkee - vbq__sea
            itgw__stajw = pre_alloc_str_arr_view(boovy__gfh, tmkbv__xgjz, A
                ._data)
            item_ind = 0
            qyyr__eeomc = 0
            for bag__yxjp in range(dey__whasc):
                if ind[bag__yxjp]:
                    vbq__sea = getitem_c_arr(A._index_offsets, bag__yxjp)
                    lxr__npkee = getitem_c_arr(A._index_offsets, bag__yxjp + 1)
                    vvt__jbfxm = lxr__npkee - vbq__sea
                    setitem_c_arr(itgw__stajw._index_offsets, item_ind,
                        qyyr__eeomc)
                    ogrq__yuicz = get_c_arr_ptr(A._data_offsets, vbq__sea)
                    zum__fqbp = get_c_arr_ptr(itgw__stajw._data_offsets,
                        qyyr__eeomc)
                    _memcpy(zum__fqbp, ogrq__yuicz, vvt__jbfxm, kyy__xyfz)
                    boug__tvv = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A.
                        _null_bitmap, bag__yxjp)
                    bodo.libs.int_arr_ext.set_bit_to_arr(itgw__stajw.
                        _null_bitmap, item_ind, boug__tvv)
                    item_ind += 1
                    qyyr__eeomc += vvt__jbfxm
            setitem_c_arr(itgw__stajw._index_offsets, item_ind, qyyr__eeomc)
            return itgw__stajw
        return _impl
