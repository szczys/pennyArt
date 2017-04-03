'''******************************
* Penny Mosaic Generator        *
* MIT License               	*
* Copyright 2017 - Mike Szczys  *
* http://jumptuck.com 	    	*
*				*
******************************'''

import pygame
import sys
from math import sqrt
import pickle
import glob
from pennyCharacterizer import \
	samplePennies, \
	getPixelArray, \
	getLuminosityValues, \
	getCircleAverageLuminosity, \
	getAllPointsInCircle
from random import randrange

#Global variable to help with testing (populated by runGame()
mosaicData = []

#triagePennies variable will repeat penny use if False.
#this is useful if you have a small penny set and just want
#a preview using repeating images
triagePennies = False

def getMapData(mosaicSet, pennySet):

    mosaicLow= 255
    mosaicHigh= 0
    pennyLow= 255
    pennyHigh= 0

    for i in mosaicSet:
        if i[1] < mosaicLow:
            mosaicLow = i[1]
        if i[1] > mosaicHigh:
            mosaicHigh = i[1]

    for pKey in pennySet.keys():
        if pKey < pennyLow:
            pennyLow = pKey
        if pKey > pennyHigh:
            pennyHigh = pKey

    mosaicSpan = mosaicHigh - mosaicLow
    pennySpan = pennyHigh - pennyLow

    steps = pennySpan/float(mosaicSpan)

    return (steps, mosaicLow, pennyLow, pennyHigh)

def calcMapValues(value, MapData, pennySet, maxDeviation=1):
    #Takes a luminosity value and maps it to list of mapped penny luminosities
    #Parameters:
    #   value: (0-255) calculated from circular area on input image
    #   MapData: output of getMapData
    #   pennySet: from samplePennies() or unPicklePennies()
    #   maxDeviation: (Default=1) how many steps away are acceptables matches
    #      if 'steps' is less than 1 this will include multiple penny values
    steps = MapData[0]
    mosaicLow = MapData[1]
    pennyLow = MapData[2]
    pennyHigh = MapData[3]

    increment = int((value-mosaicLow)*steps)
    testMap = pennyLow+increment
    mappedValues = []
    #Apply deviation values
    for i in range(0,maxDeviation+1):
        thisDeviation = testMap+i
        if thisDeviation in pennySet.keys() and \
           thisDeviation < 255 and \
           thisDeviation not in mappedValues:
            mappedValues.append(thisDeviation)
        if testMap >= i:
            thisDeviation = testMap-i
            if thisDeviation in pennySet.keys() and \
               thisDeviation not in mappedValues:
                mappedValues.append(thisDeviation)
    return mappedValues

def mapTest(deviation=1):
	"""Returns number of values that are not mappable based on the pennies currently in the set."""
    #Sanity checking calcMapValues()
    #Returns number of values not mappable.
    #Increase deviation to decrease the unmappable values
	a = unPicklePennies()
	missing = set([])
	for i in mosaicData:
		x = calcMapValues(i[1],getMapData(mosaicData, a), a,deviation)
		if x == []:
			missing.add(i[1])
	print len(missing)
	print missing
            
		
##This dict is a hack for testing
#valueSet = {35: 'sampleSet/000032-penny.png', 36: 'sampleSet/000033-penny.png', 43: 'sampleSet/000031-penny.png', 44: 'sampleSet/000012-penny.png', 45: 'sampleSet/000030-penny.png', 49: 'sampleSet/000029-penny.png', 50: 'sampleSet/000035-penny.png', 51: 'sampleSet/000018-penny.png', 54: 'sampleSet/000014-penny.png', 55: 'sampleSet/000011-penny.png', 57: 'sampleSet/000051-penny.png', 58: 'sampleSet/000017-penny.png', 59: 'sampleSet/000010-penny.png', 60: 'sampleSet/000034-penny.png', 62: 'sampleSet/000050-penny.png', 64: 'sampleSet/000054-penny.png', 65: 'sampleSet/000026-penny.png', 66: 'sampleSet/000028-penny.png', 68: 'sampleSet/000027-penny.png', 71: 'sampleSet/000057-penny.png', 72: 'sampleSet/000016-penny.png', 73: 'sampleSet/000038-penny.png', 74: 'sampleSet/000008-penny.png', 75: 'sampleSet/000040-penny.png', 77: 'sampleSet/000061-penny.png', 78: 'sampleSet/000060-penny.png', 79: 'sampleSet/000005-penny.png', 86: 'sampleSet/000042-penny.png', 89: 'sampleSet/000009-penny.png', 94: 'sampleSet/000022-penny.png', 97: 'sampleSet/000006-penny.png', 99: 'sampleSet/000049-penny.png', 100: 'sampleSet/000041-penny.png', 103: 'sampleSet/000046-penny.png', 106: 'sampleSet/000020-penny.png', 107: 'sampleSet/000058-penny.png', 109: 'sampleSet/000047-penny.png', 114: 'sampleSet/000024-penny.png', 115: 'sampleSet/000059-penny.png', 117: 'sampleSet/000043-penny.png', 126: 'sampleSet/000001-penny.png', 129: 'sampleSet/000021-penny.png', 134: 'sampleSet/000023-penny.png', 138: 'sampleSet/000056-penny.png', 148: 'sampleSet/000055-penny.png', 156: 'sampleSet/000045-penny.png'}
##end testing hack

#### Testruns: ####

# mahler2 runGame(786,976,8)
# mahler2-lowcontrast.jpg runGame(786,976,8)
# mahler2-cropped.jpg runGame(534,798,8)

def tm():
	# This is probably a testrun to making things faster and is likely now deprecated.
    from time import time
    for key in valueSet.keys():
        pixel = getPixelArray(valueSet[key])
        x = len(pixel)/2
        r = x
        if r%2 == 0:
            r -= 1
        y = getAllPointsInCircle(x,x,r)
        t0 = time()
        z= getCircleAverageLuminosity(pixel,y)
        t1 = time()
        print key,z,t1-t0


###############################


def testPoints(x):
    #Just a quick test to sanity check circle points set
    for i in range(21):
            thisRow = ""
            for j in range(21):
                    if (j,i) in x:
                            thisRow += "0 "
                    else:
                            thisRow += "- "
            print thisRow

###################################

def calcVertices(xSize,ySize,horizontalBisect,verticalDist):
    #returns points for equidistance circle centers in plane bound by x,y
    allVertices = []

    #starting vertices accounts for left and top padding
    curX = horizontalBisect
    curY = horizontalBisect
    row = 0

    while True:
        allVertices.append((curX,curY))
        #print allVertices[-1]
        #increment X
        curX += (2*horizontalBisect)

        #check for X overflow
        if curX > (xSize-horizontalBisect):
            row += 1
            curX = horizontalBisect+((row%2)*horizontalBisect)
            curY = curY + verticalDist
            if curY > (ySize-horizontalBisect):
                return allVertices

def picklePennies():
    #sample all pennies and write output to a file for later use
    saveSet = samplePennies()
    pickleHelper("pennySet.p",saveSet)

def unPicklePennies():
    #read in previously harvested sample set data
    return unPickleHelper("pennySet.p")

def unPicklePaintByNumber():
    return unPickleHelper("paintByNumber.p")

def pickleHelper(fn, data):
    with open(fn,"wb") as outfile:
        pickle.dump(data, outfile)

def unPickleHelper(fn):
    try:
        with open(fn,"rb") as infile:
            saveSet = pickle.load(infile)
    except:
        saveSet = {}
    return saveSet

def runGame(sourceImage='mahler2-cropped.jpg',radius=32,scalingValue=8,usePennies=False):
    from time import time
    t0 = time()
    #Parameters:
    #sourceImage - Image you want to create as a penny mosaic
    #radius - radius in pixels of each penny area for this image
    #scalingValue - how much larger should the mock up be than the source image
    #393x488

    inputImage = pygame.image.load(sourceImage)

    pygameSurfaceX = inputImage.get_rect().size[0]*scalingValue
    pygameSurfaceY = inputImage.get_rect().size[1]*scalingValue

    #horizontal distances should be easy:
    horizontalBisect = radius

    #vertial is trickier (non-integer)
    verticalDist = int(sqrt(((horizontalBisect*2)**2)-(horizontalBisect**2)))

    #stock colors
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    darkBlue = (0,0,128)
    white = (255,255,255)
    black = (0,0,0)
    pink = (255,200,200)

    #Get a list of all points
    print "Generating penny locations"
    testPoints = calcVertices(pygameSurfaceX, \
                              pygameSurfaceY, \
                              horizontalBisect, \
                              verticalDist)

    #Get pixel data from source image
    print "Calculating luminance of penny areas"
    circlesAndLum = getLuminosityValues(testPoints, scalingValue, radius, sourceImage)
    global mosaicData
    mosaicData = circlesAndLum
    print "Total pennies for this mosaic:",len(circlesAndLum)

    #Show how it's going to look!
    pygame.init()
    screen = pygame.display.set_mode((pygameSurfaceX,pygameSurfaceY))
    screen.fill((187,136,85))
    
    if usePennies:
        pennyImages = unPicklePennies()
        
        uniqueInputLums = {}
        for group in circlesAndLum:
            uniqueInputLums[group[1]] = []
        for lum in uniqueInputLums.keys():
            #Fixme: figure out how to set deviation (min value of 5 was predetermined for testing)
            mappedValues = calcMapValues(lum, \
                                         getMapData(mosaicData, pennyImages), \
                                         pennyImages, \
                                         maxDeviation=5 \
                                         )
            uniqueInputLums[lum] = mappedValues
        
        #TODO: Normalize the spans of lightness (easiest would be randomize the order in which circle areas are assigned

        usedPennyCount = 0
        missingPennyCount = 0
        paintByNumber = []
        for group in circlesAndLum:
            if triagePennies:
                nextPenny = ''
                lum = group[1]
                for i in uniqueInputLums[lum]:
                    if len(pennyImages[i]):
                        nextPenny = pennyImages[i].pop()
                        paintByNumber.append((group[0],i))
                        break
                if nextPenny:
                    usedPennyCount += 1
                    
                    img = pygame.image.load(nextPenny)
                    img = pygame.transform.scale(img, (radius*2, radius*2))
                    screen.blit(img,(group[0][0]-radius,group[0][1]-radius))
                else:
                    missingPennyCount += 1
                    pygame.draw.circle(screen, \
                                   (group[1],group[1],group[1]), \
                                   group[0],
                                   horizontalBisect \
                                   )
            else:
                lum = group[1]
                thisGroup = uniqueInputLums[lum][0]
                randFromGroup = 0
                if len(pennyImages[thisGroup]) > 1:
					randFromGroup = randrange(0,len(pennyImages[thisGroup]))
                
                
                img = pygame.image.load(pennyImages[thisGroup][randFromGroup])
                img = pygame.transform.scale(img, (radius*2, radius*2))
                screen.blit(img,(group[0][0]-radius,group[0][1]-radius))
        if triagePennies:
            print "Pennies Used:",usedPennyCount
            print "Pennies Still Needed:",missingPennyCount
            print
            print "Writing penny location info to paintByNumber.p"
            with open("paintByNumber.p","wb") as outfile:
                pickle.dump(paintByNumber, outfile)
            print "Done"
    else:
        print "Using greyscale circles (parameter option)" 
        for group in circlesAndLum:
            pygame.draw.circle(screen, \
                               (group[1],group[1],group[1]), \
                               group[0],
                               horizontalBisect \
                               )
    
    
    print "Saving screenshot."
    t1 = time()
    print t1-t0
    pygame.image.save(screen, "screenshot.jpeg")
    pygame.display.update()
    
    loopFlag = True
    while loopFlag:
       for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                 loopFlag = False

    pygame.quit()
    #return circlesAndLum
