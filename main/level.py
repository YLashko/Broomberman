from main.layers.bonus_layer import BonusLayer
from main.layers.bonuses import Bonuses
from main.layers.ground_layer import GroundLayer
from main.layers.obstacles_layer import ObstaclesLayer
from main.layers.weird_fishes import FishLayer


class GameLevel:
    def __init__(self, size: list[int]):
        self.sx = size[0]
        self.sy = size[1]
        self.ground = GroundLayer(size)
        self.obstacles = ObstaclesLayer(size)
        self.bonuses = BonusLayer(size)
        self.fishes = FishLayer(size)
        print(size)

    def set_ground_map(self, level_map):
        self.ground.set_level_map(level_map)

    def set_obstacles_map(self, obstacles_map):
        self.obstacles.set_level_map(obstacles_map)

    def set_bonuses_map(self, bonuses_map):
        self.bonuses.set_level_map(bonuses_map)

    def set_fishes_map(self, fishes_map):
        self.fishes.set_level_map(fishes_map)

    def place_random_bonuses(self, amount):
        can_place_map = [
            [(self.ground.level_map[x][y] == 1
              and self.obstacles.level_map[x][y] == 0
              and self.fishes.level_map[x][y] == 0) for y in range(self.sy)]
            for x in range(self.sx)]
        self.bonuses.place_bonuses_random(amount, can_place_map)

    def out_of_bounds(self, x, y):
        if x < 0 or x >= self.sx:
            return True
        if y < 0 or y > self.sy:
            return True
        return False
