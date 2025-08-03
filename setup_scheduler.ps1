# Windows 작업 스케줄러에 일요일마다 YouTube 동영상 업데이트 작업 등록
# 관리자 권한으로 실행해야 합니다.

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$batchFile = Join-Path $scriptPath "run_update.bat"

# 작업 이름
$taskName = "YouTube_Video_Update"

# 작업 설명
$taskDescription = "일요일마다 예산화타 YouTube 채널에서 동영상을 가져와서 홈페이지를 업데이트합니다."

# 작업 스케줄러에 등록
$action = New-ScheduledTaskAction -Execute $batchFile -WorkingDirectory $scriptPath
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 9AM

# 작업 설정
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# 작업 등록
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description $taskDescription -Force

Write-Host "작업 스케줄러에 등록되었습니다!"
Write-Host "작업 이름: $taskName"
Write-Host "실행 시간: 매주 일요일 오전 9시"
Write-Host "실행 파일: $batchFile"

# 작업 상태 확인
Get-ScheduledTask -TaskName $taskName | Select-Object TaskName, State, LastRunTime, NextRunTime 