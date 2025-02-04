class EntityMannager(object):
    def __init__(self, game):
        self.entities = []
    # def new(self, game):
        gameMap = game.get_map()
        for char in gameMap:
            if char.split[0] == "E":
                self.entities.append(char.split(":")[1])

    def get_entities(self):
        return self.entities

    def update(self):
        for entity in self.entities:
            entity.update()
