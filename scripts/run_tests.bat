@echo off
:: run_tests.bat — run the pytest suite from the project root on Windows

cd /d "%~dp0.."

call .venv\Scripts\activate.bat

echo.
echo Running test suite...
echo.

pytest tests\ -v

echo.
pause
