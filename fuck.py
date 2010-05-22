import run_gui

from garlicsim_lib.simpacks.cute_life.cute_life.boards import *
from garlicsim_lib.simpacks.cute_life.cute_life import *

def p(x):
    print inty.int_four_board.to_string(x)
    
x=12944
qb=QuadBoard(x,0,0,0)
bqb=qb.get_bloated_to_quad_board()
bqb.get_future_sub_quad_board(1)