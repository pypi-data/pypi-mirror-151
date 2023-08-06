import enum
import operator
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.typing import NOT_CONSTANT, BodoError, MetaType, check_unsupported_args, dtype_to_array_type, get_literal_value, get_overload_const, get_overload_const_bool, is_common_scalar_dtype, is_iterable_type, is_list_like_index_type, is_literal_type, is_overload_constant_bool, is_overload_none, is_overload_true, is_scalar_type, raise_bodo_error


class PDCategoricalDtype(types.Opaque):

    def __init__(self, categories, elem_type, ordered, data=None, int_type=None
        ):
        self.categories = categories
        self.elem_type = elem_type
        self.ordered = ordered
        self.data = _get_cat_index_type(elem_type) if data is None else data
        self.int_type = int_type
        ycof__eny = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=ycof__eny)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    bxg__okeo = tuple(val.categories.values)
    elem_type = None if len(bxg__okeo) == 0 else bodo.typeof(val.categories
        .values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(bxg__okeo, elem_type, val.ordered, bodo.
        typeof(val.categories), int_type)


def _get_cat_index_type(elem_type):
    elem_type = bodo.string_type if elem_type is None else elem_type
    return bodo.utils.typing.get_index_type_from_dtype(elem_type)


@lower_constant(PDCategoricalDtype)
def lower_constant_categorical_type(context, builder, typ, pyval):
    categories = context.get_constant_generic(builder, bodo.typeof(pyval.
        categories), pyval.categories)
    ordered = context.get_constant(types.bool_, pyval.ordered)
    return lir.Constant.literal_struct([categories, ordered])


@register_model(PDCategoricalDtype)
class PDCategoricalDtypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yryj__igoh = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, yryj__igoh)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    obyy__wdqt = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    swxv__cxws = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, poel__mxrpe, poel__mxrpe = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    lbllq__mtuwk = PDCategoricalDtype(swxv__cxws, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, obyy__wdqt)
    return lbllq__mtuwk(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qvgcz__mbwgu = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, qvgcz__mbwgu
        ).value
    c.pyapi.decref(qvgcz__mbwgu)
    dsagq__noix = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, dsagq__noix).value
    c.pyapi.decref(dsagq__noix)
    mhwmo__bcvvy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=mhwmo__bcvvy)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    qvgcz__mbwgu = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    kxui__ronj = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    wfcn__isp = c.context.insert_const_string(c.builder.module, 'pandas')
    yozb__nix = c.pyapi.import_module_noblock(wfcn__isp)
    xcx__rzfb = c.pyapi.call_method(yozb__nix, 'CategoricalDtype', (
        kxui__ronj, qvgcz__mbwgu))
    c.pyapi.decref(qvgcz__mbwgu)
    c.pyapi.decref(kxui__ronj)
    c.pyapi.decref(yozb__nix)
    c.context.nrt.decref(c.builder, typ, val)
    return xcx__rzfb


@overload_attribute(PDCategoricalDtype, 'nbytes')
def pd_categorical_nbytes_overload(A):
    return lambda A: A.categories.nbytes + bodo.io.np_io.get_dtype_size(types
        .bool_)


class CategoricalArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(CategoricalArrayType, self).__init__(name=
            f'CategoricalArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return CategoricalArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.Categorical)
def _typeof_pd_cat(val, c):
    return CategoricalArrayType(bodo.typeof(val.dtype))


@register_model(CategoricalArrayType)
class CategoricalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ujt__bif = get_categories_int_type(fe_type.dtype)
        yryj__igoh = [('dtype', fe_type.dtype), ('codes', types.Array(
            ujt__bif, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, yryj__igoh)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    ydob__oniun = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), ydob__oniun
        ).value
    c.pyapi.decref(ydob__oniun)
    xcx__rzfb = c.pyapi.object_getattr_string(val, 'dtype')
    hftw__hzdae = c.pyapi.to_native_value(typ.dtype, xcx__rzfb).value
    c.pyapi.decref(xcx__rzfb)
    buxva__roqos = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    buxva__roqos.codes = codes
    buxva__roqos.dtype = hftw__hzdae
    return NativeValue(buxva__roqos._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    aoev__gdl = get_categories_int_type(typ.dtype)
    dscrc__jfx = context.get_constant_generic(builder, types.Array(
        aoev__gdl, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, dscrc__jfx])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    hvay__xcz = len(cat_dtype.categories)
    if hvay__xcz < np.iinfo(np.int8).max:
        dtype = types.int8
    elif hvay__xcz < np.iinfo(np.int16).max:
        dtype = types.int16
    elif hvay__xcz < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    wfcn__isp = c.context.insert_const_string(c.builder.module, 'pandas')
    yozb__nix = c.pyapi.import_module_noblock(wfcn__isp)
    ujt__bif = get_categories_int_type(dtype)
    vfx__njs = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    kylwb__qqhih = types.Array(ujt__bif, 1, 'C')
    c.context.nrt.incref(c.builder, kylwb__qqhih, vfx__njs.codes)
    ydob__oniun = c.pyapi.from_native_value(kylwb__qqhih, vfx__njs.codes, c
        .env_manager)
    c.context.nrt.incref(c.builder, dtype, vfx__njs.dtype)
    xcx__rzfb = c.pyapi.from_native_value(dtype, vfx__njs.dtype, c.env_manager)
    wvgwx__mayn = c.pyapi.borrow_none()
    ocldc__wqaom = c.pyapi.object_getattr_string(yozb__nix, 'Categorical')
    jwj__dekb = c.pyapi.call_method(ocldc__wqaom, 'from_codes', (
        ydob__oniun, wvgwx__mayn, wvgwx__mayn, xcx__rzfb))
    c.pyapi.decref(ocldc__wqaom)
    c.pyapi.decref(ydob__oniun)
    c.pyapi.decref(xcx__rzfb)
    c.pyapi.decref(yozb__nix)
    c.context.nrt.decref(c.builder, typ, val)
    return jwj__dekb


def _to_readonly(t):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, TimedeltaIndexType
    if isinstance(t, CategoricalArrayType):
        return CategoricalArrayType(_to_readonly(t.dtype))
    if isinstance(t, PDCategoricalDtype):
        return PDCategoricalDtype(t.categories, t.elem_type, t.ordered,
            _to_readonly(t.data), t.int_type)
    if isinstance(t, types.Array):
        return types.Array(t.dtype, t.ndim, 'C', True)
    if isinstance(t, NumericIndexType):
        return NumericIndexType(t.dtype, t.name_typ, _to_readonly(t.data))
    if isinstance(t, (DatetimeIndexType, TimedeltaIndexType)):
        return t.__class__(t.name_typ, _to_readonly(t.data))
    return t


@lower_cast(CategoricalArrayType, CategoricalArrayType)
def cast_cat_arr(context, builder, fromty, toty, val):
    if _to_readonly(toty) == fromty:
        return val
    raise BodoError(f'Cannot cast from {fromty} to {toty}')


def create_cmp_op_overload(op):

    def overload_cat_arr_cmp(A, other):
        if not isinstance(A, CategoricalArrayType):
            return
        if A.dtype.categories and is_literal_type(other) and types.unliteral(
            other) == A.dtype.elem_type:
            val = get_literal_value(other)
            snba__imioe = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                zdx__tvzjg = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), snba__imioe)
                return zdx__tvzjg
            return impl_lit

        def impl(A, other):
            snba__imioe = get_code_for_value(A.dtype, other)
            zdx__tvzjg = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), snba__imioe)
            return zdx__tvzjg
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        aqv__ccul = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(aqv__ccul)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    vfx__njs = cat_dtype.categories
    n = len(vfx__njs)
    for kqx__htmj in range(n):
        if vfx__njs[kqx__htmj] == val:
            return kqx__htmj
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    jznd__egvpa = bodo.utils.typing.parse_dtype(dtype,
        'CategoricalArray.astype')
    if jznd__egvpa != A.dtype.elem_type and jznd__egvpa != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if jznd__egvpa == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            zdx__tvzjg = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for kqx__htmj in numba.parfors.parfor.internal_prange(n):
                fao__glcjp = codes[kqx__htmj]
                if fao__glcjp == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(zdx__tvzjg
                            , kqx__htmj)
                    else:
                        bodo.libs.array_kernels.setna(zdx__tvzjg, kqx__htmj)
                    continue
                zdx__tvzjg[kqx__htmj] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[fao__glcjp]))
            return zdx__tvzjg
        return impl
    kylwb__qqhih = dtype_to_array_type(jznd__egvpa)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        zdx__tvzjg = bodo.utils.utils.alloc_type(n, kylwb__qqhih, (-1,))
        for kqx__htmj in numba.parfors.parfor.internal_prange(n):
            fao__glcjp = codes[kqx__htmj]
            if fao__glcjp == -1:
                bodo.libs.array_kernels.setna(zdx__tvzjg, kqx__htmj)
                continue
            zdx__tvzjg[kqx__htmj] = bodo.utils.conversion.unbox_if_timestamp(
                categories[fao__glcjp])
        return zdx__tvzjg
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        yehp__hni, hftw__hzdae = args
        vfx__njs = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        vfx__njs.codes = yehp__hni
        vfx__njs.dtype = hftw__hzdae
        context.nrt.incref(builder, signature.args[0], yehp__hni)
        context.nrt.incref(builder, signature.args[1], hftw__hzdae)
        return vfx__njs._getvalue()
    lwzdi__bvod = CategoricalArrayType(cat_dtype)
    sig = lwzdi__bvod(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    shvr__wiq = args[0]
    if equiv_set.has_shape(shvr__wiq):
        return ArrayAnalysis.AnalyzeResult(shape=shvr__wiq, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    ujt__bif = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, ujt__bif)
        return init_categorical_array(codes, cat_dtype)
    return impl


def alloc_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_alloc_categorical_array
    ) = alloc_categorical_array_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_categorical_arr_codes(A):
    return lambda A: A.codes


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_categorical_array',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_categorical_arr_codes',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func


@overload_method(CategoricalArrayType, 'copy', no_unliteral=True)
def cat_arr_copy_overload(arr):
    return lambda arr: init_categorical_array(arr.codes.copy(), arr.dtype)


def build_replace_dicts(to_replace, value, categories):
    return dict(), np.empty(len(categories) + 1), 0


@overload(build_replace_dicts, no_unliteral=True)
def _build_replace_dicts(to_replace, value, categories):
    if isinstance(to_replace, types.Number) or to_replace == bodo.string_type:

        def impl(to_replace, value, categories):
            return build_replace_dicts([to_replace], value, categories)
        return impl
    else:

        def impl(to_replace, value, categories):
            n = len(categories)
            ltv__phgt = {}
            dscrc__jfx = np.empty(n + 1, np.int64)
            sevuw__inrt = {}
            isw__xmmm = []
            iubhq__vjuyd = {}
            for kqx__htmj in range(n):
                iubhq__vjuyd[categories[kqx__htmj]] = kqx__htmj
            for sxslq__cjbqb in to_replace:
                if sxslq__cjbqb != value:
                    if sxslq__cjbqb in iubhq__vjuyd:
                        if value in iubhq__vjuyd:
                            ltv__phgt[sxslq__cjbqb] = sxslq__cjbqb
                            isqw__jrvbc = iubhq__vjuyd[sxslq__cjbqb]
                            sevuw__inrt[isqw__jrvbc] = iubhq__vjuyd[value]
                            isw__xmmm.append(isqw__jrvbc)
                        else:
                            ltv__phgt[sxslq__cjbqb] = value
                            iubhq__vjuyd[value] = iubhq__vjuyd[sxslq__cjbqb]
            aqsc__umh = np.sort(np.array(isw__xmmm))
            uckx__vmnrq = 0
            aeoll__vont = []
            for reo__gcjd in range(-1, n):
                while uckx__vmnrq < len(aqsc__umh) and reo__gcjd > aqsc__umh[
                    uckx__vmnrq]:
                    uckx__vmnrq += 1
                aeoll__vont.append(uckx__vmnrq)
            for igusr__ekjv in range(-1, n):
                uct__hymo = igusr__ekjv
                if igusr__ekjv in sevuw__inrt:
                    uct__hymo = sevuw__inrt[igusr__ekjv]
                dscrc__jfx[igusr__ekjv + 1] = uct__hymo - aeoll__vont[
                    uct__hymo + 1]
            return ltv__phgt, dscrc__jfx, len(aqsc__umh)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for kqx__htmj in range(len(new_codes_arr)):
        new_codes_arr[kqx__htmj] = codes_map_arr[old_codes_arr[kqx__htmj] + 1]


@overload_method(CategoricalArrayType, 'replace', inline='always',
    no_unliteral=True)
def overload_replace(arr, to_replace, value):

    def impl(arr, to_replace, value):
        return bodo.hiframes.pd_categorical_ext.cat_replace(arr, to_replace,
            value)
    return impl


def cat_replace(arr, to_replace, value):
    return


@overload(cat_replace, no_unliteral=True)
def cat_replace_overload(arr, to_replace, value):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_replace,
        'CategoricalArray.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'CategoricalArray.replace()')
    wick__gaeyv = arr.dtype.ordered
    ykgws__cbom = arr.dtype.elem_type
    jqfbb__vhv = get_overload_const(to_replace)
    tny__pimcu = get_overload_const(value)
    if (arr.dtype.categories is not None and jqfbb__vhv is not NOT_CONSTANT and
        tny__pimcu is not NOT_CONSTANT):
        sowar__vcz, codes_map_arr, poel__mxrpe = python_build_replace_dicts(
            jqfbb__vhv, tny__pimcu, arr.dtype.categories)
        if len(sowar__vcz) == 0:
            return lambda arr, to_replace, value: arr.copy()
        uwm__kmmn = []
        for ywo__uty in arr.dtype.categories:
            if ywo__uty in sowar__vcz:
                tayx__yncly = sowar__vcz[ywo__uty]
                if tayx__yncly != ywo__uty:
                    uwm__kmmn.append(tayx__yncly)
            else:
                uwm__kmmn.append(ywo__uty)
        vqiq__tilab = pd.CategoricalDtype(uwm__kmmn, wick__gaeyv
            ).categories.values
        ajscs__igvb = MetaType(tuple(vqiq__tilab))

        def impl_dtype(arr, to_replace, value):
            dhi__krbcx = init_cat_dtype(bodo.utils.conversion.
                index_from_array(vqiq__tilab), wick__gaeyv, None, ajscs__igvb)
            vfx__njs = alloc_categorical_array(len(arr.codes), dhi__krbcx)
            reassign_codes(vfx__njs.codes, arr.codes, codes_map_arr)
            return vfx__njs
        return impl_dtype
    ykgws__cbom = arr.dtype.elem_type
    if ykgws__cbom == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            ltv__phgt, codes_map_arr, gtmr__oylm = build_replace_dicts(
                to_replace, value, categories.values)
            if len(ltv__phgt) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), wick__gaeyv,
                    None, None))
            n = len(categories)
            vqiq__tilab = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                gtmr__oylm, -1)
            wicul__tnbbw = 0
            for reo__gcjd in range(n):
                davqc__uyfof = categories[reo__gcjd]
                if davqc__uyfof in ltv__phgt:
                    ojc__uqhk = ltv__phgt[davqc__uyfof]
                    if ojc__uqhk != davqc__uyfof:
                        vqiq__tilab[wicul__tnbbw] = ojc__uqhk
                        wicul__tnbbw += 1
                else:
                    vqiq__tilab[wicul__tnbbw] = davqc__uyfof
                    wicul__tnbbw += 1
            vfx__njs = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                vqiq__tilab), wick__gaeyv, None, None))
            reassign_codes(vfx__njs.codes, arr.codes, codes_map_arr)
            return vfx__njs
        return impl_str
    pkko__ycs = dtype_to_array_type(ykgws__cbom)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        ltv__phgt, codes_map_arr, gtmr__oylm = build_replace_dicts(to_replace,
            value, categories.values)
        if len(ltv__phgt) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), wick__gaeyv, None, None))
        n = len(categories)
        vqiq__tilab = bodo.utils.utils.alloc_type(n - gtmr__oylm, pkko__ycs,
            None)
        wicul__tnbbw = 0
        for kqx__htmj in range(n):
            davqc__uyfof = categories[kqx__htmj]
            if davqc__uyfof in ltv__phgt:
                ojc__uqhk = ltv__phgt[davqc__uyfof]
                if ojc__uqhk != davqc__uyfof:
                    vqiq__tilab[wicul__tnbbw] = ojc__uqhk
                    wicul__tnbbw += 1
            else:
                vqiq__tilab[wicul__tnbbw] = davqc__uyfof
                wicul__tnbbw += 1
        vfx__njs = alloc_categorical_array(len(arr.codes), init_cat_dtype(
            bodo.utils.conversion.index_from_array(vqiq__tilab),
            wick__gaeyv, None, None))
        reassign_codes(vfx__njs.codes, arr.codes, codes_map_arr)
        return vfx__njs
    return impl


@overload(len, no_unliteral=True)
def overload_cat_arr_len(A):
    if isinstance(A, CategoricalArrayType):
        return lambda A: len(A.codes)


@overload_attribute(CategoricalArrayType, 'shape')
def overload_cat_arr_shape(A):
    return lambda A: (len(A.codes),)


@overload_attribute(CategoricalArrayType, 'ndim')
def overload_cat_arr_ndim(A):
    return lambda A: 1


@overload_attribute(CategoricalArrayType, 'nbytes')
def cat_arr_nbytes_overload(A):
    return lambda A: A.codes.nbytes + A.dtype.nbytes


@register_jitable
def get_label_dict_from_categories(vals):
    ctyx__xmxii = dict()
    jbytx__dayvc = 0
    for kqx__htmj in range(len(vals)):
        val = vals[kqx__htmj]
        if val in ctyx__xmxii:
            continue
        ctyx__xmxii[val] = jbytx__dayvc
        jbytx__dayvc += 1
    return ctyx__xmxii


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    ctyx__xmxii = dict()
    for kqx__htmj in range(len(vals)):
        val = vals[kqx__htmj]
        ctyx__xmxii[val] = kqx__htmj
    return ctyx__xmxii


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    nrjlj__bqhd = dict(fastpath=fastpath)
    qqjfd__ecuj = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', nrjlj__bqhd, qqjfd__ecuj)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        qnx__szts = get_overload_const(categories)
        if qnx__szts is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                mhfq__psf = False
            else:
                mhfq__psf = get_overload_const_bool(ordered)
            rrx__vsj = pd.CategoricalDtype(qnx__szts, mhfq__psf
                ).categories.values
            qjaf__udf = MetaType(tuple(rrx__vsj))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                dhi__krbcx = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(rrx__vsj), mhfq__psf, None, qjaf__udf)
                return bodo.utils.conversion.fix_arr_dtype(data, dhi__krbcx)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            bxg__okeo = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                bxg__okeo, ordered, None, None)
            return bodo.utils.conversion.fix_arr_dtype(data, cat_dtype)
        return impl_cats
    elif is_overload_none(ordered):

        def impl_auto(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, 'category')
        return impl_auto
    raise BodoError(
        f'pd.Categorical(): argument combination not supported yet: {values}, {categories}, {ordered}, {dtype}'
        )


@overload(operator.getitem, no_unliteral=True)
def categorical_array_getitem(arr, ind):
    if not isinstance(arr, CategoricalArrayType):
        return
    if isinstance(ind, types.Integer):

        def categorical_getitem_impl(arr, ind):
            tmfek__rzzu = arr.codes[ind]
            return arr.dtype.categories[max(tmfek__rzzu, 0)]
        return categorical_getitem_impl
    if is_list_like_index_type(ind) or isinstance(ind, types.SliceType):

        def impl_bool(arr, ind):
            return init_categorical_array(arr.codes[ind], arr.dtype)
        return impl_bool
    raise BodoError(
        f'getitem for CategoricalArrayType with indexing type {ind} not supported.'
        )


class CategoricalMatchingValues(enum.Enum):
    DIFFERENT_TYPES = -1
    DONT_MATCH = 0
    MAY_MATCH = 1
    DO_MATCH = 2


def categorical_arrs_match(arr1, arr2):
    if not (isinstance(arr1, CategoricalArrayType) and isinstance(arr2,
        CategoricalArrayType)):
        return CategoricalMatchingValues.DIFFERENT_TYPES
    if arr1.dtype.categories is None or arr2.dtype.categories is None:
        return CategoricalMatchingValues.MAY_MATCH
    return (CategoricalMatchingValues.DO_MATCH if arr1.dtype.categories ==
        arr2.dtype.categories and arr1.dtype.ordered == arr2.dtype.ordered else
        CategoricalMatchingValues.DONT_MATCH)


@register_jitable
def cat_dtype_equal(dtype1, dtype2):
    if dtype1.ordered != dtype2.ordered or len(dtype1.categories) != len(dtype2
        .categories):
        return False
    arr1 = dtype1.categories.values
    arr2 = dtype2.categories.values
    for kqx__htmj in range(len(arr1)):
        if arr1[kqx__htmj] != arr2[kqx__htmj]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    uco__yyi = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    ykcp__hsye = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    sorbc__nbwpj = categorical_arrs_match(arr, val)
    ubz__mys = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    npty__axv = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not uco__yyi:
            raise BodoError(ubz__mys)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            tmfek__rzzu = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = tmfek__rzzu
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (uco__yyi or ykcp__hsye or sorbc__nbwpj !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ubz__mys)
        if sorbc__nbwpj == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(npty__axv)
        if uco__yyi:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                rrfz__vez = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for reo__gcjd in range(n):
                    arr.codes[ind[reo__gcjd]] = rrfz__vez
            return impl_scalar
        if sorbc__nbwpj == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for kqx__htmj in range(n):
                    arr.codes[ind[kqx__htmj]] = val.codes[kqx__htmj]
            return impl_arr_ind_mask
        if sorbc__nbwpj == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(npty__axv)
                n = len(val.codes)
                for kqx__htmj in range(n):
                    arr.codes[ind[kqx__htmj]] = val.codes[kqx__htmj]
            return impl_arr_ind_mask
        if ykcp__hsye:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for reo__gcjd in range(n):
                    tmrka__eby = bodo.utils.conversion.unbox_if_timestamp(val
                        [reo__gcjd])
                    if tmrka__eby not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    tmfek__rzzu = categories.get_loc(tmrka__eby)
                    arr.codes[ind[reo__gcjd]] = tmfek__rzzu
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (uco__yyi or ykcp__hsye or sorbc__nbwpj !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ubz__mys)
        if sorbc__nbwpj == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(npty__axv)
        if uco__yyi:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                rrfz__vez = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for reo__gcjd in range(n):
                    if ind[reo__gcjd]:
                        arr.codes[reo__gcjd] = rrfz__vez
            return impl_scalar
        if sorbc__nbwpj == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                nkzx__ymskc = 0
                for kqx__htmj in range(n):
                    if ind[kqx__htmj]:
                        arr.codes[kqx__htmj] = val.codes[nkzx__ymskc]
                        nkzx__ymskc += 1
            return impl_bool_ind_mask
        if sorbc__nbwpj == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(npty__axv)
                n = len(ind)
                nkzx__ymskc = 0
                for kqx__htmj in range(n):
                    if ind[kqx__htmj]:
                        arr.codes[kqx__htmj] = val.codes[nkzx__ymskc]
                        nkzx__ymskc += 1
            return impl_bool_ind_mask
        if ykcp__hsye:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                nkzx__ymskc = 0
                categories = arr.dtype.categories
                for reo__gcjd in range(n):
                    if ind[reo__gcjd]:
                        tmrka__eby = bodo.utils.conversion.unbox_if_timestamp(
                            val[nkzx__ymskc])
                        if tmrka__eby not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        tmfek__rzzu = categories.get_loc(tmrka__eby)
                        arr.codes[reo__gcjd] = tmfek__rzzu
                        nkzx__ymskc += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (uco__yyi or ykcp__hsye or sorbc__nbwpj !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(ubz__mys)
        if sorbc__nbwpj == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(npty__axv)
        if uco__yyi:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                rrfz__vez = arr.dtype.categories.get_loc(val)
                qwgvj__lskr = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for reo__gcjd in range(qwgvj__lskr.start, qwgvj__lskr.stop,
                    qwgvj__lskr.step):
                    arr.codes[reo__gcjd] = rrfz__vez
            return impl_scalar
        if sorbc__nbwpj == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if sorbc__nbwpj == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(npty__axv)
                arr.codes[ind] = val.codes
            return impl_arr
        if ykcp__hsye:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                qwgvj__lskr = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                nkzx__ymskc = 0
                for reo__gcjd in range(qwgvj__lskr.start, qwgvj__lskr.stop,
                    qwgvj__lskr.step):
                    tmrka__eby = bodo.utils.conversion.unbox_if_timestamp(val
                        [nkzx__ymskc])
                    if tmrka__eby not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    tmfek__rzzu = categories.get_loc(tmrka__eby)
                    arr.codes[reo__gcjd] = tmfek__rzzu
                    nkzx__ymskc += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
