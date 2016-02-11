from PyQt4.QtCore import QRect
from PyQt4.QtGui import QApplication

def getScreenDimensions():
    """Returns the posx, posy, width and height of the monitor(s) as a QRect."""
    return QRect(QApplication.desktop().x(),
            QApplication.desktop().y(),
            QApplication.desktop().width(),
            QApplication.desktop().height())

def cropImage(qpixmap, qrect):
    """Returns a cropped QPixmap using the QRect as dimensions."""
    if qrect.width == 0 or qrect.height == 0:
        return None
    return qpixmap.copy(qrect.normalized())
