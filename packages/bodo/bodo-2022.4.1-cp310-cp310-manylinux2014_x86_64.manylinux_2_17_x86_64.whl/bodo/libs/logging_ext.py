"""
JIT support for Python's logging module
"""
import logging
import numba
from numba.core import types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import bound_function
from numba.core.typing.templates import AttributeTemplate, infer_getattr, signature
from numba.extending import NativeValue, box, models, overload_attribute, overload_method, register_model, typeof_impl, unbox
from bodo.utils.typing import create_unsupported_overload, gen_objmode_attr_overload


class LoggingLoggerType(types.Type):

    def __init__(self, is_root=False):
        self.is_root = is_root
        super(LoggingLoggerType, self).__init__(name=
            f'LoggingLoggerType(is_root={is_root})')


@typeof_impl.register(logging.RootLogger)
@typeof_impl.register(logging.Logger)
def typeof_logging(val, c):
    if isinstance(val, logging.RootLogger):
        return LoggingLoggerType(is_root=True)
    else:
        return LoggingLoggerType(is_root=False)


register_model(LoggingLoggerType)(models.OpaqueModel)


@box(LoggingLoggerType)
def box_logging_logger(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(LoggingLoggerType)
def unbox_logging_logger(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@lower_constant(LoggingLoggerType)
def lower_constant_logger(context, builder, ty, pyval):
    jkj__otek = context.get_python_api(builder)
    return jkj__otek.unserialize(jkj__otek.serialize_object(pyval))


gen_objmode_attr_overload(LoggingLoggerType, 'level', None, types.int64)
gen_objmode_attr_overload(LoggingLoggerType, 'name', None, 'unicode_type')
gen_objmode_attr_overload(LoggingLoggerType, 'propagate', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'disabled', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'parent', None,
    LoggingLoggerType())
gen_objmode_attr_overload(LoggingLoggerType, 'root', None,
    LoggingLoggerType(is_root=True))


@infer_getattr
class LoggingLoggerAttribute(AttributeTemplate):
    key = LoggingLoggerType

    def _resolve_helper(self, logger_typ, args, kws):
        kws = dict(kws)
        vyd__ofr = ', '.join('e{}'.format(iexb__vgza) for iexb__vgza in
            range(len(args)))
        if vyd__ofr:
            vyd__ofr += ', '
        ozei__enino = ', '.join("{} = ''".format(fttqg__hfxse) for
            fttqg__hfxse in kws.keys())
        dlswr__zbij = f'def format_stub(string, {vyd__ofr} {ozei__enino}):\n'
        dlswr__zbij += '    pass\n'
        agw__mftu = {}
        exec(dlswr__zbij, {}, agw__mftu)
        fsut__pft = agw__mftu['format_stub']
        tdvyh__gvjut = numba.core.utils.pysignature(fsut__pft)
        umvok__quzo = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, umvok__quzo).replace(pysig=tdvyh__gvjut)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for chm__hqmki in ('logging.Logger', 'logging.RootLogger'):
        for oqm__yrhl in func_names:
            lzwwu__ugcqz = f'@bound_function("{chm__hqmki}.{oqm__yrhl}")\n'
            lzwwu__ugcqz += (
                f'def resolve_{oqm__yrhl}(self, logger_typ, args, kws):\n')
            lzwwu__ugcqz += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(lzwwu__ugcqz)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for lrgbo__vnn in logging_logger_unsupported_attrs:
        rijr__dfmwp = 'logging.Logger.' + lrgbo__vnn
        overload_attribute(LoggingLoggerType, lrgbo__vnn)(
            create_unsupported_overload(rijr__dfmwp))
    for nlzer__noxli in logging_logger_unsupported_methods:
        rijr__dfmwp = 'logging.Logger.' + nlzer__noxli
        overload_method(LoggingLoggerType, nlzer__noxli)(
            create_unsupported_overload(rijr__dfmwp))


_install_logging_logger_unsupported_objects()
