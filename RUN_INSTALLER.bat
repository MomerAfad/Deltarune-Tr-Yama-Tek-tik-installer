@echo off
echo Deltarune Turkce Yama Kurulum Araci Baslatiliyor...
echo.
python installer.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Python bulunamadi! Lutfen Python 3.6+ yukleyin.
    echo https://www.python.org/downloads/
    pause
)
