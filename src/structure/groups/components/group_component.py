from typing import Dict, Set

from src.computation.components.computation_component import ComputationComponent
from src.infrastructure.core.base_core import BaseCore
from src.structure.groups.types.group import Group
from src.structure.groups.types.group_config import GroupConfig
from src.structure.groups.types.group_element import GroupElement
from src.infrastructure.cache.unity_cache import UnityCache
from src.infrastructure.omni_component import OmniComponent
from src.structure.sets.integers.omni_integer import OmniInteger


class GroupComponent(OmniComponent):
    def __init__(self, unity_cache: UnityCache, core: BaseCore,
                 computation_component: ComputationComponent):
        super(GroupComponent, self).__init__(unity_cache, core)
        self.__computation_component = computation_component

    def create_group(self, config: GroupConfig):
        group = Group(config.modulo, self.core)
        group.initialize()
        group.totient = self.__computation_component.totient_int(config.modulo)
        self.__find_add_inverses__(group)

        if config.find_multiplicative_inverses:
            self.__find_mul_inverses__(group)
        if config.find_totients:
            self.__find_totients__(group)
        if config.find_factors:
            self.__find_factors__(group)
        if config.find_residues:
            self.__find_residues__(group, config.residue_roots)
        if config.find_sub_groups:
            sub_group_config = config.sub_group_config
            if sub_group_config is None:
                sub_group_config = config
            self.__find_sub_groups__(group, sub_group_config)
        if config.find_quotients:
            self.__find_quotients__(group, config.quotient_divisors)
        if config.find_quotient_relatables:
            self.__find_quotient_relatables__(group, config.quotient_relatables)
        return group

    def find_residue_paths(self, group: Group) -> Dict[OmniInteger, Set['GroupElement']]:
        g_totient = group.totient

        d_indices = self.core.range(g_totient)
        self.__find_residues__(group, d_indices)
        identity_elem = group.elements[self.core.m_identity]
        identity_roots = identity_elem.get_roots()
        return identity_roots

    def count_residue_paths(self, group: Group, unique=True) -> Dict[OmniInteger, OmniInteger]:
        identity_roots = self.find_residue_paths(group)
        index_store = set()
        index_count_map = dict()

        for n_root in identity_roots.keys():
            n_root_set = identity_roots[n_root]
            index_count = len(n_root_set)
            if unique:
                filter_roots = n_root_set.symmetric_difference(n_root_set.intersection(index_store))
                index_count = len(filter_roots)
                index_store.update(n_root_set)
            index_count_map[n_root] = self.core.__cons__(index_count)
        return index_count_map

    def __find_add_inverses__(self, group: Group):
        elems = group.elements
        for elem_key in elems.keys():
            elem = elems[elem_key]
            inv_int = self.core.sub(group.modulo, elem_key)
            elem.set_add_inverse(elems[inv_int])

    def __find_mul_inverses__(self, group: Group):
        elems = group.elements
        g_totient = group.totient
        for elem_key in elems.keys():
            elem = elems[elem_key]
            inv_int = self.__computation_component.exponential_mod(elem_key, self.core.sub(g_totient, self.core.m_identity), group.modulo)
            if elems.keys().__contains__(inv_int):
                elem.set_mul_inverse(elems[inv_int])

    def __find_totients__(self, group: Group):
        elems = group.elements
        for elem_key in elems:
            elem = elems[elem_key]
            totient = self.__computation_component.totient_int(elem.id)
            totient_elem = elems[totient]
            elem.set_totient(totient_elem)

    def __find_factors__(self, group: Group):
        elems = group.elements
        for elem_key in elems.keys():
            elem = elems[elem_key]
            factors = self.__computation_component.factor_int(elem.id)
            grouped_factors = []
            for factor in factors.get_entries().keys():
                if elems.keys().__contains__(factor):
                    group_factor = elems[factor]
                    grouped_factors.append(group_factor)
            elem.set_factors(grouped_factors)

    def __find_residues__(self, group: Group, roots):
        elems = group.elements
        for elem_key in elems.keys():
            elem = elems[elem_key]
            for root in roots:
                omni_root = self.core.__cons__(root)
                residue = self.__computation_component.exponential_mod(elem.id, omni_root, group.modulo)
                if elems.keys().__contains__(residue):
                    elems[residue].add_nth_root(elem, omni_root)
                    elem.add_index(elems[residue], root)

    def __find_quotients__(self, group: Group, divisors):
        elems = group.elements
        divisor_map = dict()
        for divisor in divisors:
            divisor_elem = elems[divisor]
            divisor_elem_inv = divisor_elem.get_mul_inverse()
            if divisor_elem_inv is None:
                inv_int = self.__computation_component.exponential_mod(divisor, self.core.sub(group.totient, self.core.m_identity), group.modulo)
                if elems.keys().__contains__(inv_int):
                    divisor_elem_inv = elems[inv_int]
                    divisor_elem.set_mul_inverse(divisor_elem_inv)
                else:
                    continue
            divisor_map[divisor] = divisor_elem_inv.id
        for elem_key in elems.keys():
            elem = elems[elem_key]
            for divisor in divisor_map.keys():
                divisor_operand = divisor_map[divisor]
                divisor_prod = self.core.mod(self.core.multiply(elem.id, divisor_operand), group.modulo)
                if elems.keys().__contains__(divisor_prod):
                    divisor_prod_elem = elems[divisor_prod]
                    elem.add_quotient(divisor_prod_elem, divisor)

    def __find_quotient_relatables__(self, group: Group, relatables):
        elems = group.elements
        relatable_elems = []
        for relatable in relatables:
            if not elems.keys().__contains__(relatable):
                continue
            relatable_elem = elems[relatable]
            relatable_elems.append(relatable_elem)
        for elem_key in elems.keys():
            elem = elems[elem_key]
            elem_inv = elem.get_mul_inverse()
            if elem_inv is None:
                inv_int = self.__computation_component.exponential_mod(elem.id, self.core.sub(group.totient, self.core.m_identity), group.modulo)
                if elems.keys().__contains__(inv_int):
                    elem_inv = elems[inv_int]
                    elem.set_mul_inverse(elem_inv)
                else:
                    continue
            elem_inv_id = elem_inv.id
            for relatable_elem in relatable_elems:
                relatable_id = relatable_elem.id
                relatable_prod = self.core.mod(self.core.multiply(elem_inv_id, relatable_id), group.modulo)
                if elems.keys().__contains__(relatable_prod):
                    relatable_prod_elem = elems[relatable_prod]
                    elem.add_quotient_relation(relatable_prod_elem, relatable_id)

    def __find_sub_groups__(self, group: Group, sub_group_config: GroupConfig):
        g_modulo = group.modulo
        g_factors = self.__computation_component.factor_int(g_modulo).get_entries()
        sub_groups = []
        for factor_key in g_factors.keys():
            if factor_key == g_modulo:
                continue
            factor_group = self.create_group(sub_group_config.to_copy(factor_key.get_val()))
            sub_groups.append(factor_group)
        group.set_sub_groups(sub_groups)
