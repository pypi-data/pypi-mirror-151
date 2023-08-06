"""
Class information for DataFrame iterators returned by pd.read_csv. This is used
to handle situations in which pd.read_csv is used to return chunks with separate
read calls instead of just a single read.
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir_utils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl
from numba.core.typing.templates import signature
from numba.extending import intrinsic, lower_builtin, models, register_model
import bodo
import bodo.ir.connector
import bodo.ir.csv_ext
from bodo import objmode
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io import csv_cpp
from bodo.ir.csv_ext import _gen_read_csv_objmode, astype
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname
ll.add_symbol('update_csv_reader', csv_cpp.update_csv_reader)
ll.add_symbol('initialize_csv_reader', csv_cpp.initialize_csv_reader)


class CSVIteratorType(types.SimpleIteratorType):

    def __init__(self, df_type, out_colnames, out_types, usecols, sep,
        index_ind, index_arr_typ, index_name, escapechar, storage_options):
        assert isinstance(df_type, DataFrameType
            ), 'CSVIterator must return a DataFrame'
        mchc__kgu = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(mchc__kgu)
        self._yield_type = df_type
        self._out_colnames = out_colnames
        self._out_types = out_types
        self._usecols = usecols
        self._sep = sep
        self._index_ind = index_ind
        self._index_arr_typ = index_arr_typ
        self._index_name = index_name
        self._escapechar = escapechar
        self._storage_options = storage_options

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(CSVIteratorType)
class CSVIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        aof__ondig = [('csv_reader', bodo.ir.connector.stream_reader_type),
            ('index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, aof__ondig)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    dda__aczk = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    rmtjc__ivc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()]
        )
    kpm__gejog = cgutils.get_or_insert_function(builder.module, rmtjc__ivc,
        name='initialize_csv_reader')
    builder.call(kpm__gejog, [dda__aczk.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), dda__aczk.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [zjpb__haq] = sig.args
    [laq__aneee] = args
    dda__aczk = cgutils.create_struct_proxy(zjpb__haq)(context, builder,
        value=laq__aneee)
    rmtjc__ivc = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()]
        )
    kpm__gejog = cgutils.get_or_insert_function(builder.module, rmtjc__ivc,
        name='update_csv_reader')
    kyej__rjm = builder.call(kpm__gejog, [dda__aczk.csv_reader])
    result.set_valid(kyej__rjm)
    with builder.if_then(kyej__rjm):
        cpp__epep = builder.load(dda__aczk.index)
        wsh__lhgb = types.Tuple([sig.return_type.first_type, types.int64])
        tqqxk__atz = gen_read_csv_objmode(sig.args[0])
        sluj__zsckb = signature(wsh__lhgb, bodo.ir.connector.
            stream_reader_type, types.int64)
        syy__wof = context.compile_internal(builder, tqqxk__atz,
            sluj__zsckb, [dda__aczk.csv_reader, cpp__epep])
        nzsyc__kvjb, cwc__ulhfy = cgutils.unpack_tuple(builder, syy__wof)
        wyadi__kvoej = builder.add(cpp__epep, cwc__ulhfy, flags=['nsw'])
        builder.store(wyadi__kvoej, dda__aczk.index)
        result.yield_(nzsyc__kvjb)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        amn__egf = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        amn__egf.csv_reader = args[0]
        eiesz__typ = context.get_constant(types.uintp, 0)
        amn__egf.index = cgutils.alloca_once_value(builder, eiesz__typ)
        return amn__egf._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    wgrw__yxv = csv_iterator_typeref.instance_type
    sig = signature(wgrw__yxv, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    hfjvh__bou = 'def read_csv_objmode(f_reader):\n'
    phwvj__qvqh = [sanitize_varname(txh__lnpr) for txh__lnpr in
        csv_iterator_type._out_colnames]
    ospn__gzxr = ir_utils.next_label()
    vmk__uzkjl = globals()
    out_types = csv_iterator_type._out_types
    vmk__uzkjl[f'table_type_{ospn__gzxr}'] = TableType(tuple(out_types))
    vmk__uzkjl[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    zprh__qqo = list(range(len(csv_iterator_type._usecols)))
    hfjvh__bou += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        phwvj__qvqh, out_types, csv_iterator_type._usecols, zprh__qqo,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, ospn__gzxr, vmk__uzkjl,
        parallel=False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    gug__mnopq = bodo.ir.csv_ext._gen_parallel_flag_name(phwvj__qvqh)
    tfdp__xugi = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [gug__mnopq]
    hfjvh__bou += f"  return {', '.join(tfdp__xugi)}"
    vmk__uzkjl = globals()
    duos__xkn = {}
    exec(hfjvh__bou, vmk__uzkjl, duos__xkn)
    kzhf__twqj = duos__xkn['read_csv_objmode']
    ktugx__ivybj = numba.njit(kzhf__twqj)
    bodo.ir.csv_ext.compiled_funcs.append(ktugx__ivybj)
    dydj__rznak = 'def read_func(reader, local_start):\n'
    dydj__rznak += f"  {', '.join(tfdp__xugi)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        dydj__rznak += f'  local_len = len(T)\n'
        dydj__rznak += '  total_size = local_len\n'
        dydj__rznak += f'  if ({gug__mnopq}):\n'
        dydj__rznak += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        dydj__rznak += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        rpxv__wnhh = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        dydj__rznak += '  total_size = 0\n'
        rpxv__wnhh = (
            f'bodo.utils.conversion.convert_to_index({tfdp__xugi[1]}, {csv_iterator_type._index_name!r})'
            )
    dydj__rznak += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({tfdp__xugi[0]},), {rpxv__wnhh}, out_df_typ), total_size)
"""
    exec(dydj__rznak, {'bodo': bodo, 'objmode_func': ktugx__ivybj, '_op':
        np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, duos__xkn)
    return duos__xkn['read_func']
