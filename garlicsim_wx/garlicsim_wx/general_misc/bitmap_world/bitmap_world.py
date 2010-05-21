# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import wx

from garlicsim_wx.general_misc import wx_tools

class BitmapEntry(object):
    def __init__(self, bitmap, position_or_rect):
        
        self.bitmap = bitmap
        if isinstance(position_or_rect, wx.Rect):
            self.rect = position_or_rect
        else:
            assert len(position_or_rect) == 2
            position = position_or_rect
            self.rect = wx.Rect(
                position[0],
                position[1],
                *bitmap.GetSize()
            )
        
        
    

class BitmapWorld(object):
    def __init__(self, render_function):
        self.bitmap_entries = []
        self.render_function = render_function
    
    def add_bitmap(self, bitmap, position_or_rect):
        self.bitmap_entries.append(
            BitmapEntry(bitmap, position_or_rect)
        )
        
    def remove_bitmap(self, bitmap_or_bitmap_entry):
        if isinstance(bitmap_or_bitmap_entry, wx.Bitmap):
            bitmap = bitmap_or_bitmap_entry
            matches = [entry for entry in self.bitmap_entries if 
                       entry.bitmap is bitmap]
            
            if len(matches) == 0:
                raise LookupError
            if len(matches) >= 2:
                raise Exception(
                    'Bitmap appears twice, must specify by bitmap entry'
                )
            
            (bitmap_entry,) =  matches
        else:
            bitmap_entry = bitmap_or_bitmap_entry
            if bitmap_entry not in self.bitmap_entries:
                raise LookupError
        
        self.bitmap_entries.remove(bitmap_entry)
        
    
    def _get_existing_region(self):
        region = wx.Region()
        for bitmap_entry in self.bitmap_entries:
            region.Union(
                *(
                    bitmap_entry.position + tuple(bitmap_entry.bitmap.GetSize())
                )
            )
        return region
    
    
    def draw_rect_bitmap_to_dc(self, rect, dc):
        
        assert isinstance(dc, wx.DC)
        
        wanted_rect = rect
        
        needed_region_that_isnt_rendered_yet = \
            wx.Region(*wanted_rect).SubtractRegion(self._get_existing_region())
                
        for rect in wx_tools.iter_rects_of_region(
            needed_region_that_isnt_rendered_yet
            ):
            
            bitmap = self.render_function(rect)
            self.add_bitmap(bitmap, rect)
            
        # Okay, now we have all the needed bitmaps for this rect. Time to draw
        # it on the DC.
        
        region = wx.Region(*wanted_rect)
        
        x, y, w, h = wanted_rect
        
        
            