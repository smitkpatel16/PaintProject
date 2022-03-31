import math
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtWidgets import QMenu
from PyQt6 import QtCore
from PyQt6 import QtGui


# ===============================================================================
# DrawingView-
# ===============================================================================
class DrawingView(QGraphicsView):
    zoomEvent = QtCore.pyqtSignal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(1)
        self.__scaleFactor = 1.0
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.TextAntialiasing
                           )
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setScrollMode(True)

    def wheelEvent(self, event):

        setScale = False
        if event.angleDelta().y() > 0 and self.__scaleFactor < 4:
            self.__scaleFactor += 0.1
            setScale = True
        elif self.__scaleFactor > 0.5 and event.angleDelta().y() < 0:
            self.__scaleFactor -= 0.1
            setScale = True
        if setScale:
            self.resetTransform()
            self.scale(self.__scaleFactor, self.__scaleFactor)
            self.zoomEvent.emit(self.__scaleFactor)
        self.update()
        return super().wheelEvent(event)

    def setScrollMode(self, mode):

        if mode:
            self.setTransformationAnchor(
                QGraphicsView.ViewportAnchor.AnchorUnderMouse)
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        else:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.setTransformationAnchor(
                QGraphicsView.ViewportAnchor.AnchorUnderMouse)


# ===============================================================================
# DrawingCanvas-
# ===============================================================================
class DrawingCanvas(QGraphicsScene):
    movePosition = QtCore.pyqtSignal(QtCore.QPointF)
    measurement = QtCore.pyqtSignal(str)

    def __init__(self, toolBar):
        super().__init__()
        self.toolBar = toolBar
        self.drawing = False
        self.__currentDraw = None
        self.__firstPoint = None
        self.__freeHandPath = None
        self.__addedItems = []
        self.__contextMenuActions = [
            "Delete", "Move to top", "Move to bottom", "Move up", "Move down"]
        self.__menu = QMenu()
        self.__selectedItem = None
        self.__selectionPen = QtGui.QPen(QtGui.QColor("black"), 2,
                                         QtCore.Qt.PenStyle.DotLine,
                                         QtCore.Qt.PenCapStyle.RoundCap,
                                         QtCore.Qt.PenJoinStyle.RoundJoin)
        self.__measuremetText = None
        for action in self.__contextMenuActions:
            menuAction = QtGui.QAction(action, self)
            self.__menu.addAction(menuAction)
            menuAction.triggered.connect(self.__contextActionStep)
        self.setSceneRect(0, 0, 5000, 5000)

    def __contextActionStep(self, action):
        if self.sender().text() == "Delete":
            self.removeItem(self.__selectedItem)
            for tup in self.__addedItems:
                if tup[0] == self.__selectedItem:
                    self.__addedItems.remove(tup)
                    break
        if self.sender().text() == "Move to top":
            for i, tup in enumerate(self.__addedItems):
                if tup[0] == self.__selectedItem:
                    self.__addedItems.pop(i)
                    self.__addedItems.append(tup)
                    break
        if self.sender().text() == "Move to bottom":
            for i, tup in enumerate(self.__addedItems):
                if tup[0] == self.__selectedItem:
                    self.__addedItems.pop(i)
                    self.__addedItems.insert(0, tup)
                    break
        if self.sender().text() == "Move up":
            for i, tup in enumerate(self.__addedItems):
                if tup[0] == self.__selectedItem:
                    if i < len(self.__addedItems)-1:
                        self.__addedItems.pop(i)
                        self.__addedItems.insert(i + 1, tup)
                        break
        if self.sender().text() == "Move down":
            for i, tup in enumerate(self.__addedItems):
                if tup[0] == self.__selectedItem:
                    if i > 0:
                        self.__addedItems.pop(i)
                        self.__addedItems.insert(i - 1, tup)
                        break
        for i, tup in enumerate(self.__addedItems):
            tup[0].setZValue(i)
        self.__selectedItem = None
        self.update()

    def contextMenuEvent(self, event):
        self.__menu.exec(event.screenPos())
        return super().contextMenuEvent(event)

    # method for checking mouse cicks
    def mousePressEvent(self, event):
        # if left mouse button is pressed
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.toolBar.selectedItem:
            # make drawing flag true
            self.drawing = True
        if not self.drawing:
            self.__selectedItem = self.itemAt(
                event.scenePos(), QtGui.QTransform())
        return super().mousePressEvent(event)

    # method for tracking mouse activity
    def mouseMoveEvent(self, event):
        # self.movePosition.emit(event.scenePos())
        # checking if left button is pressed and drawing flag is true
        if (event.buttons() and QtCore.Qt.MouseButton.LeftButton) and self.drawing:
            if not self.__firstPoint:
                self.__firstPoint = event.scenePos()
            if self.__currentDraw:
                self.removeItem(self.__currentDraw)
            if self.__measuremetText:
                self.removeItem(self.__measuremetText)
            if self.toolBar.selectedItem == "line":
                self.__currentDraw = self.addLine(self.__firstPoint.x(),
                                                  self.__firstPoint.y(),
                                                  event.scenePos().x(),
                                                  event.scenePos().y(),
                                                  self.toolBar.pen)
            if self.toolBar.selectedItem == "ellipse":
                self.__currentDraw = self.addEllipse(self.__firstPoint.x(),
                                                     self.__firstPoint.y(),
                                                     event.scenePos().x()-self.__firstPoint.x(),
                                                     event.scenePos().y()-self.__firstPoint.y(),
                                                     self.toolBar.pen)
            if self.toolBar.selectedItem == "rectangle":
                self.__currentDraw = self.addRect(self.__firstPoint.x(),
                                                  self.__firstPoint.y(),
                                                  event.scenePos().x()-self.__firstPoint.x(),
                                                  event.scenePos().y()-self.__firstPoint.y(),
                                                  self.toolBar.pen)
            if self.toolBar.selectedItem == "measure":
                self.__currentDraw = self.addLine(self.__firstPoint.x(),
                                                  self.__firstPoint.y(),
                                                  event.scenePos().x(),
                                                  event.scenePos().y(),
                                                  self.toolBar.measurePen)
                m = math.sqrt((event.scenePos().x()-self.__firstPoint.x())**2 +
                              (event.scenePos().y()-self.__firstPoint.y())**2)
                px = self.__firstPoint.x()+((event.scenePos().x()-self.__firstPoint.x())/2)
                py = self.__firstPoint.y()+((event.scenePos().y()-self.__firstPoint.y())/2)
                theta = math.atan2(event.scenePos().y()-self.__firstPoint.y(),
                                   event.scenePos().x()-self.__firstPoint.x())*180/math.pi

                self.__measuremetText = self.addText(self.toolBar.pix2Met(m))
                self.__measuremetText.setRotation(theta)
                self.__measuremetText.setPos(px, py)

            if self.toolBar.selectedItem == "freeHand":
                if not self.__freeHandPath:
                    self.__freeHandPath = QtGui.QPainterPath()
                    self.__freeHandPath.moveTo(self.__firstPoint)
                self.__freeHandPath.lineTo(event.scenePos())
                self.__currentDraw = self.addPath(
                    self.__freeHandPath, self.toolBar.pen)
                self.__firstPoint = event.scenePos()
            # update
            self.update()
        if not self.drawing:
            return super().mouseMoveEvent(event)

    def dragMoveEvent(self, event):
        print("dragMoveEvent")

        return super().dragMoveEvent(event)

    # method for mouse left button release
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.drawing and self.__currentDraw:
                self.__currentDraw.setFlag(
                    QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
                self.__currentDraw.setZValue(len(self.__addedItems))
                self.__addedItems.append(
                    (self.__currentDraw, QtGui.QPen(self.toolBar.pen)))
            # make drawing flag false
            self.drawing = False
            self.__firstPoint = None
            self.__currentDraw = None
            self.__freeHandPath = None
            self.__measuremetText = None
        return super().mouseReleaseEvent(event)
