#!/usr/bin/env bash
export PIPENV_VENV_IN_PROJECT=True
pipenv uninstall --all
rm -rf `dirname $0`/.venv
