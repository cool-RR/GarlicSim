import random

import numpy.random
import garlicsim.data_structures
from garlicsim.general_misc import cute_iter_tools

SIZE = 10 # blocktodo: kill

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
        
        for i, j in cute_iter_tools.product(xrange(1, width - 1),
                                            xrange(1, length - 1)):
            neighbors = []
            for ii, jj in cute_iter_tools.product((-1, 0, -1), (-1, 0, -1)):
                if ii == jj == 0:
                    continue
                distance = (ii**2 + jj**2) ** 0.5
                weight = 1 / distance
                value = self.heights[i + ii, j + jj]
                neighbors.append((value, weight))
                
            values, weights = zip(*neighbors)
            total_weight = sum(weights)
            expected_height = numpy.average(values, weights=weights)
                
            new_acceleration = 0.2 * (expected_height - self.heights[i, j])**2
            if new_acceleration in (numpy.inf, -numpy.inf, numpy.nan):
                raise garlicsim.misc.WorldEnded
                1/0
            new_velocity = self.velocities[i, j] + t * new_acceleration
            new_height = self.heights[i, j] + t * new_velocity
            
            new_accelerations[i, j] = new_acceleration
            new_velocities[i, j] = new_velocity
            new_heights[i, j] = new_height
            
                
        return State(new_heights,
                     new_velocities,
                     new_accelerations)
        

    
    @staticmethod
    def create_messy_root():
        return State(
            heights=numpy.random.random((SIZE, SIZE))
        )
                                 
    