"""Support distributed deep learning with Horovod
"""
import time
import numba
import numpy as np
from mpi4py import MPI
import bodo
from bodo.libs.distributed_api import create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks
dl_status = None


def assert_dl_initialized():
    assert dl_status is not None, 'Horovod has not been initialized. Call bodo.dl.start() first'


class DLStatus(object):

    def __init__(self, framework, gpu_ranks):
        self.framework = framework
        self.gpu_ranks = gpu_ranks


def get_num_gpus(framework):
    if framework == 'torch':
        import torch
        return torch.cuda.device_count()
    elif framework == 'tensorflow':
        import tensorflow as tf
        return len(tf.config.experimental.list_physical_devices('GPU'))
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))


def get_gpu_ranks(framework):
    dpcv__wcm = MPI.COMM_WORLD
    seb__zlg = dpcv__wcm.Get_rank()
    gwrnm__ptbd = get_host_ranks()
    tuc__dhznx = get_nodes_first_ranks()
    if seb__zlg in tuc__dhznx:
        try:
            cqid__ntslq = get_num_gpus(framework)
        except Exception as lvkmp__psptd:
            cqid__ntslq = lvkmp__psptd
        muyt__gtu = create_subcomm_mpi4py(tuc__dhznx)
        beao__itgy = muyt__gtu.gather(cqid__ntslq)
        if seb__zlg == 0:
            gpu_ranks = []
            ilxr__cmm = None
            for hbogd__kmw, ueu__iqng in enumerate(gwrnm__ptbd.values()):
                eias__xpani = beao__itgy[hbogd__kmw]
                if isinstance(eias__xpani, Exception):
                    ilxr__cmm = eias__xpani
                    break
                if eias__xpani == 0:
                    continue
                diw__qyi = len(ueu__iqng) // eias__xpani
                for rwb__qvws, xpfz__bln in enumerate(ueu__iqng):
                    if rwb__qvws % diw__qyi == 0:
                        kejjp__ofdfc = rwb__qvws / diw__qyi
                        if kejjp__ofdfc < eias__xpani:
                            gpu_ranks.append(xpfz__bln)
            if ilxr__cmm:
                dpcv__wcm.bcast(ilxr__cmm)
                raise ilxr__cmm
            else:
                dpcv__wcm.bcast(gpu_ranks)
    if seb__zlg != 0:
        gpu_ranks = dpcv__wcm.bcast(None)
        if isinstance(gpu_ranks, Exception):
            lvkmp__psptd = gpu_ranks
            raise lvkmp__psptd
    return gpu_ranks


def is_cuda_available():
    assert_dl_initialized()
    return len(dl_status.gpu_ranks) > 0


def initialize_horovod(framework):
    global dl_status
    if dl_status is not None:
        assert dl_status.framework == framework, 'Attempted to initialize Horovod with different DL frameworks'
        return np.array(dl_status.gpu_ranks, dtype=np.int32)
    gpu_ranks = get_gpu_ranks(framework)
    if framework == 'torch':
        import horovod.torch as hvd
        import torch
        torch.set_num_threads(1)
    elif framework == 'tensorflow':
        import horovod.tensorflow as hvd
        import tensorflow as tf
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))
    bop__mvanb = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        muyt__gtu = MPI.COMM_WORLD.Split(color=0 if bop__mvanb in gpu_ranks
             else MPI.UNDEFINED, key=bop__mvanb)
        if muyt__gtu != MPI.COMM_NULL:
            hvd.init(comm=muyt__gtu)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                rxdk__oxy = tf.config.experimental.list_physical_devices('GPU')
                for syhp__cur in rxdk__oxy:
                    tf.config.experimental.set_memory_growth(syhp__cur, True)
                tf.config.experimental.set_visible_devices(rxdk__oxy[hvd.
                    local_rank()], 'GPU')
    else:
        if bop__mvanb == 0:
            print('[BODO-DL]: No GPUs found in cluster. Using CPUs')
        hvd.init()
    dl_status = DLStatus(framework, np.array(gpu_ranks, dtype=np.int32))


@numba.njit
def start(framework):
    with numba.objmode:
        initialize_horovod(framework)


@numba.njit
def end():
    with numba.objmode:
        end_py()


def end_py():
    if is_cuda_available():
        gowme__jyd = 17
        dpcv__wcm = MPI.COMM_WORLD
        nqng__weyc = MPI.Get_processor_name()
        vgyoj__xwl = get_host_ranks()[nqng__weyc]
        assert_dl_initialized()
        if bodo.get_rank() == vgyoj__xwl[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for seb__zlg in vgyoj__xwl[1:]:
                dpcv__wcm.isend(1, dest=seb__zlg, tag=gowme__jyd)
        else:
            while True:
                ubt__eggg = MPI.Status()
                wui__abm = dpcv__wcm.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    ubt__eggg)
                if wui__abm:
                    assert ubt__eggg.source == vgyoj__xwl[0]
                    assert ubt__eggg.tag == gowme__jyd
                    dpcv__wcm.recv(source=0, tag=gowme__jyd)
                    break
                time.sleep(1.0)
    else:
        bodo.barrier()


def _prepare_data_get_gpu_ranks():
    assert_dl_initialized()
    return dl_status.gpu_ranks


@numba.njit
def prepare_data(data):
    with numba.objmode(gpu_ranks='int32[:]'):
        gpu_ranks = _prepare_data_get_gpu_ranks()
    if len(gpu_ranks) > 0:
        data = bodo.rebalance(data, dests=list(gpu_ranks), parallel=True)
    else:
        data = bodo.rebalance(data, parallel=True)
    return data
