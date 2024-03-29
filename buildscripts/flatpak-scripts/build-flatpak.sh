#!/bin/bash

echo "** Building Flatpak **"
flatpak-builder --force-clean build-dir ./io.github.riftr.intelpy.yml

echo "** Running Flatpak **"
set QT_DEBUG_PLUGINS = 1
flatpak-builder --run build-dir ./io.github.riftr.intelpy.yml run.sh