import pygame
from setting import *
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    
    def __init__(self, groups, x, y, enemy_group):
        super().__init__(groups)
        
        self.screen = pygame.display.get_surface()
        
        #グループ
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = enemy_group
        
        #画像
        self.image_list = []
        for i in range(3):
            image = pygame.image.load(f'pygame1 shooting/assets/img/player/{i}.png')
            self.image_list.append(image)
            
        self.index = 0 #０：正面　１：左　２：右
        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(self.pre_image,(50,50))
        self.rect = self.image.get_rect(center = (x,y))
        
        #移動
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
        #弾
        self.fire = False
        self.timer = 0
        
        #体力
        self.health = 1
        self.alive = True
        
    def input(self):
        key = pygame.key.get_pressed()
        
        if key[pygame.K_UP] == 1:
            self.direction.y = -1
        elif key[pygame.K_DOWN] == 1:
            self.direction.y = 1
        else:
            self.direction.y = 0
            
        if key[pygame.K_LEFT] == 1:
            self.direction.x = -1
            self.index = 1
        elif key[pygame.K_RIGHT] == 1:
            self.direction.x = 1
            self.index = 2
        else:
            self.direction.x = 0
            self.index = 0
            
        if key[pygame.K_z] == 1 and self.fire == False:
            bullet = Bullet(self.bullet_group, self.rect.centerx, self.rect.top)
            self.fire = True
            
            
    def cooldown_bullet(self):
        if self.fire == True:
            self.timer += 1
        if self.timer > 10:
            self.fire = False
            self.timer = 0
             
            
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        
        self.rect.x += self.direction.x * self.speed
        self.check_off_screen('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.check_off_screen('vertical')
        
    def check_off_screen(self,direction):
        if direction == 'horizontal':
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > screen_width:
                self.rect.right = screen_width
                
        if direction == 'vertical':
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                
    def collision_enemy(self):
        for enemy in self.enemy_group:
            if self.rect.colliderect(enemy.rect) and enemy.alive:
                self.health -= 1
                
        if self.health <= 0:
            self.alive = False
            
    def check_death(self):
        if self.alive == False:
            self.kill()
                
            
    def update_image(self):
        self.pre_image = self.image_list[self.index]
        self.image = pygame.transform.scale(self.pre_image,(50,50))
        

    def update(self):
        self.input()
        self.move()
        self.update_image()
        self.cooldown_bullet()
        self.collision_enemy()
        self.check_death()
        
        #グループの描画と更新
        self.bullet_group.draw(self.screen)
        self.bullet_group.update()
        
