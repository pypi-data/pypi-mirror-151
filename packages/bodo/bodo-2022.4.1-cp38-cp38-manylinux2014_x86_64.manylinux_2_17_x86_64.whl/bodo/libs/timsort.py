import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    jua__icqke = hi - lo
    if jua__icqke < 2:
        return
    if jua__icqke < MIN_MERGE:
        ydmrw__gsite = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + ydmrw__gsite, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    xcn__sezb = minRunLength(jua__icqke)
    while True:
        oaaqw__xzd = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if oaaqw__xzd < xcn__sezb:
            ysymh__gqxoz = jua__icqke if jua__icqke <= xcn__sezb else xcn__sezb
            binarySort(key_arrs, lo, lo + ysymh__gqxoz, lo + oaaqw__xzd, data)
            oaaqw__xzd = ysymh__gqxoz
        stackSize = pushRun(stackSize, runBase, runLen, lo, oaaqw__xzd)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += oaaqw__xzd
        jua__icqke -= oaaqw__xzd
        if jua__icqke == 0:
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
        hkjzr__rgs = getitem_arr_tup(key_arrs, start)
        vrwl__vpyk = getitem_arr_tup(data, start)
        rlo__anlj = lo
        zcry__ycx = start
        assert rlo__anlj <= zcry__ycx
        while rlo__anlj < zcry__ycx:
            wvzpo__tdam = rlo__anlj + zcry__ycx >> 1
            if hkjzr__rgs < getitem_arr_tup(key_arrs, wvzpo__tdam):
                zcry__ycx = wvzpo__tdam
            else:
                rlo__anlj = wvzpo__tdam + 1
        assert rlo__anlj == zcry__ycx
        n = start - rlo__anlj
        copyRange_tup(key_arrs, rlo__anlj, key_arrs, rlo__anlj + 1, n)
        copyRange_tup(data, rlo__anlj, data, rlo__anlj + 1, n)
        setitem_arr_tup(key_arrs, rlo__anlj, hkjzr__rgs)
        setitem_arr_tup(data, rlo__anlj, vrwl__vpyk)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    cso__vjvce = lo + 1
    if cso__vjvce == hi:
        return 1
    if getitem_arr_tup(key_arrs, cso__vjvce) < getitem_arr_tup(key_arrs, lo):
        cso__vjvce += 1
        while cso__vjvce < hi and getitem_arr_tup(key_arrs, cso__vjvce
            ) < getitem_arr_tup(key_arrs, cso__vjvce - 1):
            cso__vjvce += 1
        reverseRange(key_arrs, lo, cso__vjvce, data)
    else:
        cso__vjvce += 1
        while cso__vjvce < hi and getitem_arr_tup(key_arrs, cso__vjvce
            ) >= getitem_arr_tup(key_arrs, cso__vjvce - 1):
            cso__vjvce += 1
    return cso__vjvce - lo


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
    idvgo__phri = 0
    while n >= MIN_MERGE:
        idvgo__phri |= n & 1
        n >>= 1
    return n + idvgo__phri


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    ydyw__ebfwo = len(key_arrs[0])
    tmpLength = (ydyw__ebfwo >> 1 if ydyw__ebfwo < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    ldfmt__keyf = (5 if ydyw__ebfwo < 120 else 10 if ydyw__ebfwo < 1542 else
        19 if ydyw__ebfwo < 119151 else 40)
    runBase = np.empty(ldfmt__keyf, np.int64)
    runLen = np.empty(ldfmt__keyf, np.int64)
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
    ijr__zcfv = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert ijr__zcfv >= 0
    base1 += ijr__zcfv
    len1 -= ijr__zcfv
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
    rya__ufzk = 0
    vek__foy = 1
    if key > getitem_arr_tup(arr, base + hint):
        jxnr__udyo = _len - hint
        while vek__foy < jxnr__udyo and key > getitem_arr_tup(arr, base +
            hint + vek__foy):
            rya__ufzk = vek__foy
            vek__foy = (vek__foy << 1) + 1
            if vek__foy <= 0:
                vek__foy = jxnr__udyo
        if vek__foy > jxnr__udyo:
            vek__foy = jxnr__udyo
        rya__ufzk += hint
        vek__foy += hint
    else:
        jxnr__udyo = hint + 1
        while vek__foy < jxnr__udyo and key <= getitem_arr_tup(arr, base +
            hint - vek__foy):
            rya__ufzk = vek__foy
            vek__foy = (vek__foy << 1) + 1
            if vek__foy <= 0:
                vek__foy = jxnr__udyo
        if vek__foy > jxnr__udyo:
            vek__foy = jxnr__udyo
        tmp = rya__ufzk
        rya__ufzk = hint - vek__foy
        vek__foy = hint - tmp
    assert -1 <= rya__ufzk and rya__ufzk < vek__foy and vek__foy <= _len
    rya__ufzk += 1
    while rya__ufzk < vek__foy:
        atp__mgof = rya__ufzk + (vek__foy - rya__ufzk >> 1)
        if key > getitem_arr_tup(arr, base + atp__mgof):
            rya__ufzk = atp__mgof + 1
        else:
            vek__foy = atp__mgof
    assert rya__ufzk == vek__foy
    return vek__foy


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    vek__foy = 1
    rya__ufzk = 0
    if key < getitem_arr_tup(arr, base + hint):
        jxnr__udyo = hint + 1
        while vek__foy < jxnr__udyo and key < getitem_arr_tup(arr, base +
            hint - vek__foy):
            rya__ufzk = vek__foy
            vek__foy = (vek__foy << 1) + 1
            if vek__foy <= 0:
                vek__foy = jxnr__udyo
        if vek__foy > jxnr__udyo:
            vek__foy = jxnr__udyo
        tmp = rya__ufzk
        rya__ufzk = hint - vek__foy
        vek__foy = hint - tmp
    else:
        jxnr__udyo = _len - hint
        while vek__foy < jxnr__udyo and key >= getitem_arr_tup(arr, base +
            hint + vek__foy):
            rya__ufzk = vek__foy
            vek__foy = (vek__foy << 1) + 1
            if vek__foy <= 0:
                vek__foy = jxnr__udyo
        if vek__foy > jxnr__udyo:
            vek__foy = jxnr__udyo
        rya__ufzk += hint
        vek__foy += hint
    assert -1 <= rya__ufzk and rya__ufzk < vek__foy and vek__foy <= _len
    rya__ufzk += 1
    while rya__ufzk < vek__foy:
        atp__mgof = rya__ufzk + (vek__foy - rya__ufzk >> 1)
        if key < getitem_arr_tup(arr, base + atp__mgof):
            vek__foy = atp__mgof
        else:
            rya__ufzk = atp__mgof + 1
    assert rya__ufzk == vek__foy
    return vek__foy


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
        jou__lsvf = 0
        gpfp__blr = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                gpfp__blr += 1
                jou__lsvf = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                jou__lsvf += 1
                gpfp__blr = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not jou__lsvf | gpfp__blr < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            jou__lsvf = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if jou__lsvf != 0:
                copyRange_tup(tmp, cursor1, arr, dest, jou__lsvf)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, jou__lsvf)
                dest += jou__lsvf
                cursor1 += jou__lsvf
                len1 -= jou__lsvf
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            gpfp__blr = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if gpfp__blr != 0:
                copyRange_tup(arr, cursor2, arr, dest, gpfp__blr)
                copyRange_tup(arr_data, cursor2, arr_data, dest, gpfp__blr)
                dest += gpfp__blr
                cursor2 += gpfp__blr
                len2 -= gpfp__blr
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
            if not jou__lsvf >= MIN_GALLOP | gpfp__blr >= MIN_GALLOP:
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
        jou__lsvf = 0
        gpfp__blr = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                jou__lsvf += 1
                gpfp__blr = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                gpfp__blr += 1
                jou__lsvf = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not jou__lsvf | gpfp__blr < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            jou__lsvf = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if jou__lsvf != 0:
                dest -= jou__lsvf
                cursor1 -= jou__lsvf
                len1 -= jou__lsvf
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, jou__lsvf)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    jou__lsvf)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            gpfp__blr = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if gpfp__blr != 0:
                dest -= gpfp__blr
                cursor2 -= gpfp__blr
                len2 -= gpfp__blr
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, gpfp__blr)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    gpfp__blr)
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
            if not jou__lsvf >= MIN_GALLOP | gpfp__blr >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    ddgsl__bnwlp = len(key_arrs[0])
    if tmpLength < minCapacity:
        lapw__fgp = minCapacity
        lapw__fgp |= lapw__fgp >> 1
        lapw__fgp |= lapw__fgp >> 2
        lapw__fgp |= lapw__fgp >> 4
        lapw__fgp |= lapw__fgp >> 8
        lapw__fgp |= lapw__fgp >> 16
        lapw__fgp += 1
        if lapw__fgp < 0:
            lapw__fgp = minCapacity
        else:
            lapw__fgp = min(lapw__fgp, ddgsl__bnwlp >> 1)
        tmp = alloc_arr_tup(lapw__fgp, key_arrs)
        tmp_data = alloc_arr_tup(lapw__fgp, data)
        tmpLength = lapw__fgp
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        gnryl__tgq = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = gnryl__tgq


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    hmaz__uqb = arr_tup.count
    iswcm__kbyhm = 'def f(arr_tup, lo, hi):\n'
    for i in range(hmaz__uqb):
        iswcm__kbyhm += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        iswcm__kbyhm += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        iswcm__kbyhm += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    iswcm__kbyhm += '  return\n'
    ildyc__awjq = {}
    exec(iswcm__kbyhm, {}, ildyc__awjq)
    ugdli__whtxc = ildyc__awjq['f']
    return ugdli__whtxc


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    hmaz__uqb = src_arr_tup.count
    assert hmaz__uqb == dst_arr_tup.count
    iswcm__kbyhm = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(hmaz__uqb):
        iswcm__kbyhm += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    iswcm__kbyhm += '  return\n'
    ildyc__awjq = {}
    exec(iswcm__kbyhm, {'copyRange': copyRange}, ildyc__awjq)
    vgzre__vurc = ildyc__awjq['f']
    return vgzre__vurc


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    hmaz__uqb = src_arr_tup.count
    assert hmaz__uqb == dst_arr_tup.count
    iswcm__kbyhm = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(hmaz__uqb):
        iswcm__kbyhm += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    iswcm__kbyhm += '  return\n'
    ildyc__awjq = {}
    exec(iswcm__kbyhm, {'copyElement': copyElement}, ildyc__awjq)
    vgzre__vurc = ildyc__awjq['f']
    return vgzre__vurc


def getitem_arr_tup(arr_tup, ind):
    myes__gue = [arr[ind] for arr in arr_tup]
    return tuple(myes__gue)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    hmaz__uqb = arr_tup.count
    iswcm__kbyhm = 'def f(arr_tup, ind):\n'
    iswcm__kbyhm += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'
        .format(i) for i in range(hmaz__uqb)]), ',' if hmaz__uqb == 1 else '')
    ildyc__awjq = {}
    exec(iswcm__kbyhm, {}, ildyc__awjq)
    ivd__jooo = ildyc__awjq['f']
    return ivd__jooo


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, yqld__juksr in zip(arr_tup, val_tup):
        arr[ind] = yqld__juksr


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    hmaz__uqb = arr_tup.count
    iswcm__kbyhm = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(hmaz__uqb):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            iswcm__kbyhm += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            iswcm__kbyhm += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    iswcm__kbyhm += '  return\n'
    ildyc__awjq = {}
    exec(iswcm__kbyhm, {}, ildyc__awjq)
    ivd__jooo = ildyc__awjq['f']
    return ivd__jooo


def test():
    import time
    quj__kfqiq = time.time()
    oqtd__yusrv = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((oqtd__yusrv,), 0, 3, data)
    print('compile time', time.time() - quj__kfqiq)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    fmtgh__mnsbz = np.random.ranf(n)
    mgc__utdks = pd.DataFrame({'A': fmtgh__mnsbz, 'B': data[0], 'C': data[1]})
    quj__kfqiq = time.time()
    pwmn__wci = mgc__utdks.sort_values('A', inplace=False)
    mafb__odk = time.time()
    sort((fmtgh__mnsbz,), 0, n, data)
    print('Bodo', time.time() - mafb__odk, 'Numpy', mafb__odk - quj__kfqiq)
    np.testing.assert_almost_equal(data[0], pwmn__wci.B.values)
    np.testing.assert_almost_equal(data[1], pwmn__wci.C.values)


if __name__ == '__main__':
    test()
