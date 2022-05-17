import pygame
import random

# инициализирует pygame
pygame.init()
# создает экран размером 1280 на 720 и обновляет его
width = 1280
height = 720
display = pygame.display.set_mode((width, height))
pygame.display.update()
pygame.display.set_caption("Snakee game by Vader")
# задаем цвета:
colors = {
    "snake_head": (0, 255, 0),  # головы змеи
    "snake_tail": (0, 200, 0),  # хвоста змеи
    "apple": (255, 0, 0)  # еды
}
# размер змейки
SIZE_SNAKE = 10
# размер еды (лучше чтобы был больше размера змейки)
SIZE_FOOD = 20
# скорость змейки
SPEED = 10

# положение змеи со смещениям
snake_pos = {
    "x": width / 2 - SIZE_SNAKE,
    "y": height / 2 - SIZE_SNAKE,
    "x_change": 0,
    "y_change": 0
}
# размер змейки
snake_size = (SIZE_SNAKE, SIZE_SNAKE)
# скорость движения змеи (задается выше)
snake_speed = SPEED
# массив частей змейки
snake_tails = []
# задаем направление движения змейки на старте
snake_pos["x_change"] = -snake_speed
# создаем 10 частей змейки
for i in range(10):
    snake_tails.append([snake_pos["x"] + SIZE_SNAKE * i, snake_pos["y"]])

# размер еды
food_size = (SIZE_FOOD, SIZE_FOOD)

# еда (случайное положение на экране)
food_pos = {
            "x": round(random.randrange(0, width - food_size[0]) / SIZE_FOOD) * SIZE_FOOD,
            "y": round(random.randrange(0, height - food_size[1]) / SIZE_FOOD) * SIZE_FOOD,
}

# счетчик съеденной еды
food_eaten = 0
# начало игрового цикла
game_end = False
clock = pygame.time.Clock()

while not game_end:
    # игровой цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # если событие выхода -> выходим
            game_end = True
        elif event.type == pygame.KEYDOWN:  # если нажата клавиша
            if event.key == pygame.K_LEFT and snake_pos["x_change"] == 0:
                #  движени влево
                snake_pos["x_change"] = -snake_speed
                snake_pos["y_change"] = 0  # по вертикали не смещаем!!!
            elif event.key == pygame.K_RIGHT and snake_pos["x_change"] == 0:
                # движение вправо
                snake_pos["x_change"] = snake_speed
                snake_pos["y_change"] = 0  # по вертикали не смещаем!!!
            elif event.key == pygame.K_UP and snake_pos["y_change"] == 0:
                # движение вверх
                snake_pos["x_change"] = 0  # по горизонтали не смещаем!!!
                snake_pos["y_change"] = -snake_speed
            elif event.key == pygame.K_DOWN and snake_pos["y_change"] == 0:
                # движение вниз
                snake_pos["x_change"] = 0  # по горизонтали не смещаем!!!
                snake_pos["y_change"] = snake_speed
    # очищаем экран
    display.fill((0, 0, 0))
    # перемещение частей змейки
    ltx = snake_pos["x"]
    lty = snake_pos["y"]
    for i, v in enumerate(snake_tails):
        _ltx = snake_tails[i][0]
        _lty = snake_tails[i][1]
        snake_tails[i][0] = ltx
        snake_tails[i][1] = lty
        ltx = _ltx
        lty = _lty
    # рисуем части змейки
    for t in snake_tails:
        pygame.draw.rect(display, colors["snake_tail"], [
            t[0],
            t[1],
            snake_size[0],
            snake_size[1]])
    # перемещение змейки
    snake_pos["x"] += snake_pos["x_change"]
    snake_pos["y"] += snake_pos["y_change"]
    # телепортируем змейку при выходе за пределы экрана
    if (snake_pos["x"] < -snake_size[0]):
        snake_pos["x"] = width
    elif (snake_pos["x"] > width):
        snake_pos["x"] = 0
    elif (snake_pos["y"] < -snake_size[1]):
        snake_pos["y"] = height
    elif (snake_pos["y"] > height):
        snake_pos["y"] = 0
    # рисуем змейку
    pygame.draw.rect(display, colors["snake_head"], [
        snake_pos["x"],
        snake_pos["y"],
        snake_size[0],
        snake_size[1]])
    # рисуем еду
    pygame.draw.rect(display, colors["apple"], [
        food_pos["x"],
        food_pos["y"],
        food_size[0],
        food_size[1]])
    # проверяем столкновение с едой
    if (abs(snake_pos["x"] - food_pos["x"]) <= abs(SIZE_SNAKE - SIZE_FOOD)
and abs(snake_pos["y"] - food_pos["y"]) <= abs(SIZE_SNAKE - SIZE_FOOD)):
        # увеличиваем счетчик съеденной еды
        food_eaten += 1
        # добавляем ячейку тела змейки
        snake_tails.append([food_pos["x"], food_pos["y"]])
        # создаем новую еду
        food_pos = {
            "x": round(random.randrange(0, width - food_size[0]) / SIZE_FOOD) * SIZE_FOOD,
            "y": round(random.randrange(0, height - food_size[1]) / SIZE_FOOD) * SIZE_FOOD,
        }
    # проверяем столкновение с телом
    for i, v in enumerate(snake_tails):
        if (snake_pos["x"] + snake_pos["x_change"] == snake_tails[i][0]
                and snake_pos["y"] + snake_pos["y_change"] == snake_tails[i][1]):
            # обрезаем змейку
            snake_tails = snake_tails[:i]
            break
        # обновляем экран
    pygame.display.update()
    # FPS кадры в секунду
    clock.tick(30)

# выводим количество съеденных яблок
print(food_eaten)

# закрываем если конец
pygame.quit()
quit()
