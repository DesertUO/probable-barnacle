import os
from utils import os_specific
from get_input import getchar
from entity import Entity
from entity_manager import EntityMannager
from config import Config


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


# Game class
class Game(object):
    def __init__(self, title: str, defaultMap: str = "default_map.txt",
                 defaultConfig: str = "config.txt"):
        self.title = title

        self.isRunning = False
        self.char = ''

        self.defaultConfig = defaultConfig
        # Default only if config fails (just for linter and intellisense anti-error method idk)
        self.borderConfig = ["|","*","~","*","|","*","~","*"]
        self.config = Config(self)

        self.charPairs = {"-": " ", "S": "S"}

        # Reading the default map, defined in the player constructor
        # (defaultMap)
        with open(defaultMap, "r") as file:
            mapContent = file.read().split("\n")
            mapReading = []
            for line in mapContent:
                if not line == "":
                    # Checking if the line is a comment, prefixed by a "#"
                    if line[0] == "#":
                        continue
                    if "WIDTH" == line.split(" ")[0]:
                        self.w = int(line.split(" ")[1])
                    elif "HEIGHT" == line.split(" ")[0]:
                        self.h = int(line.split(" ")[1])
                    else:
                        mapReading.append(line)
            newMap = []
            for line in mapReading:
                for el in line.split(" "):
                    newMap.append(el)

        self.map = newMap

        # self.entities = HashTable(889)
        self.entityManager = EntityMannager(self)
        self.entities = self.entityManager.get_entities()

        # Setting a Player instance from the player position in the map
        if "P" in self.map:
            self.player = Player(self.get_player_pos_in_map()[1],
                                 self.get_player_pos_in_map()[0], self)
            for i in range(0, self.w * self.h - 1):
                if self.map[i] == "P":
                    self.map[i] = "S"
        # If player is not in the defaultMap then default it to (0, 0)
        else:
            self.player = Player(0, 0, self)
            self.map[0] = "S"

    # Function to get the element in given position (row, col)
    def get_el_in_map(self, row: int, col: int) -> str:
        if (col < 0 or col >= self.w) or (row < 0 or row >= self.h):
            raise Exception("Invalid index for map: col:" +
                            str(col) + ", row:" + str(row))

        return self.map[(row * self.w) + col]

    # Function to get the position of the player
    def get_player_pos_in_map(self) -> list[int]:
        row = 0
        col = 0
        for el in self.map:
            if (col >= self.w):
                col = 0
                row += 1
            if el == "P":
                return [row, col]
            col += 1
        return [-1, -1]

    # Game runner/starter
    def run(self):
        self.isRunning = True

        while (self.isRunning):
            os_specific(lambda: os.system("cls"), lambda: os.system("clear"))
            self.update()
            self.render()
            self.char = getchar()

    # Game stopper/shutdown(er)
    def stop(self):
        self.isRunning = False
        print("Game successfully exited!")
        quit()

    # So much nesting aaaaaaaa
    # Game updater
    def update(self):
        if self.char == "0":
            self.stop()
        self.player.update()
        if self.player.hasFired:
            self.entities.append(Entity(len(self.entities)+1, self.player.x + (self.player.facing == FacingRight) - (self.player.facing == FacingLeft), self.player.y - (self.player.facing == FacingUp) + (self.player.facing == FacingDown), "bullet"))
            self.entities[len(self.entities)-1].bullet_step = 0
            self.entities[len(self.entities)-1].bullet_dir = self.player.facing

        # Monster killing (WIP)
        for entity in self.entities:
            if self.player.x == entity.x and self.player.y == entity.y:
                match entity.get_type():
                    case "monster":
                        self.entities.remove(entity)
            if entity.get_type() == "bullet":
                for entity1 in self.entities:
                    if entity1.type == "monster":
                        if (entity.x == entity1.x) and (entity.y == entity1.y):
                            self.entities.remove(entity)
                            self.entities.remove(entity1)
                            self.player.incrementKills()
                entity.bullet_step += 1
                if (entity.bullet_step == 10):
                    self.entities.remove(entity)
                else:
                    entity.x += (entity.bullet_dir == 1) - (entity.bullet_dir == 2)
                    entity.y += -(entity.bullet_dir == 3) + (entity.bullet_dir == 4)

    # Game renderer
    def render(self):
        # Misc
        print("Welcome to " + self.title + "!")
        print("Kills: " + str(self.player.getKills()))
        # print("Key pressed: ", self.char)
        # Print bottom side
        print()
        print("Press '0' to quit")
        print("Has the player fired a shot?:", self.player.hasFired)

        print(self.borderConfig[1] + self.w*self.borderConfig[2] + self.borderConfig[3])
        for row in range(0, self.h):
            # Print left side
            print(self.borderConfig[0], end="")
            for col in range(0, self.w):
                for entity in self.entities:
                    # If curent cell has the position of an entity then do this
                    if col == entity.x and row == entity.y:
                        if ((entity.x == self.player.x) and
                                (entity.y == self.player.y)):
                            print(entity.char, end="\b")
                        else:
                            print(entity.char, end="")
                # If current cell has the position of the player then do this
                if col == self.player.x and row == self.player.y:
                    match self.player.facing:
                        case 0:
                            print("x", end="")
                        case 1:
                            print(">", end="")
                        case 2:
                            print("<", end="")
                        case 3:
                            print("˄", end="")
                        case 4:
                            print("˅", end="")
                        case _:
                            print("x", end="")
                # else
                else:
                    # We already check for player pos. here we check if current
                    # cell is a cell of any entity, and if not, then print " "
                    isOnTop = False
                    for entity in self.entities:
                        if col == entity.x and row == entity.y:
                            isOnTop = True
                    if not isOnTop:
                        print(self.charPairs.get(self.get_el_in_map(row, col)),
                              end="")
            # Print right side
            print(self.borderConfig[4] + "\n", end="")
        # Print bottom side
        print(self.borderConfig[7] + self.w*self.borderConfig[6] + self.borderConfig[5])


# Main function
def main():
    game = Game("test game")
    game.run()


# If this is the file executed
if __name__ == '__main__':
    main()
