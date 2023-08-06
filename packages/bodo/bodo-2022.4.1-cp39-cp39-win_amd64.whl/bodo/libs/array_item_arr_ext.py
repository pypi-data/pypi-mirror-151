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
        vilv__hns = [('n_arrays', types.int64), ('data', fe_type.array_type
            .dtype), ('offsets', types.Array(offset_type, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, vilv__hns)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        vilv__hns = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, vilv__hns)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    vibm__epos = builder.module
    yku__bctwm = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    vcg__fusue = cgutils.get_or_insert_function(vibm__epos, yku__bctwm,
        name='.dtor.array_item.{}'.format(array_item_type.dtype))
    if not vcg__fusue.is_declaration:
        return vcg__fusue
    vcg__fusue.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(vcg__fusue.append_basic_block())
    yugkw__felwm = vcg__fusue.args[0]
    edfqg__ach = context.get_value_type(payload_type).as_pointer()
    hiyog__hozox = builder.bitcast(yugkw__felwm, edfqg__ach)
    xrcky__eyxci = context.make_helper(builder, payload_type, ref=hiyog__hozox)
    context.nrt.decref(builder, array_item_type.dtype, xrcky__eyxci.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'),
        xrcky__eyxci.offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        xrcky__eyxci.null_bitmap)
    builder.ret_void()
    return vcg__fusue


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    ebox__yzsi = context.get_value_type(payload_type)
    hqw__auh = context.get_abi_sizeof(ebox__yzsi)
    qansm__qzn = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    sbgwy__clzo = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, hqw__auh), qansm__qzn)
    lkasn__nqeh = context.nrt.meminfo_data(builder, sbgwy__clzo)
    jhj__hgooc = builder.bitcast(lkasn__nqeh, ebox__yzsi.as_pointer())
    xrcky__eyxci = cgutils.create_struct_proxy(payload_type)(context, builder)
    xrcky__eyxci.n_arrays = n_arrays
    szcwq__lsof = n_elems.type.count
    evfb__ljzqj = builder.extract_value(n_elems, 0)
    ouuh__pjkq = cgutils.alloca_once_value(builder, evfb__ljzqj)
    qrc__cybgx = builder.icmp_signed('==', evfb__ljzqj, lir.Constant(
        evfb__ljzqj.type, -1))
    with builder.if_then(qrc__cybgx):
        builder.store(n_arrays, ouuh__pjkq)
    n_elems = cgutils.pack_array(builder, [builder.load(ouuh__pjkq)] + [
        builder.extract_value(n_elems, zdvbj__emsy) for zdvbj__emsy in
        range(1, szcwq__lsof)])
    xrcky__eyxci.data = gen_allocate_array(context, builder,
        array_item_type.dtype, n_elems, c)
    xnbu__lwt = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    gepob__oyxj = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [xnbu__lwt])
    offsets_ptr = gepob__oyxj.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    xrcky__eyxci.offsets = gepob__oyxj._getvalue()
    gxq__nirkp = builder.udiv(builder.add(n_arrays, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    qaiaj__usi = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [gxq__nirkp])
    null_bitmap_ptr = qaiaj__usi.data
    xrcky__eyxci.null_bitmap = qaiaj__usi._getvalue()
    builder.store(xrcky__eyxci._getvalue(), jhj__hgooc)
    return sbgwy__clzo, xrcky__eyxci.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    ueg__mzj, tyxph__ajw = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    abz__fhaa = context.insert_const_string(builder.module, 'pandas')
    mfpr__pqwk = c.pyapi.import_module_noblock(abz__fhaa)
    sxo__nmz = c.pyapi.object_getattr_string(mfpr__pqwk, 'NA')
    nvdom__ltal = c.context.get_constant(offset_type, 0)
    builder.store(nvdom__ltal, offsets_ptr)
    qflh__itky = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as crt__oey:
        cqwms__yob = crt__oey.index
        item_ind = builder.load(qflh__itky)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [cqwms__yob]))
        arr_obj = seq_getitem(builder, context, val, cqwms__yob)
        set_bitmap_bit(builder, null_bitmap_ptr, cqwms__yob, 0)
        lqd__pau = is_na_value(builder, context, arr_obj, sxo__nmz)
        wcion__yka = builder.icmp_unsigned('!=', lqd__pau, lir.Constant(
            lqd__pau.type, 1))
        with builder.if_then(wcion__yka):
            set_bitmap_bit(builder, null_bitmap_ptr, cqwms__yob, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), qflh__itky)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(qflh__itky), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(mfpr__pqwk)
    c.pyapi.decref(sxo__nmz)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    gjw__bwd = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types
        .int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if gjw__bwd:
        yku__bctwm = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        pjw__cqksh = cgutils.get_or_insert_function(c.builder.module,
            yku__bctwm, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(pjw__cqksh,
            [val])])
    else:
        quqm__fiu = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            quqm__fiu, zdvbj__emsy) for zdvbj__emsy in range(1, quqm__fiu.
            type.count)])
    sbgwy__clzo, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if gjw__bwd:
        uprh__juvt = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        bwq__ysynr = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        yku__bctwm = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        vcg__fusue = cgutils.get_or_insert_function(c.builder.module,
            yku__bctwm, name='array_item_array_from_sequence')
        c.builder.call(vcg__fusue, [val, c.builder.bitcast(bwq__ysynr, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), uprh__juvt)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    wgrw__ncy = c.context.make_helper(c.builder, typ)
    wgrw__ncy.meminfo = sbgwy__clzo
    ztqv__wxw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wgrw__ncy._getvalue(), is_error=ztqv__wxw)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    wgrw__ncy = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    lkasn__nqeh = context.nrt.meminfo_data(builder, wgrw__ncy.meminfo)
    jhj__hgooc = builder.bitcast(lkasn__nqeh, context.get_value_type(
        payload_type).as_pointer())
    xrcky__eyxci = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(jhj__hgooc))
    return xrcky__eyxci


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    abz__fhaa = context.insert_const_string(builder.module, 'numpy')
    keax__wbtvv = c.pyapi.import_module_noblock(abz__fhaa)
    lfa__lzqvs = c.pyapi.object_getattr_string(keax__wbtvv, 'object_')
    iqvd__syy = c.pyapi.long_from_longlong(n_arrays)
    unh__yyvq = c.pyapi.call_method(keax__wbtvv, 'ndarray', (iqvd__syy,
        lfa__lzqvs))
    trp__hza = c.pyapi.object_getattr_string(keax__wbtvv, 'nan')
    qflh__itky = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as crt__oey:
        cqwms__yob = crt__oey.index
        pyarray_setitem(builder, context, unh__yyvq, cqwms__yob, trp__hza)
        osn__lbg = get_bitmap_bit(builder, null_bitmap_ptr, cqwms__yob)
        tnc__cdld = builder.icmp_unsigned('!=', osn__lbg, lir.Constant(lir.
            IntType(8), 0))
        with builder.if_then(tnc__cdld):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(cqwms__yob, lir.Constant(
                cqwms__yob.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [cqwms__yob]))), lir.IntType(64))
            item_ind = builder.load(qflh__itky)
            ueg__mzj, onvxe__coj = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), qflh__itky)
            arr_obj = c.pyapi.from_native_value(typ.dtype, onvxe__coj, c.
                env_manager)
            pyarray_setitem(builder, context, unh__yyvq, cqwms__yob, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(keax__wbtvv)
    c.pyapi.decref(lfa__lzqvs)
    c.pyapi.decref(iqvd__syy)
    c.pyapi.decref(trp__hza)
    return unh__yyvq


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    xrcky__eyxci = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = xrcky__eyxci.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), xrcky__eyxci.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), xrcky__eyxci.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        uprh__juvt = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        bwq__ysynr = c.context.make_helper(c.builder, typ.dtype, data_arr).data
        yku__bctwm = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        ksnj__eaq = cgutils.get_or_insert_function(c.builder.module,
            yku__bctwm, name='np_array_from_array_item_array')
        arr = c.builder.call(ksnj__eaq, [xrcky__eyxci.n_arrays, c.builder.
            bitcast(bwq__ysynr, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), uprh__juvt)])
    else:
        arr = _box_array_item_array_generic(typ, c, xrcky__eyxci.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    syz__fosg, vmi__xdsg, ccjl__asqz = args
    ymytx__ukssc = bodo.utils.transform.get_type_alloc_counts(array_item_type
        .dtype)
    pff__gnetb = sig.args[1]
    if not isinstance(pff__gnetb, types.UniTuple):
        vmi__xdsg = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for ccjl__asqz in range(ymytx__ukssc)])
    elif pff__gnetb.count < ymytx__ukssc:
        vmi__xdsg = cgutils.pack_array(builder, [builder.extract_value(
            vmi__xdsg, zdvbj__emsy) for zdvbj__emsy in range(pff__gnetb.
            count)] + [lir.Constant(lir.IntType(64), -1) for ccjl__asqz in
            range(ymytx__ukssc - pff__gnetb.count)])
    sbgwy__clzo, ccjl__asqz, ccjl__asqz, ccjl__asqz = (
        construct_array_item_array(context, builder, array_item_type,
        syz__fosg, vmi__xdsg))
    wgrw__ncy = context.make_helper(builder, array_item_type)
    wgrw__ncy.meminfo = sbgwy__clzo
    return wgrw__ncy._getvalue()


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
    n_arrays, utj__oeakb, gepob__oyxj, qaiaj__usi = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    ebox__yzsi = context.get_value_type(payload_type)
    hqw__auh = context.get_abi_sizeof(ebox__yzsi)
    qansm__qzn = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    sbgwy__clzo = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, hqw__auh), qansm__qzn)
    lkasn__nqeh = context.nrt.meminfo_data(builder, sbgwy__clzo)
    jhj__hgooc = builder.bitcast(lkasn__nqeh, ebox__yzsi.as_pointer())
    xrcky__eyxci = cgutils.create_struct_proxy(payload_type)(context, builder)
    xrcky__eyxci.n_arrays = n_arrays
    xrcky__eyxci.data = utj__oeakb
    xrcky__eyxci.offsets = gepob__oyxj
    xrcky__eyxci.null_bitmap = qaiaj__usi
    builder.store(xrcky__eyxci._getvalue(), jhj__hgooc)
    context.nrt.incref(builder, signature.args[1], utj__oeakb)
    context.nrt.incref(builder, signature.args[2], gepob__oyxj)
    context.nrt.incref(builder, signature.args[3], qaiaj__usi)
    wgrw__ncy = context.make_helper(builder, array_item_type)
    wgrw__ncy.meminfo = sbgwy__clzo
    return wgrw__ncy._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    xrnq__ogsq = ArrayItemArrayType(data_type)
    sig = xrnq__ogsq(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xrcky__eyxci = _get_array_item_arr_payload(context, builder,
            arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xrcky__eyxci.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        xrcky__eyxci = _get_array_item_arr_payload(context, builder,
            arr_typ, arr)
        bwq__ysynr = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, xrcky__eyxci.offsets).data
        gepob__oyxj = builder.bitcast(bwq__ysynr, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(gepob__oyxj, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xrcky__eyxci = _get_array_item_arr_payload(context, builder,
            arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xrcky__eyxci.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        xrcky__eyxci = _get_array_item_arr_payload(context, builder,
            arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            xrcky__eyxci.null_bitmap)
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
        xrcky__eyxci = _get_array_item_arr_payload(context, builder,
            arr_typ, arr)
        return xrcky__eyxci.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, cgvsh__zmx = args
        wgrw__ncy = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        lkasn__nqeh = context.nrt.meminfo_data(builder, wgrw__ncy.meminfo)
        jhj__hgooc = builder.bitcast(lkasn__nqeh, context.get_value_type(
            payload_type).as_pointer())
        xrcky__eyxci = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(jhj__hgooc))
        context.nrt.decref(builder, data_typ, xrcky__eyxci.data)
        xrcky__eyxci.data = cgvsh__zmx
        context.nrt.incref(builder, data_typ, cgvsh__zmx)
        builder.store(xrcky__eyxci._getvalue(), jhj__hgooc)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    utj__oeakb = get_data(arr)
    cbba__zbkcq = len(utj__oeakb)
    if cbba__zbkcq < new_size:
        wijf__uve = max(2 * cbba__zbkcq, new_size)
        cgvsh__zmx = bodo.libs.array_kernels.resize_and_copy(utj__oeakb,
            old_size, wijf__uve)
        replace_data_arr(arr, cgvsh__zmx)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    utj__oeakb = get_data(arr)
    gepob__oyxj = get_offsets(arr)
    ugxp__brbd = len(utj__oeakb)
    utw__fej = gepob__oyxj[-1]
    if ugxp__brbd != utw__fej:
        cgvsh__zmx = bodo.libs.array_kernels.resize_and_copy(utj__oeakb,
            utw__fej, utw__fej)
        replace_data_arr(arr, cgvsh__zmx)


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
            gepob__oyxj = get_offsets(arr)
            utj__oeakb = get_data(arr)
            mgcbo__wshyf = gepob__oyxj[ind]
            gbj__cref = gepob__oyxj[ind + 1]
            return utj__oeakb[mgcbo__wshyf:gbj__cref]
        return array_item_arr_getitem_impl
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        qzj__tkg = arr.dtype

        def impl_bool(arr, ind):
            whtu__nded = len(arr)
            if whtu__nded != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            qaiaj__usi = get_null_bitmap(arr)
            n_arrays = 0
            uetdd__oehvq = init_nested_counts(qzj__tkg)
            for zdvbj__emsy in range(whtu__nded):
                if ind[zdvbj__emsy]:
                    n_arrays += 1
                    htegk__luoz = arr[zdvbj__emsy]
                    uetdd__oehvq = add_nested_counts(uetdd__oehvq, htegk__luoz)
            unh__yyvq = pre_alloc_array_item_array(n_arrays, uetdd__oehvq,
                qzj__tkg)
            mzsy__ndvcx = get_null_bitmap(unh__yyvq)
            oiu__bgc = 0
            for gxgxc__roi in range(whtu__nded):
                if ind[gxgxc__roi]:
                    unh__yyvq[oiu__bgc] = arr[gxgxc__roi]
                    kwe__ctttg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        qaiaj__usi, gxgxc__roi)
                    bodo.libs.int_arr_ext.set_bit_to_arr(mzsy__ndvcx,
                        oiu__bgc, kwe__ctttg)
                    oiu__bgc += 1
            return unh__yyvq
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        qzj__tkg = arr.dtype

        def impl_int(arr, ind):
            qaiaj__usi = get_null_bitmap(arr)
            whtu__nded = len(ind)
            n_arrays = whtu__nded
            uetdd__oehvq = init_nested_counts(qzj__tkg)
            for kgx__apt in range(whtu__nded):
                zdvbj__emsy = ind[kgx__apt]
                htegk__luoz = arr[zdvbj__emsy]
                uetdd__oehvq = add_nested_counts(uetdd__oehvq, htegk__luoz)
            unh__yyvq = pre_alloc_array_item_array(n_arrays, uetdd__oehvq,
                qzj__tkg)
            mzsy__ndvcx = get_null_bitmap(unh__yyvq)
            for xku__nzbv in range(whtu__nded):
                gxgxc__roi = ind[xku__nzbv]
                unh__yyvq[xku__nzbv] = arr[gxgxc__roi]
                kwe__ctttg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    qaiaj__usi, gxgxc__roi)
                bodo.libs.int_arr_ext.set_bit_to_arr(mzsy__ndvcx, xku__nzbv,
                    kwe__ctttg)
            return unh__yyvq
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            whtu__nded = len(arr)
            zhenv__gxm = numba.cpython.unicode._normalize_slice(ind, whtu__nded
                )
            nib__zbqn = np.arange(zhenv__gxm.start, zhenv__gxm.stop,
                zhenv__gxm.step)
            return arr[nib__zbqn]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            gepob__oyxj = get_offsets(A)
            qaiaj__usi = get_null_bitmap(A)
            if idx == 0:
                gepob__oyxj[0] = 0
            n_items = len(val)
            zhu__hib = gepob__oyxj[idx] + n_items
            ensure_data_capacity(A, gepob__oyxj[idx], zhu__hib)
            utj__oeakb = get_data(A)
            gepob__oyxj[idx + 1] = gepob__oyxj[idx] + n_items
            utj__oeakb[gepob__oyxj[idx]:gepob__oyxj[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(qaiaj__usi, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            zhenv__gxm = numba.cpython.unicode._normalize_slice(idx, len(A))
            for zdvbj__emsy in range(zhenv__gxm.start, zhenv__gxm.stop,
                zhenv__gxm.step):
                A[zdvbj__emsy] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            gepob__oyxj = get_offsets(A)
            qaiaj__usi = get_null_bitmap(A)
            xru__txety = get_offsets(val)
            hqjh__pafw = get_data(val)
            bnxlk__vwt = get_null_bitmap(val)
            whtu__nded = len(A)
            zhenv__gxm = numba.cpython.unicode._normalize_slice(idx, whtu__nded
                )
            spxo__izupi, nqq__snr = zhenv__gxm.start, zhenv__gxm.stop
            assert zhenv__gxm.step == 1
            if spxo__izupi == 0:
                gepob__oyxj[spxo__izupi] = 0
            keih__acar = gepob__oyxj[spxo__izupi]
            zhu__hib = keih__acar + len(hqjh__pafw)
            ensure_data_capacity(A, keih__acar, zhu__hib)
            utj__oeakb = get_data(A)
            utj__oeakb[keih__acar:keih__acar + len(hqjh__pafw)] = hqjh__pafw
            gepob__oyxj[spxo__izupi:nqq__snr + 1] = xru__txety + keih__acar
            tkhs__rqw = 0
            for zdvbj__emsy in range(spxo__izupi, nqq__snr):
                kwe__ctttg = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    bnxlk__vwt, tkhs__rqw)
                bodo.libs.int_arr_ext.set_bit_to_arr(qaiaj__usi,
                    zdvbj__emsy, kwe__ctttg)
                tkhs__rqw += 1
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
