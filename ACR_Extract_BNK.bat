@echo off
for %%F in (%*) do (
    python "%~dp0ACR_Extract_BNK.py" "%%~F"
)
pause
