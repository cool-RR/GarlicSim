from __future__ import division

import itertools
import math
import colorsys

import wx

from garlicsim.general_misc import caching
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc import color_tools

BIG_LENGTH = 221
THICKNESS = 21
HALF_THICKNESS = THICKNESS / 2
AA_THICKNESS = 1.5
RADIUS = int((BIG_LENGTH / 2) - THICKNESS - 5)
SMALL_RADIUS = RADIUS - HALF_THICKNESS
BIG_RADIUS = RADIUS + HALF_THICKNESS

two_pi = math.pi * 2


@caching.cache
def make_bitmap(lightness=1, saturation=1):
    bitmap = wx.EmptyBitmap(BIG_LENGTH, BIG_LENGTH)
    assert isinstance(bitmap, wx.Bitmap)
    dc = wx.MemoryDC(bitmap)
    
    dc.SetBrush(wx_tools.get_background_brush())
    dc.SetPen(wx.TRANSPARENT_PEN)
    dc.DrawRectangle(-5, -5, BIG_LENGTH + 10, BIG_LENGTH + 10)
    
    center_x = center_y = BIG_LENGTH // 2 
    background_color_rgb = wx_tools.wx_color_to_rgb(
        wx_tools.get_background_color()
    )
    
    for x, y in itertools.product(xrange(BIG_LENGTH), xrange(BIG_LENGTH)):
        
        # This is a big loop so the code is optimized to keep it fast.
        
        rx, ry = (x - center_x), (y - center_y)
        distance = (rx ** 2 + ry ** 2) ** 0.5
        
        if (SMALL_RADIUS - AA_THICKNESS) <= distance <= \
           (BIG_RADIUS + AA_THICKNESS):
            
            angle = -math.atan2(rx, ry)
            hue = (angle + math.pi) / two_pi
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            
            if abs(distance - RADIUS) > HALF_THICKNESS:
                
                # This pixel requires some anti-aliasing.
                
                if distance < RADIUS:
                    aa_distance = SMALL_RADIUS - distance
                else: # distance > RADIUS
                    aa_distance = distance - BIG_RADIUS
                
                aa_ratio = aa_distance / AA_THICKNESS
                
                rgb = color_tools.mix_rgb(
                    aa_ratio,
                    background_color_rgb,
                    rgb
                )
                
            color = wx_tools.rgb_to_wx_color(rgb)
            pen = wx.Pen(color)
            dc.SetPen(pen)
            
            dc.DrawPoint(x, y)
        
    dc.Destroy()
    return bitmap


class Wheel(wx.Panel):
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog,
                          size=(BIG_LENGTH, BIG_LENGTH))
        self.SetDoubleBuffered(True)
        self.hue_selection_dialog = hue_selection_dialog
        self.hue = hue_selection_dialog.hue
        self.lightness = hue_selection_dialog.lightness # tododoc: needed?
        self.saturation = hue_selection_dialog.saturation # tododoc: needed?
        self.bitmap = make_bitmap(hue_selection_dialog.lightness,
                                  hue_selection_dialog.saturation)
        self._calculate_angle()
        self._pen = wx.Pen(wx.Color(255, 255, 255) if self.lightness < 0.5 \
                           else wx.Color(0, 0, 0),
                           width=2,
                           style=wx.DOT)
        self._cursor_set_to_bullseye = False
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)
        
    
    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
                    
        dc.DrawBitmap(self.bitmap, 0, 0)

        
        #######################################################################
        # Drawing dashed line which marks the selected color:
        
        gc = wx.GraphicsContext.Create(dc)
        assert isinstance(gc, wx.GraphicsContext)
        gc.SetPen(self._pen)
        cx, cy = BIG_LENGTH // 2, BIG_LENGTH // 2
        start_x, start_y = cx + SMALL_RADIUS * math.sin(self.angle), \
                           cy + SMALL_RADIUS * math.cos(self.angle)
        end_x, end_y = cx + BIG_RADIUS * math.sin(self.angle), \
                       cy + BIG_RADIUS * math.cos(self.angle)
        gc.StrokeLine(start_x, start_y, end_x, end_y)

        #dc.SetPen(self._pen)
        #dc.DrawLine(start_x, start_y, end_x, end_y)
                
        
        dc.Destroy()
        
        
    def on_mouse(self, event):
        
        center_x = center_y = BIG_LENGTH // 2 
        x, y = event.GetPosition()
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        inside_wheel = (SMALL_RADIUS <= distance <= BIG_RADIUS) # tododoc: doc

        
        if inside_wheel and not self._cursor_set_to_bullseye:
            
            self.SetCursor(wx.StockCursor(wx.CURSOR_BULLSEYE))
            self._cursor_set_to_bullseye = True
            
        elif not inside_wheel and not self.HasCapture() and \
             self._cursor_set_to_bullseye:
            
            self.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
            self._cursor_set_to_bullseye = False

            
        if event.LeftIsDown():
            
            if inside_wheel and not self.HasCapture():
                self.CaptureMouse()
                
            if self.HasCapture():
                angle = -math.atan2((x - center_x), (y - center_y))
                hue = (angle + math.pi) / (math.pi * 2)
                self.hue_selection_dialog.setter(hue)
                
            
        else: # Left mouse button is up
            if self.HasCapture():
                self.ReleaseMouse()
            
                
        
    def _calculate_angle(self):
        self.angle = - (2 * self.hue - 1) * math.pi
        
        
    def update(self):
        if self.hue != self.hue_selection_dialog.hue:
            self.hue = self.hue_selection_dialog.hue
            self._calculate_angle()
            self.Refresh()
            
        
        
    