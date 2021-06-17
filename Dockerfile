FROM python:3.8

COPY requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt

COPY . /home/conductor
RUN pip install /home/conductor


CMD ["python", "/home/conductor/conductor/run_conductor.py"]