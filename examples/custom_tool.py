"""
Custom Tool Example: Extending Nexus-Agent with domain-specific tools.
"""

from pydantic import BaseModel, Field
from nexus_agent import NexusAgent
from nexus_agent.core.schema import AgentConfig, ToolCategory
from nexus_agent.tools import BaseTool, create_default_registry


# 1. Define input parameters using standard Pydantic
class DatabaseQueryInput(BaseModel):
    query: str = Field(..., description="SQL query string")
    max_records: int = Field(5, description="Max rows to return")


# 2. Inherit BaseTool and implement run()
class DatabaseQueryTool(BaseTool):
    name = "query_database"
    description = "Execute a read-only SQL query against the internal analytics database."
    category = ToolCategory.CUSTOM
    args_schema = DatabaseQueryInput

    def run(self, query: str, max_records: int = 5) -> str:
        # Custom logic (e.g. Postgres / SQLite / BigQuery)
        return f"[MOCK DB RESPONSE] Executed '{query}'. Returned {max_records} rows successfully."


def main():
    # 3. Register your custom tool into the default arsenal
    registry = create_default_registry()
    registry.register(DatabaseQueryTool())

    # 4. Initialize agent with the customized registry
    agent = NexusAgent(config=AgentConfig(provider="mock"), registry=registry)

    # 5. The agent will now automatically see the tool schema and can call it!
    print("Registered tools:", [t.name for t in registry.list_tools()])


if __name__ == "__main__":
    main()
