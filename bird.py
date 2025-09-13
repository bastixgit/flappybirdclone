import pygame, time, random
(width, height) = (1200, 800)
pos_x, pos_y = 200, 100
velocity = 0
jumped = False
pipes = []
screen = pygame.display.set_mode((width, height))
screen.fill((0, 181, 204))


def applyGravity(dt):
    global velocity
    velocity = velocity + 0.4 * dt
    

def applyJump():
    global velocity
    velocity = -12

def createPipe():
    topSectionHeight = random.randint(100, 400)
    passageHeight = random.randint(300, 400)
    pipeConfig = [1200, topSectionHeight, passageHeight] #[x, topSectionHeight]
    pipes.append(pipeConfig)

def drawPipe(pipeConfig):

    pygame.draw.rect(screen,(200,80,100),(pipeConfig[0],0,100,pipeConfig[1]))
    pygame.draw.rect(screen,(200,80,100),(pipeConfig[0],0+pipeConfig[1]+ pipeConfig[2],100,800))

def movePipe(pipeConfig):
    pipeConfig[0] = pipeConfig[0] - 2.5 * dt
    if pipeConfig[0]==-100:
        pipes.remove(pipeConfig)

def checkCollision():
    pass
    #check if player is left, above or below the rectangle
    # compare the distance between the side of the rectangle and the middlepoint of the player to the radius


last_time = time.time()
clock = pygame.time.Clock()
pipeCounter = random.randint(30,120)
#createPipe()
#loop
running = True
while running:
    clock.tick(60)

    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()
    screen.fill((0, 181, 204))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                applyJump()
                jumped = True
            elif event.key == pygame.K_ESCAPE:
                running = False
    if jumped==False:
        applyGravity(dt)
    jumped = False
    pos_y += velocity

    if pipeCounter == 0:
        createPipe()
        pipeCounter = random.randint(90,200)
    else:
        pipeCounter -= 1

    # draw the objects
    for pipe in pipes:
        drawPipe(pipe)
        movePipe(pipe)
    pygame.draw.circle(screen, (200,80,100), (pos_x,pos_y), 30)
    pygame.display.flip()

