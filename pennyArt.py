import pygame
import sys

#393x488
x = 786
y = 976

#### Calculating Luminance ####
#http://stackoverflow.com/a/689547
# first divide R G B by 255, and compute
# Y = .2126 * R^gamma + .7152 * G^gamma + .0722 * B^gamma
# assume gamma of 2.2

def luminance(pixelColors):
    #pixelColors will be 3 value tuple
    gamma = 2.2
    lum = (.2126 * ((pixelColors[0]/255)**gamma)) + \
          (.7152 * ((pixelColors[1]/255)**gamma)) + \
          (.0722 * ((pixelColors[2]/255)**gamma))

    
    return lum

###############################

#### Is point inside a circle? ####
#http://stackoverflow.com/a/15856549
#
# Quadratic equation calculates if it is on the hypotenuse
# Do this for one quadrant and then transpose the points

def getAllPointsInCircle(x,y,r):
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

def testPoints(x):
    for i in range(21):
            thisRow = ""
            for j in range(21):
                    if (j,i) in x:
                            thisRow += "0 "
                    else:
                            thisRow += "- "
            print thisRow

###################################


red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

#Begin messy triangle prototyping

#horizontal distances should be easy:
horizontalBisect = 15

#vertial is trickier (non-integer)
from math import sqrt
verticalDist = sqrt(((horizontalBisect*2)**2)-(horizontalBisect**2))

def vertRounded(multiple):
    #give this function a multiple to use with verticalDist
    #it will return the nearest integer to plot in display
    return int(round(multiple*verticalDist))

def calcVertices(xSize,ySize):
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
            curY = int(round((verticalDist*row)+horizontalBisect))
            if curY > (ySize-horizontalBisect):
                return allVertices

def getPixelArray(filename):
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    return pygame.surfarray.array3d(image)

def runGame():
    pygame.init()
    screen = pygame.display.set_mode((x,y))
    screen.fill(red)

    testPoints = calcVertices(x,y)

    pixels = getPixelArray('mahler2.jpg')
    print pixels.shape


    #pygame.draw.lines(screen, blue, True, testPoints, 2)

    for points in testPoints:
        pygame.draw.circle(screen, blue, points,horizontalBisect)



    pygame.display.update()

    while True:
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit(); sys.exit();
