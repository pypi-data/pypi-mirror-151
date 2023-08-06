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
        koq__pssb = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(koq__pssb)
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
        bme__xyf = [('csv_reader', bodo.ir.connector.stream_reader_type), (
            'index', types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, bme__xyf)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    gzabn__kjxi = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    lbc__btf = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    ctcsn__aeue = cgutils.get_or_insert_function(builder.module, lbc__btf,
        name='initialize_csv_reader')
    builder.call(ctcsn__aeue, [gzabn__kjxi.csv_reader])
    builder.store(context.get_constant(types.uint64, 0), gzabn__kjxi.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [dsww__zlkvx] = sig.args
    [izwxw__rkcd] = args
    gzabn__kjxi = cgutils.create_struct_proxy(dsww__zlkvx)(context, builder,
        value=izwxw__rkcd)
    lbc__btf = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    ctcsn__aeue = cgutils.get_or_insert_function(builder.module, lbc__btf,
        name='update_csv_reader')
    awyi__zasy = builder.call(ctcsn__aeue, [gzabn__kjxi.csv_reader])
    result.set_valid(awyi__zasy)
    with builder.if_then(awyi__zasy):
        byj__mbi = builder.load(gzabn__kjxi.index)
        nkjfk__pedi = types.Tuple([sig.return_type.first_type, types.int64])
        fdcv__uzhom = gen_read_csv_objmode(sig.args[0])
        gujem__ing = signature(nkjfk__pedi, bodo.ir.connector.
            stream_reader_type, types.int64)
        wcdn__zmmsg = context.compile_internal(builder, fdcv__uzhom,
            gujem__ing, [gzabn__kjxi.csv_reader, byj__mbi])
        drz__jeebu, tml__fnih = cgutils.unpack_tuple(builder, wcdn__zmmsg)
        aowy__ugd = builder.add(byj__mbi, tml__fnih, flags=['nsw'])
        builder.store(aowy__ugd, gzabn__kjxi.index)
        result.yield_(drz__jeebu)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        njxht__ral = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        njxht__ral.csv_reader = args[0]
        hrl__hzms = context.get_constant(types.uintp, 0)
        njxht__ral.index = cgutils.alloca_once_value(builder, hrl__hzms)
        return njxht__ral._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    kdir__ngs = csv_iterator_typeref.instance_type
    sig = signature(kdir__ngs, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    xwqdh__koyop = 'def read_csv_objmode(f_reader):\n'
    qdto__knlhg = [sanitize_varname(bfu__prgj) for bfu__prgj in
        csv_iterator_type._out_colnames]
    gykt__mco = ir_utils.next_label()
    gyvx__uzwd = globals()
    out_types = csv_iterator_type._out_types
    gyvx__uzwd[f'table_type_{gykt__mco}'] = TableType(tuple(out_types))
    gyvx__uzwd[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    ixtk__oloak = list(range(len(csv_iterator_type._usecols)))
    xwqdh__koyop += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        qdto__knlhg, out_types, csv_iterator_type._usecols, ixtk__oloak,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, gykt__mco, gyvx__uzwd, parallel
        =False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    wlq__rxzx = bodo.ir.csv_ext._gen_parallel_flag_name(qdto__knlhg)
    yuc__ntxq = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [wlq__rxzx]
    xwqdh__koyop += f"  return {', '.join(yuc__ntxq)}"
    gyvx__uzwd = globals()
    sibb__pvqv = {}
    exec(xwqdh__koyop, gyvx__uzwd, sibb__pvqv)
    lpqo__fpgsu = sibb__pvqv['read_csv_objmode']
    jmfu__iiodr = numba.njit(lpqo__fpgsu)
    bodo.ir.csv_ext.compiled_funcs.append(jmfu__iiodr)
    czfq__uwns = 'def read_func(reader, local_start):\n'
    czfq__uwns += f"  {', '.join(yuc__ntxq)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        czfq__uwns += f'  local_len = len(T)\n'
        czfq__uwns += '  total_size = local_len\n'
        czfq__uwns += f'  if ({wlq__rxzx}):\n'
        czfq__uwns += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        czfq__uwns += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        mgq__gyr = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        czfq__uwns += '  total_size = 0\n'
        mgq__gyr = (
            f'bodo.utils.conversion.convert_to_index({yuc__ntxq[1]}, {csv_iterator_type._index_name!r})'
            )
    czfq__uwns += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({yuc__ntxq[0]},), {mgq__gyr}, out_df_typ), total_size)
"""
    exec(czfq__uwns, {'bodo': bodo, 'objmode_func': jmfu__iiodr, '_op': np.
        int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        'out_df_typ': csv_iterator_type.yield_type}, sibb__pvqv)
    return sibb__pvqv['read_func']
