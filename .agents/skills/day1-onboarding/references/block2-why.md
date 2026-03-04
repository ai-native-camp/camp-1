# Block 2: Why

## EXPLAIN

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/how-claude-code-works#%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8-%EB%A3%A8%ED%94%84
> ```

왜 CLI인가? 왜 터미널인가? 2개의 퀴즈로 이해한다.

> Block 2는 설명 없이 바로 퀴즈로 진행하는 특수 블록이다.
> Phase A에서 퀴즈 1을 내고, Phase B에서 퀴즈 2 + 영상을 안내한다.

## QUIZ-1

### Quiz 1: 왜 CLI인가?

```json
AskUserQuestion({
  "questions": [{
    "question": "왜 굳이 터미널을 깔아서 Claude Code를 사용해야 할까요?",
    "header": "Quiz 1",
    "options": [
      {"label": "CLI는 컴퓨터의 모든 일을 할 수 있어서", "description": "GUI는 버튼만 누를 수 있지만 CLI는 제한 없음"},
      {"label": "터미널이 더 예뻐서", "description": "예쁜 건 GUI가 더 예쁨"},
      {"label": "프로그래머처럼 보이려고", "description": "멋은 부산물일 뿐"},
      {"label": "Anthropic이 시켜서", "description": "아무도 안 시킴"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번. 해설로 아래 도식을 보여준다:

```
GUI:  사용자 → [버튼] [버튼] [버튼] → 제한된 기능
CLI:  사용자 → 자유로운 명령어 ────→ 컴퓨터의 모든 기능
      AI 에이전트 → CLI ────────────→ 소프트웨어 직접 제어
```

## QUIZ-2

### Quiz 2: 왜 Cowork가 아니라 터미널인가?

```json
AskUserQuestion({
  "questions": [{
    "question": "왜 CoWork 같은 비개발자용 툴이 아니라 터미널에서 Claude Code를 써야 할까요?",
    "header": "Quiz 2",
    "options": [
      {"label": "모두가 코딩으로 새로운 차원의 일을 하게 될 것이라서", "description": "코딩 = 개발자 전유물이 아니라 모든 지식노동의 도구가 된다"},
      {"label": "Claude CoWork 같은 비개발자용 도구가 더 나아서", "description": "CoWork도 좋지만 터미널이 자유도의 끝판왕"},
      {"label": "터미널이 무료라서", "description": "둘 다 유료"},
      {"label": "개발자만 쓸 수 있어서", "description": "비개발자도 씀. 지금 여기서."}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번. 해설:

```
Cursor, CoWork 같은 도구 → 정해진 UI 안에서의 생산성
터미널 Claude Code   → 코딩이라는 새로운 차원의 일

결과적으로 토큰을 많이 쓸 수 있다 = 엄청나게 많은 노동력을 가진 사람이 된다
```

오늘만 지나면 출발선에 서게 된다. 내일부터는 더 근본적인 원리를 알게 되는 날들이다.

### 영상 시청

아래 영상을 시청하라고 안내한다:

https://youtu.be/JI8S9T7r2SQ?si=aGYqNMqklAeL9pZs&t=23

> "AI 분야가 지식 노동보다 더 큰 규모가 될 수 있는 '소프트웨어 공장 카테고리'라고 보고 있다. 그럴듯한게, 이 그래프들을 보면 말도 안됨. 기존 코딩 생산성 툴의 시장을 그냥 키워버림"
