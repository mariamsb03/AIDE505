# Docker Setup

This Dockerfile runs both the FastAPI backend and Flask frontend in a single container.

## Building the Docker Image

```bash
docker build -t auth-app .
```

## Running the Container

You need to provide the database connection string and other environment variables:

```bash
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:password@host:port/database \
  -e SECRET_KEY=your-secret-key \
  -e FLASK_SECRET_KEY=your-flask-secret-key \
  auth-app
```

### Example with PostgreSQL on localhost:

```bash
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/auth_db \
  -e SECRET_KEY=your-secret-key-change-in-production \
  -e FLASK_SECRET_KEY=your-flask-secret-key-change-in-production \
  auth-app
```

### Using environment file:

Create a `.env.docker` file:
```
DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/auth_db
SECRET_KEY=your-secret-key-change-in-production
FLASK_SECRET_KEY=your-flask-secret-key-change-in-production
```

Then run:
```bash
docker run -p 5000:5000 --env-file .env.docker auth-app
```

## Accessing the Application

- Frontend: http://localhost:5000
- Backend API: http://localhost:8000 (only accessible from within the container)

## Notes

- The container exposes only port 5000 (Flask frontend)
- The FastAPI backend runs on port 8000 but is only accessible from within the container
- Both applications communicate via localhost inside the container
- Make sure your database is accessible from the Docker container (use `host.docker.internal` for localhost databases on Windows/Mac)

## Database Setup

Before running the container, make sure:
1. Your PostgreSQL database is running
2. The database exists (create it if needed)
3. Run migrations to set up the schema:

```bash
# If you need to run migrations, you can exec into the container
docker exec -it <container_id> bash
cd /app/fastapi_backend
python migrate.py init
```

