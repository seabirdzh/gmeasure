#!/bin/sh

# v1.0 - 2013.5.27
# project inited.

if [ -d 'fakeroot' ]; then
	rm -rvf fakeroot
fi

PYLIB='fakeroot/usr/lib/python3/dist-packages/'
APP='gmeasure'

mkdir -vp fakeroot/usr/bin fakeroot/DEBIAN $PYLIB

cp -v ../${APP}.py fakeroot/usr/bin/$APP
cp -rvf ../$APP $PYLIB/
rm -rvf $PYLIB/$APP/__pycache__
mv -vf $PYLIB/$APP/Config.py.build $PYLIB/$APP/Config.py
cp -rvf ../share fakeroot/usr/share
cp -vf control fakeroot/DEBIAN/
