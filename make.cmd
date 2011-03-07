cd src
python setup.py py2exe
rd /s /q build
cd ..
del exe\w9xpopen.exe