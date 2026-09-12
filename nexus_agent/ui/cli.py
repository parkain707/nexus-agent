"""
Rich Interactive Terminal CLI Interface for Nexus-Agent (Agent 2: Iris).
Features cyberpunk ASCII banners, live spinners, colorful streaming diffs, and interactive prompts.
"""

import sys
import os
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.table import Table
from rich.syntax import Syntax

from nexus_agent.version import __version__
from nexus_agent.core.schema import AgentConfig, AgentStatus
from nexus_agent.core.agent import NexusAgent
from nexus_agent.tools import create_default_registry

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

console = Console(safe_box=True)

BANNER = r"""[bold cyan]
  _   _ _____ _   _ _   _ ____        _     ____ _____ _   _ _____ 
 | \ | | ____| \ | | | | / ___|      / \   / ___| ____| \ | |_   _|
 |  \| |  _| |  \| | | | \___ \     / _ \ | |  _|  _| |  \| | | |  
 | |\  | |___| |\  | |_| |___) |   / ___ \| |_| | |___| |\  | | |  
 |_| \_|_____|_| \_|\___/|____/   /_/   \_\\____|_____|_| \_| |_|  
[/bold cyan][dim white]Autonomous Engineering & Self-Healing ReAct Engine v""" + __version__ + r"""[/dim white]
"""


def display_banner():
    console.print(BANNER)


@click.group()
@click.version_option(version=__version__, prog_name="nexus-agent")
def main():
    """Nexus-Agent: Next-Gen Autonomous AI Engineering Agent."""
    pass


@main.command()
@click.argument("goal", required=True)
@click.option("--provider", default="mock", help="LLM provider (mock, openai, anthropic, gemini, ollama)")
@click.option("--model", default="mock-model", help="Model name")
@click.option("--max-iters", default=25, help="Maximum iterations")
@click.option("--api-key", default=None, envvar="OPENAI_API_KEY", help="API Key")
def run(goal: str, provider: str, model: str, max_iters: int, api_key: str):
    """Execute a task goal autonomously in the terminal."""
    display_banner()
    console.print(Panel(f"[bold green]Target Goal:[/bold green] {goal}\n[dim]Provider: {provider} | Model: {model}[/dim]", border_style="cyan"))

    config = AgentConfig(
        provider=provider,
        model=model,
        max_iterations=max_iters,
        api_key=api_key,
    )
    agent = NexusAgent(config=config)

    def cli_callback(event_type: str, data: dict):
        if event_type == "thought":
            step = data.get("step", 0)
            thought = data.get("thought", "")
            console.print(f"\n[bold yellow]── Step {step} ── Thinking[/bold yellow]")
            console.print(Panel(thought, border_style="yellow", subtitle="[dim]Chain of Thought[/dim]"))
        elif event_type == "tool_call":
            tool_data = data.get("tool", {})
            name = tool_data.get("name", "tool")
            args = tool_data.get("arguments", {})
            console.print(f"[bold magenta]>> Action:[/bold magenta] Calling [bold cyan]{name}[/bold cyan] with args: [dim]{args}[/dim]")
        elif event_type == "tool_result":
            res = data.get("result", {})
            success = res.get("success", False)
            out = res.get("output", "")
            err = res.get("error", "")
            if success:
                console.print(f"[bold green][OK] Observation:[/bold green]")
                if len(out) > 500:
                    console.print(f"[dim]{out[:500]}... [Truncated][/dim]")
                else:
                    console.print(f"[dim]{out}[/dim]")
            else:
                console.print(f"[bold red][ERROR] Observation (Self-Healing Triggered):[/bold red] {err}")
        elif event_type == "reflection":
            console.print(f"[bold red][!] Reflection Alert:[/bold red] {data.get('warning')}")

    agent.register_callback(cli_callback)

    with console.status("[bold cyan]Nexus-Agent is actively planning and operating...[/bold cyan]", spinner="dots12"):
        final_state = agent.run(goal)

    console.print("\n" + "=" * 60)
    if final_state.status == AgentStatus.COMPLETED:
        console.print(Panel(
            Markdown(final_state.final_output or "Goal achieved successfully."),
            title="[bold green][MISSION ACCOMPLISHED][/bold green]",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold red]Execution Failed or Exceeded Limit:[/bold red] {final_state.error}",
            title="[bold red][EXECUTION INCOMPLETE][/bold red]",
            border_style="red"
        ))


@main.command()
def tools():
    """List all registered tools available to Nexus-Agent."""
    display_banner()
    registry = create_default_registry()
    table = Table(title="[bold cyan]Nexus-Agent Built-in Tool Arsenal[/bold cyan]", border_style="cyan")
    table.add_column("Tool Name", style="bold green", no_wrap=True)
    table.add_column("Category", style="magenta")
    table.add_column("Description", style="white")

    for tool in registry.list_tools():
        table.add_row(tool.name, tool.category.value, tool.description)

    console.print(table)


@main.command()
@click.option("--host", default="127.0.0.1", help="Web host interface")
@click.option("--port", default=8000, help="Web port")
@click.option("--no-browser", is_flag=True, help="Do not open browser automatically")
def web(host: str, port: int, no_browser: bool):
    """Launch the Cyberpunk Glassmorphism Mission Control Web Dashboard."""
    import socket
    import threading
    import time
    import webbrowser

    display_banner()

    # Check port availability and auto-fallback if busy
    target_port = port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((host, target_port)) != 0:
                # Port is available
                break
            else:
                target_port += 1
                if target_port > port + 10:
                    break

    if target_port != port:
        console.print(f"[bold yellow][!] Notice: Port {port} is occupied. Automatically switching to http://{host}:{target_port}[/bold yellow]")

    target_url = f"http://{host}:{target_port}"
    console.print(f"[bold green][START] Launching Nexus Web Mission Control on {target_url}[/bold green]")
    console.print("[dim]Press Ctrl+C to terminate the web server.[/dim]\n")

    if not no_browser:
        def open_browser():
            time.sleep(1.2)
            try:
                webbrowser.open(target_url)
            except Exception:
                pass
        threading.Thread(target=open_browser, daemon=True).start()

    try:
        import uvicorn
        from nexus_agent.ui.web.server import app
        uvicorn.run(app, host=host, port=target_port, log_level="info")
    except ImportError:
        console.print("[bold red]Error: uvicorn is required to run the web server. Install with `pip install uvicorn fastapi`[/bold red]")


@main.command()
def interactive():
    """Enter interactive REPL conversational mode."""
    display_banner()
    console.print("[bold cyan]Entering Interactive Command Mode. Type 'exit' or 'quit' to end session.[/bold cyan]\n")
    agent = NexusAgent(config=AgentConfig(provider="mock"))

    while True:
        try:
            prompt = console.input("[bold green]nexus-agent>[/bold green] ")
            if prompt.strip().lower() in ["exit", "quit", "q"]:
                console.print("[dim]Exiting Nexus-Agent session. Goodbye![/dim]")
                break
            if not prompt.strip():
                continue
            final_state = agent.run(prompt)
            console.print(f"\n[bold cyan]Result:[/bold cyan] {final_state.final_output}\n")
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()
