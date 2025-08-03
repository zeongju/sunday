# 화타의 진료실 - 예산 종합 병원

예산 종합 병원의 YouTube 채널 동영상을 자동으로 가져와서 표시하는 웹사이트입니다.

## 기능

- YouTube 채널에서 동영상 자동 수집
- 새 동영상이 있을 때만 업데이트 (중복 방지)
- 카테고리별 동영상 분류 (목, 허리, 어깨, 팔꿈치, 손/손목, 엉덩이/고관절, 무릎, 발목/발, 일반의학)
- PWA(Progressive Web App) 지원
- 반응형 디자인
- 업데이트 로그 기록

## 파일 구조

```
화타홈페이지/
├── index.html              # 메인 웹페이지
├── manifest.json           # PWA 매니페스트
├── update_videos.py        # YouTube 동영상 자동 업데이트 스크립트
├── run_update.bat          # Windows 배치 파일
├── setup_scheduler.ps1     # 작업 스케줄러 설정 스크립트
└── README.md              # 이 파일
```

## 설치 및 설정

### 1. 필요한 Python 패키지 설치

```bash
pip install requests
```

### 2. 자동 업데이트 설정 (Windows)

1. PowerShell을 관리자 권한으로 실행
2. 프로젝트 폴더로 이동
3. 다음 명령 실행:

```powershell
.\setup_scheduler.ps1
```

이렇게 하면 매주 일요일 오전 9시에 자동으로 YouTube 채널에서 동영상을 가져와서 업데이트합니다.

### 3. 수동 업데이트

```bash
python update_videos.py
```

또는

```bash
run_update.bat
```

## YouTube Data API 사용 (선택사항)

더 안정적인 동영상 수집을 위해 YouTube Data API v3를 사용할 수 있습니다:

1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성
2. YouTube Data API v3 활성화
3. API 키 생성
4. `update_videos.py` 파일의 `API_KEY` 변수에 API 키 입력

## 카테고리 분류 규칙

동영상 제목의 첫 번째 숫자를 기준으로 자동 분류됩니다:

- 1: 목
- 2: 허리
- 3: 어깨
- 4: 팔꿈치
- 5: 손/손목
- 6: 엉덩이/고관절
- 7: 무릎
- 8: 발목/발
- 9: 일반의학

## 배포

이 웹사이트는 정적 파일로 구성되어 있어 GitHub Pages, Netlify, Vercel 등에 쉽게 배포할 수 있습니다.

### GitHub Pages 배포

1. 이 저장소를 GitHub에 업로드
2. Settings > Pages에서 Source를 "Deploy from a branch"로 설정
3. Branch를 "main"으로 설정
4. Save 클릭

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여

버그 리포트나 기능 제안은 GitHub Issues를 통해 해주세요.
