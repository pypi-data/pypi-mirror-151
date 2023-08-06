"""Tools for handling bodo arrays, e.g. passing to C/C++ code
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import intrinsic, models, register_model
from numba.np.arrayobj import _getitem_array_single_int
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, get_categories_int_type
from bodo.libs import array_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, define_array_item_dtor, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType, int128_type
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType, _get_map_arr_data_type, init_map_arr_codegen
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, char_arr_type, null_bitmap_arr_type, offset_arr_type, string_array_type
from bodo.libs.struct_arr_ext import StructArrayPayloadType, StructArrayType, StructType, _get_struct_arr_payload, define_struct_arr_dtor
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, is_str_arr_type, raise_bodo_error
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, numba_to_c_type
ll.add_symbol('list_string_array_to_info', array_ext.list_string_array_to_info)
ll.add_symbol('nested_array_to_info', array_ext.nested_array_to_info)
ll.add_symbol('string_array_to_info', array_ext.string_array_to_info)
ll.add_symbol('dict_str_array_to_info', array_ext.dict_str_array_to_info)
ll.add_symbol('get_nested_info', array_ext.get_nested_info)
ll.add_symbol('get_has_global_dictionary', array_ext.get_has_global_dictionary)
ll.add_symbol('numpy_array_to_info', array_ext.numpy_array_to_info)
ll.add_symbol('categorical_array_to_info', array_ext.categorical_array_to_info)
ll.add_symbol('nullable_array_to_info', array_ext.nullable_array_to_info)
ll.add_symbol('interval_array_to_info', array_ext.interval_array_to_info)
ll.add_symbol('decimal_array_to_info', array_ext.decimal_array_to_info)
ll.add_symbol('info_to_nested_array', array_ext.info_to_nested_array)
ll.add_symbol('info_to_list_string_array', array_ext.info_to_list_string_array)
ll.add_symbol('info_to_string_array', array_ext.info_to_string_array)
ll.add_symbol('info_to_numpy_array', array_ext.info_to_numpy_array)
ll.add_symbol('info_to_nullable_array', array_ext.info_to_nullable_array)
ll.add_symbol('info_to_interval_array', array_ext.info_to_interval_array)
ll.add_symbol('alloc_numpy', array_ext.alloc_numpy)
ll.add_symbol('alloc_string_array', array_ext.alloc_string_array)
ll.add_symbol('arr_info_list_to_table', array_ext.arr_info_list_to_table)
ll.add_symbol('info_from_table', array_ext.info_from_table)
ll.add_symbol('delete_info_decref_array', array_ext.delete_info_decref_array)
ll.add_symbol('delete_table_decref_arrays', array_ext.
    delete_table_decref_arrays)
ll.add_symbol('delete_table', array_ext.delete_table)
ll.add_symbol('shuffle_table', array_ext.shuffle_table)
ll.add_symbol('get_shuffle_info', array_ext.get_shuffle_info)
ll.add_symbol('delete_shuffle_info', array_ext.delete_shuffle_info)
ll.add_symbol('reverse_shuffle_table', array_ext.reverse_shuffle_table)
ll.add_symbol('hash_join_table', array_ext.hash_join_table)
ll.add_symbol('drop_duplicates_table', array_ext.drop_duplicates_table)
ll.add_symbol('sort_values_table', array_ext.sort_values_table)
ll.add_symbol('sample_table', array_ext.sample_table)
ll.add_symbol('shuffle_renormalization', array_ext.shuffle_renormalization)
ll.add_symbol('shuffle_renormalization_group', array_ext.
    shuffle_renormalization_group)
ll.add_symbol('groupby_and_aggregate', array_ext.groupby_and_aggregate)
ll.add_symbol('pivot_groupby_and_aggregate', array_ext.
    pivot_groupby_and_aggregate)
ll.add_symbol('get_groupby_labels', array_ext.get_groupby_labels)
ll.add_symbol('array_isin', array_ext.array_isin)
ll.add_symbol('get_search_regex', array_ext.get_search_regex)
ll.add_symbol('array_info_getitem', array_ext.array_info_getitem)
ll.add_symbol('array_info_getdata1', array_ext.array_info_getdata1)


class ArrayInfoType(types.Type):

    def __init__(self):
        super(ArrayInfoType, self).__init__(name='ArrayInfoType()')


array_info_type = ArrayInfoType()
register_model(ArrayInfoType)(models.OpaqueModel)


class TableTypeCPP(types.Type):

    def __init__(self):
        super(TableTypeCPP, self).__init__(name='TableTypeCPP()')


table_type = TableTypeCPP()
register_model(TableTypeCPP)(models.OpaqueModel)


@intrinsic
def array_to_info(typingctx, arr_type_t=None):
    return array_info_type(arr_type_t), array_to_info_codegen


def array_to_info_codegen(context, builder, sig, args, incref=True):
    in_arr, = args
    arr_type = sig.args[0]
    if incref:
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, TupleArrayType):
        udtu__zzna = context.make_helper(builder, arr_type, in_arr)
        in_arr = udtu__zzna.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        zwh__azw = context.make_helper(builder, arr_type, in_arr)
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='list_string_array_to_info')
        return builder.call(mkj__kwn, [zwh__azw.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                zgvdg__etpw = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for nnsfn__lukod in arr_typ.data:
                    zgvdg__etpw += get_types(nnsfn__lukod)
                return zgvdg__etpw
            elif isinstance(arr_typ, (types.Array, IntegerArrayType)
                ) or arr_typ == boolean_array:
                return get_types(arr_typ.dtype)
            elif arr_typ == string_array_type:
                return [CTypeEnum.STRING.value]
            elif arr_typ == binary_array_type:
                return [CTypeEnum.BINARY.value]
            elif isinstance(arr_typ, DecimalArrayType):
                return [CTypeEnum.Decimal.value, arr_typ.precision, arr_typ
                    .scale]
            else:
                return [numba_to_c_type(arr_typ)]

        def get_lengths(arr_typ, arr):
            hcmxi__ccai = context.compile_internal(builder, lambda a: len(a
                ), types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                bgr__oxv = context.make_helper(builder, arr_typ, value=arr)
                mts__efdwb = get_lengths(_get_map_arr_data_type(arr_typ),
                    bgr__oxv.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                szt__dyst = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                mts__efdwb = get_lengths(arr_typ.dtype, szt__dyst.data)
                mts__efdwb = cgutils.pack_array(builder, [szt__dyst.
                    n_arrays] + [builder.extract_value(mts__efdwb,
                    nzpg__yqgkc) for nzpg__yqgkc in range(mts__efdwb.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                szt__dyst = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                mts__efdwb = []
                for nzpg__yqgkc, nnsfn__lukod in enumerate(arr_typ.data):
                    ukm__snhw = get_lengths(nnsfn__lukod, builder.
                        extract_value(szt__dyst.data, nzpg__yqgkc))
                    mts__efdwb += [builder.extract_value(ukm__snhw,
                        odobs__qmq) for odobs__qmq in range(ukm__snhw.type.
                        count)]
                mts__efdwb = cgutils.pack_array(builder, [hcmxi__ccai,
                    context.get_constant(types.int64, -1)] + mts__efdwb)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                mts__efdwb = cgutils.pack_array(builder, [hcmxi__ccai])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return mts__efdwb

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                bgr__oxv = context.make_helper(builder, arr_typ, value=arr)
                wbwu__cizwy = get_buffers(_get_map_arr_data_type(arr_typ),
                    bgr__oxv.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                szt__dyst = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                rok__ytful = get_buffers(arr_typ.dtype, szt__dyst.data)
                gajb__fwhy = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, szt__dyst.offsets)
                hdww__jsp = builder.bitcast(gajb__fwhy.data, lir.IntType(8)
                    .as_pointer())
                dmro__zeldc = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, szt__dyst.null_bitmap)
                usel__rgdkk = builder.bitcast(dmro__zeldc.data, lir.IntType
                    (8).as_pointer())
                wbwu__cizwy = cgutils.pack_array(builder, [hdww__jsp,
                    usel__rgdkk] + [builder.extract_value(rok__ytful,
                    nzpg__yqgkc) for nzpg__yqgkc in range(rok__ytful.type.
                    count)])
            elif isinstance(arr_typ, StructArrayType):
                szt__dyst = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                rok__ytful = []
                for nzpg__yqgkc, nnsfn__lukod in enumerate(arr_typ.data):
                    twfs__xmktk = get_buffers(nnsfn__lukod, builder.
                        extract_value(szt__dyst.data, nzpg__yqgkc))
                    rok__ytful += [builder.extract_value(twfs__xmktk,
                        odobs__qmq) for odobs__qmq in range(twfs__xmktk.
                        type.count)]
                dmro__zeldc = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, szt__dyst.null_bitmap)
                usel__rgdkk = builder.bitcast(dmro__zeldc.data, lir.IntType
                    (8).as_pointer())
                wbwu__cizwy = cgutils.pack_array(builder, [usel__rgdkk] +
                    rok__ytful)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                eoo__bgks = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    eoo__bgks = int128_type
                elif arr_typ == datetime_date_array_type:
                    eoo__bgks = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                xim__lpaq = context.make_array(types.Array(eoo__bgks, 1, 'C'))(
                    context, builder, arr.data)
                dmro__zeldc = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                dlhs__bwm = builder.bitcast(xim__lpaq.data, lir.IntType(8).
                    as_pointer())
                usel__rgdkk = builder.bitcast(dmro__zeldc.data, lir.IntType
                    (8).as_pointer())
                wbwu__cizwy = cgutils.pack_array(builder, [usel__rgdkk,
                    dlhs__bwm])
            elif arr_typ in (string_array_type, binary_array_type):
                szt__dyst = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                ihoqx__yos = context.make_helper(builder, offset_arr_type,
                    szt__dyst.offsets).data
                iqj__nlog = context.make_helper(builder, char_arr_type,
                    szt__dyst.data).data
                fdn__ckof = context.make_helper(builder,
                    null_bitmap_arr_type, szt__dyst.null_bitmap).data
                wbwu__cizwy = cgutils.pack_array(builder, [builder.bitcast(
                    ihoqx__yos, lir.IntType(8).as_pointer()), builder.
                    bitcast(fdn__ckof, lir.IntType(8).as_pointer()),
                    builder.bitcast(iqj__nlog, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                dlhs__bwm = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                dgly__bctf = lir.Constant(lir.IntType(8).as_pointer(), None)
                wbwu__cizwy = cgutils.pack_array(builder, [dgly__bctf,
                    dlhs__bwm])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return wbwu__cizwy

        def get_field_names(arr_typ):
            tfgud__wun = []
            if isinstance(arr_typ, StructArrayType):
                for bgx__brhta, wire__kyug in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    tfgud__wun.append(bgx__brhta)
                    tfgud__wun += get_field_names(wire__kyug)
            elif isinstance(arr_typ, ArrayItemArrayType):
                tfgud__wun += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                tfgud__wun += get_field_names(_get_map_arr_data_type(arr_typ))
            return tfgud__wun
        zgvdg__etpw = get_types(arr_type)
        wmaa__gttef = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in zgvdg__etpw])
        shm__fwb = cgutils.alloca_once_value(builder, wmaa__gttef)
        mts__efdwb = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, mts__efdwb)
        wbwu__cizwy = get_buffers(arr_type, in_arr)
        xuzko__czmm = cgutils.alloca_once_value(builder, wbwu__cizwy)
        tfgud__wun = get_field_names(arr_type)
        if len(tfgud__wun) == 0:
            tfgud__wun = ['irrelevant']
        qxnzp__vsf = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in tfgud__wun])
        qyws__djta = cgutils.alloca_once_value(builder, qxnzp__vsf)
        if isinstance(arr_type, MapArrayType):
            dvg__tcpja = _get_map_arr_data_type(arr_type)
            luiwi__tbfpy = context.make_helper(builder, arr_type, value=in_arr)
            umx__fqa = luiwi__tbfpy.data
        else:
            dvg__tcpja = arr_type
            umx__fqa = in_arr
        sbmgt__imhr = context.make_helper(builder, dvg__tcpja, umx__fqa)
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='nested_array_to_info')
        aheqm__lfrnc = builder.call(mkj__kwn, [builder.bitcast(shm__fwb,
            lir.IntType(32).as_pointer()), builder.bitcast(xuzko__czmm, lir
            .IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            qyws__djta, lir.IntType(8).as_pointer()), sbmgt__imhr.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return aheqm__lfrnc
    if arr_type in (string_array_type, binary_array_type):
        qnrgh__bwlty = context.make_helper(builder, arr_type, in_arr)
        zty__mtw = ArrayItemArrayType(char_arr_type)
        zwh__azw = context.make_helper(builder, zty__mtw, qnrgh__bwlty.data)
        szt__dyst = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        ihoqx__yos = context.make_helper(builder, offset_arr_type,
            szt__dyst.offsets).data
        iqj__nlog = context.make_helper(builder, char_arr_type, szt__dyst.data
            ).data
        fdn__ckof = context.make_helper(builder, null_bitmap_arr_type,
            szt__dyst.null_bitmap).data
        ngrr__bqhlc = builder.zext(builder.load(builder.gep(ihoqx__yos, [
            szt__dyst.n_arrays])), lir.IntType(64))
        pdwuk__asz = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='string_array_to_info')
        return builder.call(mkj__kwn, [szt__dyst.n_arrays, ngrr__bqhlc,
            iqj__nlog, ihoqx__yos, fdn__ckof, zwh__azw.meminfo, pdwuk__asz])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        zpi__uzga = arr.data
        efisc__vgymx = arr.indices
        sig = array_info_type(arr_type.data)
        ldxgn__mufs = array_to_info_codegen(context, builder, sig, (
            zpi__uzga,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        mwebo__tmr = array_to_info_codegen(context, builder, sig, (
            efisc__vgymx,), False)
        xqdk__kbkix = cgutils.create_struct_proxy(bodo.libs.dict_arr_ext.
            dict_indices_arr_type)(context, builder, efisc__vgymx)
        usel__rgdkk = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, xqdk__kbkix.null_bitmap).data
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='dict_str_array_to_info')
        gnuw__lrk = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(mkj__kwn, [ldxgn__mufs, mwebo__tmr, builder.
            bitcast(usel__rgdkk, lir.IntType(8).as_pointer()), gnuw__lrk])
    ljz__uyf = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        tmoxo__ngj = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        wyw__yyt = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(wyw__yyt, 1, 'C')
        ljz__uyf = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if ljz__uyf:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        hcmxi__ccai = builder.extract_value(arr.shape, 0)
        mpum__othnm = arr_type.dtype
        qtt__neydl = numba_to_c_type(mpum__othnm)
        cyw__alnm = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), qtt__neydl))
        if ljz__uyf:
            knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(64), lir.IntType(8).as_pointer()])
            mkj__kwn = cgutils.get_or_insert_function(builder.module,
                knt__ewlw, name='categorical_array_to_info')
            return builder.call(mkj__kwn, [hcmxi__ccai, builder.bitcast(arr
                .data, lir.IntType(8).as_pointer()), builder.load(cyw__alnm
                ), tmoxo__ngj, arr.meminfo])
        else:
            knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer()])
            mkj__kwn = cgutils.get_or_insert_function(builder.module,
                knt__ewlw, name='numpy_array_to_info')
            return builder.call(mkj__kwn, [hcmxi__ccai, builder.bitcast(arr
                .data, lir.IntType(8).as_pointer()), builder.load(cyw__alnm
                ), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        mpum__othnm = arr_type.dtype
        eoo__bgks = mpum__othnm
        if isinstance(arr_type, DecimalArrayType):
            eoo__bgks = int128_type
        if arr_type == datetime_date_array_type:
            eoo__bgks = types.int64
        xim__lpaq = context.make_array(types.Array(eoo__bgks, 1, 'C'))(context,
            builder, arr.data)
        hcmxi__ccai = builder.extract_value(xim__lpaq.shape, 0)
        inp__wsoci = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        qtt__neydl = numba_to_c_type(mpum__othnm)
        cyw__alnm = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), qtt__neydl))
        if isinstance(arr_type, DecimalArrayType):
            knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
            mkj__kwn = cgutils.get_or_insert_function(builder.module,
                knt__ewlw, name='decimal_array_to_info')
            return builder.call(mkj__kwn, [hcmxi__ccai, builder.bitcast(
                xim__lpaq.data, lir.IntType(8).as_pointer()), builder.load(
                cyw__alnm), builder.bitcast(inp__wsoci.data, lir.IntType(8)
                .as_pointer()), xim__lpaq.meminfo, inp__wsoci.meminfo,
                context.get_constant(types.int32, arr_type.precision),
                context.get_constant(types.int32, arr_type.scale)])
        else:
            knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
                IntType(64), lir.IntType(8).as_pointer(), lir.IntType(32),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                lir.IntType(8).as_pointer()])
            mkj__kwn = cgutils.get_or_insert_function(builder.module,
                knt__ewlw, name='nullable_array_to_info')
            return builder.call(mkj__kwn, [hcmxi__ccai, builder.bitcast(
                xim__lpaq.data, lir.IntType(8).as_pointer()), builder.load(
                cyw__alnm), builder.bitcast(inp__wsoci.data, lir.IntType(8)
                .as_pointer()), xim__lpaq.meminfo, inp__wsoci.meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        oarsh__xkcht = context.make_array(arr_type.arr_type)(context,
            builder, arr.left)
        uovtu__qsb = context.make_array(arr_type.arr_type)(context, builder,
            arr.right)
        hcmxi__ccai = builder.extract_value(oarsh__xkcht.shape, 0)
        qtt__neydl = numba_to_c_type(arr_type.arr_type.dtype)
        cyw__alnm = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), qtt__neydl))
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='interval_array_to_info')
        return builder.call(mkj__kwn, [hcmxi__ccai, builder.bitcast(
            oarsh__xkcht.data, lir.IntType(8).as_pointer()), builder.
            bitcast(uovtu__qsb.data, lir.IntType(8).as_pointer()), builder.
            load(cyw__alnm), oarsh__xkcht.meminfo, uovtu__qsb.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    ojxir__owktl = cgutils.alloca_once(builder, lir.IntType(64))
    dlhs__bwm = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    ycpp__gvh = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    knt__ewlw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(64).as_pointer(), lir.IntType(8).as_pointer().
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
        name='info_to_numpy_array')
    builder.call(mkj__kwn, [in_info, ojxir__owktl, dlhs__bwm, ycpp__gvh])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    xobx__kfqs = context.get_value_type(types.intp)
    amsp__ncoz = cgutils.pack_array(builder, [builder.load(ojxir__owktl)],
        ty=xobx__kfqs)
    peu__fdcm = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    daiv__hawu = cgutils.pack_array(builder, [peu__fdcm], ty=xobx__kfqs)
    iqj__nlog = builder.bitcast(builder.load(dlhs__bwm), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=iqj__nlog, shape=amsp__ncoz,
        strides=daiv__hawu, itemsize=peu__fdcm, meminfo=builder.load(ycpp__gvh)
        )
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    gfe__xysxu = context.make_helper(builder, arr_type)
    knt__ewlw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer
        (), lir.IntType(8).as_pointer().as_pointer()])
    mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
        name='info_to_list_string_array')
    builder.call(mkj__kwn, [in_info, gfe__xysxu._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return gfe__xysxu._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    eph__kiwm = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        fyp__zwtqm = lengths_pos
        ewpw__zom = infos_pos
        mltl__dua, lengths_pos, infos_pos = nested_to_array(context,
            builder, arr_typ.dtype, lengths_ptr, array_infos_ptr, 
            lengths_pos + 1, infos_pos + 2)
        dfwgt__atgh = ArrayItemArrayPayloadType(arr_typ)
        hyi__ccr = context.get_data_type(dfwgt__atgh)
        hcrt__umrr = context.get_abi_sizeof(hyi__ccr)
        trb__bnwrh = define_array_item_dtor(context, builder, arr_typ,
            dfwgt__atgh)
        hbbw__njf = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, hcrt__umrr), trb__bnwrh)
        raqjj__berb = context.nrt.meminfo_data(builder, hbbw__njf)
        tlbny__umzk = builder.bitcast(raqjj__berb, hyi__ccr.as_pointer())
        szt__dyst = cgutils.create_struct_proxy(dfwgt__atgh)(context, builder)
        szt__dyst.n_arrays = builder.extract_value(builder.load(lengths_ptr
            ), fyp__zwtqm)
        szt__dyst.data = mltl__dua
        xftfn__qmpz = builder.load(array_infos_ptr)
        hyw__ieb = builder.bitcast(builder.extract_value(xftfn__qmpz,
            ewpw__zom), eph__kiwm)
        szt__dyst.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, hyw__ieb)
        gfjt__sow = builder.bitcast(builder.extract_value(xftfn__qmpz, 
            ewpw__zom + 1), eph__kiwm)
        szt__dyst.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, gfjt__sow)
        builder.store(szt__dyst._getvalue(), tlbny__umzk)
        zwh__azw = context.make_helper(builder, arr_typ)
        zwh__azw.meminfo = hbbw__njf
        return zwh__azw._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        vvrg__pboaa = []
        ewpw__zom = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for xnx__hld in arr_typ.data:
            mltl__dua, lengths_pos, infos_pos = nested_to_array(context,
                builder, xnx__hld, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            vvrg__pboaa.append(mltl__dua)
        dfwgt__atgh = StructArrayPayloadType(arr_typ.data)
        hyi__ccr = context.get_value_type(dfwgt__atgh)
        hcrt__umrr = context.get_abi_sizeof(hyi__ccr)
        trb__bnwrh = define_struct_arr_dtor(context, builder, arr_typ,
            dfwgt__atgh)
        hbbw__njf = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, hcrt__umrr), trb__bnwrh)
        raqjj__berb = context.nrt.meminfo_data(builder, hbbw__njf)
        tlbny__umzk = builder.bitcast(raqjj__berb, hyi__ccr.as_pointer())
        szt__dyst = cgutils.create_struct_proxy(dfwgt__atgh)(context, builder)
        szt__dyst.data = cgutils.pack_array(builder, vvrg__pboaa
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, vvrg__pboaa)
        xftfn__qmpz = builder.load(array_infos_ptr)
        gfjt__sow = builder.bitcast(builder.extract_value(xftfn__qmpz,
            ewpw__zom), eph__kiwm)
        szt__dyst.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, gfjt__sow)
        builder.store(szt__dyst._getvalue(), tlbny__umzk)
        ixpin__rbaay = context.make_helper(builder, arr_typ)
        ixpin__rbaay.meminfo = hbbw__njf
        return ixpin__rbaay._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        xftfn__qmpz = builder.load(array_infos_ptr)
        zwzsl__dqf = builder.bitcast(builder.extract_value(xftfn__qmpz,
            infos_pos), eph__kiwm)
        qnrgh__bwlty = context.make_helper(builder, arr_typ)
        zty__mtw = ArrayItemArrayType(char_arr_type)
        zwh__azw = context.make_helper(builder, zty__mtw)
        knt__ewlw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='info_to_string_array')
        builder.call(mkj__kwn, [zwzsl__dqf, zwh__azw._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        qnrgh__bwlty.data = zwh__azw._getvalue()
        return qnrgh__bwlty._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        xftfn__qmpz = builder.load(array_infos_ptr)
        wcsts__xuvjy = builder.bitcast(builder.extract_value(xftfn__qmpz, 
            infos_pos + 1), eph__kiwm)
        return _lower_info_to_array_numpy(arr_typ, context, builder,
            wcsts__xuvjy), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        eoo__bgks = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            eoo__bgks = int128_type
        elif arr_typ == datetime_date_array_type:
            eoo__bgks = types.int64
        xftfn__qmpz = builder.load(array_infos_ptr)
        gfjt__sow = builder.bitcast(builder.extract_value(xftfn__qmpz,
            infos_pos), eph__kiwm)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, gfjt__sow)
        wcsts__xuvjy = builder.bitcast(builder.extract_value(xftfn__qmpz, 
            infos_pos + 1), eph__kiwm)
        arr.data = _lower_info_to_array_numpy(types.Array(eoo__bgks, 1, 'C'
            ), context, builder, wcsts__xuvjy)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, fypji__vswot = args
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        return _lower_info_to_array_list_string_array(arr_type, context,
            builder, in_info)
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType,
        StructArrayType, TupleArrayType)):

        def get_num_arrays(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 1 + get_num_arrays(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_arrays(xnx__hld) for xnx__hld in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(xnx__hld) for xnx__hld in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            lmlf__sbx = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            lmlf__sbx = _get_map_arr_data_type(arr_type)
        else:
            lmlf__sbx = arr_type
        qvsda__rssw = get_num_arrays(lmlf__sbx)
        mts__efdwb = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), 0) for fypji__vswot in range(qvsda__rssw)])
        lengths_ptr = cgutils.alloca_once_value(builder, mts__efdwb)
        dgly__bctf = lir.Constant(lir.IntType(8).as_pointer(), None)
        sdqcy__amwv = cgutils.pack_array(builder, [dgly__bctf for
            fypji__vswot in range(get_num_infos(lmlf__sbx))])
        array_infos_ptr = cgutils.alloca_once_value(builder, sdqcy__amwv)
        knt__ewlw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='info_to_nested_array')
        builder.call(mkj__kwn, [in_info, builder.bitcast(lengths_ptr, lir.
            IntType(64).as_pointer()), builder.bitcast(array_infos_ptr, lir
            .IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, fypji__vswot, fypji__vswot = nested_to_array(context, builder,
            lmlf__sbx, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            udtu__zzna = context.make_helper(builder, arr_type)
            udtu__zzna.data = arr
            context.nrt.incref(builder, lmlf__sbx, arr)
            arr = udtu__zzna._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, lmlf__sbx)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        qnrgh__bwlty = context.make_helper(builder, arr_type)
        zty__mtw = ArrayItemArrayType(char_arr_type)
        zwh__azw = context.make_helper(builder, zty__mtw)
        knt__ewlw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='info_to_string_array')
        builder.call(mkj__kwn, [in_info, zwh__azw._get_ptr_by_name('meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        qnrgh__bwlty.data = zwh__azw._getvalue()
        return qnrgh__bwlty._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='get_nested_info')
        ldxgn__mufs = builder.call(mkj__kwn, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        mwebo__tmr = builder.call(mkj__kwn, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        eprx__cqjgc = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        eprx__cqjgc.data = info_to_array_codegen(context, builder, sig, (
            ldxgn__mufs, context.get_constant_null(arr_type.data)))
        clxv__voyf = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = clxv__voyf(array_info_type, clxv__voyf)
        eprx__cqjgc.indices = info_to_array_codegen(context, builder, sig,
            (mwebo__tmr, context.get_constant_null(clxv__voyf)))
        knt__ewlw = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='get_has_global_dictionary')
        gnuw__lrk = builder.call(mkj__kwn, [in_info])
        eprx__cqjgc.has_global_dictionary = builder.trunc(gnuw__lrk,
            cgutils.bool_t)
        return eprx__cqjgc._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        wyw__yyt = get_categories_int_type(arr_type.dtype)
        uqwzk__pzw = types.Array(wyw__yyt, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(uqwzk__pzw, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            huw__kxtw = pd.CategoricalDtype(arr_type.dtype.categories,
                is_ordered).categories.values
            new_cats_tup = MetaType(tuple(huw__kxtw))
            int_type = arr_type.dtype.int_type
            hmz__gyomb = bodo.typeof(huw__kxtw)
            bvqv__jpf = context.get_constant_generic(builder, hmz__gyomb,
                huw__kxtw)
            mpum__othnm = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(hmz__gyomb), [bvqv__jpf])
        else:
            mpum__othnm = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, mpum__othnm)
        out_arr.dtype = mpum__othnm
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        iqj__nlog = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = iqj__nlog
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        eoo__bgks = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            eoo__bgks = int128_type
        elif arr_type == datetime_date_array_type:
            eoo__bgks = types.int64
        mqim__eyrvj = types.Array(eoo__bgks, 1, 'C')
        xim__lpaq = context.make_array(mqim__eyrvj)(context, builder)
        bvljz__qqj = types.Array(types.uint8, 1, 'C')
        cpi__ahhzv = context.make_array(bvljz__qqj)(context, builder)
        ojxir__owktl = cgutils.alloca_once(builder, lir.IntType(64))
        yjno__rlou = cgutils.alloca_once(builder, lir.IntType(64))
        dlhs__bwm = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        fmac__ksab = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ycpp__gvh = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        tpnig__vkbf = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        knt__ewlw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='info_to_nullable_array')
        builder.call(mkj__kwn, [in_info, ojxir__owktl, yjno__rlou,
            dlhs__bwm, fmac__ksab, ycpp__gvh, tpnig__vkbf])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        xobx__kfqs = context.get_value_type(types.intp)
        amsp__ncoz = cgutils.pack_array(builder, [builder.load(ojxir__owktl
            )], ty=xobx__kfqs)
        peu__fdcm = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(eoo__bgks)))
        daiv__hawu = cgutils.pack_array(builder, [peu__fdcm], ty=xobx__kfqs)
        iqj__nlog = builder.bitcast(builder.load(dlhs__bwm), context.
            get_data_type(eoo__bgks).as_pointer())
        numba.np.arrayobj.populate_array(xim__lpaq, data=iqj__nlog, shape=
            amsp__ncoz, strides=daiv__hawu, itemsize=peu__fdcm, meminfo=
            builder.load(ycpp__gvh))
        arr.data = xim__lpaq._getvalue()
        amsp__ncoz = cgutils.pack_array(builder, [builder.load(yjno__rlou)],
            ty=xobx__kfqs)
        peu__fdcm = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(types.uint8)))
        daiv__hawu = cgutils.pack_array(builder, [peu__fdcm], ty=xobx__kfqs)
        iqj__nlog = builder.bitcast(builder.load(fmac__ksab), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(cpi__ahhzv, data=iqj__nlog, shape=
            amsp__ncoz, strides=daiv__hawu, itemsize=peu__fdcm, meminfo=
            builder.load(tpnig__vkbf))
        arr.null_bitmap = cpi__ahhzv._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        oarsh__xkcht = context.make_array(arr_type.arr_type)(context, builder)
        uovtu__qsb = context.make_array(arr_type.arr_type)(context, builder)
        ojxir__owktl = cgutils.alloca_once(builder, lir.IntType(64))
        apfk__ung = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ldid__poh = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        kzgu__qsy = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        fzzem__svs = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        knt__ewlw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='info_to_interval_array')
        builder.call(mkj__kwn, [in_info, ojxir__owktl, apfk__ung, ldid__poh,
            kzgu__qsy, fzzem__svs])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        xobx__kfqs = context.get_value_type(types.intp)
        amsp__ncoz = cgutils.pack_array(builder, [builder.load(ojxir__owktl
            )], ty=xobx__kfqs)
        peu__fdcm = context.get_constant(types.intp, context.get_abi_sizeof
            (context.get_data_type(arr_type.arr_type.dtype)))
        daiv__hawu = cgutils.pack_array(builder, [peu__fdcm], ty=xobx__kfqs)
        frrn__uhx = builder.bitcast(builder.load(apfk__ung), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(oarsh__xkcht, data=frrn__uhx,
            shape=amsp__ncoz, strides=daiv__hawu, itemsize=peu__fdcm,
            meminfo=builder.load(kzgu__qsy))
        arr.left = oarsh__xkcht._getvalue()
        puwdq__xhi = builder.bitcast(builder.load(ldid__poh), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(uovtu__qsb, data=puwdq__xhi, shape
            =amsp__ncoz, strides=daiv__hawu, itemsize=peu__fdcm, meminfo=
            builder.load(fzzem__svs))
        arr.right = uovtu__qsb._getvalue()
        return arr._getvalue()
    raise_bodo_error(f'info_to_array(): array type {arr_type} is not supported'
        )


@intrinsic
def info_to_array(typingctx, info_type, array_type):
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    assert info_type == array_info_type, 'info_to_array: expected info type'
    return arr_type(info_type, array_type), info_to_array_codegen


@intrinsic
def test_alloc_np(typingctx, len_typ, arr_type):
    array_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type

    def codegen(context, builder, sig, args):
        hcmxi__ccai, fypji__vswot = args
        qtt__neydl = numba_to_c_type(array_type.dtype)
        cyw__alnm = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), qtt__neydl))
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='alloc_numpy')
        return builder.call(mkj__kwn, [hcmxi__ccai, builder.load(cyw__alnm)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        hcmxi__ccai, clozp__xxkk = args
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='alloc_string_array')
        return builder.call(mkj__kwn, [hcmxi__ccai, clozp__xxkk])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    jlqtr__hzh, = args
    klvlv__vou = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], jlqtr__hzh)
    knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer().as_pointer(), lir.IntType(64)])
    mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
        name='arr_info_list_to_table')
    return builder.call(mkj__kwn, [klvlv__vou.data, klvlv__vou.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='info_from_table')
        return builder.call(mkj__kwn, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    wjoys__qquv = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        gdq__pczhx, dlp__lhcm, fypji__vswot = args
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='info_from_table')
        vsfs__ksu = cgutils.create_struct_proxy(wjoys__qquv)(context, builder)
        vsfs__ksu.parent = cgutils.get_null_value(vsfs__ksu.parent.type)
        vgp__uun = context.make_array(table_idx_arr_t)(context, builder,
            dlp__lhcm)
        dnt__buv = context.get_constant(types.int64, -1)
        knxmm__nwoq = context.get_constant(types.int64, 0)
        qbh__sum = cgutils.alloca_once_value(builder, knxmm__nwoq)
        for t, opql__akw in wjoys__qquv.type_to_blk.items():
            hfxnc__lopbq = context.get_constant(types.int64, len(
                wjoys__qquv.block_to_arr_ind[opql__akw]))
            fypji__vswot, mwhs__xfzc = ListInstance.allocate_ex(context,
                builder, types.List(t), hfxnc__lopbq)
            mwhs__xfzc.size = hfxnc__lopbq
            kszlt__tqi = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(wjoys__qquv.block_to_arr_ind
                [opql__akw], dtype=np.int64))
            nayrc__dko = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, kszlt__tqi)
            with cgutils.for_range(builder, hfxnc__lopbq) as iitfw__wymgp:
                nzpg__yqgkc = iitfw__wymgp.index
                zhn__etc = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    nayrc__dko, nzpg__yqgkc)
                ffc__qcn = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, vgp__uun, zhn__etc)
                uxxom__uss = builder.icmp_unsigned('!=', ffc__qcn, dnt__buv)
                with builder.if_else(uxxom__uss) as (hobri__flzhj, mjthw__ffco
                    ):
                    with hobri__flzhj:
                        weta__tmnh = builder.call(mkj__kwn, [gdq__pczhx,
                            ffc__qcn])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            weta__tmnh])
                        mwhs__xfzc.inititem(nzpg__yqgkc, arr, incref=False)
                        hcmxi__ccai = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(hcmxi__ccai, qbh__sum)
                    with mjthw__ffco:
                        uoyam__mtaz = context.get_constant_null(t)
                        mwhs__xfzc.inititem(nzpg__yqgkc, uoyam__mtaz,
                            incref=False)
            setattr(vsfs__ksu, f'block_{opql__akw}', mwhs__xfzc.value)
        vsfs__ksu.len = builder.load(qbh__sum)
        return vsfs__ksu._getvalue()
    return wjoys__qquv(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    wjoys__qquv = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        tkou__cavyf, fypji__vswot = args
        lap__osqs = cgutils.create_struct_proxy(wjoys__qquv)(context,
            builder, tkou__cavyf)
        if wjoys__qquv.has_runtime_cols:
            zxx__pja = lir.Constant(lir.IntType(64), 0)
            for opql__akw, t in enumerate(wjoys__qquv.arr_types):
                pff__hnlmf = getattr(lap__osqs, f'block_{opql__akw}')
                sdjod__nhoo = ListInstance(context, builder, types.List(t),
                    pff__hnlmf)
                zxx__pja = builder.add(zxx__pja, sdjod__nhoo.size)
        else:
            zxx__pja = lir.Constant(lir.IntType(64), len(wjoys__qquv.arr_types)
                )
        fypji__vswot, msuv__mpq = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), zxx__pja)
        msuv__mpq.size = zxx__pja
        if wjoys__qquv.has_runtime_cols:
            qrct__yvg = lir.Constant(lir.IntType(64), 0)
            for opql__akw, t in enumerate(wjoys__qquv.arr_types):
                pff__hnlmf = getattr(lap__osqs, f'block_{opql__akw}')
                sdjod__nhoo = ListInstance(context, builder, types.List(t),
                    pff__hnlmf)
                hfxnc__lopbq = sdjod__nhoo.size
                with cgutils.for_range(builder, hfxnc__lopbq) as iitfw__wymgp:
                    nzpg__yqgkc = iitfw__wymgp.index
                    arr = sdjod__nhoo.getitem(nzpg__yqgkc)
                    flf__xvl = signature(array_info_type, t)
                    aex__niczm = arr,
                    myd__smmp = array_to_info_codegen(context, builder,
                        flf__xvl, aex__niczm)
                    msuv__mpq.inititem(builder.add(qrct__yvg, nzpg__yqgkc),
                        myd__smmp, incref=False)
                qrct__yvg = builder.add(qrct__yvg, hfxnc__lopbq)
        else:
            for t, opql__akw in wjoys__qquv.type_to_blk.items():
                hfxnc__lopbq = context.get_constant(types.int64, len(
                    wjoys__qquv.block_to_arr_ind[opql__akw]))
                pff__hnlmf = getattr(lap__osqs, f'block_{opql__akw}')
                sdjod__nhoo = ListInstance(context, builder, types.List(t),
                    pff__hnlmf)
                kszlt__tqi = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(wjoys__qquv.
                    block_to_arr_ind[opql__akw], dtype=np.int64))
                nayrc__dko = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, kszlt__tqi)
                with cgutils.for_range(builder, hfxnc__lopbq) as iitfw__wymgp:
                    nzpg__yqgkc = iitfw__wymgp.index
                    zhn__etc = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        nayrc__dko, nzpg__yqgkc)
                    rgxe__tdop = signature(types.none, wjoys__qquv, types.
                        List(t), types.int64, types.int64)
                    euo__vpq = tkou__cavyf, pff__hnlmf, nzpg__yqgkc, zhn__etc
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, rgxe__tdop, euo__vpq)
                    arr = sdjod__nhoo.getitem(nzpg__yqgkc)
                    flf__xvl = signature(array_info_type, t)
                    aex__niczm = arr,
                    myd__smmp = array_to_info_codegen(context, builder,
                        flf__xvl, aex__niczm)
                    msuv__mpq.inititem(zhn__etc, myd__smmp, incref=False)
        mlf__vdsp = msuv__mpq.value
        lpb__qmm = signature(table_type, types.List(array_info_type))
        sgst__tfxk = mlf__vdsp,
        gdq__pczhx = arr_info_list_to_table_codegen(context, builder,
            lpb__qmm, sgst__tfxk)
        context.nrt.decref(builder, types.List(array_info_type), mlf__vdsp)
        return gdq__pczhx
    return table_type(wjoys__qquv, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='delete_table')
        builder.call(mkj__kwn, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='shuffle_table')
        aheqm__lfrnc = builder.call(mkj__kwn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return aheqm__lfrnc
    return table_type(table_t, types.int64, types.boolean, types.int32
        ), codegen


class ShuffleInfoType(types.Type):

    def __init__(self):
        super(ShuffleInfoType, self).__init__(name='ShuffleInfoType()')


shuffle_info_type = ShuffleInfoType()
register_model(ShuffleInfoType)(models.OpaqueModel)
get_shuffle_info = types.ExternalFunction('get_shuffle_info',
    shuffle_info_type(table_type))


@intrinsic
def delete_shuffle_info(typingctx, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[0] == types.none:
            return
        knt__ewlw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='delete_shuffle_info')
        return builder.call(mkj__kwn, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='reverse_shuffle_table')
        return builder.call(mkj__kwn, args)
    return table_type(table_type, shuffle_info_t), codegen


@intrinsic
def get_null_shuffle_info(typingctx):

    def codegen(context, builder, sig, args):
        return context.get_constant_null(sig.return_type)
    return shuffle_info_type(), codegen


@intrinsic
def hash_join_table(typingctx, left_table_t, right_table_t, left_parallel_t,
    right_parallel_t, n_keys_t, n_data_left_t, n_data_right_t, same_vect_t,
    same_need_typechange_t, is_left_t, is_right_t, is_join_t,
    optional_col_t, indicator, _bodo_na_equal, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len):
    assert left_table_t == table_type
    assert right_table_t == table_type

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='hash_join_table')
        aheqm__lfrnc = builder.call(mkj__kwn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return aheqm__lfrnc
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.int64, types.int64, types.int64, types.voidptr,
        types.voidptr, types.boolean, types.boolean, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.int64, types.voidptr, types.int64), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='sort_values_table')
        aheqm__lfrnc = builder.call(mkj__kwn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return aheqm__lfrnc
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='sample_table')
        aheqm__lfrnc = builder.call(mkj__kwn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return aheqm__lfrnc
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='shuffle_renormalization')
        aheqm__lfrnc = builder.call(mkj__kwn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return aheqm__lfrnc
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='shuffle_renormalization_group')
        aheqm__lfrnc = builder.call(mkj__kwn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return aheqm__lfrnc
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='drop_duplicates_table')
        aheqm__lfrnc = builder.call(mkj__kwn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return aheqm__lfrnc
    return table_type(table_t, types.boolean, types.int64, types.int64,
        types.boolean, types.boolean), codegen


@intrinsic
def pivot_groupby_and_aggregate(typingctx, table_t, n_keys_t,
    dispatch_table_t, dispatch_info_t, input_has_index, ftypes,
    func_offsets, udf_n_redvars, is_parallel, is_crosstab, skipdropna_t,
    return_keys, return_index, update_cb, combine_cb, eval_cb,
    udf_table_dummy_t):
    assert table_t == table_type
    assert dispatch_table_t == table_type
    assert dispatch_info_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='pivot_groupby_and_aggregate')
        aheqm__lfrnc = builder.call(mkj__kwn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return aheqm__lfrnc
    return table_type(table_t, types.int64, table_t, table_t, types.boolean,
        types.voidptr, types.voidptr, types.voidptr, types.boolean, types.
        boolean, types.boolean, types.boolean, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, table_t), codegen


@intrinsic
def groupby_and_aggregate(typingctx, table_t, n_keys_t, input_has_index,
    ftypes, func_offsets, udf_n_redvars, is_parallel, skipdropna_t,
    shift_periods_t, transform_func, head_n, return_keys, return_index,
    dropna, update_cb, combine_cb, eval_cb, general_udfs_cb, udf_table_dummy_t
    ):
    assert table_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        mkj__kwn = cgutils.get_or_insert_function(builder.module, knt__ewlw,
            name='groupby_and_aggregate')
        aheqm__lfrnc = builder.call(mkj__kwn, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return aheqm__lfrnc
    return table_type(table_t, types.int64, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        int64, types.int64, types.int64, types.boolean, types.boolean,
        types.boolean, types.voidptr, types.voidptr, types.voidptr, types.
        voidptr, table_t), codegen


get_groupby_labels = types.ExternalFunction('get_groupby_labels', types.
    int64(table_type, types.voidptr, types.voidptr, types.boolean, types.bool_)
    )
_array_isin = types.ExternalFunction('array_isin', types.void(
    array_info_type, array_info_type, array_info_type, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def array_isin(out_arr, in_arr, in_values, is_parallel):
    in_arr = decode_if_dict_array(in_arr)
    in_values = decode_if_dict_array(in_values)
    vxyes__lxf = array_to_info(in_arr)
    dcry__rwkw = array_to_info(in_values)
    qotro__kecy = array_to_info(out_arr)
    ykt__wifbb = arr_info_list_to_table([vxyes__lxf, dcry__rwkw, qotro__kecy])
    _array_isin(qotro__kecy, vxyes__lxf, dcry__rwkw, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(ykt__wifbb)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, pat, out_arr):
    vxyes__lxf = array_to_info(in_arr)
    qotro__kecy = array_to_info(out_arr)
    _get_search_regex(vxyes__lxf, case, pat, qotro__kecy)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    lbndg__uyk = col_array_typ.dtype
    if isinstance(lbndg__uyk, types.Number) or lbndg__uyk in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                vsfs__ksu, pptuv__iwla = args
                vsfs__ksu = builder.bitcast(vsfs__ksu, lir.IntType(8).
                    as_pointer().as_pointer())
                yhjny__odeb = lir.Constant(lir.IntType(64), c_ind)
                jzfqe__vhj = builder.load(builder.gep(vsfs__ksu, [yhjny__odeb])
                    )
                jzfqe__vhj = builder.bitcast(jzfqe__vhj, context.
                    get_data_type(lbndg__uyk).as_pointer())
                return builder.load(builder.gep(jzfqe__vhj, [pptuv__iwla]))
            return lbndg__uyk(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.string_array_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                vsfs__ksu, pptuv__iwla = args
                vsfs__ksu = builder.bitcast(vsfs__ksu, lir.IntType(8).
                    as_pointer().as_pointer())
                yhjny__odeb = lir.Constant(lir.IntType(64), c_ind)
                jzfqe__vhj = builder.load(builder.gep(vsfs__ksu, [yhjny__odeb])
                    )
                knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                gsjuq__eofpz = cgutils.get_or_insert_function(builder.
                    module, knt__ewlw, name='array_info_getitem')
                jkbcw__gdyw = cgutils.alloca_once(builder, lir.IntType(64))
                args = jzfqe__vhj, pptuv__iwla, jkbcw__gdyw
                dlhs__bwm = builder.call(gsjuq__eofpz, args)
                return context.make_tuple(builder, sig.return_type, [
                    dlhs__bwm, builder.load(jkbcw__gdyw)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                dyiel__jskq = lir.Constant(lir.IntType(64), 1)
                pdx__hrbd = lir.Constant(lir.IntType(64), 2)
                vsfs__ksu, pptuv__iwla = args
                vsfs__ksu = builder.bitcast(vsfs__ksu, lir.IntType(8).
                    as_pointer().as_pointer())
                yhjny__odeb = lir.Constant(lir.IntType(64), c_ind)
                jzfqe__vhj = builder.load(builder.gep(vsfs__ksu, [yhjny__odeb])
                    )
                knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64)])
                wcx__dvjh = cgutils.get_or_insert_function(builder.module,
                    knt__ewlw, name='get_nested_info')
                args = jzfqe__vhj, pdx__hrbd
                ixyah__cloh = builder.call(wcx__dvjh, args)
                knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer()])
                mnalc__fzr = cgutils.get_or_insert_function(builder.module,
                    knt__ewlw, name='array_info_getdata1')
                args = ixyah__cloh,
                wvjr__jjzh = builder.call(mnalc__fzr, args)
                wvjr__jjzh = builder.bitcast(wvjr__jjzh, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                bkqvr__ecxn = builder.sext(builder.load(builder.gep(
                    wvjr__jjzh, [pptuv__iwla])), lir.IntType(64))
                args = jzfqe__vhj, dyiel__jskq
                btqre__lvmp = builder.call(wcx__dvjh, args)
                knt__ewlw = lir.FunctionType(lir.IntType(8).as_pointer(), [
                    lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                gsjuq__eofpz = cgutils.get_or_insert_function(builder.
                    module, knt__ewlw, name='array_info_getitem')
                jkbcw__gdyw = cgutils.alloca_once(builder, lir.IntType(64))
                args = btqre__lvmp, bkqvr__ecxn, jkbcw__gdyw
                dlhs__bwm = builder.call(gsjuq__eofpz, args)
                return context.make_tuple(builder, sig.return_type, [
                    dlhs__bwm, builder.load(jkbcw__gdyw)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{lbndg__uyk}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if (isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType) or
        col_array_dtype == bodo.libs.bool_arr_ext.boolean_array or
        is_str_arr_type(col_array_dtype) or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                elqqk__wszb, pptuv__iwla = args
                elqqk__wszb = builder.bitcast(elqqk__wszb, lir.IntType(8).
                    as_pointer().as_pointer())
                yhjny__odeb = lir.Constant(lir.IntType(64), c_ind)
                jzfqe__vhj = builder.load(builder.gep(elqqk__wszb, [
                    yhjny__odeb]))
                fdn__ckof = builder.bitcast(jzfqe__vhj, context.
                    get_data_type(types.bool_).as_pointer())
                dpr__etqa = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    fdn__ckof, pptuv__iwla)
                enohl__jed = builder.icmp_unsigned('!=', dpr__etqa, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(enohl__jed, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        lbndg__uyk = col_array_dtype.dtype
        if lbndg__uyk in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    vsfs__ksu, pptuv__iwla = args
                    vsfs__ksu = builder.bitcast(vsfs__ksu, lir.IntType(8).
                        as_pointer().as_pointer())
                    yhjny__odeb = lir.Constant(lir.IntType(64), c_ind)
                    jzfqe__vhj = builder.load(builder.gep(vsfs__ksu, [
                        yhjny__odeb]))
                    jzfqe__vhj = builder.bitcast(jzfqe__vhj, context.
                        get_data_type(lbndg__uyk).as_pointer())
                    zpafz__ozsac = builder.load(builder.gep(jzfqe__vhj, [
                        pptuv__iwla]))
                    enohl__jed = builder.icmp_unsigned('!=', zpafz__ozsac,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(enohl__jed, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(lbndg__uyk, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    vsfs__ksu, pptuv__iwla = args
                    vsfs__ksu = builder.bitcast(vsfs__ksu, lir.IntType(8).
                        as_pointer().as_pointer())
                    yhjny__odeb = lir.Constant(lir.IntType(64), c_ind)
                    jzfqe__vhj = builder.load(builder.gep(vsfs__ksu, [
                        yhjny__odeb]))
                    jzfqe__vhj = builder.bitcast(jzfqe__vhj, context.
                        get_data_type(lbndg__uyk).as_pointer())
                    zpafz__ozsac = builder.load(builder.gep(jzfqe__vhj, [
                        pptuv__iwla]))
                    orbz__udhh = signature(types.bool_, lbndg__uyk)
                    dpr__etqa = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, orbz__udhh, (zpafz__ozsac,))
                    return builder.not_(builder.sext(dpr__etqa, lir.IntType(8))
                        )
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
