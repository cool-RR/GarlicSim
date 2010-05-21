
import random
import itertools
import copy

from garlicsim.general_misc.third_party import abc
from garlicsim.general_misc import caching
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import misc_tools

import garlicsim.data_structures

from cute_life import World


class State(garlicsim.data_structures.State):
    
    def __init__(self, world=None):
        garlicsim.data_structures.State.__init__(self)
        self.world = world or World()
    
    """
    @staticmethod
    def create_diehard(width=45, height=25):
        state = State()
        state.BaseBoard = BaseBoard.create_diehard(width, height)
        return state
    """
    
    @staticmethod
    def create_root():
        return State()
    
    
    @staticmethod
    def create_messy_root(length=40):
        return State(World.create_messy(length))
    
    
    @staticmethod
    def create_glider():
        return State(World.create_glider())
    
    
    def step(self):
        new_state = copy.deepcopy(self, garlicsim.misc.StepCopy())
        new_state.clock += 1
        new_state.world.step()
        return new_state

    
    def __repr__(self):
        return self.world.__repr__()
    
    
    def __eq__(self, other):
        return isinstance(other, State) and self.world == other.world

    
    def __ne__(self, other):
        return not self.__eq__(other)

    