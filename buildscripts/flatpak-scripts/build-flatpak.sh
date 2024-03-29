#!/bin/bash

echo "** Building Flatpak **"
flatpak-builder --force-clean build-dir ./io.github.riftr.intelpy.yml

echo "** Running Flatpak **"
flatpak-builder --run build-dir ./io.github.riftr.intelpy.yml run.sh