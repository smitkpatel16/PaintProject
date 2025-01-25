# importing libraries
import sys
import fitz

from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets  # QtWidgets for QApplication
from PyQt6.QtGui import QPixmap, QImage

from MenuBar import MenuBar
from ToolBar import ToolBar
from DrawingBoard import DrawingCanvas
from DrawingBoard import DrawingView
from Interactions import Interactions


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
        # shortcut
        self.__undoAction = QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+Z"), self)
        self.__redoAction = QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+Y"), self)
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
# |--------------------------End of Constructor--------------------------------|

    def __initWidgets(self):
        cw = QtWidgets.QWidget()
        self.setCentralWidget(cw)
        self.__layout = QtWidgets.QHBoxLayout()
        cw.setLayout(self.__layout)
        self.__tb = ToolBar(dpi=self.__dpi)
        self.__dc = DrawingCanvas(self.__tb)
        self.__v = DrawingView()
        self.__v.setScene(self.__dc)
        # integrating interaction to take final actions
        # to be used for undo/redo
        self.__interaction = Interactions(canvas=self.__dc, view=self.__v)

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

    def __connectWidgets(self):
        # connect the signals to the slots
        self.__v.zoomEvent.connect(self.__zoomStatus)
        self.__dc.itemAdded.connect(self.__interaction.itemAdded)
        self.__tb.scrollMode.connect(self.__v.setScrollMode)
        self.__undoAction.activated.connect(self.__interaction.undo)
        self.__redoAction.activated.connect(self.__interaction.redo)

    def __zoomStatus(self, zoom):
        self.__status.showMessage("Zoom : " + str(zoom))
    # paint event

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
        self.__interaction.clear()
    # methods for changing pixel sizes
    # import pdf and convert to image

    def importPDF(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Import PDF", "",
                                                            "PDF(*.pdf);;All Files(*.*) ")
        if filePath == "":
            return
        doc = fitz.open(filePath)
        page = doc.load_page(0)  # number of page
        pix = page.get_pixmap(alpha=False)
        pm = QPixmap.fromImage(QImage.fromData(pix.tobytes(output="png")))
        self.__interaction.importPDF(pm=pm)


# create pyqt5 app
App = QtWidgets.QApplication(sys.argv)

# create the instance of our Window
window = Window(dpi=(App.primaryScreen().physicalDotsPerInchY() +
                App.primaryScreen().physicalDotsPerInchX())/2)

# showing the window
window.show()

# start the app
sys.exit(App.exec())
