from plane_sprites import *


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        """初始化"""
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        # 创建背景精灵和组
        bg_sprites = Ground()
        bg_sprites1 = Ground(True)
        self.back_ground = pygame.sprite.Group(bg_sprites, bg_sprites1)

        # 创建敌机机灵组，因为敌机是定时启动的不再此创建
        self.enemy_ground = pygame.sprite.Group()

        # 创建英雄精灵和组
        self.hero = Hero()  # 下面要用，所以定义成属性
        self.hero_ground = pygame.sprite.Group(self.hero)

    def start_game(self):
        print('游戏开始...')
        while True:
            # 刷新频率
            self.clock.tick(FRAME_PER_SEC)
            # 事件检测
            self.__even_handler()
            # 碰撞检测
            self.__check_collide()
            # 更新精灵组
            self.__sprites_update()
            # 更新画面
            pygame.display.update()

    def __even_handler(self):
        # 便利事件列表
        for even in pygame.event.get():
            # 捕获退出按钮
            if even.type == pygame.QUIT:
                PlaneGame.__game_over()
            # 定时器，来生成敌机
            elif even.type == CREATE_ENEMY_EVENT:
                # print('敌机来了')
                enemy = Enemy()
                self.enemy_ground.add(enemy)
            # 监听子弹定时器
            elif even.type == HERO_FIRE_EVENT:
                self.hero.fire()
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_RIGHT]:
            self.hero.speed = 5
        elif key_press[pygame.K_LEFT]:
            self.hero.speed = -5
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 子弹与敌机碰撞
        pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_ground, True, True)
        # 英雄与敌机碰撞
        collide = pygame.sprite.spritecollide(self.hero, self.enemy_ground, True)
        if len(collide) > 0:
            self.hero.kill()
            PlaneGame.__game_over()

    def __sprites_update(self):
        # 背景精灵组更新
        self.back_ground.update()
        self.back_ground.draw(self.screen)

        # 敌机精灵组更新
        self.enemy_ground.update()
        self.enemy_ground.draw(self.screen)

        # 英雄精灵组更新
        self.hero_ground.update()
        self.hero_ground.draw(self.screen)

        # 子弹精灵组更新
        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print('游戏结束...')
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()
