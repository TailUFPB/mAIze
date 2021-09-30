import pygame
from pygame.locals import *
from random import randint
from utils import *

pygame.init()
font = pygame.font.SysFont('arial', 25)

rat_up = load_image("spr_rat_up.png")
rat_down = load_image("spr_rat_down.png")
rat_left = load_image("spr_rat_left.png")
rat_right = load_image("spr_rat_right.png")

floor_img = load_image("spr_floor_normal.png", res = (50,50))
wall_img = load_image("spr_tile_middle.png", res = (50,50))
goal_img = load_image("spr_floor_goal.png", res = (50,50))
cheese_img = load_image("spr_cheese.png", res = (50,50))

class Rat_Game:

    """

    Autor: Moisés Filipe
    Descrição: Classe principal que contem o comportamento do jogo.
    
    """

    def __init__(self, w=500, h=500):
        self.width = w
        self.height = h

        self.screen = pygame.display.set_mode((self.width, self.height)) # inicializa o display com a largura e altura especificada
        pygame.display.set_caption("Rat")
        self.clock = pygame.time.Clock()

        self.reset() # inicializa o jogador e o grid

        self.rect_width = self.width//self.grid.n_cols
        self.rect_height = self.height//self.grid.n_rows

    def reset(self):
        self.player = Player()
        self.grid = Grid(self.player, n_cols = 10, n_rows = 10)

    def game_step(self):
        if self.grid.done:
            self.reset() 

        text = font.render("Score: " + str(self.player.score), True, (0,0,0))   # Salva o score a ser exibido
        self.screen.blit(text, [0, 0])                                          # Renderiza o score no canto superior esquerdo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type ==  KEYDOWN:
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

        return self.grid.done, self.player.score # Retorna os dados importantes desse step
    
    def draw_grid(self, screen):
        for x in range(0, self.grid.n_cols):
            for y in range(0, self.grid.n_rows):
                rect = pygame.Rect(x * self.rect_width,  y * self.rect_height, self.rect_width, self.rect_height)
                screen.blit(floor_img, rect)
                if self.grid.grid[x][y] == 1:
                    if self.player.direction == "Up":
                        screen.blit(rat_up, ((x*self.rect_width) - 32 + self.rect_width//2, (y*self.rect_height)-32+self.rect_height//2))
                    elif self.player.direction == "Down":
                        screen.blit(rat_down, ((x*self.rect_width) - 32 + self.rect_width//2, (y*self.rect_height)-32+self.rect_height//2))
                    elif self.player.direction == "Right":
                        screen.blit(rat_right, ((x*self.rect_width) - 32 + self.rect_width//2, (y*self.rect_height)-32+self.rect_height//2))
                    else:
                        screen.blit(rat_left, ((x*self.rect_width) - 32 + self.rect_width//2, (y*self.rect_height)-32+self.rect_height//2))
                elif self.grid.grid[x][y] == 2:
                    self.screen.blit(goal_img, rect)
                elif self.grid.grid[x][y] == 3:
                    self.screen.blit(wall_img, rect)
                elif self.grid.grid[x][y] == 4:
                    self.screen.blit(cheese_img, rect)

class Player:
    
    def __init__(self):
        # Atual posicao no grid
        self.x = 1
        self.y = 1

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
    
    def __init__(self, player, n_rows = 10, n_cols = 10, screen_width = 500, screen_height = 500):

        self.player = player

        # Dimensoes do grid
        self.n_cols = n_cols
        self.n_rows = n_rows
        
        # Dimensoes da tela, importante para renderizar o grid.
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.done = False   # Variavel que determina se o jogo acabou

        self.grid = [[0]*n_cols for i in range(n_rows)] # Matriz que representa o grid.
        
        # Posicao do objetivo
        self.goal_x = randint(0, n_cols-1)
        self.goal_y = randint(0, n_rows-1)

        while self.grid[self.goal_x][self.goal_y] != 2:
            if self.grid[self.goal_x][self.goal_y] == 0:
                self.grid[self.goal_x][self.goal_y] = 2 # Popula a posicao do objetivo com um objetivo
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
        if self.grid[self.player.x][self.player.y] == 2:   # Se a posicao do jogador eh a mesma do objetivo
            self.player.score += self.player.reward_amount # Some a recompensa ao score
            self.done = True                               # Jogo encerrado
        elif self.grid[self.player.x][self.player.y] == 4:
            self.player.score += 1
            self.clear_player_position()

        self.grid[self.player.x][self.player.y] = 1 # Popule a atual posicao do jogador com 1

    def clear_position(self, x, y):
        self.grid[x][y] = 0
    
    def clear_player_position(self):
        self.grid[self.player.x][self.player.y] = 0


if __name__ == "__main__":
    game = Rat_Game()
    main_menu(game.screen)
    while True:
        game.game_step()