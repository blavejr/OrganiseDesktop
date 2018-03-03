import sys
import os
from os import path, mkdir, listdir, rename, environ

class OrganiseDesktop():
    extensions = {}
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

            # Determine Windows version; check if this is XP; accordingly, read target folders
            if not sys.getwindowsversion() == 10:
                if sys.getwindowsversion().major < 6:
                    self.Alldesktopdir = path.join(environ['ALLUSERSPROFILE'], 'Desktop')
                else:
                    self.Alldesktopdir = path.join(environ['PUBLIC'], 'Desktop')
            '''list of folders to be created'''
        elif sys.platform == 'linux' or 'darwin':
            if environ['TEST_DIR'] != '':
                self.desktopdir = environ['TEST_DIR']
            else:
                self.desktopdir = path.join(environ['HOME'], 'Desktop')
        else:
            print("{} version not implemented".format(sys.platform))
            raise NotImplementedError

    def makdir(self, folders_to_make):
        '''
        This function makes the needed folders if they are not already found.
        '''
        try:
            '''For all the folders in the folder_name list, if that folder is not(False) on the main_desktop
               then create that folder.
            '''
            if sys.platform == 'win32':
                for nam in folders_to_make:
                    if path.isdir(self.desktopdir + '\\' + nam) is False:
                        mkdir(self.desktopdir + "\\" + nam)
            elif sys.platform == 'linux' or 'darwin':
                for nam in folders_to_make:
                    if path.isdir(self.desktopdir + '/' + nam) is False:
                        mkdir(self.desktopdir + "/" + nam)
        except Exception as e:
            print(e)

    def mapper(self):
        '''
        This function checks the two folders (current user desktop and all user desktop),
        if on windows, only checks one folder if on linux or macOS,
        it takes all the items there and puts them into two respective lists which are
        returned and used by the mover function
        '''
        if sys.platform == 'linux' or sys.platform == 'darwin' or sys.getwindowsversion()[0] == 10:
            return [listdir(self.desktopdir)]
        maps = [listdir(self.desktopdir), listdir(self.Alldesktopdir)]
        return maps

    def mover(self, maps, folder_names, separator):
        print('moving with : '+str(folder_names))
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
        map1 = maps[0]
        try:

            '''Anything from the All_users_desktop goes to shortcuts, mainly because that's all that's ever there (i think)'''
            if separator != '/' and not sys.getwindowsversion()[0] == 10:
                map2 = maps[1]
                for item in map2:
                    '''This is a cmd command to move items from one folder to the other'''
                    rename(self.Alldesktopdir + separator + item, self.desktopdir + separator + item)
            for file_or_folder in map1:
                if file_or_folder not in folder_names and not file_or_folder.startswith(".") and not file_or_folder.startswith(".."):
                    found = False
                    for sorting_folder in folder_names:
                        if os.path.isdir(self.desktopdir + separator + file_or_folder) and file_or_folder not in self.extensions and "Folders" in folder_names:
                            rename(src=self.desktopdir + separator + file_or_folder,
                                   dst=self.desktopdir + separator + 'text' + separator + file_or_folder)
                            found = True
                            break
                        for extension in self.extensions[sorting_folder]:
                            if str(file_or_folder.lower()).endswith(extension) and \
                               str(file_or_folder) != "Clean.lnk" and \
                               str(file_or_folder) != "Clean.exe.lnk":
                                rename(src=self.desktopdir + separator + file_or_folder,
                                       dst=self.desktopdir + separator + sorting_folder + separator + file_or_folder)
                                if separator == '/':
                                    os.system('cd ..')
                                found = True
                                break
                    if not found:
                        print("Did not sort " + file_or_folder)
        except () as e:
            print(e)

    def writter(self, maps):
        '''
        This function writes the two lists of all the items left on the desktop
        just incase something isn't right and we need a log.
        '''
        lists1 = maps[0]

        writeOB = open('Read_Me.txt', 'w')
        writeOB.write("This is a list of all the items on your desktop before it was cleaned.\n"
                      "Email this list to kalimbatech@gmail.com if anything is not working as planned, it will help with debugging\n"
                      "Together we can make a better app\n\n")

        for i in lists1:
            writeOB.write(i)
            writeOB.write("\n")

        if sys.platform == 'win32' and not sys.getwindowsversion()[0] == 10:
            lists2 = maps[1]
            for i in lists2:
                writeOB.write(i)
                writeOB.write("\n")
        writeOB.close()
