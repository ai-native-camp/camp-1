# Block 4: /plugin으로 MCP 확장

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/plugins
> 📖 플러그인 마켓: https://code.claude.com/docs/ko/discover-plugins
> ```

## EXPLAIN

### Plugin과 MCP의 관계

Day 1에서 배웠듯, **Plugin = Skill + MCP + Hook + Agent를 묶은 패키지**다.

```
Plugin 안에 MCP가 포함될 수 있다
┌─────────────────────────────────┐
│         My Plugin               │
│                                 │
│  ┌─────────┐  ┌──────────────┐  │
│  │ Skills  │  │ MCP Servers  │  │
│  └─────────┘  └──────────────┘  │
│  ┌─────────┐  ┌──────────────┐  │
│  │ Hooks   │  │ Agents       │  │
│  └─────────┘  └──────────────┘  │
└─────────────────────────────────┘
```

Plugin을 설치하면 그 안에 포함된 MCP 서버가 **자동으로** 연결된다. 따로 `claude mcp add`를 할 필요가 없다.

### /plugin 명령어

| 명령어 | 동작 |
|--------|------|
| `/plugin` | 플러그인 관리 메뉴 열기 |
| `/plugin marketplace add [URL]` | 마켓플레이스 등록 |
| `/plugin install [이름]` | 플러그인 설치 |

### Plugin이 MCP보다 좋은 점

| 항목 | MCP만 | Plugin + MCP |
|------|-------|--------------|
| 설치 | `claude mcp add ...` 직접 입력 | `/plugin install` 한 줄 |
| 팀 공유 | 각자 설정 | 플러그인 하나로 동일 환경 |
| 추가 기능 | MCP 도구만 | Skill + Hook + Agent까지 |
| 업데이트 | 수동 | 플러그인 업데이트로 자동 |

### Official Plugin vs Community Plugin

```
Official Plugins                    Community Plugins
  ├─ Anthropic이 검증              ├─ 커뮤니티가 만든 것
  ├─ /plugin에서 바로 설치          ├─ marketplace 등록 후 설치
  └─ 안정성 보장                   └─ 다양한 기능

  /plugin                          /plugin marketplace add [URL]
  → 목록에서 선택                   → /plugin install [이름]
```

## EXECUTE

3단계로 Plugin을 통한 MCP 확장을 체험해보자:

**1단계: /plugin으로 공식 플러그인 탐색**

Claude Code에서 아래를 입력한다:

```
/plugin
```

> 설치 가능한 공식 플러그인 목록이 나온다. 각 플러그인의 설명을 읽어보고 마음에 드는 것을 골라 설치해보자.

**2단계: 커뮤니티 마켓플레이스 등록**

Anthropic 공식 외에도 커뮤니티가 만든 플러그인이 있다. 마켓플레이스를 등록해보자:

```
/plugin marketplace add obra/superpowers-marketplace
```

등록 후 플러그인을 설치한다:

```
/plugin install superpowers@superpowers-marketplace
```

> superpowers는 TDD, 디버깅, 코드리뷰 등 개발 워크플로우를 강화하는 플러그인이다.

**3단계: 설치된 플러그인의 MCP 확인**

플러그인을 설치한 후 `/mcp`를 실행해서 플러그인이 자동으로 추가한 MCP 서버가 있는지 확인한다:

```
/mcp
```

> 플러그인에 MCP 서버가 포함되어 있으면 자동으로 목록에 나타난다.

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "Plugin에 MCP 서버가 포함되어 있으면?",
    "header": "Quiz 4",
    "options": [
      {"label": "설치하면 MCP 서버가 자동으로 연결된다", "description": "claude mcp add 없이 자동 설정"},
      {"label": "별도로 claude mcp add를 해야 한다", "description": "Plugin이 자동 처리"},
      {"label": "MCP와 Plugin은 관련 없다", "description": "Plugin은 MCP를 포함할 수 있음"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
피드백: "정확합니다! Plugin의 큰 장점이 바로 이겁니다. 복잡한 설정 없이 설치 한 줄이면 MCP 서버까지 자동 연결됩니다."
