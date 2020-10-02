.. _Input_page:

***********
Input files
***********

Whole Slide Image files
=======================

Supported Formats
-----------------

NDPI (Hamamatsu) and SVS (Leica) files are accepted by the program as whole slide image files.

Tissue array map file
=====================

An xlsx file which acts as a map of the array.

This is also a method of providing indexed information.

File locations
==============

If the WSI file and the tissue array map file are saved in the same directory with the same name
then the array map will be loaded automatically when the WSI file is loaded.

Here is an example of a normal tree file structure containing the WSI file and the index file.

.. code-block:: bash

   .
   ├── WSI.ndpi
   └── WSI.xlsx

When the images are exported a new directory will be created inside the root to host the output files.

User interface
==============

.. image:: images/Pathology_maps.png

Left - Image of the first tab.

Right - Image of the second tab.



The first tab contains 1 where a core is present and 0 where there is no core. There should be nothing in the rest
of the document

The second tab contains pathology info and is used to make a figure if needed. This is not necessary to run the
program. T and N stand for Tumour and Normal respectively.