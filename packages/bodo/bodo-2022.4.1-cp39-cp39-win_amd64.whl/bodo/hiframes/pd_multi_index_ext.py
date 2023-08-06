"""Support for MultiIndex type of Pandas
"""
import operator
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from bodo.utils.conversion import ensure_contig_if_np
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_val_type_maybe_str_literal, is_overload_none


class MultiIndexType(types.Type):

    def __init__(self, array_types, names_typ=None, name_typ=None):
        names_typ = (types.none,) * len(array_types
            ) if names_typ is None else names_typ
        name_typ = types.none if name_typ is None else name_typ
        self.array_types = array_types
        self.names_typ = names_typ
        self.name_typ = name_typ
        super(MultiIndexType, self).__init__(name=
            'MultiIndexType({}, {}, {})'.format(array_types, names_typ,
            name_typ))
    ndim = 1

    def copy(self):
        return MultiIndexType(self.array_types, self.names_typ, self.name_typ)

    @property
    def nlevels(self):
        return len(self.array_types)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(MultiIndexType)
class MultiIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        tude__dskeq = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, tude__dskeq)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[siir__vajid].values) for
        siir__vajid in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (wit__llo) for wit__llo in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    njd__maa = c.context.insert_const_string(c.builder.module, 'pandas')
    devk__lhq = c.pyapi.import_module_noblock(njd__maa)
    pio__vjzf = c.pyapi.object_getattr_string(devk__lhq, 'MultiIndex')
    huwrd__skwlm = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        huwrd__skwlm.data)
    cdd__pih = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        huwrd__skwlm.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ),
        huwrd__skwlm.names)
    grwv__irj = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        huwrd__skwlm.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, huwrd__skwlm.name)
    bje__jmv = c.pyapi.from_native_value(typ.name_typ, huwrd__skwlm.name, c
        .env_manager)
    tvyvb__wpj = c.pyapi.borrow_none()
    zoti__kgk = c.pyapi.call_method(pio__vjzf, 'from_arrays', (cdd__pih,
        tvyvb__wpj, grwv__irj))
    c.pyapi.object_setattr_string(zoti__kgk, 'name', bje__jmv)
    c.pyapi.decref(cdd__pih)
    c.pyapi.decref(grwv__irj)
    c.pyapi.decref(bje__jmv)
    c.pyapi.decref(devk__lhq)
    c.pyapi.decref(pio__vjzf)
    c.context.nrt.decref(c.builder, typ, val)
    return zoti__kgk


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    mtrsv__wyc = []
    imgue__yeand = []
    for siir__vajid in range(typ.nlevels):
        dfk__vvxbu = c.pyapi.unserialize(c.pyapi.serialize_object(siir__vajid))
        bkwpp__cqfd = c.pyapi.call_method(val, 'get_level_values', (
            dfk__vvxbu,))
        aoh__kjtju = c.pyapi.object_getattr_string(bkwpp__cqfd, 'values')
        c.pyapi.decref(bkwpp__cqfd)
        c.pyapi.decref(dfk__vvxbu)
        ndt__mxl = c.pyapi.to_native_value(typ.array_types[siir__vajid],
            aoh__kjtju).value
        mtrsv__wyc.append(ndt__mxl)
        imgue__yeand.append(aoh__kjtju)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, mtrsv__wyc)
    else:
        data = cgutils.pack_struct(c.builder, mtrsv__wyc)
    grwv__irj = c.pyapi.object_getattr_string(val, 'names')
    yas__srlf = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    djtrn__tubk = c.pyapi.call_function_objargs(yas__srlf, (grwv__irj,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), djtrn__tubk
        ).value
    bje__jmv = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, bje__jmv).value
    huwrd__skwlm = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    huwrd__skwlm.data = data
    huwrd__skwlm.names = names
    huwrd__skwlm.name = name
    for aoh__kjtju in imgue__yeand:
        c.pyapi.decref(aoh__kjtju)
    c.pyapi.decref(grwv__irj)
    c.pyapi.decref(yas__srlf)
    c.pyapi.decref(djtrn__tubk)
    c.pyapi.decref(bje__jmv)
    return NativeValue(huwrd__skwlm._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    peuxi__mzgbv = 'pandas.MultiIndex.from_product'
    jofy__qjx = dict(sortorder=sortorder)
    iao__dptn = dict(sortorder=None)
    check_unsupported_args(peuxi__mzgbv, jofy__qjx, iao__dptn, package_name
        ='pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{peuxi__mzgbv}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{peuxi__mzgbv}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{peuxi__mzgbv}: iterables and names must be of the same length.')


def from_product(iterable, sortorder=None, names=None):
    pass


@overload(from_product)
def from_product_overload(iterables, sortorder=None, names=None):
    from_product_error_checking(iterables, sortorder, names)
    array_types = tuple(dtype_to_array_type(iterable.dtype) for iterable in
        iterables)
    if is_overload_none(names):
        names_typ = tuple([types.none] * len(iterables))
    else:
        names_typ = names.types
    tmot__fvk = MultiIndexType(array_types, names_typ)
    sfbl__qkv = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, sfbl__qkv, tmot__fvk)
    zxaw__ymh = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{sfbl__qkv}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    pqh__xmpzh = {}
    exec(zxaw__ymh, globals(), pqh__xmpzh)
    yktbf__iqi = pqh__xmpzh['impl']
    return yktbf__iqi


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        jqp__umi, gncz__lxezh, jms__kwpn = args
        xfnjb__bhg = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        xfnjb__bhg.data = jqp__umi
        xfnjb__bhg.names = gncz__lxezh
        xfnjb__bhg.name = jms__kwpn
        context.nrt.incref(builder, signature.args[0], jqp__umi)
        context.nrt.incref(builder, signature.args[1], gncz__lxezh)
        context.nrt.incref(builder, signature.args[2], jms__kwpn)
        return xfnjb__bhg._getvalue()
    ptico__gnivj = MultiIndexType(data.types, names.types, name)
    return ptico__gnivj(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        wpfwf__tns = len(I.array_types)
        zxaw__ymh = 'def impl(I, ind):\n'
        zxaw__ymh += '  data = I._data\n'
        zxaw__ymh += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{siir__vajid}][ind])' for
            siir__vajid in range(wpfwf__tns))))
        pqh__xmpzh = {}
        exec(zxaw__ymh, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, pqh__xmpzh)
        yktbf__iqi = pqh__xmpzh['impl']
        return yktbf__iqi


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    qlks__sqsvy, dflbf__qvejc = sig.args
    if qlks__sqsvy != dflbf__qvejc:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
