rd release /q /s

cd src
python setup_csv.py bdist_egg --dist-dir ..\release
IF ERRORLEVEL 1 pause

python setup_msaccess.py bdist_egg --dist-dir ..\release
IF ERRORLEVEL 1 pause

rd build /q /s
rd CSV.egg-info /q /s
rd MSACCESS.egg-info /q /s

cd ..

rem pause
