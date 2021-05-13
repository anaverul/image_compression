# Image compression
This software provides a tool to compress .png, .jpg and .gif files. To run, make sure all the files you would like to compress are located in the same directory as compress.py and compress_gui.py. Software can be used in both, CLI and GUI

## Dependencies:

* **os**
* **sklearn**
* **Tkinter**
*  **PIL**
*  **itertools*
*  **time**
*  **shutil**
*  **numpy**
*  **joblib**

## How to use:

* On the CLI: navigate to the image_compression folder and type ```$python3 compress.py -i filename```, where filename indicates the name of the file you would like to process.
* Using GUI: navigate to the image_compression folder on the CLI and type ```$python3 compress_gui.py```. In the GUI window, click "browse" and select the file you would like to process. Then, click "compress". Compressed files will be Displayed in the GUI and saved in the same directory as compress.py and compress_gui.py

