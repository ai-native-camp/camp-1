# Block 1: MCP 서버 추가하기

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/mcp
> ```

## EXPLAIN

### MCP 서버를 추가하는 3가지 방법

MCP 서버는 **어디서 실행되느냐**에 따라 추가 방법이 다르다.

| 방법 | 서버 위치 | 비유 | 언제 쓰나 |
|------|-----------|------|-----------|
| **HTTP** | 클라우드 | 웹사이트 접속 | Notion, Sentry 등 클라우드 서비스 |
| **SSE** | 클라우드 (구버전) | HTTP의 이전 버전 | 아직 HTTP 미지원인 서비스 |
| **stdio** | 내 컴퓨터 | 앱 설치 | 로컬 파일, DB 접근 |

### 핵심 명령어: `claude mcp add`

```
claude mcp add --transport [방법] [이름] [주소]
```

#### 방법 1: HTTP (가장 추천)

```bash
# Notion에 연결
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Sentry에 연결
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

#### 방법 2: stdio (내 컴퓨터에서 실행)

```bash
# 파일 시스템 접근 서버
claude mcp add --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem /path/to/folder
```

> `--` 뒤에 오는 건 MCP 서버를 실행하는 명령어다.

### 서버 관리 명령어

| 명령어 | 동작 |
|--------|------|
| `claude mcp list` | 설치된 서버 목록 |
| `claude mcp get [이름]` | 서버 상세 정보 |
| `claude mcp remove [이름]` | 서버 제거 |

### 저장 범위 (scope)

| scope | 저장 위치 | 누가 쓰나 |
|-------|-----------|-----------|
| `local` (기본) | 이 프로젝트에서만 | 나만 |
| `project` | `.mcp.json` 파일 | 팀 전체 (git으로 공유) |
| `user` | `~/.claude.json` | 모든 프로젝트에서 나만 |

```bash
# 모든 프로젝트에서 쓸 서버 추가
claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp
```

## EXECUTE

실제로 MCP 서버를 하나 추가해보자. 아래 중 하나를 선택해서 실행한다:

**옵션 A: Context7 (프로그래밍 문서 검색 — 추천)**

```bash
claude mcp add --transport stdio context7 -- npx -y @upstash/context7-mcp@latest
```

> Context7은 라이브러리 공식 문서를 실시간으로 검색해주는 MCP 서버다.

**옵션 B: Notion (노션 사용자)**

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**옵션 C: Fetch (웹페이지 가져오기)**

```bash
claude mcp add --transport stdio fetch -- npx -y @anthropic-ai/mcp-fetch@latest
```

설치 후 확인:

```bash
claude mcp list
```

> 방금 추가한 서버가 목록에 보이면 성공!
> Claude Code를 재시작해야 적용되는 경우가 있다. 새 세션을 시작해보자.

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "클라우드 서비스(Notion, Sentry)에 연결할 때 추천하는 transport 방법은?",
    "header": "Quiz 1",
    "options": [
      {"label": "HTTP", "description": "클라우드 서비스 연결의 표준 방식"},
      {"label": "stdio", "description": "stdio는 내 컴퓨터에서 로컬 실행할 때 사용"},
      {"label": "FTP", "description": "MCP에서 FTP는 지원하지 않음"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
피드백: "정확합니다! 클라우드 = HTTP, 로컬 = stdio. 이 두 가지만 기억하면 됩니다."
