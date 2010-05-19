import run_gui

import garlicsim
from garlicsim_lib.simpacks.cute_life import *

board = QuadBoard(
    QuadBoard(
        QuadBoard(
            QuadBoard(True, False, True, False),
            QuadBoard(True, True, True, False),
            QuadBoard(True, False, True, True),
            QuadBoard(True, False, False, False)
            ),
        QuadBoard(
            QuadBoard(True, True, False, False),
            QuadBoard(False, True, False, False),
            QuadBoard(False, False, True, True),
            QuadBoard(True, False, False, True)
        ),
        QuadBoard(
            QuadBoard(True, False, False, True),
            QuadBoard(False, True, True, False),
            QuadBoard(True, False, False, True),
            QuadBoard(True, False, False, True)
        ),
        QuadBoard(
            QuadBoard(True, True, False, False),
            QuadBoard(True, False, False, True),
            QuadBoard(True, True, False, False),
            QuadBoard(False, False, True, True)
        )
    ),
    QuadBoard(
        QuadBoard(
            QuadBoard(True, True, False, False),
            QuadBoard(False, False, True, True),
            QuadBoard(False, True, False, False),
            QuadBoard(True, False, False, True)
        ),
        QuadBoard(
            QuadBoard(False, False, True, False),
            QuadBoard(True, True, True, False),
            QuadBoard(True, False, True, True),
            QuadBoard(True, False, False, False)
            ),
        QuadBoard(
            QuadBoard(True, False, False, True),
            QuadBoard(True, False, False, True),
            QuadBoard(False, True, True, False),
            QuadBoard(True, False, False, True),
        ),
        QuadBoard(
            QuadBoard(True, True, False, False),
            QuadBoard(False, False, True, True),
            QuadBoard(True, False, False, True),
            QuadBoard(True, True, False, False)
        )
    ),
    QuadBoard(
        QuadBoard(
            QuadBoard(False, False, True, False),
            QuadBoard(True, True, True, False),
            QuadBoard(True, False, False, False),
            QuadBoard(True, False, True, True),
            ),        
        QuadBoard(
            QuadBoard(True, False, False, True),
            QuadBoard(False, True, True, False),
            QuadBoard(True, False, False, True),
            QuadBoard(True, False, False, True),
        ),
        QuadBoard(
            QuadBoard(True, True, False, False),
            QuadBoard(False, False, False, True),
            QuadBoard(False, True, False, False),
            QuadBoard(True, False, False, True)
        ),
        QuadBoard(
            QuadBoard(True, True, False, False),
            QuadBoard(True, False, False, True),
            QuadBoard(False, False, True, True),
            QuadBoard(True, True, False, False)
        )
    ),
    QuadBoard(
        QuadBoard(
            QuadBoard(True, True, False, False),
            QuadBoard(True, True, False, False),
            QuadBoard(True, False, False, True),
            QuadBoard(False, False, True, True),
        ),
        QuadBoard(
            QuadBoard(False, False, True, False),
            QuadBoard(True, False, False, True),
            QuadBoard(True, False, True, True),
            QuadBoard(True, True, True, False),
            ),        
        QuadBoard(
            QuadBoard(True, False, False, True),
            QuadBoard(True, False, False, True),
            QuadBoard(False, True, True, False),
            QuadBoard(True, False, False, True),
        ),
        QuadBoard(
            QuadBoard(False, True, False, False),
            QuadBoard(True, False, False, True),
            QuadBoard(False, True, False, False),
            QuadBoard(False, False, True, True),
            
        ),
    ),
)
    


state = State(board)

def do():
    return garlicsim.simulate(state, 30)

if __name__ == '__main__':
    s = do()
    garlicsim.simulate(s, 3)