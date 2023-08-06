import gc
import inspect
import sys
import types as pytypes
import bodo
master_mode_on = False
MASTER_RANK = 0


class MasterModeDispatcher(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, *args, **kwargs):
        assert bodo.get_rank() == MASTER_RANK
        return master_wrapper(self.dispatcher, *args, **kwargs)

    def __getstate__(self):
        assert bodo.get_rank() == MASTER_RANK
        return self.dispatcher.py_func

    def __setstate__(self, state):
        assert bodo.get_rank() != MASTER_RANK
        ntwup__kog = state
        har__ydzx = inspect.getsourcelines(ntwup__kog)[0][0]
        assert har__ydzx.startswith('@bodo.jit') or har__ydzx.startswith('@jit'
            )
        jdwf__rurul = eval(har__ydzx[1:])
        self.dispatcher = jdwf__rurul(ntwup__kog)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    ocwmg__xxong = MPI.COMM_WORLD
    while True:
        vxpy__yznt = ocwmg__xxong.bcast(None, root=MASTER_RANK)
        if vxpy__yznt[0] == 'exec':
            ntwup__kog = pickle.loads(vxpy__yznt[1])
            for phm__wmi, twgin__ctgqs in list(ntwup__kog.__globals__.items()):
                if isinstance(twgin__ctgqs, MasterModeDispatcher):
                    ntwup__kog.__globals__[phm__wmi] = twgin__ctgqs.dispatcher
            if ntwup__kog.__module__ not in sys.modules:
                sys.modules[ntwup__kog.__module__] = pytypes.ModuleType(
                    ntwup__kog.__module__)
            har__ydzx = inspect.getsourcelines(ntwup__kog)[0][0]
            assert har__ydzx.startswith('@bodo.jit') or har__ydzx.startswith(
                '@jit')
            jdwf__rurul = eval(har__ydzx[1:])
            func = jdwf__rurul(ntwup__kog)
            qlv__prj = vxpy__yznt[2]
            jqfrw__lkcup = vxpy__yznt[3]
            lqzvw__awx = []
            for nmdse__gzbif in qlv__prj:
                if nmdse__gzbif == 'scatter':
                    lqzvw__awx.append(bodo.scatterv(None))
                elif nmdse__gzbif == 'bcast':
                    lqzvw__awx.append(ocwmg__xxong.bcast(None, root=
                        MASTER_RANK))
            saqo__srva = {}
            for argname, nmdse__gzbif in jqfrw__lkcup.items():
                if nmdse__gzbif == 'scatter':
                    saqo__srva[argname] = bodo.scatterv(None)
                elif nmdse__gzbif == 'bcast':
                    saqo__srva[argname] = ocwmg__xxong.bcast(None, root=
                        MASTER_RANK)
            spvd__zdtr = func(*lqzvw__awx, **saqo__srva)
            if spvd__zdtr is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(spvd__zdtr)
            del (vxpy__yznt, ntwup__kog, func, jdwf__rurul, qlv__prj,
                jqfrw__lkcup, lqzvw__awx, saqo__srva, spvd__zdtr)
            gc.collect()
        elif vxpy__yznt[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    ocwmg__xxong = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        qlv__prj = ['scatter' for daq__fem in range(len(args))]
        jqfrw__lkcup = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        zpp__zdz = func.py_func.__code__.co_varnames
        amg__kes = func.targetoptions

        def get_distribution(argname):
            if argname in amg__kes.get('distributed', []
                ) or argname in amg__kes.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        qlv__prj = [get_distribution(argname) for argname in zpp__zdz[:len(
            args)]]
        jqfrw__lkcup = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    ryw__nsaa = pickle.dumps(func.py_func)
    ocwmg__xxong.bcast(['exec', ryw__nsaa, qlv__prj, jqfrw__lkcup])
    lqzvw__awx = []
    for nijgo__gaohj, nmdse__gzbif in zip(args, qlv__prj):
        if nmdse__gzbif == 'scatter':
            lqzvw__awx.append(bodo.scatterv(nijgo__gaohj))
        elif nmdse__gzbif == 'bcast':
            ocwmg__xxong.bcast(nijgo__gaohj)
            lqzvw__awx.append(nijgo__gaohj)
    saqo__srva = {}
    for argname, nijgo__gaohj in kwargs.items():
        nmdse__gzbif = jqfrw__lkcup[argname]
        if nmdse__gzbif == 'scatter':
            saqo__srva[argname] = bodo.scatterv(nijgo__gaohj)
        elif nmdse__gzbif == 'bcast':
            ocwmg__xxong.bcast(nijgo__gaohj)
            saqo__srva[argname] = nijgo__gaohj
    alb__ucaqd = []
    for phm__wmi, twgin__ctgqs in list(func.py_func.__globals__.items()):
        if isinstance(twgin__ctgqs, MasterModeDispatcher):
            alb__ucaqd.append((func.py_func.__globals__, phm__wmi, func.
                py_func.__globals__[phm__wmi]))
            func.py_func.__globals__[phm__wmi] = twgin__ctgqs.dispatcher
    spvd__zdtr = func(*lqzvw__awx, **saqo__srva)
    for alx__clx, phm__wmi, twgin__ctgqs in alb__ucaqd:
        alx__clx[phm__wmi] = twgin__ctgqs
    if spvd__zdtr is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        spvd__zdtr = bodo.gatherv(spvd__zdtr)
    return spvd__zdtr


def init_master_mode():
    if bodo.get_size() == 1:
        return
    global master_mode_on
    assert master_mode_on is False, 'init_master_mode can only be called once on each process'
    master_mode_on = True
    assert sys.version_info[:2] >= (3, 8
        ), 'Python 3.8+ required for master mode'
    from bodo import jit
    globals()['jit'] = jit
    import cloudpickle
    from mpi4py import MPI
    globals()['pickle'] = cloudpickle
    globals()['MPI'] = MPI

    def master_exit():
        MPI.COMM_WORLD.bcast(['exit'])
    if bodo.get_rank() == MASTER_RANK:
        import atexit
        atexit.register(master_exit)
    else:
        worker_loop()
