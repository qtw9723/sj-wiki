@echo off
rem 매일 아침 실행용 (Windows 작업 스케줄러에서 호출). 저장소 루트 기준으로 동작한다.
rem 사용: run_daily.bat [run_daily.py 옵션...]   예) run_daily.bat --opencritic --limit 30
rem 키는 이 파일에 쓰지 말고 시스템 환경변수 RAPIDAPI_KEY 로 설정할 것.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0..\.."
git pull --rebase --autostash origin main
py -3 tools\game-crawler\run_daily.py --metacritic %*
