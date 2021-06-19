# Press the green button in the gutter to run the script.
from src.structure.groups.types.group_config import GroupConfig
from src.infrastructure.service.component_config import ComponentConfig
from src.infrastructure.service.component_factory import ComponentFactory
from src.structure.sets.integers.omni_integer import OmniInteger
from src.visual.components.graph_config import GraphConfig

config = ComponentConfig()
factory = ComponentFactory(config)
v_component = factory.create_visual_component()
g_component = factory.create_group_component()


def get_group_config(modulo: int):
    return GroupConfig(modulo)

def get_residue_stats(modulo: int):
    c = GroupConfig(modulo)
    g = g_component.create_group(c)
    paths = g_component.find_residue_paths(g)
    path_counts = g_component.count_residue_paths(g)
    return paths, path_counts

def get_graph_config():
    return GraphConfig()


def main():
    v_component.plot_totient_3d(OmniInteger(100))


if __name__ == '__main__':
    main()
