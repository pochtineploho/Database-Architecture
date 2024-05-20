FROM python:latest

RUN apt-get update && apt-get install -y postgresql-client

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "backup_script.py"]