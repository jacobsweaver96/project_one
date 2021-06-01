from sympy import factorint, perfect_power, totient

from src.computation_engine.components.core.base_core import BaseCore
from src.infrastructure.cache.factor_cache import FactorCollectionCache
from src.infrastructure.cache.unity_cache import UnityCache
from src.infrastructure.omni_component import OmniComponent
from src.infrastructure.service.compatibility_component import CompatibilityComponent
from src.infrastructure.types.omni_integer import OmniInteger, IntegerEnum


class FactorComponent(OmniComponent):
    def __init__(self, unity_cache: UnityCache, core: BaseCore,
                 compatibility_component: CompatibilityComponent
                 ):
        super(FactorComponent, self).__init__(unity_cache, core)
        self.__compatibility_component = compatibility_component

    def factor_int(self, n: OmniInteger) -> FactorCollectionCache:
        has_cache = self.factor_cache.has_cache(n)
        if has_cache:
            return self.factor_cache.get_cache(n)
        g_val = self.__compatibility_component.int_type_guard(n, IntegerEnum.default)
        factors = factorint(g_val)
        f_cache = self.factor_cache.upsert_cache(n, factors)
        return f_cache

    # TODO cache
    def is_perfect_power_of(self, n: OmniInteger, base=None) -> bool:
        g_val = self.__compatibility_component.int_type_guard(n, IntegerEnum.default)
        candidates = None
        if base is not None:
            candidates = [base]
        is_pow = perfect_power(g_val, candidates=candidates)
        return is_pow

    def totient_int(self, n: OmniInteger) -> OmniInteger:
        t_cache = self.totient_cache.get_totient_cache(n)
        if t_cache.has_value():
            return t_cache.get_value()
        g_val = self.__compatibility_component.int_type_guard(n, IntegerEnum.default)
        n_totient = totient(g_val)
        src_totient = self.core.__cons__(n_totient)
        self.totient_cache.upsert_cache(n, src_totient)
        return src_totient

    def totient_log_int(self, n: OmniInteger) -> OmniInteger:
        t_cache = self.totient_cache.get_totient_log_cache(n)
        if t_cache.has_value():
            return t_cache.get_log().get_value()
        n_tot = self.totient_int(n)
        n_spare = n_tot
        tot_log = 1

        while self.core.is_greater(n_spare, self.core.m_identity):
            n_spare = self.totient_int(n_spare)
            tot_log = tot_log + 1

        src_tot_log = self.core.__cons__(tot_log)
        self.totient_cache.upsert_cache(n, n_tot, src_tot_log)
        return src_tot_log

    def totient_log_range(self, n_range: OmniInteger) -> dict:
        tot_set = dict()
        g_range = self.__compatibility_component.int_type_guard(n_range, IntegerEnum.default)
        for val in self.core.range(g_range):
            tot_set[val] = self.totient_log_int(val)
        return tot_set
