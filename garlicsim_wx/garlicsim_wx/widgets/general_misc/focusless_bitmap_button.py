# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import wx
from focusless_window import FocuslessWindowMixin

class FocuslessBitmapButton(wx.BitmapButton, FocuslessWindowMixin):
    def __init__(self, *args, **kwargs):
        wx.BitmapButton.__init__(self, *args, **kwargs)
        FocuslessWindowMixin.__init__(self, *args, **kwargs)