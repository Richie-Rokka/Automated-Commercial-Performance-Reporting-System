
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
    echo PIPELINE FAILED - PAD WILL NOT RUN
    echo ============================================================
    exit /b 1
)

echo.
echo ============================================================
echo PYTHON PIPELINE COMPLETED SUCCESSFULLY
echo LAUNCHING POWER AUTOMATE DESKTOP
echo ============================================================

start "" "ms-powerautomate:/console/flow/run?environmentid=one-drive-environment-Id&workflowid=8a145cde-78fe-4442-b239-c5faeba343aa&source=Other"

exit /b 0