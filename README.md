# OrganiseDesktop

Takes all the files on your desktop and put them in folders according to extensions. NO MORE MESSY DESKTOPS!
At least not on the outside :)

# Slack Channel invite link
Feel free to join the channel and contribute, if you have already had a PR merged please join the [channel](https://join.slack.com/t/organisedesktop/shared_invite/enQtMzA2NTI2MTI0MzY4LWRlOWRjOGM0YTJmYjFiZGU3ZTUzM2M0MTA2N2U3MzljMmFhNGIyODlmZDg2N2E1Y2EwOWFiZjcxMzYzYjcyMTk).

# Getting Started

The setup file isn't yet setup up properly (work in progress). To run the program download
the repo and install the required packages then run the Clean.py file.

# Prerequisites
All the necessary packages are mentioned in requirements.txt. They can be installed by
running `pip install -r requirements.txt` or using ``pipenv install`` and it will be automatically detect the `requirements.txt` and setup an enviroment for you. For development purposes, I suggest you create a
virtual environment ore use a dependency manager like [pipenv](https://github.com/pypa/pipenv)
 to keep a clear state, separate from your own setup.
The activate.sh script has been provided to ensure a standard development environment. To create the environment if it doesn't already exist, or simply load it otherwise, run `source ./activate.sh`

You can also use docker in combination with pipenv, [here](https://github.com/dfederschmidt/docker-pipenv-sample) you have an example.

If you do not want to create a virtual environment, just run the pip command above and ignore the following. Otherwise, the activate.sh script will handle the creation and loading of the virtual environment with all the necessary dependencies. Furthermore, once a new dependency is established, remove requirements.txt and please run `pip freeze > requirements.txt` to generate a new file that should be commited to version control.

Python3 Instructions:
`python -m venv organise_desktop`

To activate it, run `source organise_desktop/bin/activate`

### Build from Source

`$ git clone https://github.com/blavejr/OrganiseDesktop.git`
Navigate to the repo and run the following command:
`$ pip install -r requirements.txt`
