import pygame
import math
from lines import intercept
def calcAngle(x1,y1,x2,y2):
    # calc top
    #vector 2 should be a vector coming from p1:
    x2 = x2-x1
    y2 = y2-y1
    # vector 1 should be a vertical line from p1 // upside down because pygame...
    x1 = 0
    y1 = -1
    dot = x1*x2 + y1*y2
    denominator = math.sqrt(x2**2 + y2**2);
    if denominator == 0:
        return 0
    left = dot/denominator;

    angle = (math.acos(left)*180/math.pi)
    if(x2>0):
        angle = angle*-1
    return angle
def normalAngle(theta):
    while theta < 0:
        theta = 360+theta
    while theta > 360:
        theta = theta-360
    if theta == 360:
        return 0
    return theta

def betweenAngle(theta,lower,upper):
    # normalize.
    lower = normalAngle(lower)
    upper = normalAngle(upper)
    theta  = normalAngle(theta)
    if lower > upper:
        # it's might get complicated
        return theta>lower or theta<upper
    else:
        return theta > lower and theta < upper


class Mob(object):
    """docstring for Mob."""
    def __init__(self, sprite,x,y,facing,surface,speed,turnSpeed,collisionMap):
        super(Mob, self).__init__()
        self.sprite = sprite.copy()
        self.x = x
        self.y = y
        self.facing = facing
        self.turningRate = turnSpeed
        if facing == 0:
            self.rotated = False
            self.rect = sprite.get_rect(center=(x,y))
            self.display = sprite.copy()
        else:
            self.display = pygame.transform.rotate(self.sprite,self.facing)
            self.rect = sprite.get_rect(center=(x,y))
        self.surface = surface
        self.speed = speed
        self.collisionMap = collisionMap
    def draw(self):
        self.surface.blit(self.display,self.rect)
    def move(self,x,y):
        # check that we haven't crossed over into a wall.
        # we are a ball shaped object with radius 50.
        # we are moving from x1,y1 to x2,y2 so that is our segment: If there's a collision then we will stop there.
        segment = ((self.x,self.y),(self.x+x,self.y+y))
        collision = False
        collisionCoordinates = (0,0)
        for i in self.collisionMap:
            collision,collisionCoordinates = intercept(segment,i)
            if collision:
                break
        if collision:
            if x>0:
                self.x = collisionCoordinates[0] - 1
            if x<0:
                self.x = collisionCoordinates[0] + 1
            if y>0:
                self.y = collisionCoordinates[1] - 1
            if y<0:
                self.y = collisionCoordinates[1] + 1
        else:
            self.x = self.x+x
            self.y =self.y+y
        self.rect.center = (self.x,self.y)
    def rotateTo(self,facing):
        # Well... We should try rotate to the new location as much as we can in this frame:
        # normalize input to be within 360:
        facing = normalAngle(facing)
        self.facing = normalAngle(self.facing)
        # if we're close enough, just set it to be there.
        # print(str(facing) + "," + str(self.facing))

        if self.facing-self.turningRate-1 < facing and self.facing+self.turningRate+1 > facing:
            self.facing = facing
        else:
            # find out if we should be turning left or right:
            thetaPrime = 360-self.facing
            if (self.facing<=180 and ((facing > self.facing) and facing < normalAngle(self.facing + 180))) or (normalAngle(facing+thetaPrime)>0 and normalAngle(facing+thetaPrime) < 180):
                # rotate right
                turn = self.turningRate
            else:
                # rotate left
                turn = -1*self.turningRate

            self.facing = self.facing + turn;
        # self.facing = facing
        self.display = pygame.transform.rotate(self.sprite,self.facing)
        self.rect = self.display.get_rect(center=(self.x,self.y))
    def faceTarget(self,coordinates):
        # target is at angle theta
        # coordinates = (400,400)
        theta = calcAngle(self.x,self.y,coordinates[0],coordinates[1])
        self.rotateTo(theta)
    def getCoordinates(self):
        return (self.x,self.y)
    def getFacing(self):
        return self.facing
