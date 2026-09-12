# 💬 개발자 커뮤니티 (Discord / 카카오 오픈채팅 / 슬랙) 홍보 키트

아래 메시지 템플릿은 국내외 주요 AI/개발자 커뮤니티의 `#프로젝트-공유`, `#오픈소스-홍보`, `#share-your-project` 채널에 복사하여 붙여넣을 수 있도록 작성되었습니다.

---

## 🇰🇷 국내 커뮤니티용 (AI Korea, GPTers, LangChain KR, 파이썬 사용자 모임)

### 템플릿 A: 짧고 임팩트 있는 소개 (디스코드/슬랙 권장)
```markdown
안녕하세요 개발자 여러분! 👋
기존 AI 에이전트를 쓰면서 문법 에러로 코드가 깨지거나, 멋대로 코드를 덮어써서 멘붕 오던 문제를 해결하고자 만든 오픈소스 코딩 에이전트 **Nexus-Agent**를 공유드립니다! ⚡

🌟 **핵심 기능**:
- 🛡️ **AST 구문 사전 검증**: 코드를 저장하기 전 메모리에서 문법을 검사해 구문 에러를 원천 차단
- ⏱️ **타임 트래블 롤백**: 파일 수정 시점마다 SQLite에 자동 스냅샷 저장, 웹 UI에서 1클릭 1ms 복구
- 🛠️ **자가 치유(Self-Healing)**: 테스트 실패 시 traceback을 분석해 스스로 코드를 패치
- 💡 **Zero-API-Key 오프라인 데모**: OpenAI/Claude 키 없이도 `start.bat` 더블 클릭 한 번으로 가상환경 구축 & 웹 대시보드 즉시 체험

현재 20개 테스트 100% 통과된 상태이며 완전한 MIT 오픈소스입니다!
도움이 되셨다면 깃허브 Star(⭐) 하나씩 부탁드립니다 🙌

🔗 **GitHub**: https://github.com/parkain707/nexus-agent
```

### 템플릿 B: 카카오톡 오픈채팅방용 (줄바꿈 최적화)
```text
[오픈소스 공유] 자가 치유(Self-Healing) & 타임트래블 롤백 AI 코딩 에이전트 'Nexus-Agent' v1.0.0

안녕하세요! AI 코딩 에이전트가 들여쓰기 실수나 문법 오류로 코드를 망가뜨리는 걸 막기 위해 개발한 Nexus-Agent를 오픈소스로 공개했습니다.

주요 특징:
1. AST 사전 검증: 문법 에러가 있는 코드는 저장되지 않고 즉시 스스로 재수정
2. 타임트래블 롤백: 에이전트가 코드를 망쳐도 웹 UI에서 1클릭 1초 만에 과거 시점 복원
3. 자가 치유: pytest 실패 시 트레이스백 분석 후 스스로 버그 수정
4. 100% 무료 오프라인 모드: API 키 없이도 누구나 start.bat만 누르면 즉시 작동 확인

- 깃허브: https://github.com/parkain707/nexus-agent
- MIT 라이선스

피드백과 스타(Star ⭐) 환영합니다! 감사합니다 :)
```

---

## 🌐 글로벌 커뮤니티용 (Discord: Together AI, LangChain, Cursor/Devin community, LocalLLaMA)

### English Discord Template
```markdown
Hey everyone! 🚀
I've just open-sourced **Nexus-Agent** – a lightweight, autonomous engineering agent designed to eliminate syntax hallucinations and destructive overwrites!

🔥 **Highlights**:
- 🛡️ **In-Memory AST Guardrails**: Pre-validates code with `ast.parse` before writing to disk; syntax errors are trapped and routed back to reflection.
- ⏱️ **Time-Travel Snapshots & 1-Click Rollback**: Every edit creates an atomic snapshot in SQLite. Roll back any file state in 1ms via Web UI.
- 🛠️ **Autonomous Self-Healing**: Automatically catches pytest/shell failures and iteratively patches code.
- 💰 **Zero-Cost Offline Mock Mode**: Test the full ReAct loop without any OpenAI/Claude API keys.
- 🎮 **Cyberpunk Glassmorphism Web UI & Rich CLI**: Interactive chat, live log streaming, and system benchmarking.

Check it out and star if you like it! ⭐
👉 GitHub: https://github.com/parkain707/nexus-agent
```
