# Block 0: MCP 개념 이해

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/mcp
> 📖 MCP 소개: https://modelcontextprotocol.io/introduction
> ```

## EXPLAIN

### MCP가 뭔가?

**MCP = Model Context Protocol**

AI 앱과 외부 도구를 연결하는 **오픈 표준**이다.

| 비유 | 설명 |
|------|------|
| USB-C | USB-C가 충전기, 모니터, 외장하드를 하나의 포트로 연결하듯, MCP는 Slack, Calendar, Notion을 하나의 규격으로 Claude에 연결한다 |
| 번역기 | Claude가 Slack의 언어, Notion의 언어를 각각 배울 필요 없이, MCP라는 공용어로 소통한다 |

### MCP가 없으면 vs 있으면

```
MCP 없이                              MCP로
┌──────────┐                         ┌──────────┐
│ Claude   │                         │ Claude   │
│ Code     │                         │ Code     │
└────┬─────┘                         └────┬─────┘
     │                                    │ MCP (표준 규격)
     │ ❌ 각각 다른 방식으로               │
     │    연결해야 함                 ┌────┴────┐
     │                               │ MCP     │
┌────┼──────┐                        │ Server  │
│    │      │                        └────┬────┘
▼    ▼      ▼                             │
Slack Notion Calendar             ┌───────┼───────┐
(각각 다른 API)                    ▼       ▼       ▼
                                 Slack  Notion  Calendar
                                 (전부 같은 방식)
```

### 3가지 핵심 요소

| 요소 | 역할 | 비유 |
|------|------|------|
| **Host** | AI 앱 (Claude Code) | 내 컴퓨터 |
| **Client** | 연결을 관리하는 중간자 | USB-C 포트 |
| **Server** | 외부 도구 제공자 | USB-C 기기 (모니터, 충전기) |

```
┌─────────────────────────────────┐
│         Host (Claude Code)      │
│                                 │
│  ┌─────────┐  ┌─────────┐      │
│  │ Client 1│  │ Client 2│      │
│  └────┬────┘  └────┬────┘      │
└───────┼────────────┼────────────┘
        │            │
   ┌────▼────┐  ┌────▼────┐
   │ Slack   │  │ Notion  │
   │ Server  │  │ Server  │
   └─────────┘  └─────────┘
```

### MCP Server가 제공하는 3가지

| 종류 | 설명 | 예시 |
|------|------|------|
| **Tools** | Claude가 실행할 수 있는 기능 | "메시지 보내기", "파일 읽기" |
| **Resources** | Claude가 참조할 수 있는 데이터 | 데이터베이스 스키마, 파일 내용 |
| **Prompts** | 미리 만든 대화 템플릿 | "PR 리뷰해줘" 슬래시 명령 |

> 가장 많이 쓰는 건 **Tools**다. "Slack 메시지 읽어줘"라고 하면 Claude가 MCP를 통해 Slack Server의 Tool을 호출한다.

## EXECUTE

Claude Code에 아래를 입력해서 MCP 개념을 확인해보자:

**1. 현재 연결된 MCP 서버 확인:**

```
/mcp
```

> /mcp를 입력하면 지금 내 Claude Code에 연결된 MCP 서버 목록이 나온다.
> 아직 아무것도 없어도 괜찮다. 다음 블록에서 추가한다.

**2. MCP에 대해 Claude에게 물어보기:**

```
MCP가 뭔지, 내가 쓸 수 있는 대표적인 MCP 서버 5개를 알려줘
```

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "MCP를 USB-C에 비유했습니다. MCP의 핵심 역할은?",
    "header": "Quiz 0",
    "options": [
      {"label": "AI와 외부 도구를 표준 규격으로 연결", "description": "USB-C처럼 하나의 표준으로 다양한 도구를 꽂는 것"},
      {"label": "Claude의 성능을 높이는 업그레이드", "description": "MCP는 성능이 아니라 연결의 문제를 해결"},
      {"label": "코드를 자동으로 작성해주는 도구", "description": "MCP는 외부 서비스 연결 프로토콜"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
피드백: "맞습니다! MCP = 표준 연결 규격. USB-C가 기기를 하나로 통일했듯, MCP는 AI와 외부 도구 연결을 하나로 통일합니다."
