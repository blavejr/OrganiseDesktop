from os import listdir, environ, path, rename, rmdir
import sys
import json
import os


Extensions = json.load(open(os.path.dirname(os.path.abspath(__file__))+'/Extension.json'))


def execute():
    if sys.platform == 'win32':
        desktopdir = path.join(environ['USERPROFILE'], 'Desktop')

        # Determine Windows version; check if this is XP; accordingly, read target folders
        if not sys.getwindowsversion()[0] == 10:
            if sys.getwindowsversion().major < 6:
                desktopdir = path.join(environ['ALLUSERSPROFILE'], 'Desktop')
            else:
                desktopdir = path.join(environ['PUBLIC'], 'Desktop')

        '''list of folders to be created'''
    elif sys.platform == 'linux' or sys.platform == 'darwin':
        desktopdir = path.join(environ['HOME'], 'Desktop')

    else:
        print("{} version not implemented".format(sys.platform))
        raise NotImplementedError

    map1 = listdir(desktopdir)
    if sys.platform == 'win32':
        separator = '\\'
    else:
        separator = '/'
    for folder in map1:
        if folder in Extensions:
            contents = listdir(path.join(desktopdir, folder))
            for thing in contents:
                rename(desktopdir+separator+folder+separator+thing, desktopdir+separator+thing)
            rmdir(desktopdir+separator+folder)


