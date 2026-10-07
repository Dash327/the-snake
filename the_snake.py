import sys
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


def handle_keys(key, game_object):
    """Обрабатывает нажатия клавиш для смены направления."""
    if key == pygame.K_UP and game_object.direction != DOWN:
        game_object.next_direction = UP
    elif key == pygame.K_DOWN and game_object.direction != UP:
        game_object.next_direction = DOWN
    elif key == pygame.K_LEFT and game_object.direction != RIGHT:
        game_object.next_direction = LEFT
    elif key == pygame.K_RIGHT and game_object.direction != LEFT:
        game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self):
        """Инициализирует базовые атрибуты: позицию и цвет."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Метод отрисовки, переопределяется в наследниках."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко на игровом поле."""

    def __init__(self):
        """Инициализирует яблоко, задает цвет и случайную позицию."""
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Генерирует случайные координаты яблока в пределах сетки."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на экране в виде квадрата с границей."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку и управляющий её состоянием."""

    def __init__(self):
        """Инициализирует змейку с начальными параметрами."""
        super().__init__()
        start = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [start]
        self.direction = (1, 0)
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def get_head_position(self):
        """Возвращает текущие координаты головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовывает змейку, включая затирание хвоста."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет направление движения, если задано следующее."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Вычисляет новую позицию головы и обновляет список сегментов."""
        self.update_direction()
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()
            else:
                self.last = None

    def reset(self):
        """Сбрасывает состояние змейки к начальному и очищает экран."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        start = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [start]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def main():
    """Основная функция: инициализация и бесконечный игровой цикл."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                handle_keys(event.key, snake)

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
