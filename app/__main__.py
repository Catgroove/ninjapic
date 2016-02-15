from surface import Surface
from custom_widgets import KeySequenceDialog
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import (QApplication, QSystemTrayIcon, QIcon, QMenu, QAction,
                         QKeySequence, QInputDialog, QLineEdit, QMessageBox)
from pyimgur import Imgur
from pygs import QxtGlobalShortcut
from requests.exceptions import HTTPError

import os
import sys
import webbrowser


class trayApp(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(trayApp, self).__init__(parent)
        self.loadSettings()
        self.setIcon(QIcon("icon.png"))
        self.createSysTrayMenu()
        self.setGlobalHotkeys()
        self.imgurClient = Imgur("", "")
        self.clipboard = QApplication.clipboard()

    def createSysTrayMenu(self):
        self.sysTrayMenu = QMenu()
        self.setContextMenu(self.sysTrayMenu)
        self.createSysTrayActions()

    def createSysTrayActions(self):
        self.sysTrayMenuRegionAction = self.createAction("&Capture region", self.createDrawSurface, self.hotkey)
        self.sysTrayMenuHotkeyAction = self.createAction("&Change hotkey...", self.createKeySequenceDialog)
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

    def createKeySequenceDialog(self):
        self.keySequenceDialog = KeySequenceDialog(self.hotkey)
        self.keySequenceDialog.accepted.connect(self.changeHotkey)
        self.keySequenceDialog.show()

    def changeHotkey(self):
        text = self.keySequenceDialog.keySequenceLineEdit.text()
        if text:
            self.hotkey = text
            self.sysTrayMenuRegionAction.setShortcut(self.hotkey)
            self.sysTrayMenuRegionGlobalHotkey.setShortcut(QKeySequence(self.hotkey))

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
            QMessageBox.warning(None, "Image Error", "The image couldn't be saved.")
            return
        if self.sysTrayMenuUploadAction.isChecked():
            try:
                uploaded_image = self.imgurClient.upload_image("screenshot.png")
                self.clipboard.setText(uploaded_image.link)
                webbrowser.open(uploaded_image.link)
            except HTTPError, e:
                self.surface.dispose()
                QMessageBox.warning(None, "Imgur Error", unicode(e))
        if not self.sysTrayMenuSaveAction.isChecked():
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
