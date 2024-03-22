#!/bin/bash
rm -rf dist
pyinstaller ../intelpy.py --onefile --add-data "../intelpy/resources/*:resources" --noconfirm --icon=..\intelpy\gui\goodpie2.ico
mkdir -pv dist/resources
cp -R ../intelpy/resources dist/