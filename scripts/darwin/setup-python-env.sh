echo "****************************************************************************************************************************"
echo " Clone ssh://git@rizhan.asuscomm.com:8091/Ricky/wxpython-src-2.9.4.0.git to ~/Downloads/wxPython-src-2.9.4.0/"
echo " NOTE: Do the following manually:"
echo " "
echo "      mkvirtualenv -p /opt/local/bin/python2 Cura"
echo "      workon Cura"
echo " "
echo "****************************************************************************************************************************"
read -p "Press any key if you confirm above steps have been done. Otherwise Ctrl+C to abort..."

cd ~/Downloads/wxPython-src-2.9.4.0
echo "Enter into ~/Downloads/wxPython-src-2.9.4.0. Press any key to build wxPython C library"
read -p "Press any key..."
sh exe_configure.sh
make install -j 8

read -p "Press any key to build and install wxPython Python code..."
cd ~/Downloads/wxPython-src-2.9.4.0/wxPython/
sh build-wxPython.sh
sh install-wxPython.sh


read -p "Press any key to install Pypi requirment..."
cd ~/repo/github/LegacyCura
pip install -r requirements_darwin.txt
