"""
AST-Aware File Operations Tools for Nexus-Agent.
Performs pre-validation of Python syntax using AST before writing or editing files,
preventing broken code from being committed.
"""

import os
import ast
import difflib
from pathlib import Path
from typing import Optional, Type
from pydantic import BaseModel, Field

from nexus_agent.core.schema import ToolCategory
from nexus_agent.tools.base import BaseTool


class ReadFileInput(BaseModel):
    path: str = Field(..., description="Path to the file to read")
    start_line: Optional[int] = Field(None, description="Optional 1-indexed starting line number")
    end_line: Optional[int] = Field(None, description="Optional 1-indexed ending line number")


class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Read file contents with optional line range slicing."
    category = ToolCategory.FILE
    args_schema: Type[BaseModel] = ReadFileInput

    def run(self, path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not file_path.is_file():
            raise IsADirectoryError(f"Path is a directory, not a file: {path}")

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        total_lines = len(lines)
        if start_line is not None or end_line is not None:
            s = max(1, start_line or 1) - 1
            e = min(total_lines, end_line or total_lines)
            selected = lines[s:e]
            numbered = [f"{i + s + 1:4d} | {line}" for i, line in enumerate(selected)]
            return "".join(numbered)
        else:
            numbered = [f"{i + 1:4d} | {line}" for i, line in enumerate(lines)]
            return "".join(numbered)


class WriteFileInput(BaseModel):
    path: str = Field(..., description="Path to the file to write")
    content: str = Field(..., description="Complete text content to write into the file")
    validate_syntax: bool = Field(True, description="Validate Python AST syntax if writing a .py file")


class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Write or overwrite a file with AST syntax pre-validation for Python code."
    category = ToolCategory.FILE
    args_schema: Type[BaseModel] = WriteFileInput

    def run(self, path: str, content: str, validate_syntax: bool = True) -> str:
        file_path = Path(path)
        
        # AST syntax pre-validation if Python file
        if validate_syntax and file_path.suffix.lower() == ".py":
            try:
                ast.parse(content, filename=str(file_path))
            except SyntaxError as syn_err:
                raise ValueError(
                    f"AST Syntax Validation Failed for '{path}' on line {syn_err.lineno}: {syn_err.msg}\n"
                    f"Code line: {syn_err.text}"
                )

        # Create parent directories
        file_path.parent.mkdir(parents=True, exist_ok=True)

        is_new = not file_path.exists()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        line_count = len(content.splitlines())
        byte_count = len(content.encode("utf-8"))
        action = "Created new" if is_new else "Updated existing"
        return f"{action} file '{path}' ({line_count} lines, {byte_count} bytes) successfully."


class EditFileInput(BaseModel):
    path: str = Field(..., description="Target file path")
    target_text: str = Field(..., description="Exact substring in target file to replace")
    replacement_text: str = Field(..., description="New replacement text")


class EditFileTool(BaseTool):
    name = "edit_file"
    description = "Replace a precise block of text in an existing file with AST verification."
    category = ToolCategory.FILE
    args_schema: Type[BaseModel] = EditFileInput

    def run(self, path: str, target_text: str, replacement_text: str) -> str:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            original = f.read()

        if target_text not in original:
            raise ValueError(f"Target text was not found in '{path}'. Please inspect the file contents first.")

        occurrences = original.count(target_text)
        if occurrences > 1:
            raise ValueError(
                f"Target text appears {occurrences} times in '{path}'. Must match a unique single block."
            )

        new_content = original.replace(target_text, replacement_text, 1)

        # AST syntax check for Python files
        if file_path.suffix.lower() == ".py":
            try:
                ast.parse(new_content, filename=str(file_path))
            except SyntaxError as syn_err:
                raise ValueError(
                    f"AST Syntax Validation Failed after edit on line {syn_err.lineno}: {syn_err.msg}"
                )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        # Generate diff summary
        diff = list(difflib.unified_diff(
            original.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
            n=2
        ))
        diff_summary = "".join(diff[:20])

        # Record Time-Travel snapshot
        try:
            from nexus_agent.core.memory import PersistentKnowledgeStore
            snap_id = PersistentKnowledgeStore().record_snapshot(path, original, new_content, diff_summary)
            snap_note = f"\n[Time-Travel Snapshot #{snap_id} created - reversible at any time]"
        except Exception:
            snap_note = ""

        return f"Successfully edited '{path}'.{snap_note}\nDiff:\n{diff_summary}"


class ListDirInput(BaseModel):
    path: str = Field(".", description="Directory path to list")
    recursive: bool = Field(False, description="Whether to recurse into subdirectories")


class ListDirTool(BaseTool):
    name = "list_dir"
    description = "List entries in a directory with file sizes and type details."
    category = ToolCategory.FILE
    args_schema: Type[BaseModel] = ListDirInput

    def run(self, path: str = ".", recursive: bool = False) -> str:
        dir_path = Path(path)
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {path}")

        results = []
        if recursive:
            for root, dirs, files in os.walk(dir_path):
                # skip git and venv
                dirs[:] = [d for d in dirs if d not in [".git", ".venv", "__pycache__", "node_modules"]]
                for file in files:
                    full_p = Path(root) / file
                    rel_p = full_p.relative_to(dir_path)
                    sz = full_p.stat().st_size
                    results.append(f"[FILE] {rel_p} ({sz} bytes)")
        else:
            for item in sorted(dir_path.iterdir()):
                if item.name.startswith((".", "__")):
                    continue
                if item.is_dir():
                    count = len(list(item.iterdir())) if item.is_dir() else 0
                    results.append(f"[DIR]  {item.name}/ ({count} items)")
                else:
                    results.append(f"[FILE] {item.name} ({item.stat().st_size} bytes)")

        return "\n".join(results) if results else "(Empty directory)"
