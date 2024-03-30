FROM postgres:latest

# Копируем скрипт миграций в контейнер
COPY migrations /migrations

# Копируем скрипт для запуссоздания БД и пользователя
COPY init.sh /docker-entrypoint-initdb.d/init.sh

# Копируем скрипт для запуска миграций
COPY run_migrations.sh /docker-entrypoint-initdb.d/run_migrations.sh

# Устанавливаем переменную окружения для версии миграции
ENV MIGRATION_VERSION=latest
