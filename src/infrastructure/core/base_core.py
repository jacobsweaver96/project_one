import math

from src.structure.sets.integers.omni_integer import OmniInteger, IntegerEnum


class BaseCore:
    def __init__(self, int_type: IntegerEnum):
        self.__int_type = int_type
        self.a_identity = self.__cons__(0)
        self.inv_identity = self.__cons__(-1)
        self.m_identity = self.__cons__(1)

    def __cons__(self, val):
        omni_int = OmniInteger(val, self.__int_type)
        if isinstance(val, OmniInteger):
            omni_int = OmniInteger(val.get_val(), self.__int_type)
        return omni_int

    def add(self, left, right):
        l_spare = left
        r_spare = right
        if isinstance(left, OmniInteger):
            l_spare = left.get_val()
        if isinstance(right, OmniInteger):
            r_spare = right.get_val()
        val = l_spare + r_spare
        return self.__cons__(val)

    def sub(self, left, right):
        l_spare = left
        r_spare = right
        if isinstance(left, OmniInteger):
            l_spare = left.get_val()
        if isinstance(right, OmniInteger):
            r_spare = right.get_val()
        val = l_spare - r_spare
        return self.__cons__(val)

    def multiply(self, left, right):
        l_spare = left
        r_spare = right
        if isinstance(left, OmniInteger):
            l_spare = left.get_val()
        if isinstance(right, OmniInteger):
            r_spare = right.get_val()
        val = l_spare * r_spare
        return self.__cons__(val)

    def divide(self, dividend, divisor):
        l_spare = dividend
        r_spare = divisor
        if isinstance(dividend, OmniInteger):
            l_spare = dividend.get_val()
        if isinstance(divisor, OmniInteger):
            r_spare = divisor.get_val()
        val = l_spare / r_spare
        return self.__cons__(val)

    def mod(self, n, base):
        l_spare = n
        r_spare = base
        if isinstance(n, OmniInteger):
            l_spare = n.get_val()
        if isinstance(base, OmniInteger):
            r_spare = base.get_val()
        val = l_spare % r_spare
        return self.__cons__(val)

    def log_floor(self, n, base):
        l_spare = n
        r_spare = base
        if isinstance(n, OmniInteger):
            l_spare = n.get_val()
        if isinstance(base, OmniInteger):
            r_spare = base.get_val()
        val = int(math.floor(math.log(l_spare, r_spare)))
        return self.__cons__(val)

    def power(self, n, base):
        l_spare = n
        r_spare = base
        if isinstance(n, OmniInteger):
            l_spare = n.get_val()
        if isinstance(base, OmniInteger):
            r_spare = base.get_val()
        val = int(math.pow(r_spare, l_spare))
        return self.__cons__(val)

    def is_greater(self, left, right) -> bool:
        l_spare = left
        r_spare = right
        if isinstance(left, OmniInteger):
            l_spare = left.get_val()
        if isinstance(right, OmniInteger):
            r_spare = right.get_val()
        return l_spare > r_spare

    def range(self, n, exclusive=False) -> list:
        ls = []
        n_spare = n
        if isinstance(n, OmniInteger):
            n_spare = n.get_val()
        for val in range(1, n_spare):
            ls.append(self.__cons__(val))
        if not exclusive:
            ls.append(self.__cons__(n_spare))
        return ls
