"""
NexusAgent: Core Autonomous ReAct & Self-Healing Agent Engine.
Coordinates planning, execution, tool invocation, error recovery, and reflection.
"""

import uuid
from typing import Callable, List, Optional
from datetime import datetime

from nexus_agent.core.schema import (
    AgentConfig,
    AgentState,
    AgentStatus,
    Message,
    TaskStep,
    ToolCall,
    ToolResult,
)
from nexus_agent.core.llm import BaseLLMProvider, get_llm_provider
from nexus_agent.core.memory import WorkingMemory, PersistentKnowledgeStore
from nexus_agent.tools.base import ToolRegistry
from nexus_agent.tools import create_default_registry


SYSTEM_PROMPT_TEMPLATE = """You are Nexus-Agent, an elite autonomous software engineering AI agent.
Your objective is to solve tasks with extreme precision, self-verification, and robust error recovery.

Capabilities and Guardrails:
1. ReAct Loop: For each step, think through your plan (Chain-of-Thought) and select the optimal tool.
2. Self-Healing: If a tool execution fails or a command fails, inspect stderr, understand the root cause, and apply a fix.
3. Quality First: Verify your changes by running tests or reading modified files before concluding.
4. Conclude: When the goal is completely achieved, provide a comprehensive final response without calling any tools.

Available tools will be provided via the tool schema.
"""


class NexusAgent:
    """The central autonomous agent runner."""

    def __init__(
        self,
        config: Optional[AgentConfig] = None,
        registry: Optional[ToolRegistry] = None,
        llm_provider: Optional[BaseLLMProvider] = None,
    ):
        self.config = config or AgentConfig()
        self.registry = registry or create_default_registry()
        self.llm = llm_provider or get_llm_provider(self.config)
        self.working_memory = WorkingMemory(max_messages=40)
        self.persistent_store = PersistentKnowledgeStore(db_path=self.config.memory_db_path)

        # Event callbacks for CLI and Web streaming
        self.callbacks: List[Callable[[str, dict], None]] = []

    def register_callback(self, cb: Callable[[str, dict], None]):
        """Register listener for real-time telemetry events."""
        self.callbacks.append(cb)

    def _emit(self, event_type: str, data: dict):
        for cb in self.callbacks:
            try:
                cb(event_type, data)
            except Exception:
                pass

    def run(self, goal: str) -> AgentState:
        """Execute a goal autonomously end-to-end."""
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        state = AgentState(
            task_id=task_id,
            goal=goal,
            status=AgentStatus.PLANNING,
            max_iterations=self.config.max_iterations,
        )

        self._emit("state_update", state.model_dump())

        # Initialize working memory with system and user goal
        self.working_memory.clear()
        self.working_memory.add_message("system", SYSTEM_PROMPT_TEMPLATE)
        self.working_memory.add_message("user", f"Target Goal:\n{goal}")

        tool_schemas = self.registry.get_schemas()
        previous_tool_signatures = []

        while state.current_iteration < state.max_iterations:
            state.current_iteration += 1
            step_num = state.current_iteration

            # 1. Ask LLM for next thought and action
            state.status = AgentStatus.PLANNING
            self._emit("status_change", {"status": state.status.value, "step": step_num})

            llm_response = self.llm.generate(
                messages=self.working_memory.get_messages(),
                tools_schema=tool_schemas,
            )

            thought = llm_response.get("thought", "")
            tool_calls = llm_response.get("tool_calls", [])
            content = llm_response.get("content", "")

            self._emit("thought", {"step": step_num, "thought": thought})

            # 2. Check if agent concluded without tools
            if not tool_calls:
                state.status = AgentStatus.COMPLETED
                state.final_output = content or "Task completed successfully."
                step = TaskStep(
                    step_number=step_num,
                    thought=thought,
                    action_type="final_response",
                    observation=state.final_output,
                    status=state.status,
                )
                state.steps.append(step)
                self._emit("task_completed", {"final_output": state.final_output})
                break

            # 3. Execute Tool Calls
            state.status = AgentStatus.EXECUTING
            for tc in tool_calls:
                # Anti-loop detection guard
                sig = f"{tc.name}:{sorted(tc.arguments.items())}"
                previous_tool_signatures.append(sig)
                if previous_tool_signatures.count(sig) >= 3:
                    # Loop detected! Break loop and reflect
                    state.status = AgentStatus.REFLECTING
                    warning_msg = f"Loop detected: Tool '{tc.name}' called with identical arguments 3 times. Stopping repeated call."
                    self._emit("reflection", {"warning": warning_msg})
                    self.working_memory.add_message(
                        "user",
                        f"System Notice: You are repeating the exact same tool call '{tc.name}'. Please reconsider your strategy."
                    )
                    continue

                self._emit("tool_call", {"step": step_num, "tool": tc.model_dump()})
                result = self.registry.execute(tc)
                self._emit("tool_result", {"step": step_num, "result": result.model_dump()})

                # Record step
                obs = result.output if result.success else f"Tool execution failed: {result.error}"
                step = TaskStep(
                    step_number=step_num,
                    thought=thought,
                    action_type="tool_call",
                    tool_call=tc,
                    observation=obs,
                    status=AgentStatus.EXECUTING if result.success else AgentStatus.REFLECTING,
                )
                state.steps.append(step)

                # If failed, trigger self-healing reflection
                if not result.success:
                    state.status = AgentStatus.REFLECTING
                    self.persistent_store.record_reflection(
                        task_id=task_id,
                        error_signature=tc.name,
                        root_cause=result.error or "Unknown error",
                        remedy="Self-healing prompt injected"
                    )
                    self.working_memory.add_message(
                        "tool",
                        f"Observation (FAILURE): {result.error}\nPlease diagnose the failure, reflect on the cause, and self-heal in the next step."
                    )
                else:
                    self.working_memory.add_message(
                        "tool",
                        f"Observation (SUCCESS):\n{result.output}"
                    )

            state.updated_at = datetime.utcnow()
            self._emit("state_update", state.model_dump())

        # Check if exceeded max iterations
        if state.status != AgentStatus.COMPLETED:
            state.status = AgentStatus.FAILED
            state.error = f"Agent reached maximum iterations ({state.max_iterations}) without completing goal."
            self._emit("task_failed", {"error": state.error})

        return state
