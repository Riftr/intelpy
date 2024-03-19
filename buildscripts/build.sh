#!/bin/bash
mkdir dist
mkdir dist/intelpy
pyinstaller ../IntelPy.py --onefile --add-data ../intelpy/resources:resources --noconfirm --icon=..\intelpy\gui\goodpie2.ico
cp -R ../intelpy/resources dist/intelpy/resources