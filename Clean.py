__author__ = "Remigius Kalimba"
'''Add a timer so it does this automatically everyday at a set time'''

from os import path, mkdir, listdir, rename, environ
from getpass import getuser
import time
import sys
import json

if sys.version_info >= (3,):
    from tkinter import *
    from tkinter import messagebox as tkMessageBox
else:
    from tkinter import *
    import tkMessageBox

import Globals

Extensions = json.load(open('Extension.json'))

class App(Frame):
    def clean(self):
        main()

    def quit_all(self):
        quit()
        sys.exit(0)

    def check(self, item):
        if item == 0:
            Globals.sc = not Globals.sc
        elif item == 1:
            Globals.zips = not Globals.zips
        elif item == 2:
            Globals.audio = not Globals.audio
        elif item == 3:
            Globals.img = not Globals.img
        elif item == 4:
            Globals.exes = not Globals.exes
        elif item == 5:
            Globals.mov = not Globals.mov
        elif item == 6:
            Globals.txt = not Globals.txt
        elif item == 7:
            Globals.cad = not Globals.cad
        elif item == 8:
            Globals.programming = not Globals.programming

    def create(self):
        self.winfo_toplevel().title("Desktop Cleaner")

        self.shortcuts = Checkbutton(self)
        self.shortcuts["text"] = "Shortcuts"
        self.shortcuts.select()
        self.shortcuts["command"] = lambda: self.check(0)
        self.shortcuts.pack({"side":"top"})

        self.zip = Checkbutton(self)
        self.zip["text"] = "Archives"
        self.zip.select()
        self.zip["command"] = lambda: self.check(1)
        self.zip.pack({"side": "top"})

        self.music = Checkbutton(self)
        self.music["text"] = "Music"
        self.music.select()
        self.music["command"] = lambda: self.check(2)
        self.music.pack({"side": "top"})

        self.images = Checkbutton(self)
        self.images["text"] = "Images"
        self.images.select()
        self.images["command"] = lambda: self.check(3)
        self.images.pack({"side": "top"})

        self.exe = Checkbutton(self)
        self.exe["text"] = "Executables"
        self.exe.select()
        self.exe["command"] = lambda: self.check(4)
        self.exe.pack({"side": "top"})

        self.movies = Checkbutton(self)
        self.movies["text"] = "Movies"
        self.movies.select()
        self.movies["command"] = lambda: self.check(5)
        self.movies.pack({"side": "top"})

        self.text = Checkbutton(self)
        self.text["text"] = "Text"
        self.text.select()
        self.text["command"] = lambda: self.check(6)
        self.text.pack({"side": "top"})

        self.d3 = Checkbutton(self)
        self.d3["text"] = "CAD Files"
        self.d3.select()
        self.d3["command"] = lambda: self.check(7)
        self.d3.pack({"side": "top"})

        self.code = Checkbutton(self)
        self.code["text"] = "Code"
        self.code.select()
        self.code["command"] = lambda: self.check(8)
        self.code.pack({"side": "top"})

        self.clean_button = Button(self)
        self.clean_button["text"] = "Clean"
        self.clean_button["command"] = self.clean
        self.clean_button.pack({"side": "left"})

        self.quit_button = Button(self)
        self.quit_button["text"] = "Exit"
        self.quit_button["command"] = self.quit_all
        self.quit_button.pack({"side":"left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create()


class OrganiseDesktop():
    def __init__(self):
        '''
        This is an initialization function, I do not wish to explain this.

        This is a smart way to get the username
        We could also have used os.environ, this brings a list and a lot of information we can manipulate.
        '''
        user = getuser()

        #
        # References:   https://en.wikipedia.org/wiki/Environment_variable#Default_values
        #               https://en.wikipedia.org/wiki/Windows_NT#Releases
        #
        if sys.platform == 'win32':
            self.desktopdir = path.join(environ['USERPROFILE'],'Desktop')

            # Determine Windows version; check if this is XP; accordingly, read target folders
            if sys.getwindowsversion().major < 6:
                self.Alldesktopdir = path.join(environ['ALLUSERSPROFILE'],'Desktop')
            else:
                self.Alldesktopdir = path.join(environ['PUBLIC'],'Desktop')

            '''list of folders to be created'''
            self.folder_names = ["Folders", "Shortcuts", "Zips", "Executables", "Pictures", "Music", "Movies", "Docs", "Code"]
            self.special_folders = []
        else:
            print("{} version not implemented".format(sys.platform))
            raise NotImplementedError

    def makdir(self):
        '''
        This function makes the needed folders if they are not already found.
        '''
        try:
            '''For all the folders in the folder_name list, if that folder is not(False) on the main_desktop
               then create that folder.
            '''
            for nam in range(0, len(self.folder_names)):
                if path.isdir(self.desktopdir+'\\'+self.folder_names[nam]) == False:
                    mkdir(self.desktopdir+"\\"+self.folder_names[nam])
                    print(self.folder_names[nam]+" has been created!")
                else:
                    print("Folder already exists!")
        except Exception as e:
            print(e)

    def mapper(self):
        '''
        This function checks the two folders (current user desktop and all user desktop)
        it takes all the items there and puts them into two respective lists which are
        returned and used by the mover function
        '''
        map = listdir(self.desktopdir)
        map2 = listdir(self.Alldesktopdir)
        maps = [map, map2]
        return maps

    def mover(self, map, map2):
        '''
        This function gets two lists with all the things on the desktops
        and copies them into their respective folders, using a forloop and if statements
        '''
        map = map
        map2 = map2

        '''
        Extension Lists
        '''
        shortcuts_extensions = Extensions['shortcut']
        executable_extensions = Extensions['executable']

        # zip extensions source: http://bit.ly/2fnWz4D
        zip_extensions = Extensions['zip']

        # image extensions source: https://fileinfo.com/filetypes/raster_image, https://fileinfo.com/filetypes/vector_image, and https://fileinfo.com/filetypes/camera_raw
        images_extensions = Extensions['image']

        # music extensions source: https://fileinfo.com/filetypes/audio
        music_extensions = Extensions['music']

        # movie extensions source: http://bit.ly/2wvYjyr
        movie_extensions = Extensions['movie']

        # text extensions source: http://bit.ly/2wwcfZs
        text_extensions = Extensions['text']
        D3_work = Extensions['D3work']
        programming_languages_extensions = Extensions['programming']
        try:

            '''Anything from the All_users_desktop goes to shortcuts, mainly because that's all that's ever there (i think)'''
            for item in map2:
                '''This is a cmd command to move items from one folder to the other'''
                rename(self.Alldesktopdir+'\\'+item, self.desktopdir+"\\"+self.folder_names[1]+"\\"+item)

            for a in range(0, len(map)):

                if Globals.sc:
                    for b in shortcuts_extensions:
                        if str(map[a].lower()).endswith(b) and str(map[a]) != "Clean.lnk" and str(map[a]) != "Clean.exe.lnk":
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[1]+"\\"+map[a])

                if Globals.exes:
                    for b in executable_extensions:
                        if str(map[a].lower()).endswith(b) and str(map[a].lower()) != "Clean.exe":
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[3]+"\\"+map[a])

                if Globals.zips:
                    for b in zip_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[2]+"\\"+map[a])

                if Globals.img:
                    for b in images_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[4]+"\\"+map[a])

                if Globals.audio:
                    for b in music_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[5]+"\\"+map[a])

                if Globals.mov:
                    for b in movie_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[6]+"\\"+map[a])

                if Globals.txt:
                    for b in text_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[7]+"\\"+map[a])

                if Globals.programming:
                    for b in programming_languages_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[8]+"\\"+map[a])

                for b in shortcuts_extensions:
                    if str(map[a].lower()).endswith(b) and str(map[a]) != "Clean.lnk" and str(map[a]) != "Clean.exe.lnk":
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[1]+"\\"+map[a])

                for b in executable_extensions:
                    if str(map[a].lower()).endswith(b) and str(map[a].lower()) != "Clean.exe":
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[3]+"\\"+map[a])

                for b in zip_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[2]+"\\"+map[a])

                for b in images_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[4]+"\\"+map[a])

                for b in music_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[5]+"\\"+map[a])

                for b in movie_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[6]+"\\"+map[a])

                for b in text_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[7]+"\\"+map[a])

                for b in D3_work:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[8]+"\\"+map[a])

                for b in programming_languages_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[8]+"\\"+map[a])


                '''This weird part looks for the ".", if its not there this must be a folder'''
                if "." not in str(map[a]) and map[a] not in self.folder_names:
                    rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[0]+"\\"+map[a])
                else:
                    '''Just some error handling here'''
                    if map[a].lower() not in self.folder_names:
                        print("I do not know what to do with "+map[a]+" please update me!")
                    pass
        except Exception as e:
            print(e)

    def writter(self, maps):
        '''
        This function writes the two lists of all the items left on the desktop
        just incase something isnt right and we need a log.
        '''
        lists1 = maps[0]
        lists2 = maps[1]
        writeOB = open('Read_Me.txt', 'w')
        writeOB.write("This is a list of all the items on your desktop before it was cleaned.\n"
                      "Email this list to kalimbatech@gmail.com if anything is not working as planned, it will help with debugging\n"
                      "Together we can make a better app\n\n")

        for i in lists1:
            writeOB.write(i)
            writeOB.write("\n")

        for i in lists2:
            writeOB.write(i)
            writeOB.write("\n")
        writeOB.close()

def automate():
    '''
    * This function keeps the program running and scans the desktop and cleans it after a set time
    * Link explains the syntax https://technet.microsoft.com/en-us/library/cc725744(v=ws.11).aspx
    Something isnt right here
    '''
    # os.system(SchTasks /Create /SC DAILY /TN “My Task” /TR “C:RunMe.bat” /ST 09:00)

def run_at_time():
    while True:
        tim = time.strftime('%X')
        if str(tim).startswith('6:30:00'):
            main()
            time.sleep(1)
            run_at_time()

def main():
    ''' The oh so magnificent main function keeping shit in order '''
    projectOB = OrganiseDesktop()
    projectOB.makdir()
    maps = projectOB.mapper()
    projectOB.mover(maps[0], maps[1])
    projectOB.writter(maps)
    tkMessageBox.showinfo("Complete", "Desktop clean finished.")


root = Tk()
app = App(root)
app.mainloop()
root.destroy()
