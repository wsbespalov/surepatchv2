#!/bin/sh
echo "Start build..................."
cd ../
echo "Install python requirements..."
pip3 install -r requirements.txt
echo "Run installer................."
pyinstaller --onefile surepatch.py
cd dist
echo "Rename file..................."
mv surepatch surepatch_mac
echo "Make it executable............"
chmod 777 surepatch_mac
echo "Your executable in /dist dir.."