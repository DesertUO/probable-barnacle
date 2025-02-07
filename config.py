class Config(object):
    def __init__(self, game):
        self.game = game

        # Reading the config file, with path defined in the Game class instance
        # (defaultConfigu)
        with open(self.game.defaultConfig, "r") as file:
            configContent = file.read().split("\n")
            for line in configContent:
                if not line == "":
                    # Checking if the line is not  a comment, prefixed by a "#"
                    if line[0] == "#":
                        continue
                    if "BORDER" == line.split(":")[0]:
                        borderConfig = line.split(":")[1].split(",")
                        self.game.borderConfig = borderConfig
