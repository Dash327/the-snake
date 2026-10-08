import sys
from random import randint, choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Координаты центра экрана:
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


def handle_keys(key, game_object):
    """Обрабатывает нажатия клавиш для смены направления."""
    if key == pg.K_UP and game_object.direction != DOWN:
        game_object.next_direction = UP
    elif key == pg.K_DOWN and game_object.direction != UP:
        game_object.next_direction = DOWN
    elif key == pg.K_LEFT and game_object.direction != RIGHT:
        game_object.next_direction = LEFT
    elif key == pg.K_RIGHT and game_object.direction != LEFT:
        game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, color, border_color=BORDER_COLOR):
        """Инициализирует базовые атрибуты: позицию и цвет."""
        self.position = SCREEN_CENTER
        self.body_color = color
        self.border_color = border_color

    def draw_cell(self, position, color, border_color):
        """Отрисовывает одну ячейку в виде квадрата с границей."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Метод отрисовки, переопределяется в наследниках."""


class Apple(GameObject):
    """Класс, представляющий яблоко на игровом поле."""

    def __init__(self, occupied_positions=(SCREEN_CENTER,)):
        """Инициализирует яблоко, задает цвет и случайную позицию."""
        super().__init__(APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=(SCREEN_CENTER,)):
        """Генерирует случайные координаты яблока в пределах сетки."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (x, y)
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на экране в виде квадрата с границей."""
        self.draw_cell(self.position, self.body_color, self.border_color)


class Snake(GameObject):
    """Класс, представляющий змейку и управляющий её состоянием."""

    def __init__(self):
        """Инициализирует змейку с начальными параметрами."""
        super().__init__(SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает текущие координаты головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовывает змейку, включая затирание хвоста."""
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color, self.border_color)

        # Отрисовка головы змейки
        self.draw_cell(
            self.get_head_position(), self.body_color, self.border_color
        )

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет направление движения, если задано следующее."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Вычисляет новую позицию головы и обновляет список сегментов."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        # Просто добавляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Если длина списка превышает текущую длину змейки, удаляем хвост
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def reset(self):
        """Сбрасывает состояние змейки к начальному и очищает экран."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def main():
    """Основная функция: инициализация и бесконечный игровой цикл."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                handle_keys(event.key, snake)

        snake.update_direction()

        # 3. Двигаем змейку (модифицируем список позиций)
        snake.move()

        # 4. Проверяем, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        # 5. Проверяем столкновения змейки с собой
        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
