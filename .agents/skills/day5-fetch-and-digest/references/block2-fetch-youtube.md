# Block 2: fetch-youtube 스킬 만들기

> 공식 문서: https://github.com/yt-dlp/yt-dlp
> 참고: https://code.claude.com/docs/ko/skills

## EXPLAIN

Block 1에서 fetch-tweet을 만들었습니다. 이제 더 복잡한 fetch-youtube를 만듭니다. YouTube가 트윗보다 어려운 이유가 있습니다.

### 트윗 vs YouTube — 왜 YouTube가 더 어려운가?

| | 트윗 | YouTube |
|---|------|---------|
| 텍스트 길이 | 짧다 (280자) | 길다 (30분 영상 = 수천 단어) |
| 데이터 소스 | API 한 번 호출 | 자막 추출 + 메타데이터 |
| 정확도 | 원문 그대로 | **자동 자막은 틀릴 수 있다** |
| 처리 방식 | 메인 세션에서 바로 | **Task Agent 필요** (긴 컨텍스트) |

**핵심 차이**: YouTube의 자동 자막은 AI가 생성한 것이라 전문 용어, 사람 이름, 약어가 틀릴 수 있습니다. 예를 들어 "Claude"를 "Cloud"로, "Anthropic"을 "앤트로픽"이 아닌 "앤트로피"로 인식할 수 있습니다.

### 해결책: Web Search 보정

```
1. 자막 추출 (yt-dlp)
2. 영상 제목 + 설명 추출 (메타데이터)
3. 제목/설명의 키워드로 웹 검색 → 올바른 고유명사/용어 확인
4. 자동 자막의 오류를 보정
```

**비유**: 자동 자막은 "받아쓰기"이고, Web Search 보정은 "교정"입니다. 받아쓰기에서 틀린 부분을 검색으로 교정하는 것입니다.

### yt-dlp란?

YouTube에서 영상을 다운로드하는 오픈소스 도구입니다. 우리는 **영상은 다운로드하지 않고 자막만 추출**합니다.

```bash
# 자막만 추출 (영상 다운로드 안 함)
yt-dlp --write-auto-sub --sub-lang "ko,en" --skip-download \
  --convert-subs vtt -o "%(title)s" "{URL}"
```

> 이 명령어를 외우거나 직접 타이핑할 필요는 없습니다. SKILL.md에 적어두면 Claude가 알아서 실행합니다.

- `--write-auto-sub`: 자동 자막 포함
- `--sub-lang "ko,en"`: 한국어 우선, 영어 차선
- `--skip-download`: 영상 다운로드 안 함
- `--convert-subs vtt`: VTT 형식으로 변환

### SKILL.md를 5단계로 만든다

| 단계 | 내용 | 하는 일 |
|------|------|---------|
| Step 1 | frontmatter | 스킬 이름과 설명 |
| Step 2 | 자막 추출 | yt-dlp로 자막 가져오기 + 정제 |
| Step 3 | 메타데이터 추출 | 영상 제목, 설명, 채널명 |
| Step 4 | Web Search 보정 | 키워드로 웹 검색 → 자동 자막 오류 수정 |
| Step 5 | 번역 파이프라인 | 요약-인사이트-전체 번역 (fetch-tweet과 동일) |

---

## EXECUTE

> **안심하세요**: 아래 명령어가 복잡해 보이지만, SKILL.md에 적어두면 Claude가 알아서 실행합니다. 직접 타이핑하거나 외울 필요가 없습니다. 프롬프트를 복사해서 붙여넣기만 하면 됩니다.

### 사전 준비: yt-dlp 설치 확인

먼저 yt-dlp가 설치되어 있는지 확인합니다:

```
yt-dlp가 설치되어 있는지 확인해줘. 없으면 설치 방법을 알려줘.
```

> yt-dlp 설치:
> - Mac: `brew install yt-dlp`
> - Python이 있다면: `pip install yt-dlp` 또는 `uv tool install yt-dlp`
> - 이미 설치되어 있으면 "다음 단계로"
> - **설치가 안 되면**: Claude에게 "내 컴퓨터에 yt-dlp 설치가 안 돼. 도와줘"라고 말하세요

### 준비

```
나만의 fetch-youtube 스킬을 만들 거야.
.claude/skills/my-fetch-youtube/ 폴더를 만들고, SKILL.md 파일을 생성해줘.
```

### Step 1: frontmatter 추가

```
my-fetch-youtube/SKILL.md에 frontmatter를 추가해줘:
- name: my-fetch-youtube
- description: YouTube URL을 받으면 자막을 추출하고, Web Search로 자동자막 오류를 보정한 뒤, 요약-인사이트-전체 번역을 제공하는 스킬. "유튜브 번역", "영상 정리", "YouTube 요약" 요청에 사용.
```

### Step 2: 자막 추출 + 정제

YouTube 자막 추출의 핵심 부분입니다.

```
SKILL.md에 자막 추출 섹션을 추가해줘.

1. yt-dlp로 자막 추출하는 명령어:
   yt-dlp --write-auto-sub --sub-lang "ko,en" --skip-download --convert-subs vtt -o "%(title)s" "{URL}"

2. VTT 자막을 순수 텍스트로 정제하는 sed 파이프라인도 포함해줘:
   sed -E 's/^[0-9]+$//' | sed -E 's/[0-9]{2}:[0-9]{2}:[0-9]{2}.*//g' | sed -E 's/<[^>]+>//g' | tr -s '\n' | grep -v '^$'
   (번호 제거 → 타임스탬프 제거 → 웹 형식 표시 제거 → 빈 줄 정리)

3. 자막 언어 우선순위:
   한국어 수동 > 영어 수동 > 한국어 자동 > 영어 자동

4. 자막이 없는 경우: "이 영상에는 자막이 없습니다. 다른 영상을 선택해주세요" 안내
```

### Step 3: 메타데이터 추출

```
SKILL.md에 메타데이터 추출 섹션을 추가해줘.
yt-dlp --dump-json --no-download "{URL}" 명령어로:
- title: 영상 제목
- description: 영상 설명
- channel: 채널명
- duration: 길이
- chapters: 챕터 (있으면)
```

### Step 4: Web Search 보정 (핵심!)

이 부분이 fetch-youtube를 fetch-tweet보다 한 단계 더 발전시키는 핵심입니다.

```
SKILL.md에 Web Search 보정 섹션을 추가해줘.
이 부분이 가장 중요해:

1. 영상 제목과 description에서 키워드 추출 (5-10개)
   - 고유명사 (사람 이름, 회사명, 제품명)
   - 전문 용어
   - 약어

2. 추출한 키워드로 WebSearch 병렬 실행:
   - "{키워드} 정확한 표기"
   - "{사람 이름} {회사명}"
   - "{전문 용어} explained"

3. 검색 결과로 자동 자막 보정:
   - "Cloud"를 "Claude"로 수정
   - "앤트로피"를 "Anthropic"으로 수정
   - 보정 내역을 기록 (원문 → 수정)

보정 전/후 예시도 포함해줘.
```

> **Fast Track**: 시간이 부족하면 Step 2~4를 한 번에 요청할 수 있습니다:
> "content-digest 원본 스킬의 YouTube 처리 방식을 참고해서 자막 추출, 메타데이터, Web Search 보정을 한꺼번에 추가해줘"

### Step 5: 번역 파이프라인

fetch-tweet과 동일한 3단계입니다.

```
SKILL.md에 번역 파이프라인 섹션을 추가해줘.
fetch-tweet과 같은 3단계:

1단계 - 요약 (3-5문장): 영상 핵심 내용
2단계 - 인사이트 (3개): 핵심 메시지, 시사점, 적용점
3단계 - 전체 번역된 아티클:
  - 영상 전체를 읽기 쉬운 아티클 형태로 번역
  - 챕터가 있으면 챕터별로 구분
  - 보정된 용어 사용
  - 전문 용어는 원문 병기

긴 영상(10분 이상)은 Task Agent를 사용해서 처리하라는 안내도 추가해줘.
```

### 최종 확인

```
만들어진 my-fetch-youtube/SKILL.md 전체 내용을 보여줘.
```

> **여기까지 잘 따라오셨습니다!** fetch-youtube는 yt-dlp + Web Search 보정이 포함된 만큼 가장 복잡한 스킬이었습니다. 다음 content-digest는 이보다 구조가 단순합니다.

---

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "fetch-youtube에서 'Web Search 보정'이 필요한 이유는?",
    "header": "Quiz 2",
    "options": [
      {"label": "자막 파일의 인코딩이 깨져서 글자가 깨질 수 있어서", "description": "VTT 파일의 문자 인코딩 문제 해결"},
      {"label": "YouTube가 번역 기능을 제공하지 않아서", "description": "자체 번역이 필요하기 때문"},
      {"label": "자동 자막이 고유명사/전문 용어를 틀리게 인식할 수 있어서", "description": "AI 생성 자막의 한계를 웹 검색으로 보완"}
    ],
    "multiSelect": false
  }]
})
```

**정답: 3번.** YouTube의 자동 자막은 AI가 음성을 텍스트로 변환한 것이라 고유명사(Claude → Cloud), 전문 용어(Anthropic → 앤트로피), 약어 등이 틀릴 수 있다. 영상 제목과 설명에서 키워드를 추출한 뒤 웹 검색으로 올바른 표기를 확인하여 보정한다.
