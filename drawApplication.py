# importing libraries
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets  # QtWidgets for QApplication
import sys


# =============================================================================
# Window- Main Window for the application
# ===============================================================================
class Window(QtWidgets.QMainWindow):
    # Constructor :-
    def __init__():
        # setting title
        self.setWindowTitle("Paint with PyQt6")

        # setting geometry to main window
        self.setGeometry(100, 100, 800, 600)

        # creating image object
        self.image = QtGui.QImage(
            self.size(), QtGui.QImage.Format.Format_RGB32)

        # making image color to white
        # self.image.fill(QtCore.Qt.GlobalColor.white)

        # variables
        # drawing flag
        self.drawing = False
        # default brush size
        self.brushSize = 2
        # default color
        self.brushColor = QtCore.Qt.GlobalColor.black

        # QPoint object to tract the point
        self.lastPoint = QtCore.QPoint()

        # creating menu bar
        mainMenu = self.menuBar()

        # creating file menu for save and clear action
        fileMenu = mainMenu.addMenu("File")

        # adding brush size to main menu
        b_size = mainMenu.addMenu("Brush Size")

        # adding brush color to ain menu
        b_color = mainMenu.addMenu("Brush Color")

        # creating save action
        saveAction = QtGui.QAction("Save", self)
        # adding short cut for save action
        saveAction.setShortcut("Ctrl + S")
        # adding save to the file menu
        fileMenu.addAction(saveAction)
        # adding action to the save
        saveAction.triggered.connect(self.save)

        # creating clear action
        clearAction = QtGui.QAction("Clear", self)
        # adding short cut to the clear action
        clearAction.setShortcut("Ctrl + C")
        # adding clear to the file menu
        fileMenu.addAction(clearAction)
        # adding action to the clear
        clearAction.triggered.connect(self.clear)

        # creating options for brush sizes
        # creating action for selecting pixel of 4px
        pix_4 = QtGui.QAction("4px", self)
        # adding this action to the brush size
        b_size.addAction(pix_4)
        # adding method to this
        pix_4.triggered.connect(self.Pixel_4)

        # similarly repeating above steps for different sizes
        pix_7 = QtGui.QAction("7px", self)
        b_size.addAction(pix_7)
        pix_7.triggered.connect(self.Pixel_7)

        pix_9 = QtGui.QAction("9px", self)
        b_size.addAction(pix_9)
        pix_9.triggered.connect(self.Pixel_9)

        pix_12 = QtGui.QAction("12px", self)
        b_size.addAction(pix_12)
        pix_12.triggered.connect(self.Pixel_12)

        # creating options for brush color
        # creating action for black color
        black = QtGui.QAction("Black", self)
        # adding this action to the brush colors
        b_color.addAction(black)
        # adding methods to the black
        black.triggered.connect(self.blackColor)

        # creating action for white color
        white = QtGui.QAction("Eraser", self)
        b_color.addAction(white)
        white.triggered.connect(self.whiteColor)

        # similarly repeating above steps for different color
        blue = QtGui.QAction("Blue", self)
        b_color.addAction(blue)
        blue.triggered.connect(self.blueColor)

        green = QtGui.QAction("Green", self)
        b_color.addAction(green)
        green.triggered.connect(self.greenColor)

        yellow = QtGui.QAction("Yellow", self)
        b_color.addAction(yellow)
        yellow.triggered.connect(self.yellowColor)

        red = QtGui.QAction("Red", self)
        b_color.addAction(red)
        red.triggered.connect(self.redColor)
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
    def Pixel_4(self):
        self.brushSize = 4

    def Pixel_7(self):
        self.brushSize = 7

    def Pixel_9(self):
        self.brushSize = 9

    def Pixel_12(self):
        self.brushSize = 12

    # methods for changing brush color
    def blackColor(self):
        self.brushColor = QtCore.Qt.GlobalColor.black

    def blueColor(self):
        self.brushColor = QtCore.Qt.GlobalColor.blue

    def greenColor(self):
        self.brushColor = QtCore.Qt.GlobalColor.green

    def yellowColor(self):
        self.brushColor = QtCore.Qt.GlobalColor.yellow

    def redColor(self):
        self.brushColor = QtCore.Qt.GlobalColor.red

    def whiteColor(self):
        self.brushColor = QtCore.Qt.GlobalColor.white


# create pyqt5 app
App = QtWidgets.QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing the window
window.show()

# start the app
sys.exit(App.exec())
