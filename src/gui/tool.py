##################################################
# Built-in Libs
##################################################
import sys
import datetime
import re
import ctypes
import os

##################################################
# External Libs
##################################################
import keyboard
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

##################################################
# Project Libs
##################################################
from gui.qt.mainwindows import Ui_MainWindow
from core.organizer import Organizer
from core.utils.resources import resource_path, get_user_data_dir, get_icons_dir


##################################################
# GUI Core
##################################################
class Tool(QMainWindow):
    def __init__(self, organizer, overlay):
        self.MyApp = "Steezy.organizer.2_0_0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.MyApp)

        """ GUI Init """
        super(Tool, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Steezy Organizer")
        self.appIcon = QIcon()
        self.appIcon.addFile(resource_path("gui/assets/logos/icon_1616.png"), QSize(16, 16))
        self.appIcon.addFile(resource_path("gui/assets/logos/icon_3232.png"), QSize(32, 32))
        self.appIcon.addFile(resource_path("gui/assets/logos/icon_4848.png"), QSize(48, 48))
        self.appIcon.addFile(resource_path("gui/assets/logos/icon_6464.png"), QSize(64, 64))
        self.appIcon.addFile(resource_path("gui/assets/logos/icon_128128.png"), QSize(128, 128))
        self.appIcon.addFile(resource_path("gui/assets/logos/icon_256256.png"), QSize(256, 256))
        self.setWindowIcon(self.appIcon)

        """ organizer instance storage """
        self.Organizer = organizer
        self.overlay = overlay

        """ Init actions and character index """
        self.CharIndex = 0
        self.Keys = ["massclick", "massdclick", "nextwindow", "prevwindow"]

        self.__HandleTextBrowser(color="Blue", text="----------------------------------")
        self.__HandleTextBrowser(text=self.__TimedLog("Initialisation du module ..."))

        """ Connect UI components """
        self.ui.ui_btn_autodetect.clicked.connect(self.__HandleCfgAutoDetect)
        self.ui.ui_btn_savecfg.clicked.connect(self.__HandleCfgSave)
        self.ui.ui_btn_loadcfg.clicked.connect(self.__HandleCfgLoad)
        self.ui.ui_btn_startstop.clicked.connect(self.__HandleCfgStartStop)
        self.ui.ui_btn_delay.textChanged.connect(self.__HandleEditDelay)

        """ Init start/stop component """
        self.ui.ui_btn_startstop.setText("GO")
        self.ui.img_startstop.setPixmap(QPixmap(resource_path("gui/assets/utils/stop.png")))
        self.ui.img_startstop.show()

        """ Load Config """
        self.__HandleTextBrowser(text=self.__TimedLog("Chargement de la config ..."))
        self.__HandleCfgLoad()
        self.ui.ui_console.setFontPointSize(8)
        self.__HandleTextBrowser(color="Grey", text=str(self.Organizer.Config["Characters"]))
        self.ui.ui_console.setFontPointSize(10)
        self.__HandleTextBrowser(color="Blue", text="----------------------------------")

    ##################################################
    # Link actions to UI Components
    ##################################################
    def __HandleEditDelay(self):
        self.delay = self.ui.ui_btn_delay.text()
        self.Organizer.delay = float(self.delay)

    def __HandleUiBtns(self):
        sender = self.sender().objectName()

        if "_btnup" in sender:
            char_idx = int(re.findall(r'\d+', f"{sender.split('_')[0]}")[0]) - 1
            self.Organizer.Characters[char_idx], self.Organizer.Characters[char_idx - 1] = self.Organizer.Characters[char_idx - 1], self.Organizer.Characters[char_idx]
            self.__CreateChar()
            self.overlay.update_icons(self.Organizer.Characters, self.Organizer.CharactersIcons)

        elif "_btndown" in sender:
            char_idx = int(re.findall(r'\d+', f"{sender.split('_')[0]}")[0]) - 1
            self.Organizer.Characters[char_idx], self.Organizer.Characters[char_idx + 1] = self.Organizer.Characters[char_idx + 1], self.Organizer.Characters[char_idx]
            self.__CreateChar()
            self.overlay.update_icons(self.Organizer.Characters, self.Organizer.CharactersIcons)

        elif "_btndel" in sender:
            char_idx = int(re.findall(r'\d+', f"{sender.split('_')[0]}")[0]) - 1
            self.Organizer.Characters.pop(char_idx)
            self.__CreateChar()
            self.overlay.update_icons(self.Organizer.Characters, self.Organizer.CharactersIcons)

        elif "x1_" in sender:
            x1Key = sender.split("x1_")[1]
            if x1Key in self.Organizer.kbKeys:
                prevKey = self.Organizer.kbKeys[x1Key]
                self.Organizer.mKeys[x1Key] = "x1"
                del self.Organizer.kbKeys[x1Key]
            elif x1Key in self.Organizer.mKeys:
                prevKey = self.Organizer.mKeys[x1Key]
                self.Organizer.mKeys[x1Key] = "x1"
            label = f"ui_btn_{x1Key}"
            exec(f"self.ui.{label}.setText(u'x1')")
            exec(f"self.ui.{label}.repaint()")

            self.__HandleTextBrowser("Blue", self.__TimedLog(f"[{x1Key}] {prevKey} >>> x1"))

        elif "x2_" in sender:
            x2Key = sender.split("x2_")[1]
            if x2Key in self.Organizer.kbKeys:
                prevKey = self.Organizer.kbKeys[x2Key]
                self.Organizer.mKeys[x2Key] = "x2"
                del self.Organizer.kbKeys[x2Key]
            elif x2Key in self.Organizer.mKeys:
                prevKey = self.Organizer.mKeys[x2Key]
                self.Organizer.mKeys[x2Key] = "x2"
            label = f"ui_btn_{x2Key}"
            exec(f"self.ui.{label}.setText(u'x2')")
            exec(f"self.ui.{label}.repaint()")
            self.__HandleTextBrowser("Blue", self.__TimedLog(f"[{x2Key}] {prevKey} >>> x2"))

        """ Edit Keybinds """
        for key in self.Keys:
            prevM = False
            if f"btn_{key}" in sender:
                label = f"ui_btn_{key}"
                exec(f"self.ui.{label}.setText(u'...')")
                exec(f"self.ui.{label}.repaint()")
                keyPressed = False
                if key in self.Organizer.mKeys:
                    prevKey = self.Organizer.mKeys[key]
                    prevM = True
                elif key in self.Organizer.kbKeys:
                    prevKey = self.Organizer.kbKeys[key]
                tmpKey = None
                while not keyPressed:
                    tmpKey = keyboard.read_key()
                    if tmpKey is not None:
                        if tmpKey == "esc":
                            exec(f"self.ui.{label}.setText(u'{prevKey}')")
                            exec(f"self.ui.{label}.repaint()")
                        if prevM:
                            del self.Organizer.mKeys[key]
                        self.Organizer.kbKeys[key] = tmpKey
                        keyPressed = True
                        exec(f"self.ui.{label}.setText(u'{tmpKey}')")
                        exec(f"self.ui.{label}.repaint()")

                if prevKey != tmpKey:
                    self.__HandleTextBrowser("Blue", self.__TimedLog(f"[{key}] {prevKey} >>> {tmpKey}"))

    ##################################################
    # Create X characters components on UI
    ##################################################
    def __CreateChar(self):
        self.__ResetView()
        self.CharIndex = 0
        begin = 180 - 40 * (len(self.Organizer.Characters) / 2)
        for Char in self.Organizer.Characters:
            self.CharIndex += 1
            label = f"char{self.CharIndex}_charname"
            setattr(self.ui, label, QLabel(self.ui.centralwidget))
            exec(f"self.ui.{label}.setObjectName(u'{label}')")
            exec(f"self.ui.{label}.setText(u'{Char}')")
            exec(f"self.ui.{label}.setGeometry(QRect(300, {begin + 40 * (self.CharIndex -1)}, 231, 31))")
            exec(f"self.ui.{label}.show()")

            label = f"char{self.CharIndex}_iconbtn"
            setattr(self.ui, label, QPushButton(self.ui.centralwidget))
            exec(f"self.ui.{label}.setObjectName(u'{label}')")
            icon_path = self.Organizer.CharactersIcons.get(Char, "gui/assets/logos/icon_6464.png")
            exec(f"self.ui.{label}.setIcon(QIcon('{icon_path}'))")
            exec(f"self.ui.{label}.setIconSize(QSize(24, 24))")
            exec(f"self.ui.{label}.setGeometry(QRect(256, {begin + 40 * (self.CharIndex - 1)}, 31, 31))")
            exec(f"self.ui.{label}.clicked.connect(self.__HandleIconSelection)")
            exec(f"self.ui.{label}.show()")

            label = f"char{self.CharIndex}_btnup"
            setattr(self.ui, label, QPushButton(self.ui.centralwidget))
            exec(f"self.ui.{label}.setObjectName(u'{label}')")
            exec(f"self.ui.{label}.setText(u'')")
            if self.CharIndex != 1:
                exec(f"self.ui.{label}.setIcon(QIcon(resource_path('gui/assets/utils/up.png')))")
                exec(f"self.ui.{label}.clicked.connect(self.__HandleUiBtns)")
            else:
                exec(f"self.ui.{label}.setIcon(QIcon(resource_path('gui/assets/utils/upgrey.png')))")
            exec(f"self.ui.{label}.setGeometry(QRect(440, {begin + 40 * (self.CharIndex -1)}, 31, 31))")
            exec(f"self.ui.{label}.show()")

            label = f"char{self.CharIndex}_btndown"
            setattr(self.ui, label, QPushButton(self.ui.centralwidget))
            exec(f"self.ui.{label}.setObjectName(u'{label}')")
            exec(f"self.ui.{label}.setText(u'')")
            if self.CharIndex != len(self.Organizer.Characters):
                exec(f"self.ui.{label}.setIcon(QIcon(resource_path('gui/assets/utils/down.png')))")
                exec(f"self.ui.{label}.clicked.connect(self.__HandleUiBtns)")
            else:
                exec(f"self.ui.{label}.setIcon(QIcon(resource_path('gui/assets/utils/downgrey.png')))")
            exec(f"self.ui.{label}.setGeometry(QRect(480, {begin + 40 * (self.CharIndex -1)}, 31, 31))")
            exec(f"self.ui.{label}.show()")

            label = f"char{self.CharIndex}_btndel"
            setattr(self.ui, label, QPushButton(self.ui.centralwidget))
            exec(f"self.ui.{label}.setObjectName(u'{label}')")
            exec(f"self.ui.{label}.setText(u'')")
            exec(f"self.ui.{label}.setIcon(QIcon(resource_path('gui/assets/utils/trash.png')))")
            exec(f"self.ui.{label}.setGeometry(QRect(550, {begin + 40 * (self.CharIndex -1)}, 31, 31))")
            exec(f"self.ui.{label}.clicked.connect(self.__HandleUiBtns)")
            exec(f"self.ui.{label}.show()")

    ##################################################
    # Handle Auto Detect method
    ##################################################
    def __HandleCfgAutoDetect(self):
        self.__ResetView()
        Windows = self.Organizer.GetActiveWindowsFiltered()
        self.__HandleTextBrowser("Blue", self.__TimedLog(f"Auto-Detect : {Windows}"))
        self.Organizer.Characters = Windows
        for char in Windows:
            if char not in self.Organizer.CharactersIcons:
                self.Organizer.CharactersIcons[char] = resource_path("gui/assets/logos/icon_6464.png")
        self.__CreateChar()
        self.overlay.update_icons(self.Organizer.Characters, self.Organizer.CharactersIcons)

    ##################################################
    # Handle Save Button
    ##################################################
    def __HandleCfgSave(self):
        Config = dict()
        self.__HandleTextBrowser("Green", self.__TimedLog("Config sauvegardée"))
        Config["Characters"] = self.Organizer.Characters
        Config["CharactersIcons"] = self.Organizer.CharactersIcons
        Config["mKeys"] = self.Organizer.mKeys
        Config["kbKeys"] = self.Organizer.kbKeys
        Config["Delay"] = self.delay
        self.Organizer.SetConfig(data=Config)
        self.Organizer.UpdateModel()

    ##################################################
    # Handle Load Button
    ##################################################
    def __HandleCfgLoad(self):
        self.Organizer.UpdateModel()
        self.__ResetView()
        self.__HandleTextBrowser("Green", self.__TimedLog("Config chargée"))
        self.__CreateChar()
        self.__LoadKeyBinds()

    ##################################################
    # Handle Icons Selection
    ##################################################
    def __HandleIconSelection(self):
        sender = self.sender()
        char_idx = int(re.findall(r'\d+', sender.objectName())[0]) - 1
        char_name = self.Organizer.Characters[char_idx]

        icons_dir = get_icons_dir()

        # Open file dialog to select an icon
        icon_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Icon",
            icons_dir,
            "Images (*.png *.jpg *.bmp)"
        )

        if icon_path:
            # Ensure the icon is within the characterIcons directory
            if not icon_path.startswith(icons_dir):
                # Copy the icon to the characterIcons directory
                icon_filename = os.path.basename(icon_path)
                destination_path = os.path.join(icons_dir, icon_filename)
                shutil.copyfile(icon_path, destination_path)
                icon_path = destination_path

            # Update the icon button
            sender.setIcon(QIcon(icon_path))
            sender.setIconSize(QSize(24, 24))

            # Update the organizer's CharactersIcons with the relative path
            relative_icon_path = os.path.relpath(icon_path, icons_dir)
            self.Organizer.Config['CharactersIcons'][char_name] = relative_icon_path
            self.Organizer.CharactersIcons[char_name] = icon_path

            # Update the overlay
            self.overlay.update_icons(self.Organizer.Characters, self.Organizer.CharactersIcons)

            self.__HandleTextBrowser("Blue",
                                     self.__TimedLog(f"Icône mise à jour:\n{char_name} -> {relative_icon_path}"))

    ##################################################
    # Remove Characters Components
    ##################################################
    def __ResetView(self):
        self.CharIndex = 0
        for widget in self.ui.centralwidget.children():
            if "char" in widget.objectName():
                widget.deleteLater()

    ##################################################
    # Handle Console writing
    ##################################################
    def __HandleTextBrowser(self, color="White", text=""):
        if color == "Blue":
            self.ui.ui_console.setTextColor("#4287f5")
        elif color == "Red":
            self.ui.ui_console.setTextColor("#c45c45")
        elif color == "Green":
            self.ui.ui_console.setTextColor("#74b870")
        elif color == "White":
            self.ui.ui_console.setTextColor("#ffffff")
        elif color == "Grey":
            self.ui.ui_console.setTextColor("#5c5c5c")
        self.ui.ui_console.append(text)
        self.ui.ui_console.setTextColor("#ffffff")

    ##################################################
    # Draw time on console writing
    ##################################################
    def __TimedLog(self, log):
        n = datetime.datetime.now()
        h = str(n.hour)
        m = str(n.minute)
        s = str(n.second)
        sep = ":"
        return "[" + h + sep + m + sep + s + "]" + " " + log

    ##################################################
    # Handle start/stop component
    ##################################################
    def __HandleCfgStartStop(self):
        Status = self.Organizer.ManageKb()
        if Status:
            self.ui.img_startstop.setPixmap(QPixmap(resource_path("gui/assets/utils/start.png")))
            self.__HandleTextBrowser("Green", self.__TimedLog("Lancement d'organizer"))
            self.ui.ui_btn_startstop.setText("STOP")
            self.ui.img_startstop.show()
            self.overlay.show()
        else:
            self.ui.img_startstop.setPixmap(QPixmap(resource_path("gui/assets/utils/stop.png")))
            self.__HandleTextBrowser("Red", self.__TimedLog("Arrêt d'organizer"))
            self.ui.ui_btn_startstop.setText("GO")
            self.ui.img_startstop.show()
            self.overlay.hide()

    ##################################################
    # Load Keybinds and init components
    ##################################################
    def __LoadKeyBinds(self):
        keyIndex = 0
        for key in self.Keys:
            keyIndex += 1
            label = f"ui_btn_{key}"
            if key in self.Organizer.mKeys:
                exec(f"self.ui.{label}.setText(u'{self.Organizer.mKeys[key]}')")
            elif key in self.Organizer.kbKeys:
                exec(f"self.ui.{label}.setText(u'{self.Organizer.kbKeys[key]}')")
            exec(f"self.ui.{label}.clicked.connect(self.__HandleUiBtns)")
            label = f"ui_x1_{key}"
            setattr(self.ui, label, QPushButton(self.ui.centralwidget))
            exec(f"self.ui.{label}.setObjectName(u'{label}')")
            exec(f"self.ui.{label}.setText(u'')")
            exec(f"self.ui.{label}.setIcon(QIcon(resource_path('gui/assets/utils/x1.png')))")
            exec(f"self.ui.{label}.clicked.connect(self.__HandleUiBtns)")
            exec(f"self.ui.{label}.setGeometry(QRect(705, {380 + 40 * (keyIndex - 1)}, 31, 31))")
            exec(f"self.ui.{label}.show()")
            label = f"ui_x2_{key}"
            setattr(self.ui, label, QPushButton(self.ui.centralwidget))
            exec(f"self.ui.{label}.setObjectName(u'{label}')")
            exec(f"self.ui.{label}.setText(u'')")
            exec(f"self.ui.{label}.setIcon(QIcon(resource_path('gui/assets/utils/x2.png')))")
            exec(f"self.ui.{label}.clicked.connect(self.__HandleUiBtns)")
            exec(f"self.ui.{label}.setGeometry(QRect(670, {380 + 40 * (keyIndex - 1)}, 31, 31))")
            exec(f"self.ui.{label}.show()")
        self.ui.ui_btn_delay.setText(str(self.Organizer.delay))


##################################################
# For debug usage only
##################################################
if __name__ == '__main__':
    Organizer = Organizer()

    app = QApplication(sys.argv)

    with open('gui/style/stylesheet.qss', 'r') as f:
        style = f.read()

    app.setStyleSheet(style)

    window = Tool(organizer=Organizer, overlay=None)
    window.show()

    sys.exit(app.exec())
    exit()
