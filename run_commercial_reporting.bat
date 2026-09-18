@echo off
setlocal

cd /d "%~dp0"

echo ============================================================
echo AUTOMATED COMMERCIAL PERFORMANCE REPORTING SYSTEM
echo ============================================================
echo.

".venv\Scripts\python.exe" -m src.run_commercial_reporting

if errorlevel 1 (
    echo.
    echo ============================================================
    echo PIPELINE FAILED
    echo ============================================================
    exit /b 1
)

echo.
echo ============================================================
echo PIPELINE COMPLETED SUCCESSFULLY
echo ============================================================
exit /b 0
