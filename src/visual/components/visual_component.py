from pyvis.network import Network
import networkx as nx

from src.infrastructure.core.base_core import BaseCore
from src.structure.groups.components.group_component import GroupComponent
from src.structure.groups.types.group_config import GroupConfig
from src.infrastructure.cache.unity_cache import UnityCache
from src.infrastructure.omni_component import OmniComponent
from src.structure.sets.integers.omni_integer import OmniInteger
from src.query.components.query_component import QueryComponent
from src.visual.components.graph_config import GraphConfig
from src.visual.components.plot_builder import PlotBuilder3d
import matplotlib.pyplot as plt


class VisualComponent(OmniComponent):
    def __init__(self, unity_cache: UnityCache, core: BaseCore,
                 query_component: QueryComponent,
                 group_component: GroupComponent):
        super(VisualComponent, self).__init__(unity_cache, core)
        self.__query_component = query_component
        self.__group_component = group_component

    def plot_totient_3d(self, size: int):
        omni_size = OmniInteger(size)
        q_builder = self.__query_component.get_query_builder()
        p_builder = PlotBuilder3d()

        q_builder.include_totient()
        q_builder.set_range(omni_size)
        query = q_builder.build()

        data_collection = self.__query_component.search(query)
        data_collection.order_totient()
        p_builder.add_x_axis(data_collection.ordered_int_set, 'Z')
        p_builder.add_y_axis(data_collection.ordered_totient_set, 'Totient')
        p_builder.add_z_axis(data_collection.ordered_totient_time_set, 'Time')
        p_builder.add_c_axis(data_collection.ordered_totient_time_set)

        plt.ion()
        p_builder.build()

    def plot_group_graph(self, group_config: GroupConfig, graph_config: GraphConfig):
        group = self.__group_component.create_group(group_config)

        group_net = nx.Graph()
        group_index = 0

        group_net = self.__add_init_group__(group_net, group, group_index, graph_config)

        if group_config.find_additive_inverses:
            group_net = self.__add_additive_inverse_group__(group_net, group, group_index, graph_config)
            group_index = group_index + 1

        if group_config.find_multiplicative_inverses:
            group_net = self.__add_mul_inverse_group__(group_net, group, group_index, graph_config)
            group_index = group_index + 1

        if group_config.find_adjacencies:
            group_net = self.__add_adjacency_group__(group_net, group, group_index, graph_config)
            group_index = group_index + 1

        if group_config.find_totients:
            group_net = self.__add_totients_group__(group_net, group, group_index, graph_config)
            group_index = group_index + 1

        if group_config.find_factors:
            group_net = self.__add_factors_group__(group_net, group, group_index, graph_config)
            group_index = group_index + 1

        if group_config.find_residues:
            for root in group_config.residue_roots:
                omni_root = self.core.__cons__(root)
                group_net = self.__add_residues_group__(group_net, group, group_index, graph_config, omni_root)
                group_index = group_index + 1

        if group_config.find_quotients:
            for divisor in group_config.quotient_divisors:
                group_net = self.__add_quotients_group__(group_net, group, group_index, graph_config, divisor)
                group_index = group_index + 1

        if group_config.find_quotient_relatables:
            for relatable in group_config.quotient_relatables:
                group_net = self.__add_quotient_relatables_group__(group_net, group, group_index, graph_config, relatable)
                group_index = group_index + 1

        group_net_vis = Network(height='100%', width='100%', bgcolor='#222222', font_color='white')
        group_net_vis.from_nx(group_net)
        group_net_vis.toggle_physics(True)

        if graph_config.is_circle or graph_config.is_layered:
            group_pos = None
            if graph_config.is_circle:
                group_pos = nx.circular_layout(group_net)
            if graph_config.is_layered:
                group_pos = nx.kamada_kawai_layout(group_net)
            group_net_vis.toggle_physics(False)
            for node in group_net.nodes:
                pos = group_pos[node]
                vis_node = group_net_vis.get_node(node)
                vis_node['x'] = pos[0] * 3.7 * group.modulo.get_val()
                vis_node['y'] = pos[1] * 3.7 * group.modulo.get_val()

        group_net_vis.show_buttons()
        group_net_vis.show(f'group_{group.modulo.get_val()}.html')

    def __add_init_group__(self, graph, group, group_index, graph_config):
        for elem_key in group.elements:
            elem = group.elements[elem_key]
            omni_elem_id = elem.id
            elem_id = omni_elem_id.get_val()

            graph.add_node(elem_id, label=str(elem_id), group=group_index)
        return graph

    def __add_residues_group__(self, graph, group, group_index, graph_config, n_root):
        for elem_key in group.elements:
            elem = group.elements[elem_key]
            omni_elem_id = elem.id
            elem_id = omni_elem_id.get_val()

            residues = elem.get_nth_roots(n_root)
            for residue_elem in residues:
                residue_id = residue_elem.id.get_val()
                graph.add_edge(elem_id, residue_id, color=graph_config.get_color(group_index))
                graph.edges[elem_id, residue_id]['color'] = graph_config.get_color(group_index)
                if graph_config.is_symmetric:
                    residue_sym = residue_elem.get_add_inverse()
                    omni_sym_id = residue_sym.id
                    sym_id = omni_sym_id.get_val()
                    graph.add_edge(elem_id, sym_id, color=graph_config.get_inverse_color(group_index))
                    graph.edges[elem_id, sym_id]['color'] = graph_config.get_inverse_color(group_index)
        return graph

    def __add_quotients_group__(self, graph, group, group_index, graph_config, n_divisor):
        for elem_key in group.elements:
            elem = group.elements[elem_key]
            omni_elem_id = elem.id
            elem_id = omni_elem_id.get_val()

            quotient_elem = elem.get_quotient_of(n_divisor)
            quotient_id = quotient_elem.id.get_val()
            graph.add_edge(elem_id, quotient_id, color=graph_config.get_color(group_index))
            graph.edges[elem_id, quotient_id]['color'] = graph_config.get_color(group_index)

            if graph_config.is_symmetric:
                quotient_sym = quotient_elem.get_add_inverse()
                omni_sym_id = quotient_sym.id
                sym_id = omni_sym_id.get_val()
                graph.add_edge(elem_id, sym_id, color=graph_config.get_inverse_color(group_index))
                graph.edges[elem_id, sym_id]['color'] = graph_config.get_inverse_color(group_index)
        return graph

    def __add_quotient_relatables_group__(self, graph, group, group_index, graph_config, n_relatable):
        for elem_key in group.elements:
            elem = group.elements[elem_key]
            omni_elem_id = elem.id
            elem_id = omni_elem_id.get_val()

            relatable_elem = elem.get_quotient_relation_to(n_relatable)
            relatable_id = relatable_elem.id.get_val()
            graph.add_edge(elem_id, relatable_id, color=graph_config.get_color(group_index))
            graph.edges[elem_id, relatable_id]['color'] = graph_config.get_color(group_index)

            if graph_config.is_symmetric:
                relatable_sym = relatable_elem.get_add_inverse()
                omni_sym_id = relatable_sym.id
                sym_id = omni_sym_id.get_val()
                graph.add_edge(elem_id, sym_id, color=graph_config.get_inverse_color(group_index))
                graph.edges[elem_id, sym_id]['color'] = graph_config.get_inverse_color(group_index)
        return graph

    def __add_totients_group__(self, graph, group, group_index, graph_config):
        for elem_key in group.elements:
            elem = group.elements[elem_key]
            omni_elem_id = elem.id
            omni_totient = elem.get_totient()
            elem_id = omni_elem_id.get_val()
            totient_id = omni_totient.id.get_val()

            graph.add_edge(elem_id, totient_id, color=graph_config.get_color(group_index))
            graph.edges[elem_id, totient_id]['color'] = graph_config.get_color(group_index)

            if graph_config.is_symmetric:
                totient_sym = omni_totient.get_add_inverse()
                omni_sym_id = totient_sym.id
                sym_id = omni_sym_id.get_val()
                graph.add_edge(elem_id, sym_id, color=graph_config.get_inverse_color(group_index))
                graph.edges[elem_id, sym_id]['color'] = graph_config.get_inverse_color(group_index)
        return graph

    def __add_factors_group__(self, graph, group, group_index, graph_config):
        for elem_key in group.elements:
            elem = group.elements[elem_key]
            omni_elem_id = elem.id
            elem_id = omni_elem_id.get_val()
            elem_factors = elem.get_factors()
            for factor in elem_factors:
                factor_id = factor.id.get_val()
                graph.add_edge(elem_id, factor_id, color=graph_config.get_color(group_index))
                graph.edges[elem_id, factor_id]['color'] = graph_config.get_color(group_index)
                if graph_config.is_symmetric:
                    factor_sym = factor.get_add_inverse()
                    omni_sym_id = factor_sym.id
                    sym_id = omni_sym_id.get_val()
                    graph.add_edge(elem_id, sym_id, color=graph_config.get_inverse_color(group_index))
                    graph.edges[elem_id, sym_id]['color'] = graph_config.get_inverse_color(group_index)
        return graph

    def __add_mul_inverse_group__(self, graph, group, group_index, graph_config):
        for elem_key in group.elements:
            elem = group.elements[elem_key]
            omni_elem_id = elem.id
            elem_id = omni_elem_id.get_val()

            elem_inv = elem.get_mul_inverse()
            if elem_inv is None:
                continue
            omni_inv_id = elem_inv.id
            inv_id = omni_inv_id.get_val()

            graph.add_edge(elem_id, inv_id, color=graph_config.get_color(group_index))
            graph.edges[elem_id, inv_id]['color'] = graph_config.get_color(group_index)

            if graph_config.is_symmetric:
                elem_sym = elem_inv.get_add_inverse()
                omni_sym_id = elem_sym.id
                sym_id = omni_sym_id.get_val()
                graph.add_edge(elem_id, sym_id, color=graph_config.get_inverse_color(group_index))
                graph.edges[elem_id, sym_id]['color'] = graph_config.get_inverse_color(group_index)
        return graph

    def __add_additive_inverse_group__(self, graph, group, group_index, graph_config):
        for elem_key in group.elements:
            elem = group.elements[elem_key]
            omni_elem_id = elem.id
            elem_id = omni_elem_id.get_val()

            elem_inv_add = elem.get_add_inverse()
            omni_inv_add_id = elem_inv_add.id
            inv_add_id = omni_inv_add_id.get_val()

            graph.add_edge(elem_id, inv_add_id, color=graph_config.get_color(group_index))
            graph.edges[elem_id, inv_add_id]['color'] = graph_config.get_color(group_index)
        return graph

    def __add_adjacency_group__(self, graph, group, group_index, graph_config):
        modulo = group.modulo.get_val()
        for elem_key in group.elements:
            elem = group.elements[elem_key]
            omni_elem_id = elem.id
            elem_id = omni_elem_id.get_val()
            if elem_id == 1:
                graph.add_edge(1, 2, color=graph_config.get_color(group_index))
                graph.add_edge(1, modulo - 1, color=graph_config.get_color(group_index))
                graph.edges[1, 2]['color'] = graph_config.get_color(group_index)
                graph.edges[1, modulo - 1]['color'] = graph_config.get_color(group_index)
            elif elem_id == (modulo - 1):
                graph.add_edge(modulo - 1, 1, color=graph_config.get_color(group_index))
                graph.add_edge(modulo - 1, modulo - 2, color=graph_config.get_color(group_index))
                graph.edges[modulo - 1, 1]['color'] = graph_config.get_color(group_index)
                graph.edges[modulo - 1, modulo - 2]['color'] = graph_config.get_color(group_index)
            else:
                graph.add_edge(elem_id, elem_id + 1, color=graph_config.get_color(group_index))
                graph.add_edge(elem_id, elem_id - 1, color=graph_config.get_color(group_index))
                graph.edges[elem_id, elem_id + 1]['color'] = graph_config.get_color(group_index)
                graph.edges[elem_id, elem_id - 1]['color'] = graph_config.get_color(group_index)
        return graph
