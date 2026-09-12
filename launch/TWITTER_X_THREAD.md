# 🐦 Twitter / X Viral Thread Kit

- **작성 링크**: [https://twitter.com/compose/tweet](https://twitter.com/compose/tweet)

---

### Tweet 1 (Main Hook) 🧵👇
AI 코딩 에이전트가 들여쓰기 실수 하나로 코드를 망가뜨리거나, 멋대로 기존 로직을 날려버려 멘붕 온 적 있으신가요? 🤦‍♂️

자가 치유(Self-Healing)와 AST 구문 사전 검증, 1클릭 타임트래블 롤백을 장착한 차세대 오픈소스 AI 에이전트 **Nexus-Agent**를 공개합니다! ⚡🚀

⭐ GitHub: https://github.com/parkain707/nexus-agent

---

### Tweet 2 (Problem & AST Pre-Validation) 🛡️
기존 AI 에이전트의 가장 큰 문제:
코드에 작은 문법 오류(SyntaxError)가 있으면 전체 파이프라인이 멈춥니다.

Nexus-Agent는 코드를 디스크에 저장하기 전, 인메모리에서 Python AST(`ast.parse`)로 구문 무결성을 검증합니다.
오류가 있으면 디스크를 건드리지 않고 즉시 ReAct 루프로 재수정 피드백을 전달합니다!

---

### Tweet 3 (Time-Travel Rollback & Self-Healing) ⏱️
"에이전트가 코드를 망치면 어떡하죠?"

걱정 마세요. Nexus-Agent는 모든 파일 수정 시점마다 SQLite에 원자적 스냅샷을 보관합니다.
웹 대시보드의 `TIME-TRAVEL SNAPSHOTS` 패널에서 단 1번의 클릭(`[↺ ROLLBACK]`)으로 1ms 만에 과거 상태로 복구할 수 있습니다.
또한 테스트 실패 시 traceback을 추적해 스스로 코드를 패치합니다 🛠️

---

### Tweet 4 (Zero API Key & Instant 1-Click Launch) 💡
"API 키 없는데 써볼 수 있나요?"

네! `DeterministicMockProvider`가 기본 탑재되어 있어, OpenAI/Claude API 키 없이도 100% 무료 오프라인으로 자가 치유 루프를 테스트할 수 있습니다.

윈도우 사용자는 더블 클릭 한 번(`start.bat`)으로 가상환경 구축부터 브라우저 대시보드 오픈까지 끝납니다.

---

### Tweet 5 (Call to Action & Open Source) ⭐
Nexus-Agent는 100% MIT 라이선스 오픈소스입니다.
20개의 단위/통합 테스트가 모두 통과(100% Green)되어 안정성이 검증되었습니다.

지금 GitHub에서 Star를 누르고 직접 실행해보세요! 피드백과 PR은 언제나 환영합니다 🙌

🔗 https://github.com/parkain707/nexus-agent

#AI #Python #OpenSource #AIAgent #SelfHealing #LocalLLM #Devin #DeveloperTools
