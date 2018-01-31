from os import listdir, environ, path, rename, rmdir
import sys
import json
Extensions = json.load(open('Extension.json'))


def execute():
    if sys.platform == 'win32':
        desktopdir = path.join(environ['USERPROFILE'], 'Desktop')

        # Determine Windows version; check if this is XP; accordingly, read target folders
        if sys.getwindowsversion().major < 6:
            Alldesktopdir = path.join(environ['ALLUSERSPROFILE'], 'Desktop')
        else:
            Alldesktopdir = path.join(environ['PUBLIC'], 'Desktop')

        '''list of folders to be created'''
    elif sys.platform == 'linux':
        desktopdir = path.join(environ['HOME'], 'Desktop')
        Alldesktopdir = path.join(environ['HOME'], 'Desktop')
    elif sys.platform == 'darwin':
        desktopdir = path.join(environ['HOME'], 'Desktop')
    else:
        print("{} version not implemented".format(sys.platform))
        raise NotImplementedError

    map = listdir(desktopdir)

    for folder in map:
        if folder in Extensions:
            contents = listdir(path.join(desktopdir, folder))
            for thing in contents:
                rename(desktopdir+'/'+folder+'/'+thing, desktopdir+'/'+thing)
            rmdir(desktopdir+'/'+folder)


