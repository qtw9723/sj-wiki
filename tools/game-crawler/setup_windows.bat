@echo off
rem One-time setup on Windows: self-tests, a real 5-game run, then register a daily 07:30 task.
rem Usage: clone the repo, then double-click this file (or run it from cmd).
set PYTHONIOENCODING=utf-8
cd /d "%~dp0..\.."

set PY=py -3
%PY% --version >nul 2>nul
if errorlevel 1 set PY=python
%PY% --version
if errorlevel 1 goto nopy
where git >nul 2>nul
if errorlevel 1 goto nogit

echo [1/3] self-tests
%PY% tools\game-crawler\crawler.py --self-test
if errorlevel 1 goto fail
%PY% tools\game-crawler\process.py --self-test
if errorlevel 1 goto fail

echo.
echo [2/3] real run: 5 games
%PY% tools\game-crawler\run_daily.py --limit 5
if errorlevel 1 goto fail

echo.
echo [3/3] register daily 07:30 task
schtasks /Create /SC DAILY /ST 07:30 /TN "sj-game-crawler" /TR "\"%~dp0run_daily.bat\"" /F
if errorlevel 1 goto fail

echo.
echo Done. Open raw\games\clean-DATE.md to see the result.
echo Check the task with: schtasks /Query /TN "sj-game-crawler"
pause
exit /b 0

:nopy
echo Python not found (neither "py" nor "python"). Install from https://www.python.org/downloads/ and run again.
pause
exit /b 1

:nogit
echo git not found. Install from https://git-scm.com/download/win and run again.
pause
exit /b 1

:fail
echo.
echo Failed. Copy the error message above and paste it to Claude.
pause
exit /b 1
