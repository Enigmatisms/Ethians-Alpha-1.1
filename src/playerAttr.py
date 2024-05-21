import os
#!/usr/bin/env python3
#-*-coding:utf-8-*-
from src.calc import Calc
import random

__author__='SEe3Hz'

class Pattr:
    def __init__(self):
        self.__hp, self.__atk=0, 0
        self.__old_hp, self.__max_hp=0, 16
        self.__defence, self.__magic=0, 0
        self.__speed, self.__exp=0, 0
        self.__need_exp=12           #每一级需要的经验值
        self.__block_rate=0
        self.__weight=40
        self.__carring=0
        self.__level=0
        self.__score=0
        self.__career=-1
        self.__task=None
        self.LR=6       #光照范围
        self.blind=False
        self.frozen=False
        self.bleeding = False
        self.kill_dict={2*i:0 for i in range(25)}
        self.__equips=({'Left':0, 'Right':0, 'Head':0, 'Armoos.path.join(":0, ")Leg':0, 'Necklace':0,
                        'Ring':0, 'Feet':0, 'Wand':0, 'Book':0, 'Cape':0, 'Amulet':0, 'Dual':0, 'Arrow':0})      #考虑加一项Dual
        self.nowLvl=0           #每次生成地图时会对应更新
        self.cc=Calc()
        self.__bag=list()
        self.eqf, self.loopSetter=None, None            #传入一个hq方法
        self.gui=None
        self.__stat={1:0, 2:0, 3:0, 5:0, 6:0, 7:0}        #人物状态
        self.stat_lst={1:self.stat1, 2:self.stat2, 3:self.stat3, 5:self.stat5, 6:self.stat6, 7:self.stat7}         #遍历使用
        self.deepest_lvl=0          #地牢最深层
        self.inUse = None
        #五项抗性: 毒抗（中毒不造成伤害概率），火抗（火焰伤害），魔抗（受伤几率），物抗（格挡几率）
        self.poisonR=0
        self.fireR=0
        self.iceR=0
        self.magicR=0
        self.itemTags={i:0 for i in range(1,11)}        #右手或双手武器的属性可以堆在这里
        self.inf=None
        self.dungeon=random.sample([2,3,4,5,6,7,8,9,10, -1, -1, -1, -1], k=5)       #地图属性


    '''===========背包方法============'''
    def putInBag(self, stuff):      #背包里直接储存类的实例！
        if self.weightMeasure(stuff):
            self.carring_adder(stuff.weight)
            for k in self.__bag:
                if stuff.name==k.name and stuff.tag!='Arrow':
                    k.count += stuff.count
                    break
                elif stuff.name==k.name and stuff.tag=='Arrow':       #弓箭在数量上不堆叠，能量堆叠
                    k.energy += stuff.energy
                    break
            else:
                self.__bag.append(stuff)        #背包里没有就添加
            self.inf.prefabTell('pickup', back=self.inf.measure(stuff.count, stuff.tag, stuff.name))
            return True
        else:
            self.inf.prefabTell('ovrw')
            return False

    def weightMeasure(self, stuff):
        if self.carring_getter()+stuff.weight>self.weight_getter():
            return False
        else:
            return True

    def throwAway(self, stuff, tag=0):        #tag为1时为丢弃全部
        if stuff in self.__bag:
            if stuff.equipped==1:          #装备好的物品丢弃要先取下
                self.deEquip(stuff)
            if tag and stuff.weight==0:
                self.inf.prefabTell('throw', back=self.inf.measure(stuff.count, stuff.tag, stuff.name))
                self.__bag.remove(stuff)
            elif tag and stuff.weight != 0 and stuff.count>1:         #有重量物品不可一次性全部丢弃
                #TBS!!
                self.inf.prefabTell('throwx')
                return False
            else:
                self.inf.prefabTell('pickup', back=self.inf.measure(1, stuff.tag, stuff.name))
                if stuff.count>1:
                    stuff.count-=1
                else:
                    self.__bag.remove(stuff)
            self.carring_adder(-stuff.weight)
            return True
        else:
            return False

    '''=========================================================================================='''
    def equipTest(self):        #self.__equips相当于只是个地址字典，装备都储存在self.__bag中，但是装备上的装备会复制储存到self.__equips中
        num=self.gui.flag+16*self.gui.page_now
        stuff=self.__bag[num]
        if not stuff.equipped and stuff.tag in {'Task', 'Others'}:          #防止无法装备的物品被装备
            self.gui.reset()
            self.gui.quitSetter()
            self.gui.quitSetter()
            return
        if stuff.tag != 'Dual':     #装备的不是双手武器时，正常进行
            if stuff.tag=='Bow':
                if self.getEquip('Left'):
                    self.Equip(stuff)
                else:
                    self.swapItem(stuff)
            else:
                if self.getEquip(stuff.tag):
                    self.Equip(stuff)
                else:
                    self.swapItem(stuff)        #若对应标签的装备已经有物品了，就交换未装备和已装备
                #包括了：当装备了双持武器之后，如果要装备单手武器，会deEquip(stuff=1)
                #deEquip(stuff=1)时会触发deEquip(self.__equips['Dual'])，则可以去装备
        else:       #装备双持武器：如果已经装备了双持武器, 则卸下，如果装备的是单手武器，也是卸下
            if self.__equips['Left'] or self.__equips['Right']:
                if self.__equips['Dual']:       #如果双持武器标签不为零，说明LEFT,RIGHT必然为1
                    self.deEquip(self.__equips['Dual'])
                    self.__equips['Left'], self.__equips['Right']=0,0
                else:       #没有双持，则卸下对应武器
                    self.deEquip(self.__equips['Left'])
                    self.deEquip(self.__equips['Right'])
            self.Equip(stuff)
        self.gui.reset()
        self.gui.quitSetter()
        self.gui.quitSetter()

    '''==========================================================================================='''
    def deEquipTest(self):          #卸下的文字API
        num=self.gui.flag+16*self.gui.page_now
        stuff=self.__bag[num]
        if stuff:
            self.deEquip(stuff)
        self.gui.reset()
        self.gui.quitSetter()
        self.gui.quitSetter()

    '''==========================================================================================='''
    def getItem(self, name):                #TBS：通过名字寻找已装备的物品实例，用于API deEquip，之后不需要
        for k,v in self.__equips.items():
            if v and v != 1:
                if v.name==name:
                    return v            #直接返回字典对应的值，是一个类的实例
        return None

    def swapItem(self, stuff):      #单个物品交换
        if stuff.tag=='Bow':
            self.deEquip(self.__equips['Left'])
        else:
            self.deEquip(self.__equips[stuff.tag])
        self.Equip(stuff)

    '''=========================================================================================='''
    def deEquip(self, stuff):
        if stuff and stuff != 1:       #双持武器比较特殊，要求双手都卸下武器才能装备，这就可能导致某一只手没武器时卸下
            self.inf.prefabTell('deq', back=stuff.name)
            if stuff.equipped==1:          #TBS: （这个判断后期可以去掉）只有装备了装备才能取下
                self.atk_adder(-stuff.atk)
                self.def_adder(-stuff.defc)
                self.magic_adder(-stuff.magic)
                self.speed_adder(-stuff.speed)
                if stuff.label == 0:
                    for i in stuff.attr:  # 物品攻击属性
                        if stuff.tag in {'Dual', 'Right'}: self.itemTags[i] -= 1
                        self.armorAttri(i, -1)
                name=stuff.name         #TBS：所有同名的物品都要卸下（这个地方需要改，因为以后会有战士双持能力）
                for i in self.__bag:            #TBS：遍历搜索（在物品较多时较慢，物品数量将不会超过100）
                    if i.name==name:
                        i.equipped=0
                if stuff.tag=='Dual':       #双手武器不太一样
                    self.__equips['Left'], self.__equips['Right']=0,0
                    self.__equips[stuff.tag]=0
                elif stuff.tag=='Bow':
                    self.__equips['Left']=0
                else:
                    self.__equips[stuff.tag]=0
        if stuff == 1:
            self.inf.prefabTell('deq', self.__equips['Dual'].name)
            self.deEquip(self.__equips['Dual'])
        '''目的解释：当装备双手武器需要卸下时，由于装备双手武器时左右手都被设为1
        所以在卸下时需要重新设为0，但实际上stuff为1时，不是实例，没有属性，如果
        不设置判断将会报错，在stuff等于1时只需要设置为0即可
                stuff为1时，触发deEquip( 1 )只可能在“已经装备双手武器的情况下，要装备单手武器“时
        此时由于Left或Right为1，则要”取下“1,方法就是直接取下双持武器，执行时：
        self.__equips['Left'], self.__equips['Right']=0,0
        '''
    def getEquipped(self):
        return self.__equips

    def armorAttri(self, tag, multiplier=1):
        if tag in {13, 14, 15, 16}:         #毒抗
            self.poisonR += (17 % tag) * multiplier
            self.poisonR = min(4, self.poisonR)
        elif tag in {17, 18, 19, 20}:       #火抗
            self.fireR += (21 % tag) * multiplier
            self.fireR = min(4, self.fireR)
        elif tag in {21, 22, 23, 24}:           #魔防
            self.magicR += (25 % tag) * multiplier
            self.magicR = min(self.magicR, 4)
        elif tag in {25, 26, 27, 28}:           #冰抗
            self.iceR += (29 % tag) * multiplier
            self.iceR = min(self.iceR, 4)
        elif tag in {29, 30, 31, 32}:           #物抗
            self.brate_adder((33 % tag) * multiplier)
        elif tag ==11:      #光明
            self.LR += 1 * multiplier
        elif tag==12:       #黑暗
            self.LR -= 1 * multiplier

    def Equip(self, stuff):
        if not stuff.equipped:          #TBS: （这个判断后期可以去掉）防止重复装备
            if self.career_getter()==0 and (stuff.tag in {'Bow', 'Book', 'Arrow'}
                    or (stuff.longRange and stuff.tag !='Wand')):        #战士不可使用书籍或是远程武器
                self.inf.prefabTell("berserker", back=stuff.name)
                return
            elif self.career_getter()==1 and stuff.tag=='Book':
                self.inf.prefabTell("archer", back=stuff.name)
                return
            elif self.career_getter()==2 and (stuff.tag in {'Bow', 'Arrow'} or (stuff.longRange
                    and not stuff.tag in {'Wand', 'Book'})):
                self.inf.prefabTell("sorcerer", back=stuff.name)
                return
            self.atk_adder(stuff.atk)
            self.def_adder(stuff.defc)
            self.magic_adder(stuff.magic)
            self.speed_adder(stuff.speed)
            if stuff.label==0:
                for i in stuff.attr:        #物品攻击属性
                    if stuff.tag in {'Dual', 'Right'} and i<11: self.itemTags[i]+=1
                    self.armorAttri(i)
            stuff.equipped=1
            if stuff.tag=='Dual':       #双手武器不太一样
                self.__equips['Left']=1
                self.__equips['Right']=1
                self.__equips['Dual']=stuff
            elif stuff.tag=='Bow':
                self.__equips['Left']=stuff
            else:
                self.__equips[stuff.tag]=stuff
            self.inf.prefabTell('eq', back=stuff.name)

    def getEquip(self, tag):            #根据物品标签来搜索是否已经装备
        if self.__equips[ tag ]:
            return False
        else:
            return True

    def getBag(self):
        return self.__bag

    def useItem(self, item):         #主动使用      设置inUse(正在使用的远程武器)
        #TBS：需要写一个函数：对Item使用此方法会触发其效用
        self.inf.prefabTell('attack')
        if item.tag=='Bow':
            if self.getEquip('Arrow'):
                self.useItem(self.__equips['Arrow'])
        elif item.tag=='Book':
            self.inUse=item
        else:
            if item.energy and item.count:
                if item.tag=='Wand' or item.tag=='Arrow':           #判断,使用能量物品时，有能量物品标签的物品能量为0时自动删除
                    self.inUse=item
                else:
                    self.inUse=None
            else:
                if not item.count or item.energy:          #数量为0时自动删除
                    if item.equipped==1:       #若装备了，则取下
                        self.deEquip(item)
                    self.__bag.remove(item)
                    self.inUse=None

    def useInUse(self):         #使用正在使用的武器
        if self.inUse.energy:
            self.inUse.energy-=1
            if self.inUse.tag=='Wand' or self.inUse.tag=='Arrow':           #判断,使用能量物品时，有能量物品标签的物品能量为0时自动删除
                if not self.inUse.energy:
                    self.deEquip(self.inUse)
                    self.__bag.remove(self.inUse)
            elif self.inUse.energy==0 and self.inUse.count:
                if not self.inUse.count:          #数量为0时自动删除
                    if self.inUse.equipped==1:       #若装备了，则取下
                        self.deEquip(self.inUse)
                    self.__bag.remove(self.inUse)

    def inUseAmmo(self):            #判断装备的物品是否有能量剩余
        if self.inUse.tag=='Wand' or self.inUse.tag=='Arrow':
            if self.inUse.energy<=0:
                return False
            else:
                return True
        elif self.inUse.tag=='Book':        #法书能量无限
            return True
        else:
            return False

    def inUseID(self):
        return self.inUse.ID if self.inUse else -1

    def inUseTag(self):
        if self.inUse:
            if self.inUse.tag in {'Arrow', 'Bow', 'Dual'}:
                return 1
            elif self.inUse.tag=='Book':
                return 2
            elif self.inUse.tag in {'Others', 'Wand'}:
                return 3
        return 0

    def getMoney(self):
        for i in self.__bag:
            if i.ID==46:
                return i.count
        return 0

    def haveKey(self):          #判断是否有钥匙
        for i in self.__bag:
            if i.ID in [117, 118, 186]:
                return True
        return False

    def useKey(self, tag=0):            #在背包中搜索key,使用优先级为普通钥匙，金钥匙，冰霜钥匙
        #tag=0是指最低级的锁，可以用任意钥匙打开
        lst=[118, 117, 186]
        judge=0
        for k in lst[tag:]: #切片
            if judge:
                break
            length=len(self.__bag)
            for i in range(length):
                if self.__bag[i].ID==k:
                    self.__bag[i].count-=1
                    judge=1
                    if self.__bag[i].count==0:
                        del self.__bag[i]
                    break
    '''=============================================='''
        
    def career_setup(self, career):
        self.reset()
        if career == 0:     #战士！
            self.hp_setter(21)     #21
            self.maxhp_setter(21)
            self.atk_setter(18)         #18
            self.def_setter(15)         #15
            self.magic_setter(0)
            self.speed_setter(10)        #10
            self.weight_setter(43)
            self.lv_adder()
            self.__career_setter(0)
            self.eqf.bagSetUp(0, self.__bag)
        elif career == 2:       #法师！
            self.hp_setter(15)
            self.maxhp_setter(15)
            self.atk_setter(10)
            self.def_setter(10)
            self.magic_setter(18)
            self.speed_setter(10)
            self.weight_setter(39)
            self.lv_adder()
            self.__career_setter(2)
            self.LR+=1
            self.eqf.bagSetUp(2, self.__bag)
        elif career == 1:       #游侠！
            self.hp_setter(18)
            self.maxhp_setter(18)
            self.atk_setter(14)
            self.def_setter(12)
            self.magic_setter(3)
            self.speed_setter(16)
            self.weight_setter(41)
            self.lv_adder()
            self.__career_setter(1)
            self.LR+=2
            self.eqf.bagSetUp(1, self.__bag)
        else:
            raise ValueError('Career number out of range(3).')
        
    '''===================================
        ========各类属性的设置和取得===========
    ==================================='''
    #===========血量属性=============
    def hp_setter(self, val):
        self.__hp=val
        self.__old_hp=val

    def hp_adder(self, val=1):
        self.de_diff()
        self.__hp+=val

    def hp_getter(self):
        return self.__hp

    def diff_getter(self):
        return self.__hp-self.__old_hp

    def de_diff(self):
        self.__old_hp=self.__hp

    def maxhp_setter(self, val):
        self.__max_hp=val

    def maxhp_getter(self):
        return self.__max_hp

    def maxhp_adder(self, val=1):
        self.__max_hp+=val

    #===========攻击属性=============
    def atk_setter(self, val):
        self.__atk=val

    def atk_adder(self, val=1):
        self.__atk+=val

    def atk_getter(self):
        return self.__atk

    #===========防御属性=============
    def def_setter(self, val):
        self.__defence=val

    def def_adder(self, val=1):
        self.__defence+=val

    def def_getter(self):
        return self.__defence

    #===========魔法属性=============
    def magic_setter(self, val):
        self.__magic=val

    def magic_adder(self, val=1):
        self.__magic+=val

    def magic_getter(self):
        return self.__magic

    #===========速度属性=============
    def speed_setter(self, val):
        self.__speed=val

    def speed_adder(self, val=1):
        self.__speed+=val

    def speed_getter(self):
        return self.__speed

    #===========格挡率属性============
    def brate_setter(self, val):
        self.__block_rate=val
        self.__block_rate=min(self.__block_rate, 4)

    def brate_adder(self, val):
        self.__block_rate+=val
        self.__block_rate = min(self.__block_rate, 4)

    def brate_getter(self):
        return self.__block_rate

    #==========经验值===============
    def exp_adder(self, val):
        self.__exp+=val

    def exp_getter(self):
        return self.__exp

    def exp_setter(self, val):
        self.__exp=val

    #===========负重能力=============
    def weight_setter(self, val):
        if val<=210 and val>=30:
            self.__weight=val

    def weight_getter(self):
        return self.__weight

    def weight_adder(self, val=3):
        if self.weight_getter()+val<=210:
            self.__weight+=val

    #=========已经背在身上的重量========
    def carring_getter(self):
        return self.__carring

    def carring_adder(self, val):
        self.__carring+=val

    def carring_setter(self, val):
        self.__carring=val

    #===========等级属性=============
    def lv_adder(self, val=1):
        self.__level+=val

    def lv_getter(self):
        return self.__level
            
    #===========升级所需经验值===========
    def need_getter(self):
        return self.__need_exp

    def need_setter(self):
        self.__need_exp=self.cc.getExp(self.__level)

    #===========积分===============
    def score_adder(self, val):
        self.__score+=val

    def score_getter(self):
        return self.__score

    #限定方法：职业属性只能在一开始设置
    def __career_setter(self, val):
        self.__career=val

    def career_getter(self):
        return self.__career

    def career_str_getter(self):
        if self.__level<50:
            career={0:'Warrior', 2:'Wizard', 1:'Ranger'}
        else:
            career={0:'Berserker', 2:'Conjurer', 1:'Archer'}
        return career[self.career_getter()]
    #=============人物状态=================
    def getStat(self):
        return self.__stat

    def setStat(self, val=1, time=-1):
        self.__stat[val]=time         #状态val持续时间为time

    def stat1(self):            #中毒效果（可能导致死亡）
        if self.poisonR==4:
            self.__stat[1]=0
            return 0
        if self.__stat[1]<=-1:
            self.__stat[1]-=1
        if self.__stat[1]==-13:
            self.__stat[1]=-1
            possi=[0.25*self.poisonR, 0.25*(4-self.poisonR)]
            judge=random.choices([0, 1], possi)[0]
            if judge:
                self.hp_adder(-1)
                if self.hp_getter()<=0:
                    self.inf.deathCause('poison')
                    return 1
        return 0

    def stat2(self):            #燃烧效果（可能导致死亡）
        if self.__stat[2]:
            self.__stat[2]-=1
            self.hp_adder(-1)
            if self.hp_getter() <= 0:
                self.inf.deathCause('burn')
                return 1
        return 0

    def stat3(self):            #失明效果(不致死)
        if self.__stat[3] and self.__stat[3]>1:
            self.__stat[3]-=1
        elif self.__stat[3]==1:
            self.__stat[3] -= 1
            self.LR += 4
            self.blind=False
        return 0

    def stat5(self):        #破甲效果，可能导致死亡
        if self.__stat[5]:
            self.__stat[5]=0
            self.hp_adder(-3)
            if self.hp_getter() <= 0:
                self.inf.deathCause('break')
                return 1
        return 0

    def stat6(self):            #冰冻效果(不会死)
        if self.__stat[6] and self.__stat[6] > 1:
            self.__stat[6] -= 1
        elif self.__stat[6] == 1:
            self.__stat[6] -= 1
            self.__speed += 10
            self.frozen = False
        return 0

    def stat7(self):        #流血效果：药物使用无效（不致死）
        if self.__stat[7] and self.__stat[7] > 1:
            self.__stat[7] -= 1
        elif self.__stat[7] == 1:
            self.__stat[7] -= 1
            self.bleeding = False
        return 0

    def bloodDrain(self, x=0, y=0, tag=0):       #从怪物处吸血,tag=1是治疗卷轴或法杖
        if tag:
            point=random.randint(3, 5)
        else:
            choices = [[1, 2], [0.6, 0.2]]
            point = random.choices(*choices)[0]
        if self.__hp+point>self.__max_hp:
            self.__hp=self.__max_hp
        else:
            self.__hp+=point
        return True

    #==========地牢最深层=============
    def deepestSet(self, lvl):
        if lvl>self.deepest_lvl:
            self.deepest_lvl=lvl

    #==========自动处理部分=============
    def lv_autoAdder(self):     #自动判断经验值升级
        if self.__exp>=self.__need_exp:
            diff=self.__exp-self.__need_exp
            self.exp_setter(diff)       #升级的时候如果经验值超出，则会加到下一次对应的经验中
            self.lv_adder()
            self.need_setter()
            self.auto_effect()
            self.score_adder(self.lv_getter() * 5)
            self.loopSetter(4)
        self.winJudge()

    def auto_effect(self):          #升级增加的属性
        self.hp_adder()
        self.de_diff()
        self.maxhp_adder()
        self.weight_adder()

    def winJudge(self):
        if self.kill_dict[44]:
            self.score_adder(1000)
            self.loopSetter(12)

    def statEffect(self):          #状态存在时，自动进行一些操作
        for k in self.__stat.keys():
            if self.__stat[k]:
                self.stat_lst[k]()

    def death(self, tag=1, win=False):
        text=list()
        text.append(self.career_str_getter())
        if win:
            text.append(self.inf.truimph[self.career_getter()])
            text.append("He has slayed the King of Goblins.")
        else: text.append(self.inf.epitaph[self.career_getter()])        #墓志铭
        text.append('Current Attack Point: %d'%self.__atk)
        text.append('Current Defence Point: %d' % self.__defence)
        text.append('Current Magic Point: %d' % self.__magic)
        text.append('Current Speed Point: %d' % self.__speed)
        text.append('Current Fire Resistance: %d' % self.fireR)
        text.append('Current Ice Resistance: %d' % self.iceR)
        text.append('Current Poison Resistance: %d' %self.poisonR)
        text.append('Current Wizardry Resistance: %d' % self.magicR)
        text.append('Current Blocking Rate: %d' % self.__block_rate)
        if tag:         #tag=1对应了loop9死亡界面输出的信息
            for k in self.__stat.keys():
                if self.__stat[k]:
                    text.append(self.inf.stat_death[k])
        elif not tag and not win: text.append(self.inf.death)
        text.append('Current Level: %d'%self.__level)
        text.append('Current Scores: %d'%self.__score)
        if not win: text.append('Gold Coins Lost: %d g'%self.getMoney())
        else: text.append('Gold Coins He had: %d g'%self.getMoney())
        if not win: text.append('Deepest Level of Dungeon Reached: %d'%self.deepest_lvl)
        length=len(text)
        if not tag:
            for i in range(length):
                text[i]=text[i].replace("Current", "His")
            text.append(self.career_getter())
        return text

    def winSentence(self):
        text=list()
        text.append(self.career_str_getter())
        text.append(self.inf.truimph[self.career_getter()])
        text.append("You have slayed the King of Goblins.")
        text.append('Your Level: %d' % self.__level)
        text.append('Your Scores: %d' % self.__score)
        text.append('Gold Coins You Have: %d g' % self.getMoney())
        text.append(self.career_getter())
        return text

    def reset(self):       #重置
        self.__hp, self.__atk = 0, 0
        self.__old_hp, self.__max_hp = 0, 16
        self.__defence, self.__magic = 0, 0
        self.__speed, self.__exp = 0, 0
        self.__need_exp = 12  # 每一级需要的经验值
        self.__block_rate = 0
        self.__weight = 40
        self.__carring = 0
        self.__level = 0
        self.__score = 0
        self.__career = -1
        self.__task = None
        self.LR = 6  # 光照范围
        self.blind = False
        self.frozen = False
        self.bleeding = False
        self.kill_dict={2*i:0 for i in range(25)}
        self.__equips = ({'Left': 0, 'Right': 0, 'Head': 0, 'Armor': 0, 'Leg': 0, 'Necklace': 0,
                          'Ring': 0, 'Feet': 0, 'Wand': 0, 'Book': 0, 'Cape': 0, 'Amulet': 0, 'Dual': 0,
                          'Arrow': 0})  # 考虑加一项Dual
        self.nowLvl = 0  # 每次生成地图时会对应更新
        self.__bag = []
        self.__stat = {1: 0, 2: 0, 3: 0, 5: 0, 6: 0, 7: 0}
        self.deepest_lvl = 0  # 地牢最深层
        self.inUse = None
        # 五项抗性: 毒抗（中毒不造成伤害概率），火抗（火焰伤害），魔抗（受伤几率），物抗（格挡几率）
        self.poisonR = 0
        self.fireR = 0
        self.iceR = 0
        self.magicR = 0
        self.itemTags={1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
        self.inf.reset()
        self.dungeon = random.sample([2, 3, 4, 5, 6, 7, 8, 9, 10], k=5)  # 地图属性

