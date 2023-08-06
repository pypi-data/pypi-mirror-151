from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from mpi4py import MPI
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import Table, TableType
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname


class CsvReader(ir.Stmt):

    def __init__(self, file_name, df_out, sep, df_colnames, out_vars,
        out_types, usecols, loc, header, compression, nrows, skiprows,
        chunksize, is_skiprows_list, low_memory, escapechar,
        storage_options=None, index_column_index=None, index_column_typ=
        types.none):
        self.connector_typ = 'csv'
        self.file_name = file_name
        self.df_out = df_out
        self.sep = sep
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.usecols = usecols
        self.loc = loc
        self.skiprows = skiprows
        self.nrows = nrows
        self.header = header
        self.compression = compression
        self.chunksize = chunksize
        self.is_skiprows_list = is_skiprows_list
        self.pd_low_memory = low_memory
        self.escapechar = escapechar
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_typ = index_column_typ
        self.type_usecol_offset = list(range(len(usecols)))

    def __repr__(self):
        return (
            '{} = ReadCsv(file={}, col_names={}, types={}, vars={}, nrows={}, skiprows={}, chunksize={}, is_skiprows_list={}, pd_low_memory={}, escapechar={}, storage_options={}, index_column_index={}, index_colum_typ = {}, type_usecol_offsets={})'
            .format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars, self.nrows, self.skiprows, self.
            chunksize, self.is_skiprows_list, self.pd_low_memory, self.
            escapechar, self.storage_options, self.index_column_index, self
            .index_column_typ, self.type_usecol_offset))


def check_node_typing(node, typemap):
    bcsu__vpfao = typemap[node.file_name.name]
    if types.unliteral(bcsu__vpfao) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {bcsu__vpfao}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        vnjkb__cmkge = typemap[node.skiprows.name]
        if isinstance(vnjkb__cmkge, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(vnjkb__cmkge, types.Integer) and not (isinstance
            (vnjkb__cmkge, (types.List, types.Tuple)) and isinstance(
            vnjkb__cmkge.dtype, types.Integer)) and not isinstance(vnjkb__cmkge
            , (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {vnjkb__cmkge}."
                , loc=node.skiprows.loc)
        elif isinstance(vnjkb__cmkge, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        cbw__xvbs = typemap[node.nrows.name]
        if not isinstance(cbw__xvbs, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {cbw__xvbs}."
                , loc=node.nrows.loc)


import llvmlite.binding as ll
from bodo.io import csv_cpp
ll.add_symbol('csv_file_chunk_reader', csv_cpp.csv_file_chunk_reader)
csv_file_chunk_reader = types.ExternalFunction('csv_file_chunk_reader',
    bodo.ir.connector.stream_reader_type(types.voidptr, types.bool_, types.
    voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
    storage_options_dict_type, types.int64, types.bool_, types.int64, types
    .bool_))


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        xqago__ncyl = csv_node.out_vars[0]
        if xqago__ncyl.name not in lives:
            return None
    else:
        xnjg__uwkl = csv_node.out_vars[0]
        mcp__mqf = csv_node.out_vars[1]
        if xnjg__uwkl.name not in lives and mcp__mqf.name not in lives:
            return None
        elif mcp__mqf.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif xnjg__uwkl.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    vnjkb__cmkge = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            qzdv__mtc = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            rehcz__ytahn = csv_node.loc.strformat()
            khq__kxogq = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', qzdv__mtc,
                rehcz__ytahn, khq__kxogq)
            eau__zffwd = csv_node.out_types[0].yield_type.data
            mwz__rvu = [osmqb__wgzqp for gnm__kzyqd, osmqb__wgzqp in
                enumerate(csv_node.df_colnames) if isinstance(eau__zffwd[
                gnm__kzyqd], bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if mwz__rvu:
                hjrf__mnv = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    hjrf__mnv, rehcz__ytahn, mwz__rvu)
        if array_dists is not None:
            bjozu__irc = csv_node.out_vars[0].name
            parallel = array_dists[bjozu__irc] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        ymqpp__fqifn = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        ymqpp__fqifn += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        ymqpp__fqifn += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        urv__bjr = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(ymqpp__fqifn, {}, urv__bjr)
        qjo__lgs = urv__bjr['csv_iterator_impl']
        qdzs__twv = 'def csv_reader_init(fname, nrows, skiprows):\n'
        qdzs__twv += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        qdzs__twv += '  return f_reader\n'
        exec(qdzs__twv, globals(), urv__bjr)
        gptqc__vyjf = urv__bjr['csv_reader_init']
        etss__ajbrh = numba.njit(gptqc__vyjf)
        compiled_funcs.append(etss__ajbrh)
        ewrq__puv = compile_to_numba_ir(qjo__lgs, {'_csv_reader_init':
            etss__ajbrh, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, vnjkb__cmkge), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(ewrq__puv, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        pbmf__ace = ewrq__puv.body[:-3]
        pbmf__ace[-1].target = csv_node.out_vars[0]
        return pbmf__ace
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    ymqpp__fqifn = 'def csv_impl(fname, nrows, skiprows):\n'
    ymqpp__fqifn += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    urv__bjr = {}
    exec(ymqpp__fqifn, {}, urv__bjr)
    zttun__kwf = urv__bjr['csv_impl']
    ntq__mwp = csv_node.usecols
    if ntq__mwp:
        ntq__mwp = [csv_node.usecols[gnm__kzyqd] for gnm__kzyqd in csv_node
            .type_usecol_offset]
    if bodo.user_logging.get_verbose_level() >= 1:
        qzdv__mtc = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        rehcz__ytahn = csv_node.loc.strformat()
        khq__kxogq = []
        mwz__rvu = []
        if ntq__mwp:
            for gnm__kzyqd in ntq__mwp:
                wgdr__gakc = csv_node.df_colnames[gnm__kzyqd]
                khq__kxogq.append(wgdr__gakc)
                if isinstance(csv_node.out_types[gnm__kzyqd], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    mwz__rvu.append(wgdr__gakc)
        bodo.user_logging.log_message('Column Pruning', qzdv__mtc,
            rehcz__ytahn, khq__kxogq)
        if mwz__rvu:
            hjrf__mnv = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', hjrf__mnv,
                rehcz__ytahn, mwz__rvu)
    ekfj__mic = _gen_csv_reader_py(csv_node.df_colnames, csv_node.out_types,
        ntq__mwp, csv_node.type_usecol_offset, csv_node.sep, parallel,
        csv_node.header, csv_node.compression, csv_node.is_skiprows_list,
        csv_node.pd_low_memory, csv_node.escapechar, csv_node.
        storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    ewrq__puv = compile_to_numba_ir(zttun__kwf, {'_csv_reader_py':
        ekfj__mic}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, vnjkb__cmkge), typemap=typemap, calltypes
        =calltypes).blocks.popitem()[1]
    replace_arg_nodes(ewrq__puv, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    pbmf__ace = ewrq__puv.body[:-3]
    pbmf__ace[-1].target = csv_node.out_vars[1]
    pbmf__ace[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not ntq__mwp
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        pbmf__ace.pop(-1)
    elif not ntq__mwp:
        pbmf__ace.pop(-2)
    return pbmf__ace


def csv_remove_dead_column(csv_node, column_live_map, equiv_vars, typemap):
    if csv_node.chunksize is not None:
        return False
    return bodo.ir.connector.base_connector_remove_dead_columns(csv_node,
        column_live_map, equiv_vars, typemap, 'CSVReader', csv_node.usecols)


numba.parfors.array_analysis.array_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[CsvReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[CsvReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[CsvReader] = remove_dead_csv
numba.core.analysis.ir_extension_usedefs[CsvReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[CsvReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[CsvReader] = csv_distributed_run
remove_dead_column_extensions[CsvReader] = csv_remove_dead_column
ir_extension_table_column_use[CsvReader
    ] = bodo.ir.connector.connector_table_column_use


def _get_dtype_str(t):
    ckazc__lax = t.dtype
    if isinstance(ckazc__lax, PDCategoricalDtype):
        yefi__ecktt = CategoricalArrayType(ckazc__lax)
        yeob__risjv = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, yeob__risjv, yefi__ecktt)
        return yeob__risjv
    if ckazc__lax == types.NPDatetime('ns'):
        ckazc__lax = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        myqm__xjr = 'int_arr_{}'.format(ckazc__lax)
        setattr(types, myqm__xjr, t)
        return myqm__xjr
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if ckazc__lax == types.bool_:
        ckazc__lax = 'bool_'
    if ckazc__lax == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(ckazc__lax, (
        StringArrayType, ArrayItemArrayType)):
        kqkwh__xbo = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, kqkwh__xbo, t)
        return kqkwh__xbo
    return '{}[::1]'.format(ckazc__lax)


def _get_pd_dtype_str(t):
    ckazc__lax = t.dtype
    if isinstance(ckazc__lax, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(ckazc__lax.categories)
    if ckazc__lax == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if ckazc__lax.signed else 'U',
            ckazc__lax.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(ckazc__lax, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(ckazc__lax)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    ddnp__jtg = ''
    from collections import defaultdict
    oiery__ese = defaultdict(list)
    for hgs__luzt, gwh__pebwa in typemap.items():
        oiery__ese[gwh__pebwa].append(hgs__luzt)
    dhua__etgh = df.columns.to_list()
    oyytx__gpyqr = []
    for gwh__pebwa, hhk__ofbv in oiery__ese.items():
        try:
            oyytx__gpyqr.append(df.loc[:, hhk__ofbv].astype(gwh__pebwa,
                copy=False))
            df = df.drop(hhk__ofbv, axis=1)
        except (ValueError, TypeError) as zwefl__ybc:
            ddnp__jtg = (
                f"Caught the runtime error '{zwefl__ybc}' on columns {hhk__ofbv}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    ecpi__xkpt = bool(ddnp__jtg)
    if parallel:
        rpkki__ayn = MPI.COMM_WORLD
        ecpi__xkpt = rpkki__ayn.allreduce(ecpi__xkpt, op=MPI.LOR)
    if ecpi__xkpt:
        hgc__kvy = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if ddnp__jtg:
            raise TypeError(f'{hgc__kvy}\n{ddnp__jtg}')
        else:
            raise TypeError(
                f'{hgc__kvy}\nPlease refer to errors on other ranks.')
    df = pd.concat(oyytx__gpyqr + [df], axis=1)
    swifw__mzlin = df.loc[:, dhua__etgh]
    return swifw__mzlin


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    mvx__xnwaj = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        ymqpp__fqifn = '  skiprows = sorted(set(skiprows))\n'
    else:
        ymqpp__fqifn = '  skiprows = [skiprows]\n'
    ymqpp__fqifn += '  skiprows_list_len = len(skiprows)\n'
    ymqpp__fqifn += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    ymqpp__fqifn += '  check_java_installation(fname)\n'
    ymqpp__fqifn += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    ymqpp__fqifn += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    ymqpp__fqifn += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    ymqpp__fqifn += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, mvx__xnwaj, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    ymqpp__fqifn += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    ymqpp__fqifn += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    ymqpp__fqifn += "      raise FileNotFoundError('File does not exist')\n"
    return ymqpp__fqifn


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    mgq__hzntk = [str(gnm__kzyqd) for gnm__kzyqd, dfn__rlca in enumerate(
        usecols) if col_typs[type_usecol_offset[gnm__kzyqd]].dtype == types
        .NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        mgq__hzntk.append(str(idx_col_index))
    fud__jjim = ', '.join(mgq__hzntk)
    pga__ryt = _gen_parallel_flag_name(sanitized_cnames)
    ienlh__kkp = f"{pga__ryt}='bool_'" if check_parallel_runtime else ''
    blo__hyilv = [_get_pd_dtype_str(col_typs[type_usecol_offset[gnm__kzyqd]
        ]) for gnm__kzyqd in range(len(usecols))]
    qsbdo__wwhk = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    ygnf__kay = [dfn__rlca for gnm__kzyqd, dfn__rlca in enumerate(usecols) if
        blo__hyilv[gnm__kzyqd] == 'str']
    if idx_col_index is not None and qsbdo__wwhk == 'str':
        ygnf__kay.append(idx_col_index)
    wvh__rxos = np.array(ygnf__kay, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = wvh__rxos
    ymqpp__fqifn = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    xzfxg__mgdn = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = xzfxg__mgdn
    ymqpp__fqifn += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    dcs__txiuq = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = dcs__txiuq
        ymqpp__fqifn += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    vnbo__mxom = defaultdict(list)
    for gnm__kzyqd, dfn__rlca in enumerate(usecols):
        if blo__hyilv[gnm__kzyqd] == 'str':
            continue
        vnbo__mxom[blo__hyilv[gnm__kzyqd]].append(dfn__rlca)
    if idx_col_index is not None and qsbdo__wwhk != 'str':
        vnbo__mxom[qsbdo__wwhk].append(idx_col_index)
    for gnm__kzyqd, hqw__mvy in enumerate(vnbo__mxom.values()):
        glbs[f't_arr_{gnm__kzyqd}_{call_id}'] = np.asarray(hqw__mvy)
        ymqpp__fqifn += (
            f'  t_arr_{gnm__kzyqd}_{call_id}_2 = t_arr_{gnm__kzyqd}_{call_id}\n'
            )
    if idx_col_index != None:
        ymqpp__fqifn += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {ienlh__kkp}):
"""
    else:
        ymqpp__fqifn += (
            f'  with objmode(T=table_type_{call_id}, {ienlh__kkp}):\n')
    ymqpp__fqifn += f'    typemap = {{}}\n'
    for gnm__kzyqd, pwpq__toth in enumerate(vnbo__mxom.keys()):
        ymqpp__fqifn += f"""    typemap.update({{i:{pwpq__toth} for i in t_arr_{gnm__kzyqd}_{call_id}_2}})
"""
    ymqpp__fqifn += '    if f_reader.get_chunk_size() == 0:\n'
    ymqpp__fqifn += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    ymqpp__fqifn += '    else:\n'
    ymqpp__fqifn += '      df = pd.read_csv(f_reader,\n'
    ymqpp__fqifn += '        header=None,\n'
    ymqpp__fqifn += '        parse_dates=[{}],\n'.format(fud__jjim)
    ymqpp__fqifn += (
        f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n')
    ymqpp__fqifn += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        ymqpp__fqifn += f'    {pga__ryt} = f_reader.is_parallel()\n'
    else:
        ymqpp__fqifn += f'    {pga__ryt} = {parallel}\n'
    ymqpp__fqifn += f'    df = astype(df, typemap, {pga__ryt})\n'
    if idx_col_index != None:
        mgeci__ycc = sorted(xzfxg__mgdn).index(idx_col_index)
        ymqpp__fqifn += f'    idx_arr = df.iloc[:, {mgeci__ycc}].values\n'
        ymqpp__fqifn += (
            f'    df.drop(columns=df.columns[{mgeci__ycc}], inplace=True)\n')
    if len(usecols) == 0:
        ymqpp__fqifn += f'    T = None\n'
    else:
        ymqpp__fqifn += f'    arrs = []\n'
        ymqpp__fqifn += f'    for i in range(df.shape[1]):\n'
        ymqpp__fqifn += f'      arrs.append(df.iloc[:, i].values)\n'
        ymqpp__fqifn += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return ymqpp__fqifn


def _gen_parallel_flag_name(sanitized_cnames):
    pga__ryt = '_parallel_value'
    while pga__ryt in sanitized_cnames:
        pga__ryt = '_' + pga__ryt
    return pga__ryt


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(osmqb__wgzqp) for osmqb__wgzqp in
        col_names]
    ymqpp__fqifn = 'def csv_reader_py(fname, nrows, skiprows):\n'
    ymqpp__fqifn += _gen_csv_file_reader_init(parallel, header, compression,
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    ner__hvjv = globals()
    if idx_col_typ != types.none:
        ner__hvjv[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        ner__hvjv[f'table_type_{call_id}'] = types.none
    else:
        ner__hvjv[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    ymqpp__fqifn += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, type_usecol_offset, sep, escapechar,
        storage_options, call_id, ner__hvjv, parallel=parallel,
        check_parallel_runtime=False, idx_col_index=idx_col_index,
        idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        ymqpp__fqifn += '  return (T, idx_arr)\n'
    else:
        ymqpp__fqifn += '  return (T, None)\n'
    urv__bjr = {}
    ner__hvjv['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(ymqpp__fqifn, ner__hvjv, urv__bjr)
    ekfj__mic = urv__bjr['csv_reader_py']
    etss__ajbrh = numba.njit(ekfj__mic)
    compiled_funcs.append(etss__ajbrh)
    return etss__ajbrh
