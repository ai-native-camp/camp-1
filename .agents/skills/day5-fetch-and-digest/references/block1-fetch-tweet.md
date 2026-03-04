# Block 1: fetch-tweet 스킬 만들기

> 공식 문서: https://code.claude.com/docs/ko/skills
> 참고: https://github.com/FixTweet/FxTwitter

## EXPLAIN

Block 0에서 콘텐츠 소화 파이프라인과 스킬 체이닝 개념을 이해했습니다. 이제 첫 번째 스킬인 fetch-tweet을 직접 만듭니다.

### fetch-tweet이 하는 일

X/Twitter URL을 받으면:

1. **원문 가져오기** — FxEmbed API로 트윗 텍스트, 작성자, 인게이지먼트 데이터를 추출
2. **번역 파이프라인** — 요약 → 인사이트 → 전체 번역 순서로 제공

### 핵심 기술: FxEmbed API

X/Twitter는 로그인 없이는 트윗을 읽기 어렵습니다. 하지만 **FxEmbed**라는 오픈소스 프로젝트가 이 문제를 해결합니다.

```
원래 URL: https://x.com/garrytan/status/123456
변환 URL: https://api.fxtwitter.com/garrytan/status/123456
```

도메인만 바꾸면 컴퓨터가 읽기 좋은 형태(JSON)로 트윗 전체 데이터가 옵니다. 스크립트 하나면 충분합니다.

### 번역 파이프라인 — 3단계

```
┌────────────────────────────────────────────┐
│  1. 요약 (3-5문장)                          │
│     "이 트윗이 뭘 말하는지 30초 만에 파악"    │
├────────────────────────────────────────────┤
│  2. 인사이트 (3개)                          │
│     "핵심 메시지 + 시사점 + 내게 어떤 의미"   │
├────────────────────────────────────────────┤
│  3. 전체 번역                              │
│     "원문 전체를 한국어로"                   │
└────────────────────────────────────────────┘
```

왜 이 순서인가요? 긴 스레드 트윗이라면 전체를 번역하기 전에 핵심부터 파악하는 것이 효율적입니다. 짧은 단일 트윗이라도 인사이트를 먼저 뽑으면 맥락 이해가 깊어집니다.

### SKILL.md를 4단계로 만든다

| 단계 | 내용 | 하는 일 |
|------|------|---------|
| Step 1 | frontmatter (이름표) | 스킬 이름과 설명, 트리거 키워드 |
| Step 2 | API 연동 방법 | FxEmbed API URL 변환 규칙 |
| Step 3 | 번역 파이프라인 | 요약-인사이트-전체 번역 3단계 |
| Step 4 | WebFetch Fallback | 스크립트 없이도 동작하는 대안 |

---

## EXECUTE

> **안심하세요**: 아래 프롬프트를 Claude에게 복사해서 붙여넣기만 하면 됩니다. 코드는 Claude가 작성합니다.

> **Fast Track**: 시간이 부족하면 아래 Step 1~4 대신 이 한 프롬프트로 한번에 만들 수 있습니다:
> "fetch-tweet 원본 스킬을 참고해서, .claude/skills/my-fetch-tweet/SKILL.md를 만들어줘. FxEmbed API 활용 + 요약-인사이트-전체 번역 3단계 파이프라인 + WebFetch Fallback 포함해서."

### 준비

```
나만의 fetch-tweet 스킬을 만들 거야.
.claude/skills/my-fetch-tweet/ 폴더를 만들고, SKILL.md 파일을 생성해줘.
먼저 빈 파일로 시작하자.
```

### Step 1: frontmatter 추가

스킬의 이름표를 붙입니다.

> **frontmatter란?** 파일 맨 위에 `---`로 감싸서 적는 "이름표"입니다. 스킬의 이름(name)과 설명(description)을 적어야 Claude가 "아, 이 스킬은 트윗을 가져올 때 쓰는 거구나"라고 인식합니다.

```
my-fetch-tweet/SKILL.md에 frontmatter를 추가해줘:
- name: my-fetch-tweet
- description: X/Twitter URL을 받으면 트윗 원문을 가져와서 요약-인사이트-전체 번역을 제공하는 스킬. "트윗 번역", "트윗 가져와", "X 게시글" 요청에 사용.
```

### Step 2: API 연동 방법 작성

```
SKILL.md에 API 연동 섹션을 추가해줘.
FxEmbed API (api.fxtwitter.com) 사용 방법:
1. URL에서 screen_name과 status_id 추출
2. 도메인을 api.fxtwitter.com으로 변환
3. WebFetch로 JSON 데이터 가져오기
4. 트윗 본문(tweet.text), 작성자(tweet.author), 반응 수치(좋아요/리트윗/조회수) 필드 설명

지원 URL: x.com, twitter.com, fxtwitter.com, fixupx.com
```

### Step 3: 번역 파이프라인 작성

이 스킬의 핵심입니다. 전체 번역을 바로 보여주지 않고, 단계별로 제공합니다.

```
SKILL.md에 번역 파이프라인 섹션을 추가해줘.
3단계로 구성해:

1단계 - 요약 (3-5문장):
  - 트윗의 핵심 주장을 한국어로 요약
  - 작성자 정보와 인게이지먼트 수치 포함

2단계 - 인사이트 (3개):
  - 핵심 메시지: 이 트윗이 정말 말하고 싶은 것
  - 시사점: 업계/트렌드에서의 의미
  - 적용점: 나(독자)에게 어떤 의미인지

3단계 - 전체 번역:
  - 원문 전체를 자연스러운 한국어로 번역
  - 인용 트윗이 있으면 함께 번역
  - 전문 용어는 원문 병기 (예: "에이전트(Agent)")
```

> 여기까지 완료했으면, Claude에게 "지금까지 만든 SKILL.md를 보여줘"라고 입력해서 중간 결과를 확인하세요.

### Step 4: WebFetch Fallback 추가

```
SKILL.md 마지막에 WebFetch Fallback 섹션을 추가해줘.
스크립트 실행이 어려울 때 WebFetch로 직접 API를 호출하는 방법:
- URL: https://api.fxtwitter.com/{screen_name}/status/{status_id}
- Prompt: "Extract the full tweet text, author name, and engagement metrics"
```

### 최종 확인

```
만들어진 my-fetch-tweet/SKILL.md 전체 내용을 보여줘.
```

> **테스트해보기**: 스킬을 만들었으면 바로 테스트해보세요!
> 좋아하는 영어 트윗 URL을 하나 찾아서 "이 트윗 번역해줘 [URL]"이라고 입력하면 됩니다.

---

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "fetch-tweet 스킬에서 번역 파이프라인의 순서가 '요약 → 인사이트 → 전체 번역'인 이유는?",
    "header": "Quiz 1",
    "options": [
      {"label": "긴 텍스트는 토큰 제한 때문에 단계별 처리가 필수라서", "description": "Claude의 컨텍스트 윈도우 관리를 위해"},
      {"label": "전체 번역을 먼저 보면 핵심을 놓치기 쉬우니까", "description": "요약으로 핵심 잡고, 인사이트로 의미 파악 후 전체를 읽으면 이해도 향상"},
      {"label": "API가 요약, 인사이트, 전체를 순서대로 반환하니까", "description": "FxEmbed API의 응답 구조 때문"}
    ],
    "multiSelect": false
  }]
})
```

**정답: 2번.** 전체 번역부터 보면 핵심을 놓치기 쉽다. 요약으로 "이 트윗이 뭘 말하는지" 파악하고, 인사이트로 "나에게 어떤 의미인지" 정리한 뒤, 전체를 읽으면 맥락 속에서 이해도가 훨씬 높아진다. 토큰 제한이나 API 응답 구조와는 무관하다.
