@echo off
rem Windows PC 한 번 설정: 모의 테스트 -> 실제 수집 시험(5개) -> 매일 07:30 작업 등록
rem 사용: 저장소를 클론한 뒤 이 파일을 더블클릭하거나 cmd 에서 실행
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0..\.."

where py >nul 2>nul
if errorlevel 1 goto nopy
where git >nul 2>nul
if errorlevel 1 goto nogit

echo [1/3] 모의 테스트
py -3 tools\game-crawler\crawler.py --self-test
if errorlevel 1 goto fail
py -3 tools\game-crawler\process.py --self-test
if errorlevel 1 goto fail

echo.
echo [2/3] 실제 수집 시험 - 게임 5개
py -3 tools\game-crawler\run_daily.py --limit 5
if errorlevel 1 goto fail

echo.
echo [3/3] 매일 07:30 작업 등록
schtasks /Create /SC DAILY /ST 07:30 /TN "sj-game-crawler" /TR "\"%~dp0run_daily.bat\"" /F
if errorlevel 1 goto fail

echo.
echo 완료. 결과는 raw\games 폴더의 clean-날짜.md 를 보세요.
echo 작업 확인: schtasks /Query /TN "sj-game-crawler"
pause
exit /b 0

:nopy
echo Python 의 py 런처가 없습니다. https://www.python.org/downloads/ 에서 설치 후 다시 실행하세요.
pause
exit /b 1

:nogit
echo git 이 없습니다. https://git-scm.com/download/win 에서 설치 후 다시 실행하세요.
pause
exit /b 1

:fail
echo.
echo 실패했습니다. 위의 오류 메시지를 복사해서 Claude 에게 붙여넣어 주세요.
pause
exit /b 1
