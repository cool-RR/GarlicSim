# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `HueSelectionDialog` class.

See its documentation for more details.
'''

# todo: should have validation in `Textual`, currently can enter words

from __future__ import division
from __future__ import with_statement

import wx

from garlicsim.general_misc import freezers
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel
from garlicsim.general_misc.context_managers import ReentrantContextManager




        

import wx

from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel


class Textual(wx.Panel):
    '''Display (and allow modifying) the hue as a number 0-359.'''
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 100))
        
        self.hue_selection_dialog = hue_selection_dialog
        #self.hue = hue_selection_dialog.hue
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.hue_static_text = wx.StaticText(self, label='&Hue:')
        
        self.main_v_sizer.Add(self.hue_static_text, 0,
                              wx.ALIGN_LEFT | wx.BOTTOM, border=5)
        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.h_sizer, 0)
        
        self.spin_ctrl = wx.SpinCtrl(self, min=0, max=359,
                                     initial=77,
                                     size=(70, -1), style=wx.SP_WRAP)
        #if wx_tools.is_mac:
            #self.spin_ctrl.SetValue(ratio_to_round_degrees(self.hue))
        
        self.h_sizer.Add(self.spin_ctrl, 0)
        
        self.degree_static_text = wx.StaticText(self, label=unichr(176))
        
        self.h_sizer.Add(self.degree_static_text, 0)
        
        self.SetSizerAndFit(self.main_v_sizer)
        
        self.Bind(wx.EVT_SPINCTRL, self._on_spin, source=self.spin_ctrl)
        self.Bind(wx.EVT_TEXT, self._on_text, source=self.spin_ctrl)
        #self.Bind(wx.EVT_KILL_FOCUS, self._on_kill_focue)
        
        
    value_freezer = freezers.FreezerProperty()
                    
        
    def update(self):
        '''Update to show the new hue.'''
        if not self.value_freezer.frozen and \
           self.hue != self.hue_selection_dialog.hue:
            self.hue = self.hue_selection_dialog.hue
            self.spin_ctrl.SetValue(ratio_to_round_degrees(self.hue))
    

            
    def _on_spin(self, event):
        self.hue_selection_dialog.setter(
            degrees_to_ratio(self.spin_ctrl.Value)
        )

        
    def _on_text(self, event):
        with self.value_freezer:
            self.hue_selection_dialog.setter(
                degrees_to_ratio(self.spin_ctrl.Value)
            )

            
    #def _on_kill_focus(self, event):
        #assert not self.value_freezer.frozen

            
    def set_focus_on_spin_ctrl_and_select_all(self):
        '''
        
        
        The "select all" part works only on Windows and generic `wx.SpinCtrl`
        implementations.
        '''
        self.spin_ctrl.SetFocus()
        self.spin_ctrl.SetSelection(-1, -1)



class Comparer(CutePanel):
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
        self.Bind(wx.EVT_SET_FOCUS, self._on_set_focus)
        self.Bind(wx.EVT_KILL_FOCUS, self._on_kill_focus)
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
            
            
    def _on_set_focus(self, event):
        event.Skip()
        self.Refresh()
        

    def _on_kill_focus(self, event):
        event.Skip()
        self.Refresh()
                
        
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
            


