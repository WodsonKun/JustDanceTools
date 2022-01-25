@shift /0
SetLocal EnableDelayedExpansion
$global:ProgressPreference = 'SilentlyContinue'

@echo off
SET version=1.0.0b
TITLE Mainscene Generator (v%version%)
mode con: cols=84 lines=32
color 0D
goto :startScreen


:startScreen
echo.
echo Welcome to Mainscene Generator by WodsonKun (v%version%).
echo Thanks to yunyl and mishok!
echo.
SET /p _UpperCodename="Please enter the codename for the song you would like to convert: "
SET /p CoachCount="Please enter coachCount for the song: "
echo.
CALL :LCase _UpperCodename _LowerCodename
ECHO.%_LowerCodename%


ENDLOCAL
GOTO:EOF


:LCase
:UCase
:: Converts to upper/lower case variable contents
:: Syntax: CALL :UCase _VAR1 _VAR2
:: Syntax: CALL :LCase _VAR1 _VAR2
:: _VAR1 = Variable NAME whose VALUE is to be converted to upper/lower case
:: _VAR2 = NAME of variable to hold the converted value
:: Note: Use variable NAMES in the CALL, not values (pass "by reference")

SET _UCase=A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
SET _LCase=a b c d e f g h i j k l m n o p q r s t u v w x y z
SET _Lib_UCase_Tmp=!%1!
IF /I "%0"==":UCase" SET _Abet=%_UCase%
IF /I "%0"==":LCase" SET _Abet=%_LCase%
FOR %%Z IN (%_Abet%) DO SET _Lib_UCase_Tmp=!_Lib_UCase_Tmp:%%Z=%%Z!
SET %2=%_Lib_UCase_Tmp%

mkdir tmp

echo.
echo Downloading JDNow ZIPs...
echo.
REM set zip urls cuz its ez to do this with bat than node.js
set zip="http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/dist/bundle/%_UpperCodename%.zip"
set zip1="http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/dist/bundle/%_UpperCodename%_1.zip"
set zip2="http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/dist/bundle/%_UpperCodename%_2.zip"
set zip3="http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/dist/bundle/%_UpperCodename%_3.zip"
set zip4="http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/dist/bundle/%_UpperCodename%_4.zip"
set zip5="http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/dist/bundle/%_UpperCodename%_5.zip"
set zip6="http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/dist/bundle/%_UpperCodename%_6.zip"
set zip7="http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/dist/bundle/%_UpperCodename%_7.zip"
set zip8="http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/dist/bundle/%_UpperCodename%_8.zip"
set zip9="http://jdnowweb-s.cdn.ubi.com/uat/release_tu2/20150928_1740/dist/bundle/%_UpperCodename%_9.zip"

curl --fail --silent -# -H "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "%zip%" -o "tmp\%_UpperCodename%.zip"
curl --fail --silent -# -H "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "%zip1%" -o "tmp\%_UpperCodename%_1.zip"
curl --fail --silent -# -H "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "%zip2%" -o "tmp\%_UpperCodename%_2.zip"
curl --fail --silent -# -H "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "%zip3%" -o "tmp\%_UpperCodename%_3.zip"
curl --fail --silent -# -H "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "%zip4%" -o "tmp\%_UpperCodename%_4.zip"
curl --fail --silent -# -H "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "%zip5%" -o "tmp\%_UpperCodename%_5.zip"
curl --fail --silent -# -H "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "%zip6%" -o "tmp\%_UpperCodename%_6.zip"
curl --fail --silent -# -H "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "%zip7%" -o "tmp\%_UpperCodename%_7.zip"
curl --fail --silent -# -H "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "%zip8%" -o "tmp\%_UpperCodename%_8.zip"
curl --fail --silent -# -H "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "%zip9%" -o "tmp\%_UpperCodename%_9.zip"

echo.
echo Extracting JDNow ZIPs...
echo.

if exist tmp\%_UpperCodename%_9.zip (
powershell Expand-Archive tmp\%_UpperCodename%_9.zip -DestinationPath tmp\%_UpperCodename%
del tmp\*.zip
)

if exist tmp\%_UpperCodename%_8.zip (
powershell  Expand-Archive tmp\%_UpperCodename%_8.zip -DestinationPath tmp\%_UpperCodename%
del tmp\*.zip
)

if exist tmp\%_UpperCodename%_7.zip (
powershell  Expand-Archive tmp\%_UpperCodename%_7.zip -DestinationPath tmp\%_UpperCodename%
del tmp\*.zip
)

if exist tmp\%_UpperCodename%_6.zip (
powershell  Expand-Archive tmp\%_UpperCodename%_6.zip -DestinationPath tmp\%_UpperCodename%
del tmp\*.zip
)

if exist tmp\%_UpperCodename%_5.zip (
powershell  Expand-Archive tmp\%_UpperCodename%_5.zip -DestinationPath tmp\%_UpperCodename%
del tmp\*.zip
)

if exist tmp\%_UpperCodename%_4.zip (
powershell  Expand-Archive tmp\%_UpperCodename%_4.zip -DestinationPath tmp\%_UpperCodename%
del tmp\*.zip
)

if exist tmp\%_UpperCodename%_3.zip (
powershell  Expand-Archive tmp\%_UpperCodename%_3.zip -DestinationPath tmp\%_UpperCodename%
del tmp\*.zip
)

if exist tmp\%_UpperCodename%_2.zip (
powershell  Expand-Archive tmp\%_UpperCodename%_2.zip -DestinationPath tmp\%_UpperCodename%
del tmp\*.zip
)

if exist tmp\%_UpperCodename%_1.zip (
powershell  Expand-Archive tmp\%_UpperCodename%_1.zip -DestinationPath tmp\%_UpperCodename%
del tmp\*.zip
)

if exist tmp\%_UpperCodename%.zip (
powershell  Expand-Archive tmp\%_UpperCodename%.zip -DestinationPath tmp\%_UpperCodename%
del tmp\*.zip
)

del tmp\*.zip 2>NUL

REM download song data
node downloadDataUtility.js %_UpperCodename% %CoachCount%
REM run j2d
echo.
echo Running JSON to DTAPE

mkdir input\%_UpperCodename%\
py bin\j2d\main.py "%_UpperCodename%"
REM move dtape ktape and musictrack to mainscene creators folder
@RD /s /q "output" 2>NUL
REM copypaste placeholder textures !
xcopy /s bin\textures input\%_UpperCodename%\textures\ /Y|rem
REM rename textures to the right codename
echo.
node texturesRenameUtility.js %_UpperCodename% %CoachCount%

REM pictos
echo.
echo Preparing pictos...
echo.
mkdir bin\pictos\%_UpperCodename%\pictos\dds
mkdir bin\pictos\%_UpperCodename%\pictos\ckd

python bin\pictocutter\pictocutter.py %_UpperCodename%

node pictoControllerUtility.js %_UpperCodename%
node pictoControllerUtility_alt.js %_UpperCodename%

robocopy bin\pictos\%_UpperCodename%\pictos\ckd\ input\%_UpperCodename%\pictos /MOVE /NFL /NDL /NJH /NJS /nc /ns /np 2>NUL

@RD /s /q "bin\pictos" 2>NUL
@RD /s /q "picto_input" 2>NUL
@RD /s /q "picto_output" 2>NUL


echo Moving msm (movespace) files...
echo.
REM move movespace files
robocopy tmp\%_UpperCodename%\classifiers input\%_UpperCodename%\moves /MOVE  /NFL /NDL /NJH /NJS /nc /ns /np 2>NUL|rem
@RD /s /q "tmp" 2>NUL

echo.
REM generate songdesc !!!
node generateSongDescUtility.js %_UpperCodename% %CoachCount%
goto :webmScreen

:webmScreen
echo.
echo Please put your webM file inside input\%_UpperCodename%\ folder
echo Type "later" if you want to put webm later
SET /p responsewebm="or type "done" when you're done: "
IF "%responsewebm%"=="done" (
	goto :audioScreen
)
IF "%responsewebm%"=="later" (
	goto :audioScreen
) ELSE (
echo "You should have typed done or later. Re-do the whole process."
pause
)

:audioScreen
echo.
echo.
echo Please put your audio file in ".wav.ckd" format inside input\%_UpperCodename%\ folder
echo Type "later" if you want to put audio later
SET /p responsewav="or type "done" when you're done: "
IF "%responsewav%"=="done" (
	goto :startMainScene
)
IF "%responsewav%"=="later" (
	goto :startMainScene
) ELSE (
echo "You should have typed done or later. Re-do the whole process."
pause
)

:startMainScene
echo.
echo.
SET /p platform="Enter your platform (pc, wiiu, orbis, nx... (not wii)): "
node customMainscene.js %_UpperCodename% %CoachCount% %platform%|rem
goto :packIPK

:packIPK
echo.
echo.
SET /p packIpkR="Would you like to pack the IPK? (y\n): "
IF "%packIpkR%"=="y" (
	goto :packingIPKaccepted
) 
IF "%packIpkR%"=="n" (
	goto :finishedPage
) 
ELSE (
echo "You should have typed y or n. Re-do the whole process."
pause
)

:packingIPKaccepted
echo.
mkdir output_IPK
node generateIPKUtility.js %_UpperCodename%
goto :finishedPage

:finishedPage
del bin\j2d\input\input.json
del bin\j2d\input\inputmoves.json
del bin\j2d\input\inputmovesp2.json
del bin\j2d\input\inputmovesp3.json
del bin\j2d\input\inputmovesp4.json
echo.
echo.
echo Congratulations! You have created a mainscene IPK for %_UpperCodename%
echo Please contact me on Discord if you have any kind of issue with this tool!
echo WodsonKun#5972
echo.
echo.
pause
