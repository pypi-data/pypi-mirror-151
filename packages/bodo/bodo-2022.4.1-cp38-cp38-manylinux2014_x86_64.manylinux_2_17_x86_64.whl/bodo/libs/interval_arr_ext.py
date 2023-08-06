"""
Array of intervals corresponding to IntervalArray of Pandas.
Used for IntervalIndex, which is necessary for Series.value_counts() with 'bins'
argument.
"""
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo


class IntervalType(types.Type):

    def __init__(self):
        super(IntervalType, self).__init__('IntervalType()')


class IntervalArrayType(types.ArrayCompatible):

    def __init__(self, arr_type):
        self.arr_type = arr_type
        self.dtype = IntervalType()
        super(IntervalArrayType, self).__init__(name=
            f'IntervalArrayType({arr_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntervalArrayType(self.arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(IntervalArrayType)
class IntervalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        phiv__okr = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, phiv__okr)


make_attribute_wrapper(IntervalArrayType, 'left', '_left')
make_attribute_wrapper(IntervalArrayType, 'right', '_right')


@typeof_impl.register(pd.arrays.IntervalArray)
def typeof_interval_array(val, c):
    arr_type = bodo.typeof(val._left)
    return IntervalArrayType(arr_type)


@intrinsic
def init_interval_array(typingctx, left, right=None):
    assert left == right, 'Interval left/right array types should be the same'

    def codegen(context, builder, signature, args):
        zwtj__mvrk, pqzu__rinps = args
        qezsx__vby = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        qezsx__vby.left = zwtj__mvrk
        qezsx__vby.right = pqzu__rinps
        context.nrt.incref(builder, signature.args[0], zwtj__mvrk)
        context.nrt.incref(builder, signature.args[1], pqzu__rinps)
        return qezsx__vby._getvalue()
    eni__wmwxb = IntervalArrayType(left)
    yenj__fps = eni__wmwxb(left, right)
    return yenj__fps, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    egl__nztmq = []
    for tsjb__uwr in args:
        jlg__lpgl = equiv_set.get_shape(tsjb__uwr)
        if jlg__lpgl is not None:
            egl__nztmq.append(jlg__lpgl[0])
    if len(egl__nztmq) > 1:
        equiv_set.insert_equiv(*egl__nztmq)
    left = args[0]
    if equiv_set.has_shape(left):
        return ArrayAnalysis.AnalyzeResult(shape=left, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_interval_arr_ext_init_interval_array
    ) = init_interval_array_equiv


def alias_ext_init_interval_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_interval_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_interval_array


@box(IntervalArrayType)
def box_interval_arr(typ, val, c):
    qezsx__vby = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, qezsx__vby.left)
    vsgb__rnwk = c.pyapi.from_native_value(typ.arr_type, qezsx__vby.left, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, qezsx__vby.right)
    oxvfo__eleh = c.pyapi.from_native_value(typ.arr_type, qezsx__vby.right,
        c.env_manager)
    fyiha__jcje = c.context.insert_const_string(c.builder.module, 'pandas')
    zzo__hcc = c.pyapi.import_module_noblock(fyiha__jcje)
    zkz__smpit = c.pyapi.object_getattr_string(zzo__hcc, 'arrays')
    weqmp__clod = c.pyapi.object_getattr_string(zkz__smpit, 'IntervalArray')
    gsuzd__uala = c.pyapi.call_method(weqmp__clod, 'from_arrays', (
        vsgb__rnwk, oxvfo__eleh))
    c.pyapi.decref(vsgb__rnwk)
    c.pyapi.decref(oxvfo__eleh)
    c.pyapi.decref(zzo__hcc)
    c.pyapi.decref(zkz__smpit)
    c.pyapi.decref(weqmp__clod)
    c.context.nrt.decref(c.builder, typ, val)
    return gsuzd__uala


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    vsgb__rnwk = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, vsgb__rnwk).value
    c.pyapi.decref(vsgb__rnwk)
    oxvfo__eleh = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, oxvfo__eleh).value
    c.pyapi.decref(oxvfo__eleh)
    qezsx__vby = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    qezsx__vby.left = left
    qezsx__vby.right = right
    tfg__crrn = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qezsx__vby._getvalue(), is_error=tfg__crrn)


@overload(len, no_unliteral=True)
def overload_interval_arr_len(A):
    if isinstance(A, IntervalArrayType):
        return lambda A: len(A._left)


@overload_attribute(IntervalArrayType, 'shape')
def overload_interval_arr_shape(A):
    return lambda A: (len(A._left),)


@overload_attribute(IntervalArrayType, 'ndim')
def overload_interval_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntervalArrayType, 'nbytes')
def overload_interval_arr_nbytes(A):
    return lambda A: A._left.nbytes + A._right.nbytes


@overload_method(IntervalArrayType, 'copy', no_unliteral=True)
def overload_interval_arr_copy(A):
    return lambda A: bodo.libs.interval_arr_ext.init_interval_array(A._left
        .copy(), A._right.copy())
