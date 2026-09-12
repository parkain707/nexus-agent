"""
Tools module initialization and factory.
"""

from nexus_agent.tools.base import BaseTool, ToolRegistry
from nexus_agent.tools.file_ops import ReadFileTool, WriteFileTool, EditFileTool, ListDirTool
from nexus_agent.tools.shell_ops import ExecuteCommandTool
from nexus_agent.tools.code_search import GrepSearchTool, FindFilesTool
from nexus_agent.tools.git_ops import GitStatusTool, GitDiffTool, GitCommitTool
from nexus_agent.tools.web_search import WebFetchTool, WebSearchTool
from nexus_agent.tools.diagram import GenerateDiagramTool


def create_default_registry() -> ToolRegistry:
    """Create and register all built-in standard tools."""
    registry = ToolRegistry()
    registry.register(ReadFileTool())
    registry.register(WriteFileTool())
    registry.register(EditFileTool())
    registry.register(ListDirTool())
    registry.register(ExecuteCommandTool())
    registry.register(GrepSearchTool())
    registry.register(FindFilesTool())
    registry.register(GitStatusTool())
    registry.register(GitDiffTool())
    registry.register(GitCommitTool())
    registry.register(WebFetchTool())
    registry.register(WebSearchTool())
    registry.register(GenerateDiagramTool())
    return registry


__all__ = [
    "BaseTool",
    "ToolRegistry",
    "create_default_registry",
    "ReadFileTool",
    "WriteFileTool",
    "EditFileTool",
    "ListDirTool",
    "ExecuteCommandTool",
    "GrepSearchTool",
    "FindFilesTool",
    "GitStatusTool",
    "GitDiffTool",
    "GitCommitTool",
    "WebFetchTool",
    "WebSearchTool",
    "GenerateDiagramTool",
]
