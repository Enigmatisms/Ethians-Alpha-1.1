#-*-coding:utf-8-*-
import pygame
from ezplot import MySprite

class Monument:
    def __init__(self, surface):
        self.screen=surface
        self.stone=MySprite()
        self.stone.load(r'asset\stones.png', 0, 0, 600, 650, 2)
        self.inf, self.svt, self.hq=None, None, None
        self.mode=0         #0表示墓碑，1表示黄金纪念碑
        self.stone.X, self.stone.Y = 300, 0
        self.deaths=None
        self.heroes=None
        self.loopRecord=1
        self.font=pygame.font.Font(r'asset\fonts\verdana.ttf', 13)
        self.font2=pygame.font.Font(r'asset\fonts\verdana.ttf', 18)
        self.text=[]
        self.text_len=0     #text surface列表的长度
        self.deathMap={(4, 7+3*i):i for i in range(11)}         #死亡信息保存点
        for i in range(11, 29):
            self.deathMap[(3*(i-11)+5,4)]=i
        for i in range(29, 40):
            self.deathMap[(59, 7+3*(i-29))]=i
        self.heroMap={(14, 14+2*i):i for i in range(10)}            #英雄信息保存点
        for i in range(10, 20):
            self.heroMap[(49, 14+2*(i-10))]=i
        for i in range(20, 27):
            self.heroMap[(19, 14+2*(i-20))]=i
        for i in range(27, 34):
            self.heroMap[(44, 14+2*(i-27))]=i

    def drawStone(self):            #loop11主绘制函数
        self.stone.frame, self.stone.last_frame=self.mode, self.mode
        self.stone.update(0)
        self.stone.draw(self.screen)
        self.drawInfo(398, 110)      #绘制石碑上的信息

    def DeathInfo(self):     #loop11开始前准备
        self.deaths=self.svt.loadDeath()

    def HeroInfo(self):          #loop11开始前准备
        self.heroes=self.svt.loadHero()

    def inspect(self, judge, xat, yat):            #在ply中调用它
        if not self.deaths: self.DeathInfo()            #信息准备
        if not self.heroes: self.HeroInfo()             #信息准备
        if judge==40: self.mode=1           #40ID对应了金色雕塑
        else: self.mode=0
        if self.mode:
            num=self.heroMap[(xat, yat)]
            self.prepInfo(self.getOneHero(num))
        else:
            num = self.deathMap[(xat, yat)]
            self.prepInfo(self.getOneDeath(num))


    def getOneDeath(self, num):
        if num>=len(self.deaths):
            return None
        return self.deaths[num]

    def getOneHero(self, num):
        if num>=len(self.heroes):
            return None
        return self.heroes[num]

    def prepInfo(self, lst):
        if not lst is None:
            self.loopRecord=self.hq.get_loop()
            length = len(lst)
            self.text.clear()
            if self.mode:
                self.text.append(self.font2.render(lst[0], True, (0, 0, 0)))
                self.text.append(self.font2.render(lst[1], True, (0, 0, 0)))
                self.text.append(self.font.render(lst[2], True, (0, 0, 0)))
            else:
                self.text.append(self.font2.render(lst[0], True, (255, 255, 255)))
                self.text.append(self.font2.render(lst[1], True, (255, 255, 255)))
                self.text.append(self.font.render(lst[2], True, (255, 255, 255)))
            for i in range(3, length-1):
                if self.mode: self.text.append(self.font2.render(lst[i], True, (0, 0, 0)))
                else: self.text.append(self.font2.render(lst[i], True, (255, 255, 255)))
            self.text_len = length-1
            self.hq.set_loop(11)  # 如果墓碑或纪念碑有主人，就可以绘制
        else:
            self.text_len=0

    def drawInfo(self, x, y):
        self.screen.blit(self.text[0], (512, 110))
        self.screen.blit(self.text[1], (590, 140))
        for i in range(2, self.text_len):
            self.screen.blit(self.text[i], (x, y+i*30))

    def quitSetter(self):
        self.hq.set_loop(self.loopRecord)

    def mapChange(self):            #提供dg.sur需要更新的位置
        lst1, lst2=[], []           #lst1是石棺位置,lst2是石雕位置
        count1, count2=0, 0
        if not self.deaths: self.DeathInfo()            #信息准备
        if not self.heroes: self.HeroInfo()             #信息准备
        death_len=len(self.deaths)
        hero_len=len(self.heroes)
        for i in self.deathMap.keys():
            if count1 >= death_len: break
            lst1.append(i)
            count1+=1
        for i in self.heroMap.keys():
            if count2 >= hero_len: break
            lst2.append(i)
            count2 += 1
        return [lst1, lst2]




