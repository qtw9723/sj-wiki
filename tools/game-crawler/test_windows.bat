@echo off
rem Test only (no scheduled task): self-tests + a real 5-game run. Writes tools\game-crawler\test_result.txt
setlocal
set PYTHONIOENCODING=utf-8
set OUT=%~dp0test_result.txt
cd /d "%~dp0..\.."
echo start %date% %time% > "%OUT%"
echo repo root: %CD% >> "%OUT%"

set PY=py -3
%PY% --version >nul 2>nul
if errorlevel 1 set PY=python
%PY% --version >> "%OUT%" 2>&1
if errorlevel 1 goto nopython

echo ===== self-test: crawler ===== >> "%OUT%"
%PY% tools\game-crawler\crawler.py --self-test >> "%OUT%" 2>&1
echo ===== self-test: process ===== >> "%OUT%"
%PY% tools\game-crawler\process.py --self-test >> "%OUT%" 2>&1

echo ===== real run: 5 games ===== >> "%OUT%"
%PY% tools\game-crawler\crawler.py --source steamspy-top --limit 5 >> "%OUT%" 2>&1
echo ===== process ===== >> "%OUT%"
%PY% tools\game-crawler\process.py >> "%OUT%" 2>&1
echo ===== files ===== >> "%OUT%"
dir /b raw\games >> "%OUT%" 2>&1
echo ===== DONE %date% %time% ===== >> "%OUT%"
goto end

:nopython
echo NO PYTHON FOUND (neither py nor python works) >> "%OUT%"

:end
echo Finished. See tools\game-crawler\test_result.txt
pause
