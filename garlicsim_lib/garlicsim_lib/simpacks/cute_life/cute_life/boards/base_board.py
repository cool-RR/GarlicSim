
import random
import itertools

from garlicsim.general_misc.third_party import abc
from garlicsim.general_misc import caching
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import misc_tools

import garlicsim

from .misc import CachedAbstractType, NotEnoughInformation


class BaseBoard(garlicsim.misc.CrossProcessPersistent):
    # tododoc: need to think what happens to these on pickling/unpickling
    __metaclass__ = CachedAbstractType
    
    @abc.abstractmethod
    def get(self, x, y):
        pass
    
    
    def __iter__(self):
        length = self.length
        coordinate_pairs = (reversed(divmod(i, length)) for i
                            in xrange(length ** 2))
        for coordinate_pair in coordinate_pairs:
            yield self.get(*coordinate_pair)
            
    def __repr__(self):
        '''Display the BaseBoard, ASCII-art style.'''
        repr_cell = lambda x, y: '#' if self.get(x, y) is True else ' '
        repr_row = lambda y: ''.join(repr_cell(x, y) for x in xrange(self.length))
        return '\n'.join(repr_row(y) for y in xrange(self.length))
        
    
    def __eq__(self, other):
        return self is other
        #if not isinstance(other, BaseBoard):
            #return NotImplemented
        #return self.length == other.length and \
               #all((x == y for (x, y) in itertools.izip(self.kids, other.kids)))

    
    def __ne__(self, other):
        return not (self is other)
    
    
