from main.layers.bonuses import Bonuses


class FishLayer:
    def __init__(self, size: list, level_map: list[list[int | None]] = None):
        if level_map:
            self.level_map = level_map
        else:
            self.sx = size[0]
            self.sy = size[1]
            self.generate_map()

    def generate_map(self):
        self.level_map = [[
            0 for x in range(self.sx)
        ] for y in range(self.sy)]

    def set_level_map(self, level_map):
        self.level_map = level_map

    def pickup_fish(self, player):
        fishes_on_map = self.level_map[player.cx][player.cy]
        if fishes_on_map != 0 and not (Bonuses.Fish in player.keys):
            player.add_key(Bonuses.Fish)
            self.level_map[player.cx][player.cy] -= 1
