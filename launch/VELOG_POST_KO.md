# ✍️ Velog / 브런치 / 미디엄 기술 블로그 포스팅 키트

- **권장 플랫폼**: [Velog 글쓰기](https://velog.io/write) 또는 [Medium](https://medium.com/new-story) / [Brunch](https://brunch.co.kr/)
- **태그 (Tags)**: `Python`, `AIAgent`, `오픈소스`, `인공지능`, `개발자도구`, `자가치유`
- **제목 (Title)**: `AI 에이전트가 코드를 망가뜨리는 걸 보다 못해 직접 만든 '자가 치유(Self-Healing)' 오픈소스 엔진: Nexus-Agent 제작기`

---

## 📝 포스팅 본문 마크다운 (그대로 복사하여 발행)

![Nexus-Agent Banner](https://raw.githubusercontent.com/parkain707/nexus-agent/master/nexus_agent/ui/web/static/images/banner.png)
*(이미지가 없을 경우 GitHub 리포지토리 링크로 대체 가능합니다)*

> **"AI가 코드를 짜줬는데... 문법 에러가 나서 실행조차 안 되네요?"**  
> **"기존에 잘 돌던 코드까지 덮어써서 망쳤는데, 되돌릴 방법이 없나요?"**

최근 Devin, Claude Engineer, AutoGPT 등 자율 AI 에이전트들이 쏟아져 나오고 있습니다. 하지만 실제로 프로젝트에 써보신 개발자분들은 아실 겁니다. 에이전트가 들여쓰기 실수나 오타 하나로 치명적인 `SyntaxError`를 일으키고, 기껏 동작하던 이전 코드를 멋대로 덮어써서 `git checkout`으로 되돌리느라 진땀을 빼는 일이 얼마나 허다한지요.

**"에이전트가 코드를 망가뜨리지 못하게 원천 차단하고, 오류가 나면 스스로 고치며, 언제든 1초 만에 과거로 되돌릴 수는 없을까?"**

이 질문에서 출발하여 만든 오픈소스 프로젝트, **Nexus-Agent**의 설계 과정과 핵심 아키텍처를 공유합니다.

---

### 1. 문제의 본질: LLM은 확률적이다

아무리 똑똑한 최신 LLM(GPT-4o, Claude 3.5 Sonnet, DeepSeek-Coder 등)이라 할지라도, 토큰 단위의 확률적 텍스트 생성기라는 본질은 변하지 않습니다.

복잡한 다단계 리팩토링이나 엣지 케이스를 다룰 때 LLM은 다음과 같은 실수를 필연적으로 범합니다:
1. **구문 파괴(Syntax Hallucination)**: 괄호 불일치, 인덴트 에러, 오탈자.
2. **파괴적 덮어쓰기(Destructive Overwrite)**: 전체 파일을 다시 쓰면서 기존의 중요 비즈니스 로직을 누락.
3. **무한 루프(Infinite Hallucination Loop)**: 동일한 에러 메시지를 보면서 똑같은 틀린 코드를 반복 생성.

우리가 필요로 하는 것은 무조건적인 자율성이 아니라, **"실패해도 시스템을 안전하게 지켜주는 엔지니어링 가드레일"**이었습니다.

---

### 2. Nexus-Agent의 핵심 해결책 3가지

#### 🛡️ 1. AST(추상 구문 트리) 기반 인메모리 사전 검증
Nexus-Agent는 에이전트가 `write_file`이나 `edit_file` 도구를 호출할 때 코드를 파일 시스템에 즉시 쓰지 않습니다.

대신 메모리 상에서 Python의 `ast.parse()` 엔진을 통과시킵니다:
- **문법 무결성 검증**: 문법 오류가 발견되면 파일 저장을 원천 거부합니다.
- **피드백 피딩**: 발생한 정확한 라인 번호와 에러 메시지를 에이전트의 생각(Thought) 컨텍스트로 반환하여, 디스크 오염 없이 스스로 구문을 교정하도록 유도합니다.

```python
# 실제 Nexus-Agent 내부 검증 로직 요약
try:
    ast.parse(content)
except SyntaxError as e:
    return ToolResult(
        success=False,
        output=f"[AST REJECTED] Syntax error on line {e.lineno}: {e.msg}. Please fix before saving."
    )
```

#### ⏱️ 2. Time-Travel 스냅샷 & 1클릭 롤백 엔진
개발자가 실수했을 때 `Ctrl + Z`를 누르듯, 에이전트에게도 되돌리기 기능이 필요합니다.

Nexus-Agent는 파일이 수정될 때마다 변경 전 원본과 통합 diff(Unified Diff)를 SQLite 로컬 데이터베이스에 원자적(Atomic)으로 스냅샷을 생성합니다.
- 웹 UI의 `TIME-TRAVEL SNAPSHOTS` 패널에 실시간으로 히스토리가 쌓입니다.
- 마음에 들지 않거나 로직이 꼬였다면 `[↺ ROLLBACK]` 버튼 클릭 한 번으로 1ms 만에 이전 버전으로 원상복구됩니다.

#### 🛠️ 3. 자가 치유(Self-Healing) ReAct 루프
에이전트가 작성한 코드는 곧바로 단위 테스트(`pytest`)나 실행 검증 파이프라인을 거칩니다.
- 만약 테스트가 실패하면, 에러 트레이스백을 추출하여 에이전트의 ReAct 루프에 자가 성찰(Self-Reflection) 태스크로 주입합니다.
- 에이전트는 오류를 분석하고, 최소한의 패치(Diff)를 생성하여 다시 테스트를 통과할 때까지 자율적으로 치유 과정을 반복합니다.

---

### 3. API 키 없이도 누구나 10초 만에 체험 가능한 설계

오픈소스 프로젝트를 배포할 때 가장 큰 장벽은 **"API 키 발급과 복잡한 환경 설정"**입니다. 아무리 좋은 도구라도 설치하다가 터지면 사용자는 떠납니다.

Nexus-Agent는 이 허들을 완전히 없앴습니다:
1. **Zero API Key Mock Mode (`DeterministicMockProvider`)**: OpenAI, Anthropic 키가 없어도 100% 로컬 오프라인에서 ReAct 루프, AST 검증, 자가 치유 시나리오를 무료로 즉시 체험할 수 있습니다.
2. **원클릭 스타터 (`start.bat` / `start.sh`)**: 윈도우 사용자는 `start.bat`을 더블 클릭하기만 하면 가상환경 생성, 의존성 설치, 서버 실행, 브라우저 대시보드 오픈까지 전자동으로 완료됩니다.
3. **듀얼 인터페이스**: 풍부한 색감의 터미널 CLI(Rich TUI)와 최신 사이버펑크 글래스모피즘(Glassmorphism) 웹 대시보드를 기본 지원합니다. 웹 UI에서는 실시간 대화형 인터랙션(Multi-turn Chat)까지 즐길 수 있습니다.

---

### 4. 코드 품질과 테스트 검증

아무리 "자율 에이전트"라고 광고해도 자체 테스트가 부실하면 신뢰할 수 없습니다.

Nexus-Agent는 작성된 모든 모듈에 대해 20개의 단위/통합/E2E 테스트를 구축하였으며, **100% Green(통과)**을 유지하고 있습니다:
- 에이전트 ReAct 루프 제어 및 무한루프 방지 테스트
- AST 사전 문법 검증 및 에러 트랩 테스트
- Time-Travel 스냅샷 생성 및 1클릭 롤백 무결성 테스트
- 자가 치유(Self-Healing) 런타임 테스트
- 13개 도구(파일, 셸, Git, 웹 검색, Mermaid 다이어그램 등) 정밀 테스트

---

### 5. 지금 바로 사용해보기

Nexus-Agent는 100% MIT 라이선스로 자유롭게 사용 및 수정이 가능합니다.

```bash
# 1. 저장소 클론
git clone https://github.com/parkain707/nexus-agent.git
cd nexus-agent

# 2. 윈도우 원클릭 실행 (브라우저 자동 실행)
start.bat

# 3. 터미널 오프라인 무료 테스트
nexus run "calc.py에 사칙연산 함수를 작성하고 테스트로 검증해줘" --provider mock
```

- 🌟 **GitHub 저장소**: https://github.com/parkain707/nexus-agent
- 📖 **상세 아키텍처 문서**: https://github.com/parkain707/nexus-agent/blob/master/ARCHITECTURE.md

프로젝트가 흥미로우셨다면 **GitHub Star(⭐)**를 눌러 응원해 주시면 큰 힘이 됩니다!  
버그 제보나 기능 추가 제안은 언제든 이슈와 PR로 남겨주세요. 읽어주셔서 감사합니다!
