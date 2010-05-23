import random

import inty
import toroidal_array


class World(object): 
    def __init__(self, width=50, height=30):
        self.width = width
        self.height = height
        self.array = toroidal_array.ToroidalArray(width, height)
        
        
        
    def get(self, x, y):
        int_four_board = self.array.get(x // 4, y // 4)
        return inty.int_four_board.get(int_four_board, x % 4, y % 4)
        

        
    def set(self, x, y, value):
        changer = inty.int_four_board.get_with_cell_change_to_true if value else \
                inty.int_four_board.get_with_cell_change_to_false
        int_four_board = self.array.get(x // 4, y // 4)
        new_int_four_board = changer(int_four_board, x % 4, y % 4)
        self.array.set(x // 4, y // 4, new_int_four_board)
        return 

        
    def step(self):
        try:
            self.board = self.board.get_next()
        except boards.misc.NeedToBloat:
            self._bloat_board()
            self.board = self.board.get_next()
    
            
    def iter_cells(self, state=True, rectangle=None):
        new_rect = (
            rectangle[0] % self.width,
            rectangle[1] % self.height,
            rectangle[2] % self.width,
            rectangle[3] % self.height
        )
            
        
        