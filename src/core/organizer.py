##################################################
# Built-in Libs
##################################################
import ctypes
import time
import json
import threading
import os
import shutil


##################################################
# External Libs
##################################################
import keyboard
from pynput.mouse import Listener, Controller, Button
import pyperclip
from PySide6.QtCore import QObject, Signal


##################################################
# Project Libs
##################################################
import core.utils.win_hook as CW
from core.utils.resources import resource_path, get_user_data_dir, get_icons_dir


##################################################
# organizer Core
##################################################
class Organizer(QObject):
    current_index_changed = Signal(int)

    def __init__(self):
        super().__init__()
        """ Storage initialisation """
        self.Config = dict()
        self.Characters = []
        self.CharactersIcons = dict()
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
            self.delay = float(self.Config["Delay"])
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


    def GetConfig(self):
        user_data_dir = get_user_data_dir()
        config_path = os.path.join(user_data_dir, 'config.json')

        if not os.path.exists(config_path):
            # If config doesn't exist in user data dir, copy the default config
            self.copy_default_config(config_path)

        try:
            with open(config_path, "r") as filehandler:
                self.Config = json.load(filehandler)
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Error loading config: {e}")
            print("Loading default configuration.")
            self.copy_default_config(config_path)
            # Load the default config
            with open(config_path, "r") as filehandler:
                self.Config = json.load(filehandler)

    def SetConfig(self, data=None):
        user_data_dir = get_user_data_dir()
        config_path = os.path.join(user_data_dir, 'config.json')

        # Ensure the user data directory exists
        os.makedirs(user_data_dir, exist_ok=True)

        with open(config_path, "w") as filehandler:
            if data:
                json.dump(data, filehandler, indent=4)

    def copy_default_config(self, config_path):
        user_data_dir = get_user_data_dir()
        # Ensure the user data directory exists
        os.makedirs(user_data_dir, exist_ok=True)

        default_config_path = resource_path("core/utils/default.json")

        # Copy the default config to the user data directory
        shutil.copyfile(default_config_path, config_path)

    def GetCharacters(self):
        Characters = []
        icons_dir = get_icons_dir()
        for key in self.Config["Characters"]:
            Characters.append(key)
            icon_relative_path = self.Config.get("CharactersIcons", {}).get(key, None)
            if icon_relative_path:
                icon_path = os.path.join(icons_dir, icon_relative_path)
                if not os.path.exists(icon_path):
                    # If the icon file doesn't exist, use default icon
                    icon_path = resource_path('gui/assets/logos/icon_6464.png')
            else:
                # Use default icon
                icon_path = resource_path('gui/assets/logos/icon_6464.png')
            self.CharactersIcons[key] = icon_path
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
    # organizer core actions
    ##################################################

    def __IncrementIndex(self):
        if self.ProcessIndex + 1 < len(self.Characters):
            self.ProcessIndex += 1
        else:
            self.ProcessIndex = 0
        self.CurrentWindow = self.Characters[self.ProcessIndex]
        CW.switchToWindow(self.CurrentWindow)
        self.current_index_changed.emit(self.ProcessIndex)

    def __DecrementIndex(self):
        if self.ProcessIndex == 0:
            self.ProcessIndex = len(self.Characters) - 1
        else:
            self.ProcessIndex -= 1
        self.CurrentWindow = self.Characters[self.ProcessIndex]
        CW.switchToWindow(self.CurrentWindow)
        self.current_index_changed.emit(self.ProcessIndex)

    def __LoopIndex(self, action):
        position = self.Mouse.position
        for i in range(len(self.Characters)):
            self.ProcessIndex = i
            self.CurrentWindow = self.Characters[self.ProcessIndex]
            CW.switchToWindow(self.CurrentWindow)
            if action == "double_click":
                time.sleep(0.2)
                keyboard.press_and_release("space")
                keyboard.write(f"{pyperclip.paste()}")
                time.sleep(0.1)
                keyboard.press_and_release("enter")
                time.sleep(0.1)
                keyboard.press_and_release("enter")

            elif action == "click":
                self.Mouse.position = position
                self.Mouse.press(Button.left)
                time.sleep(self.delay / 2000)
                self.Mouse.release(Button.left)
                time.sleep(self.delay / 1000)
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
        if self.KeyboardHandlerStatus:
            self.CurrentWindow = self.Characters[self.ProcessIndex]
            CW.switchToWindow(self.CurrentWindow)
        return self.KeyboardHandlerStatus

    def on_click(self, x, y, button, pressed):
        if pressed:
            for key, val in self.mKeys.items():
                if val in str(button):
                    self.__InputAction(key)
                    while pressed:
                        time.sleep(0.1)

    def __KeyboardHandler(self):
        while True:
            time.sleep(0.01)
            if self.KeyboardHandlerStatus:
                for key, val in self.kbKeys.items():
                    if keyboard.is_pressed(val):
                        self.__InputAction(key)
                        while keyboard.is_pressed(val):
                            time.sleep(.01)


##################################################
# For debug usage only
##################################################

if __name__ == "__main__":
    Organizer = Organizer()
