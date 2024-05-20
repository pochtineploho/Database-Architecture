FROM python:3.9-slim

RUN apt-get update && apt-get install -y postgresql-client

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "backup_script.py"]