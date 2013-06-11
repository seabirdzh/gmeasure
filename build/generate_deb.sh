#!/bin/sh

# Generate deb package from source.
# v1.5 - 2013.6.12
# Fix the test() command error.
# v1.4 - 2013.6.11
# Simplify the operations.
# v1.3 - 2013.6.7
# Add chown operate.
# Change the usage, now no need to input fakeroot and package name, making
#  it easier to use.
# v1.2 - 2013.5.12
# A second parameter added;
# usage() added;
# v1.1 - 2013.4.29
# Change permissions in DEBIAN/
# v1.0 -2013.4.15
# project inited.

usage() {
	echo "$0"
	echo 'This program need root permission'
}


DIR="fakeroot/"
DEB="gmeasure.deb"
if [ ! -d $DIR ]; then
	echo 'Error: no such directory!!!'
	usage
	exit 1
fi

cd $DIR
chown -R root:root .
find usr -type f | xargs chmod a+r
find usr -type d | xargs chmod a+rx
echo 'Permissions of files and folders in usr/ updated..'
find usr/bin -type f | xargs chmod a+x
echo 'All files in ./usr/bin executable..'

find usr -type f | xargs md5sum > DEBIAN/md5sums
echo 'MD5sums updated...'

find DEBIAN -type f | xargs chmod a+r
find DEBIAN -type d | xargs chmod a+rx
echo 'Permissions of files and folders in DEBIAN/ updated..'

cd ../

dpkg -b $DIR $DEB
echo 'DEB generated...'

rm -rf $DIR
echo "$DIR cleaned"

# That DEB package needs to be chowned to current user.
OWNER=$(stat -c%u "$0")
GROUP=$(stat -c%g "$0")
chown $OWNER:$GROUP $DEB
echo 'file owner and group owner changed..'

mv $DEB ../
