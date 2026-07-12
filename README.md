# Flask + Postgres Docker Project

I made a Flask app and connected it with a Postgres database using Docker. Then I ran it on an EC2 server.

## Files in this project

```
app.py                 # my Flask app
requirements.txt       # python packages needed
Dockerfile             # to build the Flask app image
docker-compose.yml     # to run Flask and Postgres together
```

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV DB_HOST=db \
    DB_NAME=mydatabase \
    DB_USER=postgres \
    DB_PASSWORD=postgres \
    DB_PORT=5432

EXPOSE 5000

CMD ["python","app.py"]
```

## docker-compose.yml

```yaml
services:
  web1:
    build: .
    ports:
      - "5000:5000"

  db:
    image: postgres
    environment:
      - POSTGRES_DB=mydatabase
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
```

I already added the DB settings inside the Dockerfile using `ENV`, so I did not repeat them in the compose file. It still works fine.

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

## API Routes

- `GET /` → health check
- `GET /about` → project info
- `GET /messages` → shows all messages
- `POST /messages` → add a new message

## How I ran it on EC2

1. Wrote Dockerfile and docker-compose.yml on the EC2 server using vim.
2. `docker compose up` gave an error at first — the compose plugin was not installed.
3. Installed docker-compose manually:
   ```bash
   sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```
4. Since this is the standalone version, I run the command with a hyphen:
   ```bash
   docker-compose up
   ```
5. Opened port `5000` in the EC2 security group.
6. Checked `http://<EC2-PUBLIC-IP>:5000/` in the browser — it worked.

## Things to fix later

- Don't leave Postgres port `5432` open to the public.
- Turn off `debug=True` before using this in production.
