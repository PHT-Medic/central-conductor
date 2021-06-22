FROM python:3.8

COPY requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt
COPY setup_scripts/wait-for-it.sh /wait-for-it.sh

COPY . /home/conductor
RUN pip install /home/conductor


CMD ["python", "/home/conductor/conductor/run_conductor.py"]