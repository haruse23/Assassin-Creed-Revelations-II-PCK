@echo off
for %%F in (%*) do (
    python "%~dp0ACR_Extract_PCK.py" "%%~F"
)
pause
