FROM python:3.7-slim

# Устанавливаем необходимые пакеты
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    libyaml-dev \
    build-essential \
    wget \
    curl \
    gnupg

# Устанавливаем pip зависимости
RUN pip install --no-cache-dir \
    psycopg2-binary \
    patroni[etcd] \
    PyYAML

# Удаляем лишние пакеты, чтобы уменьшить размер образа
RUN apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем конфигурационный файл patroni.yml в контейнер
COPY patroni_master.yml /etc/patroni_master.yml
COPY patroni_replica_1.yml /etc/patroni_replica_1.yml
COPY patroni_replica_2.yml /etc/patroni_replica_2.yml

# Команда по умолчанию для запуска Patroni
CMD ["patroni", "/etc/patroni_master.yml"]