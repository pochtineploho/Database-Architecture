#!/bin/bash

users="$(cat /config/env | grep "USERS" | awk -F '=' '{print $2}')"

psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "CREATE ROLE reader login password 'reader';"
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "CREATE ROLE writer login password 'writer';"
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "GRANT SELECT ON ALL TABLES in schema public TO reader;"
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "GRANT SELECT, UPDATE, INSERT ON ALL TABLES in schema public TO writer;"

psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "CREATE USER analytic password 'analytic';"
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "GRANT SELECT ON \"Products\" to analytic;"

psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "CREATE ROLE admin superuser nologin inherit;"
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "GRANT ALL PRIVILEGES ON ALL TABLES in schema public TO admin;"

psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "CREATE GROUP admins;"
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "GRANT admin TO admins;"

for user in $users
do
  psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "CREATE USER \"$user\" login password '$user';"
  psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "GRANT admins TO \"$user\";"
done
