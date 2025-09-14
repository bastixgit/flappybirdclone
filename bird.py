import pygame, time, random, shelve
(width, height) = (1200, 800)
pos_x, pos_y = 200, 100
velocity = 0
jumped = False
pipes = []
global score
score = 0
pygame.font.init()
screen = pygame.display.set_mode((width, height))
screen.fill((0, 181, 204))

# Step 1: Load a font (size 36 here)
font = pygame.font.SysFont("Arial", 36)

d = shelve.open('score.txt')  # here you will save the score variable   
try:
    highscore = d['score']  # the score is read from disk
except: 
    d['score'] = 0
    highscore = 0

def applyGravity(dt):
    global velocity
    velocity = velocity + 0.4 * dt
    

def applyJump():
    global velocity
    velocity = -12

def createPipe():
    topSectionHeight = random.randint(100, 300)
    passageHeight = random.randint(250, 400)
    pipeConfig = [1200, topSectionHeight, passageHeight, False] #[x, topSectionHeight, passageHeight, scored]
    pipes.append(pipeConfig)

def drawPipe(pipeConfig):

    pygame.draw.rect(screen,(200,80,100),(pipeConfig[0],0,100,pipeConfig[1]), border_bottom_left_radius = 10, border_bottom_right_radius = 10)
    pygame.draw.rect(screen,(200,80,100),(pipeConfig[0],0+pipeConfig[1]+ pipeConfig[2],100,800), border_radius = 10)

def movePipe(pipeConfig):
    pipeConfig[0] = pipeConfig[0] - 3 * dt
    if pipeConfig[0]==-100:
        pipes.remove(pipeConfig)

def circleRectCollision(cx, cy, radius, rx, ry, rw, rh):
    # Find the closest point on the rectangle to the circle center
    closest_x = max(rx, min(cx, rx + rw))
    closest_y = max(ry, min(cy, ry + rh))

    # Calculate distance from circle center to closest point
    distance_x = cx - closest_x
    distance_y = cy - closest_y

    # If the distance is less than the radius, there's a collision
    return (distance_x**2 + distance_y**2) < (radius**2)

def checkCollision():
    global running
    radius = 30
    for pipe in pipes:
        pipe_x = pipe[0]
        top_height = pipe[1]
        gap_height = pipe[2]

        # Top pipe rectangle: (pipe_x, 0, 100, top_height)
        top_collision = circleRectCollision(pos_x, pos_y, radius, pipe_x, 0, 100, top_height)

        # Bottom pipe rectangle: (pipe_x, top_height + gap_height, 100, height)
        bottom_collision = circleRectCollision(pos_x, pos_y, radius, pipe_x, top_height + gap_height, 100, height)

        if top_collision or bottom_collision:
            running = False

def checkScore():
    global score
    for pipe in pipes:
        if pipe[0]<pos_x -115 and pipe[3] == False:
            score +=1
            pipe[3]  = True

    scoreboard = font.render(f"highscore: {highscore}", True, (255, 255, 255))  # White text
    screen.blit(scoreboard, (950, 25))
    scoreboard = font.render(f"score: {score}", True, (255, 255, 255))  # White text
    screen.blit(scoreboard, (750, 25))

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

if score > highscore:
    d['score'] = score
d.close()
print(f"Highscore: {highscore}")
print(f"Your score: {score}")

try: 
    pygame.quit()
    print("Quitted pygame")
except Exception as e:
    print("Error quitting pygame:", e)
