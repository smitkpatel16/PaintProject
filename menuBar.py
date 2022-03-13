from PyQt6 import QtCore
from PyQt6 import QtGui


#|============================================================================|#
# | MenuBar
#|============================================================================|#
class MenuBar(object):
    def __init__(self, windowMenu, parentWindow):

        # creating file menu for save and clear action
        fileMenu = windowMenu.addMenu("File")

        # adding brush size to main menu
        b_size = windowMenu.addMenu("Brush Size")
        sizes = ['2px', '4px', '7px', '9px', '12px']

        # adding brush color to ain menu
        b_color = windowMenu.addMenu("Brush Color")
        colors = ['Black', 'Blue', 'Green', 'Yellow', 'White', 'Red']

        # creating save action
        saveAction = QtGui.QAction("Save", parentWindow)
        # adding short cut for save action
        saveAction.setShortcut("Ctrl + S")
        # adding save to the file menu
        fileMenu.addAction(saveAction)
        # adding action to the save
        saveAction.triggered.connect(parentWindow.save)

        # creating clear action
        clearAction = QtGui.QAction("Clear", parentWindow)
        # adding short cut to the clear action
        clearAction.setShortcut("Ctrl + C")
        # adding clear to the file menu
        fileMenu.addAction(clearAction)
        # adding action to the clear
        clearAction.triggered.connect(parentWindow.clear)
