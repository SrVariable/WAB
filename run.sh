#!/bin/bash

export DISPLAY=:0
set -xe

source $HOME/GitRepos/wab/.venv/bin/activate
timeout 600 $HOME/GitRepos/wab/.venv/bin/python3 $HOME/GitRepos/wab/main.py >> $HOME/ObsidianVault/Wordle.md
deactivate
