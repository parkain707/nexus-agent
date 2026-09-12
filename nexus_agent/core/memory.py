"""
Hierarchical Memory Architecture for Nexus-Agent.
Includes Working Context Buffer (short-term) and SQLite Persistent Knowledge & Mistake Journal (long-term).
"""

import sqlite3
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from nexus_agent.core.schema import Message


class WorkingMemory:
    """Token-aware sliding window working memory."""

    def __init__(self, max_messages: int = 40):
        self.max_messages = max_messages
        self.messages: List[Message] = []

    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        msg = Message(role=role, content=content, metadata=metadata or {})
        self.messages.append(msg)
        if len(self.messages) > self.max_messages:
            # Preserve the initial system message and prune oldest user/assistant interactions
            sys_msg = self.messages[0] if self.messages and self.messages[0].role == "system" else None
            kept = self.messages[-self.max_messages:]
            if sys_msg and kept[0].role != "system":
                kept = [sys_msg] + kept[1:]
            self.messages = kept

    def get_messages(self) -> List[Message]:
        return list(self.messages)

    def clear(self):
        self.messages.clear()


class PersistentKnowledgeStore:
    """
    SQLite persistent storage for long-term project knowledge and self-reflection mistakes.
    Allows agents to recall lessons learned across executions.
    """

    def __init__(self, db_path: str = "nexus_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    category TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reflection_journal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    error_signature TEXT NOT NULL,
                    root_cause TEXT NOT NULL,
                    remedy TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def record_knowledge(self, key: str, value: str, category: str = "general"):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO knowledge_items (key, value, category, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                    value=excluded.value,
                    category=excluded.category,
                    updated_at=CURRENT_TIMESTAMP
            """, (key, value, category))
            conn.commit()

    def get_knowledge(self, key: str) -> Optional[str]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM knowledge_items WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None

    def list_knowledge(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute("SELECT key, value, category, updated_at FROM knowledge_items WHERE category = ?", (category,))
            else:
                cursor.execute("SELECT key, value, category, updated_at FROM knowledge_items")
            rows = cursor.fetchall()
            return [{"key": r[0], "value": r[1], "category": r[2], "updated_at": r[3]} for r in rows]

    def record_reflection(self, task_id: str, error_signature: str, root_cause: str, remedy: str):
        """Record a mistake and remedy to prevent repeating errors."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reflection_journal (task_id, error_signature, root_cause, remedy)
                VALUES (?, ?, ?, ?)
            """, (task_id, error_signature, root_cause, remedy))
            conn.commit()

    def recall_reflections(self, keyword: str) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT task_id, error_signature, root_cause, remedy, created_at
                FROM reflection_journal
                WHERE error_signature LIKE ? OR root_cause LIKE ?
                ORDER BY id DESC LIMIT 5
            """, (f"%{keyword}%", f"%{keyword}%"))
            rows = cursor.fetchall()
            return [
                {
                    "task_id": r[0],
                    "error_signature": r[1],
                    "root_cause": r[2],
                    "remedy": r[3],
                    "created_at": r[4]
                }
                for r in rows
            ]
