
import os
import sqlite3
from pathlib import Path

DATABASE_NAME = os.getenv(
    "AI_DOCUMENTS_DB",
    str(Path(__file__).resolve().parents[1] / "documents.db"),
)


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                file_content BLOB NOT NULL,
                extracted_text TEXT NOT NULL,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Add the summary column to existing databases if it doesn't exist.
        columns = connection.execute(
            "PRAGMA table_info(documents)"
        ).fetchall()

        column_names = [column["name"] for column in columns]

        if "summary" not in column_names:
            connection.execute("""
                ALTER TABLE documents
                ADD COLUMN summary TEXT
            """)


def save_document(
    filename: str,
    file_type: str,
    file_size: int,
    file_content: bytes,
    extracted_text: str,
    summary: str | None = None,
):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO documents (
                filename,
                file_type,
                file_size,
                file_content,
                extracted_text,
                summary
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                file_type,
                file_size,
                file_content,
                extracted_text,
                summary,
            )
        )

        return cursor.lastrowid


def update_document_summary(document_id: int, summary: str):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE documents
            SET summary = ?
            WHERE id = ?
            """,
            (summary, document_id)
        )

def delete_document(document_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM documents WHERE id = ?",
            (document_id,)
        )

        return cursor.rowcount > 0
