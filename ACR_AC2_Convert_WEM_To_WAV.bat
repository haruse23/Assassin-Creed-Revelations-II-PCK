@echo off
REM Loop over all dragged WEM files
for %%F in (%*) do (
    echo Converting "%%~F" ...
    
    REM Create Converted folder next to the WEM file
    if not exist "%%~dpFConverted" mkdir "%%~dpFConverted"
    
    REM Call vgmstream-cli.exe inside the vgmstream folder
    "%~dp0vgmstream-win\vgmstream-cli.exe" -o "%%~dpFConverted\%%~nF.wav" "%%~F"
)

pause
