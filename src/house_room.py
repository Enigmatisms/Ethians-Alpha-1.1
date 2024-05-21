import os
#!/usr/bin/env python3
#-*-coding:utf-8-*-
#This is the main loop of Ethians

__author__='SEeHz3'
__date__='2019.2.17'

import json, random
from src.Pathfinder import Astar
from src.ezplot import *
from src.surround import Surround
from src.prim import Primtree
from src.level0 import Level0

class Dungeon:    #地牢对象创建
    def __init__(self, screen):
        #图像输入
        self.level_num=0
        #self.x_len, self.y_len=(64,42)
        self.screen=screen
        self.u_x, self.u_y, self.d_x, self.d_y=(0,0,0,0)
        self.image=MySprite()
        self.image.load(os.path.join("asset", "floor2.png"), 0, 0, 32, 32, 11)
        self.level=[[0 for i in range(42)] for j in range(64)]
        self.lvl0=Level0()
        self.rooms=list()
        self.water=MySprite()
        self.sur=Surround(self)     #Surround调用Dungeon
        self.no_walk={0, 10, 13, 15, 22, 27, 28}       #ply键盘移动时需要判断，玩家是不是会移动到不能走的地方
        self.npc=None
        self.po=None        #传入Pool实例po，在每一关地图改变时创建怪物
        self.a = Astar(self)
        self.noStair = {0, 10, 13, 15, 18, 19, 22, 27, 28}
        self.detect=({0:'Wall Brick', 3:'UpStair', 4:'DownStair',
                      6:'Grass', 7:'Bush', 8:'Water', 9:'Water', 10:'Rifted Brick',
                      13:'Iron Bar', 15:'Blood Brick', 16:'UpStair', 17:'DownStair',
                      18:'Lava', 19:'Lava', 20:'Toxic', 21:'Toxic', 22:'White Brick', 25:'Stairs',
                      27:'Cave Brick', 28:'Rifted Cave Brick', 29:'UpStair', 30:'DownStair'})
        self.costs={8:2, 9:2, 18:5, 19:5, 20:3, 21:3}           #地图方块的寻路代价
        self.fem=None     #引用FloorEquipmentManager方法
        self.inf=None
        self.pm=Primtree()

    def getChar(self, x, y):        #获取一个地图方块的id
        if all([x>=0 ,x<64, y>=0, y<42]):
            return self.level[x][y]
        return -1

    def setChar(self, x, y, val):      #设置地图id为char值
        self.level[x][y]=val

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

    def create_map(self, record=None):      #重写create_map:
        self.reset()
        if not record is None:          #存档改写
            self.level_num=record       #利用存档生成地图
        if self.level_num in [1,2]:
            self.create_cave()
        elif self.level_num in range(3, 8):
            self.load_diy()
            self.scan()                         #放置潘多拉或者雕像鬼
        elif self.level_num==8:
            self.load_diy(11)
            self.scan()
        else:
            self.level=self.lvl0.setUpMap()
            self.stairs(2)
            self.npc.grt_npc()
        if self.level_num > 2: self.inf.moreArg('reach', ['dungeon', self.level_num])
        elif self.level_num>0: self.inf.moreArg('reach', ['cave', self.level_num])
        else: self.inf.prefabTell('out')
        self.po.ptr.nowLvl=self.level_num
        if self.level_num>=1:
            num=random.choices([0, 1, 2, 3], [0.88, 0.06, 0.04, 0.02])[0]
            self.fem.setRandomItems(num)
        else:
            self.fem.setRandomItems(2, True)        #放置蘑菇
        self.po.mob_spawn(self.level_num, self.po.arg_funcs)
        
    def stairs(self, tag=3):       #随机生成楼梯的位置，楼梯不能生成在墙上，上下楼梯不能重合
        #1表示只有向上的楼梯，2只有向下，3全都有
        self.u_x=random.randint(5,60)
        self.u_y=random.randint(5,38)
        if self.level_num>=3:       #如果层数为3及以上时，开始出现更骚的楼梯
            stair_pic=16
        else:
            stair_pic=29
        if tag in {1,3}:
            while self.getChar(self.u_x, self.u_y) not in {2, 11, 12, 31, 32} or self.sur.getChar(self.u_x, self.u_y) != -1:
                self.u_x = random.randint(5, 60)
                self.u_y = random.randint(5, 38)
            self.setChar(self.u_x, self.u_y, stair_pic)
        self.d_x=random.randint(5,60)
        self.d_y=random.randint(5,38)
        if tag in {2, 3}:
            while self.getChar(self.d_x, self.d_y) not in {2, 11, 12, 31, 32, 5, 6, 7} or self.sur.getChar(self.d_x, self.d_y) != -1:
                self.d_x = random.randint(5, 60)
                self.d_y = random.randint(5, 38)
            self.setChar(self.d_x, self.d_y, stair_pic + 1)

    def ledder_down(self):
        self.d_x, self.d_y=(random.randint(5, 58), random.randint(9, 32))
        while not self.getChar(self.d_x, self.d_y) in {5,6,7}:
            self.d_x, self.d_y=(random.randint(5, 58), random.randint(9, 32))
        self.setChar(self.d_x, self.d_y, 4)

    def ledder_up(self):
        self.d_x, self.d_y=(random.randint(5, 58), random.randint(9, 32))
        while not self.getChar(self.d_x, self.d_y) in {5,6,7}:
            self.d_x, self.d_y=(random.randint(5, 58), random.randint(9, 32))
        self.setChar(self.d_x, self.d_y, 4)
    '''================================================================================'''

    def load_level(self, n=None):           #从DIY地图中取出数据加载~！！
        #由于是测试，所以暂且设置level_num=-1（-1层的自定义关卡，只有开发者可以进入）
        try:
            with open(os.path.join('data', 'diy.json'), 'r') as read:
                tem=json.load(read)
        except FileNotFoundError:
            with open(os.path.join('data', 'diy.json'), 'w') as setting:
                json.dump([], setting)
        else:
            self.level=[[0 for i in range(42)] for j in range(64)]
            if tem:
                if not n is None:       #载入特定关卡
                    self.sur.reset()
                    self.npc.reset()
                    self.level = tem[n][0]
                    self.sur.level = tem[n][1]
                    self.level_num = -1
                    return
                print('You have %s map in storage.'%len(tem))
                num=input('The map you want to test:')
                try:
                    num=int(num)
                except ValueError:
                    print('Input failure: Exit.')
                else:
                    if num>0 or num<=len(tem):
                        #加载对应地图数据
                        self.sur.reset()
                        self.npc.reset()
                        self.level=tem[ num-1 ][ 0 ]
                        self.sur.level=tem[ num-1 ][1]
                        self.level_num=-1
            else:
                print('You have no map to test! Go and create one!')

    def load_diy(self, lvl=0):
        #随机载入自定义地图
        try:
            with open(os.path.join('data', 'diy.json'), 'r') as read:
                tem=json.load(read)
        except FileNotFoundError:
            with open(os.path.join('data', 'diy.json'), 'w') as setting:
                json.dump([], setting)
        else:
            if lvl: num=lvl
            else: num=self.po.ptr.dungeon[self.level_num-3]
            if num>0:
                self.sur.reset()
                self.level = tem[num][0]
                self.sur.level = tem[num][1]
                self.stairs(1) if lvl else self.stairs()
                if num == 9:
                    self.sur.treasure_box(11, 14)  # 重门迷宫需要更多宝箱
                else:
                    self.sur.treasure_box()
                self.sur.traps()
            else:
                self.pm.initMap()
                self.level, self.sur.level = self.pm.createMap()
                self.stairs()
            
            #和场景有关，自定义生成箱子，陷阱，楼梯：
    
    def reset(self):        #SPACE reset地图设置
        self.level=[[0 for i in range(42)] for j in range(64)]
        self.rooms=list()
        self.sur.reset()
        self.npc.reset()
        self.po.reset()
        self.fem.floorReset()            #上下楼时，物品会被清除

    def __getVinc(self, x, y, radius=1):
        lst = list()
        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                lst.append((i, j))
        if radius > 1:
            for i in self.__getVinc(x, y, radius - 1):
                lst.remove(i)
        return lst

    def __countWall(self, x, y, radius=1):
        lst = self.__getVinc(x, y, radius)
        count = 0
        for i in lst:
            if self.getChar(*i) in {27, 28}:
                count += 1
        return count

    def caveGen(self):
        for x in range(4, 61):
            for y in range(4, 38):
                if self.getChar(x, y) in {27, 28}:
                    if self.__countWall(x, y) < 4:
                        self.setChar(x, y, 31)
                else:
                    if self.__countWall(x, y) >= 5 or self.__countWall(x, y, 2) <= 2:
                        self.setChar(x, y, 27)

    def modCave(self):
        for x in range(4, 61):
            for y in range(4, 38):
                if self.__countWall(x, y) >= 6:
                    self.setChar(x, y, 27)

    def mapGen(self, time=3):
        for i in range(time):
            self.caveGen()
        for i in range(time - 1):
            self.modCave()

    def setCave(self, times=4):
        self.level = [[27 for i in range(42)] for j in range(64)]
        for x in range(4, 61):
            for y in range(4, 38):
                self.setChar(x, y, random.choices([31, 32, 27, 28], [0.48, 0.16, 0.30, 0.06])[0])
        self.mapGen(times)

    def create_cave(self):
        self.setCave()
        tpl=self.setStartEnd()
        judge=self.a.mapJudge(*tpl)
        while not judge:
            self.setCave()
            tpl = self.setStartEnd()
            judge = self.a.mapJudge(*tpl)
        self.u_x, self.u_y=tpl[0]
        self.d_x, self.d_y=tpl[1]
        self.setChar(*(tpl[0]), 29)
        self.setChar(*(tpl[1]), 30)
        self.sur.treasure_box(9, 13)
        self.sur.traps()

    def setStartEnd(self):              #cave的阶梯生成方式
        x1, y1 = random.randint(4, 60), random.randint(4, 38)
        judge = self.getChar(x1, y1)
        while judge in {27, 28}:
            x1, y1 = random.randint(4, 60), random.randint(4, 38)
            judge = self.getChar(x1, y1)
        x2, y2 = random.randint(4, 60), random.randint(4, 38)
        judge = self.getChar(x2, y2)
        while judge in {27, 28}:
            x2, y2 = random.randint(4, 60), random.randint(4, 38)
            judge = self.getChar(x2, y2)
        return (x1, y1), (x2, y2)

    """===============自动地图处理效果============="""
    def scan(self):
        for x in range(4, 59):
            for y in range(4, 38):
                judge=self.sur.getChar(x, y)
                if judge==5:
                    if random.choices([0, 1], [0.95, 0.05])[0]:
                        self.sur.setChar(x, y, -1)
                        self.po.more_mob((x, y), 0, 46, flag=True)
                elif judge==18:
                    if random.choices([0, 1], [0.97, 0.03])[0]:
                        self.sur.setChar(x, y, -1)
                        self.po.more_mob((x, y), 0, 48, flag=True)
                elif judge==0:
                    if random.choices([0, 1], [0.9, 0.1])[0]:
                        self.sur.setChar(x, y, 9)


