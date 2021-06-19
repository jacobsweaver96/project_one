from typing import List

from src.infrastructure.core.base_core import BaseCore
from src.structure.groups.types.group_element import GroupElement
from src.structure.sets.integers.omni_integer import OmniInteger


class Group:
    def __init__(self, modulo: OmniInteger, core: BaseCore):
        self.modulo = modulo
        self.__core = core
        self.elements = dict()
        self.sub_groups = dict()
        self.is_simple = True
        self.totient = None

    def initialize(self):
        elem_range = self.__core.range(self.modulo, exclusive=True)
        for elem in elem_range:
            self.elements[elem] = GroupElement(elem, self.__core)

    def set_sub_groups(self, sub_groups: List['Group']):
        for sub_group in sub_groups:
            self.sub_groups[sub_group.modulo] = sub_group
        self.is_simple = False

    def set_totient(self, totient: OmniInteger):
        self.totient = totient

    def __hash__(self):
        return hash(self.modulo)

    def __eq__(self, other):
        return self.modulo == other.modulo
