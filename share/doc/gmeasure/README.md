About
=====
gmeasure is a simple screen measure tool, like kruler in KDE, or measureit addon in Firefox.

App logo is picked from ![Kruler](http://www.kde.org/applications/graphics/kruler/ "Kruler") project.

Screenshoot
===========
![gmeasure screenshot](share/doc/gmeasure/screenshot.png?raw=true)

INSTALL
=======
For Debian based systems, just download the gmeasure.deb package and install. This deb package may be installed using `# dpkg -i gmeasure.deb` command.

For Fedora and other Linux systems, you need to install some dependencies first:
`python3-gi python3-cairo python3-gi-cairo` are need to be installed. Then download this program(as zip file or using `git clone`), and click `gmeasure.py`.


BUILD
=====
Current I've only learned how to build deb packages. And a shell script is written to simplify the build processing.
It's really easy to do this:
* `git clone` this project.
* run `build/build.sh` script with normal user privilege.
* run `build/generate_deb.sh` script with root privilege.
Now you should have a new deb package.
