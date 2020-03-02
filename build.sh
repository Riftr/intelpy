#!/bin/bash
#/home/robert/PycharmProjects/intelpy/venv/bin/python -m pyinstaller IntelPy.py --add-data intelpy/resources:resources --noconfirm --hidden-import=pygobject
pyinstaller IntelPy.py --onefile --add-data intelpy/resources:intelpy/resources --noconfirm
cp -R intelpy/resources dist/resources