from src.infrastructure.core.base_core import BaseCore
from src.infrastructure.cache.unity_cache import UnityCache


class OmniComponent:
    def __init__(self, unity_cache: UnityCache, core: BaseCore):
        self.__unity_cache = unity_cache
        self.factor_cache = unity_cache.get_factor_cache()
        self.totient_cache = unity_cache.get_totient_cache()
        self.core = core
