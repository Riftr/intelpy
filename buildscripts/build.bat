pyinstaller ..\intelpy.py --noconsole --onefile --add-data ..\intelpy\resources;resources --noconfirm --icon=..\intelpy\gui\goodpie2.ico
xcopy /I ..\intelpy\resources .\dist\resources\