# 📰 GeekNews (긱뉴스) 등록용 바이럴 키트

- **등록 URL**: [https://news.hada.io/submit](https://news.hada.io/submit)
- **제목 (Title)**: `Show GN: Nexus-Agent - AST 사전 검증과 자가 치유(Self-Healing)를 갖춘 오픈소스 AI 코딩 에이전트`
- **링크 (URL)**: `https://github.com/parkain707/nexus-agent`

---

## 📝 본문 내용 (그대로 복사하여 붙여넣기)

기존의 AutoGPT나 각종 ReAct 기반 코딩 에이전트를 사용하면서 가장 답답했던 점은 두 가지였습니다:
1. 에이전트가 생성한 코드에 사소한 문법 에러(SyntaxError, 들여쓰기 오류)가 포함되어 실행 자체가 터지는 문제
2. 코드를 수정하다가 기존 동작하던 코드까지 망쳐버렸을 때 되돌릴 방법이 없다는 점

이를 해결하기 위해 개발자 친화적인 안전장치와 자가 치유(Self-Healing) 루프를 코어로 장착한 **Nexus-Agent**를 오픈소스로 공개합니다.

### 🌟 핵심 기능 요약
- **AST(추상 구문 트리) 사전 검증**: 에이전트가 코드를 파일에 쓰거나 수정할 때, Python `ast.parse`를 통해 문법 무결성을 먼저 검증합니다. 문법 오류가 발생하면 파일에 덮어쓰지 않고 에이전트에게 즉시 문법 피드백을 전달하여 수정하도록 유도합니다.
- **자가 치유(Self-Healing) 루프**: 단위 테스트나 명령 실행 실패 시, 트레이스백(Traceback)을 역추적하여 근본 원인을 파악하고 스스로 패치 및 재검증을 수행합니다.
- **Time-Travel 스냅샷 & 1클릭 롤백**: 에이전트가 파일을 변경할 때마다 직전 상태를 SQLite에 원자적(Atomic)으로 기록합니다. 웹 UI에서 언제든 과거 시점으로 1ms 만에 코드를 되돌릴 수 있습니다.
- **Zero API Key 오프라인 Mock 모드**: OpenAI나 Anthropic API 키가 없어도 `DeterministicMockProvider`를 통해 완전 무료로 100% 로컬에서 동작과 자가 치유 루프를 테스트할 수 있습니다.
- **사이버펑크 글래스모피즘 Web UI & Rich CLI**: 브라우저에서 실시간 생각 흐름과 대화형 인터랙션을 제공하며, 터미널에서는 Rich 기반의 직관적인 상태창과 벤치마크 점수를 출력합니다.

### ⚡ 10초 빠른 시작
```bash
git clone https://github.com/parkain707/nexus-agent.git
cd nexus-agent

# 윈도우 원클릭 실행 (가상환경 및 의존성 자동 세팅 후 웹 UI 브라우저 자동 오픈)
start.bat

# 리눅스/macOS
chmod +x start.sh && ./start.sh

# 터미널 CLI 오프라인 데모
nexus run "calc.py 파일에 나눗셈 함수를 만들고 테스트를 검증해줘" --provider mock
```

현재 20개의 단위/통합 테스트가 모두 통과(100% Green)되어 있으며, 코드베이스는 확장하기 쉽도록 모듈화되어 있습니다.
직접 써보시고 피드백이나 개선 아이디어가 있으시다면 이슈나 PR로 편하게 남겨주시면 감사하겠습니다!

- GitHub: https://github.com/parkain707/nexus-agent
