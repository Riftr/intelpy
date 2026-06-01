python -c "import PyInstaller,sys; sys.exit(0 if int(PyInstaller.__version__.split('.',1)[0]) >= 6 else 1)"
if errorlevel 1 (
  echo PyInstaller ^>= 6.0.0 is required. Install buildscripts\requirements-build.txt first.
  exit /b 1
)

python -m PyInstaller ..\intelpy.py --noconsole --onefile --add-data ..\intelpy\resources;resources --noconfirm --icon=..\intelpy\gui\goodpie2.ico
xcopy /I ..\intelpy\resources .\dist\resources\