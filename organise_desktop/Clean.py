import sys
import json
import os
from cronController import  schedule_end, schedule_start
from organiseDesktop import undo, organise_desktop

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
    root.resizable = False
    root.minsize(width=350, height=330)
    root.maxsize(width=350, height=330)
    app = App(root)
    root.protocol('WM_DELETE_WINDOW', app.quit_all)
    app.mainloop()
    root.destroy()
