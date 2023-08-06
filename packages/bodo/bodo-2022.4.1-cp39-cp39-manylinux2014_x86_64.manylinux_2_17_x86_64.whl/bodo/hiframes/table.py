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
            pqdn__ure = 0
            rqw__yuket = []
            for i in range(usecols[-1] + 1):
                if i == usecols[pqdn__ure]:
                    rqw__yuket.append(arrs[pqdn__ure])
                    pqdn__ure += 1
                else:
                    rqw__yuket.append(None)
            for jjxuq__fzoh in range(usecols[-1] + 1, num_arrs):
                rqw__yuket.append(None)
            self.arrays = rqw__yuket
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((xcf__sjk == nczgl__tegsg).all() for xcf__sjk,
            nczgl__tegsg in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        dag__nko = len(self.arrays)
        bsuae__cii = dict(zip(range(dag__nko), self.arrays))
        df = pd.DataFrame(bsuae__cii, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        ejrsg__finut = []
        cyv__xap = []
        bns__jhvm = {}
        drw__gqon = defaultdict(int)
        ichfi__zhwx = defaultdict(list)
        if not has_runtime_cols:
            for i, pzyd__mqsd in enumerate(arr_types):
                if pzyd__mqsd not in bns__jhvm:
                    bns__jhvm[pzyd__mqsd] = len(bns__jhvm)
                jru__xdtj = bns__jhvm[pzyd__mqsd]
                ejrsg__finut.append(jru__xdtj)
                cyv__xap.append(drw__gqon[jru__xdtj])
                drw__gqon[jru__xdtj] += 1
                ichfi__zhwx[jru__xdtj].append(i)
        self.block_nums = ejrsg__finut
        self.block_offsets = cyv__xap
        self.type_to_blk = bns__jhvm
        self.block_to_arr_ind = ichfi__zhwx
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
    return TableType(tuple(numba.typeof(jcvux__spcyf) for jcvux__spcyf in
        val.arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            evd__ybpee = [(f'block_{i}', types.List(pzyd__mqsd)) for i,
                pzyd__mqsd in enumerate(fe_type.arr_types)]
        else:
            evd__ybpee = [(f'block_{jru__xdtj}', types.List(pzyd__mqsd)) for
                pzyd__mqsd, jru__xdtj in fe_type.type_to_blk.items()]
        evd__ybpee.append(('parent', types.pyobject))
        evd__ybpee.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, evd__ybpee)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    cpb__iom = c.pyapi.object_getattr_string(val, 'arrays')
    mpxor__fihr = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mpxor__fihr.parent = cgutils.get_null_value(mpxor__fihr.parent.type)
    xsuno__murld = c.pyapi.make_none()
    hps__pjlw = c.context.get_constant(types.int64, 0)
    yulh__xnr = cgutils.alloca_once_value(c.builder, hps__pjlw)
    for pzyd__mqsd, jru__xdtj in typ.type_to_blk.items():
        wfl__fdm = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[jru__xdtj]))
        jjxuq__fzoh, wjjtd__rel = ListInstance.allocate_ex(c.context, c.
            builder, types.List(pzyd__mqsd), wfl__fdm)
        wjjtd__rel.size = wfl__fdm
        tcgqb__hsnrx = c.context.make_constant_array(c.builder, types.Array
            (types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[jru__xdtj],
            dtype=np.int64))
        nbek__pojc = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, tcgqb__hsnrx)
        with cgutils.for_range(c.builder, wfl__fdm) as igp__ixtqo:
            i = igp__ixtqo.index
            efmev__wuxhc = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), nbek__pojc, i)
            zwrjx__tskk = c.pyapi.long_from_longlong(efmev__wuxhc)
            cvasd__zdpq = c.pyapi.object_getitem(cpb__iom, zwrjx__tskk)
            mud__wskow = c.builder.icmp_unsigned('==', cvasd__zdpq,
                xsuno__murld)
            with c.builder.if_else(mud__wskow) as (mfcxy__ymzu, rsue__oswax):
                with mfcxy__ymzu:
                    eavq__rfv = c.context.get_constant_null(pzyd__mqsd)
                    wjjtd__rel.inititem(i, eavq__rfv, incref=False)
                with rsue__oswax:
                    mulh__osmh = c.pyapi.call_method(cvasd__zdpq, '__len__', ()
                        )
                    gjlb__erw = c.pyapi.long_as_longlong(mulh__osmh)
                    c.builder.store(gjlb__erw, yulh__xnr)
                    c.pyapi.decref(mulh__osmh)
                    jcvux__spcyf = c.pyapi.to_native_value(pzyd__mqsd,
                        cvasd__zdpq).value
                    wjjtd__rel.inititem(i, jcvux__spcyf, incref=False)
            c.pyapi.decref(cvasd__zdpq)
            c.pyapi.decref(zwrjx__tskk)
        setattr(mpxor__fihr, f'block_{jru__xdtj}', wjjtd__rel.value)
    mpxor__fihr.len = c.builder.load(yulh__xnr)
    c.pyapi.decref(cpb__iom)
    c.pyapi.decref(xsuno__murld)
    rncjr__royi = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(mpxor__fihr._getvalue(), is_error=rncjr__royi)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    mpxor__fihr = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        hni__tmc = c.context.get_constant(types.int64, 0)
        for i, pzyd__mqsd in enumerate(typ.arr_types):
            rqw__yuket = getattr(mpxor__fihr, f'block_{i}')
            iqn__cefrs = ListInstance(c.context, c.builder, types.List(
                pzyd__mqsd), rqw__yuket)
            hni__tmc = c.builder.add(hni__tmc, iqn__cefrs.size)
        fwv__fsrms = c.pyapi.list_new(hni__tmc)
        kahp__derrt = c.context.get_constant(types.int64, 0)
        for i, pzyd__mqsd in enumerate(typ.arr_types):
            rqw__yuket = getattr(mpxor__fihr, f'block_{i}')
            iqn__cefrs = ListInstance(c.context, c.builder, types.List(
                pzyd__mqsd), rqw__yuket)
            with cgutils.for_range(c.builder, iqn__cefrs.size) as igp__ixtqo:
                i = igp__ixtqo.index
                jcvux__spcyf = iqn__cefrs.getitem(i)
                c.context.nrt.incref(c.builder, pzyd__mqsd, jcvux__spcyf)
                idx = c.builder.add(kahp__derrt, i)
                c.pyapi.list_setitem(fwv__fsrms, idx, c.pyapi.
                    from_native_value(pzyd__mqsd, jcvux__spcyf, c.env_manager))
            kahp__derrt = c.builder.add(kahp__derrt, iqn__cefrs.size)
        canw__ovh = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        ncy__hxrwq = c.pyapi.call_function_objargs(canw__ovh, (fwv__fsrms,))
        c.pyapi.decref(canw__ovh)
        c.pyapi.decref(fwv__fsrms)
        c.context.nrt.decref(c.builder, typ, val)
        return ncy__hxrwq
    fwv__fsrms = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    ovjl__twag = cgutils.is_not_null(c.builder, mpxor__fihr.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for pzyd__mqsd, jru__xdtj in typ.type_to_blk.items():
        rqw__yuket = getattr(mpxor__fihr, f'block_{jru__xdtj}')
        iqn__cefrs = ListInstance(c.context, c.builder, types.List(
            pzyd__mqsd), rqw__yuket)
        tcgqb__hsnrx = c.context.make_constant_array(c.builder, types.Array
            (types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[jru__xdtj],
            dtype=np.int64))
        nbek__pojc = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, tcgqb__hsnrx)
        with cgutils.for_range(c.builder, iqn__cefrs.size) as igp__ixtqo:
            i = igp__ixtqo.index
            efmev__wuxhc = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), nbek__pojc, i)
            jcvux__spcyf = iqn__cefrs.getitem(i)
            crvtk__oatgh = cgutils.alloca_once_value(c.builder, jcvux__spcyf)
            hly__knmk = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(pzyd__mqsd))
            jec__zac = is_ll_eq(c.builder, crvtk__oatgh, hly__knmk)
            with c.builder.if_else(c.builder.and_(jec__zac, c.builder.not_(
                ensure_unboxed))) as (mfcxy__ymzu, rsue__oswax):
                with mfcxy__ymzu:
                    xsuno__murld = c.pyapi.make_none()
                    c.pyapi.list_setitem(fwv__fsrms, efmev__wuxhc, xsuno__murld
                        )
                with rsue__oswax:
                    cvasd__zdpq = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(jec__zac, ovjl__twag)
                        ) as (ogw__kyduw, mgdxo__gjcvp):
                        with ogw__kyduw:
                            uppib__earcv = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, mpxor__fihr.
                                parent, efmev__wuxhc, pzyd__mqsd)
                            c.builder.store(uppib__earcv, cvasd__zdpq)
                        with mgdxo__gjcvp:
                            c.context.nrt.incref(c.builder, pzyd__mqsd,
                                jcvux__spcyf)
                            c.builder.store(c.pyapi.from_native_value(
                                pzyd__mqsd, jcvux__spcyf, c.env_manager),
                                cvasd__zdpq)
                    c.pyapi.list_setitem(fwv__fsrms, efmev__wuxhc, c.
                        builder.load(cvasd__zdpq))
    canw__ovh = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    ncy__hxrwq = c.pyapi.call_function_objargs(canw__ovh, (fwv__fsrms,))
    c.pyapi.decref(canw__ovh)
    c.pyapi.decref(fwv__fsrms)
    c.context.nrt.decref(c.builder, typ, val)
    return ncy__hxrwq


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
        mpxor__fihr = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        wopjb__igfd = context.get_constant(types.int64, 0)
        for i, pzyd__mqsd in enumerate(table_type.arr_types):
            rqw__yuket = getattr(mpxor__fihr, f'block_{i}')
            iqn__cefrs = ListInstance(context, builder, types.List(
                pzyd__mqsd), rqw__yuket)
            wopjb__igfd = builder.add(wopjb__igfd, iqn__cefrs.size)
        return wopjb__igfd
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    mpxor__fihr = cgutils.create_struct_proxy(table_type)(context, builder,
        table_arg)
    jru__xdtj = table_type.block_nums[col_ind]
    yqv__emg = table_type.block_offsets[col_ind]
    rqw__yuket = getattr(mpxor__fihr, f'block_{jru__xdtj}')
    iqn__cefrs = ListInstance(context, builder, types.List(arr_type),
        rqw__yuket)
    jcvux__spcyf = iqn__cefrs.getitem(yqv__emg)
    return jcvux__spcyf


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, jjxuq__fzoh = args
        jcvux__spcyf = get_table_data_codegen(context, builder, table_arg,
            col_ind, table_type)
        return impl_ret_borrowed(context, builder, arr_type, jcvux__spcyf)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, jjxuq__fzoh = args
        mpxor__fihr = cgutils.create_struct_proxy(table_type)(context,
            builder, table_arg)
        jru__xdtj = table_type.block_nums[col_ind]
        yqv__emg = table_type.block_offsets[col_ind]
        rqw__yuket = getattr(mpxor__fihr, f'block_{jru__xdtj}')
        iqn__cefrs = ListInstance(context, builder, types.List(arr_type),
            rqw__yuket)
        jcvux__spcyf = iqn__cefrs.getitem(yqv__emg)
        context.nrt.decref(builder, arr_type, jcvux__spcyf)
        eavq__rfv = context.get_constant_null(arr_type)
        iqn__cefrs.inititem(yqv__emg, eavq__rfv, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    hps__pjlw = context.get_constant(types.int64, 0)
    wejv__gba = context.get_constant(types.int64, 1)
    fegiy__cov = arr_type not in in_table_type.type_to_blk
    for pzyd__mqsd, jru__xdtj in out_table_type.type_to_blk.items():
        if pzyd__mqsd in in_table_type.type_to_blk:
            oiqxa__sxex = in_table_type.type_to_blk[pzyd__mqsd]
            wjjtd__rel = ListInstance(context, builder, types.List(
                pzyd__mqsd), getattr(in_table, f'block_{oiqxa__sxex}'))
            context.nrt.incref(builder, types.List(pzyd__mqsd), wjjtd__rel.
                value)
            setattr(out_table, f'block_{jru__xdtj}', wjjtd__rel.value)
    if fegiy__cov:
        jjxuq__fzoh, wjjtd__rel = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), wejv__gba)
        wjjtd__rel.size = wejv__gba
        wjjtd__rel.inititem(hps__pjlw, arr_arg, incref=True)
        jru__xdtj = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{jru__xdtj}', wjjtd__rel.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        jru__xdtj = out_table_type.type_to_blk[arr_type]
        wjjtd__rel = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{jru__xdtj}'))
        if is_new_col:
            n = wjjtd__rel.size
            whe__umwhl = builder.add(n, wejv__gba)
            wjjtd__rel.resize(whe__umwhl)
            wjjtd__rel.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            xpglz__pvpor = context.get_constant(types.int64, out_table_type
                .block_offsets[col_ind])
            wjjtd__rel.setitem(xpglz__pvpor, arr_arg, True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            xpglz__pvpor = context.get_constant(types.int64, out_table_type
                .block_offsets[col_ind])
            n = wjjtd__rel.size
            whe__umwhl = builder.add(n, wejv__gba)
            wjjtd__rel.resize(whe__umwhl)
            context.nrt.incref(builder, arr_type, wjjtd__rel.getitem(
                xpglz__pvpor))
            wjjtd__rel.move(builder.add(xpglz__pvpor, wejv__gba),
                xpglz__pvpor, builder.sub(n, xpglz__pvpor))
            wjjtd__rel.setitem(xpglz__pvpor, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    uaq__kjakl = in_table_type.arr_types[col_ind]
    if uaq__kjakl in out_table_type.type_to_blk:
        jru__xdtj = out_table_type.type_to_blk[uaq__kjakl]
        hqdc__ybd = getattr(out_table, f'block_{jru__xdtj}')
        gtu__cbb = types.List(uaq__kjakl)
        xpglz__pvpor = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        sixc__lbz = gtu__cbb.dtype(gtu__cbb, types.intp)
        mbkfi__rnz = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), sixc__lbz, (hqdc__ybd, xpglz__pvpor))
        context.nrt.decref(builder, uaq__kjakl, mbkfi__rnz)


@intrinsic
def set_table_data(typingctx, table_type, ind_type, arr_type):
    assert isinstance(table_type, TableType), 'invalid input to set_table_data'
    assert is_overload_constant_int(ind_type
        ), 'set_table_data expects const index'
    col_ind = get_overload_const_int(ind_type)
    is_new_col = col_ind == len(table_type.arr_types)
    zadky__gyjp = list(table_type.arr_types)
    if is_new_col:
        zadky__gyjp.append(arr_type)
    else:
        zadky__gyjp[col_ind] = arr_type
    out_table_type = TableType(tuple(zadky__gyjp))

    def codegen(context, builder, sig, args):
        table_arg, jjxuq__fzoh, tnxi__emmg = args
        out_table = set_table_data_codegen(context, builder, table_type,
            table_arg, out_table_type, arr_type, tnxi__emmg, col_ind,
            is_new_col)
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
    qadk__dey = args[0]
    if equiv_set.has_shape(qadk__dey):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            qadk__dey)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    fzzhl__vqlly = []
    for pzyd__mqsd, jru__xdtj in table_type.type_to_blk.items():
        mmt__vmdj = len(table_type.block_to_arr_ind[jru__xdtj])
        dnfqu__dpko = []
        for i in range(mmt__vmdj):
            efmev__wuxhc = table_type.block_to_arr_ind[jru__xdtj][i]
            dnfqu__dpko.append(pyval.arrays[efmev__wuxhc])
        fzzhl__vqlly.append(context.get_constant_generic(builder, types.
            List(pzyd__mqsd), dnfqu__dpko))
    zrra__iutyo = context.get_constant_null(types.pyobject)
    ncr__ehqu = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(fzzhl__vqlly + [zrra__iutyo, ncr__ehqu])


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    out_table_type = table_type
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(table_type)

    def codegen(context, builder, sig, args):
        mpxor__fihr = cgutils.create_struct_proxy(out_table_type)(context,
            builder)
        for pzyd__mqsd, jru__xdtj in out_table_type.type_to_blk.items():
            pwo__ozgzy = context.get_constant_null(types.List(pzyd__mqsd))
            setattr(mpxor__fihr, f'block_{jru__xdtj}', pwo__ozgzy)
        return mpxor__fihr._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    ogam__ipakj = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        ogam__ipakj[typ.dtype] = i
    phe__imr = table_type.instance_type if isinstance(table_type, types.TypeRef
        ) else table_type
    assert isinstance(phe__imr, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        lhe__mvu, jjxuq__fzoh = args
        mpxor__fihr = cgutils.create_struct_proxy(phe__imr)(context, builder)
        for pzyd__mqsd, jru__xdtj in phe__imr.type_to_blk.items():
            idx = ogam__ipakj[pzyd__mqsd]
            qtgdl__hmu = signature(types.List(pzyd__mqsd),
                tuple_of_lists_type, types.literal(idx))
            bpka__lfktb = lhe__mvu, idx
            hrtnd__kqt = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, qtgdl__hmu, bpka__lfktb)
            setattr(mpxor__fihr, f'block_{jru__xdtj}', hrtnd__kqt)
        return mpxor__fihr._getvalue()
    sig = phe__imr(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    jru__xdtj = get_overload_const_int(blk_type)
    arr_type = None
    for pzyd__mqsd, nczgl__tegsg in table_type.type_to_blk.items():
        if nczgl__tegsg == jru__xdtj:
            arr_type = pzyd__mqsd
            break
    assert arr_type is not None, 'invalid table type block'
    amt__mnqpq = types.List(arr_type)

    def codegen(context, builder, sig, args):
        mpxor__fihr = cgutils.create_struct_proxy(table_type)(context,
            builder, args[0])
        rqw__yuket = getattr(mpxor__fihr, f'block_{jru__xdtj}')
        return impl_ret_borrowed(context, builder, amt__mnqpq, rqw__yuket)
    sig = amt__mnqpq(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, aznqv__hfqmy = args
        ikpjf__okhy = context.get_python_api(builder)
        rbmdv__mrixk = used_cols_typ == types.none
        if not rbmdv__mrixk:
            uqrqj__jmymm = numba.cpython.setobj.SetInstance(context,
                builder, types.Set(types.int64), aznqv__hfqmy)
        mpxor__fihr = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, table_arg)
        ovjl__twag = cgutils.is_not_null(builder, mpxor__fihr.parent)
        for pzyd__mqsd, jru__xdtj in table_type.type_to_blk.items():
            wfl__fdm = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[jru__xdtj]))
            tcgqb__hsnrx = context.make_constant_array(builder, types.Array
                (types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind
                [jru__xdtj], dtype=np.int64))
            nbek__pojc = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, tcgqb__hsnrx)
            rqw__yuket = getattr(mpxor__fihr, f'block_{jru__xdtj}')
            with cgutils.for_range(builder, wfl__fdm) as igp__ixtqo:
                i = igp__ixtqo.index
                efmev__wuxhc = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    nbek__pojc, i)
                uho__hspdd = types.none(table_type, types.List(pzyd__mqsd),
                    types.int64, types.int64)
                gzub__qpbp = table_arg, rqw__yuket, i, efmev__wuxhc
                if rbmdv__mrixk:
                    ensure_column_unboxed_codegen(context, builder,
                        uho__hspdd, gzub__qpbp)
                else:
                    qxha__grn = uqrqj__jmymm.contains(efmev__wuxhc)
                    with builder.if_then(qxha__grn):
                        ensure_column_unboxed_codegen(context, builder,
                            uho__hspdd, gzub__qpbp)
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
    table_arg, mnx__afws, wnfdc__hst, fidbg__mwxcq = args
    ikpjf__okhy = context.get_python_api(builder)
    mpxor__fihr = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    ovjl__twag = cgutils.is_not_null(builder, mpxor__fihr.parent)
    iqn__cefrs = ListInstance(context, builder, sig.args[1], mnx__afws)
    uurxr__vfx = iqn__cefrs.getitem(wnfdc__hst)
    crvtk__oatgh = cgutils.alloca_once_value(builder, uurxr__vfx)
    hly__knmk = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    jec__zac = is_ll_eq(builder, crvtk__oatgh, hly__knmk)
    with builder.if_then(jec__zac):
        with builder.if_else(ovjl__twag) as (mfcxy__ymzu, rsue__oswax):
            with mfcxy__ymzu:
                cvasd__zdpq = get_df_obj_column_codegen(context, builder,
                    ikpjf__okhy, mpxor__fihr.parent, fidbg__mwxcq, sig.args
                    [1].dtype)
                jcvux__spcyf = ikpjf__okhy.to_native_value(sig.args[1].
                    dtype, cvasd__zdpq).value
                iqn__cefrs.inititem(wnfdc__hst, jcvux__spcyf, incref=False)
                ikpjf__okhy.decref(cvasd__zdpq)
            with rsue__oswax:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    jru__xdtj = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, qii__uyoq, jjxuq__fzoh = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{jru__xdtj}', qii__uyoq)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, qpxdk__fzyk = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = qpxdk__fzyk
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, to_str_if_dict_t):
    assert isinstance(list_type, types.List), 'list type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    amt__mnqpq = list_type
    if is_overload_true(to_str_if_dict_t):
        amt__mnqpq = types.List(to_str_arr_if_dict_array(list_type.dtype))

    def codegen(context, builder, sig, args):
        kkt__vuzd = ListInstance(context, builder, list_type, args[0])
        lexhq__gaa = kkt__vuzd.size
        jjxuq__fzoh, wjjtd__rel = ListInstance.allocate_ex(context, builder,
            amt__mnqpq, lexhq__gaa)
        wjjtd__rel.size = lexhq__gaa
        return wjjtd__rel.value
    sig = amt__mnqpq(list_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ=None):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    qniie__wvmc = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(qniie__wvmc)

    def codegen(context, builder, sig, args):
        lexhq__gaa, jjxuq__fzoh = args
        jjxuq__fzoh, wjjtd__rel = ListInstance.allocate_ex(context, builder,
            list_type, lexhq__gaa)
        wjjtd__rel.size = lexhq__gaa
        return wjjtd__rel.value
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
        vjw__plck = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(vjw__plck)
    return impl


def gen_table_filter(T, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    vggpg__lbgag = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, '_get_idx_length':
        _get_idx_length, 'ensure_contig_if_np': ensure_contig_if_np}
    if used_cols is not None:
        vggpg__lbgag['used_cols'] = used_cols
    fmccr__yqg = 'def impl(T, idx):\n'
    fmccr__yqg += f'  T2 = init_table(T, False)\n'
    fmccr__yqg += f'  l = 0\n'
    if used_cols is not None and len(used_cols) == 0:
        fmccr__yqg += f'  l = _get_idx_length(idx, len(T))\n'
        fmccr__yqg += f'  T2 = set_table_len(T2, l)\n'
        fmccr__yqg += f'  return T2\n'
        bty__cmq = {}
        exec(fmccr__yqg, vggpg__lbgag, bty__cmq)
        return bty__cmq['impl']
    if used_cols is not None:
        fmccr__yqg += f'  used_set = set(used_cols)\n'
    for jru__xdtj in T.type_to_blk.values():
        vggpg__lbgag[f'arr_inds_{jru__xdtj}'] = np.array(T.block_to_arr_ind
            [jru__xdtj], dtype=np.int64)
        fmccr__yqg += (
            f'  arr_list_{jru__xdtj} = get_table_block(T, {jru__xdtj})\n')
        fmccr__yqg += (
            f'  out_arr_list_{jru__xdtj} = alloc_list_like(arr_list_{jru__xdtj}, False)\n'
            )
        fmccr__yqg += f'  for i in range(len(arr_list_{jru__xdtj})):\n'
        fmccr__yqg += f'    arr_ind_{jru__xdtj} = arr_inds_{jru__xdtj}[i]\n'
        if used_cols is not None:
            fmccr__yqg += (
                f'    if arr_ind_{jru__xdtj} not in used_set: continue\n')
        fmccr__yqg += f"""    ensure_column_unboxed(T, arr_list_{jru__xdtj}, i, arr_ind_{jru__xdtj})
"""
        fmccr__yqg += f"""    out_arr_{jru__xdtj} = ensure_contig_if_np(arr_list_{jru__xdtj}[i][idx])
"""
        fmccr__yqg += f'    l = len(out_arr_{jru__xdtj})\n'
        fmccr__yqg += (
            f'    out_arr_list_{jru__xdtj}[i] = out_arr_{jru__xdtj}\n')
        fmccr__yqg += (
            f'  T2 = set_table_block(T2, out_arr_list_{jru__xdtj}, {jru__xdtj})\n'
            )
    fmccr__yqg += f'  T2 = set_table_len(T2, l)\n'
    fmccr__yqg += f'  return T2\n'
    bty__cmq = {}
    exec(fmccr__yqg, vggpg__lbgag, bty__cmq)
    return bty__cmq['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    fmccr__yqg = 'def impl(T):\n'
    fmccr__yqg += f'  T2 = init_table(T, True)\n'
    fmccr__yqg += f'  l = len(T)\n'
    vggpg__lbgag = {'init_table': init_table, 'get_table_block':
        get_table_block, 'ensure_column_unboxed': ensure_column_unboxed,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'alloc_list_like': alloc_list_like, 'decode_if_dict_array':
        decode_if_dict_array}
    for jru__xdtj in T.type_to_blk.values():
        vggpg__lbgag[f'arr_inds_{jru__xdtj}'] = np.array(T.block_to_arr_ind
            [jru__xdtj], dtype=np.int64)
        fmccr__yqg += (
            f'  arr_list_{jru__xdtj} = get_table_block(T, {jru__xdtj})\n')
        fmccr__yqg += (
            f'  out_arr_list_{jru__xdtj} = alloc_list_like(arr_list_{jru__xdtj}, True)\n'
            )
        fmccr__yqg += f'  for i in range(len(arr_list_{jru__xdtj})):\n'
        fmccr__yqg += f'    arr_ind_{jru__xdtj} = arr_inds_{jru__xdtj}[i]\n'
        fmccr__yqg += f"""    ensure_column_unboxed(T, arr_list_{jru__xdtj}, i, arr_ind_{jru__xdtj})
"""
        fmccr__yqg += (
            f'    out_arr_{jru__xdtj} = decode_if_dict_array(arr_list_{jru__xdtj}[i])\n'
            )
        fmccr__yqg += (
            f'    out_arr_list_{jru__xdtj}[i] = out_arr_{jru__xdtj}\n')
        fmccr__yqg += (
            f'  T2 = set_table_block(T2, out_arr_list_{jru__xdtj}, {jru__xdtj})\n'
            )
    fmccr__yqg += f'  T2 = set_table_len(T2, l)\n'
    fmccr__yqg += f'  return T2\n'
    bty__cmq = {}
    exec(fmccr__yqg, vggpg__lbgag, bty__cmq)
    return bty__cmq['impl']


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
        wigr__apr = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        wigr__apr = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            wigr__apr.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        rooha__eslvr, ggr__pfmy = args
        mpxor__fihr = cgutils.create_struct_proxy(table_type)(context, builder)
        mpxor__fihr.len = ggr__pfmy
        fzzhl__vqlly = cgutils.unpack_tuple(builder, rooha__eslvr)
        for i, rqw__yuket in enumerate(fzzhl__vqlly):
            setattr(mpxor__fihr, f'block_{i}', rqw__yuket)
            context.nrt.incref(builder, types.List(wigr__apr[i]), rqw__yuket)
        return mpxor__fihr._getvalue()
    table_type = TableType(tuple(wigr__apr), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen
