"""
Tests for Working Memory and SQLite Persistent Knowledge & Reflection Store.
"""

import os
import tempfile
import pytest
from nexus_agent.core.memory import WorkingMemory, PersistentKnowledgeStore


def test_working_memory_sliding_window():
    mem = WorkingMemory(max_messages=5)
    mem.add_message("system", "You are an agent.")
    for i in range(10):
        mem.add_message("user", f"Message {i}")

    messages = mem.get_messages()
    assert len(messages) == 5
    # The system prompt should remain preserved at the head
    assert messages[0].role == "system"
    assert messages[0].content == "You are an agent."
    # The latest messages should be present
    assert messages[-1].content == "Message 9"


def test_persistent_knowledge_and_reflection():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_db = f.name

    try:
        store = PersistentKnowledgeStore(db_path=temp_db)

        # 1. Test Knowledge recording & retrieval
        store.record_knowledge("repo_lang", "Python 3.10", category="convention")
        val = store.get_knowledge("repo_lang")
        assert val == "Python 3.10"

        # Update knowledge
        store.record_knowledge("repo_lang", "Python 3.12", category="convention")
        assert store.get_knowledge("repo_lang") == "Python 3.12"

        items = store.list_knowledge(category="convention")
        assert len(items) == 1
        assert items[0]["key"] == "repo_lang"

        # 2. Test Reflection Journal
        store.record_reflection(
            task_id="t_001",
            error_signature="ZeroDivisionError",
            root_cause="Divided by zero without checking denominator",
            remedy="Added `if b == 0: raise ValueError(...)`"
        )

        recalled = store.recall_reflections("ZeroDivision")
        assert len(recalled) == 1
        assert recalled[0]["error_signature"] == "ZeroDivisionError"
        assert "Divided by zero" in recalled[0]["root_cause"]

    finally:
        if os.path.exists(temp_db):
            os.remove(temp_db)
