from enum import Enum


class IntegerEnum(Enum):
    default = 1


class OmniInteger:
    def __init__(self, n, int_type: IntegerEnum = IntegerEnum.default) -> None:
        self.__val = n
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
