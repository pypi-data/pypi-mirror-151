"""Dictionary encoded array data type, similar to DictionaryArray of Arrow.
The purpose is to improve memory consumption and performance over string_array_type for
string arrays that have a lot of repetitive values (typical in practice).
Can be extended to be used with types other than strings as well.
See:
https://bodo.atlassian.net/browse/BE-2295
https://bodo.atlassian.net/wiki/spaces/B/pages/993722369/Dictionary-encoded+String+Array+Support+in+Parquet+read+compute+...
https://arrow.apache.org/docs/cpp/api/array.html#dictionary-encoded
"""
import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_builtin, lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo
from bodo.libs import hstr_ext
from bodo.libs.bool_arr_ext import init_bool_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, get_str_arr_item_length, overload_str_arr_astype, pre_alloc_string_array
from bodo.utils.typing import BodoArrayIterator, is_overload_none, raise_bodo_error
ll.add_symbol('box_dict_str_array', hstr_ext.box_dict_str_array)
dict_indices_arr_type = IntegerArrayType(types.int32)


class DictionaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self, arr_data_type):
        self.data = arr_data_type
        super(DictionaryArrayType, self).__init__(name=
            f'DictionaryArrayType({arr_data_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    @property
    def dtype(self):
        return self.data.dtype

    def copy(self):
        return DictionaryArrayType(self.data)

    @property
    def indices_type(self):
        return dict_indices_arr_type

    @property
    def indices_dtype(self):
        return dict_indices_arr_type.dtype

    def unify(self, typingctx, other):
        if other == bodo.string_array_type:
            return bodo.string_array_type


dict_str_arr_type = DictionaryArrayType(bodo.string_array_type)


@register_model(DictionaryArrayType)
class DictionaryArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        grc__yxcc = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, grc__yxcc)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        frbmz__notar, rjaj__uozzg, mlw__ldy = args
        xui__omy = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        xui__omy.data = frbmz__notar
        xui__omy.indices = rjaj__uozzg
        xui__omy.has_global_dictionary = mlw__ldy
        context.nrt.incref(builder, signature.args[0], frbmz__notar)
        context.nrt.incref(builder, signature.args[1], rjaj__uozzg)
        return xui__omy._getvalue()
    tpnfb__ovi = DictionaryArrayType(data_t)
    vojrp__ndjd = tpnfb__ovi(data_t, indices_t, types.bool_)
    return vojrp__ndjd, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    for mnj__xpsh in range(len(A)):
        if pd.isna(A[mnj__xpsh]):
            A[mnj__xpsh] = None
    return pa.array(A).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    if bodo.hiframes.boxing._use_dict_str_type:
        tjff__mdypp = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(tjff__mdypp, [val])
        c.pyapi.decref(tjff__mdypp)
    xui__omy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lpuky__veoz = c.pyapi.object_getattr_string(val, 'dictionary')
    aczqo__bptxf = c.pyapi.bool_from_bool(c.context.get_constant(types.
        bool_, False))
    juvf__bgiwj = c.pyapi.call_method(lpuky__veoz, 'to_numpy', (aczqo__bptxf,))
    xui__omy.data = c.unbox(typ.data, juvf__bgiwj).value
    vdmj__qxg = c.pyapi.object_getattr_string(val, 'indices')
    skme__jfh = c.context.insert_const_string(c.builder.module, 'pandas')
    dzadk__vzw = c.pyapi.import_module_noblock(skme__jfh)
    msh__aep = c.pyapi.string_from_constant_string('Int32')
    vmv__avv = c.pyapi.call_method(dzadk__vzw, 'array', (vdmj__qxg, msh__aep))
    xui__omy.indices = c.unbox(dict_indices_arr_type, vmv__avv).value
    xui__omy.has_global_dictionary = c.context.get_constant(types.bool_, False)
    c.pyapi.decref(lpuky__veoz)
    c.pyapi.decref(aczqo__bptxf)
    c.pyapi.decref(juvf__bgiwj)
    c.pyapi.decref(vdmj__qxg)
    c.pyapi.decref(dzadk__vzw)
    c.pyapi.decref(msh__aep)
    c.pyapi.decref(vmv__avv)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    ibfy__wpo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xui__omy._getvalue(), is_error=ibfy__wpo)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    xui__omy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, xui__omy.data)
        ajbm__bvibb = c.box(typ.data, xui__omy.data)
        layyh__syd = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, xui__omy.indices)
        fxf__pueff = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        efxm__aqd = cgutils.get_or_insert_function(c.builder.module,
            fxf__pueff, name='box_dict_str_array')
        zcpl__mwcaj = cgutils.create_struct_proxy(types.Array(types.int32, 
            1, 'C'))(c.context, c.builder, layyh__syd.data)
        pmkk__alv = c.builder.extract_value(zcpl__mwcaj.shape, 0)
        ont__upj = zcpl__mwcaj.data
        vlfgu__iod = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, layyh__syd.null_bitmap).data
        juvf__bgiwj = c.builder.call(efxm__aqd, [pmkk__alv, ajbm__bvibb,
            ont__upj, vlfgu__iod])
        c.pyapi.decref(ajbm__bvibb)
    else:
        skme__jfh = c.context.insert_const_string(c.builder.module, 'pyarrow')
        jarrv__nwvpu = c.pyapi.import_module_noblock(skme__jfh)
        nmfcf__bfnh = c.pyapi.object_getattr_string(jarrv__nwvpu,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, xui__omy.data)
        ajbm__bvibb = c.box(typ.data, xui__omy.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, xui__omy.indices
            )
        vdmj__qxg = c.box(dict_indices_arr_type, xui__omy.indices)
        ioi__zgzp = c.pyapi.call_method(nmfcf__bfnh, 'from_arrays', (
            vdmj__qxg, ajbm__bvibb))
        aczqo__bptxf = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        juvf__bgiwj = c.pyapi.call_method(ioi__zgzp, 'to_numpy', (
            aczqo__bptxf,))
        c.pyapi.decref(jarrv__nwvpu)
        c.pyapi.decref(ajbm__bvibb)
        c.pyapi.decref(vdmj__qxg)
        c.pyapi.decref(nmfcf__bfnh)
        c.pyapi.decref(ioi__zgzp)
        c.pyapi.decref(aczqo__bptxf)
    c.context.nrt.decref(c.builder, typ, val)
    return juvf__bgiwj


@overload(len, no_unliteral=True)
def overload_dict_arr_len(A):
    if isinstance(A, DictionaryArrayType):
        return lambda A: len(A._indices)


@overload_attribute(DictionaryArrayType, 'shape')
def overload_dict_arr_shape(A):
    return lambda A: (len(A._indices),)


@overload_attribute(DictionaryArrayType, 'ndim')
def overload_dict_arr_ndim(A):
    return lambda A: 1


@overload_attribute(DictionaryArrayType, 'size')
def overload_dict_arr_size(A):
    return lambda A: len(A._indices)


@overload_method(DictionaryArrayType, 'tolist', no_unliteral=True)
def overload_dict_arr_tolist(A):
    return lambda A: list(A)


overload_method(DictionaryArrayType, 'astype', no_unliteral=True)(
    overload_str_arr_astype)


@overload_method(DictionaryArrayType, 'copy', no_unliteral=True)
def overload_dict_arr_copy(A):

    def copy_impl(A):
        return init_dict_arr(A._data.copy(), A._indices.copy(), A.
            _has_global_dictionary)
    return copy_impl


@overload_attribute(DictionaryArrayType, 'dtype')
def overload_dict_arr_dtype(A):
    return lambda A: A._data.dtype


@overload_attribute(DictionaryArrayType, 'nbytes')
def dict_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._indices.nbytes


@lower_constant(DictionaryArrayType)
def lower_constant_dict_arr(context, builder, typ, pyval):
    if bodo.hiframes.boxing._use_dict_str_type and isinstance(pyval, np.ndarray
        ):
        pyval = pa.array(pyval).dictionary_encode()
    wuy__chu = pyval.dictionary.to_numpy(False)
    rprd__rmklz = pd.array(pyval.indices, 'Int32')
    wuy__chu = context.get_constant_generic(builder, typ.data, wuy__chu)
    rprd__rmklz = context.get_constant_generic(builder,
        dict_indices_arr_type, rprd__rmklz)
    sptpq__nyky = context.get_constant(types.bool_, False)
    rrn__gfowf = lir.Constant.literal_struct([wuy__chu, rprd__rmklz,
        sptpq__nyky])
    return rrn__gfowf


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            clo__onsco = A._indices[ind]
            return A._data[clo__onsco]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        frbmz__notar = A._data
        rjaj__uozzg = A._indices
        pmkk__alv = len(rjaj__uozzg)
        unktr__bpy = [get_str_arr_item_length(frbmz__notar, mnj__xpsh) for
            mnj__xpsh in range(len(frbmz__notar))]
        nlimq__fkck = 0
        for mnj__xpsh in range(pmkk__alv):
            if not bodo.libs.array_kernels.isna(rjaj__uozzg, mnj__xpsh):
                nlimq__fkck += unktr__bpy[rjaj__uozzg[mnj__xpsh]]
        wqhmp__ufwxe = pre_alloc_string_array(pmkk__alv, nlimq__fkck)
        for mnj__xpsh in range(pmkk__alv):
            if bodo.libs.array_kernels.isna(rjaj__uozzg, mnj__xpsh):
                bodo.libs.array_kernels.setna(wqhmp__ufwxe, mnj__xpsh)
                continue
            ind = rjaj__uozzg[mnj__xpsh]
            if bodo.libs.array_kernels.isna(frbmz__notar, ind):
                bodo.libs.array_kernels.setna(wqhmp__ufwxe, mnj__xpsh)
                continue
            wqhmp__ufwxe[mnj__xpsh] = frbmz__notar[ind]
        return wqhmp__ufwxe
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    clo__onsco = -1
    frbmz__notar = arr._data
    for mnj__xpsh in range(len(frbmz__notar)):
        if bodo.libs.array_kernels.isna(frbmz__notar, mnj__xpsh):
            continue
        if frbmz__notar[mnj__xpsh] == val:
            clo__onsco = mnj__xpsh
            break
    return clo__onsco


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    pmkk__alv = len(arr)
    clo__onsco = find_dict_ind(arr, val)
    if clo__onsco == -1:
        return init_bool_array(np.full(pmkk__alv, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == clo__onsco


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    pmkk__alv = len(arr)
    clo__onsco = find_dict_ind(arr, val)
    if clo__onsco == -1:
        return init_bool_array(np.full(pmkk__alv, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != clo__onsco


def get_binary_op_overload(op, lhs, rhs):
    if op == operator.eq:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_eq(lhs, rhs)
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_eq(rhs, lhs)
    if op == operator.ne:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_ne(lhs, rhs)
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: dict_arr_ne(rhs, lhs)


def convert_dict_arr_to_int(arr, dtype):
    return arr


@overload(convert_dict_arr_to_int)
def convert_dict_arr_to_int_overload(arr, dtype):

    def impl(arr, dtype):
        ihoop__lvvbt = arr._data
        mld__esb = bodo.libs.int_arr_ext.alloc_int_array(len(ihoop__lvvbt),
            dtype)
        for ymum__bpbd in range(len(ihoop__lvvbt)):
            if bodo.libs.array_kernels.isna(ihoop__lvvbt, ymum__bpbd):
                bodo.libs.array_kernels.setna(mld__esb, ymum__bpbd)
                continue
            mld__esb[ymum__bpbd] = np.int64(ihoop__lvvbt[ymum__bpbd])
        pmkk__alv = len(arr)
        rjaj__uozzg = arr._indices
        wqhmp__ufwxe = bodo.libs.int_arr_ext.alloc_int_array(pmkk__alv, dtype)
        for mnj__xpsh in range(pmkk__alv):
            if bodo.libs.array_kernels.isna(rjaj__uozzg, mnj__xpsh):
                bodo.libs.array_kernels.setna(wqhmp__ufwxe, mnj__xpsh)
                continue
            wqhmp__ufwxe[mnj__xpsh] = mld__esb[rjaj__uozzg[mnj__xpsh]]
        return wqhmp__ufwxe
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    qjhs__coh = len(arrs)
    xkjtq__igsai = 'def impl(arrs, sep):\n'
    xkjtq__igsai += '  ind_map = {}\n'
    xkjtq__igsai += '  out_strs = []\n'
    xkjtq__igsai += '  n = len(arrs[0])\n'
    for mnj__xpsh in range(qjhs__coh):
        xkjtq__igsai += f'  indices{mnj__xpsh} = arrs[{mnj__xpsh}]._indices\n'
    for mnj__xpsh in range(qjhs__coh):
        xkjtq__igsai += f'  data{mnj__xpsh} = arrs[{mnj__xpsh}]._data\n'
    xkjtq__igsai += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    xkjtq__igsai += '  for i in range(n):\n'
    uts__xavj = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{mnj__xpsh}], i)' for mnj__xpsh in
        range(qjhs__coh)])
    xkjtq__igsai += f'    if {uts__xavj}:\n'
    xkjtq__igsai += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    xkjtq__igsai += '      continue\n'
    for mnj__xpsh in range(qjhs__coh):
        xkjtq__igsai += f'    ind{mnj__xpsh} = indices{mnj__xpsh}[i]\n'
    scx__eozx = '(' + ', '.join(f'ind{mnj__xpsh}' for mnj__xpsh in range(
        qjhs__coh)) + ')'
    xkjtq__igsai += f'    if {scx__eozx} not in ind_map:\n'
    xkjtq__igsai += '      out_ind = len(out_strs)\n'
    xkjtq__igsai += f'      ind_map[{scx__eozx}] = out_ind\n'
    cqpzl__unwk = "''" if is_overload_none(sep) else 'sep'
    avws__jam = ', '.join([f'data{mnj__xpsh}[ind{mnj__xpsh}]' for mnj__xpsh in
        range(qjhs__coh)])
    xkjtq__igsai += f'      v = {cqpzl__unwk}.join([{avws__jam}])\n'
    xkjtq__igsai += '      out_strs.append(v)\n'
    xkjtq__igsai += '    else:\n'
    xkjtq__igsai += f'      out_ind = ind_map[{scx__eozx}]\n'
    xkjtq__igsai += '    out_indices[i] = out_ind\n'
    xkjtq__igsai += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    xkjtq__igsai += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)
"""
    saqo__tlwx = {}
    exec(xkjtq__igsai, {'bodo': bodo, 'numba': numba, 'np': np}, saqo__tlwx)
    impl = saqo__tlwx['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    uludg__jhkkn = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    vojrp__ndjd = toty(fromty)
    zcgzk__qha = context.compile_internal(builder, uludg__jhkkn,
        vojrp__ndjd, (val,))
    return impl_ret_new_ref(context, builder, toty, zcgzk__qha)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    wuy__chu = arr._data
    zugb__akaeh = len(wuy__chu)
    kjln__ssld = pre_alloc_string_array(zugb__akaeh, -1)
    if regex:
        lmstp__gxb = re.compile(pat, flags)
        for mnj__xpsh in range(zugb__akaeh):
            if bodo.libs.array_kernels.isna(wuy__chu, mnj__xpsh):
                bodo.libs.array_kernels.setna(kjln__ssld, mnj__xpsh)
                continue
            kjln__ssld[mnj__xpsh] = lmstp__gxb.sub(repl=repl, string=
                wuy__chu[mnj__xpsh])
    else:
        for mnj__xpsh in range(zugb__akaeh):
            if bodo.libs.array_kernels.isna(wuy__chu, mnj__xpsh):
                bodo.libs.array_kernels.setna(kjln__ssld, mnj__xpsh)
                continue
            kjln__ssld[mnj__xpsh] = wuy__chu[mnj__xpsh].replace(pat, repl)
    return init_dict_arr(kjln__ssld, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    xui__omy = arr._data
    cumc__siz = len(xui__omy)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(cumc__siz)
    for mnj__xpsh in range(cumc__siz):
        dict_arr_out[mnj__xpsh] = xui__omy[mnj__xpsh].startswith(pat)
    rprd__rmklz = arr._indices
    pmo__tmj = len(rprd__rmklz)
    wqhmp__ufwxe = bodo.libs.bool_arr_ext.alloc_bool_array(pmo__tmj)
    for mnj__xpsh in range(pmo__tmj):
        if bodo.libs.array_kernels.isna(arr, mnj__xpsh):
            bodo.libs.array_kernels.setna(wqhmp__ufwxe, mnj__xpsh)
        else:
            wqhmp__ufwxe[mnj__xpsh] = dict_arr_out[rprd__rmklz[mnj__xpsh]]
    return wqhmp__ufwxe


@register_jitable
def str_endswith(arr, pat, na):
    xui__omy = arr._data
    cumc__siz = len(xui__omy)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(cumc__siz)
    for mnj__xpsh in range(cumc__siz):
        dict_arr_out[mnj__xpsh] = xui__omy[mnj__xpsh].endswith(pat)
    rprd__rmklz = arr._indices
    pmo__tmj = len(rprd__rmklz)
    wqhmp__ufwxe = bodo.libs.bool_arr_ext.alloc_bool_array(pmo__tmj)
    for mnj__xpsh in range(pmo__tmj):
        if bodo.libs.array_kernels.isna(arr, mnj__xpsh):
            bodo.libs.array_kernels.setna(wqhmp__ufwxe, mnj__xpsh)
        else:
            wqhmp__ufwxe[mnj__xpsh] = dict_arr_out[rprd__rmklz[mnj__xpsh]]
    return wqhmp__ufwxe


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    xui__omy = arr._data
    hezo__rbbwe = pd.Series(xui__omy)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = hezo__rbbwe.array._str_contains(pat, case, flags, na,
            regex)
    rprd__rmklz = arr._indices
    pmo__tmj = len(rprd__rmklz)
    wqhmp__ufwxe = bodo.libs.bool_arr_ext.alloc_bool_array(pmo__tmj)
    for mnj__xpsh in range(pmo__tmj):
        if bodo.libs.array_kernels.isna(arr, mnj__xpsh):
            bodo.libs.array_kernels.setna(wqhmp__ufwxe, mnj__xpsh)
        else:
            wqhmp__ufwxe[mnj__xpsh] = dict_arr_out[rprd__rmklz[mnj__xpsh]]
    return wqhmp__ufwxe


@register_jitable
def str_contains_non_regex(arr, pat, case):
    xui__omy = arr._data
    cumc__siz = len(xui__omy)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(cumc__siz)
    if not case:
        vcz__pcuii = pat.upper()
    for mnj__xpsh in range(cumc__siz):
        if case:
            dict_arr_out[mnj__xpsh] = pat in xui__omy[mnj__xpsh]
        else:
            dict_arr_out[mnj__xpsh] = vcz__pcuii in xui__omy[mnj__xpsh].upper()
    rprd__rmklz = arr._indices
    pmo__tmj = len(rprd__rmklz)
    wqhmp__ufwxe = bodo.libs.bool_arr_ext.alloc_bool_array(pmo__tmj)
    for mnj__xpsh in range(pmo__tmj):
        if bodo.libs.array_kernels.isna(arr, mnj__xpsh):
            bodo.libs.array_kernels.setna(wqhmp__ufwxe, mnj__xpsh)
        else:
            wqhmp__ufwxe[mnj__xpsh] = dict_arr_out[rprd__rmklz[mnj__xpsh]]
    return wqhmp__ufwxe
