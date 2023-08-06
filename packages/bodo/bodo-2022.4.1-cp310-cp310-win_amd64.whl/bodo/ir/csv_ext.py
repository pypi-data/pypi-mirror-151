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
    kvekw__pwsn = typemap[node.file_name.name]
    if types.unliteral(kvekw__pwsn) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {kvekw__pwsn}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        trr__aatbz = typemap[node.skiprows.name]
        if isinstance(trr__aatbz, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(trr__aatbz, types.Integer) and not (isinstance(
            trr__aatbz, (types.List, types.Tuple)) and isinstance(
            trr__aatbz.dtype, types.Integer)) and not isinstance(trr__aatbz,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {trr__aatbz}."
                , loc=node.skiprows.loc)
        elif isinstance(trr__aatbz, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        rjp__hte = typemap[node.nrows.name]
        if not isinstance(rjp__hte, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {rjp__hte}."
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
        ktlwn__ueu = csv_node.out_vars[0]
        if ktlwn__ueu.name not in lives:
            return None
    else:
        meggn__beou = csv_node.out_vars[0]
        ppmbf__lvl = csv_node.out_vars[1]
        if meggn__beou.name not in lives and ppmbf__lvl.name not in lives:
            return None
        elif ppmbf__lvl.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif meggn__beou.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.type_usecol_offset = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    trr__aatbz = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            dig__uvapf = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            dziy__njswo = csv_node.loc.strformat()
            qtvzu__cafrv = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', dig__uvapf,
                dziy__njswo, qtvzu__cafrv)
            rrj__nssp = csv_node.out_types[0].yield_type.data
            zgz__yieu = [bmg__pec for iziea__dttve, bmg__pec in enumerate(
                csv_node.df_colnames) if isinstance(rrj__nssp[iziea__dttve],
                bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if zgz__yieu:
                evxp__otzi = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    evxp__otzi, dziy__njswo, zgz__yieu)
        if array_dists is not None:
            iutky__spa = csv_node.out_vars[0].name
            parallel = array_dists[iutky__spa] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        veg__fhe = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        veg__fhe += f'    reader = _csv_reader_init(fname, nrows, skiprows)\n'
        veg__fhe += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        zvnum__kjzkd = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(veg__fhe, {}, zvnum__kjzkd)
        wqres__sdwuz = zvnum__kjzkd['csv_iterator_impl']
        kuc__yswl = 'def csv_reader_init(fname, nrows, skiprows):\n'
        kuc__yswl += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        kuc__yswl += '  return f_reader\n'
        exec(kuc__yswl, globals(), zvnum__kjzkd)
        gmypu__jcxq = zvnum__kjzkd['csv_reader_init']
        tjmfp__qwhlr = numba.njit(gmypu__jcxq)
        compiled_funcs.append(tjmfp__qwhlr)
        juf__zejz = compile_to_numba_ir(wqres__sdwuz, {'_csv_reader_init':
            tjmfp__qwhlr, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, trr__aatbz), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(juf__zejz, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        urfw__sclop = juf__zejz.body[:-3]
        urfw__sclop[-1].target = csv_node.out_vars[0]
        return urfw__sclop
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    veg__fhe = 'def csv_impl(fname, nrows, skiprows):\n'
    veg__fhe += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    zvnum__kjzkd = {}
    exec(veg__fhe, {}, zvnum__kjzkd)
    tki__cbtce = zvnum__kjzkd['csv_impl']
    hsywe__ekwc = csv_node.usecols
    if hsywe__ekwc:
        hsywe__ekwc = [csv_node.usecols[iziea__dttve] for iziea__dttve in
            csv_node.type_usecol_offset]
    if bodo.user_logging.get_verbose_level() >= 1:
        dig__uvapf = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        dziy__njswo = csv_node.loc.strformat()
        qtvzu__cafrv = []
        zgz__yieu = []
        if hsywe__ekwc:
            for iziea__dttve in hsywe__ekwc:
                gjdts__twz = csv_node.df_colnames[iziea__dttve]
                qtvzu__cafrv.append(gjdts__twz)
                if isinstance(csv_node.out_types[iziea__dttve], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    zgz__yieu.append(gjdts__twz)
        bodo.user_logging.log_message('Column Pruning', dig__uvapf,
            dziy__njswo, qtvzu__cafrv)
        if zgz__yieu:
            evxp__otzi = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', evxp__otzi,
                dziy__njswo, zgz__yieu)
    ygzj__woas = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, hsywe__ekwc, csv_node.type_usecol_offset, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    juf__zejz = compile_to_numba_ir(tki__cbtce, {'_csv_reader_py':
        ygzj__woas}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, trr__aatbz), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(juf__zejz, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    urfw__sclop = juf__zejz.body[:-3]
    urfw__sclop[-1].target = csv_node.out_vars[1]
    urfw__sclop[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not hsywe__ekwc
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        urfw__sclop.pop(-1)
    elif not hsywe__ekwc:
        urfw__sclop.pop(-2)
    return urfw__sclop


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
    tnwxg__xuc = t.dtype
    if isinstance(tnwxg__xuc, PDCategoricalDtype):
        uah__byhtn = CategoricalArrayType(tnwxg__xuc)
        ypqke__pbgv = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, ypqke__pbgv, uah__byhtn)
        return ypqke__pbgv
    if tnwxg__xuc == types.NPDatetime('ns'):
        tnwxg__xuc = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        pom__affnc = 'int_arr_{}'.format(tnwxg__xuc)
        setattr(types, pom__affnc, t)
        return pom__affnc
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if tnwxg__xuc == types.bool_:
        tnwxg__xuc = 'bool_'
    if tnwxg__xuc == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(tnwxg__xuc, (
        StringArrayType, ArrayItemArrayType)):
        hmonf__ydun = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, hmonf__ydun, t)
        return hmonf__ydun
    return '{}[::1]'.format(tnwxg__xuc)


def _get_pd_dtype_str(t):
    tnwxg__xuc = t.dtype
    if isinstance(tnwxg__xuc, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(tnwxg__xuc.categories)
    if tnwxg__xuc == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if tnwxg__xuc.signed else 'U',
            tnwxg__xuc.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(tnwxg__xuc, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(tnwxg__xuc)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    jqppn__vdut = ''
    from collections import defaultdict
    mqll__ulwn = defaultdict(list)
    for ltmqd__snewd, htlmi__tlus in typemap.items():
        mqll__ulwn[htlmi__tlus].append(ltmqd__snewd)
    ufeac__odh = df.columns.to_list()
    xaref__cxilq = []
    for htlmi__tlus, orq__bnpg in mqll__ulwn.items():
        try:
            xaref__cxilq.append(df.loc[:, orq__bnpg].astype(htlmi__tlus,
                copy=False))
            df = df.drop(orq__bnpg, axis=1)
        except (ValueError, TypeError) as tulk__xcrs:
            jqppn__vdut = (
                f"Caught the runtime error '{tulk__xcrs}' on columns {orq__bnpg}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    qbl__mfhu = bool(jqppn__vdut)
    if parallel:
        mga__now = MPI.COMM_WORLD
        qbl__mfhu = mga__now.allreduce(qbl__mfhu, op=MPI.LOR)
    if qbl__mfhu:
        dkhm__ttz = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if jqppn__vdut:
            raise TypeError(f'{dkhm__ttz}\n{jqppn__vdut}')
        else:
            raise TypeError(
                f'{dkhm__ttz}\nPlease refer to errors on other ranks.')
    df = pd.concat(xaref__cxilq + [df], axis=1)
    tgqby__gfhoq = df.loc[:, ufeac__odh]
    return tgqby__gfhoq


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    bqbr__lgt = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        veg__fhe = '  skiprows = sorted(set(skiprows))\n'
    else:
        veg__fhe = '  skiprows = [skiprows]\n'
    veg__fhe += '  skiprows_list_len = len(skiprows)\n'
    veg__fhe += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    veg__fhe += '  check_java_installation(fname)\n'
    veg__fhe += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    veg__fhe += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    veg__fhe += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    veg__fhe += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, bqbr__lgt, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    veg__fhe += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    veg__fhe += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    veg__fhe += "      raise FileNotFoundError('File does not exist')\n"
    return veg__fhe


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    type_usecol_offset, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    aatho__jdr = [str(iziea__dttve) for iziea__dttve, waio__xgtq in
        enumerate(usecols) if col_typs[type_usecol_offset[iziea__dttve]].
        dtype == types.NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        aatho__jdr.append(str(idx_col_index))
    phnv__hud = ', '.join(aatho__jdr)
    dfx__ajub = _gen_parallel_flag_name(sanitized_cnames)
    zvvp__rnmee = f"{dfx__ajub}='bool_'" if check_parallel_runtime else ''
    yfrs__cbdu = [_get_pd_dtype_str(col_typs[type_usecol_offset[
        iziea__dttve]]) for iziea__dttve in range(len(usecols))]
    rep__yfk = None if idx_col_index is None else _get_pd_dtype_str(idx_col_typ
        )
    dkq__pgjqb = [waio__xgtq for iziea__dttve, waio__xgtq in enumerate(
        usecols) if yfrs__cbdu[iziea__dttve] == 'str']
    if idx_col_index is not None and rep__yfk == 'str':
        dkq__pgjqb.append(idx_col_index)
    vzr__qnvrr = np.array(dkq__pgjqb, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = vzr__qnvrr
    veg__fhe = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    wdtqt__pqcm = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = wdtqt__pqcm
    veg__fhe += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    hsz__jlnpt = np.array(type_usecol_offset, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = hsz__jlnpt
        veg__fhe += (
            f'  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}\n'
            )
    uwfgs__qissn = defaultdict(list)
    for iziea__dttve, waio__xgtq in enumerate(usecols):
        if yfrs__cbdu[iziea__dttve] == 'str':
            continue
        uwfgs__qissn[yfrs__cbdu[iziea__dttve]].append(waio__xgtq)
    if idx_col_index is not None and rep__yfk != 'str':
        uwfgs__qissn[rep__yfk].append(idx_col_index)
    for iziea__dttve, iglq__qdwz in enumerate(uwfgs__qissn.values()):
        glbs[f't_arr_{iziea__dttve}_{call_id}'] = np.asarray(iglq__qdwz)
        veg__fhe += (
            f'  t_arr_{iziea__dttve}_{call_id}_2 = t_arr_{iziea__dttve}_{call_id}\n'
            )
    if idx_col_index != None:
        veg__fhe += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {zvvp__rnmee}):
"""
    else:
        veg__fhe += f'  with objmode(T=table_type_{call_id}, {zvvp__rnmee}):\n'
    veg__fhe += f'    typemap = {{}}\n'
    for iziea__dttve, epb__yfw in enumerate(uwfgs__qissn.keys()):
        veg__fhe += f"""    typemap.update({{i:{epb__yfw} for i in t_arr_{iziea__dttve}_{call_id}_2}})
"""
    veg__fhe += '    if f_reader.get_chunk_size() == 0:\n'
    veg__fhe += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    veg__fhe += '    else:\n'
    veg__fhe += '      df = pd.read_csv(f_reader,\n'
    veg__fhe += '        header=None,\n'
    veg__fhe += '        parse_dates=[{}],\n'.format(phnv__hud)
    veg__fhe += f'        dtype={{i:str for i in str_col_nums_{call_id}_2}},\n'
    veg__fhe += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        veg__fhe += f'    {dfx__ajub} = f_reader.is_parallel()\n'
    else:
        veg__fhe += f'    {dfx__ajub} = {parallel}\n'
    veg__fhe += f'    df = astype(df, typemap, {dfx__ajub})\n'
    if idx_col_index != None:
        eego__nyazx = sorted(wdtqt__pqcm).index(idx_col_index)
        veg__fhe += f'    idx_arr = df.iloc[:, {eego__nyazx}].values\n'
        veg__fhe += (
            f'    df.drop(columns=df.columns[{eego__nyazx}], inplace=True)\n')
    if len(usecols) == 0:
        veg__fhe += f'    T = None\n'
    else:
        veg__fhe += f'    arrs = []\n'
        veg__fhe += f'    for i in range(df.shape[1]):\n'
        veg__fhe += f'      arrs.append(df.iloc[:, i].values)\n'
        veg__fhe += (
            f'    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})\n'
            )
    return veg__fhe


def _gen_parallel_flag_name(sanitized_cnames):
    dfx__ajub = '_parallel_value'
    while dfx__ajub in sanitized_cnames:
        dfx__ajub = '_' + dfx__ajub
    return dfx__ajub


def _gen_csv_reader_py(col_names, col_typs, usecols, type_usecol_offset,
    sep, parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(bmg__pec) for bmg__pec in col_names]
    veg__fhe = 'def csv_reader_py(fname, nrows, skiprows):\n'
    veg__fhe += _gen_csv_file_reader_init(parallel, header, compression, -1,
        is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    eeh__oaxq = globals()
    if idx_col_typ != types.none:
        eeh__oaxq[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        eeh__oaxq[f'table_type_{call_id}'] = types.none
    else:
        eeh__oaxq[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    veg__fhe += _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs,
        usecols, type_usecol_offset, sep, escapechar, storage_options,
        call_id, eeh__oaxq, parallel=parallel, check_parallel_runtime=False,
        idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        veg__fhe += '  return (T, idx_arr)\n'
    else:
        veg__fhe += '  return (T, None)\n'
    zvnum__kjzkd = {}
    eeh__oaxq['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(veg__fhe, eeh__oaxq, zvnum__kjzkd)
    ygzj__woas = zvnum__kjzkd['csv_reader_py']
    tjmfp__qwhlr = numba.njit(ygzj__woas)
    compiled_funcs.append(tjmfp__qwhlr)
    return tjmfp__qwhlr
