FROM python:latest

COPY external_libs.txt ./

RUN pip install -r external_libs.txt

CMD python -u src/generation.py