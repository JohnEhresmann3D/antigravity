@echo off
REM Performance Dashboard Launcher
REM Quick launcher for the Antigravity Performance Dashboard

echo ============================================================
echo Starting Performance Dashboard...
echo ============================================================
echo.
echo Dashboard will be available at: http://localhost:8080
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
python tools\dashboard\performance_dashboard.py

pause
