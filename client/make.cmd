@echo off
rd /s /q release

cd src

python setup.py py2exe
IF ERRORLEVEL 1 PAUSE

rd /s /q build

cd ..\release

del w9xpopen.exe

md data
md data\xml
md modules
md ui
rem md debug

cd ..

xcopy src\*.ini release\*.ini
xcopy /e src\ui\* release\ui\*
xcopy /e /q src\data\* release\data\*
xcopy src\modules\* release\modules\*

rem pause
