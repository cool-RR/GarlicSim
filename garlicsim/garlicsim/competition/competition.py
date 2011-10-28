import itertools
import math
import operator_module
import abc

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import caching
from garlicsim.general_misc import nifty_collections


big_map = {}



class Combination(object):
    ''' '''
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __int__(self):
        ''' '''
    
    @abc.abstractproperty
    def level(self):
        ''' '''
    

class BinaryCombination(Combination):
    ''' '''
    def __init__(self, left_member, right_member):
        ''' '''
        assert isinstance(left_member, (Combination, int))
        assert isinstance(right_member, (Combination, int))
        self.left_member = left_member
        self.right_member = right_member
    
    def __int__(self):
        ''' '''
        return self.operation(int(self.left_member), int(self.right_member))
    
    @caching.CachedProperty
    def level(self):
        ''' '''
        level_of_left_member = self.left_member if \
                  isinstance(self.left_member, int) else self.left_member.level
        level_of_right_member = self.right_member if \
                isinstance(self.right_member, int) else self.right_member.level
        return max((level_of_left_member, level_of_right_member))
        

class UnaryCombination(Combination):
    ''' '''
    def __init__(self, member):
        ''' '''
        assert isinstance(member, (Combination, int))
        self.member = member
    
    def __int__(self):
        ''' '''
        return self.operation(int(self.member))
    

class Add(BinaryCombination): operation = operator_module.add
class Sub(BinaryCombination): operation = operator_module.sub
class Mul(BinaryCombination): operation = operator_module.mul
class Div(BinaryCombination): operation = operator_module.floordiv
class Exp(BinaryCombination): operation = operator_module.pow
class Fac(UnaryCombination): operation = math.factorial

operators = (Add, Sub, Mul, Div, Exp, Fac)        
        
class Sequence(object):
    ''' '''
    def __init__(self, members=()):
        self.members = members
        
    @nifty_collections.LazyTuple.factory
    def child_sequences(self):
        for operator_module in operators
        


        

def solve(n):
    ''' '''
    for i in itertools.count(2):
        numbers = range(1, i)
        
        
1/0