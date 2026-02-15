# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

AI Native Camp 1기 수강생 커리큘럼 레포. 비개발자를 위한 Claude Code 7일 집중 캠프(2026-02-14 ~ 2026-02-21, Naver D2SF).

## Skills as Curriculum

커리큘럼이 곧 Claude Code Skills다. `.claude/skills/` 안의 Skill을 실행하면 Claude가 직접 가르치고, 질문하고, 실습을 안내한다.

| Skill | 트리거 | 내용 |
|-------|--------|------|
| day1-onboarding | `/day1-onboarding` | 설치 + 7개 핵심 기능 체험 |
| day1-test-skill | `/day1-test-skill` | Skill 체험용 데모 |
| day2-supplement-mcp | `/day2-supplement-mcp` | MCP 딥다이브 (개념 ~ 서버 설치 ~ Plugin) |
| day2-create-context-sync-skill | `/day2-create-context-sync-skill` | 나만의 Context Sync 스킬 만들기 |

> 매일 새 Skill이 추가된다 (day3-clarify, day4-wrap, ...).

## Architecture

```
.claude/skills/
├── day1-onboarding/
│   ├── SKILL.md              # 스킬 정의 + STOP PROTOCOL
│   └── references/           # 블록별 교안 (block0 ~ block4)
├── day1-test-skill/
│   └── SKILL.md
├── day2-supplement-mcp/
│   ├── SKILL.md              # MCP 딥다이브 + STOP PROTOCOL
│   └── references/           # 블록별 교안 (block0 ~ block4)
└── day2-create-context-sync-skill/
    ├── SKILL.md              # Context Sync 스킬 만들기 + STOP PROTOCOL
    ├── templates/            # 스킬 템플릿 (context-sync.md)
    └── references/           # 블록별 교안 (block0 ~ block6)
```

각 Skill의 `references/` 폴더에 블록별 교안이 있으며, `EXPLAIN → EXECUTE → QUIZ` 3단 구조로 구성된다.

## Conventions

- 교안 작성 시 STOP PROTOCOL 준수: Phase A(설명+실습) → 사용자 응답 대기 → Phase B(퀴즈+피드백)
- reference 파일은 `block{N}-{topic}.md` 네이밍
- 상위 headquarters/CLAUDE.md에 운영 컨텍스트가 있으므로 함께 참조
