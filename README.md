# Flask + Postgres App

A Flask application that stores data using a Postgres database. Configuration is handled entirely through environment variables — building the Docker image and writing the run/compose setup is up to you.

## Files

```
app.py              # Flask application (with DB logic)
requirements.txt    # Python dependencies
```

## Environment Variables

The app expects the following environment variables (defaults are used if not provided):

| Variable      | Default       | Description                  |
|---------------|---------------|-------------------------------|
| `DB_HOST`     | `db`          | Postgres container host/name |
| `DB_NAME`     | `mydatabase`  | Database name                 |
| `DB_USER`     | `postgres`    | Database user                 |
| `DB_PASSWORD` | `postgres`    | Database password             |
| `DB_PORT`     | `5432`        | Postgres port                 |

## Dependencies

```
flask==3.0.0
psycopg2-binary==2.9.9
```

## How the app works

- On startup, `init_db()` runs and creates the `messages` table if it doesn't already exist
- The DB connection has built-in retry logic (5 attempts, 3 second delay) — this prevents Flask from crashing if the Postgres container takes a bit longer to start

## API Endpoints

### `GET /`
Health check.
```json
{ "message": "Hello from Flask running inside Docker! 🐳", "status": "success" }
```

### `GET /about`
Project info.

### `GET /messages`
Fetches all messages from the database.
```json
{ "messages": [ { "id": 1, "content": "hello", "created_at": "2026-07-13 ..." } ] }
```

### `POST /messages`
Inserts a new message.

Request body:
```json
{ "content": "your message here" }
```

Response:
```json
{ "id": 2, "content": "your message here", "status": "created" }
```

## Notes for image/compose setup

- The app uses `psycopg2-binary`, so the DB service must be a Postgres image (e.g. `postgres:16-alpine`)
- The app binds to `0.0.0.0` on port `5000` (`app.run(host='0.0.0.0', port=5000)`) — this means it will be directly accessible from an EC2 instance's public IP with no extra config needed
- The DB service name (used in the `DB_HOST` env var) should match whatever service name you use in your Docker network/compose file

## Running on EC2

- **Security Group**: Make sure the EC2 instance's security group has an inbound rule for port `5000` (or whichever port you map) — Custom TCP, port 5000, source `0.0.0.0/0` or your own IP
- **Postgres port (`5432`)**: If you're also exposing the DB container's port on the host, don't make it public — keep it accessible only via the internal Docker network to the app container, otherwise your database will be exposed to the internet
- Access the app at: `http://<EC2-PUBLIC-IP>:5000/`
- If `debug=True` is left on in production, consider removing it — it's only safe for development
