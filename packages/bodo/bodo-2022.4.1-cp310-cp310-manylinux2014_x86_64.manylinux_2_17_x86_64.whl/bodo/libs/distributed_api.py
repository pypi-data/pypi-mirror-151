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
    spq__uvex = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, spq__uvex, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    spq__uvex = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, spq__uvex, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            spq__uvex = get_type_enum(arr)
            return _isend(arr.ctypes, size, spq__uvex, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        spq__uvex = np.int32(numba_to_c_type(arr.dtype))
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            apayt__jgoh = size + 7 >> 3
            fps__cnpmj = _isend(arr._data.ctypes, size, spq__uvex, pe, tag,
                cond)
            onho__yxaij = _isend(arr._null_bitmap.ctypes, apayt__jgoh,
                pge__mvdz, pe, tag, cond)
            return fps__cnpmj, onho__yxaij
        return impl_nullable
    if is_str_arr_type(arr) or arr == binary_array_type:
        haebn__ixs = np.int32(numba_to_c_type(offset_type))
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            ksq__mgk = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(ksq__mgk, pe, tag - 1)
            apayt__jgoh = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                haebn__ixs, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), ksq__mgk,
                pge__mvdz, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                apayt__jgoh, pge__mvdz, pe, tag)
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
            spq__uvex = get_type_enum(arr)
            return _irecv(arr.ctypes, size, spq__uvex, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, DecimalArrayType)) or arr in (
        boolean_array, datetime_date_array_type):
        spq__uvex = np.int32(numba_to_c_type(arr.dtype))
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            apayt__jgoh = size + 7 >> 3
            fps__cnpmj = _irecv(arr._data.ctypes, size, spq__uvex, pe, tag,
                cond)
            onho__yxaij = _irecv(arr._null_bitmap.ctypes, apayt__jgoh,
                pge__mvdz, pe, tag, cond)
            return fps__cnpmj, onho__yxaij
        return impl_nullable
    if arr in [binary_array_type, string_array_type]:
        haebn__ixs = np.int32(numba_to_c_type(offset_type))
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            eewf__hfvh = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            eewf__hfvh = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        djizd__meq = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {eewf__hfvh}(size, n_chars)
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
        wlx__cxzj = dict()
        exec(djizd__meq, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            haebn__ixs, 'char_typ_enum': pge__mvdz}, wlx__cxzj)
        impl = wlx__cxzj['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    spq__uvex = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), spq__uvex)


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
        lpb__rwl = n_pes if rank == root or allgather else 0
        uloa__xury = np.empty(lpb__rwl, dtype)
        c_gather_scalar(send.ctypes, uloa__xury.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return uloa__xury
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
        wgek__mxe = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], wgek__mxe)
        return builder.bitcast(wgek__mxe, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        wgek__mxe = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(wgek__mxe)
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
    iiv__pdbnv = types.unliteral(value)
    if isinstance(iiv__pdbnv, IndexValueType):
        iiv__pdbnv = iiv__pdbnv.val_typ
        ivsn__lkpa = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            ivsn__lkpa.append(types.int64)
            ivsn__lkpa.append(bodo.datetime64ns)
            ivsn__lkpa.append(bodo.timedelta64ns)
            ivsn__lkpa.append(bodo.datetime_date_type)
        if iiv__pdbnv not in ivsn__lkpa:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(iiv__pdbnv))
    typ_enum = np.int32(numba_to_c_type(iiv__pdbnv))

    def impl(value, reduce_op):
        kjv__rty = value_to_ptr(value)
        lpro__tkak = value_to_ptr(value)
        _dist_reduce(kjv__rty, lpro__tkak, reduce_op, typ_enum)
        return load_val_ptr(lpro__tkak, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    iiv__pdbnv = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(iiv__pdbnv))
    uwh__pdsp = iiv__pdbnv(0)

    def impl(value, reduce_op):
        kjv__rty = value_to_ptr(value)
        lpro__tkak = value_to_ptr(uwh__pdsp)
        _dist_exscan(kjv__rty, lpro__tkak, reduce_op, typ_enum)
        return load_val_ptr(lpro__tkak, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    wtsse__iivjs = 0
    wvkuq__zhksj = 0
    for i in range(len(recv_counts)):
        fyo__tnnnw = recv_counts[i]
        apayt__jgoh = recv_counts_nulls[i]
        hdxy__wkvr = tmp_null_bytes[wtsse__iivjs:wtsse__iivjs + apayt__jgoh]
        for qdg__ngkzt in range(fyo__tnnnw):
            set_bit_to(null_bitmap_ptr, wvkuq__zhksj, get_bit(hdxy__wkvr,
                qdg__ngkzt))
            wvkuq__zhksj += 1
        wtsse__iivjs += apayt__jgoh


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            acx__zaoz = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                acx__zaoz, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            pxck__klypx = data.size
            recv_counts = gather_scalar(np.int32(pxck__klypx), allgather,
                root=root)
            ludeg__rfoov = recv_counts.sum()
            etmsu__uyczs = empty_like_type(ludeg__rfoov, data)
            njm__cto = np.empty(1, np.int32)
            if rank == root or allgather:
                njm__cto = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(pxck__klypx), etmsu__uyczs.
                ctypes, recv_counts.ctypes, njm__cto.ctypes, np.int32(
                typ_val), allgather, np.int32(root))
            return etmsu__uyczs.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            etmsu__uyczs = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.str_arr_ext.init_str_arr(etmsu__uyczs)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            etmsu__uyczs = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.binary_arr_ext.init_binary_arr(etmsu__uyczs)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            pxck__klypx = len(data)
            apayt__jgoh = pxck__klypx + 7 >> 3
            recv_counts = gather_scalar(np.int32(pxck__klypx), allgather,
                root=root)
            ludeg__rfoov = recv_counts.sum()
            etmsu__uyczs = empty_like_type(ludeg__rfoov, data)
            njm__cto = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            zoiw__ttxc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                njm__cto = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                zoiw__ttxc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(pxck__klypx),
                etmsu__uyczs._days_data.ctypes, recv_counts.ctypes,
                njm__cto.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(pxck__klypx),
                etmsu__uyczs._seconds_data.ctypes, recv_counts.ctypes,
                njm__cto.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(pxck__klypx),
                etmsu__uyczs._microseconds_data.ctypes, recv_counts.ctypes,
                njm__cto.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(apayt__jgoh),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, zoiw__ttxc
                .ctypes, pge__mvdz, allgather, np.int32(root))
            copy_gathered_null_bytes(etmsu__uyczs._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return etmsu__uyczs
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            pxck__klypx = len(data)
            apayt__jgoh = pxck__klypx + 7 >> 3
            recv_counts = gather_scalar(np.int32(pxck__klypx), allgather,
                root=root)
            ludeg__rfoov = recv_counts.sum()
            etmsu__uyczs = empty_like_type(ludeg__rfoov, data)
            njm__cto = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            zoiw__ttxc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                njm__cto = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                zoiw__ttxc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(pxck__klypx),
                etmsu__uyczs._data.ctypes, recv_counts.ctypes, njm__cto.
                ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(apayt__jgoh),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, zoiw__ttxc
                .ctypes, pge__mvdz, allgather, np.int32(root))
            copy_gathered_null_bytes(etmsu__uyczs._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return etmsu__uyczs
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        xxsbc__kph = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            fgf__queor = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                fgf__queor, xxsbc__kph)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            qpfwm__xbr = bodo.gatherv(data._left, allgather, warn_if_rep, root)
            olwkd__xbyb = bodo.gatherv(data._right, allgather, warn_if_rep,
                root)
            return bodo.libs.interval_arr_ext.init_interval_array(qpfwm__xbr,
                olwkd__xbyb)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            gmyhv__hadz = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            kcmpp__irxg = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kcmpp__irxg, gmyhv__hadz)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        mugi__wlpe = np.iinfo(np.int64).max
        tst__hwyw = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            start = data._start
            stop = data._stop
            if len(data) == 0:
                start = mugi__wlpe
                stop = tst__hwyw
            start = bodo.libs.distributed_api.dist_reduce(start, np.int32(
                Reduce_Type.Min.value))
            stop = bodo.libs.distributed_api.dist_reduce(stop, np.int32(
                Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if start == mugi__wlpe and stop == tst__hwyw:
                start = 0
                stop = 0
            plm__vlze = max(0, -(-(stop - start) // data._step))
            if plm__vlze < total_len:
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
            csolw__ybogs = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, csolw__ybogs)
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
            etmsu__uyczs = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                etmsu__uyczs, data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        tod__xzg = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table}
        djizd__meq = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        djizd__meq += '  T = data\n'
        djizd__meq += '  T2 = init_table(T, True)\n'
        for sof__szocc in data.type_to_blk.values():
            tod__xzg[f'arr_inds_{sof__szocc}'] = np.array(data.
                block_to_arr_ind[sof__szocc], dtype=np.int64)
            djizd__meq += (
                f'  arr_list_{sof__szocc} = get_table_block(T, {sof__szocc})\n'
                )
            djizd__meq += f"""  out_arr_list_{sof__szocc} = alloc_list_like(arr_list_{sof__szocc}, True)
"""
            djizd__meq += f'  for i in range(len(arr_list_{sof__szocc})):\n'
            djizd__meq += (
                f'    arr_ind_{sof__szocc} = arr_inds_{sof__szocc}[i]\n')
            djizd__meq += f"""    ensure_column_unboxed(T, arr_list_{sof__szocc}, i, arr_ind_{sof__szocc})
"""
            djizd__meq += f"""    out_arr_{sof__szocc} = bodo.gatherv(arr_list_{sof__szocc}[i], allgather, warn_if_rep, root)
"""
            djizd__meq += (
                f'    out_arr_list_{sof__szocc}[i] = out_arr_{sof__szocc}\n')
            djizd__meq += (
                f'  T2 = set_table_block(T2, out_arr_list_{sof__szocc}, {sof__szocc})\n'
                )
        djizd__meq += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        djizd__meq += f'  T2 = set_table_len(T2, length)\n'
        djizd__meq += f'  return T2\n'
        wlx__cxzj = {}
        exec(djizd__meq, tod__xzg, wlx__cxzj)
        pzjax__fhehd = wlx__cxzj['impl_table']
        return pzjax__fhehd
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        cgaxd__ksqvx = len(data.columns)
        if cgaxd__ksqvx == 0:

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                scivo__vojcd = bodo.gatherv(index, allgather, warn_if_rep, root
                    )
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    scivo__vojcd, ())
            return impl
        twtch__ktov = ', '.join(f'g_data_{i}' for i in range(cgaxd__ksqvx))
        hbg__ylbos = bodo.utils.transform.gen_const_tup(data.columns)
        djizd__meq = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            rcpe__btx = bodo.hiframes.pd_dataframe_ext.DataFrameType(data.
                data, data.index, data.columns, Distribution.REP, True)
            tod__xzg = {'bodo': bodo, 'df_type': rcpe__btx}
            twtch__ktov = 'T2'
            hbg__ylbos = 'df_type'
            djizd__meq += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            djizd__meq += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            tod__xzg = {'bodo': bodo}
            for i in range(cgaxd__ksqvx):
                djizd__meq += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                djizd__meq += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        djizd__meq += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        djizd__meq += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        djizd__meq += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(twtch__ktov, hbg__ylbos))
        wlx__cxzj = {}
        exec(djizd__meq, tod__xzg, wlx__cxzj)
        ncne__jxqu = wlx__cxzj['impl_df']
        return ncne__jxqu
    if isinstance(data, ArrayItemArrayType):
        mwb__kyee = np.int32(numba_to_c_type(types.int32))
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            feg__uzf = bodo.libs.array_item_arr_ext.get_offsets(data)
            emy__ydm = bodo.libs.array_item_arr_ext.get_data(data)
            emy__ydm = emy__ydm[:feg__uzf[-1]]
            ypnyl__exm = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            pxck__klypx = len(data)
            kfmmr__pdwk = np.empty(pxck__klypx, np.uint32)
            apayt__jgoh = pxck__klypx + 7 >> 3
            for i in range(pxck__klypx):
                kfmmr__pdwk[i] = feg__uzf[i + 1] - feg__uzf[i]
            recv_counts = gather_scalar(np.int32(pxck__klypx), allgather,
                root=root)
            ludeg__rfoov = recv_counts.sum()
            njm__cto = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            zoiw__ttxc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                njm__cto = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for svp__kbqm in range(len(recv_counts)):
                    recv_counts_nulls[svp__kbqm] = recv_counts[svp__kbqm
                        ] + 7 >> 3
                zoiw__ttxc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            cnsk__yna = np.empty(ludeg__rfoov + 1, np.uint32)
            hbo__oiu = bodo.gatherv(emy__ydm, allgather, warn_if_rep, root)
            txy__cfhk = np.empty(ludeg__rfoov + 7 >> 3, np.uint8)
            c_gatherv(kfmmr__pdwk.ctypes, np.int32(pxck__klypx), cnsk__yna.
                ctypes, recv_counts.ctypes, njm__cto.ctypes, mwb__kyee,
                allgather, np.int32(root))
            c_gatherv(ypnyl__exm.ctypes, np.int32(apayt__jgoh),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, zoiw__ttxc
                .ctypes, pge__mvdz, allgather, np.int32(root))
            dummy_use(data)
            dsdf__qdw = np.empty(ludeg__rfoov + 1, np.uint64)
            convert_len_arr_to_offset(cnsk__yna.ctypes, dsdf__qdw.ctypes,
                ludeg__rfoov)
            copy_gathered_null_bytes(txy__cfhk.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                ludeg__rfoov, hbo__oiu, dsdf__qdw, txy__cfhk)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        mms__czro = data.names
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            ldl__orye = bodo.libs.struct_arr_ext.get_data(data)
            mbih__ykt = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            ces__tixa = bodo.gatherv(ldl__orye, allgather=allgather, root=root)
            rank = bodo.libs.distributed_api.get_rank()
            pxck__klypx = len(data)
            apayt__jgoh = pxck__klypx + 7 >> 3
            recv_counts = gather_scalar(np.int32(pxck__klypx), allgather,
                root=root)
            ludeg__rfoov = recv_counts.sum()
            zmi__ebgi = np.empty(ludeg__rfoov + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            zoiw__ttxc = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                zoiw__ttxc = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(mbih__ykt.ctypes, np.int32(apayt__jgoh),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, zoiw__ttxc
                .ctypes, pge__mvdz, allgather, np.int32(root))
            copy_gathered_null_bytes(zmi__ebgi.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(ces__tixa,
                zmi__ebgi, mms__czro)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            etmsu__uyczs = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.binary_arr_ext.init_binary_arr(etmsu__uyczs)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            etmsu__uyczs = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(etmsu__uyczs)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            etmsu__uyczs = bodo.gatherv(data._data, allgather, warn_if_rep,
                root)
            return bodo.libs.map_arr_ext.init_map_arr(etmsu__uyczs)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            etmsu__uyczs = bodo.gatherv(data.data, allgather, warn_if_rep, root
                )
            gycoh__mpkh = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            jlhjk__wqoe = bodo.gatherv(data.indptr, allgather, warn_if_rep,
                root)
            xxn__mgua = gather_scalar(data.shape[0], allgather, root=root)
            pue__eje = xxn__mgua.sum()
            cgaxd__ksqvx = bodo.libs.distributed_api.dist_reduce(data.shape
                [1], np.int32(Reduce_Type.Max.value))
            hyff__kxbka = np.empty(pue__eje + 1, np.int64)
            gycoh__mpkh = gycoh__mpkh.astype(np.int64)
            hyff__kxbka[0] = 0
            aiy__wuzx = 1
            eek__mfqe = 0
            for wkohk__rzpco in xxn__mgua:
                for gpw__pbzyj in range(wkohk__rzpco):
                    fgdp__fvrlb = jlhjk__wqoe[eek__mfqe + 1] - jlhjk__wqoe[
                        eek__mfqe]
                    hyff__kxbka[aiy__wuzx] = hyff__kxbka[aiy__wuzx - 1
                        ] + fgdp__fvrlb
                    aiy__wuzx += 1
                    eek__mfqe += 1
                eek__mfqe += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(etmsu__uyczs,
                gycoh__mpkh, hyff__kxbka, (pue__eje, cgaxd__ksqvx))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        djizd__meq = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        djizd__meq += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        wlx__cxzj = {}
        exec(djizd__meq, {'bodo': bodo}, wlx__cxzj)
        mkma__fytyl = wlx__cxzj['impl_tuple']
        return mkma__fytyl
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    djizd__meq = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    djizd__meq += '    if random:\n'
    djizd__meq += '        if random_seed is None:\n'
    djizd__meq += '            random = 1\n'
    djizd__meq += '        else:\n'
    djizd__meq += '            random = 2\n'
    djizd__meq += '    if random_seed is None:\n'
    djizd__meq += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        swm__ydm = data
        cgaxd__ksqvx = len(swm__ydm.columns)
        for i in range(cgaxd__ksqvx):
            djizd__meq += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        djizd__meq += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        twtch__ktov = ', '.join(f'data_{i}' for i in range(cgaxd__ksqvx))
        djizd__meq += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(bzjh__zne) for
            bzjh__zne in range(cgaxd__ksqvx))))
        djizd__meq += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        djizd__meq += '    if dests is None:\n'
        djizd__meq += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        djizd__meq += '    else:\n'
        djizd__meq += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for ptyqu__pmy in range(cgaxd__ksqvx):
            djizd__meq += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(ptyqu__pmy))
        djizd__meq += (
            """    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)
"""
            .format(cgaxd__ksqvx))
        djizd__meq += '    delete_table(out_table)\n'
        djizd__meq += '    if parallel:\n'
        djizd__meq += '        delete_table(table_total)\n'
        twtch__ktov = ', '.join('out_arr_{}'.format(i) for i in range(
            cgaxd__ksqvx))
        hbg__ylbos = bodo.utils.transform.gen_const_tup(swm__ydm.columns)
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        djizd__meq += (
            '    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, {})\n'
            .format(twtch__ktov, index, hbg__ylbos))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        djizd__meq += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        djizd__meq += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        djizd__meq += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        djizd__meq += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        djizd__meq += '    if dests is None:\n'
        djizd__meq += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        djizd__meq += '    else:\n'
        djizd__meq += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        djizd__meq += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        djizd__meq += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        djizd__meq += '    delete_table(out_table)\n'
        djizd__meq += '    if parallel:\n'
        djizd__meq += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        djizd__meq += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        djizd__meq += '    if not parallel:\n'
        djizd__meq += '        return data\n'
        djizd__meq += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        djizd__meq += '    if dests is None:\n'
        djizd__meq += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        djizd__meq += '    elif bodo.get_rank() not in dests:\n'
        djizd__meq += '        dim0_local_size = 0\n'
        djizd__meq += '    else:\n'
        djizd__meq += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        djizd__meq += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        djizd__meq += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        djizd__meq += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        djizd__meq += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        djizd__meq += '    if dests is None:\n'
        djizd__meq += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        djizd__meq += '    else:\n'
        djizd__meq += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        djizd__meq += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        djizd__meq += '    delete_table(out_table)\n'
        djizd__meq += '    if parallel:\n'
        djizd__meq += '        delete_table(table_total)\n'
        djizd__meq += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    wlx__cxzj = {}
    exec(djizd__meq, {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.
        array.array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}, wlx__cxzj
        )
    impl = wlx__cxzj['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, parallel=False):
    djizd__meq = 'def impl(data, seed=None, dests=None, parallel=False):\n'
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        djizd__meq += '    if seed is None:\n'
        djizd__meq += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        djizd__meq += '    np.random.seed(seed)\n'
        djizd__meq += '    if not parallel:\n'
        djizd__meq += '        data = data.copy()\n'
        djizd__meq += '        np.random.shuffle(data)\n'
        djizd__meq += '        return data\n'
        djizd__meq += '    else:\n'
        djizd__meq += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        djizd__meq += '        permutation = np.arange(dim0_global_size)\n'
        djizd__meq += '        np.random.shuffle(permutation)\n'
        djizd__meq += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        djizd__meq += """        output = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        djizd__meq += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        djizd__meq += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation))
"""
        djizd__meq += '        return output\n'
    else:
        djizd__meq += """    return bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
    wlx__cxzj = {}
    exec(djizd__meq, {'np': np, 'bodo': bodo}, wlx__cxzj)
    impl = wlx__cxzj['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    mswp__rdqx = np.empty(sendcounts_nulls.sum(), np.uint8)
    wtsse__iivjs = 0
    wvkuq__zhksj = 0
    for gfn__ennr in range(len(sendcounts)):
        fyo__tnnnw = sendcounts[gfn__ennr]
        apayt__jgoh = sendcounts_nulls[gfn__ennr]
        hdxy__wkvr = mswp__rdqx[wtsse__iivjs:wtsse__iivjs + apayt__jgoh]
        for qdg__ngkzt in range(fyo__tnnnw):
            set_bit_to_arr(hdxy__wkvr, qdg__ngkzt, get_bit_bitmap(
                null_bitmap_ptr, wvkuq__zhksj))
            wvkuq__zhksj += 1
        wtsse__iivjs += apayt__jgoh
    return mswp__rdqx


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    fbbhi__tjn = MPI.COMM_WORLD
    data = fbbhi__tjn.bcast(data, root)
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
    mhu__egcml = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    oihhz__idzrz = (0,) * mhu__egcml

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        gqfql__abwj = np.ascontiguousarray(data)
        yfljr__maf = data.ctypes
        mwrnn__tjhnv = oihhz__idzrz
        if rank == MPI_ROOT:
            mwrnn__tjhnv = gqfql__abwj.shape
        mwrnn__tjhnv = bcast_tuple(mwrnn__tjhnv)
        dzhc__wcllz = get_tuple_prod(mwrnn__tjhnv[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            mwrnn__tjhnv[0])
        send_counts *= dzhc__wcllz
        pxck__klypx = send_counts[rank]
        ubq__lakfn = np.empty(pxck__klypx, dtype)
        njm__cto = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(yfljr__maf, send_counts.ctypes, njm__cto.ctypes,
            ubq__lakfn.ctypes, np.int32(pxck__klypx), np.int32(typ_val))
        return ubq__lakfn.reshape((-1,) + mwrnn__tjhnv[1:])
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
        svszf__leo = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], svszf__leo)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        gmyhv__hadz = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=gmyhv__hadz)
        ygdvw__qkh = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(ygdvw__qkh)
        return pd.Index(arr, name=gmyhv__hadz)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        gmyhv__hadz = _get_name_value_for_type(dtype.name_typ)
        mms__czro = tuple(_get_name_value_for_type(t) for t in dtype.names_typ)
        ohbuv__qbo = tuple(get_value_for_type(t) for t in dtype.array_types)
        ohbuv__qbo = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in ohbuv__qbo)
        val = pd.MultiIndex.from_arrays(ohbuv__qbo, names=mms__czro)
        val.name = gmyhv__hadz
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        gmyhv__hadz = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=gmyhv__hadz)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        ohbuv__qbo = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({gmyhv__hadz: arr for gmyhv__hadz, arr in zip(
            dtype.columns, ohbuv__qbo)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        ygdvw__qkh = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(ygdvw__qkh[0],
            ygdvw__qkh[0])])
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
        mwb__kyee = np.int32(numba_to_c_type(types.int32))
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            eewf__hfvh = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            eewf__hfvh = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        djizd__meq = f"""def impl(
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
            recv_arr = {eewf__hfvh}(n_loc, n_loc_char)

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
        wlx__cxzj = dict()
        exec(djizd__meq, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            mwb__kyee, 'char_typ_enum': pge__mvdz, 'decode_if_dict_array':
            decode_if_dict_array}, wlx__cxzj)
        impl = wlx__cxzj['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        mwb__kyee = np.int32(numba_to_c_type(types.int32))
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            yzv__uwg = bodo.libs.array_item_arr_ext.get_offsets(data)
            pnh__wqrik = bodo.libs.array_item_arr_ext.get_data(data)
            pnh__wqrik = pnh__wqrik[:yzv__uwg[-1]]
            hwb__qwzdn = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            wmxq__yfc = bcast_scalar(len(data))
            mdd__beb = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                mdd__beb[i] = yzv__uwg[i + 1] - yzv__uwg[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                wmxq__yfc)
            njm__cto = bodo.ir.join.calc_disp(send_counts)
            fqxf__jfc = np.empty(n_pes, np.int32)
            if rank == 0:
                aoaza__igv = 0
                for i in range(n_pes):
                    wsye__satuz = 0
                    for gpw__pbzyj in range(send_counts[i]):
                        wsye__satuz += mdd__beb[aoaza__igv]
                        aoaza__igv += 1
                    fqxf__jfc[i] = wsye__satuz
            bcast(fqxf__jfc)
            umekl__qxj = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                umekl__qxj[i] = send_counts[i] + 7 >> 3
            zoiw__ttxc = bodo.ir.join.calc_disp(umekl__qxj)
            pxck__klypx = send_counts[rank]
            gqd__kfyyy = np.empty(pxck__klypx + 1, np_offset_type)
            snpm__tfoyg = bodo.libs.distributed_api.scatterv_impl(pnh__wqrik,
                fqxf__jfc)
            rmkc__vnep = pxck__klypx + 7 >> 3
            liuqr__zwiav = np.empty(rmkc__vnep, np.uint8)
            aci__xmu = np.empty(pxck__klypx, np.uint32)
            c_scatterv(mdd__beb.ctypes, send_counts.ctypes, njm__cto.ctypes,
                aci__xmu.ctypes, np.int32(pxck__klypx), mwb__kyee)
            convert_len_arr_to_offset(aci__xmu.ctypes, gqd__kfyyy.ctypes,
                pxck__klypx)
            dvr__lafo = get_scatter_null_bytes_buff(hwb__qwzdn.ctypes,
                send_counts, umekl__qxj)
            c_scatterv(dvr__lafo.ctypes, umekl__qxj.ctypes, zoiw__ttxc.
                ctypes, liuqr__zwiav.ctypes, np.int32(rmkc__vnep), pge__mvdz)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                pxck__klypx, snpm__tfoyg, gqd__kfyyy, liuqr__zwiav)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, DecimalArrayType)) or data in (
        boolean_array, datetime_date_array_type):
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            afhvw__vcb = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            afhvw__vcb = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            afhvw__vcb = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            afhvw__vcb = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            gqfql__abwj = data._data
            mbih__ykt = data._null_bitmap
            zry__xcbmx = len(gqfql__abwj)
            xfh__nulhj = _scatterv_np(gqfql__abwj, send_counts)
            wmxq__yfc = bcast_scalar(zry__xcbmx)
            ridt__qlfs = len(xfh__nulhj) + 7 >> 3
            kxc__olro = np.empty(ridt__qlfs, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                wmxq__yfc)
            umekl__qxj = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                umekl__qxj[i] = send_counts[i] + 7 >> 3
            zoiw__ttxc = bodo.ir.join.calc_disp(umekl__qxj)
            dvr__lafo = get_scatter_null_bytes_buff(mbih__ykt.ctypes,
                send_counts, umekl__qxj)
            c_scatterv(dvr__lafo.ctypes, umekl__qxj.ctypes, zoiw__ttxc.
                ctypes, kxc__olro.ctypes, np.int32(ridt__qlfs), pge__mvdz)
            return afhvw__vcb(xfh__nulhj, kxc__olro)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            xzsgr__bkd = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            rwd__xqpxq = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(xzsgr__bkd,
                rwd__xqpxq)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            nehvh__msrxt = data._step
            gmyhv__hadz = data._name
            gmyhv__hadz = bcast_scalar(gmyhv__hadz)
            start = bcast_scalar(start)
            stop = bcast_scalar(stop)
            nehvh__msrxt = bcast_scalar(nehvh__msrxt)
            ilrg__etca = bodo.libs.array_kernels.calc_nitems(start, stop,
                nehvh__msrxt)
            chunk_start = bodo.libs.distributed_api.get_start(ilrg__etca,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(ilrg__etca
                , n_pes, rank)
            mcyop__htzn = start + nehvh__msrxt * chunk_start
            lkntn__mjm = start + nehvh__msrxt * (chunk_start + chunk_count)
            lkntn__mjm = min(lkntn__mjm, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(mcyop__htzn,
                lkntn__mjm, nehvh__msrxt, gmyhv__hadz)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        csolw__ybogs = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            gqfql__abwj = data._data
            gmyhv__hadz = data._name
            gmyhv__hadz = bcast_scalar(gmyhv__hadz)
            arr = bodo.libs.distributed_api.scatterv_impl(gqfql__abwj,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                gmyhv__hadz, csolw__ybogs)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            gqfql__abwj = data._data
            gmyhv__hadz = data._name
            gmyhv__hadz = bcast_scalar(gmyhv__hadz)
            arr = bodo.libs.distributed_api.scatterv_impl(gqfql__abwj,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, gmyhv__hadz)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            etmsu__uyczs = bodo.libs.distributed_api.scatterv_impl(data.
                _data, send_counts)
            gmyhv__hadz = bcast_scalar(data._name)
            mms__czro = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(
                etmsu__uyczs, mms__czro, gmyhv__hadz)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            gmyhv__hadz = bodo.hiframes.pd_series_ext.get_series_name(data)
            xsn__iikhm = bcast_scalar(gmyhv__hadz)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            kcmpp__irxg = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kcmpp__irxg, xsn__iikhm)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        cgaxd__ksqvx = len(data.columns)
        twtch__ktov = ', '.join('g_data_{}'.format(i) for i in range(
            cgaxd__ksqvx))
        hbg__ylbos = bodo.utils.transform.gen_const_tup(data.columns)
        djizd__meq = (
            'def impl_df(data, send_counts=None, warn_if_dist=True):\n')
        for i in range(cgaxd__ksqvx):
            djizd__meq += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            djizd__meq += (
                """  g_data_{} = bodo.libs.distributed_api.scatterv_impl(data_{}, send_counts)
"""
                .format(i, i))
        djizd__meq += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        djizd__meq += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        djizd__meq += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(twtch__ktov, hbg__ylbos))
        wlx__cxzj = {}
        exec(djizd__meq, {'bodo': bodo}, wlx__cxzj)
        ncne__jxqu = wlx__cxzj['impl_df']
        return ncne__jxqu
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            acx__zaoz = bodo.libs.distributed_api.scatterv_impl(data.codes,
                send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                acx__zaoz, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        djizd__meq = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        djizd__meq += '  return ({}{})\n'.format(', '.join(
            'bodo.libs.distributed_api.scatterv_impl(data[{}], send_counts)'
            .format(i) for i in range(len(data))), ',' if len(data) > 0 else ''
            )
        wlx__cxzj = {}
        exec(djizd__meq, {'bodo': bodo}, wlx__cxzj)
        mkma__fytyl = wlx__cxzj['impl_tuple']
        return mkma__fytyl
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
        haebn__ixs = np.int32(numba_to_c_type(offset_type))
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            pxck__klypx = len(data)
            rmenx__inp = num_total_chars(data)
            assert pxck__klypx < INT_MAX
            assert rmenx__inp < INT_MAX
            wkaz__onje = get_offset_ptr(data)
            yfljr__maf = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            apayt__jgoh = pxck__klypx + 7 >> 3
            c_bcast(wkaz__onje, np.int32(pxck__klypx + 1), haebn__ixs, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(yfljr__maf, np.int32(rmenx__inp), pge__mvdz, np.array([
                -1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(apayt__jgoh), pge__mvdz, np.
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
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                ssi__ltjl = 0
                dmi__edjhg = np.empty(0, np.uint8).ctypes
            else:
                dmi__edjhg, ssi__ltjl = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            ssi__ltjl = bodo.libs.distributed_api.bcast_scalar(ssi__ltjl, root)
            if rank != root:
                eqseu__ctff = np.empty(ssi__ltjl + 1, np.uint8)
                eqseu__ctff[ssi__ltjl] = 0
                dmi__edjhg = eqseu__ctff.ctypes
            c_bcast(dmi__edjhg, np.int32(ssi__ltjl), pge__mvdz, np.array([-
                1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(dmi__edjhg, ssi__ltjl)
        return impl_str
    typ_val = numba_to_c_type(val)
    djizd__meq = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    wlx__cxzj = {}
    exec(djizd__meq, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, wlx__cxzj)
    hcnyj__qidv = wlx__cxzj['bcast_scalar_impl']
    return hcnyj__qidv


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple)
    zbs__mubgd = len(val)
    djizd__meq = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    djizd__meq += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(zbs__mubgd)),
        ',' if zbs__mubgd else '')
    wlx__cxzj = {}
    exec(djizd__meq, {'bcast_scalar': bcast_scalar}, wlx__cxzj)
    ynwxi__jfk = wlx__cxzj['bcast_tuple_impl']
    return ynwxi__jfk


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            pxck__klypx = bcast_scalar(len(arr), root)
            xer__xziq = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(pxck__klypx, xer__xziq)
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
        nehvh__msrxt = slice_index.step
        xhxfo__bev = 0 if nehvh__msrxt == 1 or start > arr_start else abs(
            nehvh__msrxt - arr_start % nehvh__msrxt) % nehvh__msrxt
        mcyop__htzn = max(arr_start, slice_index.start
            ) - arr_start + xhxfo__bev
        lkntn__mjm = max(slice_index.stop - arr_start, 0)
        return slice(mcyop__htzn, lkntn__mjm, nehvh__msrxt)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        ikb__qtmfk = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[ikb__qtmfk])
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
        wbi__gzs = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        pge__mvdz = np.int32(numba_to_c_type(types.uint8))
        ptxhk__gvs = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            glos__olv = np.int32(10)
            tag = np.int32(11)
            mggx__uuxtt = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                emy__ydm = arr._data
                cta__yvga = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    emy__ydm, ind)
                xar__cqy = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    emy__ydm, ind + 1)
                length = xar__cqy - cta__yvga
                wgek__mxe = emy__ydm[ind]
                mggx__uuxtt[0] = length
                isend(mggx__uuxtt, np.int32(1), root, glos__olv, True)
                isend(wgek__mxe, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(ptxhk__gvs
                , wbi__gzs, 0, 1)
            plm__vlze = 0
            if rank == root:
                plm__vlze = recv(np.int64, ANY_SOURCE, glos__olv)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    ptxhk__gvs, wbi__gzs, plm__vlze, 1)
                yfljr__maf = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(yfljr__maf, np.int32(plm__vlze), pge__mvdz,
                    ANY_SOURCE, tag)
            dummy_use(mggx__uuxtt)
            plm__vlze = bcast_scalar(plm__vlze)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    ptxhk__gvs, wbi__gzs, plm__vlze, 1)
            yfljr__maf = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(yfljr__maf, np.int32(plm__vlze), pge__mvdz, np.array([-
                1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, plm__vlze)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        flx__ncqa = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, flx__ncqa)
            if arr_start <= ind < arr_start + len(arr):
                acx__zaoz = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = acx__zaoz[ind - arr_start]
                send_arr = np.full(1, data, flx__ncqa)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = flx__ncqa(-1)
            if rank == root:
                val = recv(flx__ncqa, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            xsx__tgmt = arr.dtype.categories[max(val, 0)]
            return xsx__tgmt
        return cat_getitem_impl
    zwo__whhs = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, zwo__whhs)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, zwo__whhs)[0]
        if rank == root:
            val = recv(zwo__whhs, ANY_SOURCE, tag)
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
    sqkx__jko = get_type_enum(out_data)
    assert typ_enum == sqkx__jko
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
    djizd__meq = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        djizd__meq += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    djizd__meq += '  return\n'
    wlx__cxzj = {}
    exec(djizd__meq, {'alltoallv': alltoallv}, wlx__cxzj)
    zonec__kfqd = wlx__cxzj['f']
    return zonec__kfqd


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    start = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return start, count


@numba.njit
def get_start(total_size, pes, rank):
    uloa__xury = total_size % pes
    iwt__khatn = (total_size - uloa__xury) // pes
    return rank * iwt__khatn + min(rank, uloa__xury)


@numba.njit
def get_end(total_size, pes, rank):
    uloa__xury = total_size % pes
    iwt__khatn = (total_size - uloa__xury) // pes
    return (rank + 1) * iwt__khatn + min(rank + 1, uloa__xury)


@numba.njit
def get_node_portion(total_size, pes, rank):
    uloa__xury = total_size % pes
    iwt__khatn = (total_size - uloa__xury) // pes
    if rank < uloa__xury:
        return iwt__khatn + 1
    else:
        return iwt__khatn


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    uwh__pdsp = in_arr.dtype(0)
    nig__jvx = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        wsye__satuz = uwh__pdsp
        for ikwtm__gnh in np.nditer(in_arr):
            wsye__satuz += ikwtm__gnh.item()
        kcc__ydz = dist_exscan(wsye__satuz, nig__jvx)
        for i in range(in_arr.size):
            kcc__ydz += in_arr[i]
            out_arr[i] = kcc__ydz
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    rfe__tflo = in_arr.dtype(1)
    nig__jvx = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        wsye__satuz = rfe__tflo
        for ikwtm__gnh in np.nditer(in_arr):
            wsye__satuz *= ikwtm__gnh.item()
        kcc__ydz = dist_exscan(wsye__satuz, nig__jvx)
        if get_rank() == 0:
            kcc__ydz = rfe__tflo
        for i in range(in_arr.size):
            kcc__ydz *= in_arr[i]
            out_arr[i] = kcc__ydz
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        rfe__tflo = np.finfo(in_arr.dtype(1).dtype).max
    else:
        rfe__tflo = np.iinfo(in_arr.dtype(1).dtype).max
    nig__jvx = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        wsye__satuz = rfe__tflo
        for ikwtm__gnh in np.nditer(in_arr):
            wsye__satuz = min(wsye__satuz, ikwtm__gnh.item())
        kcc__ydz = dist_exscan(wsye__satuz, nig__jvx)
        if get_rank() == 0:
            kcc__ydz = rfe__tflo
        for i in range(in_arr.size):
            kcc__ydz = min(kcc__ydz, in_arr[i])
            out_arr[i] = kcc__ydz
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        rfe__tflo = np.finfo(in_arr.dtype(1).dtype).min
    else:
        rfe__tflo = np.iinfo(in_arr.dtype(1).dtype).min
    rfe__tflo = in_arr.dtype(1)
    nig__jvx = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        wsye__satuz = rfe__tflo
        for ikwtm__gnh in np.nditer(in_arr):
            wsye__satuz = max(wsye__satuz, ikwtm__gnh.item())
        kcc__ydz = dist_exscan(wsye__satuz, nig__jvx)
        if get_rank() == 0:
            kcc__ydz = rfe__tflo
        for i in range(in_arr.size):
            kcc__ydz = max(kcc__ydz, in_arr[i])
            out_arr[i] = kcc__ydz
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    spq__uvex = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), spq__uvex)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    juyzn__hdkw = args[0]
    if equiv_set.has_shape(juyzn__hdkw):
        return ArrayAnalysis.AnalyzeResult(shape=juyzn__hdkw, pre=[])
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
    kvqd__aqyks = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for
        i, aiakz__cbm in enumerate(args) if is_array_typ(aiakz__cbm) or
        isinstance(aiakz__cbm, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    djizd__meq = f"""def impl(*args):
    if {kvqd__aqyks} or bodo.get_rank() == 0:
        print(*args)"""
    wlx__cxzj = {}
    exec(djizd__meq, globals(), wlx__cxzj)
    impl = wlx__cxzj['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        eudab__pkr = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        djizd__meq = 'def f(req, cond=True):\n'
        djizd__meq += f'  return {eudab__pkr}\n'
        wlx__cxzj = {}
        exec(djizd__meq, {'_wait': _wait}, wlx__cxzj)
        impl = wlx__cxzj['f']
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
    mcyop__htzn = max(start, chunk_start)
    lkntn__mjm = min(stop, chunk_start + chunk_count)
    timi__btjh = mcyop__htzn - chunk_start
    jwfok__yimfr = lkntn__mjm - chunk_start
    if timi__btjh < 0 or jwfok__yimfr < 0:
        timi__btjh = 1
        jwfok__yimfr = 0
    return timi__btjh, jwfok__yimfr


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
        uloa__xury = 1
        for a in t:
            uloa__xury *= a
        return uloa__xury
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    aqe__nxb = np.ascontiguousarray(in_arr)
    kiblo__fmmsc = get_tuple_prod(aqe__nxb.shape[1:])
    qna__rfo = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        mxa__rbv = np.array(dest_ranks, dtype=np.int32)
    else:
        mxa__rbv = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, aqe__nxb.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * qna__rfo, dtype_size * kiblo__fmmsc, len(
        mxa__rbv), mxa__rbv.ctypes)
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
    ltgwq__keyr = np.ascontiguousarray(rhs)
    qjs__qvxab = get_tuple_prod(ltgwq__keyr.shape[1:])
    txp__egp = dtype_size * qjs__qvxab
    permutation_array_index(lhs.ctypes, lhs_len, txp__egp, ltgwq__keyr.
        ctypes, ltgwq__keyr.shape[0], p.ctypes, p_len)
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
        djizd__meq = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        wlx__cxzj = {}
        exec(djizd__meq, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, wlx__cxzj)
        hcnyj__qidv = wlx__cxzj['bcast_scalar_impl']
        return hcnyj__qidv
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        cgaxd__ksqvx = len(data.columns)
        twtch__ktov = ', '.join('g_data_{}'.format(i) for i in range(
            cgaxd__ksqvx))
        hbg__ylbos = bodo.utils.transform.gen_const_tup(data.columns)
        djizd__meq = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(cgaxd__ksqvx):
            djizd__meq += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            djizd__meq += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        djizd__meq += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        djizd__meq += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        djizd__meq += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, {})
"""
            .format(twtch__ktov, hbg__ylbos))
        wlx__cxzj = {}
        exec(djizd__meq, {'bodo': bodo}, wlx__cxzj)
        ncne__jxqu = wlx__cxzj['impl_df']
        return ncne__jxqu
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            start = data._start
            stop = data._stop
            nehvh__msrxt = data._step
            gmyhv__hadz = data._name
            gmyhv__hadz = bcast_scalar(gmyhv__hadz, root)
            start = bcast_scalar(start, root)
            stop = bcast_scalar(stop, root)
            nehvh__msrxt = bcast_scalar(nehvh__msrxt, root)
            ilrg__etca = bodo.libs.array_kernels.calc_nitems(start, stop,
                nehvh__msrxt)
            chunk_start = bodo.libs.distributed_api.get_start(ilrg__etca,
                n_pes, rank)
            chunk_count = bodo.libs.distributed_api.get_node_portion(ilrg__etca
                , n_pes, rank)
            mcyop__htzn = start + nehvh__msrxt * chunk_start
            lkntn__mjm = start + nehvh__msrxt * (chunk_start + chunk_count)
            lkntn__mjm = min(lkntn__mjm, stop)
            return bodo.hiframes.pd_index_ext.init_range_index(mcyop__htzn,
                lkntn__mjm, nehvh__msrxt, gmyhv__hadz)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            gqfql__abwj = data._data
            gmyhv__hadz = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(gqfql__abwj,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, gmyhv__hadz)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            gmyhv__hadz = bodo.hiframes.pd_series_ext.get_series_name(data)
            xsn__iikhm = bodo.libs.distributed_api.bcast_comm_impl(gmyhv__hadz,
                comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            kcmpp__irxg = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                kcmpp__irxg, xsn__iikhm)
        return impl_series
    if isinstance(data, types.BaseTuple):
        djizd__meq = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        djizd__meq += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        wlx__cxzj = {}
        exec(djizd__meq, {'bcast_comm_impl': bcast_comm_impl}, wlx__cxzj)
        mkma__fytyl = wlx__cxzj['impl_tuple']
        return mkma__fytyl
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    mhu__egcml = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    oihhz__idzrz = (0,) * mhu__egcml

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        gqfql__abwj = np.ascontiguousarray(data)
        yfljr__maf = data.ctypes
        mwrnn__tjhnv = oihhz__idzrz
        if rank == root:
            mwrnn__tjhnv = gqfql__abwj.shape
        mwrnn__tjhnv = bcast_tuple(mwrnn__tjhnv, root)
        dzhc__wcllz = get_tuple_prod(mwrnn__tjhnv[1:])
        send_counts = mwrnn__tjhnv[0] * dzhc__wcllz
        ubq__lakfn = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(yfljr__maf, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(ubq__lakfn.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return ubq__lakfn.reshape((-1,) + mwrnn__tjhnv[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        fbbhi__tjn = MPI.COMM_WORLD
        klzk__tklv = MPI.Get_processor_name()
        lfq__ncyio = fbbhi__tjn.allgather(klzk__tklv)
        node_ranks = defaultdict(list)
        for i, vusi__fntyw in enumerate(lfq__ncyio):
            node_ranks[vusi__fntyw].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    fbbhi__tjn = MPI.COMM_WORLD
    yvsc__jagdx = fbbhi__tjn.Get_group()
    ywpoo__zfha = yvsc__jagdx.Incl(comm_ranks)
    spgwh__bbu = fbbhi__tjn.Create_group(ywpoo__zfha)
    return spgwh__bbu


def get_nodes_first_ranks():
    cuxaa__vrtsq = get_host_ranks()
    return np.array([fwale__mwwqk[0] for fwale__mwwqk in cuxaa__vrtsq.
        values()], dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
