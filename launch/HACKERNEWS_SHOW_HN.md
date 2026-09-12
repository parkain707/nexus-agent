# 🚀 Hacker News (Show HN) Submission Kit

- **Submission URL**: [https://news.ycombinator.com/submit](https://news.ycombinator.com/submit)
- **Title**: `Show HN: Nexus-Agent – Autonomous self-healing AI coding agent with AST validation & time-travel rollback`
- **URL**: `https://github.com/parkain707/nexus-agent`

---

## 💬 First Comment / Text Submission (Post immediately after submitting)

Hi HN! I built **Nexus-Agent** ([https://github.com/parkain707/nexus-agent](https://github.com/parkain707/nexus-agent)), an open-source autonomous coding agent designed around two simple observations from working with existing agent frameworks:

1. **Agents love to hallucinate syntax errors**: A small misplaced indentation or parenthesis from an LLM output shouldn't crash the entire working tree or waste 5 round-trips of API calls.
2. **LLMs need an "undo" button**: When an agent goes off the rails or rewrites working logic into spaghetti, developers need deterministic time-travel rollback rather than manually digging through `git stash` or lost buffers.

### How Nexus-Agent solves this:

- **AST-Guarded File Operations**: Every file write or modification is pre-validated using Python's Abstract Syntax Tree (`ast.parse`) in an in-memory buffer before touching disk. If syntax verification fails, the disk write is rejected, and structured AST diagnostic feedback is fed back into the agent's ReAct loop to self-correct before executing.
- **Autonomous Self-Healing Loop**: When automated tests (`pytest`) or shell commands fail, the engine captures stdout/stderr, traces error lines back to the offending AST nodes, and enters a targeted reflection phase to formulate minimal diff patches.
- **Time-Travel Snapshots & Instant Rollback**: Prior to any file alteration, an atomic snapshot is preserved in an embedded SQLite database. In the Web UI, you can inspect the step-by-step evolution of your codebase and hit `[↺ ROLLBACK]` to revert any file to any previous millisecond state.
- **100% Offline / Zero-API-Key Deterministic Mode**: You don't need an OpenAI/Anthropic/Gemini key to evaluate this. Passing `--provider mock` activates a deterministic rule-based LLM mock that runs the full ReAct cycle, performs AST checks, triggers self-healing on deliberate test failures, and demonstrates the workflow completely offline.
- **Dual Interface**: Includes both a Rich terminal TUI (with interactive wizard, scaffold generator, and system benchmarking) and a Cyberpunk Glassmorphic web mission control with live multi-turn chat (`/api/chat`).

### Quick Start (Zero Config):
```bash
git clone https://github.com/parkain707/nexus-agent.git
cd nexus-agent

# Windows 1-click launcher (auto venv, deps & browser launch)
start.bat

# Linux / macOS
chmod +x start.sh && ./start.sh

# Zero-cost test in terminal
nexus run "Create a divide function in calc.py and verify zero division handling" --provider mock
```

The test suite contains 20 unit, integration, and E2E self-healing test cases (100% pass rate).

The repository is MIT licensed: https://github.com/parkain707/nexus-agent

I'd love to hear your thoughts, critique on the AST validation approach, and suggestions for future tools or safeguards!
