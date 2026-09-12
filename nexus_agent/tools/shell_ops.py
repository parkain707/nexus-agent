"""
Sandboxed Shell Command Execution Tool for Nexus-Agent.
Includes strict security blacklisting and execution timeout guardrails.
"""

import subprocess
import os
import re
from typing import Optional, Type
from pydantic import BaseModel, Field

from nexus_agent.core.schema import ToolCategory
from nexus_agent.tools.base import BaseTool


DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+[/~]",
    r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:",  # Fork bomb
    r"mkfs",
    r"dd\s+if=/dev/zero",
    r"format\s+[c-zC-Z]:",
    r"del\s+/[sS]\s+/[qQ]\s+[cC]:\\",
    r">\s*/dev/sda",
    r"shutdown",
    r"reboot",
]


class ExecuteCommandInput(BaseModel):
    command: str = Field(..., description="Shell command line to execute")
    cwd: Optional[str] = Field(None, description="Working directory for the command")
    timeout_seconds: int = Field(30, description="Max execution duration before timeout")


class ExecuteCommandTool(BaseTool):
    name = "execute_command"
    description = "Execute a shell command with security validation and timeout protection."
    category = ToolCategory.SHELL
    args_schema: Type[BaseModel] = ExecuteCommandInput

    def run(self, command: str, cwd: Optional[str] = None, timeout_seconds: int = 30) -> str:
        # Security blacklist check
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                raise PermissionError(f"Security Alert: Command was blocked due to dangerous pattern match: '{command}'")

        work_dir = cwd if cwd and os.path.exists(cwd) else os.getcwd()

        try:
            process = subprocess.run(
                command,
                shell=True,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                errors="replace"
            )

            stdout = process.stdout.strip()
            stderr = process.stderr.strip()
            exit_code = process.returncode

            output_lines = [f"[Exit Code: {exit_code}]"]
            if stdout:
                output_lines.append(f"[STDOUT]\n{stdout}")
            if stderr:
                output_lines.append(f"[STDERR]\n{stderr}")

            if exit_code != 0:
                return "\n".join(output_lines)

            return "\n".join(output_lines) if (stdout or stderr) else f"[Exit Code: {exit_code}] (No output)"

        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Command timed out after {timeout_seconds} seconds: '{command}'")
        except Exception as e:
            raise RuntimeError(f"Failed to execute command '{command}': {str(e)}")
