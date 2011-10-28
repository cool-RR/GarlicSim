import itertools
import math
import operator_module
import abc

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import caching
from garlicsim.general_misc import nifty_collections


big_map = {}

class AbstractCachedType(caching.CachedType, abc.ABCMeta):
    pass
        

class Combination(object):
    ''' '''
    __metaclass__ = AbstractCachedType
    
    @abc.abstractmethod
    def __int__(self):
        ''' '''
    
    @abc.abstractproperty
    def level(self):
        ''' '''
    
    @abc.abstractmethod
    def get_child_sequences_for_sequence(self, sequence):
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
    
    @caching.cache
    @nifty_collections.LazyTuple.factory
    @classmethod
    def get_child_sequences_for_sequence(cls, sequence):
        ''' '''
        if len(sequence) <= 1:
            raise StopIteration
        for i in range(len(sequence) - 1):
            left_segment = sequence.members[:i]
            our_pair = sequence.members[i:i+2]
            right_segment = sequence.members[i+2:]
            child_sequence = Sequence(
                left_segment + cls(*our_pair) + right_segment
            )
            yield child_sequence
        
        
    
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
    
    @caching.CachedProperty
    def has_maximal_bloat(self):
        ''' '''
        return isinstance(self, UnaryCombination) and \
               isinstance(self.member, UnaryCombination) and \
               isinstance(self.member.member, UnaryCombination)
    
    
    @caching.cache
    @nifty_collections.LazyTuple.factory
    @classmethod
    def get_child_sequences_for_sequence(cls, sequence):
        ''' '''
        if len(sequence) == 0:
            raise StopIteration
        for i in range(len(sequence)):
            left_segment = sequence.members[:i]
            our_member = sequence.members[i]
            right_segment = sequence.members[i+1:]
            if isinstance(our_member, UnaryCombination):
                if our_member.has_maximal_bloat:
                    continue
            child_sequence = Sequence(
                left_segment + cls(our_member) + right_segment
            )
            yield child_sequence
    

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
   
    def __len__(self):
        return len(self.members)
    
    @caching.CachedProperty
    @nifty_collections.LazyTuple.factory
    def child_sequences(self):
        for operator in operators:
            for child_sequence in \
                               operator.get_child_sequences_for_sequence(self):
                yield child_sequence
    
            
    @caching.CachedProperty
    def value(self):
        if len(self.members) != 1:
            return None
        (member,) = self.members
        return int(member)


    @caching.CachedProperty
    def has_value(self):
        return self.value is not None

        

def solve(n):
    ''' '''
    for i in itertools.count(2):
        numbers = range(1, i)
        
        
1/0