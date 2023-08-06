"""
Wrapper class for Tuples that supports tracking null entries.
This is primarily used for maintaining null information for
Series values used in df.apply
"""
import operator
import numba
from numba.core import cgutils, types
from numba.extending import box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model


class NullableTupleType(types.IterableType):

    def __init__(self, tuple_typ, null_typ):
        self._tuple_typ = tuple_typ
        self._null_typ = null_typ
        super(NullableTupleType, self).__init__(name=
            f'NullableTupleType({tuple_typ}, {null_typ})')

    @property
    def tuple_typ(self):
        return self._tuple_typ

    @property
    def null_typ(self):
        return self._null_typ

    def __getitem__(self, i):
        return self._tuple_typ[i]

    @property
    def key(self):
        return self._tuple_typ

    @property
    def dtype(self):
        return self.tuple_typ.dtype

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def iterator_type(self):
        return self.tuple_typ.iterator_type

    def __len__(self):
        return len(self.tuple_typ)


@register_model(NullableTupleType)
class NullableTupleModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nija__dckuy = [('data', fe_type.tuple_typ), ('null_values', fe_type
            .null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, nija__dckuy)


make_attribute_wrapper(NullableTupleType, 'data', '_data')
make_attribute_wrapper(NullableTupleType, 'null_values', '_null_values')


@intrinsic
def build_nullable_tuple(typingctx, data_tuple, null_values):
    assert isinstance(data_tuple, types.BaseTuple
        ), "build_nullable_tuple 'data_tuple' argument must be a tuple"
    assert isinstance(null_values, types.BaseTuple
        ), "build_nullable_tuple 'null_values' argument must be a tuple"
    data_tuple = types.unliteral(data_tuple)
    null_values = types.unliteral(null_values)

    def codegen(context, builder, signature, args):
        data_tuple, null_values = args
        rwtq__cobtn = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        rwtq__cobtn.data = data_tuple
        rwtq__cobtn.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return rwtq__cobtn._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    ftvv__jjyyu = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, ftvv__jjyyu.data)
    c.context.nrt.incref(c.builder, typ.null_typ, ftvv__jjyyu.null_values)
    cqq__kcjqq = c.pyapi.from_native_value(typ.tuple_typ, ftvv__jjyyu.data,
        c.env_manager)
    jvedo__hyliz = c.pyapi.from_native_value(typ.null_typ, ftvv__jjyyu.
        null_values, c.env_manager)
    rpiks__nwtdh = c.context.get_constant(types.int64, len(typ.tuple_typ))
    lfga__pejpz = c.pyapi.list_new(rpiks__nwtdh)
    with cgutils.for_range(c.builder, rpiks__nwtdh) as unlo__tae:
        i = unlo__tae.index
        otd__pdke = c.pyapi.long_from_longlong(i)
        humd__wsft = c.pyapi.object_getitem(jvedo__hyliz, otd__pdke)
        uuaqy__qoiw = c.pyapi.to_native_value(types.bool_, humd__wsft).value
        with c.builder.if_else(uuaqy__qoiw) as (wtcur__otr, cyho__goplg):
            with wtcur__otr:
                c.pyapi.list_setitem(lfga__pejpz, i, c.pyapi.make_none())
            with cyho__goplg:
                ifvc__kur = c.pyapi.object_getitem(cqq__kcjqq, otd__pdke)
                c.pyapi.list_setitem(lfga__pejpz, i, ifvc__kur)
        c.pyapi.decref(otd__pdke)
        c.pyapi.decref(humd__wsft)
    vlyqp__nystm = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    pzh__zcdb = c.pyapi.call_function_objargs(vlyqp__nystm, (lfga__pejpz,))
    c.pyapi.decref(cqq__kcjqq)
    c.pyapi.decref(jvedo__hyliz)
    c.pyapi.decref(vlyqp__nystm)
    c.pyapi.decref(lfga__pejpz)
    c.context.nrt.decref(c.builder, typ, val)
    return pzh__zcdb


@overload(operator.getitem)
def overload_getitem(A, idx):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A, idx: A._data[idx]


@overload(len)
def overload_len(A):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A: len(A._data)


@lower_builtin('getiter', NullableTupleType)
def nullable_tuple_getiter(context, builder, sig, args):
    rwtq__cobtn = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (rwtq__cobtn.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    edk__hmo = 'def impl(val1, val2):\n'
    edk__hmo += '    data_tup1 = val1._data\n'
    edk__hmo += '    null_tup1 = val1._null_values\n'
    edk__hmo += '    data_tup2 = val2._data\n'
    edk__hmo += '    null_tup2 = val2._null_values\n'
    edbm__dgci = val1._tuple_typ
    for i in range(len(edbm__dgci)):
        edk__hmo += f'    null1_{i} = null_tup1[{i}]\n'
        edk__hmo += f'    null2_{i} = null_tup2[{i}]\n'
        edk__hmo += f'    data1_{i} = data_tup1[{i}]\n'
        edk__hmo += f'    data2_{i} = data_tup2[{i}]\n'
        edk__hmo += f'    if null1_{i} != null2_{i}:\n'
        edk__hmo += '        return False\n'
        edk__hmo += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        edk__hmo += f'        return False\n'
    edk__hmo += f'    return True\n'
    xhom__nyf = {}
    exec(edk__hmo, {}, xhom__nyf)
    impl = xhom__nyf['impl']
    return impl


@overload_method(NullableTupleType, '__hash__')
def nullable_tuple_hash(val):

    def impl(val):
        return _nullable_tuple_hash(val)
    return impl


_PyHASH_XXPRIME_1 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_2 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_5 = numba.cpython.hashing._PyHASH_XXPRIME_1


@numba.generated_jit(nopython=True)
def _nullable_tuple_hash(nullable_tup):
    edk__hmo = 'def impl(nullable_tup):\n'
    edk__hmo += '    data_tup = nullable_tup._data\n'
    edk__hmo += '    null_tup = nullable_tup._null_values\n'
    edk__hmo += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    edk__hmo += '    acc = _PyHASH_XXPRIME_5\n'
    edbm__dgci = nullable_tup._tuple_typ
    for i in range(len(edbm__dgci)):
        edk__hmo += f'    null_val_{i} = null_tup[{i}]\n'
        edk__hmo += f'    null_lane_{i} = hash(null_val_{i})\n'
        edk__hmo += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        edk__hmo += '        return -1\n'
        edk__hmo += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        edk__hmo += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        edk__hmo += '    acc *= _PyHASH_XXPRIME_1\n'
        edk__hmo += f'    if not null_val_{i}:\n'
        edk__hmo += f'        lane_{i} = hash(data_tup[{i}])\n'
        edk__hmo += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        edk__hmo += f'            return -1\n'
        edk__hmo += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        edk__hmo += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        edk__hmo += '        acc *= _PyHASH_XXPRIME_1\n'
    edk__hmo += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    edk__hmo += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    edk__hmo += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    edk__hmo += '    return numba.cpython.hashing.process_return(acc)\n'
    xhom__nyf = {}
    exec(edk__hmo, {'numba': numba, '_PyHASH_XXPRIME_1': _PyHASH_XXPRIME_1,
        '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2, '_PyHASH_XXPRIME_5':
        _PyHASH_XXPRIME_5}, xhom__nyf)
    impl = xhom__nyf['impl']
    return impl
