import Clean
import pickle
import os
import sys

separator = ""
if sys.platform == 'win32':
    separator = '\\'
else:
    separator = '/'
with open(os.path.dirname(os.path.abspath(__file__))+separator+'settings.txt', 'rb') as setting_file:
    folders = pickle.load(setting_file)

Clean.main(folders)
