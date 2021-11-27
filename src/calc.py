#!/usr/bin/env python3
#-*-coding:utf-8-*-

import numpy as np
import random, sys

class Calc:
    def __init__(self):
        self.a = -1.84266 * (10 ** -6)
        self.b = 0.000706326
        self.c = 0.05583372942
        self.d = 0.836691169
        self.mobChance={-20:80, -15:70, -10:60, -5:50, 0:45, 5:40, 10:45, 15:30,
                        20:25, 25:20, 30:15, 35:10, 65535:8}
        self.plyChance={-20:60, -10: 70, 0:80, 10:90, 20:95, 27:98, 65535:100}
        self.mobIncre={-15:[[4, 3, 2], [0.05, 0.65, 0.3]], -10:[[3, 2, 1], [0.05, 0.45, 0.5]],
                       -5:[[2, 1],[0.1, 0.9]], 65535:[[2, 1], [0.01, 0.99]]}
        self.plyIncre={-10:[[2, 1], [0.4, 0.6]], -5:[[2, 1], [0.6, 0.4]], 0:[[2, 1], [0.9, 0.1]], 5:[[3, 2, 1], [0.2, 0.7, 0.1]],
                       15:[[3, 2, 1], [0.4, 0.5, 0.1]], 25:[[4, 3, 2, 1], [0.15, 0.45, 0.3, 0.1]], 35:[[4, 3, 2, 1], [0.25, 0.45, 0.2, 0.1]],
                       45:[[5, 4, 3, 2, 1], [0.15, 0.4, 0.3, 0.1, 0.05]], 65536:[[5, 4, 3, 2, 1], [0.25, 0.35, 0.3, 0.05, 0.05]]}

    '''================玩家攻击怪物公式================='''
    def damageOnMob(self, mob, player_attack, player_speed):
        #传入参数：mob, 需要mob的defence, speed
        m_def, m_spd=mob.defence, mob.speed
        p_atk, p_spd=player_attack, player_speed
        basic_hit=self.basic_dmg(p_atk)         #基本伤害值的确定是根据玩家的攻击
        incre=self.increment(m_def, p_atk)              
        decre=self.decrement(m_def, p_atk, m_spd, p_spd)
        maxi=max(basic_hit+incre, 1)       #伤害的最大值最小值与其他参数有关
        mini=max(basic_hit-decre, 0)        #伤害不可能为负值
        for k, v in self.plyChance.items():
            if p_spd-m_spd>k:
                if self.binChoice(v):
                    hit = random.randint(mini, maxi)
                else:
                    hit = 0
                return hit
        return 0
            
    def increment(self, mob_def, ply_atk):        #伤害增量
        for k, v in self.plyIncre.items():
            if ply_atk-mob_def<=k:
                incre=random.choices(*v)[0]
                incre+=random.choices([-1, 0, 1],[0.01, 0.8, 0.19])[0]
                return incre
        return 1

    def decrement(self, mob_def, ply_atk, mob_spd, ply_spd):          #伤害减量与速度也有关
        if ply_spd>=mob_spd:
            spd_decre=0
        else:
            spd_decre=np.sqrt(mob_spd-ply_spd)
        decre=spd_decre+self.def_decre(mob_def, ply_atk)
        return int(decre)

    '''========================================'''
    '''==============怪物攻击玩家公式==============='''
    def mobAttackHit(self, mob, player_def, player_spd):
        m_atk, m_spd=mob.attack, mob.speed
        p_def, p_spd=player_def, player_spd
        basic_hit=self.basic_dmg(m_atk)-1
        maxi=basic_hit+self.mob_incre(p_def, m_atk)
        mini=basic_hit-self.mob_decre(p_def, m_atk, p_spd, m_spd)
        mini=max(mini, 0)
        maxi=max(maxi, 1)
        for k,v in self.mobChance.items():
            if p_spd-m_spd<=k:
                chance=v
                hitJudge=random.choices([1, 0], [0.7, 0.3])[0]
                if self.binChoice(chance) and hitJudge:
                    hit = random.randint(mini, maxi)
                else:
                    hit = 0
                return hit
        return 0
            
    def mob_incre(self, ply_def, mob_atk):
        incre=1
        for k, v in self.mobIncre.items():
            if ply_def-mob_atk<=k:
                incre=random.choices(*v)[0]
        decre=random.choices([-1, 0], [0.9, 0.1])[0]
        return incre+decre


    def mob_decre(self, ply_def, mob_atk, ply_spd, mob_spd):          #伤害减量与速度也有关
        if mob_spd>=ply_spd:
            spd_decre=0
        else:
            spd_decre=np.sqrt(ply_spd-mob_spd)
        decre=spd_decre+self.def_decre(ply_def, mob_atk)
        return int(decre)

    '''========================================='''
    '''===============通用公式===================='''
    @staticmethod
    def binChoice(sucess_odd, power=1):     #参数sucess_odd是成功概率，power是选择指数
        #power=1, 为百分概率，精度为1%， 2时为0.1%精度
        basic=10*(10**power)
        range_hold=int(sucess_odd*(10**(power-1)))
        judge=random.randint(1, basic)
        if judge<=range_hold:
            return True
        else:
            return False

    def basic_dmg(self, atk):
        res=self.a*(atk**3)+self.b*(atk**2)+self.c*atk+self.d+1
        return int(res)

    #防御伤害减少
    @staticmethod
    def def_decre(_def, _atk):
        if _def>_atk+6:
            decre=int((_def-_atk)/2)
        elif _atk>_def+40:
            decre=1
        elif _atk>_def+20:
            decre=2
        elif _atk>_def+10:
            decre=3
        else:
            decre=4
        return decre
    '''=================EXP-LEVEL关系公式======================'''
    @staticmethod
    def getExp(level):
        if level<100:
            l=level
            return 2*l*l+l+9
        else:
            return sys.maxsize

    @staticmethod
    def fixChoice(tag):           #怪物特殊攻击概率
        if tag==1:
            choices=[[0, 1],[0.7, 0.3]]
            return random.choices(choices[0], choices[1])[0]
        elif tag==2:
            choices=[[0, 1],[0.75, 0.25]]
            return random.choices(choices[0], choices[1])[0]
        elif tag==3:
            choices=[[0, 1],[0.6, 0.4]]
            return random.choices(choices[0], choices[1])[0]
        else :
            return random.choice([0, 1])

    @staticmethod
    def multiChoice():             #怪物混沌魔法概率
        choices=[[5, 4, 3, 2, 1, 0], [0.2, 0.05, 0.05, 0.05, 0.2, 0.45]]
        return random.choices(*choices)[0]

    #魔法伤害
    def magicOnMob(self, mob, p_mgc, p_spd):
        m_mgc, m_spd=mob.magic, mob.speed
        hit=max(self.basic_dmg(p_mgc)-1, 1)
        incre=int(np.log2(hit))+random.choices([-1, 0, 1, 2, 3], [0.1, 0.35, 0.4, 0.1, 0.05])[0]
        incre=max(incre, 1)
        decre=self.mobMgcDecre(m_mgc)
        maxi=max(hit+incre, 1)
        mini=max(hit-decre, 0)
        for k, v in self.plyChance.items():
            if p_spd-m_spd>k:
                if self.binChoice(v):
                    real_hit = random.randint(mini, maxi)
                else:
                    real_hit = 0
                return real_hit
        return 0

    @staticmethod
    def mobMgcDecre(mob_mgc):
        decre=int(np.log2(max(mob_mgc, 1))/2)+random.choices([-1, 0, 1], [0.2, 0.4, 0.4])[0]
        decre=max(decre, 1)
        return decre

    def magicOnPly(self, mob, player_mgc, player_spd):
        m_atk, m_spd = mob.magic, mob.speed
        p_mgc, p_spd = player_mgc, player_spd
        basic_hit = self.basic_dmg(m_atk) - 1
        maxi = basic_hit + int(np.log2(max(basic_hit, 1)))+random.choices([0, 1], [0.95, 0.05])[0]-int(np.log10(max(p_mgc, 1)))
        mini = basic_hit - self.mobMgcDecre(p_mgc)
        mini = max(mini, 0)
        maxi = max(maxi, 1)
        for k, v in self.mobChance.items():
            if p_spd - m_spd <= k:
                chance = v
                hitJudge = random.choices([1, 0], [0.7, 0.3])[0]
                if self.binChoice(chance) and hitJudge:
                    hit = random.randint(mini, maxi)
                else:
                    hit = 0
                return hit
        return 0
        
        
        
        
        
            
