import sys
import json
import os
from cronController import  schedule_end, schedule_start
from organiseDesktop import undo, organise_desktop
from os import path, mkdir, listdir, rename, environ, rmdir

if sys.version_info >= (3,):
    from tkinter import *
    from tkinter import messagebox as tkMessageBox
else:
    from tkinter import *
    import tkMessageBox

pwd = os.path.dirname(os.path.abspath(__file__))
Extensions = json.load(open(pwd+'/Extension.json', 'r'))
folders = [x for x in Extensions]

class App(Frame):
    """define the GUI"""
    def clean(self):
        checked_extensions = {}
        for x in folders:
            checked_extensions[x] = Extensions[x]
        organise_desktop(checked_extensions)
        tkMessageBox.showinfo('Complete', 'Desktop clean finished.')

    def remove_empty_folder(self):    
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
            if environ.get('TEST_DIR'):
                desk_to_dir = environ.get('TEST_DIR')

            else:
                desk_to_dir = path.join(environ['HOME'], 'Desktop')
        else:
            print('{} version not implemented'.format(sys.platform))
            raise NotImplementedError

        mapped_files_dirs = listdir(desk_to_dir)

        if sys.platform == 'win32':
            separator = '\\'
        else:
            separator = '/'

        folders_list = []
        for any_file_folder in mapped_files_dirs:
            folder =  path.join(desk_to_dir, any_file_folder)
            if os.path.isdir(folder):
                folders_list.append(folder)
        for folder in folders_list:
            if not os.listdir(folder):
                os.rmdir(folder) #Removes all empty folder on the desktop
        
        tkMessageBox.showinfo('Completed', 'Empty folders removed')


    def quit_all(self):
        sys.exit(0)

    def check(self, item):
        global folders
        if item in folders:
            folders.remove(item)
        else:
            folders.append(item)

    def on_schedule_start(self):
        schedule_start(folders)

    def make_checkbutton(self, text):
        cb = Checkbutton(self, text=text, command=lambda: self.check(text))
        cb.select()
        cb.pack({'side': 'top'})
        return cb

    def make_button(self, text, command):
        btn = Button(self, text=text, command=command)
        btn.pack({'side': 'left'})
        return btn

    def create(self):
        self.winfo_toplevel().title('Desktop Cleaner')

        for ext in sorted(Extensions.keys()):
            self.make_checkbutton(ext)

        # buttons and their respective functions
        buttons = {'Clean': self.clean,
                   'Exit': self.quit_all,
                   'Undo': undo,
                   'Remove Empty\nFolder': self.remove_empty_folder,                   
                   'Schedule': self.on_schedule_start,
                   'Remove\nSchedule': schedule_end
                   }

        for key in buttons:
            self.make_button(key, buttons[key])

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create()

if __name__ == '__main__':
    root = Tk()
    # root.resizable = False            # commenting this approach and applying the below one.
    root.resizable(FALSE,FALSE)         # To make the application's size constant and restore button in windows as greyed out(with width=350 and height=330 as mentioned below)
    root.minsize(width=350, height=330)
    root.maxsize(width=350, height=330)

    '''Logic to launch the app in center - start'''
    positionRight = int(root.winfo_screenwidth() / 2 - 330 / 2) #considering width=330
    positionDown = int(root.winfo_screenheight() / 2 - 350 / 2) #considering height=350
    root.geometry("+{}+{}".format(positionRight, positionDown))
    '''Logic to launch the app in center - end'''

    app = App(root)
    root.protocol('WM_DELETE_WINDOW', app.quit_all)
    app.mainloop()
    root.destroy()
