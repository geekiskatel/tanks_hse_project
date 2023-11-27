import pytest
import pygame
from main import Tank, Bullet, Block, Bonus

class TestTank:
    @pytest.fixture
    def tank(self):
        pygame.init()
        return Tank('blue', 100, 275, 0, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE, pygame.K_6])

    def test_damage_tank_positive(self, tank):
        initial_hp = tank.hp
        tank.damage(1)
        # Проверят, что при нанесении урона 1, отнимается 1 хп
        assert tank.hp == initial_hp - 1

    def test_damage_tank_negative(self, tank):
        initial_hp = tank.hp
        tank.damage(1)
        # Проверят, что при нанесении урона 1, здоровье остается прежним
        assert not tank.hp == initial_hp


class TestBullet:
    @pytest.fixture
    def bullet(self):
        pygame.init()
        tank = Tank('blue', 100, 275, 0, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE, pygame.K_6])
        return Bullet(tank, 100, 275, 5, 0, 1)

    def test_initialization(self, bullet):
        assert bullet.px == 100
        assert bullet.py == 275
        assert bullet.dx == 5
        assert bullet.dy == 0
        assert bullet.damage == 1


class TestBlock:
    @pytest.fixture
    def block(self):
        return Block(100, 100, 32)

    def test_damage_block_positive(self, block):
        initial_hp = block.hp
        block.damage(1)
        assert block.hp == initial_hp - 1

    def test_damage_block_negative(self, block):
        initial_hp = block.hp
        block.damage(1)
        assert not block.hp == initial_hp


class TestBonus:
    @pytest.fixture
    def bonus(self):
        return Bonus(100, 100, 0)

    def test_initialization(self, bonus):
        assert bonus.rect.center == (100, 100)
        assert bonus.bonusNum == 0


if __name__ == "__main__":
    pytest.main()