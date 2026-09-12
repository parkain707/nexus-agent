"""
Tests for FastAPI Web Mission Control server and endpoints.
"""

from fastapi.testclient import TestClient
from nexus_agent.ui.web.server import app

client = TestClient(app)


def test_web_status_endpoint():
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data


def test_web_tools_endpoint():
    response = client.get("/api/tools")
    assert response.status_code == 200
    tools = response.json()
    assert isinstance(tools, list)
    assert len(tools) >= 5
    tool_names = [t["name"] for t in tools]
    assert "read_file" in tool_names
    assert "write_file" in tool_names
    assert "execute_command" in tool_names


def test_web_run_endpoint():
    payload = {
        "goal": "Write a hello world script",
        "provider": "mock",
        "max_iterations": 3
    }
    response = client.post("/api/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "started"


def test_web_chat_endpoint():
    payload = {
        "message": "안녕하세요",
        "session_id": "test_chat_session",
        "provider": "mock"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Nexus-Agent" in data["reply"]

