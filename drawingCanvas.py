from PyQt6.QtWidgets import QGraphicsScene
from PyQt6 import QtCore


class DrawingCanvas(QGraphicsScene):
    def __init__(self, toolBar):
        super().__init__()
        self.toolBar = toolBar
        self.__scaleFactor = 1.0
        self.drawing = False
        self.__currentDraw = None
    # method for checking mouse cicks

    def mousePressEvent(self, event):
        # if left mouse button is pressed
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # make drawing flag true
            self.drawing = True
            # make last point to the point of cursor
            self.lastPoint = event.scenePos()
            if self.toolBar.selectedItem == '-':
                self.__currentDraw = self.addLine(self.lastPoint.x(), self.lastPoint.y(
                ), self.lastPoint.x(), self.lastPoint.y(), self.toolBar.pen)
                self.__currentDraw.setPos(
                    self.lastPoint.x(), self.lastPoint.y())

    # method for tracking mouse activity

    def mouseMoveEvent(self, event):
        # checking if left button is pressed and drawing flag is true
        if (event.buttons() and QtCore.Qt.MouseButton.LeftButton) and self.drawing:
            if self.__currentDraw:
                self.removeItem(self.__currentDraw)
            self.__currentDraw = self.addLine(self.lastPoint.x(),
                                              self.lastPoint.y(),
                                              event.scenePos().x(),
                                              event.scenePos().y(),
                                              self.toolBar.pen)
            # update
            self.update()

    # method for mouse left button release
    def mouseReleaseEvent(self, event):

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # make drawing flag false
            self.drawing = False
