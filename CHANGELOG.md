# Changelog

All notable changes to Nexus-Agent will be documented in this file.

## [1.0.0] - 2026-09-12

### Initial Release
- **Core ReAct Engine**: Dynamic goal decomposition, self-healing reflection loop, and loop detection.
- **AST-Aware File Operations**: Pre-validation of Python syntax before writing or modifying files.
- **Sandboxed Shell**: Security blacklist pattern matcher and execution timeout safeguards.
- **Hierarchical Memory**: Working context sliding buffer and SQLite persistent reflection journal.
- **Dual Interface UX**:
  - Rich TUI terminal with cyberpunk banners, spinners, and live diff viewers.
  - Cyberpunk Glassmorphism Web Mission Control dashboard with real-time WebSocket telemetry.
- **Multi-Provider LLM Abstraction**: Supports OpenAI, Anthropic, Gemini, Ollama, DeepSeek, and offline Deterministic Mock.
- **Comprehensive Quality Assurance**: 15 unit, integration, and E2E self-healing test cases with 100% pass rate.
- **Deployment & Packaging**: Dockerfile, docker-compose.yml, GitHub Actions CI workflow, and bilingual (English & Korean) documentation.
