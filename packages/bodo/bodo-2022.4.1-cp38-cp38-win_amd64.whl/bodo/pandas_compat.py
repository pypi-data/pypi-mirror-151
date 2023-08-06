import hashlib
import inspect
import warnings
import pandas as pd
pandas_version = tuple(map(int, pd.__version__.split('.')[:2]))
_check_pandas_change = False
if pandas_version < (1, 4):

    def _set_noconvert_columns(self):
        assert self.orig_names is not None
        ijwpx__fgzv = {myaz__bxsb: dqgg__cpro for dqgg__cpro, myaz__bxsb in
            enumerate(self.orig_names)}
        fqc__markr = [ijwpx__fgzv[myaz__bxsb] for myaz__bxsb in self.names]
        usqh__yew = self._set_noconvert_dtype_columns(fqc__markr, self.names)
        for bon__vjrl in usqh__yew:
            self._reader.set_noconvert(bon__vjrl)
    if _check_pandas_change:
        lines = inspect.getsource(pd.io.parsers.c_parser_wrapper.
            CParserWrapper._set_noconvert_columns)
        if (hashlib.sha256(lines.encode()).hexdigest() !=
            'afc2d738f194e3976cf05d61cb16dc4224b0139451f08a1cf49c578af6f975d3'
            ):
            warnings.warn(
                'pd.io.parsers.c_parser_wrapper.CParserWrapper._set_noconvert_columns has changed'
                )
    (pd.io.parsers.c_parser_wrapper.CParserWrapper._set_noconvert_columns
        ) = _set_noconvert_columns
