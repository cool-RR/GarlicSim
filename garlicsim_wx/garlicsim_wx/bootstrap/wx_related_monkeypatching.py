import sys
import os.path

try:
    import wx.lib.wxcairo
except RuntimeError:
    if os.name != 'nt':
        raise
    
    path_of_executable = os.path.dirname(sys.executable)
    path_to_lib = os.path.join(path_of_executable, 'lib')
    addition_to_path = ';' + path_to_lib
    
    try:        
        os.environ['PATH'] += addition_to_path
        import wx.lib.wxcairo
    finally:
        assert os.environ['PATH'].endswith(addition_to_path)
        # Remove the addition_to_path:
        os.environ['PATH'] = os.environ['PATH'][:-len(addition_to_path)]
        