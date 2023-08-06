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
        evk__avnp = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, evk__avnp)


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
        evnr__bdln, yafu__juedy, kysh__svh, wnag__zaj = args
        ftwcy__hto = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        ftwcy__hto.data = evnr__bdln
        ftwcy__hto.indices = yafu__juedy
        ftwcy__hto.indptr = kysh__svh
        ftwcy__hto.shape = wnag__zaj
        context.nrt.incref(builder, signature.args[0], evnr__bdln)
        context.nrt.incref(builder, signature.args[1], yafu__juedy)
        context.nrt.incref(builder, signature.args[2], kysh__svh)
        return ftwcy__hto._getvalue()
    xyq__nyzm = CSRMatrixType(data_t.dtype, indices_t.dtype)
    jcznm__sar = xyq__nyzm(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return jcznm__sar, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    ftwcy__hto = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ywkdy__ofxlb = c.pyapi.object_getattr_string(val, 'data')
    tcfh__ihavp = c.pyapi.object_getattr_string(val, 'indices')
    yjx__nkbo = c.pyapi.object_getattr_string(val, 'indptr')
    akg__fzid = c.pyapi.object_getattr_string(val, 'shape')
    ftwcy__hto.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'
        ), ywkdy__ofxlb).value
    ftwcy__hto.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), tcfh__ihavp).value
    ftwcy__hto.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), yjx__nkbo).value
    ftwcy__hto.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 
        2), akg__fzid).value
    c.pyapi.decref(ywkdy__ofxlb)
    c.pyapi.decref(tcfh__ihavp)
    c.pyapi.decref(yjx__nkbo)
    c.pyapi.decref(akg__fzid)
    mtrf__iui = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ftwcy__hto._getvalue(), is_error=mtrf__iui)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    ixaib__pskv = c.context.insert_const_string(c.builder.module,
        'scipy.sparse')
    ocyi__pot = c.pyapi.import_module_noblock(ixaib__pskv)
    ftwcy__hto = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        ftwcy__hto.data)
    ywkdy__ofxlb = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        ftwcy__hto.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        ftwcy__hto.indices)
    tcfh__ihavp = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), ftwcy__hto.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        ftwcy__hto.indptr)
    yjx__nkbo = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), ftwcy__hto.indptr, c.env_manager)
    akg__fzid = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        ftwcy__hto.shape, c.env_manager)
    cecgu__wvrus = c.pyapi.tuple_pack([ywkdy__ofxlb, tcfh__ihavp, yjx__nkbo])
    kzqy__ulos = c.pyapi.call_method(ocyi__pot, 'csr_matrix', (cecgu__wvrus,
        akg__fzid))
    c.pyapi.decref(cecgu__wvrus)
    c.pyapi.decref(ywkdy__ofxlb)
    c.pyapi.decref(tcfh__ihavp)
    c.pyapi.decref(yjx__nkbo)
    c.pyapi.decref(akg__fzid)
    c.pyapi.decref(ocyi__pot)
    c.context.nrt.decref(c.builder, typ, val)
    return kzqy__ulos


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
    eixs__ufknb = A.dtype
    uoksp__dqgvc = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            dyt__tjayd, xbzi__hlp = A.shape
            pyhln__gjdq = numba.cpython.unicode._normalize_slice(idx[0],
                dyt__tjayd)
            rwflg__yoi = numba.cpython.unicode._normalize_slice(idx[1],
                xbzi__hlp)
            if pyhln__gjdq.step != 1 or rwflg__yoi.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            xaqdt__yrepe = pyhln__gjdq.start
            iax__roa = pyhln__gjdq.stop
            yqrb__wsyq = rwflg__yoi.start
            ecm__yjxl = rwflg__yoi.stop
            kmry__wqfb = A.indptr
            mpjni__wnj = A.indices
            sxf__bsyro = A.data
            adyne__pcu = iax__roa - xaqdt__yrepe
            rlpb__dfnm = ecm__yjxl - yqrb__wsyq
            ndvts__hayr = 0
            abr__nhjj = 0
            for mbq__cqw in range(adyne__pcu):
                onrjx__ztnwz = kmry__wqfb[xaqdt__yrepe + mbq__cqw]
                yzm__lbw = kmry__wqfb[xaqdt__yrepe + mbq__cqw + 1]
                for zpok__ryo in range(onrjx__ztnwz, yzm__lbw):
                    if mpjni__wnj[zpok__ryo] >= yqrb__wsyq and mpjni__wnj[
                        zpok__ryo] < ecm__yjxl:
                        ndvts__hayr += 1
            efk__mytnd = np.empty(adyne__pcu + 1, uoksp__dqgvc)
            lwohl__qyz = np.empty(ndvts__hayr, uoksp__dqgvc)
            ectjk__ajvgj = np.empty(ndvts__hayr, eixs__ufknb)
            efk__mytnd[0] = 0
            for mbq__cqw in range(adyne__pcu):
                onrjx__ztnwz = kmry__wqfb[xaqdt__yrepe + mbq__cqw]
                yzm__lbw = kmry__wqfb[xaqdt__yrepe + mbq__cqw + 1]
                for zpok__ryo in range(onrjx__ztnwz, yzm__lbw):
                    if mpjni__wnj[zpok__ryo] >= yqrb__wsyq and mpjni__wnj[
                        zpok__ryo] < ecm__yjxl:
                        lwohl__qyz[abr__nhjj] = mpjni__wnj[zpok__ryo
                            ] - yqrb__wsyq
                        ectjk__ajvgj[abr__nhjj] = sxf__bsyro[zpok__ryo]
                        abr__nhjj += 1
                efk__mytnd[mbq__cqw + 1] = abr__nhjj
            return init_csr_matrix(ectjk__ajvgj, lwohl__qyz, efk__mytnd, (
                adyne__pcu, rlpb__dfnm))
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
