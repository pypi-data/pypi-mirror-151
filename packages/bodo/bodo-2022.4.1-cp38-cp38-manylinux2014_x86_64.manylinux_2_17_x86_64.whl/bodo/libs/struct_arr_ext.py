"""Array implementation for structs of values.
Corresponds to Spark's StructType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Struct arrays: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in contiguous data arrays; one array per field. For example:
A:             ["AA", "B", "C"]
B:             [1, 2, 4]
"""
import operator
import llvmlite.binding as ll
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
from numba.typed.typedobjectutils import _cast
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_int, get_overload_const_str, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, is_overload_none
ll.add_symbol('struct_array_from_sequence', array_ext.
    struct_array_from_sequence)
ll.add_symbol('np_array_from_struct_array', array_ext.
    np_array_from_struct_array)


class StructArrayType(types.ArrayCompatible):

    def __init__(self, data, names=None):
        assert isinstance(data, tuple) and len(data) > 0 and all(bodo.utils
            .utils.is_array_typ(kvoak__cux, False) for kvoak__cux in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(kvoak__cux,
                str) for kvoak__cux in names) and len(names) == len(data)
        else:
            names = tuple('f{}'.format(i) for i in range(len(data)))
        self.data = data
        self.names = names
        super(StructArrayType, self).__init__(name=
            'StructArrayType({}, {})'.format(data, names))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return StructType(tuple(hmmt__ojhgh.dtype for hmmt__ojhgh in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(kvoak__cux) for kvoak__cux in d.keys())
        data = tuple(dtype_to_array_type(hmmt__ojhgh) for hmmt__ojhgh in d.
            values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(kvoak__cux, False) for kvoak__cux in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mhw__iljjw = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, mhw__iljjw)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        mhw__iljjw = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, mhw__iljjw)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    kdoc__nilns = builder.module
    lgjav__ybw = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    lhln__aqvsa = cgutils.get_or_insert_function(kdoc__nilns, lgjav__ybw,
        name='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not lhln__aqvsa.is_declaration:
        return lhln__aqvsa
    lhln__aqvsa.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(lhln__aqvsa.append_basic_block())
    lgy__xepcl = lhln__aqvsa.args[0]
    mycmb__slh = context.get_value_type(payload_type).as_pointer()
    cns__jkrba = builder.bitcast(lgy__xepcl, mycmb__slh)
    mqjxj__agmbw = context.make_helper(builder, payload_type, ref=cns__jkrba)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), mqjxj__agmbw.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        mqjxj__agmbw.null_bitmap)
    builder.ret_void()
    return lhln__aqvsa


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    xniz__ubauf = context.get_value_type(payload_type)
    vrhm__orp = context.get_abi_sizeof(xniz__ubauf)
    imbp__iaq = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    bdcjl__csc = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, vrhm__orp), imbp__iaq)
    zmh__kvnc = context.nrt.meminfo_data(builder, bdcjl__csc)
    guw__zak = builder.bitcast(zmh__kvnc, xniz__ubauf.as_pointer())
    mqjxj__agmbw = cgutils.create_struct_proxy(payload_type)(context, builder)
    lrupy__mpixk = []
    faorx__iycb = 0
    for arr_typ in struct_arr_type.data:
        mla__aaqap = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        qjnsm__gthvc = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(faorx__iycb, 
            faorx__iycb + mla__aaqap)])
        arr = gen_allocate_array(context, builder, arr_typ, qjnsm__gthvc, c)
        lrupy__mpixk.append(arr)
        faorx__iycb += mla__aaqap
    mqjxj__agmbw.data = cgutils.pack_array(builder, lrupy__mpixk
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, lrupy__mpixk)
    xym__cgw = builder.udiv(builder.add(n_structs, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    qodzy__hfvtl = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [xym__cgw])
    null_bitmap_ptr = qodzy__hfvtl.data
    mqjxj__agmbw.null_bitmap = qodzy__hfvtl._getvalue()
    builder.store(mqjxj__agmbw._getvalue(), guw__zak)
    return bdcjl__csc, mqjxj__agmbw.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    gca__kajg = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        ktzag__ori = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            ktzag__ori)
        gca__kajg.append(arr.data)
    bpoig__adxic = cgutils.pack_array(c.builder, gca__kajg
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, gca__kajg)
    mnevx__haxhj = cgutils.alloca_once_value(c.builder, bpoig__adxic)
    dyr__ftkpd = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(kvoak__cux.dtype)) for kvoak__cux in data_typ]
    gulpx__pphvv = cgutils.alloca_once_value(c.builder, cgutils.pack_array(
        c.builder, dyr__ftkpd))
    jwf__pab = cgutils.pack_array(c.builder, [c.context.insert_const_string
        (c.builder.module, kvoak__cux) for kvoak__cux in names])
    uzy__jtiu = cgutils.alloca_once_value(c.builder, jwf__pab)
    return mnevx__haxhj, gulpx__pphvv, uzy__jtiu


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    wxpde__ednn = all(isinstance(hmmt__ojhgh, types.Array) and hmmt__ojhgh.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for hmmt__ojhgh in typ.data)
    if wxpde__ednn:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        xzixt__qfw = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            xzixt__qfw, i) for i in range(1, xzixt__qfw.type.count)], lir.
            IntType(64))
    bdcjl__csc, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if wxpde__ednn:
        mnevx__haxhj, gulpx__pphvv, uzy__jtiu = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        lgjav__ybw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        lhln__aqvsa = cgutils.get_or_insert_function(c.builder.module,
            lgjav__ybw, name='struct_array_from_sequence')
        c.builder.call(lhln__aqvsa, [val, c.context.get_constant(types.
            int32, len(typ.data)), c.builder.bitcast(mnevx__haxhj, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            gulpx__pphvv, lir.IntType(8).as_pointer()), c.builder.bitcast(
            uzy__jtiu, lir.IntType(8).as_pointer()), c.context.get_constant
            (types.bool_, is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    lzsga__ied = c.context.make_helper(c.builder, typ)
    lzsga__ied.meminfo = bdcjl__csc
    yrrqp__qbes = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lzsga__ied._getvalue(), is_error=yrrqp__qbes)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    zvkkq__kzs = context.insert_const_string(builder.module, 'pandas')
    muoh__tnfr = c.pyapi.import_module_noblock(zvkkq__kzs)
    hqh__trbg = c.pyapi.object_getattr_string(muoh__tnfr, 'NA')
    with cgutils.for_range(builder, n_structs) as yvih__qvz:
        nqqtg__rhg = yvih__qvz.index
        cra__ybm = seq_getitem(builder, context, val, nqqtg__rhg)
        set_bitmap_bit(builder, null_bitmap_ptr, nqqtg__rhg, 0)
        for jckn__wwn in range(len(typ.data)):
            arr_typ = typ.data[jckn__wwn]
            data_arr = builder.extract_value(data_tup, jckn__wwn)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            pcxca__srxj, gbdh__cto = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, nqqtg__rhg])
        icl__jpim = is_na_value(builder, context, cra__ybm, hqh__trbg)
        yacxj__koe = builder.icmp_unsigned('!=', icl__jpim, lir.Constant(
            icl__jpim.type, 1))
        with builder.if_then(yacxj__koe):
            set_bitmap_bit(builder, null_bitmap_ptr, nqqtg__rhg, 1)
            for jckn__wwn in range(len(typ.data)):
                arr_typ = typ.data[jckn__wwn]
                if is_tuple_array:
                    smpb__qxdj = c.pyapi.tuple_getitem(cra__ybm, jckn__wwn)
                else:
                    smpb__qxdj = c.pyapi.dict_getitem_string(cra__ybm, typ.
                        names[jckn__wwn])
                icl__jpim = is_na_value(builder, context, smpb__qxdj, hqh__trbg
                    )
                yacxj__koe = builder.icmp_unsigned('!=', icl__jpim, lir.
                    Constant(icl__jpim.type, 1))
                with builder.if_then(yacxj__koe):
                    smpb__qxdj = to_arr_obj_if_list_obj(c, context, builder,
                        smpb__qxdj, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        smpb__qxdj).value
                    data_arr = builder.extract_value(data_tup, jckn__wwn)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    pcxca__srxj, gbdh__cto = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, nqqtg__rhg, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(cra__ybm)
    c.pyapi.decref(muoh__tnfr)
    c.pyapi.decref(hqh__trbg)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    lzsga__ied = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    zmh__kvnc = context.nrt.meminfo_data(builder, lzsga__ied.meminfo)
    guw__zak = builder.bitcast(zmh__kvnc, context.get_value_type(
        payload_type).as_pointer())
    mqjxj__agmbw = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(guw__zak))
    return mqjxj__agmbw


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    mqjxj__agmbw = _get_struct_arr_payload(c.context, c.builder, typ, val)
    pcxca__srxj, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), mqjxj__agmbw.null_bitmap).data
    wxpde__ednn = all(isinstance(hmmt__ojhgh, types.Array) and hmmt__ojhgh.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for hmmt__ojhgh in typ.data)
    if wxpde__ednn:
        mnevx__haxhj, gulpx__pphvv, uzy__jtiu = _get_C_API_ptrs(c,
            mqjxj__agmbw.data, typ.data, typ.names)
        lgjav__ybw = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        idqed__clss = cgutils.get_or_insert_function(c.builder.module,
            lgjav__ybw, name='np_array_from_struct_array')
        arr = c.builder.call(idqed__clss, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(mnevx__haxhj,
            lir.IntType(8).as_pointer()), null_bitmap_ptr, c.builder.
            bitcast(gulpx__pphvv, lir.IntType(8).as_pointer()), c.builder.
            bitcast(uzy__jtiu, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, mqjxj__agmbw.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    zvkkq__kzs = context.insert_const_string(builder.module, 'numpy')
    spp__sbrot = c.pyapi.import_module_noblock(zvkkq__kzs)
    axb__viq = c.pyapi.object_getattr_string(spp__sbrot, 'object_')
    mrv__qhiky = c.pyapi.long_from_longlong(length)
    gek__qff = c.pyapi.call_method(spp__sbrot, 'ndarray', (mrv__qhiky,
        axb__viq))
    orbi__mvw = c.pyapi.object_getattr_string(spp__sbrot, 'nan')
    with cgutils.for_range(builder, length) as yvih__qvz:
        nqqtg__rhg = yvih__qvz.index
        pyarray_setitem(builder, context, gek__qff, nqqtg__rhg, orbi__mvw)
        oold__uzb = get_bitmap_bit(builder, null_bitmap_ptr, nqqtg__rhg)
        fjph__vek = builder.icmp_unsigned('!=', oold__uzb, lir.Constant(lir
            .IntType(8), 0))
        with builder.if_then(fjph__vek):
            if is_tuple_array:
                cra__ybm = c.pyapi.tuple_new(len(typ.data))
            else:
                cra__ybm = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(orbi__mvw)
                    c.pyapi.tuple_setitem(cra__ybm, i, orbi__mvw)
                else:
                    c.pyapi.dict_setitem_string(cra__ybm, typ.names[i],
                        orbi__mvw)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                pcxca__srxj, eqprh__npa = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, nqqtg__rhg])
                with builder.if_then(eqprh__npa):
                    pcxca__srxj, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, nqqtg__rhg])
                    nhfxc__xffb = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(cra__ybm, i, nhfxc__xffb)
                    else:
                        c.pyapi.dict_setitem_string(cra__ybm, typ.names[i],
                            nhfxc__xffb)
                        c.pyapi.decref(nhfxc__xffb)
            pyarray_setitem(builder, context, gek__qff, nqqtg__rhg, cra__ybm)
            c.pyapi.decref(cra__ybm)
    c.pyapi.decref(spp__sbrot)
    c.pyapi.decref(axb__viq)
    c.pyapi.decref(mrv__qhiky)
    c.pyapi.decref(orbi__mvw)
    return gek__qff


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    cknut__fipu = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if cknut__fipu == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for sop__zwap in range(cknut__fipu)])
    elif nested_counts_type.count < cknut__fipu:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for sop__zwap in range(
            cknut__fipu - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(hmmt__ojhgh) for hmmt__ojhgh in
            names_typ.types)
    quod__noeah = tuple(hmmt__ojhgh.instance_type for hmmt__ojhgh in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(quod__noeah, names)

    def codegen(context, builder, sig, args):
        gzxxm__cxa, nested_counts, sop__zwap, sop__zwap = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        bdcjl__csc, sop__zwap, sop__zwap = construct_struct_array(context,
            builder, struct_arr_type, gzxxm__cxa, nested_counts)
        lzsga__ied = context.make_helper(builder, struct_arr_type)
        lzsga__ied.meminfo = bdcjl__csc
        return lzsga__ied._getvalue()
    return struct_arr_type(num_structs_typ, nested_counts_typ, dtypes_typ,
        names_typ), codegen


def pre_alloc_struct_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_struct_arr_ext_pre_alloc_struct_array
    ) = pre_alloc_struct_array_equiv


class StructType(types.Type):

    def __init__(self, data, names):
        assert isinstance(data, tuple) and len(data) > 0
        assert isinstance(names, tuple) and all(isinstance(kvoak__cux, str) for
            kvoak__cux in names) and len(names) == len(data)
        self.data = data
        self.names = names
        super(StructType, self).__init__(name='StructType({}, {})'.format(
            data, names))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple)
        self.data = data
        super(StructPayloadType, self).__init__(name=
            'StructPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructPayloadType)
class StructPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mhw__iljjw = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, mhw__iljjw)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        mhw__iljjw = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, mhw__iljjw)


def define_struct_dtor(context, builder, struct_type, payload_type):
    kdoc__nilns = builder.module
    lgjav__ybw = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    lhln__aqvsa = cgutils.get_or_insert_function(kdoc__nilns, lgjav__ybw,
        name='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not lhln__aqvsa.is_declaration:
        return lhln__aqvsa
    lhln__aqvsa.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(lhln__aqvsa.append_basic_block())
    lgy__xepcl = lhln__aqvsa.args[0]
    mycmb__slh = context.get_value_type(payload_type).as_pointer()
    cns__jkrba = builder.bitcast(lgy__xepcl, mycmb__slh)
    mqjxj__agmbw = context.make_helper(builder, payload_type, ref=cns__jkrba)
    for i in range(len(struct_type.data)):
        wxa__ultb = builder.extract_value(mqjxj__agmbw.null_bitmap, i)
        fjph__vek = builder.icmp_unsigned('==', wxa__ultb, lir.Constant(
            wxa__ultb.type, 1))
        with builder.if_then(fjph__vek):
            val = builder.extract_value(mqjxj__agmbw.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return lhln__aqvsa


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    zmh__kvnc = context.nrt.meminfo_data(builder, struct.meminfo)
    guw__zak = builder.bitcast(zmh__kvnc, context.get_value_type(
        payload_type).as_pointer())
    mqjxj__agmbw = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(guw__zak))
    return mqjxj__agmbw, guw__zak


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    zvkkq__kzs = context.insert_const_string(builder.module, 'pandas')
    muoh__tnfr = c.pyapi.import_module_noblock(zvkkq__kzs)
    hqh__trbg = c.pyapi.object_getattr_string(muoh__tnfr, 'NA')
    rbkxl__msku = []
    nulls = []
    for i, hmmt__ojhgh in enumerate(typ.data):
        nhfxc__xffb = c.pyapi.dict_getitem_string(val, typ.names[i])
        wtezv__zvwz = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        btz__rcbvx = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(hmmt__ojhgh)))
        icl__jpim = is_na_value(builder, context, nhfxc__xffb, hqh__trbg)
        fjph__vek = builder.icmp_unsigned('!=', icl__jpim, lir.Constant(
            icl__jpim.type, 1))
        with builder.if_then(fjph__vek):
            builder.store(context.get_constant(types.uint8, 1), wtezv__zvwz)
            field_val = c.pyapi.to_native_value(hmmt__ojhgh, nhfxc__xffb).value
            builder.store(field_val, btz__rcbvx)
        rbkxl__msku.append(builder.load(btz__rcbvx))
        nulls.append(builder.load(wtezv__zvwz))
    c.pyapi.decref(muoh__tnfr)
    c.pyapi.decref(hqh__trbg)
    bdcjl__csc = construct_struct(context, builder, typ, rbkxl__msku, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = bdcjl__csc
    yrrqp__qbes = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=yrrqp__qbes)


@box(StructType)
def box_struct(typ, val, c):
    btou__qmn = c.pyapi.dict_new(len(typ.data))
    mqjxj__agmbw, sop__zwap = _get_struct_payload(c.context, c.builder, typ,
        val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(btou__qmn, typ.names[i], c.pyapi.
            borrow_none())
        wxa__ultb = c.builder.extract_value(mqjxj__agmbw.null_bitmap, i)
        fjph__vek = c.builder.icmp_unsigned('==', wxa__ultb, lir.Constant(
            wxa__ultb.type, 1))
        with c.builder.if_then(fjph__vek):
            nfa__biz = c.builder.extract_value(mqjxj__agmbw.data, i)
            c.context.nrt.incref(c.builder, val_typ, nfa__biz)
            smpb__qxdj = c.pyapi.from_native_value(val_typ, nfa__biz, c.
                env_manager)
            c.pyapi.dict_setitem_string(btou__qmn, typ.names[i], smpb__qxdj)
            c.pyapi.decref(smpb__qxdj)
    c.context.nrt.decref(c.builder, typ, val)
    return btou__qmn


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(hmmt__ojhgh) for hmmt__ojhgh in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, egbi__rgzr = args
        payload_type = StructPayloadType(struct_type.data)
        xniz__ubauf = context.get_value_type(payload_type)
        vrhm__orp = context.get_abi_sizeof(xniz__ubauf)
        imbp__iaq = define_struct_dtor(context, builder, struct_type,
            payload_type)
        bdcjl__csc = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, vrhm__orp), imbp__iaq)
        zmh__kvnc = context.nrt.meminfo_data(builder, bdcjl__csc)
        guw__zak = builder.bitcast(zmh__kvnc, xniz__ubauf.as_pointer())
        mqjxj__agmbw = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        mqjxj__agmbw.data = data
        mqjxj__agmbw.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for sop__zwap in range(len(
            data_typ.types))])
        builder.store(mqjxj__agmbw._getvalue(), guw__zak)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = bdcjl__csc
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        mqjxj__agmbw, sop__zwap = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mqjxj__agmbw.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        mqjxj__agmbw, sop__zwap = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mqjxj__agmbw.null_bitmap)
    nel__jqoj = types.UniTuple(types.int8, len(struct_typ.data))
    return nel__jqoj(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, sop__zwap, val = args
        mqjxj__agmbw, guw__zak = _get_struct_payload(context, builder,
            struct_typ, struct)
        skzhm__pyroc = mqjxj__agmbw.data
        jperq__kprkc = builder.insert_value(skzhm__pyroc, val, field_ind)
        ndnag__mmac = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, ndnag__mmac, skzhm__pyroc)
        context.nrt.incref(builder, ndnag__mmac, jperq__kprkc)
        mqjxj__agmbw.data = jperq__kprkc
        builder.store(mqjxj__agmbw._getvalue(), guw__zak)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    zzk__ddzx = get_overload_const_str(ind)
    if zzk__ddzx not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            zzk__ddzx, struct))
    return struct.names.index(zzk__ddzx)


def is_field_value_null(s, field_name):
    pass


@overload(is_field_value_null, no_unliteral=True)
def overload_is_field_value_null(s, field_name):
    field_ind = _get_struct_field_ind(s, field_name, 'element access (getitem)'
        )
    return lambda s, field_name: get_struct_null_bitmap(s)[field_ind] == 0


@overload(operator.getitem, no_unliteral=True)
def struct_getitem(struct, ind):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'element access (getitem)')
    return lambda struct, ind: get_struct_data(struct)[field_ind]


@overload(operator.setitem, no_unliteral=True)
def struct_setitem(struct, ind, val):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'item assignment (setitem)')
    field_typ = struct.data[field_ind]
    return lambda struct, ind, val: set_struct_data(struct, field_ind,
        _cast(val, field_typ))


@overload(len, no_unliteral=True)
def overload_struct_arr_len(struct):
    if isinstance(struct, StructType):
        num_fields = len(struct.data)
        return lambda struct: num_fields


def construct_struct(context, builder, struct_type, values, nulls):
    payload_type = StructPayloadType(struct_type.data)
    xniz__ubauf = context.get_value_type(payload_type)
    vrhm__orp = context.get_abi_sizeof(xniz__ubauf)
    imbp__iaq = define_struct_dtor(context, builder, struct_type, payload_type)
    bdcjl__csc = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, vrhm__orp), imbp__iaq)
    zmh__kvnc = context.nrt.meminfo_data(builder, bdcjl__csc)
    guw__zak = builder.bitcast(zmh__kvnc, xniz__ubauf.as_pointer())
    mqjxj__agmbw = cgutils.create_struct_proxy(payload_type)(context, builder)
    mqjxj__agmbw.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    mqjxj__agmbw.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(mqjxj__agmbw._getvalue(), guw__zak)
    return bdcjl__csc


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    dbg__cuypc = tuple(d.dtype for d in struct_arr_typ.data)
    ftbtk__payp = StructType(dbg__cuypc, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        bwx__aftzp, ind = args
        mqjxj__agmbw = _get_struct_arr_payload(context, builder,
            struct_arr_typ, bwx__aftzp)
        rbkxl__msku = []
        bmct__znqe = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            ktzag__ori = builder.extract_value(mqjxj__agmbw.data, i)
            plzx__ihkjm = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [ktzag__ori,
                ind])
            bmct__znqe.append(plzx__ihkjm)
            bxfdt__ezqh = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            fjph__vek = builder.icmp_unsigned('==', plzx__ihkjm, lir.
                Constant(plzx__ihkjm.type, 1))
            with builder.if_then(fjph__vek):
                fttat__krew = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    ktzag__ori, ind])
                builder.store(fttat__krew, bxfdt__ezqh)
            rbkxl__msku.append(builder.load(bxfdt__ezqh))
        if isinstance(ftbtk__payp, types.DictType):
            zej__wgsx = [context.insert_const_string(builder.module,
                vvok__gzj) for vvok__gzj in struct_arr_typ.names]
            ykz__eeef = cgutils.pack_array(builder, rbkxl__msku)
            mqmfh__uinj = cgutils.pack_array(builder, zej__wgsx)

            def impl(names, vals):
                d = {}
                for i, vvok__gzj in enumerate(names):
                    d[vvok__gzj] = vals[i]
                return d
            wel__mucuw = context.compile_internal(builder, impl,
                ftbtk__payp(types.Tuple(tuple(types.StringLiteral(vvok__gzj
                ) for vvok__gzj in struct_arr_typ.names)), types.Tuple(
                dbg__cuypc)), [mqmfh__uinj, ykz__eeef])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                dbg__cuypc), ykz__eeef)
            return wel__mucuw
        bdcjl__csc = construct_struct(context, builder, ftbtk__payp,
            rbkxl__msku, bmct__znqe)
        struct = context.make_helper(builder, ftbtk__payp)
        struct.meminfo = bdcjl__csc
        return struct._getvalue()
    return ftbtk__payp(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        mqjxj__agmbw = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mqjxj__agmbw.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        mqjxj__agmbw = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            mqjxj__agmbw.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(hmmt__ojhgh) for hmmt__ojhgh in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, qodzy__hfvtl, egbi__rgzr = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        xniz__ubauf = context.get_value_type(payload_type)
        vrhm__orp = context.get_abi_sizeof(xniz__ubauf)
        imbp__iaq = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        bdcjl__csc = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, vrhm__orp), imbp__iaq)
        zmh__kvnc = context.nrt.meminfo_data(builder, bdcjl__csc)
        guw__zak = builder.bitcast(zmh__kvnc, xniz__ubauf.as_pointer())
        mqjxj__agmbw = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        mqjxj__agmbw.data = data
        mqjxj__agmbw.null_bitmap = qodzy__hfvtl
        builder.store(mqjxj__agmbw._getvalue(), guw__zak)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, qodzy__hfvtl)
        lzsga__ied = context.make_helper(builder, struct_arr_type)
        lzsga__ied.meminfo = bdcjl__csc
        return lzsga__ied._getvalue()
    return struct_arr_type(data_typ, null_bitmap_typ, names_typ), codegen


@overload(operator.getitem, no_unliteral=True)
def struct_arr_getitem(arr, ind):
    if not isinstance(arr, StructArrayType):
        return
    if isinstance(ind, types.Integer):

        def struct_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            return struct_array_get_struct(arr, ind)
        return struct_arr_getitem_impl
    eijde__tmu = len(arr.data)
    jib__dgou = 'def impl(arr, ind):\n'
    jib__dgou += '  data = get_data(arr)\n'
    jib__dgou += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        jib__dgou += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        jib__dgou += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        jib__dgou += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    jib__dgou += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(eijde__tmu)), ', '.join("'{}'".format(vvok__gzj) for
        vvok__gzj in arr.names)))
    vdldv__fjsv = {}
    exec(jib__dgou, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, vdldv__fjsv)
    impl = vdldv__fjsv['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        eijde__tmu = len(arr.data)
        jib__dgou = 'def impl(arr, ind, val):\n'
        jib__dgou += '  data = get_data(arr)\n'
        jib__dgou += '  null_bitmap = get_null_bitmap(arr)\n'
        jib__dgou += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(eijde__tmu):
            if isinstance(val, StructType):
                jib__dgou += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                jib__dgou += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                jib__dgou += '  else:\n'
                jib__dgou += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                jib__dgou += "  data[{}][ind] = val['{}']\n".format(i, arr.
                    names[i])
        vdldv__fjsv = {}
        exec(jib__dgou, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, vdldv__fjsv)
        impl = vdldv__fjsv['impl']
        return impl
    if isinstance(ind, types.SliceType):
        eijde__tmu = len(arr.data)
        jib__dgou = 'def impl(arr, ind, val):\n'
        jib__dgou += '  data = get_data(arr)\n'
        jib__dgou += '  null_bitmap = get_null_bitmap(arr)\n'
        jib__dgou += '  val_data = get_data(val)\n'
        jib__dgou += '  val_null_bitmap = get_null_bitmap(val)\n'
        jib__dgou += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(eijde__tmu):
            jib__dgou += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        vdldv__fjsv = {}
        exec(jib__dgou, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, vdldv__fjsv)
        impl = vdldv__fjsv['impl']
        return impl
    raise BodoError(
        'only setitem with scalar/slice index is currently supported for struct arrays'
        )


@overload(len, no_unliteral=True)
def overload_struct_arr_len(A):
    if isinstance(A, StructArrayType):
        return lambda A: len(get_data(A)[0])


@overload_attribute(StructArrayType, 'shape')
def overload_struct_arr_shape(A):
    return lambda A: (len(get_data(A)[0]),)


@overload_attribute(StructArrayType, 'dtype')
def overload_struct_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(StructArrayType, 'ndim')
def overload_struct_arr_ndim(A):
    return lambda A: 1


@overload_attribute(StructArrayType, 'nbytes')
def overload_struct_arr_nbytes(A):
    jib__dgou = 'def impl(A):\n'
    jib__dgou += '  total_nbytes = 0\n'
    jib__dgou += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        jib__dgou += f'  total_nbytes += data[{i}].nbytes\n'
    jib__dgou += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    jib__dgou += '  return total_nbytes\n'
    vdldv__fjsv = {}
    exec(jib__dgou, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, vdldv__fjsv)
    impl = vdldv__fjsv['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        qodzy__hfvtl = get_null_bitmap(A)
        xqdgj__vpra = bodo.ir.join.copy_arr_tup(data)
        eomww__fvao = qodzy__hfvtl.copy()
        return init_struct_arr(xqdgj__vpra, eomww__fvao, names)
    return copy_impl
