@echo off
REM Hospital Management System - Quick Start Script
REM Double-click this file to start the Flask server

echo Starting Hospital Management System...
echo.
echo Make sure your .env file contains GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
echo.

REM Activate virtual environment and run
call venv\Scripts\activate.bat

REM Start Flask (reads from .env automatically)
python run.py

pause
