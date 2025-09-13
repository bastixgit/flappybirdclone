import pygame, time, random
(width, height) = (1200, 800)
pos_x, pos_y = 200, 100
velocity = 0
jumped = False
pipes = []
global score
score = 0
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill((0, 181, 204))

# Step 1: Load a font (size 36 here)
font = pygame.font.SysFont("Arial", 36)


def applyGravity(dt):
    global velocity
    velocity = velocity + 0.4 * dt
    

def applyJump():
    global velocity
    velocity = -12

def createPipe():
    topSectionHeight = random.randint(100, 400)
    passageHeight = random.randint(300, 400)
    pipeConfig = [1200, topSectionHeight, passageHeight, False] #[x, topSectionHeight, passageHeight, scored]
    pipes.append(pipeConfig)

def drawPipe(pipeConfig):

    pygame.draw.rect(screen,(200,80,100),(pipeConfig[0],0,100,pipeConfig[1]), border_bottom_left_radius = 30, border_bottom_right_radius = 30)
    pygame.draw.rect(screen,(200,80,100),(pipeConfig[0],0+pipeConfig[1]+ pipeConfig[2],100,800), border_radius = 30)

def movePipe(pipeConfig):
    pipeConfig[0] = pipeConfig[0] - 2.5 * dt
    if pipeConfig[0]==-100:
        pipes.remove(pipeConfig)

def checkCollision():
    global closest_pipe
    current_min_distance = 1000
    closest_pipe = None
    for pipe in pipes:
        if pipe[0]>pos_x-115:
            distance = pipe[0] - pos_x
            if distance < current_min_distance:
                current_min_distance = distance
                closest_pipe = pipe
    # checke ob die pipe in den x koordinationen zwischen 185 und 215 ist heißt ob closestPipe[0] zwischen 185 bis 115 ist
    if closest_pipe[0]<185 and closest_pipe[0]>115:
    # wenn das der Fall finde die y koordinaten des gateways (zwischen topSectionHeight und topSectionHeight + passageHeight)
        gatewayTop = closest_pipe[1]
        gatewayBottom = gatewayTop + closest_pipe[2]
     # dannach schaue ob die spieler y Koordinate + - 15 außerhalb des gateway berecih liegt
        if pos_y-15 > gatewayBottom or pos_y+15<gatewayTop:
            global running
            running = False

def checkScore():
    global score
    for pipe in pipes:
        if pipe[0]<pos_x -115 and pipe[3] == False:
            score +=1
            pipe[3]  = True

    scoreboard = font.render(f"score: {score}", True, (255, 255, 255))  # White text
    screen.blit(scoreboard, (100, 100))

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
    if pipes:
        checkCollision()
        checkScore()
    
    pygame.draw.circle(screen, (200,80,100), (pos_x,pos_y), 30)
    pygame.display.flip()

pygame.quit()