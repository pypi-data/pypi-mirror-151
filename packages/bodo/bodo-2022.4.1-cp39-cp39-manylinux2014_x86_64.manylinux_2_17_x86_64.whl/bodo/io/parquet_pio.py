import os
import warnings
from collections import defaultdict
from glob import has_magic
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow
import pyarrow.dataset as ds
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, get_definition, guard, mk_unique_var, next_label, replace_arg_nodes
from numba.extending import NativeValue, intrinsic, models, overload, register_model, unbox
from pyarrow import null
import bodo
import bodo.ir.parquet_ext
import bodo.utils.tracing as tracing
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import TableType
from bodo.io.fs_io import get_hdfs_fs, get_s3_fs_from_path, get_s3_subtree_fs, get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import get_end, get_start
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.transforms import distributed_pass
from bodo.utils.transform import get_const_value
from bodo.utils.typing import BodoError, BodoWarning, FileInfo, get_overload_const_str
from bodo.utils.utils import check_and_propagate_cpp_exception, numba_to_c_type, sanitize_varname
use_nullable_int_arr = True
from urllib.parse import urlparse
import bodo.io.pa_parquet
REMOTE_FILESYSTEMS = {'s3', 'gcs', 'gs', 'http', 'hdfs', 'abfs', 'abfss'}
READ_STR_AS_DICT_THRESHOLD = 1.0
list_of_files_error_msg = (
    '. Make sure the list/glob passed to read_parquet() only contains paths to files (no directories)'
    )


class ParquetPredicateType(types.Type):

    def __init__(self):
        super(ParquetPredicateType, self).__init__(name=
            'ParquetPredicateType()')


parquet_predicate_type = ParquetPredicateType()
types.parquet_predicate_type = parquet_predicate_type
register_model(ParquetPredicateType)(models.OpaqueModel)


@unbox(ParquetPredicateType)
def unbox_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ReadParquetFilepathType(types.Opaque):

    def __init__(self):
        super(ReadParquetFilepathType, self).__init__(name=
            'ReadParquetFilepathType')


read_parquet_fpath_type = ReadParquetFilepathType()
types.read_parquet_fpath_type = read_parquet_fpath_type
register_model(ReadParquetFilepathType)(models.OpaqueModel)


@unbox(ReadParquetFilepathType)
def unbox_read_parquet_fpath_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ParquetFileInfo(FileInfo):

    def __init__(self, columns, storage_options=None, input_file_name_col=
        None, read_as_dict_cols=None):
        self.columns = columns
        self.storage_options = storage_options
        self.input_file_name_col = input_file_name_col
        self.read_as_dict_cols = read_as_dict_cols
        super().__init__()

    def _get_schema(self, fname):
        try:
            return parquet_file_schema(fname, selected_columns=self.columns,
                storage_options=self.storage_options, input_file_name_col=
                self.input_file_name_col, read_as_dict_cols=self.
                read_as_dict_cols)
        except OSError as oqcs__tvx:
            if 'non-file path' in str(oqcs__tvx):
                raise FileNotFoundError(str(oqcs__tvx))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        vgoj__yebdi = lhs.scope
        udfjr__wkdu = lhs.loc
        vlmw__hha = None
        if lhs.name in self.locals:
            vlmw__hha = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        xrwh__wbvld = {}
        if lhs.name + ':convert' in self.locals:
            xrwh__wbvld = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if vlmw__hha is None:
            tywyb__gwkkj = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/file_io.html#io_workflow'
                )
            xsct__jfs = get_const_value(file_name, self.func_ir,
                tywyb__gwkkj, arg_types=self.args, file_info=
                ParquetFileInfo(columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols))
            uoz__upvw = False
            kmohl__slxn = guard(get_definition, self.func_ir, file_name)
            if isinstance(kmohl__slxn, ir.Arg):
                typ = self.args[kmohl__slxn.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, lgjh__hdore, gnker__ampcz, col_indices,
                        partition_names, zlv__ekdd, pchb__mgpb) = typ.schema
                    uoz__upvw = True
            if not uoz__upvw:
                (col_names, lgjh__hdore, gnker__ampcz, col_indices,
                    partition_names, zlv__ekdd, pchb__mgpb) = (
                    parquet_file_schema(xsct__jfs, columns, storage_options
                    =storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            lcyu__iier = list(vlmw__hha.keys())
            lcmn__apcv = {c: tcau__aaw for tcau__aaw, c in enumerate(
                lcyu__iier)}
            dxs__afe = [eyf__ufltg for eyf__ufltg in vlmw__hha.values()]
            gnker__ampcz = 'index' if 'index' in lcmn__apcv else None
            if columns is None:
                selected_columns = lcyu__iier
            else:
                selected_columns = columns
            col_indices = [lcmn__apcv[c] for c in selected_columns]
            lgjh__hdore = [dxs__afe[lcmn__apcv[c]] for c in selected_columns]
            col_names = selected_columns
            gnker__ampcz = gnker__ampcz if gnker__ampcz in col_names else None
            partition_names = []
            zlv__ekdd = []
            pchb__mgpb = []
        mxlx__ymkhj = None if isinstance(gnker__ampcz, dict
            ) or gnker__ampcz is None else gnker__ampcz
        index_column_index = None
        index_column_type = types.none
        if mxlx__ymkhj:
            kebri__klex = col_names.index(mxlx__ymkhj)
            index_column_index = col_indices.pop(kebri__klex)
            index_column_type = lgjh__hdore.pop(kebri__klex)
            col_names.pop(kebri__klex)
        for tcau__aaw, c in enumerate(col_names):
            if c in xrwh__wbvld:
                lgjh__hdore[tcau__aaw] = xrwh__wbvld[c]
        oxn__pdu = [ir.Var(vgoj__yebdi, mk_unique_var('pq_table'),
            udfjr__wkdu), ir.Var(vgoj__yebdi, mk_unique_var('pq_index'),
            udfjr__wkdu)]
        epn__gtxd = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, lgjh__hdore, oxn__pdu, udfjr__wkdu,
            partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, zlv__ekdd, pchb__mgpb)]
        return (col_names, oxn__pdu, gnker__ampcz, epn__gtxd, lgjh__hdore,
            index_column_type)


def determine_filter_cast(pq_node, typemap, filter_val, orig_colname_map):
    jkw__byhl = filter_val[0]
    aanwy__ybs = pq_node.original_out_types[orig_colname_map[jkw__byhl]]
    lqf__hyvs = bodo.utils.typing.element_type(aanwy__ybs)
    if jkw__byhl in pq_node.partition_names:
        if lqf__hyvs == types.unicode_type:
            mwphq__yay = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(lqf__hyvs, types.Integer):
            mwphq__yay = f'.cast(pyarrow.{lqf__hyvs.name}(), safe=False)'
        else:
            mwphq__yay = ''
    else:
        mwphq__yay = ''
    ymeu__hdzf = typemap[filter_val[2].name]
    if isinstance(ymeu__hdzf, (types.List, types.Set)):
        mvkr__rvwzw = ymeu__hdzf.dtype
    else:
        mvkr__rvwzw = ymeu__hdzf
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lqf__hyvs,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(mvkr__rvwzw,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([lqf__hyvs, mvkr__rvwzw]):
        if not bodo.utils.typing.is_safe_arrow_cast(lqf__hyvs, mvkr__rvwzw):
            raise BodoError(
                f'Unsupported Arrow cast from {lqf__hyvs} to {mvkr__rvwzw} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if lqf__hyvs == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif lqf__hyvs in (bodo.datetime64ns, bodo.pd_timestamp_type):
            if isinstance(ymeu__hdzf, (types.List, types.Set)):
                tzufl__rgy = 'list' if isinstance(ymeu__hdzf, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {tzufl__rgy} values with isin filter pushdown.'
                    )
            return mwphq__yay, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return mwphq__yay, ''


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    fwdf__fcw = len(pq_node.out_vars)
    extra_args = ''
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    myxa__vgh, agve__icyoc = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    if pq_node.filters:
        dwj__peooi = []
        tft__cftx = []
        yrur__djj = False
        dgvr__zmr = None
        orig_colname_map = {c: tcau__aaw for tcau__aaw, c in enumerate(
            pq_node.original_df_colnames)}
        for rkr__sfe in pq_node.filters:
            uztre__zjlie = []
            hwy__lyhwu = []
            imhuf__qplnz = set()
            for ugxdw__jtwgf in rkr__sfe:
                if isinstance(ugxdw__jtwgf[2], ir.Var):
                    feoic__qabkt, emnng__mrtqz = determine_filter_cast(pq_node,
                        typemap, ugxdw__jtwgf, orig_colname_map)
                    if ugxdw__jtwgf[1] == 'in':
                        hwy__lyhwu.append(
                            f"(ds.field('{ugxdw__jtwgf[0]}').isin({myxa__vgh[ugxdw__jtwgf[2].name]}))"
                            )
                    else:
                        hwy__lyhwu.append(
                            f"(ds.field('{ugxdw__jtwgf[0]}'){feoic__qabkt} {ugxdw__jtwgf[1]} ds.scalar({myxa__vgh[ugxdw__jtwgf[2].name]}){emnng__mrtqz})"
                            )
                else:
                    assert ugxdw__jtwgf[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if ugxdw__jtwgf[1] == 'is not':
                        prefix = '~'
                    else:
                        prefix = ''
                    hwy__lyhwu.append(
                        f"({prefix}ds.field('{ugxdw__jtwgf[0]}').is_null())")
                if ugxdw__jtwgf[0] in pq_node.partition_names and isinstance(
                    ugxdw__jtwgf[2], ir.Var):
                    zexbk__mnz = (
                        f"('{ugxdw__jtwgf[0]}', '{ugxdw__jtwgf[1]}', {myxa__vgh[ugxdw__jtwgf[2].name]})"
                        )
                    uztre__zjlie.append(zexbk__mnz)
                    imhuf__qplnz.add(zexbk__mnz)
                else:
                    yrur__djj = True
            if dgvr__zmr is None:
                dgvr__zmr = imhuf__qplnz
            else:
                dgvr__zmr.intersection_update(imhuf__qplnz)
            luw__rxaaa = ', '.join(uztre__zjlie)
            qszd__kfqx = ' & '.join(hwy__lyhwu)
            if luw__rxaaa:
                dwj__peooi.append(f'[{luw__rxaaa}]')
            tft__cftx.append(f'({qszd__kfqx})')
        ksydi__ywq = ', '.join(dwj__peooi)
        mym__rbrq = ' | '.join(tft__cftx)
        if yrur__djj:
            if dgvr__zmr:
                qeq__brgfe = sorted(dgvr__zmr)
                dnf_filter_str = f"[[{', '.join(qeq__brgfe)}]]"
        elif ksydi__ywq:
            dnf_filter_str = f'[{ksydi__ywq}]'
        expr_filter_str = f'({mym__rbrq})'
        extra_args = ', '.join(myxa__vgh.values())
    gfs__fjnj = ', '.join(f'out{tcau__aaw}' for tcau__aaw in range(fwdf__fcw))
    bloq__dzc = f'def pq_impl(fname, {extra_args}):\n'
    bloq__dzc += (
        f'    (total_rows, {gfs__fjnj},) = _pq_reader_py(fname, {extra_args})\n'
        )
    cmyge__rdmlp = {}
    exec(bloq__dzc, {}, cmyge__rdmlp)
    zwj__iyf = cmyge__rdmlp['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        uesy__vwh = pq_node.loc.strformat()
        tdor__fplf = []
        ttze__upjet = []
        for tcau__aaw in pq_node.type_usecol_offset:
            jkw__byhl = pq_node.df_colnames[tcau__aaw]
            tdor__fplf.append(jkw__byhl)
            if isinstance(pq_node.out_types[tcau__aaw], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                ttze__upjet.append(jkw__byhl)
        hmyos__bjrx = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', hmyos__bjrx,
            uesy__vwh, tdor__fplf)
        if ttze__upjet:
            defv__noj = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', defv__noj,
                uesy__vwh, ttze__upjet)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        uefou__gmds = set(pq_node.type_usecol_offset)
        cfig__vllm = set(pq_node.unsupported_columns)
        rkva__hmzjv = uefou__gmds & cfig__vllm
        if rkva__hmzjv:
            ipzy__yitgi = sorted(rkva__hmzjv)
            webb__wfca = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            itfgf__pngc = 0
            for qyksi__qen in ipzy__yitgi:
                while pq_node.unsupported_columns[itfgf__pngc] != qyksi__qen:
                    itfgf__pngc += 1
                webb__wfca.append(
                    f"Column '{pq_node.df_colnames[qyksi__qen]}' with unsupported arrow type {pq_node.unsupported_arrow_types[itfgf__pngc]}"
                    )
                itfgf__pngc += 1
            laeo__kyyv = '\n'.join(webb__wfca)
            raise BodoError(laeo__kyyv, loc=pq_node.loc)
    pfly__ukr = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.type_usecol_offset, pq_node.out_types, pq_node.
        storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col)
    imimx__fzp = typemap[pq_node.file_name.name]
    ycqrz__rhr = (imimx__fzp,) + tuple(typemap[ugxdw__jtwgf.name] for
        ugxdw__jtwgf in agve__icyoc)
    rqr__fwa = compile_to_numba_ir(zwj__iyf, {'_pq_reader_py': pfly__ukr},
        typingctx=typingctx, targetctx=targetctx, arg_typs=ycqrz__rhr,
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(rqr__fwa, [pq_node.file_name] + agve__icyoc)
    epn__gtxd = rqr__fwa.body[:-3]
    if meta_head_only_info:
        epn__gtxd[-1 - fwdf__fcw].target = meta_head_only_info[1]
    epn__gtxd[-2].target = pq_node.out_vars[0]
    epn__gtxd[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        epn__gtxd.pop(-1)
    elif not pq_node.type_usecol_offset:
        epn__gtxd.pop(-2)
    return epn__gtxd


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    hegr__rev = get_overload_const_str(dnf_filter_str)
    bovy__wgkcg = get_overload_const_str(expr_filter_str)
    vucg__mbeo = ', '.join(f'f{tcau__aaw}' for tcau__aaw in range(len(var_tup))
        )
    bloq__dzc = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        bloq__dzc += f'  {vucg__mbeo}, = var_tup\n'
    bloq__dzc += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    bloq__dzc += f'    dnf_filters_py = {hegr__rev}\n'
    bloq__dzc += f'    expr_filters_py = {bovy__wgkcg}\n'
    bloq__dzc += '  return (dnf_filters_py, expr_filters_py)\n'
    cmyge__rdmlp = {}
    exec(bloq__dzc, globals(), cmyge__rdmlp)
    return cmyge__rdmlp['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col):
    luhfz__cdd = next_label()
    gogsl__ezwt = ',' if extra_args else ''
    bloq__dzc = f'def pq_reader_py(fname,{extra_args}):\n'
    bloq__dzc += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    bloq__dzc += f"    ev.add_attribute('g_fname', fname)\n"
    bloq__dzc += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    bloq__dzc += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{gogsl__ezwt}))
"""
    bloq__dzc += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    bloq__dzc += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    kcs__tbof = not type_usecol_offset
    olafy__eumk = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in type_usecol_offset else None
    kfa__moqcs = {c: tcau__aaw for tcau__aaw, c in enumerate(col_indices)}
    zosi__hib = {c: tcau__aaw for tcau__aaw, c in enumerate(olafy__eumk)}
    snfsj__yfu = []
    jnmbq__quh = set()
    reuse__tsu = partition_names + [input_file_name_col]
    for tcau__aaw in type_usecol_offset:
        if olafy__eumk[tcau__aaw] not in reuse__tsu:
            snfsj__yfu.append(col_indices[tcau__aaw])
        elif not input_file_name_col or olafy__eumk[tcau__aaw
            ] != input_file_name_col:
            jnmbq__quh.add(col_indices[tcau__aaw])
    if index_column_index is not None:
        snfsj__yfu.append(index_column_index)
    snfsj__yfu = sorted(snfsj__yfu)
    ggjm__ein = {c: tcau__aaw for tcau__aaw, c in enumerate(snfsj__yfu)}

    def is_nullable(typ):
        return bodo.utils.utils.is_array_typ(typ, False) and (not
            isinstance(typ, types.Array) and not isinstance(typ, bodo.
            DatetimeArrayType))
    gekrm__qvny = [(int(is_nullable(out_types[kfa__moqcs[gvpc__znbw]])) if 
        gvpc__znbw != index_column_index else int(is_nullable(
        index_column_type))) for gvpc__znbw in snfsj__yfu]
    str_as_dict_cols = []
    for gvpc__znbw in snfsj__yfu:
        if gvpc__znbw == index_column_index:
            eyf__ufltg = index_column_type
        else:
            eyf__ufltg = out_types[kfa__moqcs[gvpc__znbw]]
        if eyf__ufltg == dict_str_arr_type:
            str_as_dict_cols.append(gvpc__znbw)
    osqd__gputg = []
    arf__kyont = {}
    jaklj__aeec = []
    jjnb__swr = []
    for tcau__aaw, tndrk__ier in enumerate(partition_names):
        try:
            wcq__egb = zosi__hib[tndrk__ier]
            if col_indices[wcq__egb] not in jnmbq__quh:
                continue
        except (KeyError, ValueError) as lmpes__win:
            continue
        arf__kyont[tndrk__ier] = len(osqd__gputg)
        osqd__gputg.append(tndrk__ier)
        jaklj__aeec.append(tcau__aaw)
        nxch__yvn = out_types[wcq__egb].dtype
        tih__rdjh = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            nxch__yvn)
        jjnb__swr.append(numba_to_c_type(tih__rdjh))
    bloq__dzc += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    bloq__dzc += f'    out_table = pq_read(\n'
    bloq__dzc += f'        fname_py, {is_parallel},\n'
    bloq__dzc += f'        unicode_to_utf8(bucket_region),\n'
    bloq__dzc += f'        dnf_filters, expr_filters,\n'
    bloq__dzc += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{luhfz__cdd}.ctypes,
"""
    bloq__dzc += f'        {len(snfsj__yfu)},\n'
    bloq__dzc += f'        nullable_cols_arr_{luhfz__cdd}.ctypes,\n'
    if len(jaklj__aeec) > 0:
        bloq__dzc += (
            f'        np.array({jaklj__aeec}, dtype=np.int32).ctypes,\n')
        bloq__dzc += f'        np.array({jjnb__swr}, dtype=np.int32).ctypes,\n'
        bloq__dzc += f'        {len(jaklj__aeec)},\n'
    else:
        bloq__dzc += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        bloq__dzc += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        bloq__dzc += f'        0, 0,\n'
    bloq__dzc += f'        total_rows_np.ctypes,\n'
    bloq__dzc += f'        {input_file_name_col is not None},\n'
    bloq__dzc += f'    )\n'
    bloq__dzc += f'    check_and_propagate_cpp_exception()\n'
    pvix__vhi = 'None'
    fuan__bkoj = index_column_type
    jcoj__zyxxw = TableType(tuple(out_types))
    if kcs__tbof:
        jcoj__zyxxw = types.none
    if index_column_index is not None:
        cqov__pdo = ggjm__ein[index_column_index]
        pvix__vhi = (
            f'info_to_array(info_from_table(out_table, {cqov__pdo}), index_arr_type)'
            )
    bloq__dzc += f'    index_arr = {pvix__vhi}\n'
    if kcs__tbof:
        pcag__sxp = None
    else:
        pcag__sxp = []
        ijrcs__eigq = 0
        get__fuw = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for tcau__aaw, qyksi__qen in enumerate(col_indices):
            if ijrcs__eigq < len(type_usecol_offset
                ) and tcau__aaw == type_usecol_offset[ijrcs__eigq]:
                ywh__tcjfr = col_indices[tcau__aaw]
                if get__fuw and ywh__tcjfr == get__fuw:
                    pcag__sxp.append(len(snfsj__yfu) + len(osqd__gputg))
                elif ywh__tcjfr in jnmbq__quh:
                    gxyw__ntc = olafy__eumk[tcau__aaw]
                    pcag__sxp.append(len(snfsj__yfu) + arf__kyont[gxyw__ntc])
                else:
                    pcag__sxp.append(ggjm__ein[qyksi__qen])
                ijrcs__eigq += 1
            else:
                pcag__sxp.append(-1)
        pcag__sxp = np.array(pcag__sxp, dtype=np.int64)
    if kcs__tbof:
        bloq__dzc += '    T = None\n'
    else:
        bloq__dzc += f"""    T = cpp_table_to_py_table(out_table, table_idx_{luhfz__cdd}, py_table_type_{luhfz__cdd})
"""
    bloq__dzc += f'    delete_table(out_table)\n'
    bloq__dzc += f'    total_rows = total_rows_np[0]\n'
    bloq__dzc += f'    ev.finalize()\n'
    bloq__dzc += f'    return (total_rows, T, index_arr)\n'
    cmyge__rdmlp = {}
    vshj__iqvm = {f'py_table_type_{luhfz__cdd}': jcoj__zyxxw,
        f'table_idx_{luhfz__cdd}': pcag__sxp,
        f'selected_cols_arr_{luhfz__cdd}': np.array(snfsj__yfu, np.int32),
        f'nullable_cols_arr_{luhfz__cdd}': np.array(gekrm__qvny, np.int32),
        'index_arr_type': fuan__bkoj, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(bloq__dzc, vshj__iqvm, cmyge__rdmlp)
    pfly__ukr = cmyge__rdmlp['pq_reader_py']
    kuyi__qvzi = numba.njit(pfly__ukr, no_cpython_wrapper=True)
    return kuyi__qvzi


import pyarrow as pa
_pa_numba_typ_map = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.
    int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
    pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types.
    uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa.
    float64(): types.float64, pa.string(): string_type, pa.binary():
    bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
    NPDatetime('ns'), null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    jflk__yszt = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in jflk__yszt:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        ivs__mkyx = pa_ts_typ.to_pandas_dtype().tz
        dgo__rjze = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(ivs__mkyx)
        return bodo.DatetimeArrayType(dgo__rjze), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        pkg__dnu, jtymm__cqgr = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(pkg__dnu), jtymm__cqgr
    if isinstance(pa_typ.type, pa.StructType):
        cyu__izpbh = []
        yjed__twcar = []
        jtymm__cqgr = True
        for erden__fzes in pa_typ.flatten():
            yjed__twcar.append(erden__fzes.name.split('.')[-1])
            upetw__knbob, ypqf__hguv = _get_numba_typ_from_pa_typ(erden__fzes,
                is_index, nullable_from_metadata, category_info)
            cyu__izpbh.append(upetw__knbob)
            jtymm__cqgr = jtymm__cqgr and ypqf__hguv
        return StructArrayType(tuple(cyu__izpbh), tuple(yjed__twcar)
            ), jtymm__cqgr
    if isinstance(pa_typ.type, pa.Decimal128Type):
        return DecimalArrayType(pa_typ.type.precision, pa_typ.type.scale), True
    if str_as_dict:
        if pa_typ.type != pa.string():
            raise BodoError(
                f'Read as dictionary used for non-string column {pa_typ}')
        return dict_str_arr_type, True
    if isinstance(pa_typ.type, pa.DictionaryType):
        if pa_typ.type.value_type != pa.string():
            raise BodoError(
                f'Parquet Categorical data type should be string, not {pa_typ.type.value_type}'
                )
        sdu__jqc = _pa_numba_typ_map[pa_typ.type.index_type]
        zkq__gjcxe = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=sdu__jqc)
        return CategoricalArrayType(zkq__gjcxe), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pa_numba_typ_map:
        iql__mubx = _pa_numba_typ_map[pa_typ.type]
        jtymm__cqgr = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if iql__mubx == datetime_date_type:
        return datetime_date_array_type, jtymm__cqgr
    if iql__mubx == bytes_type:
        return binary_array_type, jtymm__cqgr
    pkg__dnu = string_array_type if iql__mubx == string_type else types.Array(
        iql__mubx, 1, 'C')
    if iql__mubx == types.bool_:
        pkg__dnu = boolean_array
    if nullable_from_metadata is not None:
        wmrl__ripvn = nullable_from_metadata
    else:
        wmrl__ripvn = use_nullable_int_arr
    if wmrl__ripvn and not is_index and isinstance(iql__mubx, types.Integer
        ) and pa_typ.nullable:
        pkg__dnu = IntegerArrayType(iql__mubx)
    return pkg__dnu, jtymm__cqgr


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None):
    if get_row_counts:
        vhmb__luyla = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    pnniv__vhcpd = MPI.COMM_WORLD
    if isinstance(fpath, list):
        nnjm__vjjd = urlparse(fpath[0])
        protocol = nnjm__vjjd.scheme
        tyqqr__dxdog = nnjm__vjjd.netloc
        for tcau__aaw in range(len(fpath)):
            oaltv__qut = fpath[tcau__aaw]
            vkisw__wvum = urlparse(oaltv__qut)
            if vkisw__wvum.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if vkisw__wvum.netloc != tyqqr__dxdog:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[tcau__aaw] = oaltv__qut.rstrip('/')
    else:
        nnjm__vjjd = urlparse(fpath)
        protocol = nnjm__vjjd.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as lmpes__win:
            izyp__ywi = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(izyp__ywi)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as lmpes__win:
            izyp__ywi = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
"""
    fs = []

    def getfs(parallel=False):
        if len(fs) == 1:
            return fs[0]
        if protocol == 's3':
            fs.append(get_s3_fs_from_path(fpath, parallel=parallel,
                storage_options=storage_options) if not isinstance(fpath,
                list) else get_s3_fs_from_path(fpath[0], parallel=parallel,
                storage_options=storage_options))
        elif protocol in {'gcs', 'gs'}:
            dzlyd__lkwd = gcsfs.GCSFileSystem(token=None)
            fs.append(dzlyd__lkwd)
        elif protocol == 'http':
            fs.append(fsspec.filesystem('http'))
        elif protocol in {'hdfs', 'abfs', 'abfss'}:
            fs.append(get_hdfs_fs(fpath) if not isinstance(fpath, list) else
                get_hdfs_fs(fpath[0]))
        else:
            fs.append(None)
        return fs[0]

    def get_legacy_fs():
        if protocol in {'s3', 'hdfs', 'abfs', 'abfss'}:
            from fsspec.implementations.arrow import ArrowFSWrapper
            return ArrowFSWrapper(getfs())
        else:
            return getfs()

    def glob(protocol, fs, path):
        if not protocol and fs is None:
            from fsspec.implementations.local import LocalFileSystem
            fs = LocalFileSystem()
        if isinstance(fs, pyarrow.fs.FileSystem):
            from fsspec.implementations.arrow import ArrowFSWrapper
            fs = ArrowFSWrapper(fs)
        try:
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{nnjm__vjjd.netloc}'
                path = path[len(prefix):]
            oivpz__ihkp = fs.glob(path)
            if protocol == 's3':
                oivpz__ihkp = [('s3://' + oaltv__qut) for oaltv__qut in
                    oivpz__ihkp if not oaltv__qut.startswith('s3://')]
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                oivpz__ihkp = [(prefix + oaltv__qut) for oaltv__qut in
                    oivpz__ihkp]
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(oivpz__ihkp) == 0:
            raise BodoError('No files found matching glob pattern')
        return oivpz__ihkp
    nlv__kokiy = False
    if get_row_counts:
        hsfci__bpw = getfs(parallel=True)
        nlv__kokiy = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        yowrh__iogj = 1
        npna__qgjm = os.cpu_count()
        if npna__qgjm is not None and npna__qgjm > 1:
            yowrh__iogj = npna__qgjm // 2
        try:
            if get_row_counts:
                inth__qbhm = tracing.Event('pq.ParquetDataset', is_parallel
                    =False)
                if tracing.is_tracing():
                    inth__qbhm.add_attribute('g_dnf_filter', str(dnf_filters))
            tkqj__fsbmm = pa.io_thread_count()
            pa.set_io_thread_count(yowrh__iogj)
            if isinstance(fpath, list):
                bwzr__nin = []
                for rxm__rmq in fpath:
                    if has_magic(rxm__rmq):
                        bwzr__nin += glob(protocol, getfs(), rxm__rmq)
                    else:
                        bwzr__nin.append(rxm__rmq)
                fpath = bwzr__nin
            elif has_magic(fpath):
                fpath = glob(protocol, getfs(), fpath)
            if protocol == 's3':
                if isinstance(fpath, list):
                    get_legacy_fs().info(fpath[0])
                else:
                    get_legacy_fs().info(fpath)
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{nnjm__vjjd.netloc}'
                if isinstance(fpath, list):
                    muxg__ipq = [oaltv__qut[len(prefix):] for oaltv__qut in
                        fpath]
                else:
                    muxg__ipq = fpath[len(prefix):]
            else:
                muxg__ipq = fpath
            zvmar__bxzlj = pq.ParquetDataset(muxg__ipq, filesystem=
                get_legacy_fs(), filters=None, use_legacy_dataset=True,
                validate_schema=False, metadata_nthreads=yowrh__iogj)
            pa.set_io_thread_count(tkqj__fsbmm)
            ufs__ychl = bodo.io.pa_parquet.get_dataset_schema(zvmar__bxzlj)
            if dnf_filters:
                if get_row_counts:
                    inth__qbhm.add_attribute('num_pieces_before_filter',
                        len(zvmar__bxzlj.pieces))
                ljf__tzot = time.time()
                zvmar__bxzlj._filter(dnf_filters)
                if get_row_counts:
                    inth__qbhm.add_attribute('dnf_filter_time', time.time() -
                        ljf__tzot)
                    inth__qbhm.add_attribute('num_pieces_after_filter', len
                        (zvmar__bxzlj.pieces))
            if get_row_counts:
                inth__qbhm.finalize()
            zvmar__bxzlj._metadata.fs = None
        except Exception as oqcs__tvx:
            if isinstance(fpath, list) and isinstance(oqcs__tvx, (OSError,
                FileNotFoundError)):
                oqcs__tvx = BodoError(str(oqcs__tvx) + list_of_files_error_msg)
            else:
                oqcs__tvx = BodoError(
                    f"""error from pyarrow: {type(oqcs__tvx).__name__}: {str(oqcs__tvx)}
"""
                    )
            pnniv__vhcpd.bcast(oqcs__tvx)
            raise oqcs__tvx
        if get_row_counts:
            fjrd__ugppc = tracing.Event('bcast dataset')
        pnniv__vhcpd.bcast(zvmar__bxzlj)
        pnniv__vhcpd.bcast(ufs__ychl)
    else:
        if get_row_counts:
            fjrd__ugppc = tracing.Event('bcast dataset')
        zvmar__bxzlj = pnniv__vhcpd.bcast(None)
        if isinstance(zvmar__bxzlj, Exception):
            smmp__uqj = zvmar__bxzlj
            raise smmp__uqj
        ufs__ychl = pnniv__vhcpd.bcast(None)
    if get_row_counts:
        oxxn__xsca = getfs()
    else:
        oxxn__xsca = get_legacy_fs()
    zvmar__bxzlj._metadata.fs = oxxn__xsca
    if get_row_counts:
        fjrd__ugppc.finalize()
    zvmar__bxzlj._bodo_total_rows = 0
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = nlv__kokiy = False
        for rxm__rmq in zvmar__bxzlj.pieces:
            rxm__rmq._bodo_num_rows = 0
    if get_row_counts or nlv__kokiy:
        if get_row_counts and tracing.is_tracing():
            hasek__iwgfc = tracing.Event('get_row_counts')
            hasek__iwgfc.add_attribute('g_num_pieces', len(zvmar__bxzlj.pieces)
                )
            hasek__iwgfc.add_attribute('g_expr_filters', str(expr_filters))
        cpooe__sds = 0.0
        num_pieces = len(zvmar__bxzlj.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        omy__qeko = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        fkc__kcgi = 0
        kae__tciv = 0
        mxkwy__jhqc = 0
        nztl__kyxbo = True
        if expr_filters is not None:
            import random
            random.seed(37)
            hlgc__mopus = random.sample(zvmar__bxzlj.pieces, k=len(
                zvmar__bxzlj.pieces))
        else:
            hlgc__mopus = zvmar__bxzlj.pieces
        for rxm__rmq in hlgc__mopus:
            rxm__rmq._bodo_num_rows = 0
        fpaths = [rxm__rmq.path for rxm__rmq in hlgc__mopus[start:omy__qeko]]
        if protocol == 's3':
            tyqqr__dxdog = nnjm__vjjd.netloc
            prefix = 's3://' + tyqqr__dxdog + '/'
            fpaths = [oaltv__qut[len(prefix):] for oaltv__qut in fpaths]
            oxxn__xsca = get_s3_subtree_fs(tyqqr__dxdog, region=getfs().
                region, storage_options=storage_options)
        else:
            oxxn__xsca = getfs()
        yowrh__iogj = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(yowrh__iogj)
        pa.set_cpu_count(yowrh__iogj)
        smmp__uqj = None
        try:
            ntcoj__bivv = ds.dataset(fpaths, filesystem=oxxn__xsca,
                partitioning=ds.partitioning(flavor='hive'))
            for nhtk__cqfd, wmuz__jdpll in zip(hlgc__mopus[start:omy__qeko],
                ntcoj__bivv.get_fragments()):
                ljf__tzot = time.time()
                qnlg__idk = wmuz__jdpll.scanner(schema=ntcoj__bivv.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                cpooe__sds += time.time() - ljf__tzot
                nhtk__cqfd._bodo_num_rows = qnlg__idk
                fkc__kcgi += qnlg__idk
                kae__tciv += wmuz__jdpll.num_row_groups
                mxkwy__jhqc += sum(okync__rwya.total_byte_size for
                    okync__rwya in wmuz__jdpll.row_groups)
                if nlv__kokiy:
                    ovrsf__mbbce = wmuz__jdpll.metadata.schema.to_arrow_schema(
                        )
                    if ufs__ychl != ovrsf__mbbce:
                        print(
                            'Schema in {!s} was different. \n{!s}\n\nvs\n\n{!s}'
                            .format(nhtk__cqfd, ovrsf__mbbce, ufs__ychl))
                        nztl__kyxbo = False
                        break
        except Exception as oqcs__tvx:
            smmp__uqj = oqcs__tvx
        if pnniv__vhcpd.allreduce(smmp__uqj is not None, op=MPI.LOR):
            for smmp__uqj in pnniv__vhcpd.allgather(smmp__uqj):
                if smmp__uqj:
                    if isinstance(fpath, list) and isinstance(smmp__uqj, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(smmp__uqj) +
                            list_of_files_error_msg)
                    raise smmp__uqj
        if nlv__kokiy:
            nztl__kyxbo = pnniv__vhcpd.allreduce(nztl__kyxbo, op=MPI.LAND)
            if not nztl__kyxbo:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            zvmar__bxzlj._bodo_total_rows = pnniv__vhcpd.allreduce(fkc__kcgi,
                op=MPI.SUM)
            isalp__uow = pnniv__vhcpd.allreduce(kae__tciv, op=MPI.SUM)
            neena__twf = pnniv__vhcpd.allreduce(mxkwy__jhqc, op=MPI.SUM)
            rqk__yxu = np.array([rxm__rmq._bodo_num_rows for rxm__rmq in
                zvmar__bxzlj.pieces])
            rqk__yxu = pnniv__vhcpd.allreduce(rqk__yxu, op=MPI.SUM)
            for rxm__rmq, meg__ppo in zip(zvmar__bxzlj.pieces, rqk__yxu):
                rxm__rmq._bodo_num_rows = meg__ppo
            if is_parallel and bodo.get_rank(
                ) == 0 and isalp__uow < bodo.get_size() and isalp__uow != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({isalp__uow}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if isalp__uow == 0:
                gnl__mwxom = 0
            else:
                gnl__mwxom = neena__twf // isalp__uow
            if (bodo.get_rank() == 0 and neena__twf >= 20 * 1048576 and 
                gnl__mwxom < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({gnl__mwxom} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                hasek__iwgfc.add_attribute('g_total_num_row_groups', isalp__uow
                    )
                hasek__iwgfc.add_attribute('total_scan_time', cpooe__sds)
                tkutr__dxf = np.array([rxm__rmq._bodo_num_rows for rxm__rmq in
                    zvmar__bxzlj.pieces])
                lwls__ocfsi = np.percentile(tkutr__dxf, [25, 50, 75])
                hasek__iwgfc.add_attribute('g_row_counts_min', tkutr__dxf.min()
                    )
                hasek__iwgfc.add_attribute('g_row_counts_Q1', lwls__ocfsi[0])
                hasek__iwgfc.add_attribute('g_row_counts_median',
                    lwls__ocfsi[1])
                hasek__iwgfc.add_attribute('g_row_counts_Q3', lwls__ocfsi[2])
                hasek__iwgfc.add_attribute('g_row_counts_max', tkutr__dxf.max()
                    )
                hasek__iwgfc.add_attribute('g_row_counts_mean', tkutr__dxf.
                    mean())
                hasek__iwgfc.add_attribute('g_row_counts_std', tkutr__dxf.std()
                    )
                hasek__iwgfc.add_attribute('g_row_counts_sum', tkutr__dxf.sum()
                    )
                hasek__iwgfc.finalize()
    zvmar__bxzlj._prefix = ''
    if protocol in {'hdfs', 'abfs', 'abfss'}:
        prefix = f'{protocol}://{nnjm__vjjd.netloc}'
        if len(zvmar__bxzlj.pieces) > 0:
            nhtk__cqfd = zvmar__bxzlj.pieces[0]
            if not nhtk__cqfd.path.startswith(prefix):
                zvmar__bxzlj._prefix = prefix
    if read_categories:
        _add_categories_to_pq_dataset(zvmar__bxzlj)
    if get_row_counts:
        vhmb__luyla.finalize()
    return zvmar__bxzlj


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region, prefix,
    str_as_dict_cols, start_offset, rows_to_read):
    import pyarrow as pa
    npna__qgjm = os.cpu_count()
    if npna__qgjm is None or npna__qgjm == 0:
        npna__qgjm = 2
    eyu__ralvv = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), npna__qgjm)
    mtjk__mikg = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), npna__qgjm
        )
    if is_parallel and len(fpaths) > mtjk__mikg and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(mtjk__mikg)
        pa.set_cpu_count(mtjk__mikg)
    else:
        pa.set_io_thread_count(eyu__ralvv)
        pa.set_cpu_count(eyu__ralvv)
    if fpaths[0].startswith('s3://'):
        tyqqr__dxdog = urlparse(fpaths[0]).netloc
        prefix = 's3://' + tyqqr__dxdog + '/'
        fpaths = [oaltv__qut[len(prefix):] for oaltv__qut in fpaths]
        oxxn__xsca = get_s3_subtree_fs(tyqqr__dxdog, region=region,
            storage_options=storage_options)
    elif prefix and prefix.startswith(('hdfs', 'abfs', 'abfss')):
        oxxn__xsca = get_hdfs_fs(prefix + fpaths[0])
    elif fpaths[0].startswith(('gcs', 'gs')):
        import gcsfs
        oxxn__xsca = gcsfs.GCSFileSystem(token=None)
    else:
        oxxn__xsca = None
    dsikw__eoag = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    zvmar__bxzlj = ds.dataset(fpaths, filesystem=oxxn__xsca, partitioning=
        ds.partitioning(flavor='hive'), format=dsikw__eoag)
    col_names = zvmar__bxzlj.schema.names
    bidj__hpl = [col_names[axt__juw] for axt__juw in selected_fields]
    yije__eaex = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if yije__eaex and expr_filters is None:
        umv__rej = []
        scwgh__sgib = 0
        nvqud__dsdz = 0
        for wmuz__jdpll in zvmar__bxzlj.get_fragments():
            gmgx__wyykw = []
            for okync__rwya in wmuz__jdpll.row_groups:
                xcjt__nwdp = okync__rwya.num_rows
                if start_offset < scwgh__sgib + xcjt__nwdp:
                    if nvqud__dsdz == 0:
                        hccjf__qyxn = start_offset - scwgh__sgib
                        jefuz__har = min(xcjt__nwdp - hccjf__qyxn, rows_to_read
                            )
                    else:
                        jefuz__har = min(xcjt__nwdp, rows_to_read - nvqud__dsdz
                            )
                    nvqud__dsdz += jefuz__har
                    gmgx__wyykw.append(okync__rwya.id)
                scwgh__sgib += xcjt__nwdp
                if nvqud__dsdz == rows_to_read:
                    break
            umv__rej.append(wmuz__jdpll.subset(row_group_ids=gmgx__wyykw))
            if nvqud__dsdz == rows_to_read:
                break
        zvmar__bxzlj = ds.FileSystemDataset(umv__rej, zvmar__bxzlj.schema,
            dsikw__eoag, filesystem=zvmar__bxzlj.filesystem)
        start_offset = hccjf__qyxn
    kipqx__mjw = zvmar__bxzlj.scanner(columns=bidj__hpl, filter=
        expr_filters, use_threads=True).to_reader()
    return zvmar__bxzlj, kipqx__mjw, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema.to_arrow_schema()
    jyvt__zuq = [c for c in pa_schema.names if isinstance(pa_schema.field(c
        ).type, pa.DictionaryType)]
    if len(jyvt__zuq) == 0:
        pq_dataset._category_info = {}
        return
    pnniv__vhcpd = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            uvscc__fmgp = pq_dataset.pieces[0].open()
            okync__rwya = uvscc__fmgp.read_row_group(0, jyvt__zuq)
            category_info = {c: tuple(okync__rwya.column(c).chunk(0).
                dictionary.to_pylist()) for c in jyvt__zuq}
            del uvscc__fmgp, okync__rwya
        except Exception as oqcs__tvx:
            pnniv__vhcpd.bcast(oqcs__tvx)
            raise oqcs__tvx
        pnniv__vhcpd.bcast(category_info)
    else:
        category_info = pnniv__vhcpd.bcast(None)
        if isinstance(category_info, Exception):
            smmp__uqj = category_info
            raise smmp__uqj
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    gnker__ampcz = None
    nullable_from_metadata = defaultdict(lambda : None)
    xbwh__fzm = b'pandas'
    if schema.metadata is not None and xbwh__fzm in schema.metadata:
        import json
        rifup__eqef = json.loads(schema.metadata[xbwh__fzm].decode('utf8'))
        igx__lnys = len(rifup__eqef['index_columns'])
        if igx__lnys > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        gnker__ampcz = rifup__eqef['index_columns'][0] if igx__lnys else None
        if not isinstance(gnker__ampcz, str) and (not isinstance(
            gnker__ampcz, dict) or num_pieces != 1):
            gnker__ampcz = None
        for vnhb__khgk in rifup__eqef['columns']:
            tazw__qmqjx = vnhb__khgk['name']
            if vnhb__khgk['pandas_type'].startswith('int'
                ) and tazw__qmqjx is not None:
                if vnhb__khgk['numpy_type'].startswith('Int'):
                    nullable_from_metadata[tazw__qmqjx] = True
                else:
                    nullable_from_metadata[tazw__qmqjx] = False
    return gnker__ampcz, nullable_from_metadata


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for tazw__qmqjx in pa_schema.names:
        erden__fzes = pa_schema.field(tazw__qmqjx)
        if erden__fzes.type == pa.string():
            str_columns.append(tazw__qmqjx)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    pnniv__vhcpd = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        hlgc__mopus = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        hlgc__mopus = pq_dataset.pieces
    awzyc__snmre = np.zeros(len(str_columns), dtype=np.int64)
    uoew__guwo = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(hlgc__mopus):
        nhtk__cqfd = hlgc__mopus[bodo.get_rank()]
        try:
            wmpwn__tgo = nhtk__cqfd.get_metadata()
            for tcau__aaw in range(wmpwn__tgo.num_row_groups):
                for ijrcs__eigq, tazw__qmqjx in enumerate(str_columns):
                    itfgf__pngc = pa_schema.get_field_index(tazw__qmqjx)
                    awzyc__snmre[ijrcs__eigq] += wmpwn__tgo.row_group(tcau__aaw
                        ).column(itfgf__pngc).total_uncompressed_size
            xyg__zhf = wmpwn__tgo.num_rows
        except Exception as oqcs__tvx:
            if isinstance(oqcs__tvx, (OSError, FileNotFoundError)):
                xyg__zhf = 0
            else:
                raise
    else:
        xyg__zhf = 0
    zaw__wxj = pnniv__vhcpd.allreduce(xyg__zhf, op=MPI.SUM)
    if zaw__wxj == 0:
        return set()
    pnniv__vhcpd.Allreduce(awzyc__snmre, uoew__guwo, op=MPI.SUM)
    eeo__qfq = uoew__guwo / zaw__wxj
    str_as_dict = set()
    for tcau__aaw, iac__onmq in enumerate(eeo__qfq):
        if iac__onmq < READ_STR_AS_DICT_THRESHOLD:
            tazw__qmqjx = str_columns[tcau__aaw][0]
            str_as_dict.add(tazw__qmqjx)
    return str_as_dict


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    lgjh__hdore = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[tcau__aaw].name for tcau__aaw in range(len(
        pq_dataset.partitions.partition_names))]
    pa_schema = pq_dataset.schema.to_arrow_schema()
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    ojr__psj = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    zmul__ldttb = read_as_dict_cols - ojr__psj
    if len(zmul__ldttb) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {zmul__ldttb}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(ojr__psj)
    ojr__psj = ojr__psj - read_as_dict_cols
    str_columns = [immdp__babdo for immdp__babdo in str_columns if 
        immdp__babdo in ojr__psj]
    str_as_dict: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    str_as_dict.update(read_as_dict_cols)
    col_names = pa_schema.names
    gnker__ampcz, nullable_from_metadata = get_pandas_metadata(pa_schema,
        num_pieces)
    dxs__afe = []
    occre__aqxm = []
    juh__dqd = []
    for tcau__aaw, c in enumerate(col_names):
        erden__fzes = pa_schema.field(c)
        iql__mubx, jtymm__cqgr = _get_numba_typ_from_pa_typ(erden__fzes, c ==
            gnker__ampcz, nullable_from_metadata[c], pq_dataset.
            _category_info, str_as_dict=c in str_as_dict)
        dxs__afe.append(iql__mubx)
        occre__aqxm.append(jtymm__cqgr)
        juh__dqd.append(erden__fzes.type)
    if partition_names:
        col_names += partition_names
        dxs__afe += [_get_partition_cat_dtype(pq_dataset.partitions.levels[
            tcau__aaw]) for tcau__aaw in range(len(partition_names))]
        occre__aqxm.extend([True] * len(partition_names))
        juh__dqd.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        dxs__afe += [dict_str_arr_type]
        occre__aqxm.append(True)
        juh__dqd.append(None)
    zbur__lfl = {c: tcau__aaw for tcau__aaw, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in zbur__lfl:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if gnker__ampcz and not isinstance(gnker__ampcz, dict
        ) and gnker__ampcz not in selected_columns:
        selected_columns.append(gnker__ampcz)
    col_names = selected_columns
    col_indices = []
    lgjh__hdore = []
    zlv__ekdd = []
    pchb__mgpb = []
    for tcau__aaw, c in enumerate(col_names):
        ywh__tcjfr = zbur__lfl[c]
        col_indices.append(ywh__tcjfr)
        lgjh__hdore.append(dxs__afe[ywh__tcjfr])
        if not occre__aqxm[ywh__tcjfr]:
            zlv__ekdd.append(tcau__aaw)
            pchb__mgpb.append(juh__dqd[ywh__tcjfr])
    return (col_names, lgjh__hdore, gnker__ampcz, col_indices,
        partition_names, zlv__ekdd, pchb__mgpb)


def _get_partition_cat_dtype(part_set):
    gzpw__gdtra = part_set.dictionary.to_pandas()
    xbjv__leqx = bodo.typeof(gzpw__gdtra).dtype
    zkq__gjcxe = PDCategoricalDtype(tuple(gzpw__gdtra), xbjv__leqx, False)
    return CategoricalArrayType(zkq__gjcxe)


_pq_read = types.ExternalFunction('pq_read', table_type(
    read_parquet_fpath_type, types.boolean, types.voidptr,
    parquet_predicate_type, parquet_predicate_type,
    storage_options_dict_type, types.int64, types.voidptr, types.int32,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.voidptr,
    types.int32, types.voidptr, types.boolean))
from llvmlite import ir as lir
from numba.core import cgutils
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_read', arrow_cpp.pq_read)
    ll.add_symbol('pq_write', arrow_cpp.pq_write)
    ll.add_symbol('pq_write_partitioned', arrow_cpp.pq_write_partitioned)


@intrinsic
def parquet_write_table_cpp(typingctx, filename_t, table_t, col_names_t,
    index_t, write_index, metadata_t, compression_t, is_parallel_t,
    write_range_index, start, stop, step, name, bucket_region, row_group_size):

    def codegen(context, builder, sig, args):
        zeuc__pzy = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        xojs__upaa = cgutils.get_or_insert_function(builder.module,
            zeuc__pzy, name='pq_write')
        builder.call(xojs__upaa, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, table_t, col_names_t, index_t, types.
        boolean, types.voidptr, types.voidptr, types.boolean, types.boolean,
        types.int32, types.int32, types.int32, types.voidptr, types.voidptr,
        types.int64), codegen


@intrinsic
def parquet_write_table_partitioned_cpp(typingctx, filename_t, data_table_t,
    col_names_t, col_names_no_partitions_t, cat_table_t, part_col_idxs_t,
    num_part_col_t, compression_t, is_parallel_t, bucket_region, row_group_size
    ):

    def codegen(context, builder, sig, args):
        zeuc__pzy = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        xojs__upaa = cgutils.get_or_insert_function(builder.module,
            zeuc__pzy, name='pq_write_partitioned')
        builder.call(xojs__upaa, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64), codegen
