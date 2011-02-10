# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `` class.

See its documentation for more information.
'''

import shutil
import os.path
import sys

assert os.path.realpath(os.getcwd()) == \
       os.path.realpath(os.path.split(__file__)[0])

folders_to_delete = []
for folder in ['build', 'garlicsim_wx.egg-info', 'py2exe_dist']:
    if os.path.isdir(folder):
        folders_to_delete.append(folder)

if folders_to_delete:
    sys.stdout.write('Preparing to delete old build folders.\n')
    for folder_to_delete in folders_to_delete:
        sys.stdout.write("Deleting the '%s' folder... " % folder_to_delete)
        shutil.rmtree(folder_to_delete)
        sys.stdout.write('Done.')
else: # No folders to delete
    sys.stdout.write('No previous build folders to delete, all clean.\n')

sys.stdout.write('Launching py2exe.\n')

sys.exit(os.system(sys.executable + ' setup.py py2exe'))