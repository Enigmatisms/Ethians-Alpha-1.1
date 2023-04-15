#!/usr/bin/env python3
#-*-coding:utf-8-*-

from src.monster import *
from src.blittools import *
from src.calc import Calc

__author__='SEeHz3'
__date__='2019.2.19'

class Pool:
    def __init__(self, surface, func_lst, func, func3):      #func_lst[ 0 ]是dg, func_lst[ 1 ]是dg.sur, func_lst[ 2 ]是npc
        self.func_lst=func_lst
        self.arg_funcs=None        #参数函数列表
        self.recreate=False
        self.mob=Monster
        self.cc=Calc()
        self.screen=surface
        self.mob_pool={}
        self.new_pool={}
        self.pl=func
        self.ptr=None
        self.itemDrop=None      #需要从外界传入的函数（fem）
        self.ms=func3               #除雾mist实例
        #self.level=[[-1 for i in range(42)] for j in range(64)]
        self.no_walk=range(1,64)
        #0-7是史莱姆，8是阴沟鼠，10是大鼠，12是骷髅， 14是蝙蝠， 16是哥布林，18是蜘蛛
        self.dict0={range(7): 10}
        self.dict1=({range(7): 0, range(7, 14): 2, range(14, 18): 4, range(18, 35): 8,
                     range(35, 41): 10})
        self.dict2=({range(8): 0, range(8, 16): 4, range(16, 20): 6, range(20, 34): 8,
                     range(34, 36): 10, range(36, 42): 12, range(42, 48): 14, range(48, 51): 16})
        self.dict3=({range(7): 0, range(7, 14): 4, range(14, 16): 6, range(16, 30): 8,
                     range(30, 33): 10, range(33, 42): 12, range(42, 50): 14,
                     range(50, 55): 16, range(55, 61): 18})
        self.dict4=({range(4):0, range(4, 8):4, range(8, 12):6, range(12, 14):8, range(14, 16):10,
                     range(16, 26):12, range(26, 34):14, range(34, 44):16, range(44, 52):18, range(52, 55):20,
                     range(55, 59):22, range(59, 62):24, range(62, 68):28, range(68, 71):30})
        self.dict5=({range(2):0, range(2, 4):4, range(4, 6):6, range(6, 8):8, range(8, 10):10,
                     range(10, 12):12, range(12, 18):14, range(18, 26):16, range(26, 30):18, range(30, 34):20,
                     range(34, 38):22, range(38, 40):24, range(40, 46):28, range(46, 50):30, range(50, 58):32,
                     range(58, 62):34, range(62, 63):36, range(63, 66):38, range(66, 68):14, range(68, 71):32})
        self.dict6 = ({range(2): 0, range(2, 4): 4, range(4, 6): 6, range(6, 8): 8, range(8, 10): 10,
                       range(10, 12): 12, range(12, 18): 14, range(18, 26): 16, range(26, 30): 18, range(30, 34): 20,
                       range(34, 38): 22, range(38, 40): 24, range(40, 46): 28, range(46, 50): 30, range(50, 58): 32,
                       range(58, 62): 34, range(62, 63): 36, range(63, 66): 38, range(66, 69): 42, range(69, 71): 40})
        self.dict7 = ({range(0, 2): 6, range(2, 4): 8, range(4, 6): 10, range(6, 8): 12, range(8, 12): 14,
                       range(12, 20): 16, range(20, 24): 18, range(24, 28): 20, range(28, 30): 22, range(30, 32): 24,
                       range(32, 38): 28, range(38, 42): 30, range(42, 52): 32, range(52, 56): 34, range(56, 60): 36,
                       range(60, 63): 38, range(63, 67): 40, range(67, 71): 42})
        self.dict8 = ({range(0, 20):32, range(20, 40):34, range(40, 45):36, range(45, 55):42, range(55, 60):40,
        range(60, 71):16})
        self.dicts=[self.dict0, self.dict1, self.dict2, self.dict3, self.dict4,self.dict5,self.dict6,self.dict7,self.dict8]
        self.detect=({0:'Green Slime', 2:'Ooze', 4:'Fiery Slime', 6:'Sand Slime', 8:'Ditch Rat',
                      10:'Rat', 12:'Skeleton', 14:'Vampire Bat', 16:'Goblin', 18:'Vemon Spider'})
        self.img, self.img_mob=Infoimage(surface), None
        self.debuff={48:self.hitWand, 49:self.poisonWand, 50:self.fieryWand, 51:self.chaosWand,
                     52:self.healWand, 192:self.frozenWand, 193:self.horroWand, 194:self.curseWand,
                     195:self.tpWand, 196:self.mapWand, 197:self.skullWand}          #怪物不良状态
        self.melee={1:self.fieryWand, 2:self.bloodDrain, 3:self.dizzyM, 4:self.knockBack, 5:self.chaosWand,
                    6:self.frozenWand, 7:self.poisonHit, 8:self.armorBreak, 9:self.penetrate, 10:self.sweap}
        with open(r'data/mob_dir.json', 'r') as dic:
            self.md=json.load(dic)
        self.fem=None
        self.summon_dict={22:26, 40:14}
        self.inf=None
        self.kingDead=False
        self.loopSetter=None

    def mob_spawn(self, level, func_lst):     #n表示生成怪物的数量
        #level表示了对应层数的地牢应该生成什么样的怪物
        self.mob_pool={}
        mob_num=level//2+23
        for i in range(mob_num):
            num=self.mobDecision(level)
            self.create_mob(num, func_lst)
        if level==8:
            self.more_mob((33, 15), radius=4, ID=44)

    def mobDecision(self, level):           #对应关卡生成不同的怪物，这个是按照关卡概率返回怪物id
        #TBS: 对应的关卡信息先写在了__init__方法里，后可以移除到一个json文件中
        index=level
        if not level:
            possi=random.randint(0, 6)
            for key, value in self.dicts[ index ].items():
                if possi in key: return value
        elif level == 1:
            possi=random.randint(0, 40)
            for key, value in self.dicts[ index ].items():
                if possi in key: return value
        elif level == 2:
            possi=random.randint(0, 50)
            for key, value in self.dicts[ index ].items():
                if possi in key: return value
        elif level == 3:
            possi=random.randint(0, 60)
            for key, value in self.dicts[ index ].items():
                if possi in key: return value
        else:
            possi=random.randint(0, 70)
            for key, value in self.dicts[ index ].items():
                if possi in key: return value
            if level==8:
                self.more_mob()

    def create_mob(self, n, func_lst, ctr:tuple=(0, 0), radius=60, flag=False, hp=0, serve=False):     #flag表示生成的怪物存放地点
        #注意，mob所召唤的怪物必须暂存在new_pool中，否则在tem_dict复制过程中将丢失数据报错
        num=str(n)          #注意n不是表数量，而是表ID
        '''===========图片获取============='''
        mob=self.mob(self.screen)
        mob.load(r'asset/mobs.png', 0, 0, 32, 32, 10)
        '''===========参数传入============'''
        mob.setup_mob(*self.md[num])
        '''=========地图位置============='''
        pos=self.mobSpawnPoint(ctr, radius)
        if pos:         #获取怪物的生成位置
            mob.posx, mob.posy = pos
        else: return
        #self.setChar(mob.posx, mob.posy, n)         #level重新设置值
        '''==========必要函数=============='''
        mob.func_lst, mob.pf.func_lst = func_lst, func_lst
        mob.pf.func_lst2= [func_lst[0], func_lst[1], func_lst[3]]       #给Astar算法传入函数参数，以便于Astar与其它函数建立联系
        mob.pool, mob.pl, mob.inf, mob.ptr=self, self.pl, self.inf, self.ptr
        '''==========速度确定方法==========='''
        mob.stp=SpdStep(self.ptr.speed_getter)
        mob.stp.mob_spd(mob.speed)
        '''=============(hp)============='''
        #史莱姆分裂是要制定怪物的血量以及清除其掉落物品的能力
        if hp:
            mob.hp=hp
            mob.origin_hp = hp
            mob.treasure=-1         #不可直接掉落金币
        if serve:           #是否是跟班怪物
            mob.servant=True
        if flag:        #updating内召唤怪物存放于new_pool中，稍后复制
            self.new_pool[ (mob.posx, mob.posy)] = mob
        else:
            self.mob_pool[(mob.posx, mob.posy)] = mob

    def mobSpawnPoint(self, ctr:tuple=(0, 0), radius=60):            #怪物的生成位置选择
        #ctr与radius都是可选参数，如果有这两个参数，表示在重心点ctr附近radius范围内生成怪物
        #self.func_lst[ 0 ]是dg, func_lst[ 1 ]是dg.sur, func_lst[ 2 ]是npc
        #TBM：有待优化
        x_min, x_max=max(ctr[0]-radius, 6), min(ctr[0]+radius, 58)
        y_min, y_max=max(ctr[1]-radius, 6), min(ctr[1]+radius, 36)
        count=0
        if radius==0:
            x, y=ctr
            return x, y
        else: x, y=random.randint(x_min, x_max), random.randint(y_min, y_max)
        judge1, judge2, judge3=self.func_lst[ 0 ].getChar(x, y), self.func_lst[ 1 ].getChar(x, y), self.func_lst[ 2 ].getChar(x, y)
        while judge1 in {0, 10, 13, 15, 18, 19, 22, 27, 28} or judge2 != -1 or judge3 != -1 or (x, y)==(self.pl.posx-1, self.pl.posy-1) or self.getChar(x, y):
            count+=1            #防止死循环保护
            x, y=random.randint(x_min, x_max), random.randint(y_min, y_max)
            judge1, judge2, judge3=self.func_lst[ 0 ].getChar(x, y), self.func_lst[ 1 ].getChar(x, y), self.func_lst[ 2 ].getChar(x, y)
            if count>48:
                return None
        return x, y

    """============怪物更新池============"""
    def updateMob(self, current_time, rate = 500):            #怪物池，怪物位置池, self.level的更新
        tem_dict = {}
        for k in list(self.mob_pool.keys()):
            if self.mob_pool[k].hp<=0:            #mob死亡
                if self.mob_pool[k].ID==44: self.kingDead=True
                self.itemDrop(k, self.mob_pool[k].treasure, self.mob_pool[k].lvl)
                self.pl.dg.fem.rangeCenter(self.pl.posx, self.pl.posy, self.pl.ptr.LR)           #Luminous_range作为一个参数
                #self.setChar(k[0], k[1], -1)
                self.img_mob=None
            else:
                #self.setChar(self.mob_pool[k].posx, self.mob_pool[k].posy, -1)
                self.mob_pool[ k ].stat_setter(current_time, rate)          #位置，状态的更新
                #逐个绘制, 和group方法差不多但是还是吃计算量
                if self.mob_pool[ k ].hp-self.mob_pool[ k ].old_hp and self.mob_pool[ k ].hp>0:         #怪物生命改变，且怪物存货时，更新old_hp
                    self.img_mob=self.mob_pool[ k ]
                    self.mob_pool[ k ].old_hp=self.mob_pool[ k ].hp
                #self.setChar(self.mob_pool[k].posx, self.mob_pool[k].posy, self.mob_pool[k].ID)
                self.lavaBurn(self.mob_pool[k])
                tem_dict[(self.mob_pool[k].posx, self.mob_pool[k].posy)]=self.mob_pool[k]      #更新位置信息
        self.mob_pool=tem_dict
        del tem_dict            #释放
        if self.new_pool:
            for k in self.new_pool.keys():
                if not k in self.mob_pool:      #防止召唤怪物覆盖原来的怪物
                    self.mob_pool[k]=self.new_pool[k]
            self.new_pool.clear()
        if self.img_mob:            #怪物存在时绘制信息概览框（如果秒杀怪物则不出现）
            self.img.getMobInfo(self.img_mob)
            self.img.blitMobInfo(self.img_mob, 100, 330)
        if self.recreate:           #避免召唤怪物覆盖的一个方法
            self.more_mob()
            self.recreate=False
        if self.kingDead:
            self.loopSetter(12)



    def more_mob(self, ctr:tuple=(0, 0), radius=3, ID=-1, flag=False, hp=0, serve=False):             #由于summon陷阱而多产生的怪物
        #ID是指定生成怪物的ID， flag表示是否是mob召唤怪物
        if ctr != (0, 0):
            center=ctr
            mob_num=1
        else:
            center=self.pl.posx, self.pl.posy
            mob_num=1 if serve else random.randint(0, 2)
        if serve: self.inf.prefabTell('summonWand')
        for i in range(mob_num):
            if ID >= 0 :
                self.create_mob(ID, self.arg_funcs, center, radius, flag, hp, serve)
            else:
                num=self.mobDecision(self.func_lst[0].level_num)
                self.create_mob(num, self.arg_funcs, center, radius, flag, hp, serve)

    def getNearBy(self, x=0, y=0):          #找到附近存在怪物的点并返回
        if (x, y)==(0, 0):
            lst=self.pl.getShootRange()
            for i in lst:
                if i in self.mob_pool:
                    return i[0] + 1, i[1] + 1
            return None
        else:       #帮助跟班怪物选择周围怪物
            lst = self.rectRange(x, y, 1)
            random.shuffle(lst)     #胡乱攻击或者治疗
            for i in lst:
                if i in self.mob_pool:
                    if not self.mob_pool[i].servant:        #只返回攻击性怪物
                        return i[0] + 1, i[1] + 1
            return None


    def getMob(self, x, y):           #获取一个位置（x, y）上的怪物,通过怪物位置池和怪物池索引的对应查找
        return self.mob_pool[ (x, y) ]
        
    def getChar(self, x, y):
        if (x, y) in self.mob_pool:
            return True
        return False

    def getMobid(self, x, y):       #返回怪物的id值
        return self.getMob(x, y).ID if self.getChar(x, y) else -1

    def getCost(self, x, y):
        if self.getChar(x, y):
            return 3
        else:
            return 0

    def getHit(self, x, y, hit):
        if self.mob_pool[(x, y)].hp - hit > 0:
            self.mob_pool[(x, y)].hp -= hit
            self.mob_pool[(x, y)].attack_info()
            if hit: self.inf.moreArg('hit', [self.mob_pool[ (x, y) ].name, hit])        #受伤信息
            else: self.inf.prefabTell('missmob', back=self.mob_pool[ (x, y) ].name)
            return True
        else:
            self.mob_pool[(x, y)].hp = 0
            self.mob_pool[(x, y)].attack_info()
            ID=self.mob_pool[(x, y)].ID
            if ID%2:
                ID-=1
            self.ptr.kill_dict[ID] += 1
            self.ptr.exp_adder(self.mob_pool[(x, y)].exp)
            self.ptr.score_adder(self.mob_pool[(x, y)].score)
            self.inf.moreArg('kill', [self.mob_pool[(x, y)].name, self.mob_pool[(x, y)].exp])
            return False

    def attacked(self, x, y):          #选择受到攻击的怪物
        #返回值True，表示怪物存活，反之表示死亡
        if not self.mob_pool[ (x, y) ].servant:
            hit=self.cc.damageOnMob(self.mob_pool[ (x, y) ], self.ptr.atk_getter(), self.ptr.speed_getter())
            judge=self.getHit(x, y, hit)
            if judge: judge=self.specMelee(x, y)      #如果怪物没有死亡则判断是否有特殊属性
            return judge
        else:
            #self.setChar(self.mob_pool[ (x, y) ].posx, self.mob_pool[ (x, y) ].posy, -1)
            self.pl.posx, self.pl.posy, self.mob_pool[ (x, y) ].posx, self.mob_pool[ (x, y) ].posy=(
                self.mob_pool[(x, y)].posx+1, self.mob_pool[(x, y)].posy+1, self.pl.posx-1, self.pl.posy-1
            )       #这是pl的位置参数和mob位置参数的关系
            #self.setChar(self.mob_pool[ (x, y) ].posx, self.mob_pool[ (x, y) ].posy, self.mob_pool[ (x, y) ].ID)
            self.mob_pool[(x, y)].idle=True
            self.inf.prefabTell('swap', back=self.mob_pool[(x, y)].name)
            #return self.posx, self.posy        #是跟班，返回值应是False,并且玩家和怪物互换位置

    def specMelee(self, x, y):
        judge=True
        for i in self.ptr.itemTags.keys():
            if self.ptr.itemTags[i]: judge=self.melee[i](x, y)
            if not judge: return False
        return True

    """========================远程攻击======================="""
    def distantAttacked(self, x, y, tag=0, ID=-1):         #远距离攻击
        if tag==1: return self.physicalHit(x, y, False)
        elif tag==2: return self.wizardHit(x, y, ID)
        elif tag==3: return self.fixedHit(x, y, ID)
        return True

    def physicalHit(self, x, y, tag=True):     #tag表示了冲击法杖
        if tag:
            hit = self.cc.damageOnMob(self.mob_pool[(x, y)], self.ptr.atk_getter(), self.ptr.speed_getter())
        else:
            hit=random.randint(0, 3)            #冲击法杖随机伤害
        judge=self.getHit(x, y, hit)
        if judge: judge=self.specMelee(x, y)
        return judge

    #巫师攻击,部分巫师之书的作用和法杖完全相同
    def wizardHit(self, x, y, tag=114):           #TBM
        hit = self.cc.magicOnMob(self.mob_pool[(x, y)], self.ptr.atk_getter(), self.ptr.speed_getter())
        if tag==114:        #灼烧 灰烬法书
            hit+=random.choices([1,2,3,4,5,6], [0.05, 0.15, 0.2, 0.2, 0.2, 0.2])[0]
            self.inf.prefabTell('mfire', back=self.mob_pool[(x, y)].name)
        elif tag==112:      #禁忌·魅惑之书
            choices=[[0, 1], [0.8, 0.2]]
            judge=random.choices(*choices)[0]
            if judge:
                self.mob_pool[(x, y)].servant=True
                self.inf.prefabTell('mcharm', self.mob_pool[(x, y)].name)
            else:  self.inf.prefabTell('no')
            return False
        elif tag==113:       #暗夜·吸血咒书
            self.ptr.bloodDrain()
            self.inf.prefabTell('mdrain', back=self.mob_pool[(x, y)].name)
        elif tag==128:         #腐烂·毒素古书
            hit=3
            self.mob_pool[(x, y)].status[1]=16          #TBS：毒素古书的持续回合与魔法有关
            self.inf.prefabTell('mpoison', back=self.mob_pool[(x, y)].name)
        elif tag==163:      #北风·冰霜之书
            self.inf.prefabTell('mfrozen', back=self.mob_pool[(x, y)].name)
            return self.frozenWand(x, y)
        elif tag==164:      #空间·传送之书
            self.inf.prefabTell('tps')
            return self.tpWand(x, y)
        elif tag==165:      #脊髓·恐惧之书
            self.inf.prefabTell('mfright', self.mob_pool[(x, y)].name)
            return self.horroWand(x, y)
        elif tag==166:      #面容·诅咒之书
            self.inf.prefabTell('mcurse', self.mob_pool[(x, y)].name)
            return self.curseWand(x, y)
        return self.getHit(x, y, hit)

    """===================模式伤害====================="""
    def fixedHit(self, x, y, tag):
        self.debuff[tag](x, y)

    #冲击法杖
    def hitWand(self, x, y):      #冲击法杖
        return self.physicalHit(x, y, False)

    #治疗法杖
    def healWand(self, x, y):
        if (x+1, y+1)==(self.pl.posx, self.pl.posy):
            self.inf.prefabTell('cureWand')
            self.ptr.bloodDrain(1)
        else:
            point=random.randint(1, 3)
            self.inf.prefabTell('cureWandm', self.mob_pool[(x, y)].name)
            if self.mob_pool[(x, y)].hp+point>self.mob_pool[(x, y)].origin_hp:
                self.mob_pool[(x, y)].hp=self.mob_pool[(x, y)].origin_hp
            else:
                self.mob_pool[(x, y)].hp+=point
        return True

    #毒素法杖
    def poisonWand(self, x, y):
        self.mob_pool[(x, y)].status[1]=4
        self.inf.prefabTell('mpoison', back=self.mob_pool[(x, y)].name)
        hit=2
        return self.getHit(x, y, hit)

    #火焰法杖
    def fieryWand(self, x, y):
        hit=random.randint(2, 5)
        self.inf.prefabTell('mfire', back=self.mob_pool[(x, y)].name)
        return self.getHit(x, y, hit)

    #混乱法杖
    def chaosWand(self, x, y):
        judge=random.randint(1, 5)
        self.inf.prefabTell('mchao', back=self.mob_pool[(x, y)].name)
        if judge==1: return self.poisonWand(x, y)
        elif judge==2: return self.fieryWand(x, y)
        elif judge==3: return self.frozenWand(x, y)
        elif judge==4: return self.horroWand(x, y)
        else: return self.curseWand(x, y)

    #冰冻法杖
    def frozenWand(self, x, y):
        hit=2
        self.inf.prefabTell('mfrozen', self.mob_pool[(x, y)].name)
        if not self.mob_pool[(x, y)].status[4]:
            self.mob_pool[(x, y)].speed-=10
        self.mob_pool[(x, y)].status[4]=10
        return self.getHit(x, y, hit)

    #恐惧法杖
    def horroWand(self, x, y):
        hit=1
        self.inf.prefabTell('mfright', self.mob_pool[(x, y)].name)
        self.mob_pool[(x, y)].aggressive=False
        self.mob_pool[(x, y)].status[2]=6
        return self.getHit(x, y, hit)

    #诅咒法杖
    def curseWand(self, x, y):
        self.inf.prefabTell('mcurse', self.mob_pool[(x, y)].name)
        hit = 1
        if not self.mob_pool[(x, y)].status[3]:
            self.mob_pool[(x, y)].defence -= 7
            self.mob_pool[(x, y)].magic -= 7
        self.mob_pool[(x, y)].status[3]=16
        return self.getHit(x, y, hit)

    #骷髅法杖
    def skullWand(self, x, y):
        self.more_mob(ID=12, serve=True)
        return True

    #地图法杖
    def mapWand(self, x, y):
        self.pl.clearMist()
        return False

    def bloodDrain(self, x, y):     #防止传入函数的问题
        self.ptr.bloodDrain(x, y)

    #传送法杖
    def tpWand(self, x, y):
        if (x, y) == (self.pl.posx - 1, self.pl.posy - 1):
            self.pl.tpScroll()
        elif (x, y) in self.mob_pool:
            self.mob_pool[(x, y)].teleported=True
        return True
    """=====================以上是不同法杖的作用======================="""
    """=====================非魔法武器特殊属性======================="""
    def dizzyM(self, x, y):
        diz=random.choices([0, 2], [0.4, 0.6])[0]
        self.mob_pool[(x, y)].status[6]=diz
        if diz: self.inf.prefabTell('mdizzy', self.mob_pool[(x, y)].name)
        return True

    def knockBack(self, x, y):
        self.mob_pool[(x, y)].knocked=True
        return True

    def poisonHit(self, x, y):      #物理攻击毒性
        self.mob_pool[(x, y)].status[5] = 10
        self.inf.prefabTell('mpoison', back=self.mob_pool[(x, y)].name)
        return True

    def armorBreak(self, x, y):     #破甲
        return self.getHit(x, y, 3)

    def penetrate(self, x, y):      #穿刺攻击
        lst=self.getLinedMob(x, y, 1)
        for i in lst:
            self.getHit(i[0], i[1], 1)
        return self.getHit(x, y, 1)

    def lavaBurn(self, mob):
        if self.func_lst[0].getChar(mob.posx, mob.posy) in {18, 19}:
            mob.hp-=2

    def getLinedMob(self, x, y, tag=0):        #寻找同一斜率上的怪物
        #tag=1时表示直线查找，否则范围查找
        mobList=[]
        if tag:
            dx=x-self.pl.xat
            dy=y-self.pl.yat
            if (x+dx, y+dy) in self.mob_pool:
                mob=self.getMob(x+dx, y+dy)
                mobList.append((x+dx, y+dy))
                if mob:
                    if (x+2*dx, y+2*dy) in self.mob_pool:
                        mob=self.getMob(x+2*dx, y+2*dy)
                        if mob: mobList.append((x+2*dx, y+2*dy))
        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (self.pl.xat+i, self.pl.yat+j) in self.mob_pool:
                        mob=self.getMob(self.pl.xat+i, self.pl.yat+j)
                        if mob: mobList.append((self.pl.xat+i, self.pl.yat+j))
        return mobList

    def sweap(self, x, y):      #范围攻击
        lst = self.getLinedMob(x, y)
        lst.remove((x, y))
        for i in lst:
            hit = random.randint(0, 2)
            self.getHit(i[0], i[1], hit)
        return self.getHit(x, y, 1)

    def summon(self):           #地牢内召唤或召唤陷阱生成单个怪物
        ID=self.mobDecision(self.func_lst[0].lvl)
        self.create_mob(ID, self.arg_funcs, radius=3)

    """========================================================="""

    """def center(self, cx, cy):
        #x, y为center基准点
        for y in range(4, 39):
            for x in range(4, 61):
                value=self.getChar(x, y)
                mob=self.getMob(x, y, value)
                if int(value)>=0:
                    mob.X = (16 - cx) * 32 + 80 + x * 32
                    mob.Y = (9 - cy) * 32 + 10 + y * 32
                    more=random.randint(0, 1)
                    if mob.intelligent==11: more=0
                    mob.frame = mob.ID + more
                    mob.last_frame = mob.frame
                    mob.updating(0)
                    if self.ms.getChar(x, y)==1:
                        mob.draw(self.screen)"""

    def center(self, cx, cy):
        for k in self.mob_pool.keys():                  #采用非稀疏矩阵的绘制方法
            mob=self.mob_pool[k]
            x, y=k                                                  #取怪物位置
            mob.X = (16 - cx) * 32 + 80 + x * 32
            mob.Y = (9 - cy) * 32 + 10 + y * 32
            more = random.randint(0, 1)
            if mob.intelligent == 11: more = 0
            mob.frame = mob.ID + more
            mob.last_frame = mob.frame
            mob.updating(0)
            if self.ms.getChar(x, y) == 1:
                mob.draw(self.screen)                       #mob直接继承了MySprite

    def frameRange(self, posx, posy, n):
        lst=self.rectRange(posx, posy, n)
        lst_deduct=self.rectRange(posx, posy, n-1)
        for i in lst_deduct:
            lst.remove(i)
        return lst

    def reset(self):
        self.mob_pool = {}
        #self.level = [[-1 for i in range(42)] for j in range(64)]
    """=================静态方法=================="""
    @staticmethod
    def rectRange(posx, posy, n):           #获取方形区域内点
        lst = []
        for x in range(max([posx - n, 0]), min([posx + n + 1, 65])):  # 保证lst内值的有效性
            for y in range(max([posy - n, 0]), min([posy + n + 1, 43])):
                lst.append((x, y))
        return lst

    @staticmethod
    def noWalk(x, y) :                          #是否可通过
        return False

#速度值确定类
class SpdStep:
    def __init__(self, ptrs):       #传入玩家速度，spd是怪物本身的速度
        self.ptrs=ptrs
        self.step=0
        self.spd=0
        self.step_dict={5:self.step5, 4:self.step4, 3:self.step3, 2:self.step2, 1:self.step1, 0:self.step0, -1:self.mstep}

    def mob_spd(self, spd=3):
        self.spd=spd
        
    def step_level(self):           #速度等级确定
        if self.spd-self.ptrs() >=10: lvl=-1
        elif self.spd-self.ptrs() >=2: lvl=0
        elif self.spd-self.ptrs()>=-25: lvl=1
        elif self.spd-self.ptrs()>=-35: lvl=2
        elif self.spd-self.ptrs()>=-45: lvl=3
        elif self.spd-self.ptrs()>=-60: lvl=4
        else: lvl=5
        if self.spd==3: lvl=5
        return lvl

    def steps(self):
        step=self.step_dict[self.step_level()]()
        return step

    def step5(self):            #速度等级5，最慢，玩家动两下怪物才能动一下
        self.step+=1
        if self.step>1: self.step=0
        return 1 if self.step%2 else 0

    def step4(self):        #速度等级4，次慢，玩家动三下怪物能动两一下
        self.step+=1
        if self.step>2: self.step=0
        return 1 if self.step%3 else 0
    
    def step3(self):        #速度等级3，较慢，玩家动四下怪物能动三下
        self.step+=1
        if self.step>3: self.step=0
        return 1 if self.step%4 else 0

    def step2(self):        #速度等级2，中，玩家动五下怪物能动四下
        self.step+=1
        if self.step>4: self.step=0
        return 1 if self.step%5 else 0

    @staticmethod
    def step1():        #正常速度，对等速度
        return 1

    def step0(self):        #速度等级0，较快，玩家动三下怪物能动四下
        self.step+=1
        if self.step>3: self.step=0
        return 1 if self.step%4 else 2

    def mstep(self):        #速度等级-1，最快，玩家动两下怪物能动三下
        self.step+=1
        if self.step>2: self.step=0
        return 1 if self.step%3 else 2