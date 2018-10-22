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

Extensions = json.load(open(pwd+'/Extension.json'))

folders = [x for x in Extensions]


class App(Frame):
    """define the GUI"""
    def clean(self):
        organise_desktop()
        tkMessageBox.showinfo('Complete', 'Desktop clean finished.')
        
    def quit_all(self):
        sys.exit(0)

    def check(self, item):
        if item in folders:
            folders.remove(item)
        else:
            folders.append(item)

    def on_schedule_start(self):
        schedule_start(folders)

    def create(self):
        self.winfo_toplevel().title('Desktop Cleaner')

        self.shortcuts = Checkbutton(self)
        self.shortcuts['text'] = 'Shortcuts'
        self.shortcuts.select()
        self.shortcuts['command'] = lambda: self.check('Shortcuts')
        self.shortcuts.pack({'side': 'top'})

        self.malware = Checkbutton(self)
        self.malware['text'] = 'Malware'
        self.malware.select()
        self.malware['command'] = lambda: self.check('Malware')
        self.malware.pack({'side': 'top'})

        self.zip = Checkbutton(self)
        self.zip['text'] = 'Folders'
        self.zip.select()
        self.zip['command'] = lambda: self.check('Folders')
        self.zip.pack({'side': 'top'})

        self.music = Checkbutton(self)
        self.music['text'] = 'Music'
        self.music.select()
        self.music['command'] = lambda: self.check('Music')
        self.music.pack({'side': 'top'})

        self.images = Checkbutton(self)
        self.images['text'] = 'Images'
        self.images.select()
        self.images['command'] = lambda: self.check('Images')
        self.images.pack({'side': 'top'})

        self.exe = Checkbutton(self)
        self.exe['text'] = 'Executables'
        self.exe.select()
        self.exe['command'] = lambda: self.check('Executables')
        self.exe.pack({'side': 'top'})

        self.movies = Checkbutton(self)
        self.movies['text'] = 'Movies'
        self.movies.select()
        self.movies['command'] = lambda: self.check('Movies')
        self.movies.pack({'side': 'top'})

        self.text = Checkbutton(self)
        self.text['text'] = 'Text'
        self.text.select()
        self.text['command'] = lambda: self.check('Text')
        self.text.pack({'side': 'top'})

        self.d3 = Checkbutton(self)
        self.d3['text'] = 'CAD'
        self.d3.select()
        self.d3['command'] = lambda: self.check('CAD')
        self.d3.pack({'side': 'top'})

        self.code = Checkbutton(self)
        self.code['text'] = 'Programming'
        self.code.select()
        self.code['command'] = lambda: self.check('Programming')
        self.code.pack({'side': 'top'})

        self.clean_button = Button(self)
        self.clean_button['text'] = 'Clean'
        self.clean_button['command'] = self.clean
        self.clean_button.pack({'side': 'left'})

        self.quit_button = Button(self)
        self.quit_button['text'] = 'Exit'
        self.quit_button['command'] = self.quit_all
        self.quit_button.pack({'side': 'left'})

        self.undo_button = Button(self)
        self.undo_button['text'] = 'Undo'
        self.undo_button['command'] = undo()
        self.undo_button.pack({'side': 'left'})

        self.schedule_button = Button(self)
        self.schedule_button['text'] = 'Schedule'
        self.schedule_button['command'] = self.on_schedule_start
        self.schedule_button.pack({'side': 'left'})

        self.remove_schedule_button = Button(self)
        self.remove_schedule_button['text'] = 'Remove \nSchedule'
        self.remove_schedule_button['command'] = schedule_end
        self.remove_schedule_button.pack({'side': 'left'})

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
