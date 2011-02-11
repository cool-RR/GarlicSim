# blocktodo: delete this

from garlicsim.general_misc import cute_profile

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

def get_divisors(x):
    return [i for i in xrange(1, x) if (x % i == 0)]

def is_perfect(x):
    return sum(get_divisors(x)) == x

@cute_profile.profile_ready()
def get_perfects(top):
    return [i for i in xrange(1, top) if is_perfect(i)]

if __name__ == '__main__':
    get_perfects.profiling_on = True
    get_perfects(1000)
    1/0