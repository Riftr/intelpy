#!/bin/bash

echo "** Validating .desktop **"
desktop-file-validate io.github.riftr.intelpy.desktop
echo "✔ if no output = validated"

echo "** Validating Metainfo **"
flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream io.github.riftr.intelpy.metainfo.xml

echo "** Building Flatpak **"
#flatpak-builder --force-clean build-dir /../../io.github.riftr.intelpy.yml
flatpak run org.flatpak.Builder --force-clean --sandbox --user --install --install-deps-from=flathub --ccache --mirror-screenshots-url=https://dl.flathub.org/media/ --repo=repo build-dir ../../io.github.riftr.intelpy.yml


echo "** Running Flatpak **"
#set QT_DEBUG_PLUGINS = 1
#flatpak-builder --run build-dir ../../io.github.riftr.intelpy.yml run.sh
flatpak run io.github.riftr.intelpy &
