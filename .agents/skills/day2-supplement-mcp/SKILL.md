---
name: day2-supplement-mcp
description: Day 2 보충 자료 - MCP 딥다이브. Claude Code에 외부 도구를 연결하는 MCP를 체계적으로 배운다. "MCP 배우기", "MCP 보충", "MCP 강의", "MCP 학습" 요청에 사용.
---

# Day 2 보충: MCP 딥다이브

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

---

## References 파일 맵

| 블록 | 파일 | 주제 |
|------|------|------|
| Block 0 | `references/block0-concept.md` | MCP 개념 이해 |
| Block 1 | `references/block1-add-server.md` | MCP 서버 추가하기 |
| Block 2 | `references/block2-mcp-command.md` | /mcp 명령어로 도구 탐색 |
| Block 3 | `references/block3-popular-servers.md` | 인기 MCP 서버 탐색 및 설치 |
| Block 4 [BONUS] | `references/block4-plugin-mcp.md` | /plugin으로 MCP 확장 |

> 파일 경로는 이 SKILL.md 기준 상대경로다.
> 각 reference 파일은 `## EXPLAIN`, `## EXECUTE`, `## QUIZ` 섹션으로 구성된다.

---

## 진행 규칙

- 한 번에 한 블록씩 진행한다
- "다음", "skip", 블록 번호/이름으로 이동한다
- BONUS 블록은 시간이 남을 때만 진행한다
- Claude Code 관련 질문이 오면 claude-code-guide 에이전트(내장 도구)로 답변한다. 답변 후 사용자가 직접 따라할 수 있게 단계별로 안내하고, 질문할 때는 AskUserQuestion을 사용한다
- Block 3 완료 후 전체 마무리 안내 (BONUS Block 4는 시간 여유 시 진행)

---

## 시작

스킬 시작 시 **먼저 최신 커리큘럼을 설치**한 뒤 블록을 선택한다.

### Step 1: 최신 스킬 설치

아래 명령어를 출력하고 Bash로 실행한다:

```bash
npx skills add ai-native-camp/camp-1 --agent claude-code --yes
```

실행 결과를 간략히 안내한다 (예: "4개 스킬이 최신 버전으로 설치되었습니다").

### Step 2: 블록 선택

아래 테이블을 보여주고 AskUserQuestion으로 어디서 시작할지 물어본다.

| Block | 주제 | 내용 |
|-------|------|------|
| 0 | MCP 개념 | MCP가 뭔지, USB-C 비유, 아키텍처 |
| 1 | 서버 추가 | `claude mcp add`로 실제 서버 연결 |
| 2 | /mcp 탐색 | 연결된 서버와 도구 목록 확인 |
| 3 | 인기 서버 | 공식 목록에서 유용한 서버 설치 |
| 4 [BONUS] | Plugin + MCP | /plugin으로 MCP 포함 플러그인 설치 |

```json
AskUserQuestion({
  "questions": [{
    "question": "어디서부터 시작할까요?",
    "header": "시작 블록",
    "options": [
      {"label": "Block 0: MCP 개념", "description": "MCP가 뭔지, 왜 필요한지부터"},
      {"label": "Block 1: 서버 추가", "description": "바로 MCP 서버 연결 실습"},
      {"label": "Block 2: /mcp 탐색", "description": "이미 서버가 있어서 도구 확인부터"},
      {"label": "Block 3: 인기 서버", "description": "어떤 서버가 있는지 둘러보기"}
    ],
    "multiSelect": false
  }]
})
```

> 시작 블록 선택 후 → 해당 블록의 Phase A부터 진행한다.
