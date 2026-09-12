"""
Web Search and Web Fetch Tools for Nexus-Agent.
Enables agents to retrieve real-time documentation and inspect online resources.
"""

import re
from typing import Optional, Type
from pydantic import BaseModel, Field
import httpx

from nexus_agent.core.schema import ToolCategory
from nexus_agent.tools.base import BaseTool


class WebFetchInput(BaseModel):
    url: str = Field(..., description="HTTP or HTTPS URL to fetch")
    max_length: int = Field(4000, description="Max character length of extracted text")


class WebFetchTool(BaseTool):
    name = "web_fetch"
    description = "Fetch webpage content and extract clean text."
    category = ToolCategory.SEARCH
    args_schema: Type[BaseModel] = WebFetchInput

    def run(self, url: str, max_length: int = 4000) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NexusAgent/1.0"
        }
        try:
            with httpx.Client(timeout=15.0, follow_redirects=True) as client:
                resp = client.get(url, headers=headers)
                resp.raise_for_status()
                text = resp.text

            # Simple HTML clean up
            text = re.sub(r"<script.*?>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text).strip()

            if len(text) > max_length:
                return text[:max_length] + "\n... [Content truncated]"
            return text if text else "(Empty webpage response)"
        except Exception as e:
            return f"Failed to fetch URL '{url}': {str(e)}"


class WebSearchInput(BaseModel):
    query: str = Field(..., description="Search query keywords")


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web using DuckDuckGo."
    category = ToolCategory.SEARCH
    args_schema: Type[BaseModel] = WebSearchInput

    def run(self, query: str) -> str:
        # Query DuckDuckGo Lite or API
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NexusAgent/1.0"}
        url = "https://html.duckduckgo.com/html/"
        try:
            with httpx.Client(timeout=15.0, follow_redirects=True) as client:
                resp = client.post(url, data={"q": query}, headers=headers)
                resp.raise_for_status()
                html = resp.text

            # Parse snippets
            snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
            titles = re.findall(r'<a class="result__url[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)

            results = []
            for i, snip in enumerate(snippets[:5]):
                clean_snip = re.sub(r"<[^>]+>", "", snip).strip()
                results.append(f"[{i+1}] {clean_snip}")

            return "\n\n".join(results) if results else f"Search for '{query}' completed with no direct snippets."
        except Exception as e:
            return f"Web search failed: {str(e)}"
