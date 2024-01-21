import pygame
import sys
import random
import time

# Инициализация Pygame
pygame.init()

# Определение констант
WIDTH, HEIGHT = 800, 600
BIRD_SIZE = 45
PIPE_WIDTH = 50
PIPE_HEIGHT = random.randint(50, 350)
PIPE_GAP = 160
GRAVITY = 0.4
JUMP_HEIGHT = 6
WAIT_TIME = 0.5  # Время в секундах, в течение которого птица не двигается

# Определение цветов
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Летящая птичка")

# Загрузка изображений
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))
bird_flap = pygame.transform.rotate(bird_img, 20)  # Наклон птицы вверх
bird_fall = pygame.transform.rotate(bird_img, -10)  # Наклон птицы вниз
bird_rotation = 0  # Изначально угол наклона равен 0

pipe_img = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
pipe_img.fill(GREEN)

# Инициализация переменных
bird_x = WIDTH // 4
bird_y = HEIGHT // 2
bird_velocity = 0
pipes = [{"x": WIDTH, "height": random.randint(100, 300)}]
last_pipe_scored = None  # Последняя труба, через которую прошла птица
score = 0  # Начальное количество очков

# Определение времени начала движения птицы
start_time = time.time()

# Основной игровой цикл
clock = pygame.time.Clock()


def show_game_over():
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 3))

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (10, 10, 10))
    screen.blit(score_text, (WIDTH // 2 - 50, HEIGHT // 2))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and time.time() - start_time > WAIT_TIME:
                bird_velocity = -JUMP_HEIGHT

    # Проверка, должна ли птица двигаться
    if time.time() - start_time > WAIT_TIME:
        # Обновление позиции птицы с ускорением вниз
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Обновление угла наклона птицы в зависимости от скорости падения
        bird_rotation = min(bird_velocity * -3, 30)  # Ограничиваем угол вниз до 30 градусов

    # Генерация новых труб
    if pipes[-1]["x"] < WIDTH - PIPE_WIDTH - PIPE_GAP:
        new_pipe_height = random.randint(100, 300)
        pipes.append({"x": WIDTH, "height": new_pipe_height})

    # Движение труб
    for pipe in pipes:
        pipe["x"] -= 5

    # Удаление труб, которые вышли за пределы экрана
    pipes = [pipe for pipe in pipes if pipe["x"] > 0]

    # Проверка столкновений с трубами и краем экрана
    for pipe in pipes:
        if (
                bird_x < pipe["x"] + PIPE_WIDTH
                and bird_x + BIRD_SIZE > pipe["x"]
                and (bird_y < pipe["height"] or bird_y + BIRD_SIZE > pipe["height"] + PIPE_GAP)
        ):
            show_game_over()
            pygame.display.flip()
            pygame.time.delay(3000)  # Пауза на 2 секунды перед завершением
            pygame.quit()
            sys.exit()

    if bird_y < 0 or bird_y + BIRD_SIZE > HEIGHT:
        show_game_over()
        pygame.display.flip()
        pygame.time.delay(2000)  # Пауза на 2 секунды перед завершением
        pygame.quit()
        sys.exit()

    # Проверка прохождения птицей между трубами
    for pipe in pipes:
        if pipe["x"] < bird_x < pipe["x"] + PIPE_WIDTH and last_pipe_scored != pipe:
            score += 1
            last_pipe_scored = pipe  # Обновляем последнюю трубу, через которую прошла птица

    # Отрисовка
    screen.fill(WHITE)

    # Отображение птицы с учетом угла наклона
    if bird_velocity < 0:  # Если птица поднимается, использовать изображение с наклоном вверх
        rotated_bird = pygame.transform.rotate(bird_flap, bird_rotation)
    else:  # Если птица падает, использовать изображение с наклоном вниз
        rotated_bird = pygame.transform.rotate(bird_fall, bird_rotation)

    # Отрисовка птицы
    screen.blit(rotated_bird, (bird_x, bird_y))

    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe["x"], 0, PIPE_WIDTH, pipe["height"]))
        pygame.draw.rect(
            screen, GREEN, (pipe["x"], pipe["height"] + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe["height"] - PIPE_GAP)
        )

    # Отображение текущего счета
    font = pygame.font.Font(None, 54)
    text = font.render(f"{score}", True, (10, 10, 10))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(30)
