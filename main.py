# This is the main file that drives the game.
import pygame
from mob import Mob
from npc import Npc
from wall import Wall

def createRectangleHitbox(coordinates):
    # given top left and bottom right
    topLeft = coordinates[0]
    topRight = (coordinates[1][0],coordinates[0][1])
    bottomLeft = (coordinates[0][0],coordinates[1][1])
    bottomRight = coordinates[1]
    hitbox = ((topLeft,topRight),(topRight,bottomRight),(bottomRight,bottomLeft),(bottomLeft,topLeft))
    return hitbox

def createRectangleWall(coordinates,gameDisplay):
    # given top left and bottom right:
    width = coordinates[1][0]-coordinates[0][0]
    height = coordinates[1][1] - coordinates[0][1]
    x = (coordinates[0][0] + coordinates[1][0]) / 2
    y = (coordinates[0][1] + coordinates[1][1]) / 2
    sprite = pygame.transform.scale(pygame.image.load("wallTexture.png"),(width,height))
    wall = Mob(sprite,x,y,0,gameDisplay,10,1,0)
    return wall

#setup pygame
pygame.init()
#window dimensions
DisplayWidth = 1400
DisplayHeight = 1280
#colours
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
# collision map is a set of segments that block line of sight.
mapSegments = (
((450,200),(550,450)),
((850,200),(950,450)),
((250,450),(550,550)),
((850,450),(1200,550)),
((250,850),(550,950)),
((850,850),(1200,950)),
((450,950),(550,1100)),
((850,950),(950,1100))
)

gameDisplay = pygame.display.set_mode((DisplayWidth,DisplayHeight))
pygame.display.set_caption("stealthy")
clock = pygame.time.Clock()

walls = []
collisionMap = []
for coordinates in mapSegments:
    for i in createRectangleHitbox(coordinates):
        collisionMap.append(i)
    walls.append(createRectangleWall(coordinates,gameDisplay))
print collisionMap
npc = Npc(pygame.image.load("npcSprite.png"),700,700,0,gameDisplay,10,5,collisionMap)
mob = Mob(pygame.image.load("playerSprite.png"),1050,350,0,gameDisplay,10,5,collisionMap)
world = [mob];
finished = False
counter = 0
xMove = 0
yMove = 0
rotation = 0
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            break

        if event.type == pygame.KEYDOWN:
            #EXIT
            if(event.key == pygame.K_ESCAPE):
                finished = True
                print("QUITING")
            # X-AXIS MOVEMENT
            if event.key == pygame.K_LEFT:
                xMove = -10
            elif event.key == pygame.K_RIGHT:
                xMove = 10
            # Y-AXIS MOVEMENT
            if event.key == pygame.K_UP:
                yMove = -10
            elif event.key == pygame.K_DOWN:
                yMove = 10
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    xMove = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    yMove = 0
    mousepos = pygame.mouse.get_pos()
    mob.faceTarget((mousepos))
    npc.activate(world)
    # mob.rotate(rotation)
    # mob.faceTarget()
    mob.move(xMove,yMove)
    gameDisplay.fill(black)
    npc.draw()
    mob.draw()
    for i in walls:
        i.draw();
    pygame.display.update()
    clock.tick(60)

pygame.quit()

# Create world
# create player
#create mob
# create walls
