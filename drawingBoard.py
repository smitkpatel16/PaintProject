from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6 import QtCore
from PyQt6 import QtGui


# ===============================================================================
# DrawingView-
# ===============================================================================
class DrawingView(QGraphicsView):
    zoomEvent = QtCore.pyqtSignal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__scaleFactor = 1.0
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

    def wheelEvent(self, event):

        setScale = False
        if event.angleDelta().y() > 0 and self.__scaleFactor < 2:
            self.__scaleFactor += 0.1
            setScale = True
        elif self.__scaleFactor > 0.5 and event.angleDelta().y() < 0:
            self.__scaleFactor -= 0.1
            setScale = True
        if setScale:
            self.resetTransform()
            self.scale(self.__scaleFactor, self.__scaleFactor)
            self.zoomEvent.emit(self.__scaleFactor)
        print(self.__scaleFactor)
        return super().wheelEvent(event)


# ===============================================================================
# DrawingCanvas-
# ===============================================================================
class DrawingCanvas(QGraphicsScene):
    movePosition = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self, toolBar):
        super().__init__()
        self.toolBar = toolBar
        self.drawing = False
        self.__currentDraw = None
        self.__firstPoint = None
        self.setSceneRect(0, 0, 250, 250)

    # method for checking mouse cicks
    def mousePressEvent(self, event):
        # if left mouse button is pressed
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.toolBar.selectedItem:
            # make drawing flag true
            self.drawing = True
        return super().mousePressEvent(event)

    # method for tracking mouse activity
    def mouseMoveEvent(self, event):
        self.movePosition.emit(event.scenePos())
        # checking if left button is pressed and drawing flag is true
        if (event.buttons() and QtCore.Qt.MouseButton.LeftButton) and self.drawing:
            if not self.__firstPoint:
                self.__firstPoint = event.scenePos()
            if self.__currentDraw:
                self.removeItem(self.__currentDraw)
            if self.toolBar.selectedItem == "-":
                self.__currentDraw = self.addLine(self.__firstPoint.x(),
                                                  self.__firstPoint.y(),
                                                  event.scenePos().x(),
                                                  event.scenePos().y(),
                                                  self.toolBar.pen)
            if self.toolBar.selectedItem == "O":
                self.__currentDraw = self.addEllipse(self.__firstPoint.x(),
                                                     self.__firstPoint.y(),
                                                     event.scenePos().x()-self.__firstPoint.x(),
                                                     event.scenePos().y()-self.__firstPoint.y(),
                                                     self.toolBar.pen)
            if self.toolBar.selectedItem == "[]":
                self.__currentDraw = self.addRect(self.__firstPoint.x(),
                                                  self.__firstPoint.y(),
                                                  event.scenePos().x()-self.__firstPoint.x(),
                                                  event.scenePos().y()-self.__firstPoint.y(),
                                                  self.toolBar.pen)
            # if self.toolBar.selectedItem == "@":
            #     if not self.__currentDraw:
            #         self.__currentDraw = self.addItem(QtGui.QGraphicsPathItem)
            #     self.addItem()
            #     self.__currentDraw = self.addLine(self.__firstPoint.x(),
            #                                       self.__firstPoint.y(),
            #                                       event.scenePos().x(),
            #                                       event.scenePos().y(),
            #                                       self.toolBar.pen)
            #     self.__firstPoint = event.scenePos()
            # update
            self.update()
        return super().mouseMoveEvent(event)

    # method for mouse left button release
    def mouseReleaseEvent(self, event):
        # if left button is released
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.drawing:
                self.__currentDraw.setFlag(
                    QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            # make drawing flag false
            self.drawing = False
            self.__firstPoint = None
            self.__currentDraw = None
        return super().mouseReleaseEvent(event)
