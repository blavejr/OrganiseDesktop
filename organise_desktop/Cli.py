import argparse
from organiseDesktop import organise_desktop
from organiseDesktop import undo
from cronController import schedule_start, schedule_end
import os
import json

pwd = os.path.dirname(os.path.abspath(__file__))
Extensions = json.load(open(pwd+'/Extension.json'))
folders = [x for x in Extensions]

#Define command line options
parser = argparse.ArgumentParser(description='Provides a command line tool to organise your desktop')
sp = parser.add_subparsers()
sp_organize = sp.add_parser('clean', help='Organises your desktop')
sp_undo = sp.add_parser('undo', help='Restores your desktop after it was organised')
sp_schedule = sp.add_parser('schedule', help='Schedules time to organise your desktop once a day')
sp_remove_schedule = sp.add_parser('remove-schedule', help='Removes scheduled time to organize')

#schedule command only works with all extension atm
def schedule():
    schedule_start(folders)


#Define the function of the command line option
sp_organize.set_defaults(func=organise_desktop)
sp_undo.set_defaults(func=undo)
sp_schedule.set_defaults(func=schedule)
sp_remove_schedule.set_defaults(func=schedule_end)

args = parser.parse_args()
args.func()
