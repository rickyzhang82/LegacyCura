echo "****************************************************************************************************************************"
echo " Download wxPython from http://sourceforge.net/projects/wxpython/files/wxPython/2.9.4.0/wxPython-src-2.9.4.0.tar.bz2"
echo " Extrac source code to ~/Downloads/wxPython-src-2.9.4.0/"
echo " NOTE: Do the following manually:"
echo " "
echo "      mkvirtualenv Cura"
echo "      workon Cura"
echo " "
echo "****************************************************************************************************************************"
read -p "Press any key if you confirm above steps have been done. Otherwise Ctrl+C to abort..."

cd ~/Downloads/wxPython-src-2.9.4.0
echo "Enter into ~/Downloads/wxPython-src-2.9.4.0. Press any key to build wxPython C library"
read -p "Press any key..."
make install -j 8

read -p "Press any key to build and install wxPython Python code..."
cd ~/Downloads/wxPython-src-2.9.4.0/wxPython/
sh build-wxPython.sh
sh install-wxPython.sh


read -p "Press any key to install Pypi requirment..."
cd ~/repo/github/LegacyCura
pip install -r requirements_darwin.txt
