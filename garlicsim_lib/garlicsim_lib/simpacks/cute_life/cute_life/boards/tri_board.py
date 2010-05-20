import random

from garlicsim.general_misc import caching

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
            