#!/bin/bash
pyinstaller Pie.py --add-data pie/resources:resources --noconfirm --hidden-import=pygobject
#--noconsole
#2> build.txt
echo "its done now"