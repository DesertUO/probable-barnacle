entityTypes = {"monster": "ξ", "bullet": "•", "unknown": "?"}


# Entity class
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

    # Updates the entity
    def update(self):
        ...

    def get_type(self) -> str:
        return self.type

    # Static method that returns a list of entities types as strings of types
    # names
    @staticmethod
    def get_types() -> list[str]:
        return list(Entity.types.keys())

    # Static method that returns a list of entities chars that are what to
    # render in the terminal for each entity
    @staticmethod
    def get_type_chars() -> list[str]:
        return list(Entity.types.values())
