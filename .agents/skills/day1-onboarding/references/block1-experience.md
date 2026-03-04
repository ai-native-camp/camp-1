# Block 1: Experience

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/quickstart
> ```

> 7일 후 모습을 먼저 체험한다. 외우지 않는다. 느끼기만 한다.

## EXPLAIN

먼저 아래 Before/After 테이블을 보여준다:

| Before (지금) | After (7일 후) |
|---------------|----------------|
| 슬랙/캘린더/노션 하나씩 열어서 30분 | 한 문장으로 자동 발송 |
| "앱 만들어줘" → 뭘 만들지 모름 | 모호한 요청 → Claude가 질문으로 명확화 |
| 기능 외우려고 문서 뒤지기 | 모르면 Claude에게 물어보기 |

3가지 데모를 안내한다:

### 데모 1: Skill 실행 — `/weekly-sync`

> 강사가 직접 시연한다. 참가자는 보기만 한다.

강사가 터미널에서 아래를 입력하고, Claude가 Slack 메시지 수집 → git log 확인 → 문서 생성까지 자동으로 진행하는 과정을 보여준다:

```
/weekly-sync
```

핵심 포인트: **한 마디면 끝**. Slack, git, 문서 작성이 하나의 Skill로 자동화된다. 7일 후에는 여러분도 이런 걸 직접 만들 수 있다.

### 데모 2: 모호한 요청 → AskUserQuestion으로 명확화

```
우리 팀 업무를 개선해줘
```

먼저 위처럼 **모호하게** 요청한다. Claude가 혼자 추측해서 결과를 내놓을 것이다.

이번엔 다르게 요청한다:

```
우리 팀 업무를 개선해줘. 모호한 부분은 AskUserQuestion으로 질문해서 명확하게 만들어
```

Claude가 "어떤 팀인가요?", "몇 명인가요?", "가장 큰 병목은?" 등 **선택지를 제시하며 질문**하는 과정을 체험시킨다.

핵심 포인트: AskUserQuestion을 활용하면 Claude가 **추측 대신 질문**한다. 결과의 정확도가 완전히 달라진다. 이 패턴이 Day 3 `/clarify`의 핵심이다.

### 데모 3: Claude에게 물어보기

```
Claude Code에서 MCP가 뭐야?
```

핵심 메시지: 기능을 다 외울 필요 없다. 모르면 Claude에게 물어보면 된다.

## EXECUTE

참가자에게 데모 2, 3을 직접 실행하라고 안내한다:

1. **데모 1** (보기만): `/weekly-sync` 시연은 강사가 보여준 것으로 완료
2. **데모 2** 실행: 일부러 모호하게 요청 → 그다음 AskUserQuestion 활용 버전으로 재요청 → 차이 체험
3. **데모 3** 실행: Claude Code 자체에 대해 질문

## QUIZ

```
체험 정리:
1. Skill 실행 → 한 마디로 복잡한 업무 자동화
2. 모호한 요청 → AskUserQuestion으로 Claude가 질문하며 명확화
3. 모르는 것 → Claude에게 물어보기
```

```json
AskUserQuestion({
  "questions": [{
    "question": "3가지 데모 중 가장 인상적이었던 건?",
    "header": "체험 확인",
    "options": [
      {"label": "데모 1: /weekly-sync", "description": "한 마디로 복잡한 업무 자동화"},
      {"label": "데모 2: AskUserQuestion", "description": "Claude가 질문으로 명확화"},
      {"label": "데모 3: Claude에게 물어보기", "description": "모르면 물어보면 된다"}
    ],
    "multiSelect": false
  }]
})
```

> Block 1도 정답이 없는 체험 확인이다.
