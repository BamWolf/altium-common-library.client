@echo off
rd /s /q dist

cd src

python setup.py py2exe
rd /s /q build

cd ..\dist

del w9xpopen.exe

rem md data
rem md debug
md modules
md ui

cd ..

copy src\*.ini dist\*.ini
copy src\ui\*.* dist\ui\*.*
copy src\modules\*.* dist\modules\*.*
