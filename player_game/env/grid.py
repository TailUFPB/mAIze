from numpy import array
from random import randint, random
from player import Player

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

    def __init__(self, player, n_rows=10, n_cols=10, screen_width=1000, screen_height=500, grid = []):


        # Dimensoes do grid
        self.player = player
        self.n_cols = n_cols
        self.n_rows = n_rows

        #self.trap_hole = True

        # Dimensoes da tela, importante para renderizar o grid.
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.done = False   # Variavel que determina se o jogo acabou

        self.maps = [array([[1, 0, 0, 0, 3, 0, 4, 0, 0, 0],
                           [3, 3, 3, 0, 3, 0, 3, 3, 3, 4],
                           [0, 0, 0, 0, 3, 0, 3, 0, 3, 0],
                           [3, 3, 3, 0, 0, 0, 0, 0, 3, 0],
                           [0, 3, 0, 0, 4, 4, 3, 3, 0, 0],
                           [0, 0, 0, 0, 3, 3, 3, 0, 3, 0],
                           [0, 3, 0, 0, 0, 0, 0, 0, 3, 0],
                           [3, 3, 0, 3, 3, 0, 3, 0, 3, 0],
                           [0, 3, 0, 0, 0, 0, 3, 0, 4, 0],
                           [0, 3, 3, 0, 0, 0, 3, 0, 0, 2]]).T,

                    array([[1, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                           [3, 3, 3, 0, 3, 3, 3, 3, 3, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                           [0, 3, 0, 3, 3, 0, 3, 0, 0, 0],
                           [0, 3, 0, 0, 0, 0, 3, 3, 0, 0],
                           [0, 3, 0, 0, 3, 3, 0, 0, 3, 0],
                           [0, 3, 3, 4, 4, 0, 0, 0, 3, 0],
                           [0, 0, 0, 3, 3, 0, 3, 0, 3, 0],
                           [0, 3, 0, 0, 0, 0, 3, 0, 4, 0],
                           [4, 3, 3, 0, 4, 0, 3, 0, 0, 2]]).T,

                    array([[1, 0, 0, 0, 3, 0, 0, 0, 4, 0],
                           [3, 3, 0, 0, 3, 0, 3, 3, 4, 0],
                           [0, 0, 0, 4, 3, 0, 3, 3, 3, 0],
                           [0, 3, 0, 3, 3, 0, 3, 0, 4, 0],
                           [0, 3, 0, 0, 0, 0, 3, 3, 0, 0],
                           [0, 3, 0, 0, 3, 3, 0, 0, 0, 0],
                           [0, 3, 3, 4, 0, 0, 0, 0, 3, 0],
                           [0, 0, 0, 3, 3, 0, 3, 0, 3, 0],
                           [3, 3, 0, 0, 0, 0, 3, 0, 0, 0],
                           [3, 3, 3, 0, 0, 0, 0, 0, 0, 2]]).T,
                           
                    array([[1, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                           [3, 3, 0, 0, 3, 3, 3, 0, 3, 0],
                           [3, 3, 3, 0, 0, 0, 0, 0, 3, 0],
                           [3, 0, 0, 3, 3, 0, 3, 0, 0, 0],
                           [3, 3, 0, 0, 0, 0, 3, 3, 0, 0],
                           [3, 0, 0, 0, 3, 3, 0, 0, 3, 3],
                           [3, 0, 3, 4, 4, 0, 0, 0, 3, 0],
                           [3, 3, 0, 3, 3, 0, 3, 0, 3, 0],
                           [3, 0, 0, 0, 0, 0, 3, 0, 4, 0],
                           [3, 3, 3, 3, 4, 0, 3, 3, 0, 2]]).T,
                           
                    array([[1, 3, 3, 4, 3, 0, 0, 0, 0, 3],
                           [0, 3, 3, 0, 3, 0, 3, 3, 0, 0],
                           [0, 0, 0, 0, 3, 3, 0, 0, 3, 0],
                           [0, 3, 3, 3, 3, 4, 3, 0, 0, 0],
                           [0, 0, 0, 0, 3, 0, 3, 3, 0, 0],
                           [0, 3, 3, 0, 3, 0, 0, 0, 3, 0],
                           [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
                           [0, 3, 0, 3, 0, 3, 3, 0, 3, 0],
                           [0, 3, 3, 0, 0, 3, 3, 0, 0, 3],
                           [0, 0, 4, 3, 0, 0, 4, 3, 0, 2]]).T,
                           
                    array([[1, 3, 3, 0, 0, 0, 0, 0, 0, 3],
                            [0, 3, 0, 3, 3, 0, 3, 0, 3, 0],
                            [0, 0, 0, 3, 0, 0, 3, 0, 3, 0],
                            [0, 3, 0, 3, 0, 3, 3, 0, 3, 0],
                            [0, 3, 3, 0, 0, 0, 3, 3, 0, 4],
                            [0, 3, 0, 0, 3, 0, 0, 0, 0, 0],
                            [0, 3, 3, 4, 0, 3, 0, 0, 3, 0],
                            [0, 4, 0, 3, 3, 0, 3, 0, 3, 0],
                            [3, 3, 0, 3, 0, 0, 3, 0, 0, 0],
                            [4, 0, 0, 0, 0, 0, 0, 0, 4, 2]]).T]

        '''self.grid = self.maps[randint(0, 5)]

        flag = 0

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 1:
                    self.player = Player(i,j,'Agent')
                    flag = 1
                    break
            if flag:
                break'''

        self.cheeses_x = []
        self.cheeses_y = []

        self.holes_x = []
        self.holes_y = []

        self.grid = grid

        self.populate_lists()

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
        #self.trapped = False
        #self.trap_hole = not self.trap_hole

        for i in range(len(self.holes_x)):
            if self.grid[self.holes_x[i]][self.holes_y[i]] != 1:
                self.grid[self.holes_x[i]][self.holes_y[i]] = 5

        # Checa se o jogador ou agente chegaram no objetivo
        if self.grid[self.player.x][self.player.y] == 2:
            self.player.score += self.player.reward_amount
            self.done = True

        # Checa se o jogador ou agente comeram o queijo
        elif self.grid[self.player.x][self.player.y] == 4:
            #self.player.score += 1
            self.player.eaten_cheese = True
            self.clear_position(self.player.x, self.player.y)

        '''elif self.grid[self.player.x][self.player.y] == 5 and self.trap_hole == True:
            #self.player.x, self.player.y = self.player.initial_x, self.player.initial_y
            self.trapped = True'''


        # Popule a atual posicao do jogador com 1 e a do agente com 10
        if self.player.name == "Player":
            self.grid[self.player.x][self.player.y] = 1
        elif self.player.name == "Agent":
            self.grid[self.player.x][self.player.y] = 1

    def clear_position(self, x, y):
        self.grid[x][y] = 0

    def clear_player_position(self):
        self.grid[self.player.x][self.player.y] = 0

    def populate_lists(self):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 5:
                    self.holes_x.append(i)
                    self.holes_y.append(j)
                elif self.grid[i][j] == 4:
                    self.cheeses_x.append(i)
                    self.cheeses_y.append(j)
