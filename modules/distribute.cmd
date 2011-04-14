@echo off
copy dist\*.egg ..\client\src\modules
if ERRORLEVEL 1 pause