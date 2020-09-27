# TMAPP
The App for the TMA histology cutter and analyser

The latest release is out! click on releases on the right hand side of the page and download the zip file. 
At the moment only the mac version is uploaded as I am waiting to deploy it on Windows and Linux. 

Log any issues in the issues tab and I will try to address them as soon as possible. 
Email me for a video of how the exporter works.
<br><br>
## TMApp main screen window
![labels](docs/images/TMAPP_main_screen.png) <br>
<br>
This screen is used to select between the following options - 
1. Opens the [Whole slide image (WSI) exporter](#tma-image-export-window)
2. Opens the [Set threshold screen](#dab-stain-threshold-selection-window)
3. Run DAB analysis in the current window
4. Overlay figure creator - this is currently not available

5 and 6 are both used as a part of the DAB analysis process when butto 3 is selected <br>
5. "Save images" is used to select whether you would like to save the mask images during the DAB analysis. 
This will slow the process slightly. 
6. Viewer window - this displays a low resolution version of the tissue core that is currently being analysed. 
It will then show the low resolution mask of the same image that had been applied. This is useful for spotting a 
poor threshold selection whilst analysis is running
<br>

## TMA image export window
![labels](docs/images/Cut_application_screen.png) <br>
<br>
## DAB stain threshold selection window
![labels](docs/images/Threshold_selector_screen.png) <br>
