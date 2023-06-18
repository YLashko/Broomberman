from random import randint, choice
from main.layers.bonuses import random_bonuses, Bonuses
from pprint import pprint


class BonusLayer:
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

    def pickup_bonus(self, player):
        bonus_on_map = self.level_map[player.cx][player.cy]
        if bonus_on_map != 0:
            if bonus_on_map in [Bonuses.GreyDoorKey, Bonuses.GoldenDoorKey]:
                if bonus_on_map not in player.keys:
                    self.level_map[player.cx][player.cy] = 0
                player.add_key(bonus_on_map)
            else:
                player.add_bonus(bonus_on_map)
                self.level_map[player.cx][player.cy] = 0
            return True
        return False

    def place_bonuses_random(self, amount, can_place_map):
        for i in range(amount):
            x = randint(0, self.sx - 1)
            y = randint(0, self.sy - 1)

            if can_place_map[x][y] and self.level_map[x][y] == 0:
                self.level_map[x][y] = choice(random_bonuses)
