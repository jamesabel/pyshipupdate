pushd .
cd ..
REM can run into this bug
REM https://github.com/psf/black#ignoring-unmodified-files
venv\Scripts\black.exe -l 192 pyshipupdate test_pyshipupdate *.py
popd
