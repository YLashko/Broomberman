class GroundLayer:
    def __init__(self, size: list, level_map: list[list[int]] = None):
        if level_map:
            self.level_map = level_map
        else:
            self.sx = size[0]
            self.sy = size[1]
            self.generate_map()

    def generate_map(self):
        self.level_map = [[
            1 for x in range(self.sx)
        ] for y in range(self.sy)]

    def set_level_map(self, level_map):
        self.level_map = level_map

    def player_can_stand_here(self, x, y):
        return self.level_map[x][y] == 1
