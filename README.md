# Quick start
Create a project folder with the following file structure:
```
project_name/
|____ input/ (contains all input images)
|____ output/ (empty folder for output images)
|____ main.py (main program)
```

Replace the constants ```INPUT``` and ```OUTPUT``` in ```main.py``` with the full paths of your input and output directories.

Navigate to the project folder and run the program:
```bash
cd project_name
python main.py
```

# Dependencies
* os module
* NumPy
* OpenCV

# How it works

The code iterates through each file in the ```input/``` directory using the os module.

It then converts the image to **grayscale** (```cv2.IMREAD_GRAYSCALE```) and removes noise from the image using ```cv2.fastNlMeansDenoising()```. This prevents small details like spots on the road or leaves of trees from being detected by the Canny edge detector.

Next, we use a **Gaussian adaptive threshold** (```cv2.adaptiveThreshold()```) to binarize the image. A simple brightness function (which uses the mean pixel values) was used to filter out very dark images and a smaller ```C``` value was used for these images when using the adaptive threshold function. When the image is very dark, the pixel values of the graysclae image are very low. Since ```C``` is a value subtracted from the weighted mean of the image, dark images end up losing all of their detail and the binarization process sets all pixels to black.

Then, we conduct a **Canny edge detection** on each image using ```cv2.Canny()``` and the default arguments.

At last, we are able to use a **probabilistic Hough Lines** detector (```cv2.HoughLinesP()```) to detect lanes. Notable changes made to arguments of this function can be found below:

* ```minLineLength``` was set at 200 to avoid processing small lines which were detected as a result of random noise and non-lane objects.
* ```maxLineGap``` was increased to 100 to accomodate dashed road markings and combine them into contiguous line segments.

During preliminary testing, it was observed that objects with defined, straights lines like overpasses, barriers and treelines were also being picked up by the Hough Lines detector. However, changing the parameters of earlier steps such as the Canny detector and adaptive threshold would inhibit our ability to detect real, lane lines. Later, I noticed that lane lines were mostly near-vertical or slanted whereas the contours in overpasses and trees were usually horizontal. As a result, I filtered out lines that were **horizontal** or within 30 degrees of being horizontal by calculating the angle of each line using ```np.arctan()```.

Finally, the code saves the output image to the output directory.

# Next steps

**Detecting line clusters**

In some images, the Hough Lines detector returns clusters of lines that are very close of one another with similar lengths and orientations. From a practical perspective, we only need one member of each of these clusters in order to determine where the lanes are.

As a result, further work needs to be done to detect such clusters and choose the most representative member of each cluster to keep in the image. As of now, the code leverages the ```minLineLength``` parameter of the ```HoughLinesP()``` function to ensure that only lines that differ by at least 5 degrees are shown.

**Finding out where lines end**

In some images, detected lane lines extend far beyond their actual start and end points and converge at some point. I can forsee this being problematic for pathfinding purposes as the vehicle might interpret two lane lines converging as a dead-end.

As a result, further work needs to be done in order to reliably determine the start and end points of lanes.