import pygame
from statistics import pvariance
from player import Player
from grid import Grid
from pygame.locals import *
from utils import *
from random import randint, choice
from numpy import array
import numpy as np
import gym
import math
import pickle
import time
import plot
#from rat_game_env import Maze_agent
import os


pygame.init()
font = pygame.font.SysFont('arial', 25)

def select_game_skin(skin):
    global rat_up 
    global rat_down 
    global rat_left
    global rat_right

    if skin == 0:
        rat_up = load_image("spr_rat_up.png")
        rat_down = load_image("spr_rat_down.png")
        rat_left = load_image("spr_rat_left.png")
        rat_right = load_image("spr_rat_right.png")
    elif skin == 1:
        rat_up = load_image("spr_remy_up.png")
        rat_down = load_image("spr_remy_down.png")
        rat_left = load_image("spr_remy_left.png")
        rat_right = load_image("spr_remy_right.png")
    elif skin == 2:
        rat_up = load_image("spr_cachorro_down.PNG")
        rat_down = load_image("spr_cachorro_down.PNG")
        rat_left = load_image("spr_cachorro_down.PNG")
        rat_right = load_image("spr_cachorro_down.PNG")
    return 0

human_rat_up = load_image("spr_human_rat_up.png", res=(64, 64))
human_rat_down = load_image("spr_human_rat_down.png", res=(64, 64))
human_rat_left = load_image("spr_human_rat_left.png", res=(64, 64))
human_rat_right = load_image("spr_human_rat_right.png", res=(64, 64))

mm_inst = load_image("maze_maker_inst.png", res=(500, 500))

RAT_IMG = load_image('spr_rat_up.png')

EPISODES = 10000
RENDER_EPISODE = 50
EPSILON_MINIMUM = 0.001
DECAY = np.prod((10, 10), dtype=float) / 20 #Decay era / 2
LEARNING_RATE_MINIMUM = 0.2
DISCOUNT = 0.99

floor_img = load_image("spr_floor_normal.png", res=(50, 50))
wall_img = load_image("spr_tile_middle.png", res=(50, 50))
goal_img = load_image("spr_floor_goal.png", res=(50, 50))
cheese_img = load_image("spr_cheese.png", res=(50, 50))
fire_img = load_image("spr_fire.png", res=(50,50))
trap_closed_img = load_image("spr_floor_trap.png", res=(50,50))
trap_open_img = load_image("spr_floor_trap_open.png", res=(50,50))

class Rat_Game_Gym(gym.Env):
    def __init__(self,grid,screen):
        self.iteration = -1
        self.curr_step = -1
        self.grid = grid
        self.initial_x, self.initial_y = self.find_initial_pos(self.grid)
        self._reset()
        self.screen = screen
        pygame.display.set_caption("Rar_Game_Env")
        self.clock = pygame.time.Clock()

    def step(self, action):

        self.curr_step += 1
        self._take_action(action)
        self.maze.update()

        reward = self._get_reward()
        ob = self._get_state()
        return ob, reward, self.maze.done

    def _reset(self):
        self.agent = Player(self.initial_x, self.initial_y, "Agent")
        grid = []
        for x in range(10):
            grid.append([])
            for y in range(10):
                grid[x].append(self.grid[x][y])
        self.maze = Grid(self.agent, n_cols=10, n_rows=10, grid=grid)

        self.number_cheese = min(len(self.maze.cheeses_x), 5)
        self.iteration += 1
        self.curr_step = 0

        return self._get_state()

    def object_draw(self, pos, rect):
        #Objetivo
        if pos == 2:
            self.screen.blit(goal_img, rect)

        # Parede
        elif pos == 3:
            self.screen.blit(wall_img, rect)
        # Queijo
        elif pos == 4:
            self.screen.blit(cheese_img, rect)

        # Armadilha 1
        '''elif pos == 5:
            if trap_hole:
                self.screen.blit(trap_open_img, rect)
            else:
                self.screen.blit(trap_closed_img, rect)'''

    def _render(self, screen):


        for x in range(0, self.maze.n_cols):
            for y in range(0, self.maze.n_rows):
                # Posicao
                rect = pygame.Rect(
                    x * 50,  y * 50, 50, 50)

                # Chao
                screen.blit(floor_img, rect)

                # Agente
                if self.maze.grid[x][y] == 1:
                    if self.agent.direction == "Up":
                        screen.blit(rat_up, ((x*50) - 32 + 50 //
                                                2, (y*50)-32+50//2))
                    elif self.agent.direction == "Down":
                        screen.blit(rat_down, ((x*50) - 32 + 50 //
                                                2, (y*50)-32+50//2))
                    elif self.agent.direction == "Right":
                        screen.blit(rat_right, ((x*50) - 32 + 50 //
                                                2, (y*50)-32+50//2))
                    else:
                        screen.blit(rat_left, ((x*50) - 32 + 50 //
                                                2, (y*50)-32+50//2))

                self.object_draw(self.maze.grid[x][y], rect)

        self.clock.tick(1000)
        pygame.display.update()

    def _get_state(self):
        # [0 , 0 , 0,  0]
        # [0 , 3 , 0,  0]
        # [0 , ^ , 0 , 0]
        # [0 , 0 , 0,  0]

        # (2, 1) -> (1,1) + (0,1) -> [0,0]

        # Retornar linha reta
        state = list()

        current_x = self.agent.x
        current_y = self.agent.y
        current_cheese = max(self.number_cheese, 0)
        state.append(current_x)
        state.append(current_y)

        if self.agent.direction == "Up":
            current_x -= 1
        if self.agent.direction == "Down":
            current_x += 1
        if self.agent.direction == "Right":
            current_y += 1
        if self.agent.direction == "Left":
            current_y -= 1

        if self.maze.is_valid_position(current_x, current_y):
            state.append(self.maze.grid[current_x][current_y])
        else:
            state.append(3)

        state.append(current_cheese)

        return state

    def _take_action(self, action):
        # print(action)
        self.agent.got_cheese = False
        directions = ["Up", "Down", "Left", "Right"]
        self.agent.move(directions[action], self.maze)

    def _get_reward(self):
        # reward = 1
        reward = -0.01

        if self.maze.done:
            reward += 5

        elif self.agent.eaten_cheese:
            reward += 1
            self.number_cheese -= 1

        return reward

    def find_initial_pos(self, grid):

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    return i, j

class Maze_agent:
    def __init__(self, maze, screen):
        self.env = Rat_Game_Gym(maze, screen)
        self.maze_size = tuple([10, 10])
        self.state_bounds = list(zip([0, 0], [10, 10]))
        self.number_actions = 4
        self.number_blocks = 5

        self.Q = self.load_model("player_game/env/model/modelTraining.pickle")

        self.epsilon = 1
        self.learning_rate = 1

        self.decay = DECAY
        self.discount = DISCOUNT
        self.all_rewards = []
        self.mean_rewards = []
        self.variance = 10000

    def discretize_state(self, state) -> tuple:
        return tuple(state)

    def decide_action(self, state) -> int:

        if np.random.random() < self.epsilon:
            action = choice(list(range(4)))
        else:
            action = int(np.argmax(self.Q[state]))

        return action

    def update_q(self, current_state, action, reward, next_state):  # FIX

        self.Q[tuple(current_state) + (action,)] = self.Q[
            tuple(current_state) + (action,)
        ] + self.learning_rate * (
            reward
            + self.discount * np.max(self.Q[tuple(next_state)])
            - self.Q[tuple(current_state) + (action,)]
        )

    def update_learning_rate(self, episode) -> float:
        learning_rate = min(1, 1 - math.log10((episode + 1) / DECAY))
        learning_rate = max(learning_rate, LEARNING_RATE_MINIMUM)

        return learning_rate

    def update_epsilon(self, episode) -> float:
        epsilon = min(1, 1 - math.log10((episode + 1) / DECAY))
        epsilon = max(epsilon, EPSILON_MINIMUM)

        return epsilon

    def train(self):
        
        for episode in range(EPISODES):

            watch = True
            
            #print('comeco do for')
            current_state = self.env._reset()
            #print('depois do reset')
            current_state = self.discretize_state(current_state)

            done = False

            rewards = 0

            moves = 0
            #print('antes do done')

            while not done:

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.variance <= 0.1:
                                self.save_model("player_game/env/model/model4.pickle")
                            return 0
                        if event.key == pygame.K_SPACE:
                            watch = False

                if episode % RENDER_EPISODE == 0 and episode != 0 and watch == True:
                    #self.save_model("player_game/env/model/modelTraining.pickle")
                    self.env._render(self.env.screen)
                    time.sleep(0.1)

                action = self.decide_action(current_state)

                next_state, reward, done = self.env.step(action)
                next_state = self.discretize_state(next_state)

                self.update_q(current_state, action, reward, next_state)

                current_state = next_state
                rewards += reward

                if moves > 1000:
                    break

                moves += 1

            if True:
                self.epsilon = self.update_epsilon(episode)
                self.learning_rate = self.update_learning_rate(episode)

            self.all_rewards.append(rewards)

            if episode >= 100:
                mean_reward = sum(self.all_rewards[-100:]) / 100
            else:
                mean_reward = sum(self.all_rewards) / (episode + 1)

            self.mean_rewards.append(mean_reward)

            self.variance = pvariance(self.all_rewards[-50:])
            
            plot.plot(self.all_rewards, self.mean_rewards, self.epsilon)
            plot_img = load_image("plot.png", res=(500,500))
            self.env.screen.blit(plot_img, pygame.Rect(500,  0, 500, 500))
            pygame.display.update()


        self.env.close()

    def save_model(self, path):
        with open(path, "wb") as model:
            pickle.dump(self.Q, model)

    def load_model(self, path) -> pickle:
        with open(path, "rb") as model:
            return pickle.load(model)

class Rat_Game:

    def __init__(self, w=1000, h=500):
        self.width = w
        self.height = h

        # inicializa o display com a largura e altura especificada
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rat")
        self.clock = pygame.time.Clock()

        self.Q = 0

        self.start()  # inicializa o jogador e o grid

        # Dimensoes de cada celula do grid na tela
        self.rect_width = (self.width//2)//self.grid.n_cols
        self.rect_height = self.height//self.grid.n_rows

    def start(self):
        self.player = Player(1, 1, "Player")
        self.agent = Player(0, 0, "Agent")
        self.player.initial_x, self.player.initial_y = 0, 0
        self.agent.initial_x, self.agent.initial_y = 0, 0
        self.grid = Grid(self.player, n_cols=10, n_rows=10)
        self.grid_ai = Grid(self.agent, n_cols=10, n_rows=10)
    
    def reset_mm(self):

        self.grid_ai.grid[self.agent.x][self.agent.y] = 2

        self.agent.x, self.agent.y = self.agent.initial_x, self.agent.initial_y

        for i in range(len(self.grid_ai.cheeses_x)):
            self.grid_ai.grid[self.grid_ai.cheeses_x[i]][self.grid_ai.cheeses_y[i]] = 4
        
        return 0

    def reset_pvi(self, winner):

        if winner == 0: #Jogador venceu o jogo
            self.grid.grid[self.player.x][self.player.y] = 2
        else: #Ratatail venceu o jogo
            self.grid_ai.grid[self.agent.x][self.agent.y] = 2

        self.agent.x, self.agent.y = self.agent.initial_x, self.agent.initial_y
        self.player.x, self.player.y = self.player.initial_x, self.player.initial_y
        
        return 0

    def level_select(self):
        cursor_pos = 0

        while True:
            self.screen.fill((0,0,0))

            self.screen.blit(RAT_IMG, (cursor_pos*107 + 40, 330))
            
            draw_text('SELECT LEVEL', MENU_FONT, (255,255,255), self.screen, 8000, 30)
            draw_text('1  2  3  4  5  6  7  8  9', SELECT_FONT, (255,255,255), self.screen, 8000, 250)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.grid.grid, self.grid_ai.grid = get_grid(cursor_pos), get_grid(cursor_pos)
                        self.player.x, self.player.y, self.agent.x, self.agent.y = get_pos(cursor_pos)
                        self.player.initial_x, self.player.initial_y, self.agent.initial_x, self.agent.initial_y = get_pos(cursor_pos)

                        self.grid.populate_lists()
                        self.grid_ai.populate_lists()

                        return cursor_pos
                    if event.key == pygame.K_RIGHT and cursor_pos < 8:
                        cursor_pos += 1
                    if event.key == pygame.K_LEFT and cursor_pos > 0:
                        cursor_pos -= 1

    def game_step(self, level):
        if self.grid.done:
            replay = self.win_screen(0)

            file1 = open('player_game/levels.txt', 'r')
            levels = file1.readlines()
            file1.close()

            levels[level] = '1\n'

            file2 = open('player_game/levels.txt', 'w')
            file2.writelines(levels)
            file2.close()

            if replay:
                self.reset_pvi(0)
                self.grid.done = False
            else:
                return 1
            
        if self.grid_ai.done:
            replay = self.win_screen(1)

            if replay:
                self.reset_pvi(1)
                self.grid_ai.done = False
            else:
                return 1
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:

                # Movimento do Agente
                state = self.get_state()
                if np.random.random() < 0.5:
                    agent_move = choice(["Up", "Down", "Left", "Right"])
                else:
                    agent_move = ["Up", "Down", "Left", "Right"][int(np.argmax(game.Q[state]))]

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
        self.screen.fill((0, 0, 0))

        self.draw_vision(self.player, self.grid, self.screen)
        self.draw_vision(self.agent, self.grid_ai, self.screen)

        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(
            self.width//2 - 4, 0, 8, self.height))    

        pygame.display.update()
        self.clock.tick(60)

        # Retorna os dados importantes desse step
        #return self.grid.done, self.player.score
        return 0

    def maze_maker(self):

        maze = [[0]*self.grid_ai.n_cols for i in range(self.grid_ai.n_rows)]
        finish_flag = 0
        rat_flag = 0
        
        while True:
            enter_flag = 0
            while not enter_flag:
                self.screen.fill((100, 100, 100))
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

                        if event.key == K_RETURN:
                            enter_flag = 1

                        if event.key == K_r and rat_flag == 0 and mouse_pos[0] < self.width//2:
                            maze[mouse_x][mouse_y] = 1
                            self.agent.x = mouse_x
                            self.agent.y = mouse_y
                            self.agent.initial_x = mouse_x
                            self.agent.initial_y = mouse_y
                            rat_flag = 1

                        if event.key == K_f and finish_flag == 0 and mouse_pos[0] < self.width//2:
                            maze[mouse_x][mouse_y] = 2
                            finish_flag = 1

                        if event.key == K_DELETE and mouse_pos[0] < self.width//2:
                            if maze[mouse_x][mouse_y] == 1:
                                rat_flag = 0
                            elif maze[mouse_x][mouse_y] == 2:
                                finish_flag = 0
                            elif maze[mouse_x][mouse_y] == 5:
                                self.grid_ai.holes_x.remove(mouse_x)
                                self.grid_ai.holes_y.remove(mouse_y)

                            maze[mouse_x][mouse_y] = 0

                        '''if event.key == K_t and mouse_pos[0] < self.width//2:
                            maze[mouse_x][mouse_y] = 5
                            self.grid_ai.holes_x.append(mouse_x)
                            self.grid_ai.holes_y.append(mouse_y)'''

                    if pygame.mouse.get_pressed()[0] and mouse_pos[0] < self.width//2:
                        maze[mouse_x][mouse_y] = 3

                    elif pygame.mouse.get_pressed()[2] and mouse_pos[0] < self.width//2:
                        maze[mouse_x][mouse_y] = 4

                for x in range(0, self.grid_ai.n_cols):
                    for y in range(0, self.grid_ai.n_rows):
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

                        '''elif maze[x][y] == 5:
                            self.screen.blit(trap_closed_img, rect)'''

                self.screen.blit(mm_inst, pygame.Rect(500, 0, 500, 500))

                pygame.display.update()

            self.grid_ai.grid = maze
            self.grid_ai.populate_lists()
            
            agent = Maze_agent(maze, self.screen)
            print(array(maze).T)
            agent.train()


    def win_screen(self, select):

        while True:
            
            if select == 0: #Player won
                draw_text('You won the game!', OPTIONS_FONT, (255,255,255), self.screen, 8000, 8000)
            elif select == 1: #AI won (Player vs IA)
                draw_text('Ratatail won the game!', OPTIONS_FONT, (255,255,255), self.screen, 8000, 8000)
            elif select == 2: # AI won (Maze maker)
                draw_text('Ratatail found the way out!', OPTIONS_FONT, (255,255,255), self.screen, 8000, 150)
                draw_text('Press Space to edit the maze', OPTIONS_FONT, (255,255,255), self.screen, 8000, 280)

            draw_text('Press Enter to play again', OPTIONS_FONT, (255,255,255), self.screen, 8000, 330)
            draw_text('Press ESC to return to the Main Menu', OPTIONS_FONT, (255,255,255), self.screen, 8000, 380)
            
            pygame.display.update()

            for event in pygame.event.get():            
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 0
                    elif event.key == pygame.K_RETURN:
                        return 1
                    elif event.key == pygame.K_SPACE:
                        return 2
                        

    def save_maze(self, maze):
        f = open(os.path.join(os.getcwd(), "player_game",
                              "maps", f"map_{randint(1,10000)}.txt"), "w+")
        for x in range(len(maze)):
            for y in range(len(maze[0])):
                f.write(f"{maze[x][y]}")
            if x != len(maze)-1:
                f.write("\n")
        f.close()

    def draw_grid(self, screen):


        for x in range(0, self.grid_ai.n_cols):
            for y in range(0, self.grid_ai.n_rows):
                # Posicao
                rect = pygame.Rect(
                    x * self.rect_width,  y * self.rect_height, self.rect_width, self.rect_height)

                # Chao
                screen.blit(floor_img, rect)

                # Agente
                if self.grid_ai.grid[x][y] == 1:
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

                self.object_draw(self.grid_ai.grid[x][y], rect)

        #pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
        #    self.width//2 - 4, 0, 8, self.height))        

    def draw_vision(self, rat, the_grid, screen):

        if rat.name == 'Player':
            constant = 500
            rat_vis_up, rat_vis_down, rat_vis_left, rat_vis_right = human_rat_up, human_rat_down, human_rat_left, human_rat_right
        else:
            rat_vis_up, rat_vis_down, rat_vis_left, rat_vis_right = rat_up, rat_down, rat_left, rat_right
            constant = 0

        if rat.direction == "Up":

            rect_left = pygame.Rect(
                    (rat.x - 1) * self.rect_width + constant,  (rat.y) * self.rect_height, self.rect_width, self.rect_height)

            rect_right = pygame.Rect(
                    (rat.x + 1) * self.rect_width + constant,  (rat.y) * self.rect_height, self.rect_width, self.rect_height)

            if rat.x > 0:
                screen.blit(floor_img, rect_left)
                self.object_draw(the_grid.grid[rat.x - 1][rat.y], rect_left)

            if rat.x < 9:
                screen.blit(floor_img, rect_right)
                self.object_draw(the_grid.grid[rat.x + 1][rat.y], rect_right)

            for i in range(4):
                if not the_grid.is_valid_position((rat.x),(rat.y - i)):
                    if the_grid.grid[rat.x][rat.y - i] == 3:
                        rect2 = pygame.Rect(
                                (rat.x) * self.rect_width + constant,  (rat.y - i) * self.rect_height, 
                                self.rect_width, self.rect_height)
                        self.screen.blit(wall_img, rect2)
                    break

                rect = pygame.Rect(
                    (rat.x) * self.rect_width + constant,  (rat.y - i) * self.rect_height, self.rect_width, self.rect_height)

                # Chao
                screen.blit(floor_img, rect)
                self.object_draw(the_grid.grid[rat.x][rat.y - i], rect)

            screen.blit(rat_vis_up, ((rat.x*self.rect_width + constant) - 30 + self.rect_width //
                                        2, (rat.y*self.rect_height)-32+self.rect_height//2))
        
        elif rat.direction == "Down":

            rect_left = pygame.Rect(
                    (rat.x - 1) * self.rect_width + constant,  (rat.y) * self.rect_height, self.rect_width, self.rect_height)

            rect_right = pygame.Rect(
                    (rat.x + 1) * self.rect_width + constant,  (rat.y) * self.rect_height, self.rect_width, self.rect_height)

            if rat.x > 0:
                screen.blit(floor_img, rect_left)
                self.object_draw(the_grid.grid[rat.x - 1][rat.y], rect_left)

            if rat.x < 9:
                screen.blit(floor_img, rect_right)
                self.object_draw(the_grid.grid[rat.x + 1][rat.y], rect_right)

            for i in range(4):

                if not the_grid.is_valid_position((rat.x),(rat.y + i)):
                    if rat.y + i < 10 and the_grid.grid[rat.x][rat.y + i] == 3:
                        rect2 = pygame.Rect(
                                (rat.x) * self.rect_width + constant,  (rat.y + i) * self.rect_height, 
                                self.rect_width, self.rect_height)
                        self.screen.blit(wall_img, rect2)
                    break
                rect = pygame.Rect(
                    (rat.x) * self.rect_width + constant,  (rat.y + i) * self.rect_height, self.rect_width, self.rect_height)

                # Chao
                screen.blit(floor_img, rect)
                self.object_draw(the_grid.grid[rat.x][rat.y + i], rect)

            screen.blit(rat_vis_down, ((rat.x*self.rect_width + constant) - 30 + self.rect_width //
                                            2, (rat.y*self.rect_height)-32+self.rect_height//2))
        
        elif rat.direction == "Right":

            rect_up = pygame.Rect(
                    (rat.x) * self.rect_width + constant,  (rat.y - 1) * self.rect_height, self.rect_width, self.rect_height)

            rect_down = pygame.Rect(
                    (rat.x) * self.rect_width + constant,  (rat.y + 1) * self.rect_height, self.rect_width, self.rect_height)

            if rat.y > 0:
                screen.blit(floor_img, rect_up)
                self.object_draw(the_grid.grid[rat.x][rat.y - 1], rect_up)

            if rat.y < 9:
                screen.blit(floor_img, rect_down)
                self.object_draw(the_grid.grid[rat.x][rat.y + 1], rect_down)

            for i in range(4):

                if not the_grid.is_valid_position((rat.x + i),(rat.y)):
                    if rat.x + i < 10 and the_grid.grid[rat.x + i][rat.y] == 3:
                        rect2 = pygame.Rect(
                                (rat.x + i) * self.rect_width + constant,  (rat.y) * self.rect_height, 
                                self.rect_width, self.rect_height)
                        self.screen.blit(wall_img, rect2)
                    break

                rect = pygame.Rect(
                    (rat.x + i) * self.rect_width + constant,  (rat.y) * self.rect_height, self.rect_width, self.rect_height)

                # Chao
                screen.blit(floor_img, rect)
                self.object_draw(the_grid.grid[rat.x + i][rat.y],  rect)

            screen.blit(rat_vis_right, ((rat.x*self.rect_width + constant) - 30 + self.rect_width //
                                            2, (rat.y*self.rect_height)-32+self.rect_height//2))
        
        else:

            rect_up = pygame.Rect(
                    (rat.x) * self.rect_width + constant,  (rat.y - 1) * self.rect_height, self.rect_width, self.rect_height)

            rect_down = pygame.Rect(
                    (rat.x) * self.rect_width + constant,  (rat.y + 1) * self.rect_height, self.rect_width, self.rect_height)

            if rat.y > 0:
                screen.blit(floor_img, rect_up)
                self.object_draw(the_grid.grid[rat.x][rat.y - 1], rect_up)

            if rat.y < 9:
                screen.blit(floor_img, rect_down)
                self.object_draw(the_grid.grid[rat.x][rat.y + 1], rect_down)
            
            for i in range(4):

                if not the_grid.is_valid_position((rat.x - i),(rat.y)):
                    if the_grid.grid[rat.x - i][rat.y] == 3:
                        rect2 = pygame.Rect(
                                (rat.x - i) * self.rect_width + constant,  (rat.y) * self.rect_height, 
                                self.rect_width, self.rect_height)
                        self.screen.blit(wall_img, rect2)
                    break

                rect = pygame.Rect(
                    (rat.x - i) * self.rect_width + constant,  (rat.y) * self.rect_height, self.rect_width, self.rect_height)

                # Chao
                screen.blit(floor_img, rect)
                self.object_draw(the_grid.grid[rat.x - i][rat.y], rect)
            
            screen.blit(rat_vis_left, ((rat.x*self.rect_width + constant) - 30 + self.rect_width //
                                            2, (rat.y*self.rect_height)-32+self.rect_height//2))

    def object_draw(self, pos, rect):
        #Objetivo
        if pos == 2:
            self.screen.blit(goal_img, rect)

        # Parede
        elif pos == 3:
            self.screen.blit(wall_img, rect)
        # Queijo
        elif pos == 4:
            self.screen.blit(cheese_img, rect)

        # Armadilha 1
        '''elif pos == 5:
            if trap_hole:
                self.screen.blit(trap_open_img, rect)
            else:
                self.screen.blit(trap_closed_img, rect)'''
    
    def load_model(self, path) -> pickle:
        with open(path, "rb") as model:
            return pickle.load(model)

    def get_state(self):
        # [0 , 0 , 0,  0]
        # [0 , 3 , 0,  0]
        # [0 , ^ , 0 , 0]
        # [0 , 0 , 0,  0]

        # (2, 1) -> (1,1) + (0,1) -> [0,0]

        # Retornar linha reta
        state = list()

        current_x = self.agent.x
        current_y = self.agent.y
        current_cheese = 0
        state.append(current_x)
        state.append(current_y)

        if self.agent.direction == "Up":
            current_x -= 1
        if self.agent.direction == "Down":
            current_x += 1
        if self.agent.direction == "Right":
            current_y += 1
        if self.agent.direction == "Left":
            current_y -= 1

        if self.grid_ai.is_valid_position(current_x, current_y):
            state.append(self.grid_ai.grid[current_x][current_y])
        else:
            state.append(3)

        state.append(current_cheese)

        return tuple(state)

if __name__ == "__main__":

    skin = 0
    while True:
        game = Rat_Game()
        mode_selection, skin = main_menu(game.screen, skin)

        select_game_skin(skin)

        finished = 0

        if mode_selection == 0:    # Maze maker
            game.maze_maker()
        elif mode_selection == 1:  # Player vs AI
            level = game.level_select()

            game.Q = game.load_model(f"player_game/env/model/model{level}.pickle")

            while finished == 0:
                finished = game.game_step(level)