# DEPLOY MAC
# sudo pyinstaller -F --windowed -p /Users/callum/callum/TMAPP/scripts --add-data "/Users/callum/callum/TMAPP/scripts:scripts" --icon=scripts/docs/he.icns DAB_application.py
# Windows
# pyinstaller -F --windowed -p C:/Users/Daniel/Downloads/TMAPP-master/TMAPP-master/scripts --add-data "C:/Users/Daniel/Downloads/TMAPP-master/TMAPP-master/scripts;scripts" --icon=scripts/docs/he.ico DAB_application.py


import sys
from PyQt5 import uic
import qdarkgraystyle
from scripts import DABanalysis, Overlay, Cut_Application_thread
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
from skimage import color
from PIL import Image

# sys._MEIPASS = '.'  # for running locally

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        # uic.loadUi('./scripts/DAB_layout.ui', self)
        uic.loadUi(sys._MEIPASS+ os.sep +"scripts" +os.sep +"DAB_layout.ui", self) # for deployment

        self.statusBar()
        self.setWindowTitle('DAB Intensity Analyser')
        self.setWindowOpacity(0.96)
        self.ndpi_exporter.clicked.connect(lambda: self.ndpi_export())
        self.trainingbutton.clicked.connect(lambda: self.dabanalysis())
        self.testingbutton.clicked.connect(lambda: self.thresh_action())
        self.overbtn.clicked.connect(lambda: self.overlay())

        self.actionNDPI_SVS_Export.triggered.connect(lambda: self.ndpi_export())
        self.actionRun_Dab_Analysis.triggered.connect(lambda: self.dabanalysis())
        self.actionSet_Thresholds.triggered.connect(lambda: self.thresh_action())
        self.actionOverlay_Figure.triggered.connect(lambda: self.overlay())
        self.saveimages = False
        self.checkBox.stateChanged.connect(self.clickbox)
        scene = QtWidgets.QGraphicsScene()
        self.pixmap = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self.pixmap)
        self.graphicsView.setScene(scene)
        self.show()

    def ndpi_export(self):  # select file(s) button 2
        self.NDPI = Cut_Application_thread.MyWindow()
        self.NDPI.show()
        # self.NDPI.signal.connect(self.updatethresholds)

    def dabanalysis(self):  # select file(s) button 1
        self.statusupdate("Select path containing PNG files")
        self.path = QFileDialog.getExistingDirectory(parent=self, caption='Open file',
                                                    directory="/Users/callum/Desktop")
        if self.path:
            self.analysis = DABanalysis.DabAnalysis(path=self.path, save=self.saveimages)
            self.analysis.maxcuts.connect(self.progress.setMaximum)
            self.analysis.countChanged.connect(self.onCountChanged)
            self.analysis.info.connect(self.statusupdate)
            self.analysis.figures.connect(self.showimage)
            self.analysis.activate.connect(self.activate_input)
            if hasattr(self, "newthreshold"):
                print("Using new DAB threshold - " + str(self.newthreshold))
                self.analysis.threshold = self.newthreshold/100
                self.analysis.start()
            else:
                self.analysis.start()

    def activate_input(self, onoff):
        self.trainingbutton.setEnabled(onoff)
        self.testingbutton.setEnabled(onoff)
        self.overbtn.setEnabled(onoff)
        self.checkBox.setEnabled(onoff)

    def statusupdate(self, message):
        self.statusbar.showMessage(message)

    def clickbox(self, state):
        if state == QtCore.Qt.Checked:
            self.saveimages = True
        else:
            self.saveimages = False

    @pyqtSlot(int)
    def onCountChanged(self, value):
        self.progress.setValue(value)

    def showimage(self):
        img = qimage2ndarray.array2qimage(self.analysis.current_image, normalize=True)
        img = QtGui.QPixmap(img)
        self.pixmap.setPixmap(img)
        self.graphicsView.fitInView(self.graphicsView.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def thresh_action(self):  # select file(s) button 2
        self.SW = SecondWindow()
        self.SW.show()
        self.SW.signal.connect(self.updatethresholds)

    def updatethresholds(self, value):
        self.newthreshold = value
        self.statusupdate("threshold value updated - " + str(value))
        self.testingbutton.setStyleSheet("background-color: rgb(0,90,0)")

    def overlay(self):
        self.statusupdate("Select path - This is slow so only a few files if large")
        path = QFileDialog.getExistingDirectory(parent=self, caption='Open file',
                                                directory="/Users/callum/Desktop")
        if path:
            self.overlayfig = Overlay.Overlay(path=path)
            self.overlayfig.maxcuts.connect(self.progress.setMaximum)
            self.overlayfig.countChanged.connect(self.onCountChanged)
            self.overlayfig.info.connect(self.statusupdate)
            self.overlayfig.figures.connect(self.showimageoverlay)
            if hasattr(self, "newthreshold"):
                print("Using new DAB threshold - " + str(self.newthreshold))
                self.overlayfig.threshold = self.newthreshold / 100
                self.overlayfig.start()
            else:
                self.overlayfig.start()

    def showimageoverlay(self):
        img = qimage2ndarray.array2qimage(self.overlayfig.current_image, normalize=True)
        img = QtGui.QPixmap(img)
        self.pixmap.setPixmap(img)
        self.graphicsView.fitInView(self.graphicsView.sceneRect(), QtCore.Qt.KeepAspectRatio)


class SecondWindow(QtWidgets.QWidget):
    signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(SecondWindow, self).__init__()
        # uic.loadUi('./scripts/Threshold_Layout.ui', self)
        uic.loadUi(sys._MEIPASS+ os.sep +"scripts" +os.sep +"Threshold_Layout.ui", self) # for deployment

        self.slider.setSingleStep(1)
        self.slider.valueChanged[int].connect(self.sliderchange)
        self.setWindowTitle('Set DAB Thresholds')
        self.setWindowOpacity(0.96)
        scene = QtWidgets.QGraphicsScene()
        self.pixmap = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self.pixmap)
        self.graphicsView.setScene(scene)
        self.trainingbutton.clicked.connect(lambda: self.getpath())
        self.imagebutton.clicked.connect(lambda: self.sampleimage())
        self.togglebtn.clicked.connect(lambda: self.toggle())
        self.applybtn.clicked.connect(lambda: self.apply())

        if not hasattr(self, "path"):
            self.imagebutton.setEnabled(False)
            self.togglebtn.setEnabled(False)
            self.applybtn.setEnabled(False)
            self.slider.setVisible(False)
            self.slbl.setEnabled(False)
            self.dablbl.setEnabled(False)
            self.lbl2.setEnabled(False)
        self.show()

    def getpath(self):  # select file(s) button 1
        self.path = QFileDialog.getExistingDirectory(parent=self, caption='Open file path',
                                                     directory="/Users/callum/Desktop")
        if self.path:
            self.imagebutton.setEnabled(True)
            self.togglebtn.setEnabled(True)
            self.applybtn.setEnabled(True)
            self.slider.setVisible(True)
            self.slbl.setEnabled(True)
            self.dablbl.setEnabled(True)
            self.lbl2.setEnabled(True)
            self.lbl.setText(self.path)
            print(self.path)

    def settext(self, text):
        self.lbl2.setText(text)
        self.lbl2.repaint()
        return

    @pyqtSlot()
    def sampleimage(self):
        if hasattr(self, "path"):
            files = [f for f in os.listdir(self.path) if f.endswith(".png") and not f.endswith("Overlay.png")]
            self.randpath = files[random.randint(0, len(files) - 1)]
            self.settext(self.randpath)
            print(self.randpath)
            self.img = np.array(Image.open(self.path + os.sep + self.randpath))[:, :, :3]
            # self.img = mpimg.imread(self.path + os.sep + self.randpath)[:, :, :3]
            self.img = self.img[::4, ::4]
            # prep for analysis
            img_hsv = color.rgb2hsv(self.img)
            self.img_hue = img_hsv[:, :, 0]
            self.image_sat = img_hsv[:, :, 1]
            self.slider.setMaximum((self.image_sat.max()) * 100)
            self.slider.setMinimum((self.image_sat.min()) * 100)
            self.togimg = qimage2ndarray.array2qimage(self.img, normalize=True)
            self.togimg = QtGui.QPixmap(self.togimg)
            self.togimg = self.togimg.scaledToWidth(484)
            self.togimg = self.togimg.scaledToHeight(356)
            self.pixmap.setPixmap(self.togimg)
            self.graphicsView.fitInView(self.graphicsView.sceneRect(), QtCore.Qt.KeepAspectRatio)
            return

    def sliderchange(self, value):
        if hasattr(self, "img"):
            self.slbl.setText(str(value))
            hue = np.logical_and(self.img_hue > 0.02, self.img_hue < 0.10)  # BROWN PIXELS BETWEEN 0.02 and 0.10
            img = np.logical_and(hue, self.image_sat > value / 100)
            img = qimage2ndarray.array2qimage(img, normalize=True)
            img = QtGui.QPixmap(img)
            img = img.scaledToWidth(484)
            img = img.scaledToHeight(356)
            self.pixmap.setPixmap(img)
            self.graphicsView.fitInView(self.graphicsView.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def toggle(self):
        if hasattr(self, "togimg"):
            self.pixmap.setPixmap(self.togimg)
            self.graphicsView.fitInView(self.graphicsView.sceneRect(), QtCore.Qt.KeepAspectRatio)

    pyqtSlot()

    def apply(self):
        self.signal.emit(int(self.slider.value()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()

    # style sheet - https://github.com/mstuttgart/qdarkgraystyle
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    sys.exit(app.exec_())
