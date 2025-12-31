import logging
from database import engine
from migrations.versions import MIGRATIONS, CURRENT_VERSION

logger = logging.getLogger(__name__)


def run_migrations():
    """Execute all pending database migrations.

    Dynamically loads and executes migration modules in order, applying schema
    changes and other database modifications. Each migration is logged for
    tracking and debugging purposes.

    Raises:
        Exception: If any migration fails during execution, the exception is
                  logged and re-raised to halt the migration process.
    """
    logger.info(f"Running migrations up to version {CURRENT_VERSION}")

    for migration in MIGRATIONS:
        try:
            module_name = migration["module"]
            version = migration["version"]
            description = migration["description"]

            logger.info(f"Applying migration {version}: {description}")

            parts = module_name.split(".")
            module = __import__(module_name, fromlist=[parts[-1]])

            module.upgrade(engine)
            logger.info(f"✓ Migration {version} applied successfully")
        except Exception as e:
            logger.error(f"✗ Migration {version} failed: {e}")
            raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_migrations()
