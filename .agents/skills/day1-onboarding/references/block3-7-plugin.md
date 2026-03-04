# Block 3-7: Plugin

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/plugins
> 📖 마켓플레이스: https://code.claude.com/docs/ko/discover-plugins
> ```

## EXPLAIN

| 항목 | 내용 |
|------|------|
| 근본 원리 | **패키징과 배포** — 위의 기능들은 모두 개별 파일이다. Plugin은 이것들을 하나의 설치 단위로 묶어서, 한 줄로 팀 전체가 동일한 환경을 갖추게 한다 |
| 비유 | 종합 패키지 — 위의 모든 기능을 묶어서 팀에 공유 |
| 예시 | "마케팅 팀용 플러그인" 하나로 Skill + MCP + Hook + Agent 설치 |

```
개별 설치 (Plugin 없이)          Plugin (한 번에)
┌─────────┐                    ┌─────────────────┐
│ Skill A │ ← 수동 복사         │ marketing-plugin│
│ Skill B │ ← 수동 복사         │ ┌─ Skill A,B   │
│ MCP 설정 │ ← 수동 설정   vs   │ ├─ MCP 설정    │
│ Hook 설정│ ← 수동 설정         │ ├─ Hook 설정   │
│ Agent   │ ← 수동 설정         │ └─ Agent       │
└─────────┘                    └────────┬────────┘
  팀원 각자 반복                         │
                              claude plugin add
                                한 줄이면 끝
```

## EXECUTE

3단계로 직접 플러그인을 설치해본다.

### 1단계: 공식 플러그인 설치

Claude Code에는 공식 마켓플레이스가 있다. `/plugin` 명령어로 둘러보고 하나를 설치해보자:

```
/plugin
```

> 목록에서 마음에 드는 공식 플러그인을 골라 설치해본다.

### 2단계: superpowers 플러그인 설치

개발 워크플로우를 강화하는 인기 플러그인이다. 마켓플레이스를 먼저 등록하고, 거기서 설치한다:

```
/plugin marketplace add obra/superpowers-marketplace
```

마켓플레이스가 등록되면 플러그인을 설치한다:

```
/plugin install superpowers@superpowers-marketplace
```

### 3단계: clarify 플러그인 설치

AI Native Camp 운영팀이 만든 플러그인이다. 우리만의 마켓플레이스에서 가져온다:

```
/plugin marketplace add team-attention/plugins-for-claude-natives
```

```
/plugin install clarify
```

> clarify는 모호한 요청을 명확하게 만들어주는 플러그인이다. Day 3에서 깊이 다룬다.

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "Plugin은 뭘 묶은 것인가요?",
    "header": "Quiz 3-7",
    "options": [
      {"label": "Skill + MCP + Hook + Agent 등을 하나의 패키지로", "description": "여러 기능을 팀 단위로 배포"},
      {"label": "Skill만 묶은 것", "description": "Skill 외에도 MCP, Hook, Agent 포함"},
      {"label": "외부 도구만 묶은 것", "description": "내부 기능도 포함"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
