---
name: my-context-sync
description: 나의 컨텍스트 싱크. 여러 소스에서 정보를 수집하고 하나의 문서로 정리한다. "싱크", "sync", "정보 수집" 요청에 사용.
triggers:
  - "싱크"
  - "sync"
  - "정보 수집"
  - "컨텍스트 싱크"
---

# My Context Sync

흩어진 정보를 한곳에 모아 정리하는 스킬.

Slack, Gmail, Google Calendar, Notion에서 최근 정보를 수집하고,
하나의 마크다운 문서로 통합한다.

## 소스 정의

<!-- ============================================ -->
<!-- 아래 4개 소스를 자신의 환경에 맞게 수정하세요 -->
<!-- 사용하지 않는 소스는 통째로 삭제해도 됩니다   -->
<!-- 새로운 소스를 추가하려면 같은 형식으로 복사하세요 -->
<!-- ============================================ -->

### 소스 1: Slack

| 항목 | 값 |
|------|-----|
| MCP 도구 | `mcp__claude_ai_Slack__slack_read_channel` |
| 수집 범위 | 최근 7일 |

수집할 채널 목록:

<!-- 자신이 주로 사용하는 채널명으로 바꾸세요 -->
```yaml
channels:
  - name: "general"          # 전체 공지
  - name: "project-updates"  # 프로젝트 소식
  - name: "random"           # 자유 채널
```

수집 방법:
```
각 채널에 대해 mcp__claude_ai_Slack__slack_read_channel 호출.
채널명과 메시지 개수(limit)를 전달한다.

예시:
  mcp__claude_ai_Slack__slack_read_channel(channel="general", limit=50)
```

추출할 정보:
- 중요 공지사항
- 의사결정 사항 ("확정", "결정", "합의" 키워드)
- 나에게 멘션된 메시지
- 답장이 필요한 질문

### 소스 2: Gmail

| 항목 | 값 |
|------|-----|
| 실행 방법 | Python 스크립트 (Gmail API) |
| 수집 범위 | 최근 7일, 받은편지함 |

<!-- Gmail은 MCP가 아닌 스크립트로 수집합니다 -->
<!-- 이 스크립트는 Block 2에서 Claude가 자동으로 작성해줍니다 -->
<!-- 스크립트 경로를 자신의 환경에 맞게 수정하세요 -->

수집 방법:
```bash
uv run python .claude/skills/my-context-sync/scripts/gmail_fetch.py --days 7
```

추출할 정보:
- 안 읽은 이메일 수
- 중요 발신자 이메일 요약
- 회신이 필요한 이메일
- 일정 초대 (캘린더 연동)

### 소스 3: Google Calendar

| 항목 | 값 |
|------|-----|
| 실행 방법 | Python 스크립트 (Google Calendar API) |
| 수집 범위 | 오늘 ~ 7일 후 |

<!-- 이 스크립트는 Block 2에서 Claude가 자동으로 작성해줍니다 -->
<!-- 캘린더 스크립트 경로를 수정하세요 -->

수집 방법:
```bash
uv run python .claude/skills/my-context-sync/scripts/calendar_fetch.py --days 7
```

추출할 정보:
- 오늘의 일정
- 이번 주 주요 미팅
- 준비가 필요한 미팅 (발표, 외부 미팅 등)
- 일정 충돌 여부

### 소스 4: Notion

| 항목 | 값 |
|------|-----|
| MCP 도구 | Notion MCP 서버 (`@notionhq/notion-mcp-server`) |
| 수집 범위 | 지정된 데이터베이스 |

<!-- Notion MCP 서버가 .mcp.json에 등록되어 있어야 합니다 -->
<!-- Block 2에서 Claude가 설정을 도와줍니다 -->
```yaml
databases:
  - name: "업무 태스크"
    id: "your-database-id"
  - name: "프로젝트 현황"
    id: "your-database-id"
```

수집 방법:
```
Notion MCP 서버의 도구를 사용하여 데이터베이스를 조회한다.

.mcp.json 설정 예시:
{
  "notion": {
    "command": "npx",
    "args": ["-y", "@notionhq/notion-mcp-server"],
    "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
  }
}

호출 예시:
  mcp__notion__query_database(database_id="your-database-id")
```

<!-- ⚠️ WebFetch는 인증이 필요한 Notion 페이지에서 작동하지 않습니다 -->
<!-- 반드시 Notion MCP 서버 또는 API 스크립트를 사용하세요 -->

추출할 정보:
- 진행 중인 태스크
- 기한이 임박한 항목
- 최근 업데이트된 페이지

## 실행 흐름

이 스킬이 트리거되면 아래 순서로 실행한다.

### 1단계: 병렬 수집

4개 소스를 **동시에** 수집한다. 서로 의존성이 없으므로 병렬 실행이 가능하다.

<!-- 소스가 2개이면 2줄, 5개이면 5줄로 조정하세요 -->
<!-- 소스 수에 맞춰 Task 호출도 같은 수만큼 추가/제거하세요 -->

```
수집 시작
  ├── [소스 1] Slack 채널 메시지 수집      ─┐
  ├── [소스 2] Gmail 이메일 수집            ├── 병렬 실행
  ├── [소스 3] Google Calendar 일정 수집    │
  └── [소스 4] Notion 태스크 수집           ─┘
수집 완료
```

각 소스 수집은 subagent(Task 도구)로 실행한다:

```
Task(description="Slack 수집", prompt="general, project-updates, random 채널에서 최근 7일 메시지를 수집하라")
Task(description="Gmail 수집", prompt="gmail_fetch.py를 실행하여 최근 7일 이메일을 수집하라")
Task(description="Calendar 수집", prompt="calendar_fetch.py를 실행하여 7일간 일정을 수집하라")
Task(description="Notion 수집", prompt="업무 태스크 DB에서 진행 중인 항목을 수집하라")
```

### 2단계: 결과 통합

수집된 정보를 하나의 문서로 합친다.

통합 규칙:
- 소스별 섹션으로 구분
- 각 섹션에서 "하이라이트" (중요 항목 3개 이내)를 선별
- 액션 아이템을 문서 하단에 모아서 정리
- 수집 실패한 소스는 "수집 실패" 표시와 함께 사유 기록

### 3단계: 문서 저장

결과 파일을 저장한다.

```
저장 위치: sync/YYYY-MM-DD-context-sync.md
```

<!-- 저장 위치를 원하는 경로로 바꾸세요 -->

### 4단계: 리포트

실행 결과를 사용자에게 보고한다.

```
싱크 완료!

수집 결과:
  Slack: 3개 채널, 47개 메시지
  Gmail: 12개 이메일 (안 읽음 5개)
  Calendar: 8개 일정
  Notion: 15개 태스크

하이라이트 3건:
  1. [Slack] #project-updates: 배포 일정 확정 (2/20)
  2. [Gmail] 파트너사 계약서 회신 필요 (기한: 2/18)
  3. [Calendar] 내일 10시 팀 미팅 (발표 자료 준비 필요)

액션 아이템 4건:
  - [ ] 파트너사 계약서 회신
  - [ ] 팀 미팅 발표 자료 준비
  - [ ] Slack #general 공지 확인
  - [ ] Notion 기한 초과 태스크 2건 처리

파일 저장: sync/2026-02-15-context-sync.md
```

## 출력 포맷

<!-- 출력 형식을 선택하세요. 여러 개를 동시에 사용할 수 있습니다 -->
출력 옵션:
1. **Markdown 파일** (기본) -- `sync/YYYY-MM-DD-context-sync.md`에 저장
2. **Slack 메시지** -- 지정 채널에 요약 발송 (Slack MCP 필요)
3. **Notion 페이지** -- 지정 DB에 기록 (Notion MCP 필요)

저장되는 마크다운 파일의 구조:

```markdown
# Context Sync - 2026-02-15

> 자동 수집 시각: 09:00

## 하이라이트

- **[Slack]** 배포 일정 2/20로 확정
- **[Gmail]** 파트너사 계약서 회신 필요 (기한 2/18)
- **[Calendar]** 내일 팀 미팅 - 발표 자료 준비

## Slack

### #general
- 주간 회의 시간 변경 공지 (화 10시 → 수 11시)

### #project-updates
- v2.0 배포일 2/20 확정
- QA 테스트 완료

## Gmail

| 발신자 | 제목 | 상태 |
|--------|------|------|
| 파트너사 | 계약서 검토 요청 | 회신 필요 |
| 팀장 | 주간 보고 | 읽음 |

## Google Calendar

### 오늘 (2/15)
- 09:00 모닝 스탠드업 (30분)
- 14:00 파트너 미팅 (1시간)

### 이번 주
- 2/17 (월) 10:00 팀 미팅
- 2/20 (수) 배포일

## Notion

### 진행 중 태스크
- [ ] 랜딩페이지 디자인 (기한: 2/18)
- [ ] API 문서 작성 (기한: 2/20)
- [x] 사용자 테스트 완료

## 액션 아이템

- [ ] 파트너사 계약서 회신 (기한: 2/18)
- [ ] 팀 미팅 발표 자료 준비 (2/17까지)
- [ ] 기한 초과 태스크 처리
- [ ] Slack 공지 확인 후 일정 반영
```

## 커스터마이징 가이드

### 소스 추가하기

새로운 소스를 추가하려면 "소스 정의" 섹션에 같은 형식으로 추가한다:

```markdown
### 소스 5: Linear

| 항목 | 값 |
|------|-----|
| MCP 도구 | `mcp__claude_ai_Linear__list_issues` |
| 수집 범위 | 나에게 할당된 이슈 |

수집 방법:
  mcp__claude_ai_Linear__list_issues 호출.

추출할 정보:
- 진행 중인 이슈
- 이번 주 마감 이슈
```

### API/스크립트 방식으로 소스 추가하기

MCP 서버가 없는 도구는 스크립트를 작성하여 연결한다.
Block 2에서 Claude가 스크립트를 자동으로 작성해준다.

예시: Fireflies 미팅록 추가

```markdown
### 소스 5: Fireflies

| 항목 | 값 |
|------|-----|
| 실행 방법 | Python 스크립트 (Fireflies GraphQL API) |
| 수집 범위 | 최근 7일 미팅록 |

수집 방법:
uv run python .claude/skills/my-context-sync/scripts/fireflies_fetch.py --days 7

추출할 정보:
- 최근 미팅 제목과 참석자
- 주요 논의 사항
- 액션 아이템
```

### 소스 제거하기

사용하지 않는 소스는 해당 "소스 N" 섹션 전체를 삭제한다.
실행 흐름의 병렬 수집 부분에서도 해당 줄을 제거한다.

### 수집 주기 변경하기

기본은 수동 실행이다. 자동 실행을 원하면 CLAUDE.md에 스케줄을 추가한다:

```markdown
## 스케줄
- context-sync: 매일 09:00 실행
```

### 출력 위치 변경하기

"3단계: 문서 저장"의 경로를 원하는 위치로 수정한다.
예: `reports/`, `docs/daily/` 등.
