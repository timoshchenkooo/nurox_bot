#!/bin/bash

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install --no-use-pep517 -r requirements.txt
