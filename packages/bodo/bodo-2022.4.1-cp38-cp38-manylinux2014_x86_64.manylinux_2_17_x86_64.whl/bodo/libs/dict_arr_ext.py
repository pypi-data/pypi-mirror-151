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
        opccl__bliw = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, opccl__bliw)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t=None):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        niugy__vau, gat__mkek, psou__jdemq = args
        khi__lpall = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        khi__lpall.data = niugy__vau
        khi__lpall.indices = gat__mkek
        khi__lpall.has_global_dictionary = psou__jdemq
        context.nrt.incref(builder, signature.args[0], niugy__vau)
        context.nrt.incref(builder, signature.args[1], gat__mkek)
        return khi__lpall._getvalue()
    kesh__jqs = DictionaryArrayType(data_t)
    mmhgd__kdmbx = kesh__jqs(data_t, indices_t, types.bool_)
    return mmhgd__kdmbx, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    for dgt__vrps in range(len(A)):
        if pd.isna(A[dgt__vrps]):
            A[dgt__vrps] = None
    return pa.array(A).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    if bodo.hiframes.boxing._use_dict_str_type:
        aohb__iug = c.pyapi.unserialize(c.pyapi.serialize_object(
            to_pa_dict_arr))
        val = c.pyapi.call_function_objargs(aohb__iug, [val])
        c.pyapi.decref(aohb__iug)
    khi__lpall = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    yxmwo__anx = c.pyapi.object_getattr_string(val, 'dictionary')
    wjfww__rugz = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    tgh__tsen = c.pyapi.call_method(yxmwo__anx, 'to_numpy', (wjfww__rugz,))
    khi__lpall.data = c.unbox(typ.data, tgh__tsen).value
    tbuwt__tqqti = c.pyapi.object_getattr_string(val, 'indices')
    vttjh__ggtcy = c.context.insert_const_string(c.builder.module, 'pandas')
    wkuxi__quzv = c.pyapi.import_module_noblock(vttjh__ggtcy)
    xlb__szyw = c.pyapi.string_from_constant_string('Int32')
    wevkk__vtck = c.pyapi.call_method(wkuxi__quzv, 'array', (tbuwt__tqqti,
        xlb__szyw))
    khi__lpall.indices = c.unbox(dict_indices_arr_type, wevkk__vtck).value
    khi__lpall.has_global_dictionary = c.context.get_constant(types.bool_, 
        False)
    c.pyapi.decref(yxmwo__anx)
    c.pyapi.decref(wjfww__rugz)
    c.pyapi.decref(tgh__tsen)
    c.pyapi.decref(tbuwt__tqqti)
    c.pyapi.decref(wkuxi__quzv)
    c.pyapi.decref(xlb__szyw)
    c.pyapi.decref(wevkk__vtck)
    if bodo.hiframes.boxing._use_dict_str_type:
        c.pyapi.decref(val)
    ctplp__vwtdb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(khi__lpall._getvalue(), is_error=ctplp__vwtdb)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    khi__lpall = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        c.context.nrt.incref(c.builder, typ.data, khi__lpall.data)
        ycepe__oqm = c.box(typ.data, khi__lpall.data)
        rxbwa__tcvp = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, khi__lpall.indices)
        yqbi__sdi = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        eme__lqk = cgutils.get_or_insert_function(c.builder.module,
            yqbi__sdi, name='box_dict_str_array')
        ctib__zze = cgutils.create_struct_proxy(types.Array(types.int32, 1,
            'C'))(c.context, c.builder, rxbwa__tcvp.data)
        hrcq__jrf = c.builder.extract_value(ctib__zze.shape, 0)
        ooy__pxr = ctib__zze.data
        jls__uffeu = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, rxbwa__tcvp.null_bitmap).data
        tgh__tsen = c.builder.call(eme__lqk, [hrcq__jrf, ycepe__oqm,
            ooy__pxr, jls__uffeu])
        c.pyapi.decref(ycepe__oqm)
    else:
        vttjh__ggtcy = c.context.insert_const_string(c.builder.module,
            'pyarrow')
        ngrmu__rgygv = c.pyapi.import_module_noblock(vttjh__ggtcy)
        mtbdx__vnfy = c.pyapi.object_getattr_string(ngrmu__rgygv,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, khi__lpall.data)
        ycepe__oqm = c.box(typ.data, khi__lpall.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, khi__lpall.
            indices)
        tbuwt__tqqti = c.box(dict_indices_arr_type, khi__lpall.indices)
        jeyb__jchmu = c.pyapi.call_method(mtbdx__vnfy, 'from_arrays', (
            tbuwt__tqqti, ycepe__oqm))
        wjfww__rugz = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        tgh__tsen = c.pyapi.call_method(jeyb__jchmu, 'to_numpy', (wjfww__rugz,)
            )
        c.pyapi.decref(ngrmu__rgygv)
        c.pyapi.decref(ycepe__oqm)
        c.pyapi.decref(tbuwt__tqqti)
        c.pyapi.decref(mtbdx__vnfy)
        c.pyapi.decref(jeyb__jchmu)
        c.pyapi.decref(wjfww__rugz)
    c.context.nrt.decref(c.builder, typ, val)
    return tgh__tsen


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
    drwy__thj = pyval.dictionary.to_numpy(False)
    tgzsu__ygqcs = pd.array(pyval.indices, 'Int32')
    drwy__thj = context.get_constant_generic(builder, typ.data, drwy__thj)
    tgzsu__ygqcs = context.get_constant_generic(builder,
        dict_indices_arr_type, tgzsu__ygqcs)
    porym__mepa = context.get_constant(types.bool_, False)
    xxf__gvz = lir.Constant.literal_struct([drwy__thj, tgzsu__ygqcs,
        porym__mepa])
    return xxf__gvz


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            zedkt__emyn = A._indices[ind]
            return A._data[zedkt__emyn]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        niugy__vau = A._data
        gat__mkek = A._indices
        hrcq__jrf = len(gat__mkek)
        kepz__scpi = [get_str_arr_item_length(niugy__vau, dgt__vrps) for
            dgt__vrps in range(len(niugy__vau))]
        kocu__ljtiu = 0
        for dgt__vrps in range(hrcq__jrf):
            if not bodo.libs.array_kernels.isna(gat__mkek, dgt__vrps):
                kocu__ljtiu += kepz__scpi[gat__mkek[dgt__vrps]]
        yen__tds = pre_alloc_string_array(hrcq__jrf, kocu__ljtiu)
        for dgt__vrps in range(hrcq__jrf):
            if bodo.libs.array_kernels.isna(gat__mkek, dgt__vrps):
                bodo.libs.array_kernels.setna(yen__tds, dgt__vrps)
                continue
            ind = gat__mkek[dgt__vrps]
            if bodo.libs.array_kernels.isna(niugy__vau, ind):
                bodo.libs.array_kernels.setna(yen__tds, dgt__vrps)
                continue
            yen__tds[dgt__vrps] = niugy__vau[ind]
        return yen__tds
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind(arr, val):
    zedkt__emyn = -1
    niugy__vau = arr._data
    for dgt__vrps in range(len(niugy__vau)):
        if bodo.libs.array_kernels.isna(niugy__vau, dgt__vrps):
            continue
        if niugy__vau[dgt__vrps] == val:
            zedkt__emyn = dgt__vrps
            break
    return zedkt__emyn


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    hrcq__jrf = len(arr)
    zedkt__emyn = find_dict_ind(arr, val)
    if zedkt__emyn == -1:
        return init_bool_array(np.full(hrcq__jrf, False, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices == zedkt__emyn


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    hrcq__jrf = len(arr)
    zedkt__emyn = find_dict_ind(arr, val)
    if zedkt__emyn == -1:
        return init_bool_array(np.full(hrcq__jrf, True, np.bool_), arr.
            _indices._null_bitmap.copy())
    return arr._indices != zedkt__emyn


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
        laxa__ucljh = arr._data
        vljoj__jhwg = bodo.libs.int_arr_ext.alloc_int_array(len(laxa__ucljh
            ), dtype)
        for ccokl__asyyl in range(len(laxa__ucljh)):
            if bodo.libs.array_kernels.isna(laxa__ucljh, ccokl__asyyl):
                bodo.libs.array_kernels.setna(vljoj__jhwg, ccokl__asyyl)
                continue
            vljoj__jhwg[ccokl__asyyl] = np.int64(laxa__ucljh[ccokl__asyyl])
        hrcq__jrf = len(arr)
        gat__mkek = arr._indices
        yen__tds = bodo.libs.int_arr_ext.alloc_int_array(hrcq__jrf, dtype)
        for dgt__vrps in range(hrcq__jrf):
            if bodo.libs.array_kernels.isna(gat__mkek, dgt__vrps):
                bodo.libs.array_kernels.setna(yen__tds, dgt__vrps)
                continue
            yen__tds[dgt__vrps] = vljoj__jhwg[gat__mkek[dgt__vrps]]
        return yen__tds
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    pgeol__pxuef = len(arrs)
    nqna__jrmux = 'def impl(arrs, sep):\n'
    nqna__jrmux += '  ind_map = {}\n'
    nqna__jrmux += '  out_strs = []\n'
    nqna__jrmux += '  n = len(arrs[0])\n'
    for dgt__vrps in range(pgeol__pxuef):
        nqna__jrmux += f'  indices{dgt__vrps} = arrs[{dgt__vrps}]._indices\n'
    for dgt__vrps in range(pgeol__pxuef):
        nqna__jrmux += f'  data{dgt__vrps} = arrs[{dgt__vrps}]._data\n'
    nqna__jrmux += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    nqna__jrmux += '  for i in range(n):\n'
    ewgp__toxeq = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{dgt__vrps}], i)' for dgt__vrps in
        range(pgeol__pxuef)])
    nqna__jrmux += f'    if {ewgp__toxeq}:\n'
    nqna__jrmux += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    nqna__jrmux += '      continue\n'
    for dgt__vrps in range(pgeol__pxuef):
        nqna__jrmux += f'    ind{dgt__vrps} = indices{dgt__vrps}[i]\n'
    dlpfe__ixs = '(' + ', '.join(f'ind{dgt__vrps}' for dgt__vrps in range(
        pgeol__pxuef)) + ')'
    nqna__jrmux += f'    if {dlpfe__ixs} not in ind_map:\n'
    nqna__jrmux += '      out_ind = len(out_strs)\n'
    nqna__jrmux += f'      ind_map[{dlpfe__ixs}] = out_ind\n'
    jjok__lbmf = "''" if is_overload_none(sep) else 'sep'
    mjeib__twke = ', '.join([f'data{dgt__vrps}[ind{dgt__vrps}]' for
        dgt__vrps in range(pgeol__pxuef)])
    nqna__jrmux += f'      v = {jjok__lbmf}.join([{mjeib__twke}])\n'
    nqna__jrmux += '      out_strs.append(v)\n'
    nqna__jrmux += '    else:\n'
    nqna__jrmux += f'      out_ind = ind_map[{dlpfe__ixs}]\n'
    nqna__jrmux += '    out_indices[i] = out_ind\n'
    nqna__jrmux += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    nqna__jrmux += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False)
"""
    gqa__hdnof = {}
    exec(nqna__jrmux, {'bodo': bodo, 'numba': numba, 'np': np}, gqa__hdnof)
    impl = gqa__hdnof['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    vvmgf__zvyx = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    mmhgd__kdmbx = toty(fromty)
    xergr__etfhm = context.compile_internal(builder, vvmgf__zvyx,
        mmhgd__kdmbx, (val,))
    return impl_ret_new_ref(context, builder, toty, xergr__etfhm)


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    drwy__thj = arr._data
    coo__tuvnf = len(drwy__thj)
    vjwj__tqy = pre_alloc_string_array(coo__tuvnf, -1)
    if regex:
        vcqos__zrpwq = re.compile(pat, flags)
        for dgt__vrps in range(coo__tuvnf):
            if bodo.libs.array_kernels.isna(drwy__thj, dgt__vrps):
                bodo.libs.array_kernels.setna(vjwj__tqy, dgt__vrps)
                continue
            vjwj__tqy[dgt__vrps] = vcqos__zrpwq.sub(repl=repl, string=
                drwy__thj[dgt__vrps])
    else:
        for dgt__vrps in range(coo__tuvnf):
            if bodo.libs.array_kernels.isna(drwy__thj, dgt__vrps):
                bodo.libs.array_kernels.setna(vjwj__tqy, dgt__vrps)
                continue
            vjwj__tqy[dgt__vrps] = drwy__thj[dgt__vrps].replace(pat, repl)
    return init_dict_arr(vjwj__tqy, arr._indices.copy(), arr.
        _has_global_dictionary)


@register_jitable
def str_startswith(arr, pat, na):
    khi__lpall = arr._data
    uobub__wtlxp = len(khi__lpall)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(uobub__wtlxp)
    for dgt__vrps in range(uobub__wtlxp):
        dict_arr_out[dgt__vrps] = khi__lpall[dgt__vrps].startswith(pat)
    tgzsu__ygqcs = arr._indices
    sygki__wurq = len(tgzsu__ygqcs)
    yen__tds = bodo.libs.bool_arr_ext.alloc_bool_array(sygki__wurq)
    for dgt__vrps in range(sygki__wurq):
        if bodo.libs.array_kernels.isna(arr, dgt__vrps):
            bodo.libs.array_kernels.setna(yen__tds, dgt__vrps)
        else:
            yen__tds[dgt__vrps] = dict_arr_out[tgzsu__ygqcs[dgt__vrps]]
    return yen__tds


@register_jitable
def str_endswith(arr, pat, na):
    khi__lpall = arr._data
    uobub__wtlxp = len(khi__lpall)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(uobub__wtlxp)
    for dgt__vrps in range(uobub__wtlxp):
        dict_arr_out[dgt__vrps] = khi__lpall[dgt__vrps].endswith(pat)
    tgzsu__ygqcs = arr._indices
    sygki__wurq = len(tgzsu__ygqcs)
    yen__tds = bodo.libs.bool_arr_ext.alloc_bool_array(sygki__wurq)
    for dgt__vrps in range(sygki__wurq):
        if bodo.libs.array_kernels.isna(arr, dgt__vrps):
            bodo.libs.array_kernels.setna(yen__tds, dgt__vrps)
        else:
            yen__tds[dgt__vrps] = dict_arr_out[tgzsu__ygqcs[dgt__vrps]]
    return yen__tds


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    khi__lpall = arr._data
    pdxf__dcv = pd.Series(khi__lpall)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = pdxf__dcv.array._str_contains(pat, case, flags, na,
            regex)
    tgzsu__ygqcs = arr._indices
    sygki__wurq = len(tgzsu__ygqcs)
    yen__tds = bodo.libs.bool_arr_ext.alloc_bool_array(sygki__wurq)
    for dgt__vrps in range(sygki__wurq):
        if bodo.libs.array_kernels.isna(arr, dgt__vrps):
            bodo.libs.array_kernels.setna(yen__tds, dgt__vrps)
        else:
            yen__tds[dgt__vrps] = dict_arr_out[tgzsu__ygqcs[dgt__vrps]]
    return yen__tds


@register_jitable
def str_contains_non_regex(arr, pat, case):
    khi__lpall = arr._data
    uobub__wtlxp = len(khi__lpall)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(uobub__wtlxp)
    if not case:
        sgac__ktshs = pat.upper()
    for dgt__vrps in range(uobub__wtlxp):
        if case:
            dict_arr_out[dgt__vrps] = pat in khi__lpall[dgt__vrps]
        else:
            dict_arr_out[dgt__vrps] = sgac__ktshs in khi__lpall[dgt__vrps
                ].upper()
    tgzsu__ygqcs = arr._indices
    sygki__wurq = len(tgzsu__ygqcs)
    yen__tds = bodo.libs.bool_arr_ext.alloc_bool_array(sygki__wurq)
    for dgt__vrps in range(sygki__wurq):
        if bodo.libs.array_kernels.isna(arr, dgt__vrps):
            bodo.libs.array_kernels.setna(yen__tds, dgt__vrps)
        else:
            yen__tds[dgt__vrps] = dict_arr_out[tgzsu__ygqcs[dgt__vrps]]
    return yen__tds
