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
    dzpvi__cfs = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        rodc__vcc, = args
        zbka__rff = cgutils.create_struct_proxy(string_type)(context,
            builder, value=rodc__vcc)
        vgyyr__sgh = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        tea__mibn = cgutils.create_struct_proxy(dzpvi__cfs)(context, builder)
        is_ascii = builder.icmp_unsigned('==', zbka__rff.is_ascii, lir.
            Constant(zbka__rff.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (ihg__ugz, oaobk__fzor):
            with ihg__ugz:
                context.nrt.incref(builder, string_type, rodc__vcc)
                vgyyr__sgh.data = zbka__rff.data
                vgyyr__sgh.meminfo = zbka__rff.meminfo
                tea__mibn.f1 = zbka__rff.length
            with oaobk__fzor:
                eufw__zqh = lir.FunctionType(lir.IntType(64), [lir.IntType(
                    8).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                ghyfs__vfu = cgutils.get_or_insert_function(builder.module,
                    eufw__zqh, name='unicode_to_utf8')
                ncvvu__hfvkl = context.get_constant_null(types.voidptr)
                gaz__xqh = builder.call(ghyfs__vfu, [ncvvu__hfvkl,
                    zbka__rff.data, zbka__rff.length, zbka__rff.kind])
                tea__mibn.f1 = gaz__xqh
                ygx__kat = builder.add(gaz__xqh, lir.Constant(lir.IntType(
                    64), 1))
                vgyyr__sgh.meminfo = context.nrt.meminfo_alloc_aligned(builder,
                    size=ygx__kat, align=32)
                vgyyr__sgh.data = context.nrt.meminfo_data(builder,
                    vgyyr__sgh.meminfo)
                builder.call(ghyfs__vfu, [vgyyr__sgh.data, zbka__rff.data,
                    zbka__rff.length, zbka__rff.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    vgyyr__sgh.data, [gaz__xqh]))
        tea__mibn.f0 = vgyyr__sgh._getvalue()
        return tea__mibn._getvalue()
    return dzpvi__cfs(string_type), codegen


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
        eufw__zqh = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        xejp__hsl = cgutils.get_or_insert_function(builder.module,
            eufw__zqh, name='memcmp')
        return builder.call(xejp__hsl, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    bgvf__rmoun = n(10)

    def impl(n):
        if n == 0:
            return 1
        wsal__hxyh = 0
        if n < 0:
            n = -n
            wsal__hxyh += 1
        while n > 0:
            n = n // bgvf__rmoun
            wsal__hxyh += 1
        return wsal__hxyh
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
        [ejxr__muk] = args
        if isinstance(ejxr__muk, StdStringType):
            return signature(types.float64, ejxr__muk)
        if ejxr__muk == string_type:
            return signature(types.float64, ejxr__muk)


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
    zbka__rff = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    eufw__zqh = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer(), lir.IntType(64)])
    nzq__nlk = cgutils.get_or_insert_function(builder.module, eufw__zqh,
        name='init_string_const')
    return builder.call(nzq__nlk, [zbka__rff.data, zbka__rff.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        lgx__dcea = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(lgx__dcea._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return lgx__dcea
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    zbka__rff = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return zbka__rff.data


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
        tzl__xpt = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, tzl__xpt)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        xwmy__lthk, = args
        iij__oki = types.List(string_type)
        wsgaq__drcr = numba.cpython.listobj.ListInstance.allocate(context,
            builder, iij__oki, xwmy__lthk)
        wsgaq__drcr.size = xwmy__lthk
        xth__iuuug = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        xth__iuuug.data = wsgaq__drcr.value
        return xth__iuuug._getvalue()
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
            vhno__ceue = 0
            blygp__gwn = v
            if blygp__gwn < 0:
                vhno__ceue = 1
                blygp__gwn = -blygp__gwn
            if blygp__gwn < 1:
                gui__lxxx = 1
            else:
                gui__lxxx = 1 + int(np.floor(np.log10(blygp__gwn)))
            length = vhno__ceue + gui__lxxx + 1 + 6
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
    eufw__zqh = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).
        as_pointer()])
    nzq__nlk = cgutils.get_or_insert_function(builder.module, eufw__zqh,
        name='str_to_float64')
    res = builder.call(nzq__nlk, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    eufw__zqh = lir.FunctionType(lir.FloatType(), [lir.IntType(8).as_pointer()]
        )
    nzq__nlk = cgutils.get_or_insert_function(builder.module, eufw__zqh,
        name='str_to_float32')
    res = builder.call(nzq__nlk, (val,))
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
    zbka__rff = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    eufw__zqh = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    nzq__nlk = cgutils.get_or_insert_function(builder.module, eufw__zqh,
        name='str_to_int64')
    res = builder.call(nzq__nlk, (zbka__rff.data, zbka__rff.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    zbka__rff = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    eufw__zqh = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    nzq__nlk = cgutils.get_or_insert_function(builder.module, eufw__zqh,
        name='str_to_uint64')
    res = builder.call(nzq__nlk, (zbka__rff.data, zbka__rff.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        oiqpl__yfijs = ', '.join('e{}'.format(fxznr__swm) for fxznr__swm in
            range(len(args)))
        if oiqpl__yfijs:
            oiqpl__yfijs += ', '
        lmo__ktwrv = ', '.join("{} = ''".format(a) for a in kws.keys())
        gib__omohg = f'def format_stub(string, {oiqpl__yfijs} {lmo__ktwrv}):\n'
        gib__omohg += '    pass\n'
        pfk__zbko = {}
        exec(gib__omohg, {}, pfk__zbko)
        emnsp__fvwml = pfk__zbko['format_stub']
        nyq__zyq = numba.core.utils.pysignature(emnsp__fvwml)
        dae__vkri = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, dae__vkri).replace(pysig=nyq__zyq)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    goy__nmkm = pat is not None and len(pat) > 1
    if goy__nmkm:
        wkmrf__nduwp = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    wsgaq__drcr = len(arr)
    nmczl__tudcp = 0
    bdpar__jevjh = 0
    for fxznr__swm in numba.parfors.parfor.internal_prange(wsgaq__drcr):
        if bodo.libs.array_kernels.isna(arr, fxznr__swm):
            continue
        if goy__nmkm:
            jon__ipk = wkmrf__nduwp.split(arr[fxznr__swm], maxsplit=n)
        elif pat == '':
            jon__ipk = [''] + list(arr[fxznr__swm]) + ['']
        else:
            jon__ipk = arr[fxznr__swm].split(pat, n)
        nmczl__tudcp += len(jon__ipk)
        for s in jon__ipk:
            bdpar__jevjh += bodo.libs.str_arr_ext.get_utf8_size(s)
    ssxj__qzfre = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        wsgaq__drcr, (nmczl__tudcp, bdpar__jevjh), bodo.libs.str_arr_ext.
        string_array_type)
    somp__ctr = bodo.libs.array_item_arr_ext.get_offsets(ssxj__qzfre)
    qnwt__lltc = bodo.libs.array_item_arr_ext.get_null_bitmap(ssxj__qzfre)
    mxvv__mpl = bodo.libs.array_item_arr_ext.get_data(ssxj__qzfre)
    rck__jaemj = 0
    for hnj__xhcpy in numba.parfors.parfor.internal_prange(wsgaq__drcr):
        somp__ctr[hnj__xhcpy] = rck__jaemj
        if bodo.libs.array_kernels.isna(arr, hnj__xhcpy):
            bodo.libs.int_arr_ext.set_bit_to_arr(qnwt__lltc, hnj__xhcpy, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(qnwt__lltc, hnj__xhcpy, 1)
        if goy__nmkm:
            jon__ipk = wkmrf__nduwp.split(arr[hnj__xhcpy], maxsplit=n)
        elif pat == '':
            jon__ipk = [''] + list(arr[hnj__xhcpy]) + ['']
        else:
            jon__ipk = arr[hnj__xhcpy].split(pat, n)
        yws__ihl = len(jon__ipk)
        for jxig__bpvo in range(yws__ihl):
            s = jon__ipk[jxig__bpvo]
            mxvv__mpl[rck__jaemj] = s
            rck__jaemj += 1
    somp__ctr[wsgaq__drcr] = rck__jaemj
    return ssxj__qzfre


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                pdwlc__axhse = '-0x'
                x = x * -1
            else:
                pdwlc__axhse = '0x'
            x = np.uint64(x)
            if x == 0:
                urp__ewbye = 1
            else:
                urp__ewbye = fast_ceil_log2(x + 1)
                urp__ewbye = (urp__ewbye + 3) // 4
            length = len(pdwlc__axhse) + urp__ewbye
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, pdwlc__axhse._data,
                len(pdwlc__axhse), 1)
            int_to_hex(output, urp__ewbye, len(pdwlc__axhse), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    hngoe__mkbj = 0 if x & x - 1 == 0 else 1
    xwctw__rdzoq = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    ganmx__olo = 32
    for fxznr__swm in range(len(xwctw__rdzoq)):
        ckbj__eiw = 0 if x & xwctw__rdzoq[fxznr__swm] == 0 else ganmx__olo
        hngoe__mkbj = hngoe__mkbj + ckbj__eiw
        x = x >> ckbj__eiw
        ganmx__olo = ganmx__olo >> 1
    return hngoe__mkbj


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        qjl__gprxs = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        eufw__zqh = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        gcctb__ipuv = cgutils.get_or_insert_function(builder.module,
            eufw__zqh, name='int_to_hex')
        vyfp__noy = builder.inttoptr(builder.add(builder.ptrtoint(
            qjl__gprxs.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(gcctb__ipuv, (vyfp__noy, out_len, int_val))
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
