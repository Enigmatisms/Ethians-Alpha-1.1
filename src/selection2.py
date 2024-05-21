import os
#-*-coding:utf-8-*-
#!/usr/bin/env python3
import pygame, time
from src.ezplot import MySprite
from pygame.locals import *

class Selection:
    def __init__(self, surface):
        self.screen=surface
        self.hq=None
        self.ptr=None
        self.svt=None   #saveit模块
        self.skillBk=pygame.image.load(os.path.join("asset", "skills.png")).convert()
        self.careerBk=pygame.image.load(os.path.join("asset", "career.png")).convert()
        self.menuBk=pygame.image.load(os.path.join("asset", "menu.png")).convert()
        self.covSkill=MySprite()
        self.covCareer=MySprite()
        self.covMenu=MySprite()
        self.covSkill.load(os.path.join("asset", "mantle.png"), 0, 0, 204, 590, 3)
        self.covCareer.load(os.path.join("asset", "mantle2.png"), 0, 0, 344, 566, 3)
        self.covMenu.load(os.path.join("asset", "mantle3.png"), 0, 0, 204, 490, 5)
        self.covSkill.Y, self.covCareer.Y = 30, 42
        self.mantle=None
        self.bk=None
        self.creatorLoaderFunc=None         #游戏开发者信息的外部辅助函数传入准备
        self.careerSet=False
        self.gameStart=False
        #======模式标签======
        self.creator=False
        self.setting=False
        self.monu=False
        #==================
        self.record=None
        self.btList=[]          #遮罩层是否显示？
        self.rectList=[]
        self.funcList=[]
        self.length=0
        self.mode=0

    def skillSelect(self):          #技能点设置
        self.mode=1
        self.mantle=self.covSkill
        self.bk=self.skillBk
        self.btList=[-1, -1, -1, -1, -1]
        self.length=5
        self.rectList.clear()
        for i in range(5):
            self.rectList.append(Rect(30+234*i, 30, 204, 590))
        self.skillFuncs()

    def careerSelect(self):         #职业设置
        self.mode = 2
        self.gameStart = True
        self.mantle = self.covCareer
        self.bk = self.careerBk
        self.btList = [-1, -1, -1]
        self.length=3
        self.rectList.clear()
        for i in range(3):
            self.rectList.append(Rect(42+386*i, 42, 344, 566))
        self.careerFuncs()
        return True

    def menuSelect(self):
        self.mode = 0
        self.mantle=self.covMenu
        self.bk=self.menuBk
        self.btList=[-1,-1,-1,-1,-1]
        self.length=5
        self.rectList.clear()
        for i in range(5):
            self.rectList.append(Rect(30+234*i, 130, 204, 490))
        self.menuFuncs()


    def mousePrep(self):
        x, y = pygame.mouse.get_pos()
        if self.mode:
            for i in range(self.length):
                if self.rectList[i].collidepoint(x, y):
                    self.btList[i] = 0
                else:
                    self.btList[i] = -1
        else:
            for i in range(self.length):
                if self.rectList[i].collidepoint(x, y):
                    self.btList[i] = i
                else:
                    self.btList[i] = -1

    def mouseJudge(self):
        x, y = pygame.mouse.get_pos()
        for i in range(self.length):
            if self.rectList[i].collidepoint(x, y):
                self.mantle.X, self.mantle.Y=self.rectList[i].topleft
                if self.mode: num=1         #信息绘制的帧数
                else: num=i
                self.mantle.frame=self.mantle.last_frame=num
                self.mantle.update(0)
                self.mantle.draw(self.screen)
                if not self.mode:      #双层绘制
                    self.mantle.draw(self.screen)
                if self.mode:       #游戏内的按钮会触发跳转至loop1的事件
                    self.hq.set_loop(1)
                judge=self.funcList[i]()
                if not judge:
                    self.mantle.frame=self.mantle.last_frame=self.mantle.columns-1
                    self.mantle.draw(self.screen)
                    self.mantle.draw(self.screen)
                pygame.display.update()
                time.sleep(0.2)
                break

    def drawButton(self):           #绘制按钮遮罩层
        for i in range(self.length):
            if self.btList[i]>=0:
                self.mantle.X, self.mantle.Y = self.rectList[i].topleft
                self.mantle.frame = self.mantle.last_frame = self.btList[i]
                self.mantle.update(0)
                self.mantle.draw(self.screen)

    def skillFuncs(self):           #技能选择模块的按键功能
        def func():
            self.ptr.maxhp_adder()
            self.ptr.hp_adder()
            self.hq.set_loop(1)
        self.funcList=[self.funcFix(self.ptr.atk_adder), self.funcFix(self.ptr.def_adder),
                       self.funcFix(self.ptr.magic_adder), self.funcFix(self.ptr.speed_adder), func]

    def partial(self, arg):         #偏函数
        def f():
            self.svt.deathJudge = False
            self.careerSet=True
            self.ptr.career_setup(arg)
            self.svt.saveGamer(self.ptr)            #初始化玩家之后要立即保存
            self.hq.set_loop(1)
            return True
        return f

    def funcFix(self, func):            #hq补充函数
        def f():
            func()
            self.hq.set_loop(1)
            return True
        return f

    def careerFuncs(self):          #职业选择按钮功能
        self.funcList=[self.partial(0), self.partial(1), self.partial(2)]

    def menuFuncs(self):            #主菜单
        self.funcList=[self.careerSelect, self.recordLoader, self.creatorLoader,
                       self.monuLoader, self.go2Setting]

    def go2Setting(self):
        self.hq.set_loop(2)

    def recordLoader(self):
        if self.svt.deathJudge:
            return False
        self.record=self.svt.loadGamer()
        if not self.record:
            return False
        self.gameStart = True
        self.careerSet = True
        return True

    def creatorLoader(self):        #开发者信息模式进入
        if self.svt.deathJudge:
            return False
        self.record=self.svt.loadGamer()
        if not self.record:
            return False
        self.creatorLoaderFunc(1)
        self.creator=True
        return True

    def monuLoader(self):       #英雄纪念厅进入
        if self.svt.deathJudge:
            return False
        self.record=self.svt.loadGamer()
        if not self.record:
            return False
        self.creatorLoaderFunc(0)
        self.monu=True
        return True

    def modeSetup(self):       #模式选择
        self.hq.set_loop(4)
        if self.careerSet and self.gameStart:
            self.skillSelect()
        elif not self.gameStart:
            self.menuSelect()
        else:
            self.careerSelect()

    def drawSelect(self):           #主绘制
        self.screen.blit(self.bk, (0,0))
        self.drawButton()








