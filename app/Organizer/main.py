##################################################
# Built-in Libs
##################################################
import time
import json
import threading

##################################################
# External Libs
##################################################
import keyboard
from pynput.mouse import Listener, Controller, Button

##################################################
# Project Libs
##################################################
import app.Organizer.Utils.Windows as CW


##################################################
# Organizer Core
##################################################
class Organizer:
    def __init__(self):

        """ Storage initialisation """
        self.Config = dict()
        self.Characters = []
        self.kbKeys = dict()
        self.mKeys = dict()
        self.Mouse = Controller()

        """ Windows PID storage """
        self.ActiveWindows = self.GetActiveWindows()

        """ Read JSON config """
        try:
            self.GetConfig()
            self.GetCharacters()
            self.GetKeys()
        except json.decoder.JSONDecodeError:
            print("ERREUR JSON")

        """ Compare PIDs and Config """
        self.ProcessIndex = -1
        try:
            self.CurrentWindow = self.Characters[self.ProcessIndex]
            self.__IncrementIndex()
        except IndexError:
            print("ERROR: Aucun personnage détecté, veuillez réparer la config")

        """ Mouse and keyboard listeners initialisation """
        self.MouseListener = Listener(on_click=self.on_click)
        self.MouseListener.start()

        self.KeyboardHandlerStatus = False
        self.KeyboardHandler = threading.Thread(target=self.__KeyboardHandler, daemon=True)
        self.KeyboardHandler.start()

    ##################################################
    # Windows Process listeners
    ##################################################
    @staticmethod
    def GetActiveWindows(process="Dofus.exe"):
        return CW.getDofusWindows(process)

    @staticmethod
    def GetActiveWindowsFiltered(process="Dofus.exe"):
        Windows = CW.getDofusWindows(process)
        for k, v in enumerate(Windows):
            Windows[k] = v.split(" ")[0]
        return Windows

    def __FilterCharsByProcess(self):
        ActiveChars = []
        InactiveChars = []
        for key in self.Config["Characters"]:
            isPlayed = False
            for Process in self.ActiveWindows:
                if key in Process:
                    isPlayed = True
            if isPlayed:
                pass
            else:
                self.Characters.pop(key)
        return ActiveChars, InactiveChars

    ##################################################
    # System Config and Model manipulation
    ##################################################

    def UpdateModel(self):
        self.ActiveWindows = self.GetActiveWindows()
        self.GetConfig()
        self.GetCharacters()
        self.GetKeys()

    def GetConfig(self, file="app/Organizer/config.json"):
        with open(file, "r") as filehandler:
            self.Config = json.load(filehandler)

    @staticmethod
    def SetConfig(file="app/Organizer/config.json", data=None):
        with open(file, "w+") as filehandler:
            if data:
                print(data)
                json.dump(data, filehandler)

    def GetCharacters(self):
        Characters = []
        for key in self.Config["Characters"]:
            Characters.append(key)
        self.Characters = Characters

    def GetKeys(self):
        mKeys = dict()
        kbKeys = dict()
        for key, value in self.Config["mKeys"].items():
            mKeys[key] = value
        for key, value in self.Config["kbKeys"].items():
            kbKeys[key] = value
        self.mKeys = mKeys
        self.kbKeys = kbKeys

    ##################################################
    # Organizer core actions
    ##################################################

    def __IncrementIndex(self):
        if self.ProcessIndex + 1 < len(self.Characters):
            self.ProcessIndex += 1
        else:
            self.ProcessIndex = 0
        self.CurrentWindow = self.Characters[self.ProcessIndex]
        CW.switchToWindow(self.CurrentWindow)

    def __DecrementIndex(self):
        if self.ProcessIndex == 0:
            self.ProcessIndex = len(self.Characters) - 1
        else:
            self.ProcessIndex -= 1
        self.CurrentWindow = self.Characters[self.ProcessIndex]
        CW.switchToWindow(self.CurrentWindow)

    def __LoopIndex(self, action):
        for i in range(len(self.Characters)):
            self.ProcessIndex = i
            self.CurrentWindow = self.Characters[self.ProcessIndex]
            CW.switchToWindow(self.CurrentWindow)
            if action == "double_click":
                self.Mouse.click(Button.left, 3)
                time.sleep(0.3)
            elif action == "click":
                self.Mouse.click(Button.left)
        self.__IncrementIndex()

    def __InputAction(self, action):
        if action == "massdclick":
            self.__LoopIndex(action="double_click")
        if action == "massclick":
            self.__LoopIndex(action="click")
        if action == "nextwindow":
            self.__IncrementIndex()
        if action == "prevwindow":
            self.__DecrementIndex()

    ##################################################
    # Mouse and Keyboard listeners
    ##################################################

    def ManageKb(self):
        self.KeyboardHandlerStatus = not self.KeyboardHandlerStatus
        return self.KeyboardHandlerStatus

    def on_click(self, x, y, button, pressed):
        if pressed:
            for key, val in self.mKeys.items():
                if val in str(button):
                    self.__InputAction(key)

    def __KeyboardHandler(self):
        while True:
            time.sleep(0.01)
            if self.KeyboardHandlerStatus:
                for key, val in self.kbKeys.items():
                    if keyboard.is_pressed(val):
                        self.__InputAction(key)
                        while keyboard.is_pressed(val):
                            continue


##################################################
# For debug usage only
##################################################

if __name__ == "__main__":
    Organizer = Organizer()
