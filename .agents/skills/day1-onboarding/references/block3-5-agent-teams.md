# Block 3-5: Agent Teams

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/agent-teams
> ```

## EXPLAIN

| 항목 | 내용 |
|------|------|
| 근본 원리 | **멀티 에이전트 협업** — 각 에이전트가 독립된 컨텍스트 윈도우를 갖고, 서로 메시지를 주고받으며 협업한다. 공유 태스크 리스트로 누가 뭘 하는지 조율한다 |
| 비유 | 프로젝트 팀 — 팀장이 일을 나누고, 팀원들이 각자 작업하면서 서로 대화하고, 공유 칸반보드로 진행상황을 관리 |
| vs Subagent | Subagent는 부하 직원(1:1 위임, 보고만 함). Agent Teams는 프로젝트 팀(팀원끼리 직접 소통 + 공유 태스크 리스트) |

```
┌─ 리더 ─────────────────────────────────────┐
│                                            │
│  ┌─ Agent A ─┐  ┌─ Agent B ─┐  ┌─ Agent C ─┐
│  │ 시장조사   │  │ 보고서    │  │ 발표자료   │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
│        │              │              │
│        └──────── 메시지 ─────────────┘
│                    +
│            공유 태스크 리스트
└────────────────────────────────────────────┘
  Subagent: 리더에게만 보고
  Teams:    팀원끼리 직접 소통
```

### Agent Teams 활성화 (settings.json)

Agent Teams는 **기본적으로 꺼져 있다.** `settings.json`에 환경 변수를 추가해야 켜진다.

아래 내용을 `~/.claude/settings.json`에 추가한다:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

> 이미 다른 설정이 있으면 `env` 블록 안에 한 줄만 추가하면 된다.
>
> ⚠️ **Ghostty 사용자 참고**: Agent Teams의 분할 창(tmux) 모드는 Ghostty에서 지원되지 않는다.
> 기본 In-process 모드는 정상 동작하니 걱정하지 않아도 된다.
> (분할 창 미지원: VS Code 터미널, Windows Terminal, Ghostty)

### 라이브 데모

> 강사가 iTerm2로 전환하여 `tmux -CC`를 실행한다.
> 여러 터미널 패널에서 Agent들이 동시에 동작하는 모습을 실시간으로 보여준다.
> "지금 보시는 것처럼 각 Agent가 독립된 터미널에서 동시에 작업하고, 서로 메시지를 주고받습니다."

## EXECUTE

### 1단계: settings.json 설정

아래 명령어를 Claude Code에 입력해서 Agent Teams를 활성화하라고 안내한다:

```
내 settings.json에 Agent Teams를 활성화하는 설정을 추가해줘
```

> Claude가 `~/.claude/settings.json` 파일에 `"env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }` 을 추가해줄 것이다.

### 2단계: 설정 확인 체크리스트

설정이 끝났으면 아래 체크리스트를 보여주고, 완료했다고 할 때 검증한다:

```
✅ 체크리스트
- [ ] ~/.claude/settings.json 에 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 가 "1"로 설정됨
```

### 검증 방법

사용자가 "완료", "했어", "다음" 등을 입력하면 Phase B에서 아래를 수행한다:

1. `~/.claude/settings.json` 파일을 Read 툴로 읽는다
2. `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`가 `"1"`로 설정되어 있는지 확인한다
3. 설정이 되어 있으면 → "설정 완료! Agent Teams를 사용할 준비가 됐습니다" + 퀴즈 진행
4. 설정이 안 되어 있으면 → "아직 설정이 안 된 것 같아요. 다시 한번 확인해볼까요?" + 재안내

## QUIZ

settings.json 검증을 먼저 수행한 후, 통과하면 퀴즈를 출제한다:

```json
AskUserQuestion({
  "questions": [{
    "question": "Agent Teams와 Subagent의 차이는?",
    "header": "Quiz 3-5",
    "options": [
      {"label": "각자 독립 인스턴스에서 서로 소통하며 협업", "description": "Subagent는 보고만, Teams는 팀원끼리 대화 + 공유 태스크 리스트"},
      {"label": "Subagent를 여러 개 돌리는 것", "description": "단순 병렬이 아니라 소통 + 공유 태스크 리스트"},
      {"label": "이름만 다름", "description": "구조 자체가 다름"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
