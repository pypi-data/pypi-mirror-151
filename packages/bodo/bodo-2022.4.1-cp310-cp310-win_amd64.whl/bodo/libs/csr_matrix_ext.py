"""CSR Matrix data type implementation for scipy.sparse.csr_matrix
"""
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.utils.typing import BodoError


class CSRMatrixType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, dtype, idx_dtype):
        self.dtype = dtype
        self.idx_dtype = idx_dtype
        super(CSRMatrixType, self).__init__(name=
            f'CSRMatrixType({dtype}, {idx_dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    def copy(self):
        return CSRMatrixType(self.dtype, self.idx_dtype)


@register_model(CSRMatrixType)
class CSRMatrixModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        azy__aqje = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, azy__aqje)


make_attribute_wrapper(CSRMatrixType, 'data', 'data')
make_attribute_wrapper(CSRMatrixType, 'indices', 'indices')
make_attribute_wrapper(CSRMatrixType, 'indptr', 'indptr')
make_attribute_wrapper(CSRMatrixType, 'shape', 'shape')


@intrinsic
def init_csr_matrix(typingctx, data_t, indices_t, indptr_t, shape_t=None):
    assert isinstance(data_t, types.Array)
    assert isinstance(indices_t, types.Array) and isinstance(indices_t.
        dtype, types.Integer)
    assert indices_t == indptr_t

    def codegen(context, builder, signature, args):
        hjg__wgvn, vrek__xet, bgoir__vbpfv, fit__ujis = args
        nbh__ijtts = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        nbh__ijtts.data = hjg__wgvn
        nbh__ijtts.indices = vrek__xet
        nbh__ijtts.indptr = bgoir__vbpfv
        nbh__ijtts.shape = fit__ujis
        context.nrt.incref(builder, signature.args[0], hjg__wgvn)
        context.nrt.incref(builder, signature.args[1], vrek__xet)
        context.nrt.incref(builder, signature.args[2], bgoir__vbpfv)
        return nbh__ijtts._getvalue()
    xjrt__wrcu = CSRMatrixType(data_t.dtype, indices_t.dtype)
    zdee__rtxvn = xjrt__wrcu(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return zdee__rtxvn, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    nbh__ijtts = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    gcu__aft = c.pyapi.object_getattr_string(val, 'data')
    tjg__jmkd = c.pyapi.object_getattr_string(val, 'indices')
    tist__dqcvp = c.pyapi.object_getattr_string(val, 'indptr')
    uckc__yazlo = c.pyapi.object_getattr_string(val, 'shape')
    nbh__ijtts.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'
        ), gcu__aft).value
    nbh__ijtts.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), tjg__jmkd).value
    nbh__ijtts.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), tist__dqcvp).value
    nbh__ijtts.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 
        2), uckc__yazlo).value
    c.pyapi.decref(gcu__aft)
    c.pyapi.decref(tjg__jmkd)
    c.pyapi.decref(tist__dqcvp)
    c.pyapi.decref(uckc__yazlo)
    weg__lrfdj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nbh__ijtts._getvalue(), is_error=weg__lrfdj)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    cwish__hkb = c.context.insert_const_string(c.builder.module, 'scipy.sparse'
        )
    qchxp__jmq = c.pyapi.import_module_noblock(cwish__hkb)
    nbh__ijtts = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        nbh__ijtts.data)
    gcu__aft = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        nbh__ijtts.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        nbh__ijtts.indices)
    tjg__jmkd = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), nbh__ijtts.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        nbh__ijtts.indptr)
    tist__dqcvp = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), nbh__ijtts.indptr, c.env_manager)
    uckc__yazlo = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        nbh__ijtts.shape, c.env_manager)
    bttu__dfsjw = c.pyapi.tuple_pack([gcu__aft, tjg__jmkd, tist__dqcvp])
    mynmx__sglh = c.pyapi.call_method(qchxp__jmq, 'csr_matrix', (
        bttu__dfsjw, uckc__yazlo))
    c.pyapi.decref(bttu__dfsjw)
    c.pyapi.decref(gcu__aft)
    c.pyapi.decref(tjg__jmkd)
    c.pyapi.decref(tist__dqcvp)
    c.pyapi.decref(uckc__yazlo)
    c.pyapi.decref(qchxp__jmq)
    c.context.nrt.decref(c.builder, typ, val)
    return mynmx__sglh


@overload(len, no_unliteral=True)
def overload_csr_matrix_len(A):
    if isinstance(A, CSRMatrixType):
        return lambda A: A.shape[0]


@overload_attribute(CSRMatrixType, 'ndim')
def overload_csr_matrix_ndim(A):
    return lambda A: 2


@overload_method(CSRMatrixType, 'copy', no_unliteral=True)
def overload_csr_matrix_copy(A):

    def copy_impl(A):
        return init_csr_matrix(A.data.copy(), A.indices.copy(), A.indptr.
            copy(), A.shape)
    return copy_impl


@overload(operator.getitem, no_unliteral=True)
def csr_matrix_getitem(A, idx):
    if not isinstance(A, CSRMatrixType):
        return
    ftqa__otbdg = A.dtype
    garpd__djbw = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            bbw__ravs, awxhi__cge = A.shape
            pxpb__eulcj = numba.cpython.unicode._normalize_slice(idx[0],
                bbw__ravs)
            vbpc__mmzef = numba.cpython.unicode._normalize_slice(idx[1],
                awxhi__cge)
            if pxpb__eulcj.step != 1 or vbpc__mmzef.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            sjr__tbl = pxpb__eulcj.start
            crim__vwr = pxpb__eulcj.stop
            oko__vyru = vbpc__mmzef.start
            oiwb__ijne = vbpc__mmzef.stop
            wyqoj__cjy = A.indptr
            piky__pjn = A.indices
            nqm__vfdno = A.data
            nrjmp__hheh = crim__vwr - sjr__tbl
            ckyzz__togq = oiwb__ijne - oko__vyru
            senp__cikdz = 0
            uryeq__ggj = 0
            for asxht__ikehg in range(nrjmp__hheh):
                haa__jus = wyqoj__cjy[sjr__tbl + asxht__ikehg]
                wxmms__iyk = wyqoj__cjy[sjr__tbl + asxht__ikehg + 1]
                for doeb__jljs in range(haa__jus, wxmms__iyk):
                    if piky__pjn[doeb__jljs] >= oko__vyru and piky__pjn[
                        doeb__jljs] < oiwb__ijne:
                        senp__cikdz += 1
            omfk__yileg = np.empty(nrjmp__hheh + 1, garpd__djbw)
            kqkc__rugn = np.empty(senp__cikdz, garpd__djbw)
            gyz__gxu = np.empty(senp__cikdz, ftqa__otbdg)
            omfk__yileg[0] = 0
            for asxht__ikehg in range(nrjmp__hheh):
                haa__jus = wyqoj__cjy[sjr__tbl + asxht__ikehg]
                wxmms__iyk = wyqoj__cjy[sjr__tbl + asxht__ikehg + 1]
                for doeb__jljs in range(haa__jus, wxmms__iyk):
                    if piky__pjn[doeb__jljs] >= oko__vyru and piky__pjn[
                        doeb__jljs] < oiwb__ijne:
                        kqkc__rugn[uryeq__ggj] = piky__pjn[doeb__jljs
                            ] - oko__vyru
                        gyz__gxu[uryeq__ggj] = nqm__vfdno[doeb__jljs]
                        uryeq__ggj += 1
                omfk__yileg[asxht__ikehg + 1] = uryeq__ggj
            return init_csr_matrix(gyz__gxu, kqkc__rugn, omfk__yileg, (
                nrjmp__hheh, ckyzz__togq))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
