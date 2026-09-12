"""
End-to-End Autonomous Coding & Self-Healing Integration Test (Agent 4: Sentinel).
Simulates a real-world software engineering workflow:
1. Agent plans and creates code with an intentional edge-case bug.
2. Agent creates test suite and executes test runner.
3. Test fails -> Self-healing loop triggers!
4. Agent edits code to fix the bug.
5. Agent verifies with test suite -> 100% PASS.
6. Agent concludes mission.
"""

import sys
from pathlib import Path
import pytest

from nexus_agent.core.schema import AgentConfig, AgentStatus, ToolCall
from nexus_agent.core.llm import DeterministicMockProvider
from nexus_agent.core.agent import NexusAgent


def test_e2e_autonomous_coding_and_self_healing(tmp_path):
    config = AgentConfig(
        provider="mock",
        max_iterations=10,
        memory_db_path=str(tmp_path / "e2e_memory.db")
    )
    mock_llm = DeterministicMockProvider(config)

    src_file = str(tmp_path / "string_tools.py")
    test_file = str(tmp_path / "test_strings.py")

    # Step 1: Write string_tools.py (with buggy palindrome check that is case-sensitive)
    buggy_code = (
        "def is_palindrome(s: str) -> bool:\n"
        "    return s == s[::-1]\n"
    )
    mock_llm.add_scripted_turn(
        thought="Step 1: Write the initial string_tools.py module.",
        tool_call=ToolCall(
            id="e2e_1",
            name="write_file",
            arguments={"path": src_file, "content": buggy_code}
        ),
        content="Writing initial string_tools.py"
    )

    # Step 2: Write test_strings.py (expects case-insensitive palindrome like 'Racecar')
    test_code = (
        f"import sys; sys.path.insert(0, r'{tmp_path}')\n"
        "from string_tools import is_palindrome\n\n"
        "def test_cases():\n"
        "    assert is_palindrome('radar') == True\n"
        "    assert is_palindrome('Racecar') == True, 'Failed case-insensitive check'\n"
        "    print('ALL_TESTS_PASSED')\n\n"
        "if __name__ == '__main__':\n"
        "    test_cases()\n"
    )
    mock_llm.add_scripted_turn(
        thought="Step 2: Write verification test suite.",
        tool_call=ToolCall(
            id="e2e_2",
            name="write_file",
            arguments={"path": test_file, "content": test_code}
        ),
        content="Writing test_strings.py"
    )

    # Step 3: Run the test suite -> Will fail with AssertionError!
    mock_llm.add_scripted_turn(
        thought="Step 3: Execute the test suite.",
        tool_call=ToolCall(
            id="e2e_3",
            name="execute_command",
            arguments={"command": f"python \"{test_file}\""}
        ),
        content="Running tests"
    )

    # Step 4: Self-Healing! Edit string_tools.py to fix case sensitivity
    mock_llm.add_scripted_turn(
        thought="Step 4: Self-Healing Triggered: Test failed on case-insensitivity. Patching is_palindrome.",
        tool_call=ToolCall(
            id="e2e_4",
            name="edit_file",
            arguments={
                "path": src_file,
                "target_text": "return s == s[::-1]",
                "replacement_text": "clean = s.lower()\n    return clean == clean[::-1]"
            }
        ),
        content="Patching string_tools.py"
    )

    # Step 5: Re-run tests -> Success!
    mock_llm.add_scripted_turn(
        thought="Step 5: Re-running test suite after self-healing patch.",
        tool_call=ToolCall(
            id="e2e_5",
            name="execute_command",
            arguments={"command": f"python \"{test_file}\""}
        ),
        content="Re-running tests"
    )

    # Step 6: Conclude mission
    mock_llm.add_scripted_turn(
        thought="Step 6: All tests pass. Autonomous engineering task complete.",
        tool_call=None,
        content="Successfully created string_tools, diagnosed failing test, self-healed, and verified 100% test pass rate."
    )

    agent = NexusAgent(config=config, llm_provider=mock_llm)
    final_state = agent.run("Build and verify string_tools with self-healing")

    assert final_state.status == AgentStatus.COMPLETED
    assert final_state.current_iteration == 6
    assert "Successfully created string_tools" in final_state.final_output

    # Check that the file was indeed patched and works
    with open(src_file, "r") as f:
        patched_code = f.read()
    assert "clean = s.lower()" in patched_code
