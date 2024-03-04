# File: Makefile
install:
    python3 -m venv venv
    . venv/bin/activate
    pip install flask keras tensorflow

run:
    . venv/bin/activate
    python run.py