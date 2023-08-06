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
            sqmp__btu = set()
            xoo__rodg = list(self.context._get_attribute_templates(self.key))
            ohrw__fklot = xoo__rodg.index(self) + 1
            for hccw__cqimi in range(ohrw__fklot, len(xoo__rodg)):
                if isinstance(xoo__rodg[hccw__cqimi], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    sqmp__btu.add(xoo__rodg[hccw__cqimi]._attr)
            self._attr_set = sqmp__btu
        return attr_name in self._attr_set
