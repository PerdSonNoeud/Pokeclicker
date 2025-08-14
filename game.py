# Import files and libraries the game need
# Files
from pokemon import Pokemon
from trainer import Trainer
import window
import moves
# Library
import random
import pygame


# Create class Game
class Game:
    def __init__(self):
        """
        Function that create the window and init all data the game needs to work well.
        """
        # Init window
        # Get Screen size
        self.infoObject = pygame.display.Info()
        self.size_x, self.size_y = self.infoObject.current_w, self.infoObject.current_h
        # Create Window
        self.window = pygame.display.set_mode((self.size_x, self.size_y), pygame.FULLSCREEN)
        # Set Window icon
        pygame.display.set_icon(pygame.image.load("assets/sprites/normal/25.png"))
        # Set Window name
        pygame.display.set_caption("Pokemon Clicker")
        # Clock
        self.clock = pygame.time.Clock()
        # Init other window
        # If False: nothing to show, If "pokedex": Showing pokedex, If "pc": Showing PC
        self.show_window = False
        # If True: showing Summary, If False: nothing to show
        self.show_summary = False
        # If True: showing FPS, If False: nothing to show
        self.show_fps = False
        # FPS Limiter
        self.fps = 60

        # Init font
        # For Title
        self.title = pygame.font.Font('assets/font/pokemon_font.ttf', 32)
        # For Sub Title
        self.sub_title = pygame.font.Font('assets/font/pokemon_font.ttf', 21)
        # For text like pokemon name, level
        self.text = pygame.font.Font('assets/font/pokemon_font.ttf', 16)
        # For Gender Symbol (♂ / ♀)
        self.gender_text = pygame.font.SysFont('arial', 16)
        # For Chat
        self.chat_text = pygame.font.Font('assets/font/pokemon_font.ttf', 12)
        # Init colors (R, G, B)
        # Window color
        self.bg_color = 150, 150, 150
        # Button colors
        self.dark_gray = 180, 180, 180
        self.gray = 220, 220, 220
        # Chat colors
        self.learn_move = 50, 210, 210
        self.neutral = 250, 250, 250
        self.console = 210, 210, 50
        self.enemy = 210, 120, 50
        self.green = 50, 220, 50
        self.ally = 50, 200, 210
        # Others
        self.blue = 50, 50, 250
        self.red = 250, 50, 50
        self.black = 0, 0, 0
        # chat = [Chat l: [Messages split to change color: ["Text", colorA], ["Text", colorB]]...]
        self.chat = [[["You started the game.", self.console]]]

        # Init game data
        # Background
        self.bg = pygame.draw.rect(self.window, self.bg_color, [0, 0, self.size_x, self.size_y])
        # Game status: "main menu": when game not started yet,
        # "is_playing": when playing, "parameter": when in parameter
        self.game_status = "main menu"
        # While window is opened
        self.running = True
        # Position of the player
        self.locate = "Route 1"
        # Index of the pokemon in the trainer team we are looking at
        self.looking_at = 0

        # Init classes from others files
        # For moves
        self.moves = moves.Move("Absorb")
        # For pokedex
        self.pokedex = window.Pokedex()
        # For wild pokemon
        self.pokemon = Pokemon()
        # For trainer
        self.trainer = Trainer()
        self.trainer_case = []
        self.trainer_button = []
        # For pokemon Profile
        self.profile = window.Profile()
        # For trainer's PC
        self.pc = window.PC()
        self.cases = []

        # Init controller
        self.mouse_position = pygame.mouse.get_pos()

        # Init timer for pokemon's attack speed
        self.timer = 0

        # Init functions
        # Select menu's buttons
        self.new_button, self.resume_button, self.quit_button = self.select_menu()
        # Parameter's buttons
        self.resume_button, self.save_button, self.quit_button = self.parameter()
        # Wild pokemon
        self.pokemon_appeared = self.summon(self.locate, prints=False)
        self.pokemon_hit_box = pygame.draw.rect(self.window, [150, 150, 150],
                                                [self.size_x / 2 - self.pokemon.pokemon_sprite.get_width() / 2,
                                                 self.size_y / 2 - self.pokemon.pokemon_sprite.get_height() / 4,
                                                 self.pokemon.pokemon_sprite.get_width(),
                                                 self.pokemon.pokemon_sprite.get_height()])
        # Pokedex
        self.window_upper = self.pokedex.window
        self.pos = [self.window.get_width() / 2 - self.window_upper.get_width() / 2,
                    self.window.get_height() / 2 - self.window_upper.get_height() / 2]
        self.pokedex_upper = self.show_pokedex_window()
        # Trainer
        self.trainer_pokemon = self.trainer.display_team(self.clock.tick(self.fps))
        self.pos_trainer = [self.window.get_width() / 2 - self.trainer_pokemon.get_width() / 2,
                            self.window.get_height() - self.trainer_pokemon.get_height()]
        # When playing Buttons
        self.parameter_button, self.pokedex_button = self.show_buttons()

    def summon(self, locate="all", prints=True):
        """
        Function which uses the function random_pokemon from the file pokemon to select a random pokemon in the
        location (location) with their rarity rate.

        :param locate: location in the dictionary location (str type)
        :param prints: True if we want to print info (Bool type)

        :return: ("the pokemon ID", the pokemon level, the experience the pokemon need to level up)
        """
        # Display pokemon
        pokemon_appeared, level = self.pokemon.random_pokemon(locate)
        shiny = self.pokemon.get_img(pokemon_appeared[0], prints=prints)

        # Gathering data
        # Get IV
        self.pokemon.get_ivs()
        # Get Stats
        self.pokemon.get_stats(pokemon_appeared[0])

        # Get HP
        self.pokemon.hp = self.pokemon.hp_max
        # Get exp to level up
        exp_required = self.pokemon.exp_to_lvlup(pokemon_appeared[0])

        self.pokemon.random_attack(pokemon_appeared[0])
        # Update pokedex
        self.pokedex.update_pokedex(pokemon_appeared[0], self.pokemon.shiny)

        if prints:
            # Stats
            print(f"\nStats{self.pokemon.stats}")
            # IVs
            print(f"IVs{self.pokemon.iv}")
            # Level up
            print(f"\n{self.pokemon.pokedex[pokemon_appeared[0]][0]} level {level} need {exp_required} exp to level up")
            # Move set
            print("\nMove set:")
            for move in self.pokemon.move_set:
                print(f"\t{move} :\n\t\tType :\t\t{self.pokemon.move[move][0]}"
                      f"\n\t\tPP:\t\t{self.pokemon.move[move][1]}\n\t\tPower:\t\t{self.pokemon.move[move][2]}")
                if self.pokemon.move[move][3] == "-":
                    print(f"\t\tAccurate: {self.pokemon.move[move][3]}\n")
                else:
                    print(f"\t\tAccurate: {self.pokemon.move[move][3]}%\n")
        # Return [Pokemon ID, pokemon level, exp to level UP, if shiny]
        return pokemon_appeared[0], level, exp_required, shiny

    def show_trainer_team(self, tick=0.0):
        """
        Function that display the trainer team at the bottom of the window with their icon,
        HP bar and Attack Speed bar. You can also click on the pokemon to open a little menu
        where you can choose to display the pokemon's summary, pokedex page or send it to the
        trainer's PC.

        :param tick: Tick between each frame to when how much whe have to add to the attack
                     speed bar. (float type)

        :return: None
        """
        # Get the trainer's team plus the team to display at the bottom center of the window
        self.trainer_pokemon = self.trainer.display_team(tick)
        # Reset the l where we are going to stock the cases of the trainer's pokemon
        self.trainer_case = []
        # Get the coord where we are going to place the team display
        self.pos_trainer = [self.window.get_width() / 2 - self.trainer_pokemon.get_width() / 2,
                            self.window.get_height() - self.trainer_pokemon.get_height()]
        # Create the cases to check when we click on a trainer's pokemon
        for number in range(len(self.trainer.trainer)):
            self.trainer_case.append(pygame.draw.rect(self.window, [0, 0, 0],
                                                      [self.pos_trainer[0] + 2 + 63 * number,
                                                       self.pos_trainer[1] + 2, 63, int(30 * 1.5)]))
        # Display the trainer's team on the window
        self.window.blit(self.trainer_pokemon, self.pos_trainer)
        # If we clicked on one of the trainer's pokemon
        if self.trainer.selected != -1:
            # Create the little menu
            pygame.draw.rect(self.window, [250, 50, 50], [self.pos_trainer[0] - 24 + 63 * self.trainer.selected,
                                                          self.pos_trainer[1] - 73, 113, 68])
            # Name of the buttons
            text = ["Summary", "Pokedex", "Send to PC"]
            # Reset the l where the buttons of those little menu are going to be stock
            self.trainer_button = []
            # Create the buttons of those little menu
            for number in range(3):
                self.trainer_button.append(pygame.draw.rect(self.window, [250, 200, 200],
                                                            [self.pos_trainer[0] - 22 + 63 * self.trainer.selected,
                                                             self.pos_trainer[1] - 71 + 22 * number, 109, 20]))
                text[number] = self.chat_text.render(text[number], True, self.black)
                self.window.blit(text[number], [self.pos_trainer[0] + 32 + 63 * self.trainer.selected
                                                - text[number].get_width() / 2, self.pos_trainer[1] - 69 + 22 * number])

    def show_pokedex_window(self):
        """
        Function that display the pokedex at the center of the window. It shows us the datas
        of the current wild pokemon in front of us or the pokemon we asked for when we open
        the pokedex. You can change the pokedex page by using <- or -> and click on the pokemon
        you want to see the datas.

        :return: (pygame.Rect type)
        """
        # Get pokemon in the current page of the pokedex plus the sprite of the current wild pokemon
        page = self.pokedex.show_pokemon(shiny=self.pokemon.shiny)
        # Name of the current wild pokemon
        name = self.text.render(f"{self.pokemon.pokedex[self.pokedex.current_pokemon[0]][0]}", True, self.black)
        # Type of the current wild pokemon
        text = self.text.render("Types: ", True, self.black)
        # Display them on the window
        self.pokedex.window.blit(name, [160, 45])
        self.pokedex.window.blit(text, [160, 75])

        row = 0
        # Display all the pokemon's ID and name
        for pokemon_id in page:
            # if we haven't encountered them yet
            if pokemon_id not in self.pokedex.pokedex[0] and pokemon_id not in self.pokedex.pokedex[1]:
                text = self.chat_text.render(f"{pokemon_id}.   ???", True, self.black)
            # if we already encountered them one time
            else:
                text = self.chat_text.render(f"{pokemon_id}.   {self.pokemon.pokedex[pokemon_id][0]}", True, self.black)
                # if we captured them one time
                if pokemon_id in self.pokedex.pokedex[1]:
                    # Get the caught icon
                    catch_icon = pygame.image.load("assets/icons/pokeball.png")
                    catch_icon.set_colorkey([189, 189, 189])
                    # Display the icon
                    self.pokedex.window.blit(catch_icon, [self.pokedex.size[0] * 2.5 / 4 - 12, 75 + 40 * row])
            # Display the ID pus the name if we already encountered it
            self.pokedex.window.blit(text, [self.pokedex.size[0] * 3 / 4 - 40, 62 + 40 * row])
            row += 1
        # Display the pokedex
        self.window.blit(self.pokedex.window, self.pos)
        # Create the upper and display it
        pos = [self.pos[0], self.pos[1], self.pokedex.size[0], 30]
        pokedex_upper = pygame.draw.rect(self.window, (220, 80, 80), pos)
        text = self.text.render("Pokedex", True, self.black)
        self.window.blit(text, [pos[0] + 15 - text.get_height() / 2, pos[1] + 15 - text.get_height() / 2])
        return pokedex_upper

    def show_pc_window(self):
        """
        Function that display the trainer's PC at the center of the window. It shows us the
        pokemon in the PC of the trainer with their icons. You can also click on the pokemon
        to open a menu on the left where you can choose to display the pokemon's summary, pokedex
        page or add it to the trainer's current team.

        :return: None
        """
        # Coord of the pokemon in the PC
        pos = [self.size_x / 2 - self.pc.size[0] / 2 + 180,
               self.size_y / 2 - self.pc.size[1] / 2 + 125]
        # Reset cases of the pokemon
        self.cases = []

        # If there are pokemon in the box of the PC
        if len(self.trainer.pc) > 0:
            column, row = 0, 0
            # Create their hit box
            for pokemon in range(len(self.trainer.pc[:30])):
                # Save them in the l
                self.cases.append(pygame.draw.rect(self.window, [0, 0, 0],
                                                   [pos[0] + 90 * column, pos[1] + 70 * row, 70, 60]))
                # Go to the next coord
                if column > 4:
                    column = 0
                    row += 1
                else:
                    column += 1

        box_name = self.pc.draw_pokemon(self.trainer.pc)
        box_name = self.title.render(box_name, True, self.black)
        self.pc.window.blit(box_name, [self.pc.size[0] / 2 - box_name.get_width() / 2, 65 - box_name.get_height() / 2])
        self.pc.draw_select(self.trainer.pc)
        self.window.blit(self.pc.window, self.pos)

    def print_summary(self):
        if len(self.trainer.trainer) > 0:
            info = self.profile.pokemon_info(self.trainer.trainer[0])
            text = self.text.render(info, True, self.black)
            self.profile.window.blit(text, [220 - text.get_width()/2, 30])
            self.window.blit(self.profile.window, [0, self.size_y / 2 - self.profile.size[1] / 2])

    def catch_pokemon(self):
        """
        Function that will catch the wild pokemon if his/her HP is under 1/5 of the HP max
        and add it to the trainer team, if there is no place in the trainer team, it sends
        it to the PC and if there is no place in the PC too, you can't capture it.

        :return: None
        """
        # If the pokemon has less than 1/5 of his/her HP max
        if self.pokemon.hp <= int(self.pokemon.hp_max / 5):
            # If you have enough place in your Team or your PC
            if len(self.trainer.trainer) + len(self.trainer.pc) < 426:
                # Say in the chat that you caught it
                self.chat.append([["You caught a ", self.console],
                                  ["shiny" if self.pokemon.shiny else "", self.console],
                                  [f"{self.pokemon.pokedex[self.pokemon_appeared[0]][0]}", self.ally],
                                  [f" level {self.pokemon.level} ", self.console]])
                # Get his/her stats
                stats = self.pokemon.stats
                # Get his/her HP
                stats.insert(0, self.pokemon.hp)
                # If you have enough place in your Team
                if len(self.trainer.trainer) < 6:
                    # Add it to your Team
                    self.trainer.trainer.append([self.pokemon_appeared[0], self.pokemon.level,
                                                 ["0", f"{self.pokemon.exp}"], stats,
                                                 self.pokemon.iv, self.pokemon.evs, self.pokemon.move_set,
                                                 self.pokemon.gender, "shiny" if self.pokemon.shiny else "normal"])
                else:
                    # Say in the chat that you don't have enough place in your Team
                    self.chat.append([["No place left in your Team.", self.console]])
                    n = 0
                    # If you don't have enough place in your PC
                    if len(self.trainer.pc) > 30:
                        # Search for the next box where you have enough place
                        while len(self.trainer.pc) >= 30:
                            self.trainer.save_pc(self.pc.page + n)
                            n += 1
                            if self.pc.page + n == 15:
                                n = 1 - self.pc.page
                            self.trainer.get_player_pc(self.pc.page + n)

                    # Add it to your PC's Box
                    self.trainer.pc.append([self.pokemon_appeared[0], self.pokemon.level,
                                            ["0", f"{self.pokemon.exp}"], stats,
                                            self.pokemon.iv, self.pokemon.evs, self.pokemon.move_set,
                                            self.pokemon.gender, "shiny" if self.pokemon.shiny else "normal"])

                    self.trainer.save_pc(self.pc.page + n)
                    self.trainer.get_player_pc(self.pc.page)
                    # Say in the chat that you send it to the PC's Box
                    self.chat.append([[f"{self.pokemon.pokedex[self.pokemon_appeared[0]][0]} has been "
                                       f"sent to Box {self.pc.page}.", self.console]])

                # Update pokedex
                self.pokedex.update_pokedex(self.pokemon_appeared[0], self.pokemon.shiny, "captured")
                # Update Stats
                self.trainer.get_stats()
                # Summon a new wild pokemon
                self.pokemon_appeared = self.summon(self.locate)
            else:
                # Say in the chat that you don't have enough place in your Team nor in your PC to stock it
                self.chat.append([["No place left in your Team nor your PC.", self.console]])

    def show_buttons(self):
        """
        Function that creates buttons at the bottom right of the screen to open parameter
        or pokedex if you click on it.

        :return: parameter button, pokedex button (tuple of pygame.Rect type)
        """
        # Create Pokedex Button
        pokedex = pygame.draw.circle(self.window, [150, 150, 150], [self.size_x - 30, self.size_y - 65], 15)
        # Get pokedex Icon
        pokedex_icon = pygame.image.load("assets/icons/pokedex.png")
        pokedex_icon.set_colorkey([255, 255, 255])
        # Display the pokedex button
        self.window.blit(pokedex_icon, [self.size_x - 45, self.size_y - 80])
        # Create Parameter Button
        parameter = pygame.draw.circle(self.window, [50, 50, 50], [self.size_x - 30, self.size_y - 25], 15)

        return parameter, pokedex

    def handle_input(self):
        """
        The function that checks which key we pressed and does an action

        :return: None
        """
        # Get which key we press
        pressed = pygame.key.get_pressed()
        # if we press ->
        if pressed[pygame.K_RIGHT]:
            self.pokemon.heal(1)
        # if we press <-
        if pressed[pygame.K_LEFT]:
            self.pokemon.damage(1)

    def show_pokemon(self):
        """
        Function which display the pokemon on the screen

        :return: None
        """
        # pokemon name and level
        name = self.text.render(f"{self.pokemon.pokedex[self.pokemon_appeared[0]][0]}", True, self.black)
        gender = self.gender_text.render("♂" if self.pokemon.gender == "male" else "♀", True, self.black)
        lvl = self.text.render(f"lvl {str(self.pokemon_appeared[1])}", True, self.black)
        self.window.blit(name, [self.size_x / 2 - 100,
                                self.size_y / 2 - self.pokemon.pokemon_sprite.get_height() / 2])
        self.window.blit(gender, [self.size_x / 2 - 90 + name.get_width(),
                                  self.size_y / 2 - self.pokemon.pokemon_sprite.get_height() / 2])
        self.window.blit(lvl, [self.size_x / 2 + 50,
                               self.size_y / 2 - self.pokemon.pokemon_sprite.get_height() / 2])

        # pokemon sprite
        self.pokemon.hit_box = pygame.draw.rect(self.window, self.bg_color,
                                                [self.size_x / 2 - self.pokemon.pokemon_sprite.get_width() / 2,
                                                 self.size_y / 2 - self.pokemon.pokemon_sprite.get_height() / 4,
                                                 self.pokemon.pokemon_sprite.get_width(),
                                                 self.pokemon.pokemon_sprite.get_height()])

        self.window.blit(self.pokemon.pokemon_sprite, [self.size_x / 2 - self.pokemon.pokemon_sprite.get_width() / 2,
                                                       self.size_y / 2 - self.pokemon.pokemon_sprite.get_height() / 4])

        # pokemon health bar
        self.pokemon.update_health_bar(self.window,
                                       self.size_x / 2 - 75,
                                       self.size_y / 2 - self.pokemon.pokemon_sprite.get_height() * .25)

        # pokemon attack speed bar
        self.pokemon.update_atk_spd_bar(self.window,
                                        self.size_x / 2 - 75,
                                        self.size_y / 2 - self.pokemon.pokemon_sprite.get_height() * .25,
                                        self.timer)

    def print_chat(self):
        """
        Function that display chat at the top left of the screen.

        :return: None
        """
        # Draw chat window
        pygame.draw.rect(self.window, [130, 130, 130], [5, 5, 500, 150])
        # the 9 last messages of the chat
        for text in range(len(self.chat[-9:])):
            text_size = 0
            # Get the text
            for element in range(len(self.chat[text + len(self.chat[:-10])])):
                new_text = ""
                for character in self.chat[text + len(self.chat[:-10])][element][0]:
                    if character == "_" or character == " ":
                        new_text += "   "
                    else:
                        new_text += character
                # Create the text the different color
                chat = self.chat_text.render(new_text, True, self.chat[text + len(self.chat[:-10])][element][1])
                # Display it on the chat
                self.window.blit(chat, [8 + text_size, 8 + (chat.get_height() + 2) * text])
                text_size += chat.get_width()

    def print_fps(self):
        """
        Function that display FPS at the top right of the screen.

        :return: None
        """
        # Get the FPS
        text = self.text.render(f"{int(self.clock.get_fps())} fps", True, (0, 0, 0))
        # Display the FPS
        self.window.blit(text, [self.size_x - text.get_width() - 10, 10])

    def parameter(self):
        """
        Function which create the game main menu with play button and game title

        :return: Resume button, Save button, Quit button (l of pygame.Rect type)
        """
        # Create the 3 buttons text
        text1 = self.sub_title.render("Resume", True, self.black)
        text2 = self.sub_title.render("Save", True, self.black)
        text3 = self.sub_title.render("Quit Game", True, self.black)

        button_list = []
        space = 0.4
        # Draw the 3 buttons
        for button in range(3):
            # Draw the button shadow
            pygame.draw.rect(self.window, self.dark_gray, [self.size_x / 2 - 150, self.size_y * space + 5, 310, 50])
            # Draw the button
            button_list.append(pygame.draw.rect(self.window, self.gray, [self.size_x / 2 - 155, self.size_y * space,
                                                                         310, 50]))
            space += 0.1

        # Display the 3 buttons text
        self.window.blit(text1, [self.size_x / 2 - text1.get_width() / 2, self.size_y * 0.4 + 15])
        self.window.blit(text2, [self.size_x / 2 - text2.get_width() / 2, self.size_y * 0.5 + 15])
        self.window.blit(text3, [self.size_x / 2 - text3.get_width() / 2, self.size_y * 0.6 + 15])

        return button_list

    def select_menu(self):
        """
        Function which create the game main menu with play button and game title

        :return: Resume button, Save button, Quit button (l of pygame.Rect type)
        """
        # Create the 3 buttons text
        text1 = self.sub_title.render("New Game", True, self.black)
        text2 = self.sub_title.render("Continue Game", True, self.black)
        text3 = self.sub_title.render("Main Menu", True, self.black)

        button_list = []
        space = 0.4
        # Draw the 3 buttons
        for button in range(3):
            # Draw the button shadow
            pygame.draw.rect(self.window, self.dark_gray, [self.size_x / 2 - 150, self.size_y * space + 5, 310, 50])
            # Draw the button
            button_list.append(pygame.draw.rect(self.window, self.gray, [self.size_x / 2 - 155, self.size_y * space,
                                                                         310, 50]))
            space += 0.1

        # Display the 3 buttons text
        self.window.blit(text1, [self.size_x / 2 - text1.get_width() / 2, self.size_y * 0.4 + 15])
        self.window.blit(text2, [self.size_x / 2 - text2.get_width() / 2, self.size_y * 0.5 + 15])
        self.window.blit(text3, [self.size_x / 2 - text3.get_width() / 2, self.size_y * 0.6 + 15])

        return button_list

    def update(self):
        """
        function that updates the game display.

        :return: None
        """
        self.bg = pygame.draw.rect(self.window, [150, 150, 150], [0, 0, self.size_x, self.size_y])
        self.mouse_position = pygame.mouse.get_pos()

        if self.game_status != "main menu" and self.game_status != "select_menu":
            # Show buttons
            self.parameter_button, self.pokedex_button = self.show_buttons()
            # Show pokemon
            trainer_pokemon = self.trainer.pokemon_info(self.window, self.size_y, self.looking_at)
            exp = self.chat_text.render(trainer_pokemon[4], True, self.black)
            self.window.blit(exp, [380, self.size_y - 92])
            move_set = []
            for move in trainer_pokemon[3]:
                move_name = ""
                for letter in move:
                    if letter == "_":
                        move_name += "   "
                    else:
                        move_name += letter
                move_set.append(move_name)

            self.window.blit(trainer_pokemon[1], [75 - trainer_pokemon[1].get_width() / 2,
                                                  self.size_y - 55 - trainer_pokemon[1].get_height() / 2])
            name = self.text.render(f"{trainer_pokemon[0]}   ", True, self.black)
            self.window.blit(name, [175, self.size_y - 115])
            if len(self.trainer.trainer) > 0:
                gender = self.gender_text.render("♂" if self.trainer.trainer[self.looking_at][7] == "male" else "♀",
                                                 True, self.blue if self.trainer.trainer[self.looking_at][7] == "male"
                                                 else self.red)
                self.window.blit(gender, [175 + name.get_width(), self.size_y - 115])
                level = self.text.render(f"lvl. {trainer_pokemon[2]}", True, self.black)
                self.window.blit(level, [430, self.size_y - 115])

                pos_x, pos_y = 0, 0
                for move in range(len(move_set)):
                    text = self.chat_text.render(move_set[move], True, self.black)
                    self.window.blit(text, [260 + 150 * (pos_x % 2) - text.get_width() / 2,
                                            self.size_y - 70 + 35 * (pos_y % 2)])
                    self.window.blit(self.pokedex.types[self.trainer.move[trainer_pokemon[3][move]][0]],
                                     [210 + 150 * (pos_x % 2), self.size_y - 55 + 35 * (pos_y % 2)])
                    self.window.blit(self.moves.category[self.trainer.move[trainer_pokemon[3][move]][1]],
                                     [280 + 150 * (pos_x % 2), self.size_y - 57 + 35 * (pos_y % 2)])
                    pos_x += 1
                    if pos_x % 2 == 0:
                        pos_y += 1

            # Show chat
            self.print_chat()
            # Show pokemon
            self.show_pokemon()

        if self.game_status == "main menu":
            play = self.text.render("Press any button to start", True, self.black)
            self.window.blit(play, [self.size_x / 2 - play.get_width() / 2,
                                    self.size_y * .75])

        elif self.game_status == "select_menu":
            # Show trainer's pokemon
            self.new_button, self.resume_button, self.quit_button = self.select_menu()

        elif self.game_status == "parameter":
            # Show trainer's pokemon
            self.show_trainer_team()
            # Show parameter
            self.resume_button, self.save_button, self.quit_button = self.parameter()

        elif self.game_status == "is_playing":
            # Show trainer's pokemon
            self.show_trainer_team(self.clock.tick(self.fps))

            # Wild pokemon attack
            self.timer += self.clock.tick(self.fps)
            if self.timer >= self.pokemon.attack_speed:
                move = random.choice(self.pokemon.move_set)
                team_n = random.randint(0, len(self.trainer.trainer) - 1)
                if self.pokemon.move[move][1] != "Status":
                    self.chat.append([["Foe", self.neutral],
                                      [f"{self.pokemon.pokedex[self.pokemon_appeared[0]][0]}", self.enemy],
                                      [f" used {move} on", self.neutral],
                                      [f" {self.trainer.pokedex[self.trainer.trainer[team_n][0]][0]}", self.ally],
                                      [" !", self.neutral]])
                    # Physical move
                    if self.pokemon.move[move][1] == "Physical":
                        move = moves.PhysicalMove(move)
                        damage, effective = move.damage([self.pokemon_appeared[0], self.pokemon.level],
                                                        self.trainer.trainer[team_n])
                        self.trainer.damage(team_n, damage * effective)
                    # Special move
                    else:
                        move = moves.SpecialMove(move)
                        damage, effective = move.damage([self.pokemon_appeared[0], self.pokemon.level],
                                                        self.trainer.trainer[team_n])
                        self.pokemon.damage(damage * effective)
                    # Effectiveness
                    if effective == 2 or effective == 4:
                        self.chat.append([["It's super effective !", self.green]])
                    elif effective == .5 or effective == .25:
                        self.chat.append([["It's not super effective !", self.red]])
                    elif effective == 0:
                        self.chat.append([["It doesn't affect ", self.black],
                                          [f"{self.trainer.pokedex[self.trainer.trainer[team_n][0]][0]} !", self.ally]])
                    # Touched or not
                    if damage == 0:
                        self.chat.append([["But it missed.", self.gray]])
                # Status move
                else:
                    self.chat.append([["Foe ", self.neutral],
                                      [f"{self.pokemon.pokedex[self.pokemon_appeared[0]][0]}", self.enemy],
                                      [f" used {move} !", self.neutral]])

                self.timer = 0

            # Team pokemon attack
            for pokemon in range(len(self.trainer.trainer)):
                if self.trainer.attack_speed[pokemon][0] >= self.trainer.attack_speed[pokemon][1]:

                    move = random.choice(self.trainer.trainer[pokemon][6])
                    self.chat.append([[f"{self.pokemon.pokedex[self.trainer.trainer[pokemon][0]][0]}", self.ally],
                                      [f" used {move} !", self.neutral]])

                    if self.trainer.move[move][1] != "Status":
                        if self.trainer.move[move][1] == "Physical":
                            move = moves.PhysicalMove(move)
                            damage, effective = move.damage(self.trainer.trainer[pokemon],
                                                            [self.pokemon_appeared[0], self.pokemon.level])
                            self.pokemon.damage(damage * effective)

                        else:
                            move = moves.SpecialMove(move)
                            damage, effective = move.damage(self.trainer.trainer[pokemon],
                                                            [self.pokemon_appeared[0], self.pokemon.level])
                            self.pokemon.damage(damage * effective)

                            # Effectiveness
                        if effective == 2 or effective == 4:
                            self.chat.append([["It's super effective !", self.green]])
                        elif effective == .5 or effective == .25:
                            self.chat.append([["It's not super effective !", self.red]])
                        elif effective == 0:
                            self.chat.append([["It doesn't affect ", self.black],
                                              [f"{self.trainer.pokedex[self.pokemon_appeared[0]][0]} !",
                                               self.enemy]])

                        if damage == 0:
                            self.chat.append([["But it missed.", self.gray]])

                    self.trainer.attack_speed[pokemon][0] = 0

            # Fainted wild pokemon
            if self.pokemon.hp <= 0:
                self.chat.append([[f"Foe ", self.neutral],
                                  [f"{self.pokemon.pokedex[self.pokemon_appeared[0]][0]} ", self.enemy],
                                  [f"level {self.pokemon.level} fainted.", self.neutral]])
                exp = self.pokemon.exp_give(self.pokemon_appeared[0], s=len(self.trainer.trainer))
                self.chat.append([[f"Your team won {exp}exp.", self.console]])
                n = 1
                # Pokemon to evolve
                evolve = ""
                text = "No new attack."
                for pokemon in range(len(self.trainer.trainer)):
                    if self.trainer.trainer[pokemon][1] < 100:
                        self.trainer.trainer[pokemon][2][0] = str(int(self.trainer.trainer[pokemon][2][0]) + exp)
                    self.trainer.get_ev_max(self.pokemon_appeared[0], pokemon)
                    if int(self.trainer.trainer[pokemon][2][0]) >= int(self.trainer.trainer[pokemon][2][1]) \
                            and self.trainer.trainer[pokemon][1] < 100:
                        lvl_up = 0
                        while int(self.trainer.trainer[pokemon][2][0]) >= int(self.trainer.trainer[pokemon][2][1]):
                            text = self.trainer.level_up(pokemon)
                            pygame.mixer.music.load("assets/sound/level_up.mp3")
                            pygame.mixer.music.play()
                            if self.trainer.pokedex[self.trainer.trainer[pokemon][0]][3] and str(pokemon) not in evolve:
                                if type(self.trainer.pokedex[self.trainer.trainer[pokemon][0]][3]) != str:
                                    if int(self.trainer.trainer[pokemon][1]) >= \
                                            self.trainer.pokedex[self.trainer.trainer[pokemon][0]][3]:
                                        evolve += str(pokemon)
                            lvl_up += 1

                        self.chat.append([[f"{self.trainer.pokedex[self.trainer.trainer[pokemon][0]][0]} ", self.ally],
                                          [f"gained {lvl_up} Level !", self.console]])
                        self.chat.append([[f"{self.trainer.pokedex[self.trainer.trainer[pokemon][0]][0]} ", self.ally],
                                          [f"is now Level {self.trainer.trainer[pokemon][1]}.", self.console]])
                    n += 1

                # Check if new move to learn
                if text != "No new attack.":
                    self.chat.append([[text[0], self.ally], [text[1], self.console]])

                if evolve != "":
                    for team_n in evolve:
                        self.trainer.evolve(int(team_n))

                self.pokemon_appeared = self.summon(self.locate)
                self.timer = 0

            if self.show_window == "pokedex":
                self.window_upper = self.show_pokedex_window()
            elif self.show_window == "pc":
                self.show_pc_window()

        # Show FPS
        if self.show_fps:
            self.print_fps()
        # Show profile
        if self.show_summary:
            self.print_summary()

    def new_game(self):
        """
        Create a new game with the "new game" button in the main menu by resetting the pokedex,
        the trainer's pokemon and the PC inventory.

        :return: None
        """
        self.pokedex = window.Pokedex(new_game=True)
        self.game_status = "is_playing"
        self.locate = "Route 1"

    def continue_game(self):
        """
        Get the saved data and continue the game.

        :return: None
        """
        self.game_status = "is_playing"
        self.trainer.get_player_pokemon()
        self.trainer.get_player_pc(self.pc.page)
        self.locate = self.trainer.get_others_data()

    def main(self):
        """
        Main function which will check all conditions of each function to make the game work well.

        :return: None
        """
        # Main while
        while self.running:

            # Update window
            self.mouse_position = pygame.mouse.get_pos()
            self.handle_input()
            self.update()

            # Check actions
            for event in pygame.event.get():
                # If player quit game
                if event.type == pygame.QUIT:
                    self.running = False

                # When player is in main menu
                elif self.game_status == "main menu":
                    # If press any button, it'll start the game
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        self.game_status = "select_menu"

                # When player is in select menu
                elif self.game_status == "select_menu":
                    if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and \
                            self.new_button.collidepoint(self.mouse_position):
                        self.new_game()

                    elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and \
                            self.resume_button.collidepoint(self.mouse_position):
                        self.continue_game()

                    elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and \
                            self.quit_button.collidepoint(self.mouse_position):
                        self.running = False

                # When player is playing
                elif self.game_status == "is_playing":
                    # Show pokedex
                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_b) \
                            or (self.pokedex_button.collidepoint(self.mouse_position) and
                                event.type == pygame.MOUSEBUTTONDOWN):
                        if self.show_window == "pokedex":
                            self.show_window = False
                        else:
                            self.window_upper = self.pokedex.window
                            self.pokedex.show_pokemon(self.pokemon_appeared[0], shiny=self.pokemon.shiny)
                            self.show_window = "pokedex"
                            self.pos = [self.window.get_width() / 2 - self.window_upper.get_width() / 2,
                                        self.window.get_height() / 2 - self.window_upper.get_height() / 2]

                    # Show pokedex
                    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_n) \
                        or (self.pokedex_button.collidepoint(self.mouse_position) and
                            event.type == pygame.MOUSEBUTTONDOWN):
                        if self.show_window == "pc":
                            self.show_window = False
                        else:
                            self.window_upper = self.pc.window
                            self.show_window = "pc"
                            self.pos = [self.window.get_width() / 2 - self.window_upper.get_width() / 2,
                                        self.window.get_height() / 2 - self.window_upper.get_height() / 2]

                    # Show parameter
                    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) \
                            or (self.parameter_button.collidepoint(self.mouse_position) and
                                event.type == pygame.MOUSEBUTTONDOWN):
                        if not self.show_window:
                            self.game_status = "parameter"
                        else:
                            self.show_window = False

                    # Keyboard pressed
                    elif event.type == pygame.KEYDOWN:
                        # Reload pokemon (test action)
                        if event.key == pygame.K_SPACE:
                            self.pokemon_appeared = self.summon(self.locate)
                            self.timer = 0
                        # Change pokemon team you looking at
                        elif event.key == pygame.K_LEFT:
                            if not self.show_window:
                                self.looking_at -= 1
                                if self.looking_at == -1:
                                    self.looking_at = len(self.trainer.trainer) - 1
                            elif self.show_window == "pc":
                                self.trainer.save_pc(self.pc.page)
                                self.pc.change_page(-1)
                                self.trainer.get_player_pc(self.pc.page)
                            elif self.show_window == "pokedex":
                                self.pokedex.change_page(-1)

                        elif event.key == pygame.K_RIGHT:
                            if not self.show_window:
                                self.looking_at += 1
                                if self.looking_at >= len(self.trainer.trainer):
                                    self.looking_at = 0
                            elif self.show_window == "pc":
                                self.trainer.save_pc(self.pc.page)
                                self.pc.change_page(1)
                                self.trainer.get_player_pc(self.pc.page)
                            elif self.show_window == "pokedex":
                                self.pokedex.change_page(1)

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Catch pokemon
                        if self.pokemon.hp <= int(self.pokemon.hp_max / 5) and not self.show_window:
                            self.catch_pokemon()

                        if self.show_window == "pc":
                            for case in self.cases:
                                if case.collidepoint(self.mouse_position):
                                    if self.pc.selected != self.cases.index(case):
                                        self.pc.selected = self.cases.index(case)
                                    else:
                                        self.pc.selected = -1

                        elif not self.show_window:
                            for case in self.trainer_case:
                                if case.collidepoint(self.mouse_position):
                                    if self.trainer.selected != self.trainer_case.index(case):
                                        self.trainer.selected = self.trainer_case.index(case)
                                    else:
                                        self.trainer.selected = -1

                        if self.trainer.selected != -1:
                            for case in self.trainer_button:
                                if case.collidepoint(self.mouse_position):
                                    if self.trainer_button.index(case) == 0:
                                        pass
                                    elif self.trainer_button.index(case) == 1:
                                        shiny = True if self.trainer.trainer[self.trainer.selected][-1] == "shiny" \
                                            else False
                                        self.pokedex.show_pokemon(self.trainer.trainer[self.trainer.selected][0],
                                                                  shiny=shiny)
                                        self.show_window = "pokedex"
                                        self.pos = [self.window.get_width() / 2 - self.pokedex.window.get_width() / 2,
                                                    self.window.get_height() / 2 - self.pokedex.window.get_height() / 2]
                                    elif self.trainer_button.index(case) == 2:
                                        self.trainer.pc.append(self.trainer.trainer.pop(self.trainer.selected))
                                    self.trainer.selected = -1

                elif self.game_status == "parameter":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game_status = "is_playing"

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.parameter_button.collidepoint(self.mouse_position) \
                                or self.resume_button.collidepoint(self.mouse_position):
                            self.game_status = "is_playing"

                        elif self.save_button.collidepoint(self.mouse_position):
                            self.trainer.save_pc(self.pc.page)
                            self.trainer.save_trainer()
                            self.pokedex.save_pokedex()
                            self.chat.append([["You saved the game.", self.console]])
                            self.game_status = "is_playing"

                        elif self.quit_button.collidepoint(self.mouse_position):
                            self.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                    if self.show_fps:
                        self.show_fps = False
                    else:
                        self.show_fps = True
                if len(self.trainer_button) > 0:
                    if event.type == pygame.MOUSEBUTTONDOWN and \
                            self.trainer_button[0].collidepoint(self.mouse_position):
                        if self.show_summary:
                            self.show_summary = False
                        else:
                            self.show_summary = True

            # FPS limiter
            self.clock.tick(self.fps)
            # Update everything
            pygame.display.flip()
