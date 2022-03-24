from PyQt6 import QtCore  # QtWidgets for QApplication
from PyQt6 import QtWidgets  # QtWidgets for QApplication
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPen
from PyQt6.QtGui import QIcon
from enum import Enum
MeasureSystem = Enum('MeasureSystem', 'Metric Imperial')


class ToolBar(QtWidgets.QWidget):
    scrollMode = QtCore.pyqtSignal(bool)

    def __init__(self, dpi=150):
        super().__init__()
        self.__dpi = dpi
        self.penSize = 1
        self.color = QColor("black")
        self.selectedItem = None
        self.pen = QPen(self.color, self.penSize,
                        QtCore.Qt.PenStyle.SolidLine, QtCore.Qt.PenCapStyle.RoundCap, QtCore.Qt.PenJoinStyle.RoundJoin)
        self.measurePen = QPen(self.color, self.penSize,
                               QtCore.Qt.PenStyle.DashLine, QtCore.Qt.PenCapStyle.FlatCap, QtCore.Qt.PenJoinStyle.RoundJoin)
        self.__initWidgets()
        self.__arrageWidgets()
        self.__connectWidgets()
        self._ratio = 1

    def __initWidgets(self):
        self.__colors = ["black", "white", "blue", "green",
                         "red", "yellow", "orange", "purple", "brown", "pink"]
        self.__sizes = ["1px", "2px", "3px", "4px",
                        "5px", "6px", "7px", "8px", "9px", "10px"]
        self.__shapes = ["line", "ellipse", "rectangle", "freehand", "measure"]

        self.__colorGrp = QtWidgets.QGroupBox("Colors")
        self.__sizeGrp = QtWidgets.QGroupBox("Pen Size")
        self.__drawShapeGrp = QtWidgets.QGroupBox("Draw Shape")
        self.__measureSystemGrp = QtWidgets.QGroupBox("Measure System")

        self.selectedItem = "line"
        self.__measureSystem = MeasureSystem.Metric

    def __arrageWidgets(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.__colorGrp.setLayout(QtWidgets.QGridLayout())
        self.__sizeGrp.setLayout(QtWidgets.QGridLayout())
        self.__measureSystemGrp.setLayout(QtWidgets.QGridLayout())
        self.__drawShapeGrp.setLayout(QtWidgets.QGridLayout())
        for i, color in enumerate(self.__colors):
            w = QtWidgets.QPushButton(parent=self.__colorGrp)
            w.setObjectName(color)
            w.setCheckable(True)
            w.setToolTip(color)
            w.setStyleSheet("background-color:"+color)
            if not i:
                w.setChecked(True)
            self.__colorGrp.layout().addWidget(w, i//2, i % 2)
        layout.addWidget(self.__colorGrp)

        for i, size in enumerate(self.__sizes):
            w = QtWidgets.QPushButton(size, parent=self.__sizeGrp)
            w.setCheckable(True)
            w.setObjectName(size)
            if not i:
                w.setChecked(True)
            self.__sizeGrp.layout().addWidget(w, i//2, i % 2)
        layout.addWidget(self.__sizeGrp)

        for i, shape in enumerate(self.__shapes):
            w = QtWidgets.QPushButton(parent=self.__drawShapeGrp)
            w.setObjectName(shape)
            w.setCheckable(True)
            w.setIcon(QIcon("./icons/"+shape+".png"))
            w.setToolTip(shape)
            self.__drawShapeGrp.layout().addWidget(w, i//2, i % 2)
        layout.addWidget(self.__drawShapeGrp)

        for i, system in enumerate(MeasureSystem):
            w = QtWidgets.QPushButton(
                system.name, parent=self.__measureSystemGrp)
            w.setObjectName(system.name)
            w.setCheckable(True)
            if not i:
                w.setChecked(True)
            self.__measureSystemGrp.layout().addWidget(w, i//2, i % 2)
        layout.addWidget(self.__measureSystemGrp)

        layout.addStretch(1)

    def __connectWidgets(self):
        for child in self.__colorGrp.children():
            if isinstance(child, QtWidgets.QPushButton):
                child.clicked.connect(self.__setColor)
        for child in self.__sizeGrp.children():
            if isinstance(child, QtWidgets.QPushButton):
                child.clicked.connect(self.__setPenSize)
        for child in self.__drawShapeGrp.children():
            if isinstance(child, QtWidgets.QPushButton):
                child.clicked.connect(self.__setSelectedItem)
        for child in self.__measureSystemGrp.children():
            if isinstance(child, QtWidgets.QPushButton):
                child.clicked.connect(self.__setMeasureSystem)

    def __setColor(self):
        self.color = QColor(self.sender().objectName())
        self.pen.setColor(self.color)
        for btn in self.__colorGrp.children():
            if isinstance(btn, QtWidgets.QPushButton):
                if btn.objectName() != self.sender().objectName():
                    btn.setChecked(False)

    def __setSelectedItem(self):
        if self.sender().objectName() == self.selectedItem:
            self.selectedItem = None
        else:
            self.selectedItem = self.sender().objectName()
        for btn in self.__drawShapeGrp.children():
            if isinstance(btn, QtWidgets.QPushButton):
                if btn.objectName() != self.sender().objectName():
                    btn.setChecked(False)
        if not self.selectedItem:
            self.scrollMode.emit(True)
        else:
            self.scrollMode.emit(False)

    def __setPenSize(self):
        self.penSize = int(self.sender().text()[:-2])
        self.pen.setWidth(self.penSize)
        for btn in self.__sizeGrp.children():
            if isinstance(btn, QtWidgets.QPushButton):
                if btn.text() != self.sender().text():
                    btn.setChecked(False)

    def __setMeasureSystem(self):
        self.__measureSystem = MeasureSystem[self.sender().text()]
        for btn in self.__measureSystemGrp.children():
            if isinstance(btn, QtWidgets.QPushButton):
                if btn.text() != self.sender().text():
                    btn.setChecked(False)

    def pix2Met(self, pix):
        if self.__measureSystem == MeasureSystem.Metric:
            v = 2.54*pix/self.__dpi
            if v > 100:
                text = "{}m {:.2f}cm".format(v//100, v - 100 * (v//100))
            else:
                text = "{:.2f}cm".format(v)
        if self.__measureSystem == MeasureSystem.Imperial:
            v = pix/self.__dpi
            if v > 12:
                text = "{}ft {:.2f}in".format(v//12, v - 12 * (v//12))
            else:
                text = "{:.2f}in".format(v)
        return text
