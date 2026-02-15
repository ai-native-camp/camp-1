# Block 5: Output Format 선택

## EXPLAIN

### 수집한 정보, 어디에 내보낼 것인가?

Block 3~4에서 여러 소스의 정보를 성공적으로 수집했다. 이제 마지막 질문이 남았다:

> "이 정보를 **어디에**, **어떤 형태로** 저장하고 공유할 것인가?"

3가지 출력 옵션이 있다.

### 옵션 1: Markdown 파일 (기본)

```
수집된 정보 → 프로젝트 폴더에 .md 파일로 저장
```

- 가장 간단하고 안정적인 방법
- 외부 서비스 연결 없이 바로 사용 가능
- 파일이 프로젝트 안에 남으므로 나중에 다시 찾기 쉬움
- 예: `sync/2026-02-15-context-sync.md`

### 옵션 2: Slack 메시지

```
수집된 정보 → Slack 채널에 요약 메시지로 전송
```

- 팀원들과 바로 공유할 때 좋음
- 매일 아침 자동으로 보내면 "모닝 브리핑" 역할
- Slack MCP가 연결되어 있어야 사용 가능 (Block 2에서 연결했다면 바로 사용)

### 옵션 3: Notion 페이지

```
수집된 정보 → Notion 데이터베이스에 새 페이지로 생성
```

- 정보가 Notion에 쌓이므로 나중에 검색과 정리가 편함
- 날짜별로 자동 축적되어 기록 관리에 좋음
- Notion MCP가 연결되어 있어야 사용 가능 (Block 2에서 연결했다면 바로 사용)

### 여러 출력을 동시에 쓸 수도 있다

```
수집된 정보
  ├── Markdown 파일로 저장 (기록용)     ← 항상 포함
  ├── Slack 채널로 전송 (공유용)        ← 선택
  └── Notion 페이지 생성 (축적용)       ← 선택
```

Markdown은 기본으로 항상 포함하고, Slack이나 Notion을 추가하면 더 편리해진다. Block 2에서 연결한 도구 중 출력용으로 쓸 수 있는 것이 있다면 함께 활용하는 것을 추천한다.

## EXECUTE

AskUserQuestion으로 출력 형식을 선택받는다:

```json
AskUserQuestion({
  "questions": [{
    "question": "수집 결과를 어떤 형식으로 출력할까요?\n\nMarkdown 파일은 기본으로 항상 포함됩니다.\n추가로 Slack이나 Notion 출력을 선택할 수 있습니다.",
    "header": "출력 형식 선택",
    "options": [
      {"label": "Markdown 파일만", "description": "프로젝트 폴더에 .md 파일로 저장 (가장 간단)"},
      {"label": "Markdown + Slack 전송", "description": "파일 저장 + 특정 Slack 채널에 요약 발송"},
      {"label": "Markdown + Notion 페이지", "description": "파일 저장 + Notion DB에 페이지 생성"},
      {"label": "Markdown + Slack + Notion", "description": "세 곳 모두에 출력"}
    ],
    "multiSelect": false
  }]
})
```

선택 결과에 따라 사용자의 스킬 파일(`.claude/skills/my-context-sync/SKILL.md`)을 수정한다:

**공통 (Markdown 파일)**:
- "출력 포맷" 섹션에 저장 경로를 확인/수정한다
- 기본 경로: `sync/YYYY-MM-DD-context-sync.md`
- 사용자가 원하는 경로가 있으면 변경한다

**Slack을 선택한 경우**:
- Slack MCP가 연결되어 있는지 확인한다
- 연결되어 있지 않으면 Block 2 방식으로 연결을 안내한다
- 전송할 채널명을 묻고 스킬에 반영한다
- "출력 포맷" 섹션에 Slack 전송 단계를 추가한다:
  ```
  mcp__claude_ai_Slack__slack_send_message(channel="채널명", content="요약 내용")
  ```

**Notion을 선택한 경우**:
- Notion MCP가 연결되어 있는지 확인한다
- 연결되어 있지 않으면 Block 2 방식으로 연결을 안내한다
- 데이터베이스 ID를 묻고 스킬에 반영한다
- "출력 포맷" 섹션에 Notion 페이지 생성 단계를 추가한다

수정이 완료되면 변경된 부분만 간략히 보여주고 Stop한다.

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "3가지 출력 형식 중 가장 간단하고, 외부 서비스 연결 없이 바로 쓸 수 있는 것은?",
    "header": "Quiz 5-1",
    "options": [
      {"label": "Markdown 파일", "description": "프로젝트 폴더에 .md 파일로 저장"},
      {"label": "Slack 메시지", "description": "Slack 채널에 전송"},
      {"label": "Notion 페이지", "description": "Notion DB에 기록"}
    ],
    "multiSelect": false
  }]
})
```

정답: Markdown 파일
피드백: "맞습니다! Markdown 파일은 별도 설정 없이 바로 사용할 수 있어서 가장 간단합니다. 그래서 기본 출력으로 항상 포함됩니다."

```json
AskUserQuestion({
  "questions": [{
    "question": "Slack으로 결과를 보내려면 뭐가 필요할까요?",
    "header": "Quiz 5-2",
    "options": [
      {"label": "Slack MCP 연결", "description": "Block 2에서 배운 MCP 연결"},
      {"label": "Slack 앱 설치", "description": "스마트폰에 Slack 앱 설치"},
      {"label": "별도 준비 없이 가능", "description": "Claude가 알아서 전송"}
    ],
    "multiSelect": false
  }]
})
```

정답: Slack MCP 연결
피드백: "정확합니다! Claude가 Slack에 메시지를 보내려면 Slack MCP라는 통로가 연결되어 있어야 합니다. Block 2에서 배운 것이 여기서 이렇게 쓰입니다."
