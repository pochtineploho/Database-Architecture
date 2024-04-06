#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
	CREATE USER docker CREATEDB;
EOSQL

psql -v ON_ERROR_STOP=1 --username "docker" <<-EOSQL
	CREATE DATABASE flowwow;
EOSQL

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
	GRANT ALL PRIVILEGES ON DATABASE flowwow to docker;
EOSQL

su -c '/migrations/run_migrations.sh' docker
