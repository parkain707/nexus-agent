"""
Tests for Schema definitions and LLM Providers (Mock & Structured).
"""

import pytest
from nexus_agent.core.schema import (
    AgentConfig,
    AgentState,
    AgentStatus,
    Message,
    ToolCall,
    ToolResult,
    TaskStep
)
from nexus_agent.core.llm import DeterministicMockProvider, get_llm_provider


def test_schema_instantiation():
    config = AgentConfig(provider="mock", model="test-model", max_iterations=10)
    assert config.provider == "mock"
    assert config.max_iterations == 10

    state = AgentState(task_id="task_123", goal="Build something awesome")
    assert state.status == AgentStatus.IDLE
    assert len(state.steps) == 0

    tool_call = ToolCall(id="c1", name="write_file", arguments={"path": "a.txt", "content": "hi"})
    assert tool_call.name == "write_file"
    assert tool_call.arguments["path"] == "a.txt"


def test_mock_llm_provider_scripting():
    config = AgentConfig(provider="mock")
    mock_llm = DeterministicMockProvider(config)

    # Script custom turns
    mock_llm.add_scripted_turn(
        thought="First step: Plan",
        tool_call=ToolCall(id="c1", name="read_file", arguments={"path": "sample.py"}),
        content="Reading sample.py"
    )
    mock_llm.add_scripted_turn(
        thought="Second step: Done",
        tool_call=None,
        content="Mission Complete"
    )

    msgs = [Message(role="user", content="Inspect sample.py")]
    
    # Turn 1
    resp1 = mock_llm.generate(msgs)
    assert resp1["thought"] == "First step: Plan"
    assert len(resp1["tool_calls"]) == 1
    assert resp1["tool_calls"][0].name == "read_file"

    # Turn 2
    resp2 = mock_llm.generate(msgs)
    assert resp2["thought"] == "Second step: Done"
    assert len(resp2["tool_calls"]) == 0
    assert resp2["content"] == "Mission Complete"


def test_factory_llm_provider():
    config = AgentConfig(provider="mock")
    provider = get_llm_provider(config)
    assert isinstance(provider, DeterministicMockProvider)
