# Block 2: /mcp 명령어로 도구 탐색

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/mcp
> ```

## EXPLAIN

### /mcp 명령어란?

Claude Code 안에서 `/mcp`를 입력하면 **연결된 MCP 서버의 상태와 도구를 한눈에 볼 수 있다.**

| 기능 | 설명 |
|------|------|
| 서버 목록 | 연결된 모든 MCP 서버 표시 |
| 연결 상태 | 각 서버의 연결/오류 상태 확인 |
| 도구 목록 | 각 서버가 제공하는 도구(Tools) 확인 |
| OAuth 인증 | 로그인이 필요한 서버 인증 처리 |

### /mcp에서 볼 수 있는 것

```
/mcp 실행 시
┌──────────────────────────────────────────┐
│ MCP Servers                              │
│                                          │
│ ✅ context7 (stdio)                      │
│    Tools: resolve-library-id, query-docs │
│                                          │
│ ✅ slack (http)                          │
│    Tools: slack_send_message,            │
│           slack_read_channel, ...        │
│                                          │
│ ❌ notion (http) - 인증 필요             │
│    → "인증" 선택하여 로그인              │
└──────────────────────────────────────────┘
```

### MCP 도구의 이름 규칙

MCP 도구는 `mcp__서버이름__도구이름` 형태로 불린다:

| 서버 | 도구 | 전체 이름 |
|------|------|-----------|
| Slack | slack_read_channel | `mcp__claude_ai_Slack__slack_read_channel` |
| context7 | query-docs | `mcp__context7__query-docs` |

> 이름이 길지만 직접 외울 필요 없다. Claude에게 "Slack 메시지 읽어줘"라고 하면 알아서 올바른 도구를 호출한다.

### claude.ai에서 MCP 연결하기 (가장 쉬운 방법)

터미널에서 `claude mcp add` 명령어 외에, **웹 브라우저에서 클릭 몇 번으로** MCP를 연결하는 방법이 있다:

```
1. https://claude.ai/settings/connectors 접속
2. 연결하고 싶은 서비스 선택 (Slack, Notion 등)
3. 로그인 후 연결 승인
4. Claude Code에서 /mcp → "claude.ai" 섹션에 자동 등록!
```

```
/mcp 실행 시 (Connectors로 연결한 경우)
┌──────────────────────────────────────────┐
│ MCP Servers                              │
│                                          │
│ 📌 claude.ai                             │
│ ✅ Slack                                 │
│    Tools: slack_send_message,            │
│           slack_read_channel, ...        │
│                                          │
│ 📌 local                                 │
│ ✅ context7 (stdio)                      │
│    Tools: resolve-library-id, query-docs │
└──────────────────────────────────────────┘
```

> **Slack을 처음 연결한다면 이 방법이 가장 쉽다.** 터미널 명령어 없이 웹에서 로그인만 하면 된다.

### OAuth 인증이 필요한 서버

Notion, GitHub, Sentry 같은 서비스는 로그인이 필요하다:

```
1. /mcp 실행
2. 인증이 필요한 서버 옆의 "인증" 선택
3. 브라우저가 열리면 로그인
4. 인증 완료 → 서버 연결됨
```

> 인증 토큰은 자동 저장되고 자동 갱신된다. 한 번만 하면 된다.

## EXECUTE

3단계로 /mcp 명령어를 체험해보자:

**1단계: /mcp 실행**

Claude Code에서 아래를 입력한다:

```
/mcp
```

> 연결된 서버 목록이 나온다. 각 서버의 상태(연결/오류)와 제공하는 도구를 확인하자.

**2단계: 도구 목록 확인**

/mcp 화면에서 각 서버를 열어보면 그 서버가 제공하는 도구(Tools) 목록이 나온다.
어떤 도구가 있는지 살펴보자.

**3단계: 도구 실제 사용**

연결된 서버의 도구를 Claude에게 사용해달라고 요청해본다:

Context7이 있다면:
```
context7으로 React의 useEffect 사용법을 검색해줘
```

Slack이 있다면:
```
Slack에서 가장 최근 메시지 5개를 보여줘
```

Fetch가 있다면:
```
https://news.ycombinator.com 에서 오늘의 인기 글 3개를 가져와줘
```

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "/mcp 명령어의 주요 역할은?",
    "header": "Quiz 2",
    "options": [
      {"label": "연결된 MCP 서버 상태와 도구 목록 확인", "description": "서버 연결 상태, 제공 도구, OAuth 인증까지"},
      {"label": "새 MCP 서버를 설치하는 명령어", "description": "설치는 claude mcp add로 함"},
      {"label": "MCP 서버를 삭제하는 명령어", "description": "삭제는 claude mcp remove로 함"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
피드백: "맞습니다! /mcp = 현황 파악. 설치는 `claude mcp add`, 삭제는 `claude mcp remove`입니다. /mcp는 '지금 뭐가 연결되어 있지?' 할 때 씁니다."
