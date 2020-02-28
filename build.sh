#!/bin/bash
#/home/robert/PycharmProjects/intelpy/venv/bin/python -m pyinstaller IntelPy.py --add-data intelpy/resources:resources --noconfirm --hidden-import=pygobject
pyinstaller IntelPy.py --add-data intelpy/resources:intelpy/resources --noconfirm