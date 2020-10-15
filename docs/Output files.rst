.. _Output_page:

*******************
Output from QuArray
*******************

Tissue core threshold output
============================

.. note::
   The outputs of the tissue core export process are as follows. They are all saved into the same location in the
   whole slide image export file.

1. Whole core images - indexed with coordinates in name
-------------------------------------------------------

Image of the selection panel
----------------------------

This will be created when overlay cores is pressed.

.. Image:: images/wsi_001_split_overlay.tiff

2. Figure of all images in the array
------------------------------------

An example of this figure is below. If pathology map is provided, then the bounding boxes are coloured bases on
pathology. Otherwise, they are not included.

.. Image:: images/wsi_001_split_layoutfig.tiff

3. Image metadata in JSON format
--------------------------------

The following fields are included.

:path: path of the whole slide image
:coordinates: list of tuple coordinates in the whole slide image
:cores: list of strings to denote core names
:diameter: int for the number of pixels in the image
:scale_index: float to show the scale index between low and high WSI levels
:lowlevel: int to show the level that the low magnification file was taken from
:arrayshape: tuple of the shape of the tissue array in col row format


Chromogen measurement output
============================

The output of the chromogen measurement window is a single excel file (.xlsx) which contains all measurements
taken from each tissue core in the input folder.

The data is organised with each core measurements taking a single row.

The column titles and data are as follows:

:CoreName: The file name of the analysed tissue image
:AMTsignal: the total amount of pixels that contained signal in the tissue image\. Also termed coverage
:Mean_intensity: The mean average of the pixel values in the threshold image
:Standard_Dev_intensity: The standard deviation of the pixel values in the threshold image
:AMTtissue: The total amount of tissue in the image. The calculation for this is in the :ref:`measurements page <Measurements_page>`
:AFperAMTT: The AMTsignal divided by the amount of tissue
:Mean_Intensity_perAMTT: The Mean_intensity divided by the amount of tissue
:SD_Intensity_perAMTT: The Standard_Dev_intensity divided by the amount of tissue

Output file structure
=====================

Below is an example of what the file structure could look like for an end to end project after running image export and
chromogen analysis.

.. code-block:: bash

   .
   ├── wsi_001.ndpi
   ├── wsi_001.xlsx
   └── wsi_001_split
       ├── CoreAnalysis_WSI_001.xlsx
       ├── wsi_001_split_A1.png
       ├── wsi_001_split_B1.png
       ├── wsi_001_split_C1.png
       ├── wsi_001_split_D1.png
       ├── wsi_001_split_layoutfig.tiff
       ├── wsi_001_split_metadata.json
       └── wsi_001_split_overlay.tiff

