# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines the BoardViewer class.'''

from __future__ import division

import random #tododoc: kill at end if unused
import cProfile #tododoc: kill at end if unused

import wx
from wx.lib import wxcairo

from garlicsim.general_misc import math_tools
from garlicsim_wx.general_misc import wx_tools

import garlicsim_wx



class BoardViewer(wx.Panel, # Rename to WorldViewer
                  garlicsim_wx.widgets.WorkspaceWidget):
    '''Widget for displaying a Life board.'''
    def __init__(self, frame):
              
        wx.Panel.__init__(self, frame, style=wx.SUNKEN_BORDER)
        
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)

        self.border_width = 1
        self.minimum_size_for_border = 4
        self.zoom = 7
        
        self.position = (0.0, 0.0) # In world coords, tuple of floats.
        # The center of the panel.
        
        self.state = None
        
        self._buffer_bitmap = wx.EmptyBitmap(1, 1)
        
        self.gui_project.active_node_changed_emitter.add_output(
            lambda: self.set_state(self.gui_project.get_active_state())
        )

        self.redraw_needed_flag = True
        

        
    def unscreenify(self, x, y):
        '''Translate screen coordinates to board coordinates.'''
        if self.board is None:
            return None
        screen_tuple = self.CalcUnscrolledPosition(x, y)
        result = [(thing // (self.border_width + self.square_size)) for
                  thing in screen_tuple]
        if (0 <= result[0] < self.board.length) and \
           (0 <= result[1] < self.board.length):
            return tuple(result)
        else:
            return None

    
        
        
    def _screen_coords_to_absolute_pixel_coords(self, x, y):
        top_left_corner_abs_x, top_left_corner_abs_y = \
            self._get_absolute_pixel_coords_of_top_left_corner()
        return (
            x + top_left_corner_abs_x,
            y + top_left_corner_abs_y
        )


    
    def _absolute_pixel_coords_to_world_coords(self, x, y):
        return (x / self.zoom, -y / self.zoom)
    
    
    def _absolute_pixel_coords_to_world_coords_int(self, x, y, round_up=False):
        float_result = self._absolute_pixel_coords_to_world_coords(x, y)
        return (
            math_tools.round_to_int(float_result[0], up=round_up),
            math_tools.round_to_int(float_result[1], up=round_up)
        )

    
    def _world_coords_to_absolute_pixel_coords(self, x, y):
        return (x * self.zoom, -y * self.zoom)
    
    
    def _absolute_pixel_coords_to_screen_coords(self, x, y):
        top_left_corner_abs_x, top_left_corner_abs_y = \
            self._get_absolute_pixel_coords_of_top_left_corner()
        return (
            x - top_left_corner_abs_x,
            y - top_left_corner_abs_y
        )

    
    def _screen_coords_to_world_coords(self, x, y):
        return self._absolute_pixel_coords_to_world_coords(
            *self._screen_coords_to_absolute_pixel_coords(x, y)
        )
    
    
    def _screen_coords_to_world_coords_int(self, x, y, round_up=False):
        abs_x, abs_y = self._screen_coords_to_absolute_pixel_coords(x, y)
        return self._absolute_pixel_coords_to_world_coords_int(
            abs_x,
            abs_y,
            round_up=round_up
        )
    
    
    
    def _world_coords_to_screen_coords(self, x, y):
        return self._absolute_pixel_coords_to_screen_coords(
            *self._world_coords_to_absolute_pixel_coords(x, y)
        )
    
    
    def _get_absolute_pixel_coords_of_top_left_corner(self):
        center_abs_x, center_abs_y = \
            self._world_coords_to_absolute_pixel_coords(*self.position)
        size_x, size_y = self.GetClientSizeTuple()
        
        return (center_abs_x - size_x / 2,
                center_abs_y - size_y / 2)
    
    

    def _get_world_coordinates_of_bottom_left_corner_int(self): #rounded down
        size_x, size_y = self.GetClientSizeTuple()
        return self._absolute_pixel_coords_to_world_coords_int(
                self.position[0] - size_x / 2,
                self.position[1] + size_y / 2,
                round_up=False
            )
    
        

    def _get_world_coordinates_of_top_right_corner_int(self): #rounded up
        size_x, size_y = self.GetClientSizeTuple()
        return self._absolute_pixel_coords_to_world_coords_int(
                self.position[0] + size_x / 2,
                self.position[1] - size_y / 2,
                round_up=True
            )
    
    
        
    def set_state(self, state):
        '''Set the state to be displayed.'''
        self.state = state
        self.redraw_needed_flag = True
        self.Refresh()

        
    def set_zoom(self, zoom):
        self.zoom = zoom if zoom <= 1 else int(round(zoom))
        self.redraw_needed_flag = True
        self.Refresh()
        
        
    def set_position(self, position):
        self.position = position
        self.redraw_needed_flag = True
        self.Refresh()
        
    """
    def _get_size_from_board(self):
        '''
        Get the size the widget should be by inspecting the size of the board.
        '''
        if self.board:
            length = self.board.length * (self.square_size + self.border_width)
            return (length, length)
        else:
            return (1, 1)
    """
        
    def _draw_buffer_bitmap(self):
        '''Draw the buffer bitmap, which `on_paint` will draw to the screen.'''
        
        if self.state is None:
            return
        
        world = self.state.world
        
        self._buffer_bitmap = wx.EmptyBitmap(*self.GetClientSize())
        
        dc = wx.MemoryDC(self._buffer_bitmap)
        context = wxcairo.ContextFromDC(dc)
        
        
        bl_x, bl_y = self._get_world_coordinates_of_bottom_left_corner_int()
        tr_x, tr_y = self._get_world_coordinates_of_top_right_corner_int()
    
        context.set_source_rgb(1, 1, 1)
        context.paint()
        
        context.set_source_rgb(0, 0, 0)
        
        for cell_x, cell_y in world.iter_cells(
            state=True, rectangle=(bl_x, bl_y, tr_x, tr_y)):
            
            cell_x_screen, cell_y_screen = self._world_coords_to_screen_coords(
                cell_x, cell_y)
            
            
            context.rectangle(cell_x_screen, cell_y_screen, self.zoom, self.zoom)
            
        context.fill()

        
        
        dc.Destroy()
        
    def on_paint(self, event):
        '''Paint event handler.'''
        
        event.Skip()
        
        if self.redraw_needed_flag is True:
            self._draw_buffer_bitmap()#cProfile.runctx('self._draw_buffer_bitmap()', globals(), locals())
            self.redraw_needed_flag = False
                
        dc = wx.BufferedPaintDC(self)
        
        dc.SetBackground(wx.Brush('white'))
        dc.Clear()
        
        dc.DrawBitmapPoint(self._buffer_bitmap, (0, 0))
        
        dc.Destroy()
        
        
        
    def on_size(self, event):
        '''EVT_SIZE handler.'''
        event.Skip()
        self.redraw_needed_flag = True
        self.Refresh()
            

    def on_mouse_event(self, event):
        '''Mouse event handler.'''
        
        if event.LeftDown():
            pos = event.GetPositionTuple()
            thing = self.unscreenify(*pos)
            if thing is not None:
                (x, y) = thing
                old_value = self.board.get(x,y)
                new_value = (not old_value)

                new_state = self.gui_project.editing_state()
                new_board = new_state.board.get_with_cell_change(x, y, new_value)
                new_state.board = self.board = new_board
            
                self.redraw_needed_flag = True


        self.Refresh()
