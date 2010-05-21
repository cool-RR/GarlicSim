import random

import boards
from boards import QuadBoard as Board

_simplest_empty_board = Board(False, False, False, False)

class World(object): # tododoc: allow setting multiple values before changing board
    def __init__(self, board=_simplest_empty_board,
                 board_position=(0, 0)):
        
        self.board = board
        assert isinstance(board, Board)
        self.board_position = board_position
        self._calculate_board_far_corner()
        
        
    def set_board_position(self, board_position):
        self.board_position = board_position
        self._calculate_board_far_corner()
        
        
    def set_board(self, board):
        self.board = board
        self._calculate_board_far_corner()
        # Could check if different length, but it's a neglible optimization
            
        
    def _calculate_board_far_corner(self):
        self.board_far_corner = (
            self.board_position[0] + self.board.length,
            self.board_position[1] + self.board.length
        )
        
        
    def _world_coords_to_board_coords(self, x, y):
        return (
            x - self.board_position[0],
            y - self.board_position[1]
        )
    
    
    def _board_coords_to_world_coords(self, x, y):
        return (
            x + self.board_position[0],
            y + self.board_position[1]
        )
        

    def _bloat_board(self):        
        bloat_radius = self.board.length // 2
        self.board_position = (
            self.board_position[0] - bloat_radius,
            self.board_position[1] - bloat_radius
        )
        self.board_far_corner = (
            self.board_far_corner[0] + bloat_radius,
            self.board_far_corner[1] + bloat_radius
        )
        self.board = self.board.get_bloated_to_quad_board()

        
        
    def get(self, x, y):
        (bx, by) = self._world_coords_to_board_coords(x, y)
        
        if (0 <= bx <= self.board.length - 1) and \
           (0 <= by <= self.board.length - 1):
            
            return self.board.get(x, y)
        
        else:
            # The requested point is not in the board, it's out in the vacuum.
            return False

        
    def set(self, x, y, value):
        
        while True:

            (bx, by) = self._world_coords_to_board_coords(x, y)

            if (0 <= bx <= self.board.length - 1) and \
               (0 <= by <= self.board.length - 1):
                break
            
            # As long as the board does not cover the point, bloat it:
            
            self._bloat_board()
            
            # (It's slightly wasteful, mostly on the first turns, to bloat it
            # mindlessly as we do here.)
            
           
        self.board = self.board.get_with_cell_change(bx, by, value)

        
    def step(self):
        try:
            self.board = self.board.get_next()
        except boards.misc.NotEnoughInformation:
            self._bloat_board()
            self.board = self.board.get_next()
    
            
    def iter_cells(self, state=True, rectangle=None):
        if rectangle is not None:
            rectangle = self._world_coords_to_board_coords(*rectangle[0:2]) + \
                        self._world_coords_to_board_coords(*rectangle[2:4]) 
        for board_coords in self.board.cells_tuple(state, rectangle):
            yield self._board_coords_to_world_coords(*board_coords)
            
            
    @staticmethod
    def create_messy(length=20):
        world = World()
        for x in xrange(length):
            for y in xrange(length):
                if random.choice([True, False]):
                    world.set(x, y, True)
        return world
                
        
if __name__ == '__main__':
    w = World.create_messy(4)
    print w.board
    x = tuple(w.iter_cells())
    print x
        
        