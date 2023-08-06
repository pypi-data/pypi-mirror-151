"""Array implementation for map values.
Corresponds to Spark's MapType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Map arrays: https://github.com/apache/arrow/blob/master/format/Schema.fbs

The implementation uses an array(struct) array underneath similar to Spark and Arrow.
For example: [{1: 2.1, 3: 1.1}, {5: -1.0}]
[[{"key": 1, "value" 2.1}, {"key": 3, "value": 1.1}], [{"key": 5, "value": -1.0}]]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, _get_array_item_arr_payload, offset_type
from bodo.libs.struct_arr_ext import StructArrayType, _get_struct_arr_payload
from bodo.utils.cg_helpers import dict_keys, dict_merge_from_seq2, dict_values, gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit
from bodo.utils.typing import BodoError
from bodo.libs import array_ext, hdist
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('map_array_from_sequence', array_ext.map_array_from_sequence)
ll.add_symbol('np_array_from_map_array', array_ext.np_array_from_map_array)


class MapArrayType(types.ArrayCompatible):

    def __init__(self, key_arr_type, value_arr_type):
        self.key_arr_type = key_arr_type
        self.value_arr_type = value_arr_type
        super(MapArrayType, self).__init__(name='MapArrayType({}, {})'.
            format(key_arr_type, value_arr_type))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.DictType(self.key_arr_type.dtype, self.value_arr_type.
            dtype)

    def copy(self):
        return MapArrayType(self.key_arr_type, self.value_arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_map_arr_data_type(map_type):
    pfwl__tno = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(pfwl__tno)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zmez__vqhp = _get_map_arr_data_type(fe_type)
        ukaga__aeuo = [('data', zmez__vqhp)]
        models.StructModel.__init__(self, dmm, fe_type, ukaga__aeuo)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    uvx__gewun = all(isinstance(mqo__btexj, types.Array) and mqo__btexj.
        dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for mqo__btexj in (typ.key_arr_type, typ.
        value_arr_type))
    if uvx__gewun:
        edx__lmauk = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        aynb__zqu = cgutils.get_or_insert_function(c.builder.module,
            edx__lmauk, name='count_total_elems_list_array')
        chgt__fiah = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            aynb__zqu, [val])])
    else:
        chgt__fiah = get_array_elem_counts(c, c.builder, c.context, val, typ)
    zmez__vqhp = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, zmez__vqhp,
        chgt__fiah, c)
    bpw__avmzw = _get_array_item_arr_payload(c.context, c.builder,
        zmez__vqhp, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, bpw__avmzw.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, bpw__avmzw.offsets).data
    zeux__wdngq = _get_struct_arr_payload(c.context, c.builder, zmez__vqhp.
        dtype, bpw__avmzw.data)
    key_arr = c.builder.extract_value(zeux__wdngq.data, 0)
    value_arr = c.builder.extract_value(zeux__wdngq.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    rbko__njr, tten__wbx = c.pyapi.call_jit_code(lambda A: A.fill(255), sig,
        [zeux__wdngq.null_bitmap])
    if uvx__gewun:
        yakt__axzxr = c.context.make_array(zmez__vqhp.dtype.data[0])(c.
            context, c.builder, key_arr).data
        yos__ivxzo = c.context.make_array(zmez__vqhp.dtype.data[1])(c.
            context, c.builder, value_arr).data
        edx__lmauk = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        opzem__jtjnt = cgutils.get_or_insert_function(c.builder.module,
            edx__lmauk, name='map_array_from_sequence')
        xvioa__moai = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        xslh__tqotd = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype
            )
        c.builder.call(opzem__jtjnt, [val, c.builder.bitcast(yakt__axzxr,
            lir.IntType(8).as_pointer()), c.builder.bitcast(yos__ivxzo, lir
            .IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), xvioa__moai), lir.Constant(lir.
            IntType(32), xslh__tqotd)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    xoxi__xduz = c.context.make_helper(c.builder, typ)
    xoxi__xduz.data = data_arr
    ius__xppe = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xoxi__xduz._getvalue(), is_error=ius__xppe)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    mgl__xnieo = context.insert_const_string(builder.module, 'pandas')
    ufs__bme = c.pyapi.import_module_noblock(mgl__xnieo)
    rsmd__ryz = c.pyapi.object_getattr_string(ufs__bme, 'NA')
    uuyaz__xrf = c.context.get_constant(offset_type, 0)
    builder.store(uuyaz__xrf, offsets_ptr)
    jzbg__kudd = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as mgmte__hxnj:
        akjh__qga = mgmte__hxnj.index
        item_ind = builder.load(jzbg__kudd)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [akjh__qga]))
        jmztp__mtida = seq_getitem(builder, context, val, akjh__qga)
        set_bitmap_bit(builder, null_bitmap_ptr, akjh__qga, 0)
        tem__chixm = is_na_value(builder, context, jmztp__mtida, rsmd__ryz)
        mtny__mpgr = builder.icmp_unsigned('!=', tem__chixm, lir.Constant(
            tem__chixm.type, 1))
        with builder.if_then(mtny__mpgr):
            set_bitmap_bit(builder, null_bitmap_ptr, akjh__qga, 1)
            ckeu__espxn = dict_keys(builder, context, jmztp__mtida)
            xuv__dqebc = dict_values(builder, context, jmztp__mtida)
            n_items = bodo.utils.utils.object_length(c, ckeu__espxn)
            _unbox_array_item_array_copy_data(typ.key_arr_type, ckeu__espxn,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                xuv__dqebc, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), jzbg__kudd)
            c.pyapi.decref(ckeu__espxn)
            c.pyapi.decref(xuv__dqebc)
        c.pyapi.decref(jmztp__mtida)
    builder.store(builder.trunc(builder.load(jzbg__kudd), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(ufs__bme)
    c.pyapi.decref(rsmd__ryz)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    xoxi__xduz = c.context.make_helper(c.builder, typ, val)
    data_arr = xoxi__xduz.data
    zmez__vqhp = _get_map_arr_data_type(typ)
    bpw__avmzw = _get_array_item_arr_payload(c.context, c.builder,
        zmez__vqhp, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, bpw__avmzw.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, bpw__avmzw.offsets).data
    zeux__wdngq = _get_struct_arr_payload(c.context, c.builder, zmez__vqhp.
        dtype, bpw__avmzw.data)
    key_arr = c.builder.extract_value(zeux__wdngq.data, 0)
    value_arr = c.builder.extract_value(zeux__wdngq.data, 1)
    if all(isinstance(mqo__btexj, types.Array) and mqo__btexj.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type) for
        mqo__btexj in (typ.key_arr_type, typ.value_arr_type)):
        yakt__axzxr = c.context.make_array(zmez__vqhp.dtype.data[0])(c.
            context, c.builder, key_arr).data
        yos__ivxzo = c.context.make_array(zmez__vqhp.dtype.data[1])(c.
            context, c.builder, value_arr).data
        edx__lmauk = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        hnna__odic = cgutils.get_or_insert_function(c.builder.module,
            edx__lmauk, name='np_array_from_map_array')
        xvioa__moai = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        xslh__tqotd = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype
            )
        arr = c.builder.call(hnna__odic, [bpw__avmzw.n_arrays, c.builder.
            bitcast(yakt__axzxr, lir.IntType(8).as_pointer()), c.builder.
            bitcast(yos__ivxzo, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), xvioa__moai),
            lir.Constant(lir.IntType(32), xslh__tqotd)])
    else:
        arr = _box_map_array_generic(typ, c, bpw__avmzw.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    mgl__xnieo = context.insert_const_string(builder.module, 'numpy')
    zooxe__dsquv = c.pyapi.import_module_noblock(mgl__xnieo)
    hpyih__calmp = c.pyapi.object_getattr_string(zooxe__dsquv, 'object_')
    bqbg__bhotp = c.pyapi.long_from_longlong(n_maps)
    zpi__ajz = c.pyapi.call_method(zooxe__dsquv, 'ndarray', (bqbg__bhotp,
        hpyih__calmp))
    pdp__hzi = c.pyapi.object_getattr_string(zooxe__dsquv, 'nan')
    drumu__mxaw = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    jzbg__kudd = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as mgmte__hxnj:
        fpu__phf = mgmte__hxnj.index
        pyarray_setitem(builder, context, zpi__ajz, fpu__phf, pdp__hzi)
        dgcb__oaoow = get_bitmap_bit(builder, null_bitmap_ptr, fpu__phf)
        rmqnp__wyg = builder.icmp_unsigned('!=', dgcb__oaoow, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(rmqnp__wyg):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(fpu__phf, lir.Constant(fpu__phf.
                type, 1))])), builder.load(builder.gep(offsets_ptr, [
                fpu__phf]))), lir.IntType(64))
            item_ind = builder.load(jzbg__kudd)
            jmztp__mtida = c.pyapi.dict_new()
            dszpx__sezam = lambda data_arr, item_ind, n_items: data_arr[
                item_ind:item_ind + n_items]
            rbko__njr, uqwf__lsoih = c.pyapi.call_jit_code(dszpx__sezam,
                typ.key_arr_type(typ.key_arr_type, types.int64, types.int64
                ), [key_arr, item_ind, n_items])
            rbko__njr, pfsjc__ttudk = c.pyapi.call_jit_code(dszpx__sezam,
                typ.value_arr_type(typ.value_arr_type, types.int64, types.
                int64), [value_arr, item_ind, n_items])
            bfcmz__rigj = c.pyapi.from_native_value(typ.key_arr_type,
                uqwf__lsoih, c.env_manager)
            dvna__ogepb = c.pyapi.from_native_value(typ.value_arr_type,
                pfsjc__ttudk, c.env_manager)
            ingd__vjyq = c.pyapi.call_function_objargs(drumu__mxaw, (
                bfcmz__rigj, dvna__ogepb))
            dict_merge_from_seq2(builder, context, jmztp__mtida, ingd__vjyq)
            builder.store(builder.add(item_ind, n_items), jzbg__kudd)
            pyarray_setitem(builder, context, zpi__ajz, fpu__phf, jmztp__mtida)
            c.pyapi.decref(ingd__vjyq)
            c.pyapi.decref(bfcmz__rigj)
            c.pyapi.decref(dvna__ogepb)
            c.pyapi.decref(jmztp__mtida)
    c.pyapi.decref(drumu__mxaw)
    c.pyapi.decref(zooxe__dsquv)
    c.pyapi.decref(hpyih__calmp)
    c.pyapi.decref(bqbg__bhotp)
    c.pyapi.decref(pdp__hzi)
    return zpi__ajz


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    xoxi__xduz = context.make_helper(builder, sig.return_type)
    xoxi__xduz.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return xoxi__xduz._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    vgk__qmvp = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return vgk__qmvp(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    gabz__nywo = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(gabz__nywo)


def pre_alloc_map_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_map_arr_ext_pre_alloc_map_array
    ) = pre_alloc_map_array_equiv


@overload(len, no_unliteral=True)
def overload_map_arr_len(A):
    if isinstance(A, MapArrayType):
        return lambda A: len(A._data)


@overload_attribute(MapArrayType, 'shape')
def overload_map_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(MapArrayType, 'dtype')
def overload_map_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(MapArrayType, 'ndim')
def overload_map_arr_ndim(A):
    return lambda A: 1


@overload_attribute(MapArrayType, 'nbytes')
def overload_map_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(MapArrayType, 'copy')
def overload_map_arr_copy(A):
    return lambda A: init_map_arr(A._data.copy())


@overload(operator.setitem, no_unliteral=True)
def map_arr_setitem(arr, ind, val):
    if not isinstance(arr, MapArrayType):
        return
    oan__fpzg = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            gzzw__irq = val.keys()
            wxrvl__lvai = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), oan__fpzg, ('key', 'value'))
            for fovjg__invym, rkrp__xfc in enumerate(gzzw__irq):
                wxrvl__lvai[fovjg__invym
                    ] = bodo.libs.struct_arr_ext.init_struct((rkrp__xfc,
                    val[rkrp__xfc]), ('key', 'value'))
            arr._data[ind] = wxrvl__lvai
        return map_arr_setitem_impl
    raise BodoError(
        'operator.setitem with MapArrays is only supported with an integer index.'
        )


@overload(operator.getitem, no_unliteral=True)
def map_arr_getitem(arr, ind):
    if not isinstance(arr, MapArrayType):
        return
    if isinstance(ind, types.Integer):

        def map_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            umu__hezfy = dict()
            ebay__oov = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            wxrvl__lvai = bodo.libs.array_item_arr_ext.get_data(arr._data)
            zjik__zhong, znyr__knbl = bodo.libs.struct_arr_ext.get_data(
                wxrvl__lvai)
            vuwsw__nnhzz = ebay__oov[ind]
            vpnd__chqv = ebay__oov[ind + 1]
            for fovjg__invym in range(vuwsw__nnhzz, vpnd__chqv):
                umu__hezfy[zjik__zhong[fovjg__invym]] = znyr__knbl[fovjg__invym
                    ]
            return umu__hezfy
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
