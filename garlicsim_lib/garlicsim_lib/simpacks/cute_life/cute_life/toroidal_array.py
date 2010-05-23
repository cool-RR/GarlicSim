import array

class ToroidalArray(object):
    
    def __init__(self, width, height, initializer):
        self.width = width
        self.height = height
        if initializer is None:
            initializer = (0 for i in xrange(width * height))
        self._array = array.array(
            'H',
            initializer
        )
    
        
    def get(self, x, y):
        xx = x % self.width
        yy = y % self.height
        return self._array[(xx % self.width) * self.height + (yy % self.height)]

    def set(self, x, y, value):
        xx = x % self.width
        yy = y % self.height
        self._array[(x % self.width) * self.height + (y % self.height)] = value
        