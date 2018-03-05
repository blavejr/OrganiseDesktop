#!/bin/bash

load_env () {
  source organise_desktop_env/bin/activate
  export TEST_DIR="$PWD/virtual_desktop"
}

if [ -d organise_desktop_env ]; then
  load_env
else
  pip install virtualenv
  virtualenv organise_desktop_env
  mkdir virtual_desktop
  load_env
  if [ $? ]; then
    pip install -r requirements.txt
  else
    echo "Loading the environment has failed"
  fi
fi
