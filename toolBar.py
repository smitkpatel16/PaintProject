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
        self.__freeHand = QtWidgets.QPushButton("@")
        sizes = ["1px", "2px", "3px", "4px",
                        "5px", "6px", "7px", "8px", "9px", "10px"]
        self.__sizesBtns = []
        for size in sizes:
            self.__sizesBtns.append(QtWidgets.QRadioButton(size))
        self.__selectedItemBtns = [self.__line,
                                   self.__ellipses,
                                   self.__rectangles,
                                   self.__freeHand]
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
        layoutPos = len(self.__colors)//2
        self.__layout.addWidget(self.__line, layoutPos, 0)
        self.__layout.addWidget(self.__ellipses, layoutPos, 1)
        self.__layout.addWidget(self.__rectangles, layoutPos+1, 0)
        self.__layout.addWidget(self.__freeHand, layoutPos+1, 1)
        layoutPos += 2
        for i, btn in enumerate(self.__sizesBtns):
            if not i:
                btn.setChecked(True)
            btn.clicked.connect(self.__setPenSize)
            self.__layout.addWidget(btn, layoutPos+i//2, i % 2)
        layoutPos += len(self.__sizesBtns)//2

        self.__layout.setRowStretch(layoutPos+2, 1)

    def __setColor(self):
        self.color = QColor(self.sender().objectName())
        self.pen.setColor(self.color)
        for btn in self.__colorBtns:
            if btn.objectName() != self.sender().objectName():
                btn.setChecked(False)

    def __setSelectedItem(self):
        if self.sender().text() == self.selectedItem:
            self.selectedItem = None
        else:
            self.selectedItem = self.sender().text()
        for btn in self.__selectedItemBtns:
            if btn.text() != self.sender().text():
                btn.setChecked(False)

    def __setPenSize(self):
        self.penSize = int(self.sender().text()[:-2])
        self.pen.setWidth(self.penSize)
        for btn in self.__sizesBtns:
            if btn.text() != self.sender().text():
                btn.setChecked(False)
