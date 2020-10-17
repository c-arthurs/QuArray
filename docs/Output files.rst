.. _Output_page:

*******************
Output from QuArray
*******************

Tissue core threshold output
============================

.. note::
   The outputs of the tissue core export process are as follows. They are all saved into the same location in the
   whole slide image export file.

1. Whole core images - indexed with coordinates in the file name
-------------------------------------------------------

Image of the selection panel
----------------------------

This will be created when overlay cores is pressed.

.. Image:: images/wsi_001_split_overlay.tiff

2. Figure containing images of all tissue cores in an array
-----------------------------------------------------------

An example of such a figure is given below. A bounding box appears (e.g. green or red) if a pathology/condition map is
included in (see :ref:`input files<Input_page>`), otherwise bounding boxes are omitted.

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

The output of the chromogen (e.g. DAB) measurement window is a single excel file (.xlsx) which contains measurements of
multiple parameters from each tissue core in the input folder.

The data is organised in a single row for the measurements for tissue each core image.

The column titles and data description appear as follows:


:CoreName: The file name of the analysed tissue image
:AMTsignal: the total number of pixels that contain 'signal' in the image\, Also termed coverage
:Mean_intensity: The mean average of the pixel values in the threshold image
:Standard_Dev_intensity: The standard deviation of the pixel values in the threshold image
:AMTtissue: The total amount of tissue in the image \(calculation provided in the :ref:`measurements page<Measurements_page>`
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

