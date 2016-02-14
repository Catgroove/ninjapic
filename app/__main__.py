from surface import Surface
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import (QApplication, QSystemTrayIcon, QIcon, QMenu, QAction,
                         QKeySequence, QInputDialog, QLineEdit)
from imgurpython import ImgurClient
from pygs import QxtGlobalShortcut

import os
import sys
import webbrowser


class trayApp(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(trayApp, self).__init__(parent)
        self.loadSettings()
        self.setIcon(QIcon("icon.png"))
        self.createSysTrayMenu()
        self.createSysTrayActions()
        self.setGlobalHotkeys()
        self.imgurClient = ImgurClient("", "")
        self.clipboard = QApplication.clipboard()

    def createSysTrayMenu(self):
        self.sysTrayMenu = QMenu()
        self.setContextMenu(self.sysTrayMenu)

    def createSysTrayActions(self):
        self.sysTrayMenuRegionAction = self.createAction("&Capture region", self.createDrawSurface, self.hotkey)
        self.sysTrayMenuHotkeyAction = self.createAction("&Change hotkey...", self.changeHotkey)
        self.sysTrayMenuUploadAction = self.createAction("&Upload to imgur", checkable=True)
        self.sysTrayMenuUploadAction.setChecked(self.upload)
        self.sysTrayMenuSaveAction = self.createAction("&Save locally", checkable=True)
        self.sysTrayMenuSaveAction.setChecked(self.save)
        self.sysTrayMenuExitAction = self.createAction("&Exit", self.quit)

        self.addActions(self.sysTrayMenu, (self.sysTrayMenuRegionAction,
                                           None,
                                           self.sysTrayMenuHotkeyAction,
                                           self.sysTrayMenuUploadAction,
                                           self.sysTrayMenuSaveAction,
                                           self.sysTrayMenuExitAction))

    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False):
        action = QAction(text, self)
        if slot is not None:
            action.triggered.connect(slot)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icon is not None:
            action.setIcon(QIcon(":/{}.png".format(icon)))
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def changeHotkey(self):
        text, ok = QInputDialog.getText(None, "Change capture hotkey", "Enter a new hotkey (requires restart)", QLineEdit.Normal, self.hotkey)
        if ok:
            self.hotkey = text

    def loadSettings(self):
        settings = QSettings("ninjapic", "settings")
        self.upload = settings.value("upload").toBool()
        self.save = settings.value("save").toBool()
        self.hotkey = settings.value("hotkey").toString()
        if not self.hotkey:
            self.hotkey = "Alt+C"

    def saveSettings(self):
        settings = QSettings("ninjapic", "settings")
        settings.setValue("upload", self.sysTrayMenuUploadAction.isChecked())
        settings.setValue("save", self.sysTrayMenuSaveAction.isChecked())
        settings.setValue("hotkey", self.hotkey)

    def createDrawSurface(self):
        self.surface = Surface()
        self.surface.imageReady.connect(self.storeImage)
        self.surface.show()

    def setGlobalHotkeys(self):
        self.sysTrayMenuRegionGlobalHotkey = QxtGlobalShortcut()
        self.sysTrayMenuRegionGlobalHotkey.setShortcut(QKeySequence(self.hotkey))
        self.sysTrayMenuRegionGlobalHotkey.activated.connect(self.createDrawSurface)

    def storeImage(self):
        if not self.surface.image.save("screenshot.png", "PNG", -1):
            return "Couldn't save image: Something went wrong."
        if self.upload:
            uploaded_image = self.imgurClient.upload_from_path("screenshot.png")
            if uploaded_image:
                link = uploaded_image["link"]
                self.clipboard.setText(link)
                webbrowser.open(link)
        if not self.save:
            os.remove("screenshot.png")

    def quit(self):
        self.saveSettings()
        self.deleteLater()
        QApplication.exit()


def main():
    app = QApplication(sys.argv, quitOnLastWindowClosed=False)
    tray_app = trayApp()
    tray_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
