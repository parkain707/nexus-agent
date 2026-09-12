"""
Unit tests for AST-Aware File Tools, Sandboxed Shell, Search, and Tool Registry.
"""

import os
import tempfile
import pytest
from pathlib import Path

from nexus_agent.tools.base import ToolRegistry
from nexus_agent.tools.file_ops import ReadFileTool, WriteFileTool, EditFileTool, ListDirTool
from nexus_agent.tools.shell_ops import ExecuteCommandTool
from nexus_agent.tools.code_search import GrepSearchTool, FindFilesTool
from nexus_agent.core.schema import ToolCall


def test_tool_registry_registration_and_schemas():
    registry = ToolRegistry()
    registry.register(ReadFileTool())
    registry.register(WriteFileTool())

    assert registry.get("read_file") is not None
    assert registry.get("non_existent") is None

    schemas = registry.get_schemas()
    assert len(schemas) == 2
    assert schemas[0]["function"]["name"] in ["read_file", "write_file"]


def test_file_ops_ast_validation(tmp_path):
    write_tool = WriteFileTool()
    read_tool = ReadFileTool()
    edit_tool = EditFileTool()

    target_py = str(tmp_path / "script.py")

    # 1. Valid python code
    valid_code = "def greet(name: str) -> str:\n    return f'Hello, {name}'\n"
    res = write_tool.run(path=target_py, content=valid_code)
    assert "Created new file" in res
    assert os.path.exists(target_py)

    # 2. Invalid python code -> AST Syntax Error
    invalid_code = "def broken(:\n    return False\n"
    with pytest.raises(ValueError) as exc:
        write_tool.run(path=target_py, content=invalid_code, validate_syntax=True)
    assert "AST Syntax Validation Failed" in str(exc.value)

    # 3. Read file with line numbering
    read_output = read_tool.run(path=target_py)
    assert "1 | def greet" in read_output

    # 4. Safe edit
    target_str = "return f'Hello, {name}'"
    replacement_str = "return f'Hi, {name}!'"
    edit_res = edit_tool.run(path=target_py, target_text=target_str, replacement_text=replacement_str)
    assert "Successfully edited" in edit_res

    # Check updated content
    updated_read = read_tool.run(path=target_py)
    assert "Hi, {name}!" in updated_read


def test_shell_command_sandbox_and_blacklist():
    shell_tool = ExecuteCommandTool()

    # 1. Benign command
    out = shell_tool.run("python -c \"print('nexus test')\"")
    assert "nexus test" in out
    assert "[Exit Code: 0]" in out

    # 2. Dangerous command blocked by Sentinel/Oracle guardrails
    with pytest.raises(PermissionError) as exc:
        shell_tool.run("rm -rf /")
    assert "Security Alert: Command was blocked" in str(exc.value)


def test_search_tools(tmp_path):
    # Create sample files
    f1 = tmp_path / "alpha.py"
    f1.write_text("def find_nexus_token(): pass", encoding="utf-8")
    f2 = tmp_path / "beta.txt"
    f2.write_text("random notes about something", encoding="utf-8")

    grep_tool = GrepSearchTool()
    find_tool = FindFilesTool()

    # Grep search
    grep_res = grep_tool.run(query="find_nexus_token", path=str(tmp_path))
    assert "alpha.py:1: def find_nexus_token(): pass" in grep_res

    # Find files
    find_res = find_tool.run(pattern="*.py", path=str(tmp_path))
    assert "alpha.py" in find_res
    assert "beta.txt" not in find_res


def test_diagram_tool():
    from nexus_agent.tools.diagram import GenerateDiagramTool
    diag = GenerateDiagramTool()
    out = diag.run(title="System Architecture", diagram_type="flowchart", mermaid_code="A[User] --> B[API]")
    assert "### [Architecture Diagram] System Architecture" in out
    assert "graph TD" in out
    assert "A[User] --> B[API]" in out

