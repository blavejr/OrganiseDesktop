__author__ = "Remigius Kalimba"
"""Add a timer so it does this automatically every day at a set time"""

import pickle
import os
import sys
import getpass
from subprocess import call
from crontab import CronTab

pwd = os.path.dirname(os.path.abspath(__file__))


def schedule_start(folders):
    """Starts a schedule to organize the desktop once a day"""

    # Save the folder settings
    with open('./settings.txt', 'wb') as setting_file:
        pickle.dump(folders, setting_file)

    # Schedule the job based on the operating system
    if sys.platform in ['darwin', 'linux']:
        my_cron = CronTab(user=getpass.getuser())
        
        # Create a new cron job
        job = my_cron.new(command=f"{sys.executable} {pwd}/cronCleanUp.py", comment='OrganiseDesktop')
        
        # Set the job to run every day at a specific time (e.g., 2:00 AM)
        job.setall("0 2 * * *")  # This sets the time to 2:00 AM every day
        
        my_cron.write()
    else:  # For Windows
        # Copy the script if it doesn't exist
        if not os.path.isfile(os.path.join(pwd, 'cronCleanUp.pyw')):
            call(f'copy {os.path.join(pwd, "cronCleanUp.py")} {os.path.join(pwd, "cronCleanUp.pyw")}', shell=True)

        # Create a new scheduled task
        call(f'SCHTASKS /Create /SC DAILY /TN OrganiseDesktop /TR "{os.path.join(pwd, "cronCleanUp.pyw")}" /F',
             shell=True)


def schedule_end():
    """Removes the schedule if one is defined"""

    # Remove the settings file
    if os.path.isfile('./settings.txt'):
        os.remove('./settings.txt')
    
    # Remove the scheduled job based on the operating system
    if sys.platform in ['darwin', 'linux']:
        my_cron = CronTab(user=getpass.getuser())
        my_cron.remove_all(comment='OrganiseDesktop')
        my_cron.write()
    else:  # For Windows
        call('SCHTASKS /Delete /TN OrganiseDesktop /F', shell=True)
