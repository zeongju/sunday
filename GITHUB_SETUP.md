# GitHub 업로드 가이드

## 1. GitHub 저장소 생성

1. [GitHub.com](https://github.com)에 로그인
2. 우측 상단의 "+" 버튼 클릭 → "New repository" 선택
3. 저장소 설정:
   - **Repository name**: `hwata-hospital` (또는 원하는 이름)
   - **Description**: `화타의 진료실 - 예산 종합 병원 웹사이트`
   - **Visibility**: Public (또는 Private)
   - **Initialize this repository with**: 체크하지 않음
4. "Create repository" 클릭

## 2. Git 설치 (아직 설치하지 않은 경우)

1. [Git for Windows](https://git-scm.com/download/win)에서 Git 다운로드
2. 설치 시 기본 설정 사용 (Next 클릭)
3. 설치 완료 후 PowerShell 재시작

## 3. Git 초기화 및 파일 업로드

### PowerShell에서 실행 (관리자 권한으로 실행)

```powershell
# 프로젝트 폴더로 이동
cd "C:\Users\USER\Desktop\화타홈페이지"

# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 번째 커밋
git commit -m "Initial commit: 화타의 진료실 웹사이트"

# main 브랜치로 변경
git branch -M main

# 원격 저장소 추가 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/hwata-hospital.git

# GitHub에 업로드
git push -u origin main
```

## 4. GitHub Pages 설정 (선택사항)

웹사이트를 무료로 호스팅하려면:

1. GitHub 저장소 페이지에서 "Settings" 탭 클릭
2. 왼쪽 메뉴에서 "Pages" 클릭
3. "Source" 섹션에서:
   - "Deploy from a branch" 선택
   - "Branch"를 "main"으로 설정
   - "Folder"를 "/ (root)"로 설정
4. "Save" 클릭

## 5. 자동 업데이트 설정

### Python 설치 (아직 설치하지 않은 경우)

1. [Python.org](https://www.python.org/downloads/)에서 Python 다운로드
2. 설치 시 "Add Python to PATH" 체크
3. 설치 완료 후 PowerShell 재시작

### 필요한 패키지 설치

```powershell
pip install requests
```

### 자동 업데이트 스케줄러 설정

```powershell
# PowerShell을 관리자 권한으로 실행
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_scheduler.ps1
```

## 6. 파일 구조 확인

업로드될 파일들:

```
화타홈페이지/
├── index.html              # 메인 웹페이지
├── manifest.json           # PWA 매니페스트
├── update_videos.py        # YouTube 동영상 자동 업데이트 스크립트
├── run_update.bat          # Windows 배치 파일
├── setup_scheduler.ps1     # 작업 스케줄러 설정 스크립트
├── requirements.txt         # Python 패키지 목록
├── README.md              # 프로젝트 설명서
├── .gitignore             # Git 제외 파일 목록
└── GITHUB_SETUP.md        # 이 파일
```

## 7. 업데이트 확인

### 수동 업데이트 테스트

```powershell
python update_videos.py
```

### 로그 확인

```powershell
Get-Content update_log.txt
```

## 8. 문제 해결

### Git 인증 문제

GitHub에서 Personal Access Token을 사용해야 할 수 있습니다:

1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token" 클릭
3. 필요한 권한 선택 (repo, workflow)
4. 토큰을 안전한 곳에 저장

### Python 경로 문제

```powershell
# Python 경로 확인
where python
where py

# 환경 변수 확인
$env:PATH
```

## 9. 추가 설정 (선택사항)

### YouTube Data API 사용

더 안정적인 동영상 수집을 위해:

1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성
2. YouTube Data API v3 활성화
3. API 키 생성
4. `update_videos.py`의 `API_KEY` 변수에 키 입력

### 커스텀 도메인 설정

GitHub Pages에서 커스텀 도메인을 사용하려면:

1. 도메인 구매
2. DNS 설정에서 CNAME 레코드 추가
3. GitHub 저장소 Settings → Pages에서 Custom domain 설정

## 완료!

이제 매주 일요일 오전 9시에 자동으로 YouTube 채널에서 새 동영상을 확인하고 업데이트합니다.
