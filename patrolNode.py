
class patrolNode(object):
    """docstring for patrolNode."""
    def __init__(self, sprite,x,y,facing,surface,speed,turnSpeed,collisionMap):
        super(Mob, self).__init__()
        self.sprite = sprite.copy()
        self.x = x
        self.y = y
