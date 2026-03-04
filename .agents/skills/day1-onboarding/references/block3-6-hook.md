# Block 3-6: Hook

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/hooks-guide
> ```

## EXPLAIN

| 항목 | 내용 |
|------|------|
| 근본 원리 | **결정론적 프로그래밍** — AI는 확률적이라 "대부분" 맞지만 100%는 아니다. Hook은 AI가 아니라 코드(셸 스크립트)가 실행되므로 100% 확실하게 동작한다 |
| 비유 | 자동 체크리스트 — 특정 이벤트가 발생하면 자동으로 실행 |
| 예시 | "Claude 응답 완료 시 자동 요약", "도구 실행 전 자동 검증" |

```
AI (확률적)                    Hook (결정론적)
  "파일 저장 후                   파일 저장 이벤트
   포맷팅 해줘"                      │
      │                            ▼
      ▼                     ┌──────────────┐
  대부분 함                  │ prettier     │
  가끔 까먹음                │ --write .    │ ← 100% 실행
                            └──────────────┘
```

## EXECUTE

2단계로 안내한다.

### 1단계: Hook 이해하기

먼저 Claude에게 물어보라고 안내한다:

```
Hook이 뭔지 예시와 함께 설명해줘. 내 업무에서 쓸 수 있는 Hook 아이디어 3개도 제안해줘
```

### 2단계: 직접 Hook 추가하기

Claude에게 아래와 같이 입력하라고 안내한다:

```
Stop Hook을 추가해줘. 응답이 끝나면 현재 시간을 터미널에 출력하도록
```

> Claude가 `.claude/settings.local.json`에 Stop 이벤트 Hook을 추가해줄 것이다.
> 예시 결과: 응답이 끝날 때마다 `[완료] 14:32:05` 같은 시간이 터미널에 표시된다.

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "Hook은 언제 실행되나요?",
    "header": "Quiz 3-6",
    "options": [
      {"label": "특정 이벤트가 발생했을 때 자동으로", "description": "응답 완료, 도구 실행 등 이벤트 기반"},
      {"label": "내가 직접 실행할 때", "description": "자동 실행이 핵심"},
      {"label": "매일 정해진 시간에", "description": "스케줄러와는 다름"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
