import pygame
import glob

SAMPLEBASENAME = 'sampleSet/{number}-penny.png'

def samplePennies(baseName=SAMPLEBASENAME):
    #process the penny sample set to characterize their luminance values
    #returns list of tuples: (luminance value, image name)

    #default image names look like: 'sampleSet/000001-penny.png'
    #images should be square with penning spanning edge to edge
    #this will automatically poll largest circular area in the image

    sampleFileList = glob.glob(baseName.format(number="*"))
    circlePointSets = {}
    
    pennySet = {}
    count = 1
    print "Characterizing ", len(sampleFileList), "pennies..."
    for sample in sampleFileList:
        if count%25 == 0:
            print 'Characterization Progress:', count, 'of', len(sampleFileList), 'pennies.'
        count += 1

        #assume sample is square, use height to get values we need
        pixels = getPixelArray(sample)
        
        centerX = len(pixels)/2
        r = centerX
        if r%2 == 0:
            r -= 1
            
        if len(pixels) not in circlePointSets.keys():
            circlePointSets[len(pixels)] = getAllPointsInCircle(centerX,centerX,r)
        
        #lumValue = getLuminosityValues([(radius,radius)],1,radius,sample)[0][1]
        lumValue = getCircleAverageLuminosity(pixels, circlePointSets[len(pixels)])
        
        if lumValue not in pennySet.keys():
            pennySet[lumValue] = [sample]
        else:
            pennySet[lumValue].append(sample)
    print "Done!"
    print
    return pennySet

def getPixelArray(filename):
    #Get all RGB pixel colors from this image file
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    return pygame.surfarray.array3d(image)

def getLuminosityValues(listOfPoints, scalingValue, radiusBeforeScaling, sourceImage):
    #scaling value is how much to divide the
    #xy values by to fit within source image resolution
    lumList = []
    
    #Get pixel data from source image
    pixels = getPixelArray(sourceImage)
    #print pixels.shape

    adjustedR = radiusBeforeScaling/scalingValue
    testPoints = getAllPointsInCircle(adjustedR, adjustedR, adjustedR)

    #iterate each point in listOfPoints
    for point in listOfPoints:
        #get list of points in circle around each point
        testOffsetX = (point[0]/scalingValue)-adjustedR
        testOffsetY = (point[1]/scalingValue)-adjustedR

        lumAvg = getCircleAverageLuminosity( \
            pixels, \
            testPoints, \
            (testOffsetX, testOffsetY) \
            )
        lumList.append([point,lumAvg])
        if len(lumList)%250 == 0:
            print "Calculated",len(lumList),"values so far..."

    return lumList

def getPixelLuminance(pixelColors):
    #pixelColors will be 3 value tuple

    #### Calculating Luminance ####
    #http://stackoverflow.com/a/689547
    # first divide R G B by 255, and compute
    # Y = .2126 * R^gamma + .7152 * G^gamma + .0722 * B^gamma
    # assume gamma of 2.2
    
    #actually ended up going with this simple equation:
    #http://stackoverflow.com/a/596243
    
    lum = (.299 * pixelColors[0]) + \
          (.587 * pixelColors[1]) + \
          (.114 * pixelColors[2])
    
    return int(lum)
    
def getCircleAverageLuminosity(pixArray, pixelsToTest, offsets=(0,0)):
    #pixArray is an image loaded and passed into this function
    #pixelsToTest are a circular area of points (x,y)
    #offsets are so you can use the same pixelsToTest array and move it around
    #a larger image if necessary.
    pixelAverages = [0,0,0]
    #moved to averaging colors then calculating luminance (~6.9x speedup).
    #possible loss of precision? But I think it is still valid. 
    for point in pixelsToTest:
        thisPixel = pixArray[point[0]+offsets[0], point[1]+offsets[1]]
        pixelAverages[0] += thisPixel[0]
        pixelAverages[1] += thisPixel[1]
        pixelAverages[2] += thisPixel[2]
    pixelAverages[0] = pixelAverages[0]/len(pixelsToTest)
    pixelAverages[1] = pixelAverages[1]/len(pixelsToTest)
    pixelAverages[2] = pixelAverages[2]/len(pixelsToTest)
    pixelLum = getPixelLuminance(pixelAverages)
    return pixelLum
    
def getAllPointsInCircle(x,y,r):
	#### Is point inside a circle? ####
	#http://stackoverflow.com/a/15856549
	#
	# Quadratic equation calculates if it is on the hypotenuse
	# Do this for one quadrant and then transpose the points
	
    quarterPoints = []

    for testX in range(x-r,x+1):
        for testY in range(y-r,y+1):
            aLen = x-testX
            bLen = y-testY
            if (aLen**2) + (bLen**2) <= r*r:
                quarterPoints.append((testX,testY))
    
    #We now have a quarter circle, fill out the set
    allPoints = set([]) #use a set to avoid duplicate points
    for points in quarterPoints:
        
        reflectX = x+(x-points[0])
        reflectY = y+(y-points[1])

        allPoints.add(points)
        allPoints.add((reflectX,points[1]))
        allPoints.add((points[0],reflectY))
        allPoints.add((reflectX,reflectY))
    return allPoints
