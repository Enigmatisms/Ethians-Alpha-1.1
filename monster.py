#!/usr/bin/env python3
#-*-coding:utf-8-*-

import random
from pygame.locals import *
from ezplot import MySprite
from Pathfinder import Astar
from blittools import Note
from calc import Calc

__author__='SEe3Hz'

#这个可能是一个非常大的类，包括了多个子类
#怪物类:单个怪物类，不是怪物群

class Monster(MySprite):        #继承了父类MySprite
    def __init__(self, screen):
        super().__init__()
        self.name=None
        self.attack=None
        self.ID=None
        self.cc=Calc()          #伤害计算模块
        self.posx, self.posy, self.xat, self.yat=0,0,0,0
        self.pl, self.pool=None, None       #传入pl类，需要里面的一些数据，比如玩家位置
        self.func_lst=[]        #传入本身作为参数，需要判断不同的怪物是否会撞在一起，原则上不允许
        '''self.func_lst包含的类有：dg, dg.sur, npc, po'''
        self.aggressive=True        #是否有进攻性（血量低的时候，怪物可能会逃跑）
        self.hp, self.defence, self.exp, self.speed, self.treasure, self.magic = None, None, None, None, None, None
        self.old_hp, self.origin_hp, self.stp, self.ptr=None, None, None, None
        self.pf=Astar()        #内嵌Pathfinder类的创建
        self.intelligent=0              #逃跑智力值默认为0，不逃跑
        self.nt=Note(screen)
        self.d2=1.414214
        self.lvl=0
        self.score=0
        self.servant=False          #从属标签，True是说明是玩家的跟班
        self.tem_x1, self.tem_y1=0, 0
        self.tags=[]            #怪物状态标签
        self.status={1:0, 2:0, 3:0, 4:0, 5:0, 6:0}          #怪物现阶段状态
        self.idle=False         #怪物在于玩家交换位置后，会静止一回合
        self.knocked=False      #被击退
        self.teleported=False
        self.inf=None
        self.dgNoTp={1,2,11,12,14,18,19, 22, 27, 28}        #怪物传送可到达的地方
        self.surNoTp={0, 3, 10, 12, 16, 17, 18, 23, 25, 26, 30, 31, 33, 34, 37,38,40, 41,42} #怪物传送不可到达的地方
        '''五个参数的意思是：怪物生命， 怪物防御， 击杀怪物可以获得的经验值，怪物的速度， 怪物携带的财宝^^^'''
        #...
        
    def setup_mob(self, hp=12, atk=6, defc=8, mgc=0, spd=12, exp=2,
                  trs=0, ID=0, name='Rat', iq=0, lvl=0, attr=[]):
        self.hp, self.defence, self.exp, self.speed, self.treasure, self.ID, self.name, self.attack, self.magic \
            = hp, defc, exp, spd, trs, ID, name, atk, mgc
        self.old_hp, self.origin_hp, self.lvl=hp, hp, lvl
        self.score=int((self.exp*self.origin_hp/2+self.attack+self.defence+self.magic+self.speed)*((self.lvl+1)**0.5))
        self.intelligent=iq
        self.tags=attr

    def getpos(self):
        return self.pl.xat, self.pl.yat
    
    def updating(self, current_time, rate = 500, stat=0):        #重写update方法
        """stat参数解释：怪物的状态参数
        >>stat=0，怪物和玩家都无法互相检测，不绘制这样的怪物
        >>stat=1，怪物发现玩家，开始追踪，但还没有开始攻击
        >>stat=2，怪物攻击玩家
        >>stat=3，怪物血量过低，开始逃跑
        >>stat=4，怪物眩晕了         怪物debuff
        >>stat=5,   怪物使用特殊技能：传送         怪物逃跑的另一方式
        >>stat=6,   怪物使用特殊技能：召唤
        >>stat=7,   怪物使用特殊技能：自疗
        """
        self.stat2Behave(stat)
        #更新图像模块
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self. frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect) 
            self.old_frame = self.frame
    
    def chase_player(self, tuple1, rev_arg=0):      #追逐玩家的方法，tuple1接收玩家的位置参数(self.xat, self.yat)，rev_arg接收反向参数，为1时怪物逃跑
        if rev_arg:
            point=self.selectPoint((self.posx, self.posy), tuple1)
            self.tem_x1, self.tem_y1=self.pf.pathfind((self.posx, self.posy), point)
        else:
            self.tem_x1, self.tem_y1=self.pf.pathfind((self.posx, self.posy), tuple1)         #建立临时位置，临时位置是由pathfind模块离起点最近的一个点确定的
        self.canWalk()

    def canWalk(self, Kbktag=False):          #判断此处是否可以走
        #Kbktag是击退标签，如果击退效果时怪物碰到墙壁，则扣血
        tem_x, tem_y=self.posx, self.posy
        f1=self.func_lst[1]
        judge=1
        for i in range(4):              #func_lst是[dg, dg.sur, npc, mob]，func_lst在mob的create_mob中传入
            if self.func_lst[i].getChar(self.tem_x1, self.tem_y1) in self.func_lst[ i ].no_walk:
                #no_walk(列表)与noWalk判断是不一样的
                '''TBS:no_walk是不能踩踏的砖块或地图道具对应id。noWalk判断的砖块或地图道具是永久不可变，不可通过的
                也就是说，石砖不可通过，不会在寻路算法中计算，但是关闭的门虽然不能直接踩踏，但是开门后可以通过
                所以关闭的门noWalk返回值是False'''
                judge=0
        if (self.posx, self.posy)==(self.pl.xat, self.pl.yat): judge=0
        if judge:
            self.posx, self.posy=self.tem_x1, self.tem_y1
            judge1=f1.getChar(self.tem_x1, self.tem_y1)
            if judge1==13:      #传送
                self.posx, self.posy=self.mons_portal()
                self.func_lst[1].setChar(self.posx, self.posy, -1)
            elif judge1==14:
                self.pool.recreate=True
                self.func_lst[ 1 ].setChar(self.posx, self.posy, -1)
            elif judge1==15:
                hit=random.randint(1, 2)
                self.hp-=hit
        else:
            if Kbktag:          #被击退
                hit=random.randint(1,2)
                self.hp -= hit
            else:
                judge1=f1.getChar(self.tem_x1, self.tem_y1)
                if judge1 in f1.doors:
                    f1.mons_door(self.tem_x1, self.tem_y1, judge1)
                elif judge1 in {10, 11}:
                    f1.mons_trap(self.tem_x1, self.tem_y1)
                    self.hp=0
        #self.pool.setChar(tem_x, tem_y, -1)
        #self.pool.setChar(self.posx, self.posy, self.ID)

    def selectPoint(self, start, target):
        sx, sy=start[0], start[1]
        tx, ty=target[0], target[1]
        max_cost=0
        point=start
        for x in range(sx-1, sx+2):
            for y in range(sy-1, sy+2):
                cost=self.calcCost(x, y, tx, ty)
                if cost>max_cost:
                    judge=1
                    for func in self.func_lst[:-1]:
                        if func.getChar(x, y) in func.no_walk:
                            judge=0
                    if judge:
                        max_cost=cost
                        point=(x, y)
        return point

    def calcCost(self, x1, y1, x2, y2):
        dy=abs(y1-y2)
        dx=abs(x1-x2)
        cost=(dy+dx)+(self.d2-2)*min(dy, dx)
        return cost

    def attack_info(self):      #怪物受到攻击的伤害显示
        hits=self.hp-self.old_hp
        if hits:
            self.nt.center_note(hits, self)
    
    def attack_player(self):
        #player类写一个怪物侦测区，怪物攻击区
        if self.intelligent not in [6, 7]:
            hit=self.cc.mobAttackHit(self, self.ptr.def_getter(), self.ptr.speed_getter())          #获取伤害值
        else:
            hit=self.cc.magicOnPly(self, self.ptr.magic_getter(), self.ptr.speed_getter())
        #怪物攻击造成的实际攻击还是要计算的
        if hit and self.ptr.hp_getter():
            self.tagEffect()            #攻击属性
            self.ptr.hp_adder(-hit)
            self.inf.moreArg('mhit', [self.name, hit])
            if not self.ptr.hp_getter():
                self.inf.deathCause('mob', self.name)
        elif hit==0:
            judge=random.randint(0, 1)
            if judge: self.inf.prefabTell('miss', self.name)
            else: self.inf.prefabTell('dodge', back=self.name)


    def stat_setter(self, current_time, rate = 500 ):  #改变update的stat值
        if self.servant:
            if self.idle: self.idle=False
            else:
                self.statusUpdate()
                if (self.posx, self.posy) in self.pl.getActiveRange():
                    if self.teleported: flag = 11       #被传送走了
                    else: flag=11
                    self.updating(current_time, rate, flag)
                elif (self.posx, self.posy) in self.pl.getAttackRange():
                    if self.teleported: flag = 11   #被传送走了
                    else: flag=9
                    self.updating(current_time, rate, flag)            #选择打怪物或者乱走
            if self.lvl > 2: self.servant = False       #高级怪物马上会恢复
        else:       #正常怪物
            if self.aggressive and self.intelligent not in [4]:
                self.aggressive = self.getStat()
            elif self.intelligent in [4]:  # 高阙值怪物：生命值在阙值以上时可以再战
                self.aggressive = self.getStat()
            self.statusUpdate()
            if (self.posx, self.posy) in self.pl.getActiveRange():
                flag = self.behavior(self.aggressive, True)
                if self.status[6]: flag=4
                if self.teleported: flag=11     #被传送走了
                self.updating(current_time, rate, flag)
            elif (self.posx, self.posy) in self.pl.getAttackRange():
                flag = self.behavior(self.aggressive, False)
                if self.status[6]: flag = 4
                if self.teleported: flag=11     #被传送走了
                self.updating(current_time, rate, flag)

    def getStat(self):
        #spec_tag为真的，表示生命过低阙值偏高，如自疗怪物，boss等
        """intelligence值有八等，0>>>，不会逃跑
        1>>>生命过低逃跑
        2>>>开始时逃跑，受到攻击时反击
        3>>>生命过低时传送
        4>>>生命过低时自疗
        5>>>有召唤能力
        6>>>远程攻击能力
        7>>>远程攻击+召唤
        8>>>boss
        """
        if self.intelligent in {1, 3}:
            if self.hp < int(self.origin_hp / 4):
                run_away_judge = random.randint(0, 1)
                if not run_away_judge:
                    return False
        elif self.intelligent==2:
            if self.hp==self.origin_hp:
                return False
        elif self.intelligent==4:           #自疗怪物阙值高
            if self.hp < int(self.origin_hp / 3):
                return False
        return True

    def stat2Behave(self, stat):
        if stat==1:
            self._chase()                #发现玩家开始跟踪
        elif stat==2:                    #近身攻击玩家
            self._attack()
        elif stat==3:                    #非传送逃跑
            self._flee()
        elif stat==4:                    #眩晕时会跳过一个回合
            pass
        elif stat==5:                    #怪物开始传送
            self._tpFlee()
        elif stat==6:                    #召唤怪物
            self._summon()
        elif stat==7:                    #自疗
            self._selfHeal()
        elif stat==8:                    #发动远程攻击
            self._longRange()
        elif stat == 9:                  #跟班怪物胡乱走动
            self._wander()
        elif stat==10:                  #攻击效果：击退
            self._getKnocked()
        elif stat==11:                  #攻击效果：传送
            self._getTped()
        elif stat==12:                  #萨满治疗
            self._shamanHeal()
        elif stat==13:                  #怪物召唤
            self._bossSummon()
        else:
            pass

    def tagEffect(self):            #怪物特殊攻击效果
        if self.tags:
            #中毒
            if 1 in self.tags:
                if self.cc.fixChoice(1):
                    self.ptr.setStat()      #中毒标准效果（30%）
                    self.inf.prefabTell('poison', back=self.name)
            #燃烧
            if 2 in self.tags:
                if self.cc.fixChoice(1):
                    if 6 in self.ptr.getStat(): self.ptr.setStat(6, 0)      #清除冰冻效果
                    self.ptr.setStat(2, 4-self.ptr.fireR)      #燃烧标准效果
                    if 4-self.ptr.fireR: self.inf.prefabTell('fire')
            #冰冻
            elif 6 in self.tags:
                if self.cc.fixChoice(2):          #（25%概率）
                    if 2 in self.ptr.getStat(): self.ptr.setStat(2, 0)      #清除燃烧效果
                    self.ptr.setStat(6, 80-20*self.ptr.iceR)      #冰冻标准效果
                    if 80-20*self.ptr.iceR: self.inf.prefabTell('frozen')
                    if not self.ptr.frozen:
                        self.ptr.speed_adder(-10)
                        self.ptr.frozen=True
            # 混沌魔法可以造成不同伤害
            if 3 in self.tags:
                tag=self.cc.multiChoice()
                if tag==5:
                    self.ptr.setStat(3, 50)          #失明50步
                    self.inf.prefabTell('blind')
                    if not self.ptr.blind:          #没瞎才能让玩家瞎
                        self.ptr.blind=True     #失明判断（防止重复减小玩家视野）
                        self.ptr.LR-=1
                elif tag==4:
                    self.ptr.setStat(2, 4-self.ptr.fireR)             #燃烧
                    if 4 - self.ptr.fireR: self.inf.prefabTell('fire')
                    self.ptr.setStat(6, 0)          #清除冰冻效果
                elif tag==3:
                    self.ptr.setStat(5, 1)         #破甲
                    self.inf.prefabTell('break', back=self.name)
                elif tag==2:        #冰冻
                    self.ptr.setStat(2, 0)          #清除燃烧效果
                    self.ptr.setStat(6, 80-20*self.ptr.iceR)
                    if 80 - 20 * self.ptr.iceR: self.inf.prefabTell('frozen')
                    if not self.ptr.frozen:         #只能冻住没冻住的玩家，已经冻住的玩家只会重设时间
                        self.ptr.speed_adder(-10)
                        self.ptr.frozen=True
                elif tag==1: self.bloodSteal()          #有概率偷取生命
            # 66%概率生命偷取
            if 4 in self.tags: self.bloodSteal()
            # 40%概率破甲
            if 5 in self.tags:
                if self.cc.fixChoice(3):
                    self.ptr.hp_adder(-3)
            # 药剂反胃效果
            if 7 in self.tags:
                self.inf.prefabTell('bleed')
                if self.cc.fixChoice(4):        #50%
                    self.ptr.setStat(7, 50)
                    self.ptr.bleeding=True


    def behavior(self, attack=False, remote=False):         #不同AI等级怪物的行为
        if attack:
            if self.knocked:                                                 #受到击退立即返回击退对应标签
                return 10
            if self.intelligent==0:                                         #智力为0，只会跟踪和进攻
                return 1 if remote else 2
            if self.intelligent==1:                                         #智力为1，可能会逃跑
                if remote: return 1
                else:
                    return 3 if self.hp<int(self.origin_hp/4) else 2    #逃跑：血量过低
            elif self.intelligent == 5:
                if remote:
                    return 6 if self.cc.binChoice(10) else 1        #远离玩家时10%召唤怪物
                else:
                    return 2 if self.cc.binChoice(90) else 6         #20%召唤怪物
            elif self.intelligent == 6:                                     #远程施法攻击
                return 8 if remote else 2
            elif self.intelligent == 7:                                     #萨满会治疗身边怪物，并且发动远程攻击或者随意走动
                if remote:
                    return 12 if self.cc.binChoice(50) else random.choice([8, 8, 9])  # 远离玩家时10%召唤怪物
                else:                                                               #玩家近身时可能走动或攻击玩家，也可能自疗
                    return random.choice([2, 3]) if self.cc.binChoice(80) else 7  # 20%召唤怪物
            elif self.intelligent==8:                                        #远程物理攻击怪物
                if remote:
                    return 2 if self.cc.binChoice(90) else random.choice([1, 3])    #可能追击，可能逃跑，可能进攻
                else:
                    return random.choice([2, 3])                        #近身时攻击或逃跑
            elif self.intelligent==11:                                      #石像鬼，潘多拉
                if remote: return 4                                          #远离时无反应
                else:
                    self.intelligent=0
                    return 2
            elif self.intelligent==12:                                      #boss第一重形态
                if self.hp < int(self.origin_hp / 5): self.intelligent = 13
                if remote:
                    return 2 if self.cc.binChoice(50) else random.choice([1,1,1,1,1,13])
                else:
                    return 2 if self.cc.binChoice(90) else 13
            elif self.intelligent==13:                                      #boss第二重形态
                if remote:                                                       #1/4几率远程攻击。其他时候可能传送，逃跑，召唤怪物
                    return 2 if self.cc.binChoice(25) else random.choice([3, 11, 11, 13])
                else:                                                               #近身时1/5攻击，其他时候传送走
                    return 2 if self.cc.binChoice(20) else 11
            else:                                                                   #其他所有等级暂定：离玩家远则追击，近则攻击
                return 1 if remote else 2
        else:                                                                       #逃跑有关
            if self.intelligent==3: return 5
            elif self.intelligent==4: return 7
            else: return 3
            
    def mons_portal(self):          #怪物踩到传送门
        """self.func_lst包含的类有：dg, dg.sur, npc, po
                此方法还将用于怪物的逃跑传送"""
        count=0
        x, y=random.randint(5, 58), random.randint(5, 38)
        judge1=self.func_lst[ 0 ].getChar(x-1, y-1)
        judge2=self.func_lst[ 1 ].getChar(x-1, y-1)
        judge3=self.func_lst[ 2 ].getChar(x-1, y-1)
        judge4=self.func_lst[ 3 ].getChar(x-1, y-1)
        judge5=((x, y) == (self.pl.posx - 1, self.pl.posy - 1))
        while not judge1 in self.dgNoTp or judge2 in self.surNoTp or judge3 != -1 or judge4 !=-1 or judge5 or count>48:
            x, y=random.randint(5, 58), random.randint(5, 38)
            judge1=self.func_lst[ 0 ].getChar(x-1, y-1)
            judge2=self.func_lst[ 1 ].getChar(x-1, y-1)
            judge3=self.func_lst[ 2 ].getChar(x-1, y-1)
            judge4=self.func_lst[ 3 ].getChar(x-1, y-1)
            count+=1
        return x, y


    """======================怪物特殊技能======================"""
    def heal(self):             #自疗或者萨满治疗
        if self.hp < self.origin_hp:
            min_h = int(self.origin_hp / 16) + 1
            max_h = int(self.origin_hp / 4)
            plus_hp = random.randint(min_h, max_h)
            if self.hp + plus_hp > self.origin_hp:
                self.hp = self.origin_hp
            else:
                self.hp += plus_hp
            self.old_hp = self.hp

    def shamanHeal(self):
        tuple1=self.pool.getNearBy(self.posx, self.posy)
        if tuple1:
            mob=self.pool.getMob(tuple1[0]-1, tuple1[1]-1)
            if mob.hp < mob.origin_hp:
                min_h = int(mob.origin_hp / 16) + 1
                max_h = int(mob.origin_hp / 4)
                plus_hp = random.randint(min_h, max_h)
                if mob.hp + plus_hp > mob.origin_hp:
                    mob.hp = mob.origin_hp
                else:
                    mob.hp += plus_hp
                mob.old_hp = mob.hp

    def bloodSteal(self):           #血量偷取
        if self.hp<self.origin_hp:
            hp=random.randint(0, 2)
            if hp: self.inf.prefabTell('mdrain')
            if self.hp+hp>self.origin_hp:
                self.hp=self.origin_hp
            else:
                self.hp+=hp
    """================================================"""
    """================跟班属性=================="""
    def wander(self):       #在attackRange时可能到处乱跑，不在时追踪玩家
        target=[]
        for x in range(self.posx-1, self.posx+2):
            for y in range(self.posy-1, self.posy+2):
                target.append((x, y))
        if (self.pl.xat, self.pl.yat) in target:
            target.remove((self.pl.xat, self.pl.yat))
        choice=random.choice(target)
        self.tem_x1, self.tem_y1=choice
        self.canWalk()

    def knockBack(self):
        dx=self.posx-self.pl.xat
        dy=self.posy-self.pl.yat
        self.tem_x1=dx+self.posx
        self.tem_y1=dy+self.posy
        self.canWalk(True)      #击退判断
    """========================================="""
    """================自动更新函数================"""
    def attackMob(self, x, y):     #非主动地攻击周围怪物
        choices=[[0, 1, 2], [0.6, 0.35, 0.05]]
        hit=random.choices(choices[0], choices[1])[0]
        if self.pool.mob_pool[ (x, y) ].hp-hit>0:
            self.pool.mob_pool[ (x, y) ].hp-=hit
            self.inf.moreArg("servantA", [self.name, self.pool.mob_pool[ (x, y) ].name, hit])
        else:
            self.pool.mob_pool[ (x, y) ].hp=0
            self.inf.moreArg("servantK", [self.name, self.pool.mob_pool[(x, y)].name])

    #怪物debuff自动更新
    def statusUpdate(self):
        if self.status[1]:      #法术中毒效果
            if self.status[1]%2:
                self.hp-=2
            self.status[1]-=1
        if self.status[2]:      #恐惧效果
            self.aggressive=False
            if self.status[2]==1:       #恢复效果：注意原来是中立的怪物被击中后会变成不中立的怪物
                self.aggressive=True
            self.status[2]-=1
        if self.status[3]:          #祖咒效果
            if self.status[3]==1:
                self.defence+=7
                self.magic+=7
            self.status[3]-=1
        if self.status[4]:      #冰冻效果
            if self.status[4]==1:
                self.speed+=10
            self.status[4]-=1
        if self.status[5]:      #物理攻击中毒
            if not self.status[5] %3:
                self.hp-=1
            self.status[5] -= 1
        if self.status[6]:      #眩晕
            self.status[6] -= 1

    """==============================================
    ++++++++++++++++++++++怪物行为+++++++++++++++++++++
    ================================================"""
    def _chase(self):
        step = self.stp.steps()
        while step > 0:
            step -= 1
            if not (self.posx, self.posy) in self.pl.getAttackRange(): self.chase_player(self.getpos())

    def _attack(self):
        step = self.stp.steps()
        while step > 0:
            step -= 1
            self.attack_player()

    def _flee(self):
        step = self.stp.steps()
        while step > 0:
            step -= 1
            self.chase_player(self.getpos(), 1)

    def _tpFlee(self):
        step = self.stp.steps()
        if step > 0:  # 一次传送两下没有意义
            self.inf.prefabTell('mtp', self.name)
            #self.pool.setChar(self.posx, self.posy, -1)
            self.posx, self.posy = self.mons_portal()
           # self.pool.setChar(self.posx, self.posy, self.ID)

    def _summon(self):
        step = self.stp.steps()
        while step > 0:
            step -= 1
            if (self.ID == 0 or self.ID == 2) and self.hp > 5:  # 史莱姆的分裂
                self.hp = int(self.hp / 2)
                self.origin_hp = self.hp
                self.pool.more_mob(ctr=(self.posx, self.posy), radius=4, ID=self.ID, flag=True, hp=self.hp)
                self.inf.prefabTell('slime', self.name)
            elif self.ID > 2:
                self.pool.more_mob(ctr=(self.posx, self.posy), radius=4, ID=self.pool.summon_dict[self.ID],
                                   flag=True)  # 召唤标准写法
                self.inf.prefabTell('msummon', back=self.name)

    def _selfHeal(self):
        step = self.stp.steps()
        while step > 0:
            self.inf.prefabTell('mcure', self.name)
            step -= 1
            self.heal()

    def _longRange(self):
        step = self.stp.steps()
        while step > 0:  # 远程攻击
            step -= 1
            self.attack_player()

    def _wander(self):
        step = self.stp.steps()
        while step > 0:
            step -= 1
            if self.servant:
                tuple1 = self.pool.getNearBy(self.posx, self.posy)
            else:
                tuple1 = None
            if tuple1:  # 出现空元组时直接wander
                x, y = tuple1[0] - 1, tuple1[1] - 1
                if (x, y) and (x, y) != (self.posx, self.posy):
                    self.attackMob(x, y)  # 怪物攻击
                else:
                    self.wander()
            else:
                self.wander()

    def _getKnocked(self):
        self.knockBack()
        self.knocked = False
        self.inf.prefabTell('mback', back=self.name)

    def _getTped(self):
        self.posx, self.posy = self.mons_portal()
        self.teleported = False
        self.inf.prefabTell('stare', self.name)

    def _shamanHeal(self):
        self.shamanHeal()
        self.inf.prefabTell('shaman')

    def _bossSummon(self):
        self.pool.more_mob((self.posx, self.posy), ID=42, flag=True)  # 召唤暴狼
        self.pool.more_mob((self.posx, self.posy), ID=32, flag=True)  # 召唤地精精英
        self.inf.prefabTell('msummon', back=self.name)











        
