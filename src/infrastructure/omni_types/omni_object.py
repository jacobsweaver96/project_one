from typing import Generic, TypeVar

TIndex = TypeVar('TIndex')


class OmniObject(Generic[TIndex]):
    def __init__(self, index: TIndex):
        super(OmniObject, self).__init__()
        self.__index = index

    def get_index(self) -> TIndex:
        return self.__index

    def __hash__(self):
        return hash(self.__index)
