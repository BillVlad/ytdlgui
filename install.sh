#!/bin/bash
echo "Youtube-DL GUI Ver. 1.2.2"
echo 
echo "Вы можете прочитать изменения в программе в файле changelog.html"
echo "Started..."
sleep 2s
sudo pacman -S python-pip python-pyqt5 python-pyqt5-sip
pip install youtube-dl
sudo mkdir /opt/ytdlgui
sudo cp "main.py" /opt/ytdlgui/main.py
sudo cp "gui.py" /opt/ytdlgui/gui.py
sudo cp "ytdlgui.png" /opt/ytdlgui/ytdlgui.png
sudo cp "uninstall.sh" /opt/ytdlgui/uninstall.sh
sudo cp "ytdlgui" /opt/ytdlgui/ytdlgui
sudo ln "/opt/ytdlgui/ytdlgui" /bin/ytdlgui
echo "Installed in /opt/ytdlgui"
bash desktopfile.sh
sleep 2s
desktop-file-install --dir=$HOME/.local/share/applications ytdlgui.desktop
echo "ytdlgui.desktop file copied"
read -p "[Press enter to continue]"
