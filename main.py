import os


# Input check
def getchar():
   #Returns a single character from standard input

    import tty, termios, sys
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ord(ch) == 3: exit()
    return ch


class Entity(object):
    def __init__(self, Id: int, x: int, y: int, entityType: str = "",isInvincible: bool = False):
        # Entity identifier
        self.id = Id

        # Entity position
        self.x = x
        self.y = y

        # entity type
        self.type = entityType

        # Entity character to print in the "sccreen" (terminal)
        match (self.type):
            case "monster":
                self.char = "&"
            case _:
                self.char = "?"

        # Wether the entity is invincible
        self.isInvincible = isInvincible

    def update():
        ...


class Player(object):
    def __init__(self, x: int, y: int, game: "Game"):
        self.x = x
        self.y = y
        self.game = game

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
    def __init__(self, title: str):
        self.title = title
        self.w = 40
        self.h = 20

        self.player = Player(0, 0, self)

        self.isRunning = False
        self.char = ''

        # self.entities = HashTable(889)
        self.entities = []
    
    # Game runner/starter
    def run(self):
        self.isRunning = True

        entity_one = Entity(0, 4, 6, "monster")
        entity_two = Entity(1, 26, 10)
        self.entities.append(entity_one)
        self.entities.append(entity_two)

        while (self.isRunning):
            os.system("clear")
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
                    case _:
                        pass

    # Game renderer
    def render(self):
        # Misc
        # print(self.title)
        # print("Key pressed: ", self.char)
        # Print bottom side
        print(self.w*"_")
        for row in range(0, self.h):
            # Print left side
            print("|", end="")
            for col in range(0, self.w):
                for entity in self.entities:
                    # If curent cell has the position of an entity then do this
                    if col == entity.x and row == entity.y:
                        if entity.x == self.player.x and entity.y == self.player.y:
                            print(entity.char, end="\b")
                        else:
                            print(entity.char, end="")
                # If current cell has the position of the player then do this
                if col == self.player.x and row == self.player.y:
                    print("x", end="")
                # else
                else:
                    # We already check for player pos. here we check if current cell is a cell of any entity, and if not, then print " "
                    isOnTop = False
                    for entity in self.entities:
                        if col == entity.x and row == entity.y:
                            isOnTop = True
                    if not isOnTop:
                        print(" ", end="")
            # Print right side
            print("|\n", end="")
        # Print bottom side
        print(self.w*"-", end="")
        print("\n", end="")


# Main function
def main():
    game = Game("test game")
    game.run()

# If this is the file executed
if __name__ == '__main__':
    main()
