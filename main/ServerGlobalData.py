from main.Game import Game
import json


class ServerGlobalData:
    def __init__(self):
        self.games: dict[str, Game] = {}
        self.users_games: dict[str, str] = {}

    def add_game(self, game_config, user_name):
        if game_config["name"] in self.games.keys():
            raise ValueError("The game with the specified name already exists!")
        with open("main/maps/map1.json", "r") as f:
            game_map_data = json.loads(f.read())
        self.games[game_config["name"]] = Game(game_config, user_name, game_map_data)
        self.users_games[user_name] = game_config["name"]

    def remove_game(self, game_name, user):
        game = self.games[game_name]
        if self.games[self.users_games[user]].monitor != user:
            raise PermissionError("This is not your game!")
        for player in game.players_names:
            if player is not None:
                self.disconnect_player(player)
        self.users_games[game.monitor] = None
        self.games.pop(game_name)

    def disconnect_player(self, player_name):
        if self.games[self.users_games[player_name]].monitor == player_name:
            raise PermissionError("You cannot disconnect from a game where you are a monitor, delete it instead")
        self.games[self.users_games[player_name]].remove_player(player_name)
        self.users_games[player_name] = None

    def get_user_game_name(self, user_name):
        if user_name not in self.users_games.keys():
            return None
        return self.users_games[user_name]

    def add_player_to_game(self, game_name, player_name, passphrase):
        if not self.get_user_game_name(player_name) is None:
            raise PermissionError("You are already in a game, disconnect first")
        self.games[game_name].add_player(player_name, passphrase)
        self.users_games[player_name] = game_name

    def get_user_game(self, user_name):
        if user_name not in self.users_games.keys():
            return None
        if self.get_user_game_name(user_name) is None:
            return None
        return self.games[self.get_user_game_name(user_name)]

    def set_player_move(self, player_name, move):
        game = self.get_user_game(player_name)
        game.player_ready(player_name, move)

    def get_games_names(self):
        return list(self.games.keys())

    def get_main_screen_data(self):
        return [{
            "name": game_key,
            "players_count": self.games[game_key].get_players_count()
        } for game_key in self.games.keys()]
