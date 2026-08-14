FROM postgres:16-alpine
COPY sql/postgres/schema.sql /docker-entrypoint-initdb.d/01-schema.sql
COPY sql/postgres/crm_staging.sql /docker-entrypoint-initdb.d/02-crm-staging.sql
COPY sql/postgres/indexes.sql /docker-entrypoint-initdb.d/03-indexes.sql
COPY sql/postgres/seed.sql /docker-entrypoint-initdb.d/04-seed.sql
