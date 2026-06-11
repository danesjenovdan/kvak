# Kvak

## Deployment with docker compose

Configure environment:

- copy `.env.example` to `.env`
- set values in `.env` file

Create location for persistend data on disk:

```sh
# assuming you did not change the location in .env
mkdir -p persistent-data/kvak-storage
mkdir -p persistent-data/postgres-data
```

Build the app:

```sh
docker compose -f compose.prod.yaml build
```

Start services with docker compose:

```sh
docker compose -f compose.prod.yaml up
```

Import a database dump:

```sh
# DELETE ALL DATA IN THE DATABASE
docker container exec -i $(docker compose ps -q db) psql -U kvak kvak -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# IMPORT FROM db.dump
docker container exec -i $(docker compose ps -q db) psql -U kvak kvak < db.dump
```
