# Database Migrations

This FastAPI project uses Alembic for database migrations.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure your `.env` file has the correct database credentials.

3. Initialize the database (run all migrations):
```bash
python migrate.py init
```

## Migration Commands

### Initialize Database
Run all migrations to set up the database:
```bash
python migrate.py init
```

### Upgrade Database
Apply all pending migrations:
```bash
python migrate.py upgrade
```

Upgrade to a specific revision:
```bash
python migrate.py upgrade <revision_id>
```

### Downgrade Database
Rollback the last migration:
```bash
python migrate.py downgrade
```

Rollback to a specific revision:
```bash
python migrate.py downgrade <revision_id>
```

### Check Current Revision
See which migration is currently applied:
```bash
python migrate.py current
```

### View Migration History
See all available migrations:
```bash
python migrate.py history
```

### Create New Migration
Create a new migration from model changes:
```bash
python migrate.py create "Your migration message"
```

## Direct Alembic Commands

You can also use Alembic commands directly:

```bash
# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Create migration
alembic revision --autogenerate -m "Your message"

# Check current
alembic current

# View history
alembic history
```

## Migration Files

Migrations are stored in the `alembic/versions/` directory. Each migration file contains:
- `upgrade()`: Applies the migration
- `downgrade()`: Reverses the migration

## Notes

- Always test migrations in a development environment first
- Never edit existing migration files that have been applied to production
- Create new migrations for schema changes instead of modifying existing ones

