from typing import TypeVar, Generic, Optional, Callable

from src.infrastructure.core.base_core import BaseCore
from src.structure.sets.omni_set import OmniSet
from src.structure.sets.integers.omni_integer import OmniInteger

TGroupIndex = TypeVar('TGroupIndex')
TSetIndex = TypeVar('TSetIndex')
TSetMember = TypeVar('TSetMember')
TSetMemberIndex = TypeVar('TSetMemberIndex')


class OmniGroup(Generic[TGroupIndex, TSetIndex, TSetMember, TSetMemberIndex],
                OmniSet[TGroupIndex, TSetMember, TSetMemberIndex]):
    def __init__(self, index: TGroupIndex,
                 core: BaseCore,

                 group_set: OmniSet[TSetIndex, TSetMember, TSetMemberIndex]):
        self.__core = core
        self.__set = group_set
        self.index = index

    def get_member(self, index: TSetMemberIndex) -> Optional[TSetMember]:
        return self.__set.get_member(index)

    def get_subset(self, name: TSetIndex, conditional: Callable[[Optional[TSetMember]], Optional[TSetMember]]):
        return self.__set.get_subset(name, conditional)
