@echo off
cd /d "%~dp0"
echo YouTube 동영상 업데이트 시작...
python update_videos.py
echo 업데이트 완료!
pause 