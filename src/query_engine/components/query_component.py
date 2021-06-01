from src.computation_engine.components.core.base_core import BaseCore
from src.computation_engine.components.factor_component import FactorComponent
from src.infrastructure.cache.unity_cache import UnityCache
from src.infrastructure.omni_component import OmniComponent
from src.query_engine.components.query_builder import QueryBuilder
from src.query_engine.types.request.query_options import QueryOptions
from src.query_engine.types.result.result_query import QueryDataCollection, QueryDataElement


class QueryComponent(OmniComponent):
    def __init__(self, unity_cache: UnityCache, core: BaseCore,
                 factor_component: FactorComponent):
        super(QueryComponent, self).__init__(unity_cache, core)
        self.__factor_component = factor_component

    def get_query_builder(self) -> QueryBuilder:
        return QueryBuilder(self.core)

    def search(self, query: QueryOptions) -> QueryDataCollection:
        query_config = query.config
        query_range = query_config.range_int
        find_totient = query_config.find_totient
        totient_depth = query_config.tot_length
        find_totient_log = find_totient and self.core.is_greater(self.core.m_identity, totient_depth)

        q_data_set = dict()

        for q_int in self.core.range(query_range):
            q_data_set[q_int] = QueryDataElement(q_int)

        for q_key in q_data_set.keys():
            q_elem = q_data_set[q_key]
            q_elem.factor_set = self.__factor_component.factor_int(q_key).get_entries()

        if find_totient:
            for q_key in q_data_set.keys():
                q_elem = q_data_set[q_key]
                q_totient = self.__factor_component.totient_int(q_key)
                if self.core.is_greater(q_totient, self.core.a_identity):
                    q_elem.totient_element = q_data_set[q_totient]

        if find_totient_log:
            for q_key in q_data_set.keys():
                q_elem = q_data_set[q_key]
                q_elem.totient_log = self.__factor_component.totient_log_int(q_key)

        data_collection = QueryDataCollection(q_data_set)
        return data_collection
