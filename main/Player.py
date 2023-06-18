class Player:
    def __init__(self, name, index, coordinates):
        self.cx = coordinates[0]
        self.cy = coordinates[1]
        self.name = name
        self.index = index
        self.keys = set()
        self.move = None
        self.bonuses = [101, 100, 102]

    def __str__(self):
        return self.name

    def set_move(self, move):
        self.move = move

    def remove_move(self):
        self.move = None

    @property
    def ready(self):
        return self.move is not None

    def move_to(self, x, y):
        self.cx = x
        self.cy = y

    def move_rel(self, x, y):
        self.cx += x
        self.cy += y

    def add_bonus(self, bonus):
        self.bonuses.append(bonus)
        if len(self.bonuses) > 3:
            self.bonuses.pop(0)

    def has_bonus(self, bonus_type):
        return bonus_type in self.bonuses

    def remove_bonus(self, bonus_type):
        self.bonuses.pop(self.bonuses.index(bonus_type))

    def remove_key(self, key):
        self.keys.remove(key)

    def add_key(self, key):
        self.keys.add(key)
