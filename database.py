
import sqlite3
import uuid
from datetime import datetime, timezone

DB_NAME = "scar_tissue.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id TEXT PRIMARY KEY,
                service TEXT NOT NULL,
                description TEXT NOT NULL,
                observations TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS outcomes (
                id TEXT PRIMARY KEY,
                incident_id TEXT NOT NULL,
                action_attempted TEXT NOT NULL,
                outcome_status TEXT NOT NULL,
                observed_result TEXT,
                confirmed_cause TEXT,
                recorded_at TEXT NOT NULL,
                memory_sync_status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (incident_id)
                    REFERENCES incidents(id),
                CHECK (
                    outcome_status IN (
                        'Failed',
                        'Temporary relief',
                        'Resolved',
                        'Unknown'
                    )
                ),
                CHECK (
                    memory_sync_status IN (
                        'pending',
                        'saved',
                        'failed'
                    )
                )
            )
        """)


def create_incident(service, description, observations):
    incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
    created_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO incidents
            (id, service, description, observations, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            incident_id,
            service,
            description,
            observations,
            created_at
        ))

    return incident_id


def save_outcome(
    incident_id,
    action_attempted,
    outcome_status,
    observed_result,
    confirmed_cause=""
):
    outcome_id = f"OUT-{uuid.uuid4().hex[:8].upper()}"
    recorded_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO outcomes (
                id,
                incident_id,
                action_attempted,
                outcome_status,
                observed_result,
                confirmed_cause,
                recorded_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            outcome_id,
            incident_id,
            action_attempted,
            outcome_status,
            observed_result,
            confirmed_cause,
            recorded_at
        ))

    return outcome_id


def get_incident(incident_id):
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM incidents
            WHERE id = ?
        """, (incident_id,)).fetchone()


def get_outcomes(incident_id):
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM outcomes
            WHERE incident_id = ?
            ORDER BY recorded_at DESC
        """, (incident_id,)).fetchall()


def update_memory_status(outcome_id, status):
    if status not in ("pending", "saved", "failed"):
        raise ValueError("Invalid memory sync status")

    with get_connection() as conn:
        conn.execute("""
            UPDATE outcomes
            SET memory_sync_status = ?
            WHERE id = ?
        """, (status, outcome_id))
