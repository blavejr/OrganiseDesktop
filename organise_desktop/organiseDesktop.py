import sys
import os
import json
from os import path, mkdir, listdir, rename, environ, rmdir


class OrganiseDesktop():
    # TODO: Please add a Docstring for this Class
    """ """
    extensions = {}
    separator = '/'
    desktopdir = ''
    Alldesktopdir = None

    def __init__(self, extensions):
      
        """
        This is an initialization function, I do not wish to explain this.

        This is a smart way to get the username
        We could also have used os.environ, this brings a list and a lot of information we can manipulate.
        """


        #
        # References:   https://en.wikipedia.org/wiki/Environment_variable#Default_values
        #               https://en.wikipedia.org/wiki/Windows_NT#Releases
        #
        self.extensions = extensions
        if sys.platform == 'win32':
            self.desktopdir = path.join(environ['USERPROFILE'], 'Desktop')
            # TODO: Set desktopdir to Virtual Directory for testing on Windows too.

            # Determine Windows version; check if this is XP; read target folders accordingly
            if not sys.getwindowsversion() == 10:
                if sys.getwindowsversion().major < 6:
                    self.Alldesktopdir = path.join(environ['ALLUSERSPROFILE'], 'Desktop')
                else:
                    self.Alldesktopdir = path.join(environ['PUBLIC'], 'Desktop')
            '''list of folders to be created'''
        elif sys.platform in ['linux', 'darwin']:
            if environ.get('TEST_DIR'):
                self.desktopdir = environ.get('TEST_DIR')
            else:
                self.desktopdir = path.join(environ['HOME'], 'Desktop')
                print(self.desktopdir)
        else:
            print("{} version not implemented".format(sys.platform))
            raise NotImplementedError

    def _create_dir_path(self, directory):
        return self.desktopdir + self.separator + directory

    def makdir(self, folders_to_make):

        """
        This function makes the needed folders if they are not already found.

        For all the folders in the folder_name list, if that folder is not(False) on the main_desktop
        then create that folder.
        """

        directories = [self._create_dir_path(dir) for dir in folders_to_make ]
        for dir in directories:
            if not path.isdir(dir):
                mkdir(dir)

    def list_directory_content(self):

        """
        This function checks the two folders (current user desktop and all user desktop),
        if on windows, only checks one folder if on linux or macOS,
        it takes all the items there and puts them into two respective lists which are
        returned and used by the mover function
        """

        # TODO: Is this really necessary? To be removed at PR stage
        content = [listdir(self.desktopdir)]
        if self.Alldesktopdir:
            content += [listdir(self.Alldesktopdir)]
        return content


    def mover(self, content):

        """
        This function gets two lists with all the things on the desktops
        and copies them into their respective folders, using a forloop and if statements
        """

        print('moving with : ' + str(self.extensions))
        # image extensions source: https://fileinfo.com/filetypes/raster_image,
        #                          https://fileinfo.com/filetypes/vector_image, and
        #                          https://fileinfo.com/filetypes/camera_raw
        # music extensions source: https://fileinfo.com/filetypes/audio
        # movie extensions source: http://bit.ly/2wvYjyr
        # text extensions source:  http://bit.ly/2wwcfZs

        user_dir_content = content[0]

        # Anything from the All_users_desktop goes to shortcuts, mainly because that's all that's ever there (i think)
        if self.separator != '/' and not sys.getwindowsversion()[0] == 10:
            all_users_content = content[1]
            for item in all_users_content:
                # This is a cmd command to move items from one folder to the other
                rename(self.Alldesktopdir + self.separator + item, self.desktopdir + self.separator + item)

        to_be_cleaned = [entry for entry in user_dir_content
                            if entry not in self.extensions and not (entry.startswith('.') or entry.startswith('..'))]

        for item in to_be_cleaned:
            found = False
            for sorting_folder in self.extensions:
                # TODO: please short this 'if' statement
                if os.path.isdir(self.desktopdir + self.separator + item) and item not in self.extensions and "Folders" in self.extensions:
                   rename(src=self.desktopdir + self.separator + item,
                          dst=self.desktopdir + self.separator + 'Folders' + self.separator + item)
                   found = True
                   break
                for extension in self.extensions[sorting_folder]:
                    if (str(item.lower()).endswith(extension) and
                        str(item) != 'Clean.lnk' and
                        str(item) != 'Clean.exe.lnk'):
                        rename(src=self.desktopdir + self.separator + item,
                               dst=self.desktopdir + self.separator + sorting_folder + self.separator + item)
                        found = True
                        break
            if not found:
                print('Did not sort ' + item)

    def writter(self, content):

        """
        This function writes the two lists of all the items left on the desktop
        just incase something isn't right and we need a log.
        """

        if not os.path.isdir(path.dirname(os.getcwd())+'/log'):  # Create log folder if non exists
            os.makedirs(path.dirname(os.getcwd())+'/log')


        writeOB = open(path.dirname(os.getcwd()) + '/log/modifications.log', 'w')
        writeOB.write('This is a list of all the items on your desktop before it was cleaned.\n'
                      # This message is to long. PEP8 says 120. This is 133 characters long. 
                      'Email this list to kalimbatech@gmail.com if anything is not working as planned, it will help with debugging\n'
                      'Together we can make a better app\n\n')

        for desktop_entry in content:
            for i in desktop_entry:
                writeOB.write(i)
                writeOB.write('\n')

        writeOB.close()

def organise_desktop():

    """
    Cleans up the desktop
    """

    pwd = os.path.dirname(os.path.abspath(__file__))

    extensions = json.load(open(pwd+'/Extension.json'))

    folders = [x for x in extensions]

    # The oh so magnificent main function keeping the stuff in order
    projectOB = OrganiseDesktop(extensions)
    projectOB.makdir(extensions)
    maps = projectOB.list_directory_content()
    projectOB.mover(maps)
    projectOB.writter(maps)

def undo():

    """
    restores the changes from organising your desktop
    """

    Extensions = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/Extension.json'))

    if sys.platform == 'win32':
        desk_to_dir = path.join(environ['USERPROFILE'], 'Desktop')

        # Determine Windows version; check if this is XP; accordingly, read target folders
        if not sys.getwindowsversion()[0] == 10:
            if sys.getwindowsversion().major < 6:
                desk_to_dir = path.join(environ['ALLUSERSPROFILE'], 'Desktop')
            else:
                desk_to_dir = path.join(environ['PUBLIC'], 'Desktop')

    # list of folders to be created
    elif sys.platform == 'linux' or sys.platform == 'darwin':
        if environ.get('TEST_DIR') != '':
            desk_to_dir = environ.get('TEST_DIR')
        else:
            desk_to_dir = path.join(environ['HOME'], 'Desktop')
    else:
        print('{} version not implemented'.format(sys.platform))
        raise NotImplementedError

    map1 = listdir(desk_to_dir)
    if sys.platform == 'win32':
        separator = '\\'
    else:
        separator = '/'
    for folder in map1:
        if folder in Extensions:
            contents = listdir(path.join(desk_to_dir, folder))
            for thing in contents:
                rename(src=desk_to_dir+separator+folder+separator+thing, dst=desk_to_dir+separator+thing)
            rmdir(desk_to_dir+separator+folder)


if __name__ == '__main__':
    organise_desktop()
