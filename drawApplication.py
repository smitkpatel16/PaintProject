# importing libraries
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets  # QtWidgets for QApplication
from PyQt6.QtGui import QPixmap, QImage
import fitz

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
    def __init__(self, dpi=150):
        super().__init__()
        self.__dpi = dpi
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
        MenuBar(self.menuBar(), self)
        self.__status = self.statusBar()

    def __initWidgets(self):
        cw = QtWidgets.QWidget()
        self.setCentralWidget(cw)
        self.__layout = QtWidgets.QHBoxLayout()
        cw.setLayout(self.__layout)
        self.__tb = ToolBar(dpi=self.__dpi)
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
        self.__dc.movePosition.connect(self.__positionStatus)
        self.__dc.measurement.connect(self.__measurement)
        self.__tb.scrollMode.connect(self.__v.setScrollMode)

    def __measurement(self, m):
        self.__status.showMessage(m)

    def __zoomStatus(self, zoom):
        self.__status.showMessage("Zoom : " + str(zoom))
    # paint event

    def __positionStatus(self, pos):
        self.__status.showMessage(
            "Position : " + str(pos.x()) + "," + str(pos.y()))

    # method for saving canvas
    def save(self):
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "",
                                                            "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        area = self.__dc.itemsBoundingRect().toRect()
        image = QtGui.QImage(
            area.size(), QtGui.QImage.Format.Format_ARGB4444_Premultiplied)
        painter = QtGui.QPainter(image)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        r = image.rect()
        self.__dc.render(painter, QtCore.QRectF(
            r.x(), r.y(), r.width(), r.height()), QtCore.QRectF(
            area.x(), area.y(), area.width(), area.height()))
        painter.end()
        image.save(filePath)

    # method for clearing every thing on canvas
    def clear(self):
        self.__dc.clear()
        self.__v.update()

    # methods for changing pixel sizes
    # import pdf and convert to image
    def importPDF(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import PDF", "",
                                                            "PDF(*.pdf);;All Files(*.*) ")
        if filePath == "":
            return

        doc = fitz.open(filePath)
        page = doc.loadPage(0)  # number of page
        pix = page.get_pixmap(alpha=False)
        pm = QPixmap.fromImage(QImage.fromData(pix.tobytes(output="png")))
        pm = self.__dc.addPixmap(pm)
        pm.setPos(0, 0)
        self.__v.update()


# create pyqt5 app
App = QtWidgets.QApplication(sys.argv)

# create the instance of our Window
window = Window(dpi=(App.primaryScreen().physicalDotsPerInchY() +
                App.primaryScreen().physicalDotsPerInchX())/2)

# showing the window
window.show()

# start the app
sys.exit(App.exec())
