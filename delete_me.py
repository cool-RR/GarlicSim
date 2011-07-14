from garlicsim.general_misc.nifty_collections import LazyTuple
from garlicsim.general_misc import cute_iter_tools

def _iterate_fibonacci():
    yield 1
    yield 1
    for pair in cute_iter_tools.consecutive_pairs(fibonacci_sequence):
        yield sum(pair)
        
fibonacci_sequence = LazyTuple(_iterate_fibonacci())

print(fibonacci_sequence[:10])