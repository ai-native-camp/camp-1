# Block 4: 통합 실습 + 마무리

> 공식 문서: https://code.claude.com/docs/ko/skills

## EXPLAIN

Block 1~3에서 3개의 스킬을 만들었습니다:

- **my-fetch-tweet**: X/Twitter 트윗 가져오기 + 번역
- **my-fetch-youtube**: YouTube 자막 추출 + 보정 + 번역
- **my-content-digest**: 가져온 콘텐츠로 퀴즈-학습

이제 이 3개를 **연결해서 실제로 사용**해봅니다.

### 스킬 체이닝 실전

Block 0에서 배운 "스킬 체이닝"을 실제로 해봅니다:

```
[URL 입력] → [fetch 스킬로 가져오기] → [content-digest로 퀴즈-학습]
```

### 나만의 워크플로우 만들기

3개 스킬이 있으면 다양한 조합이 가능합니다:

| 워크플로우 | 사용 스킬 | 상황 |
|-----------|----------|------|
| 트윗 빠른 번역 | fetch-tweet만 | 시간 없을 때 요약만 보기 |
| YouTube 깊이 학습 | fetch-youtube → content-digest | 중요한 영상 제대로 소화 |
| 트윗 스레드 학습 | fetch-tweet → content-digest | 긴 스레드의 핵심 파악 |
| 비교 분석 | fetch-tweet + fetch-youtube → content-digest | 같은 주제 여러 소스 비교 |

### 스킬 개선 팁

실습하면서 느낀 개선점을 바로 반영하는 것이 가장 좋은 학습입니다:

```
my-fetch-tweet 스킬에서 [개선할 부분]을 수정해줘.
```

> 스킬은 한 번 만들면 끝이 아닙니다. 직접 써보면서 계속 다듬어가는 것입니다.

---

## EXECUTE

### 실습 1: 실제 트윗으로 fetch-tweet 테스트

좋아하는 영어 트윗 URL을 하나 찾아서 테스트합니다.

```
이 트윗을 요약-인사이트-전체 번역 해줘: [여기에 실제 X/Twitter URL]
```

> 결과를 보고 다음을 확인하세요:
> - 요약이 핵심을 잘 잡았는지
> - 인사이트가 실제로 유용한지
> - 전체 번역이 자연스러운지

### 실습 2: 실제 YouTube로 fetch-youtube 테스트

관심 있는 영어 YouTube 영상 URL로 테스트합니다.

```
이 영상을 요약-인사이트-전체 번역 해줘: [여기에 실제 YouTube URL]
```

> 결과를 보고 다음을 확인하세요:
> - 자막이 잘 추출되었는지
> - 고유명사가 올바르게 보정되었는지
> - 아티클 형태가 읽기 쉬운지

### 실습 3: content-digest로 퀴즈-학습

위에서 가져온 콘텐츠 중 하나를 선택해서 퀴즈를 풀어봅니다.

```
방금 가져온 콘텐츠로 퀴즈 내줘. Quiz-First 방식으로.
```

> Pre-Quiz 3문제를 먼저 풀고, 틀린 부분을 확인하고, 본 퀴즈 9문제까지 도전해보세요.

### (선택) 스킬 개선

실습 중 개선하고 싶은 부분이 있다면:

```
my-fetch-tweet 스킬에서 [개선할 부분]을 수정해줘.
```

> 직접 써보면서 개선하는 것이 가장 좋은 학습입니다.

---

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "오늘 만든 3개 스킬의 역할을 올바르게 연결한 것은?",
      "header": "Quiz 4-1",
      "options": [
        {"label": "fetch = 번역하기, digest = 저장하기", "description": "fetch가 번역, digest가 파일 저장"},
        {"label": "fetch = 가져오기, digest = 소화하기", "description": "fetch-tweet/youtube가 가져오고, content-digest가 소화"},
        {"label": "fetch = 검색하기, digest = 요약하기", "description": "fetch가 웹 검색, digest가 요약"}
      ],
      "multiSelect": false
    },
    {
      "question": "fetch-youtube에만 있고 fetch-tweet에는 없는 단계는?",
      "header": "Quiz 4-2",
      "options": [
        {"label": "Web Search 보정", "description": "자동 자막의 고유명사/전문 용어 오류를 웹 검색으로 교정"},
        {"label": "번역 파이프라인", "description": "요약-인사이트-전체 번역 3단계"},
        {"label": "frontmatter 작성", "description": "스킬 이름표 작성"}
      ],
      "multiSelect": false
    }
  ]
})
```

**정답 4-1: 2번.** fetch 스킬(fetch-tweet, fetch-youtube)은 외부 콘텐츠를 "가져오는" 역할이고, content-digest는 가져온 콘텐츠를 퀴즈-학습으로 "소화하는" 역할이다.

**정답 4-2: 1번.** YouTube의 자동 자막은 고유명사와 전문 용어를 틀리게 인식할 수 있다. 영상 제목과 설명에서 키워드를 추출한 뒤 웹 검색으로 올바른 표기를 확인하여 보정한다. 트윗은 원문 텍스트 그대로라 이 과정이 불필요하다.

---

### 마무리

오늘 배운 것을 정리합니다:

1. **콘텐츠 소화 파이프라인**: URL → fetch(가져오기) → translate(번역) → digest(소화)
2. **fetch-tweet**: FxEmbed API로 트윗 추출 → 요약-인사이트-전체 번역
3. **fetch-youtube**: yt-dlp로 자막 추출 → Web Search로 오류 보정 → 요약-인사이트-전체 번역
4. **content-digest**: Quiz-First 학습 — 퀴즈부터 → 틀린 부분 공부 → 본 퀴즈
5. **스킬 체이닝**: 스킬 결과를 다른 스킬의 입력으로 연결

> **다음 단계**: 만든 스킬을 매일 사용하면서 개선해보세요. 실제 사용이 최고의 학습입니다.
