# Block 2: 도구 연결

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://modelcontextprotocol.io/
> 📖 공식 문서: https://code.claude.com/en/docs/claude-code/mcp
> ```

## EXPLAIN

### Day 1 복습: MCP

Day 1 Block 3-3에서 **MCP**를 배웠다. "Claude와 외부 도구를 연결하는 표준 프로토콜. Slack, Calendar 등을 플러그처럼 꽂는 것."

Block 0에서 도구를 선택하고, Block 1에서 프로젝트를 탐색했다. 이제 선택한 도구를 **실제로 연결**할 차례다.

### 도구를 연결하는 3가지 방법

도구를 Claude에 연결하는 방법은 3가지다. **가장 쉬운 것부터** 소개한다:

```
1순위: claude.ai Connectors (클릭 몇 번이면 끝)
──────────────────────────────────────────────
웹 브라우저에서 로그인만 하면 자동으로 연결된다.
마치 스마트폰에서 "Google로 로그인" 버튼 누르는 것과 같다.

2순위: claude mcp add 명령어 (한 줄 입력)
──────────────────────────────────────────────
터미널에 명령어 한 줄을 입력하면 연결된다.
마치 와이파이 비밀번호를 한 번 입력하면 자동 접속되는 것과 같다.

3순위: API 스크립트 (Claude가 코드를 짜줌)
──────────────────────────────────────────────
위 두 가지 방법이 안 되는 도구라면, Claude가 직접 코드를 작성해서 연결한다.
사용자가 코드를 짤 필요는 없다. Claude가 대신 한다.
```

| 비교 | Connectors | mcp add 명령어 | API 스크립트 |
|------|-----------|---------------|-------------|
| 비유 | 블루투스 자동 연결 | 와이파이 비밀번호 입력 | 맞춤형 케이블 제작 |
| 난이도 | 클릭만 (가장 쉬움) | 명령어 한 줄 (쉬움) | Claude가 코드 작성 (사용자는 보기만) |
| 대표 도구 | Slack, Notion, Linear, GitHub | Slack, Notion (HTTP MCP 서버가 있는 도구) | Gmail, Google Calendar, Fireflies |
| 장점 | 설정 파일도 필요 없음 | 빠르고 안정적 | 어떤 도구든 연결 가능 |

### 1순위: claude.ai Connectors

가장 쉬운 방법이다. 웹 브라우저에서 클릭 몇 번이면 끝난다.

```
① https://claude.ai/settings/connectors 접속
② 연결하고 싶은 서비스 선택 (Slack, Notion 등)
③ 해당 서비스에 로그인
④ "허용" 클릭
⑤ 끝! Claude Code에서 바로 사용 가능
```

연결이 완료되면 Claude Code에서 `/mcp` 명령을 입력했을 때 **"claude.ai" 섹션**에 자동으로 등록되어 있다:

```
/mcp
→ claude.ai:
→   slack: connected (tools: 11)
→   notion: connected (tools: 8)
```

> Connectors로 연결하면 API 키도 필요 없고, 설정 파일도 건드릴 필요가 없다. 가능하면 이 방법을 먼저 시도하자.

### 2순위: claude mcp add 명령어

Connectors에 원하는 서비스가 없거나, HTTP MCP 서버 주소를 알고 있다면 명령어 한 줄로 연결할 수 있다.

```
claude mcp add --transport http slack https://api.slack.com/mcp
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

이렇게 입력하면 Claude가 자동으로 설정 파일(`.mcp.json`)을 만들어준다. 직접 파일을 수정할 필요가 없다.

<details>
<summary>궁금하면 확인해보세요: .mcp.json 파일이란?</summary>

MCP 서버를 등록하는 설정 파일이다. 프로젝트 루트(최상위 폴더)에 위치한다.

```
내 프로젝트/
├── .mcp.json          <-- MCP 서버 설정 파일 (여기!)
├── .claude/
│   └── skills/
│       └── my-context-sync/
└── ...
```

`claude mcp add` 명령어를 실행하면 이 파일이 자동으로 만들어진다. 예를 들어:

```json
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://api.slack.com/mcp"
    },
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

> "어떤 서버를, 어떻게 연결할지" 적어놓는 파일이다. 하지만 대부분의 경우 Claude가 알아서 만들어주므로 직접 수정할 일은 거의 없다.

</details>

### 3순위: API 스크립트

MCP 서버도 없고 Connectors도 지원하지 않는 도구라면, Claude가 직접 코드를 작성해서 연결한다.

```
대표적인 도구:
  Gmail       → Claude가 Python 스크립트 작성
  Calendar    → Claude가 Python 스크립트 작성
  Fireflies   → Claude가 Python 스크립트 작성
```

사용자가 코드를 짤 필요는 전혀 없다. Claude가 코드를 짜고, 테스트까지 해준다.

### 환경변수 (API 키)란?

2순위, 3순위 방법을 쓸 때는 **열쇠**가 필요할 수 있다. 이것을 **API 키** 또는 **토큰**이라고 부른다.

```
예시:
  Notion   → Notion API 키
  Gmail    → Google OAuth 인증
  Linear   → Linear API 키
```

> 1순위(Connectors)를 사용하면 API 키가 필요 없다. 로그인만 하면 된다.

이 열쇠들은 보안이 중요하므로 `.env` 파일이나 시스템 환경변수에 저장한다. 코드에 직접 적지 않는다.

### 연결이 안 되면? (Plan B)

도구 연결은 인증 문제로 막히는 경우가 꽤 있다. 당황하지 말자.

```
Plan B: Fetch MCP만으로 먼저 진행하기
──────────────────────────────────────
Fetch MCP는 웹페이지의 내용을 가져오는 도구다.
인증이 필요 없는 공개 정보라면 이것만으로도 sync를 만들 수 있다.

설치:
  claude mcp add fetch -- npx -y @anthropic-ai/mcp-fetch@latest

이것만 연결해도 RSS 피드, 공개 API, 웹페이지 등에서 정보를 수집할 수 있다.
```

> 이 단계는 캠프 기간 중 천천히 해도 된다. 지금은 **연결 가능한 소스만으로 먼저 진행**하자. 완벽한 연결보다 동작하는 스킬이 더 중요하다.

## EXECUTE

### 1단계: Connectors로 연결 시도 (1순위)

먼저 가장 쉬운 방법부터 시도한다.

```json
AskUserQuestion({
  "questions": [{
    "question": "claude.ai Connectors로 먼저 연결해볼까요? 웹 브라우저에서 클릭 몇 번이면 됩니다.",
    "header": "Connectors 연결",
    "options": [
      {"label": "Connectors로 연결할게요", "description": "https://claude.ai/settings/connectors 에서 설정. 가장 쉬운 방법"},
      {"label": "이미 Connectors로 연결했어요", "description": "/mcp에서 claude.ai 섹션에 보이는 상태"},
      {"label": "다른 방법으로 할게요", "description": "명령어 입력 또는 API 스크립트 방식으로 진행"}
    ],
    "multiSelect": false
  }]
})
```

Connectors로 연결하는 경우:

```
Claude가 안내:

① 브라우저에서 https://claude.ai/settings/connectors 에 접속하세요
② 연결할 서비스(Slack, Notion 등)를 선택하고 로그인하세요
③ 완료되면 터미널에서 /mcp 를 입력해서 확인하세요

연결 확인:
  /mcp
  → claude.ai:
  →   slack: connected (tools: 11)
```

> Connectors로 연결할 수 있는 도구는 이 단계에서 모두 처리한다. 나머지만 2단계, 3단계에서 다른 방법으로 연결한다.

### 2단계: mcp add 명령어로 연결 (2순위)

Connectors에 없는 도구 중, HTTP MCP 서버가 있는 도구를 연결한다.

```
Claude가 수행:

① 도구의 MCP 서버 주소 확인
   이미 알려진 주요 서비스:
     Slack:  https://api.slack.com/mcp
     Notion: https://mcp.notion.com/mcp

② 명령어 한 줄로 등록
   claude mcp add --transport http slack https://api.slack.com/mcp

③ 연결 확인
   /mcp
   → slack: connected (tools: 11)
```

> `claude mcp add` 명령어를 실행하면 Claude가 알아서 `.mcp.json` 설정 파일을 만들어준다. 직접 파일을 편집할 필요 없다.

사용자가 직접 하는 것:
- 인증이 필요한 경우 브라우저에서 로그인
- `/mcp` 명령 입력하여 연결 상태 확인

### 3단계: API 스크립트 연결 (3순위)

MCP 서버가 없는 도구는 Claude가 직접 코드를 작성한다.

```
Claude가 수행:

① API 문서 조사
   해당 도구의 공식 API 문서를 조사한다.

② 수집 스크립트 작성
   Python 스크립트를 작성하여 스킬의 scripts/ 폴더에 저장한다.
   예: .claude/skills/my-context-sync/scripts/gmail_fetch.py

③ 스크립트 테스트 실행
   작성한 스크립트를 실행하여 데이터가 정상 수집되는지 확인한다.
```

사용자가 직접 하는 것:
- API 키 발급 (필요한 경우)
- OAuth 인증 (Google 서비스의 경우 브라우저에서 로그인)

### 4단계: 스킬 파일 업데이트

연결이 완료되면, Claude가 `.claude/skills/my-context-sync/SKILL.md`의 각 소스에 대해 "수집 방법" 부분을 실제 연결 정보로 업데이트한다.

```
변경 전 (Block 0에서 생성한 골격):
  수집 방법: (Block 2에서 설정 예정)

변경 후 (실제 연결 정보 반영):
  수집 방법: mcp__claude_ai_Slack__slack_read_channel 호출
```

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "도구를 Claude에 연결하는 가장 쉬운 방법은?",
      "header": "Quiz Block 2-1",
      "options": [
        {"label": "claude.ai Connectors", "description": "웹 브라우저에서 클릭 몇 번이면 끝"},
        {"label": ".mcp.json 파일 직접 수정", "description": "이건 Claude가 알아서 해주는 부분"},
        {"label": "API 스크립트 작성", "description": "이건 MCP가 없는 도구에 쓰는 3순위 방법"}
      ],
      "multiSelect": false
    },
    {
      "question": "MCP 서버가 없는 도구를 연결하려면 어떻게 하나요?",
      "header": "Quiz Block 2-2",
      "options": [
        {"label": "Claude가 API 스크립트를 작성해서 연결한다", "description": "MCP가 없어도 코드로 연결 가능"},
        {"label": "연결할 수 없다", "description": "API 스크립트로 어떤 도구든 연결 가능"},
        {"label": "사용자가 직접 코드를 작성한다", "description": "Claude가 대신 작성해준다"}
      ],
      "multiSelect": false
    }
  ]
})
```

정답: 둘 다 1번.
- 가장 쉬운 방법은 **claude.ai Connectors**다. 웹 브라우저에서 로그인만 하면 자동으로 연결된다. 설정 파일도, API 키도 필요 없다.
- MCP 서버가 없는 도구는 **Claude가 API 스크립트를 직접 작성**하여 연결한다. 비개발자도 걱정할 필요 없다. Claude가 코드를 짜고, 테스트까지 해준다.
