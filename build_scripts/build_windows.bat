echo "Start build..................."
cd ../
echo "Install python requirements..."
pip3 install -r requirements.txt
echo "Run installer................."
pyinstaller --onefile surepatch.py
cd dist
echo "Rename file..................."
move surepatch surepatch_win
echo "Your executable in /dist dir.."