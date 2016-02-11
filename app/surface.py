from helpers import cropImage, getScreenDimensions
from screenshot import Screenshot

from PyQt4.QtCore import Qt, QRect, QSize, QPoint, pyqtSignal, QObject
from PyQt4.QtGui import QLabel, QApplication, QCursor, QRubberBand

import sys


class Surface(QLabel):
    imageReady = pyqtSignal(object)

    def __init__(self, parent=None):
        super(Surface, self).__init__(parent)
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        self.setCursor(QCursor(Qt.CrossCursor))
        self.setGeometry(getScreenDimensions())
        self.prepareSurface()

    def prepareSurface(self):
        """Cover the entire screen with a screenshot of the screen."""
        self.surfaceImage = Screenshot().captureFullScreen()
        self.setPixmap(self.surfaceImage)
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)

    def mousePressEvent(self, event):
        """Creates the starting point in any corner of a rectangle."""
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubberband.setGeometry(QRect(self.origin, QSize()))
            self.rubberband.show()
        if event.button() == Qt.RightButton and self.rubberband.isVisible():
            self.dispose()

    def keyPressEvent(self, event):
        """Adds hotkey cancel functionality."""
        if event.key() == Qt.Key_Escape:
            self.dispose()

    def mouseMoveEvent(self, event):
        """Expands the rectangle created in mousePressEvent to the mouse location."""
        if self.rubberband.isVisible():
            self.rubberband.setGeometry(
                QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        """Takes a screenshot of region specified by the rectangle created with mousePressEvent & mouseMoveEvent."""
        if self.rubberband.isVisible():
            printRect = QRect(QPoint(self.origin.x(), self.origin.y()), QPoint(event.pos().x(), event.pos().y()))
            self.image = cropImage(self.surfaceImage, printRect)
            self.imageReady.emit("QPixmap ready")
            self.dispose()

    def dispose(self):
        """General clean-up of the QWidget and its children."""
        self.rubberband.hide()
        self.hide()
        self.deleteLater()
