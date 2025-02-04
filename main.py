import os
from get_input import getchar
from entity import Entity


class Player(object):
    def __init__(self, x: int, y: int, game: "Game"):
        self.x = x
        self.y = y
        self.game = game

        self.kills = 0

    def update(self):
        if self.game.char == "d":
            self.x = self.x+1
        if self.game.char == "a":
            self.x = self.x-1
        if self.game.char == "w":
            self.y = self.y-1
        if self.game.char == "s":
            self.y = self.y+1

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
    def __init__(self, title: str, defaultMap: str = "default_map.txt"):
        self.title = title

        self.isRunning = False
        self.char = ''

        # self.entities = HashTable(889)
        self.entities = []

        with open(defaultMap, "r") as file:
            mapContent = file.read().split("\n")
            mapReading = []
            for line in mapContent:
                if not line == "":
                    if not line[0] == "#":
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

        if "P" in self.map:
            self.player = Player(self.get_player_pos_in_map()[1],
                                 self.get_player_pos_in_map()[0], self)
            for i in range(0, self.w * self.h - 1):
                if self.map[i] == "P":
                    self.map[i] = "S"
        else:
            self.player = Player(0, 0, self)

    def get_el_in_map(self, row: int, col: int) -> str:
        if (col < 0 or col >= self.w) or (row < 0 or row >= self.h):
            raise Exception("Invalid index for map: col:" +
                            str(col) + ", row:" + str(row))

        return self.map[(row * self.w) + col]

    def get_player_pos_in_map(self) -> list:
        row = 0
        col = 0
        for el in self.map:
            if (col >= self.w):
                col = 0
                row += 1
            if el == "P":
                return [row, col]
            col += 1

    # Game runner/starter
    def run(self):
        self.isRunning = True

        entity_one = Entity(0, 4, 6, "monster")
        entity_two = Entity(1, 26, 10)
        self.entities.append(entity_one)
        self.entities.append(entity_two)

        while (self.isRunning):
            os.system("cls||clear")
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

        # Monster killing (WIP)
        for entity in self.entities:
            if self.player.x == entity.x and self.player.y == entity.y:
                match entity.type:
                    case "monster":
                        self.entities.remove(entity)
                        self.player.kills += 1
                    case _:
                        pass

    # Game renderer
    def render(self):
        # Misc
        print("Welcome to " + self.title + "!")
        print("Kills: " + str(self.player.kills))
        # print("Key pressed: ", self.char)
        # Print bottom side
        print()
        print("Press '0' to quit")

        print((self.w+2)*"_")
        for row in range(0, self.h):
            # Print left side
            print("|", end="")
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
                        print(self.get_el_in_map(row, col), end="")
            # Print right side
            print("|\n", end="")
        # Print bottom side
        print((self.w+2)*"-", end="")
        print("\n", end="")

    def get_map(self):
        return self.map


# Main function
def main():
    game = Game("test game")
    game.run()


# If this is the file executed
if __name__ == '__main__':
    main()
