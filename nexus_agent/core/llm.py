"""
Multi-Provider LLM Abstraction Layer with Deterministic Mock Engine.
Supports OpenAI, Anthropic, Gemini, Ollama, DeepSeek, and Offline Mock.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json
import re

from nexus_agent.core.schema import AgentConfig, Message, ToolCall


class BaseLLMProvider(ABC):
    """Abstract interface for LLM backends."""

    def __init__(self, config: AgentConfig):
        self.config = config

    @abstractmethod
    def generate(
        self,
        messages: List[Message],
        tools_schema: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Generate response from LLM.
        Returns dict:
        {
            "thought": str,
            "tool_calls": List[ToolCall],
            "content": str
        }
        """
        pass


class DeterministicMockProvider(BaseLLMProvider):
    """
    Zero-cost, offline deterministic mock provider.
    Enables instant CI testing and local zero-dependency demos without API keys.
    Can be scripted with predetermined responses or rule-based heuristics.
    """

    def __init__(self, config: AgentConfig, custom_scripts: Optional[List[Dict[str, Any]]] = None):
        super().__init__(config)
        self.custom_scripts = custom_scripts or []
        self.call_count = 0

    def add_scripted_turn(self, thought: str, tool_call: Optional[ToolCall] = None, content: str = ""):
        self.custom_scripts.append({
            "thought": thought,
            "tool_calls": [tool_call] if tool_call else [],
            "content": content
        })

    def generate(
        self,
        messages: List[Message],
        tools_schema: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        if self.custom_scripts and self.call_count < len(self.custom_scripts):
            resp = self.custom_scripts[self.call_count]
            self.call_count += 1
            return resp

        # Default intelligent heuristic for general test tasks
        last_message = messages[-1].content if messages else ""
        self.call_count += 1

        # Check if previous message was tool error -> trigger self-healing
        if "Tool execution failed" in last_message or "error" in last_message.lower():
            return {
                "thought": "Self-healing triggered: An error occurred in the previous step. Analyzing stderr and applying fix.",
                "tool_calls": [],
                "content": "I detected the issue in the previous execution. Applying correction to resolve the bug."
            }

        # Check if asking to create file
        if "create" in last_message.lower() or "write" in last_message.lower():
            return {
                "thought": "User requested code/file creation. Formulating code and invoking write_file tool.",
                "tool_calls": [
                    ToolCall(
                        id=f"call_{self.call_count}",
                        name="write_file",
                        arguments={"path": "sample.py", "content": "print('Hello from Nexus-Agent!')\n"}
                    )
                ],
                "content": "Creating sample.py to accomplish the objective."
            }

        # Check if asked to run/test
        if "test" in last_message.lower() or "run" in last_message.lower():
            return {
                "thought": "Testing the code by executing shell command.",
                "tool_calls": [
                    ToolCall(
                        id=f"call_{self.call_count}",
                        name="execute_command",
                        arguments={"command": "python sample.py"}
                    )
                ],
                "content": "Running test suite to verify implementation."
            }

        # Check conversational queries
        lower_msg = last_message.lower()
        if any(w in lower_msg for w in ["안녕", "hello", "hi", "반가워"]):
            return {
                "thought": "User initiated a friendly greeting. Responding warmly and offering assistance.",
                "tool_calls": [],
                "content": "안녕하세요! 저는 완전 자율형 AI 엔지니어링 에이전트 **Nexus-Agent**입니다. ⚡\n코드 생성, 아키텍처 설계, 버그 디버깅, 테스트 자동화 등 무엇이든 편하게 말씀해 주세요!"
            }
        if any(w in lower_msg for w in ["누구", "who are you", "소개", "what are you"]):
            return {
                "thought": "User inquired about agent identity and capabilities.",
                "tool_calls": [],
                "content": "안녕하세요! 저는 완전 자율형 소프트웨어 엔지니어링 AI 에이전트 **Nexus-Agent**입니다.\n\n주요 기능 및 특징:\n- 🧠 **자율 ReAct 엔진**: 목표를 스스로 분석하고 적합한 도구를 선택하여 실행합니다.\n- 🛠️ **자가 치유(Self-Healing)**: 테스트 에러가 발생하면 원인을 역추적하여 코드를 자동으로 패치합니다.\n- 💬 **실시간 페어 프로그래밍**: 가벼운 대화부터 아키텍처 설계, 코드 작성까지 자유롭게 대화할 수 있습니다.\n\n어떤 프로젝트나 코딩 작업을 함께 시작해 볼까요?"
            }
        if any(w in lower_msg for w in ["대화", "chat", "이야기", "talk"]):
            return {
                "thought": "User asking about conversational capability.",
                "tool_calls": [],
                "content": "네! 저는 자율 엔지니어링뿐만 아니라 이렇게 자유로운 **실시간 대화와 페어 프로그래밍**도 완벽하게 지원합니다. 궁금하신 점이나 필요한 작업이 있으시면 언제든 말씀해 주세요!"
            }

        # Check specific mathematical/scientific knowledge queries
        if any(w in lower_msg for w in ["리만", "riemann"]):
            return {
                "thought": "User inquired about the Riemann Hypothesis in mathematics. Providing detailed conceptual explanation.",
                "tool_calls": [],
                "content": "### 📐 리만 가설(Riemann Hypothesis)이란?\n\n1859년 독일의 수학자 **베른하르트 리만(Bernhard Riemann)**이 제시한 수학 역사상 가장 거대하고 아름다운 미해결 난제(밀레니엄 7대 난제 중 하나)입니다.\n\n#### 1. 핵심 정의\n리만 제타 함수 $\\zeta(s) = \\sum_{n=1}^{\\infty} \\frac{1}{n^s}$에서,\n**함숫값이 0이 되는 모든 비자명한 근(Non-trivial zeros)의 실수부는 예외 없이 전부 $\\frac{1}{2}$이다**라는 가설입니다.\n\n#### 2. 왜 현대 수학에서 가장 중요한가?\n- **소수(Prime Numbers)의 규칙성**: 2, 3, 5, 7, 11... 처럼 무질서하게 흩어져 있는 것처럼 보이는 소수의 출현 빈도와 분포가 제타 함수의 영점들과 완벽하게 대응됩니다.\n- **현대 암호학 및 양자물리**: 소수의 비밀은 현대 공개키 암호(RSA) 및 복잡계 양자 역학의 에너지 준위 분포와도 깊은 연관이 있습니다.\n\n> 💡 **안내**: 현재 **[Deterministic Mock (오프라인 모드)]**에서 지식 응답을 제공하였습니다. 드롭다운에서 OpenAI, Gemini, Ollama 등 실제 LLM Provider를 선택하시면 세상의 모든 심층 질의응답을 무제한으로 수행할 수 있습니다!"
            }

        if any(w in lower_msg for w in ["태양계", "solar", "행성", "우주", "수성", "금성", "지구", "화성", "목성", "토성", "천왕성", "해왕성"]):
            return {
                "thought": "User inquired about the Solar System structure. Providing a comprehensive, engaging, and clear astronomy explanation.",
                "tool_calls": [],
                "content": "### ☀️ 한눈에 쏙 들어오는 태양계(Solar System)의 구성과 비밀\n\n태양계는 중심에서 활활 타오르는 거대한 항성 **'태양(Sun)'**과 그 주위를 도는 **8개의 행성**, 왜소행성, 소행성대, 그리고 혜성들로 구성된 거대한 천체 가족입니다! 🚀\n\n---\n\n#### 1. 태양계의 중심 사령관: 태양 (Sun) ☀️\n- 태양계 전체 질량의 **99.86%**를 혼자 차지하는 초거대 불꽃 덩어리입니다.\n- 강력한 중력으로 모든 행성을 공전 궤도에 묶어두며, 생명체의 근원인 빛과 에너지를 공급합니다.\n\n---\n\n#### 2. 단단한 바위로 이루어진 [지구형 행성 (내행성 4총사)] 🪨\n태양과 가까워 비교적 따뜻하고, 단단한 지표면(땅)이 있는 암석형 행성들입니다:\n\n1. ☿ **수성 (Mercury)**: 태양과 가장 가까운 막내 행성. 대기가 없어 낮(430℃)과 밤(-180℃)의 온도차가 극단적입니다.\n2. ♀ **금성 (Venus)**: 가장 뜨거운 행성(약 465℃). 두꺼운 이산화탄소 대기와 온실효과로 펄펄 끓는 용광로 같은 곳입니다.\n3. ⊕ **지구 (Earth)**: 우리가 살아 숨 쉬는 기적의 별! 액체 상태의 물과 생명체가 존재하는 유일한 곳입니다.\n4. ♂ **화성 (Mars)**: 붉은 산화철 모래로 뒤덮인 행성. 과거 물의 흔적이 발견되어 인류의 미래 거주지로 가장 유력한 후보입니다.\n\n---\n\n#### 3. 돌멩이들의 경계선: 소행성대 (Asteroid Belt) 🪐\n- 화성과 목성 사이에는 수백만 개의 암석 파편들이 도넛 형태로 태양을 돌고 있습니다.\n\n---\n\n#### 4. 거대한 가스와 얼음으로 뭉쳐진 [목성형 행성 (외행성 4총사)] 🌀\n태양과 멀리 떨어져 엄청나게 거대하며, 지표면이 기체와 얼음으로 덮여 있습니다:\n\n5. ♃ **목성 (Jupiter)**: 태양계의 맏형이자 가장 거대한 행성! 지구 1,300개가 들어갈 크기이며, 수백 년째 부는 붉은 폭풍 '대적점'이 유명합니다.\n6. ♄ **토성 (Saturn)**: 태양계 최고의 미모를 자랑하는 행성! 얼음과 암석 조각들로 이루어진 거대하고 찬란한 고리(Ring)를 지녔습니다.\n7. ♅ **천왕성 (Uranus)**: 메탄 대기 때문에 신비로운 청록색을 띠며, 공처럼 옆으로 누워서 자전하는 별난 행성입니다.\n8. ♆ **해왕성 (Neptune)**: 태양계 최외곽의 짙푸른 얼음 거인. 시속 2,000km가 넘는 태양계에서 가장 사나운 초강풍이 휘몰아칩니다.\n\n---\n\n#### 💡 1초 암기 공식!\n👉 **\"수 - 금 - 지 - 화 - 목 - 토 - 천 - 해\"**\n\n> 🌟 **안내**: 현재 **[Deterministic Mock (오프라인 지식 베이스)]**에서 즉각 응답을 제공하였습니다. 드롭다운에서 **Google Gemini**를 선택하시면 실시간 생성형 AI로 더욱 심화된 천문학 지식을 탐색하실 수 있습니다!"
            }

        # Otherwise informative finish
        return {
            "thought": "Goal has been processed. Providing informative offline guide.",
            "tool_calls": [],
            "content": f"'{last_message}'에 대한 요청을 확인했습니다.\n\n💡 **현재 [Deterministic Mock (오프라인 모드)]로 동작 중입니다.**\n- 오프라인 모드는 API 키 결제 없이 **코드 생성, AST 문법 검증, 자가 치유(Self-Healing)** 엔지니어링 루프를 100% 무료로 체험하기 위한 모의 엔진입니다.\n- 실시간 생성형 AI 지능 탐색을 원하시면, 좌측 드롭다운에서 **Google Gemini**를 선택해 주세요!"
        }


class OpenAICompatibleProvider(BaseLLMProvider):
    """Provider for OpenAI, DeepSeek, and local vLLM/Ollama OpenAI-compatible endpoints."""

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        import httpx
        self.client = httpx.Client(timeout=60.0)
        self.api_key = config.api_key or "no-key"
        self.base_url = config.base_url or "https://api.openai.com/v1"

    def generate(
        self,
        messages: List[Message],
        tools_schema: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload: Dict[str, Any] = {
            "model": self.config.model or "gpt-4o",
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": self.config.temperature
        }
        if tools_schema:
            payload["tools"] = tools_schema
            payload["tool_choice"] = "auto"

        response = self.client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        choice = data["choices"][0]["message"]
        content = choice.get("content") or ""
        
        raw_tool_calls = choice.get("tool_calls") or []
        parsed_tools = []
        for tc in raw_tool_calls:
            fn = tc.get("function", {})
            args = fn.get("arguments", "{}")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            parsed_tools.append(
                ToolCall(
                    id=tc.get("id", "call_0"),
                    name=fn.get("name", "unknown"),
                    arguments=args
                )
            )

        # Extract thought if CoT reasoning tags are present
        thought = "Reasoning step completed."
        thought_match = re.search(r"<thought>(.*?)</thought>", content, re.DOTALL)
        if thought_match:
            thought = thought_match.group(1).strip()
            content = re.sub(r"<thought>.*?</thought>", "", content, flags=re.DOTALL).strip()

        return {
            "thought": thought,
            "tool_calls": parsed_tools,
            "content": content
        }


class GeminiProvider(BaseLLMProvider):
    """Native Google Gemini REST API Provider."""

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        import os
        import httpx
        self.client = httpx.Client(timeout=45.0)
        self.api_key = config.api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model = config.model or "gemini-2.5-flash"
        if not self.model or self.model in ["mock-model", "gpt-4o"]:
            self.model = "gemini-2.5-flash"

    def generate(
        self,
        messages: List[Message],
        tools_schema: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        if not self.api_key or self.api_key == "no-key":
            return {
                "thought": "Gemini API key missing.",
                "tool_calls": [],
                "content": "[Google Gemini 오류] GEMINI_API_KEY가 설정되지 않았습니다. .env 파일에 GEMINI_API_KEY를 입력해 주세요."
            }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        contents = []
        for m in messages:
            role = "user" if m.role == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": m.content}]
            })

        payload = {"contents": contents}

        try:
            resp = self.client.post(url, json=payload)
            if resp.status_code != 200:
                return {
                    "thought": f"Gemini API returned status {resp.status_code}",
                    "tool_calls": [],
                    "content": f"[Google Gemini 오류: HTTP {resp.status_code}]\n{resp.text}"
                }
            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                return {
                    "thought": "No response candidates from Gemini.",
                    "tool_calls": [],
                    "content": "Gemini로부터 응답을 수신하지 못했습니다."
                }
            parts = candidates[0].get("content", {}).get("parts", [])
            text = "".join([p.get("text", "") for p in parts])
            return {
                "thought": "Successfully generated response via Google Gemini.",
                "tool_calls": [],
                "content": text
            }
        except Exception as e:
            return {
                "thought": f"Gemini connection error: {str(e)}",
                "tool_calls": [],
                "content": f"[Google Gemini 통신 오류] {str(e)}"
            }



class AnthropicClaudeProvider(BaseLLMProvider):
    """Native Anthropic Claude REST API Provider with intelligent graceful fallback."""

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        import os
        import httpx
        self.client = httpx.Client(timeout=45.0)
        self.api_key = config.api_key or os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
        self.model = config.model or "claude-3-5-sonnet-20241022"
        if not self.model or self.model in ["mock-model", "gpt-4o"]:
            self.model = "claude-3-5-sonnet-20241022"

    def generate(
        self,
        messages: List[Message],
        tools_schema: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        import os
        # If Anthropic API key is not set, check if Gemini key is available for smart delegation
        if not self.api_key or self.api_key == "no-key":
            gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if gemini_key:
                gemini_prov = GeminiProvider(self.config)
                res = gemini_prov.generate(messages, tools_schema)
                prefix = "> ⚡ **[지능형 오토 라우팅]** 서버에 `ANTHROPIC_API_KEY`가 미설정 상태여서, 활성화된 **Google Gemini 2.5 Flash** 엔진이 즉각 최상의 답변을 생성했습니다.\n\n"
                res["content"] = prefix + res.get("content", "")
                return res
            mock_prov = DeterministicMockProvider(self.config)
            return mock_prov.generate(messages, tools_schema)

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        formatted = []
        for m in messages:
            role = "user" if m.role == "user" else "assistant"
            formatted.append({"role": role, "content": m.content})

        payload = {
            "model": self.model,
            "max_tokens": 2048,
            "messages": formatted
        }
        try:
            resp = self.client.post(url, headers=headers, json=payload)
            if resp.status_code != 200:
                gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
                if gemini_key:
                    gemini_prov = GeminiProvider(self.config)
                    res = gemini_prov.generate(messages, tools_schema)
                    res["content"] = f"> ⚠️ **[안내]** Claude API 오류 (HTTP {resp.status_code})로 인해 **Google Gemini 2.5 Flash** 엔진으로 자동 전환되어 답변을 생성했습니다.\n\n" + res.get("content", "")
                    return res
                return {
                    "thought": f"Claude API returned status {resp.status_code}",
                    "tool_calls": [],
                    "content": f"[Anthropic Claude 오류: HTTP {resp.status_code}]\n{resp.text}"
                }
            data = resp.json()
            content_blocks = data.get("content", [])
            text = "".join([b.get("text", "") for b in content_blocks if b.get("type") == "text"])
            return {
                "thought": "Successfully generated response via Anthropic Claude.",
                "tool_calls": [],
                "content": text
            }
        except Exception as e:
            gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if gemini_key:
                gemini_prov = GeminiProvider(self.config)
                res = gemini_prov.generate(messages, tools_schema)
                res["content"] = f"> ⚠️ **[안내]** Claude 통신 에러로 인해 **Google Gemini 2.5 Flash** 엔진으로 자동 전환되어 답변을 생성했습니다.\n\n" + res.get("content", "")
                return res
            return {
                "thought": f"Claude connection error: {str(e)}",
                "tool_calls": [],
                "content": f"[Anthropic Claude 통신 오류] {str(e)}"
            }


def get_llm_provider(config: AgentConfig) -> BaseLLMProvider:
    """Factory function for LLM providers."""
    import os
    provider_name = (config.provider or "mock").lower()
    if provider_name == "mock":
        return DeterministicMockProvider(config)
    elif provider_name in ["gemini", "google"]:
        return GeminiProvider(config)
    elif provider_name in ["anthropic", "claude"]:
        return AnthropicClaudeProvider(config)
    elif provider_name in ["openai", "deepseek", "ollama", "vllm"]:
        return OpenAICompatibleProvider(config)
    else:
        # If Gemini API key is present on server, use Gemini as active provider, otherwise mock
        if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
            return GeminiProvider(config)
        return DeterministicMockProvider(config)
