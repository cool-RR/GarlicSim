# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


import wx

class Textual(wx.Panel):
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 100))
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.hue_static_text = wx.StaticText(self, label='&Hue:')
        
        self.main_v_sizer.Add(self.hue_static_text)
        
        self.spin_ctrl = wx.SpinCtrl(self, min=0, max=359,
                                     initial=77,
                                     size=(70, -1), style=wx.SP_WRAP)
        
        self.main_v_sizer.Add(self.spin_ctrl)
        
        self.SetSizerAndFit(self.main_v_sizer)
        
        

class Comparer(wx.Panel):
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 90))
                            
        
class HueSelectionDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.comparer = Comparer(self)
        self.main_v_sizer.Add(self.comparer)
        
        self.textual = Textual(self)
        self.main_v_sizer.Add(self.textual)
                
        self.SetSizer(self.main_v_sizer)
        self.main_v_sizer.Fit(self)
            


app = wx.App()

HueSelectionDialog(None).Show()

app.MainLoop()
