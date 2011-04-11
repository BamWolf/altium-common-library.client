cd src
python setup_csv.py bdist_egg --dist-dir ..\dist
rd build /q /s
rd CSV.egg-info /q /s

cd ..

