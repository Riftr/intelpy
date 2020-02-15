#!/bin/bash
pyinstaller app.py --add-data intelpy/resources:resources --noconfirm --hidden-import=pygobject
#--noconsole
#2> build.txt
echo "its done now"