import numpy as np
import os
from natsort import natsorted
import pandas as pd
from skimage.color import rgb2hsv, rgb2gray
from skimage.filters import gaussian, threshold_triangle
from skimage.exposure import rescale_intensity
from PyQt5.QtCore import QThread, pyqtSignal
from PIL import Image


class DabAnalysis(QThread):

    maxcuts = pyqtSignal(int)
    info = pyqtSignal(str)
    countChanged = pyqtSignal(int)
    figures = pyqtSignal()
    activate = pyqtSignal(bool)

    def __init__(self, path, save=False):
        super().__init__()
        self.inputpath = path
        self.save = save
        self.threshold = None

    def run(self, debug=False):
        self.activate.emit(False)
        analysis = []
        files = [f for f in natsorted(os.listdir(self.inputpath)) if not f.endswith("Overlay.png")]
        self.maxcuts.emit(len([f for f in files if f.endswith('.png')]))
        i = 0
        for file in files:
            if file.endswith('.png'):
                self.info.emit("Analysing "+file)
                print(file)
                info = []
                image = np.array(Image.open(self.inputpath+os.sep+file))[:, :, :3]
                self.current_image = image[::10, ::10]
                self.figures.emit()
                info.append(str(file))
                info.extend(self.QuantStain(image, filename=file, save=self.save))
                info.append(self.QuantCore(image, filename=file, save=self.save))
                analysis.append(info)
                print(info)
                self.countChanged.emit(int(i)+1)  # EMIT the loading bar
            self.info.emit(file + " analysed")
            i += 1
        # TODO can make this more lightweight by removing pandas and using csv
        df = pd.DataFrame(analysis, columns=('CoreName', 'AMTsignal', 'Mean_intensity', 'Standard_Dev_intensity',
                                             'AMTtissue'))
        df['AFperAMTT'] = df['AMTsignal']/df['AMTtissue']*100
        df['Mean_Intensity_perAMTT'] = df['Mean_intensity'] / df['AMTtissue'] * 100
        df['SD_Intensity_perAMTT'] = df['Standard_Dev_intensity'] / df['AMTtissue'] * 100
        df.to_excel(self.inputpath+os.sep+'CoreAnalysis_'+str(df['CoreName'][0])[:-6]+'.xlsx')
        self.info.emit("All Files Analysed - ready")
        self.activate.emit(True)

    def QuantStain(self, image, filename, save=False):
        img_hsv = rgb2hsv(image)
        img_hue = img_hsv[:, :, 0]
        image_sat = img_hsv[:, :, 1]
        hue = np.logical_and(img_hue > 0.02, img_hue < 0.10)  # BROWN PIXELS BETWEEN 0.02 and 0.10
        if self.threshold:
            stain = np.logical_and(hue, image_sat > self.threshold)
        else:
            print("normal threshold")
            stain = np.logical_and(hue, image_sat > 0.79)
        # TODO : fix this - sent bug report to Github
        self.current_image = stain[::10, ::10].astype(float)
        print(type(stain))
        self.figures.emit()
        if save:
            self.info.emit("Saving - " + filename+'_stain.tiff')
            imagesave = Image.fromarray(stain)
            imagesave.save(self.inputpath+os.sep+filename+'_stain.tiff')

        stint = np.copy(image)
        stint = rescale_intensity(stint, out_range=(0, 255))
        stint[stain == 0] = 0  # array with only the stained pixels
        stint = rgb2gray(stint)
        stint = np.ravel(stint)
        stint = stint[stint != 0]
        stint_mean = stint.mean()
        stint_std = stint.std()
        stained = np.sum(stain)
        return stained, stint_mean, stint_std

    def QuantCore(self, image, filename, save=False):
        image = gaussian(rgb2gray(image), sigma=2)
        thresh = threshold_triangle(image[image > 0])
        binary = np.logical_and(image < thresh, image > 0)
        wholeCore = np.sum(binary)
        if save:
            self.info.emit("Saving - " + filename + '_core.tiff')
            imagesave = Image.fromarray(binary)
            imagesave.save(self.inputpath+os.sep+filename + '_core.tiff')
        return wholeCore
