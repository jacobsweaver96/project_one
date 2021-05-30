# -*- coding: utf-8 -*-

from mpmath import *
import sympy
import math

################
### Solution ###
################

def int_factorization(k):
    return 0

###############
### Helpers ###
###############

##### Functions #####
        
# Given integer n coprime to prime p: find a -> an =% 1 mod p
def squeeze_mod(n, p):
    n_spare = fmod(n, p)
    d_spare = 1
    u_diff = fsub(fsub(p, 1), n_spare)
    d_diff = fsub(n_spare, 1)
    while u_diff > 0 and d_diff > 0:
        u_diff_plus = fadd(u_diff, 1)
        if fmod(p, n_spare) == 0:
            return n_spare
        if fmod(p, u_diff_plus) == 0:
            return u_diff_plus
        if u_diff <= d_diff:
            d_spare = fmod(fmul(d_spare, ceil(fdiv(n_spare, u_diff))), p)
        else:
            d_spare = fmod(fmul(d_spare, ceil(fdiv(fsub(p, n_spare), d_diff))), p)
        n_spare = fmod(fmul(n, d_spare), p)
        u_diff = fsub(fsub(p, 1), n_spare)
        d_diff = fsub(n_spare, 1)
    if u_diff == 0:
        d_spare = fsub(p, d_spare)
    return d_spare

def exp_mod(b, e, n):
    b_ls = []
    e_log = math.floor(math.log(e, 2))
    
    # Spare for generating power set
    a_spare = fmod(b, n)
    # Spare for aggregating result
    b_spare = 1
    # Spare for exp reduction
    m_spare = e
    
    b_ls.append(a_spare)
    # Generate binary powers
    for i in range(0, e_log):
        a_spare = fmod(fmul(a_spare, a_spare), n)
        b_ls.append(a_spare)
    # Large to small
    b_ls.reverse()
    index = 0
    for j in b_ls:
        p_spare = power(2, fsub(e_log, index))
        if m_spare >= p_spare:
            b_spare = fmod(fmul(b_spare, j), n)
            m_spare = fsub(m_spare, p_spare)
        index = index + 1
            
    return b_spare
        
    