# Block 3: 인기 MCP 서버 탐색 및 설치

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/mcp#popular-mcp-servers
> 📖 MCP 서버 목록: https://github.com/modelcontextprotocol/servers/blob/main/README.md
> ```

## EXPLAIN

### MCP 서버는 어디서 찾나?

| 출처 | URL | 특징 |
|------|-----|------|
| **Claude Code 공식 문서** | https://code.claude.com/docs/ko/mcp | Claude Code와 호환 확인된 서버 |
| **MCP 서버 GitHub** | https://github.com/modelcontextprotocol/servers | 전체 목록 (레퍼런스 + 서드파티) |
| **MCP Registry** | https://registry.modelcontextprotocol.io | 최신 서버 검색 |

### 비개발자에게 추천하는 인기 서버

#### 커뮤니케이션

| 서버 | 할 수 있는 것 | 추가 명령어 |
|------|--------------|-------------|
| **Slack** | 메시지 읽기/보내기, 채널 검색 | `claude mcp add --transport http slack https://api.slack.com/mcp` |
| **Gmail** | 이메일 읽기/보내기, 검색 | 별도 설정 필요 (Google API) |

#### 생산성

| 서버 | 할 수 있는 것 | 추가 명령어 |
|------|--------------|-------------|
| **Notion** | 페이지 읽기/쓰기, DB 쿼리 | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| **Google Calendar** | 일정 조회/생성 | 별도 설정 필요 (Google API) |
| **Linear** | 이슈 관리, 프로젝트 추적 | `claude mcp add --transport http linear https://mcp.linear.app/sse` |

#### 개발

| 서버 | 할 수 있는 것 | 추가 명령어 |
|------|--------------|-------------|
| **GitHub** | PR 리뷰, 이슈 관리 | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` |
| **Sentry** | 에러 모니터링, 디버깅 | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` |
| **Context7** | 라이브러리 문서 검색 | `claude mcp add --transport stdio context7 -- npx -y @upstash/context7-mcp@latest` |

#### 데이터

| 서버 | 할 수 있는 것 | 추가 명령어 |
|------|--------------|-------------|
| **Fetch** | 웹페이지 내용 가져오기 | `claude mcp add --transport stdio fetch -- npx -y @anthropic-ai/mcp-fetch@latest` |
| **Filesystem** | 로컬 파일 읽기/쓰기 | `claude mcp add --transport stdio fs -- npx -y @modelcontextprotocol/server-filesystem /path` |
| **Memory** | 지식 그래프 기반 기억 | `claude mcp add --transport stdio memory -- npx -y @modelcontextprotocol/server-memory` |

### 서버 선택 기준

```
내가 매일 쓰는 도구가 뭐지?
  │
  ├─ Slack 많이 쓴다 → Slack MCP
  ├─ Notion에 정보 정리 → Notion MCP
  ├─ 이메일 관리 → Gmail MCP
  ├─ 코딩한다 → GitHub + Sentry MCP
  └─ 웹 검색/리서치 → Fetch MCP
```

> 한 번에 다 설치하지 말고, **가장 자주 쓰는 도구 1~2개**부터 시작하자.

### MCP의 한계 — 왜 Skill을 직접 만들어야 하나?

MCP 서버는 **남이 만들어둔 범용 도구**다. 설치만 하면 바로 쓸 수 있어서 편하지만, 한계가 있다:

```
MCP 서버 (남이 만든 것)              나만의 Skill (직접 만든 것)
  ├─ 설치 즉시 사용 가능              ├─ 내 워크플로우에 딱 맞게 설계
  ├─ 범용적 기능 제공                 ├─ 필요한 기능만 조합
  ├─ 커스텀이 어려움 ⚠️              ├─ 자유롭게 수정 가능
  └─ 모든 기능이 다 필요한 건 아님     └─ 진짜 효율적인 자동화
```

예를 들어, Slack MCP를 설치하면 메시지를 읽고 보낼 수 있다. 하지만 **"매일 아침 3개 채널의 중요 메시지를 요약해서 Notion에 정리해줘"** 같은 나만의 워크플로우는 MCP만으로는 만들 수 없다.

> **결론: MCP로 시작하되, 진짜 효과적인 워크플로우를 원한다면 직접 Skill로 만들자.**
> Day 2에서 이걸 직접 해본다!

## EXECUTE

3단계로 인기 서버를 탐색하고 설치해보자:

**1단계: 공식 문서에서 인기 서버 확인**

Claude에게 물어보자:

```
Claude Code 공식 문서에서 추천하는 인기 MCP 서버 목록을 보여줘. 각각 뭘 할 수 있는지도 알려줘
```

**2단계: 내게 필요한 서버 선택 및 설치**

위 목록에서 하나를 골라 설치한다. 추천 순서:

1. 업무에서 가장 많이 쓰는 도구
2. 모르겠으면 **Notion** 또는 **Fetch**부터

설치 후 Claude Code를 **새 세션으로 재시작**한다 (기존 세션 종료 → `claude` 다시 실행).

**3단계: 설치한 서버 도구 사용해보기**

새 세션에서 `/mcp`로 서버가 연결되었는지 확인한 후, Claude에게 도구를 사용해달라고 요청한다.

```
방금 설치한 MCP 서버의 도구를 사용해서 뭔가 해봐
```

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "MCP 서버를 선택할 때 가장 좋은 기준은?",
    "header": "Quiz 3",
    "options": [
      {"label": "내가 매일 쓰는 도구부터 1~2개", "description": "실제 업무에서 바로 활용할 수 있는 것"},
      {"label": "인기 순위 1위부터 전부 설치", "description": "안 쓰는 서버는 리소스 낭비"},
      {"label": "가장 기술적으로 복잡한 것", "description": "복잡할수록 좋은 게 아님"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
피드백: "맞습니다! 매일 쓰는 도구부터 연결하면 바로 체감할 수 있습니다. 나중에 필요할 때 하나씩 추가하면 됩니다."
