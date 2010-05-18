
import random


from garlicsim.general_misc.third_party import abc
from garlicsim.general_misc import caching
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import misc_tools

import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    # This is your State subclass. Your state objects should contain all the
    # information there is about a moment of time in your simulation.
    
    def __init__(self):
        pass
    
    
    def step(self):
        # This function is the heart of your simpack. What it does is take an
        # existing world state, and output the next world state.
        #
        # This is where all the crunching gets done. This function defines the
        # laws of your simulation world.
        # 
        # The step function is one of the very few things that your simpack
        # **must** define. Almost all of the other definitions are optional.
        pass
    
        
    @staticmethod
    def create_root():
        # In this function you create a root state. This usually becomes the
        # first state in your simulation. You can make this function do
        # something simple: For example, if you're simulating Life, you can make
        # this function create an empty board.
        #
        # This function may take arguments, if you wish, to be used in making
        # the state. For example, in a Life simulation you may want to specify
        # the width and height of the board using arguments to this function.
        #
        # This function returns the newly-created state.
        pass

    
    @staticmethod
    def create_messy_root():
        # In this function you create a messy root state. This usually becomes the
        # first state in your simulation. 
        #
        # Why messy? Because sometimes you want to have fun in your simulations.
        # You want to create a world where there's a lot of mess, with many
        # objects interacting with each other. This is a good way to test-drive
        # your simulation.
        #
        # This function may take arguments, if you wish, to be used in making
        # the state. For example, in a Life simulation you may want to specify
        # the width and height of the board using arguments to this function.
        #
        # This function returns the newly-created state.
        pass
                                 
    
    # def step_generator(self):
    #     yield None
    #     pass
    #
    # Do you want to use a step generator as your step function? If so, you may
    # uncomment the above and fill it in, and it will be used instead of the
    # normal step function.
    # 
    # A step generator is similar to a regular step function: it takes a
    # starting state, and computes the next state. But it doesn't `return` it,
    # it `yield`s it. And then it doesn't exit, it just keeps on crunching and
    # yielding more states one by one.
    # 
    # A step generator is useful when you want to set up some environment and/or
    # variables when you do your crunching. It can help you save resources,
    # because you won't have to do all that initialization every time garlicsim
    # computes a step.
    #
    # (You may write your step generator to terminate at some point or to never
    # terminate-- Both ways are handled by garlicsim.)
    
    
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
        
        """
        return '<%s of level %s with %s cells at %s>' % \
               (
                   misc_tools.shorten_class_address(
                       self.__class__.__module__,
                       self.__class__.__name__
                   ),
                   self.level,
                   self.length ** 2,
                   hex(id(self))
               )
        """
    

    
class QuadBoard(Board):

    @staticmethod
    def create_root(level):
        pass#tododoc
    
    @staticmethod
    def create_messy_root(level):
        if level == 0:
            return random.choice([True, False])
        else:
            return QuadBoard(
                tuple(
                    QuadBoard.create_messy_root(level - 1) for i in range(4)
                )
            )
            
    
    def __init__(self, kids):
        assert isinstance(kids, tuple) # Important for caching
        assert len(kids) == 4
        self.kids = kids
        
        if (True in kids) or (False in kids):
            assert all(isinstance(kid, bool) for kid in kids)
            self.level = 1
            
        else:
            self.level = level = kids[0].level + 1
        
            if level >= 2:
                
                self.sub_quad_board = QuadBoard((
                    kids[0].kids[3],
                    kids[1].kids[2],
                    kids[2].kids[1],
                    kids[3].kids[0]
                ))
                
                if level >= 3:
                    
                    self.extended_kids = (
                        
                        kids[0],
                        
                        QuadBoard((
                            kids[0].kids[1],
                            kids[1].kids[0],
                            kids[0].kids[3],
                            kids[1].kids[2]
                        )),
                        
                        kids[1],
                        
                        QuadBoard((
                            kids[0].kids[2],
                            kids[0].kids[3],
                            kids[2].kids[0],
                            kids[2].kids[1]
                            )),
                        
                        self.sub_quad_board,
                        
                        QuadBoard((
                            kids[1].kids[2],
                            kids[1].kids[3],
                            kids[3].kids[0],
                            kids[3].kids[1]
                            )),
                        
                        kids[2],
                        
                        QuadBoard((
                            kids[2].kids[1],
                            kids[3].kids[0],
                            kids[2].kids[3],
                            kids[3].kids[2]
                            )),
                        
                        kids[3]
                        
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

    @caching.cache
    def is_empty(self):
        if self.level == 1:
            return all((kid is False for kid in self.kids))
        else: # self.level >= 2
            return all((kid.is_empty() for kid in self.kids))
        
    @caching.cache    
    def get_next(self):
        if self.level <= 1:
            raise NotEnoughInformation
        border_grand_kids = [self.kids[i].kids[j] for (i, j) in 
                             cute_iter_tools.product(xrange(4), xrange(4))
                             if i + j != 3]
        if not all((border_grand_kid.is_empty() for border_grand_kid
                    in border_grand_kids)):
            
            raise NotEnoughInformation
        
        next_sub_quad_board = self.get_future_sub_quad_board(1)
        
        raise NotImplementedError
        
    @caching.cache
    def get_future_sub_tri_board(self, n):
        assert self.level >= 3
        assert 0 <= n <= 2 ** (self.level - 3)
        return TriBoard(
            tuple(
                extended_kid.get_future_sub_quad_board(n) for extended_kid
                in self.extended_kids
            )
        )
    
            
    @caching.cache
    def get_future_sub_quad_board(self, n):
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
        new_kids = []
        for x in (1, 2):
            for y in (1, 2):
                true_neighbor_count = 0
                for i in (-1, 0, 1):
                    for j in (-1, 0, 1):
                        if i == j == 0:
                            continue
                        true_neighbor_count += self.get(x + i, y + j)
                
                if self.get(x, y) is True:
                    if 2 <= true_neighbor_count <= 3:
                        new_kids.append(True)
                    else:
                        new_kids.append(False)
                else: # self.get(x, y) is False
                    if true_neighbor_count == 3:
                        new_kids.append(True)
                    else:
                        new_kids.append(False)
        return QuadBoard(tuple(new_kids))
                        
    

class TriBoard(Board):

    @staticmethod
    def create_from_parents(parents):
        return TriBoard(tuple(parent.sub_quad_board for parent in parents))
    
    def __init__(self, kids):
        assert isinstance(kids, tuple) # Important for caching
        assert len(kids) == 9
        self.kids = kids
        
        assert all(isinstance(kid, QuadBoard) for kid in kids)            
        
        self.level = level = kids[0].level + 1.5
        # It's actually 1.5849625007211, but who's counting.
        
        assert self.level >= 2.5
        
        self.length = 3 * (2 ** int(self.level - 1))
        
        self.sub_quad_board = QuadBoard((
            QuadBoard((
                kids[0].kids[3],
                kids[1].kids[2],
                kids[3].kids[1],
                kids[4].kids[0]
                )),
            QuadBoard((
                kids[1].kids[3],
                kids[2].kids[2],
                kids[4].kids[1],
                kids[5].kids[0]
                )),
            QuadBoard((
                kids[3].kids[3],
                kids[4].kids[2],
                kids[6].kids[1],
                kids[7].kids[0]
                )),
            QuadBoard((
                kids[4].kids[3],
                kids[5].kids[2],
                kids[7].kids[1],
                kids[8].kids[0]
                ))
        ))
        
        self.bloated_kids = (
                        
                        QuadBoard((
                            kids[0],
                            kids[1],
                            kids[3],
                            kids[4]
                        )),
                        
                        QuadBoard((
                            kids[1],
                            kids[2],
                            kids[4],
                            kids[5]
                        )),
                        
                        QuadBoard((
                            kids[3],
                            kids[4],
                            kids[6],
                            kids[7]
                        )),
                        
                        QuadBoard((
                            kids[4],
                            kids[5],
                            kids[7],
                            kids[8]
                        )),
                        
                    )
        
    
    def get(self, x, y):
        x_div, x_mod = divmod(x, self.length // 3)
        y_div, y_mod = divmod(y, self.length // 3)
        kid = self.kids[x_div + 3 * y_div]
        return kid.get(x_mod, y_mod)
    
            
    @caching.cache
    def get_future_sub_quad_board(self, n):
        assert 0 <= n <= 2 ** (self.level - 2.5)
        return QuadBoard(
            tuple(
                bloated_kid.get_future_sub_quad_board(n) for bloated_kid
                in self.bloated_kids
            )
        )
            
    
if __name__ == '__main__':
    board = QuadBoard.create_messy_root(6)
    assert board.get_future_sub_quad_board(0) == board.sub_quad_board
    junk = board.get_future_sub_quad_board(2)
    1+1