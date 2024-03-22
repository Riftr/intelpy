#!/bin/bash
# https://docs.flatpak.org/en/latest/first-build.html
echo "*** Compiling with Pyinstaller ***"
#./build.sh   #commented out so we don't rebuild while testing this script

echo "*** Building Flatpak ***"
flatpak-builder build-dir io.github.riftr.intelpy.yml

echo "*** Testing Flatpak ***"
flatpak-builder --user --install --force-clean build-dir io.github.riftr.intelpy.yml
flatpak run io.github.riftr.intelpy

#echo "*** Sending flatpak to Flathub repo ***"
# todo