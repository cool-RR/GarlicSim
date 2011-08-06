import random

import numpy.random
import garlicsim.data_structures
from garlicsim.general_misc import cute_iter_tools

SIZE = 20 # blocktodo: kill

# blocktodo: should probably have acceleration changing from nearby water.

class State(garlicsim.data_structures.State):
    
    
    def __init__(self, heights=numpy.zeros((SIZE, SIZE)),
                       velocities=None,
                       accelerations=None):
        self.heights = heights
        self.velocities = velocities if velocities is not None else \
                                                     numpy.zeros(heights.shape)
        self.accelerations = accelerations if accelerations is not None else \
                                                     numpy.zeros(heights.shape)
    
    
    def step(self, t=1):
        width, length = self.heights.shape
        new_accelerations = numpy.zeros((width, length))
        new_velocities = numpy.zeros((width, length))
        new_heights = numpy.zeros((width, length))
        
        for (x, y), height in numpy.ndenumerate(self.heights):
            
            neighbors = []
            for i, j in cute_iter_tools.product((-1, 0, -1), (-1, 0, -1)):
                if i == j == 0:
                    continue
                distance = (i**2 + j**2) ** 0.5
                weight = 1 / distance
                value = self.heights[x + i, y + j]
                neighbors.append((value, weight))
                
            values, weights = zip(*neighbors)
            expected_height = numpy.average(values, weights=weights)
                
            new_acceleration = 0.02 * (expected_height - height)
            if new_acceleration in (numpy.inf, -numpy.inf, numpy.nan):
                raise garlicsim.misc.WorldEnded
            new_velocity = self.velocities[x, y] + t * new_acceleration
            new_height = self.heights[x, y] + t * new_velocity
            
            new_accelerations[x, y] = new_acceleration
            new_velocities[x, y] = new_velocity
            new_heights[x, y] = new_height
            
                
        return State(new_heights,
                     new_velocities,
                     new_accelerations)
        

    
    @staticmethod
    def create_messy_root():
        return State(
            heights=numpy.random.random((SIZE, SIZE))
        )
                                 
    