from main.layers.obstacles import Obstacles


class ObstaclesLayer:
    def __init__(self, size: list, level_map: list[list[int | None]] = None):
        if level_map:
            self.level_map = level_map
        else:
            self.sx = size[0]
            self.sy = size[1]
            self.generate_map()

    def generate_map(self):
        self.level_map = [[
            None for x in range(self.sx)
        ] for y in range(self.sy)]

    def set_level_map(self, level_map):
        self.level_map = level_map

    def remove_rock(self, x, y):
        if self.level_map[x][y] == Obstacles.Stone:
            self.level_map[x][y] = 0

    def try_to_go_here(self, x, y, player):
        if self.level_map[x][y] == 0:
            return True
        if self.level_map[x][y] in player.keys:
            self.level_map[x][y] = 0
            return True
        return False
