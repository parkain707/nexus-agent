"""
Tests for Core Autonomous NexusAgent ReAct Loop, Self-Healing, and Loop Detector.
"""

import pytest
from nexus_agent.core.schema import AgentConfig, AgentStatus, ToolCall
from nexus_agent.core.llm import DeterministicMockProvider
from nexus_agent.core.agent import NexusAgent
from nexus_agent.tools import create_default_registry


def test_agent_react_execution_flow(tmp_path):
    config = AgentConfig(provider="mock", memory_db_path=str(tmp_path / "test_mem.db"))
    mock_llm = DeterministicMockProvider(config)

    target_file = str(tmp_path / "math_ops.py")

    # Script 3-step autonomous workflow:
    # 1. Write file
    mock_llm.add_scripted_turn(
        thought="Step 1: Create math_ops.py with a square function.",
        tool_call=ToolCall(
            id="c1",
            name="write_file",
            arguments={"path": target_file, "content": "def square(x):\n    return x * x\n"}
        ),
        content="Writing file"
    )
    # 2. Run verification command
    mock_llm.add_scripted_turn(
        thought="Step 2: Verify by testing math_ops.py.",
        tool_call=ToolCall(
            id="c2",
            name="execute_command",
            arguments={"command": f"python -c \"import sys; sys.path.append(r'{tmp_path}'); import math_ops; assert math_ops.square(4) == 16; print('VERIFIED')\""}
        ),
        content="Running verification test"
    )
    # 3. Final response (no tools)
    mock_llm.add_scripted_turn(
        thought="Step 3: All verification passed. Concluding mission.",
        tool_call=None,
        content="Successfully implemented and verified math_ops.py."
    )

    events_captured = []
    def callback(event_type, data):
        events_captured.append(event_type)

    agent = NexusAgent(config=config, llm_provider=mock_llm)
    agent.register_callback(callback)

    final_state = agent.run("Create square function and verify")

    assert final_state.status == AgentStatus.COMPLETED
    assert final_state.current_iteration == 3
    assert len(final_state.steps) == 3
    assert "Successfully implemented and verified" in final_state.final_output

    # Check telemetry events
    assert "thought" in events_captured
    assert "tool_call" in events_captured
    assert "tool_result" in events_captured
    assert "task_completed" in events_captured


def test_agent_loop_detection(tmp_path):
    config = AgentConfig(provider="mock", max_iterations=6, memory_db_path=str(tmp_path / "test_mem.db"))
    mock_llm = DeterministicMockProvider(config)

    # Script agent repeating the exact same tool call 4 times
    identical_call = ToolCall(id="repeat", name="list_dir", arguments={"path": "."})
    for i in range(5):
        mock_llm.add_scripted_turn(
            thought=f"Looping step {i}",
            tool_call=identical_call,
            content=""
        )

    reflections = []
    def cb(event, data):
        if event == "reflection":
            reflections.append(data)

    agent = NexusAgent(config=config, llm_provider=mock_llm)
    agent.register_callback(cb)
    state = agent.run("Do something in a loop")

    # Anti-loop detector should have caught it after 3 calls
    assert len(reflections) >= 1
    assert "Loop detected" in reflections[0]["warning"]
