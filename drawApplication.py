# importing libraries
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets  # QtWidgets for QApplication
from PyQt6.QtGui import QPen

from menuBar import MenuBar
from toolBar import ToolBar
from drawingBoard import DrawingCanvas
from drawingBoard import DrawingView
import sys


# =============================================================================
# Window- Main Window for the application
# ===============================================================================
class Window(QtWidgets.QMainWindow):
    # Constructor :-
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # basic frame of the UI including menu bar
        self.__initVars()
        # setting title
        self.setWindowTitle("Paint with PyQt6")
        # setting geometry to main window
        self.setGeometry(100, 100, 800, 600)
        self.__initWidgets()
        self.__arrageWidgets()
        self.__connectWidgets()
        # creating menu bar
        self.__menu = MenuBar(self.menuBar(), self)
        self.__status = self.statusBar()

    def __initWidgets(self):
        cw = QtWidgets.QWidget()
        self.setCentralWidget(cw)
        self.__layout = QtWidgets.QHBoxLayout()
        cw.setLayout(self.__layout)
        self.__tb = ToolBar()
        self.__dc = DrawingCanvas(self.__tb)
        self.__v = DrawingView()
        self.__v.setScene(self.__dc)

    def __arrageWidgets(self):
        self.__layout.addWidget(self.__tb)
        self.__layout.addWidget(self.__v)

    def __initVars(self):
        # creating image object
        self.image = QtGui.QImage(
            self.size(), QtGui.QImage.Format.Format_RGB32)
        # making image color to white
        self.image.fill(QtCore.Qt.GlobalColor.white)
        # variables
        # drawing flag
        self.drawing = False
        # default brush size
        self.brushSize = 2
        # default color
        self.brushColor = QtCore.Qt.GlobalColor.black
        # QPoint object to tract the point
        self.lastPoint = QtCore.QPoint()

# |--------------------------End of Constructor--------------------------------|
    def __connectWidgets(self):
        # connect the signals to the slots
        self.__v.zoomEvent.connect(self.__zoomStatus)

    def __zoomStatus(self, zoom):
        self.__status.showMessage("Zoom : " + str(zoom))
    # paint event

    def paintEvent(self, event):
        # create a canvas
        canvasPainter = QtGui.QPainter(self)

        # draw rectangle on the canvas
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # method for saving canvas
    def save(self):
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "",
                                                            "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)

    # method for clearing every thing on canvas
    def clear(self):
        # make the whole canvas white
        self.image.fill(QtCore.Qt.GlobalColor.white)
        # update
        self.update()

    # methods for changing pixel sizes

    def changeSize(self):
        size = int(self.sender().text().replace("px", ""))
        self.brushSize = size

    # methods for changing colors
    def changeColor(self):
        col = QtGui.QColor(0, 0, 0)
        col.setNamedColor(self.sender().text().lower())
        self.brushColor = col


# create pyqt5 app
App = QtWidgets.QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing the window
window.show()

# start the app
sys.exit(App.exec())
