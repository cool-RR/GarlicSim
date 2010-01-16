#tododoc

import threading
import Queue
from garlicsim.general_misc import queue_tools


modules_to_import = Queue.Queue()

active_async_importer = None
'''tododoc'''

imported_modules = {}

class AsyncImporter(threading.Thread):
    
    def run(self):
        
        global imported_modules, modules_to_import
        
        for module_name in queue_tools.iterate(modules_to_import):
            
            imported_modules[module_name] = \
                __import__(module_name, fromlist=[''])
    
    is_alive = threading.Thread.isAlive
    '''Crutch for Python 2.5.'''


def async_import(modules):
    
    global active_async_importer, modules_to_import
    
    modules = [modules] if isinstance(modules, basestring) else modules
    
    for module in modules:
        modules_to_import.put(module)
    
    if (active_async_importer is None) or \
       (active_async_importer.is_alive() is False):
        
        active_async_importer = AsyncImporter()
        
        active_async_importer.start()
        
        
if __name__ == '__main__':
    import time
    async_import('wx')
    time.sleep(2)
    import wx