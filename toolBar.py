from PyQt6 import QtCore  # QtWidgets for QApplication
from PyQt6 import QtWidgets  # QtWidgets for QApplication
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPen


class ToolBar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.penSize = 1
        self.color = QColor("black")
        self.selectedItem = None
        self.pen = QPen(self.color, self.penSize,
                        QtCore.Qt.PenStyle.SolidLine, QtCore.Qt.PenCapStyle.RoundCap, QtCore.Qt.PenJoinStyle.RoundJoin)

        self.__initWidgets()
        self.__arrageWidgets()

    def __initWidgets(self):
        self.__colors = ["black", "white", "blue", "green",
                         "red", "yellow", "orange", "purple", "brown", "pink"]
        self.__line = QtWidgets.QPushButton("-")
        self.__ellipses = QtWidgets.QPushButton("O")
        self.__rectangles = QtWidgets.QPushButton("[]")
        self.__selectedItemBtns = [self.__line,
                                   self.__ellipses, self.__rectangles]
        for btn in self.__selectedItemBtns:
            btn.setCheckable(True)
            btn.clicked.connect(self.__setSelectedItem)
        self.__colorBtns = []
        self.selectedItem = self.__line.text()
        self.__line.setChecked(True)

    def __arrageWidgets(self):
        self.__layout = QtWidgets.QGridLayout()
        self.setLayout(self.__layout)
        for i, color in enumerate(self.__colors):
            btn = QtWidgets.QPushButton()
            btn.setObjectName(color)
            btn.setCheckable(True)
            btn.setToolTip(color)
            btn.setStyleSheet("background-color:"+color)
            btn.clicked.connect(self.__setColor)
            self.__layout.addWidget(btn, i//2, i % 2)
            self.__colorBtns.append(btn)
            if not i:
                btn.setChecked(True)
                self.color = QColor(color)
        self.__layout.addWidget(self.__line, len(self.__colors)//2, 0)
        self.__layout.addWidget(self.__ellipses, len(self.__colors)//2, 1)
        self.__layout.addWidget(self.__rectangles, len(self.__colors)//2+1, 0)

        self.__layout.setRowStretch(len(self.__colors)//2+2, 1)

    def __setColor(self):
        self.color = QColor(self.sender().objectName())
        self.pen.setColor(self.color)
        for btn in self.__colorBtns:
            if btn.objectName() != self.sender().objectName():
                btn.setChecked(False)

    def __setSelectedItem(self):
        self.selectedItem = self.sender().text()
        for btn in self.__selectedItemBtns:
            if btn.text() != self.sender().text():
                btn.setChecked(False)
