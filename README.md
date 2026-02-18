# AI Native Camp - 1기

> 7일 후, 당신의 업무 방식은 영구적으로 바뀐다.

비개발자를 위한 Claude Code 7일 집중 캠프. 2026-02-14 ~ 2026-02-21 (일요일 휴식), Naver D2SF.

## 설치

```bash
npx skills add ai-native-camp/camp-1 --agent claude-code --yes
```

이 한 줄이면 모든 커리큘럼 스킬이 Claude Code에 설치됩니다. 특정 Day만 설치하려면:

```bash
# Day 1만 설치
npx skills add ai-native-camp/camp-1 --skill day1-onboarding --agent claude-code --yes

# Day 2만 설치
npx skills add ai-native-camp/camp-1 --skill day2-create-context-sync-skill --agent claude-code --yes

# Day 4만 설치
npx skills add ai-native-camp/camp-1 --skill day4-wrap-and-analyze --agent claude-code --yes
```

> 설치 후 Claude Code에서 `/day1-onboarding`, `/day2-create-context-sync-skill`, `/day4-wrap-and-analyze` 등으로 시작하세요.

## Skills as Curriculum

이 캠프의 커리큘럼은 **Claude Code Skills 그 자체**다.

슬라이드를 넘기며 듣는 강의가 아니다. `/day1-onboarding`을 실행하면 Claude가 직접 가르치고, 질문하고, 실습을 안내한다. 매일 새로운 Skill이 열리고, 어제 배운 것 위에 오늘을 쌓는다.

```
.claude/skills/
├── day1-onboarding/                  # 설치 + 7개 핵심 기능
├── day2-supplement-mcp/                        # MCP 딥다이브 (개념 ~ 서버 설치 ~ Plugin)
├── day2-create-context-sync-skill/   # 나만의 Context Sync 스킬 만들기
├── day3-clarify/                      # 요구사항 명확화
├── day4-wrap-and-analyze/             # session-wrap 스킬 만들기 + 세션 분석
├── ...
└── day7-graduation/
```

Skill을 만드는 법을 Skill로 배운다. 이것이 이 캠프의 방식이다.

## 커리큘럼

| Day | Skill | 주제 |
|-----|-------|------|
| 1 | `day1-onboarding` | Claude Code 설치 + 7개 핵심 기능 (CLAUDE.md, Skill, MCP, Subagent, Agent Teams, Hook, Plugin) |
| 2 | `day2-supplement-mcp` | MCP 딥다이브 — 개념 이해, 서버 설치, /mcp 명령어, 인기 서버, Plugin MCP |
| 2 | `day2-create-context-sync-skill` | 나만의 Context Sync 스킬 만들기 — 도구 선택 → MCP/API 연결 → 병렬 수집 → 완성 |
| 3 | *coming soon* | 요구사항 명확화 |
| 4 | `day4-wrap-and-analyze` | session-wrap 스킬 직접 만들기 + history-insight + session-analyzer |
| ... | | |
| 7 | *coming soon* | 졸업 |

## 캠프가 끝나면

수료가 아니라 시작이다. Claude Code라는 불을 다루는 신인류 커뮤니티의 일원이 된다.
