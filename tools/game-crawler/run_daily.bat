@echo off
rem Daily run for Windows Task Scheduler: pull, then crawl + clean.
rem Usage: run_daily.bat [options for run_daily.py], e.g. run_daily.bat --opencritic --limit 30
rem Keep keys out of this file; set RAPIDAPI_KEY as a system environment variable.
set PYTHONIOENCODING=utf-8
cd /d "%~dp0..\.."
git pull --rebase --autostash origin main
set PY=py -3
%PY% --version >nul 2>nul
if errorlevel 1 set PY=python
%PY% tools\game-crawler\run_daily.py --metacritic %*
