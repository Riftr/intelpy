#!/bin/bash

python - <<'PY'
import sys
import PyInstaller

major = int(PyInstaller.__version__.split('.', 1)[0])
if major < 6:
	raise SystemExit(
		f"PyInstaller >= 6.0.0 is required (found {PyInstaller.__version__}). "
		"Install build deps from buildscripts/requirements-build.txt."
	)
PY

rm -rf dist
python -m PyInstaller ../intelpy.py --onefile --add-data "../intelpy/resources/*:resources" --noconfirm --icon=..\intelpy\gui\goodpie2.ico
mkdir -pv dist/resources
cp -R ../intelpy/resources dist/