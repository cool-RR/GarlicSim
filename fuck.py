import run_gui

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import caching

import garlicsim
from garlicsim_lib.simpacks.cute_life import *


@caching.cache
def _all_boards(level):
    if level == 0:
        return (True, False)

    smaller = _all_boards(level - 1)
    
    return tuple(QuadBoard(x, y, z, w) \
                 for x in smaller for y in smaller \
                 for z in smaller for w in smaller)
    
    

def cache_all_boards(level):
    assert level >= 2
    for board in _all_boards(level):
        board.get_future_sub_quad_board()

if __name__ == '__main__':
    pass