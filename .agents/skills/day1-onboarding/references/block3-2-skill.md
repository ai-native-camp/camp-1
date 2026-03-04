# Block 3-2: Skill

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/skills
> 📖 참고: https://agentskills.io/what-are-skills
> ```

## EXPLAIN

| 항목 | 내용 |
|------|------|
| 근본 원리 | **점진적 로딩(Progressive Disclosure)** — CLAUDE.md는 항상 전부 읽히지만, Skill은 필요할 때만 꺼내 읽힌다. 컨텍스트 윈도우는 유한하므로, 필요한 순간에 필요한 지식만 로딩한다 |
| 비유 | 업무 레시피 — 반복하는 업무를 한 번 저장하면 다음부터 한 줄로 실행 |
| 예시 | "매주 월요일 캠페인 리포트", "일일 브리핑" |

```
CLAUDE.md ━━━━━━━━━━━━━━━━━━━━━━━━━ 항상 로딩 (매 세션)
Skill A   ─ ─ ─ ─ ─ ─ ┐
Skill B   ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
Skill C   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐  필요할 때만 로딩
                       ▼         ▼         ▼
                  "/sync" 호출  자동 매칭  "/wrap" 호출
```

### Skill 폴더 구조

```
my-skill/
├── SKILL.md          # 필수: 스킬의 본체. 메타데이터 + 지시사항
├── scripts/          # 선택: 실행할 코드 (Python, Bash 등)
├── references/       # 선택: 참고 문서, 교안, 데이터
└── assets/           # 선택: 템플릿, 리소스 파일
```

- `SKILL.md`만 있으면 스킬이 된다. 나머지는 필요할 때 추가한다
- 지금 이 온보딩도 `SKILL.md` + `references/` 구조로 만들어져 있다

## EXECUTE

지금 이 온보딩 자체가 Skill이다. 직접 체험해보기 위해, 새 세션을 열고 아래를 입력해보라고 안내한다:

```
/day1-test-skill
```

> 이 테스트 스킬을 실행하면 축하 메시지가 나온다. Skill이 어떻게 동작하는지 직접 체험하는 것이다.

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "Skill은 CLAUDE.md와 달리 어떻게 로드되나요?",
    "header": "Quiz 3-2",
    "options": [
      {"label": "필요할 때만 점진적으로 로드된다", "description": "호출하거나 자동 매칭될 때만 컨텍스트에 올라옴"},
      {"label": "CLAUDE.md처럼 매번 전부 로드된다", "description": "그러면 컨텍스트 윈도우가 금방 찬다"},
      {"label": "한 번 로드하면 영구 저장된다", "description": "세션이 끝나면 사라짐"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번. CLAUDE.md는 매 세션마다 전부 로드되지만, Skill은 **점진적 로딩(Progressive Disclosure)** — 필요할 때만 꺼내 읽힌다. 컨텍스트 윈도우는 유한하니까.
