import pygame
import random
from setting import *
from player import Player
from enemy import Enemy
import support


class Game:
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
        
        #グループの作成
        self.create_group()
        
        #自機
        self.player = Player(self.player_group, 300, 500, self.enemy_group)
        
        #敵
        self.timer = 0
        
        #背景
        self.pre_bg_img = pygame.image.load('pygame1 shooting/assets/img/background/bg.png')
        self.bg_img = pygame.transform.scale(self.pre_bg_img,(screen_width,screen_height))
        self.bg_y = 0
        self.scroll_speed = 0.5
        
        #ゲームオーバー
        self.game_over = False
        
    def create_group(self):
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.Group()
        
    def create_enemy(self):
        self.timer += 1
        if self.timer > 50:
            enemy = Enemy(self.enemy_group, random.randint(50,550), 0, self.player.bullet_group)
            self.timer = 0
            
    def player_death(self):
        if len(self.player_group) == 0:
            self.game_over = True
            support.draw_text(self.screen, 'GameOver', screen_width // 2, screen_height // 2, 75, Red)
            support.draw_text(self.screen,'press SPACE to restart', screen_width // 2, screen_height // 2 + 100, 50, Red )
            
    def reset(self):
        key = pygame.key.get_pressed()
        if self.game_over and key[pygame.K_SPACE]:
            self.player = Player(self.player_group, 300, 500, self.enemy_group)
            self.enemy_group.empty()
            self.game_over = False
            
        
    def scroll_bg(self):
        self.bg_y = (self.bg_y + self.scroll_speed) % screen_height
        self.screen.blit(self.bg_img, (0, self.bg_y))
        self.screen.blit(self.bg_img, (0, self.bg_y - screen_height))

    def run(self):
        self.scroll_bg()
        
        self.create_enemy()
        
        self.player_death()
        self.reset()
        
        #グループの描画と更新
        self.player_group.draw(self.screen)
        self.player_group.update()
        self.enemy_group.draw(self.screen)
        self.enemy_group.update()
