"""
Nexus-Agent Viral Launch Autopilot
Automatically launches pre-filled browser submission tabs for 1-click publishing.
"""

import urllib.parse
import webbrowser
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

URLS = [
    {
        "platform": "Hacker News (Show HN)",
        "url": "https://news.ycombinator.com/submitlink?" + urllib.parse.urlencode({
            "u": "https://github.com/parkain707/nexus-agent",
            "t": "Show HN: Nexus-Agent – Autonomous self-healing AI coding agent with AST validation & time-travel rollback"
        }),
        "instruction": "Title and URL are already pre-filled! Just click [Submit]."
    },
    {
        "platform": "Twitter / X",
        "url": "https://twitter.com/intent/tweet?" + urllib.parse.urlencode({
            "text": "Nexus-Agent – Autonomous Self-Healing AI Coding Agent with AST Validation & Time-Travel Rollback! 🚀\n\n100% Open-Source & Runs Offline with Zero-Cost Mock Mode.\n\n⭐ GitHub: https://github.com/parkain707/nexus-agent\n\n#AI #Python #OpenSource #DevTools"
        }),
        "instruction": "Tweet text is already pre-filled! Just click [Post]."
    },
    {
        "platform": "Reddit (r/LocalLLaMA)",
        "url": "https://www.reddit.com/r/LocalLLaMA/submit?" + urllib.parse.urlencode({
            "title": "[P] Nexus-Agent: Autonomous self-healing coding agent with AST validation, time-travel rollback, and 100% offline mode",
            "url": "https://github.com/parkain707/nexus-agent"
        }),
        "instruction": "Title and Link are already pre-filled! Just click [Post]."
    },
    {
        "platform": "GeekNews (국내 1위 테크)",
        "url": "https://news.hada.io/submit?" + urllib.parse.urlencode({
            "url": "https://github.com/parkain707/nexus-agent",
            "title": "Show GN: Nexus-Agent - AST 사전 검증과 자가 치유(Self-Healing)를 갖춘 오픈소스 AI 코딩 에이전트"
        }),
        "instruction": "URL and Title are already pre-filled! Just click [Submit]."
    },
    {
        "platform": "Velog (국내 기술 블로그)",
        "url": "https://velog.io/write",
        "instruction": "Velog editor opened. Paste body from launch/VELOG_POST_KO.md and click [출간하기]."
    }
]

def main():
    print("=" * 65)
    print(">> NEXUS-AGENT // VIRAL LAUNCH AUTOPILOT")
    print("=" * 65)
    print("Pre-filling title, links, and content into your active browser tabs...")
    print("You only need to click [Submit / Post] on each tab!\n")

    for i, item in enumerate(URLS, 1):
        print(f"[{i}/{len(URLS)}] Launching {item['platform']}...")
        print(f"       -> {item['instruction']}")
        try:
            webbrowser.open(item["url"])
        except Exception as e:
            print(f"       -> Error opening browser: {e}")

    print("\n" + "=" * 65)
    print("[OK] All 5 launch tabs have been opened in your default browser!")
    print("If you are already logged in, you can complete all 5 in under 30 seconds.")
    print("=" * 65)

if __name__ == "__main__":
    main()
