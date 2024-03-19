pyinstaller ..\IntelPy.py --noconsole --onefile --add-data ..\intelpy\resources;intelpy\resources --noconfirm --icon=..\intelpy\gui\goodpie2.ico
mkdir ..\dist
cd ..\dist
mkdir intelpy
xcopy /I ..\intelpy\resources .\intelpy\resources\
cd..