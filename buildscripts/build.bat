pyinstaller ..\intelpy.py --noconsole --onefile --add-data ..\intelpy\resources;resources --noconfirm --icon=..\intelpy\gui\goodpie2.ico
mkdir ..\dist
cd ..\dist
xcopy /I ..\intelpy\resources .\resources\
cd..