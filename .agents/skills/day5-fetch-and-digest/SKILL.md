---
name: day5-fetch-and-digest
description: AI Native Camp Day 5 콘텐츠 소화 스킬 만들기. fetch-tweet, fetch-youtube, content-digest 3개 스킬을 직접 만들고 활용한다. "5일차", "Day 5", "fetch", "콘텐츠 스킬", "트윗 스킬", "유튜브 스킬", "다이제스트 스킬" 요청에 사용.
---

# Day 5: Fetch & Digest — 콘텐츠를 내 것으로 만드는 스킬

이 스킬이 호출되면 아래 **STOP PROTOCOL**을 반드시 따른다.

---

## 용어 정리

이 스킬에서 사용하는 핵심 용어:

| 용어 | 설명 |
|------|------|
| **fetch** | 외부에서 데이터를 가져오는 것. "배달 주문처럼 URL만 주면 내용이 도착" |
| **digest** | 가져온 내용을 소화(요약·퀴즈·학습)하는 것. "읽고 끝이 아니라 씹어서 내 것으로 만들기" |
| **API** | 프로그램끼리 대화하는 창구. "식당 메뉴판처럼 요청 형식이 정해져 있다" |
| **JSON** | 컴퓨터가 읽기 좋은 데이터 형식. 사람이 보면 중괄호 투성이지만 Claude는 완벽히 이해한다 |
| **yt-dlp** | YouTube에서 자막·메타데이터를 추출하는 무료 도구 |
| **자동 자막** | YouTube가 AI로 만든 자막. 전문 용어나 이름이 틀릴 수 있다 |
| **Web Search 보정** | 자동 자막의 오류를 웹 검색으로 바로잡는 기법 |
| **Quiz-First** | 요약을 먼저 보지 않고 퀴즈부터 푸는 학습법. 9-12% 기억력 향상 효과 |
| **스킬 체이닝** | 하나의 스킬 결과를 다른 스킬의 입력으로 연결하는 것. "fetch → digest 파이프라인" |

---

## STOP PROTOCOL — 절대 위반 금지

> 이 프로토콜은 이 스킬의 최우선 규칙이다.
> 아래 규칙을 위반하면 수업이 망가진다.

### 각 블록은 반드시 2턴에 걸쳐 진행한다

```
┌─ Phase A (첫 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 EXPLAIN 섹션을 읽는다    │
│ 2. 기능을 설명한다                                        │
│ 3. references/에서 해당 블록 파일의 EXECUTE 섹션을 읽는다    │
│ 4. "지금 직접 실행해보세요"라고 안내한다                     │
│ 5. ⛔ 여기서 반드시 STOP. 턴을 종료한다.                    │
│                                                          │
│ ❌ 절대 하지 않는 것: 퀴즈 출제, QUIZ 섹션 읽기             │
│ ❌ 절대 하지 않는 것: AskUserQuestion 호출                  │
│ ❌ 절대 하지 않는 것: "실행해봤나요?" 질문                   │
└──────────────────────────────────────────────────────────┘

  ⬇️ 사용자가 돌아와서 "했어", "완료", "다음" 등을 입력한다

┌─ Phase B (두 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 QUIZ 섹션을 읽는다       │
│ 2. AskUserQuestion으로 퀴즈를 출제한다                     │
│ 3. 정답/오답 피드백을 준다                                 │
│ 4. 다음 블록으로 이동할지 AskUserQuestion으로 묻는다         │
│ 5. ⛔ 다음 블록을 시작하면 다시 Phase A부터.                │
└──────────────────────────────────────────────────────────┘
```

### 핵심 금지 사항 (절대 위반 금지)

1. **Phase A에서 AskUserQuestion을 호출하지 않는다** — 설명 + 실행 안내 후 바로 Stop
2. **Phase A에서 퀴즈를 내지 않는다** — QUIZ 섹션은 Phase B에서만 읽는다
3. **Phase A에서 "실행해봤나요?"를 묻지 않는다** — 사용자가 먼저 말할 때까지 기다린다
4. **한 턴에 EXPLAIN + QUIZ를 동시에 하지 않는다** — 반드시 2턴으로 나눈다

### 공식 문서 URL 출력 (절대 누락 금지)

모든 블록의 Phase A 시작 시, 해당 reference 파일 상단의 `> 공식 문서:` URL을 **반드시 그대로 출력**한다.

```
📖 공식 문서: [URL]
```

- reference 파일에 URL이 여러 개 있으면 전부 출력한다
- URL을 요약하거나 생략하지 않는다

### Phase A 종료 시 필수 문구

Phase A의 마지막에는 반드시 아래 형태의 문구를 출력하고 Stop한다:

```
---
👆 위 내용을 직접 실행해보세요.
실행이 끝나면 "완료" 또는 "다음"이라고 입력해주세요.
```

이 문구 이후에 어떤 도구 호출(AskUserQuestion 포함)이나 추가 텍스트도 출력하지 않는다.

---

## 소요 시간 가이드

| Block | 주제 | 예상 시간 |
|-------|------|-----------|
| 0 | 개념 이해 | ~10분 |
| 1 | fetch-tweet 스킬 만들기 | ~20분 |
| 2 | fetch-youtube 스킬 만들기 | ~30분 |
| 3 | content-digest 스킬 만들기 | ~20분 |
| 4 | 통합 실습 + 마무리 | ~15분 |
| **합계** | | **~95분** |

> Block 2가 가장 시간이 많이 걸리는 핵심 블록입니다. yt-dlp 설정과 Web Search 보정이 포함되어 있습니다.
> **사전 준비 권장**: yt-dlp 설치를 미리 해오면 Block 2 시간을 10분 이상 단축할 수 있습니다. (`brew install yt-dlp` 또는 `pip install yt-dlp`)
> **Fast Track**: 시간이 부족하면 Block 1~3을 각각 하나의 프롬프트로 한 번에 만들 수 있습니다.

---

## 핵심 전략: 실제 스킬을 해체하며 배우기

아래 방식으로 진행한다:

1. Block 0에서 콘텐츠 소화 파이프라인(fetch → digest) 개념을 이해한다
2. Block 1에서 fetch-tweet 스킬을 직접 만든다 (API 활용 + 번역 파이프라인)
3. Block 2에서 fetch-youtube 스킬을 직접 만든다 (자막 추출 + Web Search 보정)
4. Block 3에서 content-digest 스킬을 직접 만든다 (Quiz-First 학습)
5. Block 4에서 3개 스킬을 연결하여 실제 콘텐츠로 실습한다

> 운영진이 실제로 사용하는 스킬(fetch-tweet, content-digest)을 참고하며 자기만의 버전을 만든다.

---

## 블록 특수 규칙

- **Block 0 (개념 이해)**: Phase A에서 콘텐츠 파이프라인 개념 설명 + 원본 스킬 구조 분석 안내 → Stop. Phase B에서 퀴즈.
- **Block 1 (fetch-tweet)**: Phase A에서 fetch-tweet 스킬을 Step-by-Step으로 만드는 방법 안내 → 참가자가 직접 작성 → Stop. Phase B에서 퀴즈.
- **Block 2 (fetch-youtube)**: Phase A에서 fetch-youtube 스킬 만들기 안내 (yt-dlp + Web Search 보정) → 참가자가 직접 작성 → Stop. Phase B에서 퀴즈. (가장 긴 블록 — 완료 후 "여기까지 잘 따라오셨습니다!" 격려)
- **Block 3 (content-digest)**: Phase A에서 content-digest 스킬 만들기 안내 (Quiz-First 학습) → 참가자가 직접 작성 → Stop. Phase B에서 퀴즈.
- **Block 4 (통합 실습)**: Phase A에서 3개 스킬 연결 실습 안내 → 실제 콘텐츠로 실습 → Stop. Phase B에서 종합 퀴즈 + 마무리.

---

## References 파일 맵

| 블록 | 파일 | 주제 |
|------|------|------|
| Block 0 | `references/block0-concept.md` | 콘텐츠 소화 파이프라인 + 스킬 체이닝 |
| Block 1 | `references/block1-fetch-tweet.md` | fetch-tweet 스킬 만들기 |
| Block 2 | `references/block2-fetch-youtube.md` | fetch-youtube 스킬 만들기 |
| Block 3 | `references/block3-content-digest.md` | content-digest 스킬 만들기 |
| Block 4 | `references/block4-integration.md` | 통합 실습 + 마무리 |

> 파일 경로는 이 SKILL.md 기준 상대경로다.
> 각 reference 파일은 `## EXPLAIN`, `## EXECUTE`, `## QUIZ` 섹션으로 구성된다.

---

## 진행 규칙

- 한 번에 한 블록씩 진행한다
- "다음", "skip", 블록 번호/이름으로 이동한다
- 각 블록에서 생성한 스킬 파일은 다음 블록에서 이어서 활용한다
- 참가자의 프로젝트에 `.claude/skills/` 아래에 스킬을 생성한다
- Claude Code 관련 질문이 오면 claude-code-guide 에이전트(내장 도구)로 답변한다. 답변 후 사용자가 직접 따라할 수 있게 단계별로 안내하고, 질문할 때는 AskUserQuestion을 사용한다. 내장 에이전트 답변이 부정확하다고 판단되면, 공식 문서를 `curl`로 파일에 저장한 뒤 Read 툴로 꼼꼼히 읽고 정확한 정보로 다시 답한다 (WebFetch는 요약/손실 위험이 있으므로 사용하지 않는다)

---

## 시작

스킬 시작 시 **먼저 최신 커리큘럼을 설치**한 뒤 블록을 선택한다.

### Step 1: 최신 스킬 설치

아래 명령어를 출력하고 Bash로 실행한다:

```bash
npx skills add ai-native-camp/camp-1 --agent claude-code --yes
```

실행 결과를 간략히 안내한다 (예: "스킬이 최신 버전으로 설치되었습니다").

### Step 2: 블록 선택

아래 테이블을 보여주고 AskUserQuestion으로 어디서 시작할지 물어본다.

| Block | 주제 | 내용 |
|-------|------|------|
| 0 | 개념 이해 | 콘텐츠 소화 파이프라인, 스킬 체이닝이란? |
| 1 | fetch-tweet | X/Twitter 트윗을 가져와서 번역하는 스킬 만들기 |
| 2 | fetch-youtube | YouTube 자막을 가져와서 번역하는 스킬 만들기 |
| 3 | content-digest | 가져온 콘텐츠로 퀴즈-학습하는 스킬 만들기 |
| 4 | 통합 실습 | 3개 스킬을 연결해서 실제 콘텐츠로 실습 |

```json
AskUserQuestion({
  "questions": [{
    "question": "Day 5: Fetch & Digest\n\n어디서부터 시작할까요?",
    "header": "시작 블록",
    "options": [
      {"label": "처음부터 (Block 0)", "description": "콘텐츠 파이프라인 개념부터 차근차근"},
      {"label": "fetch-tweet (Block 1)", "description": "바로 트윗 스킬 만들기부터"},
      {"label": "fetch-youtube (Block 2)", "description": "YouTube 스킬 만들기부터"},
      {"label": "content-digest (Block 3~4)", "description": "퀴즈-학습 스킬 만들기부터"}
    ],
    "multiSelect": false
  }]
})
```

> 시작 블록 선택 후 → 해당 블록의 Phase A부터 진행한다.
