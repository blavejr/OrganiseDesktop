import Clean
import pickle
import os
import sys

# Determine the file path separator based on the operating system
separator = ""
if sys.platform == 'win32':
    separator = '\\'
else:
    separator = '/'

# Correctly open the settings file using the right file path
settings_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.txt')
with open(settings_file_path, 'rb') as setting_file:
    folders = pickle.load(setting_file)

# Call the main function from the Clean module with the loaded folders
Clean.main(folders)
