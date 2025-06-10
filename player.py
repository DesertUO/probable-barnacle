FacingIdle = 0
FacingRight = 1
FacingLeft = 2
FacingUp = 3
FacingDown = 4


# Player class
class Player(object):
    def __init__(self, x: int, y: int, game: "Game"):
        self.x = x
        self.y = y
        self.game = game

        self.kills = 0

        self.hasFired = False

        self.facing = FacingIdle

    def incrementKills(self):
        self.kills += 1

    def setKills(self, newNumber):
        self.kills = newNumber

    def getKills(self) -> int:
        return self.kills

    # Updates player depending on the key pressed
    # or whether the player is within boundries
    def update(self):
        # Input checking
        if self.game.char == "d":
            self.x = self.x+1
            self.facing = FacingRight
        if self.game.char == "a":
            self.x = self.x-1
            self.facing = FacingLeft
        if self.game.char == "w":
            self.y = self.y-1
            self.facing = FacingUp
        if self.game.char == "s":
            self.y = self.y+1
            self.facing = FacingDown

        if self.game.char == "f":
            self.hasFired = True
        else:
            self.hasFired = False

        # Boundry checking
        if self.x >= self.game.w:
            self.x = self.game.w-1
        if self.x < 0:
            self.x = 0
        if self.y >= self.game.h:
            self.y = self.game.h-1
        if self.y < 0:
            self.y = 0
