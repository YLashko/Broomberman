from main.Player import Player
from main.layers.bonuses import Bonuses
from main.layers.obstacles import Obstacles
from main.level import GameLevel
from random import shuffle


def transpose(map_):
    return [list(a) for a in list(zip(*map_))]


def transpose_pos(pos):
    return [pos[1], pos[0]]


class Game:
    def __init__(self, config, user, game_map):
        self.player_animations = {}
        self.passphrase = None
        self.name = None
        self.monitor = user
        self.max_players = 4
        self.moves = 3
        self.game_map_config = game_map
        self.starting_positions = [a for a in game_map["starting_positions"]]
        self.level = GameLevel(game_map["size"])
        self.finish_positions = [a for a in game_map["finish_positions"]]
        self.bonus_arr = []
        self.winner = None
        self.bonus_animations = []
        self.sound_effects = []
        self.players: list[Player | None] = [None, None, None, None]
        self.config = config
        self.tea_coords = None
        self.running = True
        self.move_counter = 0
        self.bonuses_period_amount = config["bonus_spawn_amount"]
        self.bonuses_period_delay = config["bonus_spawn_delay"]
        self.configure()

    def role(self, user_name):
        if self.monitor == user_name:
            return "Monitor"
        else:
            return "Player"

    def configure(self):
        self.name = self.config["name"]
        self.passphrase = self.config["passphrase"]
        keys = list(self.game_map_config.keys())
        if "ground_map" in keys:
            self.level.ground.set_level_map(transpose(self.game_map_config["ground_map"]))
        if "obstacles_map" in keys:
            self.level.obstacles.set_level_map(transpose(self.game_map_config["obstacles_map"]))
        if "bonuses_map" in keys:
            self.level.bonuses.set_level_map(transpose(self.game_map_config["bonuses_map"]))
        if "fishes_map" in keys:
            self.level.set_fishes_map(transpose(self.game_map_config["fishes_map"]))
        if "starting_random_bonuses" in keys:
            self.level.place_random_bonuses(self.game_map_config["starting_random_bonuses"])

    def start(self):
        self.running = True

    def place_bonuses_period(self):
        if (self.move_counter + 1) % self.bonuses_period_delay == 0 and self.move_counter != 0:
            self.level.place_random_bonuses(self.bonuses_period_amount)

    def check_ready(self):
        if all(
                [player.ready for player in self.players if player is not None]
        ) and self.get_players_count() != 0:
            self.outcome()
            self.move_counter += 1

    def check_wins(self):
        for player in self.non_none_players():
            if [player.cx, player.cy] in self.finish_positions and Bonuses.Fish in player.keys:
                self.win(player)

    def win(self, player):
        self.running = False
        self.winner = player

    def player_ready(self, player_name, move):
        if not self.running:
            return
        player = self.players[self.player_index(player_name)]
        player.set_move(move)
        self.check_ready()

    def get_move_count(self):
        return self.move_counter

    def outcome(self):
        self.bonus_animations = []
        self.sound_effects = []
        self.reset_player_animations()

        for move in range(self.moves):
            for player in self.non_none_players():
                self.check_bonus(player, move)
            self.outcome_bonuses(move)
            rand_players = self.non_none_players()
            shuffle(rand_players)
            for player in rand_players:
                self.make_move(player, move)
            self.check_wins()

        for player in self.non_none_players():
            self.check_bonus(player, self.moves)
        self.outcome_bonuses(self.moves)

        self.execute_tea()
        self.place_bonuses_period()
        self.reset_moves()

    def execute_tea(self):
        if self.tea_coords is not None:
            for player in self.non_none_players():
                player.move_to(self.tea_coords[0], self.tea_coords[1])
                self.player_animations[player.name].append({
                    "from_pos": [player.cx, player.cy],
                    "to_pos": self.tea_coords,
                    "anim_delay": 4
                })
            self.tea_coords = None

    def reset_moves(self):
        for player in self.non_none_players():
            player.move = None

    def non_none_players(self) -> list[Player]:
        return [player for player in self.players if player is not None]

    def reset_player_animations(self):
        self.player_animations = {}
        for player in self.non_none_players():
            self.player_animations[player.name] = []

    def outcome_bonuses(self, index):
        for bonus in self.bonus_arr:
            self.process_bonus(bonus, index)
        self.bonus_arr = []

    def validate_offset(self, offset, bonus_type):
        if bonus_type == Bonuses.Bomb or bonus_type == Bonuses.Spear:
            if abs(offset[0]) > 4 or abs(offset[1]) > 4:
                raise PermissionError("Too big offset")

    def stoneAnimation(self, x, y, delay):
        if self.level.obstacles.level_map[x][y] == Obstacles.Stone:
            self.bonus_animations.append({
                "type": "stone",
                "to_pos": [x, y],
                "anim_delay": delay + 0.5
            })

    def process_bonus(self, bonus_data, anim_delay):
        bonus_type = bonus_data["type"]
        self.validate_offset(bonus_data["to_offset"], bonus_type)

        if bonus_type == Bonuses.Bomb:
            landing_x = bonus_data["from_pos"][0] + bonus_data["to_offset"][0]
            landing_y = bonus_data["from_pos"][1] + bonus_data["to_offset"][1]
            for x in range(-1, 2, 1):
                for y in range(-1, 2, 1):
                    lx, ly = landing_x + x, landing_y + y
                    print(lx, ly)
                    if not self.level.out_of_bounds(lx, ly):
                        self.stoneAnimation(lx, ly, anim_delay)
                        self.level.obstacles.remove_rock(lx, ly)
                        self.move_to_start(lx, ly, anim_delay)
                        self.bonus_animations.append({
                            "type": "explosion",
                            "to_pos": [lx, ly],
                            "anim_delay": anim_delay + 0.5
                        })

            self.bonus_animations.append({
                "type": "bomb",
                "from_pos": bonus_data["from_pos"],
                "to_pos": [landing_x, landing_y],
                "anim_delay": anim_delay
            })

            self.sound_effects.append({
                "type": "boom",
                "delay": anim_delay + 0.5,
            })

        elif bonus_type == Bonuses.Spear:

            fx, fy = bonus_data["from_pos"]
            lx, ly = bonus_data["to_offset"]
            if abs(lx) > abs(ly):
                additional_offset = 1 if lx > 0 else 0
                for x in range(min(fx, fx + lx) + additional_offset, max(fx, fx + lx) + additional_offset):
                    self.stoneAnimation(lx, ly, anim_delay)
                    self.level.obstacles.remove_rock(x, fy)
                    self.move_to_start(x, fy, anim_delay)
                    self.bonus_animations.append({
                        "type": "explosion",
                        "to_pos": [x, fy],
                        "anim_delay": anim_delay + 0.5
                    })
            else:
                additional_offset = 1 if ly > 0 else 0
                for y in range(min(fy, fy + ly) + additional_offset, max(fy, fy + ly) + additional_offset):
                    self.level.obstacles.remove_rock(fx, y)
                    self.move_to_start(fx, y, anim_delay)
                    self.bonus_animations.append({
                        "type": "explosion",
                        "to_pos": [fx, y],
                        "anim_delay": anim_delay + 0.5
                    })

            self.sound_effects.append({
                "type": "boom",
                "delay": anim_delay + 0.5,
            })

    def move_to_start(self, x, y, index):
        for i, player in enumerate(self.players):
            if player is None:
                continue
            if player.cx == x and player.cy == y:
                self.remove_gold_key(player)
                self.remove_fish(player)
                self.player_animations[player.name].append({
                    "from_pos": [player.cx, player.cy],
                    "to_pos": self.starting_positions[i],
                    "anim_delay": index
                })
                player.move_to(self.starting_positions[i][0], self.starting_positions[i][1])

    def remove_fish(self, player):
        if Bonuses.Fish in player.keys:
            player.remove_key(Bonuses.Fish)
            self.level.fishes.level_map[player.cx][player.cy] += 1

    def remove_gold_key(self, player):
        if Bonuses.GoldenDoorKey in player.keys:
            player.remove_key(Bonuses.GoldenDoorKey)
            self.level.bonuses.level_map[player.cx][player.cy] = Bonuses.GoldenDoorKey

    def make_move(self, player, index):
        if player.move is None:
            raise PermissionError("This player has no move")
        self.move_path_rel(player, index)

    def move_path_rel(self, player, index):
        moves = player.move["path"]

        def valid_distance(cx, cy):
            return abs(cx) + abs(cy) < 2

        def valid_move(x, y, cx, cy, player):
            if self.level.out_of_bounds(x + cx, y + cy):
                raise PermissionError("Out of bounds")
            if not self.level.obstacles.try_to_go_here(x + cx, y + cy, player):
                raise PermissionError("Blocked by obstacle")
            if not self.level.ground.player_can_stand_here(x + cx, y + cy):
                raise PermissionError("There is no ground")

        x = player.cx
        y = player.cy
        move = moves[index]
        mx = move[0]
        my = move[1]
        if not valid_distance(mx, my):
            raise PermissionError("Not a valid move distance")
        try:
            valid_move(x, y, mx, my, player)
        except:
            return

        x += mx
        y += my
        self.player_animations[player.name].append({
            "from_pos": [player.cx, player.cy],
            "to_pos": [x, y],
            "anim_delay": index
        })
        player.move_to(x, y)
        if self.level.bonuses.pickup_bonus(player):
            self.sound_effects.append({
                "type": "key",
                "delay": index + 1,
            })
        self.level.fishes.pickup_fish(player)

    def check_bonus(self, player, index):
        bonus_data = player.move["bonus"]
        if not bonus_data["active"]:
            return

        if bonus_data["on_move"] == index:
            bonus_data["from_pos"] = [player.cx, player.cy]
            if not player.has_bonus(bonus_data["type"]):
                raise PermissionError("You haven't got any bonuses of that type")
            self.use_bonus(player, bonus_data)

    def use_bonus(self, player, bonus_data):
        bonus_type = bonus_data["type"]
        bonus_data["from_pos"] = [player.cx, player.cy]
        x, y = bonus_data["from_pos"]

        if bonus_type == Bonuses.Bomb:
            self.bonus_arr.append(bonus_data)
        elif bonus_type == Bonuses.Spear:
            self.bonus_arr.append(bonus_data)
        elif bonus_type == Bonuses.Tea:
            self.tea_coords = [x, y]

        player.remove_bonus(bonus_type)

    def place_players_on_starting_positions(self):
        for i, player in enumerate(self.players):
            if player is None:
                continue
            player.move_to(self.starting_positions[i][0], self.starting_positions[i][1])

    def set_monitor_user(self, username):
        self.monitor = username

    def get_data_for_monitor(self, username):
        if self.monitor != username:
            raise PermissionError("You are not a monitor for this game!")
        return self.name

    def get_players_count(self):
        return self.max_players - self.players.count(None)

    def add_player(self, player_name, passphrase):

        if passphrase != self.passphrase:
            raise PermissionError("Wrong passphrase!")

        if self.players.count(None) == 0:
            raise PermissionError("This game is already full!")

        index = self.players.index(None)
        self.players[index] = Player(player_name, index, self.starting_positions[index])

    def player_index(self, player_name):
        return self.players_names.index(player_name)

    def fill_empty_player_animations(self):
        for player in self.non_none_players():
            if player.name not in self.player_animations:
                self.player_animations[player.name] = []
            if len(self.player_animations[player.name]) == 0:
                self.player_animations[player.name].append({
                    "from_pos": [player.cx, player.cy],
                    "to_pos": [player.cx, player.cy],
                    "anim_delay": 0
                })

    def monitor_data(self):
        self.fill_empty_player_animations()
        return {
            "type": "Monitor",
            "name": self.name,
            "players": self.gather_player_data(),
            "ground_map": self.level.ground.level_map,
            "obstacles_map": self.level.obstacles.level_map,
            "bonus_map": self.level.bonuses.level_map,
            "fishes_map": self.level.fishes.level_map,
            "bonus_animations": self.bonus_animations,
            "player_animations": self.player_animations,
            "finish_positions": self.finish_positions,
            "winner": self.gather_player_data()[self.winner.index] if self.winner is not None else None,
            "sound_effects": self.sound_effects
        }

    def cut_map(self, level_map, from_x, from_y, to_x, to_y):
        return [level_map[x][from_y: to_y] for x in range(from_x, to_x)]

    def player_data(self, player_name):
        player = self.players[self.player_index(player_name)]
        size = 9
        x, y = player.cx, player.cy
        from_x = max(0, min(self.level.sx - size, x - int(size / 2)))
        from_y = max(0, min(self.level.sy - size, y - int(size / 2)))
        to_x, to_y = from_x + size, from_y + size
        players = self.gather_player_data()
        for p in players:
            if p is None:
                continue
            p["x"] -= from_x
            p["y"] -= from_y
        return {
            "type": "Player",
            "name": self.name,
            "bonuses": player.bonuses,
            "player_keys": list(player.keys),
            "players": players,
            "x_rel": player.cx - from_x,
            "y_rel": player.cy - from_y,
            "ground_map": self.cut_map(self.level.ground.level_map, from_x, from_y, to_x, to_y),
            "obstacles_map": self.cut_map(self.level.obstacles.level_map, from_x, from_y, to_x, to_y),
            "bonus_map": self.cut_map(self.level.bonuses.level_map, from_x, from_y, to_x, to_y),
            "fishes_map": self.cut_map(self.level.fishes.level_map, from_x, from_y, to_x, to_y),
            "finish_positions": [
                [p[0] - from_x, p[1] - from_y]
                for p in self.finish_positions
                if 0 <= p[0] - from_x < size
                   and 0 <= p[1] - from_y < size
            ]
        }

    def get_players_ready_status(self):
        return {player.name: player.ready for player in self.non_none_players()}

    def gather_player_data(self):
        return [{
                    "name": p.name,
                    "index": p.index,
                    "has_fish": Bonuses.Fish in p.keys,
                    "x": p.cx,
                    "y": p.cy
                } if p is not None else None for p in self.players]

    @property
    def players_names(self):
        return [player.name if player is not None else None for player in self.players]

    def remove_player(self, player_name):
        self.players[self.players_names.index(player_name)] = None
