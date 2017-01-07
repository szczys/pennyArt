import pygame
import pygame.camera
from PIL import Image, ImageOps, ImageDraw

DEVICE = '/dev/video0'
SIZE = (1280, 720)
FILENAME = 'capture.png'

OffsetX = 419
OffsetY = 110
radius = 180

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
    capture = True

    #get image for masking out the penny
    mask = makeCircleMask()
    
    while capture:
        screen = camera.get_image(screen)
        pygame.draw.circle(screen,(0,255,0),(OffsetX+radius,OffsetY+radius),radius+6,6)
        display.blit(screen, (0,0))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                capture = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
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
                    
                elif event.key == pygame.K_SPACE:
                    print "Spacebar"
    camera.stop()
    pygame.quit()
    return

if __name__ == '__main__':
    camstream()
