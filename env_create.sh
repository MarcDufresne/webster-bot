#!/usr/bin/env bash
export PIPENV_VENV_IN_PROJECT=True
pipenv install --dev --ignore-hashes --three --python python3.6
pipenv run pip install -e `dirname $0`
