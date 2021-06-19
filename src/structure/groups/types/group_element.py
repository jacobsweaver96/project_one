from typing import Set, Dict, List

from src.infrastructure.core.base_core import BaseCore
from src.structure.sets.integers.omni_integer import OmniInteger


class GroupElement:
    def __init__(self, n: OmniInteger, core: BaseCore):
        self.id = n
        self.__core = core
        self.__mul_inverse = None
        self.__add_inverse = None
        self.__totient = None
        self.__factors = []
        self.__roots = dict()
        # key: target element id (OmniInteger), value: exponential count (OmniInteger)
        self.__indices = dict()
        # key: divisor, value: dividend
        self.__quotients = dict()
        # key: (OmniInteger) relation r, value: (element) product p, such that np=r
        self.__quotient_relations = dict()

    def get_mul_inverse(self) -> 'GroupElement':
        return self.__mul_inverse

    def set_mul_inverse(self, elem: 'GroupElement'):
        self.__mul_inverse = elem

    def get_add_inverse(self) -> 'GroupElement':
        return self.__add_inverse

    def set_add_inverse(self, elem: 'GroupElement'):
        self.__add_inverse = elem

    def get_roots(self) -> Dict[OmniInteger, Set['GroupElement']]:
        return self.__roots

    def get_nth_roots(self, n_root: OmniInteger) -> Set['GroupElement']:
        if self.__roots.__contains__(n_root):
            return self.__roots[n_root]
        return set()

    def add_nth_root(self, root_elem: 'GroupElement', n_root: OmniInteger):
        if not self.__roots.keys().__contains__(n_root):
            self.__roots[n_root] = set()
        self.__roots[n_root].add(root_elem)

    def get_indices(self) -> Dict['GroupElement', Set[OmniInteger]]:
        return self.__indices

    def get_indices_of(self, target_elem: 'GroupElement') -> Set[OmniInteger]:
        if self.__indices.keys().__contains__(target_elem):
            return self.__indices[target_elem]
        return set()

    def get_min_index_of(self, target_elem: 'GroupElement') -> OmniInteger:
        indices = self.get_indices_of(target_elem)
        if len(indices) == 0:
            return OmniInteger(0)
        min_index = None
        for index in indices:
            if min_index is None or self.__core.is_greater(min_index, index):
                min_index = index
        return min_index

    def add_index(self, target_elem: 'GroupElement', index: OmniInteger):
        if not self.__indices.keys().__contains__(target_elem):
            self.__indices[target_elem] = set()
        self.__indices[target_elem].add(index)

    def get_quotient_of(self, divisor: OmniInteger) -> 'GroupElement':
        if not self.__quotients.keys().__contains__(divisor):
            return self
        return self.__quotients[divisor]

    def add_quotient(self, dividend_elem: 'GroupElement', divisor: OmniInteger):
        self.__quotients[divisor] = dividend_elem

    def get_quotient_relation_to(self, relatable: OmniInteger) -> 'GroupElement':
        if not self.__quotient_relations.keys().__contains__(relatable):
            return self
        return self.__quotient_relations[relatable]

    def add_quotient_relation(self, product_elem: 'GroupElement', relatable: OmniInteger):
        self.__quotient_relations[relatable] = product_elem

    def get_totient(self) -> 'GroupElement':
        return self.__totient

    def set_totient(self, elem: 'GroupElement'):
        self.__totient = elem

    def get_factors(self) -> List['GroupElement']:
        return self.__factors

    def set_factors(self, factors: List['GroupElement']):
        self.__factors = factors

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f'{self.id}'

    def __repr__(self):
        return f'{self.id}'
