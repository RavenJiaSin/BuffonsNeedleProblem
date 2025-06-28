import os
import pygame

# 畫面設定
WIDTH, HEIGHT = 1000, 700
DRAW_AREA_HEIGHT = 480

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# 字型載入
FONT_PATH = os.path.join("assets", "msjh.ttc")
pygame.font.init()
FONT = pygame.font.Font(FONT_PATH, 20)
