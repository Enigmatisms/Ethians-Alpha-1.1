#!/usr/bin/env python3
#-*-coding:utf-8-*-


import pygame, time, sys
from pygame.locals import *

class Quitting:
    def __init__(self, surface):
        self.screen=surface
        self.hq=None
        self.svt=None
        self.ptr=None
        self.slt=None           #只为了设置在mainMenu函数触发时，跳出的界面问题
        self.quitBk=pygame.image.load(r'asset/quitBk.png').convert_alpha()
        self.covButton=pygame.image.load(r'asset/covQuit.png').convert_alpha()
        self.btList=[0,0,0]
        self.rectList=[Rect(260+238*i, 280, 208, 124) for i in range(3)]
        self.funcList=[self.mainMenu, self.resume, self.quitGame]
        self.loopNum=4

    def mousePrep(self):
        x, y=pygame.mouse.get_pos()
        for i in range(3):
            if self.rectList[i].collidepoint(x, y):
                self.btList[i]=1
            else:
                self.btList[i]=0

    def mouseJudge(self):
        x, y = pygame.mouse.get_pos()
        for i in range(3):
            if self.rectList[i].collidepoint(x, y):
                self.screen.blit(self.covButton, self.rectList[i].topleft)
                self.screen.blit(self.covButton, self.rectList[i].topleft)
                self.funcList[i]()
                pygame.display.update()
                time.sleep(0.2)
                return

    def drawButton(self, x, y):
        self.screen.blit(self.quitBk, (x, y))
        for i in range(3):
            if self.btList[i]:
                self.screen.blit(self.covButton, self.rectList[i].topleft)

    def mainMenu(self):
        self.slt.gameStart=False
        self.slt.careerSet=False
        self.slt.creator = False
        self.slt.setting = False
        self.slt.monu = False
        if self.loopNum !=4 :
            self.svt.saveGamer(self.ptr)
        self.hq.set_loop(4)

    def resume(self):
        self.hq.set_loop(self.loopNum)

    def quitGame(self):
        if self.loopNum !=4 :       #不是主菜单时才能保存游戏
         self.svt.saveGamer(self.ptr)
        pygame.quit()
        sys.exit()





