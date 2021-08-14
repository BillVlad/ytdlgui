#!/bin/bash
test -f ${XDG_CONFIG_HOME:-~/.config}/user-dirs.dirs && source ${XDG_CONFIG_HOME:-~/.config}/user-dirs.dirs
echo -e '[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Path='${XDG_DOWNLOAD_DIR:-$HOME}'/Youtube-DL
Exec=/opt/ytdlgui/ytdlgui
Name=Youtube-Dl GUI
Icon=/opt/ytdlgui/ytdlgui.png
Categories=Utility' > ytdlgui.desktop
desktop-file-validate ytdlgui.desktop
mkdir ${XDG_DOWNLOAD_DIR:-$HOME}/Youtube-DL
desktop-file-install --dir=$HOME/.local/share/applications ytdlgui.desktop

