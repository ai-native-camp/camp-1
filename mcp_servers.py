#!/usr/bin/env python3
"""MCP Servers 카탈로그 — GitHub README를 다운로드하여 파싱·검색한다.

사용법:
    python mcp_servers.py                  # 전체 목록 (카테고리별 개수 요약)
    python mcp_servers.py search slack     # "slack" 키워드 검색
    python mcp_servers.py list official    # 카테고리별 리스트 (reference|archived|official|community|framework)
    python mcp_servers.py list all        # 전체 리스트
    python mcp_servers.py stats            # 통계
"""

import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

README_URL = "https://raw.githubusercontent.com/modelcontextprotocol/servers/main/README.md"
CACHE_PATH = Path(__file__).parent / ".mcp-servers-cache.md"


# ── 데이터 구조 ────────────────────────────────────────────


@dataclass
class McpServer:
    name: str
    url: str
    description: str
    category: str  # reference | archived | official | community | framework


# ── 다운로드 ───────────────────────────────────────────────


def download_readme() -> str:
    """curl로 README.md를 다운로드하고 캐시에 저장한다."""
    result = subprocess.run(
        ["curl", "-sL", README_URL],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"다운로드 실패: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    CACHE_PATH.write_text(result.stdout, encoding="utf-8")
    return result.stdout


# ── 파싱 ───────────────────────────────────────────────────

# 섹션 헤더 → 카테고리 매핑
SECTION_MAP = {
    "Reference Servers": "reference",
    "Archived": "archived",
    "Official Integrations": "official",
    "Community Servers": "community",
    "For servers": "framework",
    "For clients": "framework",
}

# 서버 항목 패턴: 선택적 <img> 태그 + **[Name](URL)** - Description
SERVER_PATTERN = re.compile(
    r"^- (?:<img[^>]*>\s*)?(?:\*\*\[([^\]]+)\]\(([^)]+)\)\*\*)"
    r"(?:\s*[-–—]\s*(.+))?$"
)


def parse_servers(md: str) -> list[McpServer]:
    """마크다운에서 MCP 서버 항목을 추출한다."""
    servers: list[McpServer] = []
    current_category = ""

    for line in md.splitlines():
        stripped = line.strip()

        # 섹션 헤더 감지 (## 또는 ###)
        header_match = re.match(r"^#{2,3}\s+(?:[\U0001f300-\U0001faff\u2600-\u27bf]\s*)?(.+)$", stripped)
        if header_match:
            title = header_match.group(1).strip()
            for key, cat in SECTION_MAP.items():
                if key in title:
                    current_category = cat
                    break

        # 서버 항목 감지
        if not current_category:
            continue

        m = SERVER_PATTERN.match(stripped)
        if m:
            name = m.group(1).strip()
            url = m.group(2).strip()
            desc = (m.group(3) or "").strip()
            # 마크다운 링크 잔여물 정리
            desc = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", desc)
            servers.append(McpServer(name=name, url=url, description=desc, category=current_category))

    return servers


# ── 출력 ───────────────────────────────────────────────────

CATEGORY_LABELS = {
    "reference": "Reference Servers",
    "archived": "Archived",
    "official": "Official Integrations",
    "community": "Community Servers",
    "framework": "Frameworks",
}


def print_stats(servers: list[McpServer]) -> None:
    """카테고리별 통계를 출력한다."""
    counts: dict[str, int] = {}
    for s in servers:
        counts[s.category] = counts.get(s.category, 0) + 1

    print(f"\n{'='*50}")
    print(f" MCP Servers 카탈로그 — 총 {len(servers)}개")
    print(f"{'='*50}")
    for cat, label in CATEGORY_LABELS.items():
        c = counts.get(cat, 0)
        if c:
            print(f"  {label:<25} {c:>4}개")
    print(f"{'─'*50}")
    print(f"  {'합계':<25} {len(servers):>4}개\n")


def print_servers(servers: list[McpServer], title: str = "") -> None:
    """서버 목록을 보기 좋게 출력한다."""
    if title:
        print(f"\n── {title} ({len(servers)}개) ──\n")

    for s in servers:
        cat_tag = f"[{CATEGORY_LABELS.get(s.category, s.category)}]"
        desc_short = s.description[:80] + "…" if len(s.description) > 80 else s.description
        print(f"  {s.name:<30} {cat_tag:<25} {desc_short}")
        print(f"  {'':30} {s.url}")
        print()


def search(servers: list[McpServer], keyword: str) -> list[McpServer]:
    """이름, 설명, URL에서 키워드를 검색한다 (대소문자 무시)."""
    kw = keyword.lower()
    return [
        s for s in servers
        if kw in s.name.lower() or kw in s.description.lower() or kw in s.url.lower()
    ]


def output_json(servers: list[McpServer]) -> None:
    """JSON 형태로 출력한다."""
    print(json.dumps([asdict(s) for s in servers], ensure_ascii=False, indent=2))


# ── CLI ────────────────────────────────────────────────────


def main() -> None:
    args = sys.argv[1:]

    # 1. README 다운로드 & 파싱
    print("README.md 다운로드 중...", file=sys.stderr)
    md = download_readme()
    servers = parse_servers(md)
    print(f"파싱 완료: {len(servers)}개 서버 발견\n", file=sys.stderr)

    if not args:
        # 기본: 통계 출력
        print_stats(servers)
        print("사용법:")
        print("  python mcp_servers.py search <keyword>   키워드 검색")
        print("  python mcp_servers.py list <category>    카테고리별 리스트")
        print("  python mcp_servers.py list all           전체 리스트")
        print("  python mcp_servers.py stats              통계")
        print("  python mcp_servers.py json               JSON 출력")
        print("  python mcp_servers.py json <keyword>     검색 결과 JSON")
        print()
        print("카테고리: reference, archived, official, community, framework")
        return

    cmd = args[0].lower()

    if cmd == "search" and len(args) >= 2:
        keyword = " ".join(args[1:])
        results = search(servers, keyword)
        if results:
            print_servers(results, f'"{keyword}" 검색 결과')
        else:
            print(f'\n  "{keyword}"에 해당하는 서버가 없습니다.\n')

    elif cmd == "list":
        cat = args[1].lower() if len(args) >= 2 else "all"
        if cat == "all":
            for c, label in CATEGORY_LABELS.items():
                group = [s for s in servers if s.category == c]
                if group:
                    print_servers(group, label)
        else:
            group = [s for s in servers if s.category == cat]
            label = CATEGORY_LABELS.get(cat, cat)
            if group:
                print_servers(group, label)
            else:
                print(f'\n  카테고리 "{cat}"에 해당하는 서버가 없습니다.')
                print(f"  가능한 카테고리: {', '.join(CATEGORY_LABELS.keys())}\n")

    elif cmd == "stats":
        print_stats(servers)

    elif cmd == "json":
        if len(args) >= 2:
            keyword = " ".join(args[1:])
            output_json(search(servers, keyword))
        else:
            output_json(servers)

    else:
        print(f'알 수 없는 명령: {cmd}', file=sys.stderr)
        print("사용법: python mcp_servers.py [search|list|stats|json] [args...]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
