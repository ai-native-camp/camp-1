# Block 3-1: CLAUDE.md

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/memory
> 📖 기능을 목표에 맞추기: https://code.claude.com/docs/ko/features-overview#%EA%B8%B0%EB%8A%A5%EC%9D%84-%EB%AA%A9%ED%91%9C%EC%97%90-%EB%A7%9E%EC%B6%94%EA%B8%B0
> 📖 기능이 어떻게 로드되는지 이해하기: https://code.claude.com/docs/ko/features-overview#%EA%B8%B0%EB%8A%A5%EC%9D%B4-%EC%96%B4%EB%96%BB%EA%B2%8C-%EB%A1%9C%EB%93%9C%EB%90%98%EB%8A%94%EC%A7%80-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0
> ```

## EXPLAIN

| 항목 | 내용 |
|------|------|
| 근본 원리 | **시스템 프롬프트** — AI가 대화를 시작할 때 가장 먼저 읽는 지시문. 매 세션마다 규칙을 주입하여 AI의 휘발성 기억을 영구 기억으로 만든다 |
| 비유 | 팀 위키 — Claude가 매 대화 시작할 때 읽는 규칙서 |
| 예시 | "항상 존댓말로", "표로 정리해줘", "내 이름은 OOO" |

```
세션 시작
  │
  ▼
┌─────────────┐     ┌─────────────┐
│ CLAUDE.md   │────▶│ 시스템       │────▶ Claude가 규칙을 아는 상태로 대화 시작
│ (영구 기억)  │     │ 프롬프트     │
└─────────────┘     └─────────────┘
  항상 읽힘            매번 자동 주입
```

## EXECUTE

2가지 명령어를 순서대로 실행하라고 안내한다:

**1. `/init` — CLAUDE.md 자동 생성**

```
/init
```

> 현재 폴더를 분석해서 CLAUDE.md를 자동으로 생성해준다. 프로젝트 구조, 기술 스택, 빌드 방법 등을 자동으로 파악해서 작성한다.

**2. `/memory` — 개인 기억 저장**

```
/memory
```

> 대화 중 발견한 패턴이나 선호사항을 영구 기억으로 저장한다. "항상 존댓말로 해줘", "표로 정리해줘" 같은 개인 규칙을 기억하게 만든다.

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "CLAUDE.md는 언제 읽히나요?",
    "header": "Quiz 3-1",
    "options": [
      {"label": "매 대화 시작할 때 자동으로", "description": "Claude가 세션 시작 시 항상 읽음"},
      {"label": "내가 '읽어'라고 할 때만", "description": "수동으로 읽히는 게 아님"},
      {"label": "하루에 한 번", "description": "대화마다 읽음"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
