from PyQt4.QtGui import (QDialog, QLineEdit, QLabel, QBoxLayout, QKeySequence,
                         QDialogButtonBox)
from PyQt4.QtCore import QEvent, Qt


class KeySequenceDialog(QDialog):
    def __init__(self, keySequence, parent=None):
        super(KeySequenceDialog, self).__init__(parent)
        self.keySequence = keySequence
        self.createWidgets()
        self.layoutWidgets()
        self.createConnections()
        self.setWindowTitle("Change capture hotkey")

    def createWidgets(self):
        self.keySequenceLabel = QLabel("Enter a new hotkey")
        self.keySequenceLineEdit = KeySequenceEdit(QKeySequence(self.keySequence))
        self.keySequenceButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

    def layoutWidgets(self):
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.addWidget(self.keySequenceLabel)
        layout.addWidget(self.keySequenceLineEdit)
        layout.addWidget(self.keySequenceButtonBox)
        self.setLayout(layout)

    def createConnections(self):
        self.keySequenceButtonBox.accepted.connect(self.accept)
        self.keySequenceButtonBox.rejected.connect(self.reject)


class KeySequenceEdit(QLineEdit):
    # Inspired by http://stackoverflow.com/a/23919177/1234259 and http://stackoverflow.com/a/13491729/1234259
    def __init__(self, keySequence, parent=None):
        super(KeySequenceEdit, self).__init__(parent)
        self.setKeySequence(keySequence)

    def setKeySequence(self, keySequence):
        self.keySequence = keySequence
        self.setText(self.keySequence.toString(QKeySequence.NativeText))
        self.selectAll()

    def keyPressEvent(self, e):
        if e.type() == QEvent.KeyPress:
            key = e.key()

            if key == Qt.Key_unknown:
                return

            if key == Qt.Key_Escape or key == Qt.Key_Backspace:
                self.setText("")
                return

            if (key == Qt.Key_Control or
                key == Qt.Key_Shift or
                key == Qt.Key_Alt or
                key == Qt.Key_Meta):
                return

            modifiers = e.modifiers()
            if modifiers & Qt.ControlModifier:
                key += Qt.CTRL
            if modifiers & Qt.ShiftModifier:
                key += Qt.SHIFT
            if modifiers & Qt.AltModifier:
                key += Qt.ALT
            if modifiers & Qt.MetaModifier:
                key += Qt.META

            self.setKeySequence(QKeySequence(key))
