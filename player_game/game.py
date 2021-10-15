import pygame
from pygame.locals import *
from utils import *
from random import randint, choice
from numpy import array
import os

pygame.init()
font = pygame.font.SysFont('arial', 25)

rat_up = load_image("spr_rat_up.png")
rat_down = load_image("spr_rat_down.png")
rat_left = load_image("spr_rat_left.png")
rat_right = load_image("spr_rat_right.png")

human_rat_up = load_image("spr_human_rat_up.png", res=(64, 64))
human_rat_down = load_image("spr_human_rat_down.png", res=(64, 64))
human_rat_left = load_image("spr_human_rat_left.png", res=(64, 64))
human_rat_right = load_image("spr_human_rat_right.png", res=(64, 64))

floor_img = load_image("spr_floor_normal.png", res=(50, 50))
wall_img = load_image("spr_tile_middle.png", res=(50, 50))
goal_img = load_image("spr_floor_goal.png", res=(50, 50))
cheese_img = load_image("spr_cheese.png", res=(50, 50))


class Rat_Game:

    def __init__(self, w=1000, h=500):
        self.width = w
        self.height = h

        # inicializa o display com a largura e altura especificada
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rat")
        self.clock = pygame.time.Clock()

        self.reset()  # inicializa o jogador e o grid

        # Dimensoes de cada celula do grid na tela
        self.rect_width = (self.width//2)//self.grid.n_cols
        self.rect_height = self.height//self.grid.n_rows

    def reset(self):
        self.player = Player(1, 1, "Player")
        self.agent = Player(0, 0, "Agent")
        self.grid = Grid(self.player, n_cols=10, n_rows=10)
        self.grid_ai = Grid(self.agent, n_cols=10, n_rows=10)

    def game_step(self):
        if self.grid.done:
            self.reset()
        if self.grid_ai.done:
            self.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:

                # Movimento do Agente
                agent_move = choice(["Up", "Down", "Left", "Right"])

                # Movimento do Jogador
                if event.key == K_DOWN:
                    self.player.move("Down", self.grid)
                    self.agent.move(agent_move, self.grid_ai)
                if event.key == K_UP:
                    self.player.move("Up", self.grid)
                    self.agent.move(agent_move, self.grid_ai)
                if event.key == K_LEFT:
                    self.player.move("Left", self.grid)
                    self.agent.move(agent_move, self.grid_ai)
                if event.key == K_RIGHT:
                    self.player.move("Right", self.grid)
                    self.agent.move(agent_move, self.grid_ai)

        # Atualiza o grid com as mudancas realizadas nesse step
        self.grid.update()
        self.grid_ai.update()
        self.draw_grid(self.screen)      # Renderiza o grid em self.screen

        pygame.display.update()
        self.clock.tick(60)

        # Retorna os dados importantes desse step
        return self.grid.done, self.player.score

    def maze_maker(self):

        maze = [[0]*self.grid.n_cols for i in range(self.grid.n_rows)]
        rat_flag = 0

        while True:
            self.screen.fill((100,100,100))
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = mouse_pos[0]//self.rect_width, mouse_pos[1]//self.rect_height

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.save_maze(maze)
                        return 0
                    
                    if event.key == K_r and rat_flag == 0 and mouse_pos[0] < self.width//2:
                        maze[mouse_x][mouse_y] = 1
                        rat_flag = 1

                    if event.key == K_DELETE and mouse_pos[0] < self.width//2:
                        if maze[mouse_x][mouse_y] == 1:
                            rat_flag = 0

                        maze[mouse_x][mouse_y] = 0


                if pygame.mouse.get_pressed()[0] and mouse_pos[0] < self.width//2:
                    maze[mouse_x][mouse_y] = 3

                elif pygame.mouse.get_pressed()[2] and mouse_pos[0] < self.width//2:
                    maze[mouse_x][mouse_y] = 4

            for x in range(0, self.grid.n_cols):
                for y in range(0, self.grid.n_rows):
                    rect = pygame.Rect(
                        x * self.rect_width,  y * self.rect_height, self.rect_width, self.rect_height)

                    self.screen.blit(floor_img, rect)
                    
                    if maze[x][y] == 1:
                        self.screen.blit(rat_up, ((x*self.rect_width) - 32 + self.rect_width //
                                             2, (y*self.rect_height)-32+self.rect_height//2))

                    if maze[x][y] == 2:
                        self.screen.blit(goal_img, rect)

                    elif maze[x][y] == 3:
                        self.screen.blit(wall_img, rect)

                    elif maze[x][y] == 4:
                        self.screen.blit(cheese_img, rect)

            draw_text("Right Mouse to place Cheese", font, (0,0,0), self.screen, 550, 50)
            draw_text("Left Mouse to place Wall", font, (0,0,0), self.screen, 550, 150)
            draw_text("R to place Rattatail", font, (0,0,0), self.screen, 550, 250)
            draw_text("Delete to remove cell content", font, (0,0,0), self.screen, 550, 350)
            draw_text("Esc to save maze and quit", font, (0,0,0), self.screen, 550, 450)

            pygame.display.update()
    
    def save_maze(self, maze):
        f = open(os.path.join(os.getcwd(),"player_game","maps", f"map_{randint(1,10000)}.txt"), "w+")
        for x in range(len(maze)):
            for y in range(len(maze[0])):
                f.write(f"{maze[x][y]}")
            if x != len(maze)-1:
                f.write("\n")
        f.close()
        
    def draw_grid(self, screen):

        for x in range(0, self.grid.n_cols):
            for y in range(0, self.grid.n_rows):
                # Posicao
                rect = pygame.Rect(
                    x * self.rect_width + 502,  y * self.rect_height, self.rect_width, self.rect_height)

                # Chao
                screen.blit(floor_img, rect)

                # Jogador
                if self.grid.grid[x][y] == 1:
                    if self.player.direction == "Up":
                        screen.blit(human_rat_up, ((x*self.rect_width + 502) - 32 + self.rect_width //
                                                   2, (y*self.rect_height)-32+self.rect_height//2))
                    elif self.player.direction == "Down":
                        screen.blit(human_rat_down, ((x*self.rect_width + 502) - 32 + self.rect_width //
                                                     2, (y*self.rect_height)-32+self.rect_height//2))
                    elif self.player.direction == "Right":
                        screen.blit(human_rat_right, ((x*self.rect_width + 502) - 32 + self.rect_width //
                                                      2, (y*self.rect_height)-32+self.rect_height//2))
                    else:
                        screen.blit(human_rat_left, ((x*self.rect_width + 502) - 32 + self.rect_width //
                                                     2, (y*self.rect_height)-32+self.rect_height//2))

                # Objetivo
                elif self.grid.grid[x][y] == 2:
                    self.screen.blit(goal_img, rect)

                # Parede
                elif self.grid.grid[x][y] == 3:
                    self.screen.blit(wall_img, rect)
                # Queijo
                elif self.grid.grid[x][y] == 4:
                    self.screen.blit(cheese_img, rect)

        for x in range(0, self.grid_ai.n_cols):
            for y in range(0, self.grid_ai.n_rows):
                # Posicao
                rect = pygame.Rect(
                    x * self.rect_width,  y * self.rect_height, self.rect_width, self.rect_height)

                # Chao
                screen.blit(floor_img, rect)

                # Agente
                if self.grid_ai.grid[x][y] == 10:
                    if self.agent.direction == "Up":
                        screen.blit(rat_up, ((x*self.rect_width) - 32 + self.rect_width //
                                             2, (y*self.rect_height)-32+self.rect_height//2))
                    elif self.agent.direction == "Down":
                        screen.blit(rat_down, ((x*self.rect_width) - 32 + self.rect_width //
                                               2, (y*self.rect_height)-32+self.rect_height//2))
                    elif self.agent.direction == "Right":
                        screen.blit(rat_right, ((x*self.rect_width) - 32 + self.rect_width //
                                                2, (y*self.rect_height)-32+self.rect_height//2))
                    else:
                        screen.blit(rat_left, ((x*self.rect_width) - 32 + self.rect_width //
                                               2, (y*self.rect_height)-32+self.rect_height//2))

                # Objetivo
                elif self.grid_ai.grid[x][y] == 2:
                    self.screen.blit(goal_img, rect)

                # Parede
                elif self.grid_ai.grid[x][y] == 3:
                    self.screen.blit(wall_img, rect)
                # Queijo
                elif self.grid_ai.grid[x][y] == 4:
                    self.screen.blit(cheese_img, rect)

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
            self.width//2 - 4, 0, 8, self.height))


class Player:

    def __init__(self, x, y, name):
        # Atual posicao no grid
        self.name = name
        self.x = x
        self.y = y

        self.direction = "Right"

        self.reward_amount = 20

        self.score = 0

    def move(self, direction, grid):

        if direction == "Up":
            self.direction = "Up"
            if grid.is_valid_position(self.x, self.y - 1):
                grid.clear_position(self.x, self.y)
                self.y -= 1
        if direction == "Down":
            self.direction = "Down"
            if grid.is_valid_position(self.x, self.y + 1):
                grid.clear_position(self.x, self.y)
                self.y += 1
        if direction == "Left":
            self.direction = "Left"
            if grid.is_valid_position(self.x-1, self.y):
                grid.clear_position(self.x, self.y)
                self.x -= 1
        if direction == "Right":
            self.direction = "Right"
            if grid.is_valid_position(self.x+1, self.y):
                grid.clear_position(self.x, self.y)
                self.x += 1


class Grid:

    """

    Aqui e armazenado todo o estado do jogo. Esta classe recebe uma instancia de Player em sua inicializacao.

    O estado do jogo e representado em uma matriz NxM, de forma que seus elementos representem diferentes entidades do jogo.
    Esta forma de representacao nos permite adicionar novas entidades arbitrariamente com relativa facilidade.

    1 -> Representa o jogador
    2 -> Representa o objetivo
    3 -> Representa um obstaculo
    4 -> Queijo

    Exemplo:

    Um grid onde o jogador está no canto superior esquerdo mas não consegue alcançar o objetivo, pois esta cercado de obstaculos.

    [1,0,3,0]
    [0,0,3,0]
    [3,3,3,0]
    [0,0,0,2]

    """

    def __init__(self, player, n_rows=10, n_cols=10, screen_width=1000, screen_height=500):

        self.player = player

        # Dimensoes do grid
        self.n_cols = n_cols
        self.n_rows = n_rows

        # Dimensoes da tela, importante para renderizar o grid.
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.done = False   # Variavel que determina se o jogo acabou

        self.grid = array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 3, 3, 3, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 3, 3, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0, 3, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 0, 0, 0],
                           [0, 0, 3, 0, 0, 0, 3, 3, 0, 0]]).T

        # Posicao do objetivo
        self.goal_x = randint(0, n_cols-1)
        self.goal_y = randint(0, n_rows-1)

        while self.grid[self.goal_x][self.goal_y] != 2:
            if self.grid[self.goal_x][self.goal_y] == 0:
                # Popula a posicao do objetivo com um objetivo
                self.grid[self.goal_x][self.goal_y] = 2
            else:
                self.goal_x = randint(0, n_cols-1)
                self.goal_y = randint(0, n_rows-1)

        # Posicoes dos queijos
        self.cheeses_x = []
        self.cheeses_y = []

        for i in range(5):
            cheese_x = randint(0, n_cols-1)
            cheese_y = randint(0, n_rows-1)
            while self.grid[cheese_x][cheese_y] != 4:
                if self.grid[cheese_x][cheese_y] == 0:
                    self.grid[cheese_x][cheese_y] = 4
                else:
                    cheese_x = randint(0, n_cols-1)
                    cheese_y = randint(0, n_rows-1)
            self.cheeses_x.append(cheese_x)
            self.cheeses_y.append(cheese_y)

    def is_valid_position(self, x, y):
        """Checa se a posicao atual esta populada com um obstaculo ou esta out of bounds"""
        if (x > self.n_cols-1 or y > self.n_rows-1) or (x < 0 or y < 0):
            return False

        elif self.grid[x][y] == 3:
            return False

        return True

    def update(self):
        """Atualiza o grid com as mudancas de estado realizadas."""

        # Checa se o jogador ou agente chegaram no objetivo
        if self.grid[self.player.x][self.player.y] == 2:
            self.player.score += self.player.reward_amount
            self.done = True

        # Checa se o jogador ou agente comeram o queijo
        elif self.grid[self.player.x][self.player.y] == 4:
            self.player.score += 1
            self.clear_position(self.player.x, self.player.y)

        # Popule a atual posicao do jogador com 1 e a do agente com 10
        if self.player.name == "Player":
            self.grid[self.player.x][self.player.y] = 1
        elif self.player.name == "Agent":
            self.grid[self.player.x][self.player.y] = 10

    def clear_position(self, x, y):
        self.grid[x][y] = 0

    def clear_player_position(self):
        self.grid[self.player.x][self.player.y] = 0

if __name__ == "__main__":
    game = Rat_Game()
    mode_selection = main_menu(game.screen)

    if mode_selection == 0:    # Maze maker
        game.maze_maker()
    elif mode_selection == 1:  # Player vs AI
        while True:
            game.game_step()