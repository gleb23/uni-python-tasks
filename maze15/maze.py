import os
import operator
import time
import numpy.random.mtrand
import random
import numpy
import pygame

MAZE_SIZE = (16, 16)
PIXELS_FOR_CELL = 25
EXTRA_SPACE = (0, 0)


def load_png(name):
    """
    Load image and return image object
    """
    fullname = os.path.join('resources', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image, image.get_rect()


class MazeWall(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('brick.png')
        self.rect = pygame.Rect((position[1] * PIXELS_FOR_CELL, position[0] * PIXELS_FOR_CELL),
                            (PIXELS_FOR_CELL, PIXELS_FOR_CELL))
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('bat.png')
        self.current_position = position
        self.rect = pygame.Rect((position[1] * PIXELS_FOR_CELL, position[0] * PIXELS_FOR_CELL),
                            (PIXELS_FOR_CELL, PIXELS_FOR_CELL))
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def move(self, new_position):
        self.current_position = new_position
        self.rect = pygame.Rect((self.current_position[1] * PIXELS_FOR_CELL, self.current_position[0] * PIXELS_FOR_CELL),
                            (PIXELS_FOR_CELL, PIXELS_FOR_CELL))
        print self.current_position


class Game:
    def __init__(self):
        # Initialise screen
        pygame.init()
        self.screen = pygame.display.set_mode((PIXELS_FOR_CELL * MAZE_SIZE[1] + EXTRA_SPACE[0],
                                               PIXELS_FOR_CELL * MAZE_SIZE[0] + EXTRA_SPACE[1]))
        pygame.display.set_caption('It\'s a maze! Try to get out!')

        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))

        self.new_game()

    def new_game(self):
        self.screen.blit(self.background, (0, 0))

        self.maze, self.current_position = generate_maze(MAZE_SIZE)

        for i in range(self.maze.shape[0]):
            for j in range(self.maze.shape[1]):
                if self.maze[i][j] == 1:
                    wall = MazeWall((i, j))
                    wall_sprite = pygame.sprite.RenderPlain(wall)
                    wall_sprite.draw(self.screen)

        self.player = Player(self.current_position)
        self.player_sprite = pygame.sprite.RenderPlain(self.player)
        self.player_sprite.draw(self.screen)

        pygame.display.flip()

        self.game()

    def update(self):
        self.player_sprite.draw(self.screen)
        pygame.display.flip()



    def game(self):
        TO_SLEEP = 0.1
        # Event loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                direction = (0, -1)
                self.move_if_possible(direction)
                time.sleep(TO_SLEEP)
            if keys[pygame.K_RIGHT]:
                direction = (0, 1)
                self.move_if_possible(direction)
                time.sleep(TO_SLEEP)
            if keys[pygame.K_UP]:
                direction = (-1, 0)
                self.move_if_possible(direction)
                time.sleep(TO_SLEEP)
            if keys[pygame.K_DOWN]:
                direction = (1, 0)
                self.move_if_possible(direction)
                time.sleep(TO_SLEEP)

    def move_if_possible(self, direction):
        new_position = tuple(map(operator.add, self.player.current_position, direction))
        if new_position[0] >= 0 and self.maze.shape[0] > 0 <= new_position[1] < self.maze.shape[1]:
            if self.maze[new_position] == 0:
                self.screen.blit(self.background, self.player.rect, self.player.rect)
                self.player.move(new_position)
                self.update()
        else:
            self.new_game()


def _weighted_value(values, probabilities):
    bins = numpy.cumsum(probabilities)
    return values[numpy.digitize(numpy.random.mtrand.random_sample(1), bins)]


def generate_maze(maze_size):
    """
    Puts walls and passages, chooses starting point of a maze
    """
    hors = maze_size[0]
    vers = maze_size[1]
    # init maze with 1
    maze = numpy.zeros(hors * vers).reshape(maze_size)
    for i in range(hors):
        for j in range(vers):
            maze[i][j] = 1

    # choose starting point
    center = (hors / 2, vers / 2)
    hors_for_start = hors / 2
    vers_for_start = vers / 2
    N_STARTING_POINTS = 4
    substarting_points = []
    for i in range(N_STARTING_POINTS):
        starting_point = (random.randint(center[0] - hors_for_start / 2, center[0] + hors_for_start / 2),
                          random.randint(center[1] - vers_for_start / 2, center[1] + vers_for_start / 2))
        substarting_points.append(starting_point)
    INITIAL_DEATH_RATE = 20
    INITIAL_BIRTH_RATE = INITIAL_DEATH_RATE * 2
    death_rate = INITIAL_DEATH_RATE
    birth_rate = INITIAL_BIRTH_RATE
    DIRECTIONS = ['L', 'U', 'R', 'D']
    next_direction = _weighted_value(DIRECTIONS, (0.25, 0.25, 0.25, 0.25))
    while substarting_points:
        substarting_point = substarting_points.pop()
        if not substarting_points:
            death_rate = 0
        alive_index = 1000
        birth_index = 1000
        while alive_index > death_rate:  # one way in this loop
            if birth_index < birth_rate:
                birth_rate = birth_rate * 4 / 5
                death_rate = INITIAL_DEATH_RATE
                substarting_points.append(substarting_point)

            maze[substarting_point] = 0

            # stop if the edge is reached
            if substarting_point[0] in [0, hors - 1] or substarting_point[1] in [0, vers - 1]:
                break

            if next_direction == 'L':
                substarting_point = (substarting_point[0], substarting_point[1] - 1)
                next_direction = _weighted_value(DIRECTIONS, (0.5, 0.25, 0.0, 0.25))
            elif next_direction == 'U':
                substarting_point = (substarting_point[0] - 1, substarting_point[1])
                next_direction = _weighted_value(DIRECTIONS, (0.25, 0.5, 0.25, 0.0))
            elif next_direction == 'R':
                substarting_point = (substarting_point[0], substarting_point[1] + 1)
                next_direction = _weighted_value(DIRECTIONS, (0.0, 0.25, 0.5, 0.25))
            else:
                substarting_point = (substarting_point[0] + 1, substarting_point[1])
                next_direction = _weighted_value(DIRECTIONS, (0.25, 0.0, 0.25, 0.5))
            alive_index = random.randint(1, 1000)
            birth_index = random.randint(1, 800)

    print maze, starting_point
    return maze, starting_point


if __name__ == '__main__':
    Game()
