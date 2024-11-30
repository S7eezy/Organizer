# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Tool - untitledKeUjrw.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from src.core.utils.resources import resource_path


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"Tool")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ui_console = QTextBrowser(self.centralwidget)
        self.ui_console.setObjectName(u"ui_console")
        self.ui_console.setGeometry(QRect(30, 301, 401, 281))

        ## Config - Labels
        x = 470
        y = 320
        s = 40
        self.ui_label_massclick = QLabel(self.centralwidget)
        self.ui_label_massclick.setObjectName(u"ui_label_massclick")
        self.ui_label_massclick.setGeometry(QRect(x, y, 91, 31))
        y += s

        self.ui_label_massdclick = QLabel(self.centralwidget)
        self.ui_label_massdclick.setObjectName(u"ui_label_massdclick")
        self.ui_label_massdclick.setGeometry(QRect(x, y, 91, 31))
        y += s

        self.ui_label_nextwindow = QLabel(self.centralwidget)
        self.ui_label_nextwindow.setObjectName(u"ui_label_nextwindow")
        self.ui_label_nextwindow.setGeometry(QRect(x, y, 91, 31))
        y += s

        self.ui_label_prevwindow = QLabel(self.centralwidget)
        self.ui_label_prevwindow.setObjectName(u"ui_label_prevwindow")
        self.ui_label_prevwindow.setGeometry(QRect(x, y, 91, 31))
        y += s

        self.ui_label_delay = QLabel(self.centralwidget)
        self.ui_label_delay.setObjectName(u"ui_label_delay")
        self.ui_label_delay.setGeometry(QRect(x, y, 91, 31))

        ## Config - Buttons
        x = 580
        y = 320
        s = 40
        self.ui_btn_massclick = QPushButton(self.centralwidget)
        self.ui_btn_massclick.setObjectName(u"ui_btn_massclick")
        self.ui_btn_massclick.setGeometry(QRect(x, y, 75, 31))
        y += s

        self.ui_btn_massdclick = QPushButton(self.centralwidget)
        self.ui_btn_massdclick.setObjectName(u"ui_btn_massdclick")
        self.ui_btn_massdclick.setGeometry(QRect(x, y, 75, 31))
        y += s

        self.ui_btn_nextwindow = QPushButton(self.centralwidget)
        self.ui_btn_nextwindow.setObjectName(u"ui_btn_nextwindow")
        self.ui_btn_nextwindow.setGeometry(QRect(x, y, 75, 31))
        y += s

        self.ui_btn_prevwindow = QPushButton(self.centralwidget)
        self.ui_btn_prevwindow.setObjectName(u"ui_btn_prevwindow")
        self.ui_btn_prevwindow.setGeometry(QRect(x, y, 75, 31))
        y += s

        self.ui_btn_delay = QLineEdit(self.centralwidget)
        self.ui_btn_delay.setObjectName(u"ui_btn_delay")
        self.ui_btn_delay.setGeometry(QRect(x, y, 75, 31))


        ## Actions - Buttons
        x = 70
        y = 100
        s = 40
        self.ui_btn_autodetect = QPushButton(self.centralwidget)
        self.ui_btn_autodetect.setObjectName(u"ui_btn_autodetect")
        self.ui_btn_autodetect.setGeometry(QRect(x, y, 121, 23))
        y += s

        self.ui_btn_loadcfg = QPushButton(self.centralwidget)
        self.ui_btn_loadcfg.setObjectName(u"ui_btn_loadcfg")
        self.ui_btn_loadcfg.setGeometry(QRect(x, y, 121, 23))
        y += s

        self.ui_btn_savecfg = QPushButton(self.centralwidget)
        self.ui_btn_savecfg.setObjectName(u"ui_btn_savecfg")
        self.ui_btn_savecfg.setGeometry(QRect(x, y, 121, 23))
        y += s

        self.ui_btn_startstop = QPushButton(self.centralwidget)
        self.ui_btn_startstop.setObjectName(u"ui_btn_startstop")
        self.ui_btn_startstop.setGeometry(QRect(x, y, 121, 23))

        self.img_startstop = QLabel(self.centralwidget)
        self.img_startstop.setObjectName(u"img_startstop")
        self.img_startstop.setGeometry(QRect(30, 210, 41, 41))


        self.img_gif = QLabel(self.centralwidget)
        self.img_gif.setObjectName(u"img_gif")
        self.img_gif.setGeometry(QRect(85, 260, 48, 48))
        self.gifmovie = QMovie(resource_path("src/gui/assets/logos/gif.gif"))

        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName(u"logo")
        self.logo.setGeometry(QRect(20, 20, 250, 60))
        self.logo.setPixmap(QPixmap(resource_path("src/gui/assets/logos/logomain.png")))

        self.img_gif.setMovie(self.gifmovie)
        self.gifmovie.start()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("Tool", u"Tool", None))
        self.ui_label_massclick.setText(QCoreApplication.translate("Tool", u"Mass Click", None))
        self.ui_label_massdclick.setText(QCoreApplication.translate("Tool", u"Mass Autopilot", None))
        self.ui_label_nextwindow.setText(QCoreApplication.translate("Tool", u"Pers. suivant", None))
        self.ui_label_prevwindow.setText(QCoreApplication.translate("Tool", u"Pers. pr\u00e9c\u00e9dent", None))
        self.ui_label_delay.setText(QCoreApplication.translate("Tool", u"D\u00e9lai (ms)", None))
        self.ui_btn_massclick.setText(QCoreApplication.translate("Tool", u"...", None))
        self.ui_btn_massdclick.setText(QCoreApplication.translate("Tool", u"...", None))
        self.ui_btn_nextwindow.setText(QCoreApplication.translate("Tool", u"...", None))
        self.ui_btn_prevwindow.setText(QCoreApplication.translate("Tool", u"...", None))
        self.ui_btn_autodetect.setText(QCoreApplication.translate("Tool", u"Auto-Detect", None))
        self.ui_btn_loadcfg.setText(QCoreApplication.translate("Tool", u"Charg. Config", None))
        self.ui_btn_savecfg.setText(QCoreApplication.translate("Tool", u"Sauv. Config", None))
        self.ui_btn_startstop.setText(QCoreApplication.translate("Tool", u"Start / Stop", None))
        self.img_startstop.setText("")
    # retranslateUi

