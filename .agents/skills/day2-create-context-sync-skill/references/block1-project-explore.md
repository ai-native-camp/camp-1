# Block 1: 프로젝트 탐색

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/sub-agents
> ```

## EXPLAIN

### Day 1 복습: Subagent

Day 1 Block 3-4에서 **Subagent**를 배웠다. "부하 직원처럼 독립된 공간에서 특정 작업을 전담 처리하는 것."

오늘은 그 Subagent 중에서도 **Explore 에이전트**를 사용한다.

### Explore 에이전트란?

Explore 에이전트는 프로젝트의 폴더와 파일을 빠르게 탐색하는 **전문 subagent**다. 일반 subagent와의 차이는:

| 구분 | 일반 Subagent | Explore 에이전트 |
|------|--------------|-----------------|
| 역할 | 다양한 작업 수행 | 파일/폴더 탐색 전문 |
| 권한 | 파일 읽기 + 쓰기 | **읽기 전용** (안전함) |
| 용도 | 분석, 작성, 실행 등 | 프로젝트 구조 파악 |

```
Claude ── "이 프로젝트 구조 파악해줘"
  │
  ▼ Task 도구 호출 (subagent_type: Explore)
┌─ Explore 에이전트 ──────────────┐
│ 읽기 전용으로 폴더/파일 탐색     │
│                                │
│ 결과:                           │
│  📁 프로젝트 루트               │
│  ├── .claude/skills/            │
│  ├── .mcp.json                 │
│  ├── .env                      │
│  └── src/                      │
└────────────────────────────────┘
  │
  ▼ 결과 전달
Claude ── "이런 구조입니다. 스킬을 수정하겠습니다"
```

### 왜 프로젝트를 탐색하는가?

Block 0에서 스킬의 골격을 만들었다. 하지만 스킬이 잘 동작하려면 프로젝트의 **현재 상태**를 알아야 한다:

- `.claude/skills/my-context-sync/` 가 제대로 생성되었는지
- `.mcp.json` 이 이미 있는지 (있으면 기존 MCP 설정을 활용할 수 있다)
- `.env` 파일이 있는지 (환경변수가 이미 설정되어 있을 수 있다)
- 다른 스킬이 이미 존재하는지 (참고할 수 있다)

> 요리를 시작하기 전에 냉장고를 여는 것과 같다. 뭐가 있는지 먼저 파악해야 빠진 재료를 알 수 있다.

## EXECUTE

### 1단계: Explore 에이전트로 프로젝트 탐색

Claude가 Explore 에이전트를 호출하여 프로젝트 구조를 파악한다.

```
Claude가 수행:
  Task(
    description="프로젝트 구조 탐색",
    prompt="프로젝트 루트에서 다음을 확인하라:
      1. 전체 폴더 구조 (최대 2단계)
      2. .claude/ 디렉토리 내용
      3. .mcp.json 존재 여부와 내용
      4. .env 파일 존재 여부
      5. 기존 스킬이 있다면 목록",
    subagent_type="Explore"
  )
```

> 사용자는 결과를 보기만 하면 된다. Claude가 알아서 탐색하고 정리해준다.

### 2단계: 탐색 결과를 바탕으로 스킬 조정

Explore 결과를 보고, Block 0에서 생성한 스킬의 내용을 조정한다:

| 발견 사항 | 조정 내용 |
|-----------|----------|
| `.mcp.json`에 Slack MCP가 이미 설정됨 | 스킬의 Slack 소스에 기존 설정 반영 |
| `.env`에 API 키가 이미 있음 | Block 2에서 해당 키 재사용 |
| 기존 sync 스킬이 있음 | 중복 방지, 기존 스킬 참고 |
| 특정 폴더 구조 발견 | 스킬의 description을 프로젝트에 맞게 수정 |

Claude가 스킬의 frontmatter(스킬 설명 부분)와 수집 범위를 프로젝트 환경에 맞게 자동 수정한다.

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "Explore 에이전트는 어떤 종류의 subagent인가요?",
      "header": "Quiz Block 1-1",
      "options": [
        {"label": "읽기 전용으로 파일/폴더를 탐색하는 전문 subagent", "description": "파일을 수정하지 않고 구조만 파악"},
        {"label": "파일을 자동으로 수정하는 subagent", "description": "Explore는 읽기 전용"},
        {"label": "외부 서비스에 접속하는 subagent", "description": "외부 연결은 MCP의 역할"}
      ],
      "multiSelect": false
    },
    {
      "question": "스킬을 만든 후 프로젝트를 탐색하는 이유는?",
      "header": "Quiz Block 1-2",
      "options": [
        {"label": "기존 설정(.mcp.json, .env 등)을 파악하여 스킬을 프로젝트에 맞게 조정하려고", "description": "냉장고 열어서 재료 확인하는 것과 같다"},
        {"label": "예쁜 폴더 구조를 보려고", "description": "탐색의 진짜 목적은 스킬 조정"},
        {"label": "Claude Code가 시키니까", "description": "목적이 있어서 하는 것"}
      ],
      "multiSelect": false
    }
  ]
})
```

정답: 둘 다 1번.
- Explore 에이전트는 **읽기 전용** 전문 subagent다. 파일을 수정하지 않아 안전하게 프로젝트 구조를 파악할 수 있다.
- 프로젝트 탐색은 **기존 설정을 활용하고 스킬을 환경에 맞게 조정**하기 위함이다. 요리 전에 냉장고를 확인하는 것과 같다.
