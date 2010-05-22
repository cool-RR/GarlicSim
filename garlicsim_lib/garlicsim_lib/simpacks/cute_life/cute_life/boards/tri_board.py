import random

from garlicsim.general_misc import caching

import inty
from base_board import BaseBoard

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
        
        if isinstance(kid_nw, int):
            
            self.level = 3.5
            # It's actually 3.5849625007211, but who's counting.
            self.length = 12
        
            self.sub_quad_board = QuadBoard(
                inty.int_four_board.combine_four(kid_nw, kid_n, kid_w, kid_c),
                inty.int_four_board.combine_four(kid_n, kid_ne, kid_c, kid_e),
                inty.int_four_board.combine_four(kid_w, kid_c, kid_sw, kid_s),
                inty.int_four_board.combine_four(kid_c, kid_e, kid_s, kid_se)
            )
            
            self.bloated_kids = (
                QuadBoard(kid_nw, kid_n, kid_w, kid_c),
                QuadBoard(kid_n, kid_ne, kid_c, kid_e),
                QuadBoard(kid_w, kid_c, kid_sw, kid_s),
                QuadBoard(kid_c, kid_e, kid_s, kid_se)
            )
            
        else:
            
            self.level = level = kid_nw.level + 1.5
            # It's actually 1.5849625007211.
            
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
                QuadBoard(kid_nw, kid_n, kid_w, kid_c),
                QuadBoard(kid_n, kid_ne, kid_c, kid_e),
                QuadBoard(kid_w, kid_c, kid_sw, kid_s),
                QuadBoard(kid_c, kid_e, kid_s, kid_se)
            )
        

    
        
    def get_kid_by_number(self, n):
        if n == 0:
            return self.kid_nw
        elif n == 1:
            return self.kid_n
        elif n == 2:
            return self.kid_ne
        elif n == 3:
            return self.kid_w
        elif n == 4:
            return self.kid_c
        elif n == 5:
            return self.kid_e
        elif n == 6:
            return self.kid_sw
        elif n == 7:
            return self.kid_s
        else: # n == 8
            return self.kid_se
        
            
    def get(self, x, y):
        x_div, x_mod = divmod(x, self.length // 3)
        y_div, y_mod = divmod(y, self.length // 3)
        kid = self.get_kid_by_number(x_div + 3 * y_div)
        if self.level == 3.5:
            return inty.int_four_board.get(kid, x_mod, y_mod)
        else: # self.level >= 4.5
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

from quad_board import QuadBoard