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
        except OSError as lkaqb__kxcyu:
            if 'non-file path' in str(lkaqb__kxcyu):
                raise FileNotFoundError(str(lkaqb__kxcyu))
            raise


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None):
        xvk__mjbb = lhs.scope
        rmex__ovb = lhs.loc
        navu__wzoh = None
        if lhs.name in self.locals:
            navu__wzoh = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        sxz__vgj = {}
        if lhs.name + ':convert' in self.locals:
            sxz__vgj = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if navu__wzoh is None:
            pqbwd__uplyy = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/source/programming_with_bodo/file_io.html#io_workflow'
                )
            btdr__xpkbo = get_const_value(file_name, self.func_ir,
                pqbwd__uplyy, arg_types=self.args, file_info=
                ParquetFileInfo(columns, storage_options=storage_options,
                input_file_name_col=input_file_name_col, read_as_dict_cols=
                read_as_dict_cols))
            nsvih__seh = False
            pysc__lvp = guard(get_definition, self.func_ir, file_name)
            if isinstance(pysc__lvp, ir.Arg):
                typ = self.args[pysc__lvp.index]
                if isinstance(typ, types.FilenameType):
                    (col_names, arphg__sci, yhy__vuwx, col_indices,
                        partition_names, llb__cptrp, ybqrb__tpihq) = typ.schema
                    nsvih__seh = True
            if not nsvih__seh:
                (col_names, arphg__sci, yhy__vuwx, col_indices,
                    partition_names, llb__cptrp, ybqrb__tpihq) = (
                    parquet_file_schema(btdr__xpkbo, columns,
                    storage_options=storage_options, input_file_name_col=
                    input_file_name_col, read_as_dict_cols=read_as_dict_cols))
        else:
            paxz__scqby = list(navu__wzoh.keys())
            hxm__blyn = {c: oji__wrdv for oji__wrdv, c in enumerate(
                paxz__scqby)}
            ctwi__lqyp = [xvo__kzfcu for xvo__kzfcu in navu__wzoh.values()]
            yhy__vuwx = 'index' if 'index' in hxm__blyn else None
            if columns is None:
                selected_columns = paxz__scqby
            else:
                selected_columns = columns
            col_indices = [hxm__blyn[c] for c in selected_columns]
            arphg__sci = [ctwi__lqyp[hxm__blyn[c]] for c in selected_columns]
            col_names = selected_columns
            yhy__vuwx = yhy__vuwx if yhy__vuwx in col_names else None
            partition_names = []
            llb__cptrp = []
            ybqrb__tpihq = []
        hcgrk__pxz = None if isinstance(yhy__vuwx, dict
            ) or yhy__vuwx is None else yhy__vuwx
        index_column_index = None
        index_column_type = types.none
        if hcgrk__pxz:
            xdo__ulmfx = col_names.index(hcgrk__pxz)
            index_column_index = col_indices.pop(xdo__ulmfx)
            index_column_type = arphg__sci.pop(xdo__ulmfx)
            col_names.pop(xdo__ulmfx)
        for oji__wrdv, c in enumerate(col_names):
            if c in sxz__vgj:
                arphg__sci[oji__wrdv] = sxz__vgj[c]
        lqcju__zgr = [ir.Var(xvk__mjbb, mk_unique_var('pq_table'),
            rmex__ovb), ir.Var(xvk__mjbb, mk_unique_var('pq_index'), rmex__ovb)
            ]
        jyu__tmy = [bodo.ir.parquet_ext.ParquetReader(file_name, lhs.name,
            col_names, col_indices, arphg__sci, lqcju__zgr, rmex__ovb,
            partition_names, storage_options, index_column_index,
            index_column_type, input_file_name_col, llb__cptrp, ybqrb__tpihq)]
        return (col_names, lqcju__zgr, yhy__vuwx, jyu__tmy, arphg__sci,
            index_column_type)


def determine_filter_cast(pq_node, typemap, filter_val, orig_colname_map):
    czwz__tyr = filter_val[0]
    ipy__hcan = pq_node.original_out_types[orig_colname_map[czwz__tyr]]
    qqvh__vik = bodo.utils.typing.element_type(ipy__hcan)
    if czwz__tyr in pq_node.partition_names:
        if qqvh__vik == types.unicode_type:
            qvu__jwmtl = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(qqvh__vik, types.Integer):
            qvu__jwmtl = f'.cast(pyarrow.{qqvh__vik.name}(), safe=False)'
        else:
            qvu__jwmtl = ''
    else:
        qvu__jwmtl = ''
    fnui__kwe = typemap[filter_val[2].name]
    if isinstance(fnui__kwe, (types.List, types.Set)):
        sogss__kdt = fnui__kwe.dtype
    else:
        sogss__kdt = fnui__kwe
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(qqvh__vik,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(sogss__kdt,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([qqvh__vik, sogss__kdt]):
        if not bodo.utils.typing.is_safe_arrow_cast(qqvh__vik, sogss__kdt):
            raise BodoError(
                f'Unsupported Arrow cast from {qqvh__vik} to {sogss__kdt} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if qqvh__vik == types.unicode_type:
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif qqvh__vik in (bodo.datetime64ns, bodo.pd_timestamp_type):
            if isinstance(fnui__kwe, (types.List, types.Set)):
                ndhpi__pocbo = 'list' if isinstance(fnui__kwe, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {ndhpi__pocbo} values with isin filter pushdown.'
                    )
            return qvu__jwmtl, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return qvu__jwmtl, ''


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, meta_head_only_info=None):
    ken__aesr = len(pq_node.out_vars)
    extra_args = ''
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    tye__beorg, dma__yes = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    if pq_node.filters:
        ukt__azxlk = []
        rjia__ilpmt = []
        gkqj__wwdnd = False
        jcmu__usbgz = None
        orig_colname_map = {c: oji__wrdv for oji__wrdv, c in enumerate(
            pq_node.original_df_colnames)}
        for zsdwa__ykglc in pq_node.filters:
            jtkdo__islj = []
            ayo__ywihi = []
            bthv__lnbk = set()
            for siknx__jmza in zsdwa__ykglc:
                if isinstance(siknx__jmza[2], ir.Var):
                    rov__zmcpq, cmhvy__eawxl = determine_filter_cast(pq_node,
                        typemap, siknx__jmza, orig_colname_map)
                    if siknx__jmza[1] == 'in':
                        ayo__ywihi.append(
                            f"(ds.field('{siknx__jmza[0]}').isin({tye__beorg[siknx__jmza[2].name]}))"
                            )
                    else:
                        ayo__ywihi.append(
                            f"(ds.field('{siknx__jmza[0]}'){rov__zmcpq} {siknx__jmza[1]} ds.scalar({tye__beorg[siknx__jmza[2].name]}){cmhvy__eawxl})"
                            )
                else:
                    assert siknx__jmza[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if siknx__jmza[1] == 'is not':
                        prefix = '~'
                    else:
                        prefix = ''
                    ayo__ywihi.append(
                        f"({prefix}ds.field('{siknx__jmza[0]}').is_null())")
                if siknx__jmza[0] in pq_node.partition_names and isinstance(
                    siknx__jmza[2], ir.Var):
                    ifrmd__vmj = (
                        f"('{siknx__jmza[0]}', '{siknx__jmza[1]}', {tye__beorg[siknx__jmza[2].name]})"
                        )
                    jtkdo__islj.append(ifrmd__vmj)
                    bthv__lnbk.add(ifrmd__vmj)
                else:
                    gkqj__wwdnd = True
            if jcmu__usbgz is None:
                jcmu__usbgz = bthv__lnbk
            else:
                jcmu__usbgz.intersection_update(bthv__lnbk)
            flti__azi = ', '.join(jtkdo__islj)
            uora__tuqd = ' & '.join(ayo__ywihi)
            if flti__azi:
                ukt__azxlk.append(f'[{flti__azi}]')
            rjia__ilpmt.append(f'({uora__tuqd})')
        wupq__ddn = ', '.join(ukt__azxlk)
        gmk__kla = ' | '.join(rjia__ilpmt)
        if gkqj__wwdnd:
            if jcmu__usbgz:
                aspx__blvl = sorted(jcmu__usbgz)
                dnf_filter_str = f"[[{', '.join(aspx__blvl)}]]"
        elif wupq__ddn:
            dnf_filter_str = f'[{wupq__ddn}]'
        expr_filter_str = f'({gmk__kla})'
        extra_args = ', '.join(tye__beorg.values())
    nxea__lvtrw = ', '.join(f'out{oji__wrdv}' for oji__wrdv in range(ken__aesr)
        )
    dca__qlekr = f'def pq_impl(fname, {extra_args}):\n'
    dca__qlekr += (
        f'    (total_rows, {nxea__lvtrw},) = _pq_reader_py(fname, {extra_args})\n'
        )
    lsll__knnty = {}
    exec(dca__qlekr, {}, lsll__knnty)
    xupkj__ckut = lsll__knnty['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        kfqn__rzuwh = pq_node.loc.strformat()
        wrkj__rihl = []
        xdi__zbi = []
        for oji__wrdv in pq_node.type_usecol_offset:
            czwz__tyr = pq_node.df_colnames[oji__wrdv]
            wrkj__rihl.append(czwz__tyr)
            if isinstance(pq_node.out_types[oji__wrdv], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                xdi__zbi.append(czwz__tyr)
        zsni__oxbs = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', zsni__oxbs,
            kfqn__rzuwh, wrkj__rihl)
        if xdi__zbi:
            ypm__bkx = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', ypm__bkx,
                kfqn__rzuwh, xdi__zbi)
    parallel = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        shc__sbh = set(pq_node.type_usecol_offset)
        lok__tdw = set(pq_node.unsupported_columns)
        yvp__gsv = shc__sbh & lok__tdw
        if yvp__gsv:
            xedtz__xigbk = sorted(yvp__gsv)
            svt__ukav = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            cmwq__vjz = 0
            for tyi__beq in xedtz__xigbk:
                while pq_node.unsupported_columns[cmwq__vjz] != tyi__beq:
                    cmwq__vjz += 1
                svt__ukav.append(
                    f"Column '{pq_node.df_colnames[tyi__beq]}' with unsupported arrow type {pq_node.unsupported_arrow_types[cmwq__vjz]}"
                    )
                cmwq__vjz += 1
            qzhxs__wrm = '\n'.join(svt__ukav)
            raise BodoError(qzhxs__wrm, loc=pq_node.loc)
    kvwmf__nweyz = _gen_pq_reader_py(pq_node.df_colnames, pq_node.
        col_indices, pq_node.type_usecol_offset, pq_node.out_types, pq_node
        .storage_options, pq_node.partition_names, dnf_filter_str,
        expr_filter_str, extra_args, parallel, meta_head_only_info, pq_node
        .index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col)
    oil__oqzq = typemap[pq_node.file_name.name]
    zza__vqz = (oil__oqzq,) + tuple(typemap[siknx__jmza.name] for
        siknx__jmza in dma__yes)
    wna__ldf = compile_to_numba_ir(xupkj__ckut, {'_pq_reader_py':
        kvwmf__nweyz}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        zza__vqz, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(wna__ldf, [pq_node.file_name] + dma__yes)
    jyu__tmy = wna__ldf.body[:-3]
    if meta_head_only_info:
        jyu__tmy[-1 - ken__aesr].target = meta_head_only_info[1]
    jyu__tmy[-2].target = pq_node.out_vars[0]
    jyu__tmy[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        type_usecol_offset
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        jyu__tmy.pop(-1)
    elif not pq_node.type_usecol_offset:
        jyu__tmy.pop(-2)
    return jyu__tmy


distributed_pass.distributed_run_extensions[bodo.ir.parquet_ext.ParquetReader
    ] = pq_distributed_run


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    ubhhw__lfcpx = get_overload_const_str(dnf_filter_str)
    guy__bcrfw = get_overload_const_str(expr_filter_str)
    lofj__onwy = ', '.join(f'f{oji__wrdv}' for oji__wrdv in range(len(var_tup))
        )
    dca__qlekr = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        dca__qlekr += f'  {lofj__onwy}, = var_tup\n'
    dca__qlekr += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    dca__qlekr += f'    dnf_filters_py = {ubhhw__lfcpx}\n'
    dca__qlekr += f'    expr_filters_py = {guy__bcrfw}\n'
    dca__qlekr += '  return (dnf_filters_py, expr_filters_py)\n'
    lsll__knnty = {}
    exec(dca__qlekr, globals(), lsll__knnty)
    return lsll__knnty['impl']


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


def _gen_pq_reader_py(col_names, col_indices, type_usecol_offset, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col):
    kbojk__nrp = next_label()
    ulixa__fyfs = ',' if extra_args else ''
    dca__qlekr = f'def pq_reader_py(fname,{extra_args}):\n'
    dca__qlekr += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    dca__qlekr += f"    ev.add_attribute('g_fname', fname)\n"
    dca__qlekr += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={is_parallel})
"""
    dca__qlekr += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{ulixa__fyfs}))
"""
    dca__qlekr += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    dca__qlekr += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    tot_rows_to_read = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        tot_rows_to_read = meta_head_only_info[0]
    lrsk__pvq = not type_usecol_offset
    zkqef__reiid = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in type_usecol_offset else None
    ive__fkdx = {c: oji__wrdv for oji__wrdv, c in enumerate(col_indices)}
    sdsib__vmxp = {c: oji__wrdv for oji__wrdv, c in enumerate(zkqef__reiid)}
    dvv__ubt = []
    bct__sban = set()
    xdkr__ykdhi = partition_names + [input_file_name_col]
    for oji__wrdv in type_usecol_offset:
        if zkqef__reiid[oji__wrdv] not in xdkr__ykdhi:
            dvv__ubt.append(col_indices[oji__wrdv])
        elif not input_file_name_col or zkqef__reiid[oji__wrdv
            ] != input_file_name_col:
            bct__sban.add(col_indices[oji__wrdv])
    if index_column_index is not None:
        dvv__ubt.append(index_column_index)
    dvv__ubt = sorted(dvv__ubt)
    qvcon__pcsyl = {c: oji__wrdv for oji__wrdv, c in enumerate(dvv__ubt)}

    def is_nullable(typ):
        return bodo.utils.utils.is_array_typ(typ, False) and (not
            isinstance(typ, types.Array) and not isinstance(typ, bodo.
            DatetimeArrayType))
    fyid__tux = [(int(is_nullable(out_types[ive__fkdx[zwc__tuof]])) if 
        zwc__tuof != index_column_index else int(is_nullable(
        index_column_type))) for zwc__tuof in dvv__ubt]
    str_as_dict_cols = []
    for zwc__tuof in dvv__ubt:
        if zwc__tuof == index_column_index:
            xvo__kzfcu = index_column_type
        else:
            xvo__kzfcu = out_types[ive__fkdx[zwc__tuof]]
        if xvo__kzfcu == dict_str_arr_type:
            str_as_dict_cols.append(zwc__tuof)
    ebvu__nnzpp = []
    brkjc__zcp = {}
    drpg__qkak = []
    ffwmx__tfosb = []
    for oji__wrdv, lknp__rfy in enumerate(partition_names):
        try:
            etgu__xbpnl = sdsib__vmxp[lknp__rfy]
            if col_indices[etgu__xbpnl] not in bct__sban:
                continue
        except (KeyError, ValueError) as rbqur__qee:
            continue
        brkjc__zcp[lknp__rfy] = len(ebvu__nnzpp)
        ebvu__nnzpp.append(lknp__rfy)
        drpg__qkak.append(oji__wrdv)
        fnpwa__nnt = out_types[etgu__xbpnl].dtype
        lzjoh__ged = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            fnpwa__nnt)
        ffwmx__tfosb.append(numba_to_c_type(lzjoh__ged))
    dca__qlekr += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    dca__qlekr += f'    out_table = pq_read(\n'
    dca__qlekr += f'        fname_py, {is_parallel},\n'
    dca__qlekr += f'        unicode_to_utf8(bucket_region),\n'
    dca__qlekr += f'        dnf_filters, expr_filters,\n'
    dca__qlekr += f"""        storage_options_py, {tot_rows_to_read}, selected_cols_arr_{kbojk__nrp}.ctypes,
"""
    dca__qlekr += f'        {len(dvv__ubt)},\n'
    dca__qlekr += f'        nullable_cols_arr_{kbojk__nrp}.ctypes,\n'
    if len(drpg__qkak) > 0:
        dca__qlekr += (
            f'        np.array({drpg__qkak}, dtype=np.int32).ctypes,\n')
        dca__qlekr += (
            f'        np.array({ffwmx__tfosb}, dtype=np.int32).ctypes,\n')
        dca__qlekr += f'        {len(drpg__qkak)},\n'
    else:
        dca__qlekr += f'        0, 0, 0,\n'
    if len(str_as_dict_cols) > 0:
        dca__qlekr += f"""        np.array({str_as_dict_cols}, dtype=np.int32).ctypes, {len(str_as_dict_cols)},
"""
    else:
        dca__qlekr += f'        0, 0,\n'
    dca__qlekr += f'        total_rows_np.ctypes,\n'
    dca__qlekr += f'        {input_file_name_col is not None},\n'
    dca__qlekr += f'    )\n'
    dca__qlekr += f'    check_and_propagate_cpp_exception()\n'
    smrs__kmen = 'None'
    rjkq__znrb = index_column_type
    avpb__brjhs = TableType(tuple(out_types))
    if lrsk__pvq:
        avpb__brjhs = types.none
    if index_column_index is not None:
        qcwq__khjhv = qvcon__pcsyl[index_column_index]
        smrs__kmen = (
            f'info_to_array(info_from_table(out_table, {qcwq__khjhv}), index_arr_type)'
            )
    dca__qlekr += f'    index_arr = {smrs__kmen}\n'
    if lrsk__pvq:
        ugvdd__ycluy = None
    else:
        ugvdd__ycluy = []
        xlo__ctjnr = 0
        uxlrq__onw = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for oji__wrdv, tyi__beq in enumerate(col_indices):
            if xlo__ctjnr < len(type_usecol_offset
                ) and oji__wrdv == type_usecol_offset[xlo__ctjnr]:
                oany__oga = col_indices[oji__wrdv]
                if uxlrq__onw and oany__oga == uxlrq__onw:
                    ugvdd__ycluy.append(len(dvv__ubt) + len(ebvu__nnzpp))
                elif oany__oga in bct__sban:
                    nan__ceqrm = zkqef__reiid[oji__wrdv]
                    ugvdd__ycluy.append(len(dvv__ubt) + brkjc__zcp[nan__ceqrm])
                else:
                    ugvdd__ycluy.append(qvcon__pcsyl[tyi__beq])
                xlo__ctjnr += 1
            else:
                ugvdd__ycluy.append(-1)
        ugvdd__ycluy = np.array(ugvdd__ycluy, dtype=np.int64)
    if lrsk__pvq:
        dca__qlekr += '    T = None\n'
    else:
        dca__qlekr += f"""    T = cpp_table_to_py_table(out_table, table_idx_{kbojk__nrp}, py_table_type_{kbojk__nrp})
"""
    dca__qlekr += f'    delete_table(out_table)\n'
    dca__qlekr += f'    total_rows = total_rows_np[0]\n'
    dca__qlekr += f'    ev.finalize()\n'
    dca__qlekr += f'    return (total_rows, T, index_arr)\n'
    lsll__knnty = {}
    tsjr__tlok = {f'py_table_type_{kbojk__nrp}': avpb__brjhs,
        f'table_idx_{kbojk__nrp}': ugvdd__ycluy,
        f'selected_cols_arr_{kbojk__nrp}': np.array(dvv__ubt, np.int32),
        f'nullable_cols_arr_{kbojk__nrp}': np.array(fyid__tux, np.int32),
        'index_arr_type': rjkq__znrb, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo}
    exec(dca__qlekr, tsjr__tlok, lsll__knnty)
    kvwmf__nweyz = lsll__knnty['pq_reader_py']
    vuhbw__hvq = numba.njit(kvwmf__nweyz, no_cpython_wrapper=True)
    return vuhbw__hvq


import pyarrow as pa
_pa_numba_typ_map = {pa.bool_(): types.bool_, pa.int8(): types.int8, pa.
    int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.int64,
    pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32(): types.
    uint32, pa.uint64(): types.uint64, pa.float32(): types.float32, pa.
    float64(): types.float64, pa.string(): string_type, pa.binary():
    bytes_type, pa.date32(): datetime_date_type, pa.date64(): types.
    NPDatetime('ns'), null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    ctpo__byh = 'ns', 'us', 'ms', 's'
    if pa_ts_typ.unit not in ctpo__byh:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        plj__dfclu = pa_ts_typ.to_pandas_dtype().tz
        anyhy__ivx = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            plj__dfclu)
        return bodo.DatetimeArrayType(anyhy__ivx), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ, is_index, nullable_from_metadata,
    category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        uuzft__fpfp, isc__tau = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(uuzft__fpfp), isc__tau
    if isinstance(pa_typ.type, pa.StructType):
        qlg__cse = []
        xpw__shnvm = []
        isc__tau = True
        for vgph__iikhc in pa_typ.flatten():
            xpw__shnvm.append(vgph__iikhc.name.split('.')[-1])
            bhstf__txvv, sdrra__wxcb = _get_numba_typ_from_pa_typ(vgph__iikhc,
                is_index, nullable_from_metadata, category_info)
            qlg__cse.append(bhstf__txvv)
            isc__tau = isc__tau and sdrra__wxcb
        return StructArrayType(tuple(qlg__cse), tuple(xpw__shnvm)), isc__tau
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
        qfomb__ifdff = _pa_numba_typ_map[pa_typ.type.index_type]
        biu__enhhx = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=qfomb__ifdff)
        return CategoricalArrayType(biu__enhhx), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pa_numba_typ_map:
        nwtdq__zrhwp = _pa_numba_typ_map[pa_typ.type]
        isc__tau = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if nwtdq__zrhwp == datetime_date_type:
        return datetime_date_array_type, isc__tau
    if nwtdq__zrhwp == bytes_type:
        return binary_array_type, isc__tau
    uuzft__fpfp = (string_array_type if nwtdq__zrhwp == string_type else
        types.Array(nwtdq__zrhwp, 1, 'C'))
    if nwtdq__zrhwp == types.bool_:
        uuzft__fpfp = boolean_array
    if nullable_from_metadata is not None:
        aab__rmpym = nullable_from_metadata
    else:
        aab__rmpym = use_nullable_int_arr
    if aab__rmpym and not is_index and isinstance(nwtdq__zrhwp, types.Integer
        ) and pa_typ.nullable:
        uuzft__fpfp = IntegerArrayType(nwtdq__zrhwp)
    return uuzft__fpfp, isc__tau


def get_parquet_dataset(fpath, get_row_counts=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories=False,
    is_parallel=False, tot_rows_to_read=None):
    if get_row_counts:
        ldvjv__jid = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    rmldk__xsq = MPI.COMM_WORLD
    if isinstance(fpath, list):
        qlhcw__ucleu = urlparse(fpath[0])
        protocol = qlhcw__ucleu.scheme
        afs__wek = qlhcw__ucleu.netloc
        for oji__wrdv in range(len(fpath)):
            anbad__qlt = fpath[oji__wrdv]
            jzk__hjpf = urlparse(anbad__qlt)
            if jzk__hjpf.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if jzk__hjpf.netloc != afs__wek:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[oji__wrdv] = anbad__qlt.rstrip('/')
    else:
        qlhcw__ucleu = urlparse(fpath)
        protocol = qlhcw__ucleu.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as rbqur__qee:
            aaq__wrlg = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(aaq__wrlg)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as rbqur__qee:
            aaq__wrlg = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            nreop__uqu = gcsfs.GCSFileSystem(token=None)
            fs.append(nreop__uqu)
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
                prefix = f'{protocol}://{qlhcw__ucleu.netloc}'
                path = path[len(prefix):]
            kmbg__kmg = fs.glob(path)
            if protocol == 's3':
                kmbg__kmg = [('s3://' + anbad__qlt) for anbad__qlt in
                    kmbg__kmg if not anbad__qlt.startswith('s3://')]
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                kmbg__kmg = [(prefix + anbad__qlt) for anbad__qlt in kmbg__kmg]
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(kmbg__kmg) == 0:
            raise BodoError('No files found matching glob pattern')
        return kmbg__kmg
    zgesg__chi = False
    if get_row_counts:
        vetk__euvv = getfs(parallel=True)
        zgesg__chi = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        wew__bkzbf = 1
        aqob__nyifk = os.cpu_count()
        if aqob__nyifk is not None and aqob__nyifk > 1:
            wew__bkzbf = aqob__nyifk // 2
        try:
            if get_row_counts:
                fzna__vgmdl = tracing.Event('pq.ParquetDataset',
                    is_parallel=False)
                if tracing.is_tracing():
                    fzna__vgmdl.add_attribute('g_dnf_filter', str(dnf_filters))
            lto__mfafm = pa.io_thread_count()
            pa.set_io_thread_count(wew__bkzbf)
            if isinstance(fpath, list):
                moud__keuz = []
                for hegx__unifb in fpath:
                    if has_magic(hegx__unifb):
                        moud__keuz += glob(protocol, getfs(), hegx__unifb)
                    else:
                        moud__keuz.append(hegx__unifb)
                fpath = moud__keuz
            elif has_magic(fpath):
                fpath = glob(protocol, getfs(), fpath)
            if protocol == 's3':
                if isinstance(fpath, list):
                    get_legacy_fs().info(fpath[0])
                else:
                    get_legacy_fs().info(fpath)
            if protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{qlhcw__ucleu.netloc}'
                if isinstance(fpath, list):
                    adm__ict = [anbad__qlt[len(prefix):] for anbad__qlt in
                        fpath]
                else:
                    adm__ict = fpath[len(prefix):]
            else:
                adm__ict = fpath
            ukusy__hvqj = pq.ParquetDataset(adm__ict, filesystem=
                get_legacy_fs(), filters=None, use_legacy_dataset=True,
                validate_schema=False, metadata_nthreads=wew__bkzbf)
            pa.set_io_thread_count(lto__mfafm)
            rtnwo__dxnqy = bodo.io.pa_parquet.get_dataset_schema(ukusy__hvqj)
            if dnf_filters:
                if get_row_counts:
                    fzna__vgmdl.add_attribute('num_pieces_before_filter',
                        len(ukusy__hvqj.pieces))
                phyp__ocwii = time.time()
                ukusy__hvqj._filter(dnf_filters)
                if get_row_counts:
                    fzna__vgmdl.add_attribute('dnf_filter_time', time.time(
                        ) - phyp__ocwii)
                    fzna__vgmdl.add_attribute('num_pieces_after_filter',
                        len(ukusy__hvqj.pieces))
            if get_row_counts:
                fzna__vgmdl.finalize()
            ukusy__hvqj._metadata.fs = None
        except Exception as lkaqb__kxcyu:
            if isinstance(fpath, list) and isinstance(lkaqb__kxcyu, (
                OSError, FileNotFoundError)):
                lkaqb__kxcyu = BodoError(str(lkaqb__kxcyu) +
                    list_of_files_error_msg)
            else:
                lkaqb__kxcyu = BodoError(
                    f"""error from pyarrow: {type(lkaqb__kxcyu).__name__}: {str(lkaqb__kxcyu)}
"""
                    )
            rmldk__xsq.bcast(lkaqb__kxcyu)
            raise lkaqb__kxcyu
        if get_row_counts:
            jjo__bnatl = tracing.Event('bcast dataset')
        rmldk__xsq.bcast(ukusy__hvqj)
        rmldk__xsq.bcast(rtnwo__dxnqy)
    else:
        if get_row_counts:
            jjo__bnatl = tracing.Event('bcast dataset')
        ukusy__hvqj = rmldk__xsq.bcast(None)
        if isinstance(ukusy__hvqj, Exception):
            sszi__fsg = ukusy__hvqj
            raise sszi__fsg
        rtnwo__dxnqy = rmldk__xsq.bcast(None)
    if get_row_counts:
        tkvi__qvdd = getfs()
    else:
        tkvi__qvdd = get_legacy_fs()
    ukusy__hvqj._metadata.fs = tkvi__qvdd
    if get_row_counts:
        jjo__bnatl.finalize()
    ukusy__hvqj._bodo_total_rows = 0
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = zgesg__chi = False
        for hegx__unifb in ukusy__hvqj.pieces:
            hegx__unifb._bodo_num_rows = 0
    if get_row_counts or zgesg__chi:
        if get_row_counts and tracing.is_tracing():
            mdjps__xqd = tracing.Event('get_row_counts')
            mdjps__xqd.add_attribute('g_num_pieces', len(ukusy__hvqj.pieces))
            mdjps__xqd.add_attribute('g_expr_filters', str(expr_filters))
        tmda__cekht = 0.0
        num_pieces = len(ukusy__hvqj.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        gjm__cgd = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        jjacg__txq = 0
        btq__fosi = 0
        ryvi__ghqp = 0
        qpo__imgxj = True
        if expr_filters is not None:
            import random
            random.seed(37)
            fpyw__pebzx = random.sample(ukusy__hvqj.pieces, k=len(
                ukusy__hvqj.pieces))
        else:
            fpyw__pebzx = ukusy__hvqj.pieces
        for hegx__unifb in fpyw__pebzx:
            hegx__unifb._bodo_num_rows = 0
        fpaths = [hegx__unifb.path for hegx__unifb in fpyw__pebzx[start:
            gjm__cgd]]
        if protocol == 's3':
            afs__wek = qlhcw__ucleu.netloc
            prefix = 's3://' + afs__wek + '/'
            fpaths = [anbad__qlt[len(prefix):] for anbad__qlt in fpaths]
            tkvi__qvdd = get_s3_subtree_fs(afs__wek, region=getfs().region,
                storage_options=storage_options)
        else:
            tkvi__qvdd = getfs()
        wew__bkzbf = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(wew__bkzbf)
        pa.set_cpu_count(wew__bkzbf)
        sszi__fsg = None
        try:
            ctm__nllk = ds.dataset(fpaths, filesystem=tkvi__qvdd,
                partitioning=ds.partitioning(flavor='hive'))
            for euzq__fiy, flosc__sjm in zip(fpyw__pebzx[start:gjm__cgd],
                ctm__nllk.get_fragments()):
                phyp__ocwii = time.time()
                vex__uzw = flosc__sjm.scanner(schema=ctm__nllk.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                tmda__cekht += time.time() - phyp__ocwii
                euzq__fiy._bodo_num_rows = vex__uzw
                jjacg__txq += vex__uzw
                btq__fosi += flosc__sjm.num_row_groups
                ryvi__ghqp += sum(qbnf__rsx.total_byte_size for qbnf__rsx in
                    flosc__sjm.row_groups)
                if zgesg__chi:
                    cjz__wngq = flosc__sjm.metadata.schema.to_arrow_schema()
                    if rtnwo__dxnqy != cjz__wngq:
                        print(
                            'Schema in {!s} was different. \n{!s}\n\nvs\n\n{!s}'
                            .format(euzq__fiy, cjz__wngq, rtnwo__dxnqy))
                        qpo__imgxj = False
                        break
        except Exception as lkaqb__kxcyu:
            sszi__fsg = lkaqb__kxcyu
        if rmldk__xsq.allreduce(sszi__fsg is not None, op=MPI.LOR):
            for sszi__fsg in rmldk__xsq.allgather(sszi__fsg):
                if sszi__fsg:
                    if isinstance(fpath, list) and isinstance(sszi__fsg, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(sszi__fsg) +
                            list_of_files_error_msg)
                    raise sszi__fsg
        if zgesg__chi:
            qpo__imgxj = rmldk__xsq.allreduce(qpo__imgxj, op=MPI.LAND)
            if not qpo__imgxj:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            ukusy__hvqj._bodo_total_rows = rmldk__xsq.allreduce(jjacg__txq,
                op=MPI.SUM)
            mrjxf__yiero = rmldk__xsq.allreduce(btq__fosi, op=MPI.SUM)
            djme__ehgb = rmldk__xsq.allreduce(ryvi__ghqp, op=MPI.SUM)
            sqv__syjry = np.array([hegx__unifb._bodo_num_rows for
                hegx__unifb in ukusy__hvqj.pieces])
            sqv__syjry = rmldk__xsq.allreduce(sqv__syjry, op=MPI.SUM)
            for hegx__unifb, cwa__posh in zip(ukusy__hvqj.pieces, sqv__syjry):
                hegx__unifb._bodo_num_rows = cwa__posh
            if is_parallel and bodo.get_rank(
                ) == 0 and mrjxf__yiero < bodo.get_size(
                ) and mrjxf__yiero != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({mrjxf__yiero}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if mrjxf__yiero == 0:
                msoh__nmr = 0
            else:
                msoh__nmr = djme__ehgb // mrjxf__yiero
            if (bodo.get_rank() == 0 and djme__ehgb >= 20 * 1048576 and 
                msoh__nmr < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({msoh__nmr} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                mdjps__xqd.add_attribute('g_total_num_row_groups', mrjxf__yiero
                    )
                mdjps__xqd.add_attribute('total_scan_time', tmda__cekht)
                ihty__gwv = np.array([hegx__unifb._bodo_num_rows for
                    hegx__unifb in ukusy__hvqj.pieces])
                tup__sal = np.percentile(ihty__gwv, [25, 50, 75])
                mdjps__xqd.add_attribute('g_row_counts_min', ihty__gwv.min())
                mdjps__xqd.add_attribute('g_row_counts_Q1', tup__sal[0])
                mdjps__xqd.add_attribute('g_row_counts_median', tup__sal[1])
                mdjps__xqd.add_attribute('g_row_counts_Q3', tup__sal[2])
                mdjps__xqd.add_attribute('g_row_counts_max', ihty__gwv.max())
                mdjps__xqd.add_attribute('g_row_counts_mean', ihty__gwv.mean())
                mdjps__xqd.add_attribute('g_row_counts_std', ihty__gwv.std())
                mdjps__xqd.add_attribute('g_row_counts_sum', ihty__gwv.sum())
                mdjps__xqd.finalize()
    ukusy__hvqj._prefix = ''
    if protocol in {'hdfs', 'abfs', 'abfss'}:
        prefix = f'{protocol}://{qlhcw__ucleu.netloc}'
        if len(ukusy__hvqj.pieces) > 0:
            euzq__fiy = ukusy__hvqj.pieces[0]
            if not euzq__fiy.path.startswith(prefix):
                ukusy__hvqj._prefix = prefix
    if read_categories:
        _add_categories_to_pq_dataset(ukusy__hvqj)
    if get_row_counts:
        ldvjv__jid.finalize()
    return ukusy__hvqj


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, storage_options, region, prefix,
    str_as_dict_cols, start_offset, rows_to_read):
    import pyarrow as pa
    aqob__nyifk = os.cpu_count()
    if aqob__nyifk is None or aqob__nyifk == 0:
        aqob__nyifk = 2
    bti__imf = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), aqob__nyifk)
    wiuo__bon = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), aqob__nyifk
        )
    if is_parallel and len(fpaths) > wiuo__bon and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(wiuo__bon)
        pa.set_cpu_count(wiuo__bon)
    else:
        pa.set_io_thread_count(bti__imf)
        pa.set_cpu_count(bti__imf)
    if fpaths[0].startswith('s3://'):
        afs__wek = urlparse(fpaths[0]).netloc
        prefix = 's3://' + afs__wek + '/'
        fpaths = [anbad__qlt[len(prefix):] for anbad__qlt in fpaths]
        tkvi__qvdd = get_s3_subtree_fs(afs__wek, region=region,
            storage_options=storage_options)
    elif prefix and prefix.startswith(('hdfs', 'abfs', 'abfss')):
        tkvi__qvdd = get_hdfs_fs(prefix + fpaths[0])
    elif fpaths[0].startswith(('gcs', 'gs')):
        import gcsfs
        tkvi__qvdd = gcsfs.GCSFileSystem(token=None)
    else:
        tkvi__qvdd = None
    itzf__hxf = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    ukusy__hvqj = ds.dataset(fpaths, filesystem=tkvi__qvdd, partitioning=ds
        .partitioning(flavor='hive'), format=itzf__hxf)
    col_names = ukusy__hvqj.schema.names
    uccvh__zcl = [col_names[kidk__bfjhh] for kidk__bfjhh in selected_fields]
    mgex__uor = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if mgex__uor and expr_filters is None:
        ieb__fum = []
        pita__yxt = 0
        odwz__enbhy = 0
        for flosc__sjm in ukusy__hvqj.get_fragments():
            wjrxj__wbt = []
            for qbnf__rsx in flosc__sjm.row_groups:
                wyz__vbac = qbnf__rsx.num_rows
                if start_offset < pita__yxt + wyz__vbac:
                    if odwz__enbhy == 0:
                        qia__vye = start_offset - pita__yxt
                        uobk__yawwl = min(wyz__vbac - qia__vye, rows_to_read)
                    else:
                        uobk__yawwl = min(wyz__vbac, rows_to_read - odwz__enbhy
                            )
                    odwz__enbhy += uobk__yawwl
                    wjrxj__wbt.append(qbnf__rsx.id)
                pita__yxt += wyz__vbac
                if odwz__enbhy == rows_to_read:
                    break
            ieb__fum.append(flosc__sjm.subset(row_group_ids=wjrxj__wbt))
            if odwz__enbhy == rows_to_read:
                break
        ukusy__hvqj = ds.FileSystemDataset(ieb__fum, ukusy__hvqj.schema,
            itzf__hxf, filesystem=ukusy__hvqj.filesystem)
        start_offset = qia__vye
    sxr__enxd = ukusy__hvqj.scanner(columns=uccvh__zcl, filter=expr_filters,
        use_threads=True).to_reader()
    return ukusy__hvqj, sxr__enxd, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema.to_arrow_schema()
    cfz__jzvfj = [c for c in pa_schema.names if isinstance(pa_schema.field(
        c).type, pa.DictionaryType)]
    if len(cfz__jzvfj) == 0:
        pq_dataset._category_info = {}
        return
    rmldk__xsq = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            znnd__bbz = pq_dataset.pieces[0].open()
            qbnf__rsx = znnd__bbz.read_row_group(0, cfz__jzvfj)
            category_info = {c: tuple(qbnf__rsx.column(c).chunk(0).
                dictionary.to_pylist()) for c in cfz__jzvfj}
            del znnd__bbz, qbnf__rsx
        except Exception as lkaqb__kxcyu:
            rmldk__xsq.bcast(lkaqb__kxcyu)
            raise lkaqb__kxcyu
        rmldk__xsq.bcast(category_info)
    else:
        category_info = rmldk__xsq.bcast(None)
        if isinstance(category_info, Exception):
            sszi__fsg = category_info
            raise sszi__fsg
    pq_dataset._category_info = category_info


def get_pandas_metadata(schema, num_pieces):
    yhy__vuwx = None
    nullable_from_metadata = defaultdict(lambda : None)
    wepjx__wur = b'pandas'
    if schema.metadata is not None and wepjx__wur in schema.metadata:
        import json
        hbwf__jsg = json.loads(schema.metadata[wepjx__wur].decode('utf8'))
        esosi__feh = len(hbwf__jsg['index_columns'])
        if esosi__feh > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        yhy__vuwx = hbwf__jsg['index_columns'][0] if esosi__feh else None
        if not isinstance(yhy__vuwx, str) and (not isinstance(yhy__vuwx,
            dict) or num_pieces != 1):
            yhy__vuwx = None
        for zxl__bfc in hbwf__jsg['columns']:
            udvki__umm = zxl__bfc['name']
            if zxl__bfc['pandas_type'].startswith('int'
                ) and udvki__umm is not None:
                if zxl__bfc['numpy_type'].startswith('Int'):
                    nullable_from_metadata[udvki__umm] = True
                else:
                    nullable_from_metadata[udvki__umm] = False
    return yhy__vuwx, nullable_from_metadata


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for udvki__umm in pa_schema.names:
        vgph__iikhc = pa_schema.field(udvki__umm)
        if vgph__iikhc.type == pa.string():
            str_columns.append(udvki__umm)
    return str_columns


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns):
    from mpi4py import MPI
    rmldk__xsq = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    if len(pq_dataset.pieces) > bodo.get_size():
        import random
        random.seed(37)
        fpyw__pebzx = random.sample(pq_dataset.pieces, bodo.get_size())
    else:
        fpyw__pebzx = pq_dataset.pieces
    osz__znqt = np.zeros(len(str_columns), dtype=np.int64)
    kzvo__lxjbw = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(fpyw__pebzx):
        euzq__fiy = fpyw__pebzx[bodo.get_rank()]
        try:
            bloqj__jcyp = euzq__fiy.get_metadata()
            for oji__wrdv in range(bloqj__jcyp.num_row_groups):
                for xlo__ctjnr, udvki__umm in enumerate(str_columns):
                    cmwq__vjz = pa_schema.get_field_index(udvki__umm)
                    osz__znqt[xlo__ctjnr] += bloqj__jcyp.row_group(oji__wrdv
                        ).column(cmwq__vjz).total_uncompressed_size
            ldxu__wcew = bloqj__jcyp.num_rows
        except Exception as lkaqb__kxcyu:
            if isinstance(lkaqb__kxcyu, (OSError, FileNotFoundError)):
                ldxu__wcew = 0
            else:
                raise
    else:
        ldxu__wcew = 0
    rxkek__qpncf = rmldk__xsq.allreduce(ldxu__wcew, op=MPI.SUM)
    if rxkek__qpncf == 0:
        return set()
    rmldk__xsq.Allreduce(osz__znqt, kzvo__lxjbw, op=MPI.SUM)
    qdmt__nkn = kzvo__lxjbw / rxkek__qpncf
    str_as_dict = set()
    for oji__wrdv, dtox__nmpcs in enumerate(qdmt__nkn):
        if dtox__nmpcs < READ_STR_AS_DICT_THRESHOLD:
            udvki__umm = str_columns[oji__wrdv][0]
            str_as_dict.add(udvki__umm)
    return str_as_dict


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None):
    col_names = []
    arphg__sci = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True)
    partition_names = [] if pq_dataset.partitions is None else [pq_dataset.
        partitions.levels[oji__wrdv].name for oji__wrdv in range(len(
        pq_dataset.partitions.partition_names))]
    pa_schema = pq_dataset.schema.to_arrow_schema()
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    nmi__guy = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    gua__rvuos = read_as_dict_cols - nmi__guy
    if len(gua__rvuos) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {gua__rvuos}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(nmi__guy)
    nmi__guy = nmi__guy - read_as_dict_cols
    str_columns = [xsjh__cahbb for xsjh__cahbb in str_columns if 
        xsjh__cahbb in nmi__guy]
    str_as_dict: set = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    str_as_dict.update(read_as_dict_cols)
    col_names = pa_schema.names
    yhy__vuwx, nullable_from_metadata = get_pandas_metadata(pa_schema,
        num_pieces)
    ctwi__lqyp = []
    stam__fkuw = []
    xjpk__udk = []
    for oji__wrdv, c in enumerate(col_names):
        vgph__iikhc = pa_schema.field(c)
        nwtdq__zrhwp, isc__tau = _get_numba_typ_from_pa_typ(vgph__iikhc, c ==
            yhy__vuwx, nullable_from_metadata[c], pq_dataset._category_info,
            str_as_dict=c in str_as_dict)
        ctwi__lqyp.append(nwtdq__zrhwp)
        stam__fkuw.append(isc__tau)
        xjpk__udk.append(vgph__iikhc.type)
    if partition_names:
        col_names += partition_names
        ctwi__lqyp += [_get_partition_cat_dtype(pq_dataset.partitions.
            levels[oji__wrdv]) for oji__wrdv in range(len(partition_names))]
        stam__fkuw.extend([True] * len(partition_names))
        xjpk__udk.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        col_names += [input_file_name_col]
        ctwi__lqyp += [dict_str_arr_type]
        stam__fkuw.append(True)
        xjpk__udk.append(None)
    abg__tdvhh = {c: oji__wrdv for oji__wrdv, c in enumerate(col_names)}
    if selected_columns is None:
        selected_columns = col_names
    for c in selected_columns:
        if c not in abg__tdvhh:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if yhy__vuwx and not isinstance(yhy__vuwx, dict
        ) and yhy__vuwx not in selected_columns:
        selected_columns.append(yhy__vuwx)
    col_names = selected_columns
    col_indices = []
    arphg__sci = []
    llb__cptrp = []
    ybqrb__tpihq = []
    for oji__wrdv, c in enumerate(col_names):
        oany__oga = abg__tdvhh[c]
        col_indices.append(oany__oga)
        arphg__sci.append(ctwi__lqyp[oany__oga])
        if not stam__fkuw[oany__oga]:
            llb__cptrp.append(oji__wrdv)
            ybqrb__tpihq.append(xjpk__udk[oany__oga])
    return (col_names, arphg__sci, yhy__vuwx, col_indices, partition_names,
        llb__cptrp, ybqrb__tpihq)


def _get_partition_cat_dtype(part_set):
    ayee__wrgiz = part_set.dictionary.to_pandas()
    vfb__odyf = bodo.typeof(ayee__wrgiz).dtype
    biu__enhhx = PDCategoricalDtype(tuple(ayee__wrgiz), vfb__odyf, False)
    return CategoricalArrayType(biu__enhhx)


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
        vkwnp__yhaoi = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        cufqc__oxy = cgutils.get_or_insert_function(builder.module,
            vkwnp__yhaoi, name='pq_write')
        builder.call(cufqc__oxy, args)
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
        vkwnp__yhaoi = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        cufqc__oxy = cgutils.get_or_insert_function(builder.module,
            vkwnp__yhaoi, name='pq_write_partitioned')
        builder.call(cufqc__oxy, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64), codegen
