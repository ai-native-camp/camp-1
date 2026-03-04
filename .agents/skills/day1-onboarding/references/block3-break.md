# Block 3-Break: 쉬어가기 — 터미널 & Status Line

> 이 블록은 퀴즈 없이 가볍게 진행한다. Phase A만 있고 Phase B는 없다.
> 사용자가 "완료" 또는 "다음"이라고 하면 Block 3-5로 넘어간다.

## EXPLAIN

여기까지 Claude Code의 핵심 기능 4개(CLAUDE.md, Skill, MCP, Subagent)를 배웠다. 잠깐 숨 고르기.

Claude Code는 **터미널**에서 돌아간다. 어떤 터미널을 쓰느냐에 따라 경험이 달라진다.

### 터미널 추천

| 터미널 | 특징 | 설치 |
|--------|------|------|
| **Ghostty** | 빠르고 가벼움. GPU 가속. 오픈소스 | [ghostty.org](https://ghostty.org) |
| **iTerm2** | macOS 대표 터미널. 풍부한 기능 | [iterm2.com](https://iterm2.com) |
| **WezTerm** | 크로스플랫폼. Lua로 설정 | [wezfurlong.org/wezterm](https://wezfurlong.org/wezterm) |

> 기본 Terminal.app도 쓸 수 있지만, 위 터미널들은 색상, 폰트, 분할 화면 등이 훨씬 자유롭다.

### Claude Code Status Line

Claude Code 화면 맨 아래에 **상태 표시줄**을 커스터마이즈할 수 있다.
지금 쓰는 모델, 컨텍스트 사용량, Git 브랜치 등을 실시간으로 보여준다.

**설정하는 가장 쉬운 방법:**

Claude Code에 이렇게 말하면 된다:

```
/statusline 모델 이름과 컨텍스트 사용률을 보여줘
```

이 한 줄이면 Claude가 알아서 스크립트를 만들고 설정까지 해준다.

**직접 만들고 싶다면:**

`~/.claude/settings.json`에 추가:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

그리고 `~/.claude/statusline.sh`를 만든다:

```bash
#!/bin/bash
input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

# 프로그레스 바
BAR_WIDTH=10
FILLED=$((PCT * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))
BAR=$(printf "%${FILLED}s" | tr ' ' '▓')$(printf "%${EMPTY}s" | tr ' ' '░')

echo "[$MODEL] $BAR $PCT%"
```

결과: `[Opus] ▓▓░░░░░░░░ 25%`

> `jq`가 없으면 `brew install jq` (Mac) 또는 `sudo apt install jq` (Linux)

## EXECUTE

두 가지를 해보라고 안내한다:

1. **Status Line 설정**: Claude Code에 `/statusline 모델 이름과 컨텍스트 사용률을 프로그레스 바로 보여줘`라고 입력
2. **터미널 구경**: 위 터미널 중 하나의 공식 사이트를 방문해서 스크린샷 구경
