import os
import sys
import math
import random
import pygame

WIDTH = 623
HEIGHT = 150

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")


class BG:
    def __init__(self, x):
        self.width = WIDTH
        self.height = HEIGHT
        self.x = x
        self.y = 0
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx
        if self.x <= -WIDTH:
            self.x = WIDTH

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join("assets/images/bg.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Dino:
    def __init__(self):
        self.width = 44
        self.height = 44
        self.x = 10
        self.y = 80
        self.texture_num = 0
        self.dy = 2.6
        self.gravity = 1.2
        self.onground = True
        self.jumping = False
        self.jump_stop = 10
        self.falling = False
        self.fall_stop = self.y
        self.set_texture()
        self.show()

    def update(self, loops):
        # dino jump
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()

        # dino onground after jump
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fall_stop:
                self.stop()

        # dino moving(running)
        elif self.onground and loops % 4 == 0:
            self.texture_num = (self.texture_num + 1) % 3
            self.set_texture()

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join(f"assets/images/dino{self.texture_num}.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def jump(self):
        self.jumping = True
        self.onground = False

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop(self):
        self.falling = False
        self.onground = True


class Cactus:
    def __init__(self, x):
        self.width = 34
        self.height = 44
        self.x = x
        self.y = 80
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx

    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def set_texture(self):
        path = os.path.join("assets/images/cactus.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Collision:
    def between(self, obj1, obj2):
        distance = math.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2)
        return distance < 35


class Score:
    def __init__(self, hs):
        self.hs = hs
        self.act = 0
        self.font = pygame.font.SysFont("monospace", 20)
        self.color = (0, 0, 0)
        self.show()

    def update(self, loops):
        self.act = loops // 10
        self.check_hs()

    def show(self):
        self.lbl = self.font.render(f"HI {self.hs} {self.act}", 1, self.color)
        lbl_width = self.lbl.get_rect().width
        screen.blit(self.lbl, (WIDTH - lbl_width - 10, 10))

    def check_hs(self):
        if self.act >= self.hs:
            self.hs = self.act


class Game:
    def __init__(self):
        self.bg = [BG(x=0), BG(x=WIDTH)]
        self.dino = Dino()
        self.obstacles = []
        self.collision = Collision()
        self.score = Score(hs=0)
        self.speed = 3
        self.playing = False

    def start(self):
        self.playing = True

    def over(self):
        self.playing = False

    def tospawn(self, loops):
        return loops % 100 == 0

    def spawn_cactus(self):
        # list with cactus
        if len(self.obstacles) > 0:
            prev_cactus = self.obstacles[-1]
            # 44 pixels is width of dino
            # 84 pixels is random value for dino to jump between two cactus without dying
            x = random.randint(
                prev_cactus.x + self.dino.width + 130,
                WIDTH + prev_cactus.x + self.dino.width + 100,
            )
        else:
            x = random.randint(WIDTH + 100, 1000)

        # create new cactus
        cactus = Cactus(x)
        self.obstacles.append(cactus)


def main():
    # Objects
    game = Game()
    dino = game.dino

    clock = pygame.time.Clock()

    loops = 0

    while True:
        if game.playing:
            loops += 1

            # Code to display Background
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()

            # Code to display Dino
            dino.update(loops)
            dino.show()

            # Code to display Cactus
            if game.tospawn(loops):
                game.spawn_cactus()

            for cactus in game.obstacles:
                cactus.update(-game.speed)
                cactus.show()

                # logic for collisions
                if game.collision.between(dino, cactus):
                    game.over()

            # score
            game.score.update(loops)
            game.score.show()

        for event in pygame.event.get():
            # end the game on clicking quit button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if dino.onground:
                        dino.jump()

                    if not game.playing:
                        game.start()

        clock.tick(120)
        pygame.display.update()


main()
