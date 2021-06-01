from src.query_engine.types.request.query_config import QueryConfig


class QueryOptions:
    def __init__(self, config: QueryConfig, factors: dict):
        self.config = config
        self.factors = factors
