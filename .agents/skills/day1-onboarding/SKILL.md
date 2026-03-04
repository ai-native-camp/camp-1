---
name: day1-onboarding
description: AI Native Camp Day 1 온보딩. Claude와 대화하면서 Claude Code를 익힌다. "1일차", "Day 1", "온보딩" 요청에 사용.
---

# Day 1: Onboarding

이 스킬이 호출되면 아래 **STOP PROTOCOL**을 반드시 따른다.

---

## STOP PROTOCOL — 절대 위반 금지

> 이 프로토콜은 이 스킬의 최우선 규칙이다.
> 아래 규칙을 위반하면 수업이 망가진다.

### 각 블록은 반드시 2턴에 걸쳐 진행한다

```
┌─ Phase A (첫 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 EXPLAIN 섹션을 읽는다    │
│ 2. 기능을 설명한다                                        │
│ 3. references/에서 해당 블록 파일의 EXECUTE 섹션을 읽는다    │
│ 4. "지금 직접 실행해보세요"라고 안내한다                     │
│ 5. ⛔ 여기서 반드시 STOP. 턴을 종료한다.                    │
│                                                          │
│ ❌ 절대 하지 않는 것: 퀴즈 출제, QUIZ 섹션 읽기             │
│ ❌ 절대 하지 않는 것: AskUserQuestion 호출                  │
│ ❌ 절대 하지 않는 것: "실행해봤나요?" 질문                   │
└──────────────────────────────────────────────────────────┘

  ⬇️ 사용자가 돌아와서 "했어", "완료", "다음" 등을 입력한다

┌─ Phase B (두 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 QUIZ 섹션을 읽는다       │
│ 2. AskUserQuestion으로 퀴즈를 출제한다                     │
│ 3. 정답/오답 피드백을 준다                                 │
│ 4. 다음 블록으로 이동할지 AskUserQuestion으로 묻는다         │
│ 5. ⛔ 다음 블록을 시작하면 다시 Phase A부터.                │
└──────────────────────────────────────────────────────────┘
```

### 핵심 금지 사항 (절대 위반 금지)

1. **Phase A에서 AskUserQuestion을 호출하지 않는다** — 설명 + 실행 안내 후 바로 Stop
2. **Phase A에서 퀴즈를 내지 않는다** — QUIZ 섹션은 Phase B에서만 읽는다
3. **Phase A에서 "실행해봤나요?"를 묻지 않는다** — 사용자가 먼저 말할 때까지 기다린다
4. **한 턴에 EXPLAIN + QUIZ를 동시에 하지 않는다** — 반드시 2턴으로 나눈다

### 공식 문서 URL 출력 (절대 누락 금지)

모든 블록의 Phase A 시작 시, 해당 reference 파일 상단의 `> 공식 문서:` URL을 **반드시 그대로 출력**한다.

```
📖 공식 문서: [URL]
```

- reference 파일에 URL이 여러 개 있으면 전부 출력한다
- URL을 요약하거나 생략하지 않는다
- 참가자가 직접 클릭해서 공식 문서를 볼 수 있어야 한다

### Phase A 종료 시 필수 문구

Phase A의 마지막에는 반드시 아래 형태의 문구를 출력하고 Stop한다:

```
---
👆 위 내용을 직접 실행해보세요.
실행이 끝나면 "완료" 또는 "다음"이라고 입력해주세요.
```

이 문구 이후에 어떤 도구 호출(AskUserQuestion 포함)이나 추가 텍스트도 출력하지 않는다.

### 블록 특수 규칙

- **Block 0 (Setup)**: 퀴즈 없음. Phase A에서 설명+실행 안내 → Stop. Phase B에서 완료 확인만.
- **Block 1 (Experience)**: Phase A에서 3가지 데모 안내 → Stop. Phase B에서 체험 소감 확인.
- **Block 2 (Why)**: Phase A에서 Quiz 1 출제 → 피드백 → Stop. Phase B에서 Quiz 2 + 영상 안내.
- **Block 3 (What)**: 7개 기능 각각이 독립 블록. 3-1부터 3-7까지 각각 Phase A → Phase B.
- **Block 3-Break (쉬어가기)**: Phase A만 있고 Phase B 없음. 퀴즈 없음. 터미널 소개 + Status Line 설정 체험.
- **Block 4 (Basics)**: Phase A에서 설명+실행 안내 → Stop. Phase B에서 퀴즈 3개 연속.

---

## References 파일 맵

| 블록 | 파일 |
|------|------|
| Block 0 | `references/block0-setup.md` |
| Block 1 | `references/block1-experience.md` |
| Block 2 | `references/block2-why.md` |
| Block 3-1 ~ 3-4 | `references/block3-1-claude-md.md` ~ `references/block3-4-subagent.md` |
| Block 3-Break | `references/block3-break.md` (쉬어가기: 터미널 & Status Line) |
| Block 3-5 ~ 3-7 | `references/block3-5-agent-teams.md` ~ `references/block3-7-plugin.md` |
| Block 3 마무리 | `references/block3-summary.md` |
| Block 4 | `references/block4-basics.md` |

> 파일 경로는 이 SKILL.md 기준 상대경로다.
> 각 reference 파일은 `## EXPLAIN`, `## EXECUTE`, `## QUIZ` 섹션으로 구성된다.

---

## 진행 규칙

- 한 번에 한 블록씩 진행한다
- "다음", "skip", 블록 번호/이름으로 이동한다
- Claude Code 관련 질문이 오면 claude-code-guide 에이전트(내장 도구)로 답변한다. 답변 후 사용자가 직접 따라할 수 있게 단계별로 안내하고, 질문할 때는 AskUserQuestion을 사용한다. 내장 에이전트 답변이 부정확하다고 판단되면, 공식 문서를 `curl`로 파일에 저장한 뒤 Read 툴로 꼼꼼히 읽고 정확한 정보로 다시 답한다 (WebFetch는 요약/손실 위험이 있으므로 사용하지 않는다)
- Block 3-4(Subagent) 완료 후 → Block 3-Break(쉬어가기) → Block 3-5(Agent Teams)로 이어진다
- Block 3의 7개 기능이 모두 끝나면 `references/block3-summary.md`를 읽고 관계도를 보여준다

---

## 시작

스킬 시작 시 아래 테이블을 보여주고 AskUserQuestion으로 어디서 시작할지 물어본다.

| Block | 주제 | 내용 |
|-------|------|------|
| 0 | Setup | Claude Code 설치 + 첫 대화 + CLAUDE.md |
| 1 | Experience | Working Backward 데모 3가지 |
| 2 | Why | 왜 CLI? 왜 터미널? (퀴즈 2개) |
| 3 | What | 7개 기능 소개 |
| 4 | Basics | CLI + git + GitHub (퀴즈 3개) |

```json
AskUserQuestion({
  "questions": [{
    "question": "어디서부터 시작할까요?",
    "header": "시작 블록",
    "options": [
      {"label": "Block 0: Setup", "description": "Claude Code 설치 + 첫 대화 + CLAUDE.md"},
      {"label": "Block 1: Experience", "description": "Working Backward 데모 3가지"},
      {"label": "Block 2: Why", "description": "왜 CLI? 왜 터미널?"},
      {"label": "Block 3: What", "description": "7개 기능 소개"}
    ],
    "multiSelect": false
  }]
})
```

> 시작 블록 선택 후 → 해당 블록의 Phase A부터 진행한다.
