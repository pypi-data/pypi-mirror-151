"""File containing utility functions for supporting DataFrame operations with Table Format."""
import numba
import numpy as np
from numba.core import types
import bodo
from bodo.hiframes.table import TableType
from bodo.utils.typing import get_overload_const_str, is_overload_constant_str, is_overload_none, raise_bodo_error


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_mappable_table_func(table, func_name, out_arr_typ, used_cols=None
    ):
    if not is_overload_constant_str(func_name):
        raise_bodo_error(
            'generate_mappable_table_func(): func_name must be a constant string'
            )
    func_name = get_overload_const_str(func_name)
    ultkb__buvbb = out_arr_typ.instance_type if isinstance(out_arr_typ,
        types.TypeRef) else out_arr_typ
    zplrz__vcle = len(table.arr_types)
    oscqu__aqkcj = tuple([ultkb__buvbb] * zplrz__vcle)
    bugav__xcnzv = TableType(oscqu__aqkcj)
    xhea__qiios = {'bodo': bodo, 'lst_dtype': ultkb__buvbb, 'table_typ':
        bugav__xcnzv}
    mdqg__qss = 'def impl(table, func_name, out_arr_typ, used_cols=None):\n'
    mdqg__qss += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({zplrz__vcle}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        mdqg__qss += f'  used_cols_set = set(used_cols)\n'
    else:
        mdqg__qss += f'  used_cols_set = used_cols\n'
    mdqg__qss += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for rehfi__wkck in table.type_to_blk.values():
        mdqg__qss += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {rehfi__wkck})\n'
            )
        xhea__qiios[f'col_indices_{rehfi__wkck}'] = np.array(table.
            block_to_arr_ind[rehfi__wkck], dtype=np.int64)
        mdqg__qss += f'  for i in range(len(blk)):\n'
        mdqg__qss += f'    col_loc = col_indices_{rehfi__wkck}[i]\n'
        if not is_overload_none(used_cols):
            mdqg__qss += f'    if col_loc not in used_cols_set:\n'
            mdqg__qss += f'        continue\n'
        mdqg__qss += f'    out_list[col_loc] = {func_name}(blk[i])\n'
    mdqg__qss += (
        '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)'
        )
    iwq__uavkw = {}
    exec(mdqg__qss, xhea__qiios, iwq__uavkw)
    return iwq__uavkw['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    xhea__qiios = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    mdqg__qss = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    mdqg__qss += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for rehfi__wkck in table.type_to_blk.values():
        mdqg__qss += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {rehfi__wkck})\n'
            )
        xhea__qiios[f'col_indices_{rehfi__wkck}'] = np.array(table.
            block_to_arr_ind[rehfi__wkck], dtype=np.int64)
        mdqg__qss += '  for i in range(len(blk)):\n'
        mdqg__qss += f'    col_loc = col_indices_{rehfi__wkck}[i]\n'
        mdqg__qss += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    mdqg__qss += '  if parallel:\n'
    mdqg__qss += '    for i in range(start_offset, len(out_arr)):\n'
    mdqg__qss += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    iwq__uavkw = {}
    exec(mdqg__qss, xhea__qiios, iwq__uavkw)
    return iwq__uavkw['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    rrjys__vtnh = table.type_to_blk[arr_type]
    xhea__qiios = {'bodo': bodo}
    xhea__qiios['col_indices'] = np.array(table.block_to_arr_ind[
        rrjys__vtnh], dtype=np.int64)
    mdqg__qss = 'def impl(table, col_nums, arr_type):\n'
    mdqg__qss += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {rrjys__vtnh})\n')
    mdqg__qss += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    mdqg__qss += '  n = len(table)\n'
    qbmns__chsj = bodo.utils.typing.is_str_arr_type(arr_type)
    if qbmns__chsj:
        mdqg__qss += '  total_chars = 0\n'
        mdqg__qss += '  for c in col_nums:\n'
        mdqg__qss += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        mdqg__qss += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        mdqg__qss += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        mdqg__qss += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        mdqg__qss += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    mdqg__qss += '  for i in range(len(col_nums)):\n'
    mdqg__qss += '    c = col_nums[i]\n'
    if not qbmns__chsj:
        mdqg__qss += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    mdqg__qss += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    mdqg__qss += '    off = i * n\n'
    mdqg__qss += '    for j in range(len(arr)):\n'
    mdqg__qss += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    mdqg__qss += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    mdqg__qss += '      else:\n'
    mdqg__qss += '        out_arr[off+j] = arr[j]\n'
    mdqg__qss += '  return out_arr\n'
    ogclj__chbq = {}
    exec(mdqg__qss, xhea__qiios, ogclj__chbq)
    pwp__nbcct = ogclj__chbq['impl']
    return pwp__nbcct
