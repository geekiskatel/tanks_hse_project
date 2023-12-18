import pytest
import pygame
from main import Bullet, Block, Tank, Bang


# Проверка правильного перемещения пуль
def test_bullet_update_position():
    pygame.init()
    bullet = Bullet(None, 100, 100, 5, 0, 1)
    bullet.update()
    assert bullet.px == 105
    pygame.quit()


# Негативный тест для проверки скорости пули
def test_bullet_update_position_negative():
    pygame.init()
    bullet = Bullet(None, 100, 100, 5, 0, 1)
    bullet.update()
    assert bullet.px < 106
    pygame.quit()


# Проверка позитивного исхода при нанесении урона боку
def test_block_damage():
    pygame.init()
    block = Block(100, 100, 32)
    block.damage(1)
    assert block.hp == 0
    pygame.quit()


# Проверка позитивного исхода при нанесении урона танку
def test_damage_tank_positive():
    pygame.init()
    tank = Tank('blue', 100, 100, 0, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE, pygame.K_6])
    initial_hp = tank.hp
    tank.damage(1)
    assert tank.hp == initial_hp - 1
    pygame.quit()


# Проверка негативного исхода при нанесении урона танку
def test_damage_tank_negative():
    pygame.init()
    tank = Tank('blue', 100, 100, 0, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE, pygame.K_6])
    initial_hp = tank.hp
    tank.damage(1)
    assert not tank.hp == initial_hp   # Проверка, что здоровье танка уменьшилось на 1
    pygame.quit()


# Проверка корректности обновления фрейма
def test_bang_update():
    pygame.init()
    bang = Bang(100, 100)
    initial_frame = bang.frame
    bang.update()
    assert bang.frame > initial_frame  # Проверка, что кадр анимации взрыва увеличился
    pygame.quit()
    

# Запускаем все тесты одновременно
if __name__ == "__main__":
    pytest.main()
