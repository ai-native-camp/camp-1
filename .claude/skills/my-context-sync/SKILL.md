---
name: my-context-sync
description: 나의 컨텍스트 싱크. Slack, Notion, Granola에서 정보를 수집하고 하나의 문서로 정리한다. "싱크", "sync", "정보 수집" 요청에 사용.
triggers:
  - "싱크"
  - "sync"
  - "정보 수집"
  - "컨텍스트 싱크"
---

# My Context Sync

흩어진 정보를 한곳에 모아 정리하는 스킬.

Slack, Notion, Granola에서 최근 정보를 수집하고,
하나의 마크다운 문서로 통합한다.

## 소스 정의

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

### 소스 2: Notion

| 항목 | 값 |
|------|-----|
| MCP 도구 | claude.ai Notion 커넥터 (`mcp__claude_ai_Notion__*`) |
| 수집 범위 | 지정된 데이터베이스 |

<!-- claude.ai/settings/connectors 에서 Notion을 연결하면 자동으로 사용 가능 -->
```yaml
databases:
  - name: "업무 태스크"
    id: "your-database-id"
  - name: "프로젝트 현황"
    id: "your-database-id"
```

수집 방법:
```
claude.ai Notion 커넥터의 도구를 사용하여 데이터베이스를 조회한다.

호출 예시:
  mcp__claude_ai_Notion__notion-search(query="태스크")
  mcp__claude_ai_Notion__notion-fetch(resource_uri="notion://page/{page-id}")
```

추출할 정보:
- 진행 중인 태스크
- 기한이 임박한 항목
- 최근 업데이트된 페이지

### 소스 3: Granola

| 항목 | 값 |
|------|-----|
| MCP 도구 | Granola MCP 서버 (`https://mcp.granola.ai/mcp`) |
| 수집 범위 | 최근 7일 미팅 노트 |

<!-- 연결 방법 2가지:
  1. claude.ai/settings/connectors 에서 Granola 검색 후 연결 (가장 쉬움)
  2. claude mcp add --transport http granola https://mcp.granola.ai/mcp
-->

수집 방법:
```
Granola MCP 서버의 도구를 사용하여 미팅 노트를 검색/조회한다.

호출 예시:
  Granola MCP로 최근 7일간의 미팅 노트를 검색하라
```

추출할 정보:
- 최근 미팅 제목과 참석자
- 주요 논의 사항
- 액션 아이템

## 실행 흐름

이 스킬이 트리거되면 아래 순서로 실행한다.

### 1단계: 병렬 수집

3개 소스를 **동시에** 수집한다. 서로 의존성이 없으므로 병렬 실행이 가능하다.

```
수집 시작
  ├── [소스 1] Slack 채널 메시지 수집      ─┐
  ├── [소스 2] Notion 태스크 수집           ├── 병렬 실행
  └── [소스 3] Granola 미팅록 수집       ─┘
수집 완료
```

각 소스 수집은 subagent(Task 도구)로 실행한다:

```
Task(description="Slack 수집", prompt="general, project-updates, random 채널에서 최근 7일 메시지를 수집하라")
Task(description="Notion 수집", prompt="업무 태스크 DB에서 진행 중인 항목을 수집하라")
Task(description="Granola 수집", prompt="fireflies_fetch.py를 실행하여 최근 7일 미팅록을 수집하라")
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

### 4단계: 리포트

실행 결과를 사용자에게 보고한다.

```
싱크 완료!

수집 결과:
  Slack: 3개 채널, 47개 메시지
  Notion: 15개 태스크
  Granola: 3개 미팅록

하이라이트 3건:
  1. [Slack] #project-updates: 배포 일정 확정 (2/20)
  2. [Notion] 랜딩페이지 디자인 기한 임박 (2/18)
  3. [Granola] 파트너 미팅 액션아이템 3건

액션 아이템 4건:
  - [ ] 파트너 미팅 후속 조치
  - [ ] 랜딩페이지 디자인 마감
  - [ ] Slack #general 공지 확인
  - [ ] Notion 기한 초과 태스크 2건 처리

파일 저장: sync/2026-02-15-context-sync.md
```

## 출력 포맷

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
- **[Notion]** 랜딩페이지 디자인 기한 임박
- **[Granola]** 파트너 미팅 액션아이템 3건

## Slack

### #general
- 주간 회의 시간 변경 공지 (화 10시 → 수 11시)

### #project-updates
- v2.0 배포일 2/20 확정
- QA 테스트 완료

## Notion

### 진행 중 태스크
- [ ] 랜딩페이지 디자인 (기한: 2/18)
- [ ] API 문서 작성 (기한: 2/20)
- [x] 사용자 테스트 완료

## Granola

### 최근 미팅록
- **파트너 미팅** (2/14, 참석: 3명)
  - 계약 조건 합의
  - 액션: 계약서 초안 작성 (담당: 구봉)
- **팀 스탠드업** (2/15, 참석: 5명)
  - 스프린트 리뷰 완료
  - 액션: 배포 전 QA 체크리스트 작성

## 액션 아이템

- [ ] 파트너 미팅 후속 조치 (기한: 2/18)
- [ ] 랜딩페이지 디자인 마감 (2/18까지)
- [ ] 기한 초과 태스크 처리
- [ ] Slack 공지 확인 후 일정 반영
```

## 커스터마이징 가이드

### 소스 추가하기

새로운 소스를 추가하려면 "소스 정의" 섹션에 같은 형식으로 추가한다:

```markdown
### 소스 4: Linear

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
