set PYTHONPATH=%CD%
venv\Scripts\pytest.exe --rootdir="." -s test_pyshipupdate
set PYTHONPATH=
