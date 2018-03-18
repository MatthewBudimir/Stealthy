from mob import Mob

class Player(Mob):
    """docstring for Player."""
    def __init__(self, arg):
        super(Player, self).__init__()
        self.arg = arg
    def activate(self):
        pass
