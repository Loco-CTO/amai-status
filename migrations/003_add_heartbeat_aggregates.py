"""Description: Add heartbeat_aggregates table for precomputed interval buckets."""

from sqlalchemy import text


def upgrade(engine):
    """Apply migration - create aggregate table and indexes."""
    with engine.connect() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS heartbeat_aggregates (
                    id INTEGER PRIMARY KEY,
                    monitor_name VARCHAR NOT NULL,
                    interval VARCHAR NOT NULL,
                    bucket_start DATETIME NOT NULL,
                    count INTEGER NOT NULL DEFAULT 0,
                    down_count INTEGER NOT NULL DEFAULT 0,
                    degraded_count INTEGER NOT NULL DEFAULT 0,
                    response_sample_count INTEGER NOT NULL DEFAULT 0,
                    avg_response_time FLOAT,
                    issue_percentage FLOAT NOT NULL DEFAULT 0,
                    status VARCHAR NOT NULL DEFAULT 'up',
                    is_up BOOLEAN NOT NULL DEFAULT 1,
                    updated_at DATETIME NOT NULL,
                    CONSTRAINT uq_heartbeat_aggregate UNIQUE (monitor_name, interval, bucket_start)
                )
                """
            )
        )

        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_heartbeat_aggregate_lookup "
                "ON heartbeat_aggregates(monitor_name, interval, bucket_start DESC)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_heartbeat_aggregate_interval_bucket "
                "ON heartbeat_aggregates(interval, bucket_start DESC)"
            )
        )
        connection.commit()


def downgrade(engine):
    """Revert migration - drop aggregate table and indexes."""
    with engine.connect() as connection:
        connection.execute(text("DROP INDEX IF EXISTS idx_heartbeat_aggregate_lookup"))
        connection.execute(
            text("DROP INDEX IF EXISTS idx_heartbeat_aggregate_interval_bucket")
        )
        connection.execute(text("DROP TABLE IF EXISTS heartbeat_aggregates"))
        connection.commit()
