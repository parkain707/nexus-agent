"""
Core Pydantic Schema and Type Definitions for Nexus-Agent.
Enforces strict schema validation (Oracle Anti-Hallucination Guard).
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    REVIEW_REQUESTED = "review_requested"
    COMPLETED = "completed"
    FAILED = "failed"


class ToolCategory(str, Enum):
    FILE = "file"
    SHELL = "shell"
    GIT = "git"
    SEARCH = "search"
    CUSTOM = "custom"


class Message(BaseModel):
    role: str = Field(..., description="'system', 'user', 'assistant', or 'tool'")
    content: str = Field(..., description="Text content of the message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    id: str = Field(..., description="Unique call ID")
    name: str = Field(..., description="Name of the tool being called")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Parsed arguments")


class ToolResult(BaseModel):
    tool_call_id: str = Field(..., description="Matching ToolCall ID")
    name: str = Field(..., description="Tool name")
    success: bool = Field(..., description="True if executed without unhandled errors")
    output: str = Field(..., description="String output, stdout, or result summary")
    error: Optional[str] = Field(None, description="Error message or stderr if failed")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TaskStep(BaseModel):
    step_number: int
    thought: str = Field(..., description="CoT (Chain of Thought) reasoning")
    action_type: str = Field(..., description="'tool_call', 'reflection', or 'final_response'")
    tool_call: Optional[ToolCall] = None
    observation: Optional[str] = None
    status: AgentStatus = AgentStatus.EXECUTING
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentState(BaseModel):
    task_id: str
    goal: str
    status: AgentStatus = AgentStatus.IDLE
    current_iteration: int = 0
    max_iterations: int = 25
    steps: List[TaskStep] = Field(default_factory=list)
    final_output: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AgentConfig(BaseModel):
    provider: str = Field(default="mock", description="LLM provider: mock, openai, anthropic, gemini, ollama, deepseek")
    model: str = Field(default="mock-model")
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_iterations: int = Field(default=25, ge=1, le=100)
    workspace_dir: str = Field(default=".")
    enable_ast_validation: bool = True
    enable_human_in_the_loop: bool = False
    memory_db_path: str = Field(default="nexus_memory.db")
