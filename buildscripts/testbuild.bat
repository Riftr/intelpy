pyinstaller intelpy.py -w --onefile --add-data intelpy\resources;resources --noconfirm --icon=intelpy\gui\goodpie2.ico
cd dist
xcopy /I ..\intelpy\resources .\resources\
xcopy /I ..\tests\intelpydebug.bat .
cd..