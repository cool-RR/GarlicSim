# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `CuteHtmlWindow` class.

See its documentation for more information.
'''

import webbrowser

import wx.html
import wx.webkit

from garlicsim_wx.widgets.general_misc.cute_window import CuteWindow


class CuteHtmlWindow(wx.webkit.WebKitCtrl, CuteWindow):

    event_modules = wx.html
    
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, 
                 size=wx.DefaultSize, style=0,
                 name=wx.webkit.WebKitNameStr):
        wx.webkit.WebKitCtrl.__init__(self, parent=parent)#, winID=id, pos=pos,
                                    #size=size, style=style, name=name)
        self.bind_event_handlers(CuteHtmlWindow)
        self.SetPage = self.SetPageSource
        
        
    def _on_html_link_clicked(self, event):
        webbrowser.open_new_tab(
            event.GetLinkInfo().GetHref()
        )