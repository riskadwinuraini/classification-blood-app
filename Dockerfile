FROM python:3.10-slim-buster
WORKDIR /srv
COPY . /srv

COPY requirements.txt /srv

RUN python -m pip install --upgrade pip 
RUN pip install --force-reinstall -r requirements.txt
RUN pip cache purge


CMD ["python","run.py"]
