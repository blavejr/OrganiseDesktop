import sys
import json
import os
from .cronController import schedule_end, schedule_start
from .organiseDesktop import undo, organise_desktop
from .duplicateCleaner import clean_duplicates  # Importing the duplicate cleaner

# Import Tkinter based on Python version
if sys.version_info >= (3,):
    from tkinter import *
    from tkinter import messagebox as tkMessageBox
else:
    from tkinter import *
    import tkMessageBox

# Get the directory of the current file
pwd = os.path.dirname(os.path.abspath(__file__))
# Load extensions from the JSON file
with open(os.path.join(pwd, 'Extension.json'), 'r') as ext_file:
    Extensions = json.load(ext_file)

folders = list(Extensions.keys())

class App(Frame):
    """Define the GUI for the desktop cleaner."""

    def clean(self):
        """Clean the desktop by organizing files with checked extensions."""
        checked_extensions = {x: Extensions[x] for x in folders}
        organise_desktop(checked_extensions)
        tkMessageBox.showinfo('Complete', 'Desktop clean finished.')

    def clean_duplicates_gui(self):
        """Clean duplicate files by using the duplicate cleaner."""
        directory = tkMessageBox.askdirectory(title="Select Directory to Clean Duplicates")
        if directory:
            clean_duplicates(directory)
            tkMessageBox.showinfo('Complete', 'Duplicate file cleanup finished.')

    def quit_all(self):
        """Exit the application."""
        sys.exit(0)

    def check(self, item):
        """Toggle the selection of a file extension."""
        if item in folders:
            folders.remove(item)
        else:
            folders.append(item)

    def on_schedule_start(self):
        """Start the scheduling process for organizing the desktop."""
        schedule_start(folders)

    def make_checkbutton(self, text):
        """Create a checkbutton for a file extension."""
        cb = Checkbutton(self, text=text, command=lambda: self.check(text))
        cb.select()  # Select the checkbutton by default
        cb.pack(side='top')
        return cb

    def make_button(self, text, command):
        """Create a button with the specified command."""
        btn = Button(self, text=text, command=command)
        btn.pack(side='left')
        return btn

    def create(self):
        """Create the GUI layout."""
        self.winfo_toplevel().title('Desktop Cleaner')

        # Create checkbuttons for each file extension
        for ext in sorted(Extensions.keys()):
            self.make_checkbutton(ext)

        # Create buttons and their respective functions
        buttons = {
            'Clean': self.clean,
            'Exit': self.quit_all,
            'Undo': undo,
            'Schedule': self.on_schedule_start,
            'Remove\nSchedule': schedule_end,
            'Clean\nDuplicates': self.clean_duplicates_gui  # Added button for cleaning duplicates
        }

        for key in buttons:
            self.make_button(key, buttons[key])

    def __init__(self, master=None):
        """Initialize the application."""
        Frame.__init__(self, master)
        self.pack()
        self.create()

def main():
    """Main function to run the application."""
    root = Tk()
    root.resizable(FALSE, FALSE)  # Make the application's size constant
    root.minsize(width=350, height=330)
    
    # Center the application window on the screen
    positionRight = int(root.winfo_screenwidth() / 2 - 350 / 2)
    positionDown = int(root.winfo_screenheight() / 2 - 330 / 2)
    root.geometry(f"+{positionRight}+{positionDown}")

    app = App(root)
    root.protocol('WM_DELETE_WINDOW', app.quit_all)
    app.mainloop()
    root.destroy()

if __name__ == '__main__':
    main()
