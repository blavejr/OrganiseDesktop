import sys
import json
import os
from .cronController import  schedule_end, schedule_start
from .organiseDesktop import undo, organise_desktop
from tkinter import ttk
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
        cb = ttk.Checkbutton(self, text=text, command=lambda: self.check(text))
        cb.state(['!alternate'])
        cb.state(['selected'])
        cb.pack(side='top', fill='x')
        return cb

    def make_button(self, text, command):
        btn = ttk.Button(self, text=text, command=command)
        btn.pack(side='left')
        return btn

    def create(self):
        self.winfo_toplevel().title('Desktop Cleaner')

        for ext in sorted(Extensions.keys()):
            self.make_checkbutton(ext)

        # buttons and their respective functions
        buttons = {'Clean': self.clean,
                   'Exit': self.quit_all,
                   'Undo': undo,
                   'Schedule': self.on_schedule_start,
                   'Remove\nSchedule': schedule_end
                   }

        for key in buttons:
            self.make_button(key, buttons[key])

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create()

def main():
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

if __name__ == '__main__':
    main()