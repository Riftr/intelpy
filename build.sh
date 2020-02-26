#!/bin/bash
/home/robert/PycharmProjects/intelpy/venv/bin/python -m pyinstaller IntelPy.py --add-data intelpy/resources:resources --noconfirm --hidden-import=pygobject
#--noconsole
#2> build.txt
echo "its done now"
