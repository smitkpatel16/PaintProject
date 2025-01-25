
# ===============================================================================
# Interactions- Main class where all the interactions are routed through
# ===============================================================================
class Interactions(object):
    def __init__(self, canvas, view):
        self.__canvas = canvas
        self.__view = view
        self.__sessionActions = []
        self.__currentAction = -1

    def clear(self, manual=True):
        # push the action done
        if manual:
            self.__sessionActions.append(("Clear"))
            self.__currentAction = len(self.__sessionActions) - 1
        self.__canvas.clear()
        self.__view.update()

    def importPDF(self, pm=None, manual=True):
        # push the action done
        if manual:
            self.__sessionActions.append(("Import", pm))
            self.__currentAction = len(self.__sessionActions) - 1
        pm = self.__canvas.addPixmap(pm)
        self.__view.shear(150, 500)
        pm.setPos(0, 0)
        self.__view.update()

    def itemAdded(self, item, manual=True):
        # push the action done
        if manual:
            self.__sessionActions.append(("Add", item))
            self.__currentAction = len(self.__sessionActions) - 1
        self.__view.update()

    def undo(self):
        try:
            if self.__currentAction < 0:
                return
            undoAction = self.__sessionActions[self.__currentAction]
            if undoAction[0] == "Add":
                self.__canvas.removeItem(undoAction[1])
            if undoAction[0] == "Import":
                self.__canvas.clear()
                for act in self.__sessionActions[:self.__currentAction]:
                    if act[0] == "Add":
                        self.__canvas.addItem(act[1])
            self.__currentAction -= 1
            self.__view.update()
        except Exception as ex:
            print(ex)

    def redo(self):
        if self.__currentAction == len(self.__sessionActions) - 1:
            return
        self.__currentAction += 1
        redoAction = self.__sessionActions[self.__currentAction]
        if redoAction[0] == "Add":
            self.__canvas.addItem(redoAction[1])
        if redoAction[0] == "Import":
            self.__canvas.clear()
            for act in self.__sessionActions[:self.__currentAction]:
                if act[0] == "Add":
                    self.__canvas.addItem(act[1])
            self.__canvas.addPixmap(redoAction[1])
        self.__view.update()
