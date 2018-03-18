# from mob import Mob
from mob import Mob
from mob import calcAngle
from mob import betweenAngle
from mob import normalAngle
from task import Task
from lines import intercept
import Queue
import math
# An NPC is a mob that has a queue of tasks that it needs to complete.
class Npc(Mob):
    """docstring for Npc."""
    def __init__(self,sprite,x,y,facing,surface,speed,turnSpeed,collisionMap):
        super(Npc, self).__init__(sprite,x,y,facing,surface,speed,turnSpeed,collisionMap)
        self.tasks = Queue.PriorityQueue()
        self.currentTask = Task((x,y),0) # generate first task
        self.speed = 5
        self.patrol = ((700,100),(700,700),(1300,700),(700,700),(700,1150),(700,700),(100,700),(700,700))
        self.patrolStep = 0
        self.n = 0
    def moveTo(self,coordinates):
        if coordinates != (self.x,self.y):
            movementVector = (coordinates[0]-self.x,coordinates[1] - self.y)
            scalar = self.speed/(math.sqrt(((coordinates[0]-self.x)**2) + ((coordinates[1]-self.y)**2)))
            if scalar > 1:
                self.x = coordinates[0]
                self.y = coordinates[1]
            else:
                destination = (movementVector[0]*scalar,movementVector[1]*scalar)
                self.x = self.x + destination[0]
                self.y = self.y + destination[1]
    def lookTo(self,theta):
        self.rotateTo(theta)
    def genPatrolTask(self):
        # Face patrol target.
        n = self.patrolStep
        angle = normalAngle(calcAngle(self.x,self.y,self.patrol[n][0],self.patrol[n][1]))
        left = normalAngle(angle-89)
        right = normalAngle(angle+89)
        print("I will look to " +str(angle) + " a place without moving")
        priority = 100 #Priority 100 means that other tasks will be more important than this tasks if they come up.
        self.tasks.put((priority+1,Task((self.x,self.y),angle)))
        # Move there.
        print("I will then move there, not changing my angle")
        self.tasks.put((priority+2,Task((self.patrol[n][0],self.patrol[n][1]),angle)))
        # self.tasks.put(Task((self.patrol[n][0],self.patrol[n][1]),angle,1))
        # Stop and look around
        print("And then i'll look around")
        self.tasks.put((priority+3,Task((self.patrol[n][0],self.patrol[n][1]),right)))
        self.tasks.put((priority+4,Task((self.patrol[n][0],self.patrol[n][1]),left)))
        self.tasks.put((priority+5,Task((self.patrol[n][0],self.patrol[n][1]),angle)))
        # Increment patrol step
        self.patrolStep = (self.patrolStep + 1) % len(self.patrol)
        print(self.patrolStep)
    def activate(self,world):
        # Take a Queue

        if self.currentTask.fulfilled(self):
            self.n = self.n+1
            print("count " + str(self.n))
            # we need a new task:
            if self.tasks.empty():
                self.genPatrolTask()
            self.currentTask = self.tasks.get()[1]
            print("Starting task: Move to: " +str(self.currentTask.getPos()) +" turning to " +  str(self.currentTask.getAngle()))

        self.lookTo(self.currentTask.getAngle())
        self.moveTo(self.currentTask.getPos())
        self.detect(world)

    def detect(self,world):
        # print("looking at " + str(self.facing))
        for person in world:
            # figure out if I can see them:
            angle = calcAngle(self.x,self.y,person.x,person.y)
            upper = angle + 45
            lower = angle - 45
            if betweenAngle(self.facing,lower,upper):
                # we can see them!
                # Check collisionMap to see if there's a wall in the way.
                # print("Someone in sight")
                blocked = False
                for segment in self.collisionMap:
                    blocked,coor = intercept(((self.x,self.y),(person.x,person.y)),segment)
                    if blocked:
                        break
                if not blocked:
                    print("I see target at: " + str(person.x) + "," + str(person.y))
