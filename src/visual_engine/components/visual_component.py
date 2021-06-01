from src.computation_engine.components.core.base_core import BaseCore
from src.infrastructure.cache.unity_cache import UnityCache
from src.infrastructure.omni_component import OmniComponent
from src.infrastructure.types.omni_integer import OmniInteger
from src.query_engine.components.query_component import QueryComponent
from src.visual_engine.components.plot_builder import PlotBuilder3d
import matplotlib.pyplot as plt


class VisualComponent(OmniComponent):
    def __init__(self, unity_cache: UnityCache, core: BaseCore,
                 query_component: QueryComponent):
        super(VisualComponent, self).__init__(unity_cache, core)
        self.__query_component = query_component

    def plot_totient_3d(self, size: OmniInteger):
        q_builder = self.__query_component.get_query_builder()
        p_builder = PlotBuilder3d()

        q_builder.include_totient()
        q_builder.set_range(size)
        query = q_builder.build()

        data_collection = self.__query_component.search(query)
        data_collection.order_totient()
        p_builder.add_x_axis(data_collection.ordered_int_set, 'Z')
        p_builder.add_y_axis(data_collection.ordered_totient_set, 'Totient')
        p_builder.add_z_axis(data_collection.ordered_totient_time_set, 'Time')
        p_builder.add_c_axis(data_collection.ordered_totient_time_set)

        plt.ion()
        p_builder.build()
