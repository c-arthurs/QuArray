import sys
from PyQt5 import QtGui, uic
import qdarkgraystyle
from scripts import DABanalysis, Overlay
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore  # QtWidgets
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import qimage2ndarray
import random
import numpy as np
import matplotlib.image as mpimg
from skimage import color
from PyQt5.QtWidgets import QGraphicsScene

#
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        print(x, y)

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('./scripts/Threshold_Layout.ui', self)
        # self.scene = GraphicsScene(self)
        # self.graphicsView.setScene(self.scene)
        self.load_ndpi.clicked.connect(lambda: self.loadndpi())
        self.load_ndpi.clicked.connect(lambda: self.loadndpi())
        print('hi')
        self.show()

    def loadndpi(self):
        print('1')
        self.path = QFileDialog.getOpenFileName(parent=self, caption='Open file',
                                                     directory="/Users/callum/Desktop")
        if self.path:
            self.image = OpenSlide(self.path)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
