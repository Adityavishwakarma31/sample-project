# Flask + Postgres App

Ek Flask application jo Postgres database ke saath data store karta hai. Environment variables se DB config leta hai — Docker image aur run/compose setup khud manage karo.

## Files

```
app.py              # Flask application (DB logic ke saath)
requirements.txt    # Python dependencies
```

## Environment Variables

App yeh environment variables expect karta hai (agar nahi diye, toh defaults use honge):

| Variable      | Default       | Description              |
|---------------|---------------|---------------------------|
| `DB_HOST`     | `db`          | Postgres container ka host/name |
| `DB_NAME`     | `mydatabase`  | Database ka naam          |
| `DB_USER`     | `postgres`    | Database user              |
| `DB_PASSWORD` | `postgres`    | Database password          |
| `DB_PORT`     | `5432`        | Postgres port               |

## Dependencies

```
flask==3.0.0
psycopg2-binary==2.9.9
```

## App kaise kaam karta hai

- Startup pe `init_db()` chalta hai jo `messages` table create karta hai (agar exist nahi karti)
- DB connect karne mein retry logic hai (5 attempts, 3 sec gap) — isse Postgres container thoda late start ho toh bhi Flask crash nahi hoga

## API Endpoints

### `GET /`
Health check.
```json
{ "message": "Hello from Flask running inside Docker! 🐳", "status": "success" }
```

### `GET /about`
Project info.

### `GET /messages`
Sab messages fetch karta hai database se.
```json
{ "messages": [ { "id": 1, "content": "hello", "created_at": "2026-07-13 ..." } ] }
```

### `POST /messages`
Naya message insert karta hai.

Request body:
```json
{ "content": "your message here" }
```

Response:
```json
{ "id": 2, "content": "your message here", "status": "created" }
```

## Notes for image/compose setup

- App `psycopg2-binary` use karta hai, isliye DB service Postgres image (jaise `postgres:16-alpine`) ka hona chahiye
- App port `5000` par run hota hai (`app.run(host='0.0.0.0', port=5000)`)
- DB service ka naam (`DB_HOST` env var mein) waisa hi rakhna jo docker network/compose mein service ka naam ho
