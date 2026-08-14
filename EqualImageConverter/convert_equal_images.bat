@echo off
REM Run the Python script to create equal-size images (fit/pad and crop)

REM Change directory to where the batch file is located
cd /d "%~dp0"

REM Check if Python is installed and available
python --version >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not added to PATH. Please install Python and try again.
    pause
    exit /b
)

REM Run the Python script
python convert_equal_images.py

REM Wait for the user to press a key before closing the window
pause
