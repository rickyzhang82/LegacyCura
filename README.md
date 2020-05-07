Cura
====

Read this, it's important!
===========================

If you are reading this, then you are looking at the *development* version of Cura. If you just want to use Cura, take a look at the following location: https://daid.github.com/Cura

Development
===========

Cura is developed in Python with a C++ engine. The part you are looking at right now is the Python GUI.
The C++ engine is responsible for generating the actual toolpath. For development of the engine check out https://github.com/Ultimaker/CuraEngine

Issues
===========

Before posting issues (either Bugs, Feature requests or Requests for information) please read our policies carefully. These will be regulary updated and can be found at https://github.com/daid/Cura/wiki/Issue-policies


Packaging
---------

Cura development comes with a script "package.sh", this script has been designed to run under *nix OSes (Linux, MacOS, FreeBSD). For Windows the package.sh script can be run from bash using git.
The "package.sh" script generates a final release package. You should not need it during development, unless you are changing the release process. If you want to distribute your own version of Cura, then the package.sh script will allow you to do that.

The "package.sh" script understands a number of envrionement variables defined at the top of the script. Review and adjust settings to match your needs.

Both MacOS and Linux require some extra instructions for development, as you need to prepare an environment. Look below at the proper section to see what is needed.

Fedora
--------

Fedora builds Cura by using ```mock```, thereby enabling it to build RPMs for
every distribution that ```mock``` has a configuration file for. In pratice
this means that Fedora can build RPMs for several versions of Fedora, CentOS
and RHEL.

Cura can be built under a regular user account, there is no need to have root
privileges. In fact, having root privileges is very much discouraged.

However, the user account under which the build is performed needs to be a
member of the 'mock' group. This is accomplished as follows:

```bash
sudo usermod -a -G mock "$(whoami)"
```

To install the software that is required to build Cura, run the following
commands:

```bash
sudo dnf install -y git rpmdevtools rpm-build mock arduino

# Ensure that the Arduino tools can be found by the build
sudo mkdir -p /usr/share/arduino/hardware/tools/avr
sudo ln -sf /usr/bin /usr/share/arduino/hardware/tools/avr/bin

```

To release for Fedora 29, make sure `default.cfg` symlink to feodar 29 x86_64.

```bash
cd /etc/mock
ls -alh default.cfg 
lrwxrwxrwx. 1 root root 20 May  6 17:03 default.cfg -> fedora-29-x86_64.cfg
```

To build and install Cura, run the following commands:

```bash
# Get the Cura software, only required once
git clone https://github.com/rickyzhang82/LegacyCura.git Cura

# Build for the current system
cd Cura
./package.sh fedora

# Install on the current system
sudo yum localinstall -y scripts/linux/fedora/RPMS/Cura-*.rpm
```

Examples of building other configurations:

```bash
# Build for Fedora rawhide x86-64 and i386
./package.sh fedora fedora-rawhide-x86_64.cfg fedora-rawhide-i386.cfg

# Since only the basename of the mock configurations is used, this also works:
./package.sh fedora /etc/mock/fedora-21-x86_64.cfg /etc/mock/fedora-rawhide-i386.cfg
```

Fedora 29 in Virtual Box
------------------------

Since Fedora 30 discotinue Python 2, I have to migrate the Fedora 29 development environment to Virtualbox.

1. Install Fedora 29.
1. Install `mesa-libGLU`, `python2-pyopengl`.
1. Run Gnome 3 in Xorg mode.

Debian and Ubuntu Linux
--------

To build and install Cura, run the following commands:

```bash
git clone https://github.com/daid/Cura.git

sudo apt-get install python-opengl python-numpy python-serial python-setuptools python-wxgtk2.8 curl arduino

cd Cura

./package.sh debian_amd64          # or debian_i386 for 32bit
# this will prompt for your root password to run dpkg-deb

sudo dpkg -i ./scripts/linux/cura*.deb
```

Mac OS X
--------
The following section describes how to prepare working environment for developing and packaing for Mac OS X.
The working environment consist of build of Python, build of wxPython and all required Python packages.

We assume you already have Apple hardware with [64bit processor](http://support.apple.com/kb/HT3696) and you are familiar with tools like [virtualenv](http://pypi.python.org/pypi/virtualenv), [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) and [pip](http://www.pip-installer.org/en/latest/). Also ensure you have modern compiler installed.


### Install Python
Install Python 2.7 from macport.

### Configure Virtualenv
```
mkvirtualenv -p /opt/local/bin/python2 Cura
workon Cura
```

### Install wxPython
wxPython cannot be installed via pip, we have to build it from source by specifing prefix to our virtualenv.

Assuming you have virtualenv at *~/.virtualenvs/Cura/* and clone [wxPython sources](https://github.com/rickyzhang82/wxpython-src-2.9.4.0) at *~/Downloads/wxPython-src-2.9.4.0/*.

Prepare Mac OS SDK 10.11. Clone [legacy Maco OS SDK repository](https://github.com/rickyzhang82/MacOSX-SDKs) to */Users/Ricky/repo/github/MacOSX-SDKs*.

Run bash script `sh scripts/darwin/setup-python-env.sh` to automate step 1 to 6

1. `cd` into *~/Downloads/wxPython-src-2.9.4.0/* and configure the sources:

./configure \
    CFLAGS='-msse2 -mno-sse3 -mno-sse4' \
    CXXFLAGS='-msse2 -mno-sse3 -mno-sse4 -D__ASSERT_MACROS_DEFINE_VERSIONS_WITHOUT_UNDERSCORES=1' \
    --disable-debug \
    --enable-clipboard \
    --enable-display \
    --enable-dnd \
    --enable-monolithic \
    --enable-optimise \
    --enable-std_string \
    --enable-svg \
    --enable-unicode \
    --enable-webkit \
    --prefix=$HOME/.virtualenvs/Cura/ \
    --with-expat \
    --with-libjpeg=builtin \
    --with-libpng=builtin \
    --with-libtiff=builtin \
    --with-macosx-sdk=/Users/Ricky/repo/github/MacOSX-SDKs/MacOSX10.11.sdk \
    --with-macosx-version-min=10.9 \
    --with-opengl \
    --with-osx_cocoa \
    --with-zlib=builtin

2. `make install`
    Note to speedup the process I recommend you to enable multicore build by adding the -j*cores* flag:
    `make -j4 install`

    Chances are high that compilation will fail with type mismatch error in Obj-C code. If it's the case then apply a patch at *scripts/darwin/wxPython-src-2.9.4.0.patch*.
    If it won't fix all the errors, just modify source files manually by casting types to those expected by clang.

3. `cd` into *~/Downloads/wxPython-src-2.9.4.0/wxPython/*
4. Build wxPython (Note `python` is the python of your virtualenv):

        python setup.py build_ext \
        BUILD_GIZMOS=1 \
        BUILD_GLCANVAS=1 \
        BUILD_STC=1 \
        INSTALL_MULTIVERSION=0 \
        UNICODE=1 \
        WX_CONFIG=$HOME/.virtualenvs/Cura/bin/wx-config \
        WXPORT=osx_cocoa

5. Install wxPython (Note `python` is the python of your virtualenv):

        python setup.py install \
        --prefix=$HOME/.virtualenvs/Cura \
        BUILD_GIZMOS=1 \
        BUILD_GLCANVAS=1 \
        BUILD_STC=1 \
        INSTALL_MULTIVERSION=0 \
        UNICODE=1 \
        WX_CONFIG=$HOME/.virtualenvs/Cura/bin/wx-config \
        WXPORT=osx_cocoa

6. Create file *~/.virtualenvs/Cura/bin/pythonw* with the following content:

        #!/bin/bash
        ENV=`python -c "import sys; print sys.prefix"`
        PYTHON=`python -c "import sys; print sys.real_prefix"`/bin/python
        export PYTHONHOME=$ENV
        exec $PYTHON "$@"

At this point virtualenv is configured for wxPython development.
Remember to use `python` for pacakging and `pythonw` to run app for debugging.


### Install Python Packages
Required python packages are specified in *requirements.txt* and *requirements_darwin.txt*
If you use virtualenv, installing requirements as easy as `pip install -r requirements_darwin.txt`


### Install Arduino.app
[Arduino.app](http://www.arduino.cc/en/Main/Software) is required to compile certain components used by Cura. Tested version on Mac OS X is 1.0.5 but recent releases should also work.


### Package Cura into application
Ensure that virtualenv is activated, so `python` points to the python of your virtualenv (e.g. ~/.virtualenvs/Cura/bin/python). Use package.sh to build Cura:
`./package.sh darwin`

Note that application is only guaranteed to work on Mac OS X version used to build and higher, but may not support lower versions.
E.g. Cura built on 10.8 will work on 10.8 and 10.7, but not on 10.6. In other hand, Cura built on 10.6 will work on 10.6, 10.7 and 10.8.

FreeBSD
--------
On FreeBSD simply use the Port Tree (`cd /usr/ports/cad/cura`) to create (`make package`) and install (`make install`) the package as root. Port will check for all necessary dependencies. You can also use the provided binary package with `pkg install Cura`.

If you want to create an archive for local use the `package.sh freebsd` script (as an ordinary user) will give you a tarball with the program.
