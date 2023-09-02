FROM python:3.10

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY main/ main/

ENTRYPOINT ["python3", "main/main.py"]