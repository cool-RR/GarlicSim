import random

import numpy.random

import garlicsim.data_structures

SIZE = 50 # blocktodo: kill

class State(garlicsim.data_structures.State):
    
    
    def __init__(self, heights=numpy.zeros((SIZE, SIZE))):
        self.heights = heights
        
    
    
    def step(self):
        width, length = self.heights.shape
        new_heights = numpy.zeros((width, length))
        
        for i in xrange(width):
            for j in xrange(length):
                new_heights[i, j] = 0.8 * self.heights + 0.2 * random()
                
        return State(new_heights)
        

    
    @staticmethod
    def create_messy_root():
        return State(
            heights=numpy.random.random((SIZE, SIZE))
        )
                                 
    