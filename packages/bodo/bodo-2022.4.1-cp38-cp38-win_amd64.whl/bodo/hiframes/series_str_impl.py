"""
Support for Series.str methods
"""
import operator
import re
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import StringIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.split_impl import get_split_view_data_ptr, get_split_view_index, string_array_split_view_type
from bodo.libs.array import get_search_regex
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.str_arr_ext import get_utf8_size, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import str_findall_count
from bodo.utils.typing import BodoError, create_unsupported_overload, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_str_len, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error


class SeriesStrMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        rpym__ikch = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(rpym__ikch)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lngh__ftsf = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, lngh__ftsf)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        pploi__mhvun, = args
        mkrc__qsur = signature.return_type
        onx__gkfse = cgutils.create_struct_proxy(mkrc__qsur)(context, builder)
        onx__gkfse.obj = pploi__mhvun
        context.nrt.incref(builder, signature.args[0], pploi__mhvun)
        return onx__gkfse._getvalue()
    return SeriesStrMethodType(obj)(obj), codegen


def str_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.UnicodeType) and not is_overload_constant_str(
        arg):
        raise_bodo_error(
            "Series.str.{}(): parameter '{}' expected a string object, not {}"
            .format(func_name, arg_name, arg))


def int_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.Integer) and not is_overload_constant_int(arg
        ):
        raise BodoError(
            "Series.str.{}(): parameter '{}' expected an int object, not {}"
            .format(func_name, arg_name, arg))


def not_supported_arg_check(func_name, arg_name, arg, defval):
    if arg_name == 'na':
        if not isinstance(arg, types.Omitted) and (not isinstance(arg,
            float) or not np.isnan(arg)):
            raise BodoError(
                "Series.str.{}(): parameter '{}' is not supported, default: np.nan"
                .format(func_name, arg_name))
    elif not isinstance(arg, types.Omitted) and arg != defval:
        raise BodoError(
            "Series.str.{}(): parameter '{}' is not supported, default: {}"
            .format(func_name, arg_name, defval))


def common_validate_padding(func_name, width, fillchar):
    if is_overload_constant_str(fillchar):
        if get_overload_const_str_len(fillchar) != 1:
            raise BodoError(
                'Series.str.{}(): fillchar must be a character, not str'.
                format(func_name))
    elif not isinstance(fillchar, types.UnicodeType):
        raise BodoError('Series.str.{}(): fillchar must be a character, not {}'
            .format(func_name, fillchar))
    int_arg_check(func_name, 'width', width)


@overload_attribute(SeriesType, 'str')
def overload_series_str(S):
    if not (is_str_arr_type(S.data) or S.data ==
        string_array_split_view_type or isinstance(S.data, ArrayItemArrayType)
        ):
        raise_bodo_error(
            'Series.str: input should be a series of string or arrays')
    return lambda S: bodo.hiframes.series_str_impl.init_series_str_method(S)


@overload_method(SeriesStrMethodType, 'len', inline='always', no_unliteral=True
    )
def overload_str_method_len(S_str):

    def impl(S_str):
        S = S_str._obj
        bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(bwiue__cpqqs, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'split', inline='always',
    no_unliteral=True)
def overload_str_method_split(S_str, pat=None, n=-1, expand=False):
    if not is_overload_none(pat):
        str_arg_check('split', 'pat', pat)
    int_arg_check('split', 'n', n)
    not_supported_arg_check('split', 'expand', expand, False)
    if is_overload_constant_str(pat) and len(get_overload_const_str(pat)
        ) == 1 and get_overload_const_str(pat).isascii(
        ) and is_overload_constant_int(n) and get_overload_const_int(n
        ) == -1 and S_str.stype.data == string_array_type:

        def _str_split_view_impl(S_str, pat=None, n=-1, expand=False):
            S = S_str._obj
            bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
            rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(bwiue__cpqqs,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                dve__vnim, rpym__ikch)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(bwiue__cpqqs, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    gymck__cucm = S_str.stype.data
    if (gymck__cucm != string_array_split_view_type and not is_str_arr_type
        (gymck__cucm)) and not isinstance(gymck__cucm, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(gymck__cucm, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
            rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(bwiue__cpqqs, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                dve__vnim, rpym__ikch)
        return _str_get_array_impl
    if gymck__cucm == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
            rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(bwiue__cpqqs)
            smoa__ohfvh = 0
            for msw__snb in numba.parfors.parfor.internal_prange(n):
                dtm__ssth, dtm__ssth, nimk__oum = get_split_view_index(
                    bwiue__cpqqs, msw__snb, i)
                smoa__ohfvh += nimk__oum
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, smoa__ohfvh)
            for eftg__bgz in numba.parfors.parfor.internal_prange(n):
                jjvg__hrkn, kibs__txlxv, nimk__oum = get_split_view_index(
                    bwiue__cpqqs, eftg__bgz, i)
                if jjvg__hrkn == 0:
                    bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
                    bgt__lfc = get_split_view_data_ptr(bwiue__cpqqs, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr, eftg__bgz
                        )
                    bgt__lfc = get_split_view_data_ptr(bwiue__cpqqs,
                        kibs__txlxv)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    eftg__bgz, bgt__lfc, nimk__oum)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                dve__vnim, rpym__ikch)
        return _str_get_split_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(bwiue__cpqqs)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for eftg__bgz in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(bwiue__cpqqs, eftg__bgz
                ) or not len(bwiue__cpqqs[eftg__bgz]) > i >= -len(bwiue__cpqqs
                [eftg__bgz]):
                out_arr[eftg__bgz] = ''
                bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
            else:
                out_arr[eftg__bgz] = bwiue__cpqqs[eftg__bgz][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    gymck__cucm = S_str.stype.data
    if (gymck__cucm != string_array_split_view_type and gymck__cucm !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        gymck__cucm)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(hdabc__xuu)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for eftg__bgz in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(hdabc__xuu, eftg__bgz):
                out_arr[eftg__bgz] = ''
                bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
            else:
                ujs__ogb = hdabc__xuu[eftg__bgz]
                out_arr[eftg__bgz] = sep.join(ujs__ogb)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'replace', inline='always',
    no_unliteral=True)
def overload_str_method_replace(S_str, pat, repl, n=-1, case=None, flags=0,
    regex=True):
    not_supported_arg_check('replace', 'n', n, -1)
    not_supported_arg_check('replace', 'case', case, None)
    str_arg_check('replace', 'pat', pat)
    str_arg_check('replace', 'repl', repl)
    int_arg_check('replace', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_replace_dict_impl(S_str, pat, repl, n=-1, case=None, flags
            =0, regex=True):
            S = S_str._obj
            bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
            rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(bwiue__cpqqs, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                dve__vnim, rpym__ikch)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
            rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            ytj__pby = re.compile(pat, flags)
            miiip__bopn = len(bwiue__cpqqs)
            out_arr = pre_alloc_string_array(miiip__bopn, -1)
            for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
                if bodo.libs.array_kernels.isna(bwiue__cpqqs, eftg__bgz):
                    out_arr[eftg__bgz] = ''
                    bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
                    continue
                out_arr[eftg__bgz] = ytj__pby.sub(repl, bwiue__cpqqs[eftg__bgz]
                    )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                dve__vnim, rpym__ikch)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(bwiue__cpqqs)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(miiip__bopn, -1)
        for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(bwiue__cpqqs, eftg__bgz):
                out_arr[eftg__bgz] = ''
                bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
                continue
            out_arr[eftg__bgz] = bwiue__cpqqs[eftg__bgz].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    wqv__lui = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(tua__geata in pat) for tua__geata in wqv__lui])
    else:
        return True


@overload_method(SeriesStrMethodType, 'contains', no_unliteral=True)
def overload_str_method_contains(S_str, pat, case=True, flags=0, na=np.nan,
    regex=True):
    not_supported_arg_check('contains', 'na', na, np.nan)
    str_arg_check('contains', 'pat', pat)
    int_arg_check('contains', 'flags', flags)
    if not is_overload_constant_bool(regex):
        raise BodoError(
            "Series.str.contains(): 'regex' argument should be a constant boolean"
            )
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.contains(): 'case' argument should be a constant boolean"
            )
    vkj__omaj = re.IGNORECASE.value
    mrvwa__spvmy = 'def impl(\n'
    mrvwa__spvmy += (
        '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n')
    mrvwa__spvmy += '):\n'
    mrvwa__spvmy += '  S = S_str._obj\n'
    mrvwa__spvmy += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    mrvwa__spvmy += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    mrvwa__spvmy += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    mrvwa__spvmy += '  l = len(arr)\n'
    mrvwa__spvmy += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                mrvwa__spvmy += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                mrvwa__spvmy += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            mrvwa__spvmy += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        mrvwa__spvmy += """  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)
"""
    else:
        mrvwa__spvmy += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            mrvwa__spvmy += '  upper_pat = pat.upper()\n'
        mrvwa__spvmy += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        mrvwa__spvmy += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        mrvwa__spvmy += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        mrvwa__spvmy += '      else: \n'
        if is_overload_true(case):
            mrvwa__spvmy += '          out_arr[i] = pat in arr[i]\n'
        else:
            mrvwa__spvmy += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    mrvwa__spvmy += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    les__bhk = {}
    exec(mrvwa__spvmy, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': vkj__omaj, 'get_search_regex':
        get_search_regex}, les__bhk)
    impl = les__bhk['impl']
    return impl


@overload_method(SeriesStrMethodType, 'cat', no_unliteral=True)
def overload_str_method_cat(S_str, others=None, sep=None, na_rep=None, join
    ='left'):
    if not isinstance(others, DataFrameType):
        raise_bodo_error(
            "Series.str.cat(): 'others' must be a DataFrame currently")
    if not is_overload_none(sep):
        str_arg_check('cat', 'sep', sep)
    if not is_overload_constant_str(join) or get_overload_const_str(join
        ) != 'left':
        raise_bodo_error("Series.str.cat(): 'join' not supported yet")
    mrvwa__spvmy = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    mrvwa__spvmy += '  S = S_str._obj\n'
    mrvwa__spvmy += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    mrvwa__spvmy += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    mrvwa__spvmy += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    mrvwa__spvmy += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        mrvwa__spvmy += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(uiu__zkta == bodo
        .dict_str_arr_type for uiu__zkta in others.data):
        kgzut__obzbs = ', '.join(f'data{i}' for i in range(len(others.columns))
            )
        mrvwa__spvmy += f"""  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {kgzut__obzbs}), sep)
"""
    else:
        ilwm__hbgm = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        mrvwa__spvmy += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        mrvwa__spvmy += '  numba.parfors.parfor.init_prange()\n'
        mrvwa__spvmy += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        mrvwa__spvmy += f'      if {ilwm__hbgm}:\n'
        mrvwa__spvmy += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        mrvwa__spvmy += '          continue\n'
        gwuzd__rdu = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        ksoa__evmit = "''" if is_overload_none(sep) else 'sep'
        mrvwa__spvmy += (
            f'      out_arr[i] = {ksoa__evmit}.join([{gwuzd__rdu}])\n')
    mrvwa__spvmy += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    les__bhk = {}
    exec(mrvwa__spvmy, {'bodo': bodo, 'numba': numba}, les__bhk)
    impl = les__bhk['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        ytj__pby = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(miiip__bopn, np.int64)
        for i in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(ytj__pby, hdabc__xuu[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'find', inline='always', no_unliteral
    =True)
def overload_str_method_find(S_str, sub, start=0, end=None):
    str_arg_check('find', 'sub', sub)
    int_arg_check('find', 'start', start)
    if not is_overload_none(end):
        int_arg_check('find', 'end', end)

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(miiip__bopn, np.int64)
        for i in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = hdabc__xuu[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'rfind', inline='always',
    no_unliteral=True)
def overload_str_method_rfind(S_str, sub, start=0, end=None):
    str_arg_check('rfind', 'sub', sub)
    if start != 0:
        int_arg_check('rfind', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rfind', 'end', end)

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(miiip__bopn, np.int64)
        for i in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = hdabc__xuu[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'center', inline='always',
    no_unliteral=True)
def overload_str_method_center(S_str, width, fillchar=' '):
    common_validate_padding('center', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(miiip__bopn, -1)
        for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, eftg__bgz):
                out_arr[eftg__bgz] = ''
                bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
            else:
                out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'slice_replace', inline='always',
    no_unliteral=True)
def overload_str_method_slice_replace(S_str, start=0, stop=None, repl=''):
    int_arg_check('slice_replace', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice_replace', 'stop', stop)
    str_arg_check('slice_replace', 'repl', repl)

    def impl(S_str, start=0, stop=None, repl=''):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(miiip__bopn, -1)
        for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, eftg__bgz):
                bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
            else:
                if stop is not None:
                    bsoe__ohbpc = hdabc__xuu[eftg__bgz][stop:]
                else:
                    bsoe__ohbpc = ''
                out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz][:start
                    ] + repl + bsoe__ohbpc
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):

        def impl(S_str, repeats):
            S = S_str._obj
            hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
            rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
            dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            miiip__bopn = len(hdabc__xuu)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(miiip__bopn,
                -1)
            for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
                if bodo.libs.array_kernels.isna(hdabc__xuu, eftg__bgz):
                    bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
                else:
                    out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                dve__vnim, rpym__ikch)
        return impl
    elif is_overload_constant_list(repeats):
        hqve__jqo = get_overload_const_list(repeats)
        aeay__nahof = all([isinstance(dbfrh__kwr, int) for dbfrh__kwr in
            hqve__jqo])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        aeay__nahof = True
    else:
        aeay__nahof = False
    if aeay__nahof:

        def impl(S_str, repeats):
            S = S_str._obj
            hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
            rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
            dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
            sdbi__mqxbx = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            miiip__bopn = len(hdabc__xuu)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(miiip__bopn,
                -1)
            for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
                if bodo.libs.array_kernels.isna(hdabc__xuu, eftg__bgz):
                    bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
                else:
                    out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz] * sdbi__mqxbx[
                        eftg__bgz]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                dve__vnim, rpym__ikch)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


@overload_method(SeriesStrMethodType, 'ljust', inline='always',
    no_unliteral=True)
def overload_str_method_ljust(S_str, width, fillchar=' '):
    common_validate_padding('ljust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(miiip__bopn, -1)
        for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, eftg__bgz):
                out_arr[eftg__bgz] = ''
                bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
            else:
                out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz].ljust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'rjust', inline='always',
    no_unliteral=True)
def overload_str_method_rjust(S_str, width, fillchar=' '):
    common_validate_padding('rjust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(miiip__bopn, -1)
        for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, eftg__bgz):
                out_arr[eftg__bgz] = ''
                bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
            else:
                out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz].rjust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'pad', no_unliteral=True)
def overload_str_method_pad(S_str, width, side='left', fillchar=' '):
    common_validate_padding('pad', width, fillchar)
    if is_overload_constant_str(side):
        if get_overload_const_str(side) not in ['left', 'right', 'both']:
            raise BodoError('Series.str.pad(): Invalid Side')
    else:
        raise BodoError('Series.str.pad(): Invalid Side')

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(miiip__bopn, -1)
        for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, eftg__bgz):
                out_arr[eftg__bgz] = ''
                bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
            elif side == 'left':
                out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)

    def impl(S_str, width):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(miiip__bopn, -1)
        for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, eftg__bgz):
                out_arr[eftg__bgz] = ''
                bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
            else:
                out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'slice', no_unliteral=True)
def overload_str_method_slice(S_str, start=None, stop=None, step=None):
    if not is_overload_none(start):
        int_arg_check('slice', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice', 'stop', stop)
    if not is_overload_none(step):
        int_arg_check('slice', 'step', step)

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(miiip__bopn, -1)
        for eftg__bgz in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, eftg__bgz):
                out_arr[eftg__bgz] = ''
                bodo.libs.array_kernels.setna(out_arr, eftg__bgz)
            else:
                out_arr[eftg__bgz] = hdabc__xuu[eftg__bgz][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
            rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(bwiue__cpqqs,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                dve__vnim, rpym__ikch)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(miiip__bopn)
        for i in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = hdabc__xuu[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
            dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
            rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(bwiue__cpqqs, pat, na
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                dve__vnim, rpym__ikch)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        hdabc__xuu = bodo.hiframes.pd_series_ext.get_series_data(S)
        rpym__ikch = bodo.hiframes.pd_series_ext.get_series_name(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        miiip__bopn = len(hdabc__xuu)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(miiip__bopn)
        for i in numba.parfors.parfor.internal_prange(miiip__bopn):
            if bodo.libs.array_kernels.isna(hdabc__xuu, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = hdabc__xuu[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, dve__vnim,
            rpym__ikch)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_str_method_getitem(S_str, ind):
    if not isinstance(S_str, SeriesStrMethodType):
        return
    if not isinstance(types.unliteral(ind), (types.SliceType, types.Integer)):
        raise BodoError(
            'index input to Series.str[] should be a slice or an integer')
    if isinstance(ind, types.SliceType):
        return lambda S_str, ind: S_str.slice(ind.start, ind.stop, ind.step)
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda S_str, ind: S_str.get(ind)


@overload_method(SeriesStrMethodType, 'extract', inline='always',
    no_unliteral=True)
def overload_str_method_extract(S_str, pat, flags=0, expand=True):
    if not is_overload_constant_bool(expand):
        raise BodoError(
            "Series.str.extract(): 'expand' argument should be a constant bool"
            )
    mpjx__nkfod, regex = _get_column_names_from_regex(pat, flags, 'extract')
    hbr__rdodl = len(mpjx__nkfod)
    mrvwa__spvmy = 'def impl(S_str, pat, flags=0, expand=True):\n'
    mrvwa__spvmy += '  regex = re.compile(pat, flags=flags)\n'
    mrvwa__spvmy += '  S = S_str._obj\n'
    mrvwa__spvmy += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    mrvwa__spvmy += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    mrvwa__spvmy += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    mrvwa__spvmy += '  numba.parfors.parfor.init_prange()\n'
    mrvwa__spvmy += '  n = len(str_arr)\n'
    for i in range(hbr__rdodl):
        mrvwa__spvmy += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    mrvwa__spvmy += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    mrvwa__spvmy += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(hbr__rdodl):
        mrvwa__spvmy += "          out_arr_{}[j] = ''\n".format(i)
        mrvwa__spvmy += (
            '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    mrvwa__spvmy += '      else:\n'
    mrvwa__spvmy += '          m = regex.search(str_arr[j])\n'
    mrvwa__spvmy += '          if m:\n'
    mrvwa__spvmy += '            g = m.groups()\n'
    for i in range(hbr__rdodl):
        mrvwa__spvmy += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    mrvwa__spvmy += '          else:\n'
    for i in range(hbr__rdodl):
        mrvwa__spvmy += "            out_arr_{}[j] = ''\n".format(i)
        mrvwa__spvmy += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        rpym__ikch = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        mrvwa__spvmy += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(rpym__ikch))
        les__bhk = {}
        exec(mrvwa__spvmy, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, les__bhk)
        impl = les__bhk['impl']
        return impl
    crmou__jjdh = ', '.join('out_arr_{}'.format(i) for i in range(hbr__rdodl))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(mrvwa__spvmy,
        mpjx__nkfod, crmou__jjdh, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    mpjx__nkfod, dtm__ssth = _get_column_names_from_regex(pat, flags,
        'extractall')
    hbr__rdodl = len(mpjx__nkfod)
    pmow__abyt = isinstance(S_str.stype.index, StringIndexType)
    mrvwa__spvmy = 'def impl(S_str, pat, flags=0):\n'
    mrvwa__spvmy += '  regex = re.compile(pat, flags=flags)\n'
    mrvwa__spvmy += '  S = S_str._obj\n'
    mrvwa__spvmy += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    mrvwa__spvmy += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    mrvwa__spvmy += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    mrvwa__spvmy += (
        '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    mrvwa__spvmy += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    mrvwa__spvmy += '  numba.parfors.parfor.init_prange()\n'
    mrvwa__spvmy += '  n = len(str_arr)\n'
    mrvwa__spvmy += '  out_n_l = [0]\n'
    for i in range(hbr__rdodl):
        mrvwa__spvmy += '  num_chars_{} = 0\n'.format(i)
    if pmow__abyt:
        mrvwa__spvmy += '  index_num_chars = 0\n'
    mrvwa__spvmy += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if pmow__abyt:
        mrvwa__spvmy += (
            '      index_num_chars += get_utf8_size(index_arr[i])\n')
    mrvwa__spvmy += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    mrvwa__spvmy += '          continue\n'
    mrvwa__spvmy += '      m = regex.findall(str_arr[i])\n'
    mrvwa__spvmy += '      out_n_l[0] += len(m)\n'
    for i in range(hbr__rdodl):
        mrvwa__spvmy += '      l_{} = 0\n'.format(i)
    mrvwa__spvmy += '      for s in m:\n'
    for i in range(hbr__rdodl):
        mrvwa__spvmy += '        l_{} += get_utf8_size(s{})\n'.format(i, 
            '[{}]'.format(i) if hbr__rdodl > 1 else '')
    for i in range(hbr__rdodl):
        mrvwa__spvmy += '      num_chars_{0} += l_{0}\n'.format(i)
    mrvwa__spvmy += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(hbr__rdodl):
        mrvwa__spvmy += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if pmow__abyt:
        mrvwa__spvmy += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        mrvwa__spvmy += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    mrvwa__spvmy += '  out_match_arr = np.empty(out_n, np.int64)\n'
    mrvwa__spvmy += '  out_ind = 0\n'
    mrvwa__spvmy += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    mrvwa__spvmy += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    mrvwa__spvmy += '          continue\n'
    mrvwa__spvmy += '      m = regex.findall(str_arr[j])\n'
    mrvwa__spvmy += '      for k, s in enumerate(m):\n'
    for i in range(hbr__rdodl):
        mrvwa__spvmy += (
            """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
            .format(i, '[{}]'.format(i) if hbr__rdodl > 1 else ''))
    mrvwa__spvmy += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    mrvwa__spvmy += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    mrvwa__spvmy += '        out_ind += 1\n'
    mrvwa__spvmy += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    mrvwa__spvmy += (
        "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    crmou__jjdh = ', '.join('out_arr_{}'.format(i) for i in range(hbr__rdodl))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(mrvwa__spvmy,
        mpjx__nkfod, crmou__jjdh, 'out_index', extra_globals={
        'get_utf8_size': get_utf8_size, 're': re})
    return impl


def _get_column_names_from_regex(pat, flags, func_name):
    if not is_overload_constant_str(pat):
        raise BodoError(
            "Series.str.{}(): 'pat' argument should be a constant string".
            format(func_name))
    if not is_overload_constant_int(flags):
        raise BodoError(
            "Series.str.{}(): 'flags' argument should be a constant int".
            format(func_name))
    pat = get_overload_const_str(pat)
    flags = get_overload_const_int(flags)
    regex = re.compile(pat, flags=flags)
    if regex.groups == 0:
        raise BodoError(
            'Series.str.{}(): pattern {} contains no capture groups'.format
            (func_name, pat))
    rkqba__culhw = dict(zip(regex.groupindex.values(), regex.groupindex.keys())
        )
    mpjx__nkfod = [rkqba__culhw.get(1 + i, i) for i in range(regex.groups)]
    return mpjx__nkfod, regex


def create_str2str_methods_overload(func_name):
    if func_name in ['lstrip', 'rstrip', 'strip']:
        mrvwa__spvmy = 'def f(S_str, to_strip=None):\n'
    else:
        mrvwa__spvmy = 'def f(S_str):\n'
    mrvwa__spvmy += '    S = S_str._obj\n'
    mrvwa__spvmy += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    mrvwa__spvmy += '    str_arr = decode_if_dict_array(str_arr)\n'
    mrvwa__spvmy += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    mrvwa__spvmy += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    mrvwa__spvmy += '    numba.parfors.parfor.init_prange()\n'
    mrvwa__spvmy += '    n = len(str_arr)\n'
    if func_name in ('capitalize', 'lower', 'swapcase', 'title', 'upper'):
        mrvwa__spvmy += '    num_chars = num_total_chars(str_arr)\n'
    else:
        mrvwa__spvmy += '    num_chars = -1\n'
    mrvwa__spvmy += (
        '    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)\n'
        )
    mrvwa__spvmy += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    mrvwa__spvmy += '        if bodo.libs.array_kernels.isna(str_arr, j):\n'
    mrvwa__spvmy += '            out_arr[j] = ""\n'
    mrvwa__spvmy += '            bodo.libs.array_kernels.setna(out_arr, j)\n'
    mrvwa__spvmy += '        else:\n'
    if func_name in ['lstrip', 'rstrip', 'strip']:
        mrvwa__spvmy += ('            out_arr[j] = str_arr[j].{}(to_strip)\n'
            .format(func_name))
    else:
        mrvwa__spvmy += '            out_arr[j] = str_arr[j].{}()\n'.format(
            func_name)
    mrvwa__spvmy += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    les__bhk = {}
    exec(mrvwa__spvmy, {'bodo': bodo, 'numba': numba, 'num_total_chars':
        bodo.libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, les__bhk)
    xed__kbajv = les__bhk['f']
    if func_name in ['lstrip', 'rstrip', 'strip']:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            return xed__kbajv
        return overload_strip_method
    else:

        def overload_str2str_methods(S_str):
            return xed__kbajv
        return overload_str2str_methods


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        mrvwa__spvmy = 'def f(S_str):\n'
        mrvwa__spvmy += '    S = S_str._obj\n'
        mrvwa__spvmy += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        mrvwa__spvmy += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        mrvwa__spvmy += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        mrvwa__spvmy += '    numba.parfors.parfor.init_prange()\n'
        mrvwa__spvmy += '    l = len(str_arr)\n'
        mrvwa__spvmy += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        mrvwa__spvmy += (
            '    for i in numba.parfors.parfor.internal_prange(l):\n')
        mrvwa__spvmy += (
            '        if bodo.libs.array_kernels.isna(str_arr, i):\n')
        mrvwa__spvmy += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        mrvwa__spvmy += '        else:\n'
        mrvwa__spvmy += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        mrvwa__spvmy += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        mrvwa__spvmy += '      out_arr,index, name)\n'
        les__bhk = {}
        exec(mrvwa__spvmy, {'bodo': bodo, 'numba': numba, 'np': np}, les__bhk)
        xed__kbajv = les__bhk['f']
        return xed__kbajv
    return overload_str2bool_methods


def _install_str2str_methods():
    for fmdo__pzrl in bodo.hiframes.pd_series_ext.str2str_methods:
        ztv__kkt = create_str2str_methods_overload(fmdo__pzrl)
        overload_method(SeriesStrMethodType, fmdo__pzrl, inline='always',
            no_unliteral=True)(ztv__kkt)


def _install_str2bool_methods():
    for fmdo__pzrl in bodo.hiframes.pd_series_ext.str2bool_methods:
        ztv__kkt = create_str2bool_methods_overload(fmdo__pzrl)
        overload_method(SeriesStrMethodType, fmdo__pzrl, inline='always',
            no_unliteral=True)(ztv__kkt)


_install_str2str_methods()
_install_str2bool_methods()


@overload_attribute(SeriesType, 'cat')
def overload_series_cat(s):
    if not isinstance(s.dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):
        raise BodoError('Can only use .cat accessor with categorical values.')
    return lambda s: bodo.hiframes.series_str_impl.init_series_cat_method(s)


class SeriesCatMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        rpym__ikch = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(rpym__ikch)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lngh__ftsf = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, lngh__ftsf)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        pploi__mhvun, = args
        wfua__nlg = signature.return_type
        vzutw__hyuqs = cgutils.create_struct_proxy(wfua__nlg)(context, builder)
        vzutw__hyuqs.obj = pploi__mhvun
        context.nrt.incref(builder, signature.args[0], pploi__mhvun)
        return vzutw__hyuqs._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        bwiue__cpqqs = bodo.hiframes.pd_series_ext.get_series_data(S)
        dve__vnim = bodo.hiframes.pd_series_ext.get_series_index(S)
        rpym__ikch = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(bwiue__cpqqs),
            dve__vnim, rpym__ikch)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for xxouu__taje in unsupported_cat_attrs:
        zxn__rbnx = 'Series.cat.' + xxouu__taje
        overload_attribute(SeriesCatMethodType, xxouu__taje)(
            create_unsupported_overload(zxn__rbnx))
    for ualpg__qoxo in unsupported_cat_methods:
        zxn__rbnx = 'Series.cat.' + ualpg__qoxo
        overload_method(SeriesCatMethodType, ualpg__qoxo)(
            create_unsupported_overload(zxn__rbnx))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for ualpg__qoxo in unsupported_str_methods:
        zxn__rbnx = 'Series.str.' + ualpg__qoxo
        overload_method(SeriesStrMethodType, ualpg__qoxo)(
            create_unsupported_overload(zxn__rbnx))


_install_strseries_unsupported()
