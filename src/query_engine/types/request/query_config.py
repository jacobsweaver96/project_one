from src.infrastructure.types.omni_integer import OmniInteger


class QueryConfig:
    def __init__(self, range_int: OmniInteger, tot_length: OmniInteger, find_totient: bool):
        self.range_int = range_int
        self.tot_length = tot_length
        self.find_totient = find_totient
