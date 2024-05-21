import os
#-*-coding:utf-8-*-
import random
import numpy as np
from src.ezplot import *

class Surround:                                                                                                                 #建立在Dungeon基础上的类，在Dungeon原有地图上绘制其他地形道具，附加值代号1
    def __init__(self, func):                                                                                      #数据输入函数为func参数，参数对应dg(Dungeon 类)， 数据渲染函数为func2对应函数，为pl(Player 类)
        self.image=MySprite()
        self.image.load(os.path.join("asset", "surroundings.png"), 0, 0, 32, 32, 11)
        self.func, self.eqf = func, None
        self.level=np.full((64, 42), -1, dtype = int)
        self.no_walk={0, 3, 10, 12, 16, 17, 18, 23, 25, 26, 30, 31, 33, 34, 37, 38, 40, 41, 42}         #不能直接踩在这个图形id对应的图形上
        self.nowalk_through={16, 17, 18, 23, 25, 26, 30, 31, 33, 34, 37, 38, 40, 41, 42}               #这个对应了No_walk,pathfinder不能通过的
        self.doors=[0, 3]                                                                                                         #不能直接踩在这个图形id对应的图形上，在踩之前会改变id的图形
        #这个表示了能够和玩家交互的环境道具，陷阱
        self.inter_dict={0,1,3,4, 5,6,7,10, 11, 12, 13, 14, 15, 22, 25, 26, 27, 28, 31, 33, 35, 37, 38  }     #交互字典，具体用法间self.modChar()
        #注意，changable是可以踩踏的，只有踩踏在上面才会起效果。
        self.detect=({0:'Door Shut', 1:'Door Opened', 2:'Door Broken', 3:'Cell Gate', 4:'Cell Gate',
                      5:'Mystery Chest', 6:'Gold Chest', 7:'Trap Chest', 8:'Empty Chest', 9:'Empty Chest',
                      10:'Trap', 11:'Triggered Trap', 12:'Door Locked', 13:'Portal', 14:'Summonor',
                      15:'Spikes', 18:'Statue', 22:'Preach Desk', 23:'Stone Coffin', 24:'Uncovered Coffin',
                      25:'Bookshelf', 26:'Shelf', 27:'Table', 28:'Chair', 29:'Waste', 30:'Seat', 31:'Barrel', 32:'Waste',
                      33:'Mirror', 34:'Broken Mirror', 35:'Desk', 36:'Wooden Coffin', 37:'Uncovered Coffin',
                      38:'Potionshelf', 39:'Hidden Door', 40:'Hero Statue', 41:'Tomb Cross'})
        self.costs={10:8, 11:10, 13:4, 15:4}
        self.monster_trig=()
        self.itemDrop=None
        self.pl, self.inf=None, None
        self.getLoop=None        #由于在光标模式和正常操作模式中，inter_dict方法有所不同，要一个参数判断

    #地牢内部设施，门，宝箱，陷阱等
    def interDict(self, x, y, where):
        if where in {0, 1, 3, 4, 12}: self.inter_door(x, y, where)
        elif where in {5, 6}: self.inter_box(x, y, where)
        elif where in range(13, 16): self.de_trap2(x, y, where)
        elif where in {10, 11}: self.de_trap(x, y, where)
        elif where ==7: self.de_trap1(x, y, where)
        elif where in {26, 27, 28, 35}: self.debris1(x, y, where)
        elif where in {22, 25, 31, 33, 38}: self.debris2(x, y, where)

    def treasure_box(self, minThres:int=6, maxThres:int=9):     #按照概率在普通地砖上生成宝箱,possi是生成概率.
        lst=[]
        for x in range(64):
            for y in range(42):
                if self.func.getChar(x, y) in {2, 11, 12, 14, 31, 32} and self.getChar(x, y)==-1:
                    lst.append((x, y))
        boxNum=random.randint(minThres, maxThres)
        lst=random.sample(lst, boxNum)
        for point in lst:
            self.setChar(*point, 5)

    '''=============================================================
      ============================================================='''
    #=====================各种陷阱以及地图道具生成======================
    def trap(self):         #每个关卡有一个陷阱，这个陷阱踩到后会掉到下一层
        if self.func.level_num<8:
            x = random.randint(5, 59)
            y = random.randint(5, 37)
            while self.func.getChar(x, y) not in {2, 11, 12, 14, 31, 32} or self.getChar(x, y) != -1:
                x = random.randint(5, 59)
                y = random.randint(5, 37)
            self.setChar(x, y, 10)

    def spikes(self):       #钉刺陷阱，踩到会减血
        maxi=random.randint(1, 6)
        for i in range(1, maxi):
            x=random.randint(5, 59)
            y=random.randint(5, 37)
            while self.func.getChar(x, y) not in {2, 11, 12, 14, 31, 32} or self.getChar(x, y)!=-1:
                x=random.randint(5, 59)
                y=random.randint(5, 37)
            self.setChar(x, y, 15)

    def portal(self):       #随机传送门，踩到会飞到这一层其他地方
        maxi=random.randint(1, 3)
        for i in range(1, maxi):
            x=random.randint(5, 59)
            y=random.randint(5, 37)
            while self.func.getChar(x, y) not in {2, 11, 12, 14, 31, 32} or self.getChar(x, y)!=-1:
                x=random.randint(5, 59)
                y=random.randint(5, 37)
            self.setChar(x, y, 13)

    def summon(self):       #怪物召唤陷阱，踩到会召唤怪物
        maxi=random.randint(1, 3)
        for i in range(1, maxi):
            x=random.randint(5, 59)
            y=random.randint(5, 37)
            while self.func.getChar(x, y) not in {2, 11, 12, 14, 31, 32} or self.getChar(x, y)!=-1:
                x=random.randint(5, 59)
                y=random.randint(5, 37)
            self.setChar(x, y, 14)

    def traps(self):
        self.trap()
        self.spikes()
        self.portal()
        self.summon()
    '''=============================================================
      ============================================================='''
    
    def gate_way(self, x1, y1, x2, y2):     #（x1，y1）处是一堵门，（x2, y2）处是一堵墙
        self.setChar(x1, y1, 0)
        self.func.setChar(x2, y2, 0)
        self.func.setChar(x1, y1, 1)
        
    '''=============================================================
      ============================================================='''
    #=======================Char的修改==========================
    def getChar(self, x, y):  # 获取一个地图方块的id
        # if x>=0 and x<64 and y>=0 and y<42:
        return self.level[x, y]

    def setChar(self, x, y, val):      #设置地图id为char值
        self.level[x, y]=val

    def modChar(self, x, y):        #修改Char值，这个修改是不赋值的
        #就是开门的作用
        judge=self.getChar(x, y)
        if judge in self.doors:
            self.setChar(x, y, judge+1)

    def getCost(self, x, y):            #寻路代价计算方法
        k=self.getChar(x, y)
        if k in self.costs:
            return self.costs[ k ]
        else:
            return 0

    def noWalk(self, x, y):
        bejudge=self.getChar(x, y)
        if bejudge in self.no_walk:
            return True
        return False
        
    def reset(self):
        self.level=np.full((64, 42), -1, dtype = int)

    #===================环境交互===============================
    '''======================================================='''
    def inter_door(self, x, y, where):
        if where==0:
            self.setChar(x, y, where+1)
            self.inf.prefabTell('door+')
        elif where==1:
            self.setChar(x, y, where-1)
            self.inf.prefabTell('door-')
        elif where==3:
            self.setChar(x, y, where + 1)
            self.inf.prefabTell('gate+')
        elif where == 4:
            self.setChar(x, y, where - 1)
            self.inf.prefabTell('gate-')
        elif where == 12:
            if self.eqf.ptr.haveKey():
                self.eqf.ptr.useKey()
                self.inf.prefabTell('door#')
                self.setChar(x, y, 1)
            else:
                self.inf.prefabTell('door!')
            
    def de_trap(self, x, y, where=None):     #完全除去陷阱（setChar参数值为-1）,主要用于下落陷阱
        self.inf.prefabTell('trap-')
        self.setChar(x, y, -1)
        self.eqf.ptr.exp_adder(5)

    
    def de_trap1(self, x, y, where):        #除去陷阱1：setChar改变值只有1
        if self.getLoop()==1:   #打开陷阱箱后会被刺
            self.inf.prefabTell('boxtrap')
            self.setChar(x, y, 8)
            self.itemDrop((x, y), self.itemLevelNum())
            self.pl.dg.fem.rangeCenter(self.pl.posx, self.pl.posy, self.pl.ptr.LR)  # TBS:luminous_range应该作为一个参数
            self.eqf.ptr.hp_adder(-2)
        else:
            self.inf.prefabTell('trap-')
            self.setChar(x, y, 8)
            self.itemDrop((x, y), self.itemLevelNum())
            self.pl.dg.fem.rangeCenter(self.pl.posx, self.pl.posy, self.pl.ptr.LR)  # TBS:luminous_range应该作为一个参数
            self.eqf.ptr.exp_adder(5)

    def de_trap2(self, x, y, where):
        self.inf.prefabTell('trap-')
        self.setChar(x, y, where+6)
        self.eqf.ptr.exp_adder(5)

    def inter_box(self, x, y, where):       #参数x, y应该是self.xat, self.yat
        if where==5:
            choices=[[0, 1], [0.9, 0.1]]
            possi=random.choices(choices[0], choices[1])[0]
            if possi:
                self.setChar(x, y, 7)
            else:
                self.setChar(x, y, 8)
                self.itemDrop((x, y), self.itemLevelNum())
                self.pl.dg.fem.rangeCenter(self.pl.posx, self.pl.posy, self.pl.ptr.LR)

    '''========================================================='''
    #==========================怪物环境交互=======================
    def mons_door(self, x, y, val):     #怪物开门或撞坏门
        if not val:
            door_set=random.randint(1,2)
            if door_set==2: self.inf.prefabTell('doorx')
            self.setChar(x, y, door_set)
        elif val==3:
            self.setChar(x, y, 4)

    def mons_trap(self, x, y):      #怪物掉进地板陷阱
        self.setChar(x, y, 11)

    def itemLevelNum(self):
        res=int(self.func.level_num**(2/3)+0.4)
        return res

    def modSur(self, lst1, lst2):       #在纪念馆模式中，已经使用的石棺要盖板并且点燃祭拜之火，英雄雕塑变成金色
        for i in lst1:          #石棺和祭拜之火
            if i[0]<5 and i[1]>6:
                self.setChar(i[0], i[1]-1, 23)
                self.setChar(i[0]+1, i[1]-1, random.choice([16, 17]))
            elif i[0]>58 and i[1]>6:
                self.setChar(i[0], i[1] - 1, 23)
                self.setChar(i[0] - 1, i[1] - 1, random.choice([16, 17]))
            elif i[1]==4 and i[0]<31:
                self.setChar(i[0]+1, 4, 23)
                self.setChar(i[0]+1, 5, random.choice([16, 17]))
            elif i[1]==4 and i[0]>32:
                self.setChar(i[0] - 1, 4, 23)
                self.setChar(i[0] - 1, 5, random.choice([16, 17]))
        for j in lst2:          #金色雕塑
            self.setChar(*j, 40)

    def debris1(self, x, y, where):      #杂碎非桶和镜子以及烧杯柜，书柜的物品
        if where in {26, 27, 28, 35}: self.setChar(x, y, 29)

    def debris2(self, x, y, where):     #其他类型杂物的破坏
        if where in {25, 33}: self.setChar(x, y, where+1)
        elif where==22: self.setChar(x, y, 35)
        elif where==38: self.setChar(x, y, 26)
        elif where==37: self.setChar(x, y, 36)
        elif where==31:
            self.setChar(x, y, 32)
            choices = [[0, 1], [0.6, 0.4]]
            possi = random.choices(choices[0], choices[1])[0]
            if possi:
                if self.func.level_num>0:       #防止纪念馆内掉落
                    self.itemDrop((x, y), 1)
                self.pl.dg.fem.rangeCenter(self.pl.posx, self.pl.posy, self.pl.ptr.LR)



            
        
        

    
            

        
                

        



        
