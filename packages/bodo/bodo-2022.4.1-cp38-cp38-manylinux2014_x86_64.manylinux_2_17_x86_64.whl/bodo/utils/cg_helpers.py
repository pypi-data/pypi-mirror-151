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
    uvju__fcv = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    jqnn__hugo = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    lwqe__galxk = builder.gep(null_bitmap_ptr, [uvju__fcv], inbounds=True)
    eidrx__wloxv = builder.load(lwqe__galxk)
    plk__bvc = lir.ArrayType(lir.IntType(8), 8)
    wpcle__viha = cgutils.alloca_once_value(builder, lir.Constant(plk__bvc,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    her__dshp = builder.load(builder.gep(wpcle__viha, [lir.Constant(lir.
        IntType(64), 0), jqnn__hugo], inbounds=True))
    if val:
        builder.store(builder.or_(eidrx__wloxv, her__dshp), lwqe__galxk)
    else:
        her__dshp = builder.xor(her__dshp, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(eidrx__wloxv, her__dshp), lwqe__galxk)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    uvju__fcv = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    jqnn__hugo = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    eidrx__wloxv = builder.load(builder.gep(null_bitmap_ptr, [uvju__fcv],
        inbounds=True))
    plk__bvc = lir.ArrayType(lir.IntType(8), 8)
    wpcle__viha = cgutils.alloca_once_value(builder, lir.Constant(plk__bvc,
        (1, 2, 4, 8, 16, 32, 64, 128)))
    her__dshp = builder.load(builder.gep(wpcle__viha, [lir.Constant(lir.
        IntType(64), 0), jqnn__hugo], inbounds=True))
    return builder.and_(eidrx__wloxv, her__dshp)


def pyarray_check(builder, context, obj):
    qpes__equjl = context.get_argument_type(types.pyobject)
    mpr__cfuiq = lir.FunctionType(lir.IntType(32), [qpes__equjl])
    coz__dxbj = cgutils.get_or_insert_function(builder.module, mpr__cfuiq,
        name='is_np_array')
    return builder.call(coz__dxbj, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    qpes__equjl = context.get_argument_type(types.pyobject)
    rdxws__wkaf = context.get_value_type(types.intp)
    pexpv__ohk = lir.FunctionType(lir.IntType(8).as_pointer(), [qpes__equjl,
        rdxws__wkaf])
    fcodv__uuc = cgutils.get_or_insert_function(builder.module, pexpv__ohk,
        name='array_getptr1')
    wzozt__iwes = lir.FunctionType(qpes__equjl, [qpes__equjl, lir.IntType(8
        ).as_pointer()])
    hkj__osteu = cgutils.get_or_insert_function(builder.module, wzozt__iwes,
        name='array_getitem')
    dvh__bae = builder.call(fcodv__uuc, [arr_obj, ind])
    return builder.call(hkj__osteu, [arr_obj, dvh__bae])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    qpes__equjl = context.get_argument_type(types.pyobject)
    rdxws__wkaf = context.get_value_type(types.intp)
    pexpv__ohk = lir.FunctionType(lir.IntType(8).as_pointer(), [qpes__equjl,
        rdxws__wkaf])
    fcodv__uuc = cgutils.get_or_insert_function(builder.module, pexpv__ohk,
        name='array_getptr1')
    bgqfh__lgag = lir.FunctionType(lir.VoidType(), [qpes__equjl, lir.
        IntType(8).as_pointer(), qpes__equjl])
    ghd__gkr = cgutils.get_or_insert_function(builder.module, bgqfh__lgag,
        name='array_setitem')
    dvh__bae = builder.call(fcodv__uuc, [arr_obj, ind])
    builder.call(ghd__gkr, [arr_obj, dvh__bae, val_obj])


def seq_getitem(builder, context, obj, ind):
    qpes__equjl = context.get_argument_type(types.pyobject)
    rdxws__wkaf = context.get_value_type(types.intp)
    evx__thulc = lir.FunctionType(qpes__equjl, [qpes__equjl, rdxws__wkaf])
    tgt__jpu = cgutils.get_or_insert_function(builder.module, evx__thulc,
        name='seq_getitem')
    return builder.call(tgt__jpu, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    qpes__equjl = context.get_argument_type(types.pyobject)
    mrmmm__nyp = lir.FunctionType(lir.IntType(32), [qpes__equjl, qpes__equjl])
    apq__qmrmp = cgutils.get_or_insert_function(builder.module, mrmmm__nyp,
        name='is_na_value')
    return builder.call(apq__qmrmp, [val, C_NA])


def list_check(builder, context, obj):
    qpes__equjl = context.get_argument_type(types.pyobject)
    lqpzo__pkszn = context.get_value_type(types.int32)
    xjrm__emr = lir.FunctionType(lqpzo__pkszn, [qpes__equjl])
    wixvw__wlqw = cgutils.get_or_insert_function(builder.module, xjrm__emr,
        name='list_check')
    return builder.call(wixvw__wlqw, [obj])


def dict_keys(builder, context, obj):
    qpes__equjl = context.get_argument_type(types.pyobject)
    xjrm__emr = lir.FunctionType(qpes__equjl, [qpes__equjl])
    wixvw__wlqw = cgutils.get_or_insert_function(builder.module, xjrm__emr,
        name='dict_keys')
    return builder.call(wixvw__wlqw, [obj])


def dict_values(builder, context, obj):
    qpes__equjl = context.get_argument_type(types.pyobject)
    xjrm__emr = lir.FunctionType(qpes__equjl, [qpes__equjl])
    wixvw__wlqw = cgutils.get_or_insert_function(builder.module, xjrm__emr,
        name='dict_values')
    return builder.call(wixvw__wlqw, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    qpes__equjl = context.get_argument_type(types.pyobject)
    xjrm__emr = lir.FunctionType(lir.VoidType(), [qpes__equjl, qpes__equjl])
    wixvw__wlqw = cgutils.get_or_insert_function(builder.module, xjrm__emr,
        name='dict_merge_from_seq2')
    builder.call(wixvw__wlqw, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    zxq__fzqn = cgutils.alloca_once_value(builder, val)
    tbkbh__ykl = list_check(builder, context, val)
    isar__plwsk = builder.icmp_unsigned('!=', tbkbh__ykl, lir.Constant(
        tbkbh__ykl.type, 0))
    with builder.if_then(isar__plwsk):
        zeu__kvx = context.insert_const_string(builder.module, 'numpy')
        agxth__plecw = c.pyapi.import_module_noblock(zeu__kvx)
        qywo__xiusl = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            qywo__xiusl = str(typ.dtype)
        doxb__jjts = c.pyapi.object_getattr_string(agxth__plecw, qywo__xiusl)
        zfibb__ecll = builder.load(zxq__fzqn)
        pkyp__qwooh = c.pyapi.call_method(agxth__plecw, 'asarray', (
            zfibb__ecll, doxb__jjts))
        builder.store(pkyp__qwooh, zxq__fzqn)
        c.pyapi.decref(agxth__plecw)
        c.pyapi.decref(doxb__jjts)
    val = builder.load(zxq__fzqn)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        uggq__foclc = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        sqbnx__seovg, qht__pwl = c.pyapi.call_jit_code(lambda a:
            get_utf8_size(a), types.int64(bodo.string_type), [uggq__foclc])
        context.nrt.decref(builder, typ, uggq__foclc)
        return cgutils.pack_array(builder, [qht__pwl])
    if isinstance(typ, (StructType, types.BaseTuple)):
        zeu__kvx = context.insert_const_string(builder.module, 'pandas')
        pbqkg__dqult = c.pyapi.import_module_noblock(zeu__kvx)
        C_NA = c.pyapi.object_getattr_string(pbqkg__dqult, 'NA')
        hdwp__ypcga = bodo.utils.transform.get_type_alloc_counts(typ)
        ebxas__bznsc = context.make_tuple(builder, types.Tuple(hdwp__ypcga *
            [types.int64]), hdwp__ypcga * [context.get_constant(types.int64,
            0)])
        pkek__upx = cgutils.alloca_once_value(builder, ebxas__bznsc)
        pegh__tfa = 0
        vqcm__stgpq = typ.data if isinstance(typ, StructType) else typ.types
        for mnq__doq, t in enumerate(vqcm__stgpq):
            xlm__wrdf = bodo.utils.transform.get_type_alloc_counts(t)
            if xlm__wrdf == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    mnq__doq])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, mnq__doq)
            trf__prn = is_na_value(builder, context, val_obj, C_NA)
            euza__louts = builder.icmp_unsigned('!=', trf__prn, lir.
                Constant(trf__prn.type, 1))
            with builder.if_then(euza__louts):
                ebxas__bznsc = builder.load(pkek__upx)
                bsaqv__doy = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for mnq__doq in range(xlm__wrdf):
                    mgs__atvm = builder.extract_value(ebxas__bznsc, 
                        pegh__tfa + mnq__doq)
                    ijf__awjca = builder.extract_value(bsaqv__doy, mnq__doq)
                    ebxas__bznsc = builder.insert_value(ebxas__bznsc,
                        builder.add(mgs__atvm, ijf__awjca), pegh__tfa +
                        mnq__doq)
                builder.store(ebxas__bznsc, pkek__upx)
            pegh__tfa += xlm__wrdf
        c.pyapi.decref(pbqkg__dqult)
        c.pyapi.decref(C_NA)
        return builder.load(pkek__upx)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    zeu__kvx = context.insert_const_string(builder.module, 'pandas')
    pbqkg__dqult = c.pyapi.import_module_noblock(zeu__kvx)
    C_NA = c.pyapi.object_getattr_string(pbqkg__dqult, 'NA')
    hdwp__ypcga = bodo.utils.transform.get_type_alloc_counts(typ)
    ebxas__bznsc = context.make_tuple(builder, types.Tuple(hdwp__ypcga * [
        types.int64]), [n] + (hdwp__ypcga - 1) * [context.get_constant(
        types.int64, 0)])
    pkek__upx = cgutils.alloca_once_value(builder, ebxas__bznsc)
    with cgutils.for_range(builder, n) as vakwi__weyaj:
        usiu__ijgx = vakwi__weyaj.index
        rwm__wgkr = seq_getitem(builder, context, arr_obj, usiu__ijgx)
        trf__prn = is_na_value(builder, context, rwm__wgkr, C_NA)
        euza__louts = builder.icmp_unsigned('!=', trf__prn, lir.Constant(
            trf__prn.type, 1))
        with builder.if_then(euza__louts):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                ebxas__bznsc = builder.load(pkek__upx)
                bsaqv__doy = get_array_elem_counts(c, builder, context,
                    rwm__wgkr, typ.dtype)
                for mnq__doq in range(hdwp__ypcga - 1):
                    mgs__atvm = builder.extract_value(ebxas__bznsc, 
                        mnq__doq + 1)
                    ijf__awjca = builder.extract_value(bsaqv__doy, mnq__doq)
                    ebxas__bznsc = builder.insert_value(ebxas__bznsc,
                        builder.add(mgs__atvm, ijf__awjca), mnq__doq + 1)
                builder.store(ebxas__bznsc, pkek__upx)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                pegh__tfa = 1
                for mnq__doq, t in enumerate(typ.data):
                    xlm__wrdf = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if xlm__wrdf == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(rwm__wgkr, mnq__doq)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(rwm__wgkr,
                            typ.names[mnq__doq])
                    trf__prn = is_na_value(builder, context, val_obj, C_NA)
                    euza__louts = builder.icmp_unsigned('!=', trf__prn, lir
                        .Constant(trf__prn.type, 1))
                    with builder.if_then(euza__louts):
                        ebxas__bznsc = builder.load(pkek__upx)
                        bsaqv__doy = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for mnq__doq in range(xlm__wrdf):
                            mgs__atvm = builder.extract_value(ebxas__bznsc,
                                pegh__tfa + mnq__doq)
                            ijf__awjca = builder.extract_value(bsaqv__doy,
                                mnq__doq)
                            ebxas__bznsc = builder.insert_value(ebxas__bznsc,
                                builder.add(mgs__atvm, ijf__awjca), 
                                pegh__tfa + mnq__doq)
                        builder.store(ebxas__bznsc, pkek__upx)
                    pegh__tfa += xlm__wrdf
            else:
                assert isinstance(typ, MapArrayType), typ
                ebxas__bznsc = builder.load(pkek__upx)
                sut__qdi = dict_keys(builder, context, rwm__wgkr)
                qsyn__wlc = dict_values(builder, context, rwm__wgkr)
                tkqf__ucbj = get_array_elem_counts(c, builder, context,
                    sut__qdi, typ.key_arr_type)
                aucsd__vmch = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for mnq__doq in range(1, aucsd__vmch + 1):
                    mgs__atvm = builder.extract_value(ebxas__bznsc, mnq__doq)
                    ijf__awjca = builder.extract_value(tkqf__ucbj, mnq__doq - 1
                        )
                    ebxas__bznsc = builder.insert_value(ebxas__bznsc,
                        builder.add(mgs__atvm, ijf__awjca), mnq__doq)
                cnp__uvhe = get_array_elem_counts(c, builder, context,
                    qsyn__wlc, typ.value_arr_type)
                for mnq__doq in range(aucsd__vmch + 1, hdwp__ypcga):
                    mgs__atvm = builder.extract_value(ebxas__bznsc, mnq__doq)
                    ijf__awjca = builder.extract_value(cnp__uvhe, mnq__doq -
                        aucsd__vmch)
                    ebxas__bznsc = builder.insert_value(ebxas__bznsc,
                        builder.add(mgs__atvm, ijf__awjca), mnq__doq)
                builder.store(ebxas__bznsc, pkek__upx)
                c.pyapi.decref(sut__qdi)
                c.pyapi.decref(qsyn__wlc)
        c.pyapi.decref(rwm__wgkr)
    c.pyapi.decref(pbqkg__dqult)
    c.pyapi.decref(C_NA)
    return builder.load(pkek__upx)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    cro__iotml = n_elems.type.count
    assert cro__iotml >= 1
    cnee__gue = builder.extract_value(n_elems, 0)
    if cro__iotml != 1:
        azpmy__rmm = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, mnq__doq) for mnq__doq in range(1, cro__iotml)])
        ftakj__ygjs = types.Tuple([types.int64] * (cro__iotml - 1))
    else:
        azpmy__rmm = context.get_dummy_value()
        ftakj__ygjs = types.none
    bblwq__alv = types.TypeRef(arr_type)
    kyple__jqpz = arr_type(types.int64, bblwq__alv, ftakj__ygjs)
    args = [cnee__gue, context.get_dummy_value(), azpmy__rmm]
    ivw__vtbdv = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        sqbnx__seovg, pxiz__hbuxr = c.pyapi.call_jit_code(ivw__vtbdv,
            kyple__jqpz, args)
    else:
        pxiz__hbuxr = context.compile_internal(builder, ivw__vtbdv,
            kyple__jqpz, args)
    return pxiz__hbuxr


def is_ll_eq(builder, val1, val2):
    noa__tctw = val1.type.pointee
    wka__jinz = val2.type.pointee
    assert noa__tctw == wka__jinz, 'invalid llvm value comparison'
    if isinstance(noa__tctw, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(noa__tctw.elements) if isinstance(noa__tctw, lir.
            BaseStructType) else noa__tctw.count
        oble__rabe = lir.Constant(lir.IntType(1), 1)
        for mnq__doq in range(n_elems):
            npzlb__tjf = lir.IntType(32)(0)
            kldsv__zug = lir.IntType(32)(mnq__doq)
            dqv__wirwo = builder.gep(val1, [npzlb__tjf, kldsv__zug],
                inbounds=True)
            ayfx__skqi = builder.gep(val2, [npzlb__tjf, kldsv__zug],
                inbounds=True)
            oble__rabe = builder.and_(oble__rabe, is_ll_eq(builder,
                dqv__wirwo, ayfx__skqi))
        return oble__rabe
    jgllk__vso = builder.load(val1)
    vocbr__qevto = builder.load(val2)
    if jgllk__vso.type in (lir.FloatType(), lir.DoubleType()):
        lbikn__hghvl = 32 if jgllk__vso.type == lir.FloatType() else 64
        jgllk__vso = builder.bitcast(jgllk__vso, lir.IntType(lbikn__hghvl))
        vocbr__qevto = builder.bitcast(vocbr__qevto, lir.IntType(lbikn__hghvl))
    return builder.icmp_unsigned('==', jgllk__vso, vocbr__qevto)
