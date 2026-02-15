#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx"]
# ///
"""MCP 서버 검색 도구

GitHub의 MCP 서버 목록에서 원하는 서비스를 검색하고
.mcp.json 설정을 생성한다.

Usage:
    python mcp_servers.py search <keyword>     # 서버 검색
    python mcp_servers.py generate <server>    # .mcp.json 설정 생성
    python mcp_servers.py download             # README.md 최신 다운로드
"""

import json
import re
import sys
import time
from pathlib import Path

import httpx

README_URL = "https://raw.githubusercontent.com/modelcontextprotocol/servers/main/README.md"
CACHE_DIR = Path(__file__).parent / ".cache"
CACHE_FILE = CACHE_DIR / "mcp-servers-readme.md"
CACHE_META = CACHE_DIR / "cache-meta.json"
CACHE_TTL = 3600  # 1시간


# ─── 캐시 관리 ───────────────────────────────────────────────


def _is_cache_valid() -> bool:
    """캐시가 유효한지 확인 (1시간 이내)."""
    if not CACHE_FILE.exists() or not CACHE_META.exists():
        return False
    try:
        meta = json.loads(CACHE_META.read_text())
        return (time.time() - meta.get("downloaded_at", 0)) < CACHE_TTL
    except (json.JSONDecodeError, KeyError):
        return False


def _save_cache(content: str) -> None:
    """README 내용을 로컬에 캐시."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(content, encoding="utf-8")
    CACHE_META.write_text(
        json.dumps({"downloaded_at": time.time()}), encoding="utf-8"
    )


def _load_cache() -> str | None:
    """캐시된 README를 읽는다."""
    if CACHE_FILE.exists():
        return CACHE_FILE.read_text(encoding="utf-8")
    return None


# ─── 다운로드 ────────────────────────────────────────────────


def download_readme(force: bool = False) -> str:
    """README.md를 다운로드하고 캐시한다.

    네트워크 실패 시 캐시된 파일을 사용한다.
    """
    if not force and _is_cache_valid():
        cached = _load_cache()
        if cached:
            return cached

    try:
        resp = httpx.get(README_URL, timeout=15, follow_redirects=True)
        resp.raise_for_status()
        content = resp.text
        _save_cache(content)
        print("README.md 다운로드 완료 (최신)")
        return content
    except (httpx.HTTPError, httpx.TimeoutException) as e:
        cached = _load_cache()
        if cached:
            print(f"네트워크 오류 ({e}). 캐시된 파일을 사용합니다.")
            return cached
        print(f"오류: README를 다운로드할 수 없고 캐시도 없습니다. ({e})")
        sys.exit(1)


# ─── 파싱 ────────────────────────────────────────────────────


def parse_servers(readme: str) -> list[dict]:
    """README에서 MCP 서버 목록을 파싱한다.

    서버 항목 형식:
      <img .../> **[Name](url)** - Description
    또는:
      - **[Name](url)** - Description
    """
    servers: list[dict] = []

    # 패턴: **[Name](URL)** 뒤에 설명이 오는 형태
    pattern = re.compile(
        r"\*\*\[([^\]]+)\]\(([^)]+)\)\*\*"  # **[Name](URL)**
        r"\s*[-–—:]\s*"  # 구분자
        r"(.+)"  # 설명
    )

    for line in readme.splitlines():
        m = pattern.search(line)
        if not m:
            continue

        name = m.group(1).strip()
        url = m.group(2).strip()
        description = m.group(3).strip()
        # 설명에서 후행 마크다운 정리
        description = re.sub(r"\s*\[.*?\]\(.*?\)\s*$", "", description)
        description = description.rstrip(" .")

        # GitHub URL에서 패키지명 추정
        package = _guess_package(name, url)

        servers.append(
            {
                "name": name,
                "url": url,
                "description": description,
                "package": package,
            }
        )

    return servers


def _guess_package(name: str, url: str) -> str:
    """GitHub URL에서 npm 패키지명을 추정한다."""
    # 잘 알려진 매핑
    known: dict[str, str] = {
        "Slack": "@anthropic/slack-mcp",
        "GitHub": "@github/github-mcp-server",
        "Notion": "@notionhq/notion-mcp-server",
        "Linear": "@linear/linear-mcp-server",
        "Google Maps": "@anthropic/google-maps-mcp",
        "Google Drive": "@anthropic/google-drive-mcp",
        "Puppeteer": "@anthropic/puppeteer-mcp",
        "Filesystem": "@anthropic/filesystem-mcp",
        "PostgreSQL": "@anthropic/postgres-mcp",
        "Sentry": "@anthropic/sentry-mcp",
        "Memory": "@anthropic/memory-mcp",
        "Brave Search": "@anthropic/brave-search-mcp",
        "Fetch": "@anthropic/fetch-mcp",
        "Exa": "exa-mcp-server",
        "Supabase": "@supabase/mcp-server-supabase",
    }
    if name in known:
        return known[name]

    # GitHub URL에서 org/repo 추출
    gh_match = re.match(r"https?://github\.com/([^/]+)/([^/#]+)", url)
    if gh_match:
        org, repo = gh_match.group(1), gh_match.group(2)
        # npm scoped package 추정: @org/repo
        return f"@{org}/{repo}"

    return name.lower().replace(" ", "-")


# ─── 환경변수 추정 ───────────────────────────────────────────


_ENV_HINTS: dict[str, dict[str, str]] = {
    "slack": {"SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"},
    "github": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"},
    "notion": {"NOTION_API_KEY": "${NOTION_API_KEY}"},
    "linear": {"LINEAR_API_KEY": "${LINEAR_API_KEY}"},
    "google-maps": {"GOOGLE_MAPS_API_KEY": "${GOOGLE_MAPS_API_KEY}"},
    "google-drive": {"GOOGLE_DRIVE_CREDENTIALS": "${GOOGLE_DRIVE_CREDENTIALS}"},
    "brave-search": {"BRAVE_API_KEY": "${BRAVE_API_KEY}"},
    "sentry": {"SENTRY_AUTH_TOKEN": "${SENTRY_AUTH_TOKEN}"},
    "postgres": {"POSTGRES_URL": "${POSTGRES_URL}"},
    "supabase": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}",
        "SUPABASE_PROJECT_REF": "${SUPABASE_PROJECT_REF}",
    },
    "exa": {"EXA_API_KEY": "${EXA_API_KEY}"},
    "firebase": {"FIREBASE_TOKEN": "${FIREBASE_TOKEN}"},
    "mongodb": {"MONGODB_URI": "${MONGODB_URI}"},
    "stripe": {"STRIPE_SECRET_KEY": "${STRIPE_SECRET_KEY}"},
    "twilio": {
        "TWILIO_ACCOUNT_SID": "${TWILIO_ACCOUNT_SID}",
        "TWILIO_AUTH_TOKEN": "${TWILIO_AUTH_TOKEN}",
    },
}


def _guess_env(name: str, package: str) -> dict[str, str]:
    """서버명/패키지명에서 필요한 환경변수를 추정한다."""
    key = name.lower().replace(" ", "-")
    if key in _ENV_HINTS:
        return _ENV_HINTS[key]
    # 패키지명에서도 시도
    for hint_key, env_vars in _ENV_HINTS.items():
        if hint_key in package.lower():
            return env_vars
    # 범용: 서버명 기반 토큰
    token_name = re.sub(r"[^A-Z0-9]", "_", name.upper()) + "_API_KEY"
    return {token_name: f"${{{token_name}}}"}


# ─── 검색 ────────────────────────────────────────────────────


def search_servers(keyword: str, servers: list[dict]) -> list[dict]:
    """키워드로 서버를 검색한다 (대소문자 무시)."""
    kw = keyword.lower()
    results = []
    for s in servers:
        if (
            kw in s["name"].lower()
            or kw in s["description"].lower()
            or kw in s["package"].lower()
            or kw in s["url"].lower()
        ):
            results.append(s)
    return results


def print_search_results(results: list[dict], keyword: str) -> None:
    """검색 결과를 보기 좋게 출력한다."""
    if not results:
        print(f'"{keyword}"에 대한 검색 결과가 없습니다.')
        return

    print(f'"{keyword}" 검색 결과: {len(results)}건\n')
    for i, s in enumerate(results, 1):
        env = _guess_env(s["name"], s["package"])
        env_str = ", ".join(env.keys())
        print(f"  {i}. {s['name']} ({s['package']})")
        print(f"     {s['description']}")
        print(f"     설치: npx -y {s['package']}")
        if env_str:
            print(f"     환경변수: {env_str}")
        print(f"     GitHub: {s['url']}")
        print()


# ─── .mcp.json 생성 ─────────────────────────────────────────


def generate_config(server_query: str, servers: list[dict]) -> str | None:
    """서버에 대한 .mcp.json 설정 예시를 JSON으로 생성한다."""
    # 정확한 패키지명 매칭 우선
    match = None
    for s in servers:
        if s["package"] == server_query or s["name"].lower() == server_query.lower():
            match = s
            break

    # 부분 매칭
    if not match:
        results = search_servers(server_query, servers)
        if len(results) == 1:
            match = results[0]
        elif len(results) > 1:
            print(f'"{server_query}"에 대한 결과가 여러 개입니다. 더 구체적으로 지정하세요:\n')
            for s in results:
                print(f"  - {s['package']} ({s['name']})")
            return None
        else:
            print(f'"{server_query}"에 해당하는 서버를 찾을 수 없습니다.')
            return None

    # 설정명: 패키지에서 간단한 이름 추출
    config_name = match["name"].lower().replace(" ", "-")

    env = _guess_env(match["name"], match["package"])

    config = {
        config_name: {
            "command": "npx",
            "args": ["-y", match["package"]],
            "env": env,
        }
    }

    return json.dumps(config, indent=2, ensure_ascii=False)


# ─── CLI ─────────────────────────────────────────────────────


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "download":
        download_readme(force=True)
        print("캐시가 갱신되었습니다.")

    elif command == "search":
        if len(sys.argv) < 3:
            print("사용법: python mcp_servers.py search <keyword>")
            sys.exit(1)
        keyword = " ".join(sys.argv[2:])
        readme = download_readme()
        servers = parse_servers(readme)
        results = search_servers(keyword, servers)
        print_search_results(results, keyword)

    elif command == "generate":
        if len(sys.argv) < 3:
            print("사용법: python mcp_servers.py generate <server_name_or_package>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        readme = download_readme()
        servers = parse_servers(readme)
        config_json = generate_config(query, servers)
        if config_json:
            print(f"\n.mcp.json 설정 예시:\n")
            print(config_json)

    else:
        print(f'알 수 없는 명령: "{command}"')
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
