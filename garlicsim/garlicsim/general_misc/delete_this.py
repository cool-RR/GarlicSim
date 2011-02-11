# blocktodo: delete this



#def divisorGen(n):
    #factors = list(factorGenerator(n))
    #nfactors = len(factors)
    #f = [0] * nfactors
    #while True:
        #yield reduce(lambda x, y: x*y, [factors[x][0]**f[x] for x in range(nfactors)], 1)
        #i = 0
        #while True:
            #f[i] += 1
            #if f[i] <= factors[i][1]:
                #break
            #f[i] = 0
            #i += 1
            #if i >= nfactors:
                #return

import operator
import itertools
from collections import Counter
from garlicsim.general_misc import caching

def product(seq):
    return reduce(operator.mul, seq, 1)

prime_list = [2]

def iter_primes(top=float('inf')):
    for prime in prime_list:
        if prime >= top:
            raise StopIteration
        yield prime
    if prime + 1 == top:
        raise StopIteration
    for new_prime in iter_new_primes():
        if new_prime >= top:
            raise StopIteration
        yield new_prime
    
def iter_new_primes():
    for number in itertools.count(prime_list[-1] + 1):
        smaller_primes = iter_primes(top=number)
        found_divisor = False
        for smaller_prime in smaller_primes:
            if number % smaller_prime == 0:
                found_divisor = True
                break
        if not found_divisor:
            prime_list.append(number)
            yield number
            
def is_prime(x):
    new_primes_iterator = iter_new_primes()
    while prime_list[-1] < x: 
        new_primes_iterator.next()
    return x in prime_list
    
caching.cache()
def get_prime_divisors(x):
    if x == 1:
        return []
    prime_divisors = []
    for prime in iter_primes():
        if x % prime == 0:
            prime_divisors = [prime] + get_prime_divisors(x // prime)
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
    value_combinations = itertools.product(
        *(xrange(value + 1) for value in values)
    )
    contained_counters = []
    for value_combination in value_combinations:
        contained_counters.append(Counter(dict(zip(keys, value_combination))))
    return contained_counters


def get_divisors(x):
    if x == 1:
        return [1]
    prime_divisors_counter = Counter(get_prime_divisors(x))
    contained_prime_divisors_counters = \
        get_contained_counters(prime_divisors_counter)
    divisors = []
    for contained_prime_divisors_counter in contained_prime_divisors_counters:
        divisors.append(product(contained_prime_divisors_counter.elements()))
    divisors.remove(x)
    return sorted(divisors)
    

from garlicsim.general_misc import cute_profile
        
        
def alt_get_divisors(x):
    return [i for i in xrange(1, x) if (x % i == 0)]

def is_perfect(x):
    return sum(get_divisors(x)) == x

@cute_profile.profile_ready()
def get_perfects(top):
    return [i for i in xrange(1, top) if is_perfect(i)]

if __name__ == '__main__':
    #get_divisors = alt_get_divisors
    get_perfects.profiling_on = True
    get_perfects(10000)
    0