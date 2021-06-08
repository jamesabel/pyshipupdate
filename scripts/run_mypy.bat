pushd .
cd ..
call venv\Scripts\activate.bat 
mypy -m pyshipupdate
call deactivate
popd
