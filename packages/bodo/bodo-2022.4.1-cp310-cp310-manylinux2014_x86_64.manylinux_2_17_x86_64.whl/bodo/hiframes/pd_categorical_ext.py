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
        sqhc__keod = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=sqhc__keod)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    jwdj__kxlif = tuple(val.categories.values)
    elem_type = None if len(jwdj__kxlif) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(jwdj__kxlif, elem_type, val.ordered, bodo.
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
        kyydc__mae = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, kyydc__mae)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    wnrb__ylcu = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    hme__hivvp = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, fuxd__cbpwt, fuxd__cbpwt = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    frc__nruw = PDCategoricalDtype(hme__hivvp, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, wnrb__ylcu)
    return frc__nruw(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hmut__vgmdi = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, hmut__vgmdi).value
    c.pyapi.decref(hmut__vgmdi)
    fhfto__siqyd = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, fhfto__siqyd
        ).value
    c.pyapi.decref(fhfto__siqyd)
    yegtr__eudz = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=yegtr__eudz)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    hmut__vgmdi = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    qkqby__gsjk = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    edkgx__fuqc = c.context.insert_const_string(c.builder.module, 'pandas')
    rfr__oinio = c.pyapi.import_module_noblock(edkgx__fuqc)
    hxeyb__zxkqd = c.pyapi.call_method(rfr__oinio, 'CategoricalDtype', (
        qkqby__gsjk, hmut__vgmdi))
    c.pyapi.decref(hmut__vgmdi)
    c.pyapi.decref(qkqby__gsjk)
    c.pyapi.decref(rfr__oinio)
    c.context.nrt.decref(c.builder, typ, val)
    return hxeyb__zxkqd


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
        rip__xxmbo = get_categories_int_type(fe_type.dtype)
        kyydc__mae = [('dtype', fe_type.dtype), ('codes', types.Array(
            rip__xxmbo, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, kyydc__mae)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    pqqf__qhn = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), pqqf__qhn
        ).value
    c.pyapi.decref(pqqf__qhn)
    hxeyb__zxkqd = c.pyapi.object_getattr_string(val, 'dtype')
    majj__cdzmj = c.pyapi.to_native_value(typ.dtype, hxeyb__zxkqd).value
    c.pyapi.decref(hxeyb__zxkqd)
    ubsba__hwr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ubsba__hwr.codes = codes
    ubsba__hwr.dtype = majj__cdzmj
    return NativeValue(ubsba__hwr._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    ylx__xrbh = get_categories_int_type(typ.dtype)
    sib__tgr = context.get_constant_generic(builder, types.Array(ylx__xrbh,
        1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, sib__tgr])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    wdjzl__owij = len(cat_dtype.categories)
    if wdjzl__owij < np.iinfo(np.int8).max:
        dtype = types.int8
    elif wdjzl__owij < np.iinfo(np.int16).max:
        dtype = types.int16
    elif wdjzl__owij < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    edkgx__fuqc = c.context.insert_const_string(c.builder.module, 'pandas')
    rfr__oinio = c.pyapi.import_module_noblock(edkgx__fuqc)
    rip__xxmbo = get_categories_int_type(dtype)
    lpxr__qrpu = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    bzn__nkcws = types.Array(rip__xxmbo, 1, 'C')
    c.context.nrt.incref(c.builder, bzn__nkcws, lpxr__qrpu.codes)
    pqqf__qhn = c.pyapi.from_native_value(bzn__nkcws, lpxr__qrpu.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, lpxr__qrpu.dtype)
    hxeyb__zxkqd = c.pyapi.from_native_value(dtype, lpxr__qrpu.dtype, c.
        env_manager)
    dplvx__ehd = c.pyapi.borrow_none()
    eeof__cwpiy = c.pyapi.object_getattr_string(rfr__oinio, 'Categorical')
    xah__musa = c.pyapi.call_method(eeof__cwpiy, 'from_codes', (pqqf__qhn,
        dplvx__ehd, dplvx__ehd, hxeyb__zxkqd))
    c.pyapi.decref(eeof__cwpiy)
    c.pyapi.decref(pqqf__qhn)
    c.pyapi.decref(hxeyb__zxkqd)
    c.pyapi.decref(rfr__oinio)
    c.context.nrt.decref(c.builder, typ, val)
    return xah__musa


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
            tki__thc = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                hiey__uogwi = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), tki__thc)
                return hiey__uogwi
            return impl_lit

        def impl(A, other):
            tki__thc = get_code_for_value(A.dtype, other)
            hiey__uogwi = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), tki__thc)
            return hiey__uogwi
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        xcg__reruv = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(xcg__reruv)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    lpxr__qrpu = cat_dtype.categories
    n = len(lpxr__qrpu)
    for rpufz__xenm in range(n):
        if lpxr__qrpu[rpufz__xenm] == val:
            return rpufz__xenm
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    evf__xiza = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype')
    if evf__xiza != A.dtype.elem_type and evf__xiza != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if evf__xiza == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            hiey__uogwi = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for rpufz__xenm in numba.parfors.parfor.internal_prange(n):
                cmyji__gyyna = codes[rpufz__xenm]
                if cmyji__gyyna == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(
                            hiey__uogwi, rpufz__xenm)
                    else:
                        bodo.libs.array_kernels.setna(hiey__uogwi, rpufz__xenm)
                    continue
                hiey__uogwi[rpufz__xenm] = str(bodo.utils.conversion.
                    unbox_if_timestamp(categories[cmyji__gyyna]))
            return hiey__uogwi
        return impl
    bzn__nkcws = dtype_to_array_type(evf__xiza)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        hiey__uogwi = bodo.utils.utils.alloc_type(n, bzn__nkcws, (-1,))
        for rpufz__xenm in numba.parfors.parfor.internal_prange(n):
            cmyji__gyyna = codes[rpufz__xenm]
            if cmyji__gyyna == -1:
                bodo.libs.array_kernels.setna(hiey__uogwi, rpufz__xenm)
                continue
            hiey__uogwi[rpufz__xenm
                ] = bodo.utils.conversion.unbox_if_timestamp(categories[
                cmyji__gyyna])
        return hiey__uogwi
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        rmuf__ctkrp, majj__cdzmj = args
        lpxr__qrpu = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        lpxr__qrpu.codes = rmuf__ctkrp
        lpxr__qrpu.dtype = majj__cdzmj
        context.nrt.incref(builder, signature.args[0], rmuf__ctkrp)
        context.nrt.incref(builder, signature.args[1], majj__cdzmj)
        return lpxr__qrpu._getvalue()
    nawvv__wkc = CategoricalArrayType(cat_dtype)
    sig = nawvv__wkc(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    packc__ybjs = args[0]
    if equiv_set.has_shape(packc__ybjs):
        return ArrayAnalysis.AnalyzeResult(shape=packc__ybjs, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    rip__xxmbo = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, rip__xxmbo)
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
            hts__uwp = {}
            sib__tgr = np.empty(n + 1, np.int64)
            jtm__wdtjm = {}
            eogyi__zrjbp = []
            pgkc__xems = {}
            for rpufz__xenm in range(n):
                pgkc__xems[categories[rpufz__xenm]] = rpufz__xenm
            for msbnf__zusn in to_replace:
                if msbnf__zusn != value:
                    if msbnf__zusn in pgkc__xems:
                        if value in pgkc__xems:
                            hts__uwp[msbnf__zusn] = msbnf__zusn
                            ptak__ytii = pgkc__xems[msbnf__zusn]
                            jtm__wdtjm[ptak__ytii] = pgkc__xems[value]
                            eogyi__zrjbp.append(ptak__ytii)
                        else:
                            hts__uwp[msbnf__zusn] = value
                            pgkc__xems[value] = pgkc__xems[msbnf__zusn]
            jviah__adg = np.sort(np.array(eogyi__zrjbp))
            fvkg__cqgwi = 0
            idlc__ewa = []
            for igtya__jjvi in range(-1, n):
                while fvkg__cqgwi < len(jviah__adg
                    ) and igtya__jjvi > jviah__adg[fvkg__cqgwi]:
                    fvkg__cqgwi += 1
                idlc__ewa.append(fvkg__cqgwi)
            for guyt__ikhws in range(-1, n):
                evcan__ogxcj = guyt__ikhws
                if guyt__ikhws in jtm__wdtjm:
                    evcan__ogxcj = jtm__wdtjm[guyt__ikhws]
                sib__tgr[guyt__ikhws + 1] = evcan__ogxcj - idlc__ewa[
                    evcan__ogxcj + 1]
            return hts__uwp, sib__tgr, len(jviah__adg)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for rpufz__xenm in range(len(new_codes_arr)):
        new_codes_arr[rpufz__xenm] = codes_map_arr[old_codes_arr[
            rpufz__xenm] + 1]


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
    bdb__rvvnv = arr.dtype.ordered
    cvr__tpiy = arr.dtype.elem_type
    ovt__gvckn = get_overload_const(to_replace)
    cwxms__lnfvy = get_overload_const(value)
    if (arr.dtype.categories is not None and ovt__gvckn is not NOT_CONSTANT and
        cwxms__lnfvy is not NOT_CONSTANT):
        euktb__aryg, codes_map_arr, fuxd__cbpwt = python_build_replace_dicts(
            ovt__gvckn, cwxms__lnfvy, arr.dtype.categories)
        if len(euktb__aryg) == 0:
            return lambda arr, to_replace, value: arr.copy()
        bicz__qknlo = []
        for ywe__fmn in arr.dtype.categories:
            if ywe__fmn in euktb__aryg:
                tzl__ozd = euktb__aryg[ywe__fmn]
                if tzl__ozd != ywe__fmn:
                    bicz__qknlo.append(tzl__ozd)
            else:
                bicz__qknlo.append(ywe__fmn)
        bnjgq__jlqj = pd.CategoricalDtype(bicz__qknlo, bdb__rvvnv
            ).categories.values
        ldhen__hyhg = MetaType(tuple(bnjgq__jlqj))

        def impl_dtype(arr, to_replace, value):
            ewdjl__wdatl = init_cat_dtype(bodo.utils.conversion.
                index_from_array(bnjgq__jlqj), bdb__rvvnv, None, ldhen__hyhg)
            lpxr__qrpu = alloc_categorical_array(len(arr.codes), ewdjl__wdatl)
            reassign_codes(lpxr__qrpu.codes, arr.codes, codes_map_arr)
            return lpxr__qrpu
        return impl_dtype
    cvr__tpiy = arr.dtype.elem_type
    if cvr__tpiy == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            hts__uwp, codes_map_arr, blrxu__ihx = build_replace_dicts(
                to_replace, value, categories.values)
            if len(hts__uwp) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), bdb__rvvnv,
                    None, None))
            n = len(categories)
            bnjgq__jlqj = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                blrxu__ihx, -1)
            zzst__ymnh = 0
            for igtya__jjvi in range(n):
                byt__zxtte = categories[igtya__jjvi]
                if byt__zxtte in hts__uwp:
                    bwj__bcu = hts__uwp[byt__zxtte]
                    if bwj__bcu != byt__zxtte:
                        bnjgq__jlqj[zzst__ymnh] = bwj__bcu
                        zzst__ymnh += 1
                else:
                    bnjgq__jlqj[zzst__ymnh] = byt__zxtte
                    zzst__ymnh += 1
            lpxr__qrpu = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                bnjgq__jlqj), bdb__rvvnv, None, None))
            reassign_codes(lpxr__qrpu.codes, arr.codes, codes_map_arr)
            return lpxr__qrpu
        return impl_str
    lbizg__zdj = dtype_to_array_type(cvr__tpiy)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        hts__uwp, codes_map_arr, blrxu__ihx = build_replace_dicts(to_replace,
            value, categories.values)
        if len(hts__uwp) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), bdb__rvvnv, None, None))
        n = len(categories)
        bnjgq__jlqj = bodo.utils.utils.alloc_type(n - blrxu__ihx,
            lbizg__zdj, None)
        zzst__ymnh = 0
        for rpufz__xenm in range(n):
            byt__zxtte = categories[rpufz__xenm]
            if byt__zxtte in hts__uwp:
                bwj__bcu = hts__uwp[byt__zxtte]
                if bwj__bcu != byt__zxtte:
                    bnjgq__jlqj[zzst__ymnh] = bwj__bcu
                    zzst__ymnh += 1
            else:
                bnjgq__jlqj[zzst__ymnh] = byt__zxtte
                zzst__ymnh += 1
        lpxr__qrpu = alloc_categorical_array(len(arr.codes), init_cat_dtype
            (bodo.utils.conversion.index_from_array(bnjgq__jlqj),
            bdb__rvvnv, None, None))
        reassign_codes(lpxr__qrpu.codes, arr.codes, codes_map_arr)
        return lpxr__qrpu
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
    xvf__evl = dict()
    yll__vyrz = 0
    for rpufz__xenm in range(len(vals)):
        val = vals[rpufz__xenm]
        if val in xvf__evl:
            continue
        xvf__evl[val] = yll__vyrz
        yll__vyrz += 1
    return xvf__evl


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    xvf__evl = dict()
    for rpufz__xenm in range(len(vals)):
        val = vals[rpufz__xenm]
        xvf__evl[val] = rpufz__xenm
    return xvf__evl


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    xupv__jda = dict(fastpath=fastpath)
    asmn__sfc = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', xupv__jda, asmn__sfc)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        rzff__bemsa = get_overload_const(categories)
        if rzff__bemsa is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                qkzi__kpuzt = False
            else:
                qkzi__kpuzt = get_overload_const_bool(ordered)
            awsru__mec = pd.CategoricalDtype(rzff__bemsa, qkzi__kpuzt
                ).categories.values
            fys__nmyfu = MetaType(tuple(awsru__mec))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                ewdjl__wdatl = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(awsru__mec), qkzi__kpuzt, None, fys__nmyfu
                    )
                return bodo.utils.conversion.fix_arr_dtype(data, ewdjl__wdatl)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            jwdj__kxlif = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                jwdj__kxlif, ordered, None, None)
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
            rrt__fzz = arr.codes[ind]
            return arr.dtype.categories[max(rrt__fzz, 0)]
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
    for rpufz__xenm in range(len(arr1)):
        if arr1[rpufz__xenm] != arr2[rpufz__xenm]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    jwavk__sqcdn = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    ckwi__xavo = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    srvq__rjp = categorical_arrs_match(arr, val)
    xqhwx__foivq = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    sus__rvg = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not jwavk__sqcdn:
            raise BodoError(xqhwx__foivq)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            rrt__fzz = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = rrt__fzz
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (jwavk__sqcdn or ckwi__xavo or srvq__rjp !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(xqhwx__foivq)
        if srvq__rjp == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(sus__rvg)
        if jwavk__sqcdn:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                bcj__rbr = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for igtya__jjvi in range(n):
                    arr.codes[ind[igtya__jjvi]] = bcj__rbr
            return impl_scalar
        if srvq__rjp == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for rpufz__xenm in range(n):
                    arr.codes[ind[rpufz__xenm]] = val.codes[rpufz__xenm]
            return impl_arr_ind_mask
        if srvq__rjp == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(sus__rvg)
                n = len(val.codes)
                for rpufz__xenm in range(n):
                    arr.codes[ind[rpufz__xenm]] = val.codes[rpufz__xenm]
            return impl_arr_ind_mask
        if ckwi__xavo:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for igtya__jjvi in range(n):
                    xir__khvk = bodo.utils.conversion.unbox_if_timestamp(val
                        [igtya__jjvi])
                    if xir__khvk not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    rrt__fzz = categories.get_loc(xir__khvk)
                    arr.codes[ind[igtya__jjvi]] = rrt__fzz
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (jwavk__sqcdn or ckwi__xavo or srvq__rjp !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(xqhwx__foivq)
        if srvq__rjp == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(sus__rvg)
        if jwavk__sqcdn:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                bcj__rbr = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for igtya__jjvi in range(n):
                    if ind[igtya__jjvi]:
                        arr.codes[igtya__jjvi] = bcj__rbr
            return impl_scalar
        if srvq__rjp == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                obtvh__mkcbg = 0
                for rpufz__xenm in range(n):
                    if ind[rpufz__xenm]:
                        arr.codes[rpufz__xenm] = val.codes[obtvh__mkcbg]
                        obtvh__mkcbg += 1
            return impl_bool_ind_mask
        if srvq__rjp == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(sus__rvg)
                n = len(ind)
                obtvh__mkcbg = 0
                for rpufz__xenm in range(n):
                    if ind[rpufz__xenm]:
                        arr.codes[rpufz__xenm] = val.codes[obtvh__mkcbg]
                        obtvh__mkcbg += 1
            return impl_bool_ind_mask
        if ckwi__xavo:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                obtvh__mkcbg = 0
                categories = arr.dtype.categories
                for igtya__jjvi in range(n):
                    if ind[igtya__jjvi]:
                        xir__khvk = bodo.utils.conversion.unbox_if_timestamp(
                            val[obtvh__mkcbg])
                        if xir__khvk not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        rrt__fzz = categories.get_loc(xir__khvk)
                        arr.codes[igtya__jjvi] = rrt__fzz
                        obtvh__mkcbg += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (jwavk__sqcdn or ckwi__xavo or srvq__rjp !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(xqhwx__foivq)
        if srvq__rjp == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(sus__rvg)
        if jwavk__sqcdn:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                bcj__rbr = arr.dtype.categories.get_loc(val)
                jyb__fespx = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for igtya__jjvi in range(jyb__fespx.start, jyb__fespx.stop,
                    jyb__fespx.step):
                    arr.codes[igtya__jjvi] = bcj__rbr
            return impl_scalar
        if srvq__rjp == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if srvq__rjp == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(sus__rvg)
                arr.codes[ind] = val.codes
            return impl_arr
        if ckwi__xavo:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                jyb__fespx = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                obtvh__mkcbg = 0
                for igtya__jjvi in range(jyb__fespx.start, jyb__fespx.stop,
                    jyb__fespx.step):
                    xir__khvk = bodo.utils.conversion.unbox_if_timestamp(val
                        [obtvh__mkcbg])
                    if xir__khvk not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    rrt__fzz = categories.get_loc(xir__khvk)
                    arr.codes[igtya__jjvi] = rrt__fzz
                    obtvh__mkcbg += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
