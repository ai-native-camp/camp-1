# Block 4: Basics

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/cli-usage
> ```

## EXPLAIN

CLI, git, GitHub, 에디터 기초를 퀴즈와 함께 배운다.

### CLI 기초

| 명령어 | 의미 | 비유 |
|--------|------|------|
| cd 폴더명 | 폴더 이동 | 파인더에서 폴더 더블클릭 |
| ls | 목록 보기 | 폴더 열어서 뭐 있나 보기 |
| pwd | 현재 위치 | 주소창 보기 |
| cat 파일명 | 파일 내용 보기 | 메모장으로 파일 열어보기 |
| open 파일명 | 파일/폴더 열기 | 파인더에서 더블클릭 (Mac 전용) |

이 5개면 충분하다. Claude Code가 나머지는 다 해준다.

### git 기초

"보고서_최종.docx → 보고서_최종_진짜.docx → 보고서_최종_찐최종.docx" — git을 쓰면 이런 일이 없다.

| 동작 | 비유 |
|------|------|
| git clone | Google Drive에서 폴더 다운로드 |
| git commit | 게임 세이브 |
| git branch | A안, B안 동시 작업 |
| git push | Google Drive에 업로드 |

git은 실행 취소의 끝판왕이다. 뭘 해도 돌아갈 수 있다.

> 더 알고 싶다면:
> - [git 간편 안내서](https://rogerdudler.github.io/git-guide/index.ko.html) — 한국어, 한 페이지로 끝
> - [Learn Git Branching](https://learngitbranching.js.org/?locale=ko) — 브라우저에서 직접 해보는 시각적 git 튜토리얼
> - [코딩애플 - Git & GitHub](https://codingapple.com/course/git-and-github/) — 무료 한국어 영상 강의

### GitHub 기초

| 개념 | 비유 |
|------|------|
| Pull Request (PR) | "이렇게 바꿨는데 괜찮아?" 리뷰 요청 |
| Merge | "오케이, 합치자" 리뷰 통과 후 반영 |

> 더 알고 싶다면:
> - [GitHub 공식 시작 가이드](https://docs.github.com/ko/get-started/start-your-journey/hello-world) — 한국어, GitHub이 직접 만든 튜토리얼
> - [초보자를 위한 git과 GitHub 시작기 (모두의연구소)](https://modulabs.co.kr/blog/git-and-github-for-beginners) — 비개발자 눈높이 한국어 블로그

### 에디터 비교

| 에디터 | 특징 | 추천 대상 |
|--------|------|-----------|
| Cursor | AI 내장, CC 시너지 | 코드 편집도 할 분 |
| VSCode | 범용적, 확장 풍부 | 이미 쓰고 계신 분 |
| Antigravity | CC 전용, 가장 간단 | 처음 시작하는 분 |

"이 캠프에서는 터미널에서 claude만 쳐도 충분합니다."

## EXECUTE

Claude Code에게 명령어를 대신 시켜보는 체험이다. 아래 3가지를 순서대로 Claude Code에 입력하라고 안내한다:

**1. CLI 체험** — Claude에게 현재 위치를 물어본다:

```
지금 내가 어느 폴더에 있는지 알려줘
```

> Claude가 `pwd`를 실행해서 경로를 보여줄 것이다. 직접 pwd를 칠 필요가 없다!

**1-2. CLI 직접 체험** — Claude Code 안에서 `!`를 붙이면 터미널 명령어를 직접 실행할 수 있다:

```
!cat .claude/skills/day1-onboarding/references/block4-basics.md
```

> 지금 배우고 있는 바로 이 교안의 내용이 화면에 출력된다! `!`는 "Claude한테 시키지 말고 내가 직접 실행할게"라는 뜻이다.

**2. git 체험** — Claude에게 git 상태를 물어본다:

```
이 폴더가 git으로 관리되고 있는지 확인해줘. 최근 커밋 3개도 보여줘
```

> Claude가 `git status`와 `git log`를 실행해줄 것이다. 명령어를 몰라도 된다.

**3. GitHub 체험** — Claude에게 GitHub에 대해 물어본다:

```
GitHub이 뭔지, Pull Request가 뭔지 비개발자한테 설명하듯 알려줘
```

## QUIZ

> Block 4는 실행 확인 후 칭찬 + 퀴즈 3개를 연속으로 진행한다.
> 사용자가 돌아오면 먼저 "잘하셨습니다! 방금 CLI와 git을 Claude Code를 통해 직접 사용한 겁니다. 명령어를 몰라도 Claude에게 말로 시키면 됩니다." 라고 칭찬한 뒤, 아래 퀴즈를 순서대로 출제한다.

### Quiz 3: CLI

```json
AskUserQuestion({
  "questions": [{
    "question": "방금 Claude가 현재 폴더 위치를 알려줄 때 사용한 명령어는?",
    "header": "Quiz 3",
    "options": [
      {"label": "pwd", "description": "Print Working Directory — 현재 위치 출력"},
      {"label": "ls", "description": "목록 보기"},
      {"label": "cd", "description": "폴더 이동"},
      {"label": "where", "description": "이런 명령어는 없음"}
    ],
    "multiSelect": false
  }]
})
```

정답: pwd (Print Working Directory)
피드백: "맞습니다! 직접 외울 필요는 없지만, Claude가 뒤에서 뭘 하는지 알면 더 똑똑하게 시킬 수 있습니다."

### Quiz 4: git

```json
AskUserQuestion({
  "questions": [{
    "question": "방금 Claude가 최근 커밋을 보여줬죠. git에서 '게임 세이브'에 해당하는 동작은?",
    "header": "Quiz 4",
    "options": [
      {"label": "git commit", "description": "현재 상태를 저장"},
      {"label": "git clone", "description": "폴더 다운로드"},
      {"label": "git push", "description": "업로드"},
      {"label": "git save", "description": "이런 명령어는 없음"}
    ],
    "multiSelect": false
  }]
})
```

정답: git commit
피드백: "정확합니다! commit = 세이브. 뭘 해도 돌아갈 수 있으니 실험을 두려워하지 마세요."

### Quiz 5: GitHub

```json
AskUserQuestion({
  "questions": [{
    "question": "GitHub에서 '이렇게 바꿨는데 괜찮아?' 하고 리뷰를 요청하는 것은?",
    "header": "Quiz 5",
    "options": [
      {"label": "Pull Request (PR)", "description": "변경사항 리뷰 요청"},
      {"label": "Merge", "description": "리뷰 통과 후 합치기"},
      {"label": "git push", "description": "업로드"},
      {"label": "Issue", "description": "버그/기능 요청 등록"}
    ],
    "multiSelect": false
  }]
})
```

정답: Pull Request (PR)
피드백: "훌륭합니다! CLI, git, GitHub — 이 세 가지를 직접 체험했습니다. 앞으로 Claude에게 말로 시키면 되니까, 명령어 자체를 외울 필요는 전혀 없습니다."
