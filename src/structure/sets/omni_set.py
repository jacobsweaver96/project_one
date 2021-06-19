from typing import Generic, TypeVar, Optional, Iterable, Callable

from src.infrastructure.omni_types.omni_object import OmniObject

TSetIndex = TypeVar('TSetIndex')
TSetMember = TypeVar('TSetMember')
TSetMemberIndex = TypeVar('TSetMemberIndex')


class OmniSet(Generic[TSetIndex, TSetMember, TSetMemberIndex], OmniObject[TSetIndex]):
    def __init__(self, index: TSetIndex):
        super(OmniSet, self).__init__(index)

    def get_member(self, index: TSetMemberIndex) -> Optional[TSetMember]:
        raise NotImplementedError("get_member not implemented")

    def get_subset(self, name: str, conditional: Callable[[Optional[TSetMember]], Optional[TSetMember]]) -> 'OmniSet[TSetIndex, TSetMember, TSetMemberIndex]':
        raise NotImplementedError("get_subset not implemented")
