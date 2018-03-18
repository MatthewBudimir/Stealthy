def matchCoordinates(a,b):
    return (a[0] == b[0] and a[1] == b[1])
class Task(object):
    """docstring for Task."""
    # Task has: Conditions
    def __init__(self,pos,angle):
        super(Task, self).__init__()
        self.angleReq = angle
        self.positionReq = pos
    def fulfilled(self,npc):
        if npc.getCoordinates() == self.positionReq and npc.getFacing() == self.angleReq:
            print("Task fulfilled: Move to " + str(self.positionReq) + " turn to " + str(self.angleReq))
            print("NPC at: " + str(npc.getCoordinates()))
            return True
        else:
            return False

    def getAngle(self):
        return self.angleReq
    def getPos(self):
        return self.positionReq
