
from garlicsim.general_misc.third_party import abc
from garlicsim.general_misc import caching

import garlicsim

        
class NotEnoughInformation(garlicsim.misc.SmartException):
    pass


class CachedAbstractType(caching.CachedType, abc.ABCMeta):
    pass
