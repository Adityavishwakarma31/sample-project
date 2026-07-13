#Flask + Postgres Docker Project

I took this Flask + Postgres app and ran it using Docker on an EC2 server.

Files in this project

app.py                 # the Flask app
requirements.txt       # python packages needed
Dockerfile             # used to build the Flask app image
docker-compose.yml     # used to run Flask and Postgres together

About the Dockerfile

The Dockerfile builds the Flask app into a Docker image. It:


Uses Python 3.11 as the base image
Sets up a working directory (/app)
Copies app.py and requirements.txt into the image
Installs the required Python packages using pip
Sets the database environment variables (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT)
Exposes port 5000
Runs the app with python app.py


About the docker-compose.yml

The compose file runs two services together:


web1 – builds and runs the Flask app, mapped to port 5000
db – runs a Postgres container, mapped to port 5432


I already set the DB environment variables inside the Dockerfile, so I didn't repeat them in the compose file. It still works fine because Compose picks up whatever is baked into the image.

DB_HOST=db works because Docker Compose lets both containers talk to each other using their service name.

About the network

I also added a custom Docker network (my-network) in the compose file so both containers can talk to each other on it.

Both web1 and db are connected to my-network.
The network itself is defined once at the bottom of the compose file, at the same level as services: — not inside it. This tripped me up at first, since if you indent it wrong (put it inside services:), Compose throws an error like services.networks additional properties 'my-network' not allowed.
I could have skipped this entirely — Compose creates a default network automatically if you don't specify one. But I added a custom network so I have a named network I can recognize and reuse if needed.

I already set the DB environment variables inside the Dockerfile, so I didn't repeat them in the compose file. It still works fine because Compose picks up whatever is baked into the image.

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
