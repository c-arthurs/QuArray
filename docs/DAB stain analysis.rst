.. _DAB_page:

******************
DAB stain analysis
******************

QuArray provides the option to analyse DAB staining in your exported TMA images.

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto; margin-bottom: 2em;">
        <iframe src="https://www.youtube.com/embed/jjvIDere3ZA" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>


Input
#####

The user must have selected a threshold using the :ref:`threshold selector window <threshold_selector_window>`
. It will run analysis on any PNG file in a given directory.

.. _threshold_selector_window:

Selecting a threshold
#####################

To view the threshold selector window select the threshold button from the main window. A new window will appear.

There is an option to select the file path of the PNG files that you are loooking to analyse.

User interface
##############

.. image:: images/Threshold_selector_screen.png

#. Mask for the whole image

   * White pixels will be measured as stain.

   * This is a Low resolution version of the WSI.

#. Original whole image at a low resolution

#. Full resolution magnification mask

#. Full resolution magnification image

#. Add a file path.

   * This is used to select the directory containing the PNG images that will be used to optimise the threshold.

   * A random image from this file will be loaded into the window.

#. Load sample image.

   * This will load a new random image into the window.

   * It is good to optimise the thresholds on at least 10 sample images from the dataset

#. Saturation slider.

   * This will change the minimum saturation value for the DAB stain.

   * The value will be displayed in windows 1 and 3.

#. Toggle button which shows the original image again and it is now depreciated due to the extra windows.

#. Apply thresholds.

   * This sends the new threshold to the main window of the program.

   * This should be selected before pressing the DAB analysis button in the main window.

   * The thresholds button of the main window will turn green.


