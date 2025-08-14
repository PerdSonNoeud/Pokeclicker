import random
import pygame
import datas


class Pokemon(object):
    def __init__(self):
        # Pokemon sprites
        self.file = "assets/sprites"
        self.pokemon_sprite = pygame.image.load(f"{self.file}/normal/1.png")

        # Pokemons datas
        self.effort_value = datas.effort_value
        self.learn_set = datas.move_learnset
        self.pkm_base = datas.base_stats
        self.location = datas.location
        self.pokedex = datas.pokedex
        self.move = datas.move
        self.move_set = []

        # Pokemon levels
        self.level = 1
        self.exp = 0

        # Pokemon stats
        self.attack_speed = (200 - self.pkm_base["001"][5]) * 10
        self.stats = [0, 0, 0, 0, 0, 0]
        self.evs = [0, 0, 0, 0, 0, 0]
        self.iv = [0, 0, 0, 0, 0, 0]
        self.hp_max = self.stats[0]
        self.hp = self.hp_max
        self.gender = "male"
        self.shiny = False

    def exp_give(self, pkm_id, wild: int = 1, trade: int = 1, boost: int = 1, s: int = 1):
        """
        Function that calculi the exp to give to the trainer.

        :param pkm_id: ID of the foe pokemon (str type)
        :param wild: 1 if the fainted pokemon is wild, 1.5 if the fainted pokemon is owned by a Trainer (int type)
        :param trade: 1 if the winning pokemon's current owner is its Original Trainer,
                      1.5 if the pokemon was gained in a domestic trade (int type)
        :param boost: 1.5 if the winning pokemon is holding a Lucky Egg, 1 otherwise (int type)
        :param s: The number of pokemon that participated in the battle and have not fainted (int type)

        :return: Exp to give (int type)
        """
        return int((wild * trade * self.effort_value[pkm_id][0] * boost * self.level) / (7 * s))

    def get_img(self, pokemon: str, shiny_charm: bool = False, prints: bool = True):
        """
        Function which get the pokemon sprite and randomize the shiny.

        :param pokemon: ID of the pokemon to get the right image (str type).
        :param shiny_charm: If the player has the shiny charm (bool type).
        :param prints: True if we want to print info (Bool type)

        :return: Return True if the pokemon is shiny or False if the pokemon isn't shiny
        """
        if shiny_charm:
            shiny_rate = random.randint(1, 2048)
        else:
            shiny_rate = random.randint(1, 4096)

        if shiny_rate == 1:
            self.pokemon_sprite = pygame.image.load(f"{self.file}/shiny/{str(int(pokemon))}.png")
            self.pokemon_sprite = pygame.transform.scale(self.pokemon_sprite,
                                                         (int(self.pokemon_sprite.get_width() * 2.6),
                                                          int(self.pokemon_sprite.get_height() * 2.6)))
            self.pokemon_sprite.set_colorkey([0, 0, 0])
            if prints:
                print(f"\n\nA wild {self.pokedex[pokemon][0]} shiny appeared.")
            self.shiny = True
            return True
        else:
            self.pokemon_sprite = pygame.image.load(f"{self.file}/normal/{str(int(pokemon))}.png")
            self.pokemon_sprite = pygame.transform.scale(self.pokemon_sprite,
                                                         (int(self.pokemon_sprite.get_width()*2.6),
                                                          int(self.pokemon_sprite.get_height()*2.6)))
            if prints:
                print(f"\n\nA wild {self.pokedex[pokemon][0]} appeared.")
            self.shiny = False
            return False

    def update_atk_spd_bar(self, surface, x, y, timer):
        """
        Function which update and display the Attack Speed bar

        :param surface: Game window
        :param x: position X of the top left of the Attack Speed bar (int type)
        :param y: position Y of the top left of the Attack Speed bar (int type)
        :param timer: Time until the next attack (int type)
        """
        # Draw Attack Speed bar
        pygame.draw.rect(surface, (0, 0, 0), [x - 2, y - 2, 154, 7])
        pygame.draw.rect(surface, (130, 130, 130), [x, y, 150, 5])
        pygame.draw.rect(surface, (70, 70, 250), [x, y, int(timer / self.attack_speed * 150), 5])

    def random_pokemon(self, locate: str = "all"):
        """
        Function which select a random pokemon in the location (location) with their rarity rate

        :param locate: location in the dictionary location (str)

        :return: l of the data of the pokemon chosen
        """
        randomize = float(str(random.randint(0, 100) / 100)[:5])
        pokemon_appeared = []
        pokemon_rate = 0.0
        searching = True
        number = 0

        if locate == "all":
            pokemon_appeared = random.randint(1, 151)
            level = random.randint(1, 100)
            if len(str(pokemon_appeared)) == 1:
                pokemon_appeared = [f"00{pokemon_appeared}", [level], .0066]
            elif len(str(pokemon_appeared)) == 2:
                pokemon_appeared = [f"0{pokemon_appeared}", [level], .0066]
            elif len(str(pokemon_appeared)) == 3:
                pokemon_appeared = [f"{pokemon_appeared}", [level], .0066]
        else:
            while searching:
                pokemon_rate += self.location[locate][number][-1]
                if randomize <= pokemon_rate:
                    pokemon_appeared = self.location[locate][number]
                    searching = False
                number += 1
        self.level = random.choice([i for i in range(pokemon_appeared[1][0], pokemon_appeared[1][1] + 1)])
        gender = self.pokedex[pokemon_appeared[0]][2]
        if gender * 100 > random.randint(1, 100):
            gender = "male"
        else:
            gender = "female"
        self.gender = gender

        return pokemon_appeared, self.level

    def update_health_bar(self, surface, x, y):
        """
        Function which update and display the Health bar

        :param surface: Game window
        :param x: position X of the top left of the Health bar (int type)
        :param y: position Y of the top left of the Health bar (int type)
        """
        # HP color
        if self.hp > int(self.hp_max / 2):
            hp_color = (111, 210, 46)
        elif self.hp > int(self.hp_max / 5):
            hp_color = (230, 180, 46)
        else:
            hp_color = (210, 46, 46)
        # Draw health bar
        pygame.draw.rect(surface, (0, 0, 0), [x - 2, y - 2, 154, 14])
        pygame.draw.rect(surface, (130, 130, 130), [x, y, 150, 10])
        pygame.draw.rect(surface, hp_color, [x, y, int(self.hp / self.hp_max * 150), 10])

    def damage(self, damage: int = 1):
        if damage <= self.hp:
            self.hp -= damage
        else:
            self.hp = 0

    def random_attack(self, pkm_id):
        pkm_learn_set = self.learn_set[pkm_id]
        learnable = []
        for move in pkm_learn_set:
            if int(move[1]) <= self.level and move[0] not in learnable:
                learnable.append(move[0])

        self.move_set = []
        if len(learnable) > 4:
            for index in range(4):
                self.move_set.append(learnable.pop(learnable.index(random.choice(learnable))))
        else:
            self.move_set = learnable

    def exp_to_lvlup(self, pkm_id):
        """
        Function which calculi the number of exp the pokemon needed to level up.

        :param pkm_id: ID of the pokemon to get the right image (str type).

        :return: Experience the pokemon need to level up.
        """
        # Exp Family : Fast, Medium Fast, Medium Slow, Slow
        if self.level == 100:
            # Level max reached
            exp_required = 0
        elif self.pokedex[pkm_id][-1] == "Fast":
            # max_exp(Level + 1) - max_exp(level) = exp(level)
            exp_required = 4 * (self.level + 1) ** 3 / 5
            exp_required -= (4 * self.level ** 3 / 5)
        elif self.pokedex[pkm_id][-1] == "Medium Fast":
            # max_exp(Level + 1) - max_exp(level) = exp(level)
            exp_required = (self.level + 1) ** 3
            exp_required -= (self.level ** 3)
        elif self.pokedex[pkm_id][-1] == "Medium Slow":
            # max_exp(Level + 1) - max_exp(level) = exp(level)
            exp_required = 6/5 * (self.level + 1) ** 3 - 15 * (self.level + 1) ** 2 + 100 * (self.level + 1) - 140
            exp_required -= (6/5 * self.level ** 3 - 15 * self.level ** 2 + 100 * self.level - 140)
        else:
            # max_exp(Level + 1) - max_exp(level) = exp(level)
            exp_required = (self.level + 1) ** 3 * 5 / 4
            exp_required -= (self.level ** 3 * 5 / 4)

        return int(exp_required)

    def heal(self, heal: int = 1):
        if heal + self.hp <= self.hp_max:
            self.hp += heal
        else:
            self.hp = self.hp_max

    def get_stats(self, pkm_id):
        """
        Function that calculi the Stats of the pokemon (pkm_id) and his attack speed.

        :param pkm_id: ID of the pokemon we are looking for (str type)
        """
        self.stats[0] = \
            int(((self.iv[0] + 2 * self.pkm_base[pkm_id][0] + int(self.evs[0] / 4)) * self.level / 100)) \
            + self.level + 10
        self.hp_max = self.stats[0]
        for i in range(5):
            self.stats[i + 1] = int((self.iv[i + 1] + 2 * self.pkm_base[pkm_id][i + 1]
                                     + int(self.evs[i + 1] / 4)) / 100 * self.level) + self.level + 5

        self.attack_speed = (200 - self.pkm_base[pkm_id][-1]) * 10
        self.exp = self.exp_to_lvlup(pkm_id)

    def get_ivs(self):
        """
        Function that give random IVs to the pokemon
        """
        for i in range(6):
            self.iv[i] = random.randint(0, 31)
