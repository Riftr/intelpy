#!/bin/sh
echo "Running Application"
python /intelpy/intelpy.py 2>&1 | tee ~/.config/IntelPy/flatpak.log