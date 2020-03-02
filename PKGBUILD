# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# See http://wiki.archlinux.org/index.php/Python_Package_Guidelines for more
# information on Python packaging.

# Maintainer: Rob <robert@nospampls.com>
pkgname=intelpy
pkgver=1.0b
pkgrel=1
pkgdesc="Chat log monitor for the game Eve Online"
arch=('any')
url="https://github.com/Riifta/intelpy"
license=('GPL3')
groups=()
depends=('python3' 'python-pyqt5' 'python-pathlib' 'python-watchdog' 'python-networkx' 'python-pathlib2' 'python-gobject')
#'python-playsound')
makedepends=()
provides=('intelpy')
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
install=
source=(${pkgname}-${pkgver}.tar.gz::https://github.com/Riifta/intelpy/archive/${pkgver}.tar.gz')
md5sums=()

package() {
  cd "$srcdir/$pkgname-$pkgver"

  ln -s /usr/bin/${pkgname} ${pkgdir}/usr/bin/IntelPy.py
  install -D -m644 LICENSE ${pkgdir}/usr/share/licenses/${pkgname}/LICENSE
  install -D -m644 README.md ${pkgdir}/usr/share/doc/${pkgname}/README.md
  install -D -m644 COPYRIGHT.md ${pkgdir}/usr/share/doc/${pkgname}/COPYRIGHT.md
}

