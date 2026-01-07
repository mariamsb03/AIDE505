#!/usr/bin/env python
"""
Database migration script for FastAPI backend.
This script helps manage database migrations using Alembic.

Usage:
    python migrate.py init          - Initialize database (run all migrations)
    python migrate.py upgrade       - Apply all pending migrations
    python migrate.py downgrade     - Rollback last migration
    python migrate.py current       - Show current migration revision
    python migrate.py history       - Show migration history
    python migrate.py create "msg"  - Create a new migration
"""
import sys
import os
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv

load_dotenv()

def get_alembic_config():
    """Get Alembic configuration."""
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    return alembic_cfg

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command_name = sys.argv[1].lower()
    alembic_cfg = get_alembic_config()
    
    if command_name == "init":
        print("Running all migrations to initialize database...")
        command.upgrade(alembic_cfg, "head")
        print("Database initialized successfully!")
    
    elif command_name == "upgrade":
        if len(sys.argv) > 2:
            revision = sys.argv[2]
            print(f"Upgrading to revision: {revision}")
            command.upgrade(alembic_cfg, revision)
        else:
            print("Upgrading to head...")
            command.upgrade(alembic_cfg, "head")
        print("Upgrade completed!")
    
    elif command_name == "downgrade":
        if len(sys.argv) > 2:
            revision = sys.argv[2]
            print(f"Downgrading to revision: {revision}")
            command.downgrade(alembic_cfg, revision)
        else:
            print("Downgrading one revision...")
            command.downgrade(alembic_cfg, "-1")
        print("Downgrade completed!")
    
    elif command_name == "current":
        print("Current revision:")
        command.current(alembic_cfg)
    
    elif command_name == "history":
        print("Migration history:")
        command.history(alembic_cfg)
    
    elif command_name == "create":
        if len(sys.argv) < 3:
            print("Error: Please provide a migration message")
            print('Example: python migrate.py create "Add user roles table"')
            sys.exit(1)
        message = sys.argv[2]
        print(f"Creating new migration: {message}")
        command.revision(alembic_cfg, autogenerate=True, message=message)
        print("Migration created successfully!")
    
    else:
        print(f"Unknown command: {command_name}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()

