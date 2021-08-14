#!/usr/bin/python
from gui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import pathlib, sys, os, youtube_dl, requests, mpv, locale

app = QtWidgets.QApplication(sys.argv)
locale.setlocale(locale.LC_NUMERIC, 'C')
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)


def isConnected():
    try:
        response = requests.get("https://google.com")
        print("response code : " + str(response.status_code))
        main()
    except requests.ConnectionError:
        e = "<b>U</b> not have a internet connection :DD"
        print(e)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("<b>Error</b>")
        msg.setInformativeText(e)
        msg.setWindowTitle("Error")
        sys.exit(msg.exec())


def main():
    # Это чтобы в консоль не срало

    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            ui.statusBar.showMessage('ERROR')

    # Хук для прогресс бара в GUI и статуса видосов

    filename = None

    def my_hook(d):
        # print(d)
        text = d['filename']
        if d['status'] == 'finished':
            # GUI
            ui.statusBar.showMessage(
                f"Downloaded in:  {os.path.abspath(text)}")
            # TTY
            print(f"Downloaded in: '{os.path.abspath(text)}'")
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%', '')
            ui.progressBar.setValue(float(p))
            ui.speedLable.setText("Speed: " + str(d['_speed_str']))

    # Опции для youtube_dl.
    ydl_opts = {
        'logger': MyLogger(),
        'progress_hooks': [my_hook]
    }

    ytdll = youtube_dl.YoutubeDL(ydl_opts)

    # Типо инициализации. Если этого нету, то... всё плохо
    ui.outputLabel.setText("Instruction")
    ui.descLabel.setText(
        "Youtube-Dl GUI (Qt based) Version: 1.3\n\n1. Paste URL address on video/audio.\n2. Press on button 'Download' :D\n3. Well done!\n\nP.S. DO NOT REMOVE FOLDER Youtube-DL in Downloads!\n\nPLAY MPV:\nYou can open local file and url in MPV from here :D")

    # Скачиваем видосы бля. Пиздим инфу с строки

    def descYTThumb():
        fromurl = ui.lineEdit.text()

        # Проверяем на наличие текста в строке
        if fromurl == '':
            ui.statusBar.showMessage('ERROR: URL empty')
            return False
        # Проверяем на содержимое http (можно было и лучше, но я дебил)
        if "http" not in fromurl:
            ui.statusBar.showMessage("ERROR: It's not URL")
            return False

        # verifyURL()
        thumbYT = ytdll.extract_info(fromurl, download=False)
        ui.outputLabel.setText("Description")
        if 'description' in thumbYT:
            ui.descLabel.setText(thumbYT['description'])
        else:
            ui.descLabel.setText("None description")
            print('No')

    def getVideoInfo():
        fromurl = ui.lineEdit.text()

        # Проверяем на наличие текста в строке
        if fromurl == '':
            ui.statusBar.showMessage('ERROR: URL empty')
            return False
        # Проверяем на содержимое http (можно было и лучше, но я дебил)
        if "http" not in fromurl:
            ui.statusBar.showMessage("ERROR: It's not URL")
            return False

        # verifyURL()
        thumbYT = ytdll.extract_info(fromurl, download=False)

        urlthumb = thumbYT['thumbnail']
        data = requests.get(urlthumb).content

        pixmp = QPixmap()
        pixmp.loadFromData(data)

        ui.thumbIMG.setPixmap(pixmp)
        ui.thumbIMG.sizeHint()
        ui.thumbIMG.setScaledContents(True)
        descYTThumb()
        #ui.statusBar.showMessage("[GET_INFO_HERE]: Info here :D")

    def ytdlDownload():
        # Наша строка
        fromurl = ui.lineEdit.text()

        # Проверяем на наличие текста в строке
        if fromurl == '':
            ui.statusBar.showMessage('ERROR: URL empty')
            return False
        # Проверяем на содержимое http (можно было и лучше, но я дебил)
        if "http" not in fromurl:
            ui.statusBar.showMessage("ERROR: It's not URL")
            return False

        thumbYT = ytdll.extract_info(fromurl, download=False)
        comboIndex = ui.comboBox.currentIndex()

        ui.statusBar.showMessage(
            f"[{thumbYT['extractor_key']}] URL: {fromurl} get file..")

        if comboIndex == 0:
            ydl_video_opts = {
                'format': 'best',
                'videoformat': "mp4",
                'logger': MyLogger(),
                'progress_hooks': [my_hook]
            }
            print("Video Started")
            youtube_dl.YoutubeDL(ydl_video_opts).download([fromurl])
            print(filename)
        else:
            ydl_audio_opts = {
                'format': 'bestaudio/best',
                'logger': MyLogger(),
                'progress_hooks': [my_hook]
            }
            print("Audio Started")
            youtube_dl.YoutubeDL(ydl_audio_opts).download([fromurl])
        getVideoInfo()
        print("{0}.{1}x{2}.{3}.{4}".format(
            (thumbYT['title']) + '-' + (thumbYT['id']), (thumbYT['ext'])))

    # Воспроизведение медиа контента (встроенный, так сказать, MPV)
    # ПРИМЕЧАНИЕ: нужно иметь в директории или mpv.py, или установить библиотеку
    # Например: pip install python-mpv
    def mpvPlay():
        fromurl = ui.lineEdit.text()

        # Проверяем на наличие текста в строке
        if fromurl == '':
            ui.statusBar.showMessage('ERROR: URL empty')
            return False

        # Задаём параметры для MPV
        player = mpv.MPV(wid=str(int(ui.widget.winId())),
                         ytdl=True,
                         input_default_bindings=True,
                         osc=True)

        player.fullscreen = True
        player.play(fromurl)
        player.wait_until_playing()

    # Вешаем события на кнопки
    ui.downButt.clicked.connect(ytdlDownload)
    ui.infoButt.clicked.connect(getVideoInfo)
    ui.lineEdit.returnPressed.connect(ui.downButt.click)
    ui.playButt.clicked.connect(mpvPlay)

    MainWindow.show()
    sys.exit(app.exec_())


# Запускаем наш код, если он сам выступает как исполняемый файл
if __name__ == "__main__":
    isConnected()

