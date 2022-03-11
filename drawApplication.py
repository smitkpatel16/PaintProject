# importing libraries
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets  # QtWidgets for QApplication
from menuBar import MenuBar
from toolBar import Toolbar
from drawingCanvas import DrawingCanvas
import sys


# =============================================================================
# Window- Main Window for the application
# ===============================================================================
class Window(QtWidgets.QMainWindow):
    # Constructor :-
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #basic frame of the UI including menu bar
        self.__initUI()
        self.__initVars()

    def __initUI(self):        
        # setting title
        self.setWindowTitle("Paint with PyQt6")
        # setting geometry to main window
        self.setGeometry(100, 100, 800, 600)
            # creating menu bar
        self.__menu = MenuBar(self.menuBar(),self)

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

    # method for checking mouse cicks

    def mousePressEvent(self, event):

        # if left mouse button is pressed
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # make drawing flag true
            self.drawing = True
            # make last point to the point of cursor
            self.lastPoint = event.pos()

    # method for tracking mouse activity
    def mouseMoveEvent(self, event):

        # checking if left button is pressed and drawing flag is true
        if (event.buttons() and QtCore.Qt.MouseButton.LeftButton) and self.drawing:

            # creating painter object
            painter = QtGui.QPainter(self.image)

            # set the pen of the painter
            painter.setPen(QtGui.QPen(self.brushColor, self.brushSize,
                                      QtCore.Qt.PenStyle.SolidLine, QtCore.Qt.PenCapStyle.RoundCap, QtCore.Qt.PenJoinStyle.RoundJoin))

            # draw line from the last point of cursor to the current point
            # this will draw only one step
            painter.drawLine(self.lastPoint, event.pos())

            # change the last point
            self.lastPoint = event.pos()
            # update
            self.update()

    # method for mouse left button release
    def mouseReleaseEvent(self, event):

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # make drawing flag false
            self.drawing = False

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
        size = int(self.sender().text().replace("px",""))
        self.brushSize = size
        
    # methods for changing colors
    def changeColor(self):
        col = QtGui.QColor(0,0,0)
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
