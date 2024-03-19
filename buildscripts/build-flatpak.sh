#!/bin/bash
# https://docs.flatpak.org/en/latest/first-build.html
rm -rf flatpak/
echo "Compiling with Pyinstaller"
#./build.sh
echo "Building Flatpak"
mkdir -p flatpak/intelpy/resources
#cp ../intelpy/resources/* flatpak/intelpy/resources
cp -R dist/* flatpak/
cp org.flatpak.IntelPy.yml flatpak/
cd flatpak
flatpak-builder build-dir org.flatpak.IntelPy.yml

echo "Testing Flatpak"
flatpak-builder --user --install --force-clean build-dir org.flatpak.IntelPy.yml
#flatpak run org.flatpak.IntelPy
cd ..