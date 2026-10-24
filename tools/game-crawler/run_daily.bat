@echo off
rem Daily run for Windows Task Scheduler: pull, crawl, clean, then push raw/games to GitHub.
rem Usage: run_daily.bat [options for run_daily.py], e.g. run_daily.bat --opencritic --limit 30
rem Output is appended to tools\game-crawler\run.log (check it if a run fails).
rem Keep keys out of this file; set RAPIDAPI_KEY as a system environment variable.
set PYTHONIOENCODING=utf-8
cd /d "%~dp0..\.."
set LOG=%~dp0run.log
echo ===== %date% %time% ===== >> "%LOG%"
git pull --rebase --autostash origin main >> "%LOG%" 2>&1
set PY=py -3
%PY% --version >nul 2>nul
if errorlevel 1 set PY=python
%PY% tools\game-crawler\run_daily.py --metacritic --push %* >> "%LOG%" 2>&1
echo exit code %errorlevel% >> "%LOG%"
