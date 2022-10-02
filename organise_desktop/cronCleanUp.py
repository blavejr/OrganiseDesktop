import Clean
import pickle
import os
import sys

separator = ""
if sys.platform == 'win64':
    separator = '\\'
else:
    separator = '/'
with open(os.path.dirname(os.path.join(os.path.abspath(__file__), 'settings.txt'), 'rb')) as setting_file:
    folders = pickle.load(setting_file)

Clean.main(folders)
