"""
Analysis and transformation for HDF5 support.
"""
import types as pytypes
import numba
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, find_callname, find_const, get_definition, guard, replace_arg_nodes, require
import bodo
import bodo.io
from bodo.utils.transform import get_const_value_inner


class H5_IO:

    def __init__(self, func_ir, _locals, flags, arg_types):
        self.func_ir = func_ir
        self.locals = _locals
        self.flags = flags
        self.arg_types = arg_types

    def handle_possible_h5_read(self, assign, lhs, rhs):
        bsq__fed = self._get_h5_type(lhs, rhs)
        if bsq__fed is not None:
            cptr__vderu = str(bsq__fed.dtype)
            euem__uprcn = 'def _h5_read_impl(dset, index):\n'
            euem__uprcn += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(bsq__fed.ndim, cptr__vderu))
            fhi__uysp = {}
            exec(euem__uprcn, {}, fhi__uysp)
            fsl__cbykk = fhi__uysp['_h5_read_impl']
            pdftz__bwb = compile_to_numba_ir(fsl__cbykk, {'bodo': bodo}
                ).blocks.popitem()[1]
            rlk__btc = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(pdftz__bwb, [rhs.value, rlk__btc])
            slof__cqr = pdftz__bwb.body[:-3]
            slof__cqr[-1].target = assign.target
            return slof__cqr
        return None

    def _get_h5_type(self, lhs, rhs):
        bsq__fed = self._get_h5_type_locals(lhs)
        if bsq__fed is not None:
            return bsq__fed
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        rlk__btc = rhs.index if rhs.op == 'getitem' else rhs.index_var
        fzp__hhuw = guard(find_const, self.func_ir, rlk__btc)
        require(not isinstance(fzp__hhuw, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            jznv__txmt = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            ubbfo__nioib = get_const_value_inner(self.func_ir, jznv__txmt,
                arg_types=self.arg_types)
            obj_name_list.append(ubbfo__nioib)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        nroy__xht = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        zha__yct = h5py.File(nroy__xht, 'r')
        spo__eewqa = zha__yct
        for ubbfo__nioib in obj_name_list:
            spo__eewqa = spo__eewqa[ubbfo__nioib]
        require(isinstance(spo__eewqa, h5py.Dataset))
        ddfat__adr = len(spo__eewqa.shape)
        vzrxn__ciz = numba.np.numpy_support.from_dtype(spo__eewqa.dtype)
        zha__yct.close()
        return types.Array(vzrxn__ciz, ddfat__adr, 'C')

    def _get_h5_type_locals(self, varname):
        qreuu__kgljv = self.locals.pop(varname, None)
        if qreuu__kgljv is None and varname is not None:
            qreuu__kgljv = self.flags.h5_types.get(varname, None)
        return qreuu__kgljv
