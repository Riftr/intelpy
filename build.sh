#!/bin/bash
pyinstaller IntelPy.py --add-data intelpy/resources:resources --noconfirm --hidden-import=pygobject
#--noconsole
#2> build.txt
echo "its done now"