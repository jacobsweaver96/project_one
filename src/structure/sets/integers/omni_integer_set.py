from typing import Optional, List, Callable

from src.infrastructure.core.base_core import BaseCore
from src.structure.sets.integers.omni_integer import OmniInteger
from src.structure.sets.omni_set import OmniSet


def __identity_func__(val):
    return val


class OmniIntegerSet(OmniSet[str, OmniInteger, int]):
    def __init__(self, core: BaseCore, name="Z", conditional: Callable[[Optional[OmniInteger]], Optional[OmniInteger]] = __identity_func__):
        super(OmniIntegerSet, self).__init__(name)
        self.__core = core
        self.__conditional = conditional

    def get_member(self, index: int) -> Optional[OmniInteger]:
        return self.__conditional(self.__core.__cons__(index))

    def get_subset(self, name: str, conditional: Callable[[Optional[OmniInteger]], Optional[OmniInteger]]) -> 'OmniIntegerSet':
        def conditional_wrapper(val):
            return conditional(self.__conditional(val))

        return OmniIntegerSet(self.__core, name, conditional_wrapper)

    def get_range(self, stop: int, start=0, exclusive=False) -> List[OmniInteger]:
        ls = []
        for val in range(start, stop):
            ls.append(self.__cons__(val))
        if not exclusive:
            ls.append(self.__cons__(stop))
        return ls
