# Database

Database setup for Professor Sodabeh Imanzadeh's coursework.

## Files

| File | Description |
| --- | --- |
| `docker-compose.yml` | Docker Compose configuration for running PostgreSQL locally. |

## Run

From this directory:

```bash
docker compose up -d
```

Stop the service:

```bash
docker compose down
```

## Notes

- PostgreSQL is exposed on local port `5432`.
- Database data is stored in the local `postgres-data/` directory.
- Connection settings are defined in `docker-compose.yml`.
