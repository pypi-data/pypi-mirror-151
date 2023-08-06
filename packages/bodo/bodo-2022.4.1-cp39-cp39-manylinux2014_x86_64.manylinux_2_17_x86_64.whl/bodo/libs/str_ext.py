import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_getattr, infer_global, signature
from numba.extending import intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_str, is_overload_constant_int, is_overload_constant_str


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


ll.add_symbol('del_str', hstr_ext.del_str)
ll.add_symbol('unicode_to_utf8', hstr_ext.unicode_to_utf8)
ll.add_symbol('memcmp', hstr_ext.memcmp)
ll.add_symbol('int_to_hex', hstr_ext.int_to_hex)
string_type = types.unicode_type


@numba.njit
def contains_regex(e, in_str):
    with numba.objmode(res='bool_'):
        res = bool(e.search(in_str))
    return res


@numba.generated_jit
def str_findall_count(regex, in_str):

    def _str_findall_count_impl(regex, in_str):
        with numba.objmode(res='int64'):
            res = len(regex.findall(in_str))
        return res
    return _str_findall_count_impl


utf8_str_type = types.ArrayCTypes(types.Array(types.uint8, 1, 'C'))


@intrinsic
def unicode_to_utf8_and_len(typingctx, str_typ=None):
    assert str_typ in (string_type, types.Optional(string_type)) or isinstance(
        str_typ, types.StringLiteral)
    njmq__icxrk = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        zlz__bwk, = args
        itv__whfhb = cgutils.create_struct_proxy(string_type)(context,
            builder, value=zlz__bwk)
        lutkj__yumu = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        hwlp__gbb = cgutils.create_struct_proxy(njmq__icxrk)(context, builder)
        is_ascii = builder.icmp_unsigned('==', itv__whfhb.is_ascii, lir.
            Constant(itv__whfhb.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (zthxx__ctzyo, waru__iodu):
            with zthxx__ctzyo:
                context.nrt.incref(builder, string_type, zlz__bwk)
                lutkj__yumu.data = itv__whfhb.data
                lutkj__yumu.meminfo = itv__whfhb.meminfo
                hwlp__gbb.f1 = itv__whfhb.length
            with waru__iodu:
                uay__xcgm = lir.FunctionType(lir.IntType(64), [lir.IntType(
                    8).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                bfm__tkcsd = cgutils.get_or_insert_function(builder.module,
                    uay__xcgm, name='unicode_to_utf8')
                fjzyu__ixq = context.get_constant_null(types.voidptr)
                pjkan__eergy = builder.call(bfm__tkcsd, [fjzyu__ixq,
                    itv__whfhb.data, itv__whfhb.length, itv__whfhb.kind])
                hwlp__gbb.f1 = pjkan__eergy
                tgq__wvst = builder.add(pjkan__eergy, lir.Constant(lir.
                    IntType(64), 1))
                lutkj__yumu.meminfo = context.nrt.meminfo_alloc_aligned(builder
                    , size=tgq__wvst, align=32)
                lutkj__yumu.data = context.nrt.meminfo_data(builder,
                    lutkj__yumu.meminfo)
                builder.call(bfm__tkcsd, [lutkj__yumu.data, itv__whfhb.data,
                    itv__whfhb.length, itv__whfhb.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    lutkj__yumu.data, [pjkan__eergy]))
        hwlp__gbb.f0 = lutkj__yumu._getvalue()
        return hwlp__gbb._getvalue()
    return njmq__icxrk(string_type), codegen


def unicode_to_utf8(s):
    return s


@overload(unicode_to_utf8)
def overload_unicode_to_utf8(s):
    return lambda s: unicode_to_utf8_and_len(s)[0]


@overload(max)
def overload_builtin_max(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload(min)
def overload_builtin_min(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@intrinsic
def memcmp(typingctx, dest_t, src_t, count_t=None):

    def codegen(context, builder, sig, args):
        uay__xcgm = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        ljci__rteiu = cgutils.get_or_insert_function(builder.module,
            uay__xcgm, name='memcmp')
        return builder.call(ljci__rteiu, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    zidx__zfrn = n(10)

    def impl(n):
        if n == 0:
            return 1
        uwm__cniy = 0
        if n < 0:
            n = -n
            uwm__cniy += 1
        while n > 0:
            n = n // zidx__zfrn
            uwm__cniy += 1
        return uwm__cniy
    return impl


class StdStringType(types.Opaque):

    def __init__(self):
        super(StdStringType, self).__init__(name='StdStringType')


std_str_type = StdStringType()
register_model(StdStringType)(models.OpaqueModel)
del_str = types.ExternalFunction('del_str', types.void(std_str_type))
get_c_str = types.ExternalFunction('get_c_str', types.voidptr(std_str_type))
dummy_use = numba.njit(lambda a: None)


@overload(int)
def int_str_overload(in_str, base=10):
    if in_str == string_type:
        if is_overload_constant_int(base) and get_overload_const_int(base
            ) == 10:

            def _str_to_int_impl(in_str, base=10):
                val = _str_to_int64(in_str._data, in_str._length)
                dummy_use(in_str)
                return val
            return _str_to_int_impl

        def _str_to_int_base_impl(in_str, base=10):
            val = _str_to_int64_base(in_str._data, in_str._length, base)
            dummy_use(in_str)
            return val
        return _str_to_int_base_impl


@infer_global(float)
class StrToFloat(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        [skblt__qzq] = args
        if isinstance(skblt__qzq, StdStringType):
            return signature(types.float64, skblt__qzq)
        if skblt__qzq == string_type:
            return signature(types.float64, skblt__qzq)


ll.add_symbol('init_string_const', hstr_ext.init_string_const)
ll.add_symbol('get_c_str', hstr_ext.get_c_str)
ll.add_symbol('str_to_int64', hstr_ext.str_to_int64)
ll.add_symbol('str_to_uint64', hstr_ext.str_to_uint64)
ll.add_symbol('str_to_int64_base', hstr_ext.str_to_int64_base)
ll.add_symbol('str_to_float64', hstr_ext.str_to_float64)
ll.add_symbol('str_to_float32', hstr_ext.str_to_float32)
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('str_from_float32', hstr_ext.str_from_float32)
ll.add_symbol('str_from_float64', hstr_ext.str_from_float64)
get_std_str_len = types.ExternalFunction('get_str_len', signature(types.
    intp, std_str_type))
init_string_from_chars = types.ExternalFunction('init_string_const',
    std_str_type(types.voidptr, types.intp))
_str_to_int64 = types.ExternalFunction('str_to_int64', signature(types.
    int64, types.voidptr, types.int64))
_str_to_uint64 = types.ExternalFunction('str_to_uint64', signature(types.
    uint64, types.voidptr, types.int64))
_str_to_int64_base = types.ExternalFunction('str_to_int64_base', signature(
    types.int64, types.voidptr, types.int64, types.int64))


def gen_unicode_to_std_str(context, builder, unicode_val):
    itv__whfhb = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    uay__xcgm = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer(), lir.IntType(64)])
    jykce__inb = cgutils.get_or_insert_function(builder.module, uay__xcgm,
        name='init_string_const')
    return builder.call(jykce__inb, [itv__whfhb.data, itv__whfhb.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        omt__dlkc = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(omt__dlkc._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return omt__dlkc
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    itv__whfhb = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return itv__whfhb.data


@intrinsic
def unicode_to_std_str(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_unicode_to_std_str(context, builder, args[0])
    return std_str_type(string_type), codegen


@intrinsic
def std_str_to_unicode(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_std_str_to_unicode(context, builder, args[0], True)
    return string_type(std_str_type), codegen


class RandomAccessStringArrayType(types.ArrayCompatible):

    def __init__(self):
        super(RandomAccessStringArrayType, self).__init__(name=
            'RandomAccessStringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    def copy(self):
        RandomAccessStringArrayType()


random_access_string_array = RandomAccessStringArrayType()


@register_model(RandomAccessStringArrayType)
class RandomAccessStringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        rzz__ocngo = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, rzz__ocngo)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        oeoom__uvvp, = args
        eby__lxei = types.List(string_type)
        famep__nlqx = numba.cpython.listobj.ListInstance.allocate(context,
            builder, eby__lxei, oeoom__uvvp)
        famep__nlqx.size = oeoom__uvvp
        loelp__urez = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        loelp__urez.data = famep__nlqx.value
        return loelp__urez._getvalue()
    return random_access_string_array(types.intp), codegen


@overload(operator.getitem, no_unliteral=True)
def random_access_str_arr_getitem(A, ind):
    if A != random_access_string_array:
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]


@overload(operator.setitem)
def random_access_str_arr_setitem(A, idx, val):
    if A != random_access_string_array:
        return
    if isinstance(idx, types.Integer):
        assert val == string_type

        def impl_scalar(A, idx, val):
            A._data[idx] = val
        return impl_scalar


@overload(len, no_unliteral=True)
def overload_str_arr_len(A):
    if A == random_access_string_array:
        return lambda A: len(A._data)


@overload_attribute(RandomAccessStringArrayType, 'shape')
def overload_str_arr_shape(A):
    return lambda A: (len(A._data),)


def alloc_random_access_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_str_ext_alloc_random_access_string_array
    ) = alloc_random_access_str_arr_equiv
str_from_float32 = types.ExternalFunction('str_from_float32', types.void(
    types.voidptr, types.float32))
str_from_float64 = types.ExternalFunction('str_from_float64', types.void(
    types.voidptr, types.float64))


def float_to_str(s, v):
    pass


@overload(float_to_str)
def float_to_str_overload(s, v):
    assert isinstance(v, types.Float)
    if v == types.float32:
        return lambda s, v: str_from_float32(s._data, v)
    return lambda s, v: str_from_float64(s._data, v)


@overload(str)
def float_str_overload(v):
    if isinstance(v, types.Float):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(v):
            if v == 0:
                return '0.0'
            wefcj__rya = 0
            imzrq__bzzn = v
            if imzrq__bzzn < 0:
                wefcj__rya = 1
                imzrq__bzzn = -imzrq__bzzn
            if imzrq__bzzn < 1:
                wgw__vfcn = 1
            else:
                wgw__vfcn = 1 + int(np.floor(np.log10(imzrq__bzzn)))
            length = wefcj__rya + wgw__vfcn + 1 + 6
            s = numba.cpython.unicode._malloc_string(kind, 1, length, True)
            float_to_str(s, v)
            return s
        return impl


@overload(format, no_unliteral=True)
def overload_format(value, format_spec=''):
    if is_overload_constant_str(format_spec) and get_overload_const_str(
        format_spec) == '':

        def impl_fast(value, format_spec=''):
            return str(value)
        return impl_fast

    def impl(value, format_spec=''):
        with numba.objmode(res='string'):
            res = format(value, format_spec)
        return res
    return impl


@lower_cast(StdStringType, types.float64)
def cast_str_to_float64(context, builder, fromty, toty, val):
    uay__xcgm = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).
        as_pointer()])
    jykce__inb = cgutils.get_or_insert_function(builder.module, uay__xcgm,
        name='str_to_float64')
    res = builder.call(jykce__inb, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    uay__xcgm = lir.FunctionType(lir.FloatType(), [lir.IntType(8).as_pointer()]
        )
    jykce__inb = cgutils.get_or_insert_function(builder.module, uay__xcgm,
        name='str_to_float32')
    res = builder.call(jykce__inb, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.float64)
def cast_unicode_str_to_float64(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float64(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.float32)
def cast_unicode_str_to_float32(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float32(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.int64)
@lower_cast(string_type, types.int32)
@lower_cast(string_type, types.int16)
@lower_cast(string_type, types.int8)
def cast_unicode_str_to_int64(context, builder, fromty, toty, val):
    itv__whfhb = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    uay__xcgm = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    jykce__inb = cgutils.get_or_insert_function(builder.module, uay__xcgm,
        name='str_to_int64')
    res = builder.call(jykce__inb, (itv__whfhb.data, itv__whfhb.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    itv__whfhb = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    uay__xcgm = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    jykce__inb = cgutils.get_or_insert_function(builder.module, uay__xcgm,
        name='str_to_uint64')
    res = builder.call(jykce__inb, (itv__whfhb.data, itv__whfhb.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        yvjqg__pxrjq = ', '.join('e{}'.format(kjo__gbjia) for kjo__gbjia in
            range(len(args)))
        if yvjqg__pxrjq:
            yvjqg__pxrjq += ', '
        yeoc__vkoal = ', '.join("{} = ''".format(a) for a in kws.keys())
        kawi__mysv = (
            f'def format_stub(string, {yvjqg__pxrjq} {yeoc__vkoal}):\n')
        kawi__mysv += '    pass\n'
        ewbsl__yuopr = {}
        exec(kawi__mysv, {}, ewbsl__yuopr)
        iimaj__ksal = ewbsl__yuopr['format_stub']
        zmt__ixl = numba.core.utils.pysignature(iimaj__ksal)
        aoku__fpmh = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, aoku__fpmh).replace(pysig=zmt__ixl)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    yuhhm__lrsk = pat is not None and len(pat) > 1
    if yuhhm__lrsk:
        xudgc__izztu = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    famep__nlqx = len(arr)
    wha__dxtdm = 0
    zhoun__rzskd = 0
    for kjo__gbjia in numba.parfors.parfor.internal_prange(famep__nlqx):
        if bodo.libs.array_kernels.isna(arr, kjo__gbjia):
            continue
        if yuhhm__lrsk:
            dgk__mdjyb = xudgc__izztu.split(arr[kjo__gbjia], maxsplit=n)
        elif pat == '':
            dgk__mdjyb = [''] + list(arr[kjo__gbjia]) + ['']
        else:
            dgk__mdjyb = arr[kjo__gbjia].split(pat, n)
        wha__dxtdm += len(dgk__mdjyb)
        for s in dgk__mdjyb:
            zhoun__rzskd += bodo.libs.str_arr_ext.get_utf8_size(s)
    lpqja__korki = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        famep__nlqx, (wha__dxtdm, zhoun__rzskd), bodo.libs.str_arr_ext.
        string_array_type)
    kojvr__ectac = bodo.libs.array_item_arr_ext.get_offsets(lpqja__korki)
    vomdq__dqa = bodo.libs.array_item_arr_ext.get_null_bitmap(lpqja__korki)
    tjwpj__ffq = bodo.libs.array_item_arr_ext.get_data(lpqja__korki)
    jyuvo__rho = 0
    for ztlvo__lkng in numba.parfors.parfor.internal_prange(famep__nlqx):
        kojvr__ectac[ztlvo__lkng] = jyuvo__rho
        if bodo.libs.array_kernels.isna(arr, ztlvo__lkng):
            bodo.libs.int_arr_ext.set_bit_to_arr(vomdq__dqa, ztlvo__lkng, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(vomdq__dqa, ztlvo__lkng, 1)
        if yuhhm__lrsk:
            dgk__mdjyb = xudgc__izztu.split(arr[ztlvo__lkng], maxsplit=n)
        elif pat == '':
            dgk__mdjyb = [''] + list(arr[ztlvo__lkng]) + ['']
        else:
            dgk__mdjyb = arr[ztlvo__lkng].split(pat, n)
        gtm__wdcmp = len(dgk__mdjyb)
        for mtc__djysg in range(gtm__wdcmp):
            s = dgk__mdjyb[mtc__djysg]
            tjwpj__ffq[jyuvo__rho] = s
            jyuvo__rho += 1
    kojvr__ectac[famep__nlqx] = jyuvo__rho
    return lpqja__korki


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                ylnl__krmo = '-0x'
                x = x * -1
            else:
                ylnl__krmo = '0x'
            x = np.uint64(x)
            if x == 0:
                zyco__musb = 1
            else:
                zyco__musb = fast_ceil_log2(x + 1)
                zyco__musb = (zyco__musb + 3) // 4
            length = len(ylnl__krmo) + zyco__musb
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, ylnl__krmo._data,
                len(ylnl__krmo), 1)
            int_to_hex(output, zyco__musb, len(ylnl__krmo), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    nev__wsi = 0 if x & x - 1 == 0 else 1
    ivouy__zcnh = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    syyzn__ppw = 32
    for kjo__gbjia in range(len(ivouy__zcnh)):
        tgojd__ishrj = 0 if x & ivouy__zcnh[kjo__gbjia] == 0 else syyzn__ppw
        nev__wsi = nev__wsi + tgojd__ishrj
        x = x >> tgojd__ishrj
        syyzn__ppw = syyzn__ppw >> 1
    return nev__wsi


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        huilu__qcarv = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        uay__xcgm = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        lcpr__cur = cgutils.get_or_insert_function(builder.module,
            uay__xcgm, name='int_to_hex')
        hjt__aqo = builder.inttoptr(builder.add(builder.ptrtoint(
            huilu__qcarv.data, lir.IntType(64)), header_len), lir.IntType(8
            ).as_pointer())
        builder.call(lcpr__cur, (hjt__aqo, out_len, int_val))
    return types.void(output, out_len, header_len, int_val), codegen


def alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    pass


@overload(alloc_empty_bytes_or_string_data)
def overload_alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    typ = typ.instance_type if isinstance(typ, types.TypeRef) else typ
    if typ == bodo.bytes_type:
        return lambda typ, kind, length, is_ascii=0: np.empty(length, np.uint8)
    if typ == string_type:
        return (lambda typ, kind, length, is_ascii=0: numba.cpython.unicode
            ._empty_string(kind, length, is_ascii))
    raise BodoError(
        f'Internal Error: Expected Bytes or String type, found {typ}')


def get_unicode_or_numpy_data(val):
    pass


@overload(get_unicode_or_numpy_data)
def overload_get_unicode_or_numpy_data(val):
    if val == string_type:
        return lambda val: val._data
    if isinstance(val, types.Array):
        return lambda val: val.ctypes
    raise BodoError(
        f'Internal Error: Expected String or Numpy Array, found {val}')
