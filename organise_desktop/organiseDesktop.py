import sys
import os
import json
from os import path, mkdir, listdir, rename, environ

class OrganiseDesktop():

    extensions = {}
    separator = '/'
    desktopdir = ''
    Alldesktopdir = None

    def __init__(self, extensions):
        '''
        This is an initialization function, I do not wish to explain this.

        This is a smart way to get the username
        We could also have used os.environ, this brings a list and a lot of information we can manipulate.
        '''

        #
        # References:   https://en.wikipedia.org/wiki/Environment_variable#Default_values
        #               https://en.wikipedia.org/wiki/Windows_NT#Releases
        #
        self.extensions = extensions
        if sys.platform == 'win32':
            self.desktopdir = path.join(environ['USERPROFILE'], 'Desktop')
            # TODO: Set desktopdir to Virtual Directory for testing on Windows too.

            # Determine Windows version; check if this is XP; accordingly, read target folders
            if not sys.getwindowsversion() == 10:
                if sys.getwindowsversion().major < 6:
                    self.Alldesktopdir = path.join(environ['ALLUSERSPROFILE'], 'Desktop')
                else:
                    self.Alldesktopdir = path.join(environ['PUBLIC'], 'Desktop')
            '''list of folders to be created'''
        elif sys.platform in ['linux', 'darwin']:
            if environ['TEST_DIR'] != '':
                self.desktopdir = environ['TEST_DIR']
            else:
                self.desktopdir = path.join(environ['HOME'], 'Desktop')
        else:
            print("{} version not implemented".format(sys.platform))
            raise NotImplementedError

    def _create_dir_path(self, directory):
        return self.desktopdir + self.separator + directory

    def makdir(self, folders_to_make):
        '''
        This function makes the needed folders if they are not already found.

        For all the folders in the folder_name list, if that folder is not(False) on the main_desktop
        then create that folder.
        '''
        directories = [self._create_dir_path(dir) for dir in folders_to_make ]
        for dir in directories:
            if not path.isdir(dir):
                mkdir(dir)

    def list_directory_content(self):
        '''
        This function checks the two folders (current user desktop and all user desktop),
        if on windows, only checks one folder if on linux or macOS,
        it takes all the items there and puts them into two respective lists which are
        returned and used by the mover function
        '''
        # TODO: Is this really necessary? To be removed at PR stage
        content = [listdir(self.desktopdir)]
        if self.Alldesktopdir:
            content += [listdir(self.Alldesktopdir)]
        return content


    def mover(self, content, folder_names):
        print('moving with : ' + str(folder_names))
        '''
        This function gets two lists with all the things on the desktops
        and copies them into their respective folders, using a forloop and if statements
        '''
        # image extensions source: https://fileinfo.com/filetypes/raster_image,
        #                          https://fileinfo.com/filetypes/vector_image, and
        #                          https://fileinfo.com/filetypes/camera_raw
        # music extensions source: https://fileinfo.com/filetypes/audio
        # movie extensions source: http://bit.ly/2wvYjyr
        # text extensions source:  http://bit.ly/2wwcfZs

        user_dir_content = content[0]

        try:

            '''Anything from the All_users_desktop goes to shortcuts, mainly because that's all that's ever there (i think)'''
            if self.separator != '/' and not sys.getwindowsversion()[0] == 10:
                all_users_content = content[1]
                for item in all_users_content2:
                    '''This is a cmd command to move items from one folder to the other'''
                    rename(self.Alldesktopdir + self.separator + item, self.desktopdir + self.separator + item)

            to_be_cleaned = [entry for entry in user_dir_content
                                if entry not in folder_names and not (entry.startswith('.') or entry.startswith('..'))]

            for item in to_be_cleaned:
                found = False
                for sorting_folder in folder_names:
                    if os.path.isdir(self.desktopdir + self.separator + item) and item not in self.extensions and "Folders" in folder_names:
                       rename(src=self.desktopdir + self.separator + item,
                              dst=self.desktopdir + self.separator + 'Folders' + self.separator + item)
                       found = True
                       break
                    for extension in self.extensions[sorting_folder]:
                        if (str(item.lower()).endswith(extension) and
                            str(item) != "Clean.lnk" and
                            str(item) != "Clean.exe.lnk"):
                            rename(src=self.desktopdir + self.separator + item,
                                   dst=self.desktopdir + self.separator + sorting_folder + self.separator + item)
                            found = True
                            break
                if not found:
                    print("Did not sort " + item)
        except () as e:
            print(e)

    def writter(self, content):
        '''
        This function writes the two lists of all the items left on the desktop
        just incase something isn't right and we need a log.
        '''
        lists1 = content[0]

        writeOB = open(path.dirname(os.getcwd()) + '/log/modifications.log', 'w')
        writeOB.write("This is a list of all the items on your desktop before it was cleaned.\n"
                      "Email this list to kalimbatech@gmail.com if anything is not working as planned, it will help with debugging\n"
                      "Together we can make a better app\n\n")

        for desktop_entry in content:
            for i in desktop_entry:
                writeOB.write(i)
                writeOB.write("\n")

        writeOB.close()

if __name__ == '__main__':
    pwd = os.path.dirname(os.path.abspath(__file__))

    Extensions = json.load(open(pwd+'/Extension.json'))

    folders = [x for x in Extensions]

    ''' The oh so magnificent main function keeping shit in order '''
    projectOB = OrganiseDesktop(Extensions)
    projectOB.makdir(Extensions)
    maps = projectOB.list_directory_content()
    projectOB.mover(maps, Extensions)
    projectOB.writter(maps)
