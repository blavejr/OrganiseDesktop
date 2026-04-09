__author__ = "Remigius Kalimba"
"""Add a timer so it does this automatically everyday at a set time"""
import pickle, os, sys, getpass
from crontab import CronTab
from subprocess import call

pwd = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(pwd, "settings.txt")


def schedule_start(folders):
    """Starts a schedule to organise the desktop once a day"""
    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        cron = CronTab(user=getpass.getuser())
        job = cron.new(
            command=f'"{sys.executable}" "{os.path.join(pwd,"cronCleanUp.py")}"',
            comment="OrganiseDesktop",
        )
        job.day.every(1)
        cron.write()
    else:
        if not os.path.isfile(pwd + "\\cronCleanUp.pyw"):
            call(f'copy "{pwd}\\cronCleanUp.py" "{pwd}\\cronCleanUp.pyw"', shell=True)

        call(
            f'SCHTASKS /Create /SC DAILY /TN OrganiseDesktop /TR "{pwd}\\cronCleanUp.pyw" /F'
        )


def schedule_end():
    """Removes the schedule if one is defined"""

    os.remove(settings_path)

    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        my_cron = CronTab(user=getpass.getuser())
        my_cron.remove_all(comment="OrganiseDesktop")
        my_cron.write()

    else:
        call("SCHTASKS /Delete /TN OrganiseDesktop /F", shell=True)
