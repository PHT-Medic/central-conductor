FROM python:3.8

COPY requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt

# COPY app /home/app
# COPY run_conductor.py /home/run_conductor.py


CMD ["python", "/opt/run_conductor.py"]