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
        rauh__lcp = context.make_helper(builder, arr_type, in_arr)
        in_arr = rauh__lcp.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        ixdgk__dgp = context.make_helper(builder, arr_type, in_arr)
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='list_string_array_to_info')
        return builder.call(qkhvw__exsp, [ixdgk__dgp.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                kjsuv__tpen = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for yre__yuxr in arr_typ.data:
                    kjsuv__tpen += get_types(yre__yuxr)
                return kjsuv__tpen
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
            aeqp__ayc = context.compile_internal(builder, lambda a: len(a),
                types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                shfd__uqg = context.make_helper(builder, arr_typ, value=arr)
                gslz__nzyya = get_lengths(_get_map_arr_data_type(arr_typ),
                    shfd__uqg.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                ble__fcw = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                gslz__nzyya = get_lengths(arr_typ.dtype, ble__fcw.data)
                gslz__nzyya = cgutils.pack_array(builder, [ble__fcw.
                    n_arrays] + [builder.extract_value(gslz__nzyya,
                    ocncg__vjwca) for ocncg__vjwca in range(gslz__nzyya.
                    type.count)])
            elif isinstance(arr_typ, StructArrayType):
                ble__fcw = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                gslz__nzyya = []
                for ocncg__vjwca, yre__yuxr in enumerate(arr_typ.data):
                    gzzhq__bhfol = get_lengths(yre__yuxr, builder.
                        extract_value(ble__fcw.data, ocncg__vjwca))
                    gslz__nzyya += [builder.extract_value(gzzhq__bhfol,
                        mho__qer) for mho__qer in range(gzzhq__bhfol.type.
                        count)]
                gslz__nzyya = cgutils.pack_array(builder, [aeqp__ayc,
                    context.get_constant(types.int64, -1)] + gslz__nzyya)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType,
                types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                gslz__nzyya = cgutils.pack_array(builder, [aeqp__ayc])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return gslz__nzyya

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                shfd__uqg = context.make_helper(builder, arr_typ, value=arr)
                alr__tvvkw = get_buffers(_get_map_arr_data_type(arr_typ),
                    shfd__uqg.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                ble__fcw = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                jls__tcfmx = get_buffers(arr_typ.dtype, ble__fcw.data)
                rtvds__glp = context.make_array(types.Array(offset_type, 1,
                    'C'))(context, builder, ble__fcw.offsets)
                mlwn__tha = builder.bitcast(rtvds__glp.data, lir.IntType(8)
                    .as_pointer())
                tou__kfp = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, ble__fcw.null_bitmap)
                miec__yjxy = builder.bitcast(tou__kfp.data, lir.IntType(8).
                    as_pointer())
                alr__tvvkw = cgutils.pack_array(builder, [mlwn__tha,
                    miec__yjxy] + [builder.extract_value(jls__tcfmx,
                    ocncg__vjwca) for ocncg__vjwca in range(jls__tcfmx.type
                    .count)])
            elif isinstance(arr_typ, StructArrayType):
                ble__fcw = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                jls__tcfmx = []
                for ocncg__vjwca, yre__yuxr in enumerate(arr_typ.data):
                    jeocn__bnc = get_buffers(yre__yuxr, builder.
                        extract_value(ble__fcw.data, ocncg__vjwca))
                    jls__tcfmx += [builder.extract_value(jeocn__bnc,
                        mho__qer) for mho__qer in range(jeocn__bnc.type.count)]
                tou__kfp = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, ble__fcw.null_bitmap)
                miec__yjxy = builder.bitcast(tou__kfp.data, lir.IntType(8).
                    as_pointer())
                alr__tvvkw = cgutils.pack_array(builder, [miec__yjxy] +
                    jls__tcfmx)
            elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
                ) or arr_typ in (boolean_array, datetime_date_array_type):
                pid__bip = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    pid__bip = int128_type
                elif arr_typ == datetime_date_array_type:
                    pid__bip = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                kfjea__rhuxg = context.make_array(types.Array(pid__bip, 1, 'C')
                    )(context, builder, arr.data)
                tou__kfp = context.make_array(types.Array(types.uint8, 1, 'C')
                    )(context, builder, arr.null_bitmap)
                yfj__klxla = builder.bitcast(kfjea__rhuxg.data, lir.IntType
                    (8).as_pointer())
                miec__yjxy = builder.bitcast(tou__kfp.data, lir.IntType(8).
                    as_pointer())
                alr__tvvkw = cgutils.pack_array(builder, [miec__yjxy,
                    yfj__klxla])
            elif arr_typ in (string_array_type, binary_array_type):
                ble__fcw = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                uev__vicjp = context.make_helper(builder, offset_arr_type,
                    ble__fcw.offsets).data
                cpv__ictqs = context.make_helper(builder, char_arr_type,
                    ble__fcw.data).data
                jgts__vdgih = context.make_helper(builder,
                    null_bitmap_arr_type, ble__fcw.null_bitmap).data
                alr__tvvkw = cgutils.pack_array(builder, [builder.bitcast(
                    uev__vicjp, lir.IntType(8).as_pointer()), builder.
                    bitcast(jgts__vdgih, lir.IntType(8).as_pointer()),
                    builder.bitcast(cpv__ictqs, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                yfj__klxla = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                xqqn__fvpk = lir.Constant(lir.IntType(8).as_pointer(), None)
                alr__tvvkw = cgutils.pack_array(builder, [xqqn__fvpk,
                    yfj__klxla])
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return alr__tvvkw

        def get_field_names(arr_typ):
            wuo__jrs = []
            if isinstance(arr_typ, StructArrayType):
                for kzvlh__uuhf, fqzl__mno in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    wuo__jrs.append(kzvlh__uuhf)
                    wuo__jrs += get_field_names(fqzl__mno)
            elif isinstance(arr_typ, ArrayItemArrayType):
                wuo__jrs += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                wuo__jrs += get_field_names(_get_map_arr_data_type(arr_typ))
            return wuo__jrs
        kjsuv__tpen = get_types(arr_type)
        fpvmq__dqgs = cgutils.pack_array(builder, [context.get_constant(
            types.int32, t) for t in kjsuv__tpen])
        qjsqg__xay = cgutils.alloca_once_value(builder, fpvmq__dqgs)
        gslz__nzyya = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, gslz__nzyya)
        alr__tvvkw = get_buffers(arr_type, in_arr)
        pdris__pec = cgutils.alloca_once_value(builder, alr__tvvkw)
        wuo__jrs = get_field_names(arr_type)
        if len(wuo__jrs) == 0:
            wuo__jrs = ['irrelevant']
        mnp__mvq = cgutils.pack_array(builder, [context.insert_const_string
            (builder.module, a) for a in wuo__jrs])
        pku__jzjn = cgutils.alloca_once_value(builder, mnp__mvq)
        if isinstance(arr_type, MapArrayType):
            cxj__fadw = _get_map_arr_data_type(arr_type)
            yuv__niy = context.make_helper(builder, arr_type, value=in_arr)
            vsgct__glsbh = yuv__niy.data
        else:
            cxj__fadw = arr_type
            vsgct__glsbh = in_arr
        yvb__isbpq = context.make_helper(builder, cxj__fadw, vsgct__glsbh)
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='nested_array_to_info')
        obo__gpw = builder.call(qkhvw__exsp, [builder.bitcast(qjsqg__xay,
            lir.IntType(32).as_pointer()), builder.bitcast(pdris__pec, lir.
            IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            pku__jzjn, lir.IntType(8).as_pointer()), yvb__isbpq.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return obo__gpw
    if arr_type in (string_array_type, binary_array_type):
        yxn__kpizf = context.make_helper(builder, arr_type, in_arr)
        mzyb__djfc = ArrayItemArrayType(char_arr_type)
        ixdgk__dgp = context.make_helper(builder, mzyb__djfc, yxn__kpizf.data)
        ble__fcw = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        uev__vicjp = context.make_helper(builder, offset_arr_type, ble__fcw
            .offsets).data
        cpv__ictqs = context.make_helper(builder, char_arr_type, ble__fcw.data
            ).data
        jgts__vdgih = context.make_helper(builder, null_bitmap_arr_type,
            ble__fcw.null_bitmap).data
        req__yvahk = builder.zext(builder.load(builder.gep(uev__vicjp, [
            ble__fcw.n_arrays])), lir.IntType(64))
        hsn__ysib = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='string_array_to_info')
        return builder.call(qkhvw__exsp, [ble__fcw.n_arrays, req__yvahk,
            cpv__ictqs, uev__vicjp, jgts__vdgih, ixdgk__dgp.meminfo, hsn__ysib]
            )
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        uyp__otkz = arr.data
        bbrd__aiacc = arr.indices
        sig = array_info_type(arr_type.data)
        pywqh__zhub = array_to_info_codegen(context, builder, sig, (
            uyp__otkz,), False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        gst__wvhrh = array_to_info_codegen(context, builder, sig, (
            bbrd__aiacc,), False)
        kxq__ecou = cgutils.create_struct_proxy(bodo.libs.dict_arr_ext.
            dict_indices_arr_type)(context, builder, bbrd__aiacc)
        miec__yjxy = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, kxq__ecou.null_bitmap).data
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='dict_str_array_to_info')
        rxfnw__unx = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        return builder.call(qkhvw__exsp, [pywqh__zhub, gst__wvhrh, builder.
            bitcast(miec__yjxy, lir.IntType(8).as_pointer()), rxfnw__unx])
    mdtp__rlwyi = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        otyrb__zzx = context.compile_internal(builder, lambda a: len(a.
            dtype.categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        apl__wpu = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(apl__wpu, 1, 'C')
        mdtp__rlwyi = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if mdtp__rlwyi:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        aeqp__ayc = builder.extract_value(arr.shape, 0)
        alg__eiyu = arr_type.dtype
        kgj__nwllh = numba_to_c_type(alg__eiyu)
        xtlew__fdxh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), kgj__nwllh))
        if mdtp__rlwyi:
            uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(64), lir.IntType(8).as_pointer()])
            qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
                uttzu__pozcc, name='categorical_array_to_info')
            return builder.call(qkhvw__exsp, [aeqp__ayc, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                xtlew__fdxh), otyrb__zzx, arr.meminfo])
        else:
            uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer()])
            qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
                uttzu__pozcc, name='numpy_array_to_info')
            return builder.call(qkhvw__exsp, [aeqp__ayc, builder.bitcast(
                arr.data, lir.IntType(8).as_pointer()), builder.load(
                xtlew__fdxh), arr.meminfo])
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        alg__eiyu = arr_type.dtype
        pid__bip = alg__eiyu
        if isinstance(arr_type, DecimalArrayType):
            pid__bip = int128_type
        if arr_type == datetime_date_array_type:
            pid__bip = types.int64
        kfjea__rhuxg = context.make_array(types.Array(pid__bip, 1, 'C'))(
            context, builder, arr.data)
        aeqp__ayc = builder.extract_value(kfjea__rhuxg.shape, 0)
        hkkl__jjdt = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        kgj__nwllh = numba_to_c_type(alg__eiyu)
        xtlew__fdxh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), kgj__nwllh))
        if isinstance(arr_type, DecimalArrayType):
            uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32), lir.
                IntType(32)])
            qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
                uttzu__pozcc, name='decimal_array_to_info')
            return builder.call(qkhvw__exsp, [aeqp__ayc, builder.bitcast(
                kfjea__rhuxg.data, lir.IntType(8).as_pointer()), builder.
                load(xtlew__fdxh), builder.bitcast(hkkl__jjdt.data, lir.
                IntType(8).as_pointer()), kfjea__rhuxg.meminfo, hkkl__jjdt.
                meminfo, context.get_constant(types.int32, arr_type.
                precision), context.get_constant(types.int32, arr_type.scale)])
        else:
            uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer()])
            qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
                uttzu__pozcc, name='nullable_array_to_info')
            return builder.call(qkhvw__exsp, [aeqp__ayc, builder.bitcast(
                kfjea__rhuxg.data, lir.IntType(8).as_pointer()), builder.
                load(xtlew__fdxh), builder.bitcast(hkkl__jjdt.data, lir.
                IntType(8).as_pointer()), kfjea__rhuxg.meminfo, hkkl__jjdt.
                meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        cskg__pmqh = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        btclv__gxbs = context.make_array(arr_type.arr_type)(context,
            builder, arr.right)
        aeqp__ayc = builder.extract_value(cskg__pmqh.shape, 0)
        kgj__nwllh = numba_to_c_type(arr_type.arr_type.dtype)
        xtlew__fdxh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), kgj__nwllh))
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='interval_array_to_info')
        return builder.call(qkhvw__exsp, [aeqp__ayc, builder.bitcast(
            cskg__pmqh.data, lir.IntType(8).as_pointer()), builder.bitcast(
            btclv__gxbs.data, lir.IntType(8).as_pointer()), builder.load(
            xtlew__fdxh), cskg__pmqh.meminfo, btclv__gxbs.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    uoq__ijq = cgutils.alloca_once(builder, lir.IntType(64))
    yfj__klxla = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    pmgh__sagg = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    uttzu__pozcc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
        uttzu__pozcc, name='info_to_numpy_array')
    builder.call(qkhvw__exsp, [in_info, uoq__ijq, yfj__klxla, pmgh__sagg])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    kte__wvjxd = context.get_value_type(types.intp)
    kxs__ecj = cgutils.pack_array(builder, [builder.load(uoq__ijq)], ty=
        kte__wvjxd)
    qyo__bveit = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    kuv__fqbj = cgutils.pack_array(builder, [qyo__bveit], ty=kte__wvjxd)
    cpv__ictqs = builder.bitcast(builder.load(yfj__klxla), context.
        get_data_type(arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=cpv__ictqs, shape=kxs__ecj,
        strides=kuv__fqbj, itemsize=qyo__bveit, meminfo=builder.load(
        pmgh__sagg))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    uksq__eds = context.make_helper(builder, arr_type)
    uttzu__pozcc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
        uttzu__pozcc, name='info_to_list_string_array')
    builder.call(qkhvw__exsp, [in_info, uksq__eds._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return uksq__eds._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    hqhkd__bvbr = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        aoqe__vjmc = lengths_pos
        xdggd__cif = infos_pos
        hxl__jyl, lengths_pos, infos_pos = nested_to_array(context, builder,
            arr_typ.dtype, lengths_ptr, array_infos_ptr, lengths_pos + 1, 
            infos_pos + 2)
        biyl__yeog = ArrayItemArrayPayloadType(arr_typ)
        imrep__sya = context.get_data_type(biyl__yeog)
        nds__vfiai = context.get_abi_sizeof(imrep__sya)
        uuyv__dak = define_array_item_dtor(context, builder, arr_typ,
            biyl__yeog)
        eaia__fkkt = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, nds__vfiai), uuyv__dak)
        qlefj__rsrf = context.nrt.meminfo_data(builder, eaia__fkkt)
        soj__kxj = builder.bitcast(qlefj__rsrf, imrep__sya.as_pointer())
        ble__fcw = cgutils.create_struct_proxy(biyl__yeog)(context, builder)
        ble__fcw.n_arrays = builder.extract_value(builder.load(lengths_ptr),
            aoqe__vjmc)
        ble__fcw.data = hxl__jyl
        qgi__kzr = builder.load(array_infos_ptr)
        jpe__pgyf = builder.bitcast(builder.extract_value(qgi__kzr,
            xdggd__cif), hqhkd__bvbr)
        ble__fcw.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, jpe__pgyf)
        rixlx__ftrvv = builder.bitcast(builder.extract_value(qgi__kzr, 
            xdggd__cif + 1), hqhkd__bvbr)
        ble__fcw.null_bitmap = _lower_info_to_array_numpy(types.Array(types
            .uint8, 1, 'C'), context, builder, rixlx__ftrvv)
        builder.store(ble__fcw._getvalue(), soj__kxj)
        ixdgk__dgp = context.make_helper(builder, arr_typ)
        ixdgk__dgp.meminfo = eaia__fkkt
        return ixdgk__dgp._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        ujyc__zpytz = []
        xdggd__cif = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for fut__fnfqf in arr_typ.data:
            hxl__jyl, lengths_pos, infos_pos = nested_to_array(context,
                builder, fut__fnfqf, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            ujyc__zpytz.append(hxl__jyl)
        biyl__yeog = StructArrayPayloadType(arr_typ.data)
        imrep__sya = context.get_value_type(biyl__yeog)
        nds__vfiai = context.get_abi_sizeof(imrep__sya)
        uuyv__dak = define_struct_arr_dtor(context, builder, arr_typ,
            biyl__yeog)
        eaia__fkkt = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, nds__vfiai), uuyv__dak)
        qlefj__rsrf = context.nrt.meminfo_data(builder, eaia__fkkt)
        soj__kxj = builder.bitcast(qlefj__rsrf, imrep__sya.as_pointer())
        ble__fcw = cgutils.create_struct_proxy(biyl__yeog)(context, builder)
        ble__fcw.data = cgutils.pack_array(builder, ujyc__zpytz
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, ujyc__zpytz)
        qgi__kzr = builder.load(array_infos_ptr)
        rixlx__ftrvv = builder.bitcast(builder.extract_value(qgi__kzr,
            xdggd__cif), hqhkd__bvbr)
        ble__fcw.null_bitmap = _lower_info_to_array_numpy(types.Array(types
            .uint8, 1, 'C'), context, builder, rixlx__ftrvv)
        builder.store(ble__fcw._getvalue(), soj__kxj)
        sfpoq__smgdt = context.make_helper(builder, arr_typ)
        sfpoq__smgdt.meminfo = eaia__fkkt
        return sfpoq__smgdt._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        qgi__kzr = builder.load(array_infos_ptr)
        ykn__aeews = builder.bitcast(builder.extract_value(qgi__kzr,
            infos_pos), hqhkd__bvbr)
        yxn__kpizf = context.make_helper(builder, arr_typ)
        mzyb__djfc = ArrayItemArrayType(char_arr_type)
        ixdgk__dgp = context.make_helper(builder, mzyb__djfc)
        uttzu__pozcc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='info_to_string_array')
        builder.call(qkhvw__exsp, [ykn__aeews, ixdgk__dgp._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        yxn__kpizf.data = ixdgk__dgp._getvalue()
        return yxn__kpizf._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        qgi__kzr = builder.load(array_infos_ptr)
        oammc__muq = builder.bitcast(builder.extract_value(qgi__kzr, 
            infos_pos + 1), hqhkd__bvbr)
        return _lower_info_to_array_numpy(arr_typ, context, builder, oammc__muq
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, DecimalArrayType)
        ) or arr_typ in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        pid__bip = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            pid__bip = int128_type
        elif arr_typ == datetime_date_array_type:
            pid__bip = types.int64
        qgi__kzr = builder.load(array_infos_ptr)
        rixlx__ftrvv = builder.bitcast(builder.extract_value(qgi__kzr,
            infos_pos), hqhkd__bvbr)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, rixlx__ftrvv)
        oammc__muq = builder.bitcast(builder.extract_value(qgi__kzr, 
            infos_pos + 1), hqhkd__bvbr)
        arr.data = _lower_info_to_array_numpy(types.Array(pid__bip, 1, 'C'),
            context, builder, oammc__muq)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, kkbtq__hkk = args
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
                return 1 + sum([get_num_arrays(fut__fnfqf) for fut__fnfqf in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(fut__fnfqf) for fut__fnfqf in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            iigqv__jxc = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            iigqv__jxc = _get_map_arr_data_type(arr_type)
        else:
            iigqv__jxc = arr_type
        llv__xdy = get_num_arrays(iigqv__jxc)
        gslz__nzyya = cgutils.pack_array(builder, [lir.Constant(lir.IntType
            (64), 0) for kkbtq__hkk in range(llv__xdy)])
        lengths_ptr = cgutils.alloca_once_value(builder, gslz__nzyya)
        xqqn__fvpk = lir.Constant(lir.IntType(8).as_pointer(), None)
        tjrjp__nhj = cgutils.pack_array(builder, [xqqn__fvpk for kkbtq__hkk in
            range(get_num_infos(iigqv__jxc))])
        array_infos_ptr = cgutils.alloca_once_value(builder, tjrjp__nhj)
        uttzu__pozcc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='info_to_nested_array')
        builder.call(qkhvw__exsp, [in_info, builder.bitcast(lengths_ptr,
            lir.IntType(64).as_pointer()), builder.bitcast(array_infos_ptr,
            lir.IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, kkbtq__hkk, kkbtq__hkk = nested_to_array(context, builder,
            iigqv__jxc, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            rauh__lcp = context.make_helper(builder, arr_type)
            rauh__lcp.data = arr
            context.nrt.incref(builder, iigqv__jxc, arr)
            arr = rauh__lcp._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, iigqv__jxc)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        yxn__kpizf = context.make_helper(builder, arr_type)
        mzyb__djfc = ArrayItemArrayType(char_arr_type)
        ixdgk__dgp = context.make_helper(builder, mzyb__djfc)
        uttzu__pozcc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='info_to_string_array')
        builder.call(qkhvw__exsp, [in_info, ixdgk__dgp._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        yxn__kpizf.data = ixdgk__dgp._getvalue()
        return yxn__kpizf._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='get_nested_info')
        pywqh__zhub = builder.call(qkhvw__exsp, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        gst__wvhrh = builder.call(qkhvw__exsp, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        xcue__rgm = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        xcue__rgm.data = info_to_array_codegen(context, builder, sig, (
            pywqh__zhub, context.get_constant_null(arr_type.data)))
        abe__fqksa = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = abe__fqksa(array_info_type, abe__fqksa)
        xcue__rgm.indices = info_to_array_codegen(context, builder, sig, (
            gst__wvhrh, context.get_constant_null(abe__fqksa)))
        uttzu__pozcc = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='get_has_global_dictionary')
        rxfnw__unx = builder.call(qkhvw__exsp, [in_info])
        xcue__rgm.has_global_dictionary = builder.trunc(rxfnw__unx, cgutils
            .bool_t)
        return xcue__rgm._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        apl__wpu = get_categories_int_type(arr_type.dtype)
        tfz__vuj = types.Array(apl__wpu, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(tfz__vuj, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            djd__ucfw = pd.CategoricalDtype(arr_type.dtype.categories,
                is_ordered).categories.values
            new_cats_tup = MetaType(tuple(djd__ucfw))
            int_type = arr_type.dtype.int_type
            oow__qwad = bodo.typeof(djd__ucfw)
            fvpca__gywh = context.get_constant_generic(builder, oow__qwad,
                djd__ucfw)
            alg__eiyu = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(oow__qwad), [fvpca__gywh])
        else:
            alg__eiyu = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, alg__eiyu)
        out_arr.dtype = alg__eiyu
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        cpv__ictqs = _lower_info_to_array_numpy(arr_type.data_array_type,
            context, builder, in_info)
        arr.data = cpv__ictqs
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, DecimalArrayType)
        ) or arr_type in (boolean_array, datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        pid__bip = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            pid__bip = int128_type
        elif arr_type == datetime_date_array_type:
            pid__bip = types.int64
        dppm__lad = types.Array(pid__bip, 1, 'C')
        kfjea__rhuxg = context.make_array(dppm__lad)(context, builder)
        mci__zuej = types.Array(types.uint8, 1, 'C')
        uamp__jfpp = context.make_array(mci__zuej)(context, builder)
        uoq__ijq = cgutils.alloca_once(builder, lir.IntType(64))
        mxem__afgqe = cgutils.alloca_once(builder, lir.IntType(64))
        yfj__klxla = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        fsm__bxay = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        pmgh__sagg = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        dsy__zimrw = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        uttzu__pozcc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='info_to_nullable_array')
        builder.call(qkhvw__exsp, [in_info, uoq__ijq, mxem__afgqe,
            yfj__klxla, fsm__bxay, pmgh__sagg, dsy__zimrw])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        kte__wvjxd = context.get_value_type(types.intp)
        kxs__ecj = cgutils.pack_array(builder, [builder.load(uoq__ijq)], ty
            =kte__wvjxd)
        qyo__bveit = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(pid__bip)))
        kuv__fqbj = cgutils.pack_array(builder, [qyo__bveit], ty=kte__wvjxd)
        cpv__ictqs = builder.bitcast(builder.load(yfj__klxla), context.
            get_data_type(pid__bip).as_pointer())
        numba.np.arrayobj.populate_array(kfjea__rhuxg, data=cpv__ictqs,
            shape=kxs__ecj, strides=kuv__fqbj, itemsize=qyo__bveit, meminfo
            =builder.load(pmgh__sagg))
        arr.data = kfjea__rhuxg._getvalue()
        kxs__ecj = cgutils.pack_array(builder, [builder.load(mxem__afgqe)],
            ty=kte__wvjxd)
        qyo__bveit = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        kuv__fqbj = cgutils.pack_array(builder, [qyo__bveit], ty=kte__wvjxd)
        cpv__ictqs = builder.bitcast(builder.load(fsm__bxay), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(uamp__jfpp, data=cpv__ictqs, shape
            =kxs__ecj, strides=kuv__fqbj, itemsize=qyo__bveit, meminfo=
            builder.load(dsy__zimrw))
        arr.null_bitmap = uamp__jfpp._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        cskg__pmqh = context.make_array(arr_type.arr_type)(context, builder)
        btclv__gxbs = context.make_array(arr_type.arr_type)(context, builder)
        uoq__ijq = cgutils.alloca_once(builder, lir.IntType(64))
        gxi__yfesp = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        vtc__ayt = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        rpxy__hbnvb = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        oki__cgr = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        uttzu__pozcc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='info_to_interval_array')
        builder.call(qkhvw__exsp, [in_info, uoq__ijq, gxi__yfesp, vtc__ayt,
            rpxy__hbnvb, oki__cgr])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        kte__wvjxd = context.get_value_type(types.intp)
        kxs__ecj = cgutils.pack_array(builder, [builder.load(uoq__ijq)], ty
            =kte__wvjxd)
        qyo__bveit = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        kuv__fqbj = cgutils.pack_array(builder, [qyo__bveit], ty=kte__wvjxd)
        mco__ycd = builder.bitcast(builder.load(gxi__yfesp), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(cskg__pmqh, data=mco__ycd, shape=
            kxs__ecj, strides=kuv__fqbj, itemsize=qyo__bveit, meminfo=
            builder.load(rpxy__hbnvb))
        arr.left = cskg__pmqh._getvalue()
        nqk__ypva = builder.bitcast(builder.load(vtc__ayt), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(btclv__gxbs, data=nqk__ypva, shape
            =kxs__ecj, strides=kuv__fqbj, itemsize=qyo__bveit, meminfo=
            builder.load(oki__cgr))
        arr.right = btclv__gxbs._getvalue()
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
        aeqp__ayc, kkbtq__hkk = args
        kgj__nwllh = numba_to_c_type(array_type.dtype)
        xtlew__fdxh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), kgj__nwllh))
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='alloc_numpy')
        return builder.call(qkhvw__exsp, [aeqp__ayc, builder.load(xtlew__fdxh)]
            )
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        aeqp__ayc, nfd__ysyff = args
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='alloc_string_array')
        return builder.call(qkhvw__exsp, [aeqp__ayc, nfd__ysyff])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    ucqf__ebbql, = args
    kats__dyvlk = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], ucqf__ebbql)
    uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer().as_pointer(), lir.IntType(64)])
    qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
        uttzu__pozcc, name='arr_info_list_to_table')
    return builder.call(qkhvw__exsp, [kats__dyvlk.data, kats__dyvlk.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='info_from_table')
        return builder.call(qkhvw__exsp, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    ktl__attcn = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        qlap__ghz, gmi__dgv, kkbtq__hkk = args
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='info_from_table')
        umiw__jwws = cgutils.create_struct_proxy(ktl__attcn)(context, builder)
        umiw__jwws.parent = cgutils.get_null_value(umiw__jwws.parent.type)
        hzt__vwry = context.make_array(table_idx_arr_t)(context, builder,
            gmi__dgv)
        rry__scra = context.get_constant(types.int64, -1)
        vaeu__mwr = context.get_constant(types.int64, 0)
        sjcq__xfb = cgutils.alloca_once_value(builder, vaeu__mwr)
        for t, nsxk__cectr in ktl__attcn.type_to_blk.items():
            hlx__glj = context.get_constant(types.int64, len(ktl__attcn.
                block_to_arr_ind[nsxk__cectr]))
            kkbtq__hkk, khy__yzmxi = ListInstance.allocate_ex(context,
                builder, types.List(t), hlx__glj)
            khy__yzmxi.size = hlx__glj
            abdh__tvhp = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(ktl__attcn.block_to_arr_ind[
                nsxk__cectr], dtype=np.int64))
            xctek__hhyv = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, abdh__tvhp)
            with cgutils.for_range(builder, hlx__glj) as jutw__drtse:
                ocncg__vjwca = jutw__drtse.index
                ehaj__fxfg = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    xctek__hhyv, ocncg__vjwca)
                zpj__ipmuw = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, hzt__vwry, ehaj__fxfg)
                rfqp__sjs = builder.icmp_unsigned('!=', zpj__ipmuw, rry__scra)
                with builder.if_else(rfqp__sjs) as (dkdq__qrzrc, fsnt__nxlr):
                    with dkdq__qrzrc:
                        voq__cjyh = builder.call(qkhvw__exsp, [qlap__ghz,
                            zpj__ipmuw])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            voq__cjyh])
                        khy__yzmxi.inititem(ocncg__vjwca, arr, incref=False)
                        aeqp__ayc = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(aeqp__ayc, sjcq__xfb)
                    with fsnt__nxlr:
                        lcao__cwnxi = context.get_constant_null(t)
                        khy__yzmxi.inititem(ocncg__vjwca, lcao__cwnxi,
                            incref=False)
            setattr(umiw__jwws, f'block_{nsxk__cectr}', khy__yzmxi.value)
        umiw__jwws.len = builder.load(sjcq__xfb)
        return umiw__jwws._getvalue()
    return ktl__attcn(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    ktl__attcn = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        yskwt__wfg, kkbtq__hkk = args
        ulof__ubrmi = cgutils.create_struct_proxy(ktl__attcn)(context,
            builder, yskwt__wfg)
        if ktl__attcn.has_runtime_cols:
            pvu__qqvgh = lir.Constant(lir.IntType(64), 0)
            for nsxk__cectr, t in enumerate(ktl__attcn.arr_types):
                vzh__oxjo = getattr(ulof__ubrmi, f'block_{nsxk__cectr}')
                yjn__nysxp = ListInstance(context, builder, types.List(t),
                    vzh__oxjo)
                pvu__qqvgh = builder.add(pvu__qqvgh, yjn__nysxp.size)
        else:
            pvu__qqvgh = lir.Constant(lir.IntType(64), len(ktl__attcn.
                arr_types))
        kkbtq__hkk, lcrsy__oax = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), pvu__qqvgh)
        lcrsy__oax.size = pvu__qqvgh
        if ktl__attcn.has_runtime_cols:
            jgkv__jihe = lir.Constant(lir.IntType(64), 0)
            for nsxk__cectr, t in enumerate(ktl__attcn.arr_types):
                vzh__oxjo = getattr(ulof__ubrmi, f'block_{nsxk__cectr}')
                yjn__nysxp = ListInstance(context, builder, types.List(t),
                    vzh__oxjo)
                hlx__glj = yjn__nysxp.size
                with cgutils.for_range(builder, hlx__glj) as jutw__drtse:
                    ocncg__vjwca = jutw__drtse.index
                    arr = yjn__nysxp.getitem(ocncg__vjwca)
                    gctqq__pret = signature(array_info_type, t)
                    mfhb__cqlir = arr,
                    kcvp__jnw = array_to_info_codegen(context, builder,
                        gctqq__pret, mfhb__cqlir)
                    lcrsy__oax.inititem(builder.add(jgkv__jihe,
                        ocncg__vjwca), kcvp__jnw, incref=False)
                jgkv__jihe = builder.add(jgkv__jihe, hlx__glj)
        else:
            for t, nsxk__cectr in ktl__attcn.type_to_blk.items():
                hlx__glj = context.get_constant(types.int64, len(ktl__attcn
                    .block_to_arr_ind[nsxk__cectr]))
                vzh__oxjo = getattr(ulof__ubrmi, f'block_{nsxk__cectr}')
                yjn__nysxp = ListInstance(context, builder, types.List(t),
                    vzh__oxjo)
                abdh__tvhp = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(ktl__attcn.
                    block_to_arr_ind[nsxk__cectr], dtype=np.int64))
                xctek__hhyv = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, abdh__tvhp)
                with cgutils.for_range(builder, hlx__glj) as jutw__drtse:
                    ocncg__vjwca = jutw__drtse.index
                    ehaj__fxfg = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        xctek__hhyv, ocncg__vjwca)
                    zithm__cbaif = signature(types.none, ktl__attcn, types.
                        List(t), types.int64, types.int64)
                    rsbv__zds = yskwt__wfg, vzh__oxjo, ocncg__vjwca, ehaj__fxfg
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, zithm__cbaif, rsbv__zds)
                    arr = yjn__nysxp.getitem(ocncg__vjwca)
                    gctqq__pret = signature(array_info_type, t)
                    mfhb__cqlir = arr,
                    kcvp__jnw = array_to_info_codegen(context, builder,
                        gctqq__pret, mfhb__cqlir)
                    lcrsy__oax.inititem(ehaj__fxfg, kcvp__jnw, incref=False)
        mvzzc__mnasn = lcrsy__oax.value
        thqa__wodb = signature(table_type, types.List(array_info_type))
        orhl__xfk = mvzzc__mnasn,
        qlap__ghz = arr_info_list_to_table_codegen(context, builder,
            thqa__wodb, orhl__xfk)
        context.nrt.decref(builder, types.List(array_info_type), mvzzc__mnasn)
        return qlap__ghz
    return table_type(ktl__attcn, py_table_type_t), codegen


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        uttzu__pozcc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='delete_table')
        builder.call(qkhvw__exsp, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='shuffle_table')
        obo__gpw = builder.call(qkhvw__exsp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return obo__gpw
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
        uttzu__pozcc = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='delete_shuffle_info')
        return builder.call(qkhvw__exsp, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='reverse_shuffle_table')
        return builder.call(qkhvw__exsp, args)
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
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1), lir.IntType(1), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(8).as_pointer(), lir.IntType(64)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='hash_join_table')
        obo__gpw = builder.call(qkhvw__exsp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return obo__gpw
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
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='sort_values_table')
        obo__gpw = builder.call(qkhvw__exsp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return obo__gpw
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='sample_table')
        obo__gpw = builder.call(qkhvw__exsp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return obo__gpw
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='shuffle_renormalization')
        obo__gpw = builder.call(qkhvw__exsp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return obo__gpw
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='shuffle_renormalization_group')
        obo__gpw = builder.call(qkhvw__exsp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return obo__gpw
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='drop_duplicates_table')
        obo__gpw = builder.call(qkhvw__exsp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return obo__gpw
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
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='pivot_groupby_and_aggregate')
        obo__gpw = builder.call(qkhvw__exsp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return obo__gpw
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
        uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        qkhvw__exsp = cgutils.get_or_insert_function(builder.module,
            uttzu__pozcc, name='groupby_and_aggregate')
        obo__gpw = builder.call(qkhvw__exsp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return obo__gpw
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
    mudrb__wbk = array_to_info(in_arr)
    nny__mxnt = array_to_info(in_values)
    sdjfr__lur = array_to_info(out_arr)
    sihx__jnpul = arr_info_list_to_table([mudrb__wbk, nny__mxnt, sdjfr__lur])
    _array_isin(sdjfr__lur, mudrb__wbk, nny__mxnt, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(sihx__jnpul)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, pat, out_arr):
    mudrb__wbk = array_to_info(in_arr)
    sdjfr__lur = array_to_info(out_arr)
    _get_search_regex(mudrb__wbk, case, pat, sdjfr__lur)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    bcvj__ewzv = col_array_typ.dtype
    if isinstance(bcvj__ewzv, types.Number) or bcvj__ewzv in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                umiw__jwws, dyo__jmh = args
                umiw__jwws = builder.bitcast(umiw__jwws, lir.IntType(8).
                    as_pointer().as_pointer())
                gzh__zsat = lir.Constant(lir.IntType(64), c_ind)
                iyda__yrhra = builder.load(builder.gep(umiw__jwws, [gzh__zsat])
                    )
                iyda__yrhra = builder.bitcast(iyda__yrhra, context.
                    get_data_type(bcvj__ewzv).as_pointer())
                return builder.load(builder.gep(iyda__yrhra, [dyo__jmh]))
            return bcvj__ewzv(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.string_array_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                umiw__jwws, dyo__jmh = args
                umiw__jwws = builder.bitcast(umiw__jwws, lir.IntType(8).
                    as_pointer().as_pointer())
                gzh__zsat = lir.Constant(lir.IntType(64), c_ind)
                iyda__yrhra = builder.load(builder.gep(umiw__jwws, [gzh__zsat])
                    )
                uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                nfr__rrpu = cgutils.get_or_insert_function(builder.module,
                    uttzu__pozcc, name='array_info_getitem')
                mnwmz__xcl = cgutils.alloca_once(builder, lir.IntType(64))
                args = iyda__yrhra, dyo__jmh, mnwmz__xcl
                yfj__klxla = builder.call(nfr__rrpu, args)
                return context.make_tuple(builder, sig.return_type, [
                    yfj__klxla, builder.load(mnwmz__xcl)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                miep__orbr = lir.Constant(lir.IntType(64), 1)
                hhpx__glx = lir.Constant(lir.IntType(64), 2)
                umiw__jwws, dyo__jmh = args
                umiw__jwws = builder.bitcast(umiw__jwws, lir.IntType(8).
                    as_pointer().as_pointer())
                gzh__zsat = lir.Constant(lir.IntType(64), c_ind)
                iyda__yrhra = builder.load(builder.gep(umiw__jwws, [gzh__zsat])
                    )
                uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                zrmv__ypsf = cgutils.get_or_insert_function(builder.module,
                    uttzu__pozcc, name='get_nested_info')
                args = iyda__yrhra, hhpx__glx
                ozcj__zmf = builder.call(zrmv__ypsf, args)
                uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                fbux__dxgr = cgutils.get_or_insert_function(builder.module,
                    uttzu__pozcc, name='array_info_getdata1')
                args = ozcj__zmf,
                dswqg__mdoa = builder.call(fbux__dxgr, args)
                dswqg__mdoa = builder.bitcast(dswqg__mdoa, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                patxq__xyad = builder.sext(builder.load(builder.gep(
                    dswqg__mdoa, [dyo__jmh])), lir.IntType(64))
                args = iyda__yrhra, miep__orbr
                ylu__imj = builder.call(zrmv__ypsf, args)
                uttzu__pozcc = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                nfr__rrpu = cgutils.get_or_insert_function(builder.module,
                    uttzu__pozcc, name='array_info_getitem')
                mnwmz__xcl = cgutils.alloca_once(builder, lir.IntType(64))
                args = ylu__imj, patxq__xyad, mnwmz__xcl
                yfj__klxla = builder.call(nfr__rrpu, args)
                return context.make_tuple(builder, sig.return_type, [
                    yfj__klxla, builder.load(mnwmz__xcl)])
            return types.Tuple([types.voidptr, types.int64])(types.voidptr,
                types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{bcvj__ewzv}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if (isinstance(col_array_dtype, bodo.libs.int_arr_ext.IntegerArrayType) or
        col_array_dtype == bodo.libs.bool_arr_ext.boolean_array or
        is_str_arr_type(col_array_dtype) or isinstance(col_array_dtype,
        types.Array) and col_array_dtype.dtype == bodo.datetime_date_type):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                uodgm__idbq, dyo__jmh = args
                uodgm__idbq = builder.bitcast(uodgm__idbq, lir.IntType(8).
                    as_pointer().as_pointer())
                gzh__zsat = lir.Constant(lir.IntType(64), c_ind)
                iyda__yrhra = builder.load(builder.gep(uodgm__idbq, [
                    gzh__zsat]))
                jgts__vdgih = builder.bitcast(iyda__yrhra, context.
                    get_data_type(types.bool_).as_pointer())
                pykzw__yvn = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    jgts__vdgih, dyo__jmh)
                cfftq__zewxm = builder.icmp_unsigned('!=', pykzw__yvn, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(cfftq__zewxm, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, types.Array):
        bcvj__ewzv = col_array_dtype.dtype
        if bcvj__ewzv in [bodo.datetime64ns, bodo.timedelta64ns]:

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    umiw__jwws, dyo__jmh = args
                    umiw__jwws = builder.bitcast(umiw__jwws, lir.IntType(8)
                        .as_pointer().as_pointer())
                    gzh__zsat = lir.Constant(lir.IntType(64), c_ind)
                    iyda__yrhra = builder.load(builder.gep(umiw__jwws, [
                        gzh__zsat]))
                    iyda__yrhra = builder.bitcast(iyda__yrhra, context.
                        get_data_type(bcvj__ewzv).as_pointer())
                    kppa__smtn = builder.load(builder.gep(iyda__yrhra, [
                        dyo__jmh]))
                    cfftq__zewxm = builder.icmp_unsigned('!=', kppa__smtn,
                        lir.Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(cfftq__zewxm, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(bcvj__ewzv, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    umiw__jwws, dyo__jmh = args
                    umiw__jwws = builder.bitcast(umiw__jwws, lir.IntType(8)
                        .as_pointer().as_pointer())
                    gzh__zsat = lir.Constant(lir.IntType(64), c_ind)
                    iyda__yrhra = builder.load(builder.gep(umiw__jwws, [
                        gzh__zsat]))
                    iyda__yrhra = builder.bitcast(iyda__yrhra, context.
                        get_data_type(bcvj__ewzv).as_pointer())
                    kppa__smtn = builder.load(builder.gep(iyda__yrhra, [
                        dyo__jmh]))
                    axbt__wklj = signature(types.bool_, bcvj__ewzv)
                    pykzw__yvn = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, axbt__wklj, (kppa__smtn,))
                    return builder.not_(builder.sext(pykzw__yvn, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
