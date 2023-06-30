import pygame
from setting import *
from game import Game

pygame.init()

#ウィンドウの作成
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('shooting game')

#FPSの設定
clock = pygame.time.Clock()

#ゲーム
game = Game()

#メインループ=========================================================
run = True

while run:

  #背景の塗りつぶし
  screen.fill(Black)
  
  #ゲームの実行
  game.run()
  
  #イベントの取得
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        run = False
        
  #更新
  pygame.display.update()
  clock.tick(FPS)
  
#===================================================================
        
pygame.quit()




