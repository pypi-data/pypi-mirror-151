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
    szems__aetk = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(szems__aetk)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lqi__aijno = _get_map_arr_data_type(fe_type)
        crl__dobc = [('data', lqi__aijno)]
        models.StructModel.__init__(self, dmm, fe_type, crl__dobc)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    qaodk__samzt = all(isinstance(jfnss__plxoz, types.Array) and 
        jfnss__plxoz.dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) for jfnss__plxoz in (typ.key_arr_type, typ.
        value_arr_type))
    if qaodk__samzt:
        xjew__ucsz = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        bhucz__eki = cgutils.get_or_insert_function(c.builder.module,
            xjew__ucsz, name='count_total_elems_list_array')
        dsujg__geyv = cgutils.pack_array(c.builder, [n_maps, c.builder.call
            (bhucz__eki, [val])])
    else:
        dsujg__geyv = get_array_elem_counts(c, c.builder, c.context, val, typ)
    lqi__aijno = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, lqi__aijno,
        dsujg__geyv, c)
    jelkv__jrzi = _get_array_item_arr_payload(c.context, c.builder,
        lqi__aijno, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, jelkv__jrzi.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, jelkv__jrzi.offsets).data
    beztd__vkpj = _get_struct_arr_payload(c.context, c.builder, lqi__aijno.
        dtype, jelkv__jrzi.data)
    key_arr = c.builder.extract_value(beztd__vkpj.data, 0)
    value_arr = c.builder.extract_value(beztd__vkpj.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    cifp__hyfrh, mtwns__syom = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [beztd__vkpj.null_bitmap])
    if qaodk__samzt:
        ljw__gxqm = c.context.make_array(lqi__aijno.dtype.data[0])(c.
            context, c.builder, key_arr).data
        asl__uqa = c.context.make_array(lqi__aijno.dtype.data[1])(c.context,
            c.builder, value_arr).data
        xjew__ucsz = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        ugky__wmn = cgutils.get_or_insert_function(c.builder.module,
            xjew__ucsz, name='map_array_from_sequence')
        ozp__bjz = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        gel__fert = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        c.builder.call(ugky__wmn, [val, c.builder.bitcast(ljw__gxqm, lir.
            IntType(8).as_pointer()), c.builder.bitcast(asl__uqa, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), ozp__bjz), lir.Constant(lir.IntType(
            32), gel__fert)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    vsbk__ilo = c.context.make_helper(c.builder, typ)
    vsbk__ilo.data = data_arr
    ctcee__nzdv = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(vsbk__ilo._getvalue(), is_error=ctcee__nzdv)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    pqi__psh = context.insert_const_string(builder.module, 'pandas')
    lbqm__uvn = c.pyapi.import_module_noblock(pqi__psh)
    svmw__xaewn = c.pyapi.object_getattr_string(lbqm__uvn, 'NA')
    thul__vhhqa = c.context.get_constant(offset_type, 0)
    builder.store(thul__vhhqa, offsets_ptr)
    oxo__seneh = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as gou__hgka:
        bidk__cffgk = gou__hgka.index
        item_ind = builder.load(oxo__seneh)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [bidk__cffgk]))
        yoawy__alz = seq_getitem(builder, context, val, bidk__cffgk)
        set_bitmap_bit(builder, null_bitmap_ptr, bidk__cffgk, 0)
        boj__het = is_na_value(builder, context, yoawy__alz, svmw__xaewn)
        hdyb__csp = builder.icmp_unsigned('!=', boj__het, lir.Constant(
            boj__het.type, 1))
        with builder.if_then(hdyb__csp):
            set_bitmap_bit(builder, null_bitmap_ptr, bidk__cffgk, 1)
            veec__uja = dict_keys(builder, context, yoawy__alz)
            mlh__tsxm = dict_values(builder, context, yoawy__alz)
            n_items = bodo.utils.utils.object_length(c, veec__uja)
            _unbox_array_item_array_copy_data(typ.key_arr_type, veec__uja,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type, mlh__tsxm,
                c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), oxo__seneh)
            c.pyapi.decref(veec__uja)
            c.pyapi.decref(mlh__tsxm)
        c.pyapi.decref(yoawy__alz)
    builder.store(builder.trunc(builder.load(oxo__seneh), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(lbqm__uvn)
    c.pyapi.decref(svmw__xaewn)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    vsbk__ilo = c.context.make_helper(c.builder, typ, val)
    data_arr = vsbk__ilo.data
    lqi__aijno = _get_map_arr_data_type(typ)
    jelkv__jrzi = _get_array_item_arr_payload(c.context, c.builder,
        lqi__aijno, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, jelkv__jrzi.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, jelkv__jrzi.offsets).data
    beztd__vkpj = _get_struct_arr_payload(c.context, c.builder, lqi__aijno.
        dtype, jelkv__jrzi.data)
    key_arr = c.builder.extract_value(beztd__vkpj.data, 0)
    value_arr = c.builder.extract_value(beztd__vkpj.data, 1)
    if all(isinstance(jfnss__plxoz, types.Array) and jfnss__plxoz.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        jfnss__plxoz in (typ.key_arr_type, typ.value_arr_type)):
        ljw__gxqm = c.context.make_array(lqi__aijno.dtype.data[0])(c.
            context, c.builder, key_arr).data
        asl__uqa = c.context.make_array(lqi__aijno.dtype.data[1])(c.context,
            c.builder, value_arr).data
        xjew__ucsz = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        sqlgw__ldi = cgutils.get_or_insert_function(c.builder.module,
            xjew__ucsz, name='np_array_from_map_array')
        ozp__bjz = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        gel__fert = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype)
        arr = c.builder.call(sqlgw__ldi, [jelkv__jrzi.n_arrays, c.builder.
            bitcast(ljw__gxqm, lir.IntType(8).as_pointer()), c.builder.
            bitcast(asl__uqa, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), ozp__bjz), lir.
            Constant(lir.IntType(32), gel__fert)])
    else:
        arr = _box_map_array_generic(typ, c, jelkv__jrzi.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    pqi__psh = context.insert_const_string(builder.module, 'numpy')
    zze__jkqnn = c.pyapi.import_module_noblock(pqi__psh)
    ubcbh__rao = c.pyapi.object_getattr_string(zze__jkqnn, 'object_')
    thrbj__wbjsw = c.pyapi.long_from_longlong(n_maps)
    jibt__bdtgd = c.pyapi.call_method(zze__jkqnn, 'ndarray', (thrbj__wbjsw,
        ubcbh__rao))
    eix__gutw = c.pyapi.object_getattr_string(zze__jkqnn, 'nan')
    cir__xxlyu = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    oxo__seneh = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as gou__hgka:
        fwp__khfgu = gou__hgka.index
        pyarray_setitem(builder, context, jibt__bdtgd, fwp__khfgu, eix__gutw)
        sxxel__hxl = get_bitmap_bit(builder, null_bitmap_ptr, fwp__khfgu)
        qynhq__wzg = builder.icmp_unsigned('!=', sxxel__hxl, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(qynhq__wzg):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(fwp__khfgu, lir.Constant(
                fwp__khfgu.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [fwp__khfgu]))), lir.IntType(64))
            item_ind = builder.load(oxo__seneh)
            yoawy__alz = c.pyapi.dict_new()
            sjtpg__pkln = lambda data_arr, item_ind, n_items: data_arr[item_ind
                :item_ind + n_items]
            cifp__hyfrh, doii__orpxh = c.pyapi.call_jit_code(sjtpg__pkln,
                typ.key_arr_type(typ.key_arr_type, types.int64, types.int64
                ), [key_arr, item_ind, n_items])
            cifp__hyfrh, jzwig__wnllp = c.pyapi.call_jit_code(sjtpg__pkln,
                typ.value_arr_type(typ.value_arr_type, types.int64, types.
                int64), [value_arr, item_ind, n_items])
            sor__efvk = c.pyapi.from_native_value(typ.key_arr_type,
                doii__orpxh, c.env_manager)
            yrsh__pbp = c.pyapi.from_native_value(typ.value_arr_type,
                jzwig__wnllp, c.env_manager)
            tfya__iqxx = c.pyapi.call_function_objargs(cir__xxlyu, (
                sor__efvk, yrsh__pbp))
            dict_merge_from_seq2(builder, context, yoawy__alz, tfya__iqxx)
            builder.store(builder.add(item_ind, n_items), oxo__seneh)
            pyarray_setitem(builder, context, jibt__bdtgd, fwp__khfgu,
                yoawy__alz)
            c.pyapi.decref(tfya__iqxx)
            c.pyapi.decref(sor__efvk)
            c.pyapi.decref(yrsh__pbp)
            c.pyapi.decref(yoawy__alz)
    c.pyapi.decref(cir__xxlyu)
    c.pyapi.decref(zze__jkqnn)
    c.pyapi.decref(ubcbh__rao)
    c.pyapi.decref(thrbj__wbjsw)
    c.pyapi.decref(eix__gutw)
    return jibt__bdtgd


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    vsbk__ilo = context.make_helper(builder, sig.return_type)
    vsbk__ilo.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return vsbk__ilo._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    sdoyp__mqu = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return sdoyp__mqu(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    ixehh__ldp = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        num_maps, nested_counts, struct_typ)
    return init_map_arr(ixehh__ldp)


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
    pss__cuf = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            ejulv__uahe = val.keys()
            fbvct__hwq = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), pss__cuf, ('key', 'value'))
            for afd__qhrga, hqv__oqxf in enumerate(ejulv__uahe):
                fbvct__hwq[afd__qhrga] = bodo.libs.struct_arr_ext.init_struct((
                    hqv__oqxf, val[hqv__oqxf]), ('key', 'value'))
            arr._data[ind] = fbvct__hwq
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
            glk__toyp = dict()
            myh__vpb = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            fbvct__hwq = bodo.libs.array_item_arr_ext.get_data(arr._data)
            jeie__agt, gvrs__fgkpq = bodo.libs.struct_arr_ext.get_data(
                fbvct__hwq)
            ptvlr__ouov = myh__vpb[ind]
            ocbz__vujr = myh__vpb[ind + 1]
            for afd__qhrga in range(ptvlr__ouov, ocbz__vujr):
                glk__toyp[jeie__agt[afd__qhrga]] = gvrs__fgkpq[afd__qhrga]
            return glk__toyp
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
