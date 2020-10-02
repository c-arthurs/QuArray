.. _Measurements_page:

***********************************
Measurements as performed in python
***********************************

Amount of Tissue
================

.. code-block:: python

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


Amount of Signal
===============

.. code-block:: python

    def QuantStain(self, image, filename, save=False):
        img_hsv = rgb2hsv(image)
        img_hue = img_hsv[:, :, 0]
        image_sat = img_hsv[:, :, 1]
        hue = np.logical_and(img_hue > 0.02, img_hue < 0.10)  # BROWN PIXELS BETWEEN 0.02 and 0.10
        if self.threshold:
            stain = np.logical_and(hue, image_sat > self.threshold)  # USER DEFINED MINIMUM SATURATION THRESHOLD
        else:
            print("Defult threshold")
            stain = np.logical_and(hue, image_sat > 0.79)  #  DEFAULT SATURATION THRESHOLD APPLIED IF NO USER INPUT
        self.current_image = stain[::10, ::10].astype(float)  # SHOW A LOW RESOLUTION MASK AS A FIGURE
        self.figures.emit()
        if save:
            self.info.emit("Saving - " + filename+'_stain.tiff')  # SAVE A FIGURE IF REQUIRED
            imagesave = Image.fromarray(stain)
            imagesave.save(self.inputpath+os.sep+filename+'_stain.tiff')
        stint = image
        stint[stain == 0] = 0
        stint = np.ravel(stint).nonzero()[0]  # ARRAY OF ONLY PIXELS WITH SOME INTENSITY
        stint_mean = stint.mean()
        stint_std = stint.std()
        stained = np.sum(stain)
        return stained, stint_mean, stint_std
