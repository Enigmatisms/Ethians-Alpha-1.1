#-*-coding: utf-8-*-

import pygame, json, os, copy
from pygame.locals import *
from src.ezplot import MySprite

class keySets:
    def __init__(self, surface, func):
        path = os.path.join('asset', 'fonts', 'verdana.ttf')
        self.font=pygame.font.Font(path, 21)
        self.ind=MySprite()      #indicator
        self.wind = MySprite()       #wrong_indicator
        self.screen=surface
        self.loopSetter=func
        self.bk=pygame.image.load(r'asset\settings.png').convert_alpha()
        self.ind.load(r'asset\indicator.png', 0, 0, 48, 48, 8)
        self.wind.load(r'asset\windicator.png', 0, 0, 48, 48, 8)
        self.ind.X = 550  # 初始位置设定
        self.ind.Y = 100  # 初始位置设定
        self.default={'up':K_UP, 'down':K_DOWN, 'lf':K_LEFT, 'rt':K_RIGHT,
                      'topl': K_q, 'topr': K_w, 'btl': K_a, 'btr': K_s,
                      'etr':K_RETURN, 'esc':K_ESCAPE, 'map':K_m, 'cursor':K_c,
                      'bag':K_TAB, 'me':K_b, 'wand':K_1, 'bow':K_2,  'save':K_0}
        self.keyPads =copy.copy(self.default)
        self.posList=list(self.keyPads.keys())
        self.keyStr={32:"Space", 306:"Left Ctrl", 305:"Right Ctrl", 304:"LShift", 303:"RShift",
                     276:"Left", 275:"Right", 274:"Down", 273:"Up", 27:"ESC", 9:"TAB"}
        self.warning=self.font.render("You have a conflict setting or unknown input.", True, (220, 0, 0))
        self.judgeList=[False]*17
        self.pos=0
        self.conflict=False
        self.listen=False
        self.covSur=pygame.Surface((240, 48))
        self.covSur.set_alpha(120)
        self.surfaceList=list()

    def init(self):             #启动时必须执行
        self.surfaceList=[self.font.render(self.asciiMap(v), True, (0,0,0)) for v in self.keyPads.values()]

    def asciiMap(self, num):
        if num in range(97, 123):
            return chr(num-32)
        elif num in range(65, 91):
            return chr(num)
        elif num in range(48, 58):
            return str(num-48)
        elif num in {10, 13}:
            return "Enter"
        elif num in self.keyStr:
            return self.keyStr[num]
        else:
            return None

    def loadPreference(self):       #加载玩家设置偏好
        try:
            with open(r'data\keyshortcuts.json', 'r') as rd:
                self.keyPads=json.load(rd)
        except FileNotFoundError:
            self.keyPads = copy.copy(self.default)
            with open(r'data\keyshortcuts.json', 'w') as first:
                json.dump(self.keyPads, first)

    def savePreference(self):       #保存玩家设置偏好
        with open(r'data\keyshortcuts.json', 'w') as first:
            json.dump(self.keyPads, first)
        self.loopSetter(4)      #保存后就退出

    def abandon(self):          #放弃更改设置
        self.loadPreference()       #没有保存说明可以加载之前的设置
        self.loopSetter(4)

    def previous(self):         #上一个选项
        self.pos-=1
        if self.pos==-1:
            self.pos=19
        if self.conflict and self.pos==18:      #冲突时不可用
            self.pos=17
        self.setIndPos()

    def nextOne(self):      #下一个选项
        self.pos+=1
        if self.pos==20:
            self.pos=0
        if self.conflict and self.pos==18:      #冲突时不可用
            self.pos=19
        self.setIndPos()

    def goLeft(self):       #前往左栏
        if self.pos>9:
            self.pos-=10
        self.setIndPos()

    def goRight(self):      #前往右栏
        if self.pos<10:
            self.pos+=10
        if self.conflict and self.pos==18:      #冲突时不可用
            self.pos=8
        self.setIndPos()

    def enterKey(self):     #更改键盘设置
        #listen=1表示开始获取键盘输入作为设置值,第二次Enter表示输入完成
        if self.pos<17:
            self.listen=True
        else:
            if self.pos==17:        #设置为默认值
                self.reset2Default()
            elif self.pos==18:
                self.savePreference()
            else:
                self.abandon()


    def getSurface(self, key, judge):          #输入的是keyPads的key
        if judge: color=(255, 0, 0)
        else: color=(0,0,0)
        string=self.asciiMap(key)
        if string:
            text=self.font.render(string, True, color)
        else:
            color=(255, 0, 0)
            text=self.font.render("???", True, color)
        return text

    def putKey(self, key):
        if self.pos<17:
            k=self.posList[self.pos]            #用于keyPads设置值的key
        else:
            k=None
        if k:
            self.keyPads[k]=key

    def updateKey(self):        #更新所有key的颜色
        #这个函数只在键盘事件下响应
        for k in range(17):
            judge=self.collideKey(self.keyPads[self.posList[k]], self.posList[k])
            self.judgeList[k]=judge
            self.surfaceList[k] = self.getSurface(self.keyPads[self.posList[k]], judge)

    def _drawKey(self):                  #绘制surfaceList中的内容
        for i in range(10):
            self.screen.blit(self.surfaceList[i], (330, 108+50*i))
        for i in range(10, 17):
            self.screen.blit(self.surfaceList[i], (820, 108+50*(i-10)))

    def setIndPos(self):          #指示标志绘制
        self.ind.X=(self.pos//10)*475+550
        self.ind.Y=100+50*(self.pos%10)

    def drawInds(self, ticks, rate=80):         #绘制indicators
        for i in range(17):
            if self.judgeList[i]:
                self.wind.X = (i // 10) * 475 + 550
                self.wind.Y = 100 + 50 * (i % 10)
                self.wind.update(ticks, rate)
                self.wind.draw(self.screen)
        self.ind.update(ticks, rate)
        self.ind.draw(self.screen)

    def collideKey(self, keynum, key):      #是否有冲突按键设置？
        for k,v in self.keyPads.items():
            if keynum==v and key != k:
                self.conflict=True
                return True
        return False

    def drawSurface(self):
        self.screen.blit(self.bk, (0,0))
        if not any(self.judgeList): self.conflict = False
        if self.conflict:
            self.screen.blit(self.warning, (595, 38))
            self.screen.blit(self.covSur, (768, 500))       #save change变的灰暗，表示不可使用
        self._drawKey()

    def reset2Default(self):        #设置为默认值
        self.judgeList=[False]*17
        self.conflict=False
        self.keyPads=copy.copy(self.default)        #浅拷贝
        self.init()


