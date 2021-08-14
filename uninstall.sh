#!/bin/bash
echo "Are you sure you want uninstall?"
echo "Else no, Press Ctrl+C"
read -p ""
sudo pacman -Rcc python-pyqt5 python-pyqt5-sip
pip uninstall youtube-dl
sudo rm /opt/ytdlgui/ytdlgui
sudo rm /bin/ytdlgui
sudo rm /opt/ytdlgui/main.py
sudo rm /opt/ytdlgui/gui.py
sudo rm /opt/ytdlgui/ytdlgui.png
sudo rm /opt/ytdlgui/uninstall.sh
sudo rmdir /opt/ytdlgui/
rm $HOME/.local/share/applications/ytdlgui.desktop
echo "Done."
