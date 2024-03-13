# File: Makefile
install:
    # python3 -m venv venv  // check dulu apakah menggunakan python atau python3 di cmd
    python -m venv .venv
    pip install flask keras tensorflow

run:
    .venv\Scripts\activate
    python run.py