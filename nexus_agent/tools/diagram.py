"""
Architecture and Workflow Diagram Generator Tool for Nexus-Agent.
Generates Mermaid.js and ASCII visual representations of codebases and execution flows.
"""

from typing import Optional, Type
from pydantic import BaseModel, Field

from nexus_agent.core.schema import ToolCategory
from nexus_agent.tools.base import BaseTool


class GenerateDiagramInput(BaseModel):
    title: str = Field(..., description="Diagram title")
    diagram_type: str = Field("flowchart", description="'flowchart', 'sequence', 'classDiagram', or 'stateDiagram'")
    mermaid_code: str = Field(..., description="Valid Mermaid.js graph specification")
    description: Optional[str] = Field(None, description="Brief explanation of the architecture")


class GenerateDiagramTool(BaseTool):
    name = "generate_diagram"
    description = "Generate an architecture or system workflow diagram in Mermaid.js specification."
    category = ToolCategory.CUSTOM
    args_schema: Type[BaseModel] = GenerateDiagramInput

    def run(self, title: str, diagram_type: str, mermaid_code: str, description: Optional[str] = None) -> str:
        clean_code = mermaid_code.strip()
        if not clean_code.startswith("graph") and not clean_code.startswith(diagram_type):
            if diagram_type == "flowchart":
                clean_code = f"graph TD\n{clean_code}"
            else:
                clean_code = f"{diagram_type}\n{clean_code}"

        output = [
            f"### [Architecture Diagram] {title}",
            "",
            "```mermaid",
            clean_code,
            "```",
        ]
        if description:
            output.extend(["", f"**Explanation**: {description}"])

        return "\n".join(output)
