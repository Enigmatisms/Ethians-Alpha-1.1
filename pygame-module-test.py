#-*-coding:utf-8-*-
#test module for the pygame
import sys, os, random, pygame, time, datetime
import numpy as np
from datetime import datetime
from pygame.locals import *
from ezplot import *
from house_room import *
from ply import *
from mist import *
from keysets import keySets
from npcs import *
pygame.init()
pygame.key.set_repeat(480,30)
#defaults
black=(0, 0, 0)
white=(255, 255, 255)
gray=(128,128,128)
de_size=(1200, 650)
screen=pygame.display.set_mode(de_size, 0, 32)
path=os.path.join('c:\\','Windows','Fonts','msyh.ttc')
font=pygame.font.Font(path, 24)
text=font.render('测试用字体，一二三四五六七八九十，何千越，杀死，龖翙乀', True, (255, 255, 255))
#复制粘贴到此处之下
#Probable preparation of the test
#============================================================================
#Preparation lines:
back=pygame.image.load(r'asset\back.png').convert_alpha()
rect=Rect(100, 100, 400, 400)

framerate = pygame.time.Clock()
#============================================================================

s=pygame.Surface((1200, 650))
s.fill(black)

def loopSetter(num):
    print("Now in the loop of: %d"%num)

ks=keySets(screen, loopSetter)

#=============预处理===============
ks.loadPreference()
ks.init()
ks.drawSurface()

#main loop lines
while True:
    framerate.tick(80)
    ticks = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            if not ks.listen:
                if event.key==K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key==K_UP:
                    ks.previous()
                elif event.key==K_DOWN:
                    ks.nextOne()
                elif event.key==K_LEFT:
                    ks.goLeft()
                elif event.key==K_RIGHT:
                    ks.goRight()
                elif event.key==K_RETURN:
                    ks.enterKey()
            else:
                ks.putKey(event.key)
                ks.listen=False
                ks.updateKey()
            ks.drawSurface()
    ks.drawInds(ticks)
    pygame.display.update()



    #The modules to be tested are as follows
    #================================================================================
    #Test Section:

    
#============================================================================
