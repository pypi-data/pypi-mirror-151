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
        oqvd__uxtz = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, oqvd__uxtz)


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
        fkdvp__jeseh = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        fkdvp__jeseh.data = data_tuple
        fkdvp__jeseh.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return fkdvp__jeseh._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    gwan__spn = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, gwan__spn.data)
    c.context.nrt.incref(c.builder, typ.null_typ, gwan__spn.null_values)
    nsuz__vojj = c.pyapi.from_native_value(typ.tuple_typ, gwan__spn.data, c
        .env_manager)
    hpdv__aswh = c.pyapi.from_native_value(typ.null_typ, gwan__spn.
        null_values, c.env_manager)
    iktrf__spzd = c.context.get_constant(types.int64, len(typ.tuple_typ))
    dofs__lfg = c.pyapi.list_new(iktrf__spzd)
    with cgutils.for_range(c.builder, iktrf__spzd) as btif__pdqq:
        i = btif__pdqq.index
        xoh__xslb = c.pyapi.long_from_longlong(i)
        psm__tder = c.pyapi.object_getitem(hpdv__aswh, xoh__xslb)
        aspor__axrk = c.pyapi.to_native_value(types.bool_, psm__tder).value
        with c.builder.if_else(aspor__axrk) as (ooaso__omn, zssli__oohjq):
            with ooaso__omn:
                c.pyapi.list_setitem(dofs__lfg, i, c.pyapi.make_none())
            with zssli__oohjq:
                fvhl__bbhdj = c.pyapi.object_getitem(nsuz__vojj, xoh__xslb)
                c.pyapi.list_setitem(dofs__lfg, i, fvhl__bbhdj)
        c.pyapi.decref(xoh__xslb)
        c.pyapi.decref(psm__tder)
    yoyj__tuyvl = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    paa__hcyo = c.pyapi.call_function_objargs(yoyj__tuyvl, (dofs__lfg,))
    c.pyapi.decref(nsuz__vojj)
    c.pyapi.decref(hpdv__aswh)
    c.pyapi.decref(yoyj__tuyvl)
    c.pyapi.decref(dofs__lfg)
    c.context.nrt.decref(c.builder, typ, val)
    return paa__hcyo


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
    fkdvp__jeseh = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (fkdvp__jeseh.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    ptrnv__stuw = 'def impl(val1, val2):\n'
    ptrnv__stuw += '    data_tup1 = val1._data\n'
    ptrnv__stuw += '    null_tup1 = val1._null_values\n'
    ptrnv__stuw += '    data_tup2 = val2._data\n'
    ptrnv__stuw += '    null_tup2 = val2._null_values\n'
    olu__ybi = val1._tuple_typ
    for i in range(len(olu__ybi)):
        ptrnv__stuw += f'    null1_{i} = null_tup1[{i}]\n'
        ptrnv__stuw += f'    null2_{i} = null_tup2[{i}]\n'
        ptrnv__stuw += f'    data1_{i} = data_tup1[{i}]\n'
        ptrnv__stuw += f'    data2_{i} = data_tup2[{i}]\n'
        ptrnv__stuw += f'    if null1_{i} != null2_{i}:\n'
        ptrnv__stuw += '        return False\n'
        ptrnv__stuw += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        ptrnv__stuw += f'        return False\n'
    ptrnv__stuw += f'    return True\n'
    buakp__vjp = {}
    exec(ptrnv__stuw, {}, buakp__vjp)
    impl = buakp__vjp['impl']
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
    ptrnv__stuw = 'def impl(nullable_tup):\n'
    ptrnv__stuw += '    data_tup = nullable_tup._data\n'
    ptrnv__stuw += '    null_tup = nullable_tup._null_values\n'
    ptrnv__stuw += (
        '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n')
    ptrnv__stuw += '    acc = _PyHASH_XXPRIME_5\n'
    olu__ybi = nullable_tup._tuple_typ
    for i in range(len(olu__ybi)):
        ptrnv__stuw += f'    null_val_{i} = null_tup[{i}]\n'
        ptrnv__stuw += f'    null_lane_{i} = hash(null_val_{i})\n'
        ptrnv__stuw += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        ptrnv__stuw += '        return -1\n'
        ptrnv__stuw += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        ptrnv__stuw += (
            '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        ptrnv__stuw += '    acc *= _PyHASH_XXPRIME_1\n'
        ptrnv__stuw += f'    if not null_val_{i}:\n'
        ptrnv__stuw += f'        lane_{i} = hash(data_tup[{i}])\n'
        ptrnv__stuw += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        ptrnv__stuw += f'            return -1\n'
        ptrnv__stuw += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        ptrnv__stuw += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        ptrnv__stuw += '        acc *= _PyHASH_XXPRIME_1\n'
    ptrnv__stuw += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    ptrnv__stuw += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    ptrnv__stuw += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    ptrnv__stuw += '    return numba.cpython.hashing.process_return(acc)\n'
    buakp__vjp = {}
    exec(ptrnv__stuw, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, buakp__vjp)
    impl = buakp__vjp['impl']
    return impl
