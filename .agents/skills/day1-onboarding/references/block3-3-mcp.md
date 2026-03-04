# Block 3-3: MCP

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/mcp
> ```

## EXPLAIN

| 항목 | 내용 |
|------|------|
| 근본 원리 | **툴 콜링(Tool Calling)** — AI가 텍스트만 생성하는 게 아니라, "이 함수를 이 파라미터로 호출해"라고 구조화된 요청을 보낸다. MCP는 이 툴 콜링을 외부 서비스까지 확장하는 오픈 표준 |
| 비유 | 외부 도구 플러그 — Slack, Calendar, Notion 등을 Claude에 연결하는 오픈 표준 프로토콜 |
| 예시 | "Slack 메시지 읽어줘", "캘린더 일정 확인해줘" |

```
Claude ──── "Slack에서 메시지 읽어줘"
  │
  ▼ 툴 콜링
┌──────────┐    MCP 프로토콜    ┌──────────┐
│ Claude   │ ◀═══════════════▶ │ Slack    │
│ Code     │    표준 규격       │ Server   │
└──────────┘                   └──────────┘
  내 컴퓨터                      외부 서비스
```

## EXECUTE

Claude에게 MCP에 대해 물어보라고 안내한다:

```
MCP가 뭔지 쉽게 설명해줘. 내가 쓸 수 있는 MCP 서버 예시 3개도 알려줘
```

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "MCP를 한 마디로 말하면?",
    "header": "Quiz 3-3",
    "options": [
      {"label": "Claude와 외부 도구를 연결하는 표준 프로토콜", "description": "Slack, Calendar 등을 플러그처럼 꽂는 것"},
      {"label": "Claude의 내장 기능", "description": "MCP는 외부 연결이지 내장이 아님"},
      {"label": "프로그래밍 언어", "description": "도구 연결 프로토콜임"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
