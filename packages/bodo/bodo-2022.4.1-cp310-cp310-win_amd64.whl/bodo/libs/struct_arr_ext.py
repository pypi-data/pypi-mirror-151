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
            .utils.is_array_typ(iujr__iqwtf, False) for iujr__iqwtf in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(iujr__iqwtf,
                str) for iujr__iqwtf in names) and len(names) == len(data)
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
        return StructType(tuple(spkml__mdh.dtype for spkml__mdh in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(iujr__iqwtf) for iujr__iqwtf in d.keys())
        data = tuple(dtype_to_array_type(spkml__mdh) for spkml__mdh in d.
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
            is_array_typ(iujr__iqwtf, False) for iujr__iqwtf in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qvdk__qlojx = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, qvdk__qlojx)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        qvdk__qlojx = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, qvdk__qlojx)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    pth__znnhi = builder.module
    ugga__tft = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    diyr__mefx = cgutils.get_or_insert_function(pth__znnhi, ugga__tft, name
        ='.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not diyr__mefx.is_declaration:
        return diyr__mefx
    diyr__mefx.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(diyr__mefx.append_basic_block())
    jibz__kht = diyr__mefx.args[0]
    nfgck__cwka = context.get_value_type(payload_type).as_pointer()
    iva__tiggw = builder.bitcast(jibz__kht, nfgck__cwka)
    aptx__zjg = context.make_helper(builder, payload_type, ref=iva__tiggw)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), aptx__zjg.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), aptx__zjg
        .null_bitmap)
    builder.ret_void()
    return diyr__mefx


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    dqpqa__vfqb = context.get_value_type(payload_type)
    rjeb__kslg = context.get_abi_sizeof(dqpqa__vfqb)
    ifyq__cgltt = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    tdzx__bwb = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, rjeb__kslg), ifyq__cgltt)
    ltnol__qkhc = context.nrt.meminfo_data(builder, tdzx__bwb)
    vhqw__ctbqb = builder.bitcast(ltnol__qkhc, dqpqa__vfqb.as_pointer())
    aptx__zjg = cgutils.create_struct_proxy(payload_type)(context, builder)
    gytpw__cdg = []
    eaevw__pzjms = 0
    for arr_typ in struct_arr_type.data:
        xylps__oeck = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        mft__stckj = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(eaevw__pzjms, 
            eaevw__pzjms + xylps__oeck)])
        arr = gen_allocate_array(context, builder, arr_typ, mft__stckj, c)
        gytpw__cdg.append(arr)
        eaevw__pzjms += xylps__oeck
    aptx__zjg.data = cgutils.pack_array(builder, gytpw__cdg
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, gytpw__cdg)
    qysro__xar = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    lnfea__ksk = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [qysro__xar])
    null_bitmap_ptr = lnfea__ksk.data
    aptx__zjg.null_bitmap = lnfea__ksk._getvalue()
    builder.store(aptx__zjg._getvalue(), vhqw__ctbqb)
    return tdzx__bwb, aptx__zjg.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    facjl__ekt = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        qnugk__ksya = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            qnugk__ksya)
        facjl__ekt.append(arr.data)
    mrkb__inay = cgutils.pack_array(c.builder, facjl__ekt
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, facjl__ekt)
    ulc__nhwr = cgutils.alloca_once_value(c.builder, mrkb__inay)
    ctjzk__rpy = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(iujr__iqwtf.dtype)) for iujr__iqwtf in data_typ]
    xny__urwrs = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, ctjzk__rpy))
    dua__qbume = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, iujr__iqwtf) for iujr__iqwtf in
        names])
    wougb__vgkp = cgutils.alloca_once_value(c.builder, dua__qbume)
    return ulc__nhwr, xny__urwrs, wougb__vgkp


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    zzytg__igprq = all(isinstance(spkml__mdh, types.Array) and spkml__mdh.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for spkml__mdh in typ.data)
    if zzytg__igprq:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        wskx__idd = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            wskx__idd, i) for i in range(1, wskx__idd.type.count)], lir.
            IntType(64))
    tdzx__bwb, data_tup, null_bitmap_ptr = construct_struct_array(c.context,
        c.builder, typ, n_structs, n_elems, c)
    if zzytg__igprq:
        ulc__nhwr, xny__urwrs, wougb__vgkp = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        ugga__tft = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        diyr__mefx = cgutils.get_or_insert_function(c.builder.module,
            ugga__tft, name='struct_array_from_sequence')
        c.builder.call(diyr__mefx, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(ulc__nhwr, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(xny__urwrs,
            lir.IntType(8).as_pointer()), c.builder.bitcast(wougb__vgkp,
            lir.IntType(8).as_pointer()), c.context.get_constant(types.
            bool_, is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    kvr__jrmiz = c.context.make_helper(c.builder, typ)
    kvr__jrmiz.meminfo = tdzx__bwb
    qtfxr__ioro = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(kvr__jrmiz._getvalue(), is_error=qtfxr__ioro)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    qzl__wazon = context.insert_const_string(builder.module, 'pandas')
    ojjor__buibm = c.pyapi.import_module_noblock(qzl__wazon)
    kdwb__msi = c.pyapi.object_getattr_string(ojjor__buibm, 'NA')
    with cgutils.for_range(builder, n_structs) as lbsti__ggd:
        unf__iwp = lbsti__ggd.index
        uait__hxavg = seq_getitem(builder, context, val, unf__iwp)
        set_bitmap_bit(builder, null_bitmap_ptr, unf__iwp, 0)
        for brgn__qxcje in range(len(typ.data)):
            arr_typ = typ.data[brgn__qxcje]
            data_arr = builder.extract_value(data_tup, brgn__qxcje)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            lhcr__tijl, ctl__fmng = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, unf__iwp])
        fwml__xbloj = is_na_value(builder, context, uait__hxavg, kdwb__msi)
        gidqh__vosu = builder.icmp_unsigned('!=', fwml__xbloj, lir.Constant
            (fwml__xbloj.type, 1))
        with builder.if_then(gidqh__vosu):
            set_bitmap_bit(builder, null_bitmap_ptr, unf__iwp, 1)
            for brgn__qxcje in range(len(typ.data)):
                arr_typ = typ.data[brgn__qxcje]
                if is_tuple_array:
                    jbrsh__apz = c.pyapi.tuple_getitem(uait__hxavg, brgn__qxcje
                        )
                else:
                    jbrsh__apz = c.pyapi.dict_getitem_string(uait__hxavg,
                        typ.names[brgn__qxcje])
                fwml__xbloj = is_na_value(builder, context, jbrsh__apz,
                    kdwb__msi)
                gidqh__vosu = builder.icmp_unsigned('!=', fwml__xbloj, lir.
                    Constant(fwml__xbloj.type, 1))
                with builder.if_then(gidqh__vosu):
                    jbrsh__apz = to_arr_obj_if_list_obj(c, context, builder,
                        jbrsh__apz, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        jbrsh__apz).value
                    data_arr = builder.extract_value(data_tup, brgn__qxcje)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    lhcr__tijl, ctl__fmng = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, unf__iwp, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(uait__hxavg)
    c.pyapi.decref(ojjor__buibm)
    c.pyapi.decref(kdwb__msi)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    kvr__jrmiz = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    ltnol__qkhc = context.nrt.meminfo_data(builder, kvr__jrmiz.meminfo)
    vhqw__ctbqb = builder.bitcast(ltnol__qkhc, context.get_value_type(
        payload_type).as_pointer())
    aptx__zjg = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(vhqw__ctbqb))
    return aptx__zjg


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    aptx__zjg = _get_struct_arr_payload(c.context, c.builder, typ, val)
    lhcr__tijl, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), aptx__zjg.null_bitmap).data
    zzytg__igprq = all(isinstance(spkml__mdh, types.Array) and spkml__mdh.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for spkml__mdh in typ.data)
    if zzytg__igprq:
        ulc__nhwr, xny__urwrs, wougb__vgkp = _get_C_API_ptrs(c, aptx__zjg.
            data, typ.data, typ.names)
        ugga__tft = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        gpqoo__olec = cgutils.get_or_insert_function(c.builder.module,
            ugga__tft, name='np_array_from_struct_array')
        arr = c.builder.call(gpqoo__olec, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(ulc__nhwr, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            xny__urwrs, lir.IntType(8).as_pointer()), c.builder.bitcast(
            wougb__vgkp, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, aptx__zjg.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    qzl__wazon = context.insert_const_string(builder.module, 'numpy')
    xxezd__nub = c.pyapi.import_module_noblock(qzl__wazon)
    ezx__euxz = c.pyapi.object_getattr_string(xxezd__nub, 'object_')
    xko__mmwd = c.pyapi.long_from_longlong(length)
    blpoo__kdj = c.pyapi.call_method(xxezd__nub, 'ndarray', (xko__mmwd,
        ezx__euxz))
    egojb__flef = c.pyapi.object_getattr_string(xxezd__nub, 'nan')
    with cgutils.for_range(builder, length) as lbsti__ggd:
        unf__iwp = lbsti__ggd.index
        pyarray_setitem(builder, context, blpoo__kdj, unf__iwp, egojb__flef)
        ehe__korlg = get_bitmap_bit(builder, null_bitmap_ptr, unf__iwp)
        xbw__fzdql = builder.icmp_unsigned('!=', ehe__korlg, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(xbw__fzdql):
            if is_tuple_array:
                uait__hxavg = c.pyapi.tuple_new(len(typ.data))
            else:
                uait__hxavg = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(egojb__flef)
                    c.pyapi.tuple_setitem(uait__hxavg, i, egojb__flef)
                else:
                    c.pyapi.dict_setitem_string(uait__hxavg, typ.names[i],
                        egojb__flef)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                lhcr__tijl, zbyaa__pjhg = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, unf__iwp])
                with builder.if_then(zbyaa__pjhg):
                    lhcr__tijl, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, unf__iwp])
                    lbqpj__sls = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(uait__hxavg, i, lbqpj__sls)
                    else:
                        c.pyapi.dict_setitem_string(uait__hxavg, typ.names[
                            i], lbqpj__sls)
                        c.pyapi.decref(lbqpj__sls)
            pyarray_setitem(builder, context, blpoo__kdj, unf__iwp, uait__hxavg
                )
            c.pyapi.decref(uait__hxavg)
    c.pyapi.decref(xxezd__nub)
    c.pyapi.decref(ezx__euxz)
    c.pyapi.decref(xko__mmwd)
    c.pyapi.decref(egojb__flef)
    return blpoo__kdj


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    hgo__qqvdg = bodo.utils.transform.get_type_alloc_counts(struct_arr_type
        ) - 1
    if hgo__qqvdg == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for vim__uky in range(hgo__qqvdg)])
    elif nested_counts_type.count < hgo__qqvdg:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for vim__uky in range(
            hgo__qqvdg - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(spkml__mdh) for spkml__mdh in
            names_typ.types)
    kywdw__lnn = tuple(spkml__mdh.instance_type for spkml__mdh in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(kywdw__lnn, names)

    def codegen(context, builder, sig, args):
        bdd__gee, nested_counts, vim__uky, vim__uky = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        tdzx__bwb, vim__uky, vim__uky = construct_struct_array(context,
            builder, struct_arr_type, bdd__gee, nested_counts)
        kvr__jrmiz = context.make_helper(builder, struct_arr_type)
        kvr__jrmiz.meminfo = tdzx__bwb
        return kvr__jrmiz._getvalue()
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
        assert isinstance(names, tuple) and all(isinstance(iujr__iqwtf, str
            ) for iujr__iqwtf in names) and len(names) == len(data)
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
        qvdk__qlojx = [('data', types.BaseTuple.from_types(fe_type.data)),
            ('null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, qvdk__qlojx)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        qvdk__qlojx = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, qvdk__qlojx)


def define_struct_dtor(context, builder, struct_type, payload_type):
    pth__znnhi = builder.module
    ugga__tft = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    diyr__mefx = cgutils.get_or_insert_function(pth__znnhi, ugga__tft, name
        ='.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not diyr__mefx.is_declaration:
        return diyr__mefx
    diyr__mefx.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(diyr__mefx.append_basic_block())
    jibz__kht = diyr__mefx.args[0]
    nfgck__cwka = context.get_value_type(payload_type).as_pointer()
    iva__tiggw = builder.bitcast(jibz__kht, nfgck__cwka)
    aptx__zjg = context.make_helper(builder, payload_type, ref=iva__tiggw)
    for i in range(len(struct_type.data)):
        nol__rmsnr = builder.extract_value(aptx__zjg.null_bitmap, i)
        xbw__fzdql = builder.icmp_unsigned('==', nol__rmsnr, lir.Constant(
            nol__rmsnr.type, 1))
        with builder.if_then(xbw__fzdql):
            val = builder.extract_value(aptx__zjg.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return diyr__mefx


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    ltnol__qkhc = context.nrt.meminfo_data(builder, struct.meminfo)
    vhqw__ctbqb = builder.bitcast(ltnol__qkhc, context.get_value_type(
        payload_type).as_pointer())
    aptx__zjg = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(vhqw__ctbqb))
    return aptx__zjg, vhqw__ctbqb


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    qzl__wazon = context.insert_const_string(builder.module, 'pandas')
    ojjor__buibm = c.pyapi.import_module_noblock(qzl__wazon)
    kdwb__msi = c.pyapi.object_getattr_string(ojjor__buibm, 'NA')
    xqqca__jgel = []
    nulls = []
    for i, spkml__mdh in enumerate(typ.data):
        lbqpj__sls = c.pyapi.dict_getitem_string(val, typ.names[i])
        gfl__ewhsq = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        vufdi__ejvem = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(spkml__mdh)))
        fwml__xbloj = is_na_value(builder, context, lbqpj__sls, kdwb__msi)
        xbw__fzdql = builder.icmp_unsigned('!=', fwml__xbloj, lir.Constant(
            fwml__xbloj.type, 1))
        with builder.if_then(xbw__fzdql):
            builder.store(context.get_constant(types.uint8, 1), gfl__ewhsq)
            field_val = c.pyapi.to_native_value(spkml__mdh, lbqpj__sls).value
            builder.store(field_val, vufdi__ejvem)
        xqqca__jgel.append(builder.load(vufdi__ejvem))
        nulls.append(builder.load(gfl__ewhsq))
    c.pyapi.decref(ojjor__buibm)
    c.pyapi.decref(kdwb__msi)
    tdzx__bwb = construct_struct(context, builder, typ, xqqca__jgel, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = tdzx__bwb
    qtfxr__ioro = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=qtfxr__ioro)


@box(StructType)
def box_struct(typ, val, c):
    iobfo__tqoqn = c.pyapi.dict_new(len(typ.data))
    aptx__zjg, vim__uky = _get_struct_payload(c.context, c.builder, typ, val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(iobfo__tqoqn, typ.names[i], c.pyapi.
            borrow_none())
        nol__rmsnr = c.builder.extract_value(aptx__zjg.null_bitmap, i)
        xbw__fzdql = c.builder.icmp_unsigned('==', nol__rmsnr, lir.Constant
            (nol__rmsnr.type, 1))
        with c.builder.if_then(xbw__fzdql):
            bym__mojqv = c.builder.extract_value(aptx__zjg.data, i)
            c.context.nrt.incref(c.builder, val_typ, bym__mojqv)
            jbrsh__apz = c.pyapi.from_native_value(val_typ, bym__mojqv, c.
                env_manager)
            c.pyapi.dict_setitem_string(iobfo__tqoqn, typ.names[i], jbrsh__apz)
            c.pyapi.decref(jbrsh__apz)
    c.context.nrt.decref(c.builder, typ, val)
    return iobfo__tqoqn


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(spkml__mdh) for spkml__mdh in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, emb__xnqf = args
        payload_type = StructPayloadType(struct_type.data)
        dqpqa__vfqb = context.get_value_type(payload_type)
        rjeb__kslg = context.get_abi_sizeof(dqpqa__vfqb)
        ifyq__cgltt = define_struct_dtor(context, builder, struct_type,
            payload_type)
        tdzx__bwb = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, rjeb__kslg), ifyq__cgltt)
        ltnol__qkhc = context.nrt.meminfo_data(builder, tdzx__bwb)
        vhqw__ctbqb = builder.bitcast(ltnol__qkhc, dqpqa__vfqb.as_pointer())
        aptx__zjg = cgutils.create_struct_proxy(payload_type)(context, builder)
        aptx__zjg.data = data
        aptx__zjg.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for vim__uky in range(len(data_typ
            .types))])
        builder.store(aptx__zjg._getvalue(), vhqw__ctbqb)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = tdzx__bwb
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        aptx__zjg, vim__uky = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            aptx__zjg.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        aptx__zjg, vim__uky = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            aptx__zjg.null_bitmap)
    nfb__gtg = types.UniTuple(types.int8, len(struct_typ.data))
    return nfb__gtg(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, vim__uky, val = args
        aptx__zjg, vhqw__ctbqb = _get_struct_payload(context, builder,
            struct_typ, struct)
        adhmi__uya = aptx__zjg.data
        ppdx__spx = builder.insert_value(adhmi__uya, val, field_ind)
        mnwnv__zlhih = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, mnwnv__zlhih, adhmi__uya)
        context.nrt.incref(builder, mnwnv__zlhih, ppdx__spx)
        aptx__zjg.data = ppdx__spx
        builder.store(aptx__zjg._getvalue(), vhqw__ctbqb)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    utc__wyo = get_overload_const_str(ind)
    if utc__wyo not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            utc__wyo, struct))
    return struct.names.index(utc__wyo)


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
    dqpqa__vfqb = context.get_value_type(payload_type)
    rjeb__kslg = context.get_abi_sizeof(dqpqa__vfqb)
    ifyq__cgltt = define_struct_dtor(context, builder, struct_type,
        payload_type)
    tdzx__bwb = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, rjeb__kslg), ifyq__cgltt)
    ltnol__qkhc = context.nrt.meminfo_data(builder, tdzx__bwb)
    vhqw__ctbqb = builder.bitcast(ltnol__qkhc, dqpqa__vfqb.as_pointer())
    aptx__zjg = cgutils.create_struct_proxy(payload_type)(context, builder)
    aptx__zjg.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    aptx__zjg.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(aptx__zjg._getvalue(), vhqw__ctbqb)
    return tdzx__bwb


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    ekmj__fygsm = tuple(d.dtype for d in struct_arr_typ.data)
    vocz__yaopt = StructType(ekmj__fygsm, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        rjvb__nyn, ind = args
        aptx__zjg = _get_struct_arr_payload(context, builder,
            struct_arr_typ, rjvb__nyn)
        xqqca__jgel = []
        qhpx__kdww = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            qnugk__ksya = builder.extract_value(aptx__zjg.data, i)
            kfosa__het = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [
                qnugk__ksya, ind])
            qhpx__kdww.append(kfosa__het)
            vlsi__zghc = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            xbw__fzdql = builder.icmp_unsigned('==', kfosa__het, lir.
                Constant(kfosa__het.type, 1))
            with builder.if_then(xbw__fzdql):
                itx__fazgd = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    qnugk__ksya, ind])
                builder.store(itx__fazgd, vlsi__zghc)
            xqqca__jgel.append(builder.load(vlsi__zghc))
        if isinstance(vocz__yaopt, types.DictType):
            heo__fffnv = [context.insert_const_string(builder.module,
                kmsqi__drdcj) for kmsqi__drdcj in struct_arr_typ.names]
            wms__pof = cgutils.pack_array(builder, xqqca__jgel)
            gnpw__jsnhw = cgutils.pack_array(builder, heo__fffnv)

            def impl(names, vals):
                d = {}
                for i, kmsqi__drdcj in enumerate(names):
                    d[kmsqi__drdcj] = vals[i]
                return d
            cqzls__xlau = context.compile_internal(builder, impl,
                vocz__yaopt(types.Tuple(tuple(types.StringLiteral(
                kmsqi__drdcj) for kmsqi__drdcj in struct_arr_typ.names)),
                types.Tuple(ekmj__fygsm)), [gnpw__jsnhw, wms__pof])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                ekmj__fygsm), wms__pof)
            return cqzls__xlau
        tdzx__bwb = construct_struct(context, builder, vocz__yaopt,
            xqqca__jgel, qhpx__kdww)
        struct = context.make_helper(builder, vocz__yaopt)
        struct.meminfo = tdzx__bwb
        return struct._getvalue()
    return vocz__yaopt(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        aptx__zjg = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            aptx__zjg.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        aptx__zjg = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            aptx__zjg.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(spkml__mdh) for spkml__mdh in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, lnfea__ksk, emb__xnqf = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        dqpqa__vfqb = context.get_value_type(payload_type)
        rjeb__kslg = context.get_abi_sizeof(dqpqa__vfqb)
        ifyq__cgltt = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        tdzx__bwb = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, rjeb__kslg), ifyq__cgltt)
        ltnol__qkhc = context.nrt.meminfo_data(builder, tdzx__bwb)
        vhqw__ctbqb = builder.bitcast(ltnol__qkhc, dqpqa__vfqb.as_pointer())
        aptx__zjg = cgutils.create_struct_proxy(payload_type)(context, builder)
        aptx__zjg.data = data
        aptx__zjg.null_bitmap = lnfea__ksk
        builder.store(aptx__zjg._getvalue(), vhqw__ctbqb)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, lnfea__ksk)
        kvr__jrmiz = context.make_helper(builder, struct_arr_type)
        kvr__jrmiz.meminfo = tdzx__bwb
        return kvr__jrmiz._getvalue()
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
    enw__rtfaz = len(arr.data)
    cdrt__rvl = 'def impl(arr, ind):\n'
    cdrt__rvl += '  data = get_data(arr)\n'
    cdrt__rvl += '  null_bitmap = get_null_bitmap(arr)\n'
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        cdrt__rvl += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
    elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        cdrt__rvl += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
    elif isinstance(ind, types.SliceType):
        cdrt__rvl += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
    else:
        raise BodoError('invalid index {} in struct array indexing'.format(ind)
            )
    cdrt__rvl += ('  return init_struct_arr(({},), out_null_bitmap, ({},))\n'
        .format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
        i in range(enw__rtfaz)), ', '.join("'{}'".format(kmsqi__drdcj) for
        kmsqi__drdcj in arr.names)))
    erbe__aqlxk = {}
    exec(cdrt__rvl, {'init_struct_arr': init_struct_arr, 'get_data':
        get_data, 'get_null_bitmap': get_null_bitmap, 'ensure_contig_if_np':
        bodo.utils.conversion.ensure_contig_if_np,
        'get_new_null_mask_bool_index': bodo.utils.indexing.
        get_new_null_mask_bool_index, 'get_new_null_mask_int_index': bodo.
        utils.indexing.get_new_null_mask_int_index,
        'get_new_null_mask_slice_index': bodo.utils.indexing.
        get_new_null_mask_slice_index}, erbe__aqlxk)
    impl = erbe__aqlxk['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        enw__rtfaz = len(arr.data)
        cdrt__rvl = 'def impl(arr, ind, val):\n'
        cdrt__rvl += '  data = get_data(arr)\n'
        cdrt__rvl += '  null_bitmap = get_null_bitmap(arr)\n'
        cdrt__rvl += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(enw__rtfaz):
            if isinstance(val, StructType):
                cdrt__rvl += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                cdrt__rvl += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                cdrt__rvl += '  else:\n'
                cdrt__rvl += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                cdrt__rvl += "  data[{}][ind] = val['{}']\n".format(i, arr.
                    names[i])
        erbe__aqlxk = {}
        exec(cdrt__rvl, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, erbe__aqlxk)
        impl = erbe__aqlxk['impl']
        return impl
    if isinstance(ind, types.SliceType):
        enw__rtfaz = len(arr.data)
        cdrt__rvl = 'def impl(arr, ind, val):\n'
        cdrt__rvl += '  data = get_data(arr)\n'
        cdrt__rvl += '  null_bitmap = get_null_bitmap(arr)\n'
        cdrt__rvl += '  val_data = get_data(val)\n'
        cdrt__rvl += '  val_null_bitmap = get_null_bitmap(val)\n'
        cdrt__rvl += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(enw__rtfaz):
            cdrt__rvl += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        erbe__aqlxk = {}
        exec(cdrt__rvl, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, erbe__aqlxk)
        impl = erbe__aqlxk['impl']
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
    cdrt__rvl = 'def impl(A):\n'
    cdrt__rvl += '  total_nbytes = 0\n'
    cdrt__rvl += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        cdrt__rvl += f'  total_nbytes += data[{i}].nbytes\n'
    cdrt__rvl += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    cdrt__rvl += '  return total_nbytes\n'
    erbe__aqlxk = {}
    exec(cdrt__rvl, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, erbe__aqlxk)
    impl = erbe__aqlxk['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        lnfea__ksk = get_null_bitmap(A)
        ahde__ndj = bodo.ir.join.copy_arr_tup(data)
        ghu__yaep = lnfea__ksk.copy()
        return init_struct_arr(ahde__ndj, ghu__yaep, names)
    return copy_impl
