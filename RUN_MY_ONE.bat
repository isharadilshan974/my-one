@echo off
setlocal
title MY ONE - FINAL
cd /d "%~dp0"
echo.
echo ==========================================
echo       MY ONE - LIFE OPERATING SYSTEM
echo ==========================================
echo.
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10+ first.
  pause
  exit /b 1
)
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Could not install the required package.
  pause
  exit /b 1
)
echo.
echo Starting MY ONE...
python -m streamlit run app.py
pause
