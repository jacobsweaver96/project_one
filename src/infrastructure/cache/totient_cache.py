from src.computation_engine.components.core.base_core import BaseCore
from src.infrastructure.cache.omni_cache import OmniCache, CacheElement, CacheStatus
from src.infrastructure.types.omni_integer import OmniInteger


class TotientCacheElement(CacheElement):
    def __init__(self, source: OmniInteger, totient: OmniInteger, totient_log=None, status=CacheStatus.Hit):
        super(TotientCacheElement, self).__init__(source, status, totient)
        log_status = CacheStatus.Miss
        if totient_log is not None:
            log_status = CacheStatus.Hit
        self.__totient_log = CacheElement(source, log_status, totient_log)

    def get_log(self) -> CacheElement:
        return self.__totient_log


class TotientCache(OmniCache):
    def __init__(self, core: BaseCore):
        super(TotientCache, self).__init__(core)

    def get_totient_cache(self, n: OmniInteger) -> TotientCacheElement:
        has_cache = self.has_cache(n)
        if has_cache:
            return super().get_cache()[n]
        return TotientCacheElement(n, self.get_core().inv_identity, status=CacheStatus.Miss)

    def get_totient_log_cache(self, n: OmniInteger) -> TotientCacheElement:
        t_cache = self.get_totient_cache(n)
        if not t_cache.has_value() or t_cache.get_log().has_value():
            return t_cache
        return TotientCacheElement(n, t_cache.get_value(), status=CacheStatus.Miss)

    def upsert_cache(self, n: OmniInteger, totient: OmniInteger, totient_log=None) -> TotientCacheElement:
        t_cache = TotientCacheElement(n, totient, totient_log=totient_log)
        super().get_cache()[n] = t_cache
        if isinstance(totient_log, OmniInteger):
            tail_cache = self.get_totient_cache(totient)
            if tail_cache.has_value():
                tail_src = tail_cache.get_source()
                tail_val = tail_cache.get_value()
                self.upsert_cache(tail_src, tail_val, self.get_core().sub(totient_log, self.get_core().m_identity))
        return t_cache
