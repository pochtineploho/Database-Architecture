FROM python:latest

COPY . .

RUN apt-get update
RUN apt upgrade
RUN apt install dirmngr ca-certificates software-properties-common apt-transport-https lsb-release curl -y
RUN curl -fSsL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | tee /usr/share/keyrings/postgresql.gpg > /dev/null
RUN echo deb [arch=amd64,arm64,ppc64el signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main | tee /etc/apt/sources.list.d/postgresql.list
RUN apt update
RUN apt install -y postgresql-client-16

CMD python -u src/backup_script.py

