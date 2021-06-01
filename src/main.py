# Press the green button in the gutter to run the script.
from src.infrastructure.service.component_config import ComponentConfig
from src.infrastructure.service.component_factory import ComponentFactory
from src.infrastructure.types.omni_integer import OmniInteger


def main():
    config = ComponentConfig()
    factory = ComponentFactory(config)
    v_component = factory.__create_visual_component__()
    v_component.plot_totient_3d(OmniInteger(100))


if __name__ == '__main__':
    main()

