from PyQt4.QtCore import QRect
from PyQt4.QtGui import QApplication, QPixmap


def getScreenDimensions():
    """Returns the posx, posy, width and height of the monitor as a QRect."""
    return QRect(QApplication.desktop().x(),
                 QApplication.desktop().y(),
                 QApplication.desktop().width(),
                 QApplication.desktop().height())


def cropImage(qpixmap, qrect):
    """Returns a cropped QPixmap using the QRect as dimensions."""
    if qrect.width == 0 or qrect.height == 0:
        return None
    return qpixmap.copy(qrect.normalized())


def captureFullScreen():
    """Returns a QPixmap containing a screenshot of the entire screen."""
    rect = getScreenDimensions()
    return captureRectangle(rect)


def captureRectangle(qrect):
    """Returns a QPixmap containing a screenshot the size of qrect."""
    if qrect.width == 0 or qrect.height == 0:
        return None
    return QPixmap.grabWindow(QApplication.desktop().winId(), *qrect.getRect())
