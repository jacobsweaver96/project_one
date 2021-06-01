from enum import Enum


class LibEnum(Enum):
    default = 1


class ComponentConfig:
    def __init__(self):
        self.__core_lib = LibEnum.default

    def set_core_lib(self, lib: LibEnum) -> None:
        self.__core_lib = lib

    def get_core_lib(self) -> LibEnum:
        return self.__core_lib
