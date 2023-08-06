"""Nullable integer array corresponding to Pandas IntegerArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.str_arr_ext import kBitmask
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('mask_arr_to_bitmap', hstr_ext.mask_arr_to_bitmap)
ll.add_symbol('is_pd_int_array', array_ext.is_pd_int_array)
ll.add_symbol('int_array_from_sequence', array_ext.int_array_from_sequence)
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error, to_nullable_type


class IntegerArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(IntegerArrayType, self).__init__(name=
            f'IntegerArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntegerArrayType(self.dtype)

    @property
    def get_pandas_scalar_type_instance(self):
        sziye__cpu = int(np.log2(self.dtype.bitwidth // 8))
        bhx__fgjbw = 0 if self.dtype.signed else 4
        idx = sziye__cpu + bhx__fgjbw
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kie__ipi = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, kie__ipi)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    rskxz__ruka = 8 * val.dtype.itemsize
    rtxr__ecnu = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(rtxr__ecnu, rskxz__ruka))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        vipjk__owycg = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(vipjk__owycg)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    uhl__gnao = c.context.insert_const_string(c.builder.module, 'pandas')
    bpliq__aptu = c.pyapi.import_module_noblock(uhl__gnao)
    vnc__moe = c.pyapi.call_method(bpliq__aptu, str(typ)[:-2], ())
    c.pyapi.decref(bpliq__aptu)
    return vnc__moe


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    rskxz__ruka = 8 * val.itemsize
    rtxr__ecnu = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(rtxr__ecnu, rskxz__ruka))
    return IntDtype(dtype)


def _register_int_dtype(t):
    typeof_impl.register(t)(typeof_pd_int_dtype)
    int_dtype = typeof_pd_int_dtype(t(), None)
    type_callable(t)(lambda c: lambda : int_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


pd_int_dtype_classes = (pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.
    Int64Dtype, pd.UInt8Dtype, pd.UInt16Dtype, pd.UInt32Dtype, pd.UInt64Dtype)
for t in pd_int_dtype_classes:
    _register_int_dtype(t)


@numba.extending.register_jitable
def mask_arr_to_bitmap(mask_arr):
    n = len(mask_arr)
    jpo__skl = n + 7 >> 3
    sdo__sodoz = np.empty(jpo__skl, np.uint8)
    for i in range(n):
        ykt__niig = i // 8
        sdo__sodoz[ykt__niig] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            sdo__sodoz[ykt__niig]) & kBitmask[i % 8]
    return sdo__sodoz


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    puvg__eek = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(puvg__eek)
    c.pyapi.decref(puvg__eek)
    wejja__wrdrq = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jpo__skl = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(64),
        7)), lir.Constant(lir.IntType(64), 8))
    kenkw__zduqo = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [jpo__skl])
    xejm__kmyxi = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    sdzuv__qudna = cgutils.get_or_insert_function(c.builder.module,
        xejm__kmyxi, name='is_pd_int_array')
    lcpz__jirvp = c.builder.call(sdzuv__qudna, [obj])
    bwfov__aaud = c.builder.icmp_unsigned('!=', lcpz__jirvp, lcpz__jirvp.
        type(0))
    with c.builder.if_else(bwfov__aaud) as (iip__lqsl, wbqp__ceqbc):
        with iip__lqsl:
            agxn__qmwsy = c.pyapi.object_getattr_string(obj, '_data')
            wejja__wrdrq.data = c.pyapi.to_native_value(types.Array(typ.
                dtype, 1, 'C'), agxn__qmwsy).value
            ozwj__kub = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), ozwj__kub).value
            c.pyapi.decref(agxn__qmwsy)
            c.pyapi.decref(ozwj__kub)
            nhk__abnb = c.context.make_array(types.Array(types.bool_, 1, 'C'))(
                c.context, c.builder, mask_arr)
            xejm__kmyxi = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            sdzuv__qudna = cgutils.get_or_insert_function(c.builder.module,
                xejm__kmyxi, name='mask_arr_to_bitmap')
            c.builder.call(sdzuv__qudna, [kenkw__zduqo.data, nhk__abnb.data, n]
                )
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with wbqp__ceqbc:
            exmnz__vuh = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            xejm__kmyxi = lir.FunctionType(lir.IntType(32), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            pjwmd__xbt = cgutils.get_or_insert_function(c.builder.module,
                xejm__kmyxi, name='int_array_from_sequence')
            c.builder.call(pjwmd__xbt, [obj, c.builder.bitcast(exmnz__vuh.
                data, lir.IntType(8).as_pointer()), kenkw__zduqo.data])
            wejja__wrdrq.data = exmnz__vuh._getvalue()
    wejja__wrdrq.null_bitmap = kenkw__zduqo._getvalue()
    vvbfi__zxim = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(wejja__wrdrq._getvalue(), is_error=vvbfi__zxim)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    wejja__wrdrq = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        wejja__wrdrq.data, c.env_manager)
    vlmh__twaey = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, wejja__wrdrq.null_bitmap).data
    puvg__eek = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(puvg__eek)
    uhl__gnao = c.context.insert_const_string(c.builder.module, 'numpy')
    kvhce__mzd = c.pyapi.import_module_noblock(uhl__gnao)
    gikn__eakxw = c.pyapi.object_getattr_string(kvhce__mzd, 'bool_')
    mask_arr = c.pyapi.call_method(kvhce__mzd, 'empty', (puvg__eek,
        gikn__eakxw))
    wmufy__kjz = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    hgbw__xvs = c.pyapi.object_getattr_string(wmufy__kjz, 'data')
    ikad__yllgi = c.builder.inttoptr(c.pyapi.long_as_longlong(hgbw__xvs),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as waid__sgmx:
        i = waid__sgmx.index
        zqbap__jka = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        wvpfg__hfvs = c.builder.load(cgutils.gep(c.builder, vlmh__twaey,
            zqbap__jka))
        hcgh__wkzi = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(wvpfg__hfvs, hcgh__wkzi), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        jae__fzr = cgutils.gep(c.builder, ikad__yllgi, i)
        c.builder.store(val, jae__fzr)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        wejja__wrdrq.null_bitmap)
    uhl__gnao = c.context.insert_const_string(c.builder.module, 'pandas')
    bpliq__aptu = c.pyapi.import_module_noblock(uhl__gnao)
    xgyn__ezubi = c.pyapi.object_getattr_string(bpliq__aptu, 'arrays')
    vnc__moe = c.pyapi.call_method(xgyn__ezubi, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(bpliq__aptu)
    c.pyapi.decref(puvg__eek)
    c.pyapi.decref(kvhce__mzd)
    c.pyapi.decref(gikn__eakxw)
    c.pyapi.decref(wmufy__kjz)
    c.pyapi.decref(hgbw__xvs)
    c.pyapi.decref(xgyn__ezubi)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return vnc__moe


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        hrl__lkyrj, hzpl__vllu = args
        wejja__wrdrq = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        wejja__wrdrq.data = hrl__lkyrj
        wejja__wrdrq.null_bitmap = hzpl__vllu
        context.nrt.incref(builder, signature.args[0], hrl__lkyrj)
        context.nrt.incref(builder, signature.args[1], hzpl__vllu)
        return wejja__wrdrq._getvalue()
    izal__sjl = IntegerArrayType(data.dtype)
    uhoy__yvg = izal__sjl(data, null_bitmap)
    return uhoy__yvg, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    ipuhc__baget = np.empty(n, pyval.dtype.type)
    qrkoi__ahze = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        wiz__dadd = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(qrkoi__ahze, i, int(not wiz__dadd)
            )
        if not wiz__dadd:
            ipuhc__baget[i] = s
    jxu__ndo = context.get_constant_generic(builder, types.Array(typ.dtype,
        1, 'C'), ipuhc__baget)
    ots__aiwg = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), qrkoi__ahze)
    return lir.Constant.literal_struct([jxu__ndo, ots__aiwg])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    qdpyw__acqn = args[0]
    if equiv_set.has_shape(qdpyw__acqn):
        return ArrayAnalysis.AnalyzeResult(shape=qdpyw__acqn, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    qdpyw__acqn = args[0]
    if equiv_set.has_shape(qdpyw__acqn):
        return ArrayAnalysis.AnalyzeResult(shape=qdpyw__acqn, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_init_integer_array = (
    init_integer_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_integer_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_integer_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_integer_array
numba.core.ir_utils.alias_func_extensions['get_int_arr_data',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_int_arr_bitmap',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_int_array(n, dtype):
    ipuhc__baget = np.empty(n, dtype)
    zog__wjkgp = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(ipuhc__baget, zog__wjkgp)


def alloc_int_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_alloc_int_array = (
    alloc_int_array_equiv)


@numba.extending.register_jitable
def set_bit_to_arr(bits, i, bit_is_set):
    bits[i // 8] ^= np.uint8(-np.uint8(bit_is_set) ^ bits[i // 8]) & kBitmask[
        i % 8]


@numba.extending.register_jitable
def get_bit_bitmap_arr(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@overload(operator.getitem, no_unliteral=True)
def int_arr_getitem(A, ind):
    if not isinstance(A, IntegerArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            fbe__xat, qfoo__qroz = array_getitem_bool_index(A, ind)
            return init_integer_array(fbe__xat, qfoo__qroz)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            fbe__xat, qfoo__qroz = array_getitem_int_index(A, ind)
            return init_integer_array(fbe__xat, qfoo__qroz)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            fbe__xat, qfoo__qroz = array_getitem_slice_index(A, ind)
            return init_integer_array(fbe__xat, qfoo__qroz)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    lpsq__imom = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    gfvt__sgd = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if gfvt__sgd:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(lpsq__imom)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or gfvt__sgd):
        raise BodoError(lpsq__imom)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for IntegerArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_int_arr_len(A):
    if isinstance(A, IntegerArrayType):
        return lambda A: len(A._data)


@overload_attribute(IntegerArrayType, 'shape')
def overload_int_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(IntegerArrayType, 'dtype')
def overload_int_arr_dtype(A):
    dtype_class = getattr(pd, '{}Int{}Dtype'.format('' if A.dtype.signed else
        'U', A.dtype.bitwidth))
    return lambda A: dtype_class()


@overload_attribute(IntegerArrayType, 'ndim')
def overload_int_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntegerArrayType, 'nbytes')
def int_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(IntegerArrayType, 'copy', no_unliteral=True)
def overload_int_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.int_arr_ext.init_integer_array(
            bodo.libs.int_arr_ext.get_int_arr_data(A).copy(), bodo.libs.
            int_arr_ext.get_int_arr_bitmap(A).copy())


@overload_method(IntegerArrayType, 'astype', no_unliteral=True)
def overload_int_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "IntegerArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, IntDtype) and A.dtype == dtype.dtype:
        if is_overload_false(copy):
            return lambda A, dtype, copy=True: A
        elif is_overload_true(copy):
            return lambda A, dtype, copy=True: A.copy()
        else:

            def impl(A, dtype, copy=True):
                if copy:
                    return A.copy()
                else:
                    return A
            return impl
    if isinstance(dtype, IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.int_arr_ext.get_int_arr_data(A).
            astype(np_dtype), bodo.libs.int_arr_ext.get_int_arr_bitmap(A).
            copy()))
    nb_dtype = parse_dtype(dtype, 'IntegerArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.int_arr_ext.get_int_arr_data(A)
            n = len(data)
            szv__cgbr = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                szv__cgbr[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    szv__cgbr[i] = np.nan
            return szv__cgbr
        return impl_float
    return lambda A, dtype, copy=True: bodo.libs.int_arr_ext.get_int_arr_data(A
        ).astype(nb_dtype)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def apply_null_mask(arr, bitmap, mask_fill, inplace):
    assert isinstance(arr, types.Array)
    if isinstance(arr.dtype, types.Integer):
        if is_overload_none(inplace):
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap.copy()))
        else:
            return (lambda arr, bitmap, mask_fill, inplace: bodo.libs.
                int_arr_ext.init_integer_array(arr, bitmap))
    if isinstance(arr.dtype, types.Float):

        def impl(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = np.nan
            return arr
        return impl
    if arr.dtype == types.bool_:

        def impl_bool(arr, bitmap, mask_fill, inplace):
            n = len(arr)
            for i in numba.parfors.parfor.internal_prange(n):
                if not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bitmap, i):
                    arr[i] = mask_fill
            return arr
        return impl_bool
    return lambda arr, bitmap, mask_fill, inplace: arr


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def merge_bitmaps(B1, B2, n, inplace):
    assert B1 == types.Array(types.uint8, 1, 'C')
    assert B2 == types.Array(types.uint8, 1, 'C')
    if not is_overload_none(inplace):

        def impl_inplace(B1, B2, n, inplace):
            for i in numba.parfors.parfor.internal_prange(n):
                vajz__ogi = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                undmm__lfwnk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                rukdt__urps = vajz__ogi & undmm__lfwnk
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, rukdt__urps)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        jpo__skl = n + 7 >> 3
        szv__cgbr = np.empty(jpo__skl, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            vajz__ogi = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            undmm__lfwnk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            rukdt__urps = vajz__ogi & undmm__lfwnk
            bodo.libs.int_arr_ext.set_bit_to_arr(szv__cgbr, i, rukdt__urps)
        return szv__cgbr
    return impl


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_int_arr_op_nin_1(A):
            if isinstance(A, IntegerArrayType):
                return get_nullable_array_unary_impl(op, A)
        return overload_int_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
                IntegerArrayType):
                return get_nullable_array_binary_impl(op, lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for lma__gwy in numba.np.ufunc_db.get_ufuncs():
        jhoyo__rxni = create_op_overload(lma__gwy, lma__gwy.nin)
        overload(lma__gwy, no_unliteral=True)(jhoyo__rxni)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        jhoyo__rxni = create_op_overload(op, 2)
        overload(op)(jhoyo__rxni)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        jhoyo__rxni = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(jhoyo__rxni)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        jhoyo__rxni = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(jhoyo__rxni)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    bpu__yjkud = len(arrs.types)
    xpnh__ueg = 'def f(arrs):\n'
    vnc__moe = ', '.join('arrs[{}]._data'.format(i) for i in range(bpu__yjkud))
    xpnh__ueg += '  return ({}{})\n'.format(vnc__moe, ',' if bpu__yjkud == 
        1 else '')
    uim__lxtax = {}
    exec(xpnh__ueg, {}, uim__lxtax)
    impl = uim__lxtax['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    bpu__yjkud = len(arrs.types)
    rzx__hzk = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        bpu__yjkud))
    xpnh__ueg = 'def f(arrs):\n'
    xpnh__ueg += '  n = {}\n'.format(rzx__hzk)
    xpnh__ueg += '  n_bytes = (n + 7) >> 3\n'
    xpnh__ueg += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    xpnh__ueg += '  curr_bit = 0\n'
    for i in range(bpu__yjkud):
        xpnh__ueg += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        xpnh__ueg += '  for j in range(len(arrs[{}])):\n'.format(i)
        xpnh__ueg += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        xpnh__ueg += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        xpnh__ueg += '    curr_bit += 1\n'
    xpnh__ueg += '  return new_mask\n'
    uim__lxtax = {}
    exec(xpnh__ueg, {'np': np, 'bodo': bodo}, uim__lxtax)
    impl = uim__lxtax['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    pchr__djdo = dict(skipna=skipna, min_count=min_count)
    xgxfy__rbgje = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', pchr__djdo, xgxfy__rbgje)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0
        for i in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, i):
                val = A[i]
            s += val
        return s
    return impl


@overload_method(IntegerArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_int_arr(A):
        data = []
        hcgh__wkzi = []
        ail__megai = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not ail__megai:
                    data.append(dtype(1))
                    hcgh__wkzi.append(False)
                    ail__megai = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                hcgh__wkzi.append(True)
        fbe__xat = np.array(data)
        n = len(fbe__xat)
        jpo__skl = n + 7 >> 3
        qfoo__qroz = np.empty(jpo__skl, np.uint8)
        for ctkhn__iwpp in range(n):
            set_bit_to_arr(qfoo__qroz, ctkhn__iwpp, hcgh__wkzi[ctkhn__iwpp])
        return init_integer_array(fbe__xat, qfoo__qroz)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    wkyhd__zzfy = numba.core.registry.cpu_target.typing_context
    kge__amhs = wkyhd__zzfy.resolve_function_type(op, (types.Array(A.dtype,
        1, 'C'),), {}).return_type
    kge__amhs = to_nullable_type(kge__amhs)

    def impl(A):
        n = len(A)
        bjb__qqf = bodo.utils.utils.alloc_type(n, kge__amhs, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(bjb__qqf, i)
                continue
            bjb__qqf[i] = op(A[i])
        return bjb__qqf
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    pqz__dkny = isinstance(lhs, (types.Number, types.Boolean))
    asveq__bsyfh = isinstance(rhs, (types.Number, types.Boolean))
    bhzl__nxmo = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    dydw__kqemp = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    wkyhd__zzfy = numba.core.registry.cpu_target.typing_context
    kge__amhs = wkyhd__zzfy.resolve_function_type(op, (bhzl__nxmo,
        dydw__kqemp), {}).return_type
    kge__amhs = to_nullable_type(kge__amhs)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    ment__ojesm = 'lhs' if pqz__dkny else 'lhs[i]'
    comrz__eoyd = 'rhs' if asveq__bsyfh else 'rhs[i]'
    jjnq__rehk = ('False' if pqz__dkny else
        'bodo.libs.array_kernels.isna(lhs, i)')
    szmy__vvsn = ('False' if asveq__bsyfh else
        'bodo.libs.array_kernels.isna(rhs, i)')
    xpnh__ueg = 'def impl(lhs, rhs):\n'
    xpnh__ueg += '  n = len({})\n'.format('lhs' if not pqz__dkny else 'rhs')
    if inplace:
        xpnh__ueg += '  out_arr = {}\n'.format('lhs' if not pqz__dkny else
            'rhs')
    else:
        xpnh__ueg += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    xpnh__ueg += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    xpnh__ueg += '    if ({}\n'.format(jjnq__rehk)
    xpnh__ueg += '        or {}):\n'.format(szmy__vvsn)
    xpnh__ueg += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    xpnh__ueg += '      continue\n'
    xpnh__ueg += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(ment__ojesm, comrz__eoyd))
    xpnh__ueg += '  return out_arr\n'
    uim__lxtax = {}
    exec(xpnh__ueg, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        kge__amhs, 'op': op}, uim__lxtax)
    impl = uim__lxtax['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        pqz__dkny = lhs in [pd_timedelta_type]
        asveq__bsyfh = rhs in [pd_timedelta_type]
        if pqz__dkny:

            def impl(lhs, rhs):
                n = len(rhs)
                bjb__qqf = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(bjb__qqf, i)
                        continue
                    bjb__qqf[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return bjb__qqf
            return impl
        elif asveq__bsyfh:

            def impl(lhs, rhs):
                n = len(lhs)
                bjb__qqf = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(bjb__qqf, i)
                        continue
                    bjb__qqf[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return bjb__qqf
            return impl
    return impl
