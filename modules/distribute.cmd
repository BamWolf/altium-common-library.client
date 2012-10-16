@echo off
copy release\*.egg ..\client\src\modules
if ERRORLEVEL 1 pause