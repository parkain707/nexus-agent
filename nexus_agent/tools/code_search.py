"""
Code and File Search Tools for Nexus-Agent.
Supports ripgrep-style regex matching and filename glob search.
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Type
from pydantic import BaseModel, Field

from nexus_agent.core.schema import ToolCategory
from nexus_agent.tools.base import BaseTool


class GrepSearchInput(BaseModel):
    query: str = Field(..., description="Text or regex to search for")
    path: str = Field(".", description="Directory or file path to search within")
    file_pattern: Optional[str] = Field(None, description="Optional glob filter e.g. '*.py'")
    case_sensitive: bool = Field(False, description="Case-sensitive match")


class GrepSearchTool(BaseTool):
    name = "grep_search"
    description = "Search for text or regex patterns across files with line numbers."
    category = ToolCategory.SEARCH
    args_schema: Type[BaseModel] = GrepSearchInput

    def run(self, query: str, path: str = ".", file_pattern: Optional[str] = None, case_sensitive: bool = False) -> str:
        base_path = Path(path)
        if not base_path.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            regex = re.compile(query, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex query '{query}': {str(e)}")

        matches = []
        files_to_check = []

        if base_path.is_file():
            files_to_check.append(base_path)
        else:
            for root, dirs, files in os.walk(base_path):
                dirs[:] = [d for d in dirs if d not in [".git", ".venv", "__pycache__", "node_modules"]]
                for file in files:
                    p = Path(root) / file
                    if file_pattern and not p.match(file_pattern):
                        continue
                    files_to_check.append(p)

        for p in files_to_check:
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if regex.search(line):
                            rel_p = p.relative_to(base_path) if not base_path.is_file() else p.name
                            matches.append(f"{rel_p}:{line_num}: {line.strip()}")
                            if len(matches) >= 50:
                                matches.append("... [Output truncated at 50 matches]")
                                return "\n".join(matches)
            except Exception:
                continue

        return "\n".join(matches) if matches else f"No matches found for '{query}'."


class FindFilesInput(BaseModel):
    pattern: str = Field(..., description="Glob pattern e.g. '*.py' or '*agent*'")
    path: str = Field(".", description="Root directory to search")


class FindFilesTool(BaseTool):
    name = "find_files"
    description = "Locate files matching a glob pattern across directories."
    category = ToolCategory.SEARCH
    args_schema: Type[BaseModel] = FindFilesInput

    def run(self, pattern: str, path: str = ".") -> str:
        base_path = Path(path)
        if not base_path.exists():
            raise FileNotFoundError(f"Path not found: {path}")

        results = []
        for root, dirs, files in os.walk(base_path):
            dirs[:] = [d for d in dirs if d not in [".git", ".venv", "__pycache__", "node_modules"]]
            for file in files:
                p = Path(root) / file
                if p.match(pattern):
                    results.append(str(p.relative_to(base_path)))
                    if len(results) >= 50:
                        results.append("... [Truncated at 50 files]")
                        return "\n".join(results)

        return "\n".join(results) if results else f"No files matching pattern '{pattern}' found."
