#!/bin/bash
pyinstaller IntelPy.py --onefile --add-data intelpy/resources:intelpy/resources --noconfirm --icon=intelpy\gui\goodpie2.ico
mkdir dist/intelpy
cp -R intelpy/resources dist/intelpy/