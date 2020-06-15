pyinstaller IntelPy.py --onefile --add-data intelpy\resources;intelpy\resources --noconfirm --icon=intelpy\gui\goodpie2.ico
cd dist
mkdir intelpy
xcopy /I ..\intelpy\resources .\intelpy\resources\
xcopy /I ..\tests\intelpydebug.bat .\intelpy\
cd..