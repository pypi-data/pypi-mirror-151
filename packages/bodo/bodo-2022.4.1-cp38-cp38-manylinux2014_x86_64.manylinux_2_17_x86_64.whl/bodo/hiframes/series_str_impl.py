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
        bmwif__uuha = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(bmwif__uuha)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qrhht__var = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, qrhht__var)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        nil__ghjez, = args
        ugvj__gvqhd = signature.return_type
        frja__xwzjp = cgutils.create_struct_proxy(ugvj__gvqhd)(context, builder
            )
        frja__xwzjp.obj = nil__ghjez
        context.nrt.incref(builder, signature.args[0], nil__ghjez)
        return frja__xwzjp._getvalue()
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
        bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(bjxac__rlwi, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
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
            bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
            bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(bjxac__rlwi,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                vyr__rfab, bmwif__uuha)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(bjxac__rlwi, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    vmld__pdrtd = S_str.stype.data
    if (vmld__pdrtd != string_array_split_view_type and not is_str_arr_type
        (vmld__pdrtd)) and not isinstance(vmld__pdrtd, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(vmld__pdrtd, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
            bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(bjxac__rlwi, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                vyr__rfab, bmwif__uuha)
        return _str_get_array_impl
    if vmld__pdrtd == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
            bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(bjxac__rlwi)
            uqto__eed = 0
            for mspti__zkufs in numba.parfors.parfor.internal_prange(n):
                diecv__hdczm, diecv__hdczm, eolof__uahot = (
                    get_split_view_index(bjxac__rlwi, mspti__zkufs, i))
                uqto__eed += eolof__uahot
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, uqto__eed)
            for bkclh__gmr in numba.parfors.parfor.internal_prange(n):
                olekb__nxmhs, wpq__zuoet, eolof__uahot = get_split_view_index(
                    bjxac__rlwi, bkclh__gmr, i)
                if olekb__nxmhs == 0:
                    bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
                    yivgu__als = get_split_view_data_ptr(bjxac__rlwi, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        bkclh__gmr)
                    yivgu__als = get_split_view_data_ptr(bjxac__rlwi,
                        wpq__zuoet)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    bkclh__gmr, yivgu__als, eolof__uahot)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                vyr__rfab, bmwif__uuha)
        return _str_get_split_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(bjxac__rlwi)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for bkclh__gmr in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(bjxac__rlwi, bkclh__gmr
                ) or not len(bjxac__rlwi[bkclh__gmr]) > i >= -len(bjxac__rlwi
                [bkclh__gmr]):
                out_arr[bkclh__gmr] = ''
                bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
            else:
                out_arr[bkclh__gmr] = bjxac__rlwi[bkclh__gmr][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    vmld__pdrtd = S_str.stype.data
    if (vmld__pdrtd != string_array_split_view_type and vmld__pdrtd !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        vmld__pdrtd)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(ens__hhxfg)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for bkclh__gmr in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(ens__hhxfg, bkclh__gmr):
                out_arr[bkclh__gmr] = ''
                bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
            else:
                xhb__rck = ens__hhxfg[bkclh__gmr]
                out_arr[bkclh__gmr] = sep.join(xhb__rck)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
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
            bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
            bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(bjxac__rlwi, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                vyr__rfab, bmwif__uuha)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
            bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            gnza__nmdx = re.compile(pat, flags)
            pwmvw__grb = len(bjxac__rlwi)
            out_arr = pre_alloc_string_array(pwmvw__grb, -1)
            for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
                if bodo.libs.array_kernels.isna(bjxac__rlwi, bkclh__gmr):
                    out_arr[bkclh__gmr] = ''
                    bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
                    continue
                out_arr[bkclh__gmr] = gnza__nmdx.sub(repl, bjxac__rlwi[
                    bkclh__gmr])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                vyr__rfab, bmwif__uuha)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(bjxac__rlwi)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(pwmvw__grb, -1)
        for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(bjxac__rlwi, bkclh__gmr):
                out_arr[bkclh__gmr] = ''
                bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
                continue
            out_arr[bkclh__gmr] = bjxac__rlwi[bkclh__gmr].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    nqoph__mcecs = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(uxcbf__smzio in pat) for uxcbf__smzio in nqoph__mcecs])
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
    ifbq__svmgz = re.IGNORECASE.value
    fguv__ywbnt = 'def impl(\n'
    fguv__ywbnt += (
        '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n')
    fguv__ywbnt += '):\n'
    fguv__ywbnt += '  S = S_str._obj\n'
    fguv__ywbnt += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    fguv__ywbnt += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    fguv__ywbnt += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    fguv__ywbnt += '  l = len(arr)\n'
    fguv__ywbnt += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                fguv__ywbnt += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                fguv__ywbnt += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            fguv__ywbnt += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        fguv__ywbnt += """  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)
"""
    else:
        fguv__ywbnt += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            fguv__ywbnt += '  upper_pat = pat.upper()\n'
        fguv__ywbnt += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        fguv__ywbnt += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        fguv__ywbnt += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        fguv__ywbnt += '      else: \n'
        if is_overload_true(case):
            fguv__ywbnt += '          out_arr[i] = pat in arr[i]\n'
        else:
            fguv__ywbnt += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    fguv__ywbnt += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    xwg__qfhr = {}
    exec(fguv__ywbnt, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': ifbq__svmgz, 'get_search_regex':
        get_search_regex}, xwg__qfhr)
    impl = xwg__qfhr['impl']
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
    fguv__ywbnt = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    fguv__ywbnt += '  S = S_str._obj\n'
    fguv__ywbnt += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    fguv__ywbnt += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    fguv__ywbnt += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    fguv__ywbnt += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        fguv__ywbnt += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(hjhs__jvqjt ==
        bodo.dict_str_arr_type for hjhs__jvqjt in others.data):
        jymzg__shcm = ', '.join(f'data{i}' for i in range(len(others.columns)))
        fguv__ywbnt += f"""  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {jymzg__shcm}), sep)
"""
    else:
        yphc__fcf = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        fguv__ywbnt += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        fguv__ywbnt += '  numba.parfors.parfor.init_prange()\n'
        fguv__ywbnt += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        fguv__ywbnt += f'      if {yphc__fcf}:\n'
        fguv__ywbnt += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        fguv__ywbnt += '          continue\n'
        rygb__jmid = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        fhcff__wjfia = "''" if is_overload_none(sep) else 'sep'
        fguv__ywbnt += (
            f'      out_arr[i] = {fhcff__wjfia}.join([{rygb__jmid}])\n')
    fguv__ywbnt += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    xwg__qfhr = {}
    exec(fguv__ywbnt, {'bodo': bodo, 'numba': numba}, xwg__qfhr)
    impl = xwg__qfhr['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        gnza__nmdx = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(pwmvw__grb, np.int64)
        for i in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(gnza__nmdx, ens__hhxfg[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
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
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(pwmvw__grb, np.int64)
        for i in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ens__hhxfg[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
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
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(pwmvw__grb, np.int64)
        for i in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ens__hhxfg[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
    return impl


@overload_method(SeriesStrMethodType, 'center', inline='always',
    no_unliteral=True)
def overload_str_method_center(S_str, width, fillchar=' '):
    common_validate_padding('center', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pwmvw__grb, -1)
        for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, bkclh__gmr):
                out_arr[bkclh__gmr] = ''
                bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
            else:
                out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
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
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pwmvw__grb, -1)
        for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, bkclh__gmr):
                bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
            else:
                if stop is not None:
                    gtb__twfx = ens__hhxfg[bkclh__gmr][stop:]
                else:
                    gtb__twfx = ''
                out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr][:start
                    ] + repl + gtb__twfx
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):

        def impl(S_str, repeats):
            S = S_str._obj
            ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
            bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
            vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            pwmvw__grb = len(ens__hhxfg)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pwmvw__grb,
                -1)
            for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
                if bodo.libs.array_kernels.isna(ens__hhxfg, bkclh__gmr):
                    bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
                else:
                    out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                vyr__rfab, bmwif__uuha)
        return impl
    elif is_overload_constant_list(repeats):
        uzpct__mjlii = get_overload_const_list(repeats)
        fcgg__ewi = all([isinstance(iyd__dhvn, int) for iyd__dhvn in
            uzpct__mjlii])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        fcgg__ewi = True
    else:
        fcgg__ewi = False
    if fcgg__ewi:

        def impl(S_str, repeats):
            S = S_str._obj
            ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
            bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
            vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
            yxuup__nheim = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            pwmvw__grb = len(ens__hhxfg)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pwmvw__grb,
                -1)
            for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
                if bodo.libs.array_kernels.isna(ens__hhxfg, bkclh__gmr):
                    bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
                else:
                    out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr
                        ] * yxuup__nheim[bkclh__gmr]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                vyr__rfab, bmwif__uuha)
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
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pwmvw__grb, -1)
        for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, bkclh__gmr):
                out_arr[bkclh__gmr] = ''
                bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
            else:
                out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr].ljust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
    return impl


@overload_method(SeriesStrMethodType, 'rjust', inline='always',
    no_unliteral=True)
def overload_str_method_rjust(S_str, width, fillchar=' '):
    common_validate_padding('rjust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pwmvw__grb, -1)
        for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, bkclh__gmr):
                out_arr[bkclh__gmr] = ''
                bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
            else:
                out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr].rjust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
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
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pwmvw__grb, -1)
        for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, bkclh__gmr):
                out_arr[bkclh__gmr] = ''
                bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
            elif side == 'left':
                out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)

    def impl(S_str, width):
        S = S_str._obj
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pwmvw__grb, -1)
        for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, bkclh__gmr):
                out_arr[bkclh__gmr] = ''
                bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
            else:
                out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
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
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pwmvw__grb, -1)
        for bkclh__gmr in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, bkclh__gmr):
                out_arr[bkclh__gmr] = ''
                bodo.libs.array_kernels.setna(out_arr, bkclh__gmr)
            else:
                out_arr[bkclh__gmr] = ens__hhxfg[bkclh__gmr][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
            bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(bjxac__rlwi,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                vyr__rfab, bmwif__uuha)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(pwmvw__grb)
        for i in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ens__hhxfg[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
            vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
            bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(bjxac__rlwi, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                vyr__rfab, bmwif__uuha)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        ens__hhxfg = bodo.hiframes.pd_series_ext.get_series_data(S)
        bmwif__uuha = bodo.hiframes.pd_series_ext.get_series_name(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pwmvw__grb = len(ens__hhxfg)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(pwmvw__grb)
        for i in numba.parfors.parfor.internal_prange(pwmvw__grb):
            if bodo.libs.array_kernels.isna(ens__hhxfg, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ens__hhxfg[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, vyr__rfab,
            bmwif__uuha)
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
    znwwm__tffl, regex = _get_column_names_from_regex(pat, flags, 'extract')
    ewczo__hjx = len(znwwm__tffl)
    fguv__ywbnt = 'def impl(S_str, pat, flags=0, expand=True):\n'
    fguv__ywbnt += '  regex = re.compile(pat, flags=flags)\n'
    fguv__ywbnt += '  S = S_str._obj\n'
    fguv__ywbnt += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    fguv__ywbnt += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    fguv__ywbnt += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    fguv__ywbnt += '  numba.parfors.parfor.init_prange()\n'
    fguv__ywbnt += '  n = len(str_arr)\n'
    for i in range(ewczo__hjx):
        fguv__ywbnt += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    fguv__ywbnt += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    fguv__ywbnt += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(ewczo__hjx):
        fguv__ywbnt += "          out_arr_{}[j] = ''\n".format(i)
        fguv__ywbnt += (
            '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    fguv__ywbnt += '      else:\n'
    fguv__ywbnt += '          m = regex.search(str_arr[j])\n'
    fguv__ywbnt += '          if m:\n'
    fguv__ywbnt += '            g = m.groups()\n'
    for i in range(ewczo__hjx):
        fguv__ywbnt += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    fguv__ywbnt += '          else:\n'
    for i in range(ewczo__hjx):
        fguv__ywbnt += "            out_arr_{}[j] = ''\n".format(i)
        fguv__ywbnt += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        bmwif__uuha = "'{}'".format(list(regex.groupindex.keys()).pop()
            ) if len(regex.groupindex.keys()) > 0 else 'name'
        fguv__ywbnt += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(bmwif__uuha))
        xwg__qfhr = {}
        exec(fguv__ywbnt, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, xwg__qfhr)
        impl = xwg__qfhr['impl']
        return impl
    pyj__vakb = ', '.join('out_arr_{}'.format(i) for i in range(ewczo__hjx))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(fguv__ywbnt,
        znwwm__tffl, pyj__vakb, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    znwwm__tffl, diecv__hdczm = _get_column_names_from_regex(pat, flags,
        'extractall')
    ewczo__hjx = len(znwwm__tffl)
    ayw__ufdn = isinstance(S_str.stype.index, StringIndexType)
    fguv__ywbnt = 'def impl(S_str, pat, flags=0):\n'
    fguv__ywbnt += '  regex = re.compile(pat, flags=flags)\n'
    fguv__ywbnt += '  S = S_str._obj\n'
    fguv__ywbnt += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    fguv__ywbnt += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    fguv__ywbnt += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    fguv__ywbnt += (
        '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    fguv__ywbnt += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    fguv__ywbnt += '  numba.parfors.parfor.init_prange()\n'
    fguv__ywbnt += '  n = len(str_arr)\n'
    fguv__ywbnt += '  out_n_l = [0]\n'
    for i in range(ewczo__hjx):
        fguv__ywbnt += '  num_chars_{} = 0\n'.format(i)
    if ayw__ufdn:
        fguv__ywbnt += '  index_num_chars = 0\n'
    fguv__ywbnt += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if ayw__ufdn:
        fguv__ywbnt += '      index_num_chars += get_utf8_size(index_arr[i])\n'
    fguv__ywbnt += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    fguv__ywbnt += '          continue\n'
    fguv__ywbnt += '      m = regex.findall(str_arr[i])\n'
    fguv__ywbnt += '      out_n_l[0] += len(m)\n'
    for i in range(ewczo__hjx):
        fguv__ywbnt += '      l_{} = 0\n'.format(i)
    fguv__ywbnt += '      for s in m:\n'
    for i in range(ewczo__hjx):
        fguv__ywbnt += '        l_{} += get_utf8_size(s{})\n'.format(i, 
            '[{}]'.format(i) if ewczo__hjx > 1 else '')
    for i in range(ewczo__hjx):
        fguv__ywbnt += '      num_chars_{0} += l_{0}\n'.format(i)
    fguv__ywbnt += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(ewczo__hjx):
        fguv__ywbnt += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if ayw__ufdn:
        fguv__ywbnt += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        fguv__ywbnt += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    fguv__ywbnt += '  out_match_arr = np.empty(out_n, np.int64)\n'
    fguv__ywbnt += '  out_ind = 0\n'
    fguv__ywbnt += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    fguv__ywbnt += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    fguv__ywbnt += '          continue\n'
    fguv__ywbnt += '      m = regex.findall(str_arr[j])\n'
    fguv__ywbnt += '      for k, s in enumerate(m):\n'
    for i in range(ewczo__hjx):
        fguv__ywbnt += (
            """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
            .format(i, '[{}]'.format(i) if ewczo__hjx > 1 else ''))
    fguv__ywbnt += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    fguv__ywbnt += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    fguv__ywbnt += '        out_ind += 1\n'
    fguv__ywbnt += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    fguv__ywbnt += "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n"
    pyj__vakb = ', '.join('out_arr_{}'.format(i) for i in range(ewczo__hjx))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(fguv__ywbnt,
        znwwm__tffl, pyj__vakb, 'out_index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
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
    pxwih__atmq = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    znwwm__tffl = [pxwih__atmq.get(1 + i, i) for i in range(regex.groups)]
    return znwwm__tffl, regex


def create_str2str_methods_overload(func_name):
    if func_name in ['lstrip', 'rstrip', 'strip']:
        fguv__ywbnt = 'def f(S_str, to_strip=None):\n'
    else:
        fguv__ywbnt = 'def f(S_str):\n'
    fguv__ywbnt += '    S = S_str._obj\n'
    fguv__ywbnt += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    fguv__ywbnt += '    str_arr = decode_if_dict_array(str_arr)\n'
    fguv__ywbnt += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    fguv__ywbnt += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    fguv__ywbnt += '    numba.parfors.parfor.init_prange()\n'
    fguv__ywbnt += '    n = len(str_arr)\n'
    if func_name in ('capitalize', 'lower', 'swapcase', 'title', 'upper'):
        fguv__ywbnt += '    num_chars = num_total_chars(str_arr)\n'
    else:
        fguv__ywbnt += '    num_chars = -1\n'
    fguv__ywbnt += (
        '    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)\n'
        )
    fguv__ywbnt += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    fguv__ywbnt += '        if bodo.libs.array_kernels.isna(str_arr, j):\n'
    fguv__ywbnt += '            out_arr[j] = ""\n'
    fguv__ywbnt += '            bodo.libs.array_kernels.setna(out_arr, j)\n'
    fguv__ywbnt += '        else:\n'
    if func_name in ['lstrip', 'rstrip', 'strip']:
        fguv__ywbnt += ('            out_arr[j] = str_arr[j].{}(to_strip)\n'
            .format(func_name))
    else:
        fguv__ywbnt += '            out_arr[j] = str_arr[j].{}()\n'.format(
            func_name)
    fguv__ywbnt += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    xwg__qfhr = {}
    exec(fguv__ywbnt, {'bodo': bodo, 'numba': numba, 'num_total_chars':
        bodo.libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, xwg__qfhr)
    xwmaq__kptw = xwg__qfhr['f']
    if func_name in ['lstrip', 'rstrip', 'strip']:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            return xwmaq__kptw
        return overload_strip_method
    else:

        def overload_str2str_methods(S_str):
            return xwmaq__kptw
        return overload_str2str_methods


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        fguv__ywbnt = 'def f(S_str):\n'
        fguv__ywbnt += '    S = S_str._obj\n'
        fguv__ywbnt += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        fguv__ywbnt += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        fguv__ywbnt += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        fguv__ywbnt += '    numba.parfors.parfor.init_prange()\n'
        fguv__ywbnt += '    l = len(str_arr)\n'
        fguv__ywbnt += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        fguv__ywbnt += (
            '    for i in numba.parfors.parfor.internal_prange(l):\n')
        fguv__ywbnt += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
        fguv__ywbnt += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        fguv__ywbnt += '        else:\n'
        fguv__ywbnt += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        fguv__ywbnt += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        fguv__ywbnt += '      out_arr,index, name)\n'
        xwg__qfhr = {}
        exec(fguv__ywbnt, {'bodo': bodo, 'numba': numba, 'np': np}, xwg__qfhr)
        xwmaq__kptw = xwg__qfhr['f']
        return xwmaq__kptw
    return overload_str2bool_methods


def _install_str2str_methods():
    for zoa__rlv in bodo.hiframes.pd_series_ext.str2str_methods:
        gjgby__nxr = create_str2str_methods_overload(zoa__rlv)
        overload_method(SeriesStrMethodType, zoa__rlv, inline='always',
            no_unliteral=True)(gjgby__nxr)


def _install_str2bool_methods():
    for zoa__rlv in bodo.hiframes.pd_series_ext.str2bool_methods:
        gjgby__nxr = create_str2bool_methods_overload(zoa__rlv)
        overload_method(SeriesStrMethodType, zoa__rlv, inline='always',
            no_unliteral=True)(gjgby__nxr)


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
        bmwif__uuha = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(bmwif__uuha)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qrhht__var = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, qrhht__var)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        nil__ghjez, = args
        wtcvi__dfneq = signature.return_type
        iwm__npwjy = cgutils.create_struct_proxy(wtcvi__dfneq)(context, builder
            )
        iwm__npwjy.obj = nil__ghjez
        context.nrt.incref(builder, signature.args[0], nil__ghjez)
        return iwm__npwjy._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        bjxac__rlwi = bodo.hiframes.pd_series_ext.get_series_data(S)
        vyr__rfab = bodo.hiframes.pd_series_ext.get_series_index(S)
        bmwif__uuha = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(bjxac__rlwi),
            vyr__rfab, bmwif__uuha)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for inq__nysu in unsupported_cat_attrs:
        omjr__rhjfd = 'Series.cat.' + inq__nysu
        overload_attribute(SeriesCatMethodType, inq__nysu)(
            create_unsupported_overload(omjr__rhjfd))
    for wdj__xckqx in unsupported_cat_methods:
        omjr__rhjfd = 'Series.cat.' + wdj__xckqx
        overload_method(SeriesCatMethodType, wdj__xckqx)(
            create_unsupported_overload(omjr__rhjfd))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for wdj__xckqx in unsupported_str_methods:
        omjr__rhjfd = 'Series.str.' + wdj__xckqx
        overload_method(SeriesStrMethodType, wdj__xckqx)(
            create_unsupported_overload(omjr__rhjfd))


_install_strseries_unsupported()
