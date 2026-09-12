"""
Base Tool Interface and Tool Registry for Nexus-Agent.
Enforces Pydantic validation and anti-hallucination execution safeguards.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type
import inspect
import time
from pydantic import BaseModel, create_model

from nexus_agent.core.schema import ToolCategory, ToolResult, ToolCall


class BaseTool(ABC):
    """Abstract base class for all agent tools."""

    name: str
    description: str
    category: ToolCategory = ToolCategory.CUSTOM
    args_schema: Optional[Type[BaseModel]] = None

    @abstractmethod
    def run(self, **kwargs) -> str:
        """Run the tool logic and return output string."""
        pass

    def execute(self, call_id: str, arguments: Dict[str, Any]) -> ToolResult:
        """Execute with argument validation and performance timing."""
        start_time = time.time()
        try:
            # Validate with schema if provided
            if self.args_schema:
                validated_args = self.args_schema(**arguments)
                output = self.run(**validated_args.model_dump())
            else:
                output = self.run(**arguments)

            elapsed = round(time.time() - start_time, 4)
            return ToolResult(
                tool_call_id=call_id,
                name=self.name,
                success=True,
                output=str(output),
                error=None,
                metadata={"execution_time_sec": elapsed, "category": self.category.value}
            )
        except Exception as e:
            elapsed = round(time.time() - start_time, 4)
            return ToolResult(
                tool_call_id=call_id,
                name=self.name,
                success=False,
                output="",
                error=f"Error executing {self.name}: {type(e).__name__}: {str(e)}",
                metadata={"execution_time_sec": elapsed, "category": self.category.value}
            )

    def to_schema(self) -> Dict[str, Any]:
        """Convert tool to OpenAI/Gemini standard function calling schema."""
        properties = {}
        required = []

        if self.args_schema:
            schema = self.args_schema.model_json_schema()
            properties = schema.get("properties", {})
            required = schema.get("required", [])

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }


class ToolRegistry:
    """Registry maintaining available tools for the agent."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list_tools(self) -> List[BaseTool]:
        return list(self._tools.values())

    def get_schemas(self) -> List[Dict[str, Any]]:
        return [tool.to_schema() for tool in self._tools.values()]

    def execute(self, tool_call: ToolCall) -> ToolResult:
        tool = self.get(tool_call.name)
        if not tool:
            return ToolResult(
                tool_call_id=tool_call.id,
                name=tool_call.name,
                success=False,
                output="",
                error=f"Tool '{tool_call.name}' not found in registry. Available tools: {list(self._tools.keys())}"
            )
        return tool.execute(tool_call.id, tool_call.arguments)
