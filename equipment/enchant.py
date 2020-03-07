#-*-coding:utf-8-*-

import random


class EnchantItem:
    def __init__(self):
        self.ptr=None
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'ae', 'ao', 'au', 'ei', 'eo', 'eu', 'ea', 'ee', 'io', 'ia', 'ua', 'ue', 'ui',
                  'uo', 'oa', 'oe', 'oi', 'oy', 'oo', 'ay', 'ey', 'ù', 'è', 'ö', 'ä', 'ü', 'ì', 'à', 'ŭ', 'uh']
        # 通用辅音：
        self.consos = ['b', 'c', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'y', 'th', 'ch', 'sh', 'ph',
                  'ly', 'lz', 'st', 'ty', 'ky', 'fy', 'dy', 'by', 'my', 'ny', 'sy', 'gy', 'zy', 'py', 'phy', 'hy', 'sk', 'sp', 'ĉ']
        # 不在结尾：
        self.cap_con = ['gh', 'sch', 'dh', 'kh', 'bh', 'br', 'pr', 'dr', 'wh', 'lr', 'fr', 'cr', 'gr', 'kr', 'tr', 'pl', 'bl', 'cl', 'sl', 'str', 'fl']
        # 只在中间
        self.mid_con = ['pp', 'bb', 'tl', 'tt', 'gg', 'cc', 'dd', 'mm', 'dl', 'pch', 'psh', 'nm', 'cd', 'dc', 'sc', 'nstr', 'mstr',
                   'shm', 'chm', 'rpr', 'ndl', 'nc', 'mc', 'rs', 'ls', 'rbl', 'mbl', 'nbl', 'lc', 'rv', 'lv', 'dg',  'xc']
        # 不在开头
        self.end_con = ['mth', 'nth', 'gth', 'nch', 'mn', 'nt', 'rp', 'ng', 'ct', 'mp', 'lg', 'lt', 'rt', 'ss', 'll', 'ff',
                   'nn', 'nk', 'mk', 'rch', 'kk', 'pt', 'gn', 'nd', 'rr', 'rn', 'rm', 'rl', 'thm', 'rb', 'mb', 'x', 'rk', 'rc', 'nf', 'rd']
        self.weaponTag={1:'This will set fire on your enemies', 2:'This can drain the blood of your enemies',
                        3:'Your enemies will be stunned by this', 4:'Your enemies will be knocked back',5:'This weapon absorbs the sorcery of chaos',
                        6:'Your enemies will be frozen by this', 7:'The weapon can poison your enemies',
                        8:'This can breach the armor of your enemies', 9:'This offers penetrate attack to multiple enemies',
                        10:'This offers splash damage to multiple enemies', 11:'This will shed light on your path',
                        12:'This will blind your eyes, makes it more vulnerable to the dark.'}
        self.lvl2num=[(1,1), (1,1), (1,1), (1,2), (1,2), (1, 2), (1,2)]
        self.inf=None

    def enchant(self, item):
        if not item.label:
            if not (item.lvl+item.enchant_lvl>10):
                equipped = False
                if item.equipped:
                    self.ptr.deEquip(item)
                    equipped=True
                if item.name_set:
                    item.name_set=False
                item.lvl+=1
                item.enchant_lvl+=1
                if item.tag != 'Wand':
                    if item.enchant_lvl<6:      #小于六级是有prefix的，但是六级之后没有
                        item.deSetAttri()
                    else:
                        item.prefix.clear()
                        item.name=item.basic_name+' '+self.lvl6Name()
                        self.setUpAttri(item)           #给予特殊攻击能力
                    self.newPrefix(item)
                    item.formName()
                    item.setUpAttri()
                    item.getDesc()
                    item.count=1            #合为一体
                    item.name_set=True
                else:   #充能
                    item.energy=12
                #回到loop1
                if equipped:            #已装备武器的赋魔会自动卸下并重装
                    self.ptr.Equip(item)
                return True
            else:
                self.inf.prefabTell('lvl6x')
                self.inf.prefabTell('no')
                return False
        else:
            self.inf.prefabTell('no')
            return False

    def deEnchant(self, item):      #大于5级的装备也是不可以被退魔的
        if not item.label and item.tag != 'Wand':
            if not (item.lvl<=1 or item.enchant_lvl<1 or item.enchant_lvl>5):
                equipped = False
                if item.equipped:
                    self.ptr.deEquip(item)
                    equipped = True
                if item.name_set:
                    item.name_set=False
                item.lvl-=1
                item.enchant_lvl-=1
                item.deSetAttri()
                self.newPrefix(item)
                item.formName()
                item.setUpAttri()
                item.getDesc()
                item.name_set=True
                #回到loop1
                if equipped:            #已装备武器的退魔会自动卸下并重装
                    self.ptr.Equip(item)
                return True
            else:
                self.inf.prefabTell('lvl6-') if item.lvl==6 else self.inf.prefabTell('lvl0x')
                self.inf.prefabTell('no')
                return False
        else:
            self.inf.prefabTell('no')
            return False

    @staticmethod
    def newPrefix(item):          #直接覆盖的方式
        if item.lvl==1:
            pre=random.choices([-1, 0], k=1)
            item.prefix=pre
        elif item.lvl==2:
            kk=random.choices([1,2])[0]
            item.prefix=random.sample(range(8, 22), k=kk)
        elif item.lvl==3:
            kk=random.choices([1,2,3], [0.3, 0.6, 0.1])[0]
            item.prefix=random.sample(range(22, 29), k=kk)
        elif item.lvl==4:
            kk=random.choices([1,2,3], [0.25, 0.65, 0.1])[0]
            item.prefix=random.sample(range(29, 35), k=kk)
        elif item.lvl==5:
            kk=random.choices([1,2,3], [0.2, 0.7, 0.1])[0]
            item.prefix=random.sample(range(35, 38), k=kk)
        elif item.lvl==6:
            item.prefix.append(random.choice(range(100, 106)))
        else:           #成色较差物品
            item.prefix=random.choices(range(1, 8), k=1)

    def newPrefix2(self, item):
        if not item.prefix:                                                 #没有词缀则设置
            mini, maxi=self.lvl2num[item.lvl]
            num=random.randint(mini, maxi)                      #词缀数量
            kinds=random.sample(range(9), k=num)
            for kind in kinds:
                item.prefix.append(kind*7+item.lvl)
        else:
            if item.lvl<6:                                                      #同阶词缀升级
                length=len(item.prefix)
                for i in range(length):
                    item.prefix[length]+=1
                    


            





    def randomEnchant(self, item):      #给生成的物体进行随机附魔
        #一般是给怪物掉落物或者非背包内生成物品进行使用
        if not item.label:
            weight = [0.1, 0.46, 0.2, 0.12, 0.095, 0.02, 0.005]
            tem = [-1, 0, 1, 2, 3, 4, 5]
            if item.name_set:
                item.name_set=False
            item.lvl=item.enchant_lvl=random.choices(tem, weight)[0]
            if item.lvl==-1:        #成色差的武器
                item.enchant_lvl+=1
            if item.tag=='Wand':        #给法杖附魔只是为它加能量
                item.lvl+=1
            else:
                self.enchant(item)

    #第六级物品名称
    def lvl6Name(self):
        name = []
        l=random.randint(2, 3)
        start = random.randint(0, 1)
        for i in range(l):
            if i % 2 == start:
                p = random.choice(self.vowels)
            else:
                if i == 0:
                    choice = random.choice([0, 1])
                    if choice: p = random.choice(self.consos)
                    else: p = random.choice(self.cap_con)
                elif i == l - 1:
                    choice = random.choice([0, 1])
                    if choice: p = random.choice(self.consos)
                    else: p = random.choice(self.end_con)
                else:
                    choice = random.choice([0, 1, 2, 3])
                    if choice == 0: p = random.choice(self.consos)
                    elif choice == 1: p = random.choice(self.cap_con)
                    elif choice == 2: p = random.choice(self.mid_con)
                    else: p = random.choice(self.end_con)
            name.append(p)
        d = "'"+(''.join(name)).capitalize()+"'"
        return d

    def setUpAttri(self, item):                 #给予特殊攻击能力
        if item.tag in {'Right', 'Dual'}:       #主要是近身攻击武器和双手弓
            num=random.choices([0, 1, 2], [0.005, 0.7, 0.295])[0]
            item.attr=list(set(item.attr)|set(random.sample(self.weaponTag.keys(), k=num)))
        elif item.tag not in {'Ring', 'Feet'}:
            num = random.choices([0, 1, 2], [0.005, 0.7, 0.295])[0]
            lst=list()
            lst.append(random.choice(range(13, 17)))
            lst.append(random.choice(range(17, 21)))
            lst.append(random.choice(range(21, 25)))
            lst.append(random.choice(range(25, 29)))
            lst.append(random.choice(range(29, 33)))
            item.attr =list(set(item.attr)|set(random.sample(lst, k=num)))




            
            
            
