FROM python:latest

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

CMD python -u src/backup_script.py

