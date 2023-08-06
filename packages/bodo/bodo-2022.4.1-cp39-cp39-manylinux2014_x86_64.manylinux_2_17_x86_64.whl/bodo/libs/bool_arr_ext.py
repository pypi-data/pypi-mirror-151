"""Nullable boolean array that stores data in Numpy format (1 byte per value)
but nulls are stored in bit arrays (1 bit per value) similar to Arrow's nulls.
Pandas converts boolean array to object when NAs are introduced.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import is_list_like_index_type
ll.add_symbol('is_bool_array', hstr_ext.is_bool_array)
ll.add_symbol('is_pd_boolean_array', hstr_ext.is_pd_boolean_array)
ll.add_symbol('unbox_bool_array_obj', hstr_ext.unbox_bool_array_obj)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_overload_false, is_overload_true, parse_dtype, raise_bodo_error


class BooleanArrayType(types.ArrayCompatible):

    def __init__(self):
        super(BooleanArrayType, self).__init__(name='BooleanArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.bool_

    def copy(self):
        return BooleanArrayType()


boolean_array = BooleanArrayType()


@typeof_impl.register(pd.arrays.BooleanArray)
def typeof_boolean_array(val, c):
    return boolean_array


data_type = types.Array(types.bool_, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(BooleanArrayType)
class BooleanArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        usez__bcxto = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, usez__bcxto)


make_attribute_wrapper(BooleanArrayType, 'data', '_data')
make_attribute_wrapper(BooleanArrayType, 'null_bitmap', '_null_bitmap')


class BooleanDtype(types.Number):

    def __init__(self):
        self.dtype = types.bool_
        super(BooleanDtype, self).__init__('BooleanDtype')


boolean_dtype = BooleanDtype()
register_model(BooleanDtype)(models.OpaqueModel)


@box(BooleanDtype)
def box_boolean_dtype(typ, val, c):
    rnuk__hkzav = c.context.insert_const_string(c.builder.module, 'pandas')
    fxql__heon = c.pyapi.import_module_noblock(rnuk__hkzav)
    gnjkk__ysjoj = c.pyapi.call_method(fxql__heon, 'BooleanDtype', ())
    c.pyapi.decref(fxql__heon)
    return gnjkk__ysjoj


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    eacsd__uwujl = n + 7 >> 3
    return np.full(eacsd__uwujl, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    fti__jzxq = c.context.typing_context.resolve_value_type(func)
    vbgs__bovgf = fti__jzxq.get_call_type(c.context.typing_context,
        arg_typs, {})
    jmvo__xsels = c.context.get_function(fti__jzxq, vbgs__bovgf)
    fie__shuf = c.context.call_conv.get_function_type(vbgs__bovgf.
        return_type, vbgs__bovgf.args)
    wsacy__nhsw = c.builder.module
    wtdnl__dbzf = lir.Function(wsacy__nhsw, fie__shuf, name=wsacy__nhsw.
        get_unique_name('.func_conv'))
    wtdnl__dbzf.linkage = 'internal'
    syjxv__nzef = lir.IRBuilder(wtdnl__dbzf.append_basic_block())
    izgm__nonom = c.context.call_conv.decode_arguments(syjxv__nzef,
        vbgs__bovgf.args, wtdnl__dbzf)
    fcsry__oiooa = jmvo__xsels(syjxv__nzef, izgm__nonom)
    c.context.call_conv.return_value(syjxv__nzef, fcsry__oiooa)
    vrykd__cigg, psxgm__bwsk = c.context.call_conv.call_function(c.builder,
        wtdnl__dbzf, vbgs__bovgf.return_type, vbgs__bovgf.args, args)
    return psxgm__bwsk


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    tduf__edk = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(tduf__edk)
    c.pyapi.decref(tduf__edk)
    fie__shuf = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    hkbsg__kqzvn = cgutils.get_or_insert_function(c.builder.module,
        fie__shuf, name='is_bool_array')
    fie__shuf = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    wtdnl__dbzf = cgutils.get_or_insert_function(c.builder.module,
        fie__shuf, name='is_pd_boolean_array')
    sbyvb__iej = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vvw__pnvif = c.builder.call(wtdnl__dbzf, [obj])
    asm__nhw = c.builder.icmp_unsigned('!=', vvw__pnvif, vvw__pnvif.type(0))
    with c.builder.if_else(asm__nhw) as (uiqtz__sntr, nbcug__dek):
        with uiqtz__sntr:
            xiqn__cwszh = c.pyapi.object_getattr_string(obj, '_data')
            sbyvb__iej.data = c.pyapi.to_native_value(types.Array(types.
                bool_, 1, 'C'), xiqn__cwszh).value
            sext__zxelj = c.pyapi.object_getattr_string(obj, '_mask')
            qwn__xeu = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), sext__zxelj).value
            eacsd__uwujl = c.builder.udiv(c.builder.add(n, lir.Constant(lir
                .IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            lfb__pnp = c.context.make_array(types.Array(types.bool_, 1, 'C'))(c
                .context, c.builder, qwn__xeu)
            yicmn__ixwjr = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [eacsd__uwujl])
            fie__shuf = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            wtdnl__dbzf = cgutils.get_or_insert_function(c.builder.module,
                fie__shuf, name='mask_arr_to_bitmap')
            c.builder.call(wtdnl__dbzf, [yicmn__ixwjr.data, lfb__pnp.data, n])
            sbyvb__iej.null_bitmap = yicmn__ixwjr._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), qwn__xeu)
            c.pyapi.decref(xiqn__cwszh)
            c.pyapi.decref(sext__zxelj)
        with nbcug__dek:
            uswuv__uumss = c.builder.call(hkbsg__kqzvn, [obj])
            ibdl__lvz = c.builder.icmp_unsigned('!=', uswuv__uumss,
                uswuv__uumss.type(0))
            with c.builder.if_else(ibdl__lvz) as (fnqy__axkf, brihd__blsvn):
                with fnqy__axkf:
                    sbyvb__iej.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    sbyvb__iej.null_bitmap = call_func_in_unbox(gen_full_bitmap
                        , (n,), (types.int64,), c)
                with brihd__blsvn:
                    sbyvb__iej.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    eacsd__uwujl = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    sbyvb__iej.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [eacsd__uwujl])._getvalue()
                    csn__hxtzl = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, sbyvb__iej.data
                        ).data
                    qrby__ceqa = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, sbyvb__iej.
                        null_bitmap).data
                    fie__shuf = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    wtdnl__dbzf = cgutils.get_or_insert_function(c.builder.
                        module, fie__shuf, name='unbox_bool_array_obj')
                    c.builder.call(wtdnl__dbzf, [obj, csn__hxtzl,
                        qrby__ceqa, n])
    return NativeValue(sbyvb__iej._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    sbyvb__iej = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        sbyvb__iej.data, c.env_manager)
    ghkg__dzph = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, sbyvb__iej.null_bitmap).data
    tduf__edk = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(tduf__edk)
    rnuk__hkzav = c.context.insert_const_string(c.builder.module, 'numpy')
    fpn__vwngi = c.pyapi.import_module_noblock(rnuk__hkzav)
    kbgg__stwf = c.pyapi.object_getattr_string(fpn__vwngi, 'bool_')
    qwn__xeu = c.pyapi.call_method(fpn__vwngi, 'empty', (tduf__edk, kbgg__stwf)
        )
    mivcq__bnbk = c.pyapi.object_getattr_string(qwn__xeu, 'ctypes')
    yhtjw__dozs = c.pyapi.object_getattr_string(mivcq__bnbk, 'data')
    gsx__utw = c.builder.inttoptr(c.pyapi.long_as_longlong(yhtjw__dozs),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as picsf__ivc:
        lrwe__ifna = picsf__ivc.index
        sxegb__xpvg = c.builder.lshr(lrwe__ifna, lir.Constant(lir.IntType(
            64), 3))
        gsevw__ohp = c.builder.load(cgutils.gep(c.builder, ghkg__dzph,
            sxegb__xpvg))
        fwy__aiaht = c.builder.trunc(c.builder.and_(lrwe__ifna, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(gsevw__ohp, fwy__aiaht), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        tmpvb__hwcop = cgutils.gep(c.builder, gsx__utw, lrwe__ifna)
        c.builder.store(val, tmpvb__hwcop)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        sbyvb__iej.null_bitmap)
    rnuk__hkzav = c.context.insert_const_string(c.builder.module, 'pandas')
    fxql__heon = c.pyapi.import_module_noblock(rnuk__hkzav)
    vkur__qijz = c.pyapi.object_getattr_string(fxql__heon, 'arrays')
    gnjkk__ysjoj = c.pyapi.call_method(vkur__qijz, 'BooleanArray', (data,
        qwn__xeu))
    c.pyapi.decref(fxql__heon)
    c.pyapi.decref(tduf__edk)
    c.pyapi.decref(fpn__vwngi)
    c.pyapi.decref(kbgg__stwf)
    c.pyapi.decref(mivcq__bnbk)
    c.pyapi.decref(yhtjw__dozs)
    c.pyapi.decref(vkur__qijz)
    c.pyapi.decref(data)
    c.pyapi.decref(qwn__xeu)
    return gnjkk__ysjoj


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    auitd__zcl = np.empty(n, np.bool_)
    lbgo__ycsv = np.empty(n + 7 >> 3, np.uint8)
    for lrwe__ifna, s in enumerate(pyval):
        tsow__grtod = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(lbgo__ycsv, lrwe__ifna, int(
            not tsow__grtod))
        if not tsow__grtod:
            auitd__zcl[lrwe__ifna] = s
    dwtal__fmf = context.get_constant_generic(builder, data_type, auitd__zcl)
    qxv__hxk = context.get_constant_generic(builder, nulls_type, lbgo__ycsv)
    return lir.Constant.literal_struct([dwtal__fmf, qxv__hxk])


def lower_init_bool_array(context, builder, signature, args):
    zvt__vujdj, vro__cgc = args
    sbyvb__iej = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    sbyvb__iej.data = zvt__vujdj
    sbyvb__iej.null_bitmap = vro__cgc
    context.nrt.incref(builder, signature.args[0], zvt__vujdj)
    context.nrt.incref(builder, signature.args[1], vro__cgc)
    return sbyvb__iej._getvalue()


@intrinsic
def init_bool_array(typingctx, data, null_bitmap=None):
    assert data == types.Array(types.bool_, 1, 'C')
    assert null_bitmap == types.Array(types.uint8, 1, 'C')
    sig = boolean_array(data, null_bitmap)
    return sig, lower_init_bool_array


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_bool_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    zerx__rrtql = args[0]
    if equiv_set.has_shape(zerx__rrtql):
        return ArrayAnalysis.AnalyzeResult(shape=zerx__rrtql, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    zerx__rrtql = args[0]
    if equiv_set.has_shape(zerx__rrtql):
        return ArrayAnalysis.AnalyzeResult(shape=zerx__rrtql, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_init_bool_array = (
    init_bool_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_bool_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_bool_array',
    'bodo.libs.bool_arr_ext'] = alias_ext_init_bool_array
numba.core.ir_utils.alias_func_extensions['get_bool_arr_data',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_bool_arr_bitmap',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_bool_array(n):
    auitd__zcl = np.empty(n, dtype=np.bool_)
    cnqjz__gfwtw = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(auitd__zcl, cnqjz__gfwtw)


def alloc_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_alloc_bool_array = (
    alloc_bool_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def bool_arr_getitem(A, ind):
    if A != boolean_array:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: A._data[ind]
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            dxj__aul, labmo__bvnic = array_getitem_bool_index(A, ind)
            return init_bool_array(dxj__aul, labmo__bvnic)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            dxj__aul, labmo__bvnic = array_getitem_int_index(A, ind)
            return init_bool_array(dxj__aul, labmo__bvnic)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            dxj__aul, labmo__bvnic = array_getitem_slice_index(A, ind)
            return init_bool_array(dxj__aul, labmo__bvnic)
        return impl_slice
    raise BodoError(
        f'getitem for BooleanArray with indexing type {ind} not supported.')


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    wgg__fbw = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(wgg__fbw)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(wgg__fbw)
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
        f'setitem for BooleanArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_bool_arr_len(A):
    if A == boolean_array:
        return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'shape')
def overload_bool_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(BooleanArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: pd.BooleanDtype()


@overload_attribute(BooleanArrayType, 'ndim')
def overload_bool_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BooleanArrayType, 'nbytes')
def bool_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(BooleanArrayType, 'copy', no_unliteral=True)
def overload_bool_arr_copy(A):
    return lambda A: bodo.libs.bool_arr_ext.init_bool_array(bodo.libs.
        bool_arr_ext.get_bool_arr_data(A).copy(), bodo.libs.bool_arr_ext.
        get_bool_arr_bitmap(A).copy())


@overload_method(BooleanArrayType, 'sum', no_unliteral=True, inline='always')
def overload_bool_sum(A):

    def impl(A):
        numba.parfors.parfor.init_prange()
        s = 0
        for lrwe__ifna in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, lrwe__ifna):
                val = A[lrwe__ifna]
            s += val
        return s
    return impl


@overload_method(BooleanArrayType, 'astype', no_unliteral=True)
def overload_bool_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "BooleanArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if dtype == types.bool_:
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
    nb_dtype = parse_dtype(dtype, 'BooleanArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
            n = len(data)
            mphve__ddw = np.empty(n, nb_dtype)
            for lrwe__ifna in numba.parfors.parfor.internal_prange(n):
                mphve__ddw[lrwe__ifna] = data[lrwe__ifna]
                if bodo.libs.array_kernels.isna(A, lrwe__ifna):
                    mphve__ddw[lrwe__ifna] = np.nan
            return mphve__ddw
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload(str, no_unliteral=True)
def overload_str_bool(val):
    if val == types.bool_:

        def impl(val):
            if val:
                return 'True'
            return 'False'
        return impl


ufunc_aliases = {'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    tzhj__uxee = op.__name__
    tzhj__uxee = ufunc_aliases.get(tzhj__uxee, tzhj__uxee)
    if n_inputs == 1:

        def overload_bool_arr_op_nin_1(A):
            if isinstance(A, BooleanArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_bool_arr_op_nin_1
    elif n_inputs == 2:

        def overload_bool_arr_op_nin_2(lhs, rhs):
            if lhs == boolean_array or rhs == boolean_array:
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_bool_arr_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for jcti__nso in numba.np.ufunc_db.get_ufuncs():
        qsbp__njtyh = create_op_overload(jcti__nso, jcti__nso.nin)
        overload(jcti__nso, no_unliteral=True)(qsbp__njtyh)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        qsbp__njtyh = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(qsbp__njtyh)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        qsbp__njtyh = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(qsbp__njtyh)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        qsbp__njtyh = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(qsbp__njtyh)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        fwy__aiaht = []
        aro__ivlhs = False
        ymq__fmoo = False
        glj__neq = False
        for lrwe__ifna in range(len(A)):
            if bodo.libs.array_kernels.isna(A, lrwe__ifna):
                if not aro__ivlhs:
                    data.append(False)
                    fwy__aiaht.append(False)
                    aro__ivlhs = True
                continue
            val = A[lrwe__ifna]
            if val and not ymq__fmoo:
                data.append(True)
                fwy__aiaht.append(True)
                ymq__fmoo = True
            if not val and not glj__neq:
                data.append(False)
                fwy__aiaht.append(True)
                glj__neq = True
            if aro__ivlhs and ymq__fmoo and glj__neq:
                break
        dxj__aul = np.array(data)
        n = len(dxj__aul)
        eacsd__uwujl = 1
        labmo__bvnic = np.empty(eacsd__uwujl, np.uint8)
        for zpr__yyccz in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(labmo__bvnic, zpr__yyccz,
                fwy__aiaht[zpr__yyccz])
        return init_bool_array(dxj__aul, labmo__bvnic)
    return impl_bool_arr


@overload(operator.getitem, no_unliteral=True)
def bool_arr_ind_getitem(A, ind):
    if ind == boolean_array and (isinstance(A, (types.Array, bodo.libs.
        int_arr_ext.IntegerArrayType)) or isinstance(A, bodo.libs.
        struct_arr_ext.StructArrayType) or isinstance(A, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType) or isinstance(A, bodo.libs.
        map_arr_ext.MapArrayType) or A in (string_array_type, bodo.hiframes
        .split_impl.string_array_split_view_type, boolean_array)):
        return lambda A, ind: A[ind._data]


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    gnjkk__ysjoj = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, gnjkk__ysjoj)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    ecdcn__qogdf = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        elkc__dvxjt = bodo.utils.utils.is_array_typ(val1, False)
        xhq__bmeg = bodo.utils.utils.is_array_typ(val2, False)
        fvifm__bkoj = 'val1' if elkc__dvxjt else 'val2'
        vej__dpv = 'def impl(val1, val2):\n'
        vej__dpv += f'  n = len({fvifm__bkoj})\n'
        vej__dpv += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        vej__dpv += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if elkc__dvxjt:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            zgphi__kwahu = 'val1[i]'
        else:
            null1 = 'False\n'
            zgphi__kwahu = 'val1'
        if xhq__bmeg:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            glutn__juym = 'val2[i]'
        else:
            null2 = 'False\n'
            glutn__juym = 'val2'
        if ecdcn__qogdf:
            vej__dpv += f"""    result, isna_val = compute_or_body({null1}, {null2}, {zgphi__kwahu}, {glutn__juym})
"""
        else:
            vej__dpv += f"""    result, isna_val = compute_and_body({null1}, {null2}, {zgphi__kwahu}, {glutn__juym})
"""
        vej__dpv += '    out_arr[i] = result\n'
        vej__dpv += '    if isna_val:\n'
        vej__dpv += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        vej__dpv += '      continue\n'
        vej__dpv += '  return out_arr\n'
        miz__oomy = {}
        exec(vej__dpv, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, miz__oomy)
        impl = miz__oomy['impl']
        return impl
    return bool_array_impl


def compute_or_body(null1, null2, val1, val2):
    pass


@overload(compute_or_body)
def overload_compute_or_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == False
        elif null2:
            return val1, val1 == False
        else:
            return val1 | val2, False
    return impl


def compute_and_body(null1, null2, val1, val2):
    pass


@overload(compute_and_body)
def overload_compute_and_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == True
        elif null2:
            return val1, val1 == True
        else:
            return val1 & val2, False
    return impl


def create_boolean_array_logical_lower_impl(op):

    def logical_lower_impl(context, builder, sig, args):
        impl = create_nullable_logical_op_overload(op)(*sig.args)
        return context.compile_internal(builder, impl, sig, args)
    return logical_lower_impl


class BooleanArrayLogicalOperatorTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        if not is_valid_boolean_array_logical_op(args[0], args[1]):
            return
        jzuvy__fmeen = boolean_array
        return jzuvy__fmeen(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    ujdd__wwwn = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return ujdd__wwwn


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        ryxm__tgi = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(ryxm__tgi)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(ryxm__tgi)


_install_nullable_logical_lowering()
