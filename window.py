import pygame
import csv

import datas


# noinspection PyTypeChecker
def get_icon(widgets, x: int, y: int, a: int, b: int):
    image = pygame.Surface([a, b])
    image.blit(widgets, (0, 0), [x, y, a, b])
    return image


class Window:
    def __init__(self, size, bg_color):
        self.window = pygame.Surface(size)
        pygame.draw.rect(self.window, bg_color, (0, 0, size[0], size[1]))


class Pokedex(Window):

    types_name = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "???",
                  "Fire", "Water", "Grass", "Electric", "Psychic", "Dragon", "Ice", "Dark"]
    types = {}

    row, column = 0, 0
    for type_name in types_name:
        types[type_name] = get_icon(pygame.image.load("assets/icons/pokemon_type.png"), 32 * row, 12 * column, 32, 12)
        types[type_name].set_colorkey([0, 0, 0])
        if row < 3:
            row += 1
        else:
            row = 0
            column += 1

    pokedex_id = []
    for pokemon_id in range(1, 151):
        if len(str(pokemon_id)) == 1:
            pokemon_id = f"00{pokemon_id}"
        elif len(str(pokemon_id)) == 2:
            pokemon_id = f"0{pokemon_id}"
        elif len(str(pokemon_id)) == 3:
            pokemon_id = f"{pokemon_id}"
        pokedex_id.append(pokemon_id)

    def __init__(self, new_game=False):
        self.size = [720, 480]
        self.bg_color = 200, 200, 200
        Window.__init__(self, self.size, self.bg_color)

        self.pkdex = datas.pokedex

        self.current_pokemon = ["001", False]

        self.pokedex = [[], [], []]
        if not new_game:
            self.load_pokemon()

        self.pokemon_sprites = {}
        self.get_pokemon_sprite()

        self.page = 1

    def update_pokedex(self, pokemon_id, shiny, update_type="encounter"):
        if update_type == "encounter" and (pokemon_id not in self.pokedex[0] and pokemon_id not in self.pokedex[1]):
            self.pokedex[0].append(pokemon_id)
            print("pokemon added to the pokedex")
        elif update_type == "captured":
            if pokemon_id in self.pokedex[0]:
                self.pokedex[1].append(self.pokedex[0].pop(self.pokedex[0].index(pokemon_id)))
            else:
                self.pokedex[1].append(pokemon_id)
            if shiny:
                self.pokedex[2].append(pokemon_id)
            print("pokemon added to the pokedex")

    def show_pokemon(self, current_pokemon="", shiny=False):
        if current_pokemon != "":
            self.current_pokemon = [current_pokemon, shiny]
        pygame.draw.rect(self.window, self.bg_color, [0, 0, self.size[0], self.size[1]])
        pygame.draw.rect(self.window, [0, 0, 0], [self.size[0] / 2 - 5, 0, 10, self.size[1]])
        sprite = pygame.image.load(f"assets/sprites/"
                                   f"{'shiny' if self.current_pokemon[1] else 'normal'}/"
                                   f"{int(self.current_pokemon[0])}.png")

        sprite = pygame.transform.scale(sprite, (128, 128))
        pos = [5, 35]
        pygame.draw.rect(self.window, [250, 50, 50], [pos[0], pos[1] + 30, self.size[0] / 2 - 15,
                                                      self.size[1] - (pos[1] + 35)])
        pygame.draw.rect(self.window, [250, 200, 200], [pos[0], pos[1] + 35, self.size[0] / 2 - 20, 90])
        pygame.draw.rect(self.window, [250, 200, 200], [pos[0] + 5, pos[1] + 130, self.size[0] / 2 - 25,
                                                        self.size[1] - (pos[1] + 140)])
        pygame.draw.rect(self.window, [250, 50, 50], [pos[0], pos[1], 150, 130])
        pygame.draw.rect(self.window, [250, 200, 200], [pos[0] + 5, pos[1] + 5, 140, 120])
        self.window.blit(sprite, [pos[0] + 70 - sprite.get_width() / 2, pos[1] + 60 - sprite.get_height() / 2])

        types = self.pkdex[self.current_pokemon[0]][1].split()
        if len(types) == 1:
            self.window.blit(Pokedex.types[types[0]], [250, 80])
        else:
            self.window.blit(Pokedex.types[types[0]], [250, 80])
            self.window.blit(Pokedex.types[types[-1]], [290, 80])

        pokemon_id = []
        row = 0

        for pokemon in Pokedex.pokedex_id[10 * (self.page - 1):10 * self.page]:
            pos = [self.size[0] * 2.5 / 4 - 10,
                   50 + 40 * row]
            pygame.draw.circle(self.window, [200, 150, 150], [int(pos[0] + 20), int(pos[1] + 15)], 20)
            if pokemon in self.pokedex[0]:
                self.window.blit(self.pokemon_sprites[pokemon], pos)
            elif pokemon in self.pokedex[1]:
                self.window.blit(self.pokemon_sprites[pokemon], pos)
            else:
                self.window.blit(self.pokemon_sprites["000"], [pos[0], pos[1] - 10])
            pokemon_id.append(pokemon)

            row += 1

        return pokemon_id

    def load_pokemon(self, file_path="pokedex"):
        file = csv.reader(open(f"assets/data/{file_path}.csv", "r"), delimiter=';')
        pokedex_file = []
        for pokemon_list in file:
            pokedex_file.append(pokemon_list)
        for pokemon_list in range(3):
            for pokemon in pokedex_file[pokemon_list]:
                self.pokedex[pokemon_list].append(pokemon)

    def save_pokedex(self, file_path="pokedex"):
        """
        Function which save the trainer's pokemon data.
        """
        file = csv.writer(open(f"assets/data/{file_path}.csv", "w", newline=""), delimiter=";")
        for pokemon_list in self.pokedex:
            file.writerow(pokemon_list)

    def get_pokemon_sprite(self):
        sprite = pygame.image.load(f"assets/sprites/icons/0.png")
        self.pokemon_sprites["000"] = pygame.transform.scale(sprite, [40, 40])
        for pokemon_list in range(len(self.pokedex)):
            for pokemon in self.pokedex[pokemon_list]:
                self.pokemon_sprites[pokemon] = pygame.image.load(f"assets/sprites/icons/{int(pokemon)}.png")

    def change_page(self, page=0):
        self.page += page
        if self.page == 16:
            self.page = 1
        elif self.page == 0:
            self.page = 15


class PC(Window):
    def __init__(self):
        self.size = [720, 480]
        self.bg_color = 10, 10, 10
        Window.__init__(self, self.size, self.bg_color)

        self.selected = -1
        self.page = 1

    def draw_pokemon(self, pc):
        pygame.draw.rect(self.window, [130, 170, 130], [5, 5, self.size[0] - 10, self.size[1] - 10])
        pygame.draw.rect(self.window, [100, 130, 100], [5, 5, 165, self.size[1] - 10])
        pygame.draw.rect(self.window, [120, 100, 100], [5, 5, self.size[0] - 10, 118])

        if len(pc) > 0:
            column, row = 0, 0
            for pokemon in pc[:30]:

                sprite = pygame.image.load(f"assets/sprites/icons/{int(pokemon[0])}.png")
                sprite = pygame.transform.scale(sprite, [80, 60])

                self.window.blit(sprite, [175 + 90 * column, 125 + 70 * row])
                if column > 4:
                    column = 0
                    row += 1
                else:
                    column += 1

        return f"Box {self.page}"

    def draw_select(self, pc):
        if self.selected != -1:
            row, column = int(self.selected / 6), self.selected % 6
            pygame.draw.rect(self.window, [130, 200, 130], [180 + 90 * column, 125 + 70 * row, 70, 60])

            sprite = pygame.image.load(f"assets/sprites/icons/{int(pc[self.selected][0])}.png")
            sprite = pygame.transform.scale(sprite, [80, 60])

            self.window.blit(sprite, [175 + 90 * column, 125 + 70 * row])

    def change_page(self, page=0):
        self.page += page
        if self.page == 15:
            self.page = 1
        elif self.page == 0:
            self.page = 14
        self.selected = -1


class Profile(Window):
    def __init__(self, ):
        self.size = [480, 480]
        self.bg_color1 = 250, 200, 200
        self.bg_color2 = 250, 50, 50
        Window.__init__(self, self.size, self.bg_color2)

        self.pokedex = datas.pokedex

    def pokemon_info(self, pokemon):
        pygame.draw.rect(self.window, self.bg_color1, [5, 5, self.size[0] - 10, self.size[1] - 10])
        pygame.draw.rect(self.window, self.bg_color2, [0, 0, 138, 138])
        pygame.draw.rect(self.window, self.bg_color1, [5, 5, 128, 128])

        sprite = pygame.image.load(f"assets/sprites/{pokemon[-1]}/{int(pokemon[0])}.png")
        sprite = pygame.transform.scale(sprite, (128, 128))

        self.window.blit(sprite, [5, 5])

        name = self.pokedex[pokemon[0]][0]

        types = self.pokedex[pokemon[0]][1].split()
        if len(types) == 1:
            self.window.blit(Pokedex.types[types[0]], [350, 35])
        else:
            self.window.blit(Pokedex.types[types[0]], [350, 35])
            self.window.blit(Pokedex.types[types[-1]], [390, 35])

        return name
