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
        gucw__iupsq = state
        yvomd__sfdxh = inspect.getsourcelines(gucw__iupsq)[0][0]
        assert yvomd__sfdxh.startswith('@bodo.jit') or yvomd__sfdxh.startswith(
            '@jit')
        rpwvb__xyexi = eval(yvomd__sfdxh[1:])
        self.dispatcher = rpwvb__xyexi(gucw__iupsq)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    llvf__wcno = MPI.COMM_WORLD
    while True:
        sgd__pag = llvf__wcno.bcast(None, root=MASTER_RANK)
        if sgd__pag[0] == 'exec':
            gucw__iupsq = pickle.loads(sgd__pag[1])
            for szhu__ewrna, qblwj__dbcq in list(gucw__iupsq.__globals__.
                items()):
                if isinstance(qblwj__dbcq, MasterModeDispatcher):
                    gucw__iupsq.__globals__[szhu__ewrna
                        ] = qblwj__dbcq.dispatcher
            if gucw__iupsq.__module__ not in sys.modules:
                sys.modules[gucw__iupsq.__module__] = pytypes.ModuleType(
                    gucw__iupsq.__module__)
            yvomd__sfdxh = inspect.getsourcelines(gucw__iupsq)[0][0]
            assert yvomd__sfdxh.startswith('@bodo.jit'
                ) or yvomd__sfdxh.startswith('@jit')
            rpwvb__xyexi = eval(yvomd__sfdxh[1:])
            func = rpwvb__xyexi(gucw__iupsq)
            wbyo__pemne = sgd__pag[2]
            ihb__suowi = sgd__pag[3]
            joka__dasa = []
            for yqerr__wmu in wbyo__pemne:
                if yqerr__wmu == 'scatter':
                    joka__dasa.append(bodo.scatterv(None))
                elif yqerr__wmu == 'bcast':
                    joka__dasa.append(llvf__wcno.bcast(None, root=MASTER_RANK))
            wgut__mas = {}
            for argname, yqerr__wmu in ihb__suowi.items():
                if yqerr__wmu == 'scatter':
                    wgut__mas[argname] = bodo.scatterv(None)
                elif yqerr__wmu == 'bcast':
                    wgut__mas[argname] = llvf__wcno.bcast(None, root=
                        MASTER_RANK)
            xrgye__qyg = func(*joka__dasa, **wgut__mas)
            if xrgye__qyg is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(xrgye__qyg)
            del (sgd__pag, gucw__iupsq, func, rpwvb__xyexi, wbyo__pemne,
                ihb__suowi, joka__dasa, wgut__mas, xrgye__qyg)
            gc.collect()
        elif sgd__pag[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    llvf__wcno = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        wbyo__pemne = ['scatter' for fsibz__vzwk in range(len(args))]
        ihb__suowi = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        iea__yty = func.py_func.__code__.co_varnames
        ngdgn__rpul = func.targetoptions

        def get_distribution(argname):
            if argname in ngdgn__rpul.get('distributed', []
                ) or argname in ngdgn__rpul.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        wbyo__pemne = [get_distribution(argname) for argname in iea__yty[:
            len(args)]]
        ihb__suowi = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    rwjsu__kdysh = pickle.dumps(func.py_func)
    llvf__wcno.bcast(['exec', rwjsu__kdysh, wbyo__pemne, ihb__suowi])
    joka__dasa = []
    for egkgt__oayg, yqerr__wmu in zip(args, wbyo__pemne):
        if yqerr__wmu == 'scatter':
            joka__dasa.append(bodo.scatterv(egkgt__oayg))
        elif yqerr__wmu == 'bcast':
            llvf__wcno.bcast(egkgt__oayg)
            joka__dasa.append(egkgt__oayg)
    wgut__mas = {}
    for argname, egkgt__oayg in kwargs.items():
        yqerr__wmu = ihb__suowi[argname]
        if yqerr__wmu == 'scatter':
            wgut__mas[argname] = bodo.scatterv(egkgt__oayg)
        elif yqerr__wmu == 'bcast':
            llvf__wcno.bcast(egkgt__oayg)
            wgut__mas[argname] = egkgt__oayg
    goe__paral = []
    for szhu__ewrna, qblwj__dbcq in list(func.py_func.__globals__.items()):
        if isinstance(qblwj__dbcq, MasterModeDispatcher):
            goe__paral.append((func.py_func.__globals__, szhu__ewrna, func.
                py_func.__globals__[szhu__ewrna]))
            func.py_func.__globals__[szhu__ewrna] = qblwj__dbcq.dispatcher
    xrgye__qyg = func(*joka__dasa, **wgut__mas)
    for tpju__tni, szhu__ewrna, qblwj__dbcq in goe__paral:
        tpju__tni[szhu__ewrna] = qblwj__dbcq
    if xrgye__qyg is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        xrgye__qyg = bodo.gatherv(xrgye__qyg)
    return xrgye__qyg


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
