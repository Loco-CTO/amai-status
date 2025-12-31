import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.models import Base

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///./status.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables and run migrations.

    Creates all database tables based on SQLAlchemy models and executes
    pending migrations to ensure database schema is up to date.

    Raises:
        Exception: If migrations fail.
    """
    Base.metadata.create_all(bind=engine)

    try:
        from migrate import run_migrations

        logger.info("Running database migrations...")
        run_migrations()
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise
