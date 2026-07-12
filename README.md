# Flask + Postgres Docker Project

I took this Flask + Postgres app and ran it using Docker on an EC2 server.

## Files in this project

```
app.py                 # my Flask app
requirements.txt       # python packages needed
Dockerfile             # to build the Flask app image
compose.yml     # to run Flask and Postgres together
```

## Environment Variables

| Variable      | Value         |
|---------------|---------------|
| `DB_HOST`     | `db`          |
| `DB_NAME`     | `mydatabase`  |
| `DB_USER`     | `postgres`    |
| `DB_PASSWORD` | `postgres`    |
| `DB_PORT`     | `5432`        |

`DB_HOST=db` works because Docker Compose lets the two containers talk to each other using their service name.

## Dependencies

```
flask==3.0.0
psycopg2-binary==2.9.9
```
