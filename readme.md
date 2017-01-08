Penny Mosaic Generator
======================

This project takes an input image and turns it into a penny mosaice. Pennies are characterized using a webcam and a jig. An image of each penny is saved and can be used to show a graphic representation of what an actual build will look like.

Usage
-----

Run pennyArt.py in idle and call runGame() to generate the demo image of Gustav Mahler as greyscale circles.

Run pennyArt.py in idle and call runGame(usePennies=True) to generate the demo image of Gustav Mahler in pennies. Note that this uses the same penny over and over again for a given luminosity level becuase the sample set provided of 61 pennies is far to few to produce an image of unique penny samples.

Run pennyScanner.py and a pygame window will be launched showing your webcam image. I build a jig that holds my webcamp 6cm above the pennies. Spacebar saves a new unique photo and outputs the luminosity level for sorting your pennies. The processed photo will be automatically saved to the 'sampleSet/' subdirectory

Run pennyArt.py in idle and call picklePennies() to recharacterize all penny images and save the luminosity dataset to pennySet.p
 
License
=======

Penny Mosaic Generator
MIT License
Copyright 2017 - Mike Szczys
http://jumptuck.com
