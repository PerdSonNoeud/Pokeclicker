import pygame
import random
import datas


def get_icon(widgets, x: int, y: int, a: int, b: int):
    image = pygame.Surface([a, b])
    image.blit(widgets, (0, 0), [x, y, a, b])
    return image


def effectiveness(move, target):
    type_name = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground",
                 "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel"]

    effect_table = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, .5, 0, 1, 1, .5],
                    [1, .5, .5, 2, 1, 2, 1, 1, 1, 1, 1, 2, .5, 1, .5, 1, 2],
                    [1, 2, .5, .5, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, .5, 1, 1],
                    [1, .5, 2, .5, 1, 1, 1, .5, 2, .5, 1, .5, 2, 1, .5, 1, .5],
                    [1, 1, 2, .5, .5, 1, 1, 1, 0, 2, 1, 1, 1, 1, .5, 1, 1],
                    [1, .5, .5, 2, 1, .5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, .5],
                    [2, 1, 1, 1, 1, 2, 1, .5, 1, .5, .5, .5, 2, 0, 1, 2, 2],
                    [1, 1, 1, 2, 1, 1, 1, .5, .5, 1, 1, 1, .5, .5, 1, 1, 0],
                    [1, 2, 1, .5, 2, 1, 1, 2, 1, 0, 1, .5, 2, 1, 1, 1, 2],
                    [1, 1, 1, 2, .5, 1, 2, 1, 1, 1, 1, 2, .5, 1, 1, 1, .5],
                    [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, .5, 1, 1, 1, 1, 0, .5],
                    [1, .5, 1, 2, 1, 1, .5, .5, 1, .5, 2, 1, 1, .5, 1, 2, .5],
                    [1, 2, 1, 1, 1, 2, .5, 1, .5, 2, 1, 2, 1, 1, 1, 1, .5],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, .5, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, .5],
                    [1, 1, 1, 1, 1, 1, .5, 1, 1, 1, 2, 1, 1, 2, 1, .5, 1],
                    [1, .5, .5, 1, .5, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, .5]]

    effective = 1
    row = -1
    column = -1
    column_2 = -1

    for element in range(len(type_name)):

        if move[0] == type_name[element] and row == -1:
            row = element
        if type_name[element] in datas.pokedex[target[0]][1] and column == -1:
            column = element
        elif type_name[element] in datas.pokedex[target[0]][1]:
            column_2 = element

    if row != -1 and column != -1:
        effective *= effect_table[row][column]
        if column_2 != -1:
            effective *= effect_table[row][column_2]

    return effective


class Move:

    status_name = ["poison", "paralyze", "sleep", "freeze", "burn", "pkrs", "faint"]
    category_name = ["Physical", "Special", "Status"]

    can_make_sleep = [[], []]
    can_paralyze = [[], []]
    can_flinch = [[], []]
    can_freeze = [[], []]
    can_poison = [[], []]
    can_burn = [[], []]

    def __init__(self, move_name):
        self.move_name = move_name

        self.status = {}

        row, column = 0, 0
        for status in Move.status_name:
            self.status[status] = get_icon(pygame.image.load("assets/icons/pokemon_type.png"),
                                           32 * row, 12 * (column + 5), 32, 12)
            self.status[status].set_colorkey([0, 0, 0])
            if row < 3:
                row += 1
            else:
                row = 0
                column += 1

        self.category = {}

        row = 0
        for category in Move.category_name:
            self.category[category] = get_icon(pygame.image.load("assets/icons/move_category.png"),
                                               0, 14 * row, 32, 14)
            self.category[category].set_colorkey([0, 0, 0])
            row += 1

        if self.move_name in Move.can_make_sleep[0]:
            rate = random.randint(1, 100)
            if Move.can_make_sleep[1][Move.can_make_sleep[0].index(self.move_name)] < rate:
                pass
        if self.move_name in Move.can_paralyze[0]:
            rate = random.randint(1, 100)
            if Move.can_paralyze[1][Move.can_paralyze[0].index(self.move_name)] < rate:
                pass
        if self.move_name in Move.can_flinch[0]:
            rate = random.randint(1, 100)
            if Move.can_flinch[1][Move.can_flinch[0].index(self.move_name)] < rate:
                pass
        if self.move_name in Move.can_freeze[0]:
            rate = random.randint(1, 100)
            if Move.can_freeze[1][Move.can_freeze[0].index(self.move_name)] < rate:
                pass
        if self.move_name in Move.can_poison[0]:
            rate = random.randint(1, 100)
            if Move.can_poison[1][Move.can_poison[0].index(self.move_name)] < rate:
                pass
        if self.move_name in Move.can_burn[0]:
            rate = random.randint(1, 100)
            if Move.can_burn[1][Move.can_burn[0].index(self.move_name)] < rate:
                pass


class PhysicalMove(Move):
    def __init__(self, move_name):
        Move.__init__(self, move_name)
        self.move = datas.move[move_name]

    def damage(self, user, target):
        level = (2 * user[1]) / 5 + 2
        power = int(self.move[3])
        accurate = int(self.move[-1])
        attack = datas.base_stats[user[0]][1]
        defense = datas.base_stats[target[0]][2]
        if self.move[0] in datas.pokedex[user[0]][1]:
            stab = 1.5
        else:
            stab = 1

        effective = effectiveness(self.move, target)

        if accurate >= random.randint(0, 100):
            damage = ((level * power * (attack / defense)) / 50 + 2) * stab
        else:
            damage = 0

        return int(damage), effective


class SpecialMove(Move):
    def __init__(self, move_name):
        Move.__init__(self, move_name)
        self.move = datas.move[move_name]

    def damage(self, user, target):
        level = (2 * user[1]) / 5 + 2
        power = int(self.move[3])
        accurate = int(self.move[-1])
        attack = datas.base_stats[user[0]][3]
        defense = datas.base_stats[target[0]][4]
        if self.move[0] in datas.pokedex[user[0]][1]:
            stab = 1.5
        else:
            stab = 1

        effective = effectiveness(self.move, target)

        if accurate >= random.randint(0, 100):
            damage = ((level * power * (attack / defense)) / 50 + 2) * stab
        else:
            damage = 0

        return int(damage), effective


class StatusMove(Move):
    def __init__(self, pokemon, move_name):
        Move.__init__(self, move_name)
        self.move = datas.move[move_name]
        self.pokemon_user = pokemon
