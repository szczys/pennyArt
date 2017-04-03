Penny Mosaic Generator
======================

This project takes an input image and turns it into a penny mosaice. Pennies are characterized using a webcam and a jig. An image of each penny is saved and can be used to show a graphic representation of what an actual build will look like.

Grab pennies from a scanner with OpenCV
---------------------------------------

```scanimage --resolution 300 --mode Color > scannerPennies.pnm```

from pennyCV.py run:
```genAndSavePennySamples(scannerPennies.pnm)```

Usage
-----

Run pennyArt.py in idle and call runGame() to generate the demo image of Gustav Mahler as greyscale circles.

Run pennyArt.py in idle and call runGame(usePennies=True) to generate the demo image of Gustav Mahler in pennies. Note that this uses the same penny over and over again for a given luminosity level becuase the sample set provided of 61 pennies is far to few to produce an image of unique penny samples.

Run pennyScanner.py and a pygame window will be launched showing your webcam image. I build a jig that holds my webcamp 6cm above the pennies. Spacebar saves a new unique photo and outputs the luminosity level for sorting your pennies. The processed photo will be automatically saved to the 'sampleSet/' subdirectory

Run pennyArt.py in idle and call picklePennies() to recharacterize all penny images and save the luminosity dataset to pennySet.p

Webcam Exposure Settings
------------------------

To prevent auto exposure adjustments in the webcam I tweake the settings form the command line before running the pennyScanner.py program:

```bash
sudo apt-get install v4l-utils
```
List all settings for your camera (mine is at /dev/video1 default is /dev/video0)

```bash
v4l2-ctl -d /dev/video1 --all
```

By default my webcam uses white_balance_temperature_auto and exposure_auto. Confusingly, exposure_auto needs to be set to 1 for manual mode:

```bash
v4l2-ctl -d /dev/video1 -c white_balance_temperature_auto=0
v4l2-ctl -d /dev/video1 -c exposure_auto=1
```

Just be sure to set these values back when done scanning.

OpenCV for Python
=================
If you get a message that the cv2 library is not found, run this (Ubuntu):
```sudo apt-get install python-opencv```


License
=======

Penny Mosaic Generator
MIT License
Copyright 2017 - Mike Szczys
http://jumptuck.com
