import os
import operator
import time
import numpy.random.mtrand
import random
import numpy
import pygame

MAZE_SIZE = (16, 16)
N_STARTING_POINTS = 4
REMAIN_ALIVE_PROBABILITY = 0.98
BIRTH_PROBABILITY = 0.05
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
        self.rect = pygame.Rect(
            (self.current_position[1] * PIXELS_FOR_CELL, self.current_position[0] * PIXELS_FOR_CELL),
            (PIXELS_FOR_CELL, PIXELS_FOR_CELL)
        )
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

    def render(self):
        self.screen.blit(self.background, (0, 0))
        for i in range(self.maze_layout.shape[0]):
            for j in range(self.maze_layout.shape[1]):
                if self.maze_layout[i][j] == 1:
                    wall_sprite = pygame.sprite.RenderPlain(MazeWall((i, j)))
                    wall_sprite.draw(self.screen)

        self.player_sprite = pygame.sprite.RenderPlain(self.player)
        self.player_sprite.draw(self.screen)
        pygame.display.flip()


    def new_game(self):
        self.maze_layout, player_init_position = generate_maze_layout(
            MazeGenerationConfig(MAZE_SIZE, N_STARTING_POINTS,
                                 REMAIN_ALIVE_PROBABILITY, BIRTH_PROBABILITY)
        )
        self.player = Player(player_init_position)
        self.render()
        self.play()

    def update(self):
        self.player_sprite.draw(self.screen)
        pygame.display.flip()

    def play(self):
        move_directions = {
            pygame.K_LEFT: (0, -1),
            pygame.K_RIGHT: (0, 1),
            pygame.K_UP: (-1, 0),
            pygame.K_DOWN: (1, 0),
        }
        # Event loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    self.move_if_possible(move_directions[event.key])

    def move_if_possible(self, direction):
        new_position = tuple(map(operator.add, self.player.current_position, direction))
        if new_position[0] >= 0 and self.maze_layout.shape[0] > 0 <= new_position[1] < self.maze_layout.shape[1]:
            if self.maze_layout[new_position] == 0:
                self.screen.blit(self.background, self.player.rect, self.player.rect)
                self.player.move(new_position)
                self.update()
        else:
            self.new_game()


class MazeGenerationConfig:
    def __init__(self, maze_size, n_starting_points, remain_alive_probability, birth_probability):
        self.maze_size = maze_size
        self.n_starting_points = n_starting_points
        self.remain_alive_probability = remain_alive_probability
        self.birth_probability = birth_probability


def generate_maze_layout(config):
    """
    Puts walls and passages, chooses starting point of a maze
    :type config: MazeGenerationConfig
    """

    maze_layout = numpy.ones(config.maze_size[0] * config.maze_size[1]).reshape(config.maze_size)
    substarting_points = generate_substarting_points(config.n_starting_points, config.maze_size)
    starting_point = substarting_points[0]

    last_point = len(substarting_points) > 1

    next_direction = choose_random_direction((0.25, 0.25, 0.25, 0.25))
    while substarting_points:
        substarting_point = substarting_points.pop()
        if not substarting_points:
            last_point = True
        birth_probability = config.birth_probability
        while true_with_probability(config.remain_alive_probability) or last_point:  # one way in this loop
            if true_with_probability(birth_probability):
                birth_probability = birth_probability * 0.8
                substarting_points.append(substarting_point)
                last_point = False
            maze_layout[substarting_point] = 0
            if at_edge(substarting_point, config.maze_size):
                break

            probabilities_for_directions = {
                'L': (0.5, 0.25, 0.0, 0.25),
                'U': (0.25, 0.5, 0.25, 0.0),
                'R': (0.0, 0.25, 0.5, 0.25),
                'D': (0.25, 0.0, 0.25, 0.5)
            }

            substarting_point = move_point(substarting_point, next_direction)
            next_direction = choose_random_direction(probabilities_for_directions[next_direction])
    return maze_layout, starting_point


def choose_random_direction(probabilities):
    DIRECTIONS = ['L', 'U', 'R', 'D']
    bins = numpy.cumsum(probabilities)
    return DIRECTIONS[numpy.digitize(numpy.random.mtrand.random_sample(1), bins)]


def generate_substarting_points(n_starting_points, maze_size):
    substarting_points = []
    center = (maze_size[0] / 2, maze_size[1] / 2)
    hors_for_start = maze_size[0] / 2
    vers_for_start = maze_size[1] / 2
    for i in range(n_starting_points):
        starting_point = (random.randint(center[0] - hors_for_start / 2,
                                         center[0] + hors_for_start / 2),
                          random.randint(center[1] - vers_for_start / 2,
                                         center[1] + vers_for_start / 2))
        substarting_points.append(starting_point)
    return substarting_points


def move_point(point, direction):
    if direction == 'L':
        return point[0], point[1] - 1
    elif direction == 'U':
        return point[0] - 1, point[1]
    elif direction == 'R':
        return point[0], point[1] + 1
    elif direction == 'D':
        return point[0] + 1, point[1]
    else:
        raise ValueError('Invalid direction: {1}'.format(direction))


def at_edge(substarting_point, maze_size):
    return substarting_point[0] in [0, maze_size[0] - 1] \
           or substarting_point[1] in [0, maze_size[1] - 1]


def true_with_probability(probability):
    return random.random() < probability


if __name__ == '__main__':
    Game()
