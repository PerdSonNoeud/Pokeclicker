import pygame
import datas
import csv


class Trainer:
    def __init__(self):
        self.effort_value = datas.effort_value
        self.learn_set = datas.move_learnset
        self.pkm_base = datas.base_stats
        self.pokedex = datas.pokedex
        self.move = datas.move

        # List of the six pokemon the player can have
        self.ev_max = [0, 0, 0, 0, 0, 0]
        self.trainer = []
        self.selected = -1

        # List of the pokemon in the PC
        self.pc = []
        self.len_pc = 0

        # Others datas
        self.file_data = []

        # Attack Speed
        self.attack_speed = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

        # Quests
        self.quests = {
            "Route 01": [[["016", 1], ["019", 1]], False], "Route 03": [[["021", 3]], False],
            "Route 05": [[["043", 2], ["052", 1]], False], "Route 07": [[["052", 2], ["058", 1]], False],
            "Route 09": [[["016", 3], ["021", 2]], False], "Route 11": [[["096", 1]], False],
            "Route 13": [[["043", 2], ["048", 1]], False], "Route 15": [[["132", 1]], False],
            "Route 17": [[["084", 2], ["021", 1]], False], "Route 19": 0,
            "Route 21": 0, "Route 23": [[["132", 1]], False],
            "Route 25": [[["043", 2]], False],
        }

    def get_player_pokemon(self, file_path: str = "trainer"):
        """
        Function which get the pokemon data in a l like :
        ["pkm_id", level, [exp_need, exp_to_lvlup], [stats], [ivs], [evs], [attacks], "Shiny or normal"]
        """
        file = csv.reader(open(f"assets/data/{file_path}.csv", "r"), delimiter=';')

        for pokemon in file:
            self.trainer.append(pokemon)

        for pokemon in range(len(self.trainer)):
            for element in range(len(self.trainer[pokemon]) - 4):
                self.trainer[pokemon][element + 2] = self.trainer[pokemon][element + 2].split()

        self.get_stats()

        for pokemon in self.trainer:
            pokemon[3][0] = pokemon[3][1]

        for page in range(1, 15):
            self.get_player_pc(page)
            if len(self.pc) > 0:
                self.len_pc += len(self.pc)

    def get_others_data(self, file_path: str = "other"):
        file = csv.reader(open(f"assets/data/{file_path}.csv", "r"), delimiter=';')
        self.file_data = []

        for data in file:
            self.file_data.append(data)

        return self.file_data[0][0]

    def save_trainer(self, file_path: str = "trainer"):
        """
        Function which save the trainer's pokemon data.
        """
        file = csv.writer(open(f"assets/data/{file_path}.csv", "w", newline=""), delimiter=";")
        for pokemon in self.trainer:
            trainer = [f"{pokemon[0]}", f"{pokemon[1]}"]
            for index in range(len(pokemon) - 4):
                element = f"{pokemon[index + 2][0]}"
                for elements in pokemon[index + 2][1:]:
                    element += f" {elements}"
                trainer.append(element)
            trainer.append(pokemon[7])
            trainer.append(pokemon[8])
            file.writerow(trainer)

    def get_ev_max(self, pokemon_appeared, pokemon):
        if self.ev_max[pokemon] < 510:
            for ev in range(len(self.trainer[pokemon][5])):
                if self.trainer[pokemon][5][ev] < 252:
                    self.trainer[pokemon][5][ev] += self.effort_value[pokemon_appeared][ev + 1]
                    if self.trainer[pokemon][5][ev] > 252:
                        self.trainer[pokemon][5][ev] = 252

                self.ev_max[pokemon] = 0
                for evs in self.trainer[pokemon][5]:
                    self.ev_max[pokemon] += evs

        if self.ev_max[pokemon] > 510:
            ev_to_subtract = self.ev_max[pokemon] - 510
            bigger_ev = 0
            for ev in range(len(self.trainer[pokemon][5])):
                if self.trainer[pokemon][5][bigger_ev] < self.trainer[pokemon][5][ev]:
                    bigger_ev = ev
            self.trainer[pokemon][5][bigger_ev] -= ev_to_subtract

    def pokemon_info(self, surface, size_y, team_n):
        """
        Function which print all the data about the trainer pokemon.
        """
        pygame.draw.circle(surface, [250, 50, 50], [75, size_y - 55], 100)
        pygame.draw.circle(surface, [250, 50, 50], [75 + 400, size_y - 20], 100)
        pygame.draw.circle(surface, [100, 80, 80], [75 + 400, size_y - 20], 95)
        pygame.draw.circle(surface, [250, 50, 50], [75 + 400, size_y - 20], 75)
        pygame.draw.rect(surface, [250, 50, 50], [75, size_y - 120, 400, 120])
        pygame.draw.rect(surface, [100, 80, 80], [75, size_y - 115, 400, 20])
        # Exp
        pygame.draw.rect(surface, [50, 50, 50], [161, size_y - 91, 205, 13])
        if len(self.trainer) > 0:
            exp = int(self.trainer[team_n][2][0]) / int(self.trainer[team_n][2][1])
            pygame.draw.rect(surface, [80, 80, 200], [163, size_y - 89, int(exp * 200), 8])
        # HP
        # pygame.draw.rect(surface, [50, 50, 50], [116, size_y - 141, 205, 12])
        # hp = int(self.trainer[team_n][3][0]) / int(self.trainer[team_n][3][1])
        # pygame.draw.rect(surface, [80, 200, 80], [118, size_y - 139, int(hp * 200), 8])
        pygame.draw.circle(surface, [100, 80, 80], [75, size_y - 55], 95)
        pygame.draw.circle(surface, [250, 200, 200], [75, size_y - 55], 75)

        if len(self.trainer) > 0:
            exp = f"{self.trainer[team_n][2][0]} / {self.trainer[team_n][2][1]}"

            pos_x, pos_y = 1, 0
            for n in range(4):
                pygame.draw.rect(surface, [250, 200, 200], [190 + 150 * (pos_x % 2),
                                                            size_y - 72 + 35 * (pos_y % 2), 140, 30])
                if pos_x == 2:
                    pos_y += 1
                    pos_x = 0
                else:
                    pos_x += 1

            pokemon = self.trainer[team_n]
            pokemon_name = self.pokedex[pokemon[0]][0]
            level = pokemon[1]
            move_set = pokemon[6]

            pokemon_sprite = pygame.image.load(f"assets/sprites/{pokemon[-1]}/{int(pokemon[0])}.png")
            pokemon_sprite = pygame.transform.scale(pokemon_sprite, [96, 96])
        else:
            exp = "0 / 0"

            pos_x, pos_y = 1, 0
            for n in range(4):
                pygame.draw.rect(surface, [250, 200, 200], [190 + 150 * (pos_x % 2),
                                                            size_y - 72 + 35 * (pos_y % 2), 140, 30])
                if pos_x == 2:
                    pos_y += 1
                    pos_x = 0
                else:
                    pos_x += 1

            pokemon_name = "???"
            level = "0"
            move_set = [""]
            pokemon_sprite = pygame.image.load("assets/sprites/icons/0.png")
            pokemon_sprite = pygame.transform.scale(pokemon_sprite, [96, 96])

        return pokemon_name, pokemon_sprite, level, move_set, exp

    # noinspection PyTypeChecker
    def get_player_pc(self, page=1, file_path: str = "pc"):
        """
        Function which get the pokemon data in a l like :
        ["pkm_id", level, [exp_need, exp_to_lvlup], [stats], [ivs], [evs], [attacks], "Shiny or normal"]
        """
        file = csv.reader(open(f"assets/data/{file_path}/{page}.csv", "r"), delimiter=';')
        self.pc = []

        for pokemon in file:
            self.pc.append(pokemon)
        if len(self.pc) > 0:
            for pokemon in range(len(self.pc)):
                for element in range(len(self.pc[pokemon]) - 4):
                    self.pc[pokemon][element + 2] = self.pc[pokemon][element + 2].split()

            self.get_stats()
            for pokemon in self.pc:
                pokemon[3][0] = pokemon[3][1]

    def exp_to_lvlup(self, pkm_id, level: int):
        """
        Function which calculi the number of exp the pokemon needed to level up.

        :param pkm_id: ID of the pokemon to get the right image (str type).
        :param level: Level of the pokemon you want (int type).

        :return: Experience the pokemon need to level up.
        """
        # Exp Family : Fast, Medium Fast, Medium Slow, Slow
        if level == 100:
            # Level max reached
            exp_required = 0
        elif self.pokedex[pkm_id][-1] == "Fast":
            # max_exp(Level + 1) - max_exp(level) = exp(level)
            exp_required = 4 * (level + 1) ** 3 / 5
            exp_required -= (4 * level ** 3 / 5)
        elif self.pokedex[pkm_id][-1] == "Medium Fast":
            # max_exp(Level + 1) - max_exp(level) = exp(level)
            exp_required = (level + 1) ** 3
            exp_required -= (level ** 3)
        elif self.pokedex[pkm_id][-1] == "Medium Slow":
            # max_exp(Level + 1) - max_exp(level) = exp(level)
            exp_required = 6 / 5 * (level + 1) ** 3 - 15 * (level + 1) ** 2 + 100 * (level + 1) - 140
            exp_required -= (6 / 5 * level ** 3 - 15 * level ** 2 + 100 * level - 140)
        else:
            # max_exp(Level + 1) - max_exp(level) = exp(level)
            exp_required = (level + 1) ** 3 * 5 / 4
            exp_required -= (level ** 3 * 5 / 4)

        return int(exp_required)

    def damage(self, team_n, damage: int = 1):
        if damage <= self.trainer[team_n][3][0]:
            self.trainer[team_n][3][0] -= damage
        else:
            self.trainer[team_n][3][0] = 0

    def save_pc(self, page=1, file_path: str = "pc"):
        """
        Function which save the trainer's pokemon data.
        """
        file = csv.writer(open(f"assets/data/{file_path}/{page}.csv", "w", newline=""), delimiter=";")
        if len(self.pc) > 0:
            for pokemon in self.pc:
                pc = [f"{pokemon[0]}", f"{pokemon[1]}"]
                for index in range(len(pokemon) - 4):
                    element = f"{pokemon[index + 2][0]}"
                    for elements in pokemon[index + 2][1:]:
                        element += f" {elements}"
                    pc.append(element)
                pc.append(pokemon[7])
                pc.append(pokemon[8])
                file.writerow(pc)
        else:
            file.writerow("")

    def heal(self, team_n, heal: int = 1):
        if heal + self.trainer[team_n][3][0] <= self.trainer[team_n][3][1]:
            self.trainer[team_n][3][0] += heal
        else:
            self.trainer[team_n][3][0] = self.trainer[team_n][3][1]

    def learn_attack(self, team_n):
        pkm_learn_set = self.learn_set[self.trainer[team_n][0]]
        learn = ""
        for move in pkm_learn_set:
            if int(move[1]) == self.trainer[team_n][1]:
                learn = move[0]

        if learn != "":
            if len(self.trainer[team_n][6]) >= 4:
                return f"{self.pokedex[self.trainer[team_n][0]][0]}", " already know 4 moves."
            else:
                if learn not in self.trainer[team_n][6]:
                    self.trainer[team_n][6].append(learn)
                    return f"{self.pokedex[self.trainer[team_n][0]][0]}", f" learned {learn}."
                else:
                    return f"{self.pokedex[self.trainer[team_n][0]][0]}", " already know the new move."
        else:
            return "No new attack."

    def display_team(self, timer):
        icon_size = 61

        pokemon_team = pygame.Surface((2 + (2 + icon_size) * 6, icon_size))

        pygame.draw.rect(pokemon_team, (0, 0, 0),
                         [0, 0, 2 + (2 + icon_size) * 6, icon_size])

        pygame.draw.rect(pokemon_team, (250, 50, 50),
                         [2, 2, (2 + icon_size) * 6 - 2, int(30 * 1.5)])
        pygame.draw.rect(pokemon_team, (250, 250, 250),
                         [2, int((30 * 1.5 + 5) / 2),
                          (2 + icon_size) * 6 - 2, int((30 * 1.5) / 2)])
        pygame.draw.rect(pokemon_team, (100, 100, 100),
                         [2, int((30 * 1.5 + 5) / 2) - 2,
                          (2 + icon_size) * 6 - 2, 4])

        pygame.draw.rect(pokemon_team, (100, 100, 100),
                         [2, 4 + int(30 * 1.5),
                          (2 + icon_size) * 6 - 2, icon_size - int(30 * 1.5) - 6])

        pygame.draw.rect(pokemon_team, (0, 0, 0),
                         [2, 1 + icon_size - int((30 * 1.5 - 6) / 4),
                          (2 + icon_size) * 6 - 2, 2])

        for row in range(1, 6):
            pygame.draw.rect(pokemon_team, (0, 0, 0),
                             [int(42 * 1.5 * row), 0,
                              2, icon_size])

        team_n = 0

        for pokemon in self.trainer:
            pokemon_icon = pygame.image.load(f"assets/sprites/icons/{int(pokemon[0])}.png")
            pokemon_icon = pygame.transform.scale(pokemon_icon, (int(40 * 1.5),
                                                                 int(30 * 1.5)))
            pokemon_team.blit(pokemon_icon, (2 + (2 + icon_size) * team_n, 2))

            # HP color
            if int(pokemon[3][0]) > int(pokemon[3][1] / 2):
                hp_color = (111, 210, 46)
            elif int(pokemon[3][0]) > int(pokemon[3][1] * 3 / 5):
                hp_color = (230, 180, 46)
            else:
                hp_color = (210, 46, 46)
            # Draw health bar
            pygame.draw.rect(pokemon_team, hp_color, [2 + (2 + icon_size) * team_n, 4 + int(30 * 1.5),
                                                      int(int(pokemon[3][0]) / int(pokemon[3][1]) * int(40 * 1.5 + 1)),
                                                      4])
            # Draw attack_speed bar
            if self.trainer[team_n][3][0] > 0:
                self.attack_speed[team_n][0] += timer
            pygame.draw.rect(pokemon_team, (70, 70, 250),
                             [2 + (2 + icon_size) * team_n, 10 + int(30 * 1.5),
                              int(int(self.attack_speed[team_n][0] / self.attack_speed[team_n][1] * (40 * 1.5 + 1))),
                              4])

            team_n += 1

        return pokemon_team

    def update_attack_speed(self):
        for pokemon in range(len(self.trainer)):
            self.attack_speed[pokemon][1] = (200 - self.pkm_base[self.trainer[pokemon][0]][-1]) * 10

    def level_up(self, team_n):
        self.trainer[team_n][2][0] = str(int(self.trainer[team_n][2][0]) - int(self.trainer[team_n][2][1]))
        self.trainer[team_n][1] += 1
        self.trainer[team_n][2][1] = self.exp_to_lvlup(self.trainer[team_n][0], self.trainer[team_n][1])
        text = self.learn_attack(team_n)
        return text

    def evolve(self, team_n):
        pkm_id_before = self.trainer[team_n][0]

        if len(str(int(pkm_id_before) + 1)) == 1:
            pkm_id = f"00{str(int(pkm_id_before) + 1)}"
        elif len(str(int(pkm_id_before) + 1)) == 2:
            pkm_id = f"0{str(int(pkm_id_before) + 1)}"
        else:
            pkm_id = str(int(pkm_id_before) + 1)

        self.trainer[team_n][0] = pkm_id

        self.get_stats()

    def get_stats(self):
        """
        Function that transform the data from the CSV file into a real l.
        :return:
        """
        trainer = []
        for pokemon in self.trainer:
            pokemon[1] = int(pokemon[1])
            for iv in range(len(pokemon[4])):
                pokemon[4][iv] = int(pokemon[4][iv])
            for ev in range(len(pokemon[5])):
                pokemon[5][ev] = int(pokemon[5][ev])
            stats = [pokemon[3][0], 0, 0, 0, 0, 0, 0]
            stats[1] = \
                int(((pokemon[4][0] + 2 * self.pkm_base[pokemon[0]][0]
                      + int(pokemon[5][0] / 4)) * pokemon[1] / 100)) + pokemon[1] + 10
            for i in range(5):
                stats[i + 2] = int((pokemon[4][i + 1] + 2 * self.pkm_base[pokemon[0]][i + 1]
                                    + int(pokemon[5][i + 1] / 4)) / 100 * pokemon[1]) + pokemon[1] + 5
            pokemon[3] = stats
            pokemon[2][1] = self.exp_to_lvlup(pokemon[0], pokemon[1])
            trainer.append(pokemon)

        self.update_attack_speed()
        self.trainer = trainer

        pc = []
        if len(self.pc) > 0:
            if len(self.pc[0]) > 0:
                for pokemon in self.pc:
                    pokemon[1] = int(pokemon[1])
                    for iv in range(len(pokemon[4])):
                        pokemon[4][iv] = int(pokemon[4][iv])
                    for ev in range(len(pokemon[5])):
                        pokemon[5][ev] = int(pokemon[5][ev])
                    stats = [pokemon[3][0], 0, 0, 0, 0, 0, 0]
                    stats[1] = \
                        int(((pokemon[4][0] + 2 * self.pkm_base[pokemon[0]][0]
                              + int(pokemon[5][0] / 4)) * pokemon[1] / 100)) + pokemon[1] + 10
                    for i in range(5):
                        stats[i + 2] = int((pokemon[4][i + 1] + 2 * self.pkm_base[pokemon[0]][i + 1]
                                            + int(pokemon[5][i + 1] / 4)) / 100 * pokemon[1]) + pokemon[1] + 5
                    pokemon[3] = stats
                    pokemon[2][1] = self.exp_to_lvlup(pokemon[0], pokemon[1])
                    pc.append(pokemon)
        self.pc = pc
