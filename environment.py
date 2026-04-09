# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os


def setup_environment():

    if sys.version_info < (3, 6):
        print("Python 3.6 or higher is required...")
        sys.exit(1)
    with open("README.md", encoding="utf-8") as f:
        longd = f.read()

    base_path = os.path.dirname(os.path.abspath(__file__))
    ext_path = os.path.join(base_path, "organise_desktop", "Extension.json")
    if __name__ == "__main__":
        setup(
            name="OrganiseDesktop",
            include_package_data=True,
            packages=find_packages(),
            data_files=[("OrganiseDesktop", [ext_path])],
            entry_points={
                "console_scripts": ["organise_desktop = organise_desktop.Cli:main"]
            },
            install_requires=[
                "BeautifulSoup4",
                "requests",
                "colorama",
                "Py-stackExchange",
                "urwid",
                "crontab",
            ],
            requires=[
                "os",
                "getpass",
                "time",
                "sys",
                "tkinter",
            ],
            version="1.0",
            url="https://github.com/blavejr/OrganiseDesktop.git",
            keywords="Desktop Organiser",
            license="MIT",
            author="Remigius Kalimba",
            author_email="kalimbatech@gmail.com",
            description="Organise your desktop with one click.",
            long_description="\n\n{}".format(longd),
        )
