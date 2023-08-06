import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.utils import check_java_installation, sanitize_varname


class JsonReader(ir.Stmt):

    def __init__(self, df_out, loc, out_vars, out_types, file_name,
        df_colnames, orient, convert_dates, precise_float, lines,
        compression, storage_options):
        self.connector_typ = 'json'
        self.df_out = df_out
        self.loc = loc
        self.out_vars = out_vars
        self.out_types = out_types
        self.file_name = file_name
        self.df_colnames = df_colnames
        self.orient = orient
        self.convert_dates = convert_dates
        self.precise_float = precise_float
        self.lines = lines
        self.compression = compression
        self.storage_options = storage_options

    def __repr__(self):
        return ('{} = ReadJson(file={}, col_names={}, types={}, vars={})'.
            format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars))


import llvmlite.binding as ll
from bodo.io import json_cpp
ll.add_symbol('json_file_chunk_reader', json_cpp.json_file_chunk_reader)
json_file_chunk_reader = types.ExternalFunction('json_file_chunk_reader',
    bodo.ir.connector.stream_reader_type(types.voidptr, types.bool_, types.
    bool_, types.int64, types.voidptr, types.voidptr,
    storage_options_dict_type))


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    zhs__daekr = []
    plk__wblo = []
    kvfth__imtb = []
    for vqubo__paku, amno__gio in enumerate(json_node.out_vars):
        if amno__gio.name in lives:
            zhs__daekr.append(json_node.df_colnames[vqubo__paku])
            plk__wblo.append(json_node.out_vars[vqubo__paku])
            kvfth__imtb.append(json_node.out_types[vqubo__paku])
    json_node.df_colnames = zhs__daekr
    json_node.out_vars = plk__wblo
    json_node.out_types = kvfth__imtb
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        ujjmo__fayi = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        kktz__ihk = json_node.loc.strformat()
        fjhcv__igxhv = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', ujjmo__fayi,
            kktz__ihk, fjhcv__igxhv)
        utv__sqzx = [yei__vmk for vqubo__paku, yei__vmk in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            vqubo__paku], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if utv__sqzx:
            eni__llap = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', eni__llap,
                kktz__ihk, utv__sqzx)
    parallel = False
    if array_dists is not None:
        parallel = True
        for nuu__khquc in json_node.out_vars:
            if array_dists[nuu__khquc.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                nuu__khquc.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    jjvr__milp = len(json_node.out_vars)
    orhw__hewbh = ', '.join('arr' + str(vqubo__paku) for vqubo__paku in
        range(jjvr__milp))
    ozbue__wgc = 'def json_impl(fname):\n'
    ozbue__wgc += '    ({},) = _json_reader_py(fname)\n'.format(orhw__hewbh)
    ejehq__lob = {}
    exec(ozbue__wgc, {}, ejehq__lob)
    vnbt__tgo = ejehq__lob['json_impl']
    era__ppxo = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    wkk__sgus = compile_to_numba_ir(vnbt__tgo, {'_json_reader_py':
        era__ppxo}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(wkk__sgus, [json_node.file_name])
    lmqt__fvjix = wkk__sgus.body[:-3]
    for vqubo__paku in range(len(json_node.out_vars)):
        lmqt__fvjix[-len(json_node.out_vars) + vqubo__paku
            ].target = json_node.out_vars[vqubo__paku]
    return lmqt__fvjix


numba.parfors.array_analysis.array_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[JsonReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[JsonReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[JsonReader] = remove_dead_json
numba.core.analysis.ir_extension_usedefs[JsonReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[JsonReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[JsonReader] = json_distributed_run
compiled_funcs = []


def _gen_json_reader_py(col_names, col_typs, typingctx, targetctx, parallel,
    orient, convert_dates, precise_float, lines, compression, storage_options):
    kxkx__koqd = [sanitize_varname(yei__vmk) for yei__vmk in col_names]
    crvh__boyok = ', '.join(str(vqubo__paku) for vqubo__paku, jdtkh__ynm in
        enumerate(col_typs) if jdtkh__ynm.dtype == types.NPDatetime('ns'))
    yizlj__mtkv = ', '.join(["{}='{}'".format(ymv__pdj, bodo.ir.csv_ext.
        _get_dtype_str(jdtkh__ynm)) for ymv__pdj, jdtkh__ynm in zip(
        kxkx__koqd, col_typs)])
    kzyh__ulcb = ', '.join(["'{}':{}".format(cgbts__dpz, bodo.ir.csv_ext.
        _get_pd_dtype_str(jdtkh__ynm)) for cgbts__dpz, jdtkh__ynm in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    ozbue__wgc = 'def json_reader_py(fname):\n'
    ozbue__wgc += '  df_typeref_2 = df_typeref\n'
    ozbue__wgc += '  check_java_installation(fname)\n'
    ozbue__wgc += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    ozbue__wgc += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    ozbue__wgc += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    ozbue__wgc += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    ozbue__wgc += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    ozbue__wgc += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    ozbue__wgc += "      raise FileNotFoundError('File does not exist')\n"
    ozbue__wgc += f'  with objmode({yizlj__mtkv}):\n'
    ozbue__wgc += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    ozbue__wgc += f'       convert_dates = {convert_dates}, \n'
    ozbue__wgc += f'       precise_float={precise_float}, \n'
    ozbue__wgc += f'       lines={lines}, \n'
    ozbue__wgc += '       dtype={{{}}},\n'.format(kzyh__ulcb)
    ozbue__wgc += '       )\n'
    ozbue__wgc += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for ymv__pdj, cgbts__dpz in zip(kxkx__koqd, col_names):
        ozbue__wgc += '    if len(df) > 0:\n'
        ozbue__wgc += "        {} = df['{}'].values\n".format(ymv__pdj,
            cgbts__dpz)
        ozbue__wgc += '    else:\n'
        ozbue__wgc += '        {} = np.array([])\n'.format(ymv__pdj)
    ozbue__wgc += '  return ({},)\n'.format(', '.join(zoklj__cql for
        zoklj__cql in kxkx__koqd))
    hbvm__wbj = globals()
    hbvm__wbj.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    ejehq__lob = {}
    exec(ozbue__wgc, hbvm__wbj, ejehq__lob)
    era__ppxo = ejehq__lob['json_reader_py']
    nzny__gmotr = numba.njit(era__ppxo)
    compiled_funcs.append(nzny__gmotr)
    return nzny__gmotr
