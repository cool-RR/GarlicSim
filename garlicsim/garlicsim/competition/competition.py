import itertools
import math
import operator as operator_module
import abc

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import caching
from garlicsim.general_misc import nifty_collections


big_map = {}
_maximum_level_completed = 2

def _get_level(x):
    ''' '''
    return x if isinstance(x, int) else x.level
    

#class AbstractCachedType(caching.CachedType, abc.ABCMeta):
    #pass
        

class Combination(object):
    ''' '''
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __int__(self):
        ''' '''
    
    @abc.abstractproperty
    def level(self):
        ''' '''
    
    @abc.abstractmethod
    def get_child_sequences_for_sequence(self, sequence):
        ''' '''
    
    @abc.abstractmethod    
    def __repr__(self):
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
        raw = self.operation(int(self.left_member), int(self.right_member))
        if int(raw) == raw:
            return int(raw)
        else:
            raise ValueError
    
    @classmethod    
    @caching.cache()
    @nifty_collections.LazyTuple.factory
    def get_child_sequences_for_sequence(cls, sequence):
        ''' '''
        if len(sequence) <= 1:
            raise StopIteration
        for i in range(len(sequence) - 1):
            left_segment = sequence.members[:i]
            our_pair = sequence.members[i:i+2]
            right_segment = sequence.members[i+2:]
            child_sequence = Sequence(
                left_segment + (cls(*our_pair),) + right_segment
            )
            yield child_sequence
        
        
    
    @caching.CachedProperty
    def level(self):
        ''' '''
        level_of_left_member = _get_level(self.left_member)
        level_of_right_member = _get_level(self.right_member)
        return max((level_of_left_member, level_of_right_member))
    
    
    @caching.cache()
    def __repr__(self):
        return '(%s%s%s)' % \
                    (self.left_member, self.operator_string, self.right_member)
        

class UnaryCombination(Combination):
    ''' '''
    def __init__(self, member):
        ''' '''
        assert isinstance(member, (Combination, int))
        self.member = member
    
    def __int__(self):
        ''' '''
        if int(self.member) > 20:
            raise ValueError
        else:
            return int(self.operation(int(self.member)))
    
    @caching.CachedProperty
    def has_maximal_bloat(self):
        ''' '''
        return isinstance(self, UnaryCombination)# and \
               #isinstance(self.member, UnaryCombination)# and \
               #isinstance(self.member.member, UnaryCombination)
    
    
    @classmethod
    @caching.cache()
    @nifty_collections.LazyTuple.factory
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
                left_segment + (cls(our_member),) + right_segment
            )
            yield child_sequence
    
            
    @caching.CachedProperty
    def level(self):
        ''' '''
        return _get_level(self.member)
    
    @caching.cache()
    def __repr__(self):
        return '(%s)%s' % (self.member, self.operator_string)
    

class Add(BinaryCombination):
    operation = operator_module.add
    operator_string = '+'
    
class Sub(BinaryCombination):
    operation = operator_module.sub
    operator_string = '-'
    
class Mul(BinaryCombination):
    operation = operator_module.mul
    operator_string = '*'
    
class Div(BinaryCombination):    
    operation = operator_module.floordiv
    operator_string = '//'
    
class Pow(BinaryCombination):
    operation = operator_module.pow
    operator_string = '^'
    def __int__(self):
        ''' '''
        if int(self.right_member) > 20:
            raise ValueError
        else:
            return super(Pow, self).__int__()
    
class Fac(UnaryCombination):
    operation = math.factorial
    operator_string = '!'

operators = (Add, Sub, Mul, Div, Pow, Fac)
        
        
class Sequence(object):
    ''' '''
    def __init__(self, members=()):
        assert isinstance(members, tuple)        
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
    def level(self):
        return max(_get_level(member) for member in self.members)


    @caching.CachedProperty
    def has_value(self):
        try:
            return self.value is not None
        except (ZeroDivisionError, ValueError):
            return False
    
    def __repr__(self):
        #if len(self.members) != 1:
            #raise NotImplementedError
        return 'Sequence(%s)' % (self.members,)

        
def iterate_finished_sequences():
    for i in itertools.count(2):
        root_sequence = Sequence(tuple(range(1, i)))
        sequences_to_try = [root_sequence]
        while sequences_to_try:
            sequence = sequences_to_try.pop(0)
            if sequence.has_value:
                yield sequence
            else:
                sequences_to_try.extend(sequence.child_sequences)
    
finished_sequences_iterator = iterate_finished_sequences()


def solve(n):
    ''' '''
    if n in big_map:
        return big_map[n]
    for sequence in finished_sequences_iterator:
        possible_contender = big_map.get(sequence.value)
        if not possible_contender or possible_contender.level > sequence.level:
            big_map[sequence.value] = sequence
        if sequence.value == n:
            return sequence
                
                    
        
for i in itertools.count(2):
    print('Found solution for %s:\n    %s' % (i, solve(i)))
    
1/0