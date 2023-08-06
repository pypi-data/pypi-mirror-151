"""
Helper functions and classes to simplify Template Generation
for Bodo classes.
"""
import numba
from numba.core.typing.templates import AttributeTemplate


class OverloadedKeyAttributeTemplate(AttributeTemplate):
    _attr_set = None

    def _is_existing_attr(self, attr_name):
        if self._attr_set is None:
            dxrx__esv = set()
            vspt__frq = list(self.context._get_attribute_templates(self.key))
            dink__adf = vspt__frq.index(self) + 1
            for jerh__pba in range(dink__adf, len(vspt__frq)):
                if isinstance(vspt__frq[jerh__pba], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    dxrx__esv.add(vspt__frq[jerh__pba]._attr)
            self._attr_set = dxrx__esv
        return attr_name in self._attr_set
