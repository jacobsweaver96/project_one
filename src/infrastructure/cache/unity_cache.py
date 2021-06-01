from src.infrastructure.cache.factor_cache import FactorCache
from src.infrastructure.cache.totient_cache import TotientCache


class UnityCache:
    def __init__(self,
                 factor_cache: FactorCache,
                 totient_cache: TotientCache):
        self.__factor_cache = factor_cache
        self.__totient_cache = totient_cache

    def get_factor_cache(self):
        return self.__factor_cache

    def get_totient_cache(self):
        return self.__totient_cache
