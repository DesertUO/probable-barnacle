entityTypes = {"monster": "&", "unknown": "?"}


class Entity(object):
    types = entityTypes

    def __init__(self, Id: int, x: int, y: int,
                 entityType: str = "unknown", isInvincible: bool = False):
        # Entity identifier
        self.id = Id

        # Entity position
        self.x = x
        self.y = y

        # entity type
        self.type = entityType

        # Entity character to print in the "sccreen" (terminal)
        if entityType not in Entity.get_types():
            self.char = "?"
        else:
            self.char = self.types[self.type]

        # Wether the entity is invincible
        self.isInvincible = isInvincible

    def update(self):
        ...

    @staticmethod
    def get_types() -> list:
        return list(Entity.types.keys())
