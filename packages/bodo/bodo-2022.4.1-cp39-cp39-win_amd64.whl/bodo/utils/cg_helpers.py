"""helper functions for code generation with llvmlite
"""
import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
import bodo
from bodo.libs import array_ext, hdist
ll.add_symbol('array_getitem', array_ext.array_getitem)
ll.add_symbol('seq_getitem', array_ext.seq_getitem)
ll.add_symbol('list_check', array_ext.list_check)
ll.add_symbol('dict_keys', array_ext.dict_keys)
ll.add_symbol('dict_values', array_ext.dict_values)
ll.add_symbol('dict_merge_from_seq2', array_ext.dict_merge_from_seq2)
ll.add_symbol('is_na_value', array_ext.is_na_value)


def set_bitmap_bit(builder, null_bitmap_ptr, ind, val):
    tkkly__vtq = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    vfz__btdrs = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    haq__hbbxs = builder.gep(null_bitmap_ptr, [tkkly__vtq], inbounds=True)
    gbw__guw = builder.load(haq__hbbxs)
    cdlo__ebjq = lir.ArrayType(lir.IntType(8), 8)
    qvc__dazrh = cgutils.alloca_once_value(builder, lir.Constant(cdlo__ebjq,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    qrtbd__lzw = builder.load(builder.gep(qvc__dazrh, [lir.Constant(lir.
        IntType(64), 0), vfz__btdrs], inbounds=True))
    if val:
        builder.store(builder.or_(gbw__guw, qrtbd__lzw), haq__hbbxs)
    else:
        qrtbd__lzw = builder.xor(qrtbd__lzw, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(gbw__guw, qrtbd__lzw), haq__hbbxs)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    tkkly__vtq = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    vfz__btdrs = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    gbw__guw = builder.load(builder.gep(null_bitmap_ptr, [tkkly__vtq],
        inbounds=True))
    cdlo__ebjq = lir.ArrayType(lir.IntType(8), 8)
    qvc__dazrh = cgutils.alloca_once_value(builder, lir.Constant(cdlo__ebjq,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    qrtbd__lzw = builder.load(builder.gep(qvc__dazrh, [lir.Constant(lir.
        IntType(64), 0), vfz__btdrs], inbounds=True))
    return builder.and_(gbw__guw, qrtbd__lzw)


def pyarray_check(builder, context, obj):
    siwqs__fmwe = context.get_argument_type(types.pyobject)
    uojq__tzysb = lir.FunctionType(lir.IntType(32), [siwqs__fmwe])
    jih__zno = cgutils.get_or_insert_function(builder.module, uojq__tzysb,
        name='is_np_array')
    return builder.call(jih__zno, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    siwqs__fmwe = context.get_argument_type(types.pyobject)
    wqy__sbew = context.get_value_type(types.intp)
    ehks__hkei = lir.FunctionType(lir.IntType(8).as_pointer(), [siwqs__fmwe,
        wqy__sbew])
    gdkgi__gjmyl = cgutils.get_or_insert_function(builder.module,
        ehks__hkei, name='array_getptr1')
    ivgbp__mjlw = lir.FunctionType(siwqs__fmwe, [siwqs__fmwe, lir.IntType(8
        ).as_pointer()])
    oll__mlbd = cgutils.get_or_insert_function(builder.module, ivgbp__mjlw,
        name='array_getitem')
    fsffg__ugxrv = builder.call(gdkgi__gjmyl, [arr_obj, ind])
    return builder.call(oll__mlbd, [arr_obj, fsffg__ugxrv])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    siwqs__fmwe = context.get_argument_type(types.pyobject)
    wqy__sbew = context.get_value_type(types.intp)
    ehks__hkei = lir.FunctionType(lir.IntType(8).as_pointer(), [siwqs__fmwe,
        wqy__sbew])
    gdkgi__gjmyl = cgutils.get_or_insert_function(builder.module,
        ehks__hkei, name='array_getptr1')
    uswd__ajgv = lir.FunctionType(lir.VoidType(), [siwqs__fmwe, lir.IntType
        (8).as_pointer(), siwqs__fmwe])
    qzotx__owx = cgutils.get_or_insert_function(builder.module, uswd__ajgv,
        name='array_setitem')
    fsffg__ugxrv = builder.call(gdkgi__gjmyl, [arr_obj, ind])
    builder.call(qzotx__owx, [arr_obj, fsffg__ugxrv, val_obj])


def seq_getitem(builder, context, obj, ind):
    siwqs__fmwe = context.get_argument_type(types.pyobject)
    wqy__sbew = context.get_value_type(types.intp)
    jqbcm__ebrb = lir.FunctionType(siwqs__fmwe, [siwqs__fmwe, wqy__sbew])
    dzlg__wcox = cgutils.get_or_insert_function(builder.module, jqbcm__ebrb,
        name='seq_getitem')
    return builder.call(dzlg__wcox, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    siwqs__fmwe = context.get_argument_type(types.pyobject)
    xkd__rbqe = lir.FunctionType(lir.IntType(32), [siwqs__fmwe, siwqs__fmwe])
    ewhr__veyoe = cgutils.get_or_insert_function(builder.module, xkd__rbqe,
        name='is_na_value')
    return builder.call(ewhr__veyoe, [val, C_NA])


def list_check(builder, context, obj):
    siwqs__fmwe = context.get_argument_type(types.pyobject)
    mjjg__hmzwe = context.get_value_type(types.int32)
    mjah__vjii = lir.FunctionType(mjjg__hmzwe, [siwqs__fmwe])
    qaqd__iosi = cgutils.get_or_insert_function(builder.module, mjah__vjii,
        name='list_check')
    return builder.call(qaqd__iosi, [obj])


def dict_keys(builder, context, obj):
    siwqs__fmwe = context.get_argument_type(types.pyobject)
    mjah__vjii = lir.FunctionType(siwqs__fmwe, [siwqs__fmwe])
    qaqd__iosi = cgutils.get_or_insert_function(builder.module, mjah__vjii,
        name='dict_keys')
    return builder.call(qaqd__iosi, [obj])


def dict_values(builder, context, obj):
    siwqs__fmwe = context.get_argument_type(types.pyobject)
    mjah__vjii = lir.FunctionType(siwqs__fmwe, [siwqs__fmwe])
    qaqd__iosi = cgutils.get_or_insert_function(builder.module, mjah__vjii,
        name='dict_values')
    return builder.call(qaqd__iosi, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    siwqs__fmwe = context.get_argument_type(types.pyobject)
    mjah__vjii = lir.FunctionType(lir.VoidType(), [siwqs__fmwe, siwqs__fmwe])
    qaqd__iosi = cgutils.get_or_insert_function(builder.module, mjah__vjii,
        name='dict_merge_from_seq2')
    builder.call(qaqd__iosi, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    ooos__wus = cgutils.alloca_once_value(builder, val)
    lcj__bgl = list_check(builder, context, val)
    cae__smfzx = builder.icmp_unsigned('!=', lcj__bgl, lir.Constant(
        lcj__bgl.type, 0))
    with builder.if_then(cae__smfzx):
        olh__ojs = context.insert_const_string(builder.module, 'numpy')
        vai__cpzr = c.pyapi.import_module_noblock(olh__ojs)
        bhwx__wyuyx = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            bhwx__wyuyx = str(typ.dtype)
        ofj__zhnq = c.pyapi.object_getattr_string(vai__cpzr, bhwx__wyuyx)
        jyta__rgem = builder.load(ooos__wus)
        iirwv__nofft = c.pyapi.call_method(vai__cpzr, 'asarray', (
            jyta__rgem, ofj__zhnq))
        builder.store(iirwv__nofft, ooos__wus)
        c.pyapi.decref(vai__cpzr)
        c.pyapi.decref(ofj__zhnq)
    val = builder.load(ooos__wus)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        jbuuv__hlug = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        mwm__vamdr, pznx__ppl = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [jbuuv__hlug])
        context.nrt.decref(builder, typ, jbuuv__hlug)
        return cgutils.pack_array(builder, [pznx__ppl])
    if isinstance(typ, (StructType, types.BaseTuple)):
        olh__ojs = context.insert_const_string(builder.module, 'pandas')
        khkx__khgek = c.pyapi.import_module_noblock(olh__ojs)
        C_NA = c.pyapi.object_getattr_string(khkx__khgek, 'NA')
        ixr__nzi = bodo.utils.transform.get_type_alloc_counts(typ)
        gepwd__cegtp = context.make_tuple(builder, types.Tuple(ixr__nzi * [
            types.int64]), ixr__nzi * [context.get_constant(types.int64, 0)])
        njga__hphx = cgutils.alloca_once_value(builder, gepwd__cegtp)
        vosz__rdnso = 0
        hks__adfd = typ.data if isinstance(typ, StructType) else typ.types
        for cqas__kig, t in enumerate(hks__adfd):
            fobue__hzxo = bodo.utils.transform.get_type_alloc_counts(t)
            if fobue__hzxo == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    cqas__kig])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, cqas__kig)
            vwfjk__yku = is_na_value(builder, context, val_obj, C_NA)
            vafvo__gght = builder.icmp_unsigned('!=', vwfjk__yku, lir.
                Constant(vwfjk__yku.type, 1))
            with builder.if_then(vafvo__gght):
                gepwd__cegtp = builder.load(njga__hphx)
                ehnf__muxf = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for cqas__kig in range(fobue__hzxo):
                    gmbj__ebboa = builder.extract_value(gepwd__cegtp, 
                        vosz__rdnso + cqas__kig)
                    fskpu__aqmju = builder.extract_value(ehnf__muxf, cqas__kig)
                    gepwd__cegtp = builder.insert_value(gepwd__cegtp,
                        builder.add(gmbj__ebboa, fskpu__aqmju), vosz__rdnso +
                        cqas__kig)
                builder.store(gepwd__cegtp, njga__hphx)
            vosz__rdnso += fobue__hzxo
        c.pyapi.decref(khkx__khgek)
        c.pyapi.decref(C_NA)
        return builder.load(njga__hphx)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    olh__ojs = context.insert_const_string(builder.module, 'pandas')
    khkx__khgek = c.pyapi.import_module_noblock(olh__ojs)
    C_NA = c.pyapi.object_getattr_string(khkx__khgek, 'NA')
    ixr__nzi = bodo.utils.transform.get_type_alloc_counts(typ)
    gepwd__cegtp = context.make_tuple(builder, types.Tuple(ixr__nzi * [
        types.int64]), [n] + (ixr__nzi - 1) * [context.get_constant(types.
        int64, 0)])
    njga__hphx = cgutils.alloca_once_value(builder, gepwd__cegtp)
    with cgutils.for_range(builder, n) as wicqx__nus:
        idrv__wttv = wicqx__nus.index
        jdy__qmeyw = seq_getitem(builder, context, arr_obj, idrv__wttv)
        vwfjk__yku = is_na_value(builder, context, jdy__qmeyw, C_NA)
        vafvo__gght = builder.icmp_unsigned('!=', vwfjk__yku, lir.Constant(
            vwfjk__yku.type, 1))
        with builder.if_then(vafvo__gght):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                gepwd__cegtp = builder.load(njga__hphx)
                ehnf__muxf = get_array_elem_counts(c, builder, context,
                    jdy__qmeyw, typ.dtype)
                for cqas__kig in range(ixr__nzi - 1):
                    gmbj__ebboa = builder.extract_value(gepwd__cegtp, 
                        cqas__kig + 1)
                    fskpu__aqmju = builder.extract_value(ehnf__muxf, cqas__kig)
                    gepwd__cegtp = builder.insert_value(gepwd__cegtp,
                        builder.add(gmbj__ebboa, fskpu__aqmju), cqas__kig + 1)
                builder.store(gepwd__cegtp, njga__hphx)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                vosz__rdnso = 1
                for cqas__kig, t in enumerate(typ.data):
                    fobue__hzxo = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if fobue__hzxo == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(jdy__qmeyw, cqas__kig)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(jdy__qmeyw,
                            typ.names[cqas__kig])
                    vwfjk__yku = is_na_value(builder, context, val_obj, C_NA)
                    vafvo__gght = builder.icmp_unsigned('!=', vwfjk__yku,
                        lir.Constant(vwfjk__yku.type, 1))
                    with builder.if_then(vafvo__gght):
                        gepwd__cegtp = builder.load(njga__hphx)
                        ehnf__muxf = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for cqas__kig in range(fobue__hzxo):
                            gmbj__ebboa = builder.extract_value(gepwd__cegtp,
                                vosz__rdnso + cqas__kig)
                            fskpu__aqmju = builder.extract_value(ehnf__muxf,
                                cqas__kig)
                            gepwd__cegtp = builder.insert_value(gepwd__cegtp,
                                builder.add(gmbj__ebboa, fskpu__aqmju), 
                                vosz__rdnso + cqas__kig)
                        builder.store(gepwd__cegtp, njga__hphx)
                    vosz__rdnso += fobue__hzxo
            else:
                assert isinstance(typ, MapArrayType), typ
                gepwd__cegtp = builder.load(njga__hphx)
                tju__zwwqr = dict_keys(builder, context, jdy__qmeyw)
                tibw__rdh = dict_values(builder, context, jdy__qmeyw)
                zsaf__aqr = get_array_elem_counts(c, builder, context,
                    tju__zwwqr, typ.key_arr_type)
                kegw__bab = bodo.utils.transform.get_type_alloc_counts(typ.
                    key_arr_type)
                for cqas__kig in range(1, kegw__bab + 1):
                    gmbj__ebboa = builder.extract_value(gepwd__cegtp, cqas__kig
                        )
                    fskpu__aqmju = builder.extract_value(zsaf__aqr, 
                        cqas__kig - 1)
                    gepwd__cegtp = builder.insert_value(gepwd__cegtp,
                        builder.add(gmbj__ebboa, fskpu__aqmju), cqas__kig)
                tmt__kbnv = get_array_elem_counts(c, builder, context,
                    tibw__rdh, typ.value_arr_type)
                for cqas__kig in range(kegw__bab + 1, ixr__nzi):
                    gmbj__ebboa = builder.extract_value(gepwd__cegtp, cqas__kig
                        )
                    fskpu__aqmju = builder.extract_value(tmt__kbnv, 
                        cqas__kig - kegw__bab)
                    gepwd__cegtp = builder.insert_value(gepwd__cegtp,
                        builder.add(gmbj__ebboa, fskpu__aqmju), cqas__kig)
                builder.store(gepwd__cegtp, njga__hphx)
                c.pyapi.decref(tju__zwwqr)
                c.pyapi.decref(tibw__rdh)
        c.pyapi.decref(jdy__qmeyw)
    c.pyapi.decref(khkx__khgek)
    c.pyapi.decref(C_NA)
    return builder.load(njga__hphx)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    hbvh__dhrje = n_elems.type.count
    assert hbvh__dhrje >= 1
    uyja__lii = builder.extract_value(n_elems, 0)
    if hbvh__dhrje != 1:
        tiy__kbe = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, cqas__kig) for cqas__kig in range(1, hbvh__dhrje)])
        fsr__qeo = types.Tuple([types.int64] * (hbvh__dhrje - 1))
    else:
        tiy__kbe = context.get_dummy_value()
        fsr__qeo = types.none
    udsr__joos = types.TypeRef(arr_type)
    zobb__zps = arr_type(types.int64, udsr__joos, fsr__qeo)
    args = [uyja__lii, context.get_dummy_value(), tiy__kbe]
    pxeke__ymlm = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        mwm__vamdr, ztmiw__hlgak = c.pyapi.call_jit_code(pxeke__ymlm,
            zobb__zps, args)
    else:
        ztmiw__hlgak = context.compile_internal(builder, pxeke__ymlm,
            zobb__zps, args)
    return ztmiw__hlgak


def is_ll_eq(builder, val1, val2):
    lhn__ptq = val1.type.pointee
    bqv__mfx = val2.type.pointee
    assert lhn__ptq == bqv__mfx, 'invalid llvm value comparison'
    if isinstance(lhn__ptq, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(lhn__ptq.elements) if isinstance(lhn__ptq, lir.
            BaseStructType) else lhn__ptq.count
        jcu__omfao = lir.Constant(lir.IntType(1), 1)
        for cqas__kig in range(n_elems):
            pkp__begc = lir.IntType(32)(0)
            pzeq__gjnaj = lir.IntType(32)(cqas__kig)
            cbbq__ybj = builder.gep(val1, [pkp__begc, pzeq__gjnaj],
                inbounds=True)
            aya__iqawc = builder.gep(val2, [pkp__begc, pzeq__gjnaj],
                inbounds=True)
            jcu__omfao = builder.and_(jcu__omfao, is_ll_eq(builder,
                cbbq__ybj, aya__iqawc))
        return jcu__omfao
    yptpf__ilkvm = builder.load(val1)
    wrj__uot = builder.load(val2)
    if yptpf__ilkvm.type in (lir.FloatType(), lir.DoubleType()):
        ecfsh__bpbch = 32 if yptpf__ilkvm.type == lir.FloatType() else 64
        yptpf__ilkvm = builder.bitcast(yptpf__ilkvm, lir.IntType(ecfsh__bpbch))
        wrj__uot = builder.bitcast(wrj__uot, lir.IntType(ecfsh__bpbch))
    return builder.icmp_unsigned('==', yptpf__ilkvm, wrj__uot)
