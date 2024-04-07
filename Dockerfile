FROM postgres:latest

# Переменная окружения для версии миграции
ENV MIGRATION_VERSION=latest
# Переменная окружения для количества записей
ENV NUM_RECORDS=1000000

# Копируем скрипт миграций в контейнер
COPY migrations /migrations

# Копируем скрипты для создания БД и запуска миграций
COPY init_scripts /docker-entrypoint-initdb.d