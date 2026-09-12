"""
Nexus-Agent: Next-Gen Autonomous AI Engineering Agent
Dual-Engine UX (Rich TUI + Cyberpunk Glassmorphism Web Dashboard),
Self-Healing AST Code Engine, ReAct Loop, and Multi-Tool Sandboxing.
"""

from nexus_agent.version import __version__
from nexus_agent.core.agent import NexusAgent
from nexus_agent.core.schema import AgentState, TaskStep, Message, ToolResult

__all__ = [
    "__version__",
    "NexusAgent",
    "AgentState",
    "TaskStep",
    "Message",
    "ToolResult",
]
