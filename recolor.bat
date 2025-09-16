@echo off
setlocal

set VENV_DIR=%~dp0.venv

@REM If the venv directory doesn't exist, venv is not installed, create a virtual environment
if not exist "%VENV_DIR%" (
    echo No virtual environment detected
    echo Creating virtual environment in %VENV_DIR%
    echo This might take a second!
    python -m venv "%VENV_DIR%"
    @REM If creation fails, python may not be installed or added to path
    if errorlevel 1 (
        echo Failed to create virtual environment. Please make sure python is installed and added to path.
        exit /b 1
    )
    echo Installing packages...
    call "%VENV_DIR%\Scripts\activate.bat"
    pip install -r "%~dp0requirements.txt" -qqq
    echo Installation complete!
)

call "%~dp0.venv\Scripts\activate.bat"

python "%~dp0recolor.py" %*

deactivate
endlocal