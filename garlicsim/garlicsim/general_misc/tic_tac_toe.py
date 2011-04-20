
import copy
import numpy

import garlicsim
import cloud

WIN = 1
DRAW = 0
LOSE = -1

class Enum(object):
    

class WinStatus(Enum):
    choices = {'WIN': 'Win',
               'DRAW': 'Draw',
               'LOSE': 'Lose'}
    
    def __neg__(self):
        if self is WinStatus.WIN:
            return WinStatus.LOSE
        
        
- WIN
    

class Board(object):
    def __init__(self, array=None):
        if array is None:
            self.array = numpy.zeros((3, 3), int)
        else:
            self.array = array
        
    def iterate_possible_moves(self, our_code):
        for i in range(3):
            for j in range(3):
                if self[i, j] == 0:
                    board_copy = copy.deepcopy(self)
                    board_copy[i, j] = our_code
                    yield board_copy
                
    def __getitem__(self, *args, **kwargs):
        return self.array.__getitem__(*args, **kwargs)
    def __repr__(self, *args, **kwargs):
        return self.array.__repr__(*args, **kwargs)
    def __setitem__(self, *args, **kwargs):
        return self.array.__setitem__(*args, **kwargs)

    def _iterate_lines(self):
        for i in range(3):
            yield self[i, :]
            yield self[:, i]
            
        yield [self[0, 0], self[1, 1], self[2, 2]]
        yield [self[0, 2], self[1, 1], self[2, 0]]
    
    def who_won(self):
        for line in self._iterate_lines():
            if garlicsim.general_misc.logic_tools.all_equal(line):
                return line[0]
        return None

    @garlicsim.general_misc.caching.cache()
    def could_we_win(self, our_code):
        
        possible_moves = tuple(self.iterate_possible_moves(our_code))
        
        if not possible_moves:
            return (DRAW, None)
        
        for possible_move in possible_moves:
            if possible_move.who_won() == our_code:
                return (WIN, possible_move)

        best_result = (LOSE, possible_move)
            
        for possible_move in possible_moves:
            result = possible_move.could_we_win(3 - our_code)[0]
            if -result >= best_result[0]:
                best_result = (-result, possible_move)
                if -result == WIN:
                    break
        return best_result

import psyco
psyco.full()

if __name__ == '__main__':
    b = Board(numpy.array([[2, 0, 2],
                           [0, 1, 2],
                           [1, 0, 1]], int))
    print(b.could_we_win(1))
    1/0