# blocktodo: delete this



def divisorGen(n):
    factors = list(factorGenerator(n))
    nfactors = len(factors)
    f = [0] * nfactors
    while True:
        yield reduce(lambda x, y: x*y, [factors[x][0]**f[x] for x in range(nfactors)], 1)
        i = 0
        while True:
            f[i] += 1
            if f[i] <= factors[i][1]:
                break
            f[i] = 0
            i += 1
            if i >= nfactors:
                return

import operator
import itertools
from collections import Counter

def product(seq):
    return reduce(operator.mul, seq, 1)


def get_prime_divisors(x):
    original_x = x
    prime_divisors = []
    i = 1
    while x > 1:
        i += 1
        while x % i == 0:
            prime_divisors.append(i)
            x //= i
    assert product(prime_divisors) == original_x
    return prime_divisors

def get_clean_counter(counter):
    clean_counter = Counter(counter)    
    empty_keys = [key for key in counter.keys() if counter[key] == 0]
    for empty_key in empty_keys:
        del clean_counter[empty_key]
    return clean_counter

def get_contained_counters(counter):
    clean_counter = get_clean_counter(counter)
    keys, values = zip(*clean_counter.items())
    value_combinations = itertools.product((xrange(value) for value in values))
    contained_counters = []
    for value_combination in value_combinations:
        contained_counters.append(Counter(zip(keys, value_combination)))
    return contained_counters
    
        
    

def alt_get_divisors(x):
    
    
            
                

from garlicsim.general_misc import cute_profile
        
        
def get_divisors(x):
    return [i for i in xrange(1, x) if (x % i == 0)]

def is_perfect(x):
    return sum(get_divisors(x)) == x

@cute_profile.profile_ready()
def get_perfects(top):
    return [i for i in xrange(1, top) if is_perfect(i)]

if __name__ == '__main__':
    get_perfects.profiling_on = True
    #get_perfects(1000)
    0