from garlicsim.general_misc import cute_profile        
        
def get_divisors(x):
    '''Get all the integer divisors of `x`.'''
    return [i for i in xrange(1, x) if (x % i == 0)]

def is_perfect(x):
    '''Is the number `x` perfect?'''
    return sum(get_divisors(x)) == x

@cute_profile.profile_ready()
def get_perfects(top):
    '''Get all the perfect numbers up to the number `top`.'''
    return [i for i in xrange(1, top) if is_perfect(i)]

if __name__ == '__main__':
    get_perfects.profiling_on = True
    get_perfects(2000)
    0