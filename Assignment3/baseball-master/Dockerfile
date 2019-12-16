FROM postgres:10-alpine

COPY database-setup.sql /docker-entrypoint-initdb.d/1-setup.sql
COPY baseball-postgres.sql /docker-entrypoint-initdb.d/2-load.sql
COPY baseball-users.sql /docker-entrypoint-initdb.d/3-users.sql
