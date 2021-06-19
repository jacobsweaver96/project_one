from enum import Enum
from src.infrastructure.core.base_core import BaseCore
from src.structure.sets.integers.omni_integer import OmniInteger


class CacheStatus(Enum):
    Miss = 1
    Hit = 2


class CacheElement:
    def __init__(self, source: OmniInteger, status: CacheStatus, elem=None):
        self.__source = source
        self.__status = status
        self.__elem = elem

    def has_value(self):
        return self.__status == CacheStatus.Hit

    def get_value(self):
        return self.__elem

    def get_source(self):
        return self.__source


class OmniCache:
    def __init__(self, core: BaseCore):
        self.__core = core
        self.__cache = dict()

    def get_core(self) -> BaseCore:
        return self.__core

    def get_cache(self) -> dict:
        return self.__cache

    def has_cache(self, n: OmniInteger) -> bool:
        return self.__cache.__contains__(n)

    @staticmethod
    def create_cache_miss(source: OmniInteger) -> CacheElement:
        return CacheElement(source, CacheStatus.Miss)
