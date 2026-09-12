"""
Autonomous Git Workspace Operations for Nexus-Agent.
"""

import subprocess
import os
from typing import Optional, Type
from pydantic import BaseModel, Field

from nexus_agent.core.schema import ToolCategory
from nexus_agent.tools.base import BaseTool


class GitStatusTool(BaseTool):
    name = "git_status"
    description = "Check git repository status including staged, unstaged, and untracked files."
    category = ToolCategory.GIT

    def run(self) -> str:
        try:
            res = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, check=True)
            output = res.stdout.strip()
            return output if output else "Working tree clean. No changes detected."
        except subprocess.CalledProcessError as e:
            return f"Git error: {e.stderr}"
        except Exception as e:
            return f"Git error: {str(e)}"


class GitDiffInput(BaseModel):
    staged: bool = Field(False, description="View staged diff instead of unstaged")


class GitDiffTool(BaseTool):
    name = "git_diff"
    description = "Inspect git diff changes across the workspace."
    category = ToolCategory.GIT
    args_schema: Type[BaseModel] = GitDiffInput

    def run(self, staged: bool = False) -> str:
        cmd = ["git", "diff"]
        if staged:
            cmd.append("--cached")
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = res.stdout.strip()
            return output if output else "(No diff)"
        except Exception as e:
            return f"Git diff error: {str(e)}"


class GitCommitInput(BaseModel):
    message: str = Field(..., description="Commit message describing changes")
    add_all: bool = Field(True, description="Whether to stage all changes before committing")


class GitCommitTool(BaseTool):
    name = "git_commit"
    description = "Stage files and create a git commit."
    category = ToolCategory.GIT
    args_schema: Type[BaseModel] = GitCommitInput

    def run(self, message: str, add_all: bool = True) -> str:
        try:
            if add_all:
                subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
            res = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True, check=True)
            return f"Committed successfully:\n{res.stdout.strip()}"
        except subprocess.CalledProcessError as e:
            return f"Git commit failed: {e.stderr or e.stdout}"
        except Exception as e:
            return f"Git commit error: {str(e)}"
