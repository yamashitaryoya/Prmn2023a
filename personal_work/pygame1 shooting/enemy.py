import pygame
from setting import *
import random
from explosion import Explosion

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, x, y,bullet_group):
        super().__init__(groups)
        
        self.screen = pygame.display.get_surface()
        
        #グループ
        self.bullet_group = bullet_group
        self.explosion_group = pygame.sprite.Group()

        #画像
        self.image_list = []
        for i in range(5):
            image = pygame.image.load(f'pygame1 shooting/assets/img/enemy/{i}.png')
            self.image_list.append(image)

        self.index = 0
        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(self.pre_image, (50, 50))
        self.rect = self.image.get_rect(center = (x, y))

        #移動
        move_list = [1, -1]
        self.direction = pygame.math.Vector2((random.choice(move_list), 1))
        self.speed = 1
        self.timer = 0
        
        #体力
        self.health = 3
        self.alive = True
        
        #爆発
        self.explosion = False

    def move(self):
        self.timer += 1
        if self.timer > 80:
            self.direction.x *= -1
            self.timer = 0

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def animation(self):
        if self.alive:
            self.index += 0.15
            if self.index > len(self.image_list):
                self.index = 0

            self.pre_image = self.image_list[int(self.index)]
            self.image = pygame.transform.scale(self.pre_image, (50, 50))
            
        else:
            self.image.set_alpha(0)

    def check_off_screen(self):
        if self.rect.top > screen_height:
            self.kill()
            
    def collision_bullet(self):
        for bullet in self.bullet_group:
            if self.rect.colliderect(bullet.rect):
                bullet.kill()
                self.health -= 1
                
        if self.health <= 0:
            self.alive = False
            
    def check_death(self):
        if self.alive == False and self.explosion == False:
            self.speed = 0
            explosion = Explosion(self.explosion_group, self.rect.centerx, self.rect.centery)
            self.explosion = True
        
        if self.explosion and len(self.explosion_group) == 0:
            self.kill()            
        

    def update(self):
        self.move()
        self.check_off_screen()
        self.animation()
        self.collision_bullet()
        self.check_death()
        
        #グループの描画と交信
        self.explosion_group.draw(self.screen)
        self.explosion_group.update()