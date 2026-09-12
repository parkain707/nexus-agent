# 👾 Reddit Submission Kit

---

## 1. r/LocalLLaMA (Primary Target)
- **Subreddit URL**: [https://www.reddit.com/r/LocalLLaMA/submit](https://www.reddit.com/r/LocalLLaMA/submit)
- **Flair**: `[Project]`
- **Title**: `[P] Nexus-Agent: Autonomous self-healing coding agent with AST validation, time-travel rollback, and 100% offline mock/Ollama support`

### Body:
Hey r/LocalLLaMA!

Most AI coding agents out there are bloated wrappers that break your local working tree when smaller open-weight models inevitably make a syntax blunder or hallucinate invalid Python.

I built **Nexus-Agent** ([GitHub](https://github.com/parkain707/nexus-agent)) as a clean, lightweight autonomous engineering engine that is designed from the ground up to be safe when running both local models (via Ollama) and commercial LLMs:

### What makes it different?
1. **In-Memory AST Guardrails**: Before writing or modifying any Python file, the agent parses the code using Python's `ast` module. If syntax errors exist, the file is NEVER written to disk. Instead, the AST syntax exception is returned to the model as diagnostic feedback so it can self-repair immediately.
2. **Time-Travel Snapshot & 1-Click Rollback**: Any file mutation automatically generates a diff and stores a full atomic snapshot in an embedded SQLite database. In the Web UI, you have a live "Time-Travel" panel where you can inspect previous iterations and revert any file with 1 click.
3. **Built-in Ollama & Local Provider Support**: Out of the box, you can plug in your local Ollama instance (`nexus run "..." --provider ollama --model deepseek-coder-v2` or `llama3.1`).
4. **Deterministic Mock Provider (Zero API Keys Needed)**: You can test the entire ReAct loop, AST validation, and self-healing test repair completely offline with zero tokens and zero internet access.
5. **Cyberpunk Glassmorphic Web UI + Rich TUI**: Includes both a live web mission control (with ChatGPT-style interactive chat and websocket event streaming) and a high-performance terminal CLI.

### Quick Start:
```bash
git clone https://github.com/parkain707/nexus-agent.git
cd nexus-agent

# Windows: Double click start.bat or run:
start.bat

# Linux / Mac:
chmod +x start.sh && ./start.sh

# Run offline zero-cost demo:
nexus run "Create calc.py with tests and fix division errors" --provider mock
```

The repository includes a full test suite with 20 unit/integration tests running at 100% pass rate.

- GitHub: https://github.com/parkain707/nexus-agent
- MIT Licensed, no telemetry, no tracking.

Would love to get feedback from fellow local LLM tinkerers!

---

## 2. r/Python
- **Subreddit URL**: [https://www.reddit.com/r/Python/submit](https://www.reddit.com/r/Python/submit)
- **Flair**: `Showcase`
- **Title**: `I built Nexus-Agent: An autonomous Python coding agent that validates code with AST before saving and provides 1-click time-travel rollbacks`

### Body:
Hi everyone,

I wanted to share a project I've been working on: **Nexus-Agent** ([GitHub](https://github.com/parkain707/nexus-agent)).

While playing with LLM code generation, I kept running into cases where agents overwrote working code with unparseable syntax, completely derailing multi-step tasks.

To solve this, I designed Nexus-Agent around strict Python AST validation and atomic versioning:
- **AST Pre-Validation**: Every write operation passes through `ast.parse` in memory. If an LLM hallucinates mismatched brackets or indentation bugs, the file write is intercepted and converted into structured feedback for the agent's reflection cycle.
- **Atomic Snapshots**: Changes are logged with unified diffs in SQLite. If anything goes wrong, you can roll back to any past state from the Web UI or CLI.
- **Self-Healing Loop**: Automatically parses `pytest` and command stderr to pinpoint failure locations and formulate targeted fixes.
- **Modern Packaging & Architecture**: Built with Pydantic V2, FastAPI WebSockets, Rich terminal interface, and zero external runtime dependencies for offline testing.

Check it out on GitHub: https://github.com/parkain707/nexus-agent

Feedback and PRs are very welcome!
