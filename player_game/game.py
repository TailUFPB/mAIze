import pygame
from pygame.locals import *
from random import randint, choice
from numpy import array
from utils import *

pygame.init()
font = pygame.font.SysFont('arial', 25)

rat_up = load_image("spr_rat_up.png")
rat_down = load_image("spr_rat_down.png")
rat_left = load_image("spr_rat_left.png")
rat_right = load_image("spr_rat_right.png")

human_rat_up = load_image("spr_human_rat_up.png", res=(64,64))
human_rat_down = load_image("spr_human_rat_down.png", res=(64,64))
human_rat_left = load_image("spr_human_rat_left.png", res=(64,64))
human_rat_right = load_image("spr_human_rat_right.png", res=(64,64))

floor_img = load_image("spr_floor_normal.png", res=(50, 50))
wall_img = load_image("spr_tile_middle.png", res=(50, 50))
goal_img = load_image("spr_floor_goal.png", res=(50, 50))
cheese_img = load_image("spr_cheese.png", res=(50, 50))


class Rat_Game:

    def __init__(self, w=500, h=500):
        self.width = w
        self.height = h

        # inicializa o display com a largura e altura especificada
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rat")
        self.clock = pygame.time.Clock()

        self.reset()  # inicializa o jogador e o grid

        # Dimensoes de cada celula do grid na tela
        self.rect_width = self.width//self.grid.n_cols
        self.rect_height = self.height//self.grid.n_rows

    def reset(self):
        self.player = Player(1,1)
        self.agent = Player(0, 0)
        self.grid = Grid(self.player, self.agent, n_cols=10, n_rows=10)

    def game_step(self):
        if self.grid.done:
            self.reset()

        text = font.render("Score: " + str(self.player.score),
                           True, (0, 0, 0))   # Salva o score a ser exibido
        # Renderiza o score no canto superior esquerdo
        self.screen.blit(text, [0, 0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:

                # Movimento do Agente
                agent_move = choice(["Up", "Down", "Left", "Right"])
                if agent_move == "Up":
                    if self.grid.is_valid_position(self.agent.x, self.agent.y - 1):
                        self.grid.clear_position(self.agent.x, self.agent.y)
                        self.agent.direction = "Up"
                        self.agent.move("Up")
                if agent_move == "Down":
                    if self.grid.is_valid_position(self.agent.x, self.agent.y + 1):
                        self.grid.clear_position(self.agent.x, self.agent.y)
                        self.agent.direction = "Down"
                        self.agent.move("Down")
                if agent_move == "Left":
                    if self.grid.is_valid_position(self.agent.x - 1, self.agent.y):
                        self.grid.clear_position(self.agent.x, self.agent.y)
                        self.agent.direction = "Left"
                        self.agent.move("Left")
                if agent_move == "Right":
                    if self.grid.is_valid_position(self.agent.x + 1, self.agent.y):
                        self.grid.clear_position(self.agent.x, self.agent.y)
                        self.agent.direction = "Right"
                        self.agent.move("Right")

                # Movimento do Jogador
                if event.key == K_DOWN:
                    if self.grid.is_valid_position(self.player.x, self.player.y + 1):
                        self.grid.clear_player_position()
                        self.player.direction = "Down"
                        self.player.move("Down")
                if event.key == K_UP:
                    if self.grid.is_valid_position(self.player.x, self.player.y - 1):
                        self.grid.clear_player_position()
                        self.player.direction = "Up"
                        self.player.move("Up")
                if event.key == K_LEFT:
                    if self.grid.is_valid_position(self.player.x - 1, self.player.y):
                        self.grid.clear_player_position()
                        self.player.direction = "Left"
                        self.player.move("Left")
                if event.key == K_RIGHT:
                    if self.grid.is_valid_position(self.player.x + 1, self.player.y):
                        self.grid.clear_player_position()
                        self.player.direction = "Right"
                        self.player.move("Right")

        self.grid.update()               # Atualiza o grid com as mudancas realizadas nesse step
        self.draw_grid(self.screen)      # Renderiza o grid em self.screen

        pygame.display.update()
        self.clock.tick(60)

        # Retorna os dados importantes desse step
        return self.grid.done, self.player.score

    def draw_grid(self, screen):
        for x in range(0, self.grid.n_cols):
            for y in range(0, self.grid.n_rows):
                # Posicao
                rect = pygame.Rect(
                    x * self.rect_width,  y * self.rect_height, self.rect_width, self.rect_height)
                
                # Chao
                screen.blit(floor_img, rect)

                # Jogador
                if self.grid.grid[x][y] == 1:
                    if self.player.direction == "Up":
                        screen.blit(rat_up, ((x*self.rect_width) - 32 + self.rect_width //
                                             2, (y*self.rect_height)-32+self.rect_height//2))
                    elif self.player.direction == "Down":
                        screen.blit(rat_down, ((x*self.rect_width) - 32 + self.rect_width //
                                               2, (y*self.rect_height)-32+self.rect_height//2))
                    elif self.player.direction == "Right":
                        screen.blit(rat_right, ((x*self.rect_width) - 32 + self.rect_width //
                                                2, (y*self.rect_height)-32+self.rect_height//2))
                    else:
                        screen.blit(rat_left, ((x*self.rect_width) - 32 + self.rect_width //
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

                # Agente
                elif self.grid.grid[x][y] == 10:
                    if self.agent.direction == "Up":
                        screen.blit(human_rat_up, ((x*self.rect_width) - 32 + self.rect_width //
                                             2, (y*self.rect_height)-32+self.rect_height//2))
                    elif self.agent.direction == "Down":
                        screen.blit(human_rat_down, ((x*self.rect_width) - 32 + self.rect_width //
                                               2, (y*self.rect_height)-32+self.rect_height//2))
                    elif self.agent.direction == "Right":
                        screen.blit(human_rat_right, ((x*self.rect_width) - 32 + self.rect_width //
                                                2, (y*self.rect_height)-32+self.rect_height//2))
                    else:
                        screen.blit(human_rat_left, ((x*self.rect_width) - 32 + self.rect_width //
                                               2, (y*self.rect_height)-32+self.rect_height//2))

class Player:

    def __init__(self, x, y):
        # Atual posicao no grid
        self.x = x
        self.y = y

        self.direction = "Right"

        self.reward_amount = 20

        self.score = 0

    def move(self, direction):
        if direction == "Right":
            self.x += 1

        elif direction == "Left":
            self.x -= 1

        elif direction == "Down":
            self.y += 1

        elif direction == "Up":
            self.y -= 1


class Grid:

    """

    Aqui e armazenado todo o estado do jogo. Esta classe recebe uma instancia de Player em sua inicializacao.

    O estado do jogo e representado em uma matriz NxM, de forma que seus elementos representem diferentes entidades do jogo.
    Esta forma de representacao nos permite adicionar novas entidades arbitrariamente com relativa facilidade.

    1 -> Representa o jogador
    2 -> Representa o objetivo
    3 -> Representa um obstaculo
    TODO: 4 -> Queijo

    Exemplo:

    Um grid onde o jogador está no canto superior esquerdo mas não consegue alcançar o objetivo, pois esta cercado de obstaculos.

    [1,0,3,0]
    [0,0,3,0]
    [3,3,3,0]
    [0,0,0,2]

    """

    def __init__(self, player, agent, n_rows=10, n_cols=10, screen_width=500, screen_height=500):

        self.player = player
        self.agent = agent

        # Dimensoes do grid
        self.n_cols = n_cols
        self.n_rows = n_rows

        # Dimensoes da tela, importante para renderizar o grid.
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.done = False   # Variavel que determina se o jogo acabou

        # self.grid = [[0]*n_cols for i in range(n_rows)] # Matriz que representa o grid.
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
        
        elif self.grid[self.agent.x][self.agent.y] == 2:
            self.agent.score += self.agent.reward_amount
            self.done = True
        
        # Checa se o jogador ou agente comeram o queijo
        elif self.grid[self.player.x][self.player.y] == 4:
            self.player.score += 1
            self.clear_position(self.player.x, self.player.y)
        
        elif self.grid[self.agent.x][self.agent.y] == 4:
            self.agent.score += 1
            self.clear_position(self.agent.x, self.agent.y)


        # Popule a atual posicao do jogador com 1 e a do agente com 10
        self.grid[self.player.x][self.player.y] = 1
        self.grid[self.agent.x][self.agent.y] = 10

    def clear_position(self, x, y):
        self.grid[x][y] = 0

    def clear_player_position(self):
        self.grid[self.player.x][self.player.y] = 0


if __name__ == "__main__":
    game = Rat_Game()
    main_menu(game.screen)
    while True:
        game.game_step()
