from main.Player import Player


class Game:
    def __init__(self, config, user):
        self.passphrase = None
        self.name = None
        self.monitor = user
        self.max_players = 4
        self.players: list[Player | None] = [None, None, None, None]
        self.config = config
        self.configure()

    def role(self, user_name):
        if self.monitor == user_name:
            return "Monitor"
        else:
            return "Player"

    def configure(self):
        self.name = self.config["name"]
        self.passphrase = self.config["passphrase"]

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

        self.players[self.players.index(None)] = Player(player_name)

    def monitor_data(self):
        return {
            "type": "Monitor",
            "name": self.name
        }

    def player_data(self):
        return {
            "type": "Player",
            "name": self.name
        }

    @property
    def players_names(self):
        return [player.name if player is not None else None for player in self.players]

    def remove_player(self, player_name):
        self.players[self.players_names.index(player_name)] = None
