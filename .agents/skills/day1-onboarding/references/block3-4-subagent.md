# Block 3-4: Subagent

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/sub-agents
> ```

## EXPLAIN

| 항목 | 내용 |
|------|------|
| 근본 원리 | **프로세스 격리 + Blank Slate** — Subagent는 새로운 Claude Code 프로세스를 띄운다. 메인 대화의 컨텍스트를 물려받지 않고 빈 상태에서 시작해서, 작업만 수행하고 요약만 돌려준다 |
| 비유 | 부하 직원 — 독립된 공간에서 특정 작업을 전담 처리 |
| 예시 | "100페이지 PDF 읽고 핵심만 정리해줘" |

```
┌─ 메인 Claude ──────────────────────────┐
│  대화 컨텍스트: [A, B, C, D, E...]     │
│                                        │
│  "PDF 분석해줘" ──┐                     │
│                   ▼                    │
│  ┌─ Subagent ──────────────┐           │
│  │ 컨텍스트: [blank slate]  │           │
│  │ 작업: PDF 분석            │           │
│  │ 결과: 요약 3줄 ──────────┼──▶ 전달   │
│  └─────────────────────────┘           │
└────────────────────────────────────────┘
```

## EXECUTE

Subagent가 실제로 동작하는 걸 체험하라고 안내한다:

```
이 폴더의 파일 구조를 탐색해서 정리해줘. Explore 에이전트를 사용해
```

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "Subagent는 왜 필요한가요?",
    "header": "Quiz 3-4",
    "options": [
      {"label": "독립된 공간에서 전담 처리시키려고", "description": "메인 대화 컨텍스트를 소비하지 않고 별도 처리"},
      {"label": "Claude가 혼자 못해서", "description": "Claude가 못하는 건 아니고 효율의 문제"},
      {"label": "필수 기능이라서", "description": "없어도 되지만 있으면 강력함"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번.
