from sympy import factorint, perfect_power, totient, gcd, discrete_log

from src.infrastructure.core.base_core import BaseCore
from src.infrastructure.cache.factor_cache import FactorCollectionCache
from src.infrastructure.cache.unity_cache import UnityCache
from src.infrastructure.omni_component import OmniComponent
from src.infrastructure.service.compatibility_component import CompatibilityComponent
from src.structure.sets.integers.omni_integer import OmniInteger, IntegerEnum


class ComputationComponent(OmniComponent):
    def __init__(self, unity_cache: UnityCache, core: BaseCore,
                 compatibility_component: CompatibilityComponent
                 ):
        super(ComputationComponent, self).__init__(unity_cache, core)
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

    def is_coprime(self, left: OmniInteger, right: OmniInteger) -> bool:
        left_int = left.get_val()
        right_int = right.get_val()
        v_gcd = gcd(left_int, right_int)
        return v_gcd == 1

    def discrete_log(self, modulo: OmniInteger, target: OmniInteger, base: OmniInteger) -> OmniInteger:
        modulo_int = modulo.get_val()
        target_int = target.get_val()
        base_int = base.get_val()
        d_log = discrete_log(modulo_int, target_int, base_int)

        if d_log is None or d_log <= 0:
            return self.core.inv_identity
        return self.core.__cons__(d_log)

    def exponential_mod(self, base, exp, modulo):
        base_pow_spare = self.core.mod(base, modulo)
        if exp == self.core.m_identity:
            return base_pow_spare
        exp_log = self.core.log_floor(exp, 2)
        partition_powers = []
        partition_powers.append(base_pow_spare)

        for __ in self.core.range(exp_log):
            base_pow_spare = self.core.mod(self.core.multiply(base_pow_spare, base_pow_spare), modulo)
            partition_powers.append(base_pow_spare)

        partition_powers.reverse()
        log_spare = exp_log
        exp_spare = exp
        base_result = self.core.m_identity
        for power in partition_powers:
            power_spare = self.core.power(log_spare, 2)
            log_spare = self.core.sub(log_spare, 1)
            if not self.core.is_greater(power_spare, exp_spare):
                base_result = self.core.mod(self.core.multiply(base_result, power), modulo)
                exp_spare = self.core.sub(exp_spare, power_spare)

        return base_result
