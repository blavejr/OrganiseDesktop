import sys
import os
import json
from os import path, mkdir, listdir, rename, environ, rmdir


class OrganiseDesktop():
    """
    
    Contains desktop organisation helper functions
    
    """
    extensions = {}
    separator = '/'
    desktopdir = ''
    Alldesktopdir = None

    def __init__(self, extensions):

        """
        Obtains various localised information about the platform and user, and performs system checks upon initialization.
        """

        # References:   https://en.wikipedia.org/wiki/Environment_variable
        # Default_values
        #               https://en.wikipedia.org/wiki/Windows_NT#Releases
        self.extensions = extensions
        
        
        if sys.platform == 'win32':
            self.desktopdir = path.join(environ['USERPROFILE'], 'Desktop')
            # TODO: Set desktopdir to Virtual Directory for testing on Windows

            # Determine Windows version; check if this is XP;
            # read target folders accordingly
            if not sys.getwindowsversion() == 10:
                if sys.getwindowsversion().major < 6:
                    self.Alldesktopdir = path.join(environ['ALLUSERSPROFILE'], 'Desktop')  # noqa
                else:
                    self.Alldesktopdir = path.join(environ['PUBLIC'], 'Desktop')  # noqa
            '''list of folders to be created'''
            
            
        elif sys.platform in ['linux', 'darwin']:
            
            if environ.get('TEST_DIR'):
                self.desktopdir = environ.get('TEST_DIR')
                
            else:
                self.desktopdir = path.join(environ['HOME'], 'Desktop')
                
        else:
            print("{} version not implemented".format(sys.platform))
            raise NotImplementedError

            
            
    def _create_dir_path(self, directory):
        return os.path.join(self.desktopdir, directory)
    
    

    def makedir(self, folders_to_make):

        """
        This function makes the needed folders if they are not already found.

        For all the folders in the folder_to_make list, if that folder does not
        exist on the main_desktop, create that folder.
        """

        directories = [self._create_dir_path(dir) for dir in folders_to_make]

        for dir in directories:
            if not path.isdir(dir):
                mkdir(dir)

    def removedir(self, folders_i_made):

        """
        This function will check folders that this program made.
        If the folder is empty, it will delete that folder. simple job.
        """

        directories = [self._create_dir_path(dir) for dir in folders_i_made]

        for dir in directories:
            if not listdir(dir):
                rmdir(dir)

    def list_directory_content(self):

        """
        This function checks the two folders
        (current user desktop and all user desktop),
        if on windows, only checks one folder if on linux or macOS,
        it takes all the items there and puts them into two respective
        lists which are returned and used by the mover function
        """

        # TODO: Is this really necessary? To be removed at PR stage
        content = [listdir(self.desktopdir)]
        if self.Alldesktopdir:
            content += [listdir(self.Alldesktopdir)]
        return content

    def mover(self, content):

        """
        This function gets two lists with all the things on the desktops
        and copies them into their respective folders
        """

        # image extensions source: https://fileinfo.com/filetypes/raster_image,
        #                          https://fileinfo.com/filetypes/vector_image,
        #                          https://fileinfo.com/filetypes/camera_raw
        # music extensions source: https://fileinfo.com/filetypes/audio
        # movie extensions source: http://bit.ly/2wvYjyr
        # text extensions source:  http://bit.ly/2wwcfZs

        user_dir_content = content[0]

        # Anything from the All_users_desktop goes to shortcuts, mainly because
        # that's all that's ever there (I think)
        if self.separator != '/' and not sys.getwindowsversion()[0] == 10:
            all_users_content = content[1]
            
            for item in all_users_content:
                # This is a cmd command to move items from one folder to other
                rename( os.path.join(self.Alldesktopdir, item), os.path.join(self.desktopdir, item))  # noqa

        to_be_cleaned = [entry for entry in user_dir_content
                            if entry not in self.extensions and not (entry.startswith('.') or entry.startswith('..'))]  # noqa

        for item in to_be_cleaned:
            found = False
            
            for sorting_folder in self.extensions:
                folder = os.path.join(self.desktopdir, item)
                
                if os.path.isdir(folder) and item not in self.extensions and "Folders" in self.extensions:  # noqa
                    try:
                        rename(src= os.path.join(self.desktopdir, item),
                            dst=os.path.join(self.desktopdir, 'Folders', item))  # noqa
                        
                        found = True
                        break
                        
                    except PermissionError:
                        print("File is being used by some other process")
                        
                for extension in self.extensions[sorting_folder]:
                    
                    if (str(item.lower()).endswith(extension) and
                        str(item) != 'Clean.lnk' and str(item) != 'Clean.exe.lnk'):  # noqa
                        
                        rename(src=os.path.join(self.desktopdir, item),
                               dst=os.path.join(self.desktopdir, sorting_folder, item))  # noqa
                        
                        found = True
                        break
            if not found:
                print('Did not sort ' + item)

    def writter(self, content):

        """
        This function writes the two lists of all the items left on the desktop
        just in case something isn't right and we need a log.
        """

        if not os.path.isdir(path.dirname(os.getcwd())+'/log'):  # Create log folder if non exists  # noqa
            os.makedirs(path.dirname(os.getcwd())+'/log')
            
        writeOB = open(path.dirname(os.getcwd()) + '/log/modifications.log', 'w')  # noqa
        
        writeOB.write('This is a list of all items on your desktop before it was cleaned.\n'  # noqa
                      'Email this list to kalimbatech@gmail.com if anything is not working as planned, it will help with debugging\n'  # noqa
                      'Together we can make a better app\n\n')  # noqa

        for desktop_entry in content:
            for i in desktop_entry:
                writeOB.write(i)
                writeOB.write('\n')

        writeOB.close()


def organise_desktop(extensions):

    """
    Cleans up the desktop
    """
    #Find working directory
    pwd = os.path.dirname(os.path.abspath(__file__))

    # The oh-so-magnificent main function keeping the stuff in order
    
    #Initialize the OrganiseDesktop class
    projectOB = OrganiseDesktop(extensions)
    
    #Make the directories
    projectOB.makedir(extensions)
    
    #Get the maps of the directories
    maps = projectOB.list_directory_content()
    
    #Move the files to their appropriate locations
    projectOB.mover(maps)

    #Remove directories created by this program but empty
    projectOB.removedir(extensions)
    
    #Log the original files
    projectOB.writter(maps)


def undo():

    """
    Restores the changes from organising your desktop
    """

    Extensions = json.load( open( os.path.dirname( os.path.abspath(__file__) ) + '/Extension.json') )  # noqa

    if sys.platform == 'win32':
        desk_to_dir = path.join( environ['USERPROFILE'], 'Desktop' )

        # Determine Windows version; check if this is XP; accordingly,
        # read target folders
        if not sys.getwindowsversion()[0] == 10:
            
            if sys.getwindowsversion().major < 6:
                desk_to_dir = path.join(environ['ALLUSERSPROFILE'], 'Desktop')
            else:
                desk_to_dir = path.join(environ['PUBLIC'], 'Desktop')

    # list of folders to be created
    elif sys.platform == 'linux' or sys.platform == 'darwin':
        if environ.get('TEST_DIR') is not None:
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
            contents = listdir( path.join(desk_to_dir, folder) )
            
            for thing in contents:
                try:
                    rename(src=os.path.join(desk_to_dir, folder, thing),
                           dst=os.path.join(desk_to_dir, thing))
                except:
                    print('File is being used by some other process')
                    
            rmdir(os.path.join(desk_to_dir, folder))


#Run the app
if __name__ == '__main__':
    organise_desktop()
