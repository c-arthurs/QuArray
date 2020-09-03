from PyQt5.QtCore import QThread, pyqtSignal
from skimage import color
import numpy as np
from natsort import natsorted
import os
from PIL import Image



class Overlay(QThread):
    info = pyqtSignal(str)
    countChanged = pyqtSignal(int)
    figures = pyqtSignal()
    maxcuts = pyqtSignal(int)

    def __init__(self, path, save=False):
        super().__init__()
        self.inputpath = path
        self.save = save
        self.threshold = None

    def run(self, debug=False):
        files = [f for f in natsorted(os.listdir(self.inputpath)) if not f.endswith("Overlay.png")]
        self.maxcuts.emit(len([f for f in files if f.endswith('.png')]))
        i = 0
        for file in files:
            if file.endswith('.png'):
                self.info.emit("Preparing "+file)
                print(file)

                image = np.array(Image.open(self.inputpath+os.sep+file))[:, :, :3]

                # image = mpimg.imread(self.inputpath+os.sep+file)[:,:,:3]
                self.info.emit("Reading " + file)
                self.current_image = image[::10, ::10]
                self.figures.emit()
                self.overlay(image,filename=file, debug=debug, save=self.save)
                self.countChanged.emit(int(i))  # EMIT the loading bar
            self.info.emit(file + " Overlay Done")
            i += 1
        self.info.emit("All Overlays Saved - ready")

    def overlay(self, image, filename, debug=False, save=False):

        img_hsv = color.rgb2hsv(image)
        img_hue = img_hsv[:, :, 0]
        image_sat = img_hsv[:, :, 1]
        hue = np.logical_and(img_hue > 0.02, img_hue < 0.10)  # BROWN PIXELS BETWEEN 0.02 and 0.10
        self.info.emit("Preparing thresholds for " + filename)
        if self.threshold:
            mask = np.logical_and(hue, image_sat > self.threshold)
        else:
            print("normal threshold")
            mask = np.logical_and(hue, image_sat > 0.79)
        mask = mask.astype(int)
        self.current_image = mask[::10, ::10]
        self.figures.emit()
        self.info.emit("Creating overlay for " + filename)
        alpha = 0.9
        imbw = color.rgb2gray(image)
        rows, cols = imbw.shape
        # Construct a colour image to superimpose
        color_mask = np.zeros((rows, cols, 3))
        color_mask[:, :, 1] = mask  # Change to 0,1,2, for rgb
        # Construct RGB version of grey-level image
        img_color = np.dstack((imbw, imbw, imbw))
        img_hsv = color.rgb2hsv(img_color)
        color_mask_hsv = color.rgb2hsv(color_mask)
        img_hsv[..., 0] = color_mask_hsv[..., 0]
        img_hsv[..., 1] = color_mask_hsv[..., 1] * alpha
        self.info.emit("Converting to RGB " + filename)
        img_masked = color.hsv2rgb(img_hsv)
        # TODO : emit this fig nicely
        # self.current_image = img_masked[img_masked.shape[0]-200:img_masked.shape[0]+200,
        #                      img_masked.shape[0]-200:img_masked.shape[0]+200]
        # self.figures.emit()
        print("displaying output")
        self.info.emit("Saving " + filename)

        imagesave = Image.fromarray((img_masked * 255).astype(np.uint8))
        imagesave.save(self.inputpath+os.sep+filename+'_Overlay.png')

        # mpimg.imsave(self.inputpath+os.sep+filename+'_Overlay.png', img_masked)