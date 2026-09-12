<div align="center">

```
  _   _ _____ _   _ _   _ ____        _     ____ _____ _   _ _____ 
 | \ | | ____| \ | | | | / ___|      / \   / ___| ____| \ | |_   _|
 |  \| |  _| |  \| | | | \___ \     / _ \ | |  _|  _| |  \| | | |  
 | |\  | |___| |\  | |_| |___) |   / ___ \| |_| | |___| |\  | | |  
 |_| \_|_____|_| \_|\___/|____/   /_/   \_\\____|_____|_| \_| |_|  
```

# NEXUS-AGENT

### Next-Generation Autonomous AI Engineering & Orchestration Agent

[![CI](https://img.shields.io/badge/CI-Passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-success?style=for-the-badge&logo=codecov&logoColor=white)]()
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Release](https://img.shields.io/github/v/release/parkain707/nexus-agent?color=orange&style=for-the-badge&logo=github)](https://github.com/parkain707/nexus-agent/releases)
[![GitHub Stars](https://img.shields.io/github/stars/parkain707/nexus-agent?style=social)](https://github.com/parkain707/nexus-agent/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/parkain707/nexus-agent?style=social)](https://github.com/parkain707/nexus-agent/network/members)

[**English**](README.md) | [**한국어 설명서 (README_KO.md)**](README_KO.md)

</div>

> 🌐 **Live Interactive Web Demo**: [https://should-busy-repairs-metres.trycloudflare.com](https://should-busy-repairs-metres.trycloudflare.com)  
> *Experience the Cyberpunk Glassmorphic Mission Control in real-time with zero installation!*

---

## ⚡ What is Nexus-Agent?

**Nexus-Agent** is an open-source, production-grade autonomous software engineering agent designed to solve complex coding, refactoring, and devops tasks end-to-end.

Unlike brittle wrapper scripts that blindly chain prompts or hallucinate syntax errors, **Nexus-Agent** features:
1. **Self-Healing ReAct Loop**: Automatically captures test failures and `stderr`, pinpoints root causes, and patches code.
2. **AST-Aware Code Engine**: Verifies Python syntax trees *before* writing or modifying files, completely preventing syntax-broken commits.
3. **Dual-Engine UX**: 
   - 💻 **Rich TUI Terminal**: Colorful live diffs, spinners, step-by-step thinking visualization.
   - 🌐 **Cyberpunk Glassmorphism Web Dashboard**: Real-time WebSocket streaming of agent thoughts, live tool execution telemetry, and interactive controls.
4. **Hierarchical SQLite Memory**: Token-efficient working memory plus persistent SQLite reflection logs to learn from mistakes.
5. **Zero-API-Key Deterministic Mock Engine**: Test the entire agent suite offline in 1 second without spending a single cent on API tokens!

---

## 📊 Feature Comparison Matrix

| Feature | Nexus-Agent | AutoGPT | CrewAI | LangGraph | OpenManus |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Self-Healing AST Syntax Pre-Validation** | **Yes (Built-in)** | No | No | Custom only | No |
| **Dual Interface (Rich TUI + Glassmorphism Web)** | **Yes (Out-of-box)** | CLI only | Web optional | Custom only | CLI only |
| **Offline Zero-Key Deterministic Testing** | **Yes (1-sec CI)** | No | No | No | No |
| **Sandboxed Shell with Blacklist Guard** | **Yes** | Partial | Needs Docker | Custom only | Partial |
| **SQLite Mistake & Reflection Memory** | **Yes** | Vector DB | Key-value | State Graph | No |
| **Single-Command Docker Deployment** | **Yes** | Yes | Yes | Complex | No |

---

## 🚀 30-Second Quickstart

### 1. Installation

```bash
### ⚡ 1-Click Instant Launch (Easiest)

- **Windows**: Simply double-click **`start.bat`** in the folder! It automatically configures the environment, starts the server, and pops up your browser.
- **Mac / Linux**: Run `chmod +x start.sh && ./start.sh`.

---

### 💻 Manual CLI Installation

```bash
# Clone repository
git clone https://github.com/parkain707/nexus-agent.git
cd nexus-agent

# Install dependencies
pip install -e .
```

### 🖥️ Run in Terminal (CLI Mode)

```bash
# Runs immediately with offline demo mode (zero cost, zero API keys!)
nexus-agent run "Create a fibonacci generator in fib.py and verify with unit tests"
```

To run with live cloud LLMs:
```bash
export OPENAI_API_KEY="sk-..."
nexus-agent run "Refactor database models and optimize queries" --provider openai --model gpt-4o
```

### 🌐 Launch the Web Mission Control Dashboard

```bash
nexus-agent web --port 8000
```
> [!TIP]
> Executing `nexus-agent web` automatically opens **`http://localhost:8000`** in your default browser! If port 8000 is occupied, it automatically shifts to the next available port.

---

## 🏗️ Architecture

```mermaid
graph TD
    User([User / Developer]) -->|CLI or Browser| UI[Dual Interface Layer]
    
    subgraph UI [Interface Layer]
        CLI[Rich TUI Interactive Terminal]
        Web[Cyberpunk Glassmorphism Dashboard]
    end

    UI --> Core[Nexus Core Engine]

    subgraph Core [Autonomous Core Engine]
        ReAct[ReAct Loop & Self-Healing Controller]
        LoopDet[Anti-Loop Detector]
        Memory[Hierarchical Memory: Working + SQLite Store]
        ToolBus[Sandboxed Tool Bus & Security Guard]
    end

    subgraph Tools [Safety-Guarded Tools]
        AST[AST-Aware File & Diff Engine]
        Shell[Sandboxed Shell Executor]
        Git[Git Workspace Controller]
        Search[Web & Code Search]
    end

    subgraph LLM [Multi-Provider Layer]
        Mock[Deterministic Mock Provider]
        OpenAI[OpenAI / DeepSeek]
        Claude[Anthropic Claude]
        Gemini[Google Gemini]
        Ollama[Local Ollama / vLLM]
    end

    ReAct --> Memory
    ReAct --> LoopDet
    ReAct --> ToolBus
    ToolBus --> Tools
    ReAct -.-> LLM
```

---

## 🛠️ Built-in Tool Arsenal

Nexus-Agent comes equipped with a comprehensive suite of safety-guarded engineering tools:

- `read_file`: Line-range slicing and file content inspection.
- `write_file`: Writes files with **AST syntax pre-validation** (rejects invalid Python syntax before disk write).
- `edit_file`: Performs surgical text replacement with automated unified diff preview.
- `list_dir`: Structured directory tree explorer.
- `execute_command`: Sandboxed shell execution with execution timeouts and destructive command blacklisting.
- `grep_search`: High-speed regex code search with line number snippets.
- `find_files`: Glob-based file locator.
- `git_status` / `git_diff` / `git_commit`: Autonomous version control management.
- `web_search` / `web_fetch`: Real-time documentation querying.

---

## 🧩 Writing Custom Tools in 5 Lines

You can effortlessly extend Nexus-Agent with domain-specific tools:

```python
from pydantic import BaseModel, Field
from nexus_agent.tools import BaseTool, create_default_registry
from nexus_agent import NexusAgent

class SlackAlertInput(BaseModel):
    channel: str = Field(..., description="Target Slack channel")
    message: str = Field(..., description="Alert text")

class SlackAlertTool(BaseTool):
    name = "send_slack_alert"
    description = "Send notifications to company Slack channels."
    args_schema = SlackAlertInput

    def run(self, channel: str, message: str) -> str:
        # Your notification logic here
        return f"Alert dispatched to {channel}: {message}"

# Register and run
registry = create_default_registry()
registry.register(SlackAlertTool())
agent = NexusAgent(registry=registry)
```

---

## 🐳 Docker Deployment

```bash
# 1-command startup
docker compose up --build
```
The Web Dashboard will be immediately available at `http://localhost:8000`.

---

## 🧪 Running Tests

Nexus-Agent boasts a 100% pass rate across unit, integration, and E2E self-healing test suites:

```bash
pytest -v
```

Output:
```text
tests/e2e/test_autonomous_coding.py::test_e2e_autonomous_coding_and_self_healing PASSED
tests/test_agent_core.py::test_agent_react_execution_flow PASSED
tests/test_agent_core.py::test_agent_loop_detection PASSED
tests/test_memory.py::test_working_memory_sliding_window PASSED
tests/test_memory.py::test_persistent_knowledge_and_reflection PASSED
tests/test_memory.py::test_snapshot_and_rollback PASSED
tests/test_schema_and_llm.py::test_schema_instantiation PASSED
tests/test_tools.py::test_file_ops_ast_validation PASSED
tests/test_tools.py::test_shell_command_sandbox_and_blacklist PASSED
tests/test_tools.py::test_diagram_generator PASSED
tests/test_web_api.py::test_web_status_endpoint PASSED
tests/test_web_api.py::test_chat_endpoint PASSED
tests/test_web_api.py::test_snapshots_api_and_rollback PASSED
tests/test_cli_scaffold.py::test_scaffold_fastapi PASSED
tests/test_cli_scaffold.py::test_scaffold_cli PASSED
tests/test_cli_scaffold.py::test_scaffold_custom_tool PASSED
...
======================= 20 passed in 1.86s =======================
```

---

## 🗺️ Roadmap

- [x] Autonomous ReAct loop with self-healing error recovery
- [x] AST-aware syntax pre-validation
- [x] Time-travel code snapshots & 1-click rollback
- [x] Dual-interface (Rich TUI + Cyberpunk Glassmorphism Web)
- [x] Offline Deterministic Mock provider for zero-cost testing
- [x] SQLite persistent reflection journal
- [x] Instant code scaffolding (`fastapi`, `cli`, `custom-tool`)
- [ ] Multi-agent collaborative swarm mode
- [ ] Tree-of-Thought (ToT) branch search
- [ ] Browser-use visual DOM automation

---

## 📣 Community & Viral Launch

Looking to share or contribute to Nexus-Agent? Check out our ready-to-use launch and sharing kits in [`launch/`](launch/README.md):
- [GeekNews Submission Kit](launch/GEEKNEWS_KO.md)
- [Hacker News Show HN](launch/HACKERNEWS_SHOW_HN.md)
- [Reddit r/LocalLLaMA & r/Python](launch/REDDIT_LOCALLAMA.md)
- [X/Twitter Viral Thread](launch/TWITTER_X_THREAD.md)
- [Velog / Technical Blog Post](launch/VELOG_POST_KO.md)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=parkain707/nexus-agent&type=Date)](https://star-history.com/#parkain707/nexus-agent&Date)

---

## 🤝 Contributing & License

Contributions, bug reports, and feature proposals are warmly welcomed! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.
