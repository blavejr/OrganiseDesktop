__author__ = "Remigius Kalimba"
'''Add a timer so it does this automatically everyday at a set time'''

import pickle
import crontab as CronTab
import json
import os
import sys
from subprocess import call

import getpass

pwd = os.path.dirname(os.path.abspath(__file__))


def schedule_start(folders):
    '''
    Starts a schedule to organise the desktop once a day
    '''
    with open('./settings.txt', 'wb') as setting_file:
        pickle.dump(folders, setting_file)
    if sys.platform == 'darwin' or sys.platform == 'linux':
        my_cron = CronTab(user=getpass.getuser())
        job = my_cron.new(command=str(sys.executable + ' ' + pwd + "/cronCleanUp.py"),
                          comment="OrganiseDesktop")
        job.day.every(1)
        my_cron.write()
    else:
        if not os.path.isfile(pwd + "\\cronCleanUp.pyw"):
            call("copy " + pwd + "\\cronCleanUp.py " + pwd + "\\cronCleanUp.pyw", shell=True)
        call("SCHTASKS /Create /SC DAILY /TN OrganiseDesktop /TR " + pwd + "\\cronCleanUp.pyw /F",
             shell=True)


def schedule_end():
    '''
    Removes the schedule if one is defined
    '''
    os.remove("./settings.txt")
    if sys.platform == 'darwin' or sys.platform == 'linux':
        my_cron = CronTab(user=getpass.getuser())
        my_cron.remove_all(comment="OrganiseDesktop")
        my_cron.write()
    else:
        call("SCHTASKS /Delete /TN OrganiseDesktop /F",
                 shell=True)