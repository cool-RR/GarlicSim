
import random
import itertools

from garlicsim.general_misc import caching
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import misc_tools

from base_board import BaseBoard
from tri_board import TriBoard
import inty

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
        
        if isinstance(kid_nw, int):
            assert all(isinstance(kid, int) for kid in
                       (kid_nw, kid_ne, kid_sw, kid_se))
            self.level = 3    
            self.length = 8
            
            self.sub_quad_board = \
                inty.int_four_board.combine_four(
                    kid_nw,
                    kid_ne,
                    kid_sw,
                    kid_se
                )
            
            self.extended_kids = (
                
                kid_nw,
                
                inty.int_four_board.combine_two_horizontally(kid_nw, kid_ne),
                
                kid_ne,
                
                inty.int_four_board.combine_two_vertically(kid_nw, kid_sw),
                
                self.sub_quad_board,
                
                inty.int_four_board.combine_two_vertically(kid_ne, kid_se),
                
                kid_sw,
                
                inty.int_four_board.combine_two_horizontally(kid_sw, kid_se),
                
                kid_se
                
            )
            
                    
        else: # self.level >= 4
            self.level = level = kid_nw.level + 1
            self.length = 2 ** self.level
        
            self.sub_quad_board = QuadBoard(
                kid_nw.kid_se,
                kid_ne.kid_sw,
                kid_sw.kid_ne,
                kid_se.kid_nw
            )
            
                
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
        if self.level == 3:
            return inty.int_four_board.get(x_mod, y_mod)
        else: # self.level >= 4
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
        if self.level == 3:
            return (self.kid_nw == self.kid_ne == self.kid_sw == self.kid_se == 0)
        else: # self.level >= 4
            return self.kid_nw.is_empty() and self.kid_ne.is_empty() and \
                   self.kid_sw.is_empty() and self.kid_se.is_empty()

        
    @caching.cache    
    def get_next(self):
        # Could check that the borders around the sub_tri_board are clean
        # instead of the borders around the sub_quad_board, (in big enough
        # boards,) and that will redurce bloating, but it's O(1) so not
        # important.
        
        if self.level <= 3:
            raise NotImplemented
            # And would probably never be, just bloat your board.
            
        
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
        if self.level == 3:
            WAS HERE
        else: # self.level >= 4
            assert 0 <= n <= 2 ** (self.level - 3)
            return TriBoard(
                *(extended_kid.get_future_sub_quad_board(n) for extended_kid
                  in self.extended_kids)
            )
    
            
    @caching.cache
    def get_future_sub_quad_board(self, n=1):
        if n == 0:
            return self.sub_quad_board
        
        elif self.level == 3:
            
            if n >= 2:
                raise NotImplemented
            assert n == 1
            return self._get_next_sub_quad_board_for_level_three()
        
        else: # self.level >= 4
        
            maximum_n = 2 ** (self.level - 2)
            assert 0 <= n <= maximum_n
            
            second_n = min(n, maximum_n // 2)
            first_n = n - second_n
            
            future_sub_tri_board = self.get_future_sub_tri_board(first_n)
            
            return future_sub_tri_board.get_future_sub_quad_board(second_n)
        
    
    
        
    def _get_next_sub_quad_board_for_level_three(self):
        # todo optimize: can break `i` loop manually. After two out of three
        # runs, check true_neighbor_count. if it's bigger than 3, no use to
        # continue.        
        # not cached because it's called only from get_future_sub_quad_board,
        # which is cached.
        
        assert self.level == 3
        
        (kid_nw, kid_ne, kid_sw, kid_se) = \
            (self.kid_nw, self.kid_ne, self.kid_sw, self.kid_se)
        
        arrays = inty.arrays
        
        bloated_kid_nw = sum((
            arrays.nw_piece_for_nw_bloated_kid[kid_nw],
            arrays.ne_piece_for_nw_bloated_kid[kid_ne],
            arrays.sw_piece_for_nw_bloated_kid[kid_sw],
            arrays.se_piece_for_nw_bloated_kid[kid_se]
        ))
        
        bloated_kid_ne = sum((
            arrays.nw_piece_for_ne_bloated_kid[kid_nw],
            arrays.ne_piece_for_ne_bloated_kid[kid_ne],
            arrays.sw_piece_for_ne_bloated_kid[kid_sw],
            arrays.se_piece_for_ne_bloated_kid[kid_se]
        ))
        
        bloated_kid_sw = sum((
            arrays.nw_piece_for_sw_bloated_kid[kid_nw],
            arrays.ne_piece_for_sw_bloated_kid[kid_ne],
            arrays.sw_piece_for_sw_bloated_kid[kid_sw],
            arrays.se_piece_for_sw_bloated_kid[kid_se]
        ))
        
        bloated_kid_se = sum((
            arrays.nw_piece_for_se_bloated_kid[kid_nw],
            arrays.ne_piece_for_se_bloated_kid[kid_ne],
            arrays.sw_piece_for_se_bloated_kid[kid_sw],
            arrays.se_piece_for_se_bloated_kid[kid_se]
        ))
        
        return inty.int_two_board.combine_four_to_int_four_board(
            arrays.int_four_board_to_next_sub_int_two_board[bloated_kid_nw],
            arrays.int_four_board_to_next_sub_int_two_board[bloated_kid_ne],
            arrays.int_four_board_to_next_sub_int_two_board[bloated_kid_sw],
            arrays.int_four_board_to_next_sub_int_two_board[bloated_kid_se],
            )
    
    
        
                        
    def get_with_cell_change(self, x, y, value):
        x_div, x_mod = divmod(x, self.length // 2)
        y_div, y_mod = divmod(y, self.length // 2)
        kids = [self.kid_nw, self.kid_ne, self.kid_sw, self.kid_se]
        i_kid = x_div + 2 * y_div
        if self.level == 3:
            changer = inty.int_four_board.get_with_cell_change_to_true if value \
                    else inty.int_four_board.get_with_cell_change_to_false
            kids[i_kid] = changer(kids[i_kid])
        else: # self.level >= 4
            kids[i_kid] = kids[i_kid].get_with_cell_change(x_mod, y_mod, value)
        return QuadBoard(*kids)

    
    def cells_tuple(self, state=True, rectangle=None):
        if rectangle is None:
            return self._cells_tuple_full(state)
        
        (x, y, xx, yy) = rectangle
        assert (x <= xx) and (y <= yy)
        
        if (x <= 0) and (y <= 0) and \
           (xx >= self.length - 1) and (yy >= self.length - 1):
            # total match
            
            return self._cells_tuple_full(state)
        
        elif (x > self.length - 1) or (y > self.length - 1) or \
             (xx < 0) or (yy < 0):
            # No match at all
            return ()
        
        else: # partial match
            if self.level == 3:
                full_tuple = self._cells_tuple_full(state)
                return tuple((a, b) for (a, b) in full_tuple
                             if (x <= a <= xx) and (y <= b <= yy))    
            else: # self.level >= 4
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
        
        if self.level == 3:
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
        
        else: # self.level >= 4
                
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
        
