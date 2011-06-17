# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `BindSavvyWindow` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim.general_misc import caching

from .bind_savvy_window_type import BindSavvyWindowType


class BindSavvyWindow(wx.Window):
    '''
    Window type that allows binding events automatically by method name.
    
    Use `bind_event_handlers` 
    
    Some of this class's functionality is in its metaclass; see documentation
    of `BindSavvyWindowType`'s methods and attributes for more details.
    '''
    
    __metaclass__ = BindSavvyWindowType
    
    
    def bind_event_handers(self, cls):
        '''
        Look for event-handling methods on `cls` and bind events to them.
        
        For example, a method with a name of `_on_key_down` will be bound to
        `wx.EVT_KEY_DOWN`, while a method with a name of `_on_ok_button` will
        be bound to a `wx.EVT_BUTTON` event sent from `self.ok_button`.
        
        `cls` should usually be 
        '''
        if not isinstance(self, cls):
            raise Exception('blocktododoc')
        event_handler_grokkers = \
            cls._BindSavvyWindowType__event_handler_grokkers
        for event_handler_grokker in event_handler_grokkers:
            event_handler_grokker.bind(self)
        
        