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
    van__lkzyp = []
    tajod__qgnai = []
    fasiw__cvyz = []
    for lomqw__yiwcc, hkbm__qdd in enumerate(json_node.out_vars):
        if hkbm__qdd.name in lives:
            van__lkzyp.append(json_node.df_colnames[lomqw__yiwcc])
            tajod__qgnai.append(json_node.out_vars[lomqw__yiwcc])
            fasiw__cvyz.append(json_node.out_types[lomqw__yiwcc])
    json_node.df_colnames = van__lkzyp
    json_node.out_vars = tajod__qgnai
    json_node.out_types = fasiw__cvyz
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        cgei__wdyo = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        oshs__qqr = json_node.loc.strformat()
        ywb__bde = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', cgei__wdyo,
            oshs__qqr, ywb__bde)
        yroh__cyxra = [wkyza__spz for lomqw__yiwcc, wkyza__spz in enumerate
            (json_node.df_colnames) if isinstance(json_node.out_types[
            lomqw__yiwcc], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if yroh__cyxra:
            jzfwv__uwjr = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                jzfwv__uwjr, oshs__qqr, yroh__cyxra)
    parallel = False
    if array_dists is not None:
        parallel = True
        for yrh__gobg in json_node.out_vars:
            if array_dists[yrh__gobg.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                yrh__gobg.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    ablsv__pjs = len(json_node.out_vars)
    foahn__rdk = ', '.join('arr' + str(lomqw__yiwcc) for lomqw__yiwcc in
        range(ablsv__pjs))
    raub__krubk = 'def json_impl(fname):\n'
    raub__krubk += '    ({},) = _json_reader_py(fname)\n'.format(foahn__rdk)
    tyb__goypn = {}
    exec(raub__krubk, {}, tyb__goypn)
    wtgoi__vin = tyb__goypn['json_impl']
    amoi__eff = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    lbnjg__glt = compile_to_numba_ir(wtgoi__vin, {'_json_reader_py':
        amoi__eff}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(lbnjg__glt, [json_node.file_name])
    koxjs__yhwzt = lbnjg__glt.body[:-3]
    for lomqw__yiwcc in range(len(json_node.out_vars)):
        koxjs__yhwzt[-len(json_node.out_vars) + lomqw__yiwcc
            ].target = json_node.out_vars[lomqw__yiwcc]
    return koxjs__yhwzt


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
    utobz__fhvv = [sanitize_varname(wkyza__spz) for wkyza__spz in col_names]
    ajdti__idhs = ', '.join(str(lomqw__yiwcc) for lomqw__yiwcc, uoem__lbc in
        enumerate(col_typs) if uoem__lbc.dtype == types.NPDatetime('ns'))
    ajtwg__udfs = ', '.join(["{}='{}'".format(dcoaf__dpbzw, bodo.ir.csv_ext
        ._get_dtype_str(uoem__lbc)) for dcoaf__dpbzw, uoem__lbc in zip(
        utobz__fhvv, col_typs)])
    cfcgv__mojmr = ', '.join(["'{}':{}".format(qtqac__nkzy, bodo.ir.csv_ext
        ._get_pd_dtype_str(uoem__lbc)) for qtqac__nkzy, uoem__lbc in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    raub__krubk = 'def json_reader_py(fname):\n'
    raub__krubk += '  df_typeref_2 = df_typeref\n'
    raub__krubk += '  check_java_installation(fname)\n'
    raub__krubk += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    raub__krubk += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    raub__krubk += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    raub__krubk += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    raub__krubk += '  bodo.utils.utils.check_and_propagate_cpp_exception()\n'
    raub__krubk += '  if bodo.utils.utils.is_null_pointer(f_reader):\n'
    raub__krubk += "      raise FileNotFoundError('File does not exist')\n"
    raub__krubk += f'  with objmode({ajtwg__udfs}):\n'
    raub__krubk += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    raub__krubk += f'       convert_dates = {convert_dates}, \n'
    raub__krubk += f'       precise_float={precise_float}, \n'
    raub__krubk += f'       lines={lines}, \n'
    raub__krubk += '       dtype={{{}}},\n'.format(cfcgv__mojmr)
    raub__krubk += '       )\n'
    raub__krubk += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for dcoaf__dpbzw, qtqac__nkzy in zip(utobz__fhvv, col_names):
        raub__krubk += '    if len(df) > 0:\n'
        raub__krubk += "        {} = df['{}'].values\n".format(dcoaf__dpbzw,
            qtqac__nkzy)
        raub__krubk += '    else:\n'
        raub__krubk += '        {} = np.array([])\n'.format(dcoaf__dpbzw)
    raub__krubk += '  return ({},)\n'.format(', '.join(oydgd__bat for
        oydgd__bat in utobz__fhvv))
    btyv__kaw = globals()
    btyv__kaw.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    tyb__goypn = {}
    exec(raub__krubk, btyv__kaw, tyb__goypn)
    amoi__eff = tyb__goypn['json_reader_py']
    hdmml__ukmw = numba.njit(amoi__eff)
    compiled_funcs.append(hdmml__ukmw)
    return hdmml__ukmw
