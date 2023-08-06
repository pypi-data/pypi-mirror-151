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
    ffc__gtuxz = out_arr_typ.instance_type if isinstance(out_arr_typ, types
        .TypeRef) else out_arr_typ
    jvdf__lefdu = len(table.arr_types)
    igtdl__gmwq = tuple([ffc__gtuxz] * jvdf__lefdu)
    idsrm__rlbo = TableType(igtdl__gmwq)
    wwkse__wia = {'bodo': bodo, 'lst_dtype': ffc__gtuxz, 'table_typ':
        idsrm__rlbo}
    mlfo__qtaq = 'def impl(table, func_name, out_arr_typ, used_cols=None):\n'
    mlfo__qtaq += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({jvdf__lefdu}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        mlfo__qtaq += f'  used_cols_set = set(used_cols)\n'
    else:
        mlfo__qtaq += f'  used_cols_set = used_cols\n'
    mlfo__qtaq += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for rrof__ldg in table.type_to_blk.values():
        mlfo__qtaq += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {rrof__ldg})\n'
            )
        wwkse__wia[f'col_indices_{rrof__ldg}'] = np.array(table.
            block_to_arr_ind[rrof__ldg], dtype=np.int64)
        mlfo__qtaq += f'  for i in range(len(blk)):\n'
        mlfo__qtaq += f'    col_loc = col_indices_{rrof__ldg}[i]\n'
        if not is_overload_none(used_cols):
            mlfo__qtaq += f'    if col_loc not in used_cols_set:\n'
            mlfo__qtaq += f'        continue\n'
        mlfo__qtaq += f'    out_list[col_loc] = {func_name}(blk[i])\n'
    mlfo__qtaq += (
        '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)'
        )
    osqg__fnqvc = {}
    exec(mlfo__qtaq, wwkse__wia, osqg__fnqvc)
    return osqg__fnqvc['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    wwkse__wia = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value)}
    mlfo__qtaq = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    mlfo__qtaq += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for rrof__ldg in table.type_to_blk.values():
        mlfo__qtaq += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {rrof__ldg})\n'
            )
        wwkse__wia[f'col_indices_{rrof__ldg}'] = np.array(table.
            block_to_arr_ind[rrof__ldg], dtype=np.int64)
        mlfo__qtaq += '  for i in range(len(blk)):\n'
        mlfo__qtaq += f'    col_loc = col_indices_{rrof__ldg}[i]\n'
        mlfo__qtaq += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    mlfo__qtaq += '  if parallel:\n'
    mlfo__qtaq += '    for i in range(start_offset, len(out_arr)):\n'
    mlfo__qtaq += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    osqg__fnqvc = {}
    exec(mlfo__qtaq, wwkse__wia, osqg__fnqvc)
    return osqg__fnqvc['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    eheo__sldlv = table.type_to_blk[arr_type]
    wwkse__wia = {'bodo': bodo}
    wwkse__wia['col_indices'] = np.array(table.block_to_arr_ind[eheo__sldlv
        ], dtype=np.int64)
    mlfo__qtaq = 'def impl(table, col_nums, arr_type):\n'
    mlfo__qtaq += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {eheo__sldlv})\n')
    mlfo__qtaq += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    mlfo__qtaq += '  n = len(table)\n'
    wdafr__mtn = bodo.utils.typing.is_str_arr_type(arr_type)
    if wdafr__mtn:
        mlfo__qtaq += '  total_chars = 0\n'
        mlfo__qtaq += '  for c in col_nums:\n'
        mlfo__qtaq += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        mlfo__qtaq += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        mlfo__qtaq += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        mlfo__qtaq += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        mlfo__qtaq += """  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))
"""
    mlfo__qtaq += '  for i in range(len(col_nums)):\n'
    mlfo__qtaq += '    c = col_nums[i]\n'
    if not wdafr__mtn:
        mlfo__qtaq += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    mlfo__qtaq += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    mlfo__qtaq += '    off = i * n\n'
    mlfo__qtaq += '    for j in range(len(arr)):\n'
    mlfo__qtaq += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    mlfo__qtaq += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    mlfo__qtaq += '      else:\n'
    mlfo__qtaq += '        out_arr[off+j] = arr[j]\n'
    mlfo__qtaq += '  return out_arr\n'
    mufbv__vat = {}
    exec(mlfo__qtaq, wwkse__wia, mufbv__vat)
    xbzsy__itl = mufbv__vat['impl']
    return xbzsy__itl
