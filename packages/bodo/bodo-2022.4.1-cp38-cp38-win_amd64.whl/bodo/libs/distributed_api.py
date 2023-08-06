import atexit
import datetime
import operator
import sys
import time
import warnings
from collections import defaultdict
from decimal import Decimal
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir_utils, types
from numba.core.typing import signature
from numba.core.typing.builtins import IndexValueType
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, models, overload, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdist
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, set_bit_to_arr
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, num_total_chars, pre_alloc_string_array, set_bit_to, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, BodoWarning, decode_if_dict_array, is_overload_false, is_overload_none, is_str_arr_type
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, empty_like_type, is_array_typ, numba_to_c_type
ll.add_symbol('dist_get_time', hdist.dist_get_time)
ll.add_symbol('get_time', hdist.get_time)
ll.add_symbol('dist_reduce', hdist.dist_reduce)
ll.add_symbol('dist_arr_reduce', hdist.dist_arr_reduce)
ll.add_symbol('dist_exscan', hdist.dist_exscan)
ll.add_symbol('dist_irecv', hdist.dist_irecv)
ll.add_symbol('dist_isend', hdist.dist_isend)
ll.add_symbol('dist_wait', hdist.dist_wait)
ll.add_symbol('dist_get_item_pointer', hdist.dist_get_item_pointer)
ll.add_symbol('get_dummy_ptr', hdist.get_dummy_ptr)
ll.add_symbol('allgather', hdist.allgather)
ll.add_symbol('comm_req_alloc', hdist.comm_req_alloc)
ll.add_symbol('comm_req_dealloc', hdist.comm_req_dealloc)
ll.add_symbol('req_array_setitem', hdist.req_array_setitem)
ll.add_symbol('dist_waitall', hdist.dist_waitall)
ll.add_symbol('oneD_reshape_shuffle', hdist.oneD_reshape_shuffle)
ll.add_symbol('permutation_int', hdist.permutation_int)
ll.add_symbol('permutation_array_index', hdist.permutation_array_index)
ll.add_symbol('c_get_rank', hdist.dist_get_rank)
ll.add_symbol('c_get_size', hdist.dist_get_size)
ll.add_symbol('c_barrier', hdist.barrier)
ll.add_symbol('c_alltoall', hdist.c_alltoall)
ll.add_symbol('c_gather_scalar', hdist.c_gather_scalar)
ll.add_symbol('c_gatherv', hdist.c_gatherv)
ll.add_symbol('c_scatterv', hdist.c_scatterv)
ll.add_symbol('c_allgatherv', hdist.c_allgatherv)
ll.add_symbol('c_bcast', hdist.c_bcast)
ll.add_symbol('c_recv', hdist.dist_recv)
ll.add_symbol('c_send', hdist.dist_send)
mpi_req_numba_type = getattr(types, 'int' + str(8 * hdist.mpi_req_num_bytes))
MPI_ROOT = 0
ANY_SOURCE = np.int32(hdist.ANY_SOURCE)


class Reduce_Type(Enum):
    Sum = 0
    Prod = 1
    Min = 2
    Max = 3
    Argmin = 4
    Argmax = 5
    Or = 6
    Concat = 7
    No_Op = 8


_get_rank = types.ExternalFunction('c_get_rank', types.int32())
_get_size = types.ExternalFunction('c_get_size', types.int32())
_barrier = types.ExternalFunction('c_barrier', types.int32())


@numba.njit
def get_rank():
    return _get_rank()


@numba.njit
def get_size():
    return _get_size()


@numba.njit
def barrier():
    _barrier()


_get_time = types.ExternalFunction('get_time', types.float64())
dist_time = types.ExternalFunction('dist_get_time', types.float64())


@overload(time.time, no_unliteral=True)
def overload_time_time():
    return lambda : _get_time()


@numba.generated_jit(nopython=True)
def get_type_enum(arr):
    arr = arr.instance_type if isinstance(arr, types.TypeRef) else arr
    dtype = arr.dtype
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = bodo.hiframes.pd_categorical_ext.get_categories_int_type(dtype)
    typ_val = numba_to_c_type(dtype)
    return lambda arr: np.int32(typ_val)


INT_MAX = np.iinfo(np.int32).max
_send = types.ExternalFunction('c_send', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def send(val, rank, tag):
    send_arr = np.full(1, val)
    xqkd__gfvqt = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, xqkd__gfvqt, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    xqkd__gfvqt = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, xqkd__gfvqt, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            xqkd__gfvqt = get_type_enum(arr)
            return _isend(arr.ctypes, size, xqkd__gfvqt, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        xqkd__gfvqt = np.int32(numba_to_c_type(arr.dtype))
        hast__jgi = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            seyba__hwcy = size + 7 >> 3
            anl__klc = _isend(arr._data.ctypes, size, xqkd__gfvqt, pe, tag,
                cond)
            wwvvq__oanat = _isend(arr._null_bitmap.ctypes, seyba__hwcy,
                hast__jgi, pe, tag, cond)
            return anl__klc, wwvvq__oanat
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        rzjm__jgum = np.int32(numba_to_c_type(offset_type))
        hast__jgi = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            jla__vvdyj = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(jla__vvdyj, pe, tag - 1)
            seyba__hwcy = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                rzjm__jgum, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), jla__vvdyj,
                hast__jgi, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                seyba__hwcy, hast__jgi, pe, tag)
            return None
        return impl_str_arr
    typ_enum = numba_to_c_type(types.uint8)

    def impl_voidptr(arr, size, pe, tag, cond=True):
        return _isend(arr, size, typ_enum, pe, tag, cond)
    return impl_voidptr


_irecv = types.ExternalFunction('dist_irecv', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def irecv(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            xqkd__gfvqt = get_type_enum(arr)
            return _irecv(arr.ctypes, size, xqkd__gfvqt, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        xqkd__gfvqt = np.int32(numba_to_c_type(arr.dtype))
        hast__jgi = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            seyba__hwcy = size + 7 >> 3
            anl__klc = _irecv(arr._data.ctypes, size, xqkd__gfvqt, pe, tag,
                cond)
            wwvvq__oanat = _irecv(arr._null_bitmap.ctypes, seyba__hwcy,
                hast__jgi, pe, tag, cond)
            return anl__klc, wwvvq__oanat
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        rzjm__jgum = np.int32(numba_to_c_type(offset_type))
        hast__jgi = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            rboyh__oaln = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            rboyh__oaln = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        hpkfg__isgfy = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {rboyh__oaln}(size, n_chars)
            bodo.libs.str_arr_ext.move_str_binary_arr_payload(arr, new_arr)

            n_bytes = (size + 7) >> 3
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_offset_ptr(arr),
                size + 1,
                offset_typ_enum,
                pe,
                tag,
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_data_ptr(arr), n_chars, char_typ_enum, pe, tag
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                n_bytes,
                char_typ_enum,
                pe,
                tag,
            )
            return None"""
        poy__nbbfw = dict()
        exec(hpkfg__isgfy, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            rzjm__jgum, 'char_typ_enum': hast__jgi}, poy__nbbfw)
        impl = poy__nbbfw['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    xqkd__gfvqt = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), xqkd__gfvqt)


@numba.generated_jit(nopython=True)
def gather_scalar(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    data = types.unliteral(data)
    typ_val = numba_to_c_type(data)
    dtype = data

    def gather_scalar_impl(data, allgather=False, warn_if_rep=True, root=
        MPI_ROOT):
        n_pes = bodo.libs.distributed_api.get_size()
        rank = bodo.libs.distributed_api.get_rank()
        send = np.full(1, data, dtype)
        yngbb__mcn = n_pes if rank == root or allgather else 0
        afl__vsx = np.empty(yngbb__mcn, dtype)
        c_gather_scalar(send.ctypes, afl__vsx.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return afl__vsx
    return gather_scalar_impl


c_gather_scalar = types.ExternalFunction('c_gather_scalar', types.void(
    types.voidptr, types.voidptr, types.int32, types.bool_, types.int32))
c_gatherv = types.ExternalFunction('c_gatherv', types.void(types.voidptr,
    types.int32, types.voidptr, types.voidptr, types.voidptr, types.int32,
    types.bool_, types.int32))
c_scatterv = types.ExternalFunction('c_scatterv', types.void(types.voidptr,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.int32))


@intrinsic
def value_to_ptr(typingctx, val_tp=None):

    def codegen(context, builder, sig, args):
        bob__vgl = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], bob__vgl)
        return builder.bitcast(bob__vgl, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        bob__vgl = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(bob__vgl)
    return val_tp(ptr_tp, val_tp), codegen


_dist_reduce = types.ExternalFunction('dist_reduce', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))
_dist_arr_reduce = types.ExternalFunction('dist_arr_reduce', types.void(
    types.voidptr, types.int64, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_reduce(value, reduce_op):
    if isinstance(value, types.Array):
        typ_enum = np.int32(numba_to_c_type(value.dtype))

        def impl_arr(value, reduce_op):
            A = np.ascontiguousarray(value)
            _dist_arr_reduce(A.ctypes, A.size, reduce_op, typ_enum)
            return A
        return impl_arr
    cpgyp__bmnj = types.unliteral(value)
    if isinstance(cpgyp__bmnj, IndexValueType):
        cpgyp__bmnj = cpgyp__bmnj.val_typ
        ativ__mwglu = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            ativ__mwglu.append(types.int64)
            ativ__mwglu.append(bodo.datetime64ns)
            ativ__mwglu.append(bodo.timedelta64ns)
            ativ__mwglu.append(bodo.datetime_date_type)
        if cpgyp__bmnj not in ativ__mwglu:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(cpgyp__bmnj))
    typ_enum = np.int32(numba_to_c_type(cpgyp__bmnj))

    def impl(value, reduce_op):
        iqc__ztd = value_to_ptr(value)
        ddtz__fsht = value_to_ptr(value)
        _dist_reduce(iqc__ztd, ddtz__fsht, reduce_op, typ_enum)
        return load_val_ptr(ddtz__fsht, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    cpgyp__bmnj = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(cpgyp__bmnj))
    xzhlj__vtp = cpgyp__bmnj(0)

    def impl(value, reduce_op):
        iqc__ztd = value_to_ptr(value)
        ddtz__fsht = value_to_ptr(xzhlj__vtp)
        _dist_exscan(iqc__ztd, ddtz__fsht, reduce_op, typ_enum)
        return load_val_ptr(ddtz__fsht, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    beadv__aoiq = 0
    hdin__jelnq = 0
    for i in range(len(recv_counts)):
        kjq__cgi = recv_counts[i]
        seyba__hwcy = recv_counts_nulls[i]
        nrmxo__qiw = tmp_null_bytes[beadv__aoiq:beadv__aoiq + seyba__hwcy]
        for whai__dacao in range(kjq__cgi):
            set_bit_to(null_bitmap_ptr, hdin__jelnq, get_bit(nrmxo__qiw,
                whai__dacao))
            hdin__jelnq += 1
        beadv__aoiq += seyba__hwcy


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            igqjf__tcap = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                igqjf__tcap, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            zrqk__ljwr = data.size
            recv_counts = gather_scalar(np.int32(zrqk__ljwr), allgather,
                root=root)
            ytpij__yyfex = recv_counts.sum()
            hznki__qhkc = empty_like_type(ytpij__yyfex, data)
            hhw__zqf = np.empty(1, np.int32)
            if rank == root or allgather:
                hhw__zqf = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(zrqk__ljwr), hznki__qhkc.ctypes,
                recv_counts.ctypes, hhw__zqf.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return hznki__qhkc.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            hznki__qhkc = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.str_arr_ext.init_str_arr(hznki__qhkc)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            hznki__qhkc = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.binary_arr_ext.init_binary_arr(hznki__qhkc)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        hast__jgi = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            zrqk__ljwr = len(data)
            seyba__hwcy = zrqk__ljwr + 7 >> 3
            recv_counts = gather_scalar(np.int32(zrqk__ljwr), allgather,
                root=root)
            ytpij__yyfex = recv_counts.sum()
            hznki__qhkc = empty_like_type(ytpij__yyfex, data)
            hhw__zqf = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            dtp__dkclq = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                hhw__zqf = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                dtp__dkclq = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(zrqk__ljwr),
                hznki__qhkc._days_data.ctypes, recv_counts.ctypes, hhw__zqf
                .ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(zrqk__ljwr),
                hznki__qhkc._seconds_data.ctypes, recv_counts.ctypes,
                hhw__zqf.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(zrqk__ljwr),
                hznki__qhkc._microseconds_data.ctypes, recv_counts.ctypes,
                hhw__zqf.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(seyba__hwcy),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, dtp__dkclq
                .ctypes, hast__jgi, allgather, np.int32(root))
            copy_gathered_null_bytes(hznki__qhkc._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return hznki__qhkc
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        hast__jgi = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            zrqk__ljwr = len(data)
            seyba__hwcy = zrqk__ljwr + 7 >> 3
            recv_counts = gather_scalar(np.int32(zrqk__ljwr), allgather,
                root=root)
            ytpij__yyfex = recv_counts.sum()
            hznki__qhkc = empty_like_type(ytpij__yyfex, data)
            hhw__zqf = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            dtp__dkclq = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                hhw__zqf = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                dtp__dkclq = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(zrqk__ljwr), hznki__qhkc.
                _data.ctypes, recv_counts.ctypes, hhw__zqf.ctypes, np.int32
                (typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(seyba__hwcy),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, dtp__dkclq
                .ctypes, hast__jgi, allgather, np.int32(root))
            copy_gathered_null_bytes(hznki__qhkc._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return hznki__qhkc
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        omn__jrgg = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rga__aui = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                rga__aui, omn__jrgg)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            yywhk__cbnbq = bodo.gatherv(data._left, allgather, warn_if_rep,
                root)
            yonf__xvxge = bodo.gatherv(data._right, allgather, warn_if_rep,
                root)
            return bodo.libs.interval_arr_ext.init_interval_array(yywhk__cbnbq,
                yonf__xvxge)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            yaaqd__mcr = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            aroj__ewfdn = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                aroj__ewfdn, yaaqd__mcr)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        nab__bbts = np.iinfo(np.int64).max
        qfb__bbyj = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            start = data._start
            stop = data._stop
            if len(data) == 0:
                start = nab__bbts
                stop = qfb__bbyj
            start = bodo.libs.distributed_api.dist_reduce(start, np.int32(
                Reduce_Type.Min.value))
            stop = bodo.libs.distributed_api.dist_reduce(stop, np.int32(
                Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if start == nab__bbts and stop == qfb__bbyj:
                start = 0
                stop = 0
            nqdt__kdbmq = max(0, -(-(stop - start) // data._step))
            if nqdt__kdbmq < total_len:
                stop = start + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                start = 0
                stop = 0
            return bodo.hiframes.pd_index_ext.init_range_index(start, stop,
                data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            jrpld__qhw = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, jrpld__qhw)
        else:

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.utils.conversion.index_from_array(arr, data._name)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            hznki__qhkc = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                hznki__qhkc, data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        fwizc__pgp = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        hpkfg__isgfy = f"""def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        hpkfg__isgfy += '  T = data\n'
        hpkfg__isgfy += '  T2 = init_table(T, True)\n'
        for djux__vsti in data.type_to_blk.values():
            fwizc__pgp[f'arr_inds_{djux__vsti}'] = np.array(data.
                block_to_arr_ind[djux__vsti], dtype=np.int64)
            hpkfg__isgfy += (
                f'  arr_list_{djux__vsti} = get_table_block(T, {djux__vsti})\n'
                )
            hpkfg__isgfy += f"""  out_arr_list_{djux__vsti} = alloc_list_like(arr_list_{djux__vsti}, True)
"""
            hpkfg__isgfy += f'  for i in range(len(arr_list_{djux__vsti})):\n'
            hpkfg__isgfy += (
                f'    arr_ind_{djux__vsti} = arr_inds_{djux__vsti}[i]\n')
            hpkfg__isgfy += f"""    ensure_column_unboxed(T, arr_list_{djux__vsti}, i, arr_ind_{djux__vsti})
"""
            hpkfg__isgfy += f"""    out_arr_{djux__vsti} = bodo.gatherv(arr_list_{djux__vsti}[i], allgather, warn_if_rep, root)
"""
            hpkfg__isgfy += (
                f'    out_arr_list_{djux__vsti}[i] = out_arr_{djux__vsti}\n')
            hpkfg__isgfy += (
                f'  T2 = set_table_block(T2, out_arr_list_{djux__vsti}, {djux__vsti})\n'
                )
        hpkfg__isgfy += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        hpkfg__isgfy += f'  T2 = set_table_len(T2, length)\n'
        hpkfg__isgfy += f'  return T2\n'
        poy__nbbfw = {}
        exec(hpkfg__isgfy, fwizc__pgp, poy__nbbfw)
        zbyfk__iaf = poy__nbbfw['impl_table']
        return zbyfk__iaf
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ipvi__jpsqq = len(data.columns)
        if ipvi__jpsqq == 0:

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                jzdce__xvx = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    jzdce__xvx, ())
            return impl
        smlzz__ergpz = ', '.join(f'g_data_{i}' for i in range(ipvi__jpsqq))
        xqo__xvw = bodo.utils.transform.gen_const_tup(data.columns)
        hpkfg__isgfy = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            tcyvn__bjb = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            fwizc__pgp = {'bodo': bodo, 'df_type': tcyvn__bjb}
            smlzz__ergpz = 'T2'
            xqo__xvw = 'df_type'
            hpkfg__isgfy += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            hpkfg__isgfy += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            fwizc__pgp = {'bodo': bodo}
            for i in range(ipvi__jpsqq):
                hpkfg__isgfy += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                hpkfg__isgfy += (
                    """  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)
"""
                    .format(i, i))
        hpkfg__isgfy += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        hpkfg__isgfy += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        hpkfg__isgfy += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(smlzz__ergpz, xqo__xvw))
        poy__nbbfw = {}
        exec(hpkfg__isgfy, fwizc__pgp, poy__nbbfw)
        fhf__yhsgh = poy__nbbfw['impl_df']
        return fhf__yhsgh
    if isinstance(data, ArrayItemArrayType):
        rmbj__jsmay = np.int32(numba_to_c_type(types.int32))
        hast__jgi = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            djzye__soj = bodo.libs.array_item_arr_ext.get_offsets(data)
            rrr__oagl = bodo.libs.array_item_arr_ext.get_data(data)
            rrr__oagl = rrr__oagl[:djzye__soj[-1]]
            wty__pkq = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            zrqk__ljwr = len(data)
            stgzd__pifk = np.empty(zrqk__ljwr, np.uint32)
            seyba__hwcy = zrqk__ljwr + 7 >> 3
            for i in range(zrqk__ljwr):
                stgzd__pifk[i] = djzye__soj[i + 1] - djzye__soj[i]
            recv_counts = gather_scalar(np.int32(zrqk__ljwr), allgather,
                root=root)
            ytpij__yyfex = recv_counts.sum()
            hhw__zqf = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            dtp__dkclq = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                hhw__zqf = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for hqat__ted in range(len(recv_counts)):
                    recv_counts_nulls[hqat__ted] = recv_counts[hqat__ted
                        ] + 7 >> 3
                dtp__dkclq = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            ughh__basl = np.empty(ytpij__yyfex + 1, np.uint32)
            qcbrr__vxpvw = bodo.gatherv(rrr__oagl, allgather, warn_if_rep, root
                )
            sms__xga = np.empty(ytpij__yyfex + 7 >> 3, np.uint8)
            c_gatherv(stgzd__pifk.ctypes, np.int32(zrqk__ljwr), ughh__basl.
                ctypes, recv_counts.ctypes, hhw__zqf.ctypes, rmbj__jsmay,
                allgather, np.int32(root))
            c_gatherv(wty__pkq.ctypes, np.int32(seyba__hwcy),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, dtp__dkclq
                .ctypes, hast__jgi, allgather, np.int32(root))
            dummy_use(data)
            kjwhf__dxl = np.empty(ytpij__yyfex + 1, np.uint64)
            convert_len_arr_to_offset(ughh__basl.ctypes, kjwhf__dxl.ctypes,
                ytpij__yyfex)
            copy_gathered_null_bytes(sms__xga.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                ytpij__yyfex, qcbrr__vxpvw, kjwhf__dxl, sms__xga)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        sjj__tpxaq = data.names
        hast__jgi = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            dhy__pkec = bodo.libs.struct_arr_ext.get_data(data)
            viwy__emh = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            eggp__sbopd = bodo.gatherv(dhy__pkec, allgather=allgather, root
                =root)
            rank = bodo.libs.distributed_api.get_rank()
            zrqk__ljwr = len(data)
            seyba__hwcy = zrqk__ljwr + 7 >> 3
            recv_counts = gather_scalar(np.int32(zrqk__ljwr), allgather,
                root=root)
            ytpij__yyfex = recv_counts.sum()
            ses__jdmdn = np.empty(ytpij__yyfex + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            dtp__dkclq = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                dtp__dkclq = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(viwy__emh.ctypes, np.int32(seyba__hwcy),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, dtp__dkclq
                .ctypes, hast__jgi, allgather, np.int32(root))
            copy_gathered_null_bytes(ses__jdmdn.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(eggp__sbopd,
                ses__jdmdn, sjj__tpxaq)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            hznki__qhkc = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.binary_arr_ext.init_binary_arr(hznki__qhkc)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            hznki__qhkc = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.tuple_arr_ext.init_tuple_arr(hznki__qhkc)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            hznki__qhkc = bodo.gatherv(data._data, allgather, warn_if_rep, root
                )
            return bodo.libs.map_arr_ext.init_map_arr(hznki__qhkc)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            hznki__qhkc = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            mpvl__oop = bodo.gatherv(data.indices, allgather, warn_if_rep, root
                )
            bsxgw__royne = bodo.gatherv(data.indptr, allgather, warn_if_rep,
                root)
            tjnj__tok = gather_scalar(data.shape[0], allgather, root=root)
            clhe__cuykp = tjnj__tok.sum()
            ipvi__jpsqq = bodo.libs.distributed_api.dist_reduce(data.shape[
                1], np.int32(Reduce_Type.Max.value))
            gtz__yosrh = np.empty(clhe__cuykp + 1, np.int64)
            mpvl__oop = mpvl__oop.astype(np.int64)
            gtz__yosrh[0] = 0
            ibhs__rfjsk = 1
            mse__bro = 0
            for oje__tdsb in tjnj__tok:
                for ndha__gqgwa in range(oje__tdsb):
                    ror__wmzdo = bsxgw__royne[mse__bro + 1] - bsxgw__royne[
                        mse__bro]
                    gtz__yosrh[ibhs__rfjsk] = gtz__yosrh[ibhs__rfjsk - 1
                        ] + ror__wmzdo
                    ibhs__rfjsk += 1
                    mse__bro += 1
                mse__bro += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(hznki__qhkc,
                mpvl__oop, gtz__yosrh, (clhe__cuykp, ipvi__jpsqq))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        hpkfg__isgfy = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        hpkfg__isgfy += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        poy__nbbfw = {}
        exec(hpkfg__isgfy, {'bodo': bodo}, poy__nbbfw)
        jlzt__pux = poy__nbbfw['impl_tuple']
        return jlzt__pux
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    hpkfg__isgfy = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    hpkfg__isgfy += '    if random:\n'
    hpkfg__isgfy += '        if random_seed is None:\n'
    hpkfg__isgfy += '            random = 1\n'
    hpkfg__isgfy += '        else:\n'
    hpkfg__isgfy += '            random = 2\n'
    hpkfg__isgfy += '    if random_seed is None:\n'
    hpkfg__isgfy += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        fsrs__jdzxb = data
        ipvi__jpsqq = len(fsrs__jdzxb.columns)
        for i in range(ipvi__jpsqq):
            hpkfg__isgfy += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        hpkfg__isgfy += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        smlzz__ergpz = ', '.join(f'data_{i}' for i in range(ipvi__jpsqq))
        hpkfg__isgfy += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(yoh__vsrum) for
            yoh__vsrum in range(ipvi__jpsqq))))
        hpkfg__isgfy += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        hpkfg__isgfy += '    if dests is None:\n'
        hpkfg__isgfy += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        hpkfg__isgfy += '    else:\n'
        hpkfg__isgfy += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for ddrdu__ayk in range(ipvi__jpsqq):
            hpkfg__isgfy += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(ddrdu__ayk))
        hpkfg__isgfy += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(ipvi__jpsqq))
        hpkfg__isgfy += '    delete_table(out_table)\n'
        hpkfg__isgfy += '    if parallel:\n'
        hpkfg__isgfy += '        delete_table(table_total)\n'
        smlzz__ergpz = ', '.join('out_arr_{}'.format(i) for i in range(
            ipvi__jpsqq))
        xqo__xvw = bodo.utils.transform.gen_const_tup(fsrs__jdzxb.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        hpkfg__isgfy += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(smlzz__ergpz, index, xqo__xvw))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        hpkfg__isgfy += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        hpkfg__isgfy += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        hpkfg__isgfy += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        hpkfg__isgfy += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        hpkfg__isgfy += '    if dests is None:\n'
        hpkfg__isgfy += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        hpkfg__isgfy += '    else:\n'
        hpkfg__isgfy += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        hpkfg__isgfy += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        hpkfg__isgfy += """    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)
"""
        hpkfg__isgfy += '    delete_table(out_table)\n'
        hpkfg__isgfy += '    if parallel:\n'
        hpkfg__isgfy += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        hpkfg__isgfy += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        hpkfg__isgfy += '    if not parallel:\n'
        hpkfg__isgfy += '        return data\n'
        hpkfg__isgfy += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        hpkfg__isgfy += '    if dests is None:\n'
        hpkfg__isgfy += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        hpkfg__isgfy += '    elif bodo.get_rank() not in dests:\n'
        hpkfg__isgfy += '        dim0_local_size = 0\n'
        hpkfg__isgfy += '    else:\n'
        hpkfg__isgfy += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        hpkfg__isgfy += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        hpkfg__isgfy += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        hpkfg__isgfy += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        hpkfg__isgfy += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        hpkfg__isgfy += '    if dests is None:\n'
        hpkfg__isgfy += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        hpkfg__isgfy += '    else:\n'
        hpkfg__isgfy += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        hpkfg__isgfy += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        hpkfg__isgfy += '    delete_table(out_table)\n'
        hpkfg__isgfy += '    if parallel:\n'
        hpkfg__isgfy += '        delete_table(table_total)\n'
        hpkfg__isgfy += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    poy__nbbfw = {}
    exec(hpkfg__isgfy, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table},
        poy__nbbfw)
    impl = poy__nbbfw['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    hpkfg__isgfy = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        hpkfg__isgfy += '    if seed is None:\n'
        hpkfg__isgfy += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        hpkfg__isgfy += '    np.random.seed(seed)\n'
        hpkfg__isgfy += '    if not parallel:\n'
        hpkfg__isgfy += '        data = data.copy()\n'
        hpkfg__isgfy += '        np.random.shuffle(data)\n'
        hpkfg__isgfy += '        return data\n'
        hpkfg__isgfy += '    else:\n'
        hpkfg__isgfy += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        hpkfg__isgfy += '        permutation = np.arange(dim0_global_size)\n'
        hpkfg__isgfy += '        np.random.shuffle(permutation)\n'
        hpkfg__isgfy += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        hpkfg__isgfy += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        hpkfg__isgfy += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        hpkfg__isgfy += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        hpkfg__isgfy += '        return output\n'
    else:
        hpkfg__isgfy += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    poy__nbbfw = {}
    exec(hpkfg__isgfy, {'np': np, 'bodo': bodo}, poy__nbbfw)
    impl = poy__nbbfw['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    eea__ifq = np.empty(sendcounts_nulls.sum(), np.uint8)
    beadv__aoiq = 0
    hdin__jelnq = 0
    for ffjfj__tlh in range(len(sendcounts)):
        kjq__cgi = sendcounts[ffjfj__tlh]
        seyba__hwcy = sendcounts_nulls[ffjfj__tlh]
        nrmxo__qiw = eea__ifq[beadv__aoiq:beadv__aoiq + seyba__hwcy]
        for whai__dacao in range(kjq__cgi):
            set_bit_to_arr(nrmxo__qiw, whai__dacao, get_bit_bitmap(
                null_bitmap_ptr, hdin__jelnq))
            hdin__jelnq += 1
        beadv__aoiq += seyba__hwcy
    return eea__ifq


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    mqhu__pmpch = MPI.COMM_WORLD
    data = mqhu__pmpch.bcast(data, root)
    return data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_scatterv_send_counts(send_counts, n_pes, n):
    if not is_overload_none(send_counts):
        return lambda send_counts, n_pes, n: send_counts

    def impl(send_counts, n_pes, n):
        send_counts = np.empty(n_pes, np.int32)
        for i in range(n_pes):
            send_counts[i] = get_node_portion(n, n_pes, i)
        return send_counts
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _scatterv_np(data, send_counts=None, warn_if_dist=True):
    typ_val = numba_to_c_type(data.dtype)
    fgiby__skwmi = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    cti__kpr = (0,) * fgiby__skwmi

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        iilw__nou = np.ascontiguousarray(data)
        xuwgz__bhm = data.ctypes
        qjkmb__kog = cti__kpr
        if rank == MPI_ROOT:
            qjkmb__kog = iilw__nou.shape
        qjkmb__kog = bcast_tuple(qjkmb__kog)
        viokw__nlbxd = get_tuple_prod(qjkmb__kog[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            qjkmb__kog[0])
        send_counts *= viokw__nlbxd
        zrqk__ljwr = send_counts[rank]
        wmibz__hzfq = np.empty(zrqk__ljwr, dtype)
        hhw__zqf = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(xuwgz__bhm, send_counts.ctypes, hhw__zqf.ctypes,
            wmibz__hzfq.ctypes, np.int32(zrqk__ljwr), np.int32(typ_val))
        return wmibz__hzfq.reshape((-1,) + qjkmb__kog[1:])
    return scatterv_arr_impl


def _get_name_value_for_type(name_typ):
    assert isinstance(name_typ, (types.UnicodeType, types.StringLiteral)
        ) or name_typ == types.none
    return None if name_typ == types.none else '_' + str(ir_utils.next_label())


def get_value_for_type(dtype):
    if isinstance(dtype, types.Array):
        return np.zeros((1,) * dtype.ndim, numba.np.numpy_support.as_dtype(
            dtype.dtype))
    if dtype == string_array_type:
        return pd.array(['A'], 'string')
    if dtype == bodo.dict_str_arr_type:
        import pyarrow as pa
        return pa.array(['a'], type=pa.dictionary(pa.int32(), pa.string()))
    if dtype == binary_array_type:
        return np.array([b'A'], dtype=object)
    if isinstance(dtype, IntegerArrayType):
        xlv__cse = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], xlv__cse)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        yaaqd__mcr = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=yaaqd__mcr)
        pdxz__vwkb = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(pdxz__vwkb)
        return pd.Index(arr, name=yaaqd__mcr)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        yaaqd__mcr = _get_name_value_for_type(dtype.name_typ)
        sjj__tpxaq = tuple(_get_name_value_for_type(t) for t in dtype.names_typ
            )
        xdr__fsa = tuple(get_value_for_type(t) for t in dtype.array_types)
        xdr__fsa = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in xdr__fsa)
        val = pd.MultiIndex.from_arrays(xdr__fsa, names=sjj__tpxaq)
        val.name = yaaqd__mcr
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        yaaqd__mcr = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=yaaqd__mcr)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        xdr__fsa = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({yaaqd__mcr: arr for yaaqd__mcr, arr in zip(
            dtype.columns, xdr__fsa)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        pdxz__vwkb = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(pdxz__vwkb[0],
            pdxz__vwkb[0])])
    raise BodoError(f'get_value_for_type(dtype): Missing data type {dtype}')


def scatterv(data, send_counts=None, warn_if_dist=True):
    rank = bodo.libs.distributed_api.get_rank()
    if rank != MPI_ROOT and data is not None:
        warnings.warn(BodoWarning(
            "bodo.scatterv(): A non-None value for 'data' was found on a rank other than the root. This data won't be sent to any other ranks and will be overwritten with data from rank 0."
            ))
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return scatterv_impl(data, send_counts)


@overload(scatterv)
def scatterv_overload(data, send_counts=None, warn_if_dist=True):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.scatterv()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.scatterv()')
    return lambda data, send_counts=None, warn_if_dist=True: scatterv_impl(data
        , send_counts)


@numba.generated_jit(nopython=True)
def scatterv_impl(data, send_counts=None, warn_if_dist=True):
    if isinstance(data, types.Array):
        return lambda data, send_counts=None, warn_if_dist=True: _scatterv_np(
            data, send_counts)
    if is_str_arr_type(data) or data == binary_array_type:
        rmbj__jsmay = np.int32(numba_to_c_type(types.int32))
        hast__jgi = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            rboyh__oaln = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            rboyh__oaln = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        hpkfg__isgfy = f"""def impl(
            data, send_counts=None, warn_if_dist=True
        ):  # pragma: no cover
            data = decode_if_dict_array(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            n_all = bodo.libs.distributed_api.bcast_scalar(len(data))

            # convert offsets to lengths of strings
            send_arr_lens = np.empty(
                len(data), np.uint32
            )  # XXX offset type is offset_type, lengths for comm are uint32
            for i in range(len(data)):
                send_arr_lens[i] = bodo.libs.str_arr_ext.get_str_arr_item_length(
                    data, i
                )

            # ------- calculate buffer counts -------

            send_counts = bodo.libs.distributed_api._get_scatterv_send_counts(send_counts, n_pes, n_all)

            # displacements
            displs = bodo.ir.join.calc_disp(send_counts)

            # compute send counts for characters
            send_counts_char = np.empty(n_pes, np.int32)
            if rank == 0:
                curr_str = 0
                for i in range(n_pes):
                    c = 0
                    for _ in range(send_counts[i]):
                        c += send_arr_lens[curr_str]
                        curr_str += 1
                    send_counts_char[i] = c

            bodo.libs.distributed_api.bcast(send_counts_char)

            # displacements for characters
            displs_char = bodo.ir.join.calc_disp(send_counts_char)

            # compute send counts for nulls
            send_counts_nulls = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                send_counts_nulls[i] = (send_counts[i] + 7) >> 3

            # displacements for nulls
            displs_nulls = bodo.ir.join.calc_disp(send_counts_nulls)

            # alloc output array
            n_loc = send_counts[rank]  # total number of elements on this PE
            n_loc_char = send_counts_char[rank]
            recv_arr = {rboyh__oaln}(n_loc, n_loc_char)

            # ----- string lengths -----------

            recv_lens = np.empty(n_loc, np.uint32)
            bodo.libs.distributed_api.c_scatterv(
                send_arr_lens.ctypes,
                send_counts.ctypes,
                displs.ctypes,
                recv_lens.ctypes,
                np.int32(n_loc),
                int32_typ_enum,
            )

            # TODO: don't hardcode offset type. Also, if offset is 32 bit we can
            # use the same buffer
            bodo.libs.str_arr_ext.convert_len_arr_to_offset(recv_lens.ctypes, bodo.libs.str_arr_ext.get_offset_ptr(recv_arr), n_loc)

            # ----- string characters -----------

            bodo.libs.distributed_api.c_scatterv(
                bodo.libs.str_arr_ext.get_data_ptr(data),
                send_counts_char.ctypes,
                displs_char.ctypes,
                bodo.libs.str_arr_ext.get_data_ptr(recv_arr),
                np.int32(n_loc_char),
                char_typ_enum,
            )

            # ----------- null bitmap -------------

            n_recv_bytes = (n_loc + 7) >> 3

            send_null_bitmap = bodo.libs.distributed_api.get_scatter_null_bytes_buff(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(data), send_counts, send_counts_nulls
            )

            bodo.libs.distributed_api.c_scatterv(
                send_null_bitmap.ctypes,
                send_counts_nulls.ctypes,
                displs_nulls.ctypes,
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(recv_arr),
                np.int32(n_recv_bytes),
                char_typ_enum,
            )

            return recv_arr"""
        poy__nbbfw = dict()
        exec(hpkfg__isgfy, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            rmbj__jsmay, 'char_typ_enum': hast__jgi, 'decode_if_dict_array':
            decode_if_dict_array}, poy__nbbfw)
        impl = poy__nbbfw['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        rmbj__jsmay = np.int32(numba_to_c_type(types.int32))
        hast__jgi = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            hkli__pisy = bodo.libs.array_item_arr_ext.get_offsets(data)
            viltt__ktugz = bodo.libs.array_item_arr_ext.get_data(data)
            viltt__ktugz = viltt__ktugz[:hkli__pisy[-1]]
            stsmd__ozcxr = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            spup__vuvun = bcast_scalar(len(data))
            dhfh__wdpha = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                dhfh__wdpha[i] = hkli__pisy[i + 1] - hkli__pisy[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                spup__vuvun)
            hhw__zqf = bodo.ir.join.calc_disp(send_counts)
            eocy__sxfbp = np.empty(n_pes, np.int32)
            if rank == 0:
                krx__nhfe = 0
                for i in range(n_pes):
                    dkwv__jbv = 0
                    for ndha__gqgwa in range(send_counts[i]):
                        dkwv__jbv += dhfh__wdpha[krx__nhfe]
                        krx__nhfe += 1
                    eocy__sxfbp[i] = dkwv__jbv
            bcast(eocy__sxfbp)
            nfxwu__wvzt = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                nfxwu__wvzt[i] = send_counts[i] + 7 >> 3
            dtp__dkclq = bodo.ir.join.calc_disp(nfxwu__wvzt)
            zrqk__ljwr = send_counts[rank]
            niiha__lobsv = np.empty(zrqk__ljwr + 1, np_offset_type)
            stmr__agku = bodo.libs.distributed_api.scatterv_impl(viltt__ktugz,
                eocy__sxfbp)
            bsg__dadhj = zrqk__ljwr + 7 >> 3
            etxd__veq = np.empty(bsg__dadhj, np.uint8)
            gvvsy__tfgqb = np.empty(zrqk__ljwr, np.uint32)
            c_scatterv(dhfh__wdpha.ctypes, send_counts.ctypes, hhw__zqf.
                ctypes, gvvsy__tfgqb.ctypes, np.int32(zrqk__ljwr), rmbj__jsmay)
            convert_len_arr_to_offset(gvvsy__tfgqb.ctypes, niiha__lobsv.
                ctypes, zrqk__ljwr)
            kxsj__jxo = get_scatter_null_bytes_buff(stsmd__ozcxr.ctypes,
                send_counts, nfxwu__wvzt)
            c_scatterv(kxsj__jxo.ctypes, nfxwu__wvzt.ctypes, dtp__dkclq.
                ctypes, etxd__veq.ctypes, np.int32(bsg__dadhj), hast__jgi)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                zrqk__ljwr, stmr__agku, niiha__lobsv, etxd__veq)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        hast__jgi = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            duka__cdeuo = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            duka__cdeuo = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            duka__cdeuo = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            duka__cdeuo = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            iilw__nou = data._data
            viwy__emh = data._null_bitmap
            syt__dkf = len(iilw__nou)
            jyxc__wachb = _scatterv_np(iilw__nou, send_counts)
            spup__vuvun = bcast_scalar(syt__dkf)
            bridd__iufly = len(jyxc__wachb) + 7 >> 3
            vyerm__udmr = np.empty(bridd__iufly, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                spup__vuvun)
            nfxwu__wvzt = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                nfxwu__wvzt[i] = send_counts[i] + 7 >> 3
            dtp__dkclq = bodo.ir.join.calc_disp(nfxwu__wvzt)
            kxsj__jxo = get_scatter_null_bytes_buff(viwy__emh.ctypes,
                send_counts, nfxwu__wvzt)
            c_scatterv(kxsj__jxo.ctypes, nfxwu__wvzt.ctypes, dtp__dkclq.
                ctypes, vyerm__udmr.ctypes, np.int32(bridd__iufly), hast__jgi)
            return duka__cdeuo(jyxc__wachb, vyerm__udmr)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            zxi__avfak = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            ikxhd__jekag = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(zxi__avfak,
                ikxhd__jekag)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            dyv__gvng = data._step
            yaaqd__mcr = data._name
            yaaqd__mcr = bcast_scalar(yaaqd__mcr)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            dyv__gvng = bcast_scalar(dyv__gvng)
            dvtfi__ihg = bodo.libs.array_kernels.calc_nitems(start, stop,
                dyv__gvng)
            chunk_start = bodo.libs.distributed_api.get_start(dvtfi__ihg,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(dvtfi__ihg
                , n_pes, rank)
            fpwx__ovl = start + dyv__gvng * chunk_start
            fnp__hav = start + dyv__gvng * (chunk_start + chunk_count)
            fnp__hav = min(fnp__hav, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(fpwx__ovl,
                fnp__hav, dyv__gvng, yaaqd__mcr)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        jrpld__qhw = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            iilw__nou = data._data
            yaaqd__mcr = data._name
            yaaqd__mcr = bcast_scalar(yaaqd__mcr)
            arr = bodo.libs.distributed_api.scatterv_impl(iilw__nou,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                yaaqd__mcr, jrpld__qhw)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            iilw__nou = data._data
            yaaqd__mcr = data._name
            yaaqd__mcr = bcast_scalar(yaaqd__mcr)
            arr = bodo.libs.distributed_api.scatterv_impl(iilw__nou,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, yaaqd__mcr)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            hznki__qhkc = bodo.libs.distributed_api.scatterv_impl(data.
                _data, send_counts)
            yaaqd__mcr = bcast_scalar(data._name)
            sjj__tpxaq = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                hznki__qhkc, sjj__tpxaq, yaaqd__mcr)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            yaaqd__mcr = bodo.hiframes.pd_series_ext.get_series_name(data)
            imsii__dnc = bcast_scalar(yaaqd__mcr)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            aroj__ewfdn = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                aroj__ewfdn, imsii__dnc)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ipvi__jpsqq = len(data.columns)
        smlzz__ergpz = ', '.join('g_data_{}'.format(i) for i in range(
            ipvi__jpsqq))
        xqo__xvw = bodo.utils.transform.gen_const_tup(data.columns)
        hpkfg__isgfy = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        for i in range(ipvi__jpsqq):
            hpkfg__isgfy += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            hpkfg__isgfy += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        hpkfg__isgfy += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        hpkfg__isgfy += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        hpkfg__isgfy += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(smlzz__ergpz, xqo__xvw))
        poy__nbbfw = {}
        exec(hpkfg__isgfy, {'bodo': bodo}, poy__nbbfw)
        fhf__yhsgh = poy__nbbfw['impl_df']
        return fhf__yhsgh
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            igqjf__tcap = bodo.libs.distributed_api.scatterv_impl(data.
                codes, send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                igqjf__tcap, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        hpkfg__isgfy = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        hpkfg__isgfy += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        poy__nbbfw = {}
        exec(hpkfg__isgfy, {'bodo': bodo}, poy__nbbfw)
        jlzt__pux = poy__nbbfw['impl_tuple']
        return jlzt__pux
    if data is types.none:
        return lambda data, send_counts=None, warn_if_dist=True: None
    raise BodoError('scatterv() not available for {}'.format(data))


@intrinsic
def cptr_to_voidptr(typingctx, cptr_tp=None):

    def codegen(context, builder, sig, args):
        return builder.bitcast(args[0], lir.IntType(8).as_pointer())
    return types.voidptr(cptr_tp), codegen


def bcast(data, root=MPI_ROOT):
    return


@overload(bcast, no_unliteral=True)
def bcast_overload(data, root=MPI_ROOT):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.bcast()')
    if isinstance(data, types.Array):

        def bcast_impl(data, root=MPI_ROOT):
            typ_enum = get_type_enum(data)
            count = data.size
            assert count < INT_MAX
            c_bcast(data.ctypes, np.int32(count), typ_enum, np.array([-1]).
                ctypes, 0, np.int32(root))
            return
        return bcast_impl
    if isinstance(data, DecimalArrayType):

        def bcast_decimal_arr(data, root=MPI_ROOT):
            count = data._data.size
            assert count < INT_MAX
            c_bcast(data._data.ctypes, np.int32(count), CTypeEnum.Int128.
                value, np.array([-1]).ctypes, 0, np.int32(root))
            bcast(data._null_bitmap, root)
            return
        return bcast_decimal_arr
    if isinstance(data, IntegerArrayType) or data in (boolean_array,
        datetime_date_array_type):

        def bcast_impl_int_arr(data, root=MPI_ROOT):
            bcast(data._data, root)
            bcast(data._null_bitmap, root)
            return
        return bcast_impl_int_arr
    if is_str_arr_type(data) or data == binary_array_type:
        rzjm__jgum = np.int32(numba_to_c_type(offset_type))
        hast__jgi = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            zrqk__ljwr = len(data)
            nvxo__npb = num_total_chars(data)
            assert zrqk__ljwr < INT_MAX
            assert nvxo__npb < INT_MAX
            bshpp__skkp = get_offset_ptr(data)
            xuwgz__bhm = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            seyba__hwcy = zrqk__ljwr + 7 >> 3
            c_bcast(bshpp__skkp, np.int32(zrqk__ljwr + 1), rzjm__jgum, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(xuwgz__bhm, np.int32(nvxo__npb), hast__jgi, np.array([-
                1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(seyba__hwcy), hast__jgi, np.
                array([-1]).ctypes, 0, np.int32(root))
        return bcast_str_impl


c_bcast = types.ExternalFunction('c_bcast', types.void(types.voidptr, types
    .int32, types.int32, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def bcast_scalar(val, root=MPI_ROOT):
    val = types.unliteral(val)
    if not (isinstance(val, (types.Integer, types.Float)) or val in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.string_type, types.none,
        types.bool_]):
        raise BodoError(
            f'bcast_scalar requires an argument of type Integer, Float, datetime64ns, timedelta64ns, string, None, or Bool. Found type {val}'
            )
    if val == types.none:
        return lambda val, root=MPI_ROOT: None
    if val == bodo.string_type:
        hast__jgi = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                hbv__omwl = 0
                hknm__gfx = np.empty(0, np.uint8).ctypes
            else:
                hknm__gfx, hbv__omwl = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            hbv__omwl = bodo.libs.distributed_api.bcast_scalar(hbv__omwl, root)
            if rank != root:
                kxiu__gis = np.empty(hbv__omwl + 1, np.uint8)
                kxiu__gis[hbv__omwl] = 0
                hknm__gfx = kxiu__gis.ctypes
            c_bcast(hknm__gfx, np.int32(hbv__omwl), hast__jgi, np.array([-1
                ]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(hknm__gfx, hbv__omwl)
        return impl_str
    typ_val = numba_to_c_type(val)
    hpkfg__isgfy = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    poy__nbbfw = {}
    exec(hpkfg__isgfy, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, poy__nbbfw)
    nzbxr__vsoqu = poy__nbbfw['bcast_scalar_impl']
    return nzbxr__vsoqu


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    gkm__bes = len(val)
    hpkfg__isgfy = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    hpkfg__isgfy += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(gkm__bes)), 
        ',' if gkm__bes else '')
    poy__nbbfw = {}
    exec(hpkfg__isgfy, {'bcast_scalar': bcast_scalar}, poy__nbbfw)
    bdqtl__whgl = poy__nbbfw['bcast_tuple_impl']
    return bdqtl__whgl


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            zrqk__ljwr = bcast_scalar(len(arr), root)
            oeyo__dbsk = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(zrqk__ljwr, oeyo__dbsk)
            return arr
        return prealloc_impl
    return lambda arr, root=MPI_ROOT: arr


def get_local_slice(idx, arr_start, total_len):
    return idx


@overload(get_local_slice, no_unliteral=True, jit_options={'cache': True,
    'no_cpython_wrapper': True})
def get_local_slice_overload(idx, arr_start, total_len):

    def impl(idx, arr_start, total_len):
        slice_index = numba.cpython.unicode._normalize_slice(idx, total_len)
        start = slice_index.start
        dyv__gvng = slice_index.step
        msqgs__dyfkd = 0 if dyv__gvng == 1 or start > arr_start else abs(
            dyv__gvng - arr_start % dyv__gvng) % dyv__gvng
        fpwx__ovl = max(arr_start, slice_index.start
            ) - arr_start + msqgs__dyfkd
        fnp__hav = max(slice_index.stop - arr_start, 0)
        return slice(fpwx__ovl, fnp__hav, dyv__gvng)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        boar__wkrd = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[boar__wkrd])
    return getitem_impl


dummy_use = numba.njit(lambda a: None)


def int_getitem(arr, ind, arr_start, total_len, is_1D):
    return arr[ind]


def transform_str_getitem_output(data, length):
    pass


@overload(transform_str_getitem_output)
def overload_transform_str_getitem_output(data, length):
    if data == bodo.string_type:
        return lambda data, length: bodo.libs.str_arr_ext.decode_utf8(data.
            _data, length)
    if data == types.Array(types.uint8, 1, 'C'):
        return lambda data, length: bodo.libs.binary_arr_ext.init_bytes_type(
            data, length)
    raise BodoError(
        f'Internal Error: Expected String or Uint8 Array, found {data}')


@overload(int_getitem, no_unliteral=True)
def int_getitem_overload(arr, ind, arr_start, total_len, is_1D):
    if is_str_arr_type(arr) or arr == bodo.binary_array_type:
        safol__afa = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        hast__jgi = np.int32(numba_to_c_type(types.uint8))
        getcs__ipfj = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            qopse__emezc = np.int32(10)
            tag = np.int32(11)
            amlca__ijnu = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                rrr__oagl = arr._data
                ggp__rgdmq = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    rrr__oagl, ind)
                yfe__omps = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    rrr__oagl, ind + 1)
                length = yfe__omps - ggp__rgdmq
                bob__vgl = rrr__oagl[ind]
                amlca__ijnu[0] = length
                isend(amlca__ijnu, np.int32(1), root, qopse__emezc, True)
                isend(bob__vgl, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                getcs__ipfj, safol__afa, 0, 1)
            nqdt__kdbmq = 0
            if rank == root:
                nqdt__kdbmq = recv(np.int64, ANY_SOURCE, qopse__emezc)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    getcs__ipfj, safol__afa, nqdt__kdbmq, 1)
                xuwgz__bhm = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(xuwgz__bhm, np.int32(nqdt__kdbmq), hast__jgi,
                    ANY_SOURCE, tag)
            dummy_use(amlca__ijnu)
            nqdt__kdbmq = bcast_scalar(nqdt__kdbmq)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    getcs__ipfj, safol__afa, nqdt__kdbmq, 1)
            xuwgz__bhm = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(xuwgz__bhm, np.int32(nqdt__kdbmq), hast__jgi, np.array(
                [-1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, nqdt__kdbmq)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        epo__kmy = bodo.hiframes.pd_categorical_ext.get_categories_int_type(arr
            .dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, epo__kmy)
            if arr_start <= ind < arr_start + len(arr):
                igqjf__tcap = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = igqjf__tcap[ind - arr_start]
                send_arr = np.full(1, data, epo__kmy)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = epo__kmy(-1)
            if rank == root:
                val = recv(epo__kmy, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            dero__uuzz = arr.dtype.categories[max(val, 0)]
            return dero__uuzz
        return cat_getitem_impl
    zriod__ppqav = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, zriod__ppqav)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, zriod__ppqav)[0]
        if rank == root:
            val = recv(zriod__ppqav, ANY_SOURCE, tag)
        dummy_use(send_arr)
        val = bcast_scalar(val)
        return val
    return getitem_impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    yjjuy__zjud = get_type_enum(out_data)
    assert typ_enum == yjjuy__zjud
    if isinstance(send_data, (IntegerArrayType, DecimalArrayType)
        ) or send_data in (boolean_array, datetime_date_array_type):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data._data.ctypes,
            out_data._data.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    if isinstance(send_data, bodo.CategoricalArrayType):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data.codes.ctypes,
            out_data.codes.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    return (lambda send_data, out_data, send_counts, recv_counts, send_disp,
        recv_disp: c_alltoallv(send_data.ctypes, out_data.ctypes,
        send_counts.ctypes, recv_counts.ctypes, send_disp.ctypes, recv_disp
        .ctypes, typ_enum))


def alltoallv_tup(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    return


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(send_data, out_data, send_counts, recv_counts,
    send_disp, recv_disp):
    count = send_data.count
    assert out_data.count == count
    hpkfg__isgfy = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        hpkfg__isgfy += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    hpkfg__isgfy += '  return\n'
    poy__nbbfw = {}
    exec(hpkfg__isgfy, {'alltoallv': alltoallv}, poy__nbbfw)
    xgcr__fgyl = poy__nbbfw['f']
    return xgcr__fgyl


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    start = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return start, count


@numba.njit
def get_start(total_size, pes, rank):
    afl__vsx = total_size % pes
    til__sinzv = (total_size - afl__vsx) // pes
    return rank * til__sinzv + min(rank, afl__vsx)


@numba.njit
def get_end(total_size, pes, rank):
    afl__vsx = total_size % pes
    til__sinzv = (total_size - afl__vsx) // pes
    return (rank + 1) * til__sinzv + min(rank + 1, afl__vsx)


@numba.njit
def get_node_portion(total_size, pes, rank):
    afl__vsx = total_size % pes
    til__sinzv = (total_size - afl__vsx) // pes
    if rank < afl__vsx:
        return til__sinzv + 1
    else:
        return til__sinzv


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    xzhlj__vtp = in_arr.dtype(0)
    hldv__wllqt = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        dkwv__jbv = xzhlj__vtp
        for goxe__wotp in np.nditer(in_arr):
            dkwv__jbv += goxe__wotp.item()
        fnn__mflqj = dist_exscan(dkwv__jbv, hldv__wllqt)
        for i in range(in_arr.size):
            fnn__mflqj += in_arr[i]
            out_arr[i] = fnn__mflqj
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    low__dnw = in_arr.dtype(1)
    hldv__wllqt = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        dkwv__jbv = low__dnw
        for goxe__wotp in np.nditer(in_arr):
            dkwv__jbv *= goxe__wotp.item()
        fnn__mflqj = dist_exscan(dkwv__jbv, hldv__wllqt)
        if get_rank() == 0:
            fnn__mflqj = low__dnw
        for i in range(in_arr.size):
            fnn__mflqj *= in_arr[i]
            out_arr[i] = fnn__mflqj
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        low__dnw = np.finfo(in_arr.dtype(1).dtype).max
    else:
        low__dnw = np.iinfo(in_arr.dtype(1).dtype).max
    hldv__wllqt = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        dkwv__jbv = low__dnw
        for goxe__wotp in np.nditer(in_arr):
            dkwv__jbv = min(dkwv__jbv, goxe__wotp.item())
        fnn__mflqj = dist_exscan(dkwv__jbv, hldv__wllqt)
        if get_rank() == 0:
            fnn__mflqj = low__dnw
        for i in range(in_arr.size):
            fnn__mflqj = min(fnn__mflqj, in_arr[i])
            out_arr[i] = fnn__mflqj
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        low__dnw = np.finfo(in_arr.dtype(1).dtype).min
    else:
        low__dnw = np.iinfo(in_arr.dtype(1).dtype).min
    low__dnw = in_arr.dtype(1)
    hldv__wllqt = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        dkwv__jbv = low__dnw
        for goxe__wotp in np.nditer(in_arr):
            dkwv__jbv = max(dkwv__jbv, goxe__wotp.item())
        fnn__mflqj = dist_exscan(dkwv__jbv, hldv__wllqt)
        if get_rank() == 0:
            fnn__mflqj = low__dnw
        for i in range(in_arr.size):
            fnn__mflqj = max(fnn__mflqj, in_arr[i])
            out_arr[i] = fnn__mflqj
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    xqkd__gfvqt = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), xqkd__gfvqt)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    dcab__yxps = args[0]
    if equiv_set.has_shape(dcab__yxps):
        return ArrayAnalysis.AnalyzeResult(shape=dcab__yxps, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_dist_return = (
    dist_return_equiv)
ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_rep_return = (
    dist_return_equiv)


def threaded_return(A):
    return A


@numba.njit
def set_arr_local(arr, ind, val):
    arr[ind] = val


@numba.njit
def local_alloc_size(n, in_arr):
    return n


@infer_global(threaded_return)
@infer_global(dist_return)
@infer_global(rep_return)
class ThreadedRetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        return signature(args[0], *args)


@numba.njit
def parallel_print(*args):
    print(*args)


@numba.njit
def single_print(*args):
    if bodo.libs.distributed_api.get_rank() == 0:
        print(*args)


def print_if_not_empty(args):
    pass


@overload(print_if_not_empty)
def overload_print_if_not_empty(*args):
    xrnn__mpt = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for i,
        nuuez__oqow in enumerate(args) if is_array_typ(nuuez__oqow) or
        isinstance(nuuez__oqow, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    hpkfg__isgfy = f"""def impl(*args):
    if {xrnn__mpt} or bodo.get_rank() == 0:
        print(*args)"""
    poy__nbbfw = {}
    exec(hpkfg__isgfy, globals(), poy__nbbfw)
    impl = poy__nbbfw['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        hnz__qvjqw = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        hpkfg__isgfy = 'def f(req, cond=True):\n'
        hpkfg__isgfy += f'  return {hnz__qvjqw}\n'
        poy__nbbfw = {}
        exec(hpkfg__isgfy, {'_wait': _wait}, poy__nbbfw)
        impl = poy__nbbfw['f']
        return impl
    if is_overload_none(req):
        return lambda req, cond=True: None
    return lambda req, cond=True: _wait(req, cond)


class ReqArrayType(types.Type):

    def __init__(self):
        super(ReqArrayType, self).__init__(name='ReqArrayType()')


req_array_type = ReqArrayType()
register_model(ReqArrayType)(models.OpaqueModel)
waitall = types.ExternalFunction('dist_waitall', types.void(types.int32,
    req_array_type))
comm_req_alloc = types.ExternalFunction('comm_req_alloc', req_array_type(
    types.int32))
comm_req_dealloc = types.ExternalFunction('comm_req_dealloc', types.void(
    req_array_type))
req_array_setitem = types.ExternalFunction('req_array_setitem', types.void(
    req_array_type, types.int64, mpi_req_numba_type))


@overload(operator.setitem, no_unliteral=True)
def overload_req_arr_setitem(A, idx, val):
    if A == req_array_type:
        assert val == mpi_req_numba_type
        return lambda A, idx, val: req_array_setitem(A, idx, val)


@numba.njit
def _get_local_range(start, stop, chunk_start, chunk_count):
    assert start >= 0 and stop > 0
    fpwx__ovl = max(start, chunk_start)
    fnp__hav = min(stop, chunk_start + chunk_count)
    wwgi__ditm = fpwx__ovl - chunk_start
    ogc__funbn = fnp__hav - chunk_start
    if wwgi__ditm < 0 or ogc__funbn < 0:
        wwgi__ditm = 1
        ogc__funbn = 0
    return wwgi__ditm, ogc__funbn


@register_jitable
def _set_if_in_range(A, val, index, chunk_start):
    if index >= chunk_start and index < chunk_start + len(A):
        A[index - chunk_start] = val


@register_jitable
def _root_rank_select(old_val, new_val):
    if get_rank() == 0:
        return old_val
    return new_val


def get_tuple_prod(t):
    return np.prod(t)


@overload(get_tuple_prod, no_unliteral=True)
def get_tuple_prod_overload(t):
    if t == numba.core.types.containers.Tuple(()):
        return lambda t: 1

    def get_tuple_prod_impl(t):
        afl__vsx = 1
        for a in t:
            afl__vsx *= a
        return afl__vsx
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    pxajo__agadl = np.ascontiguousarray(in_arr)
    pyz__rxfxk = get_tuple_prod(pxajo__agadl.shape[1:])
    qxc__lfj = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        obm__ols = np.array(dest_ranks, dtype=np.int32)
    else:
        obm__ols = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, pxajo__agadl.ctypes,
        new_dim0_global_len, len(in_arr), dtype_size * qxc__lfj, dtype_size *
        pyz__rxfxk, len(obm__ols), obm__ols.ctypes)
    check_and_propagate_cpp_exception()


permutation_int = types.ExternalFunction('permutation_int', types.void(
    types.voidptr, types.intp))


@numba.njit
def dist_permutation_int(lhs, n):
    permutation_int(lhs.ctypes, n)


permutation_array_index = types.ExternalFunction('permutation_array_index',
    types.void(types.voidptr, types.intp, types.intp, types.voidptr, types.
    int64, types.voidptr, types.intp))


@numba.njit
def dist_permutation_array_index(lhs, lhs_len, dtype_size, rhs, p, p_len):
    xatt__rhk = np.ascontiguousarray(rhs)
    jmng__foie = get_tuple_prod(xatt__rhk.shape[1:])
    qed__xny = dtype_size * jmng__foie
    permutation_array_index(lhs.ctypes, lhs_len, qed__xny, xatt__rhk.ctypes,
        xatt__rhk.shape[0], p.ctypes, p_len)
    check_and_propagate_cpp_exception()


from bodo.io import fsspec_reader, hdfs_reader, s3_reader
ll.add_symbol('finalize', hdist.finalize)
finalize = types.ExternalFunction('finalize', types.int32())
ll.add_symbol('finalize_s3', s3_reader.finalize_s3)
finalize_s3 = types.ExternalFunction('finalize_s3', types.int32())
ll.add_symbol('finalize_fsspec', fsspec_reader.finalize_fsspec)
finalize_fsspec = types.ExternalFunction('finalize_fsspec', types.int32())
ll.add_symbol('disconnect_hdfs', hdfs_reader.disconnect_hdfs)
disconnect_hdfs = types.ExternalFunction('disconnect_hdfs', types.int32())


def _check_for_cpp_errors():
    pass


@overload(_check_for_cpp_errors)
def overload_check_for_cpp_errors():
    return lambda : check_and_propagate_cpp_exception()


@numba.njit
def call_finalize():
    finalize()
    finalize_s3()
    finalize_fsspec()
    _check_for_cpp_errors()
    disconnect_hdfs()


def flush_stdout():
    if not sys.stdout.closed:
        sys.stdout.flush()


atexit.register(call_finalize)
atexit.register(flush_stdout)


def bcast_comm(data, comm_ranks, nranks, root=MPI_ROOT):
    rank = bodo.libs.distributed_api.get_rank()
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype, root)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return bcast_comm_impl(data, comm_ranks, nranks, root)


@overload(bcast_comm)
def bcast_comm_overload(data, comm_ranks, nranks, root=MPI_ROOT):
    return lambda data, comm_ranks, nranks, root=MPI_ROOT: bcast_comm_impl(data
        , comm_ranks, nranks, root)


@numba.generated_jit(nopython=True)
def bcast_comm_impl(data, comm_ranks, nranks, root=MPI_ROOT):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.bcast_comm()')
    if isinstance(data, (types.Integer, types.Float)):
        typ_val = numba_to_c_type(data)
        hpkfg__isgfy = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        poy__nbbfw = {}
        exec(hpkfg__isgfy, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, poy__nbbfw)
        nzbxr__vsoqu = poy__nbbfw['bcast_scalar_impl']
        return nzbxr__vsoqu
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ipvi__jpsqq = len(data.columns)
        smlzz__ergpz = ', '.join('g_data_{}'.format(i) for i in range(
            ipvi__jpsqq))
        xqo__xvw = bodo.utils.transform.gen_const_tup(data.columns)
        hpkfg__isgfy = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(ipvi__jpsqq):
            hpkfg__isgfy += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            hpkfg__isgfy += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        hpkfg__isgfy += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        hpkfg__isgfy += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        hpkfg__isgfy += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(smlzz__ergpz, xqo__xvw))
        poy__nbbfw = {}
        exec(hpkfg__isgfy, {'bodo': bodo}, poy__nbbfw)
        fhf__yhsgh = poy__nbbfw['impl_df']
        return fhf__yhsgh
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            dyv__gvng = data._step
            yaaqd__mcr = data._name
            yaaqd__mcr = bcast_scalar(yaaqd__mcr, root)
            start = bcast_scalar(start, root)
            stop = bcast_scalar(stop, root)
            dyv__gvng = bcast_scalar(dyv__gvng, root)
            dvtfi__ihg = bodo.libs.array_kernels.calc_nitems(start, stop,
                dyv__gvng)
            chunk_start = bodo.libs.distributed_api.get_start(dvtfi__ihg,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(dvtfi__ihg
                , n_pes, rank)
            fpwx__ovl = start + dyv__gvng * chunk_start
            fnp__hav = start + dyv__gvng * (chunk_start + chunk_count)
            fnp__hav = min(fnp__hav, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(fpwx__ovl,
                fnp__hav, dyv__gvng, yaaqd__mcr)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            iilw__nou = data._data
            yaaqd__mcr = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(iilw__nou,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, yaaqd__mcr)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            yaaqd__mcr = bodo.hiframes.pd_series_ext.get_series_name(data)
            imsii__dnc = bodo.libs.distributed_api.bcast_comm_impl(yaaqd__mcr,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            aroj__ewfdn = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                aroj__ewfdn, imsii__dnc)
        return impl_series
    if isinstance(data, types.BaseTuple):
        hpkfg__isgfy = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        hpkfg__isgfy += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        poy__nbbfw = {}
        exec(hpkfg__isgfy, {'bcast_comm_impl': bcast_comm_impl}, poy__nbbfw)
        jlzt__pux = poy__nbbfw['impl_tuple']
        return jlzt__pux
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    fgiby__skwmi = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    cti__kpr = (0,) * fgiby__skwmi

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        iilw__nou = np.ascontiguousarray(data)
        xuwgz__bhm = data.ctypes
        qjkmb__kog = cti__kpr
        if rank == root:
            qjkmb__kog = iilw__nou.shape
        qjkmb__kog = bcast_tuple(qjkmb__kog, root)
        viokw__nlbxd = get_tuple_prod(qjkmb__kog[1:])
        send_counts = qjkmb__kog[0] * viokw__nlbxd
        wmibz__hzfq = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(xuwgz__bhm, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(wmibz__hzfq.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return wmibz__hzfq.reshape((-1,) + qjkmb__kog[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        mqhu__pmpch = MPI.COMM_WORLD
        jlbqf__htczc = MPI.Get_processor_name()
        xamz__pre = mqhu__pmpch.allgather(jlbqf__htczc)
        node_ranks = defaultdict(list)
        for i, ysww__vbz in enumerate(xamz__pre):
            node_ranks[ysww__vbz].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    mqhu__pmpch = MPI.COMM_WORLD
    jbfop__wjuch = mqhu__pmpch.Get_group()
    wpptz__qkcnj = jbfop__wjuch.Incl(comm_ranks)
    uylh__uwpkf = mqhu__pmpch.Create_group(wpptz__qkcnj)
    return uylh__uwpkf


def get_nodes_first_ranks():
    yha__twisy = get_host_ranks()
    return np.array([dlq__qit[0] for dlq__qit in yha__twisy.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
