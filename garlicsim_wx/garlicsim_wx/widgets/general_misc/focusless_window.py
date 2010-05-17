# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.



import wx

class FocuslessWindowMixin(wx.Window):
    
    def __init__(self, *args, **kwargs):
        self.Bind(wx.EVT_SET_FOCUS, self.on_set_focus, self)
        
    def on_set_focus(self, event):
        #tododoc: sense for backwards like robin said?
        self.Navigate()