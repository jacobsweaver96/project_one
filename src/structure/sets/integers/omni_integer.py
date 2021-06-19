from enum import Enum

from src.infrastructure.omni_types.omni_object import OmniObject


class IntegerEnum(Enum):
    default = 1


class OmniInteger(OmniObject[int]):
    def __init__(self, index, int_type: IntegerEnum = IntegerEnum.default) -> None:
        super(OmniInteger, self).__init__(index)
        self.__val = index
        self.__int_type = int_type

    def get_val(self):
        return self.__val

    def get_val_type(self):
        return self.__int_type

    def __hash__(self):
        if self.__int_type is IntegerEnum.default:
            return hash(self.__val)
        else:
            return hash(self.__val)

    def __eq__(self, other):
        return self.__val == other.__val

    def __str__(self):
        return f'{self.__val}'

    def __repr__(self):
        return f'{self.__val}'
