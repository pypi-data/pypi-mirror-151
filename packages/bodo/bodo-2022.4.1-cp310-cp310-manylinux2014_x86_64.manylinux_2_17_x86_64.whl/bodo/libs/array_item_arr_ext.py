"""Array implementation for variable-size array items.
Corresponds to Spark's ArrayType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Variable-size List: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in a contingous data array, while an offsets array marks the
individual arrays. For example:
value:             [[1, 2], [3], None, [5, 4, 6], []]
data:              [1, 2, 3, 5, 4, 6]
offsets:           [0, 2, 3, 3, 6, 6]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('array_item_array_from_sequence', array_ext.
    array_item_array_from_sequence)
ll.add_symbol('np_array_from_array_item_array', array_ext.
    np_array_from_array_item_array)
offset_type = types.uint64
np_offset_type = numba.np.numpy_support.as_dtype(offset_type)


class ArrayItemArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        assert bodo.utils.utils.is_array_typ(dtype, False)
        self.dtype = dtype
        super(ArrayItemArrayType, self).__init__(name=
            'ArrayItemArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return ArrayItemArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class ArrayItemArrayPayloadType(types.Type):

    def __init__(self, array_type):
        self.array_type = array_type
        super(ArrayItemArrayPayloadType, self).__init__(name=
            'ArrayItemArrayPayloadType({})'.format(array_type))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(ArrayItemArrayPayloadType)
class ArrayItemArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kyng__obdt = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, kyng__obdt)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        kyng__obdt = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, kyng__obdt)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    adan__fjqjp = builder.module
    tawdt__mfmjr = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    hcor__gnx = cgutils.get_or_insert_function(adan__fjqjp, tawdt__mfmjr,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not hcor__gnx.is_declaration:
        return hcor__gnx
    hcor__gnx.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(hcor__gnx.append_basic_block())
    vbpyi__mrtxw = hcor__gnx.args[0]
    rmw__zifv = context.get_value_type(payload_type).as_pointer()
    irt__fvgw = builder.bitcast(vbpyi__mrtxw, rmw__zifv)
    vjk__dat = context.make_helper(builder, payload_type, ref=irt__fvgw)
    context.nrt.decref(builder, array_item_type.dtype, vjk__dat.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), vjk__dat.
        offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), vjk__dat.
        null_bitmap)
    builder.ret_void()
    return hcor__gnx


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    fnesr__aho = context.get_value_type(payload_type)
    jldzm__jmqct = context.get_abi_sizeof(fnesr__aho)
    ghh__hos = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    tun__auqd = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, jldzm__jmqct), ghh__hos)
    ooj__vhk = context.nrt.meminfo_data(builder, tun__auqd)
    lvm__gok = builder.bitcast(ooj__vhk, fnesr__aho.as_pointer())
    vjk__dat = cgutils.create_struct_proxy(payload_type)(context, builder)
    vjk__dat.n_arrays = n_arrays
    ppduo__ucvkn = n_elems.type.count
    icanc__admgo = builder.extract_value(n_elems, 0)
    ttm__dmo = cgutils.alloca_once_value(builder, icanc__admgo)
    xst__smtdq = builder.icmp_signed('==', icanc__admgo, lir.Constant(
        icanc__admgo.type, -1))
    with builder.if_then(xst__smtdq):
        builder.store(n_arrays, ttm__dmo)
    n_elems = cgutils.pack_array(builder, [builder.load(ttm__dmo)] + [
        builder.extract_value(n_elems, nynta__prum) for nynta__prum in
        range(1, ppduo__ucvkn)])
    vjk__dat.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    wnv__ompsy = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    sjbq__pku = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [wnv__ompsy])
    offsets_ptr = sjbq__pku.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    vjk__dat.offsets = sjbq__pku._getvalue()
    smulw__zpzb = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    rpi__xia = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [smulw__zpzb])
    null_bitmap_ptr = rpi__xia.data
    vjk__dat.null_bitmap = rpi__xia._getvalue()
    builder.store(vjk__dat._getvalue(), lvm__gok)
    return tun__auqd, vjk__dat.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    uvsa__mdh, sqcpy__azkr = c.pyapi.call_jit_code(copy_data, sig, [
        data_arr, item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    xdbb__adzfw = context.insert_const_string(builder.module, 'pandas')
    lgu__cbxc = c.pyapi.import_module_noblock(xdbb__adzfw)
    xxox__vps = c.pyapi.object_getattr_string(lgu__cbxc, 'NA')
    vemfs__jglte = c.context.get_constant(offset_type, 0)
    builder.store(vemfs__jglte, offsets_ptr)
    edo__lgvoi = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as coo__fkv:
        phim__llyj = coo__fkv.index
        item_ind = builder.load(edo__lgvoi)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [phim__llyj]))
        arr_obj = seq_getitem(builder, context, val, phim__llyj)
        set_bitmap_bit(builder, null_bitmap_ptr, phim__llyj, 0)
        tcqkv__rnutq = is_na_value(builder, context, arr_obj, xxox__vps)
        twx__cmiu = builder.icmp_unsigned('!=', tcqkv__rnutq, lir.Constant(
            tcqkv__rnutq.type, 1))
        with builder.if_then(twx__cmiu):
            set_bitmap_bit(builder, null_bitmap_ptr, phim__llyj, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), edo__lgvoi)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(edo__lgvoi), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(lgu__cbxc)
    c.pyapi.decref(xxox__vps)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    tpck__locvy = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if tpck__locvy:
        tawdt__mfmjr = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        xpfz__irpy = cgutils.get_or_insert_function(c.builder.module,
            tawdt__mfmjr, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(xpfz__irpy,
            [val])])
    else:
        ojyv__mpoxv = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            ojyv__mpoxv, nynta__prum) for nynta__prum in range(1,
            ojyv__mpoxv.type.count)])
    tun__auqd, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if tpck__locvy:
        dgljn__cti = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        ype__ammey = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        tawdt__mfmjr = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        hcor__gnx = cgutils.get_or_insert_function(c.builder.module,
            tawdt__mfmjr, name='array_item_array_from_sequence')
        c.builder.call(hcor__gnx, [val, c.builder.bitcast(ype__ammey, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), dgljn__cti)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    nmk__rtd = c.context.make_helper(c.builder, typ)
    nmk__rtd.meminfo = tun__auqd
    rvg__wya = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nmk__rtd._getvalue(), is_error=rvg__wya)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    nmk__rtd = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    ooj__vhk = context.nrt.meminfo_data(builder, nmk__rtd.meminfo)
    lvm__gok = builder.bitcast(ooj__vhk, context.get_value_type(
        payload_type).as_pointer())
    vjk__dat = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(lvm__gok))
    return vjk__dat


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    xdbb__adzfw = context.insert_const_string(builder.module, 'numpy')
    kyitm__rnipr = c.pyapi.import_module_noblock(xdbb__adzfw)
    sztc__mecc = c.pyapi.object_getattr_string(kyitm__rnipr, 'object_')
    xob__tdqe = c.pyapi.long_from_longlong(n_arrays)
    bmbjw__jsbsb = c.pyapi.call_method(kyitm__rnipr, 'ndarray', (xob__tdqe,
        sztc__mecc))
    adx__aoxh = c.pyapi.object_getattr_string(kyitm__rnipr, 'nan')
    edo__lgvoi = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as coo__fkv:
        phim__llyj = coo__fkv.index
        pyarray_setitem(builder, context, bmbjw__jsbsb, phim__llyj, adx__aoxh)
        iwtgc__wbc = get_bitmap_bit(builder, null_bitmap_ptr, phim__llyj)
        wjpon__uyrj = builder.icmp_unsigned('!=', iwtgc__wbc, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(wjpon__uyrj):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(phim__llyj, lir.Constant(
                phim__llyj.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [phim__llyj]))), lir.IntType(64))
            item_ind = builder.load(edo__lgvoi)
            uvsa__mdh, dqoan__jcrn = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), edo__lgvoi)
            arr_obj = c.pyapi.from_native_value(typ.dtype, dqoan__jcrn, c.
                env_manager)
            pyarray_setitem(builder, context, bmbjw__jsbsb, phim__llyj, arr_obj
                )
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(kyitm__rnipr)
    c.pyapi.decref(sztc__mecc)
    c.pyapi.decref(xob__tdqe)
    c.pyapi.decref(adx__aoxh)
    return bmbjw__jsbsb


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    vjk__dat = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = vjk__dat.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), vjk__dat.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), vjk__dat.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        dgljn__cti = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        ype__ammey = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        tawdt__mfmjr = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        zzia__nxeiv = cgutils.get_or_insert_function(c.builder.module,
            tawdt__mfmjr, name='np_array_from_array_item_array')
        arr = c.builder.call(zzia__nxeiv, [vjk__dat.n_arrays, c.builder.
            bitcast(ype__ammey, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), dgljn__cti)])
    else:
        arr = _box_array_item_array_generic(typ, c, vjk__dat.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    vow__eik, rdfco__kyil, bcya__wnnto = args
    awuwv__uzxu = bodo.utils.transform.get_type_alloc_counts(array_item_type
        .dtype)
    fjb__uftk = sig.args[1]
    if not isinstance(fjb__uftk, types.UniTuple):
        rdfco__kyil = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), -1) for bcya__wnnto in range(awuwv__uzxu)])
    elif fjb__uftk.count < awuwv__uzxu:
        rdfco__kyil = cgutils.pack_array(builder, [builder.extract_value(
            rdfco__kyil, nynta__prum) for nynta__prum in range(fjb__uftk.
            count)] + [lir.Constant(lir.IntType(64), -1) for bcya__wnnto in
            range(awuwv__uzxu - fjb__uftk.count)])
    tun__auqd, bcya__wnnto, bcya__wnnto, bcya__wnnto = (
        construct_array_item_array(context, builder, array_item_type,
        vow__eik, rdfco__kyil))
    nmk__rtd = context.make_helper(builder, array_item_type)
    nmk__rtd.meminfo = tun__auqd
    return nmk__rtd._getvalue()


@intrinsic
def pre_alloc_array_item_array(typingctx, num_arrs_typ, num_values_typ,
    dtype_typ=None):
    assert isinstance(num_arrs_typ, types.Integer)
    array_item_type = ArrayItemArrayType(dtype_typ.instance_type)
    num_values_typ = types.unliteral(num_values_typ)
    return array_item_type(types.int64, num_values_typ, dtype_typ
        ), lower_pre_alloc_array_item_array


def pre_alloc_array_item_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_array_item_arr_ext_pre_alloc_array_item_array
    ) = pre_alloc_array_item_array_equiv


def init_array_item_array_codegen(context, builder, signature, args):
    n_arrays, szvu__fhv, sjbq__pku, rpi__xia = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    fnesr__aho = context.get_value_type(payload_type)
    jldzm__jmqct = context.get_abi_sizeof(fnesr__aho)
    ghh__hos = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    tun__auqd = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, jldzm__jmqct), ghh__hos)
    ooj__vhk = context.nrt.meminfo_data(builder, tun__auqd)
    lvm__gok = builder.bitcast(ooj__vhk, fnesr__aho.as_pointer())
    vjk__dat = cgutils.create_struct_proxy(payload_type)(context, builder)
    vjk__dat.n_arrays = n_arrays
    vjk__dat.data = szvu__fhv
    vjk__dat.offsets = sjbq__pku
    vjk__dat.null_bitmap = rpi__xia
    builder.store(vjk__dat._getvalue(), lvm__gok)
    context.nrt.incref(builder, signature.args[1], szvu__fhv)
    context.nrt.incref(builder, signature.args[2], sjbq__pku)
    context.nrt.incref(builder, signature.args[3], rpi__xia)
    nmk__rtd = context.make_helper(builder, array_item_type)
    nmk__rtd.meminfo = tun__auqd
    return nmk__rtd._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    tzsm__qtt = ArrayItemArrayType(data_type)
    sig = tzsm__qtt(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        vjk__dat = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            vjk__dat.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        vjk__dat = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        ype__ammey = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, vjk__dat.offsets).data
        sjbq__pku = builder.bitcast(ype__ammey, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(sjbq__pku, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        vjk__dat = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            vjk__dat.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        vjk__dat = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            vjk__dat.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


def alias_ext_single_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_offsets',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_data',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_null_bitmap',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array


@intrinsic
def get_n_arrays(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        vjk__dat = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return vjk__dat.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, icqi__uawhz = args
        nmk__rtd = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        ooj__vhk = context.nrt.meminfo_data(builder, nmk__rtd.meminfo)
        lvm__gok = builder.bitcast(ooj__vhk, context.get_value_type(
            payload_type).as_pointer())
        vjk__dat = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(lvm__gok))
        context.nrt.decref(builder, data_typ, vjk__dat.data)
        vjk__dat.data = icqi__uawhz
        context.nrt.incref(builder, data_typ, icqi__uawhz)
        builder.store(vjk__dat._getvalue(), lvm__gok)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    szvu__fhv = get_data(arr)
    junee__rwi = len(szvu__fhv)
    if junee__rwi < new_size:
        jtemf__wlgca = max(2 * junee__rwi, new_size)
        icqi__uawhz = bodo.libs.array_kernels.resize_and_copy(szvu__fhv,
            old_size, jtemf__wlgca)
        replace_data_arr(arr, icqi__uawhz)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    szvu__fhv = get_data(arr)
    sjbq__pku = get_offsets(arr)
    bni__jxxwp = len(szvu__fhv)
    xkh__hkism = sjbq__pku[-1]
    if bni__jxxwp != xkh__hkism:
        icqi__uawhz = bodo.libs.array_kernels.resize_and_copy(szvu__fhv,
            xkh__hkism, xkh__hkism)
        replace_data_arr(arr, icqi__uawhz)


@overload(len, no_unliteral=True)
def overload_array_item_arr_len(A):
    if isinstance(A, ArrayItemArrayType):
        return lambda A: get_n_arrays(A)


@overload_attribute(ArrayItemArrayType, 'shape')
def overload_array_item_arr_shape(A):
    return lambda A: (get_n_arrays(A),)


@overload_attribute(ArrayItemArrayType, 'dtype')
def overload_array_item_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(ArrayItemArrayType, 'ndim')
def overload_array_item_arr_ndim(A):
    return lambda A: 1


@overload_attribute(ArrayItemArrayType, 'nbytes')
def overload_array_item_arr_nbytes(A):
    return lambda A: get_data(A).nbytes + get_offsets(A
        ).nbytes + get_null_bitmap(A).nbytes


@overload(operator.getitem, no_unliteral=True)
def array_item_arr_getitem_array(arr, ind):
    if not isinstance(arr, ArrayItemArrayType):
        return
    if isinstance(ind, types.Integer):

        def array_item_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            sjbq__pku = get_offsets(arr)
            szvu__fhv = get_data(arr)
            ksr__ltwp = sjbq__pku[ind]
            mswu__oslyh = sjbq__pku[ind + 1]
            return szvu__fhv[ksr__ltwp:mswu__oslyh]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        hars__bdi = arr.dtype

        def impl_bool(arr, ind):
            embjv__yxmm = len(arr)
            if embjv__yxmm != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            rpi__xia = get_null_bitmap(arr)
            n_arrays = 0
            siiym__fov = init_nested_counts(hars__bdi)
            for nynta__prum in range(embjv__yxmm):
                if ind[nynta__prum]:
                    n_arrays += 1
                    ujd__hjcbe = arr[nynta__prum]
                    siiym__fov = add_nested_counts(siiym__fov, ujd__hjcbe)
            bmbjw__jsbsb = pre_alloc_array_item_array(n_arrays, siiym__fov,
                hars__bdi)
            jtcwj__daabh = get_null_bitmap(bmbjw__jsbsb)
            uhl__bpt = 0
            for rkm__zhgtt in range(embjv__yxmm):
                if ind[rkm__zhgtt]:
                    bmbjw__jsbsb[uhl__bpt] = arr[rkm__zhgtt]
                    bnc__fak = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        rpi__xia, rkm__zhgtt)
                    bodo.libs.int_arr_ext.set_bit_to_arr(jtcwj__daabh,
                        uhl__bpt, bnc__fak)
                    uhl__bpt += 1
            return bmbjw__jsbsb
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        hars__bdi = arr.dtype

        def impl_int(arr, ind):
            rpi__xia = get_null_bitmap(arr)
            embjv__yxmm = len(ind)
            n_arrays = embjv__yxmm
            siiym__fov = init_nested_counts(hars__bdi)
            for jibsk__pjztp in range(embjv__yxmm):
                nynta__prum = ind[jibsk__pjztp]
                ujd__hjcbe = arr[nynta__prum]
                siiym__fov = add_nested_counts(siiym__fov, ujd__hjcbe)
            bmbjw__jsbsb = pre_alloc_array_item_array(n_arrays, siiym__fov,
                hars__bdi)
            jtcwj__daabh = get_null_bitmap(bmbjw__jsbsb)
            for mwsc__smme in range(embjv__yxmm):
                rkm__zhgtt = ind[mwsc__smme]
                bmbjw__jsbsb[mwsc__smme] = arr[rkm__zhgtt]
                bnc__fak = bodo.libs.int_arr_ext.get_bit_bitmap_arr(rpi__xia,
                    rkm__zhgtt)
                bodo.libs.int_arr_ext.set_bit_to_arr(jtcwj__daabh,
                    mwsc__smme, bnc__fak)
            return bmbjw__jsbsb
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            embjv__yxmm = len(arr)
            zwc__hzmv = numba.cpython.unicode._normalize_slice(ind, embjv__yxmm
                )
            muv__oiui = np.arange(zwc__hzmv.start, zwc__hzmv.stop,
                zwc__hzmv.step)
            return arr[muv__oiui]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            sjbq__pku = get_offsets(A)
            rpi__xia = get_null_bitmap(A)
            if idx == 0:
                sjbq__pku[0] = 0
            n_items = len(val)
            dnpz__bdflx = sjbq__pku[idx] + n_items
            ensure_data_capacity(A, sjbq__pku[idx], dnpz__bdflx)
            szvu__fhv = get_data(A)
            sjbq__pku[idx + 1] = sjbq__pku[idx] + n_items
            szvu__fhv[sjbq__pku[idx]:sjbq__pku[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(rpi__xia, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            zwc__hzmv = numba.cpython.unicode._normalize_slice(idx, len(A))
            for nynta__prum in range(zwc__hzmv.start, zwc__hzmv.stop,
                zwc__hzmv.step):
                A[nynta__prum] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            sjbq__pku = get_offsets(A)
            rpi__xia = get_null_bitmap(A)
            zgk__ovjf = get_offsets(val)
            iajqf__gdvw = get_data(val)
            umk__vuedu = get_null_bitmap(val)
            embjv__yxmm = len(A)
            zwc__hzmv = numba.cpython.unicode._normalize_slice(idx, embjv__yxmm
                )
            kktye__wqkpg, zemz__fvh = zwc__hzmv.start, zwc__hzmv.stop
            assert zwc__hzmv.step == 1
            if kktye__wqkpg == 0:
                sjbq__pku[kktye__wqkpg] = 0
            szu__goury = sjbq__pku[kktye__wqkpg]
            dnpz__bdflx = szu__goury + len(iajqf__gdvw)
            ensure_data_capacity(A, szu__goury, dnpz__bdflx)
            szvu__fhv = get_data(A)
            szvu__fhv[szu__goury:szu__goury + len(iajqf__gdvw)] = iajqf__gdvw
            sjbq__pku[kktye__wqkpg:zemz__fvh + 1] = zgk__ovjf + szu__goury
            trxeg__ulhv = 0
            for nynta__prum in range(kktye__wqkpg, zemz__fvh):
                bnc__fak = bodo.libs.int_arr_ext.get_bit_bitmap_arr(umk__vuedu,
                    trxeg__ulhv)
                bodo.libs.int_arr_ext.set_bit_to_arr(rpi__xia, nynta__prum,
                    bnc__fak)
                trxeg__ulhv += 1
        return impl_slice
    raise BodoError(
        'only setitem with scalar index is currently supported for list arrays'
        )


@overload_method(ArrayItemArrayType, 'copy', no_unliteral=True)
def overload_array_item_arr_copy(A):

    def copy_impl(A):
        return init_array_item_array(len(A), get_data(A).copy(),
            get_offsets(A).copy(), get_null_bitmap(A).copy())
    return copy_impl
