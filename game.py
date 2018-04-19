import pygame, random, sys ,os,time
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5
acc_scale = 0.5
acc = 0
brake_signal = 0
car_speed = 0
count=3
baddies_acc=0.2;

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

# fonts
font = pygame.font.SysFont(None, 20)

# sounds
#gameOverSound = pygame.mixer.Sound('music/crash.wav')
#laugh = pygame.mixer.Sound('music/laugh.wav')


# images
playerImage = pygame.image.load('image/car1.png')
car3 = pygame.image.load('image/car3.png')
car4 = pygame.image.load('image/car4.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('image/car2.png')
sample = [car3,car4,baddieImage]
wallLeft = pygame.image.load('image/left.png')
wallRight = pygame.image.load('image/right.png')


# "Start" screen
drawText('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
drawText('And Enjoy', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3)+30)
pygame.display.update()
waitForPlayerToPressKey()
zero=0
accfile=0
speedfile=0
record_flag=False

# init record file
if not os.path.exists("data/accelerate.dat"):
    accfile=open("data/accelerate.dat",'w')
    accfile.write(str(zero))
    accfile.close()   
else:
    accfile=open("data/accelerate.dat",'r+')

if not os.path.exists("data/speed.dat"):
    speedfile=open("data/speed.dat",'w')
    speedfile.write(str(zero))
    speedfile.close()   
else:
    speedfile=open("data/speed.dat",'r+')

while (count>0):
    # start of the game
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 200)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0

    while True: # the game loop
        score += 1 # increase score

        for event in pygame.event.get():
            
            if event.type == QUIT:
                accfile.close()
                speedfile.close()
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == ord('r'):
                    record_flag = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == ord('b'):
                    brake_signal = 1
                    car_speed = 0
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    acc = acc_scale
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    acc = -acc_scale
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == ord('r'):
                    record_flag = False
                if event.key == K_UP or event.key == ord('w'):
                    acc = 0
                if event.key == K_DOWN or event.key == ord('s'):
                    acc = 0
                if event.key == K_ESCAPE:
                   accfile.close()
                   speedfile.close()
                   terminate()
            

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            

        # Add new baddies at the top of the screen
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            if len(baddies)<3:
                baddieSize =30 
                newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface':pygame.transform.scale(random.choice(sample), (23, 47)),
                            }
                baddies.append(newBaddie)
            
            

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            car_speed += acc  
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            car_speed += acc  
            if car_speed < -10:
                car_speed = -10
        
        for b in baddies:
            if not reverseCheat and not slowCheat:
                if b['speed']>baddies_acc:
                    b['speed'] -= baddies_acc 
                else:
                    b['speed'] = 0 
                b['rect'].move_ip(0, car_speed-b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         
        # baddies out of window
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('accelerate: %s' % (acc), font, windowSurface, 128, 0)
        drawText('speed: %s' % (car_speed), font, windowSurface,128, 20)
        
        windowSurface.blit(playerImage, playerRect)

        
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        sideLeft= {'rect': pygame.Rect(0,0,126,600),
                   'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                   'surface':pygame.transform.scale(wallLeft, (126, 599)),
                   }
        sideRight= {'rect': pygame.Rect(497,0,303,600),
                   'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                   'surface':pygame.transform.scale(wallRight, (303, 599)),
                   }
        windowSurface.blit(sideLeft['surface'], sideLeft['rect'])
        windowSurface.blit(sideRight['surface'], sideRight['rect'])
        
        pygame.display.update()

        # add code record speed and accelerate
        # Check if any of the car have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            accfile.close()
            speedfile.close()
            terminate()
            break

        if record_flag:
            accfile.write(str(acc))
            accfile.write(" ")
            speedfile.write(str(car_speed))
            speedfile.write(" ")

        mainClock.tick(FPS)

    # "Game Over" screen.
    count=count-1
    #gameOverSound.play()
    time.sleep(1)
    if (count==0):
     #laugh.play()
     drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
     drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
     pygame.display.update()
     time.sleep(2)
     waitForPlayerToPressKey()
     count=3
     #gameOverSound.stop()
