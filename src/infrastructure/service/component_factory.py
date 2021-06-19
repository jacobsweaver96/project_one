from src.infrastructure.core.base_core import BaseCore
from src.computation.components.computation_component import ComputationComponent
from src.infrastructure.cache.factor_cache import FactorCache
from src.infrastructure.cache.totient_cache import TotientCache
from src.infrastructure.cache.unity_cache import UnityCache
from src.infrastructure.service.compatibility_component import CompatibilityComponent
from src.infrastructure.service.component_config import ComponentConfig, LibEnum
from src.structure.groups.components.group_component import GroupComponent
from src.structure.sets.integers.omni_integer import IntegerEnum
from src.query.components.query_component import QueryComponent
from src.visual.components.visual_component import VisualComponent


class ComponentFactory:
    def __init__(self, config: ComponentConfig):
        self.__config = config

        if self.__config.get_core_lib() == LibEnum.default:
            self.__core = BaseCore(IntegerEnum.default)
        else:
            self.__core = BaseCore(IntegerEnum.default)

        self.__unity_cache = None
        self.__factor_component = None
        self.__compatibility_component = None
        self.__query_component = None
        self.__visual_component = None
        self.__group_component = None

    def __create_unity_cache__(self) -> UnityCache:
        if self.__unity_cache is None:
            factor_cache = FactorCache(self.__core)
            totient_cache = TotientCache(self.__core)
            self.__unity_cache = UnityCache(factor_cache, totient_cache)
        return self.__unity_cache

    def __create_compatibility_component__(self):
        if self.__compatibility_component is None:
            unity_cache = self.__create_unity_cache__()
            self.__compatibility_component = CompatibilityComponent(unity_cache, self.__core)
        return self.__compatibility_component

    def __create_factor_component__(self):
        if self.__factor_component is None:
            unity_cache = self.__create_unity_cache__()
            compatibility_component = self.__create_compatibility_component__()
            self.__factor_component = ComputationComponent(unity_cache, self.__core, compatibility_component)
        return self.__factor_component

    def __create_query_component__(self):
        if self.__query_component is None:
            unity_cache = self.__create_unity_cache__()
            factor_component = self.__create_factor_component__()
            self.__query_component = QueryComponent(unity_cache, self.__core, factor_component)
        return self.__query_component

    def __create_group_component__(self):
        if self.__group_component is None:
            unity_cache = self.__create_unity_cache__()
            factor_component = self.__create_factor_component__()
            self.__group_component = GroupComponent(unity_cache, self.__core, factor_component)
        return self.__group_component

    def __create_visual_component__(self):
        if self.__visual_component is None:
            unity_cache = self.__create_unity_cache__()
            query_component = self.__create_query_component__()
            group_component = self.__create_group_component__()
            self.__visual_component = VisualComponent(unity_cache, self.__core, query_component, group_component)
        return self.__visual_component

    def create_factor_component(self):
        return self.__create_factor_component__()

    def create_query_component(self):
        return self.__create_query_component__()

    def create_visual_component(self):
        return self.__create_visual_component__()

    def create_group_component(self):
        return self.__create_group_component__()
