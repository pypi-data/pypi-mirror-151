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
    svl__bdac = context.get_python_api(builder)
    return svl__bdac.unserialize(svl__bdac.serialize_object(pyval))


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
        pbhe__hmuxf = ', '.join('e{}'.format(awtdr__muss) for awtdr__muss in
            range(len(args)))
        if pbhe__hmuxf:
            pbhe__hmuxf += ', '
        ozqvt__zqi = ', '.join("{} = ''".format(gmir__sdx) for gmir__sdx in
            kws.keys())
        kztoa__dkwe = f'def format_stub(string, {pbhe__hmuxf} {ozqvt__zqi}):\n'
        kztoa__dkwe += '    pass\n'
        psfi__owhhm = {}
        exec(kztoa__dkwe, {}, psfi__owhhm)
        ncl__bmor = psfi__owhhm['format_stub']
        nyxdl__mmrji = numba.core.utils.pysignature(ncl__bmor)
        diyof__xrklt = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, diyof__xrklt).replace(pysig=nyxdl__mmrji)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for eojp__qld in ('logging.Logger', 'logging.RootLogger'):
        for sqxih__woul in func_names:
            gwykk__lgldc = f'@bound_function("{eojp__qld}.{sqxih__woul}")\n'
            gwykk__lgldc += (
                f'def resolve_{sqxih__woul}(self, logger_typ, args, kws):\n')
            gwykk__lgldc += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(gwykk__lgldc)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for pncwx__omqit in logging_logger_unsupported_attrs:
        sbtod__zlj = 'logging.Logger.' + pncwx__omqit
        overload_attribute(LoggingLoggerType, pncwx__omqit)(
            create_unsupported_overload(sbtod__zlj))
    for lsg__axmsq in logging_logger_unsupported_methods:
        sbtod__zlj = 'logging.Logger.' + lsg__axmsq
        overload_method(LoggingLoggerType, lsg__axmsq)(
            create_unsupported_overload(sbtod__zlj))


_install_logging_logger_unsupported_objects()
