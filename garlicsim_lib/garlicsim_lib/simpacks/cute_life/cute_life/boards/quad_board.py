
import random
import itertools

from garlicsim.general_misc import caching
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import misc_tools

from base_board import BaseBoard

from .misc import NotEnoughInformation

class QuadBoard(BaseBoard):

    @staticmethod # tododoc: consider killing
    def create_root(level, fill=False): # todo: make right
        assert isinstance(fill, bool)
        if level == 0:
            return fill
        else:
            return QuadBoard(
                *(QuadBoard.create_root(level - 1, fill) for i in range(4))
            )
        
    
    @staticmethod
    def create_messy_root(level): # tododoc: consider killing tihs
        if level == 0:
            return random.choice([True, False])
        else:
            return QuadBoard(
                *(QuadBoard.create_messy_root(level - 1) for i in range(4))
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
            self.length = 2
            
        else:
            self.level = level = kid_nw.level + 1
            self.length = 2 ** self.level
        
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
                    
                    #self.sub_tri_board = \
                        #TriBoard.create_from_parents(self.extended_kids)
        
        
    def get_kid_by_number(self, n):
        if n == 0:
            return self.kid_nw
        elif n == 1:
            return self.kid_ne
        elif n == 2:
            return self.kid_sw
        else: # n == 3
            return self.kid_se
        
    def get(self, x, y):
        x_div, x_mod = divmod(x, self.length // 2)
        y_div, y_mod = divmod(y, self.length // 2)
        assert 0 <= x_div <= 1
        assert 0 <= y_div <= 1
        kid = self.get_kid_by_number(x_div + 2 * y_div)
        if self.level == 1:
            return kid
        else:
            assert self.level >= 2
            return kid.get(x_mod, y_mod)

    @caching.cache
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
        
        border_grand_kids = (
            self.kid_nw.kid_ne, self.kid_nw.kid_sw,
            self.kid_ne.kid_nw, self.kid_ne.kid_se,
            self.kid_sw.kid_nw, self.kid_sw.kid_se,
            self.kid_se.kid_ne, self.kid_se.kid_sw,
            
            self.kid_nw.kid_nw, self.kid_ne.kid_ne,
            self.kid_sw.kid_sw, self.kid_se.kid_se,
            # Corner grandkids checked last. Faster because they have smaller
            # chance of being occupied
        )
        if not all(border_grand_kid.is_empty() for border_grand_kid
                    in border_grand_kids):
            
            raise NotEnoughInformation
                
        next_sub_tri_board = self.get_future_sub_tri_board(1)
        
        return next_sub_tri_board.get_bloated_to_quad_board()
        
        

    
    @caching.cache
    def get_future_sub_tri_board(self, n=1):
        assert self.level >= 3
        assert 0 <= n <= 2 ** (self.level - 3)
        return TriBoard(
            *(extended_kid.get_future_sub_quad_board(n) for extended_kid
              in self.extended_kids)
        )
    
            
    @caching.cache
    def get_future_sub_quad_board(self, n=1):
        if n == 0:
            return self.sub_quad_board
        if self.level >= 3:
            maximum_n = 2 ** (self.level - 2)
            assert 0 <= n <= maximum_n
            
            second_n = min(n, maximum_n // 2)
            first_n = n - second_n
            
            future_sub_tri_board = self.get_future_sub_tri_board(first_n)
            
            return future_sub_tri_board.get_future_sub_quad_board(second_n)
        else:
            assert self.level == 2
            assert n == 1
            return self._get_next_sub_quad_board_for_level_two()
        
    
    
        
    def _get_next_sub_quad_board_for_level_two(self):
        # todo optimize: can break `i` loop manually. After two out of three
        # runs, check true_neighbor_count. if it's bigger than 3, no use to
        # continue.
        # not cached because it's called only from
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
                        
    def get_with_cell_change(self, x, y, value):
        x_div, x_mod = divmod(x, self.length // 2)
        y_div, y_mod = divmod(y, self.length // 2)
        kids = [self.kid_nw, self.kid_ne, self.kid_sw, self.kid_se]
        i_kid = x_div + 2 * y_div
        if self.level == 1:    
            kids[i_kid] = value
        else: # self.level >= 2
            kids[i_kid] = kids[i_kid].get_with_cell_change(x_mod, y_mod, value)
        return QuadBoard(*kids)

    
    def cells_tuple(self, state=True, rectangle=None):
        if rectangle is None:
            return self._cells_tuple_full(state)
        
        (x, y, xx, yy) = rectangle
        assert (x <= xx) and (y <= yy)
        
        if (x <= 0) and (y <= 0) and \
           (xx >= self.length - 1) and (yy >= self.length - 1):
            
            return self._cells_tuple_full(state)
        
        elif self.level == 1:
            full_tuple = self._cells_tuple_full(state)
            return tuple((a, b) for (a, b) in full_tuple
                         if (x <= a <= xx) and (y <= b <= yy))
        
        else: # self.level >= 2 and we have a partial match
                
            half_length = self.length // 2
            return tuple(
                itertools.chain(
                    self.kid_nw.cells_tuple(state, rectangle),
                    (
                        (a + half_length, b) for (a, b) in
                        self.kid_ne.cells_tuple(
                            state,
                            (x - half_length, y, xx - half_length, yy)
                        )
                        ),
                    (
                        (a, b + half_length) for (a, b) in
                        self.kid_sw.cells_tuple(
                            state,
                            (x, y - half_length, xx, yy - half_length)
                        )
                        ),
                    (
                        (a + half_length, b + half_length) for (a, b) in
                        self.kid_se.cells_tuple(
                            state,
                            (x - half_length, y - half_length,
                             xx - half_length, yy - half_length)
                        )
                    )
                )
            )
        
    
    
    @caching.cache
    def _cells_tuple_full(self, state=True):
        
        if self.level == 1:
            result_list = []
            if self.kid_nw is state:
                result_list.append((0, 0))
            if self.kid_ne is state:
                result_list.append((1, 0))
            if self.kid_sw is state:
                result_list.append((0, 1))
            if self.kid_se is state:
                result_list.append((1, 1))
            return tuple(result_list)
        
        else: # self.level >= 2
                
            half_length = self.length // 2
            return tuple(
                itertools.chain(
                    self.kid_nw._cells_tuple_full(state),
                    (
                        (a + half_length, b) for (a, b) in
                        self.kid_ne._cells_tuple_full(state)
                        ),
                    (
                        (a, b + half_length) for (a, b) in
                        self.kid_sw._cells_tuple_full(state)
                        ),
                    (
                        (a + half_length, b + half_length) for (a, b) in
                        self.kid_se._cells_tuple_full(state)
                    )
                )
            )
        

class TriBoard(BaseBoard):

    @staticmethod
    def create_from_parents(parents):
        return TriBoard(*(parent.sub_quad_board for parent in parents))
    
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
        
        # self.kids = (kid_nw, kid_n, kid_ne, kid_w, kid_c, kid_e, kid_sw, kid_s, kid_se)
        
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
            *(bloated_kid.get_future_sub_quad_board(n) for bloated_kid
              in self.bloated_kids)
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
            
    