#!/bin/sh
echo "Go up"
cd ../
echo "install python requirements"
pip3 install -r requirements.txt
echo "Run installer"
pyinstaller --onefile surepatch.py
echo "cd dist"
cd dist
echo "rename file"
mv surepatch surepatch_mac
echo "make it executable"
chmod 777 surepatch_mac