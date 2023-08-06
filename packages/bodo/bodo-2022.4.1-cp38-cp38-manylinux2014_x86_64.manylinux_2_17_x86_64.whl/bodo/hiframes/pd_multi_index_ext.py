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
        dnnh__idzz = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, dnnh__idzz)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[tevnf__vpnqq].values) for
        tevnf__vpnqq in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (jzvfs__blxl) for jzvfs__blxl in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    gwupt__jys = c.context.insert_const_string(c.builder.module, 'pandas')
    icnpi__werb = c.pyapi.import_module_noblock(gwupt__jys)
    celq__rtud = c.pyapi.object_getattr_string(icnpi__werb, 'MultiIndex')
    lfher__bnvfc = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        lfher__bnvfc.data)
    phja__kjsk = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        lfher__bnvfc.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ),
        lfher__bnvfc.names)
    bywh__gio = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        lfher__bnvfc.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, lfher__bnvfc.name)
    ouhp__mgr = c.pyapi.from_native_value(typ.name_typ, lfher__bnvfc.name,
        c.env_manager)
    lst__jhhm = c.pyapi.borrow_none()
    lbqaw__ozf = c.pyapi.call_method(celq__rtud, 'from_arrays', (phja__kjsk,
        lst__jhhm, bywh__gio))
    c.pyapi.object_setattr_string(lbqaw__ozf, 'name', ouhp__mgr)
    c.pyapi.decref(phja__kjsk)
    c.pyapi.decref(bywh__gio)
    c.pyapi.decref(ouhp__mgr)
    c.pyapi.decref(icnpi__werb)
    c.pyapi.decref(celq__rtud)
    c.context.nrt.decref(c.builder, typ, val)
    return lbqaw__ozf


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    hbjr__huc = []
    itav__vkf = []
    for tevnf__vpnqq in range(typ.nlevels):
        tveu__rzcf = c.pyapi.unserialize(c.pyapi.serialize_object(tevnf__vpnqq)
            )
        tceq__zhzuh = c.pyapi.call_method(val, 'get_level_values', (
            tveu__rzcf,))
        akfz__rxh = c.pyapi.object_getattr_string(tceq__zhzuh, 'values')
        c.pyapi.decref(tceq__zhzuh)
        c.pyapi.decref(tveu__rzcf)
        duhds__uol = c.pyapi.to_native_value(typ.array_types[tevnf__vpnqq],
            akfz__rxh).value
        hbjr__huc.append(duhds__uol)
        itav__vkf.append(akfz__rxh)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, hbjr__huc)
    else:
        data = cgutils.pack_struct(c.builder, hbjr__huc)
    bywh__gio = c.pyapi.object_getattr_string(val, 'names')
    edxg__dhbq = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    ist__ijdz = c.pyapi.call_function_objargs(edxg__dhbq, (bywh__gio,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), ist__ijdz
        ).value
    ouhp__mgr = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, ouhp__mgr).value
    lfher__bnvfc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lfher__bnvfc.data = data
    lfher__bnvfc.names = names
    lfher__bnvfc.name = name
    for akfz__rxh in itav__vkf:
        c.pyapi.decref(akfz__rxh)
    c.pyapi.decref(bywh__gio)
    c.pyapi.decref(edxg__dhbq)
    c.pyapi.decref(ist__ijdz)
    c.pyapi.decref(ouhp__mgr)
    return NativeValue(lfher__bnvfc._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    lvu__rjoh = 'pandas.MultiIndex.from_product'
    jcqf__uvzo = dict(sortorder=sortorder)
    gmqly__dhi = dict(sortorder=None)
    check_unsupported_args(lvu__rjoh, jcqf__uvzo, gmqly__dhi, package_name=
        'pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{lvu__rjoh}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{lvu__rjoh}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{lvu__rjoh}: iterables and names must be of the same length.')


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
    lmo__hywd = MultiIndexType(array_types, names_typ)
    obav__cfewz = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, obav__cfewz, lmo__hywd)
    satx__hcp = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{obav__cfewz}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    sexp__scwg = {}
    exec(satx__hcp, globals(), sexp__scwg)
    raym__eohot = sexp__scwg['impl']
    return raym__eohot


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        fqnd__ixfrl, umvg__lbotx, dyyi__ybjzl = args
        fzhp__dnv = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        fzhp__dnv.data = fqnd__ixfrl
        fzhp__dnv.names = umvg__lbotx
        fzhp__dnv.name = dyyi__ybjzl
        context.nrt.incref(builder, signature.args[0], fqnd__ixfrl)
        context.nrt.incref(builder, signature.args[1], umvg__lbotx)
        context.nrt.incref(builder, signature.args[2], dyyi__ybjzl)
        return fzhp__dnv._getvalue()
    yyuwt__wnwmw = MultiIndexType(data.types, names.types, name)
    return yyuwt__wnwmw(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        tlvf__wrqc = len(I.array_types)
        satx__hcp = 'def impl(I, ind):\n'
        satx__hcp += '  data = I._data\n'
        satx__hcp += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{tevnf__vpnqq}][ind])' for
            tevnf__vpnqq in range(tlvf__wrqc))))
        sexp__scwg = {}
        exec(satx__hcp, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, sexp__scwg)
        raym__eohot = sexp__scwg['impl']
        return raym__eohot


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    cefys__ulhl, aayx__xsoyg = sig.args
    if cefys__ulhl != aayx__xsoyg:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
