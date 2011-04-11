@echo off
cd client
python setup.py py2exe
rd /s /q build
cd ..
del dist\w9xpopen.exe