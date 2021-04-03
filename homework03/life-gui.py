import argparse

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.width = self.cell_size * self.life.cols
        self.height = self.cell_size * self.life.rows

        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        x = 0
        y = 0
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                rectangle = pygame.Rect(x + 1, y + 1, self.cell_size - 1, self.cell_size - 1)

                if self.life.curr_generation[i][j] == 1:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')

                pygame.draw.rect(self.screen, color, rectangle)
                x += self.cell_size

            x = 0
            y += self.cell_size


    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        is_running = True
        is_paused = False

        self.draw_lines()
        while is_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    is_running = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    is_paused = not is_paused
                if event.type == MOUSEBUTTONDOWN and is_paused:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // self.cell_size, x // self.cell_size
                    self.life.curr_generation[row][col] = not self.life.curr_generation[row][col]


            if not is_paused:
                if self.life.is_max_generations_exceeded or not self.life.is_changing:
                    is_running = False
                    continue
                self.life.step()

            self.draw_grid()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-w', '--width', 
        default='640',
        help='the screen width'
    )
    parser.add_argument('-ht', '--height', 
        default='480',
        help='the screen height'
    )
    parser.add_argument('-s', '--cell-size', 
        default='10',
        help='the size of one cell in the game'
    )
    parser.add_argument('-m', '--max-generations', 
        default='50',
        help='number of the maximum generation'
    )

    args = parser.parse_args()

    width = int(args.width)
    height = int(args.height)
    cell_size = int(args.cell_size)
    max_generations = int(args.max_generations)

    game = GameOfLife((int(width / cell_size), int(height / cell_size)), max_generations)
    gui = GUI(game, cell_size)

    gui.run()
