FROM postgres:latest

# Устанавливаем переменную окружения для версии миграции
ENV MIGRATION_VERSION=latest

# Копируем скрипт миграций в контейнер
COPY migrations /migrations

# Копируем скрипты для создания БД и запуска миграций
COPY init_script /docker-entrypoint-initdb.d