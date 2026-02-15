# Block 2: 도구 연결

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://modelcontextprotocol.io/
> 📖 공식 문서: https://docs.claude.com/en/docs/claude-code/mcp
> ```

## EXPLAIN

### Day 1 복습: MCP

Day 1 Block 3-3에서 **MCP**를 배웠다. "Claude와 외부 도구를 연결하는 표준 프로토콜. Slack, Calendar 등을 플러그처럼 꽂는 것."

Block 0에서 도구를 선택하고, Block 1에서 프로젝트를 탐색했다. 이제 선택한 도구를 **실제로 연결**할 차례다.

### 도구를 연결하는 2가지 방법

도구를 Claude에 연결하는 방법은 크게 2가지다:

```
방법 1: MCP 서버 (설정만 하면 됨)
──────────────────────────────
누군가 이미 만들어놓은 "연결 통로"를 가져다 쓴다.
설정 파일(.mcp.json)에 한 줄 추가하면 끝.

방법 2: API 스크립트 (Claude가 코드를 짜줌)
──────────────────────────────────────
MCP 서버가 없는 도구라면, Claude가 직접 코드를 작성해서 연결한다.
사용자가 코드를 짤 필요는 없다. Claude가 대신 한다.
```

| 비교 | MCP 서버 | API 스크립트 |
|------|---------|-------------|
| 비유 | 기성품 어댑터 꽂기 | 맞춤형 케이블 제작 |
| 난이도 | 설정 파일 수정 (쉬움) | Claude가 코드 작성 (사용자는 보기만) |
| 대표 도구 | Slack, Notion, GitHub | Gmail, Google Calendar, Fireflies |
| 장점 | 빠르고 안정적 | 어떤 도구든 연결 가능 |

### .mcp.json 파일이란?

MCP 서버를 등록하는 설정 파일이다. 프로젝트 루트(최상위 폴더)에 위치한다.

```
내 프로젝트/
├── .mcp.json          <-- MCP 서버 설정 파일 (여기!)
├── .claude/
│   └── skills/
│       └── my-context-sync/
└── ...
```

안에는 이런 내용이 들어간다:

```json
{
  "slack": {
    "type": "sse",
    "url": "https://mcp.slack.com/sse"
  },
  "notion": {
    "command": "npx",
    "args": ["-y", "@notionhq/notion-mcp-server"],
    "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
  }
}
```

> "어떤 서버를, 어떻게 실행하고, 어떤 인증 정보를 쓸지" 적어놓는 파일이다.

### 환경변수 (API 키)란?

외부 서비스에 접속하려면 **열쇠**가 필요하다. 이것을 **API 키** 또는 **토큰**이라고 부른다.

```
예시:
  Slack    → Slack 앱 토큰
  Notion   → Notion API 키
  Gmail    → Google OAuth 인증
  Linear   → Linear API 키
```

이 열쇠들은 보안이 중요하므로 `.env` 파일이나 시스템 환경변수에 저장한다. 코드에 직접 적지 않는다.

### MCP 서버 찾는 방법

이미 누군가 만들어놓은 MCP 서버가 많다. `scripts/mcp_servers.py` 스크립트를 사용하면 GitHub에서 원하는 도구의 MCP 서버를 검색할 수 있다.

```
Claude가 수행:
  "Slack MCP 서버 찾아줘"
  → mcp_servers.py로 검색
  → 결과: @anthropic/slack-mcp, slack-mcp-server 등 후보 목록
  → 가장 적합한 서버 선택
```

## EXECUTE

### 1단계: 연결 방식 선택

Block 0에서 선택한 각 도구에 대해, MCP 서버와 API 스크립트 중 연결 방식을 선택한다.

```json
AskUserQuestion({
  "questions": [{
    "question": "각 도구를 어떤 방식으로 연결할까요? Claude가 추천하는 방식을 기본으로 선택했습니다. 바꾸고 싶은 것만 변경하세요.",
    "header": "연결 방식 선택",
    "options": [
      {"label": "Claude 추천대로 진행", "description": "각 도구에 최적의 방식을 자동 선택"},
      {"label": "직접 선택하겠다", "description": "각 도구별로 MCP/API를 하나씩 고르기"}
    ],
    "multiSelect": false
  }]
})
```

> "Claude 추천대로 진행"을 선택하면, Claude가 각 도구별 최적 방식을 자동으로 결정한다.
> 도구별 추천 기준: MCP 서버가 존재하고 안정적이면 MCP, 없으면 API 스크립트.

### 2단계: MCP 서버 연결 (MCP 선택 시)

Claude가 순서대로 수행한다. 사용자는 결과를 확인만 하면 된다.

```
Claude가 수행:

① MCP 서버 검색
   scripts/mcp_servers.py로 GitHub에서 적합한 MCP 서버를 검색한다.
   검색 결과 중 가장 적합한 서버를 선택하여 보여준다.

② .mcp.json에 서버 등록
   프로젝트의 .mcp.json 파일에 선택된 MCP 서버 설정을 추가한다.
   이미 .mcp.json이 있으면 기존 내용에 추가, 없으면 새로 생성한다.

③ 환경변수 안내
   API 키가 필요한 경우 발급 방법을 안내한다.
   예: "Notion API 키는 https://www.notion.so/my-integrations 에서 발급할 수 있습니다"

④ 연결 확인
   /mcp 명령으로 서버가 정상 연결되었는지 확인한다.
```

사용자가 직접 하는 것:
- API 키 발급 (외부 서비스 웹사이트에서)
- `/mcp` 명령 입력하여 연결 상태 확인

```
/mcp
→ slack: connected (tools: 11)
→ notion: connected (tools: 8)
```

### 3단계: API 스크립트 연결 (API 선택 시)

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
      "question": "MCP 서버 설정이 저장되는 파일의 이름은?",
      "header": "Quiz Block 2-1",
      "options": [
        {"label": ".mcp.json", "description": "프로젝트 루트에 위치하는 MCP 설정 파일"},
        {"label": "SKILL.md", "description": "이건 스킬 정의 파일"},
        {"label": "CLAUDE.md", "description": "이건 프로젝트 전체 지시사항 파일"}
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
- MCP 서버 설정은 **.mcp.json** 파일에 저장된다. 프로젝트 루트에 위치하며, 어떤 서버를 어떻게 연결할지 적어놓는 파일이다.
- MCP 서버가 없는 도구는 **Claude가 API 스크립트를 직접 작성**하여 연결한다. 비개발자도 걱정할 필요 없다. Claude가 코드를 짜고, 테스트까지 해준다.
