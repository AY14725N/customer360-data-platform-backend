FROM postgres:16-alpine
COPY sql/postgres/schema.sql /docker-entrypoint-initdb.d/01-schema.sql
COPY sql/postgres/indexes.sql /docker-entrypoint-initdb.d/02-indexes.sql
COPY sql/postgres/seed.sql /docker-entrypoint-initdb.d/03-seed.sql
