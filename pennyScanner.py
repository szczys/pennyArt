'''******************************
* Penny Mosaic Generator        *
* MIT License               	*
* Copyright 2017 - Mike Szczys  *
* http://jumptuck.com 	    	*
*				*
******************************'''

import pygame
import pygame.camera
import pygame.font
from PIL import Image, ImageOps, ImageDraw
import glob
from pennyArt import \
     getCircleAverageLuminosity, \
     getAllPointsInCircle, \
     unPicklePennies, \
     pickleHelper

DEVICE = '/dev/video1'
SIZE = (1280, 720)
FILENAME = 'capture.png'
#Sample basenames must have {number} in them and use 6-digit number in the scheme
SAMPLEBASENAME = 'sampleSet/{number}-penny.png'


#TODO: add settings file for persistent changes in GUI of these values
OffsetX = 411
OffsetY = 106
radius = 180

#speedup for finding circle points (do it once for each sample size):
circlePointsSet = {}

def getNextSampleFilename():
    #This will be called once and will find the highest
    #existing sample number and increment it by 1.
    #It will work even if there are some samples missing
    query = glob.glob(SAMPLEBASENAME.format(number="*"))
    if query == []:
        return SAMPLEBASENAME.format(number="000001")
    else:
        fileNumIdx = getFileNumIdx()
        highest = 0
        for fn in query:
            testVal = int(fn[fileNumIdx:fileNumIdx+6])
            if  testVal > highest:
                highest = testVal
        return makeSampleFilename(highest+1)

def getFileNumIdx():
    premask = SAMPLEBASENAME.format(number="######")
    fileNumIdx = len(premask.split("######")[0])
    return fileNumIdx

def makeSampleFilename(num):
    nextNum = str(num)
    nextNum = '0'*(6-len(nextNum)) + nextNum
    return SAMPLEBASENAME.format(number=nextNum)

def incrementFilename(curFn):
    fileNumIdx = getFileNumIdx()
    highest = int(curFn[fileNumIdx:fileNumIdx+6])+1
    return makeSampleFilename(highest)   

def makeCircleMask():
    #Tricks to make everything but penny transparent using mask:
    #http://stackoverflow.com/a/890114
    size = (radius*2,radius*2)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0)+size, fill=255)
    return mask

def characterizePenny(fn):
    global circlePointsSet
    pixels = pygame.surfarray.array3d(pygame.image.load(fn))
    if len(pixels) not in circlePointsSet.keys():
        centerX = len(pixels)/2
        r = centerX
        if r%2 == 0:
            r -= 1
        circlePointsSet[len(pixels)] = getAllPointsInCircle(centerX, centerX, r)
    lum = getCircleAverageLuminosity(pixels, circlePointsSet[len(pixels)])
    return lum

def camstream():
    #pygame camera code is by snim2 found here:
    #https://gist.github.com/snim2/255151
    pygame.init()
    pygame.camera.init()
    display = pygame.display.set_mode(SIZE, 0)
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)

    pygame.font.init()
    myfont = pygame.font.SysFont("monospace", 96)

    capture = True
    lastLum = 255
    #get image for masking out the penny
    mask = makeCircleMask()

    nextFilename = getNextSampleFilename()

    pennySet = unPicklePennies()
    
    while capture:
        global OffsetX
        global OffsetY
        global radius
        screen = camera.get_image(screen)
        pygame.draw.circle(screen,(0,255,0),(OffsetX+radius,OffsetY+radius),radius+6,6)
        pygame.draw.rect(screen, (255,255,255), (30,30,180,80), 0)
        displayLastLum = myfont.render(str(lastLum), 1, (0,0,0))
        screen.blit(displayLastLum,(35, 22))
        display.blit(screen, (0,0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                capture = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen = camera.get_image(screen)
                    pygame.draw.rect(screen, (255,0,0), (30,30,180,80), 0)
                    display.blit(screen, (0,0))
                    pygame.display.flip()
                    pygame.image.save(screen, FILENAME)
                    img = Image.open(FILENAME)
                    #Crop to Square
                    img2 = img.crop((OffsetX, OffsetY, OffsetX + (radius*2), OffsetY + (radius*2)))
                    #Do some magic to keep just a circle (the penny)
                    output = ImageOps.fit(img2, mask.size, centering=(0.5, 0.5))
                    output.putalpha(mask)
                    output.save(nextFilename)
                    #Characterize this:
                    lastLum = characterizePenny(nextFilename)
                    #Add to pennySet:
                    if lastLum in pennySet.keys():
                        pennySet[lastLum].append(nextFilename)
                    else:
                        pennySet[lastLum] = [nextFilename]

                    #Increment filename for next time
                    nextFilename = incrementFilename(nextFilename)
                    
                elif event.key == pygame.K_LEFT:
                    OffsetX -= 1
                    print OffsetX,OffsetY,radius
                elif event.key == pygame.K_RIGHT:
                    OffsetX += 1
                    print OffsetX,OffsetY,radius
                elif event.key == pygame.K_UP:
                    OffsetY -= 1
                    print OffsetX,OffsetY,radius
                elif event.key == pygame.K_DOWN:
                    OffsetY += 1
                    print OffsetX,OffsetY,radius
                elif event.key == pygame.K_EQUALS:
                    radius += 1
                    print OffsetX,OffsetY,radius
                elif event.key == pygame.K_MINUS:
                    radius -= 1
                    print OffsetX,OffsetY,radius

                elif event.key == pygame.K_ESCAPE:
                    capture = False
    camera.stop()
    pygame.draw.rect(screen, (255,0,0), (340,210,600,300), 0)
    saveModal = myfont.render("Save Penny", 1, (255,255,255))
    saveModal2 = myfont.render("Data? y/n", 1, (255,255,255))
    screen.blit(saveModal,(360, 230))
    screen.blit(saveModal2,(360, 360))
    display.blit(screen, (0,0))
    pygame.display.flip()
    loopFlag = True
    while loopFlag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                 loopFlag = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    pickleHelper('pennySet.p',pennySet) 
                    loopFlag = False
                elif event.key == pygame.K_n:
                    loopFlag = False
    pygame.quit()
    return

if __name__ == '__main__':
    camstream()
