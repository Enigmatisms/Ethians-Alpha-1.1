#!/usr/bin/env python3
#-*-coding:utf-8-*-

import sys
sys.path.append("..")
from equipment.enchant import *


class EquipFunction:
    def __init__(self):
        self.ptr=None
        self.eq=None
        self.gui=None
        self.pl=None
        self.inf=None
        self.ect=EnchantItem()
        self.text=[]

    def bagSetUp(self, career, bag):         #随机创建三个职业的初始物品集，只在选择完职业之后使用一次
        bag.clear()
        eq = self.eq.create(2, 2)       #两个小回复药剂
        bag.append(eq)
        eq = self.eq.create(46, 100)        #100金币
        bag.append(eq)
        eq = self.eq.create(118)        #一把铁钥匙
        bag.append(eq)
        eq = self.eq.create(119, 3)     #三个返回卷轴
        bag.append(eq)
        eq = self.eq.create(121, 2)     #2个蘑菇
        bag.append(eq)
        if career==0:
            eq = self.eq.create(58)  # 短剑
            self.ptr.carring_adder(eq.weight)
            bag.append(eq)
            eq = self.eq.create(96)  # 小盾
            self.ptr.carring_adder(eq.weight)
            bag.append(eq)
            eq = self.eq.create(86)  # 皮甲
            self.ptr.carring_adder(eq.weight)
            bag.append(eq)
        elif career==2:
            eq = self.eq.create(53)  # 长棍
            self.ptr.carring_adder(eq.weight)
            bag.append(eq)
            eq = self.eq.create(83)  # 长袍
            self.ptr.carring_adder(eq.weight)
            bag.append(eq)
            eq = self.eq.create(114)  # 火焰咒书
            self.ptr.carring_adder(eq.weight)
            bag.append(eq)
        elif career==1:
            eq = self.eq.create(64)  # 弓
            self.ptr.carring_adder(eq.weight)
            bag.append(eq)
            eq = self.eq.create(66)  #箭
            bag.append(eq)
            eq = self.eq.create(80)  # 披风
            self.ptr.carring_adder(eq.weight)
            bag.append(eq)
            eq = self.eq.create(57)  # 匕首
            self.ptr.carring_adder(eq.weight)
            bag.append(eq)

    def create(self, ID, num=1, prefix=[]):        #一般来说这个方法不会创建有重量物品，多用于地图，卷轴，金币，药水等
        eq=self.eq.create(ID, num, prefix)
        length=len(self.ptr.getBag())
        for i in range(length):     #并非直接在背包里创建另一个物品,如果背包本来就有这个物品，则不创建，进行某些参数的更改
            if eq.ID == self.ptr.getBag()[i].ID:
                if self.ptr.getBag()[i].tag=='Arrow':
                    self.ptr.getBag()[i].energy+=eq.energy
                else:
                    self.ptr.getBag()[i].count+=eq.count
                return True
        self.ptr.getBag().append(eq)
        return False


    def returnItem(self, ID, num=1, prefix=[]):        #直接在商人和牧师背包里创建物品用（用于owner的createBag()函数）
        eq=self.eq.create(ID, num, prefix)
        return eq

    '''=======================以下是GUI界面支持代码==========================='''
    def getBagInfo(self, bag, page):          #ezgui会传入相应的list
        lst=[]
        length=len(bag)
        maxi=int(len(bag)/16)+1
        if page<maxi-1:
            for i in range(page*16, 16*page+16):
                a, b, c, d=(str(bag[i].count), self.getName(bag[i].name), (' '+str(bag[i].atk)+'/'+str(bag[i].defc)+'/'+
                      str(bag[i].magic)+'/'+str(bag[i].speed)), (str(bag[i].price)+' g'))

                text="%-4s%-17s%-13s%8s"%(a, b, c, d)
                if bag[i].equipped == 1: text+='1'
                lst.append(text)
        else:
            for i in range(page*16, length):
                a, b, c, d=(str(bag[i].count), self.getName(bag[i].name), (' '+str(bag[i].atk)+'/'+str(bag[i].defc)+'/'+
                      str(bag[i].magic)+'/'+str(bag[i].speed)), (str(bag[i].price)+' g'))
                text="%-4s %-17s%-13s%8s"%(a, b, c, d)
                '''text=(str(bag[i].count)+'  '+bag[i].name+'  '+str(bag[i].atk)+'/ '+str(bag[i].defc)+'/ '+
                      str(bag[i].magic)+'/ '+str(bag[i].speed)+'          '+str(bag[i].price)+' g')'''
                if bag[i].equipped == 1: text += '1'
                lst.append(text)
        return lst

    @staticmethod
    def getName(item):
        if len(item)>=19:
            name=item[:12]+'...'
        else:
            name=item
        return name

    @staticmethod
    def getImgInfo(bag, page):      #提供每张装备图的ID
        lst=[]
        length=len(bag)
        maxi=int(len(bag)/16)+1
        if page<maxi-1:
            for i in range(page*16,page*16+16):
                lst.append(bag[i].ID)
        else:
            for i in range(page*16, length):
                lst.append(bag[i].ID)
        return lst

    @staticmethod
    def getPosInfo(bag, page):          #给ezgui提供每个装备信息的放置位置
        num=len(bag)-page*16
        lst=[]
        if num<=8:
            for i in range(num):      #第一纵列
                pos1=(110, 160, 146+i*54)
                lst.append(pos1)
        elif num>8 and num<=16:
            for i in range(8):      #第一纵列
                pos1=(110, 160, 146+i*54)
                lst.append(pos1)
            for i in range(8, num):      #第二纵列
                pos1=(660, 710, 94+(i-8)*54)
                lst.append(pos1)
        elif num>16:
            for i in range(8):      #第一纵列
                pos1=(110, 160, 146+i*54)
                lst.append(pos1)
            for i in range(8, 16):      #第二纵列
                pos1=(660, 710, 94+(i-8)*54)
                lst.append(pos1)
        return lst

    def funcsForGUI(self):      #main函数中，eqf的gui设置之后立即执行，给gui传入必要参数
        self.gui.equip_funcs={2:self.enchant, 3:self.deEnchant, 4:self.partial(self.heal, 1), 5:self.partial(self.heal, 2),
                              6:self.partial(self.heal, 3),7:self.partial(self.heal, 4), 8:self.dePoison, 9:self.strength, 10:self.defence,
                              11:self.magic, 12:self.speed, 13:self.strange_mix, 14:self.returnScroll, 15:self.tpScroll, 16:self.map,
                              17:self.passby, 18:self.summon, 19:self.knowledge, 20:self.locker}

    @staticmethod
    def partial(func, arg):         #偏函数
        def f():
            func(arg)
        return f

    '''=========================以下为装备携带的功能========================'''
    def enchant(self):      #2:附魔
        self.gui.current_npc=0
        self.gui.img_num=2
        self.gui.quitSetter()
        self.gui.getPage(self.ptr.getBag())
        self.gui.pageDisplayPrep()
        self.gui.page_now, self.bag_now=0, self.ptr.getBag()
        self.gui.prepImg(self.ptr.getBag(), self.gui.page_now)
        self.gui.func_tag=1
        self.gui.bigFunc=self.ect.enchant
        self.inf.prefabTell('enchant')

    def deEnchant(self):        #3：退魔
        self.gui.current_npc=0
        self.gui.img_num=2
        self.gui.quitSetter()
        self.gui.getPage(self.ptr.getBag())
        self.gui.pageDisplayPrep()
        self.gui.page_now, self.bag_now=0, self.ptr.getBag()
        self.gui.prepImg(self.ptr.getBag(), self.gui.page_now)
        self.gui.func_tag=1
        self.gui.bigFunc=self.ect.deEnchant
        self.inf.prefabTell('decay')

    def passby(self):       #没事干函数
        #比如你想装备金币的时候，金币无法装备又不能报错。。。那就跳过吧
        self.gui.quitSetter()
        self.gui.quitSetter()

    def heal(self, tag):        #5:恢复生命（中）
        if not self.ptr.bleeding:
            hold = int(self.ptr.maxhp_getter() / 4)
            if self.ptr.hp_getter() <= hold:  # 濒死状态加成
                judge = True
            else:
                judge = False
            if judge:
                hp = 6 + (tag - 1) * 4
                if self.ptr.hp_getter() + hp > self.ptr.maxhp_getter():
                    self.ptr.hp_setter(self.ptr.maxhp_getter())
                else:
                    self.ptr.hp_adder(hp)
            else:
                hp = 3 + (tag - 1) * 4
                if self.ptr.hp_getter() + hp > self.ptr.maxhp_getter():
                    self.ptr.hp_setter(self.ptr.maxhp_getter())
                else:
                    self.ptr.hp_adder(hp)
            self.ptr.setStat(7, 20)     #药剂恶心效果
            self.inf.prefabTell('potionx')
            self.inf.prefabTell('cure', back=hp)
        else:
            self.inf.prefabTell('bleed')
            self.inf.prefabTell('no')
        self.gui.quitSetter()
        self.gui.quitSetter()

    def dePoison(self):         #8:解毒
        self.inf.prefabTell('poison-')
        self.ptr.setStat(1, 0)
        self.heal(1)

    def strength(self):         #9：强壮药剂
        self.inf.prefabTell('atk+', back=1)
        self.ptr.atk_adder(1)
        self.gui.quitSetter()
        self.gui.quitSetter()

    def defence(self):          #10：防御药剂
        self.inf.prefabTell('defc+', back=1)
        self.ptr.def_adder(1)
        self.gui.quitSetter()
        self.gui.quitSetter()

    def magic(self):            #11: 魔法药剂
        self.inf.prefabTell('mgc+', back=1)
        self.ptr.magic_adder(1)
        self.gui.quitSetter()
        self.gui.quitSetter()

    def speed(self):            #12：加速药剂
        self.inf.prefabTell('spd+', back=1)
        self.ptr.speed_adder(1)
        self.gui.quitSetter()
        self.gui.quitSetter()

    def strange_mix(self):          #13：奇异药剂
        possi=[0.55, 0.42, 0.03]
        choice=random.choices([1,2,3], possi)[0]
        choices=[1,2,3,4]
        lst=random.choices(choices, k=choice)
        points=[-2, -1, 0, 1, 2]
        chance=[0.03, 0.36, 0.2, 0.36, 0.05]
        if 1 in lst:
            p=random.choices(points, chance)[0]
            if p>0: self.inf.prefabTell('atk+', back=p)
            elif p<0: self.inf.prefabTell('atk-', back=p)
            else: self.inf.prefabTell('no')
            self.ptr.atk_adder(p)
        elif 2 in lst:
            p=random.choices(points, chance)[0]
            if p>0: self.inf.prefabTell('defc+', back=p)
            elif p<0: self.inf.prefabTell('defc-', back=p)
            else: self.inf.prefabTell('no')
            self.ptr.def_adder(p)
        elif 3 in lst:
            p=random.choices(points, chance)[0]
            if p>0: self.inf.prefabTell('mgc+', back=p)
            elif p<0: self.inf.prefabTell('mgc-', back=p)
            else: self.inf.prefabTell('no')
            self.ptr.magic_adder(p)
        elif 4 in lst:
            p=random.choices(points, chance)[0]
            if p>0: self.inf.prefabTell('spd+', back=p)
            elif p<0: self.inf.prefabTell('spd-', back=p)
            else: self.inf.prefabTell('no')
            self.ptr.speed_adder(p)
        self.gui.quitSetter()
        self.gui.quitSetter()

    def returnScroll(self):     #14:返回卷轴
        self.pl.returnScroll()
        self.gui.quitSetter()
        self.gui.quitSetter()

    def tpScroll(self):         #15：传送卷轴
        self.pl.tpScroll()
        self.gui.quitSetter()
        self.gui.quitSetter()

    def map(self):          #16：地图
        self.pl.clearMist()
        self.gui.quitSetter()
        self.gui.quitSetter()

    def summon(self):       #18：恶魔口袋（召唤）
        self.pl.dg.po.more_mob(radius=4, serve=True)
        self.gui.quitSetter()
        self.gui.quitSetter()

    def knowledge(self):        #19：知识卷轴
        if self.ptr.lv_getter()<=98:
            diff = self.ptr.exp_getter()
            self.ptr.exp_setter(self.ptr.need_getter() + diff)
            self.gui.quitSetter()
            self.ptr.lv_autoAdder()
            self.inf.prefabTell('knowledge')
        else:
            diff = self.ptr.exp_getter()
            self.ptr.exp_setter(self.ptr.need_getter() + diff)
            self.inf.prefabTell('no')


    def locker(self):       #20:锁
        lst=[]
        for i in range(-1, 2):
            for j in range(-1, 2):
                lst.append((self.pl.xat+i, self.pl.yat+j))
        lst.remove((self.pl.xat, self.pl.yat))
        for k in lst:
            if self.pl.dg.sur.getChar(*k) in {0, 1, 3, 4}:
                self.pl.dg.sur.setChar(*k, 12)
                self.inf.prefabTell('&door')
        self.gui.quitSetter()
        self.gui.quitSetter()



            
    
        
        
            
            
            
            
            
    



        

