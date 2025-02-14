from entity import Entity


# EntityMannager class
class EntityMannager(object):
    def __init__(self, game):
        self.entities = []
    # def new(self, game):
        self.game = game
        self.gameMap = self.game.map

        # Other
        i = 0
        row = 0
        col = 0
        for char in self.gameMap:
            if col >= self.game.w:
                col = 0
                row += 1
            if char.split(":")[0] == "E":
                self.game.map[i] = "-"
                self.entities.append([char.split(":")[1], [col, row]])
            col += 1
            i += 1

    # Function to get the entities in the form of a list containing instances
    # of Entity
    def get_entities(self):
        entitiesT = []
        i = 0
        for entityType in self.entities:
            if entityType[0] not in Entity.get_type_chars():
                entityType[0] = "?"

            entity = Entity(i, entityType[1][0],
                            entityType[1][1],
                            str(list(Entity.get_types())[list(Entity.get_type_chars()).index(entityType[0])]))

            entitiesT.append(entity)
            i += 1
        return entitiesT

    # Supossedly updates each entity in the entity list
    def update(self):
        for entity in self.entities:
            entity.update()


# Entity adder
def add_entity(x: int, y: int, entityType: str, entityManager):
    entities = entityManager.get_entities()
    entities[3] = 345
