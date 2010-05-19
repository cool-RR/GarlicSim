
import random
import itertools

from garlicsim.general_misc.third_party import abc
from garlicsim.general_misc import caching
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import misc_tools

import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    """
    @staticmethod
    def create_diehard(width=45, height=25):
        state = State()
        state.board = Board.create_diehard(width, height)
        return state
    """
    
    @staticmethod
    def create_root(level=4, fill=False):
        return State(QuadBoard.create_root(level, fill))
    
    
    @staticmethod
    def create_messy_root(level=4, fill=False):
        return State(QuadBoard.create_messy_root(level))
    
    
    @staticmethod
    def create_glider():
        board = QuadBoard(
            QuadBoard(False, True, False, False),
            QuadBoard(False, False, True, False),
            QuadBoard(True, True, False, False),
            QuadBoard(True, False, False, False),
        )
        return State(board)
    
    
    def __init__(self, board):
        garlicsim.data_structures.State.__init__(self)
        self.board = board
        
    
    def step(self):
        try:
            next_board = self.board.get_next()
        except NotEnoughInformation:
            next_board = self.board.get_bloated_to_quad_board().get_next()
        return State(next_board)

    
    def __repr__(self):
        return self.board.__repr__()
    
    
    def __eq__(self, other):
        return isinstance(other, State) and self.board == other.board

    
    def __ne__(self, other):
        return not self.__eq__(other)

    
    
class NotEnoughInformation(garlicsim.misc.SmartException):
    pass
    
class CachedAbstractType(caching.CachedType, abc.ABCMeta):
    pass

class Board(object):
    __metaclass__ = CachedAbstractType
    
    @abc.abstractmethod
    def get(self, x, y):
        pass
    
    
    def __iter__(self):
        length = self.length
        coordinate_pairs = (divmod(i, length) for i in xrange(length ** 2))
        for coordinate_pair in coordinate_pairs:
            yield self.get(*coordinate_pair)
            
    def __repr__(self):
        '''Display the board, ASCII-art style.'''
        repr_cell = lambda x, y: '#' if self.get(x, y) is True else ' '
        repr_row = lambda y: ''.join(repr_cell(x, y) for x in xrange(self.length))
        return '\n'.join(repr_row(y) for y in xrange(self.length))
        
    
    def __eq__(self, other):
        return self is other
        #if not isinstance(other, Board):
            #return NotImplemented
        #return self.length == other.length and \
               #all((x == y for (x, y) in itertools.izip(self.kids, other.kids)))

    
    def __ne__(self, other):
        return not (self is other)
    
    
    
# tododoc: probably change True/False to Alive/Dead
    
class QuadBoard(Board):

    @staticmethod
    def create_root(level, fill=False): # todo: make right
        assert isinstance(fill, bool)
        if level == 0:
            return fill
        else:
            return QuadBoard(
                *tuple(
                    QuadBoard.create_root(level - 1, fill) for i in range(4)
                )
            )
        
    
    @staticmethod
    def create_messy_root(level):
        if level == 0:
            return random.choice([True, False])
        else:
            return QuadBoard(
                *tuple(
                    QuadBoard.create_messy_root(level - 1) for i in range(4)
                )
            )
            
    
    def __init__(self, kid_nw, kid_ne, kid_sw, kid_se):
        
        self.kid_nw = kid_nw
        self.kid_ne = kid_ne
        self.kid_sw = kid_sw
        self.kid_se = kid_se
        
        # self.kids = (kid_nw, kid_ne, kid_sw, kid_se)
        
        if isinstance(kid_nw, bool):
            assert all(isinstance(kid, bool) for kid in
                       (kid_nw, kid_ne, kid_sw, kid_se))
            self.level = 1
            
        else:
            self.level = level = kid_nw.level + 1
        
            if level >= 2:
                
                self.sub_quad_board = QuadBoard(
                    kid_nw.kid_se,
                    kid_ne.kid_sw,
                    kid_sw.kid_ne,
                    kid_se.kid_nw
                )
                
                if level >= 3:
                    
                    self.extended_kids = (
                        
                        kid_nw,
                        
                        QuadBoard(
                            kid_nw.kid_ne,
                            kid_ne.kid_nw,
                            kid_nw.kid_se,
                            kid_ne.kid_sw
                        ),
                        
                        kid_ne,
                        
                        QuadBoard(
                            kid_nw.kid_sw,
                            kid_nw.kid_se,
                            kid_sw.kid_nw,
                            kid_sw.kid_ne
                            ),
                        
                        self.sub_quad_board,
                        
                        QuadBoard(
                            kid_ne.kid_sw,
                            kid_ne.kid_se,
                            kid_se.kid_nw,
                            kid_se.kid_ne
                            ),
                        
                        kid_sw,
                        
                        QuadBoard(
                            kid_sw.kid_ne,
                            kid_se.kid_nw,
                            kid_sw.kid_se,
                            kid_se.kid_sw
                            ),
                        
                        kid_se
                        
                    )
                    
                    self.sub_tri_board = \
                        TriBoard.create_from_parents(self.extended_kids)
        
        self.length = 2 ** self.level
        
        
    def get(self, x, y):
        x_div, x_mod = divmod(x, self.length // 2)
        y_div, y_mod = divmod(y, self.length // 2)
        kid = self.kids[x_div + 2 * y_div]
        if self.level == 1:
            return kid
        else:
            assert self.level >= 2
            return kid.get(x_mod, y_mod)

    
    def get_bloated_to_quad_board(self):
        
        empty_smaller_quad_board = \
            QuadBoard.create_root(self.level - 1, fill=False)
        
        return QuadBoard(
            
            QuadBoard(
                empty_smaller_quad_board,
                empty_smaller_quad_board,
                empty_smaller_quad_board,
                self.kid_nw
                ),
            
            QuadBoard(
                empty_smaller_quad_board,
                empty_smaller_quad_board,
                self.kid_ne,
                empty_smaller_quad_board
                ),
            
            QuadBoard(
                empty_smaller_quad_board,
                self.kid_sw,
                empty_smaller_quad_board,
                empty_smaller_quad_board
                ),
            
            QuadBoard(
                self.kid_se,
                empty_smaller_quad_board,
                empty_smaller_quad_board,
                empty_smaller_quad_board
                )
            
        )
        
        
    @caching.cache
    def is_empty(self):
        if self.level == 1:
            return not (self.kid_nw or self.kid_ne or self.kid_sw or self.kid_se)
        else: # self.level >= 2
            return self.kid_nw.is_empty() and self.kid_ne.is_empty() and \
                   self.kid_sw.is_empty() and self.kid_se.is_empty()

        
    @caching.cache    
    def get_next(self):
        # Could check that the borders around the sub_tri_board are clean
        # instead of the borders around the sub_quad_board, (in big enough
        # boards,) and that will redurce bloating, but it's O(1) so not
        # important.
        
        if self.level <= 1:
            raise NotEnoughInformation
        
        if self.level <= 2:
            raise NotEnoughInformation
            # This is not really true in this case, but would be a bummer to
            # implement because there's no sub_tri_board.
        
        border_grand_kids = [self.kids[i].kids[j] for (i, j) in 
                             cute_iter_tools.product(xrange(4), xrange(4))
                             if i + j != 3]
        if not all((border_grand_kid.is_empty() for border_grand_kid
                    in border_grand_kids)):
            
            raise NotEnoughInformation
                
        next_sub_tri_board = self.get_future_sub_tri_board(1)
        
        return next_sub_tri_board.get_bloated_to_quad_board()
        
        

    
    @caching.cache
    def get_future_sub_tri_board(self, n=1):
        assert self.level >= 3
        assert 0 <= n <= 2 ** (self.level - 3)
        return TriBoard(
            *tuple(
                extended_kid.get_future_sub_quad_board(n) for extended_kid
                in self.extended_kids
            )
        )
    
            
    @caching.cache
    def get_future_sub_quad_board(self, n=1):
        if self.level >= 3:
            maximum_n = 2 ** (self.level - 2)
            assert 0 <= n <= maximum_n
            
            second_n = min(n, maximum_n // 2)
            first_n = n - second_n
            
            future_sub_tri_board = self.get_future_sub_tri_board(first_n)
            
            return future_sub_tri_board.get_future_sub_quad_board(second_n)
        else:
            assert self.level == 2
            if n == 0:
                return self.sub_quad_board
            else:
                assert n == 1
                return self._get_next_sub_quad_board_for_level_two()
    
    
    
        
    def _get_next_sub_quad_board_for_level_two(self):
        # todo optimize: can break `i` loop manually. After two out of three
        # runs, check true_neighbor_count. if it's bigger than 3, no use to
        # continue.
        assert self.level == 2
        
        
        n = self.kid_nw.kid_ne + self.kid_ne.kid_nw
        w = self.kid_nw.kid_sw + self.kid_sw.kid_nw
        e = self.kid_ne.kid_se + self.kid_se.kid_ne
        s = self.kid_se.kid_sw + self.kid_sw.kid_se
        
        nw = int(self.kid_nw.kid_nw)
        ne = int(self.kid_ne.kid_ne)
        sw = int(self.kid_sw.kid_sw)
        se = int(self.kid_se.kid_se)
        
        core = self.kid_nw.kid_se + self.kid_ne.kid_sw + \
             self.kid_sw.kid_ne + self.kid_se.kid_nw
        
        
        precount_for_first = n + w + nw + core
        
        if precount_for_first <= 2:
            first = False
        elif precount_for_first == 3:
            first = True
        elif precount_for_first == 4:
            first = self.kid_nw.kid_se
        else: # precount_for_first >= 5
            first = False
        
        
        precount_for_second = n + e + ne + core
        
        if precount_for_second <= 2:
            second = False
        elif precount_for_second == 3:
            second = True
        elif precount_for_second == 4:
            second = self.kid_ne.kid_sw
        else: # precount_for_second >= 5
            second = False
        
        
        precount_for_third = s + w + sw + core
        
        if precount_for_third <= 2:
            third = False
        elif precount_for_third == 3:
            third = True
        elif precount_for_third == 4:
            third = self.kid_sw.kid_ne
        else: # precount_for_third >= 5
            third = False
        
        
        precount_for_fourth = s + e + se + core
        
        if precount_for_fourth <= 2:
            fourth = False
        elif precount_for_fourth == 3:
            fourth = True
        elif precount_for_fourth == 4:
            fourth = self.kid_se.kid_nw
        else: # precount_for_fourth >= 5
            fourth = False
        
        
        return QuadBoard(first, second, third, fourth)
                        
    

class TriBoard(Board):

    @staticmethod
    def create_from_parents(parents):
        return TriBoard(*tuple(parent.sub_quad_board for parent in parents))
    
    def __init__(self, kid_nw, kid_n, kid_ne, kid_w, kid_c, kid_e, kid_sw, kid_s, kid_se):
        
        self.kid_nw = kid_nw
        self.kid_n = kid_n
        self.kid_ne = kid_ne
        self.kid_w = kid_w
        self.kid_c = kid_c
        self.kid_e = kid_e
        self.kid_sw = kid_sw
        self.kid_s = kid_s
        self.kid_se = kid_se
        
        self.kids = (kid_nw, kid_n, kid_ne, kid_w, kid_c, kid_e, kid_sw, kid_s, kid_se)
        
        assert all(isinstance(kid, QuadBoard) for kid in self.kids)            
        
        self.level = level = kid_nw.level + 1.5
        # It's actually 1.5849625007211, but who's counting.
        
        assert self.level >= 2.5
        
        self.length = 3 * (2 ** int(self.level - 1))
        
        self.sub_quad_board = QuadBoard(
            QuadBoard(
                kid_nw.kid_se,
                kid_n.kid_sw,
                kid_w.kid_ne,
                kid_c.kid_nw
                ),
            QuadBoard(
                kid_n.kid_se,
                kid_e.kid_sw,
                kid_c.kid_ne,
                kid_e.kid_nw
                ),
            QuadBoard(
                kid_w.kid_se,
                kid_c.kid_sw,
                kid_sw.kid_ne,
                kid_s.kid_nw
                ),
            QuadBoard(
                kid_c.kid_se,
                kid_e.kid_sw,
                kid_s.kid_ne,
                kid_se.kid_nw
                )
        )
        
        self.bloated_kids = (
                        
            QuadBoard(
                kid_nw,
                kid_n,
                kid_w,
                kid_c
                ),
            
            QuadBoard(
                kid_n,
                kid_ne,
                kid_c,
                kid_e
                ),
            
            QuadBoard(
                kid_w,
                kid_c,
                kid_sw,
                kid_s
                ),
            
            QuadBoard(
                kid_c,
                kid_e,
                kid_s,
                kid_se
                ),
            
        )
        

        
        
    def get(self, x, y):
        x_div, x_mod = divmod(x, self.length // 3)
        y_div, y_mod = divmod(y, self.length // 3)
        kid = self.kids[x_div + 3 * y_div]
        return kid.get(x_mod, y_mod)
    
            
    @caching.cache
    def get_future_sub_quad_board(self, n=1):
        assert 0 <= n <= 2 ** (self.level - 2.5)
        return QuadBoard(
            *tuple(
                bloated_kid.get_future_sub_quad_board(n) for bloated_kid
                in self.bloated_kids
            )
        )
    
    
    def get_bloated_to_quad_board(self):
        
        empty_tiny_quad_board = \
            QuadBoard.create_root(int(round(self.level - 2.5)), fill=False)
        
        return QuadBoard(
            
            
            QuadBoard(
                
                QuadBoard(
                    empty_tiny_quad_board,
                    empty_tiny_quad_board,
                    empty_tiny_quad_board,
                    self.kid_nw.kid_nw
                ),
                
                QuadBoard(
                    empty_tiny_quad_board,
                    empty_tiny_quad_board,
                    self.kid_nw.kid_ne,
                    self.kid_n.kid_nw
                ),
                
                QuadBoard(
                    empty_tiny_quad_board,
                    self.kid_nw.kid_sw,
                    empty_tiny_quad_board,
                    self.kid_w.kid_nw
                ),
                
                QuadBoard(
                    self.kid_nw.kid_se,
                    self.kid_n.kid_sw,
                    self.kid_w.kid_ne,
                    self.kid_c.kid_nw
                ),
                 
            ),
            
            
            QuadBoard(
                
                QuadBoard(
                    empty_tiny_quad_board,
                    empty_tiny_quad_board,
                    self.kid_n.kid_ne,
                    self.kid_ne.kid_nw
                ),
                
                QuadBoard(
                    empty_tiny_quad_board,
                    empty_tiny_quad_board,
                    self.kid_ne.kid_ne,
                    empty_tiny_quad_board
                ),
                
                QuadBoard(
                    self.kid_n.kid_se,
                    self.kid_ne.kid_sw,
                    self.kid_c.kid_ne,
                    self.kid_e.kid_nw
                ),
                
                QuadBoard(
                    self.kid_ne.kid_se,
                    empty_tiny_quad_board,
                    self.kid_e.kid_ne,
                    empty_tiny_quad_board
                )
                
            ),
            
            
            QuadBoard(
                
                QuadBoard(
                    empty_tiny_quad_board,
                    self.kid_w.kid_sw,
                    empty_tiny_quad_board,
                    self.kid_sw.kid_nw
                ),
                
                QuadBoard(
                    self.kid_w.kid_se,
                    self.kid_c.kid_sw,
                    self.kid_sw.kid_ne,
                    self.kid_s.kid_nw
                ),
                
                QuadBoard(
                    empty_tiny_quad_board,
                    self.kid_sw.kid_sw,
                    empty_tiny_quad_board,
                    empty_tiny_quad_board
                ),
                
                QuadBoard(
                    self.kid_sw.kid_se,
                    self.kid_s.kid_sw,
                    empty_tiny_quad_board,
                    empty_tiny_quad_board
                ),
                 
            ),
            
            
            QuadBoard(
                
                QuadBoard(
                    self.kid_c.kid_se,
                    self.kid_e.kid_sw,
                    self.kid_s.kid_ne,
                    self.kid_se.kid_nw
                ),
                
                QuadBoard(
                    self.kid_e.kid_se,
                    empty_tiny_quad_board,
                    self.kid_se.kid_ne,
                    empty_tiny_quad_board
                ),
                
                QuadBoard(
                    self.kid_s.kid_se,
                    self.kid_se.kid_sw,
                    empty_tiny_quad_board,
                    empty_tiny_quad_board
                ),
                
                QuadBoard(
                    self.kid_se.kid_se,
                    empty_tiny_quad_board,
                    empty_tiny_quad_board,
                    empty_tiny_quad_board
                ),
                 
            ),
            
            
        )
            
    
if __name__ == '__main__':
    board = QuadBoard(
        QuadBoard((False, True, False, False)),
        QuadBoard((False, False, True, False)),
        QuadBoard((True, True, False, False)),
        QuadBoard((True, False, False, False))
    )
    b = board.get_bloated_to_quad_board()
    b.get_future_sub_quad_board(1)
    1+1