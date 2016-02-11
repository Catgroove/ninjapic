from helpers import getScreenDimensions

from PyQt4.QtCore import QRect
from PyQt4.QtGui import QApplication, QPixmap

import sys

class Screenshot(object):
    def captureFullScreen(self):
        rect = getScreenDimensions()
        return self.captureRectangle(rect)

    def captureRectangle(self, qrect):
        if qrect.width == 0 or qrect.height == 0:
            return None
        return QPixmap.grabWindow(QApplication.desktop().winId(), *qrect.getRect())
