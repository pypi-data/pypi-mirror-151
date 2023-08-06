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
        zdiyy__apy = self._get_h5_type(lhs, rhs)
        if zdiyy__apy is not None:
            ypzdv__rrus = str(zdiyy__apy.dtype)
            zxlha__jhcl = 'def _h5_read_impl(dset, index):\n'
            zxlha__jhcl += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(zdiyy__apy.ndim, ypzdv__rrus))
            fftvt__jwd = {}
            exec(zxlha__jhcl, {}, fftvt__jwd)
            rqio__yif = fftvt__jwd['_h5_read_impl']
            eucl__flt = compile_to_numba_ir(rqio__yif, {'bodo': bodo}
                ).blocks.popitem()[1]
            uavj__qqkd = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(eucl__flt, [rhs.value, uavj__qqkd])
            sfjp__pfvl = eucl__flt.body[:-3]
            sfjp__pfvl[-1].target = assign.target
            return sfjp__pfvl
        return None

    def _get_h5_type(self, lhs, rhs):
        zdiyy__apy = self._get_h5_type_locals(lhs)
        if zdiyy__apy is not None:
            return zdiyy__apy
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        uavj__qqkd = rhs.index if rhs.op == 'getitem' else rhs.index_var
        hmz__wkn = guard(find_const, self.func_ir, uavj__qqkd)
        require(not isinstance(hmz__wkn, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            ktc__ugxtm = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            hkd__oxcxa = get_const_value_inner(self.func_ir, ktc__ugxtm,
                arg_types=self.arg_types)
            obj_name_list.append(hkd__oxcxa)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        rkta__bkbr = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        awyf__qllr = h5py.File(rkta__bkbr, 'r')
        fhvyx__zxah = awyf__qllr
        for hkd__oxcxa in obj_name_list:
            fhvyx__zxah = fhvyx__zxah[hkd__oxcxa]
        require(isinstance(fhvyx__zxah, h5py.Dataset))
        bxij__tdbmz = len(fhvyx__zxah.shape)
        lll__qlyy = numba.np.numpy_support.from_dtype(fhvyx__zxah.dtype)
        awyf__qllr.close()
        return types.Array(lll__qlyy, bxij__tdbmz, 'C')

    def _get_h5_type_locals(self, varname):
        vnyed__ctz = self.locals.pop(varname, None)
        if vnyed__ctz is None and varname is not None:
            vnyed__ctz = self.flags.h5_types.get(varname, None)
        return vnyed__ctz
