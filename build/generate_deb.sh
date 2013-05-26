#!/bin/sh

# Generate deb package from source.
# v1.3 - 2013.5.19
# fixed: A space should be added after ! operate in test() command.
#        else sh will throw an exception: unexpected operator.
# v1.2 - 2013.5.12
# A second parameter added;
# usage() added;
# v1.1 - 2013.4.29
# Change permissions in DEBIAN/
# v1.0 -2013.4.15
# project inited.

usage() {
	echo "$0 fakeroot_of_package package_name"
	echo 'This program needs root permission'
	echo 'version 1.2'
}

if [ $# -ne 2 ]; then
	echo 'parameter needed'
	usage
	exit 1
fi 

DIR=$1
DIR=${DIR%%/}
if [ ! -d $DIR ]; then
	echo 'Error: no such directory!!!'
	usage
	exit 1
fi

#DEB=${DIR%%/}.deb
DEB=$2


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
echo $DIR cleaned

mv $DEB ../
