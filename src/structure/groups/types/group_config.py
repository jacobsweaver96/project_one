from src.structure.sets.integers.omni_integer import OmniInteger


class GroupConfig:
    def __init__(self, modulo: int):
        self.modulo = OmniInteger(modulo)
        self.find_totient = True
        self.find_additive_inverses = False
        self.find_multiplicative_inverses = False
        self.find_adjacencies = False
        self.find_residues = False
        self.find_quotients = False
        self.find_quotient_relatables = False
        self.find_sub_groups = False
        self.find_totients = False
        self.find_factors = False
        self.residue_roots = []
        self.quotient_divisors = []
        self.quotient_relatables = []
        self.sub_group_config = None

    def to_copy(self, modulo: int):
        config_copy = GroupConfig(modulo)
        config_copy.find_totient = self.find_totient
        config_copy.find_additive_inverses = self.find_additive_inverses
        config_copy.find_multiplicative_inverses = self.find_multiplicative_inverses
        config_copy.find_adjacencies = self.find_adjacencies
        config_copy.find_residues = self.find_residues
        config_copy.find_quotients = self.find_quotients
        config_copy.find_quotient_relatables = self.find_quotient_relatables
        config_copy.find_sub_groups = self.find_sub_groups
        config_copy.find_totients = self.find_totients
        config_copy.find_factors = self.find_factors
        config_copy.residue_roots = self.residue_roots
        config_copy.quotient_divisors = self.quotient_divisors
        config_copy.quotient_relatables = self.quotient_relatables
        config_copy.sub_group_config = self.sub_group_config
        return config_copy

    def with_adjacencies(self, val=True):
        self.find_adjacencies = val
        return self

    def with_additive_inverses(self, val=True):
        self.find_additive_inverses = val
        return self

    def with_multiplicative_inverses(self, val=True):
        self.find_multiplicative_inverses = val
        return self

    def with_residues(self, roots, val=True):
        self.find_residues = val
        self.residue_roots = roots
        return self

    def with_quotients(self, divisors, val=True):
        omni_divisors = []
        for divisor in divisors:
            omni_divisors.append(OmniInteger(divisor))
        self.quotient_divisors = omni_divisors
        self.find_quotients = val
        return self

    def with_quotient_relations(self, relatables, val=True):
        omni_relatables = []
        for relatable in relatables:
            omni_relatables.append(OmniInteger(relatable))
        self.quotient_relatables = omni_relatables
        self.find_quotient_relatables = val
        return self

    def with_sub_groups(self, sub_group_config=None, val=True):
        self.find_sub_groups = val
        if sub_group_config is not None:
            self.sub_group_config = sub_group_config
        return self

    def with_factors(self, val=True):
        self.find_factors = val
        return self

    def with_elem_totients(self, val=True):
        self.find_totients = val
        return self
