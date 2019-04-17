import random
import pygame

# 屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 600)
# 刷新频率
FRAME_PER_SEC = 60
# 创建敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 创建发射子弹常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprites(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, images_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(images_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在垂直方向上移动
        self.rect.y += self.speed


class Ground(GameSprites):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        super().__init__('./images/background.png')
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        # 调用父类的update
        super().update()
        # 判断图片是否到底部
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprites):
    """敌机精灵"""

    def __init__(self):
        super().__init__('./images/enemy1.png')
        # 随机初始化位置
        self.rect.bottom = 0  # y方向
        max_x = SCREEN_RECT.width - self.rect.width  # x方向最大宽度
        self.rect.x = random.randint(0, max_x)
        # 随机初始速度
        self.speed = random.randint(1, 3)

    def update(self):
        super().update()
        # 到底部就在精灵组中删除
        if self.rect.y >= SCREEN_RECT.height:
            # print('删除敌机')
            self.kill()


"""(个人想法)
        # for i in range(1, 3):
        #     if i == random.randint(1, 2):
        #         if i == 1:
        #             self.rect.x += 10
        #             if self.rect.x >= SCREEN_RECT.width - self.rect.width:
        #                 self.rect.x = SCREEN_RECT.width - self.rect.width
        #             elif self.rect.x <= 0:
        #                 self.rect.x = 0
        #         elif i == 2:
        #             self.rect.x -= 10
        #             if self.rect.x >= SCREEN_RECT.width - self.rect.width:
        #                 self.rect.x = SCREEN_RECT.width - self.rect.width
        #             elif self.rect.x <= 0:
        #                 self.rect.x = 0"""


class Hero(GameSprites):
    """英雄精灵"""

    def __init__(self):
        super().__init__('./images/me1.png', 0)
        # 重写英雄位置信息
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 90
        # 定义子弹精灵组
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > SCREEN_RECT.width:
            self.rect.right = SCREEN_RECT.width

    def fire(self):
        print('开火...')
        for i in range(3):
            # 定义子弹精灵
            bullet = Bullet()
            self.bullet_group.add(bullet)
            # 子弹y位置
            bullet.rect.bottom = self.rect.y - i * 20
            # 子弹x位置
            bullet.rect.centerx = self.rect.centerx


class Bullet(GameSprites):
    """子弹精灵"""

    def __init__(self):
        super().__init__('./images/bullet1.png', -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print('子弹消失...')
