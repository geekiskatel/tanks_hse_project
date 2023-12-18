# Импорт библиотеки для создания игр на Python
import pygame
# Импорт библиотеки random для случайной генерации препятствий
from random import randint

# Инициализация pygame
pygame.init()

# Ширина и Длина Окна с игрой
WIDTH, HEIGHT = 800, 600
# Кол-во кадров в секунду (так как расчет времени идет от этого значения,
# то при увеличении FPS будет увеличена скорость игры)
FPS = 60
# Размер области, которая выделяется под каждый объект
TILE = 32

# Создание окна
window = pygame.display.set_mode((WIDTH, HEIGHT))
# Отслеживание времени при создании объекта
clock = pygame.time.Clock()
# Загрузка шрифта по умолчанию
fontUI = pygame.font.Font(None, 30)
# Загрузка текстуры блоков
imgBrick = pygame.image.load('images/block_brick.png')
# Загрузка текстуры логотипа ВШЭ
imgHSE = pygame.image.load('images/HSE_Pixel.jpg')
# Загрузка текстуры танков на разных рангах
imgTanks = [pygame.image.load(f'images/tank{i}.png') for i in range(1, 9)]
# Загрузка текстуры взрыва, для создания анимации
imgBangs = [pygame.image.load(f'images/bang{i}.png') for i in range(1, 4)]
# Загрузка текстуры бонусов
imgBonuses = [
    pygame.image.load('images/bonus_star.png'),
    pygame.image.load('images/bonus_tank.png'),
]

# Загрузка звука выстрела
sound_shot = pygame.mixer.Sound("sounds/shot.wav")
# Загрузка звука разрушения
sound_destroy = pygame.mixer.Sound("sounds/destroy.wav")
# Загрузка звука подбора бонусов
sound_star = pygame.mixer.Sound("sounds/star.wav")
# Загрузка звука активации читов
sound_of_trolling = pygame.mixer.Sound("sounds/little_trolling.mp3")
# Загрузка звука смерти
sound_finish = pygame.mixer.Sound("sounds/death.mp3")
# Загрузка звука ремикса основной мелодии
sound_theme = pygame.mixer.Sound("sounds/main_theme_remix.mp3")

# Направления (Вверх, Вправо, Вниз, Влево)
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

# Значения скорости танка в зависимости от ранга
MOVE_SPEED = [1, 2, 2, 1, 2, 3, 3, 2]
# Значения скорости пули в зависимости от ранга
BULLET_SPEED = [4, 5, 6, 5, 5, 5, 6, 7]
# Значения урона пули в зависимости от ранга
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
# Значения скорости выстрела в зависимости от ранга
SHOT_DELAY = [60, 50, 30, 40, 30, 25, 25, 30]


class UI:
    """Class for displaying the user interface in the game.

    Methods:
        update(): Empty method, needed for compatibility.
        draw(): Draws UI elements on the game window.
    """

    # Без update() вылазит ошибка
    def update(self):
        """Updates the UI elements. (Currently does nothing)"""
        pass

    def draw(self):
        """Draws UI elements on the game window."""
        # Подсчитываем игроков
        i = 0
        # Перебираем все объекты
        for obj in objects:
            # Если объект имеет тип танк, то работаем с ним
            if obj.type == 'tank':
                # Берем цвет танка и выводим информацию по координатам
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))
                # Формирование текстового поля с данными об игроке (ранг)
                text = fontUI.render(str(obj.rank), 1, 'black')
                # Формирование позиции текста по центру
                rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                # Вывод самого текста (ранг)
                window.blit(text, rect)
                # Формирование текстового поля с данными об игроке (здоровье)
                text = fontUI.render(str(obj.hp), 1, obj.color)
                # Формирование позиции текста по центру
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                # Вывод самого текста (хп)
                window.blit(text, rect)
                # Чтобы каждый данные игрока отображались по координатам, иначе пропадет
                i += 1


class Tank:
    """Class representing a tank in the game.

    Attributes:
        color (str): Color of the tank.
        px (int): Horizontal position of the tank.
        py (int): Vertical position of the tank.
        direct (list): Direction the tank is facing.
        keyList (list): List of control keys for the tank.

    Methods:
        __init__(self, color, px, py, direct, keyList): Initializes a new tank instance.
        update(self): Updates the tank's state, including movement based on player input,
        direction facing, and shooting mechanics.
        draw(self): Draws the tank on the game window.
        damage(self, value): Applies damage to the tank and handles its destruction if health falls below zero.
    """

    def __init__(self, color, px, py, direct, keyList):
        """Initializes a tank with given parameters.

        Args:
            color (str): Color of the tank.
            px (int): Initial horizontal position of the tank.
            py (int): Initial vertical position of the tank.
            direct (list of int): Initial direction of the tank.
            keyList (list of int): Control keys for the tank.
        """
        # Занесение себя в список объектов
        objects.append(self)
        # Указание типа объекта, чтобы программа различала объекты
        self.type = 'tank'

        # Указание цвета
        self.color = color
        # Координаты
        self.rect = pygame.Rect(px, py, TILE, TILE)
        # Направление
        self.direct = direct
        # Здоровье
        self.hp = 5
        # Задержка между выстрелами
        self.shotTimer = 0

        # Указание кнопок с управлением
        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]
        self.keyCHEAT = keyList[5]

        # Начальный ранг танка
        self.rank = 0

    def update(self):
        """Updates the state of the tank, including its position, direction, and shooting parameters."""
        # Обновление модели танка в зависимости от ранга
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        # Обновление параметров танка по таблице рангов:
        # Скорость танка
        self.moveSpeed = MOVE_SPEED[self.rank]
        # Задержка выстрелов
        self.shotDelay = SHOT_DELAY[self.rank]
        # Скорость пули
        self.bulletSpeed = BULLET_SPEED[self.rank]
        # Урон пули
        self.bulletDamage = BULLET_DAMAGE[self.rank]
        # Сохранение старых координат, чтобы танк не проходил через блоки
        oldX, oldY = self.rect.topleft
        # Движение влево с учетом скорости и номером направления
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        # Движение вправо с учетом скорости и номером направления
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        # Движение вверх с учетом скорости и номером направления
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        # Движение вниз с учетом скорости и номером направления
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2
        # Активация читов
        elif keys[self.keyCHEAT]:
            # Получение максимального ранга
            self.rank = 7
            # Звук активации
            sound_of_trolling.play()
        # Перебор объектов для получения информации
        for obj in objects:
            # Если координаты танка и блока равны
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                # То вернуть его к старым значениям (будет стоять на месте,
                # так как не будет выполняться условие для его движения)
                self.rect.topleft = oldX, oldY

        # Выстрел (если кнопка нажата и ограничений нет)
        if keys[self.keySHOT] and self.shotTimer == 0:
            # Направление по Х с учетом скорости
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            # Направление по Y с учетом скорости
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            #  Вызов класса пули
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            # Создание задержки
            self.shotTimer = self.shotDelay
        # Постепенное снятие задержки
        if self.shotTimer > 0:
            self.shotTimer -= 1

    def draw(self):
        """Draws the tank on the game field."""
        window.blit(self.image, self.rect)

    def damage(self, value):
        """Applies damage to the tank and handles its destruction if necessary.

        Args:
            value (int): Amount of damage to be applied to the tank.
        Returns:
            None
        """
        # Отнимание здоровья
        self.hp -= value
        # Звук получения урона
        sound_destroy.play()
        # Если все ХП израсходованы
        if self.hp <= 0:
            # Удаление танка
            objects.remove(self)
            # Звук смерти танка
            sound_finish.play()


class Bullet:
    """Class representing a bullet in the game.

    Attributes:
        parent (Tank): The tank that fired the bullet.
        px (float): Horizontal position of the bullet.
        py (float): Vertical position of the bullet.
        dx (float): Horizontal velocity of the bullet.
        dy (float): Vertical velocity of the bullet.
        damage (int): Damage inflicted by the bullet.

    Methods:
        __init__(self, parent, px, py, dx, dy, damage): Initializes a new bullet instance.
        update(self): Updates the bullet's position and checks for collisions with other game objects.
        draw(self): Draws the bullet on the game window.
    """

    def __init__(self, parent, px, py, dx, dy, damage):
        """Initializes a new bullet with given parameters.

        Args:
            parent (Tank): The tank that fired the bullet.
            px (float): Initial horizontal position of the bullet.
            py (float): Initial vertical position of the bullet.
            dx (float): Horizontal velocity of the bullet.
            dy (float): Vertical velocity of the bullet.
            damage (int): Damage inflicted by the bullet.
        """
        # Добавление пули в объекты
        bullets.append(self)
        # Звук выстрела
        sound_shot.play()
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        """Updates the bullet's position and handles its collision and removal."""
        # Вектор по Х
        self.px += self.dx
        # Вектор по Y
        self.py += self.dy
        # Если пуля выходит за пределы окна, то удалить её
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        # Иначе после столкновения генерация взрыва
        else:
            # Перебор по объектам
            for obj in objects:
                # Если объект не танк не бонус и не взрыв
                if obj != self.parent and obj.type != 'bang' and obj.type != 'bonus':
                    # Проверка на сходство координат
                    if obj.rect.collidepoint(self.px, self.py):
                        # Нанесение урона
                        obj.damage(self.damage)
                        # Удаление пули
                        bullets.remove(self)
                        # Генерация взрыва
                        Bang(self.px, self.py)
                        # Прекратить сбор информации по циклу
                        break

    def draw(self):
        """Draws the bullet on the game window."""
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Bang:
    """Class representing an explosion in the game.

    Attributes:
        px (int): Horizontal position of the explosion.
        py (int): Vertical position of the explosion.

    Methods:
        __init__(self, px, py): Initializes a new explosion instance.
        update(self): Updates the explosion animation frame and removes the explosion after it ends.
        draw(self): Draws the explosion animation on the game window.
    """

    def __init__(self, px, py):
        """Initializes a new explosion with given parameters.

        Args:
            px (int): Horizontal position of the explosion.
            py (int): Vertical position of the explosion.
        """
        # Добавление себя в объекты
        objects.append(self)
        # Тип в объектах
        self.type = 'bang'
        # Указание координат взрыва
        self.px, self.py = px, py
        # Переменная для увеличения картинки
        self.frame = 0

    def update(self):
        # Увеличение фрейма до 3
        """Updates the state of the explosion, including its animation frame."""
        self.frame += 0.2
        # При 3 и более удаление объекта
        if self.frame >= 3:
            objects.remove(self)

    def draw(self):
        """Draws the explosion on the game window."""
        # Переменная с картинкой взрыва
        image = imgBangs[int(self.frame)]
        # Генерация координат
        rect = image.get_rect(center=(self.px, self.py))
        # Отрисовка картинки по координатам
        window.blit(image, rect)


class Block:
    """Class representing a block in the game.

    Attributes:
        px (int): Horizontal position of the block.
        py (int): Vertical position of the block.
        size (int): Size of the block.

    Methods:
        __init__(self, px, py, size): Initializes a new block instance.
        update(self): Currently does nothing (placeholder for future functionality).
        draw(self): Draws the block on the game window.
        damage(self, value): Applies damage to the block, potentially destroying it.
    """

    def __init__(self, px, py, size):
        """Initializes a new block with given parameters.

        Args:
            px (int): Horizontal position of the block.
            py (int): Vertical position of the block.
            size (int): Size of the block.
        """
        # Добавление в объекты
        objects.append(self)
        # Добавление типа
        self.type = 'block'
        # Указание координат
        self.rect = pygame.Rect(px, py, size, size)
        # Указания здоровья объекта
        self.hp = 1

    # Объект не обновляется и статичен (кроме уничтожения), но отсутствие update() вызовет ошибку
    def update(self):
        """Updates the block's state. (Currently does nothing)"""
        pass

    # Отрисовка блока
    def draw(self):
        """Draws the block on the game window."""
        window.blit(imgBrick, self.rect)

    def damage(self, value):
        """Applies damage to the block and handles its destruction if necessary.

        Args:
            value (int): Amount of damage to be applied to the block.
        Returns:
            None
        """
        # Отнятие хп у блока при попадании
        self.hp -= value
        # Если уничтожить - объект пропадет
        if self.hp <= 0:
            objects.remove(self)
        # Звук уничтожения
        sound_destroy.play()


class Bonus:
    """Class representing a bonus in the game.

    Attributes:
        px (int): Horizontal position of the bonus.
        py (int): Vertical position of the bonus.
        bonusnum (int): Type of the bonus.

    Methods:
        __init__(self, px, py, bonusnum): Initializes a new bonus instance.
        update(self): Handles the bonus timer and interactions with tanks.
        draw(self): Draws the bonus on the game window.
    """

    def __init__(self, px, py, bonusnum):
        """Initializes a new bonus with given parameters.

        Args:
            px (int): Horizontal position of the bonus.
            py (int): Vertical position of the bonus.
            bonusnum (int): Type of the bonus.
        """
        # Добавляет бонус в объекты
        objects.append(self)
        # Присваивание типа бонуса
        self.type = 'bonus'
        # Картинка из списка
        self.image = imgBonuses[bonusnum]
        # Создание координат
        self.rect = self.image.get_rect(center=(px, py))
        # Таймер (В ФПС)
        self.timer = 600
        # Сохранение номера бонуса
        self.bonusNum = bonusnum

    def update(self):
        """Updates the bonus state, including its timer and interaction with tanks."""
        # Пока таймер больше 0 уменьшает его
        if self.timer > 0:
            self.timer -= 1
        # Иначе он удаляется
        else:
            objects.remove(self)
        # Сбор информации об объектах
        for obj in objects:
            # Если объект танк и его координаты сходятся с бонусом
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                # Если бонус №0, то увеличивает ранг пока это возможно
                if self.bonusNum == 0 and obj.rank < len(imgTanks) - 1:
                    obj.rank += 1
                    objects.remove(self)
                    # Звук
                    sound_star.play()
                    break
                # Если бонус №1, то добавляет здоровье
                elif self.bonusNum == 1:

                    obj.hp += 1
                    objects.remove(self)
                    # Звук
                    sound_star.play()
                    break

    # Отрисовка объекта с условием в зависимости от времени таймера (будет мигать)
    def draw(self):
        """Draws the bonus on the game window."""
        if self.timer % 30 < 15:
            window.blit(self.image, self.rect)


class HSE:
    """Class representing the HSE logo in the game.

    Attributes:
        px (int): Horizontal position of the logo.
        py (int): Vertical position of the logo.
        size (int): Size of the logo.

    Methods:
        __init__(self, px, py, size): Initializes the HSE logo instance.
        update(self): Currently does nothing (placeholder for future functionality).
        draw(self): Draws the HSE logo on the game window.
    """

    def __init__(self, px, py, size):
        """Initializes the HSE logo with given parameters.

        Args:
            px (int): Horizontal position of the logo.
            py (int): Vertical position of the logo.
            size (int): Size of the logo.
        """
        # Добавление в объекты
        objects.append(self)
        # Добавление типа
        self.type = 'block_hse'
        # Указание координат объекта
        self.rect = pygame.Rect(px, py, size, size)

    # Объект не обновляется и статичен, но отсутствие update() вызовет ошибку
    def update(self):
        """Updates the state of the HSE logo. (Currently does nothing)"""
        pass

    # Отрисовка логотипа
    def draw(self):
        """Draws the HSE logo on the game window."""
        window.blit(imgHSE, self.rect)


# Здесь хранится информация о пулях
bullets = []
# Здесь хранятся все объекты, которые есть в игре
objects = []
# Создание танка_1 (WASD SPACE 6)
Tank('blue', 100, 275, 0, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE, pygame.K_6])
# Создание танка_2 (Стрелочки BACKSPACE 9)
Tank('red', 650, 275, 0, [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_BACKSPACE, pygame.K_9])
# Проигрывание основной мелодии во время игры
sound_theme.play()
# Этот объект будет обновлять данные в пользовательском интерфейсе
ui = UI()

# Цикл для создания блоков в случайном месте, кроме координат с другими объектами 50 раз
for _ in range(50):
    while True:
        # Генерация координат по Х
        x = randint(0, WIDTH // TILE - 1) * TILE
        # Генерация координат по Y (верхний ряд не будет задействован)
        y = randint(1, HEIGHT // TILE - 1) * TILE
        # Отрисовка по координатам
        rect = pygame.Rect(x, y, TILE, TILE)
        # Флаг для условия, чтобы не было отрисовки на других объектах
        fined = False
        # Цикл проверки координат будущего блока с координатами существующих объектов
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined = True
        # Если генерация произошла на координатах UI, то отменить
        if not fined:
            break
    # Вызвать функцию блока, если все прошло
    Block(x, y, TILE)
# Создание логотипа на поле боя (в нем можно спрятаться и нельзя сломать)
HSE(770, 1, 1)
# Стартовое значения интервала времени для подбора бонусов
bonusTimer = 180
# Шаблон запуска игры на pygame
play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    # Проверка нажатия клавиш для управления в иге
    keys = pygame.key.get_pressed()
    # Уменьшение времени
    if bonusTimer > 0:
        bonusTimer -= 1
    else:
        # Генерация новых бонусов
        Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(imgBonuses) - 1))
        # Генерация случайного интервала времени
        bonusTimer = randint(120, 240)
    # Обновление статусов пуль в игре
    for bullet in bullets:
        bullet.update()
    # Обновление статусов объектов
    for obj in objects:
        obj.update()
    # Обновление счетчика жизней и отображение рангов
    ui.update()
    # Окраска фона игры в черный
    window.fill('black')
    # Отрисовка пуль
    for bullet in bullets:
        bullet.draw()
    # Отрисовка объектов
    for obj in objects:
        obj.draw()
    # Отрисовка интерфейса
    ui.draw()

    # Шаблон pygame
    pygame.display.update()
    clock.tick(FPS)
# Шаблон pygame
pygame.quit()
