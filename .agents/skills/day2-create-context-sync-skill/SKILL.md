---
name: day2-create-context-sync-skill
description: AI Native Camp Day 2 Context Sync 스킬 만들기. 여러 외부 도구에서 컨텍스트를 수집하여 하나의 sync 문서로 만드는 나만의 스킬을 직접 구축한다. "2일차", "Day 2", "context sync", "컨텍스트 싱크", "sync 스킬", "스킬 만들기", "정보 수집 스킬" 요청에 사용.
---

# Day 2: 나만의 Context Sync 스킬 만들기

이 스킬이 호출되면 아래 **STOP PROTOCOL**을 반드시 따른다.

---

## 용어 정리

이 스킬에서 사용하는 핵심 용어:

| 용어 | 설명 |
|------|------|
| **MCP** | Claude가 외부 서비스(Slack, Gmail 등)와 대화하는 통로. Day 1에서 배운 "도구"를 외부로 확장하는 것 |
| **subagent** | Claude가 다른 Claude를 불러서 일을 시키는 것. 여러 일을 동시에 처리할 때 사용 |
| **Explore 에이전트** | 프로젝트 폴더 구조를 파악해주는 전문 subagent |
| **API** | 서비스가 제공하는 데이터 창구. MCP가 없을 때 직접 코드로 데이터를 가져오는 방법 |
| **스킬(Skill)** | Claude Code에게 특정 작업 방법을 가르치는 문서. Day 1 Block 3-2에서 체험한 것 |

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
│ ❌ 절대 하지 않는 것: AskUserQuestion 호출 (Block 0,2,4 제외)│
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

1. **Phase A에서 AskUserQuestion을 호출하지 않는다 (Block 0, 2, 4 제외)** — 이 3개 블록은 사용자 선택이 필수이므로 예외
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

## 핵심 전략: 템플릿 먼저, 단계별 커스터마이징

아래 방식으로 진행한다:

1. Block 0에서 사용자가 도구를 선택하면, `templates/context-sync.md` 기반으로 스킬 파일을 즉시 생성한다
2. 이후 Block 1~5에서 생성된 스킬의 해당 부분만 수정/확장한다
3. 최종적으로 완성된 스킬을 실행하여 결과를 확인한다

> 템플릿에는 Slack, Notion, Gmail, Google Calendar 4가지 도구의 예시가 포함되어 있다.
> 사용자가 선택한 도구 조합에 맞춰 필요한 부분만 남기고, 새 도구는 같은 패턴으로 추가한다.

### 블록-템플릿 섹션 매핑

각 블록에서 수정하는 템플릿 영역:

| Block | 수정 대상 | 템플릿 섹션 |
|-------|----------|------------|
| 0 | 스킬 골격 생성 | 전체 (선택한 도구만 남기기) |
| 1 | 프로젝트 맥락 반영 | frontmatter description, 수집 범위 |
| 2 | 연결 방법 확정 | 각 소스의 "수집 방법" |
| 3 | 수집 실행 & 검증 | "실행 흐름" 섹션 + "추출할 정보" 조정 |
| 4 | 출력 형식 설정 | "출력 포맷" 섹션 |
| 5 | 최종 정리 + 실행 | 전체 마무리 |

---

## 블록 특수 규칙

- **Block 0 (도구 선택 + 스킬 생성)**: Phase A에서 설명 + AskUserQuestion으로 도구 선택. 선택 결과로 템플릿 기반 스킬 생성 → Stop. Phase B에서 생성된 스킬 확인 퀴즈.
- **Block 1 (프로젝트 탐색)**: Phase A에서 Explore 에이전트로 프로젝트 구조를 파악하고 결과 공유 → Stop. Phase B에서 퀴즈.
- **Block 2 (도구 연결)**: Phase A에서 MCP vs API 선택 안내 + AskUserQuestion → **Claude가 설정을 대신 수행**하고 사용자는 결과를 확인 → Stop. Phase B에서 퀴즈.
- **Block 3 (수집 실행 & 검증)**: Phase A에서 subagent 병렬 수집 설명 + 실행 → 수집 결과를 성공/실패로 구분하여 보여주기 → 실패한 소스 재시도 + 수집 데이터 품질 확인 → Stop. Phase B에서 퀴즈.
- **Block 4 (Output 설정)**: Phase A에서 Output format 선택 안내 + AskUserQuestion → 선택에 따라 스킬 수정 → Stop. Phase B에서 퀴즈.
- **Block 5 (완성 + 실행)**: Phase A에서 최종 스킬 구성 정리 + 실제 실행 → Stop. Phase B에서 종합 퀴즈 + 마무리.

### Block 0 예외 규칙

Block 0의 Phase A는 **AskUserQuestion을 사용**한다. 도구 선택이 이후 모든 블록의 전제 조건이므로 반드시 사용자 입력을 받아야 한다.

Phase A 진행 순서:
1. `references/block0-tool-selection.md`의 EXPLAIN 섹션을 읽고 설명한다
2. AskUserQuestion으로 도구를 선택받는다 (multiSelect: true)
3. `templates/context-sync.md` 템플릿을 읽는다
4. 선택된 도구에 맞춰 사용자의 프로젝트에 `.claude/skills/my-context-sync/SKILL.md`를 생성한다
5. 생성된 파일의 전체 구조만 간략히 보여주고 Stop한다 (세부 내용은 이후 블록에서)

### Block 2 예외 규칙

Block 2의 Phase A도 **AskUserQuestion을 사용**한다. 각 도구별로 MCP와 API 중 연결 방식을 선택해야 한다.

**핵심 원칙: Claude가 설정을 대신 수행하고, 사용자는 결과를 확인한다.**

MCP 선택 시:
1. `references/block2-tool-connection.md`의 MCP 안내를 따른다
2. `scripts/mcp_servers.py`를 사용하여 GitHub README.md에서 적합한 MCP 서버를 검색한다
3. 검색 결과를 보여주고, Claude가 `.mcp.json`에 서버를 등록한다
4. `/mcp` 명령으로 서버 연결 상태를 함께 확인한다

API 선택 시:
1. Claude가 직접 API 호출 코드를 작성한다
2. 사용자의 스킬 `scripts/` 폴더에 저장한다

### Block 4 예외 규칙

Block 4의 Phase A도 **AskUserQuestion을 사용**한다. Output format을 선택해야 한다.

---

## References 파일 맵

| 블록 | 파일 | 내용 |
|------|------|------|
| Block 0 | `references/block0-tool-selection.md` | 도구 선택 + 템플릿 기반 스킬 생성 |
| Block 1 | `references/block1-project-explore.md` | Explore 에이전트로 프로젝트 구조 파악 |
| Block 2 | `references/block2-tool-connection.md` | MCP vs API 연결 방식 선택 + 실행 |
| Block 3 | `references/block3-parallel-collection.md` | subagent 병렬 수집 + 결과 검증 |
| Block 4 | `references/block4-output-format.md` | Output format 선택 (markdown, Slack, Notion) |
| Block 5 | `references/block5-finalize.md` | 최종 스킬 완성 + 실행 + 마무리 |

> 파일 경로는 이 SKILL.md 기준 상대경로다.
> 각 reference 파일은 `## EXPLAIN`, `## EXECUTE`, `## QUIZ` 섹션으로 구성된다.

---

## Templates / Scripts 파일 맵

| 파일 | 용도 |
|------|------|
| `templates/context-sync.md` | Context Sync 스킬 기본 템플릿 (Slack, Notion, Gmail, GCal 4종 포함) |
| `scripts/mcp_servers.py` | GitHub에서 MCP 서버 검색 + README.md 파싱 + 설치 안내 |

> Gmail/Calendar 등의 수집 스크립트는 Block 2에서 Claude가 사용자의 선택에 맞춰 직접 작성한다.

---

## 진행 규칙

- 한 번에 한 블록씩 진행한다
- "다음", "skip", 블록 번호/이름으로 이동한다
- Block 0에서 생성한 스킬 파일을 이후 블록에서 점진적으로 수정한다
- 사용자 프로젝트의 `.claude/skills/my-context-sync/` 디렉토리에 스킬을 생성한다
- Explore 에이전트와 subagent 사용이 핵심이므로 적극 활용한다
- Claude Code 관련 질문이 오면 claude-code-guide 에이전트(내장 도구)로 답변한다. 답변 후 사용자가 직접 따라할 수 있게 단계별로 안내하고, 질문할 때는 AskUserQuestion을 사용한다. 내장 에이전트 답변이 부정확하다고 판단되면, 공식 문서를 `curl`로 파일에 저장한 뒤 Read 툴로 꼼꼼히 읽고 정확한 정보로 다시 답한다

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
| 0 | 도구 선택 | sync할 도구 고르기 + 스킬 골격 생성 |
| 1 | 프로젝트 탐색 | Explore로 프로젝트 구조 파악 |
| 2 | 도구 연결 | MCP or API로 도구 연결 |
| 3 | 수집 실행 & 검증 | subagent 병렬 수집 + 결과 검증 |
| 4 | Output 설정 | 출력 형식 선택 + 스킬 수정 |
| 5 | 완성 + 실행 | 최종 스킬 실행 + 마무리 |

```json
AskUserQuestion({
  "questions": [{
    "question": "Day 2: 나만의 Context Sync 스킬 만들기\n\n어디서부터 시작할까요?",
    "header": "시작 블록",
    "options": [
      {"label": "처음부터 (Block 0)", "description": "sync할 도구 고르기 + 스킬 골격 생성"},
      {"label": "도구 연결 (Block 2)", "description": "도구 선택은 했고, MCP/API 연결부터"},
      {"label": "수집 실행 & 검증 (Block 3)", "description": "연결 완료, 수집부터"},
      {"label": "Output 설정 (Block 4)", "description": "수집 완료, 출력 형식부터"}
    ],
    "multiSelect": false
  }]
})
```

> 시작 블록 선택 후 → 해당 블록의 Phase A부터 진행한다.
