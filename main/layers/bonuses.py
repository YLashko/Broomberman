class Bonuses:
    Bomb = 100
    Spear = 101
    Tea = 102
    GreyDoorKey = 1
    GoldenDoorKey = 2
    Fish = 3


random_bonuses = []
random_bonuses_non_weighted = [Bonuses.Bomb, Bonuses.Spear, Bonuses.Tea]
random_bonuses_weights = [10, 20, 5]
for i, bonus in enumerate(random_bonuses_non_weighted):
    random_bonuses += [bonus for _ in range(random_bonuses_weights[i])]
