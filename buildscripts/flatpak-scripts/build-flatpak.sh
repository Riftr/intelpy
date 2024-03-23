#!/bin/bash
# https://docs.flatpak.org/en/latest/first-build.html
echo "*** Compiling with Pyinstaller ***"
#./build.sh   #commented out so we don't rebuild while testing this script

echo "*** Building Flatpak ***"
flatpak-builder --force-clean --user build-dir io.github.riftr.intelpy.yml
#flatpak run org.flatpak.Builder --force-clean --sandbox --user --install --install-deps-from=flathub --ccache --mirror-screenshots-url=https://dl.flathub.org/media/ --repo=repo builddir io.github.riftr.intelpy.yml

#echo "*** Testing Flatpak ***"
#flatpak-builder --user --install --force-clean build-dir io.github.riftr.intelpy.yml
#flatpak run io.github.riftr.intelpy

#echo "*** Sending flatpak to Flathub repo ***"
# todo