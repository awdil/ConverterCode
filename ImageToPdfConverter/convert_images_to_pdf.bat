@echo off
REM Run the Python script to convert sequenced images into a PDF

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
python convert_images_to_pdf.py

REM Wait for the user to press a key before closing the window
pause
