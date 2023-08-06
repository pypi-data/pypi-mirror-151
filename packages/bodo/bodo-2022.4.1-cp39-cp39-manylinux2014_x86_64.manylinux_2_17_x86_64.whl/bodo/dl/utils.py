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
    arq__tuw = MPI.COMM_WORLD
    biaw__qsnqt = arq__tuw.Get_rank()
    wkqe__ymilh = get_host_ranks()
    tqr__fcz = get_nodes_first_ranks()
    if biaw__qsnqt in tqr__fcz:
        try:
            vhze__zemmm = get_num_gpus(framework)
        except Exception as cxul__ddumu:
            vhze__zemmm = cxul__ddumu
        uioyu__nuc = create_subcomm_mpi4py(tqr__fcz)
        pasy__kaboe = uioyu__nuc.gather(vhze__zemmm)
        if biaw__qsnqt == 0:
            gpu_ranks = []
            lkb__xux = None
            for xzqw__wphp, ijnz__fgak in enumerate(wkqe__ymilh.values()):
                geaqg__jqgn = pasy__kaboe[xzqw__wphp]
                if isinstance(geaqg__jqgn, Exception):
                    lkb__xux = geaqg__jqgn
                    break
                if geaqg__jqgn == 0:
                    continue
                pyub__idg = len(ijnz__fgak) // geaqg__jqgn
                for tfd__wbvz, ndrq__ixu in enumerate(ijnz__fgak):
                    if tfd__wbvz % pyub__idg == 0:
                        jftj__rnlb = tfd__wbvz / pyub__idg
                        if jftj__rnlb < geaqg__jqgn:
                            gpu_ranks.append(ndrq__ixu)
            if lkb__xux:
                arq__tuw.bcast(lkb__xux)
                raise lkb__xux
            else:
                arq__tuw.bcast(gpu_ranks)
    if biaw__qsnqt != 0:
        gpu_ranks = arq__tuw.bcast(None)
        if isinstance(gpu_ranks, Exception):
            cxul__ddumu = gpu_ranks
            raise cxul__ddumu
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
    dcf__pkkye = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        uioyu__nuc = MPI.COMM_WORLD.Split(color=0 if dcf__pkkye in
            gpu_ranks else MPI.UNDEFINED, key=dcf__pkkye)
        if uioyu__nuc != MPI.COMM_NULL:
            hvd.init(comm=uioyu__nuc)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                rmnlf__mzbuw = tf.config.experimental.list_physical_devices(
                    'GPU')
                for uixh__lke in rmnlf__mzbuw:
                    tf.config.experimental.set_memory_growth(uixh__lke, True)
                tf.config.experimental.set_visible_devices(rmnlf__mzbuw[hvd
                    .local_rank()], 'GPU')
    else:
        if dcf__pkkye == 0:
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
        ise__fiz = 17
        arq__tuw = MPI.COMM_WORLD
        rvon__ikg = MPI.Get_processor_name()
        puiw__gvvyy = get_host_ranks()[rvon__ikg]
        assert_dl_initialized()
        if bodo.get_rank() == puiw__gvvyy[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for biaw__qsnqt in puiw__gvvyy[1:]:
                arq__tuw.isend(1, dest=biaw__qsnqt, tag=ise__fiz)
        else:
            while True:
                iww__vnwnf = MPI.Status()
                gkpgd__xkpol = arq__tuw.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    iww__vnwnf)
                if gkpgd__xkpol:
                    assert iww__vnwnf.source == puiw__gvvyy[0]
                    assert iww__vnwnf.tag == ise__fiz
                    arq__tuw.recv(source=0, tag=ise__fiz)
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
