"""Table data type for storing dataframe column arrays. Supports storing many columns
(e.g. >10k) efficiently.
"""
import operator
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.parfors.array_analysis import ArrayAnalysis
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.typing import BodoError, decode_if_dict_array, get_overload_const_int, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_true, to_str_arr_if_dict_array


class Table:

    def __init__(self, arrs, usecols=None, num_arrs=-1):
        if usecols is not None:
            assert num_arrs != -1, 'num_arrs must be provided if usecols is not None'
            ggm__ndd = 0
            fzvx__ndn = []
            for i in range(usecols[-1] + 1):
                if i == usecols[ggm__ndd]:
                    fzvx__ndn.append(arrs[ggm__ndd])
                    ggm__ndd += 1
                else:
                    fzvx__ndn.append(None)
            for qyck__ofaz in range(usecols[-1] + 1, num_arrs):
                fzvx__ndn.append(None)
            self.arrays = fzvx__ndn
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((tfdaf__fabj == yib__joxu).all() for 
            tfdaf__fabj, yib__joxu in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        ddv__eci = len(self.arrays)
        jrwme__uquf = dict(zip(range(ddv__eci), self.arrays))
        df = pd.DataFrame(jrwme__uquf, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        qdtq__vesc = []
        eqt__nucz = []
        pzcon__tlbui = {}
        okrg__usbc = defaultdict(int)
        dydt__huuha = defaultdict(list)
        if not has_runtime_cols:
            for i, jtzu__rgt in enumerate(arr_types):
                if jtzu__rgt not in pzcon__tlbui:
                    pzcon__tlbui[jtzu__rgt] = len(pzcon__tlbui)
                gmgqb__dwgea = pzcon__tlbui[jtzu__rgt]
                qdtq__vesc.append(gmgqb__dwgea)
                eqt__nucz.append(okrg__usbc[gmgqb__dwgea])
                okrg__usbc[gmgqb__dwgea] += 1
                dydt__huuha[gmgqb__dwgea].append(i)
        self.block_nums = qdtq__vesc
        self.block_offsets = eqt__nucz
        self.type_to_blk = pzcon__tlbui
        self.block_to_arr_ind = dydt__huuha
        super(TableType, self).__init__(name=
            f'TableType({arr_types}, {has_runtime_cols})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return self.arr_types, self.has_runtime_cols

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(Table)
def typeof_table(val, c):
    return TableType(tuple(numba.typeof(yhnep__ctdnf) for yhnep__ctdnf in
        val.arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            zhue__vspqc = [(f'block_{i}', types.List(jtzu__rgt)) for i,
                jtzu__rgt in enumerate(fe_type.arr_types)]
        else:
            zhue__vspqc = [(f'block_{gmgqb__dwgea}', types.List(jtzu__rgt)) for
                jtzu__rgt, gmgqb__dwgea in fe_type.type_to_blk.items()]
        zhue__vspqc.append(('parent', types.pyobject))
        zhue__vspqc.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, zhue__vspqc)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    mfipz__qllq = c.pyapi.object_getattr_string(val, 'arrays')
    hpeuz__nqmxn = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    hpeuz__nqmxn.parent = cgutils.get_null_value(hpeuz__nqmxn.parent.type)
    dvy__vrlmo = c.pyapi.make_none()
    zzvxy__gzj = c.context.get_constant(types.int64, 0)
    ybfwb__mpln = cgutils.alloca_once_value(c.builder, zzvxy__gzj)
    for jtzu__rgt, gmgqb__dwgea in typ.type_to_blk.items():
        kawc__pbyo = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[gmgqb__dwgea]))
        qyck__ofaz, newok__ckeem = ListInstance.allocate_ex(c.context, c.
            builder, types.List(jtzu__rgt), kawc__pbyo)
        newok__ckeem.size = kawc__pbyo
        puvz__keg = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[
            gmgqb__dwgea], dtype=np.int64))
        aixp__wlre = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, puvz__keg)
        with cgutils.for_range(c.builder, kawc__pbyo) as rfq__jwif:
            i = rfq__jwif.index
            cxgv__ithdu = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), aixp__wlre, i)
            tfsoi__yls = c.pyapi.long_from_longlong(cxgv__ithdu)
            kwj__int = c.pyapi.object_getitem(mfipz__qllq, tfsoi__yls)
            pcbl__ryb = c.builder.icmp_unsigned('==', kwj__int, dvy__vrlmo)
            with c.builder.if_else(pcbl__ryb) as (foau__sgs, ehfyn__bgr):
                with foau__sgs:
                    yfe__nydut = c.context.get_constant_null(jtzu__rgt)
                    newok__ckeem.inititem(i, yfe__nydut, incref=False)
                with ehfyn__bgr:
                    olr__kawh = c.pyapi.call_method(kwj__int, '__len__', ())
                    gmed__xfrud = c.pyapi.long_as_longlong(olr__kawh)
                    c.builder.store(gmed__xfrud, ybfwb__mpln)
                    c.pyapi.decref(olr__kawh)
                    yhnep__ctdnf = c.pyapi.to_native_value(jtzu__rgt, kwj__int
                        ).value
                    newok__ckeem.inititem(i, yhnep__ctdnf, incref=False)
            c.pyapi.decref(kwj__int)
            c.pyapi.decref(tfsoi__yls)
        setattr(hpeuz__nqmxn, f'block_{gmgqb__dwgea}', newok__ckeem.value)
    hpeuz__nqmxn.len = c.builder.load(ybfwb__mpln)
    c.pyapi.decref(mfipz__qllq)
    c.pyapi.decref(dvy__vrlmo)
    bfxw__lybo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hpeuz__nqmxn._getvalue(), is_error=bfxw__lybo)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    hpeuz__nqmxn = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        ebie__pnk = c.context.get_constant(types.int64, 0)
        for i, jtzu__rgt in enumerate(typ.arr_types):
            fzvx__ndn = getattr(hpeuz__nqmxn, f'block_{i}')
            ysu__lkkmq = ListInstance(c.context, c.builder, types.List(
                jtzu__rgt), fzvx__ndn)
            ebie__pnk = c.builder.add(ebie__pnk, ysu__lkkmq.size)
        nir__mqv = c.pyapi.list_new(ebie__pnk)
        mol__hyt = c.context.get_constant(types.int64, 0)
        for i, jtzu__rgt in enumerate(typ.arr_types):
            fzvx__ndn = getattr(hpeuz__nqmxn, f'block_{i}')
            ysu__lkkmq = ListInstance(c.context, c.builder, types.List(
                jtzu__rgt), fzvx__ndn)
            with cgutils.for_range(c.builder, ysu__lkkmq.size) as rfq__jwif:
                i = rfq__jwif.index
                yhnep__ctdnf = ysu__lkkmq.getitem(i)
                c.context.nrt.incref(c.builder, jtzu__rgt, yhnep__ctdnf)
                idx = c.builder.add(mol__hyt, i)
                c.pyapi.list_setitem(nir__mqv, idx, c.pyapi.
                    from_native_value(jtzu__rgt, yhnep__ctdnf, c.env_manager))
            mol__hyt = c.builder.add(mol__hyt, ysu__lkkmq.size)
        iueot__pavna = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        nnn__ldg = c.pyapi.call_function_objargs(iueot__pavna, (nir__mqv,))
        c.pyapi.decref(iueot__pavna)
        c.pyapi.decref(nir__mqv)
        c.context.nrt.decref(c.builder, typ, val)
        return nnn__ldg
    nir__mqv = c.pyapi.list_new(c.context.get_constant(types.int64, len(typ
        .arr_types)))
    yyzs__twf = cgutils.is_not_null(c.builder, hpeuz__nqmxn.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for jtzu__rgt, gmgqb__dwgea in typ.type_to_blk.items():
        fzvx__ndn = getattr(hpeuz__nqmxn, f'block_{gmgqb__dwgea}')
        ysu__lkkmq = ListInstance(c.context, c.builder, types.List(
            jtzu__rgt), fzvx__ndn)
        puvz__keg = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[
            gmgqb__dwgea], dtype=np.int64))
        aixp__wlre = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, puvz__keg)
        with cgutils.for_range(c.builder, ysu__lkkmq.size) as rfq__jwif:
            i = rfq__jwif.index
            cxgv__ithdu = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), aixp__wlre, i)
            yhnep__ctdnf = ysu__lkkmq.getitem(i)
            siyx__cbyik = cgutils.alloca_once_value(c.builder, yhnep__ctdnf)
            wvjz__brrt = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(jtzu__rgt))
            qshn__fdlln = is_ll_eq(c.builder, siyx__cbyik, wvjz__brrt)
            with c.builder.if_else(c.builder.and_(qshn__fdlln, c.builder.
                not_(ensure_unboxed))) as (foau__sgs, ehfyn__bgr):
                with foau__sgs:
                    dvy__vrlmo = c.pyapi.make_none()
                    c.pyapi.list_setitem(nir__mqv, cxgv__ithdu, dvy__vrlmo)
                with ehfyn__bgr:
                    kwj__int = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(qshn__fdlln,
                        yyzs__twf)) as (umoxt__soyfq, rrk__gqvo):
                        with umoxt__soyfq:
                            pyko__rmy = get_df_obj_column_codegen(c.context,
                                c.builder, c.pyapi, hpeuz__nqmxn.parent,
                                cxgv__ithdu, jtzu__rgt)
                            c.builder.store(pyko__rmy, kwj__int)
                        with rrk__gqvo:
                            c.context.nrt.incref(c.builder, jtzu__rgt,
                                yhnep__ctdnf)
                            c.builder.store(c.pyapi.from_native_value(
                                jtzu__rgt, yhnep__ctdnf, c.env_manager),
                                kwj__int)
                    c.pyapi.list_setitem(nir__mqv, cxgv__ithdu, c.builder.
                        load(kwj__int))
    iueot__pavna = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    nnn__ldg = c.pyapi.call_function_objargs(iueot__pavna, (nir__mqv,))
    c.pyapi.decref(iueot__pavna)
    c.pyapi.decref(nir__mqv)
    c.context.nrt.decref(c.builder, typ, val)
    return nnn__ldg


@lower_builtin(len, TableType)
def table_len_lower(context, builder, sig, args):
    impl = table_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def table_len_overload(T):
    if not isinstance(T, TableType):
        return

    def impl(T):
        return T._len
    return impl


@lower_getattr(TableType, 'shape')
def lower_table_shape(context, builder, typ, val):
    impl = table_shape_overload(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def table_shape_overload(T):
    if T.has_runtime_cols:

        def impl(T):
            return T._len, compute_num_runtime_columns(T)
        return impl
    ncols = len(T.arr_types)
    return lambda T: (T._len, types.int64(ncols))


@intrinsic
def compute_num_runtime_columns(typingctx, table_type):
    assert isinstance(table_type, TableType)

    def codegen(context, builder, sig, args):
        table_arg, = args
        hpeuz__nqmxn = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        nbu__qnmq = context.get_constant(types.int64, 0)
        for i, jtzu__rgt in enumerate(table_type.arr_types):
            fzvx__ndn = getattr(hpeuz__nqmxn, f'block_{i}')
            ysu__lkkmq = ListInstance(context, builder, types.List(
                jtzu__rgt), fzvx__ndn)
            nbu__qnmq = builder.add(nbu__qnmq, ysu__lkkmq.size)
        return nbu__qnmq
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    hpeuz__nqmxn = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    gmgqb__dwgea = table_type.block_nums[col_ind]
    doagz__qfx = table_type.block_offsets[col_ind]
    fzvx__ndn = getattr(hpeuz__nqmxn, f'block_{gmgqb__dwgea}')
    ysu__lkkmq = ListInstance(context, builder, types.List(arr_type), fzvx__ndn
        )
    yhnep__ctdnf = ysu__lkkmq.getitem(doagz__qfx)
    return yhnep__ctdnf


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, qyck__ofaz = args
        yhnep__ctdnf = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, yhnep__ctdnf)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, qyck__ofaz = args
        hpeuz__nqmxn = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        gmgqb__dwgea = table_type.block_nums[col_ind]
        doagz__qfx = table_type.block_offsets[col_ind]
        fzvx__ndn = getattr(hpeuz__nqmxn, f'block_{gmgqb__dwgea}')
        ysu__lkkmq = ListInstance(context, builder, types.List(arr_type),
            fzvx__ndn)
        yhnep__ctdnf = ysu__lkkmq.getitem(doagz__qfx)
        context.nrt.decref(builder, arr_type, yhnep__ctdnf)
        yfe__nydut = context.get_constant_null(arr_type)
        ysu__lkkmq.inititem(doagz__qfx, yfe__nydut, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    zzvxy__gzj = context.get_constant(types.int64, 0)
    tkh__ehbr = context.get_constant(types.int64, 1)
    izrs__xwji = arr_type not in in_table_type.type_to_blk
    for jtzu__rgt, gmgqb__dwgea in out_table_type.type_to_blk.items():
        if jtzu__rgt in in_table_type.type_to_blk:
            yiui__moc = in_table_type.type_to_blk[jtzu__rgt]
            newok__ckeem = ListInstance(context, builder, types.List(
                jtzu__rgt), getattr(in_table, f'block_{yiui__moc}'))
            context.nrt.incref(builder, types.List(jtzu__rgt), newok__ckeem
                .value)
            setattr(out_table, f'block_{gmgqb__dwgea}', newok__ckeem.value)
    if izrs__xwji:
        qyck__ofaz, newok__ckeem = ListInstance.allocate_ex(context,
            builder, types.List(arr_type), tkh__ehbr)
        newok__ckeem.size = tkh__ehbr
        newok__ckeem.inititem(zzvxy__gzj, arr_arg, incref=True)
        gmgqb__dwgea = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{gmgqb__dwgea}', newok__ckeem.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        gmgqb__dwgea = out_table_type.type_to_blk[arr_type]
        newok__ckeem = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{gmgqb__dwgea}'))
        if is_new_col:
            n = newok__ckeem.size
            aafu__vqik = builder.add(n, tkh__ehbr)
            newok__ckeem.resize(aafu__vqik)
            newok__ckeem.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            oqnv__tqfs = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            newok__ckeem.setitem(oqnv__tqfs, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            oqnv__tqfs = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = newok__ckeem.size
            aafu__vqik = builder.add(n, tkh__ehbr)
            newok__ckeem.resize(aafu__vqik)
            context.nrt.incref(builder, arr_type, newok__ckeem.getitem(
                oqnv__tqfs))
            newok__ckeem.move(builder.add(oqnv__tqfs, tkh__ehbr),
                oqnv__tqfs, builder.sub(n, oqnv__tqfs))
            newok__ckeem.setitem(oqnv__tqfs, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    qnuc__sumd = in_table_type.arr_types[col_ind]
    if qnuc__sumd in out_table_type.type_to_blk:
        gmgqb__dwgea = out_table_type.type_to_blk[qnuc__sumd]
        tzxl__xzy = getattr(out_table, f'block_{gmgqb__dwgea}')
        ddec__xvdf = types.List(qnuc__sumd)
        oqnv__tqfs = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        wpx__lxh = ddec__xvdf.dtype(ddec__xvdf, types.intp)
        zksu__wrty = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), wpx__lxh, (tzxl__xzy, oqnv__tqfs))
        context.nrt.decref(builder, qnuc__sumd, zksu__wrty)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    xbdo__ehfr = list(table_type.arr_types)
    if is_new_col:
        xbdo__ehfr.append(arr_type)
    else:
        xbdo__ehfr[col_ind] = arr_type
    out_table_type = TableType(tuple(xbdo__ehfr))

    def codegen(context, builder, sig, args):
        table_arg, qyck__ofaz, hfm__onhm = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, hfm__onhm, col_ind, is_new_col
            )
        return out_table
    return out_table_type(table_type, ind_type, arr_type), codegen


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    xmit__hgm = args[0]
    if equiv_set.has_shape(xmit__hgm):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            xmit__hgm)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    lnfk__ofp = []
    for jtzu__rgt, gmgqb__dwgea in table_type.type_to_blk.items():
        amd__mnrcs = len(table_type.block_to_arr_ind[gmgqb__dwgea])
        aegzg__mzrjg = []
        for i in range(amd__mnrcs):
            cxgv__ithdu = table_type.block_to_arr_ind[gmgqb__dwgea][i]
            aegzg__mzrjg.append(pyval.arrays[cxgv__ithdu])
        lnfk__ofp.append(context.get_constant_generic(builder, types.List(
            jtzu__rgt), aegzg__mzrjg))
    ssrdw__hvw = context.get_constant_null(types.pyobject)
    eejhh__laxpy = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(lnfk__ofp + [ssrdw__hvw, eejhh__laxpy])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    out_table_type = table_type
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(table_type)

    def codegen(context, builder, sig, args):
        hpeuz__nqmxn = cgutils.create_struct_proxy(out_table_type)(context,
            builder)
        for jtzu__rgt, gmgqb__dwgea in out_table_type.type_to_blk.items():
            rkrw__yqlb = context.get_constant_null(types.List(jtzu__rgt))
            setattr(hpeuz__nqmxn, f'block_{gmgqb__dwgea}', rkrw__yqlb)
        return hpeuz__nqmxn._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    xck__snpen = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        xck__snpen[typ.dtype] = i
    ewe__zzzz = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(ewe__zzzz, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        qgqkw__gwtut, qyck__ofaz = args
        hpeuz__nqmxn = cgutils.create_struct_proxy(ewe__zzzz)(context, builder)
        for jtzu__rgt, gmgqb__dwgea in ewe__zzzz.type_to_blk.items():
            idx = xck__snpen[jtzu__rgt]
            ciyo__yhsnq = signature(types.List(jtzu__rgt),
                tuple_of_lists_type, types.literal(idx))
            odehg__cobel = qgqkw__gwtut, idx
            dgaz__puwqc = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, ciyo__yhsnq, odehg__cobel)
            setattr(hpeuz__nqmxn, f'block_{gmgqb__dwgea}', dgaz__puwqc)
        return hpeuz__nqmxn._getvalue()
    sig = ewe__zzzz(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    gmgqb__dwgea = get_overload_const_int(blk_type)
    arr_type = None
    for jtzu__rgt, yib__joxu in table_type.type_to_blk.items():
        if yib__joxu == gmgqb__dwgea:
            arr_type = jtzu__rgt
            break
    assert arr_type is not None, 'invalid table type block'
    trubm__qnaj = types.List(arr_type)

    def codegen(context, builder, sig, args):
        hpeuz__nqmxn = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        fzvx__ndn = getattr(hpeuz__nqmxn, f'block_{gmgqb__dwgea}')
        return impl_ret_borrowed(context, builder, trubm__qnaj, fzvx__ndn)
    sig = trubm__qnaj(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, awdgf__rznk = args
        gdwbi__hep = context.get_python_api(builder)
        snmna__jvxxn = used_cols_typ == types.none
        if not snmna__jvxxn:
            zephf__cosnd = numba.cpython.setobj.SetInstance(context,
                builder, types.Set(types.int64), awdgf__rznk)
        hpeuz__nqmxn = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, table_arg)
        yyzs__twf = cgutils.is_not_null(builder, hpeuz__nqmxn.parent)
        for jtzu__rgt, gmgqb__dwgea in table_type.type_to_blk.items():
            kawc__pbyo = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[gmgqb__dwgea]))
            puvz__keg = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                gmgqb__dwgea], dtype=np.int64))
            aixp__wlre = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, puvz__keg)
            fzvx__ndn = getattr(hpeuz__nqmxn, f'block_{gmgqb__dwgea}')
            with cgutils.for_range(builder, kawc__pbyo) as rfq__jwif:
                i = rfq__jwif.index
                cxgv__ithdu = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    aixp__wlre, i)
                jbomh__kwcmu = types.none(table_type, types.List(jtzu__rgt),
                    types.int64, types.int64)
                msnkq__hhde = table_arg, fzvx__ndn, i, cxgv__ithdu
                if snmna__jvxxn:
                    ensure_column_unboxed_codegen(context, builder,
                        jbomh__kwcmu, msnkq__hhde)
                else:
                    lkwof__ynno = zephf__cosnd.contains(cxgv__ithdu)
                    with builder.if_then(lkwof__ynno):
                        ensure_column_unboxed_codegen(context, builder,
                            jbomh__kwcmu, msnkq__hhde)
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, used_cols_typ)
    return sig, codegen


@intrinsic
def ensure_column_unboxed(typingctx, table_type, arr_list_t, ind_t, arr_ind_t):
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, arr_list_t, ind_t, arr_ind_t)
    return sig, ensure_column_unboxed_codegen


def ensure_column_unboxed_codegen(context, builder, sig, args):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table_arg, fump__dunez, oabt__nkta, vnqv__air = args
    gdwbi__hep = context.get_python_api(builder)
    hpeuz__nqmxn = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, table_arg)
    yyzs__twf = cgutils.is_not_null(builder, hpeuz__nqmxn.parent)
    ysu__lkkmq = ListInstance(context, builder, sig.args[1], fump__dunez)
    msaje__msroa = ysu__lkkmq.getitem(oabt__nkta)
    siyx__cbyik = cgutils.alloca_once_value(builder, msaje__msroa)
    wvjz__brrt = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    qshn__fdlln = is_ll_eq(builder, siyx__cbyik, wvjz__brrt)
    with builder.if_then(qshn__fdlln):
        with builder.if_else(yyzs__twf) as (foau__sgs, ehfyn__bgr):
            with foau__sgs:
                kwj__int = get_df_obj_column_codegen(context, builder,
                    gdwbi__hep, hpeuz__nqmxn.parent, vnqv__air, sig.args[1]
                    .dtype)
                yhnep__ctdnf = gdwbi__hep.to_native_value(sig.args[1].dtype,
                    kwj__int).value
                ysu__lkkmq.inititem(oabt__nkta, yhnep__ctdnf, incref=False)
                gdwbi__hep.decref(kwj__int)
            with ehfyn__bgr:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    gmgqb__dwgea = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, duzg__jfitd, qyck__ofaz = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{gmgqb__dwgea}', duzg__jfitd)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, kqkp__rvptw = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = kqkp__rvptw
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, to_str_if_dict_t):
    assert isinstance(list_type, types.List), 'list type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    trubm__qnaj = list_type
    if is_overload_true(to_str_if_dict_t):
        trubm__qnaj = types.List(to_str_arr_if_dict_array(list_type.dtype))

    def codegen(context, builder, sig, args):
        djep__mkvhv = ListInstance(context, builder, list_type, args[0])
        iacq__erx = djep__mkvhv.size
        qyck__ofaz, newok__ckeem = ListInstance.allocate_ex(context,
            builder, trubm__qnaj, iacq__erx)
        newok__ckeem.size = iacq__erx
        return newok__ckeem.value
    sig = trubm__qnaj(list_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ=None):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    dnpyy__dpf = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(dnpyy__dpf)

    def codegen(context, builder, sig, args):
        iacq__erx, qyck__ofaz = args
        qyck__ofaz, newok__ckeem = ListInstance.allocate_ex(context,
            builder, list_type, iacq__erx)
        newok__ckeem.size = iacq__erx
        return newok__ckeem.value
    sig = list_type(size_typ, data_typ)
    return sig, codegen


def _get_idx_length(idx):
    pass


@overload(_get_idx_length)
def overload_get_idx_length(idx, n):
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        return lambda idx, n: idx.sum()
    assert isinstance(idx, types.SliceType), 'slice index expected'

    def impl(idx, n):
        bpgy__oylz = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(bpgy__oylz)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    uron__agaps = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        uron__agaps['used_cols'] = used_cols
    pry__edf = 'def impl(T, idx):\n'
    pry__edf += f'  T2 = init_table(T, False)\n'
    pry__edf += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        pry__edf += f'  l = _get_idx_length(idx, len(T))\n'
        pry__edf += f'  T2 = set_table_len(T2, l)\n'
        pry__edf += f'  return T2\n'
        bllk__nduxt = {}
        exec(pry__edf, uron__agaps, bllk__nduxt)
        return bllk__nduxt['impl']
    if used_cols is not None:
        pry__edf += f'  used_set = set(used_cols)\n'
    for gmgqb__dwgea in T.type_to_blk.values():
        uron__agaps[f'arr_inds_{gmgqb__dwgea}'] = np.array(T.
            block_to_arr_ind[gmgqb__dwgea], dtype=np.int64)
        pry__edf += (
            f'  arr_list_{gmgqb__dwgea} = get_table_block(T, {gmgqb__dwgea})\n'
            )
        pry__edf += f"""  out_arr_list_{gmgqb__dwgea} = alloc_list_like(arr_list_{gmgqb__dwgea}, False)
"""
        pry__edf += f'  for i in range(len(arr_list_{gmgqb__dwgea})):\n'
        pry__edf += (
            f'    arr_ind_{gmgqb__dwgea} = arr_inds_{gmgqb__dwgea}[i]\n')
        if used_cols is not None:
            pry__edf += (
                f'    if arr_ind_{gmgqb__dwgea} not in used_set: continue\n')
        pry__edf += f"""    ensure_column_unboxed(T, arr_list_{gmgqb__dwgea}, i, arr_ind_{gmgqb__dwgea})
"""
        pry__edf += f"""    out_arr_{gmgqb__dwgea} = ensure_contig_if_np(arr_list_{gmgqb__dwgea}[i][idx])
"""
        pry__edf += f'    l = len(out_arr_{gmgqb__dwgea})\n'
        pry__edf += (
            f'    out_arr_list_{gmgqb__dwgea}[i] = out_arr_{gmgqb__dwgea}\n')
        pry__edf += (
            f'  T2 = set_table_block(T2, out_arr_list_{gmgqb__dwgea}, {gmgqb__dwgea})\n'
            )
    pry__edf += f'  T2 = set_table_len(T2, l)\n'
    pry__edf += f'  return T2\n'
    bllk__nduxt = {}
    exec(pry__edf, uron__agaps, bllk__nduxt)
    return bllk__nduxt['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    pry__edf = 'def impl(T):\n'
    pry__edf += f'  T2 = init_table(T, True)\n'
    pry__edf += f'  l = len(T)\n'
    uron__agaps = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for gmgqb__dwgea in T.type_to_blk.values():
        uron__agaps[f'arr_inds_{gmgqb__dwgea}'] = np.array(T.
            block_to_arr_ind[gmgqb__dwgea], dtype=np.int64)
        pry__edf += (
            f'  arr_list_{gmgqb__dwgea} = get_table_block(T, {gmgqb__dwgea})\n'
            )
        pry__edf += f"""  out_arr_list_{gmgqb__dwgea} = alloc_list_like(arr_list_{gmgqb__dwgea}, True)
"""
        pry__edf += f'  for i in range(len(arr_list_{gmgqb__dwgea})):\n'
        pry__edf += (
            f'    arr_ind_{gmgqb__dwgea} = arr_inds_{gmgqb__dwgea}[i]\n')
        pry__edf += f"""    ensure_column_unboxed(T, arr_list_{gmgqb__dwgea}, i, arr_ind_{gmgqb__dwgea})
"""
        pry__edf += f"""    out_arr_{gmgqb__dwgea} = decode_if_dict_array(arr_list_{gmgqb__dwgea}[i])
"""
        pry__edf += (
            f'    out_arr_list_{gmgqb__dwgea}[i] = out_arr_{gmgqb__dwgea}\n')
        pry__edf += (
            f'  T2 = set_table_block(T2, out_arr_list_{gmgqb__dwgea}, {gmgqb__dwgea})\n'
            )
    pry__edf += f'  T2 = set_table_len(T2, l)\n'
    pry__edf += f'  return T2\n'
    bllk__nduxt = {}
    exec(pry__edf, uron__agaps, bllk__nduxt)
    return bllk__nduxt['impl']


@overload(operator.getitem, no_unliteral=True)
def table_getitem(T, idx):
    if not isinstance(T, TableType):
        return
    return gen_table_filter(T)


@intrinsic
def init_runtime_table_from_lists(typingctx, arr_list_tup_typ, nrows_typ=None):
    assert isinstance(arr_list_tup_typ, types.BaseTuple
        ), 'init_runtime_table_from_lists requires a tuple of list of arrays'
    if isinstance(arr_list_tup_typ, types.UniTuple):
        if arr_list_tup_typ.dtype.dtype == types.undefined:
            return
        xyi__wve = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        xyi__wve = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            xyi__wve.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        jhz__pyhva, sfy__euhi = args
        hpeuz__nqmxn = cgutils.create_struct_proxy(table_type)(context, builder
            )
        hpeuz__nqmxn.len = sfy__euhi
        lnfk__ofp = cgutils.unpack_tuple(builder, jhz__pyhva)
        for i, fzvx__ndn in enumerate(lnfk__ofp):
            setattr(hpeuz__nqmxn, f'block_{i}', fzvx__ndn)
            context.nrt.incref(builder, types.List(xyi__wve[i]), fzvx__ndn)
        return hpeuz__nqmxn._getvalue()
    table_type = TableType(tuple(xyi__wve), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
