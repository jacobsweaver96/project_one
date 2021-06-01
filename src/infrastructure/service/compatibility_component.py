from src.computation_engine.components.core.base_core import BaseCore
from src.infrastructure.cache.unity_cache import UnityCache
from src.infrastructure.omni_component import OmniComponent
from src.infrastructure.types.omni_integer import OmniInteger, IntegerEnum


class CompatibilityComponent(OmniComponent):
    def __init__(self, unity_cache: UnityCache, core: BaseCore):
        super(CompatibilityComponent, self).__init__(unity_cache, core)

    # TODO
    def int_type_guard(self, n: OmniInteger, target_type: IntegerEnum):
        return n.get_val()
