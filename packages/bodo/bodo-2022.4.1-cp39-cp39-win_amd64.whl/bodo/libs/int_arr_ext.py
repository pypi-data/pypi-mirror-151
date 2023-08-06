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
        uau__igebh = int(np.log2(self.dtype.bitwidth // 8))
        kqv__gwmxs = 0 if self.dtype.signed else 4
        idx = uau__igebh + kqv__gwmxs
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ascjs__daa = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, ascjs__daa)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    vrict__cmpc = 8 * val.dtype.itemsize
    ehsvk__wwry = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(ehsvk__wwry, vrict__cmpc))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        jeqm__plpug = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(jeqm__plpug)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    elct__waio = c.context.insert_const_string(c.builder.module, 'pandas')
    hfx__czbn = c.pyapi.import_module_noblock(elct__waio)
    kbew__iukuh = c.pyapi.call_method(hfx__czbn, str(typ)[:-2], ())
    c.pyapi.decref(hfx__czbn)
    return kbew__iukuh


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    vrict__cmpc = 8 * val.itemsize
    ehsvk__wwry = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(ehsvk__wwry, vrict__cmpc))
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
    drmpb__vbb = n + 7 >> 3
    ztzq__haw = np.empty(drmpb__vbb, np.uint8)
    for i in range(n):
        vycub__hnnkl = i // 8
        ztzq__haw[vycub__hnnkl] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            ztzq__haw[vycub__hnnkl]) & kBitmask[i % 8]
    return ztzq__haw


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    anzjq__ncyvr = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(anzjq__ncyvr)
    c.pyapi.decref(anzjq__ncyvr)
    xwwth__fzci = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    drmpb__vbb = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    uuwqc__uiom = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [drmpb__vbb])
    fai__vbq = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()])
    wxiy__ing = cgutils.get_or_insert_function(c.builder.module, fai__vbq,
        name='is_pd_int_array')
    ecpgj__dzwaw = c.builder.call(wxiy__ing, [obj])
    tbx__gml = c.builder.icmp_unsigned('!=', ecpgj__dzwaw, ecpgj__dzwaw.type(0)
        )
    with c.builder.if_else(tbx__gml) as (qgyx__rhh, vwxlc__lbky):
        with qgyx__rhh:
            owpch__sdv = c.pyapi.object_getattr_string(obj, '_data')
            xwwth__fzci.data = c.pyapi.to_native_value(types.Array(typ.
                dtype, 1, 'C'), owpch__sdv).value
            nhs__ufi = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), nhs__ufi).value
            c.pyapi.decref(owpch__sdv)
            c.pyapi.decref(nhs__ufi)
            vean__zkmn = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, mask_arr)
            fai__vbq = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            wxiy__ing = cgutils.get_or_insert_function(c.builder.module,
                fai__vbq, name='mask_arr_to_bitmap')
            c.builder.call(wxiy__ing, [uuwqc__uiom.data, vean__zkmn.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with vwxlc__lbky:
            elsnu__dvius = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            fai__vbq = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            ykrt__bpfmj = cgutils.get_or_insert_function(c.builder.module,
                fai__vbq, name='int_array_from_sequence')
            c.builder.call(ykrt__bpfmj, [obj, c.builder.bitcast(
                elsnu__dvius.data, lir.IntType(8).as_pointer()),
                uuwqc__uiom.data])
            xwwth__fzci.data = elsnu__dvius._getvalue()
    xwwth__fzci.null_bitmap = uuwqc__uiom._getvalue()
    ubwke__mjbik = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xwwth__fzci._getvalue(), is_error=ubwke__mjbik)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    xwwth__fzci = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        xwwth__fzci.data, c.env_manager)
    nocd__calnj = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, xwwth__fzci.null_bitmap).data
    anzjq__ncyvr = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(anzjq__ncyvr)
    elct__waio = c.context.insert_const_string(c.builder.module, 'numpy')
    pra__ktzgj = c.pyapi.import_module_noblock(elct__waio)
    ssx__jqthw = c.pyapi.object_getattr_string(pra__ktzgj, 'bool_')
    mask_arr = c.pyapi.call_method(pra__ktzgj, 'empty', (anzjq__ncyvr,
        ssx__jqthw))
    ptrym__okj = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    mogs__hgm = c.pyapi.object_getattr_string(ptrym__okj, 'data')
    uoq__qcpvn = c.builder.inttoptr(c.pyapi.long_as_longlong(mogs__hgm),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as vovby__iiy:
        i = vovby__iiy.index
        fyve__egre = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        mks__rshx = c.builder.load(cgutils.gep(c.builder, nocd__calnj,
            fyve__egre))
        cdc__hamwn = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(mks__rshx, cdc__hamwn), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        yauk__ivly = cgutils.gep(c.builder, uoq__qcpvn, i)
        c.builder.store(val, yauk__ivly)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        xwwth__fzci.null_bitmap)
    elct__waio = c.context.insert_const_string(c.builder.module, 'pandas')
    hfx__czbn = c.pyapi.import_module_noblock(elct__waio)
    uborc__etcf = c.pyapi.object_getattr_string(hfx__czbn, 'arrays')
    kbew__iukuh = c.pyapi.call_method(uborc__etcf, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(hfx__czbn)
    c.pyapi.decref(anzjq__ncyvr)
    c.pyapi.decref(pra__ktzgj)
    c.pyapi.decref(ssx__jqthw)
    c.pyapi.decref(ptrym__okj)
    c.pyapi.decref(mogs__hgm)
    c.pyapi.decref(uborc__etcf)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return kbew__iukuh


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        vin__prvy, suigk__kumpo = args
        xwwth__fzci = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        xwwth__fzci.data = vin__prvy
        xwwth__fzci.null_bitmap = suigk__kumpo
        context.nrt.incref(builder, signature.args[0], vin__prvy)
        context.nrt.incref(builder, signature.args[1], suigk__kumpo)
        return xwwth__fzci._getvalue()
    fib__osqzz = IntegerArrayType(data.dtype)
    wfl__uks = fib__osqzz(data, null_bitmap)
    return wfl__uks, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    jynd__oxrch = np.empty(n, pyval.dtype.type)
    ssua__jyxi = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        suwiy__jdg = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ssua__jyxi, i, int(not suwiy__jdg)
            )
        if not suwiy__jdg:
            jynd__oxrch[i] = s
    nvow__tse = context.get_constant_generic(builder, types.Array(typ.dtype,
        1, 'C'), jynd__oxrch)
    cxp__cbbyb = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), ssua__jyxi)
    return lir.Constant.literal_struct([nvow__tse, cxp__cbbyb])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    zlza__bien = args[0]
    if equiv_set.has_shape(zlza__bien):
        return ArrayAnalysis.AnalyzeResult(shape=zlza__bien, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    zlza__bien = args[0]
    if equiv_set.has_shape(zlza__bien):
        return ArrayAnalysis.AnalyzeResult(shape=zlza__bien, pre=[])
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
    jynd__oxrch = np.empty(n, dtype)
    npi__hkxnf = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(jynd__oxrch, npi__hkxnf)


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
            uoay__zdhkl, oqo__cugjq = array_getitem_bool_index(A, ind)
            return init_integer_array(uoay__zdhkl, oqo__cugjq)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            uoay__zdhkl, oqo__cugjq = array_getitem_int_index(A, ind)
            return init_integer_array(uoay__zdhkl, oqo__cugjq)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            uoay__zdhkl, oqo__cugjq = array_getitem_slice_index(A, ind)
            return init_integer_array(uoay__zdhkl, oqo__cugjq)
        return impl_slice
    raise BodoError(
        f'getitem for IntegerArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    djn__kwqn = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    poj__qthap = isinstance(val, (types.Integer, types.Boolean))
    if isinstance(idx, types.Integer):
        if poj__qthap:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(djn__kwqn)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or poj__qthap):
        raise BodoError(djn__kwqn)
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
            ttyjx__qmd = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                ttyjx__qmd[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    ttyjx__qmd[i] = np.nan
            return ttyjx__qmd
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
                irgnf__pcdb = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
                zwcy__dlnqk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
                getbl__teh = irgnf__pcdb & zwcy__dlnqk
                bodo.libs.int_arr_ext.set_bit_to_arr(B1, i, getbl__teh)
            return B1
        return impl_inplace

    def impl(B1, B2, n, inplace):
        numba.parfors.parfor.init_prange()
        drmpb__vbb = n + 7 >> 3
        ttyjx__qmd = np.empty(drmpb__vbb, np.uint8)
        for i in numba.parfors.parfor.internal_prange(n):
            irgnf__pcdb = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B1, i)
            zwcy__dlnqk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(B2, i)
            getbl__teh = irgnf__pcdb & zwcy__dlnqk
            bodo.libs.int_arr_ext.set_bit_to_arr(ttyjx__qmd, i, getbl__teh)
        return ttyjx__qmd
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
    for fhtau__gmhuo in numba.np.ufunc_db.get_ufuncs():
        ejjs__pvxjc = create_op_overload(fhtau__gmhuo, fhtau__gmhuo.nin)
        overload(fhtau__gmhuo, no_unliteral=True)(ejjs__pvxjc)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        ejjs__pvxjc = create_op_overload(op, 2)
        overload(op)(ejjs__pvxjc)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        ejjs__pvxjc = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(ejjs__pvxjc)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        ejjs__pvxjc = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(ejjs__pvxjc)


_install_unary_ops()


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data_tup(arrs):
    qam__pdsi = len(arrs.types)
    gyg__rxs = 'def f(arrs):\n'
    kbew__iukuh = ', '.join('arrs[{}]._data'.format(i) for i in range(
        qam__pdsi))
    gyg__rxs += '  return ({}{})\n'.format(kbew__iukuh, ',' if qam__pdsi ==
        1 else '')
    odpbp__kot = {}
    exec(gyg__rxs, {}, odpbp__kot)
    impl = odpbp__kot['f']
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def concat_bitmap_tup(arrs):
    qam__pdsi = len(arrs.types)
    rwhga__asj = '+'.join('len(arrs[{}]._data)'.format(i) for i in range(
        qam__pdsi))
    gyg__rxs = 'def f(arrs):\n'
    gyg__rxs += '  n = {}\n'.format(rwhga__asj)
    gyg__rxs += '  n_bytes = (n + 7) >> 3\n'
    gyg__rxs += '  new_mask = np.empty(n_bytes, np.uint8)\n'
    gyg__rxs += '  curr_bit = 0\n'
    for i in range(qam__pdsi):
        gyg__rxs += '  old_mask = arrs[{}]._null_bitmap\n'.format(i)
        gyg__rxs += '  for j in range(len(arrs[{}])):\n'.format(i)
        gyg__rxs += (
            '    bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        gyg__rxs += (
            '    bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        gyg__rxs += '    curr_bit += 1\n'
    gyg__rxs += '  return new_mask\n'
    odpbp__kot = {}
    exec(gyg__rxs, {'np': np, 'bodo': bodo}, odpbp__kot)
    impl = odpbp__kot['f']
    return impl


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    kilvd__ueog = dict(skipna=skipna, min_count=min_count)
    sgy__osd = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', kilvd__ueog, sgy__osd)

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
        cdc__hamwn = []
        ompa__pqq = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not ompa__pqq:
                    data.append(dtype(1))
                    cdc__hamwn.append(False)
                    ompa__pqq = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                cdc__hamwn.append(True)
        uoay__zdhkl = np.array(data)
        n = len(uoay__zdhkl)
        drmpb__vbb = n + 7 >> 3
        oqo__cugjq = np.empty(drmpb__vbb, np.uint8)
        for ryhy__vupk in range(n):
            set_bit_to_arr(oqo__cugjq, ryhy__vupk, cdc__hamwn[ryhy__vupk])
        return init_integer_array(uoay__zdhkl, oqo__cugjq)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    nxdin__wmup = numba.core.registry.cpu_target.typing_context
    efl__kcep = nxdin__wmup.resolve_function_type(op, (types.Array(A.dtype,
        1, 'C'),), {}).return_type
    efl__kcep = to_nullable_type(efl__kcep)

    def impl(A):
        n = len(A)
        tqerz__rhb = bodo.utils.utils.alloc_type(n, efl__kcep, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(tqerz__rhb, i)
                continue
            tqerz__rhb[i] = op(A[i])
        return tqerz__rhb
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    inplace = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    suqr__rvvkw = isinstance(lhs, (types.Number, types.Boolean))
    wpu__eyclu = isinstance(rhs, (types.Number, types.Boolean))
    bnpjw__tgcck = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    wiz__aednc = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    nxdin__wmup = numba.core.registry.cpu_target.typing_context
    efl__kcep = nxdin__wmup.resolve_function_type(op, (bnpjw__tgcck,
        wiz__aednc), {}).return_type
    efl__kcep = to_nullable_type(efl__kcep)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    fnxq__cqmki = 'lhs' if suqr__rvvkw else 'lhs[i]'
    qdme__opjmo = 'rhs' if wpu__eyclu else 'rhs[i]'
    aqbaj__plm = ('False' if suqr__rvvkw else
        'bodo.libs.array_kernels.isna(lhs, i)')
    smp__gxr = ('False' if wpu__eyclu else
        'bodo.libs.array_kernels.isna(rhs, i)')
    gyg__rxs = 'def impl(lhs, rhs):\n'
    gyg__rxs += '  n = len({})\n'.format('lhs' if not suqr__rvvkw else 'rhs')
    if inplace:
        gyg__rxs += '  out_arr = {}\n'.format('lhs' if not suqr__rvvkw else
            'rhs')
    else:
        gyg__rxs += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    gyg__rxs += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    gyg__rxs += '    if ({}\n'.format(aqbaj__plm)
    gyg__rxs += '        or {}):\n'.format(smp__gxr)
    gyg__rxs += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    gyg__rxs += '      continue\n'
    gyg__rxs += (
        '    out_arr[i] = bodo.utils.conversion.unbox_if_timestamp(op({}, {}))\n'
        .format(fnxq__cqmki, qdme__opjmo))
    gyg__rxs += '  return out_arr\n'
    odpbp__kot = {}
    exec(gyg__rxs, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        efl__kcep, 'op': op}, odpbp__kot)
    impl = odpbp__kot['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        suqr__rvvkw = lhs in [pd_timedelta_type]
        wpu__eyclu = rhs in [pd_timedelta_type]
        if suqr__rvvkw:

            def impl(lhs, rhs):
                n = len(rhs)
                tqerz__rhb = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(tqerz__rhb, i)
                        continue
                    tqerz__rhb[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs, rhs[i]))
                return tqerz__rhb
            return impl
        elif wpu__eyclu:

            def impl(lhs, rhs):
                n = len(lhs)
                tqerz__rhb = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(tqerz__rhb, i)
                        continue
                    tqerz__rhb[i] = bodo.utils.conversion.unbox_if_timestamp(op
                        (lhs[i], rhs))
                return tqerz__rhb
            return impl
    return impl
