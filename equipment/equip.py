import os
#!/usr/bin/env python3
#-*-coding:utf-8-*-

import sys, json, copy
import numpy as np
sys.path.append("..")
from src.ezplot import MySprite
from equipment.enchant import *
from collections import deque

class FloorEquipManage:
    def __init__(self, surface):
        self.All = MySprite()
        self.All.load(os.path.join("asset", "process1.png"), 0, 0, 32, 32, 16)
        self.level=np.full((64, 42), -1, dtype = int)
        self.pool={}
        self.ptr=None       #传入ptr,需要和人物的背包联系
        self.dg=None
        self.npc=None
        self.sur=None
        self.pl=None
        self.gui=None
        self.inf=None
        self.func_list=[]
        self.screen=surface
        self.eq=Equip()
        self.eq.getInfo()
        self.ect=EnchantItem()

        with open(os.path.join("equipment", "equipment.json")) as read:       #创建测试时可以生成的武器列表
            tem=json.load(read)
            self.create=[int(k) for k in tem.keys()]
            self.gnrt_dct={int(k):v[8] for k,v in tem.items()}         #生成一个字典,内容是key为物品ID, value为物品生成等级

    def reset(self):
        self.level=np.full((64, 42), -1, dtype = int)
        self.pool = {}

    def setChar(self, x, y, val):
        self.level[x, y]=val

    def getChar(self, x, y):
        return self.level[x, y]

    def getEquip(self, x, y):           #self.pool建立的是掉落在地上的武器的位置（key）与武器类实例（value）的映射
        judge=self.getChar(x, y)
        if judge >=0:
            return self.pool[ (x, y) ]        #key是个不可变元素tuple
        else:
            return None

    def pickUp(self, x, y):         #捡起（x,y）处的武器
        posx, posy=self.pl.xat, self.pl.yat
        for i in range(posx-1, posx+2):        #只有在(x, y)邻近一格的范围内才可以被捡起
            for j in range(posy-1, posy+2):
                if (x, y) == (i, j):
                    judge=self.getEquip(x, y)
                    if judge:
                        flag=self.ptr.putInBag(judge)            #TBS：putInBag是一个代写的方法
                        if flag:
                            self.pool[ (x, y) ]=None
                            self.setChar(x, y, -1)

    def throwAway1(self):
        index=self.gui.flag+self.gui.page_now*16
        stuff=self.ptr.getBag()[ index ]
        if stuff.equipped:
            self.ptr.deEquip(stuff)
        self.drop(stuff)
        self.gui.reset()
        self.gui.quitSetter()
        self.gui.quitSetter()

    def throwAwayAll(self):
        index=self.gui.flag+self.gui.page_now*16
        stuff=self.ptr.getBag()[ index ]
        self.drop(stuff, 1)
        self.gui.reset()
        self.gui.quitSetter()
        self.gui.quitSetter()
        
    def drop(self, stuff, tag=0):     #tag为一时为丢弃全部
        posx, posy=self.pl.xat, self.pl.yat
        judge=self.getChar(posx, posy)
        if judge==-1:
            if isinstance(stuff, Equip):    #扔下的物品必须是Equip实例
                tem=copy.copy(stuff)        #丢下的是浅拷贝的stuff
                if tag:
                    judge=self.ptr.throwAway(stuff, 1)
                else:
                    judge=self.ptr.throwAway(stuff)
                if judge:
                    if tem.equipped==1: tem.equipped=0      #（拷贝数据不关联bug）修复
                    self.pool[(posx, posy)]=tem
                    self.setChar(posx, posy, tem.ID)
                    if not tag:
                        self.pool[(posx, posy)].count=1         #丢弃一件时地面物品的数量必须设置为1
        else:
            self.inf.prefabTell('occupied')

    def center(self, cx, cy):           #绘制装备
        #x, y为center基准点
        for y in range(4, 38):
            for x in range(4, 60):
                stuff=self.getChar(x, y)
                if stuff>=0:
                    posx=((16-cx) << 5) + 80 + (x << 5)
                    posy=((9-cy) << 5)+ 10 + (y << 5)
                    image=self.All.getImage(stuff)
                    self.screen.blit(image, (posx, posy))

    def rangeCenter(self, cx, cy, n):      #只在一定范围内进行的center
        x_min, x_max=max(1,cx-n), min(62, cx+n+1)
        y_min, y_max=max(1, cy-n), min(40, cy+n+1)
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                stuff=self.getChar(x, y)
                if stuff>=0 and self.pl.ms.getChar(x, y)==1:       #在光照范围内
                    posx=((16-cx) << 5) + 80 + (x << 5)
                    posy=((9-cy) << 5)+ 10 + (y << 5)
                    image = self.All.getImage(stuff)
                    self.screen.blit(image, (posx, posy))

    def setRandomItems(self, n, tag=False):            #创建随机的装备
        for i in range(n):
            x=random.randint(6, 58)
            y=random.randint(6, 37)
            judge=self.canPlace(x, y)
            while not judge:
                x=random.randint(6, 58)
                y=random.randint(6, 37)
                judge=self.canPlace(x, y)
            if tag:
                ID=121
                eq = self.eq.createEquip(ID, x, y)
            else:
                eq=self.boxDropModule(self.dg.level_num)
                if not eq: return
            if eq.label==0:
                self.ect.randomEnchant(eq)
            self.pool[(x, y)]=eq
            self.setChar(x, y, eq.ID)
    
    def floorReset(self):
        self.level=np.full((64, 42), -1, dtype = int)
        self.pool={}
            
    def canPlace(self, x, y):
        if self.dg.getChar(x, y) in {0, 10, 13, 15, 18, 19, 22, 27, 28}:
            return False
        if self.sur.getChar(x, y) in self.sur.no_walk:
            return False
        if self.npc.getChar(x, y) != -1:
           return False
        if self.getChar(x, y) != -1:
            return False
        return True

    '''=========================生成物品概率模型============================='''
    #由于在本游戏中，掉落或者开启宝箱的物品全部出现在地面上，我们将概率问题委托给fem处理
    def mobItemDrop(self, tuple1, trs, lvl):      #给mobs实例使用的
        eq=self.mobDropModule(trs, lvl)
        x, y = tuple1
        drop_deque = deque()
        drop_deque.append((x, y))
        while len(drop_deque) > 0:                  # BFS
            i, j = drop_deque.popleft()
            if self.canPlace(i, j):
                self.dropOne(eq, i, j)
                return
            for m in range(i-1, i+2):
                for n in range(j-1, j+2):
                    if m == i and j == n: continue
                    drop_deque.append((m, n))

    def boxItemDrop(self, tuple1, lvl):
        eq=self.boxDropModule(lvl)
        x, y = tuple1
        drop_deque = deque()
        drop_deque.append((x, y))
        while len(drop_deque) > 0:
            i, j = drop_deque.popleft()
            if self.canPlace(i, j):
                self.dropOne(eq, i, j)
                return
            for m in range(i-1, i+2):
                for n in range(j-1, j+2):
                    if m == i and j == n: continue
                    drop_deque.append((m, n))

    def mobDropModule(self, trs, lvl):
        if trs==-1:       #本怪物没有特征掉落物（比如史莱姆的特征掉落物是钱）
            choice=random.choices([0, 1, 2], [0.0135, 0.985, 0.0015])[0]
            #没有本征掉落物的怪物掉出装备的概率低
            if choice==0:
                num=random.randint(8, 20)
                eq=self.eq.create(46, num)
            elif choice==1:
                eq=None
            else:
                tem=dict( filter(lambda x: x[1]<=lvl, self.gnrt_dct.items() ) ).keys()          #筛选出物品等级小于lvl的物品
                lst=list( tem )
                ID=random.choice(lst)
                if ID==46:
                    eq=self.eq.create(ID, 12)
                else:
                    eq=self.eq.create(ID)
        elif trs==-2:           #潘多拉专属掉落物
            eq = self.boxDropModule(lvl)
        else:
            choice=random.choices([0, 1, 2], [0.005, 0.994, 0.001])[0]
            if choice==1:           #掉落特征掉落物
                #掉落金币的水平和lvl有关
                if trs==46:
                    mini=int(np.log(lvl+1)*42)
                    maxi=int(np.log(lvl+1)*75)
                    num=random.randint(mini, maxi)
                    eq=self.eq.create(46, num)
                else:
                    eq=self.eq.create(trs, 1)
            elif choice==2:             #掉落同级掉落物
                tem=dict( filter(lambda x: x[1]<=lvl, self.gnrt_dct.items() ) ).keys()          #筛选出物品等级小于lvl的物品
                lst=list( tem )
                ID=random.choice(lst)
                if ID==46:
                    eq=self.eq.create(ID, 12)
                else:
                    eq=self.eq.create(ID)
            else:       #不发生掉落
                eq=None
        if eq:
            self.ect.randomEnchant(eq)      #随机附魔（包括了第六级的附魔）
        return eq

    def boxDropModule(self, lvl):
        #lvl是地图层数，要取绝对值。
        gnrt_lvl=int(( abs(lvl) )**(2/3)+0.4)       #可以保证第五层比第四层多一级，第十层比第九层多一级，并且和物品等级有一定联系
        choices=[0, 1]
        possi=[0.05, 0.95]
        choice=random.choices(choices, possi)[0]
        if choice:
            lst=[self.norm(i) for i in range(0, gnrt_lvl+1)]
            lst/=sum(lst)
            choices=[i for i in range(0, gnrt_lvl+1)]
            choice=random.choices(choices, lst)[0]
            tem=dict( filter(lambda x: x[1]==choice, self.gnrt_dct.items() ) ).keys()
            tem=list( tem )
            ID=random.choice(tem)
            if ID==46:
                count=random.randint(8, 20)
                eq=self.eq.create(46, count)
            else:
                eq=self.eq.create(ID)
        else:
            eq=None
        if eq:
            self.ect.randomEnchant(eq)      #随机附魔（包括了第六级的附魔）
        else:
            self.inf.prefabTell('box0')
        return eq

    @staticmethod
    def norm(x):
        return np.exp((-x**2)/12)

    def dropOne(self, item, x, y):
        if item:
            if item.label==0:
                self.ect.randomEnchant(item)
            self.pool[(x, y)]=item
            self.setChar(x, y, item.ID)
        

class Equip:
    def __init__(self, ID=0, x=0, y=0):
        self.items={}
        self.label=0
        self.ID=ID           #装备id
        self.atk=0          #使用装备后，使用者攻击+self.atk(可为负值)
        self.defc=0
        self.magic=0
        self.speed=0
        self.weight=0           #自重
        self.price=0        #买入价格
        self.origin_price=0
        self.lvl=0              #物品等级（与物品掉率有关）
        self.gnrt_lvl=0             #物品自然生成等级标签
        self.name=None          #物品名字
        self.basic_name=None            #物品最初始的名字（用于词缀添加）
        self.describe=None
        self.equipped=0
        self.tag='Others'
        self.posx, self.posy=x, y
        self.energy=0
        self.count=1
        self.form_desc=[]
        self.name_set=False             #名字设定完成标签
        self.longRange=False            #远程武器指示标签
        self.weaponTag = {1: 'This will set fire on your enemies', 2: 'This can drain the blood of your enemies',
                          3: 'Your enemies will be stunned by this', 4: 'Your enemies will be knock back',
                          5: 'This weapon absorbs the sorcery of chaos',
                          6: 'Your enemies will be frozen by this', 7: 'The weapon can poison your enemies',
                          8: 'This can breach the armor of your enemies',
                          9: 'This offers penetrate attack to multiple enemies',
                          10: 'This offers splash damage to multiple enemies', 11: 'This will shed light on your path',
                          12: 'This will blind your eyes, makes it more vulnerable to the dark.'}

    def getInfo(self):
        with open(os.path.join("equipment", "equipment.json")) as read:
            self.items=json.load(read)

    def loadAttri(self, item, prefix=[]):            #从文档中获取对应装备的信息
        self.label, self.atk, self.defc, self.magic, self.speed=(item[0],
               item[1], item[2], item[3], item[4])
        self.weight, self.price, self.lvl, self.gnrt_lvl=(item[5],
               item[6], item[7], item[8])
        self.name, self.describe, self.tag=(item[9],
               item[10], item[11])
        if not self.label:
            self.prefix, self.enchant_lvl, self.attr=(item[12],
               item[13], item[14])
            if not self.prefix:
                self.prefix=prefix
        self.basic_name=self.name
        self.origin_price=self.price
        self.energy=item[-4]            #用了负数索引
        self.equipped=item[-2]
        self.longRange=item[-1]
        
        
    def getLabel(self, ID):
        i=str(ID)
        return self.items[ i ][0]

    def createEquip(self, ID, x, y, prefix=[]):
        label=self.getLabel(ID)
        if label:
            eq=Unenchant(ID, x, y)
            eq.loadAttri(self.items[ str(ID) ])
        else:
            eq = Enchant(ID, x, y)
            eq.loadAttri(self.items[ str(ID) ], prefix)
            eq.formName()
            eq.setUpAttri()
        eq.getDesc()
        return eq

    def create(self, ID, num=1, prefix=[]):       #（直接生成在玩家背包里）(或生成无位置信息的地面装备)
        label=self.getLabel(ID)
        if label:
            eq=Unenchant(ID)
            eq.loadAttri(self.items[ str(ID) ])
        else:
            eq = Enchant(ID)
            eq.loadAttri(self.items[ str(ID) ], prefix)
            eq.formName()
            eq.setUpAttri()
        eq.count=num
        eq.getDesc()
        return eq

    def getDesc(self):          #生成对应的描述
        self.form_desc=[]
        if self.atk>0:          #1atk
            self.form_desc.append('It can boost your attack skills.')
        elif self.atk<0:
            self.form_desc.append('It will hinder your movement when attacking.')
        else:
            self.form_desc.append('It is not helpful to your attacking still.')
        if self.defc>0:         #2defc
            self.form_desc.append('It enhances your defensive skills.')
        elif self.defc<0:
            self.form_desc.append('It shall reveal your weakness.')
        else:
            self.form_desc.append('It is not helpful for your defence.')
        if self.magic>0:            #3magic
            self.form_desc.append('It consolidates your spiritual power.')
        elif self.magic<0:
            self.form_desc.append('It will make you doubt your faith.')
        else:
            self.form_desc.append('It helps nothing to enchance your magic skills.')
        if self.speed>0:            #4speed
            self.form_desc.append('It feels like feather and touches like silk.')
        elif self.speed<0:
            self.form_desc.append('It is like heavy chains which restricts you.')
        else:
            self.form_desc.append('It will not help you to gain dexterity.')
        if self.label:
            self.form_desc.append('You will not enchant this item.')
            self.form_desc.extend(self.attrDesc())
            self.form_desc.append(0)
        else:
            if self.enchant_lvl>5: self.form_desc.append('It is a top class equipment, a relic.')
            else: self.form_desc.append('It is common to see objects like this.')
            self.form_desc.extend(self.attrDesc(self.attr))
            for i in self.attr:
                if i<13:
                    self.form_desc.append(self.weaponTag[i])
            self.form_desc.append(len(self.attr)) if self.tag in {'Right', 'Dual'} else self.form_desc.append(0)

    def formName(self):         #生成带词缀的名字
        if not self.name_set and self.lvl<=5:
            self.name_set=True
            with open(os.path.join("data", "attributes.json")) as read:
                tem=json.load(read)
                self.name=self.basic_name
                for i in self.prefix:
                    self.name=f'{tem[str(i)][0]} {self.name}'
            self.priceMultiplier(tem)
        else:
            self.price=int(self.price*1.5)

    def priceMultiplier(self, dct):      #词缀会影响物品的价格，好词缀的物品更加地贵
        self.price=self.origin_price
        for i in self.prefix:
            if self.origin_price<=1200:
                price_plus=self.origin_price*dct[str(i)][6]
                if price_plus>0:
                    self.price+=self.origin_price*dct[str(i)][6]*1.5
                else:
                    self.price+=self.origin_price*dct[str(i)][6]
            else:
                self.price+=self.origin_price*dct[str(i)][6]        #词缀字典对应的值列表第六位是比例价格比例系数
        self.price=int(self.price)

    #各种防护属性的描述
    @staticmethod
    def attrDesc(attr=None):
        origin=["Poison Resistance: Lvl. 0 / 4", "Fire Resistance: Lvl. 0 / 4",
                "Wizardry Resistance: Lvl. 0 / 4 ", "Cryo Resistance: Lvl. 0 / 4",
                "Blocking Rate: Lvl. 0 / 4"]
        if not attr: return origin
        for tag in attr:
            if tag>=13:
                if tag in {13, 14, 15, 16}:
                    poisonR = 17 % tag
                    origin[0] = "Poison Resistance: Lvl. %d / 4" % poisonR
                elif tag in {17, 18, 19, 20}:
                    fireR = (21 % tag)
                    origin[1] = "Fire Resistance: Lvl. %d / 4" % fireR
                elif tag in {21, 22, 23, 24}:
                    magicR = (25 % tag)
                    origin[2] = "Wizardry Resistance: Lvl. %d / 4 " % magicR
                elif tag in {25, 26, 27, 28}:
                    iceR = (29 % tag)
                    origin[3] = "Cryo Resistance: Lvl. %d / 4" % iceR
                elif tag in {29, 30, 31, 32}:
                    brate = (33 % tag)
                    origin[4] = "Blocking Rate: Lvl. %d / 4" % brate
        return origin

    
class Enchant(Equip):            #weapon是近战武器
    def __init__(self, ID, x=0, y=0):
        super().__init__( ID, x, y)
        self.label=0
        self.id=ID
        self.prefix=[]        #词缀
        self.enchant_lvl=0
        self.attr=[]

    def setUpAttri(self):       #附魔时，所有属性对应加上
        with open(os.path.join("data", "attributes.json"), 'r') as read:
            tem=json.load(read)
        for i in self.prefix:
            self.atk+=tem[str(i)][1]
            self.defc+=tem[str(i)][2]
            self.magic+=tem[str(i)][3]
            self.speed+=tem[str(i)][4]
            if tem[str(i)][5]==1:
                self.weight*=2

    def deSetAttri(self):           #退魔时，所有属性对照减去
        with open(os.path.join("data", "attributes.json"), 'r') as read:
            tem=json.load(read)
        for i in self.prefix:
            self.atk-=tem[str(i)][1]
            self.defc-=tem[str(i)][2]
            self.magic-=tem[str(i)][3]
            self.speed-=tem[str(i)][4]
            if tem[str(i)][4]==1:
                self.weight/=2
                self.weight=int(self.weight)
            elif tem[str(i)][4]==2:
                self.price/=2
                self.price=int(self.price)

class Unenchant(Equip):            #weapon是近战武器
    def __init__(self, ID, x=0, y=0):
        super().__init__(ID, x, y)
        self.label=1
        self.id=ID



    
        
