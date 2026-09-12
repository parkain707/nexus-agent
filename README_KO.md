<div align="center">

```
  _   _ _____ _   _ _   _ ____        _     ____ _____ _   _ _____ 
 | \ | | ____| \ | | | | / ___|      / \   / ___| ____| \ | |_   _|
 |  \| |  _| |  \| | | | \___ \     / _ \ | |  _|  _| |  \| | | |  
 | |\  | |___| |\  | |_| |___) |   / ___ \| |_| | |___| |\  | | |  
 |_| \_|_____|_| \_|\___/|____/   /_/   \_\\____|_____|_| \_| |_|  
```

# NEXUS-AGENT (넥서스 에이전트)

### 차세대 완전 자율형 AI 소프트웨어 엔지니어링 & 자가 치유(Self-Healing) 에이전트

[![CI](https://img.shields.io/badge/CI-Passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-success?style=for-the-badge&logo=codecov&logoColor=white)]()
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

[**English Document (README.md)**](README.md) | [**한국어 공식 설명서**](README_KO.md)

</div>

---

## ⚡ 넥서스 에이전트(Nexus-Agent)란?

**Nexus-Agent**는 복잡한 소프트웨어 엔지니어링, 코드 리팩토링, 디버깅, DevOps 작업을 사람의 개입 없이 **스스로 계획하고, 실행하며, 오류 발생 시 역추적하여 스스로 고치는(Self-Healing)** 프로덕션급 오픈소스 AI 엔지니어링 에이전트입니다.

단순히 프롬프트를 이어 붙인 기존의 조잡한 래퍼 도구와 달리, 넥서스는 개발 현장의 실질적인 페인포인트를 해결하기 위해 설계되었습니다:

1. **ReAct 자가 치유(Self-Healing) 엔진**: 단위 테스트 실패 및 `stderr` 런타임 에러 발생 시 원인을 역추적하여 코드를 자동 수정 및 재검증.
2. **AST(추상 구문 트리) 구문 사전 검증**: 코드를 디스크에 저장하거나 편집하기 전 Python AST 파싱을 거쳐 문법 오류가 있는 코드의 생성을 원천 차단.
3. **듀얼 인터페이스 (Dual-Engine UX)**:
   - 💻 **Rich TUI 콘솔**: 터미널 실시간 스트리밍, Git Diff 시각화, 진행 스피너 제공.
   - 🌐 **Cyberpunk Glassmorphism 웹 대시보드**: 별도 프론트엔드 빌드 없이 즉시 브라우저에서 실행되는 실시간 사고 과정(CoT) 및 도구 텔레메트리 관제 센터.
4. **계층형 SQLite 장기 기억 시스템**: 토큰을 절약하는 슬라이딩 윈도우 단기 기억 + 과거 실패와 해결책을 기록하여 같은 실수를 반복하지 않는 반추 저널(Reflection Journal).
5. **API 키 없는 Zero-Cost Deterministic Mock 모드**: API 키나 비용 결제 없이도 클론 즉시 1초 만에 전체 기능과 테스트 스위트를 100% 오프라인 검증 가능.

---

## 📊 기존 주요 에이전트 대비 비교표

| 기능 요건 | Nexus-Agent | AutoGPT | CrewAI | LangGraph | OpenManus |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **AST 구문 사전 검증 (문법오류 차단)** | **기본 내장 (Yes)** | 미지원 | 미지원 | 커스텀 필요 | 미지원 |
| **듀얼 인터페이스 (CLI + 글래스모피즘 웹)** | **기본 내장 (Yes)** | CLI 전용 | 웹 별도설치 | 커스텀 필요 | CLI 전용 |
| **비용 없는 오프라인 Mock 1초 테스트** | **기본 내장 (Yes)** | 불가 | 불가 | 불가 | 불가 |
| **위험 명령어 차단 샌드박스 쉘** | **기본 내장 (Yes)** | 부분 지원 | 도커 의존 | 커스텀 필요 | 부분 지원 |
| **SQLite 반추 저널 (실수 학습 기억)** | **기본 내장 (Yes)** | Vector DB | Key-value | State Graph | 미지원 |
| **원클릭 도커(Docker) 배포** | **기본 내장 (Yes)** | 지원 | 지원 | 복잡함 | 미지원 |

---

## 🚀 30초 퀵스타트

### ⚡ 원클릭(1-Click) 초간편 실행 (추천)

- **Windows 사용자**: 폴더 안에 있는 **`start.bat`** 파일을 더블 클릭하기만 하면 끝! (가상환경 설정, 서버 가동, 브라우저 자동 팝업까지 한 번에 완료됩니다.)
- **Mac / Linux 사용자**: 터미널에서 `chmod +x start.sh && ./start.sh` 실행.

---

### 💻 수동 터미널(CLI) 설치

```bash
# 저장소 복제
git clone https://github.com/parkain707/nexus-agent.git
cd nexus-agent

# 필수 의존성 설치
pip install -e .
```

### 🖥️ 터미널 실행 (CLI 모드)

```bash
# 기본 내장된 Mock 엔진을 통해 API 키 없이 즉시 1초 만에 자율 에이전트 동작 확인
nexus-agent run "sample.py 파일을 생성하고 소수 판별 알고리즘을 구현한 뒤 검증하라"
```

실제 클라우드/로컬 LLM과 연동하려면:
```bash
export OPENAI_API_KEY="sk-..."
nexus-agent run "FastAPI CRUD 백엔드 엔드포인트를 구축하라" --provider openai --model gpt-4o
```

### 🌐 실시간 사이버펑크 웹 관제 센터 실행

```bash
nexus-agent web --port 8000
```
> [!TIP]
> `nexus-agent web`을 실행하면 기본 웹 브라우저가 **`http://localhost:8000` 주소로 자동으로 팝업**됩니다! 만약 8000번 포트가 이미 사용 중이라면 자동으로 다음 번호 포트로 자동 전환됩니다.

---

## 🛠️ 기본 탑재 도구 목록

- `read_file`: 행 단위 슬라이싱 및 파일 정밀 읽기.
- `write_file`: Python AST 구문 사전 검증이 적용된 파일 생성 및 덮어쓰기.
- `edit_file`: 단일 코드 블록의 안전한 교체 및 자동 Unified Diff 생성.
- `list_dir`: 디렉터리 트리 구조 탐색.
- `execute_command`: 위험 명령어(rm -rf, format 등) 차단 블랙리스트 및 타임아웃 샌드박스 쉘.
- `grep_search`: 라인 번호가 표시되는 초고속 정규식 코드 검색.
- `find_files`: 글로브 패턴 파일 검색.
- `git_status` / `git_diff` / `git_commit`: 자율 Git 버전 관리.
- `web_search` / `web_fetch`: 실시간 공식 문서 검색 및 웹 추출.

---

## 🧩 5줄 만에 커스텀 도구 추가하기

```python
from pydantic import BaseModel, Field
from nexus_agent.tools import BaseTool, create_default_registry
from nexus_agent import NexusAgent

class DiscordAlertInput(BaseModel):
    message: str = Field(..., description="알림 메시지")

class DiscordAlertTool(BaseTool):
    name = "send_discord_alert"
    description = "사내 디스코드 채널로 실시간 알림을 전송합니다."
    args_schema = DiscordAlertInput

    def run(self, message: str) -> str:
        # 실제 웹훅 전송 로직
        return f"디스코드 전송 완료: {message}"

# 레지스트리에 등록 후 실행
registry = create_default_registry()
registry.register(DiscordAlertTool())
agent = NexusAgent(registry=registry)
```

---

## 🧪 테스트 검증 결과

`pytest` 실행 시 단위, 통합, E2E 자가 치유 테스트 스위트 100% 통과:

```bash
pytest -v
```

```text
tests/e2e/test_autonomous_coding.py::test_e2e_autonomous_coding_and_self_healing PASSED
tests/test_agent_core.py::test_agent_react_execution_flow PASSED
tests/test_agent_core.py::test_agent_loop_detection PASSED
tests/test_memory.py::test_working_memory_sliding_window PASSED
tests/test_memory.py::test_persistent_knowledge_and_reflection PASSED
tests/test_schema_and_llm.py::test_schema_instantiation PASSED
tests/test_tools.py::test_file_ops_ast_validation PASSED
tests/test_tools.py::test_shell_command_sandbox_and_blacklist PASSED
tests/test_web_api.py::test_web_status_endpoint PASSED
======================= 15 passed in 1.05s =======================
```

---

## 📄 라이선스 (License)

본 프로젝트는 **MIT 라이선스** 하에 오픈소스로 자유롭게 배포 및 활용할 수 있습니다. 자세한 내용은 [LICENSE](LICENSE)를 참조하십시오.
