from src.infrastructure.core.base_core import BaseCore
from src.structure.sets.integers.omni_integer import OmniInteger
from src.query.types.request.query_config import QueryConfig
from src.query.types.request.query_factor import QueryFactor
from src.query.types.request.query_options import QueryOptions


class QueryBuilder:
    def __init__(self, core: BaseCore):
        self.factors = dict()
        self.__core = core
        self.config = QueryConfig(self.__core.m_identity, self.__core.a_identity, False)

    def include_totient(self, tot_length: OmniInteger = None):
        self.config.find_totient = True
        t_length = tot_length
        if t_length is None:
            t_length = self.__core.inv_identity
        self.config.tot_length = t_length

    def set_range(self, range_int: OmniInteger):
        self.config.range_int = range_int

    def include_factor(self, n: OmniInteger):
        factor = QueryFactor(n)
        self.factors[n] = factor

    def build(self):
        query = QueryOptions(self.config, self.factors)
        return query
