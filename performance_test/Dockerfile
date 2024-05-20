FROM python:3.9-slim

WORKDIR /src

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "performance_test.py"]