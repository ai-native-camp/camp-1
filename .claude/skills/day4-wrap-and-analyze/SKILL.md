---
name: day4-wrap-and-analyze
description: AI Native Camp Day 4 Wrap & Analyze. session-wrap 스킬을 직접 만들고, history-insight와 session-analyzer로 세션을 분석한다. "4일차", "Day 4", "wrap", "세션 분석", "session wrap", "세션 래핑" 요청에 사용.
---

# Day 4: Wrap & Analyze

이 스킬이 호출되면 아래 **STOP PROTOCOL**을 반드시 따른다.

---

## 용어 정리

이 스킬에서 사용하는 핵심 용어:

| 용어 | 설명 |
|------|------|
| **session-wrap** | 코딩 세션이 끝날 때 작업을 정리하고 문서화하는 스킬. "퇴근 전 책상 정리" |
| **multi-agent** | 여러 에이전트가 동시에 일하는 패턴. "회의에서 각 팀장에게 동시에 보고 받기" |
| **병렬(Parallel)** | 여러 작업을 동시에 처리하는 것. "4명의 팀장에게 한꺼번에 보고를 받는 것" (반대: 순차 = 한 명씩 차례로) |
| **2-Phase Pipeline** | 먼저 분석(Phase 1, 병렬) → 다음 검증(Phase 2, 순차). "전문가 의견 수집 후 팀장이 중복 체크" |
| **frontmatter** | 스킬 파일 맨 위에 `---`로 감싸서 적는 "이름표". 스킬의 이름(name)과 설명(description)을 여기에 적는다 |
| **history-insight** | 과거 세션 기록을 분석해 인사이트를 추출하는 스킬 |
| **session-analyzer** | 스킬이 의도대로 실행됐는지 검증하는 분석 도구 |
| **플러그인(Plugin)** | 외부에서 설치한 스킬 모음. 스킬이 여러 개 묶여 있는 "스킬 패키지" |

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

### Phase A 종료 시 필수 문구

Phase A의 마지막에는 반드시 아래 형태의 문구를 출력하고 Stop한다:

```
---
👆 위 내용을 직접 실행해보세요.
실행이 끝나면 "완료" 또는 "다음"이라고 입력해주세요.
```

이 문구 이후에 어떤 도구 호출(AskUserQuestion 포함)이나 추가 텍스트도 출력하지 않는다.

---

## 소요 시간 가이드

| Block | 주제 | 예상 시간 |
|-------|------|-----------|
| 0 | 개념 이해 | ~10분 |
| 1 | 스킬 만들기 | ~30분 |
| 2 | 실행 & 검증 | ~15분 |
| 3 | History Insight | ~10분 |
| 4 | Session Analyzer + 마무리 | ~15분 |
| **합계** | | **~80분** |

> 참가자 속도에 따라 75~90분 소요될 수 있습니다. Block 1이 가장 시간이 오래 걸리는 핵심 블록입니다.

---

## 핵심 전략: 원본 스킬을 해체하며 배우기

아래 방식으로 진행한다:

1. Block 0에서 session-wrap 스킬의 구조와 multi-agent 원리를 이해한다
2. Block 1에서 참가자가 session-wrap 스킬의 SKILL.md를 직접 작성한다 (단계별 안내)
3. Block 2에서 직접 만든 스킬을 실행하고 결과를 확인한다
4. Block 3에서 history-insight로 과거 세션 기록을 분석한다
5. Block 4에서 session-analyzer로 스킬 실행을 검증한다

> session-wrap 원본은 플러그인에 설치되어 있다. 참가자는 이를 참고하면서 자기만의 버전을 만든다.

---

## 블록 특수 규칙

- **Block 0 (개념 이해)**: Phase A에서 multi-agent 개념 설명 + session-wrap 원본 구조 분석 안내 → Stop. Phase B에서 퀴즈.
- **Block 1 (스킬 만들기)**: Phase A에서 SKILL.md를 Step-by-Step으로 작성하는 방법 안내 → 참가자가 직접 작성 → Stop. Phase B에서 작성한 스킬 구조 퀴즈. (가장 긴 블록 — 완료 후 "여기까지 잘 따라오셨습니다!" 격려)
- **Block 2 (실행 & 검증)**: Phase A에서 만든 스킬 실행 + 결과 확인 안내 → Stop. Phase B에서 실행 결과 퀴즈.
- **Block 3 (History Insight)**: Phase A에서 history-insight 스킬 소개 + 실행 안내 → Stop. Phase B에서 퀴즈.
- **Block 4 (Session Analyzer)**: Phase A에서 session-analyzer 소개 + 실행 안내 → Stop. Phase B에서 종합 퀴즈 + 마무리.

---

## References 파일 맵

| 블록 | 파일 | 주제 |
|------|------|------|
| Block 0 | `references/block0-concept.md` | Multi-agent 패턴 + session-wrap 개념 |
| Block 1 | `references/block1-build-session-wrap.md` | session-wrap 스킬 직접 만들기 |
| Block 2 | `references/block2-run-session-wrap.md` | 만든 스킬 실행 + 검증 |
| Block 3 | `references/block3-history-insight.md` | history-insight 실습 |
| Block 4 | `references/block4-session-analyzer.md` | session-analyzer 실습 |

> 파일 경로는 이 SKILL.md 기준 상대경로다.
> 각 reference 파일은 `## EXPLAIN`, `## EXECUTE`, `## QUIZ` 섹션으로 구성된다.

---

## 진행 규칙

- 한 번에 한 블록씩 진행한다
- "다음", "skip", 블록 번호/이름으로 이동한다
- Block 1에서 생성한 스킬 파일을 Block 2에서 실행한다
- 참가자의 프로젝트에 `.claude/skills/my-session-wrap/SKILL.md`를 생성한다
- Claude Code 관련 질문이 오면 claude-code-guide 에이전트(내장 도구)로 답변한다. 답변 후 사용자가 직접 따라할 수 있게 단계별로 안내하고, 질문할 때는 AskUserQuestion을 사용한다. 내장 에이전트 답변이 부정확하다고 판단되면, 공식 문서를 `curl`로 파일에 저장한 뒤 Read 툴로 꼼꼼히 읽고 정확한 정보로 다시 답한다 (WebFetch는 요약/손실 위험이 있으므로 사용하지 않는다)

---

## 시작

스킬 시작 시 **먼저 최신 커리큘럼을 설치**한 뒤 블록을 선택한다.

### Step 1: 최신 스킬 설치

아래 명령어를 출력하고 Bash로 실행한다:

```bash
npx skills add ai-native-camp/camp-1 --agent claude-code --yes
```

실행 결과를 간략히 안내한다 (예: "스킬이 최신 버전으로 설치되었습니다").

### Step 2: 블록 선택

아래 테이블을 보여주고 AskUserQuestion으로 어디서 시작할지 물어본다.

| Block | 주제 | 내용 |
|-------|------|------|
| 0 | 개념 이해 | Multi-agent 패턴, session-wrap이란? |
| 1 | 스킬 만들기 | session-wrap SKILL.md 직접 작성 |
| 2 | 실행 & 검증 | 만든 스킬 실행 + 결과 확인 |
| 3 | History Insight | 세션 히스토리 분석 실습 |
| 4 | Session Analyzer | 세션 실행 검증 실습 |

```json
AskUserQuestion({
  "questions": [{
    "question": "Day 4: Wrap & Analyze\n\n어디서부터 시작할까요?",
    "header": "시작 블록",
    "options": [
      {"label": "처음부터 (Block 0)", "description": "Multi-agent 패턴과 session-wrap 개념부터 차근차근"},
      {"label": "스킬 만들기 (Block 1)", "description": "개념을 이미 알면 바로 스킬 작성하기"},
      {"label": "실행 & 검증 (Block 2)", "description": "스킬을 이미 만들었으면 실행 + 결과 확인"},
      {"label": "분석 도구 (Block 3~4)", "description": "history-insight와 session-analyzer 실습부터"}
    ],
    "multiSelect": false
  }]
})
```

> 시작 블록 선택 후 → 해당 블록의 Phase A부터 진행한다.
