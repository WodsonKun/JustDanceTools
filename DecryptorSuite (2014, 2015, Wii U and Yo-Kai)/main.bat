@shift /0
SetLocal EnableDelayedExpansion

@echo off
TITLE Just Dance Decryptor Suite (v1.0.0)
mode con: cols=84 lines=32
color 0D
set outputdir=%cd%\output
cd ./bin
goto :DecryptorMain

:::::::::::::::::::::::::::::::::::::::::::::::::::::::: MENU ::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:DecryptorMain
cd ./bin
color 0F
cls
echo.
echo   Welcome to Just Dance Decryptor Suite!
echo   Credits to WodsonKun and augustodoidin
echo   Works with Just Dance 2014, Just Dance 2015
echo   Just Dance Wii U and Just Dance Yo-Kai Watch
echo.
echo     [1] Decrypt Just Dance 2014 / Wii U / Yo-Kai's timeline
echo     [2] Decrypt Just Dance 2014 / Wii U / Yo-Kai's musictrack
echo     [3] Decrypt Just Dance 2014's songdesc
echo     [4] Decrypt Just Dance 2015's DTAPE
echo     [5] Decrypt Just Dance 2015's KTAPE
echo     [6] Decrypt Just Dance 2015's musictrack
echo     [7] Decrypt Just Dance 2015's songdesc
echo.
echo [8] Exit
echo.
set /p opt=Type option and press Enter: 


:::::::::::::::::::::::::::::::::::::::::::::::::::::::: Codename ::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if "%opt%"=="1" (
cls
echo.
echo Please, type the codename of the song: 
set /p _codename=
goto :TMLDec
)
if "%opt%"=="2" (
cls
echo.
echo Please, type the codename of the song: 
set /p _codename=
goto :MTDec
)
if "%opt%"=="3" (
cls
echo.
echo Please, type the codename of the song: 
set /p _codename=
goto :SDDec
)
if "%opt%"=="4" (
cls
echo.
echo Please, type the codename of the song: 
set /p _codename=
goto :DTAPEDec
)
if "%opt%"=="5" (
cls
echo.
echo Please, type the codename of the song: 
set /p _codename=
goto :KTAPEDec
)
if "%opt%"=="6" (
cls
echo.
echo Please, type the codename of the song: 
set /p _codename=
goto :MT15Dec
)
if "%opt%"=="7" (
cls
echo.
echo Please, type the codename of the song: 
set /p _codename=
goto :SD15Dec
)

:::::::::::::::::::::::::::::::::::::::::::::::::::::::: Just Dance 2014 / Wii U / Yo-Kai Watch! ::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Timeline
:TMLDec
echo off
cls
echo.
mkdir "%outputdir%\%_codename%"
py dec_jd14_tml.py "%_codename%" "%outputdir%"
goto :DecryptorMain

:: Musictrack
:MTDec
echo off
cls
echo.
mkdir "%outputdir%\%_codename%"
py dec_jd14_mt.py "%_codename%" "%outputdir%"
goto :DecryptorMain

:: Songdesc
:SDDec
echo off
cls
echo.
mkdir "%outputdir%\%_codename%"
py dec_jd14_sd.py "%_codename%" "%outputdir%"
pause
goto :DecryptorMain

:::::::::::::::::::::::::::::::::::::::::::::::::::::::: Just Dance 2015 ::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: DTAPE
:DTAPEDec
echo off
cls
echo.
mkdir "%outputdir%\%_codename%"
py dec_jd15_dtape.py "%_codename%" "%outputdir%"
goto :DecryptorMain

:: KTAPE
:KTAPEDec
echo off
cls
echo.
mkdir "%outputdir%\%_codename%"
py dec_jd15_ktape.py "%_codename%" "%outputdir%"
goto :DecryptorMain

:: Musictrack
:MT15Dec
echo off
cls
echo.
mkdir "%outputdir%\%_codename%"
py dec_jd15_mt.py "%_codename%" "%outputdir%"
goto :DecryptorMain

:: Songdesc
:SD15Dec
echo off
cls
echo.
mkdir "%outputdir%\%_codename%"
py dec_jd15_sd.py "%_codename%" "%outputdir%"
goto :DecryptorMain

pause