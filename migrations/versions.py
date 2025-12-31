CURRENT_VERSION = "1.0.1"

MIGRATIONS = [
    {
        "version": "1.0.0",
        "description": "Initial schema creation",
        "module": "migrations.001_initial_schema",
    },
    {
        "version": "1.0.1",
        "description": "Add database indexes for query optimization",
        "module": "migrations.002_add_indexes",
    },
]
