from src.computation_engine.components.core.base_core import BaseCore
from src.infrastructure.cache.omni_cache import OmniCache, CacheElement, CacheStatus
from src.infrastructure.types.omni_integer import OmniInteger, IntegerEnum

from enum import Enum


class PrimalityEnum(Enum):
    unknown = 1
    prime = 2
    composite = 3


class FactorElementCache:
    def __init__(self, n: OmniInteger, k: OmniInteger, primality: PrimalityEnum):
        self.n = n
        self.k = k
        self.primality = primality


class FactorCollectionCache(CacheElement):
    def __init__(self, source: OmniInteger, core: BaseCore, status=CacheStatus.Hit):
        self.__collection = dict()
        super(FactorCollectionCache, self).__init__(source, status, self.__collection)
        self.__core = core

    def has_entry(self, n: OmniInteger) -> bool:
        return self.__collection.__contains__(n)

    def upsert_entry(self, elements: list) -> None:
        for e in elements:
            self.__collection[e.n] = e

    def get_entries(self) -> dict:
        return self.__collection


class FactorCache(OmniCache):
    def __init__(self, core: BaseCore):
        super(FactorCache, self).__init__(core)

    def get_cache(self, n: OmniInteger) -> FactorCollectionCache:
        has_cache = self.has_cache(n)
        if has_cache:
            return self.__cache[n]
        return FactorCollectionCache(n, self.get_core(), CacheStatus.Miss)

    def upsert_cache(self, n: OmniInteger, f_set: dict) -> FactorCollectionCache:
        f_cache = self.get_cache(n)
        if not f_cache.has_value():
            f_cache = FactorCollectionCache(n, self.get_core())
        f_elems = list()
        for f_prime in f_set.keys():
            f_pow = f_set[f_prime]
            omni_prime = OmniInteger(f_prime, IntegerEnum.default)
            omni_pow = OmniInteger(f_pow, IntegerEnum.default)
            f_entry = FactorElementCache(omni_prime, omni_pow, PrimalityEnum.prime)
            f_elems.append(f_entry)
        f_cache.upsert_entry(f_elems)
        super().get_cache()[n] = f_cache
        return f_cache


