# %%
import matplotlib.pyplot as plt
import numpy as np
import mpmath
import math as math
from sympy import sieve
from sympy.ntheory import factorint
from sympy.ntheory.factor_ import totient


class QueryFactor:
    def __init__(self, n, k_min=-1, k_max=-1):
        # factor
        self.n = n
        # minimum power (default -1 implies exclusion)
        self.k_min = k_min
        # maximum power (default -1 implies inf)
        self.k_max = k_max


class QueryConfig:
    def __init__(self):
        self.range = 0
        self.tot_len = 0
        self.findTotient = False


class Query:
    def __init__(self, config, factors):
        self.config = config
        self.factors = factors


class QueryBuilder:
    def __init__(self):
        self.factors = dict()
        self.config = QueryConfig()

    def include_totient(self, tot_len=-1):
        self.config.findTotient = True
        self.config.tot_len = tot_len

    def set_range(self, range):
        self.config.range = range

    def include_factor(self, n, k_min, k_max=-1):
        factor = QueryFactor(n, k_min, k_max)
        self.factors[n] = factor

    def exclude_factor(self, n):
        factor = QueryFactor(n)
        self.factors[n] = factor

    def build(self):
        query = Query(self.config, self.factors)
        return query


class QueryResult:
    def __init__(self, integers):
        self.integers = integers

    def flatten_totient(self):S
        totient_set = dict()
        for i in self.integers.keys():
            v = self.integers[i]
            tot_obj = v.totient
            totient_ls = []
            pure = 0
            while tot_obj != 0:
                pure = tot_obj.n
                tot_obj = tot_obj.totient
                totient_ls.append(pure)
            totient_set[i] = totient_ls
        return totient_set

    def normalize_data(self, norm, data, p_val):
        d_len = len(data)
        d_spare = data
        if d_len >= norm:
            return d_spare
        for i in range(0, norm - d_len):
            d_spare.append(p_val)
        return d_spare

    def normalize_dataset(self, data, p_val):
        d_spare = data.copy()
        max_len = 0
        for k in data.keys():
            k_len = len(data[k])
            if k_len > max_len:
                max_len = k_len
        for j in data.keys():
            i_data = data[j]
            i_norm = self.normalize_data(max_len, i_data, p_val)
            d_spare[j] = i_norm
        return d_spare

    def flatten_totient_time(self):
        flat_tot = self.flatten_totient()
        norm_data = flat_tot
        n_data = []
        tot_data = []
        time_data = []
        for num in norm_data.keys():
            tot_set = norm_data[num]
            tot_len = len(tot_set)
            for i in range(0, tot_len):
                n_data.append(num)
                tot_data.append(tot_set[i])
                time_data.append(i)
        return (n_data, tot_data, time_data)


class FactorResult:
    def __init__(self, n, k, totient):
        # factor
        self.n = n
        # power
        self.k = k
        # totient
        self.totient = totient


class IntegerResult:
    def __init__(self, n, factors, totient):
        self.n = n
        self.factors = factors
        self.totient = totient


class ResultBuilder:
    def __init__(self, query):
        self.integers = dict()
        self.result = None
        self.query = query

    def find_totient_set(self, n):
        tot = totient(n)
        factors = dict()
        if tot == 1 or is_pow_2(tot):
            factors[tot] = 1
            return IntegerResult(tot, factors, 0)
        i_factors = factorint(tot)
        for factor in i_factors.keys():
            factors[factor] = FactorResult(factor, i_factors[factor], self.find_totient_set(factor))
        return IntegerResult(tot, factors, self.find_totient_set(tot))

    def solve(self):
        config = self.query.config
        queryFactors = self.query.factors
        i_range = config.range
        findTotient = config.findTotient
        tot_len = config.tot_len
        findTotientLog = findTotient and tot_len == -1
        exclude_factors = []

        for i in range(2, i_range):
            i_factors = factorint(i)
            factor_set = dict()
            tot = -1
            if findTotientLog == True:
                tot = self.find_totient_set(i)
            for f in i_factors.keys():
                f_tot = -1
                if findTotientLog == True:
                    f_tot = self.find_totient_set(f)
                factor_set[f] = FactorResult(f, i_factors[f], f_tot)
            self.integers[i] = IntegerResult(i, factor_set, tot)
        self.result = QueryResult(self.integers)
        return self.result


def exp_red(n):
    lg = math.floor(math.log2(n))
    p = []
    n_spare = n
    for j in range(0, lg + 1):
        i = lg - j
        v = 2 ** i
        n_iter = n_spare % v
        if n_iter < n_spare:
            n_spare = n_iter
            p.append(i)
    return p


def exp_eval(ls):
    n = 0
    for i in ls:
        n = n + (2 ** i)
    return n


def exp_scale(n, ls):
    ret = []
    for i in ls:
        ret.append(i + n)
    return ret


def is_pow_2(n):
    factors = factorint(n)
    if len(factors.keys()) == 1 and factors.keys().__contains__(2):
        return True
    return False


def totient_log(n):
    n_spare = n
    tlog = 0

    while (n_spare > 1):
        n_spare = totient(n_spare)
        tlog = tlog + 1
    return tlog


def totient_log_range(n):
    ret = dict()
    for i in range(2, n):
        ret[i] = totient_log(i)
    return ret


def plot_totient_log_stats(n):
    ls = totient_log_range(n)
    disp = dict()
    for i in ls.values():
        disp[i] = 0
    for j in ls.keys():
        v = ls[j]
        disp[v] = disp[v] + 1
    x = list(disp.keys())
    y = list(disp.values())
    plt.scatter(x, y)
    plt.show()


class PlotBuilder:
    def __init__(self):
        self.is2d = True
        self.is3d = False
        self.x = []
        self.x_label = None
        self.y = []
        self.y_label = None
        self.z = []
        self.z_label = None
        self.c_map = 'hsv'
        self.c = []

    def add_x_axis(self, data, label, is_color=False):
        self.x = data
        self.x_label = label
        if is_color:
            self.c = data

    def add_y_axis(self, data, label, is_color=False):
        self.y = data
        self.y_label = label
        if is_color:
            self.c = data

    def add_z_axis(self, data, label, is_color=False):
        self.is3d = True
        self.is2d = False
        self.z = data
        self.z_label = label
        if is_color:
            self.c = data

    def set_c_map(self, cmap):
        self.c_map = cmap

    def build(self):
        ax = None
        if self.is2d:
            return
        elif self.is3d:
            ax = plt.axes(projection='3d')
            ax.autoscale = True
            ax.set_xlabel(self.x_label)
            ax.set_ylabel(self.y_label)
            ax.set_zlabel(self.z_label)
            ax.scatter3D(self.x, self.y, self.z, c=self.c, cmap=self.c_map)
            # ax.plot(self.x, self.y, self.z)


def solve_stats(range):
    query_builder = QueryBuilder()
    query_builder.include_totient()
    query_builder.set_range(range)
    query = query_builder.build()
    result_builder = ResultBuilder(query)
    return result_builder.solve()


def plot_stats(queryResult, cmap):
    plotBuilder = PlotBuilder()
    plt.ion()
    (n_data, tot_data, time_data) = queryResult.flatten_totient_time()
    plotBuilder.add_z_axis(n_data, 'Z', is_color=True)
    plotBuilder.add_y_axis(tot_data, 'Totient')
    plotBuilder.add_x_axis(time_data, 'Time')
    plotBuilder.set_c_map(cmap)
    plotBuilder.build()

# %%
