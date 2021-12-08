from numpy import array
from random import randint, random

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

        self.maps = [array([[0, 0, 0, 0, 3, 0, 4, 0, 0, 0],
                           [3, 3, 3, 0, 3, 0, 3, 3, 3, 4],
                           [0, 0, 0, 0, 3, 0, 3, 0, 3, 0],
                           [3, 3, 3, 0, 0, 0, 0, 0, 3, 0],
                           [0, 3, 0, 0, 4, 4, 3, 3, 0, 0],
                           [0, 0, 0, 0, 3, 3, 3, 0, 3, 0],
                           [0, 3, 0, 0, 0, 0, 0, 0, 3, 0],
                           [3, 3, 0, 3, 3, 0, 3, 0, 3, 0],
                           [0, 3, 0, 0, 0, 0, 3, 0, 4, 0],
                           [0, 3, 3, 0, 0, 0, 3, 0, 0, 3]]).T,

                    array([[0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                           [3, 3, 3, 0, 3, 3, 3, 3, 3, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                           [0, 3, 0, 3, 3, 0, 3, 0, 0, 0],
                           [0, 3, 0, 0, 0, 0, 3, 3, 0, 0],
                           [0, 3, 0, 0, 3, 3, 0, 0, 3, 0],
                           [0, 3, 3, 4, 4, 0, 0, 0, 3, 0],
                           [0, 0, 0, 3, 3, 0, 3, 0, 3, 0],
                           [0, 3, 0, 0, 0, 0, 3, 0, 4, 0],
                           [4, 3, 3, 0, 4, 0, 3, 0, 0, 3]]).T,

                    array([[0, 0, 0, 0, 3, 0, 0, 0, 4, 0],
                           [3, 3, 0, 0, 3, 0, 3, 3, 4, 0],
                           [0, 0, 0, 4, 3, 0, 3, 3, 3, 0],
                           [0, 3, 0, 3, 3, 0, 3, 0, 4, 0],
                           [0, 3, 0, 0, 0, 0, 3, 3, 0, 0],
                           [0, 3, 0, 0, 3, 3, 0, 0, 0, 0],
                           [0, 3, 3, 4, 0, 0, 0, 0, 3, 0],
                           [0, 0, 0, 3, 3, 0, 3, 0, 3, 0],
                           [3, 3, 0, 0, 0, 0, 3, 0, 0, 0],
                           [3, 3, 3, 0, 0, 0, 0, 0, 0, 3]]).T,
                           
                    array([[3, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                           [3, 3, 0, 0, 3, 3, 3, 0, 3, 0],
                           [3, 3, 3, 0, 0, 0, 0, 0, 3, 0],
                           [3, 0, 0, 3, 3, 0, 3, 0, 0, 0],
                           [3, 3, 0, 0, 0, 0, 3, 3, 0, 0],
                           [3, 0, 0, 0, 3, 3, 0, 0, 3, 3],
                           [3, 0, 3, 4, 4, 0, 0, 0, 3, 0],
                           [3, 3, 0, 3, 3, 0, 3, 0, 3, 0],
                           [3, 0, 0, 0, 0, 0, 3, 0, 4, 0],
                           [3, 3, 3, 3, 4, 0, 3, 3, 0, 3]]).T,]

        #self.grid = self.maps[randint(0, 3)]

        self.grid = array([[0, 3, 3, 4, 3, 0, 0, 0, 0, 3],
                           [0, 3, 3, 0, 3, 0, 3, 3, 0, 0],
                           [0, 0, 0, 0, 3, 3, 0, 0, 3, 0],
                           [0, 3, 3, 3, 3, 4, 3, 0, 0, 0],
                           [0, 0, 0, 0, 3, 0, 3, 3, 0, 0],
                           [0, 3, 3, 0, 3, 0, 0, 0, 3, 0],
                           [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
                           [0, 3, 0, 3, 0, 3, 3, 0, 3, 0],
                           [0, 3, 3, 0, 0, 3, 3, 0, 0, 3],
                           [0, 0, 4, 3, 0, 0, 4, 3, 0, 4]]).T


        # Posicao do objetivo
        self.goal_x = 5 #randint(0, n_cols-1)
        self.goal_y = 0 #randint(0, n_rows-1)

        while self.grid[self.goal_x][self.goal_y] != 2:
            if self.grid[self.goal_x][self.goal_y] == 0:
                # Popula a posicao do objetivo com um objetivo
                self.grid[self.goal_x][self.goal_y] = 2
            else:
                self.goal_x = randint(0, n_cols-1)
                self.goal_y = randint(0, n_rows-1)

        self.cheeses_x = [0,4,5,7,3]
        self.cheeses_y = [9,4,4,9,9]

        '''for i in range(5):
            cheese_x = randint(0, n_cols-1)
            cheese_y = randint(0, n_rows-1)
            while self.grid[cheese_x][cheese_y] != 4:
                if self.grid[cheese_x][cheese_y] == 0:
                    self.grid[cheese_x][cheese_y] = 4
                else:
                    cheese_x = randint(0, n_cols-1)
                    cheese_y = randint(0, n_rows-1)
            self.cheeses_x.append(cheese_x)
            self.cheeses_y.append(cheese_y)'''

        # Posicoes dos queijos
        # self.cheeses_x = []
        # self.cheeses_y = []

        # for i in range(5):
        #     cheese_x = randint(0, n_cols-1)
        #     cheese_y = randint(0, n_rows-1)
        #     while self.grid[cheese_x][cheese_y] != 4:
        #         if self.grid[cheese_x][cheese_y] == 0:
        #             self.grid[cheese_x][cheese_y] = 4
        #         else:
        #             cheese_x = randint(0, n_cols-1)
        #             cheese_y = randint(0, n_rows-1)
        #     self.cheeses_x.append(cheese_x)
        #     self.cheeses_y.append(cheese_y)

    def is_valid_position(self, x, y):
        """Checa se a posicao atual esta populada com um obstaculo ou esta out of bounds"""
        if (x > self.n_cols-1 or y > self.n_rows-1) or (x < 0 or y < 0):
            return False

        elif self.grid[x][y] == 3:
            return False

        return True

    def update(self):
        """Atualiza o grid com as mudancas de estado realizadas."""
        self.player.eaten_cheese = False
        # Checa se o jogador ou agente chegaram no objetivo
        if self.grid[self.player.x][self.player.y] == 2:
            self.player.score += self.player.reward_amount
            self.done = True

        # Checa se o jogador ou agente comeram o queijo
        elif self.grid[self.player.x][self.player.y] == 4:
            self.player.score += 0.2
            self.player.eaten_cheese = True
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
