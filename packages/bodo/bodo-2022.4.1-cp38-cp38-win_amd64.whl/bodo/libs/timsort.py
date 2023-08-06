import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    ige__ndjv = hi - lo
    if ige__ndjv < 2:
        return
    if ige__ndjv < MIN_MERGE:
        uou__tax = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + uou__tax, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    hjmx__ern = minRunLength(ige__ndjv)
    while True:
        adl__iewq = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if adl__iewq < hjmx__ern:
            byvy__gcijh = ige__ndjv if ige__ndjv <= hjmx__ern else hjmx__ern
            binarySort(key_arrs, lo, lo + byvy__gcijh, lo + adl__iewq, data)
            adl__iewq = byvy__gcijh
        stackSize = pushRun(stackSize, runBase, runLen, lo, adl__iewq)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += adl__iewq
        ige__ndjv -= adl__iewq
        if ige__ndjv == 0:
            break
    assert lo == hi
    stackSize, tmpLength, tmp, tmp_data, minGallop = mergeForceCollapse(
        stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
        tmp_data, minGallop)
    assert stackSize == 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def binarySort(key_arrs, lo, hi, start, data):
    assert lo <= start and start <= hi
    if start == lo:
        start += 1
    while start < hi:
        mnakk__wnox = getitem_arr_tup(key_arrs, start)
        wrrju__box = getitem_arr_tup(data, start)
        osrk__ltzys = lo
        jmkvj__bvca = start
        assert osrk__ltzys <= jmkvj__bvca
        while osrk__ltzys < jmkvj__bvca:
            zidt__fqnq = osrk__ltzys + jmkvj__bvca >> 1
            if mnakk__wnox < getitem_arr_tup(key_arrs, zidt__fqnq):
                jmkvj__bvca = zidt__fqnq
            else:
                osrk__ltzys = zidt__fqnq + 1
        assert osrk__ltzys == jmkvj__bvca
        n = start - osrk__ltzys
        copyRange_tup(key_arrs, osrk__ltzys, key_arrs, osrk__ltzys + 1, n)
        copyRange_tup(data, osrk__ltzys, data, osrk__ltzys + 1, n)
        setitem_arr_tup(key_arrs, osrk__ltzys, mnakk__wnox)
        setitem_arr_tup(data, osrk__ltzys, wrrju__box)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    pfz__ajsl = lo + 1
    if pfz__ajsl == hi:
        return 1
    if getitem_arr_tup(key_arrs, pfz__ajsl) < getitem_arr_tup(key_arrs, lo):
        pfz__ajsl += 1
        while pfz__ajsl < hi and getitem_arr_tup(key_arrs, pfz__ajsl
            ) < getitem_arr_tup(key_arrs, pfz__ajsl - 1):
            pfz__ajsl += 1
        reverseRange(key_arrs, lo, pfz__ajsl, data)
    else:
        pfz__ajsl += 1
        while pfz__ajsl < hi and getitem_arr_tup(key_arrs, pfz__ajsl
            ) >= getitem_arr_tup(key_arrs, pfz__ajsl - 1):
            pfz__ajsl += 1
    return pfz__ajsl - lo


@numba.njit(no_cpython_wrapper=True, cache=True)
def reverseRange(key_arrs, lo, hi, data):
    hi -= 1
    while lo < hi:
        swap_arrs(key_arrs, lo, hi)
        swap_arrs(data, lo, hi)
        lo += 1
        hi -= 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def minRunLength(n):
    assert n >= 0
    fdd__vldra = 0
    while n >= MIN_MERGE:
        fdd__vldra |= n & 1
        n >>= 1
    return n + fdd__vldra


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    tqhp__yqnw = len(key_arrs[0])
    tmpLength = (tqhp__yqnw >> 1 if tqhp__yqnw < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    pnd__jxe = (5 if tqhp__yqnw < 120 else 10 if tqhp__yqnw < 1542 else 19 if
        tqhp__yqnw < 119151 else 40)
    runBase = np.empty(pnd__jxe, np.int64)
    runLen = np.empty(pnd__jxe, np.int64)
    return stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def pushRun(stackSize, runBase, runLen, runBase_val, runLen_val):
    runBase[stackSize] = runBase_val
    runLen[stackSize] = runLen_val
    stackSize += 1
    return stackSize


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeCollapse(stackSize, runBase, runLen, key_arrs, data, tmpLength,
    tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n >= 1 and runLen[n - 1] <= runLen[n] + runLen[n + 1
            ] or n >= 2 and runLen[n - 2] <= runLen[n] + runLen[n - 1]:
            if runLen[n - 1] < runLen[n + 1]:
                n -= 1
        elif runLen[n] > runLen[n + 1]:
            break
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeForceCollapse(stackSize, runBase, runLen, key_arrs, data,
    tmpLength, tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n > 0 and runLen[n - 1] < runLen[n + 1]:
            n -= 1
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeAt(stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
    tmp_data, minGallop, i):
    assert stackSize >= 2
    assert i >= 0
    assert i == stackSize - 2 or i == stackSize - 3
    base1 = runBase[i]
    len1 = runLen[i]
    base2 = runBase[i + 1]
    len2 = runLen[i + 1]
    assert len1 > 0 and len2 > 0
    assert base1 + len1 == base2
    runLen[i] = len1 + len2
    if i == stackSize - 3:
        runBase[i + 1] = runBase[i + 2]
        runLen[i + 1] = runLen[i + 2]
    stackSize -= 1
    luz__robie = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert luz__robie >= 0
    base1 += luz__robie
    len1 -= luz__robie
    if len1 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    len2 = gallopLeft(getitem_arr_tup(key_arrs, base1 + len1 - 1), key_arrs,
        base2, len2, len2 - 1)
    assert len2 >= 0
    if len2 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    if len1 <= len2:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len1)
        minGallop = mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    else:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len2)
        minGallop = mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopLeft(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    pcf__qrp = 0
    tfmw__omuff = 1
    if key > getitem_arr_tup(arr, base + hint):
        xrxod__ipa = _len - hint
        while tfmw__omuff < xrxod__ipa and key > getitem_arr_tup(arr, base +
            hint + tfmw__omuff):
            pcf__qrp = tfmw__omuff
            tfmw__omuff = (tfmw__omuff << 1) + 1
            if tfmw__omuff <= 0:
                tfmw__omuff = xrxod__ipa
        if tfmw__omuff > xrxod__ipa:
            tfmw__omuff = xrxod__ipa
        pcf__qrp += hint
        tfmw__omuff += hint
    else:
        xrxod__ipa = hint + 1
        while tfmw__omuff < xrxod__ipa and key <= getitem_arr_tup(arr, base +
            hint - tfmw__omuff):
            pcf__qrp = tfmw__omuff
            tfmw__omuff = (tfmw__omuff << 1) + 1
            if tfmw__omuff <= 0:
                tfmw__omuff = xrxod__ipa
        if tfmw__omuff > xrxod__ipa:
            tfmw__omuff = xrxod__ipa
        tmp = pcf__qrp
        pcf__qrp = hint - tfmw__omuff
        tfmw__omuff = hint - tmp
    assert -1 <= pcf__qrp and pcf__qrp < tfmw__omuff and tfmw__omuff <= _len
    pcf__qrp += 1
    while pcf__qrp < tfmw__omuff:
        dmmc__jji = pcf__qrp + (tfmw__omuff - pcf__qrp >> 1)
        if key > getitem_arr_tup(arr, base + dmmc__jji):
            pcf__qrp = dmmc__jji + 1
        else:
            tfmw__omuff = dmmc__jji
    assert pcf__qrp == tfmw__omuff
    return tfmw__omuff


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    tfmw__omuff = 1
    pcf__qrp = 0
    if key < getitem_arr_tup(arr, base + hint):
        xrxod__ipa = hint + 1
        while tfmw__omuff < xrxod__ipa and key < getitem_arr_tup(arr, base +
            hint - tfmw__omuff):
            pcf__qrp = tfmw__omuff
            tfmw__omuff = (tfmw__omuff << 1) + 1
            if tfmw__omuff <= 0:
                tfmw__omuff = xrxod__ipa
        if tfmw__omuff > xrxod__ipa:
            tfmw__omuff = xrxod__ipa
        tmp = pcf__qrp
        pcf__qrp = hint - tfmw__omuff
        tfmw__omuff = hint - tmp
    else:
        xrxod__ipa = _len - hint
        while tfmw__omuff < xrxod__ipa and key >= getitem_arr_tup(arr, base +
            hint + tfmw__omuff):
            pcf__qrp = tfmw__omuff
            tfmw__omuff = (tfmw__omuff << 1) + 1
            if tfmw__omuff <= 0:
                tfmw__omuff = xrxod__ipa
        if tfmw__omuff > xrxod__ipa:
            tfmw__omuff = xrxod__ipa
        pcf__qrp += hint
        tfmw__omuff += hint
    assert -1 <= pcf__qrp and pcf__qrp < tfmw__omuff and tfmw__omuff <= _len
    pcf__qrp += 1
    while pcf__qrp < tfmw__omuff:
        dmmc__jji = pcf__qrp + (tfmw__omuff - pcf__qrp >> 1)
        if key < getitem_arr_tup(arr, base + dmmc__jji):
            tfmw__omuff = dmmc__jji
        else:
            pcf__qrp = dmmc__jji + 1
    assert pcf__qrp == tfmw__omuff
    return tfmw__omuff


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base1, tmp, 0, len1)
    copyRange_tup(arr_data, base1, tmp_data, 0, len1)
    cursor1 = 0
    cursor2 = base2
    dest = base1
    setitem_arr_tup(arr, dest, getitem_arr_tup(arr, cursor2))
    copyElement_tup(arr_data, cursor2, arr_data, dest)
    cursor2 += 1
    dest += 1
    len2 -= 1
    if len2 == 0:
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
        return minGallop
    if len1 == 1:
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
        return minGallop
    len1, len2, cursor1, cursor2, dest, minGallop = mergeLo_inner(key_arrs,
        data, tmp_data, len1, len2, tmp, cursor1, cursor2, dest, minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len1 == 1:
        assert len2 > 0
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
    elif len1 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len2 == 0
        assert len1 > 1
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo_inner(arr, arr_data, tmp_data, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        luz__daocp = 0
        bkuz__akbib = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                bkuz__akbib += 1
                luz__daocp = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                luz__daocp += 1
                bkuz__akbib = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not luz__daocp | bkuz__akbib < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            luz__daocp = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if luz__daocp != 0:
                copyRange_tup(tmp, cursor1, arr, dest, luz__daocp)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, luz__daocp)
                dest += luz__daocp
                cursor1 += luz__daocp
                len1 -= luz__daocp
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            bkuz__akbib = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if bkuz__akbib != 0:
                copyRange_tup(arr, cursor2, arr, dest, bkuz__akbib)
                copyRange_tup(arr_data, cursor2, arr_data, dest, bkuz__akbib)
                dest += bkuz__akbib
                cursor2 += bkuz__akbib
                len2 -= bkuz__akbib
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor1, arr, dest)
            copyElement_tup(tmp_data, cursor1, arr_data, dest)
            cursor1 += 1
            dest += 1
            len1 -= 1
            if len1 == 1:
                return len1, len2, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not luz__daocp >= MIN_GALLOP | bkuz__akbib >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base2, tmp, 0, len2)
    copyRange_tup(arr_data, base2, tmp_data, 0, len2)
    cursor1 = base1 + len1 - 1
    cursor2 = len2 - 1
    dest = base2 + len2 - 1
    copyElement_tup(arr, cursor1, arr, dest)
    copyElement_tup(arr_data, cursor1, arr_data, dest)
    cursor1 -= 1
    dest -= 1
    len1 -= 1
    if len1 == 0:
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
        return minGallop
    if len2 == 1:
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
        return minGallop
    len1, len2, tmp, cursor1, cursor2, dest, minGallop = mergeHi_inner(key_arrs
        , data, tmp_data, base1, len1, len2, tmp, cursor1, cursor2, dest,
        minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len2 == 1:
        assert len1 > 0
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
    elif len2 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len1 == 0
        assert len2 > 0
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi_inner(arr, arr_data, tmp_data, base1, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        luz__daocp = 0
        bkuz__akbib = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                luz__daocp += 1
                bkuz__akbib = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                bkuz__akbib += 1
                luz__daocp = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not luz__daocp | bkuz__akbib < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            luz__daocp = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if luz__daocp != 0:
                dest -= luz__daocp
                cursor1 -= luz__daocp
                len1 -= luz__daocp
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, luz__daocp)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    luz__daocp)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            bkuz__akbib = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if bkuz__akbib != 0:
                dest -= bkuz__akbib
                cursor2 -= bkuz__akbib
                len2 -= bkuz__akbib
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, bkuz__akbib)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    bkuz__akbib)
                if len2 <= 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor1, arr, dest)
            copyElement_tup(arr_data, cursor1, arr_data, dest)
            cursor1 -= 1
            dest -= 1
            len1 -= 1
            if len1 == 0:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not luz__daocp >= MIN_GALLOP | bkuz__akbib >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    dphhd__xaxvi = len(key_arrs[0])
    if tmpLength < minCapacity:
        nsy__bsh = minCapacity
        nsy__bsh |= nsy__bsh >> 1
        nsy__bsh |= nsy__bsh >> 2
        nsy__bsh |= nsy__bsh >> 4
        nsy__bsh |= nsy__bsh >> 8
        nsy__bsh |= nsy__bsh >> 16
        nsy__bsh += 1
        if nsy__bsh < 0:
            nsy__bsh = minCapacity
        else:
            nsy__bsh = min(nsy__bsh, dphhd__xaxvi >> 1)
        tmp = alloc_arr_tup(nsy__bsh, key_arrs)
        tmp_data = alloc_arr_tup(nsy__bsh, data)
        tmpLength = nsy__bsh
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        mmsgt__vbyy = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = mmsgt__vbyy


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    lrt__dgvek = arr_tup.count
    pcyys__yfr = 'def f(arr_tup, lo, hi):\n'
    for i in range(lrt__dgvek):
        pcyys__yfr += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        pcyys__yfr += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        pcyys__yfr += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    pcyys__yfr += '  return\n'
    rdx__qriv = {}
    exec(pcyys__yfr, {}, rdx__qriv)
    ixax__jztzt = rdx__qriv['f']
    return ixax__jztzt


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    lrt__dgvek = src_arr_tup.count
    assert lrt__dgvek == dst_arr_tup.count
    pcyys__yfr = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(lrt__dgvek):
        pcyys__yfr += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    pcyys__yfr += '  return\n'
    rdx__qriv = {}
    exec(pcyys__yfr, {'copyRange': copyRange}, rdx__qriv)
    raci__vediw = rdx__qriv['f']
    return raci__vediw


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    lrt__dgvek = src_arr_tup.count
    assert lrt__dgvek == dst_arr_tup.count
    pcyys__yfr = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(lrt__dgvek):
        pcyys__yfr += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    pcyys__yfr += '  return\n'
    rdx__qriv = {}
    exec(pcyys__yfr, {'copyElement': copyElement}, rdx__qriv)
    raci__vediw = rdx__qriv['f']
    return raci__vediw


def getitem_arr_tup(arr_tup, ind):
    ytcf__azk = [arr[ind] for arr in arr_tup]
    return tuple(ytcf__azk)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    lrt__dgvek = arr_tup.count
    pcyys__yfr = 'def f(arr_tup, ind):\n'
    pcyys__yfr += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'.
        format(i) for i in range(lrt__dgvek)]), ',' if lrt__dgvek == 1 else '')
    rdx__qriv = {}
    exec(pcyys__yfr, {}, rdx__qriv)
    uogdg__gkl = rdx__qriv['f']
    return uogdg__gkl


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, dpbe__zbd in zip(arr_tup, val_tup):
        arr[ind] = dpbe__zbd


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    lrt__dgvek = arr_tup.count
    pcyys__yfr = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(lrt__dgvek):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            pcyys__yfr += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            pcyys__yfr += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    pcyys__yfr += '  return\n'
    rdx__qriv = {}
    exec(pcyys__yfr, {}, rdx__qriv)
    uogdg__gkl = rdx__qriv['f']
    return uogdg__gkl


def test():
    import time
    aue__qprui = time.time()
    hml__eta = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((hml__eta,), 0, 3, data)
    print('compile time', time.time() - aue__qprui)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    amllv__ytngm = np.random.ranf(n)
    xgdh__pgc = pd.DataFrame({'A': amllv__ytngm, 'B': data[0], 'C': data[1]})
    aue__qprui = time.time()
    tsgt__rfntq = xgdh__pgc.sort_values('A', inplace=False)
    wso__bxyb = time.time()
    sort((amllv__ytngm,), 0, n, data)
    print('Bodo', time.time() - wso__bxyb, 'Numpy', wso__bxyb - aue__qprui)
    np.testing.assert_almost_equal(data[0], tsgt__rfntq.B.values)
    np.testing.assert_almost_equal(data[1], tsgt__rfntq.C.values)


if __name__ == '__main__':
    test()
