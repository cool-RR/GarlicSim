# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines the `StateViewer` class.'''
# blocktodo: ensure no life artifacts

from __future__ import division

import wx
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel
import garlicsim_wx


@caching.cache(max_size=500)
def _draw_bitmap(state_viewer, state, client_width, client_length):
    
    client_width, client_length = state_viewer.ClientSize
    bitmap = wx.EmptyBitmap(client_width, client_length)
    
    dc = wx.MemoryDC(bitmap)
    
    dc.SetPen(wx.TRANSPARENT_PEN)
    
    if state is None:
        return bitmap
    
    rectangle_width = client_width / state.heights.shape[0]
    rectangle_length = client_length / state.heights.shape[1]
            
    rectangles = []
    brushes = []
    
    for x, y in cute_iter_tools.product(*map(xrange, state.heights.shape)):
        
        ### Calculating rectangle coordinates: ################################
        #                                                                     #
        
        rectangles.append([rectangle_width * x,
                           rectangle_length * y,
                           rectangle_width,
                           rectangle_length])
        #                                                                     #
        ### Finished calculating rectangle coordinates. #######################
        
        ### Calculating color for brush: ######################################
        #                                                                     #
        height = state.heights[x, y]
        truncated_height = \
                         1 if height > 1 else -1 if height < -1 else height
        big_luminosity = 128 + (truncated_height * 127)
        brush = wx.Brush(wx.Color(big_luminosity,
                                  big_luminosity,
                                  big_luminosity))
        brushes.append(brush)
        #                                                                     #
        ### Finished calculating color for brush. #############################

    dc.DrawRectangleList(rectangles, wx.TRANSPARENT_PEN, brushes)
    
    return bitmap

    

class StateViewer(CutePanel,
                  garlicsim_wx.widgets.WorkspaceWidget):
    
    def __init__(self, frame):
              
        CutePanel.__init__(self, frame, style=wx.SUNKEN_BORDER)
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.state = None
        
        self._buffer_bitmap = wx.EmptyBitmap(1, 1)
        
        self.gui_project.active_node_changed_emitter.add_output(
            lambda: self.set_state(self.gui_project.get_active_state())
        )
        
        self.bind_event_handlers(StateViewer)
        
        
    def unscreenify(self, x, y):
        '''Translate screen coordinates to board coordinates.'''
        if self.board is None:
            return None
        screen_tuple = self.CalcUnscrolledPosition(x, y)
        result = [(thing // (self.border_width + self.square_size)) for
                  thing in screen_tuple]
        if (0 <= result[0] < self.board.width) and \
           (0 <= result[1] < self.board.height):
            return tuple(result)
        else:
            return None

        
    def set_state(self, state):
        '''Set the state to be displayed.'''
        self.state = state
        self.Refresh()

    
    ### Event handlers: #######################################################
    #                                                                         #
    
    def _on_paint(self, event):
        
        event.Skip()
                
        dc = wx.BufferedPaintDC(self)
        
        dc.SetBackground(wx_tools.colors.get_background_brush())
        dc.Clear()
        
        dc.DrawBitmapPoint(_draw_bitmap(self, self.state, *self.ClientSize),
                           self.ClientAreaOrigin)
        
                        
    def _on_size(self, event):
        self.Refresh()
        if event is not None:
            event.Skip()

    #                                                                         #
    ### Finished event handlers. ##############################################
