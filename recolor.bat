@echo off
setlocal

set VENV_DIR=%~dp0.venv

if not exist "%VENV_DIR%" (
    echo No virtual environment detected
    echo Creating virtual environment in %VENV_DIR%
    echo This might take a second!
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment. Please make sure python is installed and added to path.
        exit /b 1
    )
    echo Installing packages...
    call "%VENV_DIR%\Scripts\activate.bat"
    pip install -r "%~dp0requirements.txt" -qqq
)

call "%~dp0.venv\Scripts\activate.bat"

python "%~dp0recolor.py" %*

deactivate
endlocal