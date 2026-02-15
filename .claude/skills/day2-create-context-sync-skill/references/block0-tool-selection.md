# Block 0: 도구 선택 + 스킬 생성

## EXPLAIN

### Context Sync란?

매일 아침 출근하면 이런 일을 한다:

1. Slack 열어서 밤새 온 메시지 확인
2. Gmail 열어서 안 읽은 이메일 확인
3. 캘린더 열어서 오늘 일정 확인
4. Notion 열어서 내 태스크 확인
5. Linear 열어서 이슈 확인

5개 앱을 돌아다니며 30분. 매일 반복. 이것이 **컨텍스트 스위칭**이다.

**Context Sync**는 이 과정을 자동화한다. Claude Code가 여러 도구에서 정보를 모아서 하나의 문서로 정리해준다. 한 번 만들어두면 "싱크해줘" 한 마디로 끝난다.

```
평소                              Context Sync 이후
─────────────                    ──────────────────
Slack 열기                        "싱크해줘" (한 마디)
Gmail 열기                              │
Calendar 열기        ──▶          Claude가 알아서 수집
Notion 열기                             │
Linear 열기                       하나의 문서로 정리!
= 30분 소요                       = 1분 소요
```

### Day 1에서 배운 것과의 연결

Day 1 Block 3-2에서 **스킬(Skill)**을 배웠다. "반복하는 업무를 한 번 저장하면 다음부터 한 줄로 실행하는 업무 레시피." 오늘은 이 스킬을 **직접 만든다.** 그것도 여러 도구를 연결하는 실전 스킬을.

### 연결할 수 있는 도구 목록

| 도구 | 어디서 쓰나 | 모아올 정보 |
|------|------------|------------|
| **Slack** | 팀 채팅 | 채널 메시지, 멘션, 공지 |
| **Gmail** | 이메일 | 안 읽은 메일, 회신 필요한 메일 |
| **Google Calendar** | 일정 관리 | 오늘/이번 주 미팅, 일정 충돌 |
| **Notion** | 문서/태스크 | 진행 중 태스크, 기한 임박 항목 |
| **Linear** | 이슈 트래커 | 내 이슈, 마감 임박 이슈 |
| **Fireflies** | 미팅 녹음 | 미팅 요약, 액션 아이템 |
| **GitHub** | 코드 관리 | 커밋 내역, PR 상태 |

> 위 목록 외에도 원하는 도구를 추가할 수 있다. "우리 회사는 Jira를 써요"라면 Jira도 가능하다.

## EXECUTE

### 1단계: 도구 선택

아래 도구 중에서 자신이 실제로 쓰는 도구를 고르세요. 여러 개를 동시에 선택할 수 있습니다.

```json
AskUserQuestion({
  "questions": [{
    "question": "Context Sync에 연결할 도구를 선택하세요. 실제로 사용하는 도구만 고르면 됩니다.",
    "header": "도구 선택",
    "options": [
      {"label": "Slack", "description": "팀 채팅 메시지 수집"},
      {"label": "Gmail", "description": "이메일 수집"},
      {"label": "Google Calendar", "description": "일정 수집"},
      {"label": "Notion", "description": "태스크/문서 수집"},
      {"label": "Linear", "description": "이슈 트래커 수집"},
      {"label": "Fireflies", "description": "미팅록 수집"},
      {"label": "GitHub", "description": "커밋/PR 수집"},
      {"label": "기타", "description": "위에 없는 도구 (직접 입력)"}
    ],
    "multiSelect": true
  }]
})
```

### 2단계: 템플릿 기반 스킬 생성

사용자가 도구를 선택하면:

1. `templates/context-sync.md`를 읽는다
2. 사용자의 프로젝트에 `.claude/skills/my-context-sync/SKILL.md`를 생성한다
3. 생성 규칙:
   - 선택한 도구만 "소스 정의" 섹션에 남긴다
   - 선택하지 않은 도구의 소스 섹션은 삭제한다
   - 템플릿에 없는 도구(Linear, Fireflies, GitHub, 기타)는 아래 커스터마이징 패턴으로 추가한다:

```markdown
### 소스 N: {도구명}

| 항목 | 값 |
|------|-----|
| MCP 도구 | `{MCP 도구명 또는 "스크립트"}` |
| 수집 범위 | {범위} |

수집 방법:
{MCP 호출 방법 또는 스크립트 실행 방법}

추출할 정보:
- {항목 1}
- {항목 2}
- {항목 3}
```

4. "실행 흐름" 섹션의 병렬 수집 부분도 선택한 도구에 맞게 조정한다
5. 소스 번호를 1부터 다시 매긴다

### 3단계: 생성 결과 확인

생성된 파일의 전체 구조만 간략히 보여준다. 예시:

```
.claude/skills/my-context-sync/SKILL.md 생성 완료!

구조:
  - 소스 1: Slack (채널 메시지)
  - 소스 2: Notion (태스크)
  - 소스 3: Linear (이슈)
  - 실행 흐름: 3개 소스 병렬 수집 → 통합 → 저장
  - 출력: sync/YYYY-MM-DD-context-sync.md
```

> 세부 내용은 이후 블록에서 하나씩 다듬는다. 지금은 골격만 만든 것이다.

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "Context Sync 스킬이 하는 일을 한 문장으로 말하면?",
    "header": "Quiz Block 0",
    "options": [
      {"label": "여러 도구에서 정보를 모아 하나의 문서로 정리한다", "description": "Slack, Gmail, Calendar 등에서 수집 → 통합"},
      {"label": "Slack 메시지만 정리한다", "description": "Slack은 여러 소스 중 하나일 뿐"},
      {"label": "Claude Code를 설치한다", "description": "설치는 Day 1에서 이미 완료"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번. Context Sync 스킬은 **여러 도구에서 정보를 모아 하나의 문서로 정리**하는 스킬이다. Day 1에서 배운 "스킬 = 업무 레시피"를 직접 만드는 것이 오늘의 핵심이다.
