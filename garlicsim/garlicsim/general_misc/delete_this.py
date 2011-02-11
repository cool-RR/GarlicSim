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

import garlicsim

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


def get_prime_divisors_dict(x):
    prime_divisors = get_prime_divisors(x)
    return dict((prime_divisor, prime_divisors.count(prime_divisor)) for
                prime_divisor in set(prime_divisors))


def get_contained_prime_divisor_dicts(prime_divisor_dict):
    contained_prime_divisor_dicts = []
    prime_divisor_dicts_to_handle = [prime_divisor_dict]
    while prime_divisor_dicts_to_handle:
        my_prime_divisor_dict = prime_divisor_dicts_to_handle.pop()
        contained_prime_divisor_dicts.append(my_prime_divisor_dict)
        
    

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