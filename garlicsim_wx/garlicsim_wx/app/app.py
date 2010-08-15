# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the App class.

See its documentation for more information.
'''

import functools

import wx

from garlicsim_wx.general_misc import wx_tools

import garlicsim_wx


class App(wx.PySimpleApp):
    '''
    A garlicsim_wx App.
    
    The App is responsible for spawning a Frame.
    '''
    # todo: need to think if i allow frames with no app. on one hand good idea,
    # to allow people to start a garlicsim_wx frame in their own app. on other
    # hand frames will need to know how to start another frame.
    # tododoc: cache `super` in critical paths.
    # tododoc: move all stuff related to shortcut keys to
    # KeyBindingManager
    def __init__(self, new_gui_project_simpack_name=None,
                 load_gui_project_file_path=None):
        '''
        Constructor.
        
        In order to start a new simulation on startup, pass the name of the
        simpack as `new_gui_project_simpack_name`.
        
        In order to load a simulation from file on startup, pass the path to the
        file as `load_gui_project_file_path`.
        
        (At most one of these can be done.)
        '''
        self.frame = None
        assert not (new_gui_project_simpack_name and load_gui_project_file_path)
        self.new_gui_project_simpack_name = new_gui_project_simpack_name
        self.load_gui_project_file_path = load_gui_project_file_path
        
        super(App, self).__init__()
        
        #self.SetCallFilterEvent()
        
        self._keys_waiting_for_char = {}
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx_tools.EVT_TOKEN, self.on_token)
        
               
    
    def OnInit(self):
        
        frame = garlicsim_wx.Frame(
            parent=None,
            title="GarlicSim",
            size=(1140, 850)
        )
        
        self.frame = frame
        
        self.SetTopWindow(frame)
        
        if self.new_gui_project_simpack_name is not None:
            simpack = __import__(
                self.new_gui_project_simpack_name,
                fromlist=['']
            )
            
            wx.CallAfter(
                functools.partial(
                    self.frame._new_gui_project_from_simpack,
                    simpack
                )
            )
            
        if self.load_gui_project_file_path is not None:
            
            wx.CallAfter(
                functools.partial(
                    self.frame._open_gui_project_from_path,
                    self.load_gui_project_file_path
                )
            )
            
        return True
    
    #def ProcessEvent(self, event):
        #return super(App, self).ProcessEvent(event)
    
    #def FilterEvent(self, event):
        #if not isinstance(event, wx.KeyEvent):
            #return super(App, self).FilterEvent(event)
        #else: # isinstance(event, wx.KeyEvent)
            #return super(App, self).FilterEvent(event)
    
    def process_key(self, key):
        assert isinstance(key, wx_tools.Key)
        if key == wx_tools.Key(ord('`')):
            1/1/1/1/1/1/1/1/1/0 # woo woo woo @
        
            
    def on_key_down(self, event):
        key = wx_tools.Key.get_from_key_event(event)
        if key.would_cause_evt_char():
            token_event = wx.PyEvent(self.GetId())
            event.SetEventType(event_binder.evtType[0])
            event.key = key
            wx.PostEvent(self, event)
        else:
            self.process_key(key)
        event.Skip()
            
        
    def on_char(self, event):
        key = wx_tools.Key.get_from_key_event(event)
        if key.would_cause_evt_char():
            self._keys_waiting_for_char[key] = False
            token_event = wx.PyEvent(self.GetId())
            event.SetEventType(event_binder.evtType[0])
            event.key = key
            wx.PostEvent(self, event)
        else:
            self.process_key(key)
        event.Skip()
        
        
    def on_token(self, event):
        key = wx_tools.Key.get_from_key_event(event)
        if key.would_cause_evt_char():
            1/0
        else:
            1/0
        event.Skip()
        
    