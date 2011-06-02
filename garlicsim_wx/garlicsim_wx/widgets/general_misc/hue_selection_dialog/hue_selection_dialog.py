# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


from __future__ import with_statement

import wx

from garlicsim_wx.general_misc import wx_tools


class Textual(wx.Panel):
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 100))
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.hue_static_text = wx.StaticText(self, label='&Hue:')
        
        self.main_v_sizer.Add(self.hue_static_text, 0,
                              wx.ALIGN_LEFT | wx.BOTTOM, border=5)
        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.h_sizer, 0)
        
        self.spin_ctrl = wx.SpinCtrl(self, min=0, max=359,
                                     initial=77,
                                     size=(70, -1), style=wx.SP_WRAP)
        
        self.h_sizer.Add(self.spin_ctrl, 0)
        
        self.SetSizerAndFit(self.main_v_sizer)
        
        

class Comparer(wx.Panel):
    '''Shows the new hue compared to the old hue before dialog was started.'''
    def __init__(self, hue_selection_dialog):
        style = wx.TAB_TRAVERSAL | (wx.SIMPLE_BORDER if wx_tools.is_gtk
                                    else wx.SUNKEN_BORDER)
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 90),
                          style=style)
        self._transparent_pen = \
            wx.Pen(wx.Colour(0, 0, 0), width=0, style=wx.TRANSPARENT)
        
        self.SetCursor(wx.StockCursor(wx.CURSOR_BULLSEYE))
        
        self.Bind(wx.EVT_LEFT_DOWN, self._on_mouse_left_down)
        self.Bind(wx.EVT_CHAR, self._on_char)
        
    
                
    
    def _on_mouse_left_down(self, event):
        x, y = event.GetPosition()
        width, height = self.GetClientSize()
        if y >= height // 2:
            self.change_to_old_hue()
            
    def _on_char(self, event):
        char = unichr(event.GetUniChar())
        if char == ' ':
            self.change_to_old_hue()
        else:
            event.Skip()
            
                
        
class HueSelectionDialog(wx.Dialog):
    '''Dialog for changing a hue.'''
    
    def __init__(self, parent, getter, setter, emitter, lightness=1,
                 saturation=1, id=-1, title='Select hue',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_DIALOG_STYLE, name=wx.DialogNameStr):

        
        wx.Dialog.__init__(self, parent, id, title, pos, size, style, name)
        
        

        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_v_sizer.Add(self.h_sizer, 0)
        
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)        
        self.h_sizer.Add(self.v_sizer, 0, wx.ALIGN_CENTER)
        self.comparer = Comparer(self)
        self.v_sizer.Add(self.comparer, 0, wx.RIGHT | wx.TOP | wx.BOTTOM,
                         border=10)
        
        self.textual = Textual(self)
        self.v_sizer.Add(self.textual, 0, wx.RIGHT | wx.TOP | wx.BOTTOM,
                         border=10)
                

        self.SetSizer(self.main_v_sizer)
        self.main_v_sizer.Fit(self)
            


