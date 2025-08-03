@echo off
echo GitHub 업로드 시작...
echo.

echo 1. Git 초기화...
git init

echo 2. 파일 추가...
git add .

echo 3. 커밋 생성...
git commit -m "Initial commit: 화타의 진료실 웹사이트"

echo 4. main 브랜치로 변경...
git branch -M main

echo.
echo 5. 원격 저장소 설정...
echo GitHub 저장소 URL을 입력하세요 (예: https://github.com/username/hwata-hospital.git)
set /p repo_url="저장소 URL: "

echo 6. 원격 저장소 추가...
git remote add origin %repo_url%

echo 7. GitHub에 업로드...
git push -u origin main

echo.
echo 업로드 완료!
echo GitHub 저장소를 확인해보세요.
pause 