#!/bin/bash

echo "*** Testing Flatpak Manifest***"
flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream io.github.riftr.intelpy.metainfo.xml


echo "*** Building Flatpak ***"
#flatpak-builder --force-clean --user build-dir io.github.riftr.intelpy.yml
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak run org.flatpak.Builder --force-clean --sandbox --user --install --install-deps-from=flathub --ccache --mirror-screenshots-url=https://dl.flathub.org/media/ --repo=repo builddir io.github.riftr.intelpy.yml

echo "*** Testing Flatpak **"
#flatpak-builder --user --install --force-clean build-dir io.github.riftr.intelpy.yml
#flatpak run io.github.riftr.intelpy

#echo "*** Sending flatpak to Flathub repo ***"
# todo