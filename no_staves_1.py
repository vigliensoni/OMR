import sys
import re
import os # GVM
import fnmatch # GVM

import subprocess # GVM

from gamera.toolkits import aruspix
from gamera.toolkits.aruspix.ax_file import AxFile

from gamera.core import *
from gamera.toolkits import musicstaves
from gamera.toolkits.musicstaves import stafffinder_miyao


from gamera import knn
from gamera.core import *
from gamera.args import *
from gamera.gui import gui
from gamera.gui import has_gui
from gamera.gui import var_name

init_gamera()


def dirEntries(dir_name, subdir, *args):
    '''Return a list of file names found in directory 'dir_name'
    If 'subdir' is True, recursively access subdirectories under 'dir_name'.
    Additional arguments, if any, are file extensions to match filenames. Matched
        file names are added to the list.
        If there are no additional arguments, all files found in the directory are
        added to the list.
        Example usage: fileList = dirEntries(r'H:\TEMP', False, 'txt', 'py')
        Only files with 'txt' and 'py' extensions will be added to the list.
        Example usage: fileList = dirEntries(r'H:\TEMP', True)
        All files and all the files in subdirectories under H:\TEMP will be added
        to the list.
        '''
    fileList = []
    for files in os.listdir(dir_name):
        dirfile = os.path.join(dir_name, files)
        if os.path.isfile(dirfile):
            if not args:
                fileList.append(dirfile)
            else:
                if os.path.splitext(dirfile)[1][1:] in args:
                    fileList.append(dirfile)

        elif os.path.isdir(dirfile) and subdir:
            print "Accessing directory:", dirfile
            fileList.extend(dirEntries(dirfile, subdir, *args))
    #print fileList
    return fileList

print
print
print

LUfolder = '/Users/gabriel/Desktop/omr_copy'

for name in dirEntries(LUfolder, True, 'tif'):
    #print name

    print name
    image = load_image(name) #157
    #image = image.to_onebit()
    staves = aruspix.swap.extract(0)
    
    
    musicstaves_no_staves = musicstaves.MusicStaves_rl_fujinaga(staves, 0, 0)
    musicstaves_no_staves.remove_staves(u'all', 4)
    
    
    
    musicstaves_no_staves.image.save_tiff((os.path.splitext(name)[0] + '_NO_ST.tif'))
    
    # o_file = os.path.splitext(name);
    # print o_file
    # 
    # axfile = AxFile(name, LUfolder)
    # print axfile
    # 
    # global swap
    # swap = axfile.get_img0()
    # print swap
    # staves0 = swap.extract(0)
    # print staves0
    # staves0.save_tiff(o_file[0] + '_ST.tif')





