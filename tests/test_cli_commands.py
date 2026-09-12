"""
Tests for CLI commands: tools, bench, and version.
"""

from click.testing import CliRunner
from nexus_agent.ui.cli import main


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.output


def test_cli_tools():
    runner = CliRunner()
    result = runner.invoke(main, ["tools"])
    assert result.exit_code == 0
    assert "read_file" in result.output
    assert "write_file" in result.output


def test_cli_bench():
    runner = CliRunner()
    result = runner.invoke(main, ["bench"])
    assert result.exit_code == 0
    assert "GRADE: S+" in result.output
    assert "AST Syntax Engine" in result.output


def test_cli_radar():
    runner = CliRunner()
    result = runner.invoke(main, ["radar"])
    assert result.exit_code == 0
    assert "GROWTH & STARGAZER RADAR" in result.output
    assert "GitHub Stars" in result.output

