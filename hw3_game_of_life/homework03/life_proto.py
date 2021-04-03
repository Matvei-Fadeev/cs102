import random
from typing import List, Tuple

import pygame
from pygame.locals import *

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = []
        if randomize:
            grid = [
                [random.randint(0, 1) for j in range(self.cell_width)]
                for i in range(self.cell_height)
            ]
        else:
            grid = [[0] * self.cell_width for i in range(self.cell_height)]
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        y = 0
        for i in range(self.cell_height):
            x = 0
            for j in range(self.cell_width):
                color = pygame.Color("white")
                if self.grid[i][j]:
                    color = pygame.Color("green")

                screen_rectangle = pygame.Rect(x + 1, y + 1, self.cell_size - 1, self.cell_size - 1)

                pygame.draw.rect(self.screen, color, screen_rectangle)
                x += self.cell_size
            y += self.cell_size

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        cells = []

        i_left = max(0, cell[0] - 1)
        i_right = min(self.cell_height, cell[0] + 2)

        j_left = max(0, cell[1] - 1)
        j_right = min(self.cell_width, cell[1] + 2)

        for i in range(i_left, i_right):
            for j in range(j_left, j_right):
                if i != cell[0] or j != cell[1]:
                    cells.append(self.grid[i][j])

        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        grid = []

        for i in range(self.cell_height):
            line = []
            for j in range(self.cell_width):
                neighbours_count = self.get_neighbours((i, j)).count(1)
                min_neighbours_count = 3 - (self.grid[i][j] == 1)
                max_neighbours_count = 3
                if min_neighbours_count <= neighbours_count <= max_neighbours_count:
                    line.append(1)
                else:
                    line.append(0)
            grid.append(line)

        return grid


if __name__ == "__main__":
    game_of_life = GameOfLife()
    game_of_life.run()
