@echo off
call "%~dp0.venv\Scripts\activate.bat"

python "%~dp0recolor.py" %*

deactivate