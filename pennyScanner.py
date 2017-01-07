import pygame
import pygame.camera
import pygame.font
from PIL import Image, ImageOps, ImageDraw
import glob

DEVICE = '/dev/video0'
SIZE = (1280, 720)
FILENAME = 'capture.png'
#Sample basenames must have {number} in them and use 6-digit number in the scheme
SAMPLEBASENAME = 'sampleSet/{number}-penny.png'


#TODO: add settings file for persistent changes in GUI of these values
OffsetX = 419
OffsetY = 110
radius = 180

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
                    display.blit(screen, (0,0))
                    pygame.image.save(screen, FILENAME)
                    img = Image.open(FILENAME)
                    #Crop to Square
                    img2 = img.crop((OffsetX, OffsetY, OffsetX + (radius*2), OffsetY + (radius*2)))
                    #Do some magic to keep just a circle (the penny)
                    output = ImageOps.fit(img2, mask.size, centering=(0.5, 0.5))
                    output.putalpha(mask)
                    output.save('capture2.png')
                    
                elif event.key == pygame.K_LEFT:
                    OffsetX -= 1
                elif event.key == pygame.K_RIGHT:
                    OffsetX += 1
                elif event.key == pygame.K_UP:
                    OffsetY -= 1
                elif event.key == pygame.K_DOWN:
                    OffsetY += 1
                elif event.key == pygame.K_PLUS:
                    radius += 1
                elif event.key == pygame.K_MINUS:
                    radius -= 1

                elif event.key == pygame.K_ESCAPE:
                    capture = False
    camera.stop()
    pygame.quit()
    return

if __name__ == '__main__':
    camstream()
